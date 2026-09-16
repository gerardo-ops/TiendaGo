using Microsoft.AspNetCore.Mvc;
using TiendaGo.DTOs.Productos;
using TiendaGo.Services;

namespace TiendaGo.Endpoints;

public static class ProductoEndpoints
{
    public static IEndpointRouteBuilder MapProductoEndpoints(this IEndpointRouteBuilder routes)
    {
        // =============================================
        // GRUPO: /api/productos (Catálogo e Inventario)
        // =============================================
        var productosGroup = routes.MapGroup("/api/productos")
            .WithTags("Productos");

        // Listar productos con filtros de búsqueda y categoría
        productosGroup.MapGet("/", async (
            [FromQuery] string? buscar,
            [FromQuery] long? categoria,
            [FromServices] IProductoService productoService) =>
        {
            var productos = await productoService.ObtenerTodosAsync(buscar, categoria);
            return Results.Ok(productos);
        })
        .WithName("ObtenerProductos")
        .WithSummary("Consulta el catálogo de productos con soporte para búsqueda y filtro por categoría");

        // Listar productos activos (para Terminal POS)
        productosGroup.MapGet("/activos", async ([FromServices] IProductoService productoService) =>
        {
            var productos = await productoService.ObtenerActivosAsync();
            return Results.Ok(productos);
        })
        .WithName("ObtenerProductosActivos")
        .WithSummary("Consulta los productos activos disponibles para la terminal POS");

        // Obtener producto por ID
        productosGroup.MapGet("/{id:long}", async (
            long id,
            [FromServices] IProductoService productoService) =>
        {
            var producto = await productoService.ObtenerPorIdAsync(id);
            return producto != null
                ? Results.Ok(producto)
                : Results.NotFound(new { mensaje = $"Producto con ID {id} no encontrado." });
        })
        .WithName("ObtenerProductoPorId")
        .WithSummary("Consulta la ficha detallada de un producto por su ID");

        // Obtener producto por código SKU / barras (escáner cámara)
        productosGroup.MapGet("/sku/{sku}", async (
            string sku,
            [FromServices] IProductoService productoService) =>
        {
            var producto = await productoService.ObtenerPorCodigoAsync(sku);
            return producto != null
                ? Results.Ok(producto)
                : Results.NotFound(new { mensaje = $"Producto con código SKU '{sku}' no encontrado." });
        })
        .WithName("ObtenerProductoPorSku")
        .WithSummary("Consulta un producto por código de barras o SKU");

        // Crear nuevo producto
        productosGroup.MapPost("/", async (
            [FromBody] ProductoRequest request,
            [FromServices] IProductoService productoService) =>
        {
            if (string.IsNullOrWhiteSpace(request.NombreProducto) || string.IsNullOrWhiteSpace(request.CodigoSku))
            {
                return Results.BadRequest(new { mensaje = "El nombre y el código SKU del producto son requeridos." });
            }

            if (request.IdCategoria <= 0)
            {
                return Results.BadRequest(new { mensaje = "Debe asignar una categoría válida al producto." });
            }

            try
            {
                var nuevoProducto = await productoService.CrearAsync(request);
                return Results.Created($"/api/productos/{nuevoProducto.IdProducto}", nuevoProducto);
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
        .WithName("CrearProducto")
        .WithSummary("Registra un nuevo producto en el catálogo e inventario");

        // Editar producto existente
        productosGroup.MapPut("/{id:long}", async (
            long id,
            [FromBody] ProductoRequest request,
            [FromServices] IProductoService productoService) =>
        {
            if (string.IsNullOrWhiteSpace(request.NombreProducto) || string.IsNullOrWhiteSpace(request.CodigoSku))
            {
                return Results.BadRequest(new { mensaje = "El nombre y el código SKU del producto son requeridos." });
            }

            try
            {
                var actualizado = await productoService.ActualizarAsync(id, request);
                return actualizado != null
                    ? Results.Ok(actualizado)
                    : Results.NotFound(new { mensaje = $"Producto con ID {id} no encontrado." });
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
        .WithName("ActualizarProducto")
        .WithSummary("Actualiza los datos, existencias o precios de un producto");

        // Eliminar producto (baja lógica)
        productosGroup.MapDelete("/{id:long}", async (
            long id,
            [FromServices] IProductoService productoService) =>
        {
            var eliminado = await productoService.EliminarAsync(id);
            return eliminado
                ? Results.NoContent()
                : Results.NotFound(new { mensaje = $"Producto con ID {id} no encontrado." });
        })
        .RequireAuthorization()
        .WithName("EliminarProducto")
        .WithSummary("Desactiva o da de baja un producto del catálogo");

        return routes;
    }
}
