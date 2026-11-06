"""
Documento de Contexto Completo del Proyecto TiendaGo
Genera un .docx profesional con toda la información del proyecto:
arquitectura, modelos, endpoints, servicios, seguridad, BD, pruebas, despliegue.
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DIR_BASE = r"c:\Users\Admin\Documents\Proyectos\TiendaGo"
OUTPUT   = os.path.join(DIR_BASE, "Contexto_Proyecto_TiendaGo.docx")
LOGO     = os.path.join(DIR_BASE, "Screenshots_DevOps", "portada_logos.png")
DIAGRAMA = os.path.join(DIR_BASE, "Screenshots_DevOps", "diagrama_despliegue_tiendago.png")
ARCH_IMG = os.path.join(DIR_BASE, "Screenshots_DevOps", "arquitectura_solucion_proyectos.png")

C_TITULO  = RGBColor(0x1F, 0x36, 0x64)
C_S2      = RGBColor(0x13, 0x63, 0x8E)
C_BODY    = RGBColor(0x0A, 0x0A, 0x0A)
C_CODE    = RGBColor(0x17, 0x5B, 0x2E)
C_MUTED   = RGBColor(0x40, 0x40, 0x40)
C_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
C_WARN    = RGBColor(0x7B, 0x1F, 0x1F)
HDR_HEX   = "1F3864"
ALT_HEX   = "EBF5FB"
CODE_HEX  = "F4F6F9"

def set_cell_bg(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=55, bottom=55, left=90, right=90):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, v in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        nd = OxmlElement(f'w:{m}')
        nd.set(qn('w:w'), str(v))
        nd.set(qn('w:type'), 'dxa')
        tcMar.append(nd)
    tcPr.append(tcMar)

def set_borders(table, color="BBBBBB", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top     w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left    w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom  w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right   w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16); p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.page_break_before = True
    r = p.add_run(text)
    r.bold = True; r.font.name = "Calibri"; r.font.size = Pt(16)
    r.font.color.rgb = C_TITULO

def h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True; r.font.name = "Calibri"; r.font.size = Pt(13)
    r.font.color.rgb = C_S2

def h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True; r.font.name = "Calibri"; r.font.size = Pt(11)
    r.font.color.rgb = C_TITULO

def body(doc, text, sa=5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(sa)
    p.paragraph_format.line_spacing = Pt(16)
    r = p.add_run(text)
    r.font.name = "Calibri"; r.font.size = Pt(10.5); r.font.color.rgb = C_BODY

def code_block(doc, lines_text):
    """Bloque de código estilo consola."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_bg(cell, CODE_HEX)
    set_cell_margins(cell, top=100, bottom=100, left=130, right=130)
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'''<w:tcBorders {nsdecls("w")}>
        <w:left w:val="single" w:sz="18" w:color="1F3864"/>
        <w:top w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>
    </w:tcBorders>'''))
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(15)
    r = p.add_run(lines_text)
    r.font.name = "Courier New"; r.font.size = Pt(9); r.font.color.rgb = C_CODE
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0); sp.paragraph_format.space_after = Pt(5)

def bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Inches(0.35)
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(16)
    r0 = p.add_run("▸  ")
    r0.font.name = "Calibri"; r0.font.size = Pt(10); r0.font.color.rgb = C_S2
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.bold = True; rb.font.name = "Calibri"; rb.font.size = Pt(10.5); rb.font.color.rgb = C_TITULO
    r = p.add_run(text)
    r.font.name = "Calibri"; r.font.size = Pt(10.5); r.font.color.rgb = C_BODY

def make_table(doc, headers, widths, data, center_cols=None):
    if center_cols is None: center_cols = [0]
    table = doc.add_table(rows=len(data)+1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(table)
    for j, h in enumerate(headers):
        c = table.rows[0].cells[j]; c.width = widths[j]
        set_cell_bg(c, HDR_HEX); set_cell_margins(c)
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True; r.font.name = "Calibri"; r.font.size = Pt(9.5); r.font.color.rgb = C_WHITE
    for i, row_data in enumerate(data):
        row = table.rows[i+1]
        for j, val in enumerate(row_data):
            c = row.cells[j]; c.width = widths[j]
            if i % 2 == 1: set_cell_bg(c, ALT_HEX)
            set_cell_margins(c)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in center_cols else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(1)
            r = p.add_run(str(val))
            r.font.name = "Calibri"; r.font.size = Pt(9.5)
            if j == 0: r.bold = True
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0); sp.paragraph_format.space_after = Pt(6)

def add_fig(doc, path, caption, w=5.8):
    if not os.path.exists(path): return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Inches(w))
    pc = doc.add_paragraph()
    pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pc.paragraph_format.space_before = Pt(2); pc.paragraph_format.space_after = Pt(10)
    rc = pc.add_run(caption)
    rc.italic = True; rc.font.name = "Calibri"; rc.font.size = Pt(9); rc.font.color.rgb = C_MUTED

# =============================================================================
def build():
    print("Generando Contexto_Proyecto_TiendaGo.docx ...")
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin    = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin   = Inches(1.1)
        section.right_margin  = Inches(1.1)
        section.page_width    = Inches(8.5)
        section.page_height   = Inches(11.0)
        hdr = section.header
        ph = hdr.paragraphs[0]; ph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        rh = ph.add_run("TiendaGo — Documento de Contexto Completo del Proyecto")
        rh.font.name = "Calibri"; rh.font.size = Pt(8.5); rh.font.color.rgb = C_MUTED
        ftr = section.footer
        pf = ftr.paragraphs[0]; pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rf = pf.add_run("Grupo N° 06 | ESFE - AGAPE | Ciclo C4-26 | Noviembre 2026")
        rf.font.name = "Calibri"; rf.font.size = Pt(8.5); rf.font.color.rgb = C_MUTED

    # =========================================================
    # PORTADA
    # =========================================================
    def cover(text, size=12, bold=False, sa=5, color=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(sa)
        r = p.add_run(text); r.bold = bold
        r.font.name = "Calibri"; r.font.size = Pt(size)
        r.font.color.rgb = color or C_TITULO

    for _ in range(4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)

    if os.path.exists(LOGO):
        pl = doc.add_paragraph(); pl.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pl.paragraph_format.space_before = Pt(6); pl.paragraph_format.space_after = Pt(14)
        pl.add_run().add_picture(LOGO, width=Inches(2.0))

    cover("ESCUELA SUPERIOR FRANCISCANA ESPECIALIZADA - AGAPE", 13, True, 3)
    cover("Carrera: Técnico en Ingeniería de Desarrollo de Software", 11, False, 2)
    cover("Módulo: Implantación de Sistemas de Software | Ciclo C4-26", 10, False, 24)
    cover("─" * 50, 10, False, 24)
    cover("DOCUMENTO DE CONTEXTO COMPLETO DEL PROYECTO", 18, True, 6)
    cover("TiendaGo", 22, True, 6)
    cover("Sistema de Punto de Venta Móvil (POS) y Gestión de Inventario Express", 12, False, 20)
    cover("Versión 2.0  |  Noviembre de 2026", 11, True, 5)
    cover("Docente: Lic. Gerber Alexis Gómez Hidalgo", 11, False, 4)
    cover("Grupo de Trabajo N° 06", 11, False, 4)
    cover("Repositorio: github.com/gerardo-ops/TiendaGo", 10, False, 2, C_S2)

    doc.add_page_break()

    # =========================================================
    # TABLA DE CONTENIDOS
    # =========================================================
    ptoc = doc.add_paragraph()
    ptoc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ptoc.paragraph_format.space_before = Pt(6); ptoc.paragraph_format.space_after = Pt(14)
    rtoc = ptoc.add_run("Tabla de Contenidos")
    rtoc.bold = True; rtoc.font.name = "Calibri"; rtoc.font.size = Pt(16); rtoc.font.color.rgb = C_TITULO

    toc = [
        ("1. Descripción General del Sistema", "3", True),
        ("2. Arquitectura y Tecnologías", "4", True),
        ("    2.1 Stack Tecnológico", "4", False),
        ("    2.2 Diagrama de Despliegue", "4", False),
        ("    2.3 Estructura del Proyecto (.NET 8)", "5", False),
        ("3. Modelo de Datos", "6", True),
        ("    3.1 Entidades Principales", "6", False),
        ("    3.2 Relaciones entre Entidades", "7", False),
        ("4. API REST — Endpoints", "8", True),
        ("    4.1 Autenticación (/api/auth)", "8", False),
        ("    4.2 Productos (/api/productos)", "8", False),
        ("    4.3 Ventas POS (/api/ventas)", "9", False),
        ("    4.4 Turnos de Caja (/api/turnos)", "9", False),
        ("    4.5 Categorías y Dashboard", "10", False),
        ("5. Lógica de Negocio — Servicios", "10", True),
        ("    5.1 VentaService — Proceso ACID", "10", False),
        ("    5.2 DashboardService", "11", False),
        ("6. Seguridad: JWT y RBAC", "12", True),
        ("7. Base de Datos y Configuración", "13", True),
        ("    7.1 Conexión Supabase PostgreSQL", "13", False),
        ("    7.2 Script de Datos Semilla", "13", False),
        ("8. Pruebas Automatizadas", "14", True),
        ("    8.1 Pruebas Unitarias (xUnit)", "14", False),
        ("    8.2 Pruebas de Integración", "15", False),
        ("9. Dependencias y Paquetes NuGet", "16", True),
        ("10. Repositorio y DevOps", "16", True),
    ]

    tt = doc.add_table(rows=len(toc), cols=2)
    tt.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(tt, color="FFFFFF")
    tw = [Inches(5.2), Inches(0.6)]
    for idx, (title, pg, main) in enumerate(toc):
        row = tt.rows[idx]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = tw[0]; c2.width = tw[1]
        set_cell_margins(c1, top=15, bottom=15, left=30, right=30)
        set_cell_margins(c2, top=15, bottom=15, left=30, right=30)
        p1 = c1.paragraphs[0]; p1.paragraph_format.space_before = Pt(0); p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(title); r1.bold = main
        r1.font.name = "Calibri"; r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_TITULO if main else C_BODY
        p2 = c2.paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_before = Pt(0); p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(pg); r2.bold = main
        r2.font.name = "Calibri"; r2.font.size = Pt(10.5); r2.font.color.rgb = C_MUTED

    doc.add_page_break()

    # =========================================================
    # 1. DESCRIPCIÓN GENERAL
    # =========================================================
    h1(doc, "1. Descripción General del Sistema")
    body(doc,
        "TiendaGo es un sistema integral de Punto de Venta Móvil (POS) y Gestión de Inventario Express "
        "concebido para pequeños y medianos establecimientos comerciales. El sistema permite a los cajeros "
        "registrar ventas en tiempo real desde dispositivos móviles Android, descontar inventario de forma "
        "atómica, calcular el IVA (13%) automáticamente, emitir tickets físicos mediante impresoras "
        "térmicas Bluetooth y gestionar turnos de caja con apertura y arqueo de cierre.")
    body(doc,
        "El sistema nació como proyecto académico del Grupo N° 06 en la Escuela Superior Franciscana "
        "Especializada AGAPE (ESFE - AGAPE) para el Módulo de Implantación de Sistemas de Software del "
        "Ciclo C4-26. Está construido 100% sobre tecnologías de código libre, eliminando costos de licencias.")

    make_table(doc,
        ["Atributo", "Valor"],
        [Inches(2.2), Inches(4.3)],
        [
            ("Nombre del Sistema", "TiendaGo — POS Móvil y Gestión de Inventario Express"),
            ("Versión", "2.0"),
            ("Institución", "ESFE - AGAPE (Escuela Superior Franciscana Especializada AGAPE)"),
            ("Módulo", "Implantación de Sistemas de Software — Ciclo C4-26"),
            ("Docente Evaluador", "Lic. Gerber Alexis Gómez Hidalgo"),
            ("Equipo", "Grupo de Trabajo N° 06"),
            ("Repositorio GitHub", "https://github.com/gerardo-ops/TiendaGo.git"),
            ("Plataforma DevOps", "https://dev.azure.com/gerardobatres06/TiendaGo"),
            ("URL API (Supabase)", "https://ywxnbqblfazplkggkcgw.supabase.co"),
            ("Credencial Admin por Defecto", "admin@tiendago.com / Admin123*"),
        ],
        center_cols=[0]
    )

    h2(doc, "Funcionalidades Principales")
    funcs = [
        ("Autenticación y Roles (RBAC)", "Login con JWT Bearer Token. Roles: Administrador (acceso total), Cajero (ventas y turnos), Supervisor (auditoría)."),
        ("Gestión de Productos", "CRUD completo del catálogo. Búsqueda por nombre, SKU o categoría. Escaneo de código de barras desde la cámara del móvil."),
        ("Punto de Venta (POS)", "Registro de ventas multi-producto con cálculo automático de IVA al 13%, vuelto y descuento atómico del inventario."),
        ("Turnos de Caja", "Apertura de turno con monto base, registro de ventas por turno y cierre con arqueo y cuadre automático de diferencias."),
        ("Impresión Térmica", "Emisión de tickets en impresoras Bluetooth 58/80 mm mediante protocolo ESC/POS."),
        ("Dashboard Analítico", "Resumen del día: total de ventas, desglose por método de pago (efectivo/digital) y alertas de bajo inventario."),
        ("Anulación de Ventas", "Reversión de ventas procesadas con reincorporación automática del stock al inventario."),
        ("Gestión de Usuarios", "Alta y administración de cajeros y supervisores con rol asignado y estado activo."),
    ]
    make_table(doc, ["Módulo", "Descripción"], [Inches(2.0), Inches(4.5)], funcs, center_cols=[0])

    # =========================================================
    # 2. ARQUITECTURA
    # =========================================================
    h1(doc, "2. Arquitectura y Tecnologías")

    h2(doc, "2.1 Stack Tecnológico")
    stack = [
        ("Backend (API)", "ASP.NET Core 8.0 — Minimal APIs + Controllers sobre servidor Kestrel", ".NET 8.0"),
        ("Base de Datos", "PostgreSQL 15 sobre Supabase Cloud (AWS US-West-2) con PgBouncer", "Npgsql EF Core 8.0.11"),
        ("ORM", "Entity Framework Core 8 con migraciones automáticas y consultas LINQ", "EF Core 8.0.14"),
        ("Autenticación", "JWT Bearer (System.IdentityModel.Tokens.Jwt) + BCrypt.Net para hashing", "v8.6.1 / v4.0.3"),
        ("Mapeo de Objetos", "AutoMapper con perfiles separados: CatalogoMappingProfile, VentasMappingProfile", "AutoMapper 16.2.0"),
        ("Cliente Supabase", "SDK oficial de Supabase para .NET para operaciones en tiempo real y auth", "Supabase 1.1.1"),
        ("Documentación API", "Swagger/OpenAPI con seguridad Bearer JWT integrada en Swashbuckle", "Swashbuckle 6.6.2"),
        ("App Móvil (cliente)", "Android nativo en Kotlin con Jetpack Compose (UI declarativa)", "Android 8.0+ (API 26+)"),
        ("Impresión", "Protocolo ESC/POS sobre Bluetooth 5.0 SPP para impresoras térmicas", "58 mm / 80 mm"),
        ("CI/CD", "Azure Pipelines + GitHub Actions para build, test y despliegue continuo", "Azure DevOps"),
    ]
    make_table(doc, ["Capa / Componente", "Tecnología Utilizada", "Versión / Detalle"],
               [Inches(1.7), Inches(3.1), Inches(1.7)], stack, center_cols=[0, 2])

    h2(doc, "2.2 Diagrama de Despliegue")
    body(doc,
        "El sistema TiendaGo opera bajo una arquitectura desacoplada en tres nodos físicos principales: "
        "terminales POS móviles Android (cajeros), servidor de aplicaciones que hospeda el Web API ASP.NET "
        "Core 8 con Kestrel, y la base de datos PostgreSQL 15 gestionada en Supabase Cloud (AWS US-West-2). "
        "La comunicación entre nodos se realiza exclusivamente por HTTPS con tokens JWT.")
    add_fig(doc, DIAGRAMA,
        "Diagrama de Despliegue UML — Distribución física del ecosistema TiendaGo v2.0.", 5.6)

    h2(doc, "2.3 Estructura del Proyecto (.NET 8)")
    body(doc,
        "La solución TiendaGo.sln está organizada en tres proyectos con separación clara de responsabilidades:")
    bullet(doc, "API RESTful principal con Minimal APIs. Contiene Endpoints, Services, Models, DTOs, Mappings y la configuración del IoC Container (Program.cs).", "TiendaGo (Proyecto Principal):  ")
    bullet(doc, "Suite de pruebas unitarias con xUnit, Moq y FluentAssertions. Cubre VentaService, AuthService y ProductoMapping de forma aislada.", "TiendaGo.UnitTests:  ")
    bullet(doc, "Suite de pruebas end-to-end sobre el pipeline HTTP con Microsoft.AspNetCore.Mvc.Testing. Cubre autenticación JWT, control RBAC y flujos completos de venta.", "TiendaGo.IntegrationTests:  ")

    if os.path.exists(ARCH_IMG):
        add_fig(doc, ARCH_IMG, "Arquitectura de la Solución TiendaGo — Estructura modular en Visual Studio 2022.", 5.6)

    # =========================================================
    # 3. MODELO DE DATOS
    # =========================================================
    h1(doc, "3. Modelo de Datos")

    h2(doc, "3.1 Entidades Principales")
    body(doc,
        "El esquema relacional de TiendaGo está en Tercera Forma Normal (3FN) y se hospeda en PostgreSQL 15 "
        "sobre Supabase. Las entidades del dominio de negocio son:")

    entidades = [
        ("roles", "id_rol (PK), nombre_rol, descripcion",
         "Define los perfiles de acceso: 1=Administrador, 2=Cajero, 3=Supervisor."),
        ("usuarios", "id_usuario (UUID PK), id_rol (FK), nombre_completo, correo_electronico, clave_hash, estado_activo, fecha_registro",
         "Usuarios del sistema. La clave se almacena con hash BCrypt. UUID compatible con Supabase Auth."),
        ("categorias", "id_categoria (PK), nombre_categoria, descripcion, estado_activo",
         "Agrupaciones del catálogo de productos."),
        ("metodos_pago", "id_metodo_pago (PK), nombre_metodo, estado_activo",
         "Métodos de cobro aceptados (Efectivo, Tarjeta, etc.)."),
        ("productos", "id_producto (PK), id_categoria (FK), nombre_producto, codigo_sku, costo_compra, precio_venta, stock_actual, stock_minimo, url_imagen, estado_activo, fecha_creacion",
         "Catálogo completo. stock_minimo dispara alertas de bajo inventario en el Dashboard."),
        ("turnos_caja", "id_turno (PK), id_usuario (FK), fecha_apertura, fecha_cierre, monto_base_inicial, total_ventas_efectivo, total_ventas_digital, monto_declarado, diferencia_cuadre, estado_turno",
         "Gestión de jornada del cajero: Abierto / Cerrado. Registra el arqueo de cierre."),
        ("ventas", "id_venta (PK), id_turno (FK), id_usuario (FK), id_metodo_pago (FK), numero_ticket, fecha_hora, subtotal, total_iva, total_venta, monto_recibido, cambio_entregado, estado_venta",
         "Cabecera de cada transacción. estado_venta: Completada / Anulada. numero_ticket auto-generado (TCK-XXXXXXXX)."),
        ("detalles_venta", "id_detalle (PK), id_venta (FK), id_producto (FK), cantidad, precio_unitario_historico, subtotal_linea",
         "Líneas de cada venta. Preserva el precio histórico del producto al momento de la venta."),
    ]
    make_table(doc, ["Tabla", "Columnas Clave", "Propósito"],
               [Inches(1.4), Inches(2.8), Inches(2.3)], entidades, center_cols=[0])

    h2(doc, "3.2 Relaciones entre Entidades")
    code_block(doc,
        "roles          1 ──< N  usuarios\n"
        "usuarios       1 ──< N  turnos_caja\n"
        "usuarios       1 ──< N  ventas\n"
        "turnos_caja    1 ──< N  ventas\n"
        "metodos_pago   1 ──< N  ventas\n"
        "ventas         1 ──< N  detalles_venta\n"
        "productos      1 ──< N  detalles_venta\n"
        "categorias     1 ──< N  productos"
    )

    # =========================================================
    # 4. API REST - ENDPOINTS
    # =========================================================
    h1(doc, "4. API REST — Endpoints")
    body(doc,
        "La API está documentada con Swagger/OpenAPI y accesible en /swagger. Todos los endpoints "
        "requieren autenticación Bearer JWT excepto los marcados como anónimos. La base URL es la "
        "dirección del servidor de despliegue. La URL de desarrollo fue: http://localhost:5000")

    h2(doc, "4.1 Autenticación — /api/auth")
    auth_eps = [
        ("POST", "/api/auth/login", "No", "Inicia sesión. Retorna Bearer JWT con Claims de rol. Campos: correo_electronico, password."),
        ("POST", "/api/auth/seed-admin", "No", "Crea el usuario administrador por defecto si no existe. Solo para inicialización."),
        ("GET",  "/api/ping", "No", "Health check de conectividad. Retorna estado: Conectado y fecha/hora UTC."),
    ]
    make_table(doc, ["Método", "Ruta", "Auth", "Descripción"],
               [Inches(0.7), Inches(1.9), Inches(0.6), Inches(3.3)], auth_eps, center_cols=[0, 2])

    h2(doc, "4.2 Productos — /api/productos")
    prod_eps = [
        ("GET",    "/api/productos",              "JWT", "Lista todos los productos con soporte para ?buscar= y ?categoria="),
        ("GET",    "/api/productos/activos",       "JWT", "Lista solo productos activos (disponibles en la terminal POS)."),
        ("GET",    "/api/productos/{id}",          "JWT", "Ficha completa de un producto por ID."),
        ("GET",    "/api/productos/buscar/{sku}",  "JWT", "Busca producto por código SKU/barras (resultado del escaneo de cámara)."),
        ("POST",   "/api/productos",              "JWT", "Crea un nuevo producto en el catálogo."),
        ("PUT",    "/api/productos/{id}",          "JWT", "Actualiza datos de un producto existente."),
        ("DELETE", "/api/productos/{id}",          "JWT", "Desactiva un producto (soft delete — no elimina físicamente)."),
        ("POST",   "/api/productos/{id}/imagen",  "JWT", "Sube imagen del producto al bucket S3 de Supabase Storage."),
    ]
    make_table(doc, ["Método", "Ruta", "Auth", "Descripción"],
               [Inches(0.7), Inches(2.2), Inches(0.6), Inches(3.0)], prod_eps, center_cols=[0, 2])

    h2(doc, "4.3 Ventas POS — /api/ventas")
    venta_eps = [
        ("POST", "/api/ventas",                   "JWT", "Registra una venta completa de forma ACID (cabecera + detalles + descuento de stock)."),
        ("GET",  "/api/ventas/{id}",               "JWT", "Consulta detalles de un ticket de venta por ID."),
        ("GET",  "/api/ventas/turno/{idTurno}",    "JWT", "Lista todas las ventas de un turno de caja específico."),
        ("GET",  "/api/ventas/historial",          "JWT", "Historial de ventas con filtro ?filtroFecha= (hoy / semana / mes)."),
        ("GET",  "/api/ventas",                    "JWT", "Lista general de todas las ventas registradas."),
        ("POST", "/api/ventas/{id}/anular",        "JWT", "Anula una venta y devuelve las unidades al inventario."),
    ]
    make_table(doc, ["Método", "Ruta", "Auth", "Descripción"],
               [Inches(0.7), Inches(2.4), Inches(0.6), Inches(2.8)], venta_eps, center_cols=[0, 2])

    h2(doc, "4.4 Turnos de Caja — /api/turnos")
    turno_eps = [
        ("POST", "/api/turnos/abrir",              "JWT", "Abre un turno de caja con monto_base_inicial para el cajero especificado."),
        ("POST", "/api/turnos/{id}/cerrar",        "JWT", "Cierra el turno y registra el monto físico declarado para calcular el cuadre."),
        ("GET",  "/api/turnos/activo/{idUsuario}", "JWT", "Consulta el turno abierto actualmente para el usuario (GUID)."),
        ("GET",  "/api/turnos/{id}",               "JWT", "Detalle de un turno por ID."),
        ("GET",  "/api/turnos",                    "JWT", "Historial completo de turnos de caja."),
    ]
    make_table(doc, ["Método", "Ruta", "Auth", "Descripción"],
               [Inches(0.7), Inches(2.4), Inches(0.6), Inches(2.8)], turno_eps, center_cols=[0, 2])

    h2(doc, "4.5 Categorías y Dashboard")
    other_eps = [
        ("GET",    "/api/categorias",        "JWT", "Lista de todas las categorías activas del catálogo."),
        ("POST",   "/api/categorias",        "JWT", "Crea una nueva categoría."),
        ("PUT",    "/api/categorias/{id}",   "JWT", "Actualiza una categoría."),
        ("DELETE", "/api/categorias/{id}",   "JWT", "Elimina una categoría."),
        ("GET",    "/api/dashboard/resumen", "JWT", "Métricas del día: total ventas, efectivo, digital y productos con bajo stock."),
    ]
    make_table(doc, ["Método", "Ruta", "Auth", "Descripción"],
               [Inches(0.7), Inches(2.0), Inches(0.6), Inches(3.2)], other_eps, center_cols=[0, 2])

    # =========================================================
    # 5. LÓGICA DE NEGOCIO
    # =========================================================
    h1(doc, "5. Lógica de Negocio — Servicios")

    h2(doc, "5.1 VentaService — Proceso ACID")
    body(doc,
        "El método RegistrarVentaAsync implementa una transacción ACID completa en la base de datos. "
        "El flujo ejecuta las siguientes validaciones y operaciones en secuencia:")
    bullet(doc, "Verifica que el turno de caja referenciado exista y esté en estado 'Abierto'. Si no, lanza InvalidOperationException.", "Paso 1 — Validar Turno Activo:  ")
    bullet(doc, "Por cada producto en la lista de detalles: verifica que exista, esté activo y tenga StockActual >= Cantidad solicitada.", "Paso 2 — Validar Existencias:  ")
    bullet(doc, "Calcula totalVenta = Σ(precio × cantidad). Verifica MontoRecibido >= totalVenta.", "Paso 3 — Calcular Importes:  ")
    bullet(doc, "totalIva = Round(totalVenta − (totalVenta / 1.13), 2). subtotalSinIva = totalVenta − totalIva. CambioEntregado = MontoRecibido − totalVenta.", "Paso 4 — IVA 13% y Vuelto:  ")
    bullet(doc, "Genera número de ticket: 'TCK-' + últimos 8 dígitos de DateTimeOffset.UtcNow.Ticks.", "Paso 5 — Generar Ticket:  ")
    bullet(doc, "Inserta la entidad Ventas (cabecera) en la BD con EF Core.", "Paso 6 — Registrar Encabezado:  ")
    bullet(doc, "Por cada línea: inserta DetallesVenta y descuenta StockActual -= Cantidad al producto.", "Paso 7 — Registrar Detalles y Descontar Stock:  ")
    bullet(doc, "SaveChangesAsync() confirma todo en una sola transacción. Si falla, EF Core hace rollback automático.", "Paso 8 — Confirmar Transacción:  ")

    code_block(doc,
        "// Fórmula de IVA (13% incluido en precio)\n"
        "var totalVenta      = Σ(precioUnitario × cantidad);\n"
        "var totalIva        = Round(totalVenta - (totalVenta / 1.13m), 2);\n"
        "var subtotalSinIva  = totalVenta - totalIva;\n"
        "var cambioEntregado = montoRecibido - totalVenta;\n"
        "var numeroTicket    = $\"TCK-{DateTime.UtcNow.Ticks.ToString()[^8..]}\";"
    )

    h2(doc, "5.2 DashboardService")
    body(doc,
        "El DashboardService consulta el resumen del día de negocio usando la zona horaria local "
        "(TimeZoneHelper.GetBusinessToday). Proporciona:")
    bullet(doc, "Total de ventas del día y cantidad de transacciones (solo estado='Completada').")
    bullet(doc, "Desglose por método de pago: ventas en Efectivo vs ventas Digitales.")
    bullet(doc, "Lista de productos cuyo StockActual <= StockMinimo (alertas de reorden).")
    bullet(doc, "Producto más vendido del día con cantidad total despachada.")

    # =========================================================
    # 6. SEGURIDAD
    # =========================================================
    h1(doc, "6. Seguridad: JWT y RBAC")
    body(doc,
        "TiendaGo implementa autenticación stateless mediante JSON Web Tokens (JWT) y control de "
        "acceso basado en roles (RBAC). La configuración de seguridad se centraliza en Program.cs.")

    h2(doc, "Configuración JWT (appsettings.json)")
    code_block(doc,
        "\"Jwt\": {\n"
        "  \"Key\":      \"TuClaveSuperSecretaDeAlMenos32Caracteres!\",\n"
        "  \"Issuer\":   \"TiendaGoAPI\",\n"
        "  \"Audience\": \"TiendaGoApp\",\n"
        "  \"ExpirationHours\": 8\n"
        "}"
    )

    sec_data = [
        ("Algoritmo de Firma", "HMAC-SHA256 (SymmetricSecurityKey con clave de 32+ caracteres)"),
        ("Vigencia del Token", "8 horas (configurable en appsettings.json)"),
        ("Claims incluidos", "id_usuario (UUID), correo_electronico, nombre_completo, rol (nombre del rol)"),
        ("Hash de Contraseñas", "BCrypt.Net-Next (factor de costo 11 por defecto)"),
        ("Validaciones activas", "ValidateIssuer, ValidateAudience, ValidateLifetime, ValidateIssuerSigningKey"),
        ("ClockSkew", "TimeSpan.Zero (expiración exacta sin tolerancia adicional)"),
        ("CORS", "AllowAll en desarrollo (AllowAnyOrigin, AllowAnyHeader, AllowAnyMethod)"),
        ("Endpoints públicos", "/api/auth/login, /api/auth/seed-admin, /api/ping"),
        ("Endpoints protegidos", "Todos los demás: RequireAuthorization()"),
    ]
    make_table(doc, ["Parámetro de Seguridad", "Valor / Configuración"],
               [Inches(2.2), Inches(4.3)], sec_data, center_cols=[0])

    h2(doc, "Roles del Sistema")
    roles_data = [
        ("1", "Administrador", "Control total: gestión de usuarios, catálogo, categorías, reportes y configuración del sistema."),
        ("2", "Cajero", "Operación del terminal POS: registrar ventas, abrir y cerrar turno de caja."),
        ("3", "Supervisor", "Auditoría: consulta del historial de ventas, métricas de rendimiento y cuadres de caja."),
    ]
    make_table(doc, ["ID", "Nombre del Rol", "Permisos y Alcance"],
               [Inches(0.5), Inches(1.5), Inches(4.5)], roles_data, center_cols=[0])

    # =========================================================
    # 7. BASE DE DATOS Y CONFIGURACIÓN
    # =========================================================
    h1(doc, "7. Base de Datos y Configuración")

    h2(doc, "7.1 Conexión Supabase PostgreSQL")
    body(doc, "La cadena de conexión usa PgBouncer en el puerto 6543 para connection pooling:")
    code_block(doc,
        "Host=aws-0-us-west-2.pooler.supabase.com;\n"
        "Port=6543;\n"
        "Database=postgres;\n"
        "Username=postgres.ywxnbqblfazplkggkcgw;\n"
        "Password=TiendaGo123;\n"
        "SSL Mode=Require;\n"
        "Trust Server Certificate=true;\n"
        "No Reset On Close=true;"
    )
    body(doc,
        "El cliente Supabase SDK (.NET) se configura con la URL y la AnonKey del proyecto para "
        "operaciones en tiempo real, autenticación y Storage (imágenes de productos):")
    code_block(doc,
        "URL:      https://ywxnbqblfazplkggkcgw.supabase.co\n"
        "AnonKey:  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...[ver appsettings.json]\n"
        "Opciones: AutoRefreshToken=true, AutoConnectRealtime=true"
    )

    h2(doc, "7.2 Script de Datos Semilla (SeedAdmin.sql)")
    body(doc,
        "El archivo Scripts/SeedAdmin.sql inicializa la base de datos con los roles base y el usuario "
        "administrador por defecto. Se ejecuta directamente en el SQL Editor de Supabase:")
    bullet(doc, "Crea los roles: Administrador (id=1), Cajero (id=2) y Supervisor (id=3) con ON CONFLICT DO NOTHING.")
    bullet(doc, "Genera hash BCrypt de la contraseña 'Admin123*' usando pgcrypto (crypt + gen_salt('bf', 6)).")
    bullet(doc, "Inserta en auth.users (UUID: 37907a7d-4609-422f-b02b-6799bb01c8f2) para Supabase Auth.")
    bullet(doc, "Inserta en public.usuarios con ON CONFLICT (correo_electronico) DO UPDATE para idempotencia.")

    code_block(doc,
        "-- Credenciales del Administrador por Defecto\n"
        "ID Usuario: 37907a7d-4609-422f-b02b-6799bb01c8f2\n"
        "Email:      admin@tiendago.com\n"
        "Password:   Admin123*\n"
        "Rol:        Administrador (id_rol = 1)"
    )

    # =========================================================
    # 8. PRUEBAS AUTOMATIZADAS
    # =========================================================
    h1(doc, "8. Pruebas Automatizadas")
    body(doc,
        "El sistema cuenta con dos suites de pruebas automatizadas gestionadas en Azure DevOps y "
        "ejecutadas con el test runner de xUnit en el pipeline de CI.")

    h2(doc, "8.1 Pruebas Unitarias — TiendaGo.UnitTests")
    body(doc,
        "Proyecto de pruebas con xUnit, Moq y FluentAssertions. Aísla la capa de servicios "
        "utilizando InMemory Database y mocks. Archivos de prueba:")

    unit_tests = [
        ("VentaServiceTests.cs", "7 casos",
         "Cálculo exacto de IVA 13%, descuento atómico de stock, prevención de venta sin existencias, "
         "cálculo correcto de vuelto, rechazo de turno cerrado, anulación de venta con reincorporación de stock."),
        ("AuthServiceTests.cs", "Varios",
         "Verificación de hash BCrypt, login con credenciales correctas e incorrectas, generación de Claims JWT."),
        ("ProductoMappingTests.cs", "Varios",
         "Validación de los perfiles AutoMapper: Producto → ProductoResponse, ProductoRequest → Producto."),
    ]
    make_table(doc, ["Archivo", "Cobertura", "Casos de Prueba"],
               [Inches(1.9), Inches(0.8), Inches(3.8)], unit_tests, center_cols=[0, 1])

    h2(doc, "8.2 Pruebas de Integración — TiendaGo.IntegrationTests")
    body(doc,
        "Suite end-to-end sobre el pipeline HTTP real usando Microsoft.AspNetCore.Mvc.Testing con "
        "un TestServer en memoria. Usa CustomWebApplicationFactory para configurar el IoC y JWT de prueba.")

    int_tests = [
        ("AuthEndpointsTests.cs",
         "Login con credenciales válidas → HTTP 200 + JWT. Login con password incorrecta → HTTP 401. "
         "Acceso a endpoint protegido sin token → HTTP 401."),
        ("SeguridadRBACTests.cs",
         "Acceso a rutas de administrador con rol Cajero → HTTP 403 Forbidden. "
         "Verificación de que la clave JWT de prueba genera Claims correctos con el rol esperado."),
        ("VentasEndpointsTests.cs",
         "Flujo completo: apertura de turno → registro de venta → verificación de descuento de stock. "
         "Venta con stock insuficiente → HTTP 409 Conflict. Consulta de historial por turno."),
    ]
    make_table(doc, ["Archivo de Test", "Escenarios Cubiertos"],
               [Inches(2.1), Inches(4.4)], int_tests, center_cols=[0])

    # =========================================================
    # 9. DEPENDENCIAS Y PAQUETES
    # =========================================================
    h1(doc, "9. Dependencias y Paquetes NuGet")
    pkgs = [
        ("AutoMapper", "16.2.0", "Mapeo automático entre entidades de dominio y DTOs de transferencia."),
        ("BCrypt.Net-Next", "4.0.3", "Hash y verificación de contraseñas con el algoritmo BCrypt."),
        ("Microsoft.AspNetCore.Authentication.JwtBearer", "8.0.14", "Middleware de autenticación JWT Bearer para ASP.NET Core."),
        ("Microsoft.AspNetCore.OpenApi", "8.0.14", "Soporte nativo de OpenAPI para ASP.NET Core 8."),
        ("Microsoft.EntityFrameworkCore.Design", "8.0.14", "Herramientas de diseño de EF Core (migraciones y scaffolding)."),
        ("Microsoft.EntityFrameworkCore.Tools", "8.0.14", "CLI de EF Core (dotnet ef migrations add/update)."),
        ("Npgsql.EntityFrameworkCore.PostgreSQL", "8.0.11", "Provider de PostgreSQL para Entity Framework Core."),
        ("Supabase", "1.1.1", "SDK oficial de Supabase para .NET (Auth, Realtime, Storage, Postgrest)."),
        ("Swashbuckle.AspNetCore", "6.6.2", "Generación automática de UI Swagger y especificación OpenAPI."),
        ("System.IdentityModel.Tokens.Jwt", "8.6.1", "Creación, firma y validación de tokens JWT."),
    ]
    make_table(doc, ["Paquete NuGet", "Versión", "Función"],
               [Inches(3.0), Inches(0.9), Inches(2.6)], pkgs, center_cols=[0, 1])

    # =========================================================
    # 10. REPOSITORIO Y DEVOPS
    # =========================================================
    h1(doc, "10. Repositorio y DevOps")
    body(doc,
        "El ciclo de vida del software de TiendaGo está gestionado de forma integral en Azure DevOps "
        "y el código fuente se hospeda en GitHub.")

    make_table(doc,
        ["Recurso", "URL / Detalle"],
        [Inches(2.0), Inches(4.5)],
        [
            ("Repositorio GitHub",   "https://github.com/gerardo-ops/TiendaGo.git"),
            ("Organización DevOps",  "https://dev.azure.com/gerardobatres06/TiendaGo"),
            ("Rama principal",       "main (código de producción, protegida)"),
            ("Pipeline CI",          "Azure Pipelines: build dotnet + xUnit test runner automático en cada push"),
            ("Test Plans",           "Azure Test Plans: suites organizadas TS01 (Funcional), TS02 (API), TS03 (Seguridad RBAC)"),
            ("Work Items",           "Azure Boards: Product Backlog, historias de usuario y bugs trazados"),
            ("Supabase Project",     "https://ywxnbqblfazplkggkcgw.supabase.co (Región: AWS US-West-2)"),
            ("Swagger UI (dev)",     "http://localhost:5000/swagger (en entorno de desarrollo local)"),
        ],
        center_cols=[0]
    )

    h2(doc, "Comandos de Desarrollo Frecuentes")
    code_block(doc,
        "# Restaurar dependencias NuGet\n"
        "dotnet restore\n\n"
        "# Compilar la solución completa\n"
        "dotnet build\n\n"
        "# Ejecutar el API en modo desarrollo (puerto 5000)\n"
        "dotnet run --project TiendaGo\n\n"
        "# Ejecutar TODAS las pruebas (unitarias + integración)\n"
        "dotnet test\n\n"
        "# Ejecutar solo las pruebas unitarias\n"
        "dotnet test TiendaGo.UnitTests\n\n"
        "# Ejecutar solo las pruebas de integración\n"
        "dotnet test TiendaGo.IntegrationTests\n\n"
        "# Crear una nueva migración de base de datos\n"
        "dotnet ef migrations add NombreDeMigracion --project TiendaGo\n\n"
        "# Aplicar migraciones pendientes a la BD\n"
        "dotnet ef database update --project TiendaGo\n\n"
        "# Publicar el binario de producción (carpeta /publish)\n"
        "dotnet publish -c Release -o ./publish"
    )

    # =========================================================
    doc.save(OUTPUT)
    print(f"Documento generado exitosamente: {OUTPUT}")

if __name__ == "__main__":
    build()

