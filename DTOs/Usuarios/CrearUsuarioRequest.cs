namespace TiendaGo.DTOs.Usuarios;

public class CrearUsuarioRequest
{
    public string NombreCompleto { get; set; } = string.Empty;
    public string CorreoElectronico { get; set; } = string.Empty;
    public string Clave { get; set; } = string.Empty;
    public long IdRol { get; set; } = 2; // Default 2: Cajero
}
