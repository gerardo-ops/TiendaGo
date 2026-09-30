using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;
using TiendaGo.Services;

namespace TiendaGo.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class UsuariosController : ControllerBase
{
    private readonly TiendaGoDbContext _context;
    private readonly IUsuarioService _usuarioService;

    public UsuariosController(TiendaGoDbContext context, IUsuarioService usuarioService)
    {
        _context = context;
        _usuarioService = usuarioService;
    }

    /// <summary>
    /// Registra un nuevo cajero en el sistema capturando errores de base de datos detallados.
    /// </summary>
    [HttpPost("cajero")]
    public async Task<IActionResult> RegistrarCajero([FromBody] CrearUsuarioRequest request)
    {
        var correo = (request.Correo ?? request.CorreoElectronico ?? string.Empty).Trim();
        var nombre = (request.Nombre ?? request.NombreCompleto ?? string.Empty).Trim();
        var password = request.Password ?? request.Clave ?? string.Empty;

        if (string.IsNullOrWhiteSpace(correo) || string.IsNullOrWhiteSpace(password) || string.IsNullOrWhiteSpace(nombre))
        {
            return BadRequest(new { mensaje = "Nombre completo, correo y contraseña son requeridos para dar de alta al cajero." });
        }

        // Forzar rol de Cajero (id_rol = 2)
        request.IdRol = 2;

        try
        {
            var nuevoCajero = await _usuarioService.RegistrarUsuarioAsync(request);
            return CreatedAtAction(nameof(ObtenerPorId), new { id = nuevoCajero.IdUsuarioGuid }, nuevoCajero);
        }
        catch (DbUpdateException ex)
        {
            // Tarea 1: Exponer la causa real de la base de datos (PostgreSQL / Supabase)
            var innerMsg = ex.InnerException?.Message ?? ex.Message;
            return BadRequest(new { mensaje = $"Error BD: {innerMsg}" });
        }
        catch (InvalidOperationException ex)
        {
            return Conflict(new { mensaje = ex.Message });
        }
        catch (Exception ex)
        {
            var innerMsg = ex.InnerException?.Message ?? ex.Message;
            return BadRequest(new { mensaje = $"Error BD: {innerMsg}" });
        }
    }

    /// <summary>
    /// Registra un usuario con cualquier rol.
    /// </summary>
    [HttpPost]
    public async Task<IActionResult> CrearUsuario([FromBody] CrearUsuarioRequest request)
    {
        var correo = (request.Correo ?? request.CorreoElectronico ?? string.Empty).Trim();
        var nombre = (request.Nombre ?? request.NombreCompleto ?? string.Empty).Trim();
        var password = request.Password ?? request.Clave ?? string.Empty;

        if (string.IsNullOrWhiteSpace(correo) || string.IsNullOrWhiteSpace(password) || string.IsNullOrWhiteSpace(nombre))
        {
            return BadRequest(new { mensaje = "Nombre completo, correo y contraseña son obligatorios." });
        }

        try
        {
            var nuevoUsuario = await _usuarioService.RegistrarUsuarioAsync(request);
            return CreatedAtAction(nameof(ObtenerPorId), new { id = nuevoUsuario.IdUsuarioGuid }, nuevoUsuario);
        }
        catch (DbUpdateException ex)
        {
            var innerMsg = ex.InnerException?.Message ?? ex.Message;
            return BadRequest(new { mensaje = $"Error BD: {innerMsg}" });
        }
        catch (InvalidOperationException ex)
        {
            return Conflict(new { mensaje = ex.Message });
        }
        catch (Exception ex)
        {
            var innerMsg = ex.InnerException?.Message ?? ex.Message;
            return BadRequest(new { mensaje = $"Error BD: {innerMsg}" });
        }
    }

    /// <summary>
    /// Obtiene la lista completa de usuarios.
    /// </summary>
    [HttpGet]
    public async Task<IActionResult> ObtenerTodos()
    {
        var usuarios = await _usuarioService.ObtenerUsuariosAsync();
        return Ok(usuarios);
    }

    /// <summary>
    /// Obtiene un usuario específico por su ID UUID.
    /// </summary>
    [HttpGet("{id:guid}")]
    public async Task<IActionResult> ObtenerPorId(Guid id)
    {
        var usuario = await _usuarioService.ObtenerPorIdAsync(id);
        if (usuario == null)
        {
            return NotFound(new { mensaje = $"Usuario con ID {id} no encontrado." });
        }
        return Ok(usuario);
    }

    /// <summary>
    /// Activa o desactiva a un usuario en el sistema.
    /// </summary>
    [HttpPatch("{id:guid}/estado")]
    public async Task<IActionResult> CambiarEstado(Guid id, [FromQuery] bool activo)
    {
        var actualizado = await _usuarioService.CambiarEstadoAsync(id, activo);
        if (!actualizado)
        {
            return NotFound(new { mensaje = $"Usuario con ID {id} no encontrado." });
        }
        return Ok(new { mensaje = $"Estado del usuario actualizado a {(activo ? "activo" : "inactivo")}." });
    }
}
