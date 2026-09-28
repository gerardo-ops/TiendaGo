using AutoMapper;
using TiendaGo.DTOs.Productos;
using TiendaGo.DTOs.Usuarios;
using TiendaGo.Models;

namespace TiendaGo.Mappings;

public class CatalogoMappingProfile : Profile
{
    public CatalogoMappingProfile()
    {
        // =============================================
        // MAPEOS DE USUARIOS (EF Core & Supabase Models)
        // =============================================
        CreateMap<Usuarios, UsuarioResponse>()
            .ForMember(dest => dest.IdUsuario, opt => opt.MapFrom(src => src.IdUsuario.GetHashCode() & 0x7FFFFFFF))
            .ForMember(dest => dest.IdUsuarioGuid, opt => opt.MapFrom(src => src.IdUsuario))
            .ForMember(dest => dest.Nombre, opt => opt.MapFrom(src => src.NombreCompleto))
            .ForMember(dest => dest.Correo, opt => opt.MapFrom(src => src.CorreoElectronico))
            .ForMember(dest => dest.Rol, opt => opt.MapFrom(src => src.IdRolNavigation != null ? src.IdRolNavigation.NombreRol : string.Empty))
            .ForMember(dest => dest.NombreRol, opt => opt.MapFrom(src => src.IdRolNavigation != null ? src.IdRolNavigation.NombreRol : string.Empty))
            .ForMember(dest => dest.Estado, opt => opt.MapFrom(src => src.EstadoActivo))
            .ForMember(dest => dest.Token, opt => opt.Ignore())
            .ReverseMap();

        CreateMap<Usuario, UsuarioResponse>()
            .ForMember(dest => dest.IdUsuario, opt => opt.MapFrom(src => src.IdUsuario.GetHashCode() & 0x7FFFFFFF))
            .ForMember(dest => dest.IdUsuarioGuid, opt => opt.MapFrom(src => src.IdUsuario))
            .ForMember(dest => dest.Nombre, opt => opt.MapFrom(src => src.NombreCompleto))
            .ForMember(dest => dest.Correo, opt => opt.MapFrom(src => src.CorreoElectronico))
            .ForMember(dest => dest.Rol, opt => opt.MapFrom(src => src.Rol != null ? src.Rol.NombreRol : string.Empty))
            .ForMember(dest => dest.NombreRol, opt => opt.MapFrom(src => src.Rol != null ? src.Rol.NombreRol : string.Empty))
            .ForMember(dest => dest.Estado, opt => opt.MapFrom(src => src.EstadoActivo))
            .ForMember(dest => dest.Token, opt => opt.Ignore())
            .ReverseMap();

        CreateMap<CrearUsuarioRequest, Usuarios>()
            .ForMember(dest => dest.IdUsuario, opt => opt.Ignore())
            .ForMember(dest => dest.NombreCompleto, opt => opt.MapFrom(src => src.Nombre))
            .ForMember(dest => dest.CorreoElectronico, opt => opt.MapFrom(src => src.Correo))
            .ForMember(dest => dest.IdRol, opt => opt.MapFrom(src => (long)src.IdRol))
            .ForMember(dest => dest.IdRolNavigation, opt => opt.Ignore())
            .ForMember(dest => dest.IdUsuarioNavigation, opt => opt.Ignore())
            .ForMember(dest => dest.TurnosCaja, opt => opt.Ignore())
            .ForMember(dest => dest.Ventas, opt => opt.Ignore())
            .ForMember(dest => dest.ClaveHash, opt => opt.Ignore())
            .ForMember(dest => dest.EstadoActivo, opt => opt.MapFrom(_ => true))
            .ForMember(dest => dest.FechaRegistro, opt => opt.MapFrom(_ => DateTime.UtcNow))
            .ReverseMap();

        CreateMap<CrearUsuarioRequest, Usuario>()
            .ForMember(dest => dest.IdUsuario, opt => opt.Ignore())
            .ForMember(dest => dest.NombreCompleto, opt => opt.MapFrom(src => src.Nombre))
            .ForMember(dest => dest.CorreoElectronico, opt => opt.MapFrom(src => src.Correo))
            .ForMember(dest => dest.IdRol, opt => opt.MapFrom(src => (long)src.IdRol))
            .ForMember(dest => dest.Rol, opt => opt.Ignore())
            .ForMember(dest => dest.ClaveHash, opt => opt.Ignore())
            .ForMember(dest => dest.EstadoActivo, opt => opt.MapFrom(_ => true))
            .ForMember(dest => dest.FechaRegistro, opt => opt.MapFrom(_ => DateTimeOffset.UtcNow))
            .ReverseMap();

        // =============================================
        // MAPEOS DE PRODUCTOS (EF Core & Supabase Models)
        // =============================================
        CreateMap<Productos, ProductoResponse>()
            .ForMember(dest => dest.IdProducto, opt => opt.MapFrom(src => (int)src.IdProducto))
            .ForMember(dest => dest.CodigoBarra, opt => opt.MapFrom(src => src.CodigoSku))
            .ForMember(dest => dest.Nombre, opt => opt.MapFrom(src => src.NombreProducto))
            .ForMember(dest => dest.Precio, opt => opt.MapFrom(src => src.PrecioVenta))
            .ForMember(dest => dest.Stock, opt => opt.MapFrom(src => src.StockActual))
            .ForMember(dest => dest.IdCategoria, opt => opt.MapFrom(src => (int)src.IdCategoria))
            .ForMember(dest => dest.NombreCategoria, opt => opt.MapFrom(src => src.IdCategoriaNavigation != null ? src.IdCategoriaNavigation.NombreCategoria : string.Empty))
            .ForMember(dest => dest.Estado, opt => opt.MapFrom(src => src.EstadoActivo))
            .ReverseMap();

        CreateMap<Producto, ProductoResponse>()
            .ForMember(dest => dest.IdProducto, opt => opt.MapFrom(src => (int)src.IdProducto))
            .ForMember(dest => dest.CodigoBarra, opt => opt.MapFrom(src => src.CodigoSku))
            .ForMember(dest => dest.Nombre, opt => opt.MapFrom(src => src.NombreProducto))
            .ForMember(dest => dest.Precio, opt => opt.MapFrom(src => src.PrecioVenta))
            .ForMember(dest => dest.Stock, opt => opt.MapFrom(src => src.StockActual))
            .ForMember(dest => dest.IdCategoria, opt => opt.MapFrom(src => (int)src.IdCategoria))
            .ForMember(dest => dest.NombreCategoria, opt => opt.MapFrom(src => src.Categoria != null ? src.Categoria.NombreCategoria : string.Empty))
            .ForMember(dest => dest.Estado, opt => opt.MapFrom(src => src.EstadoActivo))
            .ReverseMap();

        CreateMap<ProductoRequest, Productos>()
            .ForMember(dest => dest.IdProducto, opt => opt.Ignore())
            .ForMember(dest => dest.CodigoSku, opt => opt.MapFrom(src => src.CodigoBarra))
            .ForMember(dest => dest.NombreProducto, opt => opt.MapFrom(src => src.Nombre))
            .ForMember(dest => dest.PrecioVenta, opt => opt.MapFrom(src => src.Precio))
            .ForMember(dest => dest.StockActual, opt => opt.MapFrom(src => src.Stock))
            .ForMember(dest => dest.IdCategoria, opt => opt.MapFrom(src => (long)src.IdCategoria))
            .ForMember(dest => dest.EstadoActivo, opt => opt.MapFrom(src => src.Estado))
            .ForMember(dest => dest.IdCategoriaNavigation, opt => opt.Ignore())
            .ForMember(dest => dest.DetallesVenta, opt => opt.Ignore())
            .ForMember(dest => dest.FechaCreacion, opt => opt.MapFrom(_ => DateTime.UtcNow))
            .ReverseMap();

        CreateMap<ProductoRequest, Producto>()
            .ForMember(dest => dest.IdProducto, opt => opt.Ignore())
            .ForMember(dest => dest.CodigoSku, opt => opt.MapFrom(src => src.CodigoBarra))
            .ForMember(dest => dest.NombreProducto, opt => opt.MapFrom(src => src.Nombre))
            .ForMember(dest => dest.PrecioVenta, opt => opt.MapFrom(src => src.Precio))
            .ForMember(dest => dest.StockActual, opt => opt.MapFrom(src => src.Stock))
            .ForMember(dest => dest.IdCategoria, opt => opt.MapFrom(src => (long)src.IdCategoria))
            .ForMember(dest => dest.EstadoActivo, opt => opt.MapFrom(src => src.Estado))
            .ForMember(dest => dest.Categoria, opt => opt.Ignore())
            .ForMember(dest => dest.FechaCreacion, opt => opt.MapFrom(_ => DateTimeOffset.UtcNow))
            .ReverseMap();

        CreateMap<ProductoResponse, ProductoRequest>().ReverseMap();
    }
}
