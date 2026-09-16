namespace TiendaGo.DTOs.Productos;

public class ProductoResponse
{
    public long IdProducto { get; set; }
    public long IdCategoria { get; set; }
    public string? NombreCategoria { get; set; }
    public string NombreProducto { get; set; } = string.Empty;
    public string CodigoSku { get; set; } = string.Empty;
    public decimal CostoCompra { get; set; }
    public decimal PrecioVenta { get; set; }
    public int StockActual { get; set; }
    public int StockMinimo { get; set; }
    public string? UrlImagen { get; set; }
    public bool EstadoActivo { get; set; }
    public DateTime FechaCreacion { get; set; }

    // Indicador para terminal POS y catálogo
    public bool StockCritico => StockActual <= StockMinimo;
}
