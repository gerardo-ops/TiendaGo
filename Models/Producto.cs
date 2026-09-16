using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace TiendaGo.Models;

[Table("productos")]
public class Producto : BaseModel
{
    [PrimaryKey("id_producto", false)]
    public long IdProducto { get; set; }

    [Column("id_categoria")]
    public long IdCategoria { get; set; }

    [Reference(typeof(Categoria))]
    public Categoria? Categoria { get; set; }

    [Column("nombre_producto")]
    public string NombreProducto { get; set; } = string.Empty;

    [Column("codigo_sku")]
    public string CodigoSku { get; set; } = string.Empty;

    [Column("costo_compra")]
    public decimal CostoCompra { get; set; }

    [Column("precio_venta")]
    public decimal PrecioVenta { get; set; }

    [Column("stock_actual")]
    public int StockActual { get; set; }

    [Column("stock_minimo")]
    public int StockMinimo { get; set; } = 5;

    [Column("url_imagen")]
    public string? UrlImagen { get; set; }

    [Column("estado_activo")]
    public bool EstadoActivo { get; set; } = true;

    [Column("fecha_creacion")]
    public DateTimeOffset FechaCreacion { get; set; } = DateTimeOffset.UtcNow;
}
