using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using FluentAssertions;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.IntegrationTests.Infrastructure;
using Xunit;

namespace TiendaGo.IntegrationTests.Tests;

/// <summary>
/// Suite de Pruebas de Integración — Autenticación y Generación de Tokens JWT
/// Norma ISO/IEC/IEEE 29119 | Nivel 2 de Pirámide de Pruebas
/// Cobertura: POST /api/auth/login
/// </summary>
public class AuthEndpointsTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;
    private readonly CustomWebApplicationFactory _factory;

    private static readonly JsonSerializerOptions _jsonOptions = new()
    {
        PropertyNameCaseInsensitive = true
    };

    public AuthEndpointsTests(CustomWebApplicationFactory factory)
    {
        _factory = factory;
        _client  = factory.CreateClient();
    }

    // ─────────────────────────────────────────────────────────────────────────
    // IT-AUTH-01: Login con credenciales válidas devuelve HTTP 200 OK
    //             y el token JWT estructurado con claims de rol.
    // ─────────────────────────────────────────────────────────────────────────
    [Fact(DisplayName = "IT-AUTH-01: POST /api/auth/login con credenciales válidas devuelve 200 OK y JWT con claim de rol")]
    public async Task Login_ConCredencialesValidas_Devuelve200OkYTokenJwt()
    {
        // ── Arrange ───────────────────────────────────────────────────────────
        var loginRequest = new LoginRequest
        {
            UsuarioOCorreo = CustomWebApplicationFactory.AdminEmail,
            Password       = CustomWebApplicationFactory.AdminPassword
        };

        // ── Act ───────────────────────────────────────────────────────────────
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginRequest);

        // ── Assert ────────────────────────────────────────────────────────────
        response.StatusCode.Should().Be(HttpStatusCode.OK,
            because: "un login con credenciales correctas debe retornar HTTP 200 OK");

        var body = await response.Content.ReadAsStringAsync();
        body.Should().NotBeNullOrEmpty(because: "la respuesta debe contener un cuerpo JSON");

        using var jsonDoc = JsonDocument.Parse(body);
        var root = jsonDoc.RootElement;

        // Validar que existan las propiedades clave del LoginResponse
        root.TryGetProperty("token", out var tokenElement).Should().BeTrue(
            because: "la respuesta debe incluir el campo 'token'");

        root.TryGetProperty("rol", out var rolElement).Should().BeTrue(
            because: "la respuesta debe incluir el campo 'rol' con el nombre del rol del usuario");

        root.TryGetProperty("nombre", out var nombreElement).Should().BeTrue(
            because: "la respuesta debe incluir el campo 'nombre' del usuario autenticado");

        // Validar el token JWT: debe tener 3 partes (header.payload.signature)
        var tokenStr = tokenElement.GetString()!;
        tokenStr.Should().NotBeNullOrEmpty(because: "el token JWT no debe estar vacío");

        var partes = tokenStr.Split('.');
        partes.Should().HaveCount(3, because: "un JWT bien formado tiene exactamente 3 segmentos separados por '.'");

        // Decodificar el payload del JWT y verificar el claim de rol
        var payloadJson = System.Text.Encoding.UTF8.GetString(
            Convert.FromBase64String(PadBase64(partes[1])));
        using var payloadDoc = JsonDocument.Parse(payloadJson);
        var payloadRoot = payloadDoc.RootElement;

        // ClaimTypes.Role se serializa como "http://schemas.microsoft.com/ws/2008/06/identity/claims/role"
        bool tieneClaimRol = payloadRoot.TryGetProperty(
            "http://schemas.microsoft.com/ws/2008/06/identity/claims/role", out var rolClaim);

        tieneClaimRol.Should().BeTrue(because: "el JWT debe contener el claim de rol estándar de .NET");
        rolClaim.GetString().Should().Be("Administrador",
            because: "el usuario admin.test@tiendago.com tiene el rol Administrador");

        // Validar el campo 'rol' del cuerpo de respuesta
        rolElement.GetString().Should().Be("Administrador",
            because: "la respuesta de login debe reflejar el rol del usuario autenticado");
    }

    // ─────────────────────────────────────────────────────────────────────────
    // IT-AUTH-02: Login con credenciales incorrectas devuelve HTTP 401 Unauthorized
    // ─────────────────────────────────────────────────────────────────────────
    [Fact(DisplayName = "IT-AUTH-02: POST /api/auth/login con contraseña incorrecta devuelve 401 Unauthorized")]
    public async Task Login_ConPasswordIncorrecta_Devuelve401Unauthorized()
    {
        // ── Arrange ───────────────────────────────────────────────────────────
        var loginRequest = new LoginRequest
        {
            UsuarioOCorreo = CustomWebApplicationFactory.AdminEmail,
            Password       = "ContraseñaEquivocada999!"
        };

        // ── Act ───────────────────────────────────────────────────────────────
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginRequest);

        // ── Assert ────────────────────────────────────────────────────────────
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized,
            because: "credenciales incorrectas deben resultar en HTTP 401 Unauthorized");
    }

    [Fact(DisplayName = "IT-AUTH-03: POST /api/auth/login con correo inexistente devuelve 401 Unauthorized")]
    public async Task Login_ConCorreoNoRegistrado_Devuelve401Unauthorized()
    {
        // ── Arrange ───────────────────────────────────────────────────────────
        var loginRequest = new LoginRequest
        {
            UsuarioOCorreo = "noexiste@tiendago.com",
            Password       = "CualquierClave123*"
        };

        // ── Act ───────────────────────────────────────────────────────────────
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginRequest);

        // ── Assert ────────────────────────────────────────────────────────────
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized,
            because: "un correo no registrado no debe poder autenticarse");
    }

    [Fact(DisplayName = "IT-AUTH-04: POST /api/auth/login con cuerpo vacío devuelve 400 Bad Request")]
    public async Task Login_ConCuerpoVacio_Devuelve400BadRequest()
    {
        // ── Arrange ───────────────────────────────────────────────────────────
        var loginRequest = new LoginRequest
        {
            UsuarioOCorreo = "",
            Password       = ""
        };

        // ── Act ───────────────────────────────────────────────────────────────
        var response = await _client.PostAsJsonAsync("/api/auth/login", loginRequest);

        // ── Assert ────────────────────────────────────────────────────────────
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest,
            because: "enviar credenciales vacías debe resultar en 400 Bad Request");
    }

    // ─── Helper: Rellena con '=' el padding de Base64 para poder decodificar ─
    private static string PadBase64(string base64)
    {
        var padded = base64.Replace('-', '+').Replace('_', '/');
        return (padded.Length % 4) switch
        {
            2 => padded + "==",
            3 => padded + "=",
            _ => padded
        };
    }
}
