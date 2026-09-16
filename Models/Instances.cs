using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

/// <summary>
/// Auth: Manages users across multiple sites.
/// </summary>
public partial class Instances
{
    public Guid Id { get; set; }

    public Guid? Uuid { get; set; }

    public string? RawBaseConfig { get; set; }

    public DateTime? CreatedAt { get; set; }

    public DateTime? UpdatedAt { get; set; }
}
