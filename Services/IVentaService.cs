using TiendaGo.DTOs.Ventas;

namespace TiendaGo.Services;

public interface IVentaService
{
    Task<VentaResponse> RegistrarVentaAsync(VentaRequest request);
    Task<VentaResponse?> ObtenerPorIdAsync(long idVenta);
    Task<IEnumerable<VentaResponse>> ObtenerPorTurnoAsync(long idTurno);
    Task<IEnumerable<VentaResponse>> ObtenerHistorialAsync(string? filtroFecha = null);
    Task<bool> AnularVentaAsync(long idVenta);
}
