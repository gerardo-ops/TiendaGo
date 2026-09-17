namespace TiendaGo.DTOs.Usuarios;

public class LoginResponse
{
    public string Token { get; set; } = string.Empty;
    public int IdUsuario { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public string Rol { get; set; } = string.Empty;
    public DateTime Expiracion { get; set; }

    // Aliases para compatibilidad
    public Guid IdUsuarioGuid { get; set; }
    public string NombreCompleto
    {
        get => Nombre;
        set => Nombre = value ?? string.Empty;
    }
}
