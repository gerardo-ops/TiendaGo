using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace TiendaGo.Models;

[Table("metodos_pago")]
public class MetodoPago : BaseModel
{
    [PrimaryKey("id_metodo_pago", false)]
    public long IdMetodoPago { get; set; }

    [Column("nombre_metodo")]
    public string NombreMetodo { get; set; } = string.Empty;

    [Column("estado_activo")]
    public bool EstadoActivo { get; set; } = true;
}
