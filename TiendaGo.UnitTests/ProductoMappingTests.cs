using AutoMapper;
using FluentAssertions;
using Microsoft.Extensions.DependencyInjection;
using TiendaGo.DTOs.Productos;
using TiendaGo.Mappings;
using TiendaGo.Models;
using Xunit;

namespace TiendaGo.UnitTests;

/// <summary>
/// Suite de pruebas unitarias para validación de DTOs y Mapeo de Objetos (AutoMapper).
/// Aplica el estándar ISO/IEC/IEEE 29119-4 (Nivel 1: Pruebas Unitarias) bajo el patrón AAA (Arrange, Act, Assert).
/// </summary>
public class ProductoMappingTests
{
    private readonly IMapper _mapper;

    public ProductoMappingTests()
    {
        var services = new ServiceCollection();
        services.AddLogging();
        services.AddAutoMapper(cfg =>
        {
            cfg.AddProfile<CatalogoMappingProfile>();
        });

        var serviceProvider = services.BuildServiceProvider();
        _mapper = serviceProvider.GetRequiredService<IMapper>();
    }

    [Fact(DisplayName = "UT-PRD-01: Validar que ProductoRequest se mapee correctamente a la entidad Producto (incluyendo Nombre, Precio, Stock y CategoriaId)")]
    public void UT_PRD_01_ProductoRequest_DeberiaMapearseCorrectamenteAEntidadProducto()
    {
        // -------------------------------------------------------------
        // ARRANGE (Definir el DTO de entrada con datos de catálogo)
        // -------------------------------------------------------------
        var request = new ProductoRequest
        {
            CodigoBarra = "750100019283",
            Nombre = "Galletas de Chocolate 120g",
            Precio = 1.35m,
            Stock = 45,
            IdCategoria = 4,
            Estado = true
        };

        // -------------------------------------------------------------
        // ACT (Ejecutar el mapeo mediante AutoMapper hacia entidades del dominio)
        // -------------------------------------------------------------
        var productoSupabase = _mapper.Map<Producto>(request);
        var productoEf = _mapper.Map<Productos>(request);

        // -------------------------------------------------------------
        // ASSERT (Validar correspondencia exacta campo a campo)
        // -------------------------------------------------------------
        // 1. Validación para modelo Producto (Supabase / Dominio)
        productoSupabase.Should().NotBeNull();
        productoSupabase.NombreProducto.Should().Be(request.Nombre, "el nombre del producto debe coincidir exactamente con el DTO");
        productoSupabase.PrecioVenta.Should().Be(request.Precio, "el precio de venta debe coincidir con el valor del DTO");
        productoSupabase.StockActual.Should().Be(request.Stock, "el stock actual debe inicializarse con el stock provisto en la petición");
        productoSupabase.IdCategoria.Should().Be(request.IdCategoria, "el identificador de categoría foránea debe trasladarse fielmente");
        productoSupabase.CodigoSku.Should().Be(request.CodigoBarra, "el código de barra debe asignarse al SKU del sistema");
        productoSupabase.EstadoActivo.Should().Be(request.Estado, "el estado del producto debe preservarse");

        // 2. Validación para modelo Productos (EF Core / Persistencia Relacional)
        productoEf.Should().NotBeNull();
        productoEf.NombreProducto.Should().Be(request.Nombre);
        productoEf.PrecioVenta.Should().Be(request.Precio);
        productoEf.StockActual.Should().Be(request.Stock);
        productoEf.IdCategoria.Should().Be(request.IdCategoria);
        productoEf.CodigoSku.Should().Be(request.CodigoBarra);
        productoEf.EstadoActivo.Should().Be(request.Estado);
    }
}
