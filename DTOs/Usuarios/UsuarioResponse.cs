namespace TiendaGo.DTOs.Usuarios;

public class UsuarioResponse
{
    public Guid IdUsuario { get; set; }
    public long IdRol { get; set; }
    public string NombreRol { get; set; } = string.Empty;
    public string NombreCompleto { get; set; } = string.Empty;
    public string CorreoElectronico { get; set; } = string.Empty;
    public bool EstadoActivo { get; set; }
    public DateTime FechaRegistro { get; set; }
    public string? Token { get; set; }
}
