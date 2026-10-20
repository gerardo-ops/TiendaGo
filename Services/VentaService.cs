using AutoMapper;
using Microsoft.EntityFrameworkCore;
using TiendaGo.DTOs.Ventas;
using TiendaGo.Models;

namespace TiendaGo.Services;

public class VentaService : IVentaService
{
    private readonly TiendaGoDbContext? _context;
    private readonly Supabase.Client? _supabase;
    private readonly IMapper _mapper;

    public VentaService(TiendaGoDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public VentaService(Supabase.Client supabase, IMapper mapper)
    {
        _supabase = supabase;
        _mapper = mapper;
    }

    [Microsoft.Extensions.DependencyInjection.ActivatorUtilitiesConstructor]
    public VentaService(TiendaGoDbContext context, IMapper mapper, Supabase.Client? supabase = null)
    {
        _context = context;
        _mapper = mapper;
        _supabase = supabase;
    }

    public async Task<VentaResponse> RegistrarVentaAsync(VentaRequest request)
    {
        if (request.Detalles == null || !request.Detalles.Any())
        {
            throw new ArgumentException("La venta debe contener al menos un producto.");
        }

        if (_context != null)
        {
            // 1. Validar que el turno de caja esté abierto
            var turno = await _context.TurnosCaja
                .Include(t => t.IdUsuarioNavigation)
                .FirstOrDefaultAsync(t => t.IdTurno == request.IdTurno);

            if (turno == null || turno.EstadoTurno != "Abierto")
            {
                throw new InvalidOperationException($"El turno #{request.IdTurno} no existe o no se encuentra Abierto para procesar ventas.");
            }

            // 2. Validar existencias de productos y calcular importes
            decimal totalVenta = 0m;
            var listaDetallesProcesados = new List<(Productos producto, int cantidad, decimal precioUnitario, decimal subtotalLinea)>();

            foreach (var d in request.Detalles)
            {
                if (d.Cantidad <= 0)
                {
                    throw new ArgumentException($"La cantidad para el producto ID {d.IdProducto} debe ser mayor a 0.");
                }

                var producto = await _context.Productos.FirstOrDefaultAsync(p => p.IdProducto == d.IdProducto);
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
                totalVenta += subtotalLinea;

                listaDetallesProcesados.Add((producto, d.Cantidad, precioUnitario, subtotalLinea));
            }

            if (request.MontoRecibido < totalVenta)
            {
                throw new InvalidOperationException($"El monto recibido (${request.MontoRecibido:F2}) es menor al total de la venta (${totalVenta:F2}).");
            }

            var totalIva = Math.Round(totalVenta - (totalVenta / 1.13m), 2);
            var subtotalSinIva = totalVenta - totalIva;
            var cambioEntregado = request.MontoRecibido - totalVenta;
            var numeroTicket = $"TCK-{DateTimeOffset.UtcNow.Ticks.ToString()[^8..]}";

            // 3. Registrar encabezado de Venta
            var idUsuarioValido = request.IdUsuario != Guid.Empty ? request.IdUsuario : turno.IdUsuario;

            var venta = new Ventas
            {
                IdTurno = request.IdTurno,
                IdUsuario = idUsuarioValido,
                IdMetodoPago = request.IdMetodoPago,
                NumeroTicket = numeroTicket,
                FechaHora = DateTime.UtcNow,
                Subtotal = subtotalSinIva,
                TotalIva = totalIva,
                TotalVenta = totalVenta,
                MontoRecibido = request.MontoRecibido,
                CambioEntregado = cambioEntregado,
                EstadoVenta = "Completada"
            };

            _context.Ventas.Add(venta);
            await _context.SaveChangesAsync();

            // 4. Registrar detalles y descontar inventario
            var detallesResponseList = new List<DetalleVentaResponse>();
            foreach (var item in listaDetallesProcesados)
            {
                var detalle = new DetallesVenta
                {
                    IdVenta = venta.IdVenta,
                    IdProducto = item.producto.IdProducto,
                    Cantidad = item.cantidad,
                    PrecioUnitarioHistorico = item.precioUnitario,
                    SubtotalLinea = item.subtotalLinea
                };

                _context.DetallesVenta.Add(detalle);
                item.producto.StockActual -= item.cantidad;

                detallesResponseList.Add(new DetalleVentaResponse
                {
                    IdDetalle = detalle.IdDetalle,
                    IdVenta = venta.IdVenta,
                    IdProducto = item.producto.IdProducto,
                    NombreProducto = item.producto.NombreProducto,
                    CodigoSku = item.producto.CodigoSku,
                    Cantidad = item.cantidad,
                    PrecioUnitarioHistorico = item.precioUnitario,
                    SubtotalLinea = item.subtotalLinea
                });
            }

            // 5. Acumular venta en el turno de caja
            var metodoPago = await _context.MetodosPago.FirstOrDefaultAsync(m => m.IdMetodoPago == request.IdMetodoPago);
            var esEfectivo = metodoPago == null || string.Equals(metodoPago.NombreMetodo, "Efectivo", StringComparison.OrdinalIgnoreCase) || request.IdMetodoPago == 1;

            if (esEfectivo)
            {
                turno.TotalVentasEfectivo += totalVenta;
            }
            else
            {
                turno.TotalVentasDigital += totalVenta;
            }

            await _context.SaveChangesAsync();

            var usuario = await _context.Usuarios.FirstOrDefaultAsync(u => u.IdUsuario == idUsuarioValido);

            return new VentaResponse
            {
                IdVenta = venta.IdVenta,
                IdTurno = venta.IdTurno,
                IdUsuario = venta.IdUsuario,
                NombreUsuario = usuario?.NombreCompleto ?? turno.IdUsuarioNavigation?.NombreCompleto ?? "Usuario",
                IdMetodoPago = venta.IdMetodoPago,
                NombreMetodoPago = metodoPago?.NombreMetodo ?? (request.IdMetodoPago == 1 ? "Efectivo" : "Digital"),
                NumeroTicket = venta.NumeroTicket,
                FechaHora = DateTimeOffset.UtcNow,
                Subtotal = venta.Subtotal,
                TotalIva = venta.TotalIva,
                TotalVenta = venta.TotalVenta,
                MontoRecibido = venta.MontoRecibido,
                CambioEntregado = venta.CambioEntregado,
                EstadoVenta = venta.EstadoVenta,
                Detalles = detallesResponseList
            };
        }

        if (_supabase == null)
        {
            throw new InvalidOperationException("No se ha configurado un proveedor de datos para VentaService.");
        }

        // 1. Validar que el turno de caja esté abierto (Supabase)
        var turnoRes = await _supabase.From<TurnoCaja>()
            .Where(t => t.IdTurno == request.IdTurno)
            .Get();

        var turnoSupabase = turnoRes.Models.FirstOrDefault();
        if (turnoSupabase == null || turnoSupabase.EstadoTurno != "Abierto")
        {
            throw new InvalidOperationException($"El turno #{request.IdTurno} no existe o no se encuentra Abierto para procesar ventas.");
        }

        // 2. Validar existencias de productos y calcular importes (Supabase)
        decimal totalVentaSupabase = 0m;
        var listaDetallesProcesadosSupabase = new List<(Producto producto, int cantidad, decimal precioUnitario, decimal subtotalLinea)>();

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
            totalVentaSupabase += subtotalLinea;

            listaDetallesProcesadosSupabase.Add((producto, d.Cantidad, precioUnitario, subtotalLinea));
        }

        if (request.MontoRecibido < totalVentaSupabase)
        {
            throw new InvalidOperationException($"El monto recibido (${request.MontoRecibido:F2}) es menor al total de la venta (${totalVentaSupabase:F2}).");
        }

        var totalIvaSupabase = Math.Round(totalVentaSupabase - (totalVentaSupabase / 1.13m), 2);
        var subtotalSinIvaSupabase = totalVentaSupabase - totalIvaSupabase;
        var cambioEntregadoSupabase = request.MontoRecibido - totalVentaSupabase;
        var numeroTicketSupabase = $"TCK-{DateTimeOffset.UtcNow.Ticks.ToString()[^8..]}";

        // 3. Registrar encabezado de Venta en Supabase
        var idUsuarioValidoSupabase = Guid.Parse("37907a7d-4609-422f-b02b-6799bb01c8f2");

        var ventaSupabase = new Venta
        {
            IdTurno = request.IdTurno,
            IdUsuario = idUsuarioValidoSupabase,
            IdMetodoPago = request.IdMetodoPago,
            NumeroTicket = numeroTicketSupabase,
            FechaHora = DateTimeOffset.UtcNow,
            Subtotal = subtotalSinIvaSupabase,
            TotalIva = totalIvaSupabase,
            TotalVenta = totalVentaSupabase,
            MontoRecibido = request.MontoRecibido,
            CambioEntregado = cambioEntregadoSupabase,
            EstadoVenta = "Completada"
        };

        Venta ventaRegistrada;
        try
        {
            var ventaInsertRes = await _supabase.From<Venta>().Insert(ventaSupabase);
            ventaRegistrada = ventaInsertRes.Models.FirstOrDefault() ?? ventaSupabase;

            if (ventaRegistrada.IdVenta <= 0)
            {
                var vCheck = await _supabase.From<Venta>().Where(v => v.NumeroTicket == numeroTicketSupabase).Get();
                if (vCheck.Models.Any())
                {
                    ventaRegistrada = vCheck.Models.First();
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[VentaService] ERROR AL INSERTAR VENTA: {ex.Message}");
            throw;
        }

        // 4. Registrar detalles de venta y descontar stock de inventario
        var detallesResponseListSupabase = new List<DetalleVentaResponse>();

        foreach (var item in listaDetallesProcesadosSupabase)
        {
            var detalle = new DetalleVenta
            {
                IdVenta = ventaRegistrada.IdVenta,
                IdProducto = item.producto.IdProducto,
                Cantidad = item.cantidad,
                PrecioUnitarioHistorico = item.precioUnitario,
                SubtotalLinea = item.subtotalLinea
            };

            DetalleVenta nuevoDetalle;
            try
            {
                var detInsertRes = await _supabase.From<DetalleVenta>().Insert(detalle);
                nuevoDetalle = detInsertRes.Models.FirstOrDefault() ?? detalle;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[VentaService] ERROR AL INSERTAR DETALLE: {ex.Message}");
                throw;
            }

            try
            {
                item.producto.StockActual -= item.cantidad;
                await _supabase.From<Producto>()
                    .Where(p => p.IdProducto == item.producto.IdProducto)
                    .Update(item.producto);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[VentaService WARNING] Error al actualizar stock: {ex.Message}");
            }

            detallesResponseListSupabase.Add(new DetalleVentaResponse
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
        try
        {
            var metodoPagoRes = await _supabase.From<MetodoPago>()
                .Where(m => m.IdMetodoPago == request.IdMetodoPago)
                .Get();

            var metodoPago = metodoPagoRes.Models.FirstOrDefault();
            var esEfectivo = metodoPago == null || string.Equals(metodoPago.NombreMetodo, "Efectivo", StringComparison.OrdinalIgnoreCase) || request.IdMetodoPago == 1;

            if (esEfectivo)
            {
                turnoSupabase.TotalVentasEfectivo += totalVentaSupabase;
            }
            else
            {
                turnoSupabase.TotalVentasDigital += totalVentaSupabase;
            }

            await _supabase.From<TurnoCaja>()
                .Where(t => t.IdTurno == turnoSupabase.IdTurno)
                .Update(turnoSupabase);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[VentaService WARNING] Error al actualizar acumulados del turno: {ex.Message}");
        }

        // 6. Mapear y devolver respuesta
        var response = new VentaResponse
        {
            IdVenta = ventaRegistrada.IdVenta,
            IdTurno = ventaRegistrada.IdTurno,
            IdUsuario = ventaRegistrada.IdUsuario,
            NombreUsuario = turnoSupabase.Usuario?.NombreCompleto ?? "Usuario",
            IdMetodoPago = ventaRegistrada.IdMetodoPago,
            NombreMetodoPago = request.IdMetodoPago == 1 ? "Efectivo" : "QR Transferencia",
            NumeroTicket = ventaRegistrada.NumeroTicket,
            FechaHora = TimeZoneHelper.ToBusinessTime(ventaRegistrada.FechaHora),
            Subtotal = ventaRegistrada.Subtotal,
            TotalIva = ventaRegistrada.TotalIva,
            TotalVenta = ventaRegistrada.TotalVenta,
            MontoRecibido = ventaRegistrada.MontoRecibido,
            CambioEntregado = ventaRegistrada.CambioEntregado,
            EstadoVenta = ventaRegistrada.EstadoVenta,
            Detalles = detallesResponseListSupabase
        };

        try
        {
            var mpRes = await _supabase.From<MetodoPago>().Where(m => m.IdMetodoPago == ventaRegistrada.IdMetodoPago).Get();
            var mp = mpRes.Models.FirstOrDefault();
            if (mp != null) response.NombreMetodoPago = mp.NombreMetodo;
        }
        catch { }

        return response;
    }

    public async Task<VentaResponse?> ObtenerPorIdAsync(long idVenta)
    {
        if (_context != null)
        {
            var venta = await _context.Ventas
                .Include(v => v.DetallesVenta)
                    .ThenInclude(d => d.IdProductoNavigation)
                .Include(v => v.IdUsuarioNavigation)
                .Include(v => v.IdMetodoPagoNavigation)
                .FirstOrDefaultAsync(v => v.IdVenta == idVenta);

            if (venta == null) return null;

            return new VentaResponse
            {
                IdVenta = venta.IdVenta,
                IdTurno = venta.IdTurno,
                IdUsuario = venta.IdUsuario,
                NombreUsuario = venta.IdUsuarioNavigation?.NombreCompleto ?? "Usuario",
                IdMetodoPago = venta.IdMetodoPago,
                NombreMetodoPago = venta.IdMetodoPagoNavigation?.NombreMetodo ?? "Efectivo",
                NumeroTicket = venta.NumeroTicket,
                FechaHora = TimeZoneHelper.ToBusinessTime(venta.FechaHora),
                Subtotal = venta.Subtotal,
                TotalIva = venta.TotalIva,
                TotalVenta = venta.TotalVenta,
                MontoRecibido = venta.MontoRecibido,
                CambioEntregado = venta.CambioEntregado,
                EstadoVenta = venta.EstadoVenta,
                Detalles = venta.DetallesVenta.Select(d => new DetalleVentaResponse
                {
                    IdDetalle = d.IdDetalle,
                    IdVenta = d.IdVenta,
                    IdProducto = d.IdProducto,
                    NombreProducto = d.IdProductoNavigation?.NombreProducto ?? string.Empty,
                    CodigoSku = d.IdProductoNavigation?.CodigoSku ?? string.Empty,
                    Cantidad = d.Cantidad,
                    PrecioUnitarioHistorico = d.PrecioUnitarioHistorico,
                    SubtotalLinea = d.SubtotalLinea
                }).ToList()
            };
        }

        if (_supabase == null) return null;

        var res = await _supabase.From<Venta>()
            .Where(v => v.IdVenta == idVenta)
            .Get();

        var ventaSupa = res.Models.FirstOrDefault();
        if (ventaSupa == null) return null;

        await CargarRelacionesVentaAsync(ventaSupa);
        var response = _mapper.Map<VentaResponse>(ventaSupa);
        response.FechaHora = TimeZoneHelper.ToBusinessTime(ventaSupa.FechaHora);
        response.Detalles = await ObtenerDetallesVentaAsync(idVenta);

        return response;
    }

    public async Task<IEnumerable<VentaResponse>> ObtenerPorTurnoAsync(long idTurno)
    {
        if (_supabase == null) return Enumerable.Empty<VentaResponse>();

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
            dto.FechaHora = TimeZoneHelper.ToBusinessTime(v.FechaHora);
            dto.Detalles = await ObtenerDetallesVentaAsync(v.IdVenta);
            resultado.Add(dto);
        }

        return resultado;
    }

    public async Task<IEnumerable<VentaResponse>> ObtenerHistorialAsync(string? filtroFecha = null)
    {
        if (_supabase == null) return Enumerable.Empty<VentaResponse>();

        var res = await _supabase.From<Venta>().Get();
        var ventas = res.Models.AsEnumerable();

        if (!string.IsNullOrWhiteSpace(filtroFecha))
        {
            var hoyLocal = TimeZoneHelper.GetBusinessToday();

            if (filtroFecha.Equals("Hoy", StringComparison.OrdinalIgnoreCase))
            {
                ventas = ventas.Where(v => TimeZoneHelper.ToBusinessDate(v.FechaHora) == hoyLocal);
            }
            else if (filtroFecha.Equals("Ayer", StringComparison.OrdinalIgnoreCase))
            {
                var ayerLocal = hoyLocal.AddDays(-1);
                ventas = ventas.Where(v => TimeZoneHelper.ToBusinessDate(v.FechaHora) == ayerLocal);
            }
            else if (filtroFecha.Contains("Semana", StringComparison.OrdinalIgnoreCase))
            {
                var diasDesdeLunes = ((int)hoyLocal.DayOfWeek + 6) % 7;
                var inicioSemanaLocal = hoyLocal.AddDays(-diasDesdeLunes);
                ventas = ventas.Where(v =>
                {
                    var fechaVenta = TimeZoneHelper.ToBusinessDate(v.FechaHora);
                    return fechaVenta >= inicioSemanaLocal && fechaVenta <= hoyLocal;
                });
            }
        }

        var listOrdenada = ventas.OrderByDescending(v => v.FechaHora).ToList();
        var resultado = new List<VentaResponse>();
        var usuariosDict = await ObtenerDiccionarioUsuariosAsync();
        var metodosDict = await ObtenerDiccionarioMetodosPagoAsync();

        foreach (var v in listOrdenada)
        {
            if (usuariosDict.TryGetValue(v.IdUsuario, out var usr)) v.Usuario = usr;
            if (metodosDict.TryGetValue(v.IdMetodoPago, out var mp)) v.MetodoPago = mp;

            var dto = _mapper.Map<VentaResponse>(v);
            dto.FechaHora = TimeZoneHelper.ToBusinessTime(v.FechaHora);
            dto.Detalles = await ObtenerDetallesVentaAsync(v.IdVenta);
            resultado.Add(dto);
        }

        return resultado;
    }

    public async Task<bool> AnularVentaAsync(long idVenta)
    {
        if (_context != null)
        {
            var venta = await _context.Ventas
                .Include(v => v.DetallesVenta)
                    .ThenInclude(d => d.IdProductoNavigation)
                .FirstOrDefaultAsync(v => v.IdVenta == idVenta);

            if (venta == null || venta.EstadoVenta == "Anulada") return false;

            venta.EstadoVenta = "Anulada";
            foreach (var d in venta.DetallesVenta)
            {
                if (d.IdProductoNavigation != null)
                {
                    d.IdProductoNavigation.StockActual += d.Cantidad;
                }
            }
            await _context.SaveChangesAsync();
            return true;
        }

        if (_supabase == null) return false;

        var res = await _supabase.From<Venta>()
            .Where(v => v.IdVenta == idVenta)
            .Get();

        var ventaSupa = res.Models.FirstOrDefault();
        if (ventaSupa == null || ventaSupa.EstadoVenta == "Anulada") return false;

        ventaSupa.EstadoVenta = "Anulada";
        await _supabase.From<Venta>()
            .Where(v => v.IdVenta == idVenta)
            .Update(ventaSupa);

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
        if (_supabase == null) return;

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
        if (_supabase == null) return new List<DetalleVentaResponse>();

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
        if (_supabase == null) return new Dictionary<Guid, Usuario>();
        var res = await _supabase.From<Usuario>().Get();
        return res.Models.ToDictionary(u => u.IdUsuario, u => u);
    }

    private async Task<Dictionary<long, MetodoPago>> ObtenerDiccionarioMetodosPagoAsync()
    {
        if (_supabase == null) return new Dictionary<long, MetodoPago>();
        var res = await _supabase.From<MetodoPago>().Get();
        return res.Models.ToDictionary(m => m.IdMetodoPago, m => m);
    }

    private async Task<Dictionary<long, Producto>> ObtenerDiccionarioProductosAsync()
    {
        if (_supabase == null) return new Dictionary<long, Producto>();
        var res = await _supabase.From<Producto>().Get();
        return res.Models.ToDictionary(p => p.IdProducto, p => p);
    }
}
