namespace TiendaGo.DTOs.Turnos;

public class TurnoResponse
{
    public long IdTurno { get; set; }
    public Guid IdUsuario { get; set; }
    public string NombreUsuario { get; set; } = string.Empty;
    public DateTimeOffset FechaApertura { get; set; }
    public DateTimeOffset? FechaCierre { get; set; }
    public decimal MontoBaseInicial { get; set; }
    public decimal TotalVentasEfectivo { get; set; }
    public decimal TotalVentasDigital { get; set; }
    public decimal TotalVentasGeneral => TotalVentasEfectivo + TotalVentasDigital;
    public decimal TotalEsperadoCaja => MontoBaseInicial + TotalVentasEfectivo;
    public decimal? MontoDeclarado { get; set; }
    public decimal? DiferenciaCuadre { get; set; }
    public string EstadoTurno { get; set; } = string.Empty;
}
