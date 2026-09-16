using Microsoft.AspNetCore.Mvc;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Services;

namespace TiendaGo.Endpoints;

public static class UsuarioEndpoints
{
    public static IEndpointRouteBuilder MapUsuarioEndpoints(this IEndpointRouteBuilder routes)
    {
        // =============================================
        // GRUPO: /api/auth (Autenticación y Login)
        // =============================================
        var authGroup = routes.MapGroup("/api/auth")
            .WithTags("Autenticación");

        authGroup.MapPost("/login", async (
            [FromBody] LoginRequest request,
            [FromServices] IUsuarioService usuarioService) =>
        {
            if (string.IsNullOrWhiteSpace(request.CorreoElectronico) || string.IsNullOrWhiteSpace(request.Clave))
            {
                return Results.BadRequest(new { mensaje = "El correo y la contraseña son requeridos." });
            }

            var usuario = await usuarioService.LoginAsync(request);
            if (usuario == null)
            {
                return Results.Unauthorized();
            }

            return Results.Ok(new
            {
                mensaje = "Inicio de sesión exitoso.",
                token = usuario.Token,
                usuario
            });
        })
        .AllowAnonymous()
        .WithName("Login")
        .WithSummary("Inicia sesión y genera token Bearer JWT");

        // =============================================
        // GRUPO: /api/usuarios (Administración de Usuarios)
        // =============================================
        var usuariosGroup = routes.MapGroup("/api/usuarios")
            .WithTags("Usuarios")
            .RequireAuthorization();

        usuariosGroup.MapGet("/", async ([FromServices] IUsuarioService usuarioService) =>
        {
            var usuarios = await usuarioService.ObtenerTodosAsync();
            return Results.Ok(usuarios);
        })
        .WithName("ObtenerUsuarios")
        .WithSummary("Obtiene la lista de usuarios registrados");

        usuariosGroup.MapGet("/{id:guid}", async (
            Guid id,
            [FromServices] IUsuarioService usuarioService) =>
        {
            var usuario = await usuarioService.ObtenerPorIdAsync(id);
            return usuario != null
                ? Results.Ok(usuario)
                : Results.NotFound(new { mensaje = $"Usuario con ID {id} no encontrado." });
        })
        .WithName("ObtenerUsuarioPorId")
        .WithSummary("Obtiene un usuario específico por su identificador UUID");

        usuariosGroup.MapPost("/", async (
            [FromBody] CrearUsuarioRequest request,
            [FromServices] IUsuarioService usuarioService) =>
        {
            if (string.IsNullOrWhiteSpace(request.CorreoElectronico) ||
                string.IsNullOrWhiteSpace(request.Clave) ||
                string.IsNullOrWhiteSpace(request.NombreCompleto))
            {
                return Results.BadRequest(new { mensaje = "Nombre completo, correo y contraseña son obligatorios." });
            }

            try
            {
                var nuevoUsuario = await usuarioService.CrearUsuarioAsync(request);
                return Results.Created($"/api/usuarios/{nuevoUsuario.IdUsuario}", nuevoUsuario);
            }
            catch (Exception ex)
            {
                return Results.BadRequest(new { mensaje = ex.Message });
            }
        })
        .WithName("CrearUsuario")
        .WithSummary("Crea un nuevo usuario en el sistema");

        usuariosGroup.MapPatch("/{id:guid}/estado", async (
            Guid id,
            [FromQuery] bool activo,
            [FromServices] IUsuarioService usuarioService) =>
        {
            var actualizado = await usuarioService.CambiarEstadoAsync(id, activo);
            return actualizado
                ? Results.Ok(new { mensaje = $"Estado del usuario actualizado a {(activo ? "activo" : "inactivo")}." })
                : Results.NotFound(new { mensaje = $"Usuario con ID {id} no encontrado." });
        })
        .WithName("CambiarEstadoUsuario")
        .WithSummary("Activa o desactiva el acceso de un usuario");

        return routes;
    }
}
