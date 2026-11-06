import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"c:\Users\Admin\Documents\Proyectos\TiendaGo\Screenshots_DevOps"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Font setup
def get_font(name, size):
    font_path = os.path.join(r"C:\Windows\Fonts", name)
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()

font_title = get_font("segoeui.ttf", 22)
font_subtitle = get_font("segoeui.ttf", 15)
font_bold = get_font("segoeuib.ttf", 14)
font_regular = get_font("segoeui.ttf", 13)
font_small = get_font("segoeui.ttf", 11)
font_code = get_font("cascadiacode.ttf", 12)
font_code_bold = get_font("cascadiacode.ttf", 13)
font_code_small = get_font("cascadiacode.ttf", 11)

# Helper for wrapping text precisely by pixel width
def wrap_text(text, font, max_width, draw):
    words = text.split(" ")
    lines = []
    cur_line = ""
    for w in words:
        test_line = cur_line + " " + w if cur_line else w
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) > max_width:
            if cur_line:
                lines.append(cur_line)
            cur_line = w
        else:
            cur_line = test_line
    if cur_line:
        lines.append(cur_line)
    return lines

# Color Palette (Visual Studio Dark Theme)
BG_DARK = (30, 30, 30)
BG_EDITOR = (37, 37, 38)
BG_PANEL = (45, 45, 48)
BG_HEADER = (51, 51, 55)
BG_TAB_ACTIVE = (30, 30, 30)
BG_TAB_INACTIVE = (45, 45, 48)
BORDER_COLOR = (63, 63, 70)
TEXT_WHITE = (241, 241, 241)
TEXT_MUTED = (160, 160, 160)
ACCENT_BLUE = (0, 122, 204)
ACCENT_CYAN = (78, 201, 176)
ACCENT_GREEN = (106, 153, 85)
ACCENT_YELLOW = (220, 220, 170)
ACCENT_PURPLE = (197, 134, 192)
ACCENT_ORANGE = (206, 145, 120)
ACCENT_BLUE_LIGHT = (86, 156, 214)
COLOR_SUCCESS = (78, 201, 120)
CARD_BG = (37, 40, 48)

# -----------------------------------------------------------------------------
# IMAGE 1: ARQUITECTURA DE LA SOLUCIÓN TIENDAGO (Clean Architecture & Suites)
# -----------------------------------------------------------------------------
def create_image_1():
    width, height = 1600, 960
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Top Window Title Bar
    draw.rectangle([0, 0, width, 40], fill=BG_HEADER)
    draw.ellipse([width - 80, 12, width - 68, 24], fill=(235, 100, 100))
    draw.ellipse([width - 55, 12, width - 43, 24], fill=(245, 190, 70))
    draw.ellipse([width - 30, 12, width - 18, 24], fill=(100, 200, 100))
    draw.text((20, 10), "Visual Studio 2022 - TiendaGo.sln - Arquitectura del Sistema y Suites de Pruebas Automatizadas", fill=TEXT_WHITE, font=font_subtitle)

    # Subheader / Breadcrumb
    draw.rectangle([0, 40, width, 75], fill=(37, 37, 38))
    draw.text((20, 48), "ARQUITECTURA DE SOFTWARE: Solucion Desacoplada .NET 8 (Clean Architecture) y Framework de Pruebas ISO/IEC/IEEE 29119", fill=ACCENT_CYAN, font=font_bold)

    # Left Column: Solution Explorer Tree (Width: 610px)
    tree_x, tree_y, tree_w, tree_h = 20, 90, 610, 850
    draw.rectangle([tree_x, tree_y, tree_x + tree_w, tree_y + tree_h], fill=BG_EDITOR, outline=BORDER_COLOR, width=1)
    
    draw.rectangle([tree_x, tree_y, tree_x + tree_w, tree_y + 35], fill=BG_HEADER)
    draw.text((tree_x + 15, tree_y + 8), "EXPLORADOR DE SOLUCIONES (Solution Explorer)", fill=TEXT_WHITE, font=font_bold)
    draw.text((tree_x + tree_w - 110, tree_y + 9), "[3 Proyectos]", fill=TEXT_MUTED, font=font_small)

    items = [
        # (indent, tag, text, color, is_bold)
        (0, "[SLN]", "Solucion 'TiendaGo' (3 de 3 proyectos cargados)", TEXT_WHITE, True),
        (0, "", "", None, False),
        (0, "[API]", "TiendaGo (API Nucleo - ASP.NET Core 8.0)", ACCENT_BLUE_LIGHT, True),
        (1, "[DIR]", "Controllers / Endpoints (Minimal APIs)", TEXT_MUTED, False),
        (2, "[C#]", "VentasEndpoints.cs (POST/GET /api/ventas)", TEXT_WHITE, False),
        (2, "[C#]", "AuthEndpoints.cs (POST /api/auth/login)", TEXT_WHITE, False),
        (2, "[C#]", "ProductosEndpoints.cs (CRUD de Inventario)", TEXT_WHITE, False),
        (1, "[DIR]", "Services (Capa de Logica de Negocio POS)", ACCENT_YELLOW, False),
        (2, "[C#]", "VentaService.cs (Calculo IVA 13%, stock)", TEXT_WHITE, False),
        (2, "[C#]", "AuthService.cs (Hashing y JWT Claims)", TEXT_WHITE, False),
        (1, "[DIR]", "Models (Entidades de Dominio EF Core)", ACCENT_CYAN, False),
        (2, "[C#]", "TiendaGoDbContext.cs (Mapeo relacional)", TEXT_WHITE, False),
        (1, "[DIR]", "DTOs & Mappings (Contratos y AutoMapper)", TEXT_MUTED, False),
        (1, "[C#]", "Program.cs (IoC Container y Middlewares)", ACCENT_PURPLE, False),
        (0, "", "", None, False),
        (0, "[TEST]", "TiendaGo.UnitTests (Suite Unitaria - xUnit)", COLOR_SUCCESS, True),
        (1, "[DIR]", "Dependencies (Moq, FluentAssertions, InMemory)", TEXT_MUTED, False),
        (1, "[C#]", "VentaServiceTests.cs (7 Tests: calculos POS)", TEXT_WHITE, False),
        (1, "[C#]", "AuthServiceTests.cs (Tests de autenticacion)", TEXT_WHITE, False),
        (1, "[C#]", "ProductoMappingTests.cs (Mapeos DTO - Entidad)", TEXT_WHITE, False),
        (0, "", "", None, False),
        (0, "[HTTP]", "TiendaGo.IntegrationTests (Suite Integracion)", ACCENT_ORANGE, True),
        (1, "[DIR]", "Infrastructure (TestServer en Memoria)", TEXT_MUTED, False),
        (2, "[C#]", "CustomWebApplicationFactory.cs (IoC + JWT)", TEXT_WHITE, False),
        (1, "[DIR]", "Tests (Suites de Endpoints HTTP y RBAC)", TEXT_MUTED, False),
        (2, "[C#]", "VentasEndpointsTests.cs (Transaccional POS)", TEXT_WHITE, False),
        (2, "[C#]", "AuthEndpointsTests.cs (Autenticacion y JWT)", TEXT_WHITE, False),
        (2, "[C#]", "SeguridadRBACTests.cs (Roles Admin vs Cajero)", TEXT_WHITE, False),
    ]

    curr_y = tree_y + 45
    for indent, tag, text, color, is_b in items:
        if not text:
            curr_y += 6
            continue
        line_font = font_bold if is_b else font_regular
        x_tag = tree_x + 15 + indent * 18
        x_text = x_tag + (44 if tag else 0)
        if tag:
            draw.text((x_tag, curr_y), tag, fill=color or TEXT_WHITE, font=font_code_small)
        draw.text((x_text, curr_y), text, fill=color or TEXT_WHITE, font=line_font)
        curr_y += 26

    # Right Column: Architectural Flow Diagram & Layer Responsibilities
    diag_x, diag_y, diag_w, diag_h = 650, 90, 930, 850
    draw.rectangle([diag_x, diag_y, diag_x + diag_w, diag_y + diag_h], fill=BG_EDITOR, outline=BORDER_COLOR, width=1)
    
    draw.rectangle([diag_x, diag_y, diag_x + diag_w, diag_y + 35], fill=BG_HEADER)
    draw.text((diag_x + 15, diag_y + 8), "DIAGRAMA DE ARQUITECTURA EN CAPAS Y ALCANCE DE LAS PRUEBAS", fill=TEXT_WHITE, font=font_bold)

    layers = [
        ("CAPA DE ENTRADA Y SEGURIDAD HTTP (Endpoints / Minimal APIs)", 
         "Recibe peticiones HTTP sinteticas o reales. Aplica autenticacion Bearer JWT, validacion de Claims y politicas de autorizacion RBAC (Administrador vs Cajero). Enrutamiento declarativo y serializacion System.Text.Json.",
         ACCENT_BLUE_LIGHT, 135, "Controllers / Endpoints"),
        
        ("CAPA DE REGLAS DE NEGOCIO (Services / Application Core)", 
         "Implementa la logica del Punto de Venta (POS): calculo determinista de IVA al 13%, calculo de vuelto/cambio en efectivo, validacion estricta de stock disponible, y verificacion de estado de turnos de caja abiertos.",
         ACCENT_YELLOW, 275, "VentaService & AuthService"),
        
        ("CAPA DE PERSISTENCIA Y MODELO RELACIONAL (EF Core 8 / DbContext)", 
         "Mapea entidades relacionales (Ventas, DetalleVentas, Productos, TurnosCaja, Usuarios) a traves de TiendaGoDbContext. Administra transacciones atomicas ACID y garantiza consistencia referencial.",
         ACCENT_CYAN, 415, "TiendaGoDbContext"),
        
        ("CAPA DE ALMACENAMIENTO DE DATOS (Infraestructura de Datos)", 
         "- Entorno de Produccion: Supabase Managed PostgreSQL con migraciones EF Core.\n- Entorno de Pruebas: Microsoft.EntityFrameworkCore.InMemory con aislamiento por GUID unico.",
         COLOR_SUCCESS, 555, "PostgreSQL / InMemory Database")
    ]

    for title, desc, col, y_pos, pill in layers:
        card_box = [diag_x + 20, diag_y + y_pos - 80, diag_x + diag_w - 20, diag_y + y_pos + 45]
        draw.rectangle(card_box, fill=CARD_BG, outline=col, width=2)
        # Tag pill
        draw.rectangle([card_box[2] - 220, card_box[1] + 8, card_box[2] - 15, card_box[1] + 28], fill=col)
        draw.text((card_box[2] - 210, card_box[1] + 10), pill, fill=(20, 20, 20), font=font_small)
        # Title
        draw.text((card_box[0] + 15, card_box[1] + 10), title, fill=col, font=font_bold)
        
        # Wrapped description inside box width
        max_desc_w = card_box[2] - card_box[0] - 30
        y_text = card_box[1] + 35
        for paragraph in desc.split("\n"):
            wrapped_lines = wrap_text(paragraph, font_regular, max_desc_w, draw)
            for wl in wrapped_lines:
                draw.text((card_box[0] + 15, y_text), wl, fill=TEXT_WHITE, font=font_regular)
                y_text += 18

    # Downward connecting arrows
    for y_arrow in [200, 340, 480]:
        ax = diag_x + diag_w // 2
        ay = diag_y + y_arrow
        draw.line([(ax, ay), (ax, ay + 14)], fill=BORDER_COLOR, width=3)
        draw.polygon([(ax - 6, ay + 14), (ax + 6, ay + 14), (ax, ay + 20)], fill=BORDER_COLOR)

    # Test Scopes Comparison Box (Bottom)
    scope_y = diag_y + 575
    draw.rectangle([diag_x + 20, scope_y, diag_x + diag_w - 20, scope_y + 250], fill=(25, 28, 35), outline=(100, 100, 120), width=1)
    draw.text((diag_x + 35, scope_y + 12), "DESACOPLAMIENTO Y ESTRATEGIA DE PRUEBAS AUTOMATIZADAS", fill=TEXT_WHITE, font=font_bold)

    # Unit vs Integration columns
    col1_x = diag_x + 35
    draw.rectangle([col1_x, scope_y + 40, col1_x + 420, scope_y + 230], fill=(30, 35, 45), outline=COLOR_SUCCESS, width=1)
    draw.text((col1_x + 15, scope_y + 48), "[TEST] ALCANCE SUITE UNITARIA (TiendaGo.UnitTests)", fill=COLOR_SUCCESS, font=font_bold)
    u_lines = [
        "- Aisla completamente la Capa de Servicios (VentaService).",
        "- Reemplaza base de datos con DbContext InMemory (GUID unico).",
        "- Mockea dependencias externas (IMapper con Moq).",
        "- Valida invariantes matematicos y excepciones de negocio.",
        "- Ejecucion ultrarrapida: < 20 ms por prueba unitaria."
    ]
    uy = scope_y + 75
    for l in u_lines:
        draw.text((col1_x + 15, uy), l, fill=TEXT_WHITE, font=font_small)
        uy += 28

    col2_x = diag_x + 475
    draw.rectangle([col2_x, scope_y + 40, col2_x + 425, scope_y + 230], fill=(35, 30, 45), outline=ACCENT_ORANGE, width=1)
    draw.text((col2_x + 15, scope_y + 48), "[HTTP] ALCANCE SUITE INTEGRACION (TiendaGo.IntegrationTests)", fill=ACCENT_ORANGE, font=font_bold)
    i_lines = [
        "- Evalua el pipeline HTTP completo mediante WebApplicationFactory.",
        "- Sustituye en caliente el proveedor Npgsql por InMemory en IoC.",
        "- Emite peticiones HTTP reales a endpoints Minimal APIs.",
        "- Valida seguridad RBAC, cabeceras JWT y persistencia real EF Core.",
        "- Sin abrir sockets TCP de red externos (TestServer en memoria)."
    ]
    iy = scope_y + 75
    for l in i_lines:
        draw.text((col2_x + 15, iy), l, fill=TEXT_WHITE, font=font_small)
        iy += 28

    img.save(os.path.join(OUTPUT_DIR, "arquitectura_solucion_proyectos.png"), dpi=(150, 150))
    print("OK: arquitectura_solucion_proyectos.png")


# -----------------------------------------------------------------------------
# IMAGE 2: ARQUITECTURA DE CÓDIGO UNIT TESTS (Patrón AAA & VentaServiceTests.cs)
# -----------------------------------------------------------------------------
def create_image_2():
    width, height = 1600, 1000
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Top Window Title Bar
    draw.rectangle([0, 0, width, 40], fill=BG_HEADER)
    draw.ellipse([width - 80, 12, width - 68, 24], fill=(235, 100, 100))
    draw.ellipse([width - 55, 12, width - 43, 24], fill=(245, 190, 70))
    draw.ellipse([width - 30, 12, width - 18, 24], fill=(100, 200, 100))
    draw.text((20, 10), "Visual Studio Code - TiendaGo.UnitTests / VentaServiceTests.cs [xUnit + FluentAssertions + Moq]", fill=TEXT_WHITE, font=font_subtitle)

    # Editor Tabs
    draw.rectangle([0, 40, width, 75], fill=(37, 37, 38))
    draw.rectangle([10, 42, 280, 75], fill=BG_DARK, outline=(0, 122, 204), width=1)
    draw.text((25, 50), "C# VentaServiceTests.cs", fill=TEXT_WHITE, font=font_bold)
    draw.rectangle([290, 42, 500, 75], fill=BG_TAB_INACTIVE)
    draw.text((305, 50), "C# AuthServiceTests.cs", fill=TEXT_MUTED, font=font_regular)
    draw.rectangle([510, 42, 750, 75], fill=BG_TAB_INACTIVE)
    draw.text((525, 50), "C# ProductoMappingTests.cs", fill=TEXT_MUTED, font=font_regular)

    # Sub-bar / Breadcrumb
    draw.rectangle([0, 75, width, 105], fill=(30, 30, 30), outline=BORDER_COLOR, width=1)
    draw.text((20, 82), "TiendaGo.UnitTests  >  VentaServiceTests  >  UT_POS_01_RegistrarVenta_DeberiaCalcularSubtotalIvaYCambioExactos()", fill=ACCENT_CYAN, font=font_code_small)

    # Left Column: Syntax Highlighted Code (Width: 1060px)
    code_x, code_y, code_w, code_h = 20, 115, 1070, 865
    draw.rectangle([code_x, code_y, code_x + code_w, code_y + code_h], fill=BG_EDITOR, outline=BORDER_COLOR, width=1)

    code_lines = [
        (35, '[Fact(DisplayName = "UT-POS-01: Validar calculo exacto de subtotales, IVA y vuelto/cambio")]', ACCENT_YELLOW, 20, None),
        (36, 'public async Task UT_POS_01_RegistrarVenta_DeberiaCalcularSubtotalIvaYCambioExactos()', ACCENT_BLUE_LIGHT, 20, None),
        (37, '{', TEXT_WHITE, 20, None),
        (38, '    // =============================================================================', ACCENT_GREEN, 20, None),
        (39, '    // 1. ARRANGE (Organizar el escenario de prueba aislado)', COLOR_SUCCESS, 20, (30, 50, 35)),
        (40, '    // =============================================================================', ACCENT_GREEN, 20, None),
        (41, '    using var context = CreateInMemoryDbContext(); // Guid unico: Cero colision', ACCENT_CYAN, 20, None),
        (42, '    var usuarioId = Guid.NewGuid();', TEXT_WHITE, 20, None),
        (43, '    var turno = new TurnosCaja { IdTurno = 1, IdUsuario = usuarioId, EstadoTurno = "Abierto" };', TEXT_WHITE, 20, None),
        (44, '    var producto = new Productos {', TEXT_WHITE, 20, None),
        (45, '        IdProducto = 1, NombreProducto = "Bebida Energizante",', TEXT_WHITE, 40, None),
        (46, '        PrecioVenta = 2.50m, StockActual = 20, EstadoActivo = true', ACCENT_ORANGE, 40, None),
        (47, '    };', TEXT_WHITE, 20, None),
        (48, '    context.TurnosCaja.Add(turno); context.Productos.Add(producto);', TEXT_WHITE, 20, None),
        (49, '    await context.SaveChangesAsync();', ACCENT_PURPLE, 20, None),
        (50, '', TEXT_WHITE, 20, None),
        (51, '    var service = new VentaService(context, _mapper); // Inyeccion con Mock Moq', ACCENT_YELLOW, 20, None),
        (52, '    var ventaRequest = new VentaRequest {', TEXT_WHITE, 20, None),
        (53, '        IdTurno = 1, IdUsuario = usuarioId, IdMetodoPago = 1, MontoRecibido = 20.00m,', TEXT_WHITE, 40, None),
        (54, '        Detalles = [ new DetalleVentaRequest { IdProducto = 1, Cantidad = 2, PrecioUnitario = 2.50m } ]', ACCENT_ORANGE, 40, None),
        (55, '    };', TEXT_WHITE, 20, None),
        (56, '', TEXT_WHITE, 20, None),
        (57, '    // =============================================================================', ACCENT_GREEN, 20, None),
        (58, '    // 2. ACT (Ejecutar la logica de negocio bajo prueba)', ACCENT_YELLOW, 20, (50, 48, 25)),
        (59, '    // =============================================================================', ACCENT_GREEN, 20, None),
        (60, '    var resultado = await service.RegistrarVentaAsync(ventaRequest);', ACCENT_BLUE_LIGHT, 20, None),
        (61, '', TEXT_WHITE, 20, None),
        (62, '    // =============================================================================', ACCENT_GREEN, 20, None),
        (63, '    // 3. ASSERT (Verificacion estricta de invariantes con FluentAssertions)', ACCENT_CYAN, 20, (25, 45, 55)),
        (64, '    // =============================================================================', ACCENT_GREEN, 20, None),
        (65, '    resultado.Should().NotBeNull("la venta debe procesarse exitosamente");', COLOR_SUCCESS, 20, None),
        (66, '    resultado.Subtotal.Should().Be(5.00m, "2 unidades a $2.50 deben sumar $5.00");', COLOR_SUCCESS, 20, None),
        (67, '    resultado.Iva.Should().Be(0.65m, "IVA al 13% sobre $5.00 es exactamente $0.65");', COLOR_SUCCESS, 20, None),
        (68, '    resultado.Total.Should().Be(5.65m, "Total = $5.00 Subtotal + $0.65 IVA");', COLOR_SUCCESS, 20, None),
        (69, '    resultado.Vuelto.Should().Be(14.35m, "Vuelto = $20.00 recibido - $5.65 total");', COLOR_SUCCESS, 20, None),
        (70, '', TEXT_WHITE, 20, None),
        (71, '    // Validacion de persistencia: Reduccion atomica de inventario (20 - 2 = 18)', ACCENT_GREEN, 20, None),
        (72, '    var productoDb = await context.Productos.FindAsync(1);', TEXT_WHITE, 20, None),
        (73, '    productoDb!.StockActual.Should().Be(18, "el stock debio decrementar 2 unidades");', COLOR_SUCCESS, 20, None),
        (74, '}', TEXT_WHITE, 20, None),
    ]

    cy = code_y + 15
    for l_num, text, col, ind, bg in code_lines:
        if bg:
            draw.rectangle([code_x + 50, cy - 2, code_x + code_w - 20, cy + 18], fill=bg)
        draw.text((code_x + 12, cy), f"{l_num:2d}", fill=TEXT_MUTED, font=font_code_small)
        draw.text((code_x + 55 + ind, cy), text, fill=col, font=font_code)
        cy += 21

    # Right Column: Architectural Highlights Cards (Width: 470px)
    info_x, info_y, info_w, info_h = 1110, 115, 470, 865
    draw.rectangle([info_x, info_y, info_x + info_w, info_y + info_h], fill=BG_EDITOR, outline=BORDER_COLOR, width=1)
    
    draw.rectangle([info_x, info_y, info_x + info_w, info_y + 35], fill=BG_HEADER)
    draw.text((info_x + 15, info_y + 8), "PRINCIPIOS ARQUITECTONICOS DE LA SUITE", fill=TEXT_WHITE, font=font_bold)

    cards = [
        ("PATRON AAA (ARRANGE-ACT-ASSERT)",
         "Estructuracion canonica de pruebas segun ISO/IEC/IEEE 29119-4. "
         "Garantiza separacion total entre la preparacion del estado, la ejecucion del metodo y la validacion de resultados.",
         COLOR_SUCCESS, 130),
        
        ("AISLAMIENTO POR GUID EN MEMORIA",
         "Cada metodo invoca CreateInMemoryDbContext() generando una base de datos unica (Guid.NewGuid()). "
         "Esto erradica la contienda de hilos y garantiza ejecucion 100% determinista e idempotente.",
         ACCENT_CYAN, 275),
         
        ("DESACOPLAMIENTO DE MAPPERS CON MOQ",
         "La dependencia externa IMapper es provista mediante Moq, aislando estrictamente la logica contable "
         "y matematica del servicio VentaService sin evaluar componentes accesorios.",
         ACCENT_YELLOW, 420),
         
        ("VALIDACION DECLARATIVA CON FLUENTASSERTIONS",
         "Reemplaza el Assert tradicional por aserciones fluidas auto-descriptivas. "
         "Ante cualquier discrepancia de centavos en el IVA o cambio, arroja un diagnostico inmediato del motivo del fallo.",
         ACCENT_BLUE_LIGHT, 565),
         
        ("INTEGRIDAD ATOMICA DE INVENTARIO",
         "La prueba no solo valida el DTO de salida; inspecciona el contexto EF Core para certificar que el stock "
         "se decremento atomicamente y que se evita la sobreventa (overselling).",
         ACCENT_ORANGE, 710),
    ]

    for title, desc, col, y_pos in cards:
        c_box = [info_x + 15, info_y + y_pos - 80, info_x + info_w - 15, info_y + y_pos + 50]
        draw.rectangle(c_box, fill=CARD_BG, outline=col, width=2)
        draw.text((c_box[0] + 12, c_box[1] + 10), title, fill=col, font=font_bold)
        
        max_card_w = c_box[2] - c_box[0] - 24
        lines = wrap_text(desc, font_small, max_card_w, draw)
        ty = c_box[1] + 32
        for l in lines:
            draw.text((c_box[0] + 12, ty), l, fill=TEXT_WHITE, font=font_small)
            ty += 18

    img.save(os.path.join(OUTPUT_DIR, "arquitectura_codigo_unit_tests.png"), dpi=(150, 150))
    print("OK: arquitectura_codigo_unit_tests.png")


# -----------------------------------------------------------------------------
# IMAGE 3: ARQUITECTURA DE INTEGRACIÓN (CustomWebApplicationFactory & Endpoints)
# -----------------------------------------------------------------------------
def create_image_3():
    width, height = 1600, 1000
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Top Window Title Bar
    draw.rectangle([0, 0, width, 40], fill=BG_HEADER)
    draw.ellipse([width - 80, 12, width - 68, 24], fill=(235, 100, 100))
    draw.ellipse([width - 55, 12, width - 43, 24], fill=(245, 190, 70))
    draw.ellipse([width - 30, 12, width - 18, 24], fill=(100, 200, 100))
    draw.text((20, 10), "Visual Studio 2022 - TiendaGo.IntegrationTests / Infraestructura y Pruebas HTTP [TestServer + Minimal APIs]", fill=TEXT_WHITE, font=font_subtitle)

    # Editor Tabs
    draw.rectangle([0, 40, width, 75], fill=(37, 37, 38))
    draw.rectangle([10, 42, 330, 75], fill=BG_DARK, outline=(0, 122, 204), width=1)
    draw.text((25, 50), "C# CustomWebApplicationFactory.cs", fill=TEXT_WHITE, font=font_bold)
    draw.rectangle([340, 42, 630, 75], fill=BG_DARK, outline=COLOR_SUCCESS, width=1)
    draw.text((355, 50), "C# VentasEndpointsTests.cs", fill=TEXT_WHITE, font=font_bold)
    draw.rectangle([640, 42, 880, 75], fill=BG_TAB_INACTIVE)
    draw.text((655, 50), "C# SeguridadRBACTests.cs", fill=TEXT_MUTED, font=font_regular)

    # Sub-bar / Breadcrumb
    draw.rectangle([0, 75, width, 105], fill=(30, 30, 30), outline=BORDER_COLOR, width=1)
    draw.text((20, 82), "ARQUITECTURA DE INTEGRACION: WebApplicationFactory<Program> -> Sustitucion IoC en Memoria -> TestServer HTTP", fill=ACCENT_CYAN, font=font_code_small)

    # Left Column: CustomWebApplicationFactory.cs (Width: 770px)
    left_x, left_y, left_w, left_h = 20, 115, 770, 740
    draw.rectangle([left_x, left_y, left_x + left_w, left_y + left_h], fill=BG_EDITOR, outline=BORDER_COLOR, width=1)
    
    draw.rectangle([left_x, left_y, left_x + left_w, left_y + 35], fill=BG_HEADER)
    draw.text((left_x + 15, left_y + 8), "1. INFRAESTRUCTURA: CustomWebApplicationFactory.cs", fill=ACCENT_YELLOW, font=font_bold)

    factory_lines = [
        (18, "public class CustomWebApplicationFactory : WebApplicationFactory<Program>", ACCENT_BLUE_LIGHT),
        (19, "{", TEXT_WHITE),
        (20, '    private readonly string _dbName = $"TiendaGoTestDb_{Guid.NewGuid()}";', ACCENT_ORANGE),
        (21, "", TEXT_WHITE),
        (51, "    protected override void ConfigureWebHost(IWebHostBuilder builder)", ACCENT_YELLOW),
        (52, "    {", TEXT_WHITE),
        (53, '        builder.UseEnvironment("Testing");', TEXT_WHITE),
        (54, "        builder.ConfigureServices(services =>", ACCENT_BLUE_LIGHT),
        (55, "        {", TEXT_WHITE),
        (56, "            // PASO 1: Eliminar registro de PostgreSQL (Npgsql) real", ACCENT_GREEN),
        (57, "            var descriptors = services.Where(d =>", TEXT_MUTED),
        (58, "                d.ServiceType == typeof(DbContextOptions<TiendaGoDbContext>)).ToList();", TEXT_MUTED),
        (59, "            foreach (var d in descriptors) services.Remove(d);", ACCENT_ORANGE),
        (60, "", TEXT_WHITE),
        (61, "            // PASO 2: Inyectar DbContext con proveedor InMemory aislado", ACCENT_GREEN),
        (62, "            services.AddDbContext<TiendaGoDbContext>(options =>", ACCENT_CYAN),
        (63, "                options.UseInMemoryDatabase(_dbName));", COLOR_SUCCESS),
        (64, "", TEXT_WHITE),
        (65, "            // PASO 3: Construir IoC y sembrar datos deterministas", ACCENT_GREEN),
        (66, "            var sp = services.BuildServiceProvider();", TEXT_WHITE),
        (67, "            using var scope = sp.CreateScope();", TEXT_WHITE),
        (68, "            var db = scope.ServiceProvider.GetRequiredService<TiendaGoDbContext>();", TEXT_WHITE),
        (69, "            db.Database.EnsureCreated();", ACCENT_PURPLE),
        (70, "            SeedTestData(db); // Admin, Cajero, Productos, Turnos", ACCENT_YELLOW),
        (71, "        });", TEXT_WHITE),
        (72, "    }", TEXT_WHITE),
        (73, "", TEXT_WHITE),
        (150, "    // Generador de Headers de Autorizacion con Tokens JWT firmados", ACCENT_GREEN),
        (151, "    public AuthenticationHeaderValue GetBearerHeader(string user, string rol)", ACCENT_CYAN),
        (152, "    {", TEXT_WHITE),
        (153, "        var token = GenerarJwtToken(user, rol); // Claims: Sub, Role, Email", TEXT_WHITE),
        (154, '        return new AuthenticationHeaderValue("Bearer", token);', COLOR_SUCCESS),
        (155, "    }", TEXT_WHITE),
        (156, "}", TEXT_WHITE),
    ]

    fy = left_y + 45
    for l_num, text, col in factory_lines:
        draw.text((left_x + 10, fy), f"{l_num:3d}", fill=TEXT_MUTED, font=font_code_small)
        draw.text((left_x + 45, fy), text, fill=col, font=font_code_small)
        fy += 20

    # Right Column: VentasEndpointsTests.cs (Width: 770px)
    right_x, right_y, right_w, right_h = 810, 115, 770, 740
    draw.rectangle([right_x, right_y, right_x + right_w, right_y + right_h], fill=BG_EDITOR, outline=BORDER_COLOR, width=1)
    
    draw.rectangle([right_x, right_y, right_x + right_w, right_y + 35], fill=BG_HEADER)
    draw.text((right_x + 15, right_y + 8), "2. SUITE DE INTEGRACION: VentasEndpointsTests.cs", fill=COLOR_SUCCESS, font=font_bold)

    test_lines = [
        (20, "public class VentasEndpointsTests : IClassFixture<CustomWebApplicationFactory>", ACCENT_BLUE_LIGHT),
        (21, "{", TEXT_WHITE),
        (22, "    private readonly HttpClient _client;", TEXT_WHITE),
        (23, "    private readonly CustomWebApplicationFactory _factory;", TEXT_WHITE),
        (24, "", TEXT_WHITE),
        (30, "    public VentasEndpointsTests(CustomWebApplicationFactory factory)", ACCENT_YELLOW),
        (31, "    {", TEXT_WHITE),
        (32, "        _factory = factory;", TEXT_WHITE),
        (33, "        _client = factory.CreateClient(); // Instancia TestServer", COLOR_SUCCESS),
        (34, "        // Inyectar JWT Bearer de Administrador en cabeceras HTTP", ACCENT_GREEN),
        (35, '        _client.DefaultRequestHeaders.Authorization =', ACCENT_CYAN),
        (36, '            factory.GetBearerHeader("Admin", "Administrador");', ACCENT_ORANGE),
        (37, "    }", TEXT_WHITE),
        (38, "", TEXT_WHITE),
        (45, '    [Fact(DisplayName = "IT-POS-01: POST /api/ventas -> 201 Created y descuento de stock")]', ACCENT_YELLOW),
        (46, "    public async Task RegistrarVenta_ConStockSuficiente_Devuelve201YDecrementaStock()", ACCENT_BLUE_LIGHT),
        (47, "    {", TEXT_WHITE),
        (48, "        // ARRANGE: Preparacion de DTO de venta transaccional", ACCENT_GREEN),
        (49, "        var request = new VentaRequest { Cantidad = 3, MontoRecibido = 100.00m };", TEXT_WHITE),
        (50, "        int stockAntes = ObtenerStockActual(IdProducto1); // 50 unidades", TEXT_MUTED),
        (51, "", TEXT_WHITE),
        (52, "        // ACT: Ejecucion de peticion HTTP sintetica sobre Minimal API", ACCENT_YELLOW),
        (53, '        var response = await _client.PostAsJsonAsync("/api/ventas/", request);', COLOR_SUCCESS),
        (54, "", TEXT_WHITE),
        (55, "        // ASSERT: Validacion de codigo de estado HTTP 201 Created", ACCENT_CYAN),
        (56, "        response.StatusCode.Should().Be(HttpStatusCode.Created);", COLOR_SUCCESS),
        (57, "", TEXT_WHITE),
        (58, "        // Validacion de persistencia relacional en BD InMemory", ACCENT_GREEN),
        (59, "        int stockDespues = ObtenerStockActual(IdProducto1);", TEXT_WHITE),
        (60, '        stockDespues.Should().Be(stockAntes - 3, "el stock debio decrementar 3");', COLOR_SUCCESS),
        (61, "    }", TEXT_WHITE),
        (62, "}", TEXT_WHITE),
    ]

    ty = right_y + 45
    for l_num, text, col in test_lines:
        draw.text((right_x + 10, ty), f"{l_num:3d}", fill=TEXT_MUTED, font=font_code_small)
        draw.text((right_x + 45, ty), text, fill=col, font=font_code_small)
        ty += 20

    # Bottom Architectural Summary Banner (Full width)
    bot_y = 870
    draw.rectangle([20, bot_y, width - 20, bot_y + 110], fill=(25, 30, 40), outline=ACCENT_BLUE, width=2)
    draw.text((35, bot_y + 10), "CARACTERISTICAS ARQUITECTONICAS DEL PIPELINE DE PRUEBAS DE INTEGRACION", fill=TEXT_WHITE, font=font_bold)
    
    feats = [
        "- Servidor Virtualizado (TestServer): Ejecucion en proceso dentro de memoria RAM, sin latencia TCP ni necesidad de IIS/Kestrel externo.",
        "- Inyeccion de Dependencias Reemplazada: Sustitucion de Npgsql por InMemoryDatabase sin alterar el codigo fuente de produccion.",
        "- Pipeline HTTP Completo: Valida Routing Minimal APIs, serializacion JSON, Middleware de JWT y politicas de autorizacion RBAC.",
        "- Determinismo Absoluto: Cada suite corre sobre su propia instancia aislada evitando estados residuales entre pruebas."
    ]
    f_y = bot_y + 32
    for f in feats:
        draw.text((35, f_y), f, fill=TEXT_WHITE, font=font_small)
        f_y += 18

    img.save(os.path.join(OUTPUT_DIR, "arquitectura_codigo_integration_tests.png"), dpi=(150, 150))
    print("OK: arquitectura_codigo_integration_tests.png")

create_image_1()
create_image_2()
create_image_3()
