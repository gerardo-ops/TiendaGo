using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class ScimTokens
{
    public Guid Id { get; set; }

    public Guid SsoProviderId { get; set; }

    public string TokenHash { get; set; } = null!;

    public string Prefix { get; set; } = null!;

    public DateTime CreatedAt { get; set; }

    public DateTime? ExpiresAt { get; set; }

    public DateTime? RevokedAt { get; set; }

    public DateTime? LastUsedAt { get; set; }

    public virtual SsoProviders SsoProvider { get; set; } = null!;
}
