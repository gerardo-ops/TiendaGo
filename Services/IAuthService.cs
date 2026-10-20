using TiendaGo.DTOs.Usuarios;

namespace TiendaGo.Services;

public interface IAuthService
{
    Task<LoginResponse?> LoginAsync(LoginRequest request);
}
