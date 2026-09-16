using AutoMapper;
using Microsoft.EntityFrameworkCore;
using TiendaGo.DTOs.Productos;
using TiendaGo.Models;

namespace TiendaGo.Services;

public class ProductoService : IProductoService
{
    private readonly TiendaGoDbContext _context;
    private readonly IMapper _mapper;

    public ProductoService(TiendaGoDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<IEnumerable<ProductoResponse>> ObtenerTodosAsync(string? buscar = null, long? idCategoria = null)
    {
        var query = _context.Productos
            .Include(p => p.IdCategoriaNavigation)
            .AsNoTracking()
            .AsQueryable();

        if (idCategoria.HasValue && idCategoria.Value > 0)
        {
            query = query.Where(p => p.IdCategoria == idCategoria.Value);
        }

        if (!string.IsNullOrWhiteSpace(buscar))
        {
            var termino = buscar.Trim().ToLower();
            query = query.Where(p =>
                p.NombreProducto.ToLower().Contains(termino) ||
                p.CodigoSku.ToLower().Contains(termino));
        }

        var productos = await query.OrderBy(p => p.NombreProducto).ToListAsync();
        return _mapper.Map<IEnumerable<ProductoResponse>>(productos);
    }

    public async Task<IEnumerable<ProductoResponse>> ObtenerActivosAsync()
    {
        var productos = await _context.Productos
            .Include(p => p.IdCategoriaNavigation)
            .Where(p => p.EstadoActivo)
            .OrderBy(p => p.NombreProducto)
            .AsNoTracking()
            .ToListAsync();

        return _mapper.Map<IEnumerable<ProductoResponse>>(productos);
    }

    public async Task<ProductoResponse?> ObtenerPorIdAsync(long id)
    {
        var producto = await _context.Productos
            .Include(p => p.IdCategoriaNavigation)
            .FirstOrDefaultAsync(p => p.IdProducto == id);

        return producto != null ? _mapper.Map<ProductoResponse>(producto) : null;
    }

    public async Task<ProductoResponse?> ObtenerPorCodigoAsync(string codigoSku)
    {
        if (string.IsNullOrWhiteSpace(codigoSku)) return null;

        var sku = codigoSku.Trim().ToLower();
        var producto = await _context.Productos
            .Include(p => p.IdCategoriaNavigation)
            .FirstOrDefaultAsync(p => p.CodigoSku.ToLower() == sku);

        return producto != null ? _mapper.Map<ProductoResponse>(producto) : null;
    }

    public async Task<ProductoResponse> CrearAsync(ProductoRequest request)
    {
        var sku = (request.CodigoSku ?? request.Codigo ?? string.Empty).Trim();
        var nombre = (request.NombreProducto ?? request.Nombre ?? string.Empty).Trim();

        var existeSku = await _context.Productos.AnyAsync(p => p.CodigoSku.ToLower() == sku.ToLower());
        if (existeSku)
        {
            throw new InvalidOperationException($"Ya existe un producto registrado con el código SKU '{sku}'.");
        }

        var categoriaExiste = await _context.Categorias.AnyAsync(c => c.IdCategoria == request.IdCategoria);
        if (!categoriaExiste)
        {
            throw new InvalidOperationException($"La categoría con ID {request.IdCategoria} no existe.");
        }

        var producto = new Productos
        {
            IdCategoria = request.IdCategoria,
            NombreProducto = nombre,
            CodigoSku = sku,
            CostoCompra = request.CostoCompra,
            PrecioVenta = request.PrecioVenta > 0 ? request.PrecioVenta : (request.Precio ?? 0m),
            StockActual = request.StockActual > 0 ? request.StockActual : (request.Stock ?? 0),
            StockMinimo = request.StockMinimo,
            UrlImagen = request.UrlImagen,
            EstadoActivo = request.Estado ?? request.EstadoActivo,
            FechaCreacion = DateTime.UtcNow
        };

        _context.Productos.Add(producto);
        await _context.SaveChangesAsync();

        await _context.Entry(producto).Reference(p => p.IdCategoriaNavigation).LoadAsync();

        return _mapper.Map<ProductoResponse>(producto);
    }

    public async Task<ProductoResponse?> ActualizarAsync(long id, ProductoRequest request)
    {
        var producto = await _context.Productos
            .Include(p => p.IdCategoriaNavigation)
            .FirstOrDefaultAsync(p => p.IdProducto == id);

        if (producto == null) return null;

        var sku = (request.CodigoSku ?? request.Codigo ?? string.Empty).Trim();
        var nombre = (request.NombreProducto ?? request.Nombre ?? string.Empty).Trim();

        if (!string.Equals(producto.CodigoSku, sku, StringComparison.OrdinalIgnoreCase))
        {
            var skuExiste = await _context.Productos.AnyAsync(p => p.IdProducto != id && p.CodigoSku.ToLower() == sku.ToLower());
            if (skuExiste)
            {
                throw new InvalidOperationException($"El código SKU '{sku}' ya está asignado a otro producto.");
            }
        }

        if (request.IdCategoria > 0 && request.IdCategoria != producto.IdCategoria)
        {
            var catExiste = await _context.Categorias.AnyAsync(c => c.IdCategoria == request.IdCategoria);
            if (!catExiste)
            {
                throw new InvalidOperationException($"La categoría con ID {request.IdCategoria} no existe.");
            }
            producto.IdCategoria = request.IdCategoria;
        }

        producto.NombreProducto = nombre;
        producto.CodigoSku = sku;
        producto.CostoCompra = request.CostoCompra;
        producto.PrecioVenta = request.PrecioVenta > 0 ? request.PrecioVenta : (request.Precio ?? producto.PrecioVenta);
        producto.StockActual = request.StockActual >= 0 ? request.StockActual : (request.Stock ?? producto.StockActual);
        producto.StockMinimo = request.StockMinimo;
        producto.UrlImagen = request.UrlImagen;
        producto.EstadoActivo = request.Estado ?? request.EstadoActivo;

        await _context.SaveChangesAsync();

        await _context.Entry(producto).Reference(p => p.IdCategoriaNavigation).LoadAsync();

        return _mapper.Map<ProductoResponse>(producto);
    }

    public async Task<bool> EliminarAsync(long id)
    {
        var producto = await _context.Productos.FindAsync(id);
        if (producto == null) return false;

        // Baja lógica
        producto.EstadoActivo = false;
        await _context.SaveChangesAsync();

        return true;
    }
}
