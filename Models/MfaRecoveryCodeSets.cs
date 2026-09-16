using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class MfaRecoveryCodeSets
{
    public Guid Id { get; set; }

    public Guid UserId { get; set; }

    public Guid MfaFactorId { get; set; }

    public int FailedVerificationCount { get; set; }

    public DateTime? VerificationLockedUntil { get; set; }

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public virtual MfaFactors MfaFactor { get; set; } = null!;

    public virtual ICollection<MfaRecoveryCodes> MfaRecoveryCodes { get; set; } = new List<MfaRecoveryCodes>();

    public virtual Users User { get; set; } = null!;
}
