using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

public partial class Migrations
{
    public int Id { get; set; }

    public string Name { get; set; } = null!;

    public string Hash { get; set; } = null!;

    public DateTime? ExecutedAt { get; set; }
}
