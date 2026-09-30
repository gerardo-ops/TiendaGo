using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace TiendaGo.Models;

/// <summary>
/// Mapeo de la tabla 'public.usuarios' en PostgreSQL / Supabase
/// </summary>
[Table("usuarios", Schema = "public")]
public partial class Usuarios
{
    [Key]
    [Column("id_usuario")]
    public Guid IdUsuario { get; set; } = Guid.NewGuid();

    /// <summary>
    /// Relación con la tabla 'roles' (1: Administrador, 2: Cajero, 3: Supervisor)
    /// </summary>
    [Required]
    [Column("id_rol")]
    public long IdRol { get; set; } = 2; // Por defecto: 2 (Cajero)

    [Required]
    [MaxLength(150)]
    [Column("nombre_completo")]
    public string NombreCompleto { get; set; } = string.Empty;

    [Required]
    [MaxLength(150)]
    [EmailAddress]
    [Column("correo_electronico")]
    public string CorreoElectronico { get; set; } = string.Empty;

    /// <summary>
    /// Contraseña cifrada con algoritmo BCrypt
    /// </summary>
    [MaxLength(255)]
    [Column("clave_hash")]
    public string? ClaveHash { get; set; }

    [Required]
    [Column("estado_activo")]
    public bool EstadoActivo { get; set; } = true;

    [Required]
    [Column("fecha_registro")]
    public DateTime FechaRegistro { get; set; } = DateTime.UtcNow;

    [ForeignKey("IdRol")]
    public virtual Roles? IdRolNavigation { get; set; }

    [ForeignKey("IdUsuario")]
    public virtual Users? IdUsuarioNavigation { get; set; }

    public virtual ICollection<TurnosCaja> TurnosCaja { get; set; } = new List<TurnosCaja>();

    public virtual ICollection<Ventas> Ventas { get; set; } = new List<Ventas>();
}
