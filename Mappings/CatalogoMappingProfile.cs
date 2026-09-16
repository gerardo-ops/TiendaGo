using AutoMapper;
using TiendaGo.DTOs.Productos;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;

namespace TiendaGo.Mappings;

public class CatalogoMappingProfile : Profile
{
    public CatalogoMappingProfile()
    {
        // Mapeo de Usuarios (EF Core)
        CreateMap<Usuarios, UsuarioResponse>()
            .ForMember(dest => dest.NombreRol, opt => opt.MapFrom(src => src.IdRolNavigation != null ? src.IdRolNavigation.NombreRol : string.Empty))
            .ForMember(dest => dest.Token, opt => opt.Ignore())
            .ReverseMap();

        CreateMap<CrearUsuarioRequest, Usuarios>()
            .ForMember(dest => dest.IdUsuario, opt => opt.Ignore())
            .ForMember(dest => dest.IdRolNavigation, opt => opt.Ignore())
            .ForMember(dest => dest.TurnosCaja, opt => opt.Ignore())
            .ForMember(dest => dest.Ventas, opt => opt.Ignore())
            .ForMember(dest => dest.ClaveHash, opt => opt.Ignore())
            .ForMember(dest => dest.EstadoActivo, opt => opt.MapFrom(_ => true))
            .ForMember(dest => dest.FechaRegistro, opt => opt.MapFrom(_ => DateTime.UtcNow));

        // Mapeo de Productos (EF Core)
        CreateMap<Productos, ProductoResponse>()
            .ForMember(dest => dest.NombreCategoria, opt => opt.MapFrom(src => src.IdCategoriaNavigation != null ? src.IdCategoriaNavigation.NombreCategoria : string.Empty))
            .ReverseMap();

        CreateMap<ProductoRequest, Productos>()
            .ForMember(dest => dest.IdProducto, opt => opt.Ignore())
            .ForMember(dest => dest.IdCategoriaNavigation, opt => opt.Ignore())
            .ForMember(dest => dest.DetallesVenta, opt => opt.Ignore())
            .ForMember(dest => dest.FechaCreacion, opt => opt.MapFrom(_ => DateTime.UtcNow));

        CreateMap<ProductoResponse, ProductoRequest>().ReverseMap();
    }
}
