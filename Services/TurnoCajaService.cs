using AutoMapper;
using TiendaGo.DTOs.Turnos;
using TiendaGo.Models;

namespace TiendaGo.Services;

public class TurnoCajaService : ITurnoCajaService
{
    private readonly Supabase.Client _supabase;
    private readonly IMapper _mapper;

    public TurnoCajaService(Supabase.Client supabase, IMapper mapper)
    {
        _supabase = supabase;
        _mapper = mapper;
    }

    public async Task<TurnoResponse> AbrirTurnoAsync(AbrirTurnoRequest request)
    {
        if (request.MontoBaseInicial < 0)
        {
            throw new ArgumentException("El monto base inicial no puede ser negativo.");
        }

        // Verificar si ya existe un turno abierto para este usuario
        var turnoActivoRes = await _supabase.From<TurnoCaja>()
            .Where(t => t.IdUsuario == request.IdUsuario && t.EstadoTurno == "Abierto")
            .Get();

        if (turnoActivoRes.Models.Count > 0)
        {
            throw new InvalidOperationException("El usuario ya tiene un turno de caja abierto.");
        }

        var turno = _mapper.Map<TurnoCaja>(request);
        turno.FechaApertura = DateTimeOffset.UtcNow;
        turno.EstadoTurno = "Abierto";
        turno.TotalVentasEfectivo = 0m;
        turno.TotalVentasDigital = 0m;

        var insertRes = await _supabase.From<TurnoCaja>().Insert(turno);
        var nuevoTurno = insertRes.Models.FirstOrDefault() ?? turno;

        await CargarRelacionesAsync(nuevoTurno);
        return _mapper.Map<TurnoResponse>(nuevoTurno);
    }

    public async Task<TurnoResponse?> CerrarTurnoAsync(long idTurno, CerrarTurnoRequest request)
    {
        if (request.MontoDeclarado < 0)
        {
            throw new ArgumentException("El monto declarado no puede ser negativo.");
        }

        var res = await _supabase.From<TurnoCaja>()
            .Where(t => t.IdTurno == idTurno)
            .Get();

        var turno = res.Models.FirstOrDefault();
        if (turno == null) return null;

        if (turno.EstadoTurno != "Abierto")
        {
            throw new InvalidOperationException($"El turno #{idTurno} ya se encuentra cerrado o arqueado.");
        }

        var totalEsperadoEfectivo = turno.MontoBaseInicial + turno.TotalVentasEfectivo;
        var diferencia = request.MontoDeclarado - totalEsperadoEfectivo;

        turno.FechaCierre = DateTimeOffset.UtcNow;
        turno.MontoDeclarado = request.MontoDeclarado;
        turno.DiferenciaCuadre = diferencia;
        turno.EstadoTurno = "Cerrado";

        await _supabase.From<TurnoCaja>()
            .Where(t => t.IdTurno == idTurno)
            .Update(turno);

        await CargarRelacionesAsync(turno);
        return _mapper.Map<TurnoResponse>(turno);
    }

    public async Task<TurnoResponse?> ObtenerTurnoActivoAsync(Guid idUsuario)
    {
        var res = await _supabase.From<TurnoCaja>()
            .Where(t => t.IdUsuario == idUsuario && t.EstadoTurno == "Abierto")
            .Get();

        var turno = res.Models.FirstOrDefault();
        if (turno == null) return null;

        await CargarRelacionesAsync(turno);
        return _mapper.Map<TurnoResponse>(turno);
    }

    public async Task<TurnoResponse?> ObtenerPorIdAsync(long idTurno)
    {
        var res = await _supabase.From<TurnoCaja>()
            .Where(t => t.IdTurno == idTurno)
            .Get();

        var turno = res.Models.FirstOrDefault();
        if (turno == null) return null;

        await CargarRelacionesAsync(turno);
        return _mapper.Map<TurnoResponse>(turno);
    }

    public async Task<IEnumerable<TurnoResponse>> ObtenerHistorialAsync()
    {
        var res = await _supabase.From<TurnoCaja>().Get();
        var turnos = res.Models.OrderByDescending(t => t.FechaApertura).ToList();

        var usuariosDict = await ObtenerDiccionarioUsuariosAsync();
        var resultado = new List<TurnoResponse>();

        foreach (var t in turnos)
        {
            if (usuariosDict.TryGetValue(t.IdUsuario, out var usr))
            {
                t.Usuario = usr;
            }
            resultado.Add(_mapper.Map<TurnoResponse>(t));
        }

        return resultado;
    }

    private async Task CargarRelacionesAsync(TurnoCaja turno)
    {
        if (turno.IdUsuario != Guid.Empty)
        {
            var uRes = await _supabase.From<Usuario>()
                .Where(u => u.IdUsuario == turno.IdUsuario)
                .Get();
            turno.Usuario = uRes.Models.FirstOrDefault();
        }
    }

    private async Task<Dictionary<Guid, Usuario>> ObtenerDiccionarioUsuariosAsync()
    {
        var res = await _supabase.From<Usuario>().Get();
        return res.Models.ToDictionary(u => u.IdUsuario, u => u);
    }
}
