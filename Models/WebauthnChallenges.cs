using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class WebauthnChallenges
{
    public Guid Id { get; set; }

    public Guid? UserId { get; set; }

    public string ChallengeType { get; set; } = null!;

    public string SessionData { get; set; } = null!;

    public DateTime CreatedAt { get; set; }

    public DateTime ExpiresAt { get; set; }

    public virtual Users? User { get; set; }
}
