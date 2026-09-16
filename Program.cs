using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using TiendaGo.Endpoints;
using TiendaGo.Mappings;
using TiendaGo.Services;

var builder = WebApplication.CreateBuilder(args);

// =============================================
// 1. CONFIGURACIÓN DE SWAGGER / OPENAPI CON JWT
// =============================================
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "TiendaGo Web API",
        Version = "v1",
        Description = "API RESTful para el sistema POS Móvil y Gestión de Inventario TiendaGo (Supabase + .NET Core)"
    });

    // Definición de seguridad JWT Bearer
    var securityScheme = new OpenApiSecurityScheme
    {
        Name = "Authorization",
        Description = "Ingrese el token JWT Bearer. Ejemplo: Bearer {token}",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
        Reference = new OpenApiReference
        {
            Type = ReferenceType.SecurityScheme,
            Id = "Bearer"
        }
    };

    c.AddSecurityDefinition("Bearer", securityScheme);
    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            securityScheme,
            Array.Empty<string>()
        }
    });
});

// =============================================
// 2. CONFIGURACIÓN DE SUPABASE CLIENT
// =============================================
var supabaseUrl = builder.Configuration["Supabase:Url"] 
    ?? throw new InvalidOperationException("Supabase:Url no está configurado en appsettings.json.");
var supabaseKey = builder.Configuration["Supabase:AnonKey"] 
    ?? throw new InvalidOperationException("Supabase:AnonKey no está configurado en appsettings.json.");

builder.Services.AddScoped<Supabase.Client>(_ => new Supabase.Client(supabaseUrl, supabaseKey, new Supabase.SupabaseOptions
{
    AutoRefreshToken = true,
    AutoConnectRealtime = true
}));

// =============================================
// 3. INYECCIÓN DE DEPENDENCIAS (SERVICIOS Y MAPPER)
// =============================================
builder.Services.AddAutoMapper(cfg =>
{
    cfg.AddProfile<CatalogoMappingProfile>();
    cfg.AddProfile<VentasMappingProfile>();
});
builder.Services.AddScoped<IUsuarioService, UsuarioService>();
builder.Services.AddScoped<IProductoService, ProductoService>();
builder.Services.AddScoped<ITurnoCajaService, TurnoCajaService>();
builder.Services.AddScoped<IVentaService, VentaService>();
builder.Services.AddScoped<IDashboardService, DashboardService>();


// =============================================
// 4. AUTENTICACIÓN JWT Y AUTORIZACIÓN
// =============================================
var jwtKey = builder.Configuration["Jwt:Key"] ?? "TiendaGoSecretKey_SuperSecureKeyForJWT2026!#*";
var jwtIssuer = builder.Configuration["Jwt:Issuer"] ?? "TiendaGoApi";
var jwtAudience = builder.Configuration["Jwt:Audience"] ?? "TiendaGoClient";

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = false;
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey)),
        ValidateIssuer = true,
        ValidIssuer = jwtIssuer,
        ValidateAudience = true,
        ValidAudience = jwtAudience,
        ValidateLifetime = true,
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddAuthorization();

// =============================================
// 5. CORS (CLIENTE MÓVIL Y WEB)
// =============================================
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// =============================================
// 6. PIPELINE DE MIDDLEWARES HTTP
// =============================================
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "TiendaGo API v1");
    });
}

app.UseCors("AllowAll");
app.UseAuthentication();
app.UseAuthorization();

// =============================================
// 7. MAPEO DE GRUPOS DE ENDPOINTS
// =============================================
app.MapUsuarioEndpoints();
app.MapProductoEndpoints();
app.MapTurnoCajaEndpoints();
app.MapVentaEndpoints();
app.MapDashboardEndpoints();

app.Run();
