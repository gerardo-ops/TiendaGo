using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class Productos
{
    public long IdProducto { get; set; }

    public long IdCategoria { get; set; }

    public string NombreProducto { get; set; } = null!;

    public string CodigoSku { get; set; } = null!;

    public decimal CostoCompra { get; set; }

    public decimal PrecioVenta { get; set; }

    public int StockActual { get; set; }

    public int StockMinimo { get; set; }

    public string? UrlImagen { get; set; }

    public bool EstadoActivo { get; set; }

    public DateTime FechaCreacion { get; set; }

    public virtual ICollection<DetallesVenta> DetallesVenta { get; set; } = new List<DetallesVenta>();

    public virtual Categorias IdCategoriaNavigation { get; set; } = null!;
}
