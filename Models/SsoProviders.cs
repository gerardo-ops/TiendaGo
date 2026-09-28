using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

/// <summary>
/// Auth: Manages SSO identity provider information; see saml_providers for SAML.
/// </summary>
public partial class SsoProviders
{
    public Guid Id { get; set; }

    /// <summary>
    /// Auth: Uniquely identifies a SSO provider according to a user-chosen resource ID (case insensitive), useful in infrastructure as code.
    /// </summary>
    public string? ResourceId { get; set; }

    public DateTime? CreatedAt { get; set; }

    public DateTime? UpdatedAt { get; set; }

    public bool? Disabled { get; set; }

    public virtual ICollection<SamlProviders> SamlProviders { get; set; } = new List<SamlProviders>();

    public virtual ICollection<SamlRelayStates> SamlRelayStates { get; set; } = new List<SamlRelayStates>();

    public virtual ICollection<ScimTokens> ScimTokens { get; set; } = new List<ScimTokens>();

    public virtual ICollection<ScimUsers> ScimUsers { get; set; } = new List<ScimUsers>();

    public virtual ICollection<SsoDomains> SsoDomains { get; set; } = new List<SsoDomains>();
}
