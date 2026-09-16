namespace TiendaGo.DTOs.Ventas;

public class DetalleVentaRequest
{
    public long IdProducto { get; set; }
    public int Cantidad { get; set; }
    public decimal? PrecioUnitarioHistorico { get; set; }
}
