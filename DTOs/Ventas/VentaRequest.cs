namespace TiendaGo.DTOs.Ventas;

public class VentaRequest
{
    public long IdTurno { get; set; }
    public Guid IdUsuario { get; set; }
    public long IdMetodoPago { get; set; }
    public decimal MontoRecibido { get; set; }
    public List<DetalleVentaRequest> Detalles { get; set; } = new();
}
