using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class OauthClients
{
    public Guid Id { get; set; }

    public string? ClientSecretHash { get; set; }

    public string RedirectUris { get; set; } = null!;

    public string GrantTypes { get; set; } = null!;

    public string? ClientName { get; set; }

    public string? ClientUri { get; set; }

    public string? LogoUri { get; set; }

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public DateTime? DeletedAt { get; set; }

    public string TokenEndpointAuthMethod { get; set; } = null!;

    public virtual ICollection<OauthAuthorizations> OauthAuthorizations { get; set; } = new List<OauthAuthorizations>();

    public virtual ICollection<OauthConsents> OauthConsents { get; set; } = new List<OauthConsents>();

    public virtual ICollection<Sessions> Sessions { get; set; } = new List<Sessions>();
}
