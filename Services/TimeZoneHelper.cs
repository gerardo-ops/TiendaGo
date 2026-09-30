using System;

namespace TiendaGo.Services;

/// <summary>
/// Helper para la gestión de zona horaria local del negocio (El Salvador / Centroamérica UTC-6).
/// Resuelve de manera cross-platform entre Linux, macOS y Windows.
/// </summary>
public static class TimeZoneHelper
{
    private static readonly Lazy<TimeZoneInfo> _businessTimeZone = new(() =>
    {
        // 1. Intentar con el identificador estándar IANA (Linux, macOS, .NET 6+ en Windows)
        if (TimeZoneInfo.TryFindSystemTimeZoneById("America/El_Salvador", out var tzIana))
        {
            return tzIana;
        }

        // 2. Intentar con el identificador estándar de Windows
        if (TimeZoneInfo.TryFindSystemTimeZoneById("Central America Standard Time", out var tzWin))
        {
            return tzWin;
        }

        // 3. Fallback seguro a UTC-6 constante (El Salvador no tiene cambio de horario de verano)
        return TimeZoneInfo.CreateCustomTimeZone(
            "Central_America_Standard_Time",
            TimeSpan.FromHours(-6),
            "Central America Standard Time",
            "Central America Standard Time"
        );
    });

    /// <summary>
    /// Zona horaria del negocio (UTC-6).
    /// </summary>
    public static TimeZoneInfo BusinessTimeZone => _businessTimeZone.Value;

    /// <summary>
    /// Convierte un DateTimeOffset a la zona horaria del negocio conservando el instante exacto.
    /// </summary>
    public static DateTimeOffset ToBusinessTime(DateTimeOffset dateTimeOffset)
    {
        return TimeZoneInfo.ConvertTime(dateTimeOffset, BusinessTimeZone);
    }

    /// <summary>
    /// Obtiene solo el componente de fecha (00:00:00) en la zona horaria del negocio.
    /// </summary>
    public static DateTime ToBusinessDate(DateTimeOffset dateTimeOffset)
    {
        return TimeZoneInfo.ConvertTime(dateTimeOffset, BusinessTimeZone).Date;
    }

    /// <summary>
    /// Obtiene la fecha de "Hoy" (a las 00:00:00) según la hora local del negocio.
    /// </summary>
    public static DateTime GetBusinessToday()
    {
        return TimeZoneInfo.ConvertTime(DateTimeOffset.UtcNow, BusinessTimeZone).Date;
    }
}
