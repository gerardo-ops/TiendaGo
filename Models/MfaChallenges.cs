using System;
using System.Collections.Generic;
using System.Net;

namespace TiendaGo.Models;

/// <summary>
/// auth: stores metadata about challenge requests made
/// </summary>
public partial class MfaChallenges
{
    public Guid Id { get; set; }

    public Guid FactorId { get; set; }

    public DateTime CreatedAt { get; set; }

    public DateTime? VerifiedAt { get; set; }

    public IPAddress IpAddress { get; set; } = null!;

    public string? OtpCode { get; set; }

    public string? WebAuthnSessionData { get; set; }

    public virtual MfaFactors Factor { get; set; } = null!;
}
