namespace TiendaGo.DTOs.Ventas;

public class DetalleVentaResponse
{
    public long IdDetalle { get; set; }
    public long IdVenta { get; set; }
    public long IdProducto { get; set; }
    public string NombreProducto { get; set; } = string.Empty;
    public string CodigoSku { get; set; } = string.Empty;
    public int Cantidad { get; set; }
    public decimal PrecioUnitarioHistorico { get; set; }
    public decimal SubtotalLinea { get; set; }
}
