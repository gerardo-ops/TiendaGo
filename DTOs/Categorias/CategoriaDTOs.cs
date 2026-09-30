namespace TiendaGo.DTOs.Categorias;

public class CategoriaResponse
{
    public long IdCategoria { get; set; }
    public string NombreCategoria { get; set; } = string.Empty;
    public string? Descripcion { get; set; }
    public bool EstadoActivo { get; set; } = true;
    public int TotalProductos { get; set; }
}

public class CategoriaRequest
{
    public string? Nombre { get; set; }
    public string? NombreCategoria { get; set; }
    public string? Descripcion { get; set; }
    public string? Icono { get; set; }
    public string? Color { get; set; }
}
