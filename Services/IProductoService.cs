using TiendaGo.DTOs.Productos;

namespace TiendaGo.Services;

public interface IProductoService
{
    Task<IEnumerable<ProductoResponse>> ObtenerTodosAsync(string? buscar = null, long? idCategoria = null);
    Task<List<ProductoResponse>> ObtenerActivosAsync();
    Task<ProductoResponse?> ObtenerPorIdAsync(long id);
    Task<ProductoResponse?> ObtenerPorIdAsync(int id);
    Task<ProductoResponse?> ObtenerPorCodigoAsync(string codigo);
    Task<ProductoResponse> CrearAsync(ProductoRequest request);
    Task<bool> ActualizarAsync(int id, ProductoRequest request);
    Task<ProductoResponse?> ActualizarAsync(long id, ProductoRequest request);
    Task<bool> EliminarAsync(long id);
}
