using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;

namespace TiendaGo.Services;

public interface IUsuarioService
{
    Task<LoginResponse?> LoginAsync(LoginRequest request);
    Task<IEnumerable<UsuarioResponse>> ObtenerTodosAsync();
    Task<UsuarioResponse?> ObtenerPorIdAsync(Guid id);
    Task<UsuarioResponse> CrearUsuarioAsync(CrearUsuarioRequest request);
    Task<bool> CambiarEstadoAsync(Guid id, bool activo);
    string GenerarJwtToken(Usuarios usuario, out DateTime expiracion);
}
