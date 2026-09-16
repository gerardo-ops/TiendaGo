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

    // Aliases para requerimientos directos
    public string? Nombre
    {
        get => NombreProducto;
        set => NombreProducto = value ?? string.Empty;
    }

    public string? Codigo
    {
        get => CodigoSku;
        set => CodigoSku = value ?? string.Empty;
    }

    public decimal? Precio
    {
        get => PrecioVenta;
        set => PrecioVenta = value ?? 0m;
    }

    public int? Stock
    {
        get => StockActual;
        set => StockActual = value ?? 0;
    }

    public bool? Estado
    {
        get => EstadoActivo;
        set => EstadoActivo = value ?? true;
    }
}
