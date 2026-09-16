using AutoMapper;
using TiendaGo.DTOs.Turnos;
using TiendaGo.DTOs.Ventas;
using TiendaGo.Models;

namespace TiendaGo.Mappings;

public class VentasMappingProfile : Profile
{
    public VentasMappingProfile()
    {
        // Mapeo TurnoCaja <-> DTOs
        CreateMap<TurnoCaja, TurnoResponse>()
            .ForMember(dest => dest.NombreUsuario, opt => opt.MapFrom(src => src.Usuario != null ? src.Usuario.NombreCompleto : string.Empty));

        CreateMap<AbrirTurnoRequest, TurnoCaja>()
            .ForMember(dest => dest.IdTurno, opt => opt.Ignore())
            .ForMember(dest => dest.Usuario, opt => opt.Ignore())
            .ForMember(dest => dest.FechaApertura, opt => opt.MapFrom(_ => DateTimeOffset.UtcNow))
            .ForMember(dest => dest.FechaCierre, opt => opt.Ignore())
            .ForMember(dest => dest.TotalVentasEfectivo, opt => opt.MapFrom(_ => 0m))
            .ForMember(dest => dest.TotalVentasDigital, opt => opt.MapFrom(_ => 0m))
            .ForMember(dest => dest.MontoDeclarado, opt => opt.Ignore())
            .ForMember(dest => dest.DiferenciaCuadre, opt => opt.Ignore())
            .ForMember(dest => dest.EstadoTurno, opt => opt.MapFrom(_ => "Abierto"));

        // Mapeo Ventas <-> DTOs
        CreateMap<Venta, VentaResponse>()
            .ForMember(dest => dest.NombreUsuario, opt => opt.MapFrom(src => src.Usuario != null ? src.Usuario.NombreCompleto : string.Empty))
            .ForMember(dest => dest.NombreMetodoPago, opt => opt.MapFrom(src => src.MetodoPago != null ? src.MetodoPago.NombreMetodo : string.Empty))
            .ForMember(dest => dest.Detalles, opt => opt.Ignore());

        CreateMap<DetalleVenta, DetalleVentaResponse>()
            .ForMember(dest => dest.NombreProducto, opt => opt.MapFrom(src => src.Producto != null ? src.Producto.NombreProducto : string.Empty))
            .ForMember(dest => dest.CodigoSku, opt => opt.MapFrom(src => src.Producto != null ? src.Producto.CodigoSku : string.Empty));
    }
}
