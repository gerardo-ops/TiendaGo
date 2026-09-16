namespace TiendaGo.DTOs.Usuarios;

public class LoginRequest
{
    public string CorreoElectronico { get; set; } = string.Empty;
    public string Clave { get; set; } = string.Empty;
}
