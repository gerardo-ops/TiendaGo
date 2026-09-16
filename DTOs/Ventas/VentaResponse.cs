namespace TiendaGo.DTOs.Ventas;

public class VentaResponse
{
    public long IdVenta { get; set; }
    public long IdTurno { get; set; }
    public Guid IdUsuario { get; set; }
    public string NombreUsuario { get; set; } = string.Empty;
    public long IdMetodoPago { get; set; }
    public string NombreMetodoPago { get; set; } = string.Empty;
    public string NumeroTicket { get; set; } = string.Empty;
    public DateTimeOffset FechaHora { get; set; }
    public decimal Subtotal { get; set; }
    public decimal TotalIva { get; set; }
    public decimal TotalVenta { get; set; }
    public decimal MontoRecibido { get; set; }
    public decimal CambioEntregado { get; set; }
    public string EstadoVenta { get; set; } = string.Empty;
    public List<DetalleVentaResponse> Detalles { get; set; } = new();
}
