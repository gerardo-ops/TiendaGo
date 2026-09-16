using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class Ventas
{
    public long IdVenta { get; set; }

    public long IdTurno { get; set; }

    public Guid IdUsuario { get; set; }

    public long IdMetodoPago { get; set; }

    public string NumeroTicket { get; set; } = null!;

    public DateTime FechaHora { get; set; }

    public decimal Subtotal { get; set; }

    public decimal TotalIva { get; set; }

    public decimal TotalVenta { get; set; }

    public decimal MontoRecibido { get; set; }

    public decimal CambioEntregado { get; set; }

    public string EstadoVenta { get; set; } = null!;

    public virtual ICollection<DetallesVenta> DetallesVenta { get; set; } = new List<DetallesVenta>();

    public virtual MetodosPago IdMetodoPagoNavigation { get; set; } = null!;

    public virtual TurnosCaja IdTurnoNavigation { get; set; } = null!;

    public virtual Usuarios IdUsuarioNavigation { get; set; } = null!;
}
