using TiendaGo.DTOs.Productos;

namespace TiendaGo.DTOs.Dashboard;

public class DashboardResumenResponse
{
    public decimal TotalVentasDia { get; set; }
    public int CantidadVentasDia { get; set; }
    public decimal VentasEfectivoDia { get; set; }
    public decimal VentasDigitalesDia { get; set; }
    public int TotalProductosCriticos { get; set; }
    public List<ProductoResponse> ProductosStockBajo { get; set; } = new();
}
