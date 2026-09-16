using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using AutoMapper;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;

namespace TiendaGo.Services;

public class UsuarioService : IUsuarioService
{
    private readonly TiendaGoDbContext _context;
    private readonly IMapper _mapper;
    private readonly IConfiguration _configuration;

    public UsuarioService(TiendaGoDbContext context, IMapper mapper, IConfiguration configuration)
    {
        _context = context;
        _mapper = mapper;
        _configuration = configuration;
    }

    public async Task<LoginResponse?> LoginAsync(LoginRequest request)
    {
        var correo = (request.CorreoElectronico ?? request.Usuario ?? string.Empty).Trim().ToLower();
        var password = request.Clave ?? request.Password ?? string.Empty;

        if (string.IsNullOrEmpty(correo) || string.IsNullOrEmpty(password))
        {
            return null;
        }

        var usuario = await _context.Usuarios
            .Include(u => u.IdRolNavigation)
            .FirstOrDefaultAsync(u => u.CorreoElectronico.ToLower() == correo);

        if (usuario == null || !usuario.EstadoActivo)
        {
            return null;
        }

        bool passwordValida = false;
        if (!string.IsNullOrEmpty(usuario.ClaveHash))
        {
            try
            {
                passwordValida = BCrypt.Net.BCrypt.Verify(password, usuario.ClaveHash);
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

        var token = GenerarJwtToken(usuario, out var expiracion);
        var rolNombre = usuario.IdRolNavigation?.NombreRol ?? "Cajero";

        return new LoginResponse
        {
            Token = token,
            IdUsuario = usuario.IdUsuario,
            NombreCompleto = usuario.NombreCompleto,
            Rol = rolNombre,
            Expiracion = expiracion
        };
    }

    public async Task<IEnumerable<UsuarioResponse>> ObtenerTodosAsync()
    {
        var usuarios = await _context.Usuarios
            .Include(u => u.IdRolNavigation)
            .OrderBy(u => u.NombreCompleto)
            .ToListAsync();

        return _mapper.Map<IEnumerable<UsuarioResponse>>(usuarios);
    }

    public async Task<UsuarioResponse?> ObtenerPorIdAsync(Guid id)
    {
        var usuario = await _context.Usuarios
            .Include(u => u.IdRolNavigation)
            .FirstOrDefaultAsync(u => u.IdUsuario == id);

        return usuario != null ? _mapper.Map<UsuarioResponse>(usuario) : null;
    }

    public async Task<UsuarioResponse> CrearUsuarioAsync(CrearUsuarioRequest request)
    {
        var correo = (request.CorreoElectronico ?? request.Correo ?? string.Empty).Trim().ToLower();
        var nombre = (request.NombreCompleto ?? request.Nombre ?? string.Empty).Trim();
        var password = request.Clave ?? request.Password ?? string.Empty;

        var existe = await _context.Usuarios.AnyAsync(u => u.CorreoElectronico.ToLower() == correo);
        if (existe)
        {
            throw new InvalidOperationException($"El correo '{correo}' ya se encuentra registrado en el sistema.");
        }

        var rolExiste = await _context.Roles.AnyAsync(r => r.IdRol == request.IdRol);
        var idRol = rolExiste ? request.IdRol : 2; // Default a Cajero (2) si no existe

        string claveHash = BCrypt.Net.BCrypt.HashPassword(password);

        var nuevoUsuario = new Usuarios
        {
            IdUsuario = Guid.NewGuid(),
            IdRol = idRol,
            NombreCompleto = nombre,
            CorreoElectronico = correo,
            ClaveHash = claveHash,
            EstadoActivo = true,
            FechaRegistro = DateTime.UtcNow
        };

        _context.Usuarios.Add(nuevoUsuario);
        await _context.SaveChangesAsync();

        // Cargar navegación de Rol
        await _context.Entry(nuevoUsuario).Reference(u => u.IdRolNavigation).LoadAsync();

        return _mapper.Map<UsuarioResponse>(nuevoUsuario);
    }

    public async Task<bool> CambiarEstadoAsync(Guid id, bool activo)
    {
        var usuario = await _context.Usuarios.FindAsync(id);
        if (usuario == null) return false;

        usuario.EstadoActivo = activo;
        await _context.SaveChangesAsync();
        return true;
    }

    public string GenerarJwtToken(Usuarios usuario, out DateTime expiracion)
    {
        var secretKey = _configuration["Jwt:Key"] ?? "TiendaGoSecretKey_SuperSecureKeyForJWT2026!#*";
        var issuer = _configuration["Jwt:Issuer"] ?? "TiendaGoApi";
        var audience = _configuration["Jwt:Audience"] ?? "TiendaGoClient";
        var expirationHours = int.TryParse(_configuration["Jwt:ExpirationHours"], out var hours) ? hours : 8;

        expiracion = DateTime.UtcNow.AddHours(expirationHours);

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var rolNombre = usuario.IdRolNavigation?.NombreRol ?? "Cajero";

        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, usuario.IdUsuario.ToString()),
            new(ClaimTypes.Email, usuario.CorreoElectronico),
            new(ClaimTypes.Name, usuario.NombreCompleto),
            new(ClaimTypes.Role, rolNombre),
            new("id_rol", usuario.IdRol.ToString())
        };

        var token = new JwtSecurityToken(
            issuer: issuer,
            audience: audience,
            claims: claims,
            expires: expiracion,
            signingCredentials: creds
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
