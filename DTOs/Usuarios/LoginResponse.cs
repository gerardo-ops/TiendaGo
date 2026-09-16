namespace TiendaGo.DTOs.Usuarios;

public class LoginResponse
{
    public string Token { get; set; } = string.Empty;
    public Guid IdUsuario { get; set; }
    public string NombreCompleto { get; set; } = string.Empty;
    public string Rol { get; set; } = string.Empty;
    public DateTime Expiracion { get; set; }
}
