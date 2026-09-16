using Microsoft.AspNetCore.Mvc;
using TiendaGo.DTOs.Ventas;
using TiendaGo.Services;

namespace TiendaGo.Endpoints;

public static class VentaEndpoints
{
    public static IEndpointRouteBuilder MapVentaEndpoints(this IEndpointRouteBuilder routes)
    {
        var ventasGroup = routes.MapGroup("/api/ventas")
            .WithTags("Ventas POS");

        // Registrar nueva venta (Proceso ACID)
        ventasGroup.MapPost("/", async (
            [FromBody] VentaRequest request,
            [FromServices] IVentaService ventaService) =>
        {
            if (request.IdTurno <= 0 || request.IdUsuario == Guid.Empty || request.IdMetodoPago <= 0)
            {
                return Results.BadRequest(new { mensaje = "El turno, usuario y método de pago son campos obligatorios." });
            }

            try
            {
                var nuevaVenta = await ventaService.RegistrarVentaAsync(request);
                return Results.Created($"/api/ventas/{nuevaVenta.IdVenta}", nuevaVenta);
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
        .WithName("RegistrarVenta")
        .WithSummary("Procesa y registra una nueva transacción de venta POS de forma atómica (ACID)");

        // Obtener venta por ID
        ventasGroup.MapGet("/{id:long}", async (
            long id,
            [FromServices] IVentaService ventaService) =>
        {
            var venta = await ventaService.ObtenerPorIdAsync(id);
            return venta != null
                ? Results.Ok(venta)
                : Results.NotFound(new { mensaje = $"Venta con ID {id} no encontrada." });
        })
        .RequireAuthorization()
        .WithName("ObtenerVentaPorId")
        .WithSummary("Consulta los detalles de un ticket de venta por su ID");

        // Obtener ventas por turno de caja
        ventasGroup.MapGet("/turno/{idTurno:long}", async (
            long idTurno,
            [FromServices] IVentaService ventaService) =>
        {
            var ventas = await ventaService.ObtenerPorTurnoAsync(idTurno);
            return Results.Ok(ventas);
        })
        .RequireAuthorization()
        .WithName("ObtenerVentasPorTurno")
        .WithSummary("Consulta el listado de ventas procesadas durante un turno de caja específico");

        // Anular venta
        ventasGroup.MapPost("/{id:long}/anular", async (
            long id,
            [FromServices] IVentaService ventaService) =>
        {
            try
            {
                var anulada = await ventaService.AnularVentaAsync(id);
                return anulada
                    ? Results.Ok(new { mensaje = $"La venta #{id} ha sido anulada exitosamente y el inventario reincorporado." })
                    : Results.NotFound(new { mensaje = $"Venta con ID {id} no encontrada o ya se encuentra anulada." });
            }
            catch (Exception ex)
            {
                return Results.BadRequest(new { mensaje = ex.Message });
            }
        })
        .RequireAuthorization()
        .WithName("AnularVenta")
        .WithSummary("Anula una venta previa y devuelve las unidades al inventario");

        return routes;
    }
}
