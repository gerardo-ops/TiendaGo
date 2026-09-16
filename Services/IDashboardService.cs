using TiendaGo.DTOs.Dashboard;

namespace TiendaGo.Services;

public interface IDashboardService
{
    Task<DashboardResumenResponse> ObtenerResumenAsync();
}
