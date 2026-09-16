using TiendaGo.DTOs.Turnos;

namespace TiendaGo.Services;

public interface ITurnoCajaService
{
    Task<TurnoResponse> AbrirTurnoAsync(AbrirTurnoRequest request);
    Task<TurnoResponse?> CerrarTurnoAsync(long idTurno, CerrarTurnoRequest request);
    Task<TurnoResponse?> ObtenerTurnoActivoAsync(Guid idUsuario);
    Task<TurnoResponse?> ObtenerPorIdAsync(long idTurno);
    Task<IEnumerable<TurnoResponse>> ObtenerHistorialAsync();
}
