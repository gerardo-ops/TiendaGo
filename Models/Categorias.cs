using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class Categorias
{
    public long IdCategoria { get; set; }

    public string NombreCategoria { get; set; } = null!;

    public string? Descripcion { get; set; }

    public bool EstadoActivo { get; set; }

    public virtual ICollection<Productos> Productos { get; set; } = new List<Productos>();
}
