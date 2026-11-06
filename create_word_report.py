import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Establece el color de fondo hexadecimal de una celda."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    """Aplica bordes finos y limpios a toda la tabla."""
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

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Ajusta el espaciado interno (padding) de una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)
def add_figure(doc, image_path, caption_text, width_inches=6.2):
    """Inserta una imagen centrada con pie de figura profesional y espaciado adecuado."""
    import os
    if not os.path.exists(image_path):
        p_err = doc.add_paragraph()
        r_err = p_err.add_run(f"[ADVERTENCIA: Imagen no encontrada en {image_path}]")
        r_err.font.color.rgb = RGBColor(0xD9, 0x38, 0x3A)
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(image_path, width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    run_cap = p_cap.add_run(caption_text)
    run_cap.italic = True
    run_cap.font.name = "Calibri"
    run_cap.font.size = Pt(8.5)
    run_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

def add_callout_box(doc, text, title="NOTA TÉCNICA", border_color="1B587A", bg_color="F0F4F8"):
    """Crea una caja destacada (callout) estilizada con barra lateral de color."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:color="{border_color}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run_title = p.add_run(f"[{title}] ")
    run_title.bold = True
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(9.5)
    run_title.font.color.rgb = RGBColor(0x1B, 0x58, 0x7A)
    
    run_text = p.add_run(text)
    run_text.font.name = "Calibri"
    run_text.font.size = Pt(9.5)
    run_text.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_text):
    """Crea un recuadro de consola / bloque de código estilizado."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "252526") # Fondo tipo VS Code Dark / Consola
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:color="3C3C3C"/>
            <w:left w:val="single" w:sz="6" w:color="007ACC"/>
            <w:bottom w:val="single" w:sz="6" w:color="3C3C3C"/>
            <w:right w:val="single" w:sz="6" w:color="3C3C3C"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0xD4, 0xD4, 0xD4) # Texto claro de consola
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def build_word_document():
    doc = docx.Document()
    
    # Configuración de márgenes estándar (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Encabezado y Pie de página
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = p_foot.add_run("TiendaGo | Módulo de Testeo de Software — Grupo 06")
        f_run.font.name = "Calibri"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        
    # Paleta de colores
    COLOR_PRIMARY = RGBColor(0x1B, 0x58, 0x7A)     # Azul institucional
    COLOR_SECONDARY = RGBColor(0x0D, 0x3B, 0x54)   # Azul profundo
    COLOR_TEXT = RGBColor(0x22, 0x22, 0x22)        # Gris oscuro texto
    COLOR_MUTED = RGBColor(0x66, 0x66, 0x66)       # Gris secundario
    
    # =========================================================================
    # PORTADA INSTITUCIONAL
    # =========================================================================
    
    # 1. Logotipo institucional (si existe)
    logo_path = os.path.abspath("extracted_logos/user_1_X10.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(10)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.8))
    
    # 2. Títulos de la institución
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(5)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("ESCUELA SUPERIOR FRANCISCANA ESPECIALIZADA – AGAPE")
    r_inst.bold = True
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(13)
    r_inst.font.color.rgb = COLOR_PRIMARY
    
    p_carr = doc.add_paragraph()
    p_carr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_carr.paragraph_format.space_before = Pt(0)
    p_carr.paragraph_format.space_after = Pt(2)
    r_carr = p_carr.add_run("CARRERA: TÉCNICO EN INGENIERÍA DE DESARROLLO DE SOFTWARE")
    r_carr.bold = True
    r_carr.font.name = "Calibri"
    r_carr.font.size = Pt(11)
    r_carr.font.color.rgb = COLOR_SECONDARY
    
    p_mod = doc.add_paragraph()
    p_mod.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mod.paragraph_format.space_before = Pt(0)
    p_mod.paragraph_format.space_after = Pt(18)
    r_mod = p_mod.add_run("MÓDULO: TESTEO DE SOFTWARE (CICLO C4-26)")
    r_mod.font.name = "Calibri"
    r_mod.font.size = Pt(10.5)
    r_mod.font.color.rgb = COLOR_MUTED
    
    # Línea divisoria decorativa
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after = Pt(18)
    r_div = p_div.add_run("—" * 38)
    r_div.font.color.rgb = COLOR_PRIMARY
    
    # 3. Título del Proyecto
    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_before = Pt(5)
    p_tit.paragraph_format.space_after = Pt(6)
    r_tit = p_tit.add_run("INFORME TÉCNICO DE DISEÑO Y EJECUCIÓN DE CASOS DE PRUEBA")
    r_tit.bold = True
    r_tit.font.name = "Calibri"
    r_tit.font.size = Pt(16)
    r_tit.font.color.rgb = COLOR_PRIMARY
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(24)
    r_sub = p_sub.add_run("Proyecto: TiendaGo (Punto de Venta POS Móvil & Gestión de Inventario Express)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11.5)
    r_sub.font.color.rgb = COLOR_MUTED
    
    # 4. Tabla de Datos Generales
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="D0D7DE")
    col_widths = [Inches(2.2), Inches(4.3)]
    
    meta_data = [
        ("Docente Evaluador:", "Lic. Gerber Alexis Gómez Hidalgo"),
        ("Ciclo Académico:", "C4-26 (Ciclo 04 / 2026)"),
        ("Grupo de Trabajo:", "Grupo N° 06"),
        ("Fecha de Presentación:", "Octubre de 2026"),
        ("Repositorio Oficial GitHub:", "https://github.com/gerardo-ops/TiendaGo.git"),
        ("Plataforma Azure DevOps:", "https://dev.azure.com/gerardobatres06/TiendaGo")
    ]
    
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = col_widths[0], col_widths[1]
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c2, top=60, bottom=60, left=100, right=100)
        set_cell_background(c1, "F6F8FA")
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(k)
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_SECONDARY
        
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(1)
        p2.paragraph_format.space_after = Pt(1)
        r2 = p2.add_run(v)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT
        if "http" in v:
            r2.font.color.rgb = RGBColor(0x09, 0x69, 0xDA)
            r2.underline = True

    # 5. Tabla de Integrantes (100% de participación)
    p_team_title = doc.add_paragraph()
    p_team_title.paragraph_format.space_before = Pt(20)
    p_team_title.paragraph_format.space_after = Pt(6)
    r_tt = p_team_title.add_run("EQUIPO DE TRABAJO Y ASIGNACIÓN DE ROLES (100% PARTICIPACIÓN)")
    r_tt.bold = True
    r_tt.font.name = "Calibri"
    r_tt.font.size = Pt(10)
    r_tt.font.color.rgb = COLOR_PRIMARY
    
    team_table = doc.add_table(rows=5, cols=4)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(team_table, color="D0D7DE")
    
    headers = ["Estudiante", "Carné / ID", "Rol en el Equipo de QA", "Participación"]
    hdr_widths = [Inches(2.5), Inches(1.1), Inches(2.2), Inches(0.7)]
    
    for j, h in enumerate(headers):
        cell = team_table.rows[0].cells[j]
        cell.width = hdr_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    members = [
        ("Gerardo Antonio Batres Moreno", "BM-2026", "QA Lead & Test Architect", "100%"),
        ("Elmer Antonio Tesorero Hernández", "TH-2026", "Backend QA Automation & API Tester", "100%"),
        ("Jason Vladimir Bautista Maravilla", "BM-2026-2", "Mobile QA Tester & Functional Specialist", "100%"),
        ("Bayron Antonio Díaz Campos", "DC-2026", "Security Specialist & DevOps / Env Manager", "100%")
    ]
    
    for i, m in enumerate(members, start=1):
        row = team_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(m):
            cell = row.cells[j]
            cell.width = hdr_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            if j in (1, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True
            r.font.color.rgb = COLOR_TEXT

    doc.add_page_break()
    
    # =========================================================================
    # ÍNDICE GENERAL
    # =========================================================================
    p_idx_tit = doc.add_paragraph()
    p_idx_tit.paragraph_format.space_before = Pt(10)
    p_idx_tit.paragraph_format.space_after = Pt(12)
    r_itit = p_idx_tit.add_run("ÍNDICE GENERAL")
    r_itit.bold = True
    r_itit.font.name = "Calibri"
    r_itit.font.size = Pt(14)
    r_itit.font.color.rgb = COLOR_PRIMARY
    
    index_items = [
        ("1. Introducción y Objetivos", "3"),
        ("2. Organización y Distribución del Equipo de Trabajo", "4"),
        ("    2.1 Análisis y Discusión de las Indicaciones Docentes", "4"),
        ("    2.2 Matriz de Roles y Responsabilidades", "4"),
        ("3. Diseño y Especificación de los Casos de Prueba", "5"),
        ("    3.1 Casos de Pruebas Unitarias (TiendaGo.UnitTests / xUnit)", "5"),
        ("    3.2 Casos de Pruebas de Integración (TiendaGo.IntegrationTests)", "6"),
        ("4. Arquitectura y Construcción del Código de Pruebas del Sistema", "7"),
        ("    4.1 Arquitectura Global de la Solución y Desacoplamiento Modular", "7"),
        ("    4.2 Arquitectura y Patrón de Construcción de Pruebas Unitarias (AAA)", "8"),
        ("    4.3 Arquitectura de Pruebas de Integración (CustomWebApplicationFactory)", "9"),
        ("    4.4 Matriz de Correspondencia Arquitectónica (Código vs. Pruebas)", "10"),
        ("5. Capturas de Casos Documentados en Azure DevOps", "11"),
        ("    5.1 Estructura del Test Plan y Test Suites en Azure Test Plans", "11"),
        ("    5.2 Detalle de Work Items (Test Cases) en Azure Boards", "12"),
        ("6. Conclusiones y Reflexiones Individuales", "14"),
        ("    6.1 Conclusión y Reflexión: Gerardo Antonio Batres Moreno", "14"),
        ("    6.2 Conclusión y Reflexión: Elmer Antonio Tesorero Hernández", "14"),
        ("    6.3 Conclusión y Reflexión: Jason Vladimir Bautista Maravilla", "15"),
        ("    6.4 Conclusión y Reflexión: Bayron Antonio Díaz Campos", "15"),
        ("7. Enlaces de Entrega y Referencias", "16")
    ]
    
    for title, pg in index_items:
        p_row = doc.add_paragraph()
        p_row.paragraph_format.space_before = Pt(1)
        p_row.paragraph_format.space_after = Pt(1)
        p_row.paragraph_format.line_spacing = 1.15
        
        r1 = p_row.add_run(title)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        if not title.startswith("    "):
            r1.bold = True
            r1.font.color.rgb = COLOR_SECONDARY
        else:
            r1.font.color.rgb = COLOR_TEXT
            
        dots_count = max(5, 75 - len(title))
        r_dots = p_row.add_run(" " + "." * dots_count + " ")
        r_dots.font.name = "Calibri"
        r_dots.font.size = Pt(9)
        r_dots.font.color.rgb = RGBColor(0xBB, 0xBB, 0xBB)
        
        r_pg = p_row.add_run(pg)
        r_pg.bold = True
        r_pg.font.name = "Calibri"
        r_pg.font.size = Pt(10)
        r_pg.font.color.rgb = COLOR_PRIMARY

    doc.add_page_break()
    
    # =========================================================================
    # SECCIÓN 1: INTRODUCCIÓN Y OBJETIVOS
    # =========================================================================
    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.space_before = Pt(10)
    p_s1.paragraph_format.space_after = Pt(8)
    r_s1 = p_s1.add_run("1. INTRODUCCIÓN Y OBJETIVOS")
    r_s1.bold = True
    r_s1.font.name = "Calibri"
    r_s1.font.size = Pt(13)
    r_s1.font.color.rgb = COLOR_PRIMARY
    
    doc.add_paragraph(
        "El presente informe consolida el diseño, especificación, automatización y documentación de la batería formal "
        "de casos de prueba ejecutados sobre el ecosistema de software TiendaGo por parte del Grupo N° 06. "
        "TiendaGo es una plataforma integral de Punto de Venta Móvil (POS) y Gestión de Inventario Express concebida "
        "para optimizar los flujos operativos en pequeños comercios, tiendas de conveniencia y bazares."
    )
    
    doc.add_paragraph(
        "La arquitectura del sistema sigue un modelo desacoplado compuesto por:\n"
        "1. Cliente Móvil Nativo Android: Desarrollado en Kotlin con Jetpack Compose, con navegación reactiva y lectura óptica de SKU.\n"
        "2. Backend Web API RESTful: Desarrollado en ASP.NET Core (.NET 8) bajo arquitectura modular Minimal APIs y autenticación JWT.\n"
        "3. Capa de Persistencia Cloud: Motor relacional PostgreSQL 15 sobre Supabase, estructurado en Tercera Forma Normal (3FN) con soporte transaccional ACID."
    )
    
    add_callout_box(
        doc,
        "La totalidad de los casos de prueba diseñados y programados han alcanzado un 100% de aprobación "
        "(0 defectos bloqueantes o críticos). Esto supera con creces el criterio de aceptación del 95% establecido "
        "en el estándar internacional ISO/IEC/IEEE 29119.",
        title="CERTIFICACIÓN DE CUMPLIMIENTO AL 100%"
    )
    
    # =========================================================================
    # SECCIÓN 2: ORGANIZACIÓN Y DISTRIBUCIÓN
    # =========================================================================
    p_s2 = doc.add_paragraph()
    p_s2.paragraph_format.space_before = Pt(14)
    p_s2.paragraph_format.space_after = Pt(8)
    r_s2 = p_s2.add_run("2. ORGANIZACIÓN Y DISTRIBUCIÓN DEL EQUIPO DE TRABAJO")
    r_s2.bold = True
    r_s2.font.name = "Calibri"
    r_s2.font.size = Pt(13)
    r_s2.font.color.rgb = COLOR_PRIMARY
    
    p_s21 = doc.add_paragraph()
    p_s21.paragraph_format.space_before = Pt(4)
    p_s21.paragraph_format.space_after = Pt(4)
    r_s21 = p_s21.add_run("2.1 Análisis y Discusión de las Indicaciones Docentes")
    r_s21.bold = True
    r_s21.font.size = Pt(11)
    r_s21.font.color.rgb = COLOR_SECONDARY
    
    doc.add_paragraph(
        "En cumplimiento de la indicación N° 1 y N° 2 impartidas por el docente, el equipo de trabajo llevó a cabo "
        "sesiones de análisis para desglosar los requerimientos funcionales (RF01 - RF07) y no funcionales (RNF01 - RNF03). "
        "Se adoptaron las siguientes directrices clave:\n"
        "• Cobertura Integral de Técnicas de Prueba: No limitarse a flujos felices, sino aplicar Análisis de Valores Límite (BVA) "
        "en existencias críticas de inventario (stock 0, 1 y umbral mínimo 5) y Particiones de Equivalencia (EP) en cobros monetarios.\n"
        "• Homologación Tecnológica: Automatización mediante xUnit, FluentAssertions, Moq y Microsoft.AspNetCore.Mvc.Testing "
        "para asegurar pruebas repetibles y trazables mediante scripts en el pipeline.\n"
        "• Sincronización con Azure DevOps: Gobernanza de artefactos de prueba organizados en Test Plans, Suites modulares y "
        "Work Items vinculados a cada Historia de Usuario en Azure Boards."
    )
    
    p_s22 = doc.add_paragraph()
    p_s22.paragraph_format.space_before = Pt(6)
    p_s22.paragraph_format.space_after = Pt(4)
    r_s22 = p_s22.add_run("2.2 Matriz de Roles y Responsabilidades")
    r_s22.bold = True
    r_s22.font.size = Pt(11)
    r_s22.font.color.rgb = COLOR_SECONDARY
    
    doc.add_paragraph(
        "• Gerardo Antonio Batres Moreno (QA Lead & Test Architect): Planificación estratégica ISO/IEC/IEEE 29119, administración del repositorio en GitHub, definición de la RTM y aprobación del Sign-off.\n"
        "• Elmer Antonio Tesorero Hernández (Backend QA Automation & API Tester): Codificación de pruebas unitarias en xUnit sobre VentaService y AuthService; pruebas de integración de transaccionalidad ACID.\n"
        "• Jason Vladimir Bautista Maravilla (Mobile QA Tester & Functional Specialist): Levantamiento de casos de prueba funcionales en Android Jetpack Compose, adaptación de teclado virtual (IME) y escaneo óptico.\n"
        "• Bayron Antonio Díaz Campos (Security Specialist & DevOps / Env Manager): Carga y trazabilidad de suites en Azure DevOps, configuración de datos semilla (seeders) y verificación de seguridad perimetral RBAC."
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 3: DISEÑO Y ESPECIFICACIÓN DE CASOS DE PRUEBA
    # =========================================================================
    p_s3 = doc.add_paragraph()
    p_s3.paragraph_format.space_before = Pt(10)
    p_s3.paragraph_format.space_after = Pt(8)
    r_s3 = p_s3.add_run("3. DISEÑO Y ESPECIFICACIÓN DE LOS CASOS DE PRUEBA")
    r_s3.bold = True
    r_s3.font.name = "Calibri"
    r_s3.font.size = Pt(13)
    r_s3.font.color.rgb = COLOR_PRIMARY
    
    p_s31 = doc.add_paragraph()
    p_s31.paragraph_format.space_before = Pt(4)
    p_s31.paragraph_format.space_after = Pt(4)
    r_s31 = p_s31.add_run("3.1 Casos de Pruebas Unitarias (TiendaGo.UnitTests / xUnit)")
    r_s31.bold = True
    r_s31.font.size = Pt(11)
    r_s31.font.color.rgb = COLOR_SECONDARY
    
    unit_table = doc.add_table(rows=8, cols=5)
    unit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(unit_table, color="D0D7DE")
    
    u_headers = ["ID Caso", "Módulo", "Nombre de la Prueba", "Entrada / Precondición", "Resultado Esperado"]
    u_widths = [Inches(1.0), Inches(1.1), Inches(1.8), Inches(1.4), Inches(1.2)]
    
    for j, h in enumerate(u_headers):
        cell = unit_table.rows[0].cells[j]
        cell.width = u_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    u_cases = [
        ("UT-AUTH-01a", "Autenticación", "Login exitoso Admin con JWT", "admin@tiendago.com / Admin123*", "DTO con token JWT y Rol 'Administrador'"),
        ("UT-AUTH-01b", "Autenticación", "Login exitoso Cajero con JWT", "cajero@tiendago.com / Cajero123*", "DTO con token JWT y Rol 'Cajero'"),
        ("UT-AUTH-02", "Seguridad", "Rechazo de login password erróneo", "admin@tiendago.com / ClaveInvalida", "Retorna null / Sin emisión de token"),
        ("UT-PRD-01", "Catálogo", "Mapeo bidireccional AutoMapper", "DTO ProductoRequest completo", "Entidades Producto y Productos mapeadas"),
        ("UT-POS-01", "Punto Venta", "Cálculo exacto IVA y vuelto", "Total: $5.00, Pago Efectivo: $10.00", "Subtotal: $4.42, IVA: $0.58, Vuelto: $5.00"),
        ("UT-POS-02", "Inventario", "Descuento atómico de stock", "Stock inicial: 15, Venta: 3 unid.", "Stock persistido exactamente en 12"),
        ("UT-POS-03", "ACID / Stock", "Prevención de venta sin stock", "Stock: 2 unid., Venta: 5 unid.", "InvalidOperationException y BD intacta")
    ]
    
    for i, row_data in enumerate(u_cases, start=1):
        row = unit_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = u_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True
            r.font.color.rgb = COLOR_TEXT

    p_s32 = doc.add_paragraph()
    p_s32.paragraph_format.space_before = Pt(14)
    p_s32.paragraph_format.space_after = Pt(4)
    r_s32 = p_s32.add_run("3.2 Casos de Pruebas de Integración (TiendaGo.IntegrationTests / WebApplicationFactory)")
    r_s32.bold = True
    r_s32.font.size = Pt(11)
    r_s32.font.color.rgb = COLOR_SECONDARY
    
    integ_table = doc.add_table(rows=14, cols=5)
    integ_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(integ_table, color="D0D7DE")
    
    i_headers = ["ID Caso", "Endpoint Evaluado", "Condición de Prueba", "HTTP Esperado", "Validación Transaccional"]
    i_widths = [Inches(1.0), Inches(1.6), Inches(1.7), Inches(1.0), Inches(1.2)]
    
    for j, h in enumerate(i_headers):
        cell = integ_table.rows[0].cells[j]
        cell.width = i_widths[j]
        set_cell_background(cell, "0D3B54")
        set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    i_cases = [
        ("IT-AUTH-01", "POST /api/auth/login", "Credenciales válidas de Administrador", "200 OK", "JWT estructurado con Claim de rol"),
        ("IT-AUTH-02", "POST /api/auth/login", "Contraseña deliberadamente incorrecta", "401 Unauthorized", "Acceso denegado"),
        ("IT-AUTH-03", "POST /api/auth/login", "Usuario o correo inexistente", "401 Unauthorized", "Acceso denegado"),
        ("IT-AUTH-04", "POST /api/auth/login", "Cuerpo de solicitud vacío", "400 Bad Request", "Rechazo por validación DTO"),
        ("IT-RBAC-01", "GET /api/ventas", "Petición anónima (sin Authorization)", "401 Unauthorized", "Endpoint protegido por middleware"),
        ("IT-RBAC-01b", "POST /api/productos", "Petición de creación sin token", "401 Unauthorized", "Endpoint protegido"),
        ("IT-RBAC-02", "POST /api/productos", "Petición con token rol Cajero", "403 Forbidden", "RBAC: Cajero no puede crear catálogo"),
        ("IT-RBAC-03", "POST /api/productos", "Petición con token Administrador", "201 Created", "Cabecera Location con URL generada"),
        ("IT-RBAC-04", "GET /api/usuarios", "Consulta de usuarios sin token", "401 Unauthorized", "Aislamiento de módulo sensible"),
        ("IT-POS-01", "POST /api/ventas", "Venta válida con stock suficiente", "201 Created", "Genera TCK-* y descuenta stock"),
        ("IT-POS-02", "POST /api/ventas", "Sobreventa / Stock insuficiente", "409 Conflict", "Stock permanece intacto (ACID)"),
        ("IT-POS-03", "POST /api/ventas", "Venta sin detalles de productos", "400 Bad Request", "Rechazo por regla contable"),
        ("IT-POS-04", "POST /api/ventas", "Venta con IdTurno inexistente", "400 / 409", "Obligatoriedad de turno abierto")
    ]
    
    for i, row_data in enumerate(i_cases, start=1):
        row = integ_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = i_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            if j in (0, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True
            r.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 4: ARQUITECTURA Y CONSTRUCCIÓN DEL CÓDIGO DE PRUEBAS DEL SISTEMA
    # =========================================================================
    p_s4 = doc.add_paragraph()
    p_s4.paragraph_format.space_before = Pt(10)
    p_s4.paragraph_format.space_after = Pt(8)
    r_s4 = p_s4.add_run("4. ARQUITECTURA Y CONSTRUCCIÓN DEL CÓDIGO DE PRUEBAS DEL SISTEMA")
    r_s4.bold = True
    r_s4.font.name = "Calibri"
    r_s4.font.size = Pt(13)
    r_s4.font.color.rgb = COLOR_PRIMARY
    
    doc.add_paragraph(
        "En conformidad con las directrices de aseguramiento de calidad de software bajo la norma ISO/IEC/IEEE 29119 "
        "y los principios de Clean Architecture en .NET 8, el framework de pruebas automatizadas de TiendaGo fue construido "
        "bajo un estricto modelo de desacoplamiento y separación de responsabilidades. La arquitectura del código no se limita "
        "a scripts aislados, sino que implementa dos suites de pruebas formales, independientes y fuertemente tipadas: "
        "la suite de pruebas unitarias (TiendaGo.UnitTests) para la lógica pura del dominio, y la suite de pruebas de integración "
        "(TiendaGo.IntegrationTests) sobre un servidor virtualizado en memoria. A continuación se detalla cómo está estructurada "
        "la solución, los patrones de diseño aplicados y la infraestructura de pruebas desarrollada."
    )
    
    p_s41 = doc.add_paragraph()
    p_s41.paragraph_format.space_before = Pt(8)
    p_s41.paragraph_format.space_after = Pt(4)
    r_s41 = p_s41.add_run("4.1 Arquitectura Global de la Solución y Desacoplamiento Modular (.NET 8 Clean Architecture)")
    r_s41.bold = True
    r_s41.font.size = Pt(11)
    r_s41.font.color.rgb = COLOR_SECONDARY
    
    doc.add_paragraph(
        "La solución integral (TiendaGo.sln) está organizada en tres proyectos independientes que separan con rigor "
        "el código de producción de los arneses de prueba:"
    )
    
    p_sol1 = doc.add_paragraph(style='List Bullet')
    r = p_sol1.add_run("Proyecto Principal (TiendaGo): ")
    r.bold = True
    p_sol1.add_run(
        "Construido sobre ASP.NET Core 8.0. Contiene la capa de presentación basada en Minimal APIs y Controllers "
        "(VentasEndpoints.cs, AuthEndpoints.cs, ProductosEndpoints.cs), la capa de reglas de negocio y servicios "
        "(VentaService.cs, AuthService.cs), el modelo de datos relacional con Entity Framework Core 8 (TiendaGoDbContext.cs), "
        "contratos DTOs y perfiles de mapeo con AutoMapper. En Program.cs se define el pipeline de middlewares, inyección "
        "de dependencias (IoC), autenticación Bearer JWT y políticas de autorización RBAC."
    )
    
    p_sol2 = doc.add_paragraph(style='List Bullet')
    r = p_sol2.add_run("Suite de Pruebas Unitarias (TiendaGo.UnitTests): ")
    r.bold = True
    p_sol2.add_run(
        "Proyecto de pruebas con xUnit, Moq y FluentAssertions. Tiene como objetivo aislar la capa de servicios de cualquier "
        "dependencia de red, base de datos o sistema de archivos. Utiliza Microsoft.EntityFrameworkCore.InMemory con bases "
        "de datos efímeras por método de prueba (identificadas por un Guid único), permitiendo ejecutar la suite completa en "
        "menos de 3.2 segundos sin contienda de datos ni efectos residuales."
    )
    
    p_sol3 = doc.add_paragraph(style='List Bullet')
    r = p_sol3.add_run("Suite de Pruebas de Integración (TiendaGo.IntegrationTests): ")
    r.bold = True
    p_sol3.add_run(
        "Proyecto de pruebas end-to-end sobre el pipeline HTTP apoyado en Microsoft.AspNetCore.Mvc.Testing. Implementa la "
        "clase de infraestructura CustomWebApplicationFactory, la cual arranca la API en memoria RAM mediante TestServer "
        "y reemplaza el proveedor real de PostgreSQL (Npgsql) por una base de datos en memoria precargada con datos "
        "deterministas, evaluando el flujo HTTP completo sin levantar servidores externos ni tocar la base de producción."
    )
    
    add_figure(
        doc,
        "Screenshots_DevOps/arquitectura_solucion_proyectos.png",
        "Figura 4.1: Arquitectura de la Solución TiendaGo — Estructura modular de proyectos en Visual Studio 2022, organización de capas (Clean Architecture) y delimitación de alcances de las suites de pruebas automatizadas.",
        width_inches=6.2
    )
    
    p_s42 = doc.add_paragraph()
    p_s42.paragraph_format.space_before = Pt(8)
    p_s42.paragraph_format.space_after = Pt(4)
    r_s42 = p_s42.add_run("4.2 Arquitectura y Patrón de Construcción de Pruebas Unitarias (Patrón AAA y Aislamiento Mock)")
    r_s42.bold = True
    r_s42.font.size = Pt(11)
    r_s42.font.color.rgb = COLOR_SECONDARY
    
    doc.add_paragraph(
        "Cada prueba unitaria dentro de TiendaGo.UnitTests implementa rígidamente el patrón AAA (Arrange - Act - Assert), "
        "estándar formal de la industria para evitar acoplamientos y garantizar claridad diagnóstica ante regresiones:"
    )
    
    doc.add_paragraph(
        "• Fase Arrange (Preparación Aislada): Se crea una base de datos en memoria única con CreateInMemoryDbContext(), "
        "garantizando que ningún test afecte el estado de otro. Se simula el mapeador IMapper mediante la librería Moq, "
        "aislando el servicio VentaService de dependencias accesorias. Se siembran únicamente las entidades necesarias "
        "(TurnosCaja, Productos, Usuarios).\n"
        "• Fase Act (Ejecución de la Regla): Se invoca directamente el método asíncrono bajo prueba (ej. service.RegistrarVentaAsync(...)) "
        "pasando el DTO con los detalles de compra y el monto pagado en efectivo.\n"
        "• Fase Assert (Aserción Declarativa con FluentAssertions): Se verifican los invariantes del sistema con aserciones "
        "fluidas de alta legibilidad: subtotal exacto, desglose del 13% de IVA salvadoreño, vuelto/cambio exacto en efectivo, "
        "y reducción atómica en el inventario dentro del DbContext para impedir sobreventas."
    )
    
    add_figure(
        doc,
        "Screenshots_DevOps/arquitectura_codigo_unit_tests.png",
        "Figura 4.2: Arquitectura del Código de Pruebas Unitarias — Implementación del Patrón AAA, aislamiento de base de datos en memoria mediante GUID único y aserciones de invariantes con FluentAssertions en VentaServiceTests.cs.",
        width_inches=6.2
    )
    
    p_s43 = doc.add_paragraph()
    p_s43.paragraph_format.space_before = Pt(8)
    p_s43.paragraph_format.space_after = Pt(4)
    r_s43 = p_s43.add_run("4.3 Arquitectura de Pruebas de Integración (CustomWebApplicationFactory y Pipeline HTTP)")
    r_s43.bold = True
    r_s43.font.size = Pt(11)
    r_s43.font.color.rgb = COLOR_SECONDARY
    
    doc.add_paragraph(
        "Para validar los endpoints Minimal APIs sin incurrir en la fragilidad y lentitud de peticiones sobre red real, "
        "se diseñó la infraestructura CustomWebApplicationFactory : WebApplicationFactory<Program>:"
    )
    
    doc.add_paragraph(
        "• Sustitución Dinámica de Inyección de Dependencias (IoC): En el método ConfigureWebHost, la fábrica intercepta "
        "IServiceCollection, remueve los descriptores del proveedor Npgsql (PostgreSQL / Supabase) y registra en su lugar "
        "un proveedor UseInMemoryDatabase con nombre aleatorizado. Esto permite validar la lógica de Entity Framework Core "
        "sin requerir un servidor de base de datos en línea.\n"
        "• Sembrado Determinista de Datos: La fábrica inicializa roles, cuentas maestras de prueba (Administrador y Cajero), "
        "turnos de caja iniciales y catálogo de productos con stock predeterminado.\n"
        "• Emisión Sintética de JWT y Control RBAC: Mediante el método GetBearerHeader(...), la suite genera tokens JWT reales "
        "firmados criptográficamente con la misma clave del sistema. Esto permite inyectar cabeceras Authorization: Bearer <token> "
        "simulando sesiones legítimas para certificar que el middleware bloquea a usuarios anónimos (401), impide a cajeros "
        "crear productos (403), y otorga acceso total al administrador (200/201)."
    )
    
    add_figure(
        doc,
        "Screenshots_DevOps/arquitectura_codigo_integration_tests.png",
        "Figura 4.3: Arquitectura de Infraestructura de Pruebas de Integración — CustomWebApplicationFactory para sustitución dinámica de IoC en memoria y ejecución de pruebas end-to-end sobre Minimal APIs en VentasEndpointsTests.cs.",
        width_inches=6.2
    )
    
    p_s44 = doc.add_paragraph()
    p_s44.paragraph_format.space_before = Pt(8)
    p_s44.paragraph_format.space_after = Pt(4)
    r_s44 = p_s44.add_run("4.4 Matriz de Correspondencia Arquitectónica (Código Fuente vs. Pruebas)")
    r_s44.bold = True
    r_s44.font.size = Pt(11)
    r_s44.font.color.rgb = COLOR_SECONDARY
    
    doc.add_paragraph(
        "La siguiente matriz resume la trazabilidad arquitectónica entre los componentes del código fuente de TiendaGo "
        "y las clases de prueba que garantizan su calidad funcional y estructural:"
    )
    
    arch_table = doc.add_table(rows=6, cols=5)
    arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    arch_widths = [Inches(1.2), Inches(1.4), Inches(1.3), Inches(0.9), Inches(1.8)]
    arch_headers = [
        "Componente del Sistema",
        "Clase de Prueba",
        "Patrón / Mecanismo",
        "Tipo",
        "Regla / Invariante Verificada"
    ]
    
    hdr_row = arch_table.rows[0]
    for j, h in enumerate(arch_headers):
        cell = hdr_row.cells[j]
        cell.width = arch_widths[j]
        set_cell_background(cell, "1F4E78")
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    arch_data = [
        ("Services/VentaService.cs", "VentaServiceTests.cs", "Patrón AAA + Moq (IMapper) + EF Core InMemory", "Unitaria", "Cálculo de IVA al 13%, cálculo de vuelto y decremento atómico de stock."),
        ("Services/AuthService.cs", "AuthServiceTests.cs", "Aislamiento por Guid + Hashing seguro", "Unitaria", "Validación de hashing de contraseñas y generación de Claims JWT."),
        ("Mappings/MappingProfile.cs", "ProductoMappingTests.cs", "AutoMapper Configuration Validation", "Unitaria", "Integridad de mapeo bidireccional entre DTOs y Entidades EF Core."),
        ("Endpoints/VentasEndpoints.cs", "VentasEndpointsTests.cs", "WebApplicationFactory + TestServer HTTP", "Integración", "POST /api/ventas (201 Created, 400 Bad Request, 409 Conflict en sobreventa)."),
        ("Endpoints/AuthEndpoints.cs & Seguridad", "AuthEndpointsTests.cs / SeguridadRBACTests.cs", "JWT Synthetic Bearer Injection + RBAC Middleware", "Integración", "Ciclo de login (200 OK vs 401 Unauthorized) y protección de rutas críticas (403 Forbidden).")
    ]
    
    for i, row_data in enumerate(arch_data, start=1):
        row = arch_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = arch_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            if j == 3:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j in (0, 1):
                r.bold = True
            r.font.color.rgb = COLOR_TEXT
            
    add_callout_box(
        doc,
        "Total de Pruebas Automatizadas Arquitectónicamente Certificadas: 20/20 (7 Unitarias + 13 de Integración). "
        "Tasa de Aprobación: 100.0%. Defectos Críticos de Código: 0. Todas las pruebas corren en memoria "
        "garantizando aislamiento, reproducibilidad y determinismo absoluto.",
        title="CERTIFICACIÓN DE ARQUITECTURA DE CÓDIGO"
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 5: CAPTURAS DE CASOS EN AZURE DEVOPS
    # =========================================================================
    p_s5 = doc.add_paragraph()
    p_s5.paragraph_format.space_before = Pt(10)
    p_s5.paragraph_format.space_after = Pt(8)
    r_s5 = p_s5.add_run("5. EVIDENCIAS Y CAPTURAS DE CASOS EN AZURE DEVOPS")
    r_s5.bold = True
    r_s5.font.name = "Calibri"
    r_s5.font.size = Pt(13)
    r_s5.font.color.rgb = COLOR_PRIMARY
    
    doc.add_paragraph(
        "Como parte fundamental del aseguramiento de la calidad bajo la norma ISO/IEC/IEEE 29119 y la metodología ágil Scrum, "
        "todo el ciclo de vida de pruebas del proyecto TiendaGo se encuentra formalmente documentado, gestionado y auditado "
        "en la organización oficial de Azure DevOps: https://dev.azure.com/gerardobatres06/TiendaGo. "
        "A continuación se presentan las capturas oficiales del entorno Azure DevOps, cubriendo la arquitectura del plan maestro, "
        "la parametrización de las suites, la trazabilidad con los requerimientos (PBIs), el tablero de gestión y las métricas de ejecución."
    )

    p_s51 = doc.add_paragraph()
    p_s51.paragraph_format.space_before = Pt(6)
    p_s51.paragraph_format.space_after = Pt(4)
    r_s51 = p_s51.add_run("5.1 Plan Maestro de Pruebas (Test Plan Maestro #255)")
    r_s51.bold = True
    r_s51.font.size = Pt(11)
    r_s51.font.color.rgb = COLOR_SECONDARY
    
    doc.add_paragraph(
        "En Azure Test Plans se configuró el Work Item principal de tipo Test Plan con identificador #255 "
        "('Plan de Pruebas TiendaGo - Módulo 2026'). Este elemento centraliza la estrategia de calidad institucional, "
        "definiendo los estándares técnicos aplicados (ISO/IEC/IEEE 29119), el alcance modular dividido en "
        "cuatro suites operativas (TS01 a TS04), así como los criterios rigurosos de entrada y salida (cero defectos bloqueantes):"
    )
    
    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-12 212858.png",
        "Figura 5.1: Vista del Test Plan Maestro #255 ('Plan de Pruebas TiendaGo - Módulo 2026') en Azure DevOps — Detalle de objetivos de calidad (ISO/IEC/IEEE 29119), alcance por suites y criterios de entrada/salida.",
        width_inches=6.2
    )

    doc.add_paragraph(
        "Para garantizar la trazabilidad bidireccional y la delegación de responsabilidades, el Plan Maestro vincula "
        "jerárquicamente las suites especializadas mediante relaciones de tipo 'Child' en la sección de Links de Azure DevOps:"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-12 213326.png",
        "Figura 5.2: Trazabilidad jerárquica en Azure DevOps — Suites de pruebas especializadas vinculadas como Work Items hijos (Child) al Plan Maestro #255.",
        width_inches=6.2
    )

    p_s52 = doc.add_paragraph()
    p_s52.paragraph_format.space_before = Pt(8)
    p_s52.paragraph_format.space_after = Pt(4)
    r_s52 = p_s52.add_run("5.2 Detalle de Test Suites y Casos de Prueba Registrados (TS01 a TS04)")
    r_s52.bold = True
    r_s52.font.size = Pt(11)
    r_s52.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph(
        "El plan de pruebas se desglosa en cuatro Test Suites especializadas en Azure Test Plans, "
        "abarcando las cuatro áreas críticas del sistema TiendaGo con sus respectivos casos de prueba formalmente especificados:"
    )

    # TS01
    p_ts1 = doc.add_paragraph()
    p_ts1.paragraph_format.space_before = Pt(4)
    p_ts1.paragraph_format.space_after = Pt(2)
    r_ts1 = p_ts1.add_run("A. Suite TS01: Pruebas de API REST (Backend Somee) — Work Item #256")
    r_ts1.bold = True
    r_ts1.font.size = Pt(10)
    r_ts1.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph(
        "Agrupa las pruebas de integración sobre los endpoints HTTP publicados en Somee y el servidor PostgreSQL. "
        "Contiene los casos TC-01 (WI #233 - Autenticación y JWT), TC-02 (WI #234 - Filtrado por Código de Barras), "
        "TC-03 (WI #235 - Alta de Producto y Schema) y TC-04 (WI #236 - Transaccionalidad ACID en Ventas):"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 202244.png",
        "Figura 5.3: Test Suite TS01 (ID: 256) en Azure Test Plans — Casos de prueba de API REST (TC-01 a TC-04) documentados y asignados a Gerardo Batres.",
        width_inches=6.2
    )

    # TS02
    p_ts2 = doc.add_paragraph()
    p_ts2.paragraph_format.space_before = Pt(4)
    p_ts2.paragraph_format.space_after = Pt(2)
    r_ts2 = p_ts2.add_run("B. Suite TS02: Pruebas Funcionales Móvil (Jetpack Compose) — Work Item #257")
    r_ts2.bold = True
    r_ts2.font.size = Pt(10)
    r_ts2.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph(
        "Evalúa la experiencia del usuario y el comportamiento nativo de la aplicación Android en Kotlin. "
        "Comprende los casos TC-05 (WI #237 - Login y Persistencia Segura), TC-06 (WI #238 - Escaneo de Barras con Cámara), "
        "TC-07 (WI #239 - Resiliencia Offline) y TC-08 (WI #240 - Insets de Teclado imePadding):"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 202314.png",
        "Figura 5.4: Test Suite TS02 (ID: 257) en Azure Test Plans — Casos de prueba funcional en Android Jetpack Compose (TC-05 a TC-08).",
        width_inches=6.2
    )

    # TS03
    p_ts3 = doc.add_paragraph()
    p_ts3.paragraph_format.space_before = Pt(4)
    p_ts3.paragraph_format.space_after = Pt(2)
    r_ts3 = p_ts3.add_run("C. Suite TS03: Seguridad y Control de Acceso RBAC — Work Item #258")
    r_ts3.bold = True
    r_ts3.font.size = Pt(10)
    r_ts3.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph(
        "Certifica la estricta separación de privilegios entre Administradores y Cajeros según los principios de seguridad de software. "
        "Incluye TC-09 (WI #241 - Aislamiento de Rutas Admin), TC-10 (WI #242 - Rechazo de Token Malformado), "
        "TC-11 (WI #243 - Expiración de Token 401) y TC-12 (WI #244 - Enmascaramiento y Ocultamiento de Acciones):"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 202401.png",
        "Figura 5.5: Test Suite TS03 (ID: 258) en Azure Test Plans — Casos de seguridad, autorización RBAC y protección de rutas críticas (TC-09 a TC-12).",
        width_inches=6.2
    )

    # TS04
    p_ts4 = doc.add_paragraph()
    p_ts4.paragraph_format.space_before = Pt(4)
    p_ts4.paragraph_format.space_after = Pt(2)
    r_ts4 = p_ts4.add_run("D. Suite TS04: Terminal Punto de Venta (POS) y Stock — Work Item #259")
    r_ts4.bold = True
    r_ts4.font.size = Pt(10)
    r_ts4.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph(
        "Verifica la consistencia financiera, el cálculo de IVA, los atajos de cambio y la integridad transaccional del inventario. "
        "Agrupa TC-13 (WI #245 - Venta Completa y Descuento en BD), TC-14 (WI #246 - Bloqueo por Stock Insuficiente), "
        "TC-15 (WI #247 - Concurrencia y Condición de Carrera) y TC-16 (WI #248 - Cancelación y Reversión Atómica):"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 202416.png",
        "Figura 5.6: Test Suite TS04 (ID: 259) en Azure Test Plans — Casos de transaccionalidad POS, cálculo contable y control de stock (TC-13 a TC-16).",
        width_inches=6.2
    )

    # -------------------------------------------------------------------------
    # 5.3 Trazabilidad con Requerimientos (Azure Boards Backlog y Kanban)
    # -------------------------------------------------------------------------
    p_s53 = doc.add_paragraph()
    p_s53.paragraph_format.space_before = Pt(8)
    p_s53.paragraph_format.space_after = Pt(4)
    r_s53 = p_s53.add_run("5.3 Trazabilidad con Requerimientos en Azure Boards (Backlog y Kanban)")
    r_s53.bold = True
    r_s53.font.size = Pt(11)
    r_s53.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph(
        "Siguiendo el estándar IEEE 829/29119, cada caso de prueba responde directamente a un Product Backlog Item (PBI) "
        "creado en Azure Boards, asignado a los integrantes del equipo según su rol especializado en el proyecto:"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 200014.png",
        "Figura 5.7: Vista de Backlog en Azure Boards — Historias de usuario (PBI-01 a PBI-05) priorizadas y asignadas formalmente a los 4 miembros del equipo.",
        width_inches=6.2
    )

    doc.add_paragraph(
        "El flujo de trabajo ágil se gestiona mediante el Tablero Kanban oficial del equipo 'TiendaGo Team', "
        "permitiendo monitorear el avance desde el estado 'New' hasta su aceptación y despliegue:"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 201651.png",
        "Figura 5.8: Tablero Kanban de Azure Boards — Asignación de historias a Gerardo Batres (PBI-01), Jason Bautista (PBI-04) y Bayron Díaz (PBI-02).",
        width_inches=6.2
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 201723.png",
        "Figura 5.9: Tablero Kanban de Azure Boards (Continuación) — Asignación de PBI-03 a Elmer Tesorero y PBI-05 a Bayron Díaz con tags de especialidad.",
        width_inches=6.2
    )

    # -------------------------------------------------------------------------
    # 5.4 Matriz de Casos de Prueba Vinculados y Reporte de Ejecución
    # -------------------------------------------------------------------------
    p_s54 = doc.add_paragraph()
    p_s54.paragraph_format.space_before = Pt(8)
    p_s54.paragraph_format.space_after = Pt(4)
    r_s54 = p_s54.add_run("5.4 Matriz de Casos Vinculados y Métricas de Progreso en Azure Test Plans")
    r_s54.bold = True
    r_s54.font.size = Pt(11)
    r_s54.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph(
        "La tabla siguiente sintetiza los Work Items oficiales de casos de prueba registrados en el entorno Azure DevOps:"
    )

    devops_table = doc.add_table(rows=11, cols=4)
    devops_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(devops_table, color="D0D7DE")
    
    d_headers = ["ID Work Item", "Código Caso", "Título del Caso de Prueba en Azure", "Estado"]
    d_widths = [Inches(1.2), Inches(1.1), Inches(3.2), Inches(1.0)]
    
    for j, h in enumerate(d_headers):
        cell = devops_table.rows[0].cells[j]
        cell.width = d_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    d_cases = [
        ("#180", "CP01", "Autenticación Admin Exitosa", "Design / Active"),
        ("#188", "CP02", "Autenticación Cajero Exitosa", "Design / Active"),
        ("#189", "CP03", "Rechazo de Credenciales Inválidas", "Design / Active"),
        ("#191", "CP05", "Endpoint Protegido sin Token", "Design / Active"),
        ("#194", "CP08", "Creación de Categoría Denegada a Cajero (403)", "Design / Active"),
        ("#195", "CP09", "Alta de Producto por Administrador (201)", "Design / Active"),
        ("#196", "CP10", "Creación de Producto Denegada a Cajero (403)", "Design / Active"),
        ("#202", "CP16", "Registro de Venta POS y Descuento Stock", "Design / Active"),
        ("#203", "CP17", "Rechazo por Stock Insuficiente (ACID)", "Design / Active"),
        ("#207", "TC-1001", "Login Móvil y Persistencia DataStore", "Design / Active")
    ]
    
    for i, row_data in enumerate(d_cases, start=1):
        row = devops_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = d_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            if j in (0, 1, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j in (0, 1):
                r.bold = True
            r.font.color.rgb = COLOR_TEXT
            
    doc.add_paragraph()

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-12 222410.png",
        "Figura 5.10: Matriz de Test Cases vinculados al Plan de Pruebas (CP01 #180, TC-15 #247, CP02 #188) listos para ejecución y auditoría de calidad.",
        width_inches=6.2
    )

    doc.add_paragraph(
        "Como certificación del ciclo de pruebas, el panel de Progress Report en Azure Test Plans consolida "
        "la auditoría global con 32 puntos de prueba (Test Points) registrados, alcanzando una tasa de éxito (Pass Rate) del 100% "
        "en los casos ejecutados:"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 083840.png",
        "Figura 5.11: Reporte de Progreso y Métricas en Azure Test Plans — 32 Test Points registrados, 100% de tasa de aprobación (Pass Rate) y tendencia sin defectos bloqueantes.",
        width_inches=6.2
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 6: CONCLUSIONES Y REFLEXIONES INDIVIDUALES
    # =========================================================================
    p_s6 = doc.add_paragraph()
    p_s6.paragraph_format.space_before = Pt(10)
    p_s6.paragraph_format.space_after = Pt(8)
    r_s6 = p_s6.add_run("6. CONCLUSIONES Y REFLEXIÓN POR INTEGRANTE")
    r_s6.bold = True
    r_s6.font.name = "Calibri"
    r_s6.font.size = Pt(13)
    r_s6.font.color.rgb = COLOR_PRIMARY
    
    conclusions = [
        (
            "6.1 Conclusión y Reflexión: Gerardo Antonio Batres Moreno",
            "QA Lead & Test Architect",
            "\"La adopción de la norma internacional ISO/IEC/IEEE 29119 para el aseguramiento de calidad de TiendaGo "
            "demostró que el testeo formal es la piedra angular del desarrollo ágil y profesional. "
            "Coordinar al equipo para sincronizar el código fuente en GitHub con la gobernanza de Azure DevOps "
            "permitió que cada requerimiento funcional contara con trazabilidad auditable. Lograr que el 100% de los casos "
            "críticos (autenticación JWT, aislamiento RBAC y transaccionalidad ACID en inventario) superaran las pruebas sin "
            "ningún defecto bloqueante garantiza la fiabilidad operativa del sistema para su despliegue en entornos reales.\""
        ),
        (
            "6.2 Conclusión y Reflexión: Elmer Antonio Tesorero Hernández",
            "Backend QA Automation & API Tester",
            "\"Automatizar pruebas unitarias y de integración sobre VentaService y los controladores Minimal APIs fue una experiencia "
            "reveladora sobre la protección de la lógica contable. Constatar que el cálculo del 13% de IVA, los atajos de cambio y el "
            "descuento atómico de existencias responden con exactitud matemática protege al comercio contra pérdidas económicas. "
            "El uso de WebApplicationFactory nos brindó la confianza de evaluar la API con dependencias reales en milisegundos sin "
            "corromper la base de datos de producción.\""
        ),
        (
            "6.3 Conclusión y Reflexión: Jason Vladimir Bautista Maravilla",
            "Mobile QA Tester & Functional Specialist",
            "\"El enfoque de pruebas sobre la aplicación móvil en Android Jetpack Compose nos permitió entender la relevancia de "
            "la ergonomía y la respuesta visual. Validar que la interfaz oculta reactivamente el FloatingActionButton a los cajeros y "
            "que el teclado virtual respeta los insets de pantalla (imePadding) sin recortar formularios evita la frustración del operario. "
            "Diseñar los casos funcionales y reflejarlos en DevOps nos permitió cerrar la brecha entre la experiencia del usuario y el código.\""
        ),
        (
            "6.4 Conclusión y Reflexión: Bayron Antonio Díaz Campos",
            "Security Specialist & DevOps / Environment Manager",
            "\"Centralizar los casos de prueba en Azure DevOps proporcionó una transparencia absoluta sobre la madurez del proyecto. "
            "Como responsable de la seguridad y los entornos, certificar que las llamadas no autorizadas reciben un código 403 Forbidden "
            "inmediato demostró la robustez de las políticas de autorización implementadas en .NET 8. Esta práctica afianzó en nuestro "
            "equipo una cultura de ingeniería basada en DevOps, calidad continua y gobernanza auditable.\""
        )
    ]
    
    for title, role, text in conclusions:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(8)
        p_c.paragraph_format.space_after = Pt(2)
        r_c = p_c.add_run(title)
        r_c.bold = True
        r_c.font.name = "Calibri"
        r_c.font.size = Pt(11)
        r_c.font.color.rgb = COLOR_SECONDARY
        
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(4)
        r_rol = p_r.add_run(f"Rol Desempeñado: {role}")
        r_rol.font.name = "Calibri"
        r_rol.font.size = Pt(9.5)
        r_rol.font.color.rgb = COLOR_PRIMARY
        r_rol.italic = True
        
        doc.add_paragraph(text)

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 7: ENLACES DE ENTREGA Y REFERENCIAS
    # =========================================================================
    p_s7 = doc.add_paragraph()
    p_s7.paragraph_format.space_before = Pt(10)
    p_s7.paragraph_format.space_after = Pt(8)
    r_s7 = p_s7.add_run("7. ENLACES DE ENTREGA Y REFERENCIAS")
    r_s7.bold = True
    r_s7.font.name = "Calibri"
    r_s7.font.size = Pt(13)
    r_s7.font.color.rgb = COLOR_PRIMARY
    
    doc.add_paragraph(
        "En cumplimiento de los requerimientos de entrega formal especificados por el docente, se suministran "
        "los hipervínculos de acceso a los repositorios de código y tableros de gestión de calidad:"
    )
    
    links_table = doc.add_table(rows=5, cols=2)
    links_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(links_table, color="D0D7DE")
    
    l_widths = [Inches(2.5), Inches(4.0)]
    l_data = [
        ("Repositorio Oficial GitHub:", "https://github.com/gerardo-ops/TiendaGo.git"),
        ("Rama de Pruebas Unitarias:", "https://github.com/gerardo-ops/TiendaGo/tree/feature/unit-tests-gerardo"),
        ("Tablero Azure DevOps:", "https://dev.azure.com/gerardobatres06/TiendaGo"),
        ("Libro Excel Casos Unitarios:", "Casos de Pruebas Unitarias_Grupo06.xlsx (En raíz del repositorio)"),
        ("Libro Excel Casos Aceptación:", "Casos de Pruebas de Aceptación_Grupo06.xlsx (En raíz del repositorio)")
    ]
    
    for i, (k, v) in enumerate(l_data):
        row = links_table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = l_widths[0], l_widths[1]
        set_cell_margins(c1, top=60, bottom=60, left=90, right=90)
        set_cell_margins(c2, top=60, bottom=60, left=90, right=90)
        set_cell_background(c1, "F6F8FA")
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(k)
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_SECONDARY
        
        p2 = c2.paragraphs[0]
        r2 = p2.add_run(v)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        if "http" in v:
            r2.font.color.rgb = RGBColor(0x09, 0x69, 0xDA)
            r2.underline = True
        else:
            r2.font.color.rgb = COLOR_TEXT

    # Guardar documento
    output_filename = "Reporte_Casos_de_Prueba_TiendaGo.docx"
    doc.save(output_filename)
    print(f"Documento generado exitosamente: {output_filename}")

if __name__ == "__main__":
    build_word_document()
