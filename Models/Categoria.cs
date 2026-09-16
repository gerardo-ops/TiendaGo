using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace TiendaGo.Models;

[Table("categorias")]
public class Categoria : BaseModel
{
    [PrimaryKey("id_categoria", false)]
    public long IdCategoria { get; set; }

    [Column("nombre_categoria")]
    public string NombreCategoria { get; set; } = string.Empty;

    [Column("descripcion")]
    public string? Descripcion { get; set; }

    [Column("estado_activo")]
    public bool EstadoActivo { get; set; } = true;
}
