using AutoMapper;
using TiendaGo.DTOs.Ventas;
using TiendaGo.Models;

namespace TiendaGo.Services;

public class VentaService : IVentaService
{
    private readonly Supabase.Client _supabase;
    private readonly IMapper _mapper;

    public VentaService(Supabase.Client supabase, IMapper mapper)
    {
        _supabase = supabase;
        _mapper = mapper;
    }

    public async Task<VentaResponse> RegistrarVentaAsync(VentaRequest request)
    {
        if (request.Detalles == null || !request.Detalles.Any())
        {
            throw new ArgumentException("La venta debe contener al menos un producto.");
        }

        // 1. Validar que el turno de caja esté abierto
        var turnoRes = await _supabase.From<TurnoCaja>()
            .Where(t => t.IdTurno == request.IdTurno)
            .Get();

        var turno = turnoRes.Models.FirstOrDefault();
        if (turno == null || turno.EstadoTurno != "Abierto")
        {
            throw new InvalidOperationException($"El turno #{request.IdTurno} no existe o no se encuentra Abierto para procesar ventas.");
        }

        // 2. Validar existencias de productos y calcular importes
        decimal subtotalVenta = 0m;
        var listaDetallesProcesados = new List<(Producto producto, int cantidad, decimal precioUnitario, decimal subtotalLinea)>();

        foreach (var d in request.Detalles)
        {
            if (d.Cantidad <= 0)
            {
                throw new ArgumentException($"La cantidad para el producto ID {d.IdProducto} debe ser mayor a 0.");
            }

            var prodRes = await _supabase.From<Producto>()
                .Where(p => p.IdProducto == d.IdProducto)
                .Get();

            var producto = prodRes.Models.FirstOrDefault();
            if (producto == null || !producto.EstadoActivo)
            {
                throw new InvalidOperationException($"El producto ID {d.IdProducto} no existe o está inactivo.");
            }

            if (producto.StockActual < d.Cantidad)
            {
                throw new InvalidOperationException($"Stock insuficiente para '{producto.NombreProducto}'. Disponible: {producto.StockActual}, Solicitado: {d.Cantidad}.");
            }

            var precioUnitario = d.PrecioUnitarioHistorico ?? producto.PrecioVenta;
            var subtotalLinea = precioUnitario * d.Cantidad;
            subtotalVenta += subtotalLinea;

            listaDetallesProcesados.Add((producto, d.Cantidad, precioUnitario, subtotalLinea));
        }

        var totalVenta = subtotalVenta;
        if (request.MontoRecibido < totalVenta)
        {
            throw new InvalidOperationException($"El monto recibido (${request.MontoRecibido:F2}) es menor al total de la venta (${totalVenta:F2}).");
        }

        var cambioEntregado = request.MontoRecibido - totalVenta;
        var numeroTicket = $"TCK-{DateTimeOffset.UtcNow.Ticks.ToString()[^8..]}";

        // 3. Registrar encabezado de Venta
        var venta = new Venta
        {
            IdTurno = request.IdTurno,
            IdUsuario = request.IdUsuario,
            IdMetodoPago = request.IdMetodoPago,
            NumeroTicket = numeroTicket,
            FechaHora = DateTimeOffset.UtcNow,
            Subtotal = subtotalVenta,
            TotalIva = 0m,
            TotalVenta = totalVenta,
            MontoRecibido = request.MontoRecibido,
            CambioEntregado = cambioEntregado,
            EstadoVenta = "Completada"
        };

        var ventaInsertRes = await _supabase.From<Venta>().Insert(venta);
        var ventaRegistrada = ventaInsertRes.Models.FirstOrDefault() ?? venta;

        // 4. Registrar detalles de venta y descontar stock de inventario
        var detallesResponseList = new List<DetalleVentaResponse>();

        foreach (var item in listaDetallesProcesados)
        {
            var detalle = new DetalleVenta
            {
                IdVenta = ventaRegistrada.IdVenta,
                IdProducto = item.producto.IdProducto,
                Cantidad = item.cantidad,
                PrecioUnitarioHistorico = item.precioUnitario,
                SubtotalLinea = item.subtotalLinea
            };

            var detInsertRes = await _supabase.From<DetalleVenta>().Insert(detalle);
            var nuevoDetalle = detInsertRes.Models.FirstOrDefault() ?? detalle;

            // Actualizar stock de producto en EF / Supabase
            item.producto.StockActual -= item.cantidad;
            await _supabase.From<Producto>()
                .Where(p => p.IdProducto == item.producto.IdProducto)
                .Update(item.producto);

            detallesResponseList.Add(new DetalleVentaResponse
            {
                IdDetalle = nuevoDetalle.IdDetalle,
                IdVenta = ventaRegistrada.IdVenta,
                IdProducto = item.producto.IdProducto,
                NombreProducto = item.producto.NombreProducto,
                CodigoSku = item.producto.CodigoSku,
                Cantidad = item.cantidad,
                PrecioUnitarioHistorico = item.precioUnitario,
                SubtotalLinea = item.subtotalLinea
            });
        }

        // 5. Acumular venta en el turno de caja correspondiente
        var metodoPagoRes = await _supabase.From<MetodoPago>()
            .Where(m => m.IdMetodoPago == request.IdMetodoPago)
            .Get();

        var metodoPago = metodoPagoRes.Models.FirstOrDefault();
        var esEfectivo = metodoPago == null || string.Equals(metodoPago.NombreMetodo, "Efectivo", StringComparison.OrdinalIgnoreCase) || request.IdMetodoPago == 1;

        if (esEfectivo)
        {
            turno.TotalVentasEfectivo += totalVenta;
        }
        else
        {
            turno.TotalVentasDigital += totalVenta;
        }

        await _supabase.From<TurnoCaja>()
            .Where(t => t.IdTurno == turno.IdTurno)
            .Update(turno);

        // 6. Mapear y devolver respuesta
        await CargarRelacionesVentaAsync(ventaRegistrada);
        var response = _mapper.Map<VentaResponse>(ventaRegistrada);
        response.Detalles = detallesResponseList;

        return response;
    }

    public async Task<VentaResponse?> ObtenerPorIdAsync(long idVenta)
    {
        var res = await _supabase.From<Venta>()
            .Where(v => v.IdVenta == idVenta)
            .Get();

        var venta = res.Models.FirstOrDefault();
        if (venta == null) return null;

        await CargarRelacionesVentaAsync(venta);
        var response = _mapper.Map<VentaResponse>(venta);
        response.Detalles = await ObtenerDetallesVentaAsync(idVenta);

        return response;
    }

    public async Task<IEnumerable<VentaResponse>> ObtenerPorTurnoAsync(long idTurno)
    {
        var res = await _supabase.From<Venta>()
            .Where(v => v.IdTurno == idTurno)
            .Get();

        var ventas = res.Models.OrderByDescending(v => v.FechaHora).ToList();
        var resultado = new List<VentaResponse>();

        var usuariosDict = await ObtenerDiccionarioUsuariosAsync();
        var metodosDict = await ObtenerDiccionarioMetodosPagoAsync();

        foreach (var v in ventas)
        {
            if (usuariosDict.TryGetValue(v.IdUsuario, out var usr)) v.Usuario = usr;
            if (metodosDict.TryGetValue(v.IdMetodoPago, out var mp)) v.MetodoPago = mp;

            var dto = _mapper.Map<VentaResponse>(v);
            dto.Detalles = await ObtenerDetallesVentaAsync(v.IdVenta);
            resultado.Add(dto);
        }

        return resultado;
    }

    public async Task<bool> AnularVentaAsync(long idVenta)
    {
        var res = await _supabase.From<Venta>()
            .Where(v => v.IdVenta == idVenta)
            .Get();

        var venta = res.Models.FirstOrDefault();
        if (venta == null || venta.EstadoVenta == "Anulada") return false;

        venta.EstadoVenta = "Anulada";
        await _supabase.From<Venta>()
            .Where(v => v.IdVenta == idVenta)
            .Update(venta);

        // Restablecer inventarios
        var detalles = await _supabase.From<DetalleVenta>()
            .Where(d => d.IdVenta == idVenta)
            .Get();

        foreach (var d in detalles.Models)
        {
            var pRes = await _supabase.From<Producto>()
                .Where(p => p.IdProducto == d.IdProducto)
                .Get();

            var prod = pRes.Models.FirstOrDefault();
            if (prod != null)
            {
                prod.StockActual += d.Cantidad;
                await _supabase.From<Producto>()
                    .Where(p => p.IdProducto == prod.IdProducto)
                    .Update(prod);
            }
        }

        return true;
    }

    private async Task CargarRelacionesVentaAsync(Venta venta)
    {
        if (venta.IdUsuario != Guid.Empty)
        {
            var uRes = await _supabase.From<Usuario>().Where(u => u.IdUsuario == venta.IdUsuario).Get();
            venta.Usuario = uRes.Models.FirstOrDefault();
        }

        if (venta.IdMetodoPago > 0)
        {
            var mpRes = await _supabase.From<MetodoPago>().Where(m => m.IdMetodoPago == venta.IdMetodoPago).Get();
            venta.MetodoPago = mpRes.Models.FirstOrDefault();
        }
    }

    private async Task<List<DetalleVentaResponse>> ObtenerDetallesVentaAsync(long idVenta)
    {
        var res = await _supabase.From<DetalleVenta>()
            .Where(d => d.IdVenta == idVenta)
            .Get();

        var productosDict = await ObtenerDiccionarioProductosAsync();
        var lista = new List<DetalleVentaResponse>();

        foreach (var d in res.Models)
        {
            productosDict.TryGetValue(d.IdProducto, out var prod);
            d.Producto = prod;
            lista.Add(_mapper.Map<DetalleVentaResponse>(d));
        }

        return lista;
    }

    private async Task<Dictionary<Guid, Usuario>> ObtenerDiccionarioUsuariosAsync()
    {
        var res = await _supabase.From<Usuario>().Get();
        return res.Models.ToDictionary(u => u.IdUsuario, u => u);
    }

    private async Task<Dictionary<long, MetodoPago>> ObtenerDiccionarioMetodosPagoAsync()
    {
        var res = await _supabase.From<MetodoPago>().Get();
        return res.Models.ToDictionary(m => m.IdMetodoPago, m => m);
    }

    private async Task<Dictionary<long, Producto>> ObtenerDiccionarioProductosAsync()
    {
        var res = await _supabase.From<Producto>().Get();
        return res.Models.ToDictionary(p => p.IdProducto, p => p);
    }
}
