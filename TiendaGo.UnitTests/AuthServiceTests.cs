using AutoMapper;
using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Moq;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;
using TiendaGo.Services;
using Xunit;

namespace TiendaGo.UnitTests;

/// <summary>
/// Suite de pruebas unitarias para AuthService / UsuarioService (Autenticación, Emisión de Tokens JWT y Seguridad).
/// Aplica el estándar ISO/IEC/IEEE 29119-4 (Nivel 1: Pruebas Unitarias) bajo el patrón AAA (Arrange, Act, Assert).
/// </summary>
public class AuthServiceTests
{
    private readonly IMapper _mapper;
    private readonly IConfiguration _configuration;

    public AuthServiceTests()
    {
        var mapperMock = new Mock<IMapper>();
        _mapper = mapperMock.Object;

        var inMemorySettings = new Dictionary<string, string?>
        {
            { "Jwt:Key", "TuClaveSuperSecretaDeAlMenos32Caracteres!12345" },
            { "Jwt:Issuer", "TiendaGoAPI" },
            { "Jwt:Audience", "TiendaGoApp" },
            { "Jwt:ExpirationHours", "8" }
        };

        _configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(inMemorySettings)
            .Build();
    }

    private static TiendaGoDbContext CreateInMemoryDbContext()
    {
        var options = new DbContextOptionsBuilder<TiendaGoDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        return new TiendaGoDbContext(options);
    }

    [Theory(DisplayName = "UT-AUTH-01: Validar que Login con credenciales válidas retorne el DTO con el token JWT y el rol correspondiente ('Administrador' o 'Cajero')")]
    [InlineData("admin@tiendago.com", "Admin123*", "Administrador", "Gerardo Batres (Admin)")]
    [InlineData("cajero@tiendago.com", "Cajero123*", "Cajero", "Elmer Tesorero (Cajero)")]
    public async Task UT_AUTH_01_Login_ConCredencialesValidas_DeberiaRetornarTokenJWTYRolCorrespondiente(
        string correo, string passwordPlano, string rolEsperado, string nombreCompleto)
    {
        // -------------------------------------------------------------
        // ARRANGE (Sembrar usuarios y roles con hash criptográfico BCrypt)
        // -------------------------------------------------------------
        using var context = CreateInMemoryDbContext();

        var rolAdmin = new Roles { IdRol = 1, NombreRol = "Administrador", Descripcion = "Administrador" };
        var rolCajero = new Roles { IdRol = 2, NombreRol = "Cajero", Descripcion = "Cajero" };
        context.Roles.AddRange(rolAdmin, rolCajero);

        var usuarioId = Guid.NewGuid();
        var claveHash = BCrypt.Net.BCrypt.HashPassword(passwordPlano);

        var usuario = new Usuarios
        {
            IdUsuario = usuarioId,
            IdRol = rolEsperado == "Administrador" ? 1 : 2,
            IdRolNavigation = rolEsperado == "Administrador" ? rolAdmin : rolCajero,
            NombreCompleto = nombreCompleto,
            CorreoElectronico = correo,
            ClaveHash = claveHash,
            EstadoActivo = true,
            FechaRegistro = DateTime.UtcNow
        };

        context.Usuarios.Add(usuario);
        await context.SaveChangesAsync();

        var authService = new AuthService(context, _mapper, _configuration);

        var request = new LoginRequest
        {
            UsuarioOCorreo = correo,
            Password = passwordPlano
        };

        // -------------------------------------------------------------
        // ACT (Intentar inicio de sesión)
        // -------------------------------------------------------------
        var response = await authService.LoginAsync(request);

        // -------------------------------------------------------------
        // ASSERT (Verificar token JWT, rol y persistencia de claims)
        // -------------------------------------------------------------
        response.Should().NotBeNull("porque las credenciales suministradas son legítimas y activas");
        response!.Token.Should().NotBeNullOrWhiteSpace("debe generarse un token Bearer JWT firmado criptográficamente");
        response.Rol.Should().Be(rolEsperado, $"el usuario autenticado ostenta el rol {rolEsperado}");
        response.Nombre.Should().Be(nombreCompleto);
        response.IdUsuarioGuid.Should().Be(usuarioId);
        response.Expiracion.Should().BeAfter(DateTime.UtcNow, "la vigencia del token debe estar en el futuro");
    }

    [Fact(DisplayName = "UT-AUTH-02: Validar que Login con contraseña incorrecta retorne null o lance UnauthorizedAccessException")]
    public async Task UT_AUTH_02_Login_ConPasswordIncorrecto_DeberiaRetornarNull()
    {
        // -------------------------------------------------------------
        // ARRANGE (Sembrar usuario con clave legítima)
        // -------------------------------------------------------------
        using var context = CreateInMemoryDbContext();

        var rol = new Roles { IdRol = 1, NombreRol = "Administrador" };
        context.Roles.Add(rol);

        var usuario = new Usuarios
        {
            IdUsuario = Guid.NewGuid(),
            IdRol = 1,
            IdRolNavigation = rol,
            NombreCompleto = "Bayron Díaz",
            CorreoElectronico = "seguridad@tiendago.com",
            ClaveHash = BCrypt.Net.BCrypt.HashPassword("ClaveSegura123*"),
            EstadoActivo = true,
            FechaRegistro = DateTime.UtcNow
        };

        context.Usuarios.Add(usuario);
        await context.SaveChangesAsync();

        var authService = new AuthService(context, _mapper, _configuration);

        var requestErroneo = new LoginRequest
        {
            UsuarioOCorreo = "seguridad@tiendago.com",
            Password = "PasswordErroneo999!" // Contraseña deliberadamente incorrecta
        };

        // -------------------------------------------------------------
        // ACT (Ejecutar login con credencial inválida)
        // -------------------------------------------------------------
        var response = await authService.LoginAsync(requestErroneo);

        // -------------------------------------------------------------
        // ASSERT (Denegación de acceso y nulidad de token)
        // -------------------------------------------------------------
        response.Should().BeNull("porque la verificación de hash BCrypt falló impidiendo la emisión de JWT");
    }
}
