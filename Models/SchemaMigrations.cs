using System;
using System.Collections.Generic;

namespace TiendaGo.Models;

/// <summary>
/// Auth: Manages updates to the auth system.
/// </summary>
public partial class SchemaMigrations
{
    public string Version { get; set; } = null!;
}
