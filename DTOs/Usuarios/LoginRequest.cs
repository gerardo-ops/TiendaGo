namespace TiendaGo.DTOs.Usuarios;

public class LoginRequest
{
    public string UsuarioOCorreo { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;

    // Aliases para compatibilidad
    public string CorreoElectronico
    {
        get => UsuarioOCorreo;
        set => UsuarioOCorreo = value ?? string.Empty;
    }

    public string Clave
    {
        get => Password;
        set => Password = value ?? string.Empty;
    }
}
