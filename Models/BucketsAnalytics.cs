using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class BucketsAnalytics
{
    public string Name { get; set; } = null!;

    public string Format { get; set; } = null!;

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public Guid Id { get; set; }

    public DateTime? DeletedAt { get; set; }
}
