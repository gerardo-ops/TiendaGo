using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace TiendaGo.Models;

[Table("ventas")]
public class Venta : BaseModel
{
    [PrimaryKey("id_venta", false)]
    public long IdVenta { get; set; }

    [Column("id_turno")]
    public long IdTurno { get; set; }

    [Reference(typeof(TurnoCaja))]
    public TurnoCaja? TurnoCaja { get; set; }

    [Column("id_usuario")]
    public Guid IdUsuario { get; set; }

    [Reference(typeof(Usuario))]
    public Usuario? Usuario { get; set; }

    [Column("id_metodo_pago")]
    public long IdMetodoPago { get; set; }

    [Reference(typeof(MetodoPago))]
    public MetodoPago? MetodoPago { get; set; }

    [Column("numero_ticket")]
    public string NumeroTicket { get; set; } = string.Empty;

    [Column("fecha_hora")]
    public DateTimeOffset FechaHora { get; set; } = DateTimeOffset.UtcNow;

    [Column("subtotal")]
    public decimal Subtotal { get; set; }

    [Column("total_iva")]
    public decimal TotalIva { get; set; }

    [Column("total_venta")]
    public decimal TotalVenta { get; set; }

    [Column("monto_recibido")]
    public decimal MontoRecibido { get; set; }

    [Column("cambio_entregado")]
    public decimal CambioEntregado { get; set; }

    [Column("estado_venta")]
    public string EstadoVenta { get; set; } = "Completada";
}
