using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace TiendaGo.Models;

[Table("roles")]
public class Rol : BaseModel
{
    [PrimaryKey("id_rol", false)]
    public long IdRol { get; set; }

    [Column("nombre_rol")]
    public string NombreRol { get; set; } = string.Empty;

    [Column("descripcion")]
    public string? Descripcion { get; set; }
}
