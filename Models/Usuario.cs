using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace TiendaGo.Models;

[Table("usuarios")]
public class Usuario : BaseModel
{
    [PrimaryKey("id_usuario", false)]
    public Guid IdUsuario { get; set; }

    [Column("id_rol")]
    public long IdRol { get; set; }

    [Reference(typeof(Rol))]
    public Rol? Rol { get; set; }

    [Column("nombre_completo")]
    public string NombreCompleto { get; set; } = string.Empty;

    [Column("correo_electronico")]
    public string CorreoElectronico { get; set; } = string.Empty;

    [Column("clave_hash")]
    public string? ClaveHash { get; set; }

    [Column("estado_activo")]
    public bool EstadoActivo { get; set; } = true;

    [Column("fecha_registro")]
    public DateTimeOffset FechaRegistro { get; set; } = DateTimeOffset.UtcNow;
}
