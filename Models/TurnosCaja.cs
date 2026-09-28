using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class TurnosCaja
{
    public long IdTurno { get; set; }

    public Guid IdUsuario { get; set; }

    public DateTime FechaApertura { get; set; }

    public DateTime? FechaCierre { get; set; }

    public decimal MontoBaseInicial { get; set; }

    public decimal TotalVentasEfectivo { get; set; }

    public decimal TotalVentasDigital { get; set; }

    public decimal? MontoDeclarado { get; set; }

    public decimal? DiferenciaCuadre { get; set; }

    public string EstadoTurno { get; set; } = null!;

    public virtual Usuarios IdUsuarioNavigation { get; set; } = null!;

    public virtual ICollection<Ventas> Ventas { get; set; } = new List<Ventas>();
}
