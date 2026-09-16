using TiendaGo.DTOs.Usuarios;

namespace TiendaGo.Services;

public interface IUsuarioService
{
    Task<UsuarioResponse?> LoginAsync(LoginRequest request);
    Task<IEnumerable<UsuarioResponse>> ObtenerTodosAsync();
    Task<UsuarioResponse?> ObtenerPorIdAsync(Guid id);
    Task<UsuarioResponse> CrearUsuarioAsync(CrearUsuarioRequest request);
    Task<bool> CambiarEstadoAsync(Guid id, bool activo);
    string GenerarJwtToken(UsuarioResponse usuario);
}
