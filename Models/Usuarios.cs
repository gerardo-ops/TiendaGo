using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class Usuarios
{
    public Guid IdUsuario { get; set; }

    public long IdRol { get; set; }

    public string NombreCompleto { get; set; } = null!;

    public string CorreoElectronico { get; set; } = null!;

    public string? ClaveHash { get; set; }

    public bool EstadoActivo { get; set; }

    public DateTime FechaRegistro { get; set; }

    public virtual Roles IdRolNavigation { get; set; } = null!;

    public virtual Users IdUsuarioNavigation { get; set; } = null!;

    public virtual ICollection<TurnosCaja> TurnosCaja { get; set; } = new List<TurnosCaja>();

    public virtual ICollection<Ventas> Ventas { get; set; } = new List<Ventas>();
}
