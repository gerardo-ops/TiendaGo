using AutoMapper;
using TiendaGo.DTOs.Productos;
using TiendaGo.Models;

namespace TiendaGo.Services;

public class ProductoService : IProductoService
{
    private readonly Supabase.Client _supabase;
    private readonly IMapper _mapper;

    public ProductoService(Supabase.Client supabase, IMapper mapper)
    {
        _supabase = supabase;
        _mapper = mapper;
    }

    public async Task<IEnumerable<ProductoResponse>> ObtenerTodosAsync(string? buscar = null, long? idCategoria = null)
    {
        var response = await _supabase.From<Producto>().Get();
        var productos = response.Models.AsEnumerable();

        if (idCategoria.HasValue && idCategoria.Value > 0)
        {
            productos = productos.Where(p => p.IdCategoria == idCategoria.Value);
        }

        if (!string.IsNullOrWhiteSpace(buscar))
        {
            var termino = buscar.Trim().ToLower();
            productos = productos.Where(p =>
                p.NombreProducto.ToLower().Contains(termino) ||
                p.CodigoSku.ToLower().Contains(termino));
        }

        var categoriasDict = await ObtenerDiccionarioCategoriasAsync();
        var resultado = new List<ProductoResponse>();

        foreach (var p in productos)
        {
            if (categoriasDict.TryGetValue(p.IdCategoria, out var cat))
            {
                p.Categoria = cat;
            }
            resultado.Add(_mapper.Map<ProductoResponse>(p));
        }

        return resultado.OrderBy(p => p.NombreProducto);
    }

    public async Task<IEnumerable<ProductoResponse>> ObtenerActivosAsync()
    {
        var response = await _supabase.From<Producto>()
            .Where(p => p.EstadoActivo == true)
            .Get();

        var categoriasDict = await ObtenerDiccionarioCategoriasAsync();
        var resultado = new List<ProductoResponse>();

        foreach (var p in response.Models)
        {
            if (categoriasDict.TryGetValue(p.IdCategoria, out var cat))
            {
                p.Categoria = cat;
            }
            resultado.Add(_mapper.Map<ProductoResponse>(p));
        }

        return resultado.OrderBy(p => p.NombreProducto);
    }

    public async Task<ProductoResponse?> ObtenerPorIdAsync(long id)
    {
        var response = await _supabase.From<Producto>()
            .Where(p => p.IdProducto == id)
            .Get();

        var producto = response.Models.FirstOrDefault();
        if (producto == null) return null;

        var categoriasDict = await ObtenerDiccionarioCategoriasAsync();
        if (categoriasDict.TryGetValue(producto.IdCategoria, out var cat))
        {
            producto.Categoria = cat;
        }

        return _mapper.Map<ProductoResponse>(producto);
    }

    public async Task<ProductoResponse?> ObtenerPorCodigoAsync(string codigoSku)
    {
        var response = await _supabase.From<Producto>()
            .Where(p => p.CodigoSku == codigoSku.Trim())
            .Get();

        var producto = response.Models.FirstOrDefault();
        if (producto == null) return null;

        var categoriasDict = await ObtenerDiccionarioCategoriasAsync();
        if (categoriasDict.TryGetValue(producto.IdCategoria, out var cat))
        {
            producto.Categoria = cat;
        }

        return _mapper.Map<ProductoResponse>(producto);
    }

    public async Task<ProductoResponse> CrearAsync(ProductoRequest request)
    {
        // Validar SKU único
        var existente = await _supabase.From<Producto>()
            .Where(p => p.CodigoSku == request.CodigoSku.Trim())
            .Get();

        if (existente.Models.Count > 0)
        {
            throw new InvalidOperationException($"Ya existe un producto registrado con el código SKU '{request.CodigoSku}'.");
        }

        var producto = _mapper.Map<Producto>(request);
        producto.CodigoSku = request.CodigoSku.Trim();
        producto.FechaCreacion = DateTimeOffset.UtcNow;

        var insertResponse = await _supabase.From<Producto>().Insert(producto);
        var nuevo = insertResponse.Models.FirstOrDefault() ?? producto;

        var categoriasDict = await ObtenerDiccionarioCategoriasAsync();
        if (categoriasDict.TryGetValue(nuevo.IdCategoria, out var cat))
        {
            nuevo.Categoria = cat;
        }

        return _mapper.Map<ProductoResponse>(nuevo);
    }

    public async Task<ProductoResponse?> ActualizarAsync(long id, ProductoRequest request)
    {
        var response = await _supabase.From<Producto>()
            .Where(p => p.IdProducto == id)
            .Get();

        var producto = response.Models.FirstOrDefault();
        if (producto == null) return null;

        // Validar si el SKU cambió y si ya pertenece a otro producto
        if (!string.Equals(producto.CodigoSku, request.CodigoSku.Trim(), StringComparison.OrdinalIgnoreCase))
        {
            var skuExistente = await _supabase.From<Producto>()
                .Where(p => p.CodigoSku == request.CodigoSku.Trim())
                .Get();

            if (skuExistente.Models.Any(p => p.IdProducto != id))
            {
                throw new InvalidOperationException($"El código SKU '{request.CodigoSku}' ya está asignado a otro producto.");
            }
        }

        producto.IdCategoria = request.IdCategoria;
        producto.NombreProducto = request.NombreProducto.Trim();
        producto.CodigoSku = request.CodigoSku.Trim();
        producto.CostoCompra = request.CostoCompra;
        producto.PrecioVenta = request.PrecioVenta;
        producto.StockActual = request.StockActual;
        producto.StockMinimo = request.StockMinimo;
        producto.UrlImagen = request.UrlImagen;
        producto.EstadoActivo = request.EstadoActivo;

        await _supabase.From<Producto>()
            .Where(p => p.IdProducto == id)
            .Update(producto);

        var categoriasDict = await ObtenerDiccionarioCategoriasAsync();
        if (categoriasDict.TryGetValue(producto.IdCategoria, out var cat))
        {
            producto.Categoria = cat;
        }

        return _mapper.Map<ProductoResponse>(producto);
    }

    public async Task<bool> EliminarAsync(long id)
    {
        var response = await _supabase.From<Producto>()
            .Where(p => p.IdProducto == id)
            .Get();

        var producto = response.Models.FirstOrDefault();
        if (producto == null) return false;

        // Baja lógica para mantener consistencia referencial con ventas históricas
        producto.EstadoActivo = false;
        await _supabase.From<Producto>()
            .Where(p => p.IdProducto == id)
            .Update(producto);

        return true;
    }

    private async Task<Dictionary<long, Categoria>> ObtenerDiccionarioCategoriasAsync()
    {
        var catResponse = await _supabase.From<Categoria>().Get();
        return catResponse.Models.ToDictionary(c => c.IdCategoria, c => c);
    }
}
