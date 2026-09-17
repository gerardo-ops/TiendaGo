using Microsoft.AspNetCore.Mvc;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Services;

namespace TiendaGo.Endpoints;

public static class UsuarioEndpoints
{
    public static void MapUsuarioEndpoints(this IEndpointRouteBuilder routes)
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
            var usuarioOCorreo = request.UsuarioOCorreo ?? request.CorreoElectronico;
            var password = request.Password ?? request.Clave;

            if (string.IsNullOrWhiteSpace(usuarioOCorreo) || string.IsNullOrWhiteSpace(password))
            {
                return Results.BadRequest(new { mensaje = "El usuario/correo y la contraseña son requeridos." });
            }

            var loginResponse = await usuarioService.LoginAsync(request);
            if (loginResponse == null)
            {
                return Results.Unauthorized();
            }

            return Results.Ok(loginResponse);
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
            var usuarios = await usuarioService.ObtenerUsuariosAsync();
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
            var correo = request.Correo ?? request.CorreoElectronico;
            var nombre = request.Nombre ?? request.NombreCompleto;
            var password = request.Password ?? request.Clave;

            if (string.IsNullOrWhiteSpace(correo) ||
                string.IsNullOrWhiteSpace(password) ||
                string.IsNullOrWhiteSpace(nombre))
            {
                return Results.BadRequest(new { mensaje = "Nombre completo, correo y contraseña son obligatorios." });
            }

            try
            {
                var nuevoUsuario = await usuarioService.RegistrarUsuarioAsync(request);
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
    }
}
