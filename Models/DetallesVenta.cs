using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class DetallesVenta
{
    public long IdDetalle { get; set; }

    public long IdVenta { get; set; }

    public long IdProducto { get; set; }

    public int Cantidad { get; set; }

    public decimal PrecioUnitarioHistorico { get; set; }

    public decimal SubtotalLinea { get; set; }

    public virtual Productos IdProductoNavigation { get; set; } = null!;

    public virtual Ventas IdVentaNavigation { get; set; } = null!;
}
