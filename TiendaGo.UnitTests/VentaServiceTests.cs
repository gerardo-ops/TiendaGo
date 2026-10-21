using AutoMapper;
using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Moq;
using TiendaGo.DTOs.Ventas;
using TiendaGo.Models;
using TiendaGo.Services;
using Xunit;

namespace TiendaGo.UnitTests;

/// <summary>
/// Suite de pruebas unitarias para VentaService (Lógica de Punto de Venta POS y Control de Inventario).
/// Aplica el estándar ISO/IEC/IEEE 29119-4 (Nivel 1: Pruebas Unitarias) bajo el patrón AAA (Arrange, Act, Assert).
/// </summary>
public class VentaServiceTests
{
    private readonly IMapper _mapper;

    public VentaServiceTests()
    {
        var mapperMock = new Mock<IMapper>();
        _mapper = mapperMock.Object;
    }

    private static TiendaGoDbContext CreateInMemoryDbContext()
    {
        var options = new DbContextOptionsBuilder<TiendaGoDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        return new TiendaGoDbContext(options);
    }

    [Fact(DisplayName = "UT-POS-01: Validar cálculo exacto de subtotales, IVA y vuelto/cambio ante pago en efectivo")]
    public async Task UT_POS_01_RegistrarVenta_DeberiaCalcularSubtotalIvaYCambioExactos_AntePagoEnEfectivo()
    {
        // -------------------------------------------------------------
        // ARRANGE (Organizar el escenario de prueba)
        // -------------------------------------------------------------
        using var context = CreateInMemoryDbContext();

        var usuarioId = Guid.NewGuid();
        var usuario = new Usuarios
        {
            IdUsuario = usuarioId,
            IdRol = 1,
            NombreCompleto = "Gerardo Batres (Cajero)",
            CorreoElectronico = "cajero_pos@tiendago.com",
            ClaveHash = "dummy_hash",
            EstadoActivo = true,
            FechaRegistro = DateTime.UtcNow
        };

        var turno = new TurnosCaja
        {
            IdTurno = 1,
            IdUsuario = usuarioId,
            EstadoTurno = "Abierto",
            FechaApertura = DateTime.UtcNow,
            MontoBaseInicial = 50.00m,
            TotalVentasEfectivo = 0m,
            TotalVentasDigital = 0m
        };

        var metodoPago = new MetodosPago
        {
            IdMetodoPago = 1,
            NombreMetodo = "Efectivo",
            EstadoActivo = true
        };

        var producto = new Productos
        {
            IdProducto = 1,
            IdCategoria = 1,
            NombreProducto = "Bebida Energizante",
            CodigoSku = "BEB-001",
            PrecioVenta = 2.50m,
            CostoCompra = 1.50m,
            StockActual = 20,
            StockMinimo = 5,
            EstadoActivo = true,
            FechaCreacion = DateTime.UtcNow
        };

        context.Usuarios.Add(usuario);
        context.TurnosCaja.Add(turno);
        context.MetodosPago.Add(metodoPago);
        context.Productos.Add(producto);
        await context.SaveChangesAsync();

        var service = new VentaService(context, _mapper);

        // Venta de 2 unidades a $2.50 c/u => Total: $5.00
        // Pago en efectivo con billete de $10.00
        // Subtotal esperado (sin IVA): $4.42, IVA (13%): $0.58, Vuelto/Cambio: $5.00
        var request = new VentaRequest
        {
            IdTurno = turno.IdTurno,
            IdUsuario = usuarioId,
            IdMetodoPago = 1,
            MontoRecibido = 10.00m,
            Detalles = new List<DetalleVentaRequest>
            {
                new()
                {
                    IdProducto = producto.IdProducto,
                    Cantidad = 2,
                    PrecioUnitarioHistorico = 2.50m
                }
            }
        };

        // -------------------------------------------------------------
        // ACT (Ejecutar la acción bajo prueba)
        // -------------------------------------------------------------
        var response = await service.RegistrarVentaAsync(request);

        // -------------------------------------------------------------
        // ASSERT (Verificar resultados esperados)
        // -------------------------------------------------------------
        response.Should().NotBeNull();
        response.TotalVenta.Should().Be(5.00m, "porque 2 unidades a $2.50 equivalen exactamente a $5.00");
        response.Subtotal.Should().Be(4.42m, "porque el subtotal base sin el 13% de IVA redondeado es $4.42");
        response.TotalIva.Should().Be(0.58m, "porque el impuesto del 13% sobre $5.00 corresponde a $0.58");
        response.CambioEntregado.Should().Be(5.00m, "porque el cliente pagó con $10.00 para una compra de $5.00");
        response.MontoRecibido.Should().Be(10.00m);
        response.EstadoVenta.Should().Be("Completada");

        // Coherencia contable: Subtotal + IVA = Total
        (response.Subtotal + response.TotalIva).Should().Be(response.TotalVenta);
    }

    [Fact(DisplayName = "UT-POS-02: Validar que al procesar una venta se descuente la cantidad correcta de unidades del inventario (usando EF Core InMemory)")]
    public async Task UT_POS_02_RegistrarVenta_DeberiaDescontarStockCorrectoDeInventario_EnBaseDeDatos()
    {
        // -------------------------------------------------------------
        // ARRANGE (Organizar el escenario de prueba)
        // -------------------------------------------------------------
        using var context = CreateInMemoryDbContext();

        var usuarioId = Guid.NewGuid();
        var usuario = new Usuarios
        {
            IdUsuario = usuarioId,
            IdRol = 1,
            NombreCompleto = "Elmer Tesorero (Cajero)",
            CorreoElectronico = "cajero2_pos@tiendago.com",
            ClaveHash = "dummy_hash",
            EstadoActivo = true,
            FechaRegistro = DateTime.UtcNow
        };

        var turno = new TurnosCaja
        {
            IdTurno = 2,
            IdUsuario = usuarioId,
            EstadoTurno = "Abierto",
            FechaApertura = DateTime.UtcNow,
            MontoBaseInicial = 100.00m
        };

        var metodoPago = new MetodosPago
        {
            IdMetodoPago = 1,
            NombreMetodo = "Efectivo",
            EstadoActivo = true
        };

        const int stockInicial = 15;
        const int cantidadVendida = 3;
        const int stockEsperado = stockInicial - cantidadVendida; // 12

        var producto = new Productos
        {
            IdProducto = 10,
            IdCategoria = 1,
            NombreProducto = "Café Gourmet 500g",
            CodigoSku = "CAF-500",
            PrecioVenta = 4.00m,
            CostoCompra = 2.50m,
            StockActual = stockInicial,
            StockMinimo = 5,
            EstadoActivo = true,
            FechaCreacion = DateTime.UtcNow
        };

        context.Usuarios.Add(usuario);
        context.TurnosCaja.Add(turno);
        context.MetodosPago.Add(metodoPago);
        context.Productos.Add(producto);
        await context.SaveChangesAsync();

        var service = new VentaService(context, _mapper);

        var request = new VentaRequest
        {
            IdTurno = turno.IdTurno,
            IdUsuario = usuarioId,
            IdMetodoPago = 1,
            MontoRecibido = 20.00m,
            Detalles = new List<DetalleVentaRequest>
            {
                new()
                {
                    IdProducto = producto.IdProducto,
                    Cantidad = cantidadVendida,
                    PrecioUnitarioHistorico = 4.00m
                }
            }
        };

        // -------------------------------------------------------------
        // ACT (Ejecutar la venta)
        // -------------------------------------------------------------
        var response = await service.RegistrarVentaAsync(request);

        // -------------------------------------------------------------
        // ASSERT (Verificar descuento físico en la base de datos InMemory)
        // -------------------------------------------------------------
        response.Should().NotBeNull();
        response.EstadoVenta.Should().Be("Completada");

        // Consultar el estado persistido en el DbContext
        var productoPersistido = await context.Productos.FindAsync(producto.IdProducto);
        productoPersistido.Should().NotBeNull();
        productoPersistido!.StockActual.Should().Be(stockEsperado,
            $"porque se vendieron {cantidadVendida} unidades a partir de un inventario inicial de {stockInicial}");

        // Verificar registro de líneas de detalle
        var detalleEnDb = await context.DetallesVenta.FirstOrDefaultAsync(d => d.IdProducto == producto.IdProducto);
        detalleEnDb.Should().NotBeNull();
        detalleEnDb!.Cantidad.Should().Be(cantidadVendida);
    }

    [Fact(DisplayName = "UT-POS-03: Validar que si la cantidad solicitada supera el stock actual disponible, el método lance una excepción de negocio (InvalidOperationException) con mensaje 'Stock insuficiente' y no altere la base de datos")]
    public async Task UT_POS_03_RegistrarVenta_DeberiaLanzarExcepcion_YNoModificarBaseDeDatos_CuandoStockEsInsuficiente()
    {
        // -------------------------------------------------------------
        // ARRANGE (Organizar el escenario con stock menor al solicitado)
        // -------------------------------------------------------------
        using var context = CreateInMemoryDbContext();

        var usuarioId = Guid.NewGuid();
        var usuario = new Usuarios
        {
            IdUsuario = usuarioId,
            IdRol = 1,
            NombreCompleto = "Jason Bautista (Cajero)",
            CorreoElectronico = "cajero3_pos@tiendago.com",
            ClaveHash = "dummy_hash",
            EstadoActivo = true,
            FechaRegistro = DateTime.UtcNow
        };

        var turno = new TurnosCaja
        {
            IdTurno = 3,
            IdUsuario = usuarioId,
            EstadoTurno = "Abierto",
            FechaApertura = DateTime.UtcNow,
            MontoBaseInicial = 50.00m
        };

        const int stockDisponible = 2;
        const int cantidadDemandada = 5; // Supera el stock

        var producto = new Productos
        {
            IdProducto = 20,
            IdCategoria = 1,
            NombreProducto = "Snack Papas Fritas",
            CodigoSku = "SNK-001",
            PrecioVenta = 1.00m,
            CostoCompra = 0.60m,
            StockActual = stockDisponible,
            StockMinimo = 5,
            EstadoActivo = true,
            FechaCreacion = DateTime.UtcNow
        };

        context.Usuarios.Add(usuario);
        context.TurnosCaja.Add(turno);
        context.Productos.Add(producto);
        await context.SaveChangesAsync();

        var service = new VentaService(context, _mapper);

        var request = new VentaRequest
        {
            IdTurno = turno.IdTurno,
            IdUsuario = usuarioId,
            IdMetodoPago = 1,
            MontoRecibido = 10.00m,
            Detalles = new List<DetalleVentaRequest>
            {
                new()
                {
                    IdProducto = producto.IdProducto,
                    Cantidad = cantidadDemandada,
                    PrecioUnitarioHistorico = 1.00m
                }
            }
        };

        // -------------------------------------------------------------
        // ACT (Intentar registrar venta con stock insuficiente)
        // -------------------------------------------------------------
        Func<Task> accion = async () => await service.RegistrarVentaAsync(request);

        // -------------------------------------------------------------
        // ASSERT (Excepción de negocio y reversión/inalterabilidad de BD)
        // -------------------------------------------------------------
        var exception = await accion.Should().ThrowAsync<InvalidOperationException>(
            "porque no se puede despachar más mercancía de la que existe en bodega");

        exception.WithMessage("*Stock insuficiente*");

        // Verificar que la base de datos permanece totalmente intacta (Integridad transaccional ACID)
        var productoSinAlterar = await context.Productos.FindAsync(producto.IdProducto);
        productoSinAlterar.Should().NotBeNull();
        productoSinAlterar!.StockActual.Should().Be(stockDisponible,
            "el stock original no debió ser decrementado ni modificado");

        var ventasPersistidas = await context.Ventas.ToListAsync();
        ventasPersistidas.Should().BeEmpty("no debe haberse insertado ningún encabezado de venta huérfano");

        var detallesPersistidos = await context.DetallesVenta.ToListAsync();
        detallesPersistidos.Should().BeEmpty("no debe haberse insertado ninguna línea de detalle");
    }
}
