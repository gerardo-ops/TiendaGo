using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class OauthAuthorizations
{
    public Guid Id { get; set; }

    public string AuthorizationId { get; set; } = null!;

    public Guid ClientId { get; set; }

    public Guid? UserId { get; set; }

    public string RedirectUri { get; set; } = null!;

    public string Scope { get; set; } = null!;

    public string? State { get; set; }

    public string? Resource { get; set; }

    public string? CodeChallenge { get; set; }

    public string? AuthorizationCode { get; set; }

    public DateTime CreatedAt { get; set; }

    public DateTime ExpiresAt { get; set; }

    public DateTime? ApprovedAt { get; set; }

    public string? Nonce { get; set; }

    public virtual OauthClients Client { get; set; } = null!;

    public virtual Users? User { get; set; }
}
