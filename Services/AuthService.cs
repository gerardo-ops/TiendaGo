using AutoMapper;
using Microsoft.Extensions.Configuration;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;

namespace TiendaGo.Services;

public class AuthService : UsuarioService, IAuthService
{
    public AuthService(TiendaGoDbContext context, IMapper mapper, IConfiguration configuration)
        : base(context, mapper, configuration)
    {
    }
}
