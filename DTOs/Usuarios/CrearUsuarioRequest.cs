namespace TiendaGo.DTOs.Usuarios;

public class CrearUsuarioRequest
{
    public string Nombre { get; set; } = string.Empty;
    public string Correo { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
    public int IdRol { get; set; } = 2; // Default 2: Cajero

    // Aliases para compatibilidad
    public string NombreCompleto
    {
        get => Nombre;
        set => Nombre = value ?? string.Empty;
    }

    public string CorreoElectronico
    {
        get => Correo;
        set => Correo = value ?? string.Empty;
    }

    public string Clave
    {
        get => Password;
        set => Password = value ?? string.Empty;
    }
}
