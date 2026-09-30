using System.ComponentModel.DataAnnotations;

namespace TiendaGo.DTOs.Usuarios;

public class CrearUsuarioRequest
{
    [Required(ErrorMessage = "El nombre completo es requerido")]
    [MaxLength(150, ErrorMessage = "El nombre no puede exceder 150 caracteres")]
    public string Nombre { get; set; } = string.Empty;

    [Required(ErrorMessage = "El correo electrónico es requerido")]
    [EmailAddress(ErrorMessage = "El formato de correo electrónico es inválido")]
    [MaxLength(150, ErrorMessage = "El correo no puede exceder 150 caracteres")]
    public string Correo { get; set; } = string.Empty;

    [Required(ErrorMessage = "La contraseña es requerida")]
    [MinLength(6, ErrorMessage = "La contraseña debe tener al menos 6 caracteres")]
    public string Password { get; set; } = string.Empty;

    /// <summary>
    /// Identificador del rol: 1 = Administrador, 2 = Cajero, 3 = Supervisor.
    /// Por defecto es 2 (Cajero).
    /// </summary>
    public long IdRol { get; set; } = 2;

    // Aliases bidireccionales para máxima compatibilidad con clientes móviles, web y Swagger
    public string NombreCompleto
    {
        get => Nombre;
        set => Nombre = string.IsNullOrWhiteSpace(value) ? Nombre : value;
    }

    public string CorreoElectronico
    {
        get => Correo;
        set => Correo = string.IsNullOrWhiteSpace(value) ? Correo : value;
    }

    public string Clave
    {
        get => Password;
        set => Password = string.IsNullOrWhiteSpace(value) ? Password : value;
    }
}
