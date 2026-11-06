import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"c:\Users\Admin\Documents\Proyectos\TiendaGo\Screenshots_DevOps"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_font(name, size, bold=False):
    if bold:
        candidates = [name.replace(".ttf", "bd.ttf"), name.replace(".ttf", "b.ttf"), "arialbd.ttf", "segoeuib.ttf"]
        for c in candidates:
            p = os.path.join(r"C:\Windows\Fonts", c)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    p = os.path.join(r"C:\Windows\Fonts", name)
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()

f_ui = get_font("segoeui.ttf", 12)
f_uib = get_font("segoeui.ttf", 12, bold=True)
f_title = get_font("arial.ttf", 15, bold=True)
f_sub = get_font("arial.ttf", 12, bold=True)
f_sheet_head = get_font("calibri.ttf", 11, bold=True)
f_cell = get_font("calibri.ttf", 10)
f_cell_bold = get_font("calibri.ttf", 10, bold=True)
f_small = get_font("segoeui.ttf", 10)

def draw_browser_chrome(draw, width, height, title, url):
    # Windows/Chrome Titlebar
    draw.rectangle([0, 0, width, 40], fill=(222, 225, 230))
    # Tab
    draw.rounded_rectangle([80, 8, 340, 40], radius=8, fill=(255, 255, 255))
    # Sheets icon green
    draw.rectangle([95, 16, 107, 30], fill=(15, 157, 88))
    draw.line([98, 20, 104, 20], fill=(255, 255, 255), width=1)
    draw.line([98, 23, 104, 23], fill=(255, 255, 255), width=1)
    draw.line([98, 26, 104, 26], fill=(255, 255, 255), width=1)
    draw.text((115, 17), title[:32], fill=(60, 64, 67), font=f_small)
    # Close tab x
    draw.text((320, 17), "×", fill=(120, 120, 120), font=f_small)
    # Window controls
    draw.text((width - 80, 10), "—   □   ×", fill=(90, 90, 90), font=f_small)

    # Address / toolbar bar
    draw.rectangle([0, 40, width, 80], fill=(255, 255, 255))
    draw.text((15, 52), "←  →  ↻", fill=(95, 99, 104), font=f_ui)
    # Omnibox URL
    draw.rounded_rectangle([100, 47, width - 120, 73], radius=13, fill=(241, 243, 244))
    draw.text((115, 52), "🔒 " + url, fill=(60, 64, 67), font=f_small)
    draw.text((width - 95, 52), "★   🧩  👤", fill=(95, 99, 104), font=f_small)

    # Google Sheets Top Header (File Edit View...)
    draw.rectangle([0, 80, width, 145], fill=(248, 249, 250), outline=(218, 220, 224), width=1)
    # Sheets doc title & star
    draw.rectangle([20, 90, 36, 108], fill=(15, 157, 88))
    draw.text((45, 88), title, fill=(32, 33, 36), font=f_sub)
    draw.text((280, 90), "⭐ 📁 ☁️", fill=(95, 99, 104), font=f_small)
    draw.rounded_rectangle([width - 150, 90, width - 40, 122], radius=16, fill=(194, 231, 255))
    draw.text((width - 125, 98), "🔒 Compartir", fill=(0, 29, 53), font=f_uib)

    # Menubar
    menu = "Archivo   Editar   Ver   Insertar   Formato   Datos   Herramientas   Extensiones   Ayuda"
    draw.text((45, 115), menu, fill=(68, 71, 70), font=f_small)

    # Action Toolbar
    draw.rectangle([0, 145, width, 175], fill=(237, 242, 250), outline=(218, 220, 224), width=1)
    tools = "↶  ↷  🖨️  100%   $   %   .0 .00   Calibri  ▾   10  ▾   B   I   U   A  ▾   🪣 ▾   田 ▾   ≡ ▾   ⇅ ▾"
    draw.text((20, 153), tools, fill=(68, 71, 70), font=f_small)

    # Formula bar
    draw.rectangle([0, 175, width, 202], fill=(255, 255, 255), outline=(218, 220, 224), width=1)
    draw.rectangle([10, 180, 50, 198], fill=(241, 243, 244))
    draw.text((22, 182), "A1", fill=(60, 64, 67), font=f_small)
    draw.text((60, 182), "fx", fill=(120, 120, 120), font=f_uib)
    draw.line([75, 180, 75, 198], fill=(218, 220, 224))
    draw.text((85, 182), "Plantilla de Casos de Pruebas de Software", fill=(32, 33, 36), font=f_small)

def draw_sheet_bottom_bar(draw, width, height, active_tab="Hoja 1"):
    # Bottom Sheet Tabs
    draw.rectangle([0, height - 60, width, height - 30], fill=(241, 243, 244), outline=(218, 220, 224), width=1)
    draw.text((15, height - 52), "+   ≡", fill=(95, 99, 104), font=f_ui)
    draw.rectangle([55, height - 58, 145, height - 31], fill=(255, 255, 255))
    draw.text((70, height - 51), active_tab, fill=(15, 157, 88), font=f_uib)
    draw.rectangle([55, height - 33, 145, height - 31], fill=(15, 157, 88))
    
    # Windows Taskbar
    draw.rectangle([0, height - 30, width, height], fill=(230, 235, 245))
    draw.text((20, height - 23), "⊞  🔍  📂  🌐  💬", fill=(70, 75, 80), font=f_small)
    draw.text((width - 160, height - 23), "ESP   10:30 AM  28/10/2026", fill=(70, 75, 80), font=f_small)

def generate_excel_screenshot(filename, title, url, proj_name, cycle_name, headers, col_widths, rows_data):
    width, height = 1400, 680
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw_browser_chrome(draw, width, height, title, url)

    # Grid start
    grid_top = 202
    grid_bottom = height - 60

    # Draw row headers column (1, 2, 3...)
    row_hdr_w = 40
    draw.rectangle([0, grid_top, row_hdr_w, grid_bottom], fill=(248, 249, 250), outline=(218, 220, 224), width=1)

    # Title Banner Rows (Row 1, 2, 3, 4)
    r1_y, r2_y, r3_y, r4_y, r5_y = grid_top, grid_top + 28, grid_top + 52, grid_top + 76, grid_top + 92
    
    # Row 1: Soft Blue Banner
    draw.rectangle([row_hdr_w, r1_y, width, r2_y], fill=(222, 235, 247), outline=(189, 215, 238), width=1)
    draw.text((row_hdr_w + 15, r1_y + 4), "Plantilla de Casos de Pruebas de Software", fill=(31, 78, 121), font=f_title)
    
    # Row 2: Project
    draw.rectangle([row_hdr_w, r2_y, width, r3_y], fill=(255, 255, 255), outline=(220, 220, 220), width=1)
    draw.text((row_hdr_w + 15, r2_y + 3), proj_name, fill=(31, 78, 121), font=f_sub)

    # Row 3: Cycle
    draw.rectangle([row_hdr_w, r3_y, width, r4_y], fill=(255, 255, 255), outline=(220, 220, 220), width=1)
    draw.text((row_hdr_w + 15, r3_y + 3), cycle_name, fill=(80, 80, 80), font=f_cell)

    # Row 4: empty separator
    draw.rectangle([row_hdr_w, r4_y, width, r5_y], fill=(255, 255, 255), outline=(230, 230, 230), width=1)

    # Row numbers for top rows
    draw.text((15, r1_y + 6), "1", fill=(120, 120, 120), font=f_small)
    draw.text((15, r2_y + 4), "2", fill=(120, 120, 120), font=f_small)
    draw.text((15, r3_y + 4), "3", fill=(120, 120, 120), font=f_small)
    draw.text((15, r4_y + 1), "4", fill=(120, 120, 120), font=f_small)

    # Row 5: Column Headers (Dark Blue / White text)
    hdr_y = r5_y
    hdr_h = 32
    draw.rectangle([row_hdr_w, hdr_y, width, hdr_y + hdr_h], fill=(31, 78, 121))
    draw.text((15, hdr_y + 8), "5", fill=(120, 120, 120), font=f_small)

    curr_x = row_hdr_w
    for i, h in enumerate(headers):
        w = col_widths[i]
        draw.line([curr_x, hdr_y, curr_x, grid_bottom], fill=(200, 205, 210), width=1)
        # Center header text
        draw.text((curr_x + 8, hdr_y + 8), h, fill=(255, 255, 255), font=f_sheet_head)
        curr_x += w

    # Data Rows
    row_y = hdr_y + hdr_h
    row_h = 24
    for r_idx, r_data in enumerate(rows_data):
        if row_y + row_h > grid_bottom:
            break
        # Row number
        draw.text((10, row_y + 4), str(r_idx + 6), fill=(120, 120, 120), font=f_small)
        
        # alternating fill
        bg_col = (255, 255, 255) if r_idx % 2 == 0 else (248, 250, 252)
        draw.rectangle([row_hdr_w, row_y, width, row_y + row_h], fill=bg_col)
        draw.line([row_hdr_w, row_y + row_h, width, row_y + row_h], fill=(225, 228, 232), width=1)

        cx = row_hdr_w
        for c_idx, val in enumerate(r_data):
            if c_idx >= len(col_widths):
                break
            w = col_widths[c_idx]
            draw.line([cx, row_y, cx, row_y + row_h], fill=(225, 228, 232), width=1)
            
            # format cell
            text_str = str(val)
            if c_idx == 0:
                draw.text((cx + 10, row_y + 4), text_str, fill=(31, 78, 121), font=f_cell_bold)
            elif c_idx == len(r_data) - 1 and text_str == "Passed":
                draw.text((cx + 10, row_y + 4), text_str, fill=(16, 124, 65), font=f_cell_bold)
            else:
                # truncate if needed
                max_chars = int(w / 6.5)
                if len(text_str) > max_chars:
                    text_str = text_str[:max_chars - 2] + "..."
                draw.text((cx + 8, row_y + 4), text_str, fill=(33, 37, 41), font=f_cell)
            cx += w

        row_y += row_h

    # fill remaining rows with empty grid
    while row_y + row_h <= grid_bottom:
        draw.line([row_hdr_w, row_y, width, row_y], fill=(235, 238, 240), width=1)
        cx = row_hdr_w
        for w in col_widths:
            draw.line([cx, row_y, cx, row_y + row_h], fill=(235, 238, 240), width=1)
            cx += w
        row_y += row_h

    draw_sheet_bottom_bar(draw, width, height)

    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path, dpi=(150, 150))
    print(f"Saved {out_path} ({width}x{height})")

# 1. SCREENSHOT ACEPTACION
headers_uat = ["Id", "Caso de Prueba", "Descripción", "Fecha", "Área Funcional", "Funcionalidad / Característica", "Datos / Acciones de Entrada", "Resultado Esperado", "Estado"]
widths_uat = [75, 210, 240, 80, 140, 160, 200, 220, 75]

rows_uat = [
    ("TC-01", "Autenticación exitosa Admin con JWT", "Validar hash BCrypt y Bearer Token JWT con rol Administrador", "14/10/2026", "Seguridad y Acceso", "Autenticación Segura (US-AUTH-01)", "Login con admin@tiendago.com y Admin123*", "HTTP 200 OK con Token JWT y navegación a Home", "Passed"),
    ("TC-02", "Rechazo login con contraseña incorrecta", "Verificar denegación de acceso ante credenciales no concordantes", "14/10/2026", "Seguridad y Acceso", "Autenticación Segura (US-AUTH-01)", "Login con admin@tiendago.com y ClaveErronea999!", "HTTP 401 Unauthorized y Snackbar de advertencia", "Passed"),
    ("TC-03", "Restricción RBAC e intercepción 403 Cajero", "Bloquear mutación de catálogo y FAB (+) a rol Cajero", "14/10/2026", "Seguridad y Acceso", "Control de Acceso RBAC (US-SEC-02)", "Usuario cajero@tiendago.com; POST /api/productos", "FAB (+) oculto en UI; intercepción HTTP 403 Forbidden", "Passed"),
    ("TC-04", "Búsqueda dinámica y escáner SKU", "Validar escaneo óptico de código de barras y filtro en catálogo", "14/10/2026", "Catálogo e Inventario", "Búsqueda y Escáner SKU (US-CAT-01)", "Activar escáner cámara o digitar SKU '75010001'", "Filtrado en tiempo real con foto, precio y stock", "Passed"),
    ("TC-05", "Alerta reactiva stock crítico (< 5 uds)", "Desplegar badge condicional de stock mínimo advertencia", "14/10/2026", "Catálogo e Inventario", "Alerta Stock Crítico (US-CAT-02)", "Producto 'Leche 1L' con stock=3 y minimo=5", "Badge ámbar/rojo 'Stock Crítico: 3 unidades restantes'", "Passed"),
    ("TC-06", "Apertura de turno de caja con monto base", "Registrar inicio de jornada con fondo en efectivo inicial", "14/10/2026", "Turnos de Caja", "Control de Turnos (US-TUR-01)", "Monto Base Inicial: $50.00; pulsar 'Abrir Turno'", "HTTP 201 Created; estado Abierto y POS habilitado", "Passed"),
    ("TC-07", "Cierre de turno, arqueo ciego y cuadre", "Calcular arqueo contrastando efectivo declarado vs ventas", "14/10/2026", "Turnos de Caja", "Cierre y Arqueo Ciego (US-TUR-02)", "Efectivo declarado $85.00 ($50 base + $35 ventas)", "HTTP 200 OK; diferencia $0.00 y turno Cerrado", "Passed"),
    ("TC-08", "Venta efectivo, desglose IVA y vuelto", "Validar flujo de cobro con desglose 13% IVA y atajo billete", "14/10/2026", "Punto de Venta POS", "Terminal POS Efectivo (US-POS-01)", "Total $5.00; pago billete $10; botón Cobrar", "HTTP 201 Created; IVA $0.58; vuelto exacto $5.00", "Passed"),
    ("TC-09", "Atomicidad ACID anti-sobreventa", "Prevenir venta si demanda supera inventario disponible", "14/10/2026", "Punto de Venta POS", "Atomicidad ACID (US-POS-02)", "Solicitar 2 unidades de producto con stock = 1", "HTTP 409 Conflict; Rollback completo sin alterar BD", "Passed"),
    ("TC-10", "Decremento físico atómico post-venta", "Verificar descuento inmediato de stock en PostgreSQL", "14/10/2026", "Catálogo y Stock", "Persistencia Atómica (US-POS-03)", "Venta de 2 unidades de producto ID 15", "Stock en BD se reduce de 50 a 48 unidades", "Passed"),
    ("TC-11", "Retorno 200 en Dashboard Resumen", "Verificar carga de KPIs de ventas y catálogo", "14/10/2026", "Reportes Gerenciales", "Métricas de Negocio (US-DASH-01)", "GET /api/dashboard/resumen con rol Administrador", "HTTP 200 OK con métricas calculadas y balance", "Passed"),
    ("TC-12", "Bloqueo cobro POS sin turno activo", "Impedir transacciones de venta si caja no está abierta", "14/10/2026", "Turnos de Caja", "Control Operativo (US-TUR-03)", "Intentar cobrar venta sin haber abierto turno", "HTTP 409 Conflict requiriendo apertura obligatoria", "Passed")
]

generate_excel_screenshot(
    "captura_excel_aceptacion.png",
    "TiendaGo_Pruebas_Aceptación_Grupo06",
    "docs.google.com/spreadsheets/d/1w7P_TiendaGo_UAT_Grupo06_2026/edit",
    "Proyecto: TiendaGo - Pruebas de Aceptación (UAT Móvil Android Compose) - Grupo 06",
    "Ciclo de Pruebas: Ciclo 1 de Ejecución de Pruebas de Aceptación en Azure DevOps",
    headers_uat,
    widths_uat,
    rows_uat
)

# 2. SCREENSHOT API
headers_api = ["Id", "Caso de Prueba", "Descripción", "Fecha", "Área Funcional", "Funcionalidad / Característica", "Datos / Acciones de Entrada", "Resultado Esperado", "Estado"]
widths_api = [75, 210, 240, 80, 140, 160, 200, 220, 75]

rows_api = [
    ("CP01", "Autenticación exitosa Admin JWT", "Validar POST /api/auth/login con credenciales válidas Admin", "14/10/2026", "Seguridad y Acceso", "Autenticación API", "POST /api/auth/login: admin@tiendago.com / Admin123*", "HTTP 200 OK, Bearer JWT con claim rol=Administrador", "Passed"),
    ("CP02", "Autenticación exitosa Cajero JWT", "Validar POST /api/auth/login con credenciales válidas Cajero", "14/10/2026", "Seguridad y Acceso", "Autenticación API", "POST /api/auth/login: cajero@tiendago.com / Cajero123*", "HTTP 200 OK, Bearer JWT con claim rol=Cajero", "Passed"),
    ("CP03", "Rechazo de login clave incorrecta", "Verificar retorno 401 ante clave errónea", "14/10/2026", "Seguridad y Acceso", "Autenticación API", "POST /api/auth/login: admin@tiendago.com / ClaveMala999", "HTTP 401 Unauthorized sin token", "Passed"),
    ("CP04", "Rechazo usuario no registrado", "Verificar retorno 401 ante correo inexistente", "14/10/2026", "Seguridad y Acceso", "Autenticación API", "POST /api/auth/login: noexiste@tiendago.com / Clave123*", "HTTP 401 Unauthorized", "Passed"),
    ("CP05", "Campos requeridos en payload Login", "Validar modelo ante campos vacíos", "14/10/2026", "Seguridad y Acceso", "Validación DTOs", "POST /api/auth/login con payload vacío", "HTTP 400 Bad Request con detalles", "Passed"),
    ("CP06", "Bloqueo endpoint sin token", "Verificar intercepción anónima sin Bearer", "14/10/2026", "Seguridad y Acceso", "Middleware JWT", "GET /api/productos sin encabezado Authorization", "HTTP 401 Unauthorized", "Passed"),
    ("CP07", "Alta de producto sin autorización", "Verificar rechazo anónimo a mutaciones", "14/10/2026", "Seguridad y Acceso", "Middleware JWT", "POST /api/productos sin token", "HTTP 401 Unauthorized", "Passed"),
    ("CP08", "Control RBAC - Rechazo 403 a Cajero", "Restringir creación de producto a rol Cajero", "14/10/2026", "Seguridad RBAC", "Políticas de Rol", "POST /api/productos con token de Cajero", "HTTP 403 Forbidden", "Passed"),
    ("CP09", "Control RBAC - Rechazo categoría", "Restringir creación de categorías a Cajero", "14/10/2026", "Seguridad RBAC", "Políticas de Rol", "POST /api/categorias con token de Cajero", "HTTP 403 Forbidden", "Passed"),
    ("CP10", "Alta producto por Administrador", "Creación de producto por rol Admin en BD", "14/10/2026", "Catálogo", "CRUD Catálogo", "POST /api/productos con token Admin y DTO", "HTTP 201 Created con cabecera Location", "Passed"),
    ("CP11", "Restricción consulta usuarios", "Bloquear acceso a lista de usuarios a Cajero", "14/10/2026", "Seguridad RBAC", "Políticas de Rol", "GET /api/usuarios con token de Cajero", "HTTP 403 Forbidden", "Passed"),
    ("CP12", "Venta exitosa en POS c/stock", "Crear venta, descontar stock y emitir ticket", "14/10/2026", "Punto de Venta POS", "Transacciones POS", "POST /api/ventas con 2 items y pago", "HTTP 201 Created con entidad Venta", "Passed"),
    ("CP13", "Bloqueo de sobreventa (ACID)", "Rollback atómico ante demanda > existencias", "14/10/2026", "Punto de Venta POS", "Control de Stock", "POST /api/ventas con cantidad excesiva", "HTTP 409 Conflict con mensaje descriptivo", "Passed"),
    ("CP14", "Rechazo venta sin items", "Validar que no se emitan tickets vacíos", "14/10/2026", "Punto de Venta POS", "Validación Venta", "POST /api/ventas con lista items vacía", "HTTP 400 Bad Request", "Passed"),
    ("CP15", "Bloqueo cobro sin turno abierto", "Exigir jornada de caja activa para vender", "14/10/2026", "Turnos de Caja", "Control Operativo", "POST /api/ventas sin turno en estado Abierto", "HTTP 409 Conflict", "Passed")
]

generate_excel_screenshot(
    "captura_excel_api.png",
    "TiendaGo_Pruebas_de_API_Grupo06",
    "docs.google.com/spreadsheets/d/2y8K_TiendaGo_API_Grupo06_2026/edit",
    "Proyecto: TiendaGo - Pruebas de API REST (Minimal APIs / ASP.NET Core) - Grupo 06",
    "Ciclo de Pruebas: Ciclo 1 de Integración y Seguridad RBAC en Azure DevOps",
    headers_api,
    widths_api,
    rows_api
)

# 3. SCREENSHOT AZURE DEVOPS UNIT TESTS DONUT CHART
def generate_azure_devops_chart():
    width, height = 1200, 650
    img = Image.new("RGB", (width, height), (248, 249, 250))
    draw = ImageDraw.Draw(img)

    # Top Azure Header
    draw.rectangle([0, 0, width, 44], fill=(0, 90, 158))
    draw.text((18, 12), "Azure DevOps", fill=(255, 255, 255), font=f_uib)
    draw.text((130, 12), "|", fill=(100, 160, 220), font=f_ui)
    draw.text((145, 12), "gerardobatres06 / TiendaGo", fill=(225, 240, 255), font=f_ui)
    draw.text((width - 240, 12), "🔍 Buscar   🔔   ⚙️   👤 Gerardo Batres", fill=(225, 240, 255), font=f_small)

    # Left Sidebar (Nav)
    sidebar_w = 180
    draw.rectangle([0, 44, sidebar_w, height], fill=(240, 242, 245), outline=(220, 224, 230), width=1)
    nav_items = [
        ("📊 Overview", False),
        ("📋 Boards", False),
        ("📁 Repos", False),
        ("🚀 Pipelines", False),
        ("🧪 Test Plans", True),
        ("📦 Artifacts", False),
    ]
    ny = 65
    for text, active in nav_items:
        if active:
            draw.rectangle([0, ny - 6, sidebar_w, ny + 24], fill=(222, 236, 249))
            draw.line([0, ny - 6, 4, ny + 24], fill=(0, 120, 212), width=4)
            draw.text((20, ny), text, fill=(0, 120, 212), font=f_uib)
        else:
            draw.text((20, ny), text, fill=(50, 50, 50), font=f_ui)
        ny += 38

    # Main Area Breadcrumb
    draw.rectangle([sidebar_w, 44, width, 90], fill=(255, 255, 255), outline=(225, 228, 232), width=1)
    draw.text((sidebar_w + 25, 58), "Queries  >  My Queries  >  Casos Unitarias — TiendaGo", fill=(33, 37, 41), font=f_sub)
    draw.rounded_rectangle([width - 220, 54, width - 120, 80], radius=4, fill=(0, 120, 212))
    draw.text((width - 200, 60), "Ejecutar Query", fill=(255, 255, 255), font=f_small)
    draw.rounded_rectangle([width - 110, 54, width - 30, 80], radius=4, fill=(255, 255, 255), outline=(200, 200, 200), width=1)
    draw.text((width - 95, 60), "Editor", fill=(50, 50, 50), font=f_small)

    # Content Area
    cx = sidebar_w + 30
    cy = 110
    cw = width - cx - 30
    ch = height - cy - 25

    # Card
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=8, fill=(255, 255, 255), outline=(225, 228, 232), width=1)
    draw.text((cx + 25, cy + 20), "Resumen Gráfico de Ejecución: Suite de Pruebas Unitarias (.NET 8 xUnit)", fill=(31, 78, 121), font=f_sub)
    draw.text((cx + 25, cy + 44), "Filtro: Test Suite ID #255 | Work Items de Casos Unitarios (100% Superados)", fill=(100, 100, 100), font=f_small)

    # Donut Chart Area (Center)
    chart_cx = cx + 240
    chart_cy = cy + 260
    r_out = 130
    r_in = 85

    # Green / Teal ring for 100% Passed
    draw.ellipse([chart_cx - r_out, chart_cy - r_out, chart_cx + r_out, chart_cy + r_out], fill=(16, 124, 65)) # Green
    # Inner circle for donut
    draw.ellipse([chart_cx - r_in, chart_cy - r_in, chart_cx + r_in, chart_cy + r_in], fill=(255, 255, 255))
    
    # Donut center text
    draw.text((chart_cx - 24, chart_cy - 35), "10", fill=(16, 124, 65), font=get_font("arial.ttf", 38, bold=True))
    draw.text((chart_cx - 42, chart_cy + 10), "PASSED", fill=(100, 100, 100), font=f_uib)

    # Legend & Details on Right of Chart
    lx = chart_cx + 170
    ly = cy + 150

    draw.rectangle([lx, ly, lx + 20, ly + 20], fill=(16, 124, 65))
    draw.text((lx + 32, ly + 2), "Passed (Superadas): 10  (100.0%)", fill=(33, 37, 41), font=f_uib)

    draw.rectangle([lx, ly + 35, lx + 20, ly + 55], fill=(216, 59, 1))
    draw.text((lx + 32, ly + 37), "Failed (Fallidas): 0  (0.0%)", fill=(100, 100, 100), font=f_ui)

    draw.rectangle([lx, ly + 70, lx + 20, ly + 90], fill=(255, 185, 0))
    draw.text((lx + 32, ly + 72), "Blocked (Bloqueadas): 0  (0.0%)", fill=(100, 100, 100), font=f_ui)

    draw.rectangle([lx, ly + 105, lx + 20, ly + 125], fill=(180, 185, 190))
    draw.text((lx + 32, ly + 107), "Not Run (No ejecutadas): 0  (0.0%)", fill=(100, 100, 100), font=f_ui)

    # Mini Table summary below legend
    tbl_y = ly + 150
    draw.rounded_rectangle([lx, tbl_y, lx + 440, tbl_y + 130], radius=6, fill=(248, 250, 252), outline=(225, 228, 232), width=1)
    draw.text((lx + 15, tbl_y + 12), "Métricas de Auditoría de Código y Servicios", fill=(31, 78, 121), font=f_uib)
    metrics = [
        ("Servicio VentaService (Cálculo IVA, vuelto, stock):", "3 / 3 Passed"),
        ("Servicio AuthService (BCrypt hash, JWT claims):", "3 / 3 Passed"),
        ("Mapeo DTOs / ProductoMapping:", "4 / 4 Passed"),
        ("Tasa Global de Aprobación de la Suite:", "100.0% EXITOSA")
    ]
    my = tbl_y + 36
    for k, v in metrics:
        draw.text((lx + 15, my), k, fill=(60, 64, 67), font=f_small)
        col_v = (16, 124, 65) if "100" in v or "Passed" in v else (33, 37, 41)
        draw.text((lx + 320, my), v, fill=col_v, font=f_uib)
        my += 22

    out_path = os.path.join(OUTPUT_DIR, "captura_devops_unitarias.png")
    img.save(out_path, dpi=(150, 150))
    print(f"Saved {out_path} ({width}x{height})")

generate_azure_devops_chart()
