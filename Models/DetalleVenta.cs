using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace TiendaGo.Models;

[Table("detalles_venta")]
public class DetalleVenta : BaseModel
{
    [PrimaryKey("id_detalle", false)]
    public long IdDetalle { get; set; }

    [Column("id_venta")]
    public long IdVenta { get; set; }

    [Reference(typeof(Venta))]
    public Venta? Venta { get; set; }

    [Column("id_producto")]
    public long IdProducto { get; set; }

    [Reference(typeof(Producto))]
    public Producto? Producto { get; set; }

    [Column("cantidad")]
    public int Cantidad { get; set; }

    [Column("precio_unitario_historico")]
    public decimal PrecioUnitarioHistorico { get; set; }

    [Column("subtotal_linea")]
    public decimal SubtotalLinea { get; set; }
}
