using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class MfaRecoveryCodes
{
    public Guid Id { get; set; }

    public Guid MfaRecoveryCodeSetId { get; set; }

    public string CodeHash { get; set; } = null!;

    public DateTime? ConsumedAt { get; set; }

    public DateTime CreatedAt { get; set; }

    public virtual MfaRecoveryCodeSets MfaRecoveryCodeSet { get; set; } = null!;
}
