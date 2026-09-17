namespace TiendaGo.DTOs.Productos;

public class ProductoResponse
{
    public int IdProducto { get; set; }
    public string CodigoBarra { get; set; } = string.Empty;
    public string Nombre { get; set; } = string.Empty;
    public decimal Precio { get; set; }
    public int Stock { get; set; }
    public int IdCategoria { get; set; }
    public string NombreCategoria { get; set; } = string.Empty;
    public bool Estado { get; set; } = true;

    // Aliases y campos adicionales para compatibilidad
    public string CodigoSku
    {
        get => CodigoBarra;
        set => CodigoBarra = value ?? string.Empty;
    }

    public string NombreProducto
    {
        get => Nombre;
        set => Nombre = value ?? string.Empty;
    }

    public decimal PrecioVenta
    {
        get => Precio;
        set => Precio = value;
    }

    public decimal CostoCompra { get; set; }

    public int StockActual
    {
        get => Stock;
        set => Stock = value;
    }

    public int StockMinimo { get; set; }

    public string? UrlImagen { get; set; }

    public bool EstadoActivo
    {
        get => Estado;
        set => Estado = value;
    }

    public DateTime FechaCreacion { get; set; }

    public bool StockCritico => Stock <= StockMinimo;
}
