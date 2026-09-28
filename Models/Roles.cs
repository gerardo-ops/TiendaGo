using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class Roles
{
    public long IdRol { get; set; }

    public string NombreRol { get; set; } = null!;

    public string? Descripcion { get; set; }

    public virtual ICollection<Usuarios> Usuarios { get; set; } = new List<Usuarios>();
}
