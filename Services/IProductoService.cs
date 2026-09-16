using TiendaGo.DTOs.Productos;

namespace TiendaGo.Services;

public interface IProductoService
{
    Task<IEnumerable<ProductoResponse>> ObtenerTodosAsync(string? buscar = null, long? idCategoria = null);
    Task<IEnumerable<ProductoResponse>> ObtenerActivosAsync();
    Task<ProductoResponse?> ObtenerPorIdAsync(long id);
    Task<ProductoResponse?> ObtenerPorCodigoAsync(string codigoSku);
    Task<ProductoResponse> CrearAsync(ProductoRequest request);
    Task<ProductoResponse?> ActualizarAsync(long id, ProductoRequest request);
    Task<bool> EliminarAsync(long id);
}
