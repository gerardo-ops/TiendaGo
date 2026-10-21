using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.IdentityModel.Tokens;
using TiendaGo.Models;

namespace TiendaGo.IntegrationTests.Infrastructure;

/// <summary>
/// CustomWebApplicationFactory: Reemplaza la conexión PostgreSQL/Supabase por
/// EF Core InMemory aislada (Guid único por ejecución) para pruebas de integración.
/// Implementa el patrón ISO/IEC/IEEE 29119 — Nivel 2 de la Pirámide de Pruebas.
/// </summary>
public class CustomWebApplicationFactory : WebApplicationFactory<Program>
{
    // ─── Identificador único de la BD InMemory por cada instancia de Factory ───
    private readonly string _dbName = $"TiendaGoTestDb_{Guid.NewGuid()}";

    // ─── Constantes de configuración JWT (deben coincidir con appsettings) ────
    public const string JwtKey      = "TuClaveSuperSecretaDeAlMenos32Caracteres!";
    public const string JwtIssuer   = "TiendaGoAPI";
    public const string JwtAudience = "TiendaGoApp";

    // ─── IDs semilla pre-definidos para poder referenciarlos en los tests ─────
    public static readonly Guid IdAdminUsuario  = Guid.Parse("11111111-0000-0000-0000-000000000001");
    public static readonly Guid IdCajeroUsuario = Guid.Parse("22222222-0000-0000-0000-000000000002");
    public const long IdCategoriaPrueba  = 100L;
    public const long IdProducto1        = 1001L;
    public const long IdProducto2        = 1002L;
    public const int  StockInicialP1     = 50;
    public const int  StockInicialP2     = 20;
    public const long IdTurnoPrueba      = 9001L;
    public const long IdMetodoPagoPrueba = 1L;

    // ─── Credenciales de los usuarios semilla ────────────────────────────────
    public const string AdminEmail    = "admin.test@tiendago.com";
    public const string AdminPassword = "Admin123*";
    public const string CajeroEmail   = "cajero.test@tiendago.com";
    public const string CajeroPassword = "Cajero123*";

    /// <summary>
    /// Sobrescribe la configuración de servicios:
    ///   1. Elimina el DbContext real de Npgsql.
    ///   2. Registra el DbContext con InMemory con nombre de BD único.
    ///   3. Siembra los datos necesarios para los casos de prueba.
    /// </summary>
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Testing");

        builder.ConfigureServices(services =>
        {
            // ── Paso 1: Eliminar todos los registros de DbContext con Npgsql ──
            var descriptorsToRemove = services
                .Where(d =>
                    d.ServiceType == typeof(DbContextOptions<TiendaGoDbContext>) ||
                    d.ServiceType == typeof(TiendaGoDbContext) ||
                    (d.ServiceType.IsGenericType &&
                     d.ServiceType.GetGenericTypeDefinition() == typeof(DbContextOptions<>)))
                .ToList();

            foreach (var descriptor in descriptorsToRemove)
            {
                services.Remove(descriptor);
            }

            // ── Paso 2: Registrar TiendaGoDbContext con proveedor InMemory ───
            services.AddDbContext<TiendaGoDbContext>(options =>
            {
                options.UseInMemoryDatabase(_dbName);
                // Desactivar advertencias de transacciones en InMemory
                options.ConfigureWarnings(w =>
                    w.Ignore(Microsoft.EntityFrameworkCore
                        .Diagnostics.InMemoryEventId.TransactionIgnoredWarning));
            });

            // ── Paso 3: Construir el proveedor y sembrar datos ───────────────
            var sp = services.BuildServiceProvider();
            using var scope = sp.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<TiendaGoDbContext>();
            db.Database.EnsureCreated();
            SeedTestData(db);
        });
    }

    // ─────────────────────────────────────────────────────────────────────────
    // SEEDING DE DATOS DETERMINISTAS PARA LOS CASOS DE PRUEBA
    // ─────────────────────────────────────────────────────────────────────────
    private static void SeedTestData(TiendaGoDbContext db)
    {
        // ── Roles ────────────────────────────────────────────────────────────
        if (!db.Roles.Any())
        {
            db.Roles.AddRange(
                new Roles { IdRol = 1, NombreRol = "Administrador", Descripcion = "Acceso total al sistema" },
                new Roles { IdRol = 2, NombreRol = "Cajero",        Descripcion = "Operaciones POS" },
                new Roles { IdRol = 3, NombreRol = "Supervisor",    Descripcion = "Supervisión y arqueo" }
            );
            db.SaveChanges();
        }

        // ── Usuario Administrador de prueba ───────────────────────────────────
        if (!db.Usuarios.Any(u => u.CorreoElectronico == AdminEmail))
        {
            db.Usuarios.Add(new Usuarios
            {
                IdUsuario       = IdAdminUsuario,
                IdRol           = 1,
                NombreCompleto  = "Admin Test",
                CorreoElectronico = AdminEmail,
                ClaveHash       = BCrypt.Net.BCrypt.HashPassword(AdminPassword),
                EstadoActivo    = true,
                FechaRegistro   = DateTime.UtcNow
            });
        }

        // ── Usuario Cajero de prueba ──────────────────────────────────────────
        if (!db.Usuarios.Any(u => u.CorreoElectronico == CajeroEmail))
        {
            db.Usuarios.Add(new Usuarios
            {
                IdUsuario       = IdCajeroUsuario,
                IdRol           = 2,
                NombreCompleto  = "Cajero Test",
                CorreoElectronico = CajeroEmail,
                ClaveHash       = BCrypt.Net.BCrypt.HashPassword(CajeroPassword),
                EstadoActivo    = true,
                FechaRegistro   = DateTime.UtcNow
            });
        }

        db.SaveChanges();

        // ── Categoría de prueba ───────────────────────────────────────────────
        if (!db.Categorias.Any(c => c.IdCategoria == IdCategoriaPrueba))
        {
            db.Categorias.Add(new Categorias
            {
                IdCategoria    = IdCategoriaPrueba,
                NombreCategoria = "Categoría Test",
                Descripcion    = "Categoría para pruebas de integración",
                EstadoActivo   = true
            });
            db.SaveChanges();
        }

        // ── Productos de prueba ───────────────────────────────────────────────
        if (!db.Productos.Any(p => p.IdProducto == IdProducto1))
        {
            db.Productos.Add(new Productos
            {
                IdProducto      = IdProducto1,
                IdCategoria     = IdCategoriaPrueba,
                NombreProducto  = "Producto Test Alfa",
                CodigoSku       = "SKU-TEST-001",
                CostoCompra     = 10.00m,
                PrecioVenta     = 15.00m,
                StockActual     = StockInicialP1,
                StockMinimo     = 5,
                EstadoActivo    = true,
                FechaCreacion   = DateTime.UtcNow
            });
        }

        if (!db.Productos.Any(p => p.IdProducto == IdProducto2))
        {
            db.Productos.Add(new Productos
            {
                IdProducto      = IdProducto2,
                IdCategoria     = IdCategoriaPrueba,
                NombreProducto  = "Producto Test Beta",
                CodigoSku       = "SKU-TEST-002",
                CostoCompra     = 5.00m,
                PrecioVenta     = 8.50m,
                StockActual     = StockInicialP2,
                StockMinimo     = 3,
                EstadoActivo    = true,
                FechaCreacion   = DateTime.UtcNow
            });
        }

        db.SaveChanges();

        // ── Método de Pago ────────────────────────────────────────────────────
        if (!db.MetodosPago.Any(m => m.IdMetodoPago == IdMetodoPagoPrueba))
        {
            db.MetodosPago.Add(new MetodosPago
            {
                IdMetodoPago  = IdMetodoPagoPrueba,
                NombreMetodo  = "Efectivo",
                EstadoActivo  = true
            });
            db.SaveChanges();
        }

        // ── Turno de Caja abierto ─────────────────────────────────────────────
        if (!db.TurnosCaja.Any(t => t.IdTurno == IdTurnoPrueba))
        {
            db.TurnosCaja.Add(new TurnosCaja
            {
                IdTurno              = IdTurnoPrueba,
                IdUsuario            = IdAdminUsuario,
                FechaApertura        = DateTime.UtcNow,
                MontoBaseInicial     = 500.00m,
                TotalVentasEfectivo  = 0m,
                TotalVentasDigital   = 0m,
                EstadoTurno          = "Abierto"
            });
            db.SaveChanges();
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // HELPER: Genera un JWT firmado con la misma clave de Program.cs
    // ─────────────────────────────────────────────────────────────────────────

    /// <summary>
    /// Genera un token JWT válido para el usuario y rol especificados,
    /// usando la misma configuración de seguridad que la API en producción.
    /// </summary>
    /// <param name="username">Nombre de usuario a incluir en los claims</param>
    /// <param name="role">Rol a inyectar en ClaimTypes.Role (e.g. "Administrador", "Cajero")</param>
    /// <param name="userId">GUID del usuario (opcional, genera uno nuevo si no se especifica)</param>
    /// <returns>Token JWT Bearer como cadena de texto</returns>
    public string GenerateJwtToken(string username, string role, Guid? userId = null)
    {
        var key   = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(JwtKey));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var uid = userId ?? Guid.NewGuid();

        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, uid.ToString()),
            new(ClaimTypes.Name,           username),
            new(ClaimTypes.Email,          $"{username.ToLower().Replace(" ", ".")}@tiendago.com"),
            new(ClaimTypes.Role,           role),
            new("id_rol",                  role == "Administrador" ? "1" : role == "Cajero" ? "2" : "3")
        };

        var token = new JwtSecurityToken(
            issuer:            JwtIssuer,
            audience:          JwtAudience,
            claims:            claims,
            expires:           DateTime.UtcNow.AddHours(8),
            signingCredentials: creds
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    /// <summary>
    /// Genera el header Bearer listo para asignarlo a HttpClient.
    /// </summary>
    public System.Net.Http.Headers.AuthenticationHeaderValue GetBearerHeader(string username, string role, Guid? userId = null)
    {
        var token = GenerateJwtToken(username, role, userId);
        return new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);
    }
}
