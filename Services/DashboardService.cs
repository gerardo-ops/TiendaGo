using AutoMapper;
using TiendaGo.DTOs.Dashboard;
using TiendaGo.DTOs.Productos;
using TiendaGo.Models;

namespace TiendaGo.Services;

public class DashboardService : IDashboardService
{
    private readonly Supabase.Client _supabase;
    private readonly IMapper _mapper;

    public DashboardService(Supabase.Client supabase, IMapper mapper)
    {
        _supabase = supabase;
        _mapper = mapper;
    }

    public async Task<DashboardResumenResponse> ObtenerResumenAsync()
    {
        var hoyUtc = DateTimeOffset.UtcNow.Date;

        // 1. Obtener ventas del día de hoy
        var ventasRes = await _supabase.From<Venta>()
            .Where(v => v.EstadoVenta == "Completada")
            .Get();

        var ventasHoy = ventasRes.Models
            .Where(v => v.FechaHora.Date >= hoyUtc)
            .ToList();

        decimal totalVentasDia = ventasHoy.Sum(v => v.TotalVenta);
        int cantidadVentasDia = ventasHoy.Count;

        // 2. Clasificar ventas por método de pago (Efectivo vs Digital)
        var metodosRes = await _supabase.From<MetodoPago>().Get();
        var metodosDict = metodosRes.Models.ToDictionary(m => m.IdMetodoPago, m => m.NombreMetodo);

        decimal ventasEfectivoDia = 0m;
        decimal ventasDigitalesDia = 0m;

        foreach (var v in ventasHoy)
        {
            if (metodosDict.TryGetValue(v.IdMetodoPago, out var nombreMetodo) &&
                string.Equals(nombreMetodo, "Efectivo", StringComparison.OrdinalIgnoreCase))
            {
                ventasEfectivoDia += v.TotalVenta;
            }
            else
            {
                ventasDigitalesDia += v.TotalVenta;
            }
        }

        // 3. Consultar productos con stock igual o inferior al stock mínimo
        var productosRes = await _supabase.From<Producto>()
            .Where(p => p.EstadoActivo == true)
            .Get();

        var productosStockBajo = productosRes.Models
            .Where(p => p.StockActual <= p.StockMinimo)
            .OrderBy(p => p.StockActual)
            .ToList();

        var categoriasRes = await _supabase.From<Categoria>().Get();
        var catDict = categoriasRes.Models.ToDictionary(c => c.IdCategoria, c => c.NombreCategoria);

        var productosBajoDto = new List<ProductoResponse>();
        foreach (var p in productosStockBajo)
        {
            var pDto = _mapper.Map<ProductoResponse>(p);
            if (catDict.TryGetValue(p.IdCategoria, out var catNombre))
            {
                pDto.NombreCategoria = catNombre;
            }
            productosBajoDto.Add(pDto);
        }

        return new DashboardResumenResponse
        {
            TotalVentasDia = totalVentasDia,
            CantidadVentasDia = cantidadVentasDia,
            VentasEfectivoDia = ventasEfectivoDia,
            VentasDigitalesDia = ventasDigitalesDia,
            TotalProductosCriticos = productosStockBajo.Count,
            ProductosStockBajo = productosBajoDto
        };
    }
}
