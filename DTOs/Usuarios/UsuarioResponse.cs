namespace TiendaGo.DTOs.Usuarios;

public class UsuarioResponse
{
    public int IdUsuario { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public string Correo { get; set; } = string.Empty;
    public string Rol { get; set; } = string.Empty;
    public bool Estado { get; set; } = true;

    // Propiedades adicionales/aliases para compatibilidad
    public Guid IdUsuarioGuid { get; set; }
    public long IdRol { get; set; }
    public string NombreRol
    {
        get => Rol;
        set => Rol = value ?? string.Empty;
    }
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
    public bool EstadoActivo
    {
        get => Estado;
        set => Estado = value;
    }
    public DateTime FechaRegistro { get; set; }
    public string? Token { get; set; }
}
