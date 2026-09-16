namespace TiendaGo.DTOs.Productos;

public class ProductoRequest
{
    public long IdCategoria { get; set; }
    public string NombreProducto { get; set; } = string.Empty;
    public string CodigoSku { get; set; } = string.Empty;
    public decimal CostoCompra { get; set; }
    public decimal PrecioVenta { get; set; }
    public int StockActual { get; set; }
    public int StockMinimo { get; set; } = 5;
    public string? UrlImagen { get; set; }
    public bool EstadoActivo { get; set; } = true;
}
