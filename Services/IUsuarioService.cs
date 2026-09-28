using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;

namespace TiendaGo.Services;

public interface IUsuarioService
{
    Task<LoginResponse?> LoginAsync(LoginRequest request);
    Task<UsuarioResponse> RegistrarUsuarioAsync(CrearUsuarioRequest request);
    Task<UsuarioResponse> CrearUsuarioAsync(CrearUsuarioRequest request);
    Task<List<UsuarioResponse>> ObtenerUsuariosAsync();
    Task<IEnumerable<UsuarioResponse>> ObtenerTodosAsync();
    Task<UsuarioResponse?> ObtenerPorIdAsync(Guid id);
    Task<bool> CambiarEstadoAsync(Guid id, bool activo);
    string GenerarJwtToken(Usuarios usuario, out DateTime expiracion);
}
