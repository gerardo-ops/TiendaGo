using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

/// <summary>
/// auth: stores authenticator method reference claims for multi factor authentication
/// </summary>
public partial class MfaAmrClaims
{
    public Guid SessionId { get; set; }

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public string AuthenticationMethod { get; set; } = null!;

    public Guid Id { get; set; }

    public virtual Sessions Session { get; set; } = null!;
}
