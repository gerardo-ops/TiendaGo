using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class BucketsVectors
{
    public string Id { get; set; } = null!;

    public DateTime CreatedAt { get; set; }

    public DateTime UpdatedAt { get; set; }

    public virtual ICollection<VectorIndexes> VectorIndexes { get; set; } = new List<VectorIndexes>();
}
