using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TiendaGo.DTOs.Categorias;
using TiendaGo.Models;

namespace TiendaGo.Endpoints;

public static class CategoriaEndpoints
{
    public static void MapCategoriaEndpoints(this IEndpointRouteBuilder routes)
    {
        var categoriasGroup = routes.MapGroup("/api/categorias")
            .WithTags("Categorías");

        // Listar categorías (Abierto para catálogo y caja)
        categoriasGroup.MapGet("/", async ([FromServices] TiendaGoDbContext context) =>
        {
            var categorias = await context.Categorias
                .Where(c => c.EstadoActivo)
                .Select(c => new CategoriaResponse
                {
                    IdCategoria = c.IdCategoria,
                    NombreCategoria = c.NombreCategoria,
                    Descripcion = c.Descripcion,
                    EstadoActivo = c.EstadoActivo,
                    TotalProductos = c.Productos.Count(p => p.EstadoActivo)
                })
                .OrderBy(c => c.NombreCategoria)
                .ToListAsync();

            return Results.Ok(categorias);
        })
        .WithName("ObtenerCategorias")
        .WithSummary("Consulta el listado de categorías activas con total de productos asociados");

        // Crear nueva categoría (Solo Admin)
        categoriasGroup.MapPost("/", async (
            [FromBody] CategoriaRequest request,
            [FromServices] TiendaGoDbContext context) =>
        {
            var nombre = (request.Nombre ?? request.NombreCategoria ?? string.Empty).Trim();
            if (string.IsNullOrWhiteSpace(nombre))
            {
                return Results.BadRequest(new { mensaje = "El nombre de la categoría es obligatorio." });
            }

            var existe = await context.Categorias.AnyAsync(c => c.NombreCategoria.ToLower() == nombre.ToLower());
            if (existe)
            {
                return Results.Conflict(new { mensaje = $"Ya existe una categoría registrada como '{nombre}'." });
            }

            var categoria = new Categorias
            {
                NombreCategoria = nombre,
                Descripcion = request.Descripcion,
                EstadoActivo = true
            };

            context.Categorias.Add(categoria);
            await context.SaveChangesAsync();

            var response = new CategoriaResponse
            {
                IdCategoria = categoria.IdCategoria,
                NombreCategoria = categoria.NombreCategoria,
                Descripcion = categoria.Descripcion,
                EstadoActivo = categoria.EstadoActivo,
                TotalProductos = 0
            };

            return Results.Created($"/api/categorias/{categoria.IdCategoria}", response);
        })
        .RequireAuthorization()
        .WithName("CrearCategoria")
        .WithSummary("Crea una nueva categoría de productos");

        // Editar categoría existente (Solo Admin)
        categoriasGroup.MapPut("/{id:long}", async (
            long id,
            [FromBody] CategoriaRequest request,
            [FromServices] TiendaGoDbContext context) =>
        {
            var nombre = (request.Nombre ?? request.NombreCategoria ?? string.Empty).Trim();
            if (string.IsNullOrWhiteSpace(nombre))
            {
                return Results.BadRequest(new { mensaje = "El nuevo nombre de la categoría es obligatorio." });
            }

            var categoria = await context.Categorias.FindAsync(id);
            if (categoria == null)
            {
                return Results.NotFound(new { mensaje = $"Categoría con ID {id} no encontrada." });
            }

            var existeOtro = await context.Categorias.AnyAsync(c => c.IdCategoria != id && c.NombreCategoria.ToLower() == nombre.ToLower());
            if (existeOtro)
            {
                return Results.Conflict(new { mensaje = $"Ya existe otra categoría registrada como '{nombre}'." });
            }

            categoria.NombreCategoria = nombre;
            if (request.Descripcion != null)
            {
                categoria.Descripcion = request.Descripcion;
            }

            await context.SaveChangesAsync();

            return Results.Ok(new CategoriaResponse
            {
                IdCategoria = categoria.IdCategoria,
                NombreCategoria = categoria.NombreCategoria,
                Descripcion = categoria.Descripcion,
                EstadoActivo = categoria.EstadoActivo,
                TotalProductos = await context.Productos.CountAsync(p => p.IdCategoria == id && p.EstadoActivo)
            });
        })
        .RequireAuthorization()
        .WithName("ActualizarCategoria")
        .WithSummary("Actualiza los datos de una categoría");

        // Eliminar categoría (Solo Admin - valida que no tenga productos asociados)
        categoriasGroup.MapDelete("/{id:long}", async (
            long id,
            [FromServices] TiendaGoDbContext context) =>
        {
            var productosAsociados = await context.Productos.CountAsync(p => p.IdCategoria == id && p.EstadoActivo);
            if (productosAsociados > 0)
            {
                return Results.BadRequest(new
                {
                    mensaje = $"No se puede eliminar la categoría porque tiene {productosAsociados} producto(s) asociado(s) en el inventario. Reasigne o elimine los productos primero."
                });
            }

            var categoria = await context.Categorias.FindAsync(id);
            if (categoria == null)
            {
                return Results.NotFound(new { mensaje = $"Categoría con ID {id} no encontrada." });
            }

            // Si nunca tuvo productos, borrado físico; de lo contrario, borrado lógico
            var tuvoProductos = await context.Productos.AnyAsync(p => p.IdCategoria == id);
            if (tuvoProductos)
            {
                categoria.EstadoActivo = false;
            }
            else
            {
                context.Categorias.Remove(categoria);
            }

            await context.SaveChangesAsync();
            return Results.Ok(new { mensaje = $"Categoría '{categoria.NombreCategoria}' eliminada exitosamente." });
        })
        .RequireAuthorization()
        .WithName("EliminarCategoria")
        .WithSummary("Elimina una categoría si no cuenta con productos activos en el catálogo");
    }
}
