using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class OneTimeTokens
{
    public Guid Id { get; set; }

    public Guid UserId { get; set; }

    public string TokenHash { get; set; } = null!;

    public string RelatesTo { get; set; } = null!;

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public DateTime? ExpiresAt { get; set; }

    public virtual Users User { get; set; } = null!;
}
