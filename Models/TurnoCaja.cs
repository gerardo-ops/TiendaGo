using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace TiendaGo.Models;

[Table("turnos_caja")]
public class TurnoCaja : BaseModel
{
    [PrimaryKey("id_turno", false)]
    public long IdTurno { get; set; }

    [Column("id_usuario")]
    public Guid IdUsuario { get; set; }

    [Reference(typeof(Usuario))]
    public Usuario? Usuario { get; set; }

    [Column("fecha_apertura")]
    public DateTimeOffset FechaApertura { get; set; } = DateTimeOffset.UtcNow;

    [Column("fecha_cierre")]
    public DateTimeOffset? FechaCierre { get; set; }

    [Column("monto_base_inicial")]
    public decimal MontoBaseInicial { get; set; }

    [Column("total_ventas_efectivo")]
    public decimal TotalVentasEfectivo { get; set; }

    [Column("total_ventas_digital")]
    public decimal TotalVentasDigital { get; set; }

    [Column("monto_declarado")]
    public decimal? MontoDeclarado { get; set; }

    [Column("diferencia_cuadre")]
    public decimal? DiferenciaCuadre { get; set; }

    [Column("estado_turno")]
    public string EstadoTurno { get; set; } = "Abierto";
}
