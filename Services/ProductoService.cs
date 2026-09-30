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
            .Where(p => p.EstadoActivo)
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

    public async Task<List<ProductoResponse>> ObtenerActivosAsync()
    {
        var productos = await _context.Productos
            .Include(p => p.IdCategoriaNavigation)
            .Where(p => p.EstadoActivo)
            .OrderBy(p => p.NombreProducto)
            .AsNoTracking()
            .ToListAsync();

        return _mapper.Map<List<ProductoResponse>>(productos);
    }

    public async Task<ProductoResponse?> ObtenerPorIdAsync(long id)
    {
        var producto = await _context.Productos
            .Include(p => p.IdCategoriaNavigation)
            .FirstOrDefaultAsync(p => p.IdProducto == id);

        return producto != null ? _mapper.Map<ProductoResponse>(producto) : null;
    }

    public async Task<ProductoResponse?> ObtenerPorIdAsync(int id)
    {
        return await ObtenerPorIdAsync((long)id);
    }

    public async Task<ProductoResponse?> ObtenerPorCodigoAsync(string codigo)
    {
        if (string.IsNullOrWhiteSpace(codigo)) return null;

        var codigoLimpio = codigo.Trim();
        var codigoSinEspacios = codigoLimpio.Replace(" ", "");

        // Búsqueda insensible a formato, espacios y mayúsculas/minúsculas para códigos QR o barras de productos activos
        var producto = await _context.Productos
            .Include(p => p.IdCategoriaNavigation)
            .AsNoTracking()
            .FirstOrDefaultAsync(p => p.EstadoActivo &&
                (p.CodigoSku.ToLower() == codigoLimpio.ToLower() ||
                 p.CodigoSku.ToLower() == codigoSinEspacios.ToLower() ||
                 p.CodigoSku.Replace(" ", "").ToLower() == codigoSinEspacios.ToLower()));

        return producto != null ? _mapper.Map<ProductoResponse>(producto) : null;
    }

    public async Task<ProductoResponse> CrearAsync(ProductoRequest request)
    {
        var sku = (request.CodigoSku ?? request.CodigoBarra ?? request.Codigo ?? string.Empty).Trim();
        var nombre = (request.NombreProducto ?? request.Nombre ?? string.Empty).Trim();

        var existeSku = await _context.Productos.AnyAsync(p => p.CodigoSku.ToLower() == sku.ToLower());
        if (existeSku)
        {
            throw new InvalidOperationException($"Ya existe un producto registrado con el código SKU/barras '{sku}'.");
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
            PrecioVenta = request.PrecioVenta > 0 ? request.PrecioVenta : request.Precio,
            StockActual = request.StockActual > 0 ? request.StockActual : request.Stock,
            StockMinimo = request.StockMinimo,
            UrlImagen = NormalizarYGuardarImagen(request.UrlImagen, sku),
            EstadoActivo = request.EstadoActivo,
            FechaCreacion = DateTime.UtcNow
        };

        _context.Productos.Add(producto);
        await _context.SaveChangesAsync();

        await _context.Entry(producto).Reference(p => p.IdCategoriaNavigation).LoadAsync();

        return _mapper.Map<ProductoResponse>(producto);
    }

    public async Task<bool> ActualizarAsync(int id, ProductoRequest request)
    {
        var res = await ActualizarAsync((long)id, request);
        return res != null;
    }

    public async Task<ProductoResponse?> ActualizarAsync(long id, ProductoRequest request)
    {
        var producto = await _context.Productos
            .Include(p => p.IdCategoriaNavigation)
            .FirstOrDefaultAsync(p => p.IdProducto == id);

        if (producto == null) return null;

        var sku = (request.CodigoSku ?? request.CodigoBarra ?? request.Codigo ?? string.Empty).Trim();
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
        producto.PrecioVenta = request.PrecioVenta > 0 ? request.PrecioVenta : request.Precio;
        producto.StockActual = request.StockActual >= 0 ? request.StockActual : request.Stock;
        producto.StockMinimo = request.StockMinimo;
        if (!string.IsNullOrWhiteSpace(request.UrlImagen))
        {
            producto.UrlImagen = NormalizarYGuardarImagen(request.UrlImagen, sku);
        }
        producto.EstadoActivo = request.EstadoActivo;

        await _context.SaveChangesAsync();

        await _context.Entry(producto).Reference(p => p.IdCategoriaNavigation).LoadAsync();

        return _mapper.Map<ProductoResponse>(producto);
    }

    public async Task<bool> EliminarAsync(long id)
    {
        var producto = await _context.Productos.FindAsync(id);
        if (producto == null) return false;

        // Comprobar si el producto ya tiene ventas registradas en el historial (DetallesVenta)
        var tieneVentas = await _context.DetallesVenta.AnyAsync(dv => dv.IdProducto == id);

        if (tieneVentas)
        {
            // Borrado lógico: Cambiar bandera a inactivo para no violar la FK del historial de ventas
            producto.EstadoActivo = false;
            await _context.SaveChangesAsync();
        }
        else
        {
            // Borrado físico real si nunca ha tenido ventas asociadas
            try
            {
                _context.Productos.Remove(producto);
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                // Fallback seguro a borrado lógico ante cualquier otra restricción de FK
                _context.Entry(producto).State = EntityState.Unchanged;
                producto.EstadoActivo = false;
                await _context.SaveChangesAsync();
            }
        }

        return true;
    }

    private static string? NormalizarYGuardarImagen(string? imagenRaw, string sku)
    {
        if (string.IsNullOrWhiteSpace(imagenRaw)) return null;

        // Si ya es una URL HTTP o relativa estándar (/uploads/...) y tiene longitud prudente
        if (imagenRaw.StartsWith("http://", StringComparison.OrdinalIgnoreCase) ||
            imagenRaw.StartsWith("https://", StringComparison.OrdinalIgnoreCase) ||
            imagenRaw.StartsWith("/uploads/", StringComparison.OrdinalIgnoreCase))
        {
            return imagenRaw.Length <= 300 ? imagenRaw : imagenRaw.Substring(0, 300);
        }

        // Si viene en Base64 (con o sin prefijo data:image/...)
        try
        {
            var base64Data = imagenRaw;
            if (base64Data.Contains(","))
            {
                base64Data = base64Data.Substring(base64Data.IndexOf(",") + 1);
            }

            var bytes = Convert.FromBase64String(base64Data.Trim());
            var uploadsDir = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "uploads", "productos");
            if (!Directory.Exists(uploadsDir))
            {
                Directory.CreateDirectory(uploadsDir);
            }

            var safeSku = string.Concat(sku.Where(char.IsLetterOrDigit));
            if (string.IsNullOrEmpty(safeSku)) safeSku = "prod";
            var fileName = $"{safeSku}_{Guid.NewGuid():N}.jpg";
            var filePath = Path.Combine(uploadsDir, fileName);

            File.WriteAllBytes(filePath, bytes);
            return $"/uploads/productos/{fileName}";
        }
        catch
        {
            // Si no era Base64 válido pero es un string corto, guardarlo directamente
            return imagenRaw.Length <= 300 ? imagenRaw : null;
        }
    }
}
