using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class MetodosPago
{
    public long IdMetodoPago { get; set; }

    public string NombreMetodo { get; set; } = null!;

    public bool EstadoActivo { get; set; }

    public virtual ICollection<Ventas> Ventas { get; set; } = new List<Ventas>();
}
