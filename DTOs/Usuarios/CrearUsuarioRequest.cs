namespace TiendaGo.DTOs.Usuarios;

public class CrearUsuarioRequest
{
    public string NombreCompleto { get; set; } = string.Empty;
    public string CorreoElectronico { get; set; } = string.Empty;
    public string Clave { get; set; } = string.Empty;
    public long IdRol { get; set; } = 2; // Default 2: Cajero

    // Aliases
    public string? Nombre
    {
        get => NombreCompleto;
        set => NombreCompleto = value ?? string.Empty;
    }

    public string? Correo
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
