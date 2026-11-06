import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Establece el color de fondo hexadecimal de una celda."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="B0C4DE", sz="4", val="single"):
    """Aplica bordes limpios a la tabla."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def set_cell_margins(cell, top=60, bottom=60, left=90, right=90):
    """Ajusta el espaciado interno (padding) de una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()

    # Margen estándar: 1 pulgada (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Estilos base
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(10)
    normal_font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.space_before = Pt(0)

    COLOR_TITLE = RGBColor(0x1F, 0x4E, 0x79)
    COLOR_BLACK = RGBColor(0x00, 0x00, 0x00)
    COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, bold=False, italic=False, font_size=10, color=COLOR_BLACK):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if text:
            r = p.add_run(text)
            r.bold = bold
            r.italic = italic
            r.font.name = "Calibri"
            r.font.size = Pt(font_size)
            r.font.color.rgb = color
        return p

    def add_bullet_point(title_lead, body_text, space_before=2, space_after=3):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15

        r_bullet = p.add_run("● ")
        r_bullet.font.name = "Arial"
        r_bullet.font.size = Pt(8.5)
        r_bullet.font.color.rgb = COLOR_BLACK

        r_lead = p.add_run(title_lead)
        r_lead.bold = True
        r_lead.font.name = "Calibri"
        r_lead.font.size = Pt(9.5)
        r_lead.font.color.rgb = COLOR_BLACK

        r_body = p.add_run(body_text)
        r_body.font.name = "Calibri"
        r_body.font.size = Pt(9.5)
        r_body.font.color.rgb = COLOR_BLACK
        return p

    def add_metric_table(metric_header, metric_rows):
        table = doc.add_table(rows=len(metric_rows) + 1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table, color="1F4E79", sz="4")

        col_w = [Inches(3.2), Inches(3.3)]

        # Header
        hdr_row = table.rows[0]
        c1, c2 = hdr_row.cells[0], hdr_row.cells[1]
        c1.width, c2.width = col_w[0], col_w[1]
        set_cell_background(c1, "1F4E79")
        set_cell_background(c2, "1F4E79")
        set_cell_margins(c1, top=50, bottom=50, left=80, right=80)
        set_cell_margins(c2, top=50, bottom=50, left=80, right=80)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(metric_header)
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run("Valor Registrado")
        r2.bold = True
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Data rows
        for idx, (m_name, m_val) in enumerate(metric_rows, 1):
            row = table.rows[idx]
            cell_a, cell_b = row.cells[0], row.cells[1]
            cell_a.width, cell_b.width = col_w[0], col_w[1]
            bg = "FFFFFF" if idx % 2 != 0 else "F2F5F9"
            set_cell_background(cell_a, bg)
            set_cell_background(cell_b, bg)
            set_cell_margins(cell_a, top=40, bottom=40, left=80, right=80)
            set_cell_margins(cell_b, top=40, bottom=40, left=80, right=80)

            pa = cell_a.paragraphs[0]
            pa.paragraph_format.space_before = Pt(0)
            pa.paragraph_format.space_after = Pt(0)
            ra = pa.add_run(m_name)
            ra.font.name = "Calibri"
            ra.font.size = Pt(9)
            ra.font.color.rgb = COLOR_BLACK

            pb = cell_b.paragraphs[0]
            pb.paragraph_format.space_before = Pt(0)
            pb.paragraph_format.space_after = Pt(0)
            rb = pb.add_run(m_val)
            rb.font.name = "Calibri"
            rb.font.size = Pt(9)
            if "100%" in m_val or "superados" in m_val or "exitosas" in m_val:
                rb.bold = True
            rb.font.color.rgb = COLOR_BLACK

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(2)

    def add_image_box(image_path, width_inches=6.3):
        if os.path.exists(image_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run()
            r.add_picture(image_path, width=Inches(width_inches))

    # =========================================================================
    # PÁGINA 1: PORTADA
    # =========================================================================
    add_p("ESCUELA SUPERIOR FRANCISCANA ESPECIALIZADA / AGAPE", 
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=18, bold=True, font_size=11)

    logo_path = os.path.abspath("Screenshots_DevOps/portada_logos.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(0)
        p_logo.paragraph_format.space_after = Pt(24)
        p_logo.add_run().add_picture(logo_path, width=Inches(2.1))

    add_p("CARRERA", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=1, bold=True, font_size=11)
    add_p("TÉCNICO EN INGENIERÍA DE DESARROLLO DE SOFTWARE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18, font_size=9.5, color=COLOR_MUTED)

    add_p("MÓDULO", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=1, bold=True, font_size=11)
    add_p("TESTEO DE SOFTWARE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18, font_size=9.5, color=COLOR_MUTED)

    add_p("TÍTULO", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=1, bold=True, font_size=11)
    add_p("Reporte de Ejecución de Pruebas.", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=20, font_size=9.5, color=COLOR_MUTED)

    add_p("ESTUDIANTE(S)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2, bold=True, font_size=11)
    add_p("GERARDO ANTONIO BATRES MORENO 100%", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=1, font_size=9.5, color=COLOR_MUTED)
    add_p("ELMER ANTONIO TESORERO HERNÁNDEZ 100%", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=1, font_size=9.5, color=COLOR_MUTED)
    add_p("JASON VLADIMIR BAUTISTA MARAVILLA 100%", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=1, font_size=9.5, color=COLOR_MUTED)
    add_p("BAYRON ANTONIO DÍAZ CAMPOS 100%", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=20, font_size=9.5, color=COLOR_MUTED)

    add_p("FECHA DE PRESENTACIÓN", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=1, bold=True, font_size=11)
    add_p("28/10/26", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18, font_size=9.5, color=COLOR_MUTED)

    add_p("DOCENTE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=1, bold=True, font_size=11)
    add_p("GERBER ALEXIS GÓMEZ", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18, font_size=9.5, color=COLOR_MUTED)

    add_p("CICLO", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=1, bold=True, font_size=11)
    add_p("C4-26", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0, font_size=9.5, color=COLOR_MUTED)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 2: ÍNDICE
    # =========================================================================
    add_p("INDICE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=20, bold=True, font_size=12)

    toc_entries = [
        ("INTRODUCCIÓN", "3", 0, True),
        ("PRUEBAS APLICADAS", "4", 0, True),
        ("Pruebas Unitarias", "4", 1, False),
        ("Pruebas de API", "4", 1, False),
        ("Pruebas de Aceptación", "5", 1, False),
        ("RESULTADOS OBTENIDOS", "5", 0, True),
        ("Pruebas de Aceptación", "5", 1, False),
        ("Pruebas de API", "6", 1, False),
        ("Pruebas Unitarias", "7", 1, False),
        ("CONCLUSIONES", "8", 0, True),
        ("RECOMENDACIONES", "8", 0, True)
    ]

    for title, page, level, is_bold in toc_entries:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(2)
        p_toc.paragraph_format.space_after = Pt(3)
        p_toc.paragraph_format.line_spacing = 1.15
        
        # Tab stop at 6.5 inches with dot leader
        tab_stops = p_toc.paragraph_format.tab_stops
        tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

        indent = "    " if level == 1 else ""
        r_title = p_toc.add_run(indent + title)
        r_title.bold = is_bold
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(9.5 if level == 1 else 10)
        r_title.font.color.rgb = COLOR_BLACK

        r_tab = p_toc.add_run("\t")
        r_page = p_toc.add_run(page)
        r_page.bold = is_bold
        r_page.font.name = "Calibri"
        r_page.font.size = Pt(9.5 if level == 1 else 10)
        r_page.font.color.rgb = COLOR_BLACK

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 3: INTRODUCCIÓN
    # =========================================================================
    add_p("INTRODUCCIÓN", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=18, bold=True, font_size=12)

    intro_p1 = (
        "El presente informe formaliza y documenta los resultados del Ciclo 1 de Pruebas de "
        "Software realizado sobre el sistema \"TiendaGo\", una plataforma moderna orientada al "
        "punto de venta (POS) móvil y a la gestión ágil de inventario express para comercios "
        "minoristas y tiendas de conveniencia. La solución comprende una arquitectura desacoplada "
        "compuesta por un backend RESTful de alta disponibilidad desarrollado sobre .NET 8 (C#) con "
        "Entity Framework Core y PostgreSQL en Supabase Cloud, articulado con una aplicación "
        "móvil nativa desarrollada en Android con Jetpack Compose orientada a la operativa táctil "
        "de cajeros y administradores de tienda."
    )
    add_p(intro_p1, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=8, font_size=10)

    intro_p2 = (
        "El aseguramiento de la calidad (QA) del sistema se orientó a la verificación exhaustiva de "
        "los Product Backlog Items (PBI #2010 al #2035) definidos bajo la metodología ágil Scrum e "
        "implementados en Azure DevOps en la organización \"gerardobatres06\" dentro del proyecto "
        "\"TiendaGo\". El alcance del presente ciclo abarcó la validación rigurosa de las reglas de negocio "
        "de autenticación administrativa y de operadores mediante Bearer Tokens JWT, control estricto "
        "de acceso basado en roles (RBAC: Administrador y Cajero), transacciones de cobro en terminal "
        "POS con cálculo exacto de impuestos (IVA 13%) y vuelto en efectivo, blindaje transaccional "
        "ACID contra anomalías de sobreventa o inventario insuficiente, gobernanza de turnos de caja "
        "con arqueo ciego, y catálogo de productos con búsqueda dinámica y lectura óptica de códigos "
        "de barras (SKU)."
    )
    add_p(intro_p2, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=8, font_size=10)

    intro_p3 = (
        "Para garantizar un proceso formal y reproducible, el equipo aplicó el estándar internacional "
        "ISO/IEC/IEEE 29119 para la especificación y documentación de pruebas, implementando "
        "una pirámide de testing balanceada que articula pruebas unitarias de servicios, pruebas de "
        "integración sobre endpoints de Web API y pruebas funcionales de aceptación basadas en el "
        "comportamiento (BDD) estructuradas en sintaxis Gherkin y matrices de trazabilidad. Este "
        "informe expone de forma clara la tipología de pruebas aplicadas, el consolidado de resultados "
        "métricos obtenidos en Azure DevOps y las conclusiones técnicas derivadas del ciclo."
    )
    add_p(intro_p3, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=8, font_size=10)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 4: PRUEBAS APLICADAS
    # =========================================================================
    add_p("PRUEBAS APLICADAS", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=8, bold=True, font_size=11.5)

    add_p(
        "Conforme a las directrices de aseguramiento de calidad y la rúbrica de evaluación, se "
        "aplicaron tres categorías fundamentales de pruebas de software, cubriendo desde la lógica "
        "atómica de los servicios hasta la validación de la experiencia del usuario final.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=8, font_size=10
    )

    add_p("Pruebas Unitarias", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4, bold=True, font_size=10.5)

    add_p(
        "Las pruebas unitarias tuvieron como objetivo aislar y examinar el comportamiento lógico de "
        "los métodos que componen la capa de servicios de aplicación (Application Layer) de "
        "TiendaGo, verificando la adecuada respuesta ante datos válidos y el lanzamiento preciso de "
        "excepciones de dominio ante transgresiones de las reglas de negocio.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, font_size=10
    )

    add_bullet_point(
        "Entorno y Tecnologías: ",
        "Implementadas en C# bajo .NET 8 utilizando el framework xUnit 2.5, la biblioteca de "
        "dobles de prueba Moq 4.20 para la simulación de repositorios y Entity Framework Core In-Memory / "
        "SQLite para la persistencia transitoria y aislamiento de pruebas."
    )

    add_bullet_point(
        "Servicio VentaService (Casos 2001-2003): ",
        "Verificación del cálculo contable de subtotales, determinación precisa del impuesto al "
        "valor agregado (IVA 13%) y cálculo de vuelto en liquidación en efectivo, decremento atómico de "
        "existencias ante ventas exitosas, e intercepción con lanzamiento estricto de InvalidOperationException "
        "ante intentos de sobreventa con inventario insuficiente."
    )

    add_bullet_point(
        "Servicio AuthService (Casos 2004-2006): ",
        "Comprobación de la verificación criptográfica de contraseñas contra hash seguro (BCrypt / SHA-256), "
        "emisión de tokens JWT con claims de identidad y rol (Administrador y Cajero), políticas de "
        "expiración y denegación de credenciales inválidas."
    )

    add_bullet_point(
        "Servicio ProductoMapping y DTOs (Casos 2007-2010): ",
        "Validación del mapeo bidireccional entre DTOs de transferencia y entidades del modelo de "
        "dominio, validación de reglas de datos de catálogo y consistencia en el identificador de categoría."
    )

    add_p(
        "Total de pruebas unitarias declaradas: 10 casos de prueba (identificadores 2001 al 2010), "
        "registrados en Azure DevOps en la suite con ID 255.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, font_size=10
    )

    add_p("Pruebas de API", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4, bold=True, font_size=10.5)

    add_p(
        "Las pruebas de API evaluaron la integración funcional de los controladores y Minimal APIs "
        "alojados en ASP.NET Core Web API, comprobando la comunicación cliente-servidor mediante "
        "solicitudes HTTP sobre los endpoints expuestos.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, font_size=10
    )

    add_bullet_point(
        "Enfoque de Verificación: ",
        "Validación de códigos de estado HTTP (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, "
        "403 Forbidden, 409 Conflict), estructura de los DTOs en formato JSON, políticas de autorización "
        "basadas en encabezados \"Authorization: Bearer <Token>\" y persistencia relacional evaluada "
        "mediante WebApplicationFactory."
    )

    add_bullet_point(
        "Endpoints de Autenticación (/api/auth/login - CP01 a CP05): ",
        "Pruebas de autenticación exitosa para administradores y cajeros con retorno de DTO con Bearer "
        "Token JWT, validación de credenciales inválidas (401), cuentas no registradas y obligatoriedad de campos requeridos (400)."
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 5: PRUEBAS DE API (cont.) & ACEPTACIÓN & RESULTADOS
    # =========================================================================
    add_bullet_point(
        "Endpoints de Control de Acceso y Catálogo (/api/productos, /api/categorias - CP06 a CP11): ",
        "Listado de catálogo de productos activo, consulta individual por ID o SKU, creación de productos "
        "por administradores con respuesta 201 Created, intercepción de peticiones anónimas sin token (401) "
        "y rechazo estricto con código 403 Forbidden ante intentos de mutación de catálogo por usuarios con rol Cajero."
    )

    add_bullet_point(
        "Endpoints de Ventas y Turnos (/api/ventas, /api/turnos - CP12 a CP15): ",
        "Registro transaccional de ventas en Terminal POS con decremento atómico de stock, bloqueo y "
        "retorno de código 409 Conflict ante sobreventa o stock insuficiente, rechazo de ventas sin artículos "
        "(400 Bad Request) y control de bloqueo de operaciones de cobro si no existe un turno de caja activo."
    )

    add_p(
        "Total de pruebas de API declaradas: 15 casos de prueba (identificadores CP01 al CP15), "
        "registrados en Azure DevOps en la suite con ID 256.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, font_size=10
    )

    add_p("Pruebas de Aceptación", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4, bold=True, font_size=10.5)

    add_p(
        "Las pruebas de aceptación validaron la conformidad del software con respecto a las "
        "expectativas de los usuarios clave y los criterios de aceptación acordados en el Product "
        "Backlog (PBIs #2010 al #2035).",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, font_size=10
    )

    add_bullet_point(
        "Metodología y Estándar: ",
        "Basadas en el estándar ISO/IEC/IEEE 29119 y especificadas en lenguaje natural estructurado "
        "Gherkin (escenarios BDD en historias de usuario con Dado, Cuando, Entonces), respaldadas con suites "
        "de pruebas en dispositivos móviles Android y matrices de trazabilidad."
    )

    add_bullet_point(
        "Módulos de Usuario Validados: ",
        "1) Autenticación y Seguridad (TC-01 a TC-02); 2) Control de Acceso RBAC y Visibilidad de UI (TC-03); "
        "3) Catálogo, Búsqueda Rápida y Escáner SKU (TC-04); 4) Alerta Visual Reactiva de Stock Crítico (TC-05); "
        "5) Control de Turnos de Caja y Arqueo Ciego (TC-06 a TC-07); 6) Terminal POS, Venta en Efectivo e Impuestos (TC-08); "
        "7) Atomicidad Anti-Sobreventa y Persistencia (TC-09 a TC-10); 8) Resumen de Dashboard Gerencial (TC-11); "
        "9) Bloqueo de POS sin Turno Activo (TC-12)."
    )

    add_p(
        "Total de pruebas de aceptación declaradas: 12 casos de prueba (identificadores TC-01 al TC-12), "
        "registrados en Azure DevOps en la suite con ID 257.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=12, font_size=10
    )

    add_p("RESULTADOS OBTENIDOS", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=6, bold=True, font_size=11.5)

    add_p(
        "A continuación se detallan de forma resumida y consolidada los resultados obtenidos en "
        "cada una de las suites de prueba ejecutadas en el marco del Ciclo 1 en Azure DevOps.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=8, font_size=10
    )

    add_p("Pruebas de Aceptación", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=2, bold=True, font_size=10.5)

    add_p("Resumen métrico de la Suite de Aceptación (Suite ID 257 en Azure DevOps):",
          align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, font_size=10)

    metric_rows_uat = [
        ("Número de pruebas declaradas:", "12 casos (IDs TC-01 a TC-12)"),
        ("Número de pruebas ejecutadas:", "12 casos (validadas en diseño y criterios BDD)"),
        ("Número de pruebas exitosas:", "12 casos (100% de conformidad)"),
        ("Número de pruebas pendientes (fallidas):", "0 casos fallidos (0 Bugs generados)")
    ]
    add_metric_table("Métrica de Aceptación", metric_rows_uat)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 6: CAPTURA ACEPTACIÓN + TABLA API + CAPTURA API
    # =========================================================================
    img_uat = os.path.abspath("Screenshots_DevOps/captura_excel_aceptacion.png")
    add_image_box(img_uat, width_inches=6.3)

    add_p("Pruebas de API", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2, bold=True, font_size=10.5)

    add_p("Resumen métrico de la Suite de Integración de API (Suite ID 256 en Azure DevOps):",
          align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, font_size=10)

    metric_rows_api = [
        ("Número de pruebas declaradas:", "15 casos (IDs CP01 a CP15)"),
        ("Número de pruebas ejecutadas:", "15 casos (ejecutadas vía REST Client / Test Runner)"),
        ("Número de pruebas exitosas:", "15 casos (100% de respuestas esperadas)"),
        ("Número de pruebas pendientes (fallidas):", "0 casos fallidos (0 Bugs generados)")
    ]
    add_metric_table("Métrica de API REST", metric_rows_api)

    img_api = os.path.abspath("Screenshots_DevOps/captura_excel_api.png")
    add_image_box(img_api, width_inches=6.3)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 7: TABLA UNITARIAS + CAPTURA UNITARIAS + CONCLUSIONES (1 y 2)
    # =========================================================================
    add_p("Pruebas Unitarias", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=2, bold=True, font_size=10.5)

    add_p("Resumen métrico de la Suite de Pruebas Unitarias (Suite ID 255 en Azure DevOps):",
          align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, font_size=10)

    metric_rows_ut = [
        ("Número de pruebas declaradas:", "10 casos (IDs 2001 a 2010)"),
        ("Número de pruebas ejecutadas:", "10 casos (ejecutadas mediante xUnit en .NET 8)"),
        ("Número de pruebas exitosas:", "10 casos superados satisfactoriamente"),
        ("Número de pruebas pendientes (fallidas):", "0 casos fallidos (0 Bugs generados)")
    ]
    add_metric_table("Métrica Unitaria", metric_rows_ut)

    img_ut = os.path.abspath("Screenshots_DevOps/captura_devops_unitarias.png")
    add_image_box(img_ut, width_inches=6.2)

    add_p("CONCLUSIONES", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=8, space_after=4, bold=True, font_size=11.5)

    add_p(
        "A partir de la ejecución sistemática de las pruebas de software y el análisis de los resultados "
        "obtenidos, se establecen las siguientes conclusiones formales:",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, font_size=10
    )

    add_bullet_point(
        "1. Integridad y Blindaje de las Reglas de Negocio Operativas: ",
        "Las pruebas unitarias y de API verificaron que el núcleo de validaciones del sistema previene "
        "eficazmente anomalías críticas en la gestión del inventario y el punto de venta. Específicamente, se "
        "comprobó que el sistema bloquea con certeza absoluta cualquier intento de sobreventa cuando la "
        "demanda excede las existencias disponibles, rechaza operaciones de facturación si no existe una "
        "jornada de caja debidamente aperturada con monto base, y garantiza la inviolabilidad de las rutas "
        "administrativas mediante control de acceso RBAC estricto, impidiendo que usuarios con rol Cajero "
        "ejecuten alteraciones no autorizadas en el catálogo de productos."
    )

    add_bullet_point(
        "2. Exactitud Algorítmica en Transacciones y Liquidación Financiera: ",
        "La suite de pruebas confirmó la solidez y consistencia matemática de los algoritmos de cobro "
        "en el Terminal POS, calculando con exactitud decimal el subtotal, el desglose impositivo del IVA (13%) "
        "y el cálculo de vuelto en operaciones en efectivo sin incurrir en desajustes por redondeo. Asimismo, el "
        "mecanismo de arqueo ciego implementado para el cierre de turno demostró registrar fielmente los balances "
        "reales frente a los cálculos teóricos del sistema, garantizando la trazabilidad contable y la conciliación "
        "antes de formalizar el cierre definitivo de la sesión de caja."
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 8: CONCLUSIÓN (3) + RECOMENDACIONES
    # =========================================================================
    add_bullet_point(
        "3. Trazabilidad Total y Madurez del Proceso de QA en Azure DevOps: ",
        "Se consolidó una trazabilidad bidireccional del 100% entre las Historias de Usuario de los "
        "PBIs (#2010 al #2035) y los casos de prueba registrados en Azure DevOps mediante relaciones "
        "formales de tipo \"Tests / Tested By\". La estandarización de las suites (Unitarias, Integración y "
        "Aceptación) conforme al estándar internacional ISO/IEC/IEEE 29119 dota al proyecto TiendaGo de "
        "un marco de calidad transparente, reproducible y preparado para escalar a futuros ciclos de desarrollo."
    )

    add_p("RECOMENDACIONES", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6, bold=True, font_size=11.5)

    add_p(
        "Con base en las observaciones recopiladas a lo largo del proceso de pruebas, se formulan "
        "las siguientes recomendaciones estratégicas y técnicas para optimizar los ciclos venideros:",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, font_size=10
    )

    add_bullet_point(
        "1. Automatización de Pruebas en el Pipeline de CI/CD (Azure Pipelines): ",
        "Se recomienda configurar un pipeline de integración continua mediante archivo YAML en Azure "
        "DevOps que ejecute automáticamente la totalidad de la suite de pruebas unitarias y de integración "
        "en cada Pull Request hacia las ramas \"develop\" y \"main\". Esto garantizará que ninguna modificación "
        "de código introduzca regresiones en la lógica de negocio ni degrade la cobertura actual de pruebas."
    )

    add_bullet_point(
        "2. Ejecución de Pruebas de Carga y Rendimiento en Endpoints Críticos: ",
        "Dado que el módulo de terminal de punto de venta y catálogo opera bajo transacciones "
        "concurrentes en horas pico de atención comercial, es prioritario implementar pruebas de rendimiento "
        "y estrés utilizando herramientas como k6 o Apache JMeter. Esto permitirá modelar la concurrencia "
        "simultánea esperada durante aperturas de jornada o promociones especiales, validando los tiempos de "
        "respuesta del backend en la nube y el comportamiento de bloqueo de concurrencia en PostgreSQL."
    )

    add_bullet_point(
        "3. Implementación de Pruebas E2E Automatizadas para la Aplicación Móvil Android: ",
        "Se sugiere incorporar herramientas de automatización de interfaz móvil como Appium o Maestro "
        "para evaluar los flujos de interacción táctil del cajero en dispositivos Android. En particular, se debe "
        "automatizar la verificación del escaneo de códigos de barra (SKU) mediante la cámara, corroborando "
        "que la lectura óptica pueble reactivamente el carrito de compras, así como el correcto ajuste de la "
        "vista (imePadding) ante el despliegue del teclado virtual en diferentes resoluciones y versiones de sistema operativo."
    )

    # Guardar en las dos rutas del proyecto
    file_target1 = "Reporte_de_Ejecucion_de_Pruebas_TiendaGo.docx"
    file_target2 = "Reporte_Ejecucion_de_Pruebas_Azure_DevOps_TiendaGo.docx"

    doc.save(file_target1)
    doc.save(file_target2)
    print(f"Report successfully saved to {file_target1} and {file_target2}")

if __name__ == "__main__":
    create_report()
