using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class OauthConsents
{
    public Guid Id { get; set; }

    public Guid UserId { get; set; }

    public Guid ClientId { get; set; }

    public string Scopes { get; set; } = null!;

    public DateTime GrantedAt { get; set; }

    public DateTime? RevokedAt { get; set; }

    public virtual OauthClients Client { get; set; } = null!;

    public virtual Users User { get; set; } = null!;
}
