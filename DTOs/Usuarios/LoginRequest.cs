namespace TiendaGo.DTOs.Usuarios;

public class LoginRequest
{
    public string CorreoElectronico { get; set; } = string.Empty;
    public string Clave { get; set; } = string.Empty;

    // Aliases para compatibilidad
    public string? Usuario
    {
        get => CorreoElectronico;
        set => CorreoElectronico = value ?? string.Empty;
    }

    public string? Password
    {
        get => Clave;
        set => Clave = value ?? string.Empty;
    }
}
