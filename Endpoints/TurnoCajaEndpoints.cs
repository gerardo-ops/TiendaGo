using Microsoft.AspNetCore.Mvc;
using TiendaGo.DTOs.Turnos;
using TiendaGo.Services;

namespace TiendaGo.Endpoints;

public static class TurnoCajaEndpoints
{
    public static IEndpointRouteBuilder MapTurnoCajaEndpoints(this IEndpointRouteBuilder routes)
    {
        var turnosGroup = routes.MapGroup("/api/turnos")
            .WithTags("Turnos de Caja");

        // Apertura de turno de caja
        turnosGroup.MapPost("/abrir", async (
            [FromBody] AbrirTurnoRequest request,
            [FromServices] ITurnoCajaService turnoService) =>
        {
            if (request.IdUsuario == Guid.Empty)
            {
                return Results.BadRequest(new { mensaje = "Se debe especificar un ID de usuario válido." });
            }

            try
            {
                var nuevoTurno = await turnoService.AbrirTurnoAsync(request);
                return Results.Created($"/api/turnos/{nuevoTurno.IdTurno}", nuevoTurno);
            }
            catch (InvalidOperationException ex)
            {
                return Results.Conflict(new { mensaje = ex.Message });
            }
            catch (Exception ex)
            {
                return Results.BadRequest(new { mensaje = ex.Message });
            }
        })
        .RequireAuthorization()
        .WithName("AbrirTurno")
        .WithSummary("Abre un nuevo turno de caja con un monto base inicial");

        // Cierre / Arqueo de turno de caja
        turnosGroup.MapPost("/{id:long}/cerrar", async (
            long id,
            [FromBody] CerrarTurnoRequest request,
            [FromServices] ITurnoCajaService turnoService) =>
        {
            try
            {
                var turnoCerrado = await turnoService.CerrarTurnoAsync(id, request);
                return turnoCerrado != null
                    ? Results.Ok(turnoCerrado)
                    : Results.NotFound(new { mensaje = $"Turno con ID {id} no encontrado." });
            }
            catch (InvalidOperationException ex)
            {
                return Results.Conflict(new { mensaje = ex.Message });
            }
            catch (Exception ex)
            {
                return Results.BadRequest(new { mensaje = ex.Message });
            }
        })
        .RequireAuthorization()
        .WithName("CerrarTurno")
        .WithSummary("Cierra un turno de caja especificando el monto físico declarado para el cuadre");

        // Consultar turno activo por usuario
        turnosGroup.MapGet("/activo/{idUsuario:guid}", async (
            Guid idUsuario,
            [FromServices] ITurnoCajaService turnoService) =>
        {
            var turno = await turnoService.ObtenerTurnoActivoAsync(idUsuario);
            return turno != null
                ? Results.Ok(turno)
                : Results.NotFound(new { mensaje = "El usuario no tiene un turno de caja activo." });
        })
        .RequireAuthorization()
        .WithName("ObtenerTurnoActivo")
        .WithSummary("Consulta el turno de caja abierto actualmente para el usuario especificado");

        // Consultar turno por ID
        turnosGroup.MapGet("/{id:long}", async (
            long id,
            [FromServices] ITurnoCajaService turnoService) =>
        {
            var turno = await turnoService.ObtenerPorIdAsync(id);
            return turno != null
                ? Results.Ok(turno)
                : Results.NotFound(new { mensaje = $"Turno con ID {id} no encontrado." });
        })
        .RequireAuthorization()
        .WithName("ObtenerTurnoPorId")
        .WithSummary("Consulta el detalle de un turno de caja por su ID");

        // Historial de turnos de caja
        turnosGroup.MapGet("/", async ([FromServices] ITurnoCajaService turnoService) =>
        {
            var turnos = await turnoService.ObtenerHistorialAsync();
            return Results.Ok(turnos);
        })
        .RequireAuthorization()
        .WithName("ObtenerHistorialTurnos")
        .WithSummary("Consulta el historial completo de turnos de caja registrados");

        return routes;
    }
}
