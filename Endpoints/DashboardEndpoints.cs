using Microsoft.AspNetCore.Mvc;
using TiendaGo.Services;

namespace TiendaGo.Endpoints;

public static class DashboardEndpoints
{
    public static IEndpointRouteBuilder MapDashboardEndpoints(this IEndpointRouteBuilder routes)
    {
        var dashboardGroup = routes.MapGroup("/api/dashboard")
            .WithTags("Dashboard y Métricas");

        // Obtener resumen del dashboard
        dashboardGroup.MapGet("/resumen", async ([FromServices] IDashboardService dashboardService) =>
        {
            var resumen = await dashboardService.ObtenerResumenAsync();
            return Results.Ok(resumen);
        })
        .RequireAuthorization()
        .WithName("ObtenerResumenDashboard")
        .WithSummary("Obtiene las métricas consolidadas del día y alertas de inventario crítico");

        return routes;
    }
}
