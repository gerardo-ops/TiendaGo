using AutoMapper;
using TiendaGo.DTOs.Productos;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;

namespace TiendaGo.Mappings;

public class CatalogoMappingProfile : Profile
{
    public CatalogoMappingProfile()
    {
        // Mapeos de Usuarios
        CreateMap<Usuario, UsuarioResponse>()
            .ForMember(dest => dest.NombreRol, opt => opt.MapFrom(src => src.Rol != null ? src.Rol.NombreRol : string.Empty))
            .ForMember(dest => dest.Token, opt => opt.Ignore());

        CreateMap<CrearUsuarioRequest, Usuario>()
            .ForMember(dest => dest.IdUsuario, opt => opt.Ignore())
            .ForMember(dest => dest.Rol, opt => opt.Ignore())
            .ForMember(dest => dest.ClaveHash, opt => opt.Ignore())
            .ForMember(dest => dest.EstadoActivo, opt => opt.MapFrom(_ => true))
            .ForMember(dest => dest.FechaRegistro, opt => opt.MapFrom(_ => DateTimeOffset.UtcNow));

        // Mapeos de Productos
        CreateMap<Producto, ProductoResponse>()
            .ForMember(dest => dest.NombreCategoria, opt => opt.MapFrom(src => src.Categoria != null ? src.Categoria.NombreCategoria : string.Empty));

        CreateMap<ProductoRequest, Producto>()
            .ForMember(dest => dest.IdProducto, opt => opt.Ignore())
            .ForMember(dest => dest.Categoria, opt => opt.Ignore())
            .ForMember(dest => dest.FechaCreacion, opt => opt.MapFrom(_ => DateTimeOffset.UtcNow));
    }
}
