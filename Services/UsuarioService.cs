using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using AutoMapper;
using Microsoft.IdentityModel.Tokens;
using Supabase.Gotrue;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;

namespace TiendaGo.Services;

public class UsuarioService : IUsuarioService
{
    private readonly Supabase.Client _supabase;
    private readonly IMapper _mapper;
    private readonly IConfiguration _configuration;

    public UsuarioService(Supabase.Client supabase, IMapper mapper, IConfiguration configuration)
    {
        _supabase = supabase;
        _mapper = mapper;
        _configuration = configuration;
    }

    public async Task<UsuarioResponse?> LoginAsync(LoginRequest request)
    {
        // 1. Buscar usuario en base de datos por correo
        var usuariosResponse = await _supabase.From<Usuario>()
            .Where(u => u.CorreoElectronico == request.CorreoElectronico)
            .Get();

        var usuario = usuariosResponse.Models.FirstOrDefault();
        if (usuario == null || !usuario.EstadoActivo)
        {
            return null;
        }

        bool passwordValida = false;

        // Intentar autenticación con Supabase Auth primero
        try
        {
            var authResponse = await _supabase.Auth.SignInWithPassword(request.CorreoElectronico, request.Clave);
            if (authResponse?.User != null)
            {
                passwordValida = true;
            }
        }
        catch
        {
            // Si falla la llamada directa de Supabase Auth, se evalúa el hash local si está presente
        }

        // Si no validó por Supabase Auth, verificar con clave_hash (BCrypt)
        if (!passwordValida && !string.IsNullOrEmpty(usuario.ClaveHash))
        {
            try
            {
                passwordValida = BCrypt.Net.BCrypt.Verify(request.Clave, usuario.ClaveHash);
            }
            catch
            {
                passwordValida = false;
            }
        }

        if (!passwordValida)
        {
            return null;
        }

        // Obtener rol
        var rol = await ObtenerRolPorIdAsync(usuario.IdRol);
        usuario.Rol = rol;

        var response = _mapper.Map<UsuarioResponse>(usuario);
        response.Token = GenerarJwtToken(response);

        return response;
    }

    public async Task<IEnumerable<UsuarioResponse>> ObtenerTodosAsync()
    {
        var usuariosResponse = await _supabase.From<Usuario>().Get();
        var usuarios = usuariosResponse.Models;

        var rolesResponse = await _supabase.From<Rol>().Get();
        var rolesDict = rolesResponse.Models.ToDictionary(r => r.IdRol, r => r);

        var resultado = new List<UsuarioResponse>();
        foreach (var user in usuarios)
        {
            if (rolesDict.TryGetValue(user.IdRol, out var rol))
            {
                user.Rol = rol;
            }
            resultado.Add(_mapper.Map<UsuarioResponse>(user));
        }

        return resultado;
    }

    public async Task<UsuarioResponse?> ObtenerPorIdAsync(Guid id)
    {
        var response = await _supabase.From<Usuario>()
            .Where(u => u.IdUsuario == id)
            .Get();

        var usuario = response.Models.FirstOrDefault();
        if (usuario == null) return null;

        usuario.Rol = await ObtenerRolPorIdAsync(usuario.IdRol);
        return _mapper.Map<UsuarioResponse>(usuario);
    }

    public async Task<UsuarioResponse> CrearUsuarioAsync(CrearUsuarioRequest request)
    {
        string claveHash = BCrypt.Net.BCrypt.HashPassword(request.Clave);
        Guid idUsuario = Guid.NewGuid();

        // Crear usuario en Supabase Auth
        try
        {
            var options = new SignUpOptions
            {
                Data = new Dictionary<string, object>
                {
                    { "nombre_completo", request.NombreCompleto },
                    { "id_rol", request.IdRol }
                }
            };
            var session = await _supabase.Auth.SignUp(request.CorreoElectronico, request.Clave, options);
            if (session?.User != null && Guid.TryParse(session.User.Id, out var parsedGuid))
            {
                idUsuario = parsedGuid;
            }
        }
        catch
        {
            // Continuar con creación del registro
        }

        // Validar si el trigger on_auth_user_created_tiendago ya creó el registro
        var existente = await _supabase.From<Usuario>()
            .Where(u => u.CorreoElectronico == request.CorreoElectronico)
            .Get();

        Usuario usuario;
        if (existente.Models.Count > 0)
        {
            usuario = existente.Models.First();
            usuario.IdRol = request.IdRol;
            usuario.ClaveHash = claveHash;
            usuario.NombreCompleto = request.NombreCompleto;

            await _supabase.From<Usuario>()
                .Where(u => u.IdUsuario == usuario.IdUsuario)
                .Update(usuario);
        }
        else
        {
            usuario = new Usuario
            {
                IdUsuario = idUsuario,
                IdRol = request.IdRol,
                NombreCompleto = request.NombreCompleto,
                CorreoElectronico = request.CorreoElectronico,
                ClaveHash = claveHash,
                EstadoActivo = true,
                FechaRegistro = DateTimeOffset.UtcNow
            };

            var insertResponse = await _supabase.From<Usuario>().Insert(usuario);
            usuario = insertResponse.Models.FirstOrDefault() ?? usuario;
        }

        usuario.Rol = await ObtenerRolPorIdAsync(usuario.IdRol);
        return _mapper.Map<UsuarioResponse>(usuario);
    }

    public async Task<bool> CambiarEstadoAsync(Guid id, bool activo)
    {
        var response = await _supabase.From<Usuario>()
            .Where(u => u.IdUsuario == id)
            .Get();

        var usuario = response.Models.FirstOrDefault();
        if (usuario == null) return false;

        usuario.EstadoActivo = activo;
        await _supabase.From<Usuario>()
            .Where(u => u.IdUsuario == id)
            .Update(usuario);

        return true;
    }

    public string GenerarJwtToken(UsuarioResponse usuario)
    {
        var secretKey = _configuration["Jwt:Key"] ?? "ClaveSecretaPorDefectoParaTiendaGoApi2026!#*";
        var issuer = _configuration["Jwt:Issuer"] ?? "TiendaGoApi";
        var audience = _configuration["Jwt:Audience"] ?? "TiendaGoClient";
        var expirationHours = int.TryParse(_configuration["Jwt:ExpirationHours"], out var hours) ? hours : 8;

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, usuario.IdUsuario.ToString()),
            new(ClaimTypes.Email, usuario.CorreoElectronico),
            new(ClaimTypes.Name, usuario.NombreCompleto),
            new(ClaimTypes.Role, string.IsNullOrEmpty(usuario.NombreRol) ? "Cajero" : usuario.NombreRol),
            new("id_rol", usuario.IdRol.ToString())
        };

        var token = new JwtSecurityToken(
            issuer: issuer,
            audience: audience,
            claims: claims,
            expires: DateTime.UtcNow.AddHours(expirationHours),
            signingCredentials: creds
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    private async Task<Rol?> ObtenerRolPorIdAsync(long idRol)
    {
        var rolResponse = await _supabase.From<Rol>()
            .Where(r => r.IdRol == idRol)
            .Get();

        return rolResponse.Models.FirstOrDefault();
    }
}
