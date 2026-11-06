import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# =============================================================================
# CONSTANTES Y COLORES
# =============================================================================
DIR_BASE = r"c:\Users\Admin\Documents\Proyectos\TiendaGo"
OUTPUT_DOCX = os.path.join(DIR_BASE, "Plan_de_Implementacion_TiendaGo.docx")

COLOR_PRIMARY = RGBColor(0x1B, 0x58, 0x7A)     # Azul Institucional / Profundo
COLOR_SECONDARY = RGBColor(0x13, 0x7A, 0x7F)   # Teal / Cyan Oscuro
COLOR_DARK = RGBColor(0x1F, 0x29, 0x37)        # Slate Oscuro para títulos menores
COLOR_BODY = RGBColor(0x2D, 0x37, 0x48)        # Texto principal suave
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)       # Texto secundario / gris
COLOR_BORDER = "D0D7DE"                        # Bordes finos de tabla
HEX_PRIMARY = "1B587A"
HEX_ROW_ALT = "F8FAFC"
HEX_HEADER_LIGHT = "F1F5F9"

# =============================================================================
# UTILIDADES XML
# =============================================================================

def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_table_borders(table, color=COLOR_BORDER, sz="4", val="single"):
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

def set_cell_margins(cell, top=70, bottom=70, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def prevent_row_split(table):
    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def repeat_header_row(table):
    header_tr = table.rows[0]._tr.get_or_add_trPr()
    header_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def add_heading_styled(doc, text, level):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Calibri"
    
    if level == 1:
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run.font.size = Pt(14)
        run.font.color.rgb = COLOR_PRIMARY
    elif level == 2:
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run.font.size = Pt(12)
        run.font.color.rgb = COLOR_SECONDARY
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_DARK
    return p

def add_body_paragraph(doc, text="", bold_prefix="", space_after=4, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = COLOR_DARK
        
    if text:
        r_txt = p.add_run(text)
        r_txt.font.name = "Calibri"
        r_txt.font.size = Pt(10)
        r_txt.font.color.rgb = COLOR_BODY
    return p

def add_bullet_item(doc, text, bold_prefix="", space_after=2):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = COLOR_DARK
        
    r_txt = p.add_run(text)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = COLOR_BODY
    return p

def add_callout_box(doc, text, title="NOTA TÉCNICA", border_color="1B587A", bg_color="F0F4F8"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
    
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
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_title = p.add_run(f"[{title}] ")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(9.5)
    r_title.font.color.rgb = RGBColor(0x1B, 0x58, 0x7A)
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(9.5)
    r_txt.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_figure(doc, image_path, caption_text, width_inches=6.2):
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
    p_cap.paragraph_format.space_after = Pt(8)
    run_cap = p_cap.add_run(caption_text)
    run_cap.italic = True
    run_cap.font.name = "Calibri"
    run_cap.font.size = Pt(8.5)
    run_cap.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

def format_table_headers(table, headers, col_widths, bg_hex=HEX_PRIMARY):
    hdr_row = table.rows[0]
    for j, h in enumerate(headers):
        cell = hdr_row.cells[j]
        cell.width = col_widths[j]
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        run = p.add_run(h)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

def format_table_data(table, data, col_widths, alignments=None):
    for i, row_data in enumerate(data):
        row = table.rows[i + 1]
        bg_col = HEX_ROW_ALT if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = col_widths[j]
            if bg_col != "FFFFFF":
                set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
            p = cell.paragraphs[0]
            align = alignments[j] if alignments else WD_ALIGN_PARAGRAPH.LEFT
            p.alignment = align
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(str(val))
            run.font.name = "Calibri"
            run.font.size = Pt(8.5)
            run.font.color.rgb = COLOR_BODY

# =============================================================================
# CONSTRUCCIÓN DEL DOCUMENTO COMPLETO
# =============================================================================

def build_implementation_plan():
    print("Iniciando la construcción del Plan de Implementación de TiendaGo...")
    doc = docx.Document()

    # Configuración de márgenes estándar (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Encabezado sutil
        header = section.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        h_run = p_head.add_run("TiendaGo POS Móvil | Plan de Implantación y Despliegue v2.0")
        h_run.font.name = "Calibri"
        h_run.font.size = Pt(8)
        h_run.font.color.rgb = COLOR_MUTED
        
        # Pie de página
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = p_foot.add_run("ESFE - AGAPE | Grupo N° 06 — Ingeniería de Software")
        f_run.font.name = "Calibri"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------------------
    # 1. PORTADA FORMAL
    # -------------------------------------------------------------------------
    logo_path = os.path.join(DIR_BASE, "Screenshots_DevOps", "portada_logos.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(DIR_BASE, "extracted_logos", "user_1_X10.png")
    
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(12)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.8))

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(4)
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
    p_mod.paragraph_format.space_after = Pt(14)
    r_mod = p_mod.add_run("MÓDULO: IMPLANTACIÓN Y TESTEO DE SISTEMAS DE SOFTWARE (CICLO C4-26)")
    r_mod.font.name = "Calibri"
    r_mod.font.size = Pt(10)
    r_mod.font.color.rgb = COLOR_MUTED

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after = Pt(14)
    r_div = p_div.add_run("—" * 42)
    r_div.font.color.rgb = COLOR_PRIMARY

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_before = Pt(6)
    p_tit.paragraph_format.space_after = Pt(4)
    r_tit = p_tit.add_run("PLAN DE IMPLEMENTACIÓN Y DESPLIEGUE DE SOFTWARE")
    r_tit.bold = True
    r_tit.font.name = "Calibri"
    r_tit.font.size = Pt(16)
    r_tit.font.color.rgb = COLOR_PRIMARY

    p_ver = doc.add_paragraph()
    p_ver.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ver.paragraph_format.space_before = Pt(0)
    p_ver.paragraph_format.space_after = Pt(6)
    r_ver = p_ver.add_run("Plan de Implantación — Versión 2.0")
    r_ver.bold = True
    r_ver.font.name = "Calibri"
    r_ver.font.size = Pt(12)
    r_ver.font.color.rgb = COLOR_SECONDARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(18)
    r_sub = p_sub.add_run("Proyecto: TiendaGo (Punto de Venta POS Móvil & Gestión de Inventario Express)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = COLOR_MUTED

    # Tabla de Metadatos
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="D0D7DE")
    col_widths = [Inches(2.3), Inches(4.2)]
    
    meta_data = [
        ("Docente Evaluador:", "Lic. Gerber Alexis Gómez Hidalgo"),
        ("Ciclo Académico:", "C4-26 (Ciclo 04 / 2026)"),
        ("Grupo de Trabajo:", "Grupo N° 06"),
        ("Fecha de Elaboración:", "Noviembre de 2026"),
        ("Repositorio Oficial GitHub:", "https://github.com/gerardo-ops/TiendaGo.git"),
        ("Plataforma Azure DevOps:", "https://dev.azure.com/gerardobatres06/TiendaGo")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = col_widths[0], col_widths[1]
        set_cell_margins(c1, top=50, bottom=50, left=90, right=90)
        set_cell_margins(c2, top=50, bottom=50, left=90, right=90)
        set_cell_background(c1, "F6F8FA")
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(k)
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_SECONDARY
        
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(1)
        p2.paragraph_format.space_after = Pt(1)
        r2 = p2.add_run(v)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_BODY
        if "http" in v:
            r2.font.color.rgb = RGBColor(0x09, 0x69, 0xDA)
            r2.underline = True

    # Tabla de Integrantes
    p_team = doc.add_paragraph()
    p_team.paragraph_format.space_before = Pt(16)
    p_team.paragraph_format.space_after = Pt(5)
    r_tt = p_team.add_run("EQUIPO DE TRABAJO Y ASIGNACIÓN DE ROLES (100% PARTICIPACIÓN)")
    r_tt.bold = True
    r_tt.font.name = "Calibri"
    r_tt.font.size = Pt(9.5)
    r_tt.font.color.rgb = COLOR_PRIMARY
    
    team_table = doc.add_table(rows=5, cols=4)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(team_table, color="D0D7DE")
    
    headers_team = ["Estudiante", "Carné / ID", "Rol en el Equipo de Implantación", "Participación"]
    t_widths = [Inches(2.5), Inches(1.1), Inches(2.2), Inches(0.7)]
    format_table_headers(team_table, headers_team, t_widths)
    
    team_members = [
        ("Gerardo Antonio Batres Moreno", "BM-2026", "Líder de Proyecto & Arquitecto de Software", "100%"),
        ("Elmer Antonio Tesorero Hernández", "TH-2026", "Ingeniero Backend & Administrador de BD", "100%"),
        ("Jason Vladimir Bautista Maravilla", "BM-2026-2", "Ingeniero Mobile POS & Soporte Terminales", "100%"),
        ("Bayron Antonio Díaz Campos", "DC-2026", "Seguridad, DevOps & Gestor de Infraestructura", "100%")
    ]
    format_table_data(team_table, team_members, t_widths, [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER])
    prevent_row_split(team_table)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # TABLA DE CONTENIDOS
    # -------------------------------------------------------------------------
    p_toc_t = doc.add_paragraph()
    p_toc_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_t.paragraph_format.space_before = Pt(10)
    p_toc_t.paragraph_format.space_after = Pt(16)
    r_toct = p_toc_t.add_run("Tabla de Contenidos")
    r_toct.bold = True
    r_toct.font.name = "Calibri"
    r_toct.font.size = Pt(16)
    r_toct.font.color.rgb = COLOR_PRIMARY

    toc_items = [
        ("1. Introducción", "3"),
        ("    1.1 Propósito", "3"),
        ("    1.2 Alcance", "3"),
        ("    1.3 Definiciones, Acrónimos, y Abreviaciones", "4"),
        ("    1.4 Referencias", "5"),
        ("    1.5 Vista Global", "5"),
        ("2. Planificación de la Entrega", "7"),
        ("    2.1 Responsabilidades", "7"),
        ("    2.2 Cronograma", "8"),
        ("3. Recursos", "10"),
        ("    3.1 Facilidades", "10"),
        ("    3.2 Hardware", "10"),
        ("    3.3 Unidad de Implantación", "12"),
        ("        3.3.1 Software de Soporte", "12"),
        ("        3.3.2 Documentación de Soporte", "13"),
        ("        3.3.3 Personal de Soporte (personas, perfiles)", "13"),
        ("4. Entrenamiento", "14"),
        ("    4.1 Plan y Cronograma de Capacitación", "14"),
        ("    4.2 Material Didáctico y Recursos de Apoyo", "15"),
        ("    4.3 Período de Adaptación, Práctica y Evaluación", "15"),
        ("5. Plan de Contingencia, Rollback y Garantía de Calidad", "16"),
        ("    5.1 Matriz de Riesgos y Mitigación", "16"),
        ("    5.2 Procedimiento de Reversión (Rollback) Paso a Paso", "17"),
        ("    5.3 Pruebas de Humo (Smoke Testing) y Acta de Aceptación", "18")
    ]

    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(toc_table, color="FFFFFF") # Sin bordes visibles para apariencia limpia
    toc_widths = [Inches(5.7), Inches(0.8)]
    
    for idx, (title, page) in enumerate(toc_items):
        row = toc_table.rows[idx]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = toc_widths[0], toc_widths[1]
        set_cell_margins(c1, top=25, bottom=25, left=40, right=40)
        set_cell_margins(c2, top=25, bottom=25, left=40, right=40)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(title)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)
        if title.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
            r1.bold = True
            r1.font.color.rgb = COLOR_PRIMARY
        else:
            r1.font.color.rgb = COLOR_BODY
            
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_before = Pt(1)
        p2.paragraph_format.space_after = Pt(1)
        r2 = p2.add_run(page)
        r2.font.name = "Calibri"
        r2.font.size = Pt(10)
        r2.font.color.rgb = COLOR_MUTED
        if title.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
            r2.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECCIÓN 1: INTRODUCCIÓN
    # -------------------------------------------------------------------------
    add_heading_styled(doc, "1. Introducción", level=1)
    
    add_heading_styled(doc, "1.1 Propósito", level=2)
    add_body_paragraph(
        doc,
        "El presente documento describe el conjunto exhaustivo de directrices, tareas técnicas, procedimientos de "
        "instalación, configuración de infraestructura en la nube, migración de datos y validación funcional necesarias "
        "para instalar, desplegar y probar el sistema de software desarrollado TiendaGo (versión 2.0). El objetivo "
        "fundamental de este plan es asegurar que la transición tecnológica hacia los usuarios finales (personal de ventas, "
        "cajeros operativos, supervisores de almacén y administradores del comercio) se realice de forma ordenada, "
        "efectiva, segura y transparente, mitigando cualquier riesgo de disrupción sobre la facturación diaria o el inventario."
    )
    add_body_paragraph(
        doc,
        "Asimismo, este instrumento provee una agenda detallada de eventos, una delimitación precisa de dependencias "
        "técnicas y formula la estrategia global de implantación para el ecosistema TiendaGo con base en su alcance "
        "y sus restricciones de entorno. La estructura de este plan toma como referencia angular el diagrama de despliegue "
        "y el modelo de capas presentado en el Documento de Arquitectura de Software de TiendaGo (v3.0), sin reemplazarlo, "
        "sino complementándolo con instrucciones operativas de ingeniería de campo, perfiles de soporte y protocolos de verificación."
    )

    add_callout_box(
        doc,
        "La implantación de TiendaGo v2.0 certifica la integración armónica entre el cliente nativo móvil Android (Kotlin / Jetpack Compose), "
        "la API RESTful desarrollada bajo ASP.NET Core 8.0 y la base de datos gestionada en la nube Supabase PostgreSQL 15, "
        "garantizando la consistencia transaccional ACID de cada venta y corte de caja.",
        title="DIRECTRIZ DE IMPLANTACIÓN"
    )

    add_heading_styled(doc, "1.2 Alcance", level=2)
    add_body_paragraph(
        doc,
        "Este documento se inicia formalmente durante la fase de Elaboración de la metodología de desarrollo de software y se "
        "concreta en la fase de Construcción, una vez superadas de manera satisfactoria las suites de pruebas automatizadas "
        "(pruebas unitarias con xUnit y pruebas de integración sobre el pipeline HTTP). Su aplicación rige la fase de "
        "Transición y Despliegue en los ambientes operativos."
    )
    add_body_paragraph(
        doc,
        "El alcance abarca de forma integral las siguientes áreas operativas y de infraestructura:"
    )
    add_bullet_item(doc, "Preparación del ambiente de hosting y ejecución del backend: aprovisionamiento del servidor web Kestrel bajo Linux/Windows con proxy inverso Nginx, configuración de certificados SSL/TLS y parametrización de variables de entorno de producción.", bold_prefix="a) Infraestructura de Servicios: ")
    add_bullet_item(doc, "Aprovisionamiento y migración de persistencia: despliegue de esquemas relacionales en PostgreSQL 15 sobre Supabase Cloud (AWS US-West-2), ejecución de migraciones automáticas mediante Entity Framework Core 8 y carga de datos semilla (seeders).", bold_prefix="b) Base de Datos Cloud: ")
    add_bullet_item(doc, "Distribución del aplicativo cliente POS móvil: compilación del release APK firmado criptográficamente, instalación en terminales táctiles Android y vinculación por Bluetooth con impresoras térmicas de tickets (58mm/80mm).", bold_prefix="c) Terminales POS Móviles: ")
    add_bullet_item(doc, "Ejecución de pruebas de humo (Smoke Testing): verificación exhaustiva en sitio de la conectividad extremo a extremo, cálculo de IVA (13%), descuento atómico de stock y emisión de tokens Bearer JWT.", bold_prefix="d) Validación Post-Despliegue: ")
    add_bullet_item(doc, "Capacitación formal de usuarios: entrenamiento práctico a cajeros, administradores y encargados de turno, entrega de manuales operativos y acompañamiento presencial asistido.", bold_prefix="e) Transferencia de Conocimiento: ")
    add_bullet_item(doc, "Definición de procedimientos de soporte post-implantación y contingencia: establecimiento de la mesa de soporte técnico en tres niveles (N1, N2, N3) y el plan de reversión segura (Rollback) ante eventualidades críticas.", bold_prefix="f) Estabilización y Soporte: ")

    add_heading_styled(doc, "1.3 Definiciones, Acrónimos, y Abreviaciones", level=2)
    add_body_paragraph(doc, "A continuación, se describen los conceptos técnicos, términos de dominio y abreviaciones clave empleadas en este plan de implantación:")
    
    definitions = [
        ("TiendaGo", "Ecosistema integral de software compuesto por una API RESTful backend (.NET 8) y un aplicativo móvil nativo Android para el control de puntos de venta (POS), facturación rápida y gestión de inventario express."),
        ("POS", "Point of Sale (Punto de Venta). Sistema informático y físico que procesa transacciones comerciales con clientes finales en el mostrador."),
        ("API", "Application Programming Interface (Interfaz de Programación de Aplicaciones). Conjunto de subrutinas y protocolos HTTP que permiten la comunicación entre el cliente móvil y el servidor central."),
        ("RESTful", "Estilo de arquitectura de software para sistemas distribuidos basado en el protocolo sin estado HTTP/HTTPS y recursos serializados en formato JSON."),
        ("ASP.NET Core 8", "Framework moderno, modular, multiplataforma y de alto rendimiento desarrollado por Microsoft para la construcción de aplicaciones web y microservicios conectados a la nube."),
        ("JWT", "JSON Web Token (RFC 7519). Estándar compacto y seguro para transmitir información de autenticación e identidad cifrada entre el cliente y el servidor."),
        ("RBAC", "Role-Based Access Control (Control de Acceso Basado en Roles). Mecanismo de seguridad que restringe las operaciones del sistema según el rol asignado (Administrador, Supervisor, Cajero)."),
        ("PostgreSQL", "Sistema gestor de bases de datos relacional de código abierto reconocido por su alta confiabilidad, integridad referencial y robustez transaccional."),
        ("Supabase", "Plataforma Backend-as-a-Service basada en código abierto que proporciona un motor PostgreSQL gestionado en la nube con pool de conexiones PgBouncer y almacenamiento S3."),
        ("EF Core", "Entity Framework Core 8.0. Mapeador objeto-relacional (ORM) para .NET que permite manipular la base de datos utilizando objetos C# fuertemente tipados."),
        ("Jetpack Compose", "Toolkit declarativo y reactivo desarrollado por Google para el diseño moderno de interfaces de usuario en el sistema operativo Android mediante Kotlin."),
        ("Kestrel", "Servidor web HTTP asíncrono y multiplataforma de eventos de alta velocidad incluido de forma nativa en ASP.NET Core."),
        ("ESC/POS", "Protocolo estándar de comandos creado por Epson para la comunicación y formateo directo de impresión sobre impresoras térmicas de tickets."),
        ("CI/CD", "Continuous Integration / Continuous Deployment. Prácticas automatizadas de integración y despliegue continuo gestionadas mediante Azure Pipelines y GitHub."),
        ("Smoke Testing", "Pruebas de humo ejecutadas inmediatamente posterior al despliegue para certificar la estabilidad básica y operatividad del entorno antes de abrir el servicio."),
        ("Rollback", "Procedimiento de reversión técnica que permite desinstalar una versión defectuosa y restaurar el sistema a la versión previa estable sin pérdida de datos."),
        ("Turno de Caja", "Ciclo contable de un cajero que comprende monto de apertura en efectivo, registro de transacciones durante la jornada y arqueo/cierre de balance."),
        ("Stakeholders", "Individuos o entidades afectadas o interesadas en el funcionamiento del sistema: comerciantes, administradores, cajeros, clientes y equipo técnico."),
        ("ESFE - AGAPE", "Escuela Superior Franciscana Especializada AGAPE, institución formadora de educación superior tecnológica.")
    ]

    def_table = doc.add_table(rows=len(definitions) + 1, cols=2)
    def_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(def_table, color="D0D7DE")
    def_widths = [Inches(1.8), Inches(4.7)]
    format_table_headers(def_table, ["Término / Acrónimo", "Definición Técnica y Contextual"], def_widths)
    format_table_data(def_table, definitions, def_widths)
    prevent_row_split(def_table)
    repeat_header_row(def_table)

    add_heading_styled(doc, "1.4 Referencias", level=2)
    add_body_paragraph(doc, "El presente plan de implantación se apoya y articula con la siguiente documentación técnica y normativa:")
    add_bullet_item(doc, "Documento de Arquitectura de Software de TiendaGo (v3.0) — Define las vistas de casos de uso, lógica en capas (Clean Architecture), modelo de datos relacional y diagrama de despliegue físico.", bold_prefix="1. ")
    add_bullet_item(doc, "Informe Técnico de Diseño y Ejecución de Casos de Prueba de TiendaGo — Elaborado por el Grupo N° 06 para el Módulo de Testeo de Software (Ciclo C4-26, ESFE - AGAPE).", bold_prefix="2. ")
    add_bullet_item(doc, "Especificación de Requerimientos de Software (SRS) de TiendaGo (v2.1) — Catálogo de requisitos funcionales (RF) y no funcionales (RNF) del sistema POS Móvil.", bold_prefix="3. ")
    add_bullet_item(doc, "Manual de Instalación y Configuración del API TiendaGo — Parámetros de variables de entorno, cadenas de conexión Npgsql, llaves secretas JWT y políticas CORS.", bold_prefix="4. ")
    add_bullet_item(doc, "Manual de Usuario del Punto de Venta Móvil TiendaGo — Perfiles Administrador y Cajero para la operación del punto de venta y cierre de turnos.", bold_prefix="5. ")
    add_bullet_item(doc, "Normas ISO/IEC/IEEE 29119 (Software Testing) e IEEE 1012 (System Verification and Validation) — Estándares internacionales de calidad y transición de software.", bold_prefix="6. ")
    add_bullet_item(doc, "Repositorio Oficial de Código Fuente en GitHub: https://github.com/gerardo-ops/TiendaGo.git.", bold_prefix="7. ")
    add_bullet_item(doc, "Organización y Proyecto en Azure DevOps: https://dev.azure.com/gerardobatres06/TiendaGo.", bold_prefix="8. ")

    add_heading_styled(doc, "1.5 Vista Global", level=2)
    add_body_paragraph(
        doc,
        "Para llevar a cabo la implantación se conforma un equipo multidisciplinario determinando los recursos humanos y "
        "tecnológicos indispensables para instalar el sistema de software desarrollado, validar las dependencias, "
        "realizar las pruebas funcionales post-despliegue y certificar la aceptación de los usuarios finales."
    )
    add_body_paragraph(
        doc,
        "En este documento se presentan de forma detallada los recursos y facilidades requeridas para desplegar "
        "TiendaGo dentro de las instalaciones del establecimiento comercial y en la nube. Asimismo, se planifican "
        "las actividades de instalación, donde cada miembro del equipo de desarrollo asume un conjunto riguroso de "
        "responsabilidades durante la ejecución de este proceso."
    )
    add_body_paragraph(
        doc,
        "La vista de implantación complementa la arquitectura física del sistema, ilustrando cómo interactúan los "
        "dispositivos móviles de los cajeros con la capa de servicios web Kestrel y la base de datos en la nube. "
        "A continuación, se presenta el Diagrama de Despliegue UML correspondiente al ecosistema TiendaGo:"
    )

    # Inserción de la Imagen del Diagrama de Despliegue
    diag_img_path = os.path.join(DIR_BASE, "Screenshots_DevOps", "diagrama_despliegue_tiendago.png")
    add_figure(
        doc,
        diag_img_path,
        "Figura 1.1: Diagrama de Despliegue UML del Ecosistema TiendaGo v2.0 - Arquitectura desacoplada en tres capas (Terminales POS Android, Servidor Kestrel Web API y Persistencia Supabase PostgreSQL en la Nube).",
        width_inches=6.3
    )

    add_body_paragraph(
        doc,
        "Tal como se modela en la Figura 1.1, la arquitectura física y de red se estructura en nodos bien diferenciados:"
    )

    node_desc = [
        ("Nodo Terminal POS Móvil Android (Cliente)", "Dispositivos móviles (smartphones o tablets de 5.5 a 10 pulgadas) portados por cajeros y vendedores. Ejecuta la aplicación nativa en Kotlin con Jetpack Compose, gestiona la captura óptica de códigos de barra mediante la cámara y almacena localmente el token Bearer JWT de sesión de forma cifrada."),
        ("Nodo Impresora Térmica Bluetooth (Periférico)", "Mini impresoras térmicas portátiles de 58 mm o 80 mm conectadas vía Bluetooth 5.0 (perfil SPP). Reciben cadenas de bytes formateadas según el estándar ESC/POS para imprimir tickets de venta y reportes de corte de caja."),
        ("Nodo Estación Administrativa PC (Cliente Web)", "Computadoras personales de gerencia con navegadores web modernos (Chrome, Edge, Firefox) para la consulta del Dashboard analítico, gestión de catálogos y auditoría técnica mediante Swagger UI."),
        ("Nodo Servidor de Aplicación (Host Web API)", "Servidor físico o instancia cloud que hospeda el Web API ASP.NET Core 8 sobre Kestrel con proxy inverso Nginx. Contiene la lógica de negocio (cálculo de IVA 13%, stock atómico, JWT, RBAC) y el ORM Entity Framework Core 8."),
        ("Nodo Supabase Cloud Infrastructure (Base de Datos)", "Instancia gestionada de PostgreSQL 15 en AWS (US-West-2). Incluye el connection pooler PgBouncer en el puerto 6543 para absorber alta concurrencia, replicación activa y almacenamiento S3 para imágenes."),
        ("Nodo Plataforma DevOps & CI/CD", "Integración de GitHub y Azure DevOps para la gestión del ciclo de vida del software, compilación desatendida, ejecución de suites xUnit y despliegue continuo automatizado.")
    ]

    nodes_table = doc.add_table(rows=len(node_desc) + 1, cols=2)
    nodes_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(nodes_table, color="D0D7DE")
    nodes_widths = [Inches(2.2), Inches(4.3)]
    format_table_headers(nodes_table, ["Nodo del Diagrama", "Descripción de Componentes y Funcionalidad"], nodes_widths)
    format_table_data(nodes_table, node_desc, nodes_widths)
    prevent_row_split(nodes_table)
    repeat_header_row(nodes_table)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECCIÓN 2: PLANIFICACIÓN DE LA ENTREGA
    # -------------------------------------------------------------------------
    add_heading_styled(doc, "2. Planificación de la Entrega", level=1)
    
    add_heading_styled(doc, "2.1 Responsabilidades", level=2)
    add_body_paragraph(
        doc,
        "Para llevar a cabo con éxito la implantación del sistema desarrollado, es imperativo establecer un marco de compromiso "
        "formal y transparente entre los clientes (dueños del negocio, administradores de tienda, personal de operaciones) "
        "y el equipo de ingenieros de desarrollo e implantación (Grupo N° 06)."
    )
    add_body_paragraph(
        doc,
        "El equipo de desarrollo asume la responsabilidad ineludible de realizar una rigurosa fase previa de pruebas en un ambiente "
        "de Staging controlado, idéntico en configuración al entorno real de producción. Ningún binario, paquete APK o script de "
        "base de datos se transfiere a las terminales del cliente sin haber superado al 100% las suites automatizadas de pruebas unitarias "
        "y de integración registradas en Azure DevOps. Una vez concluidas estas pruebas previas, el equipo asume el compromiso formal "
        "de entregar el sistema totalmente operativo, configurado y validado en las instalaciones comerciales."
    )
    add_body_paragraph(
        doc,
        "A continuación, se define la Matriz RACI (Responsible, Accountable, Consulted, Informed) para las actividades fundamentales del despliegue:"
    )

    raci_data = [
        ("Aprovisionamiento de Nube Supabase y BD", "Elmer Tesorero", "Gerardo Batres", "Bayron Díaz", "Administrador Tienda"),
        ("Compilación y Despliegue de Web API .NET 8", "Elmer Tesorero", "Gerardo Batres", "Bayron Díaz", "Equipo QA"),
        ("Distribución e Instalación de App Móvil Android", "Jason Bautista", "Gerardo Batres", "Elmer Tesorero", "Cajeros / Vendedores"),
        ("Configuración y Enlace de Impresoras Bluetooth", "Jason Bautista", "Gerardo Batres", "Personal Tienda", "Cajeros"),
        ("Carga de Catálogo Inicial y Datos Semilla", "Elmer Tesorero", "Gerardo Batres", "Administrador Tienda", "Personal Almacén"),
        ("Batería de Pruebas de Humo (Smoke Tests) en Sitio", "Gerardo Batres", "Gerardo Batres", "Equipo Grupo 06", "Docente Evaluador"),
        ("Capacitación y Entrenamiento de Usuarios", "Bayron Díaz", "Gerardo Batres", "Jason Bautista", "Personal de Tienda"),
        ("Pase Oficial a Producción y Firma de Aceptación", "Gerardo Batres", "Docente Evaluador", "Gerencia Tienda", "Comunidad Académica")
    ]

    raci_table = doc.add_table(rows=len(raci_data) + 1, cols=5)
    raci_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(raci_table, color="D0D7DE")
    raci_widths = [Inches(2.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)]
    format_table_headers(raci_table, ["Actividad de Implantación", "Responsable (R)", "Aprobador (A)", "Consultado (C)", "Informado (I)"], raci_widths)
    format_table_data(raci_table, raci_data, raci_widths, [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER])
    prevent_row_split(raci_table)
    repeat_header_row(raci_table)

    add_heading_styled(doc, "2.2 Cronograma", level=2)
    add_body_paragraph(
        doc,
        "La implantación de TiendaGo en las instalaciones comerciales y en la nube es responsabilidad directa del Grupo N° 06. "
        "A continuación, se detalla la propuesta secuencial de actividades agrupadas en 6 fases estratégicas, diseñadas para "
        "garantizar una puesta en marcha ordenada y sin riesgos:"
    )

    add_bullet_item(doc, "El equipo de desarrollo culminará y congelará todos los manuales de usuario, especificaciones de endpoints en Swagger, scripts de migración y actas técnicas de pruebas automatizadas.", bold_prefix="1. Cierre y Auditoría Documental: ")
    add_bullet_item(doc, "Inspección física y lógica de los recursos de hardware (terminales móviles Android, impresoras térmicas, conectividad Wi-Fi y cableada) y validación de conectividad con Supabase Cloud. Tiempo estimado: 3 días hábiles.", bold_prefix="2. Verificación de Recursos Mínimos: ")
    add_bullet_item(doc, "Coordinación técnica con la gerencia del comercio y el docente evaluador (Lic. Gerber Gómez) para definir el cronograma de corte, los horarios de menor afluencia para pruebas en sitio y la asignación física de mostradores. Tiempo estimado: 2 días hábiles.", bold_prefix="3. Notificación y Coordinación Logística: ")
    add_bullet_item(doc, "Instalación de binarios en el servidor host, ejecución de migraciones en PostgreSQL, distribución de las APKs móviles en los smartphones, emparejamiento Bluetooth de impresoras y ejecución de la suite de Smoke Testing. Tiempo estimado: 4 días hábiles.", bold_prefix="4. Instalación Física, Lógica y Pruebas Piloto: ")
    add_bullet_item(doc, "Capacitación formal e intensiva al personal administrativo y cajeros operativos durante 4 jornadas consecutivas, seguida de un período de práctica asistida. Tiempo estimado: 5 días hábiles.", bold_prefix="5. Entrenamiento del Personal Operativo: ")
    add_bullet_item(doc, "Monitoreo intensivo (Hypercare) durante las primeras semanas post-despliegue por parte de los desarrolladores, asistencia inmediata ante incidencias y traspaso de administración a largo plazo. Tiempo estimado: 3 semanas.", bold_prefix="6. Soporte Técnico y Estabilización: ")

    cron_data = [
        ("F1.1", "Auditoría de código fuente y congelamiento de rama main", "1 día", "Ninguna", "Gerardo Batres", "Release Candidate v2.0"),
        ("F1.2", "Generación final de manuales técnicos y de usuario", "2 días", "F1.1", "Bayron Díaz", "Manuales PDF listos"),
        ("F2.1", "Aprovisionamiento de Supabase Cloud y pooling PgBouncer", "1 día", "F1.1", "Elmer Tesorero", "DB Host activa"),
        ("F2.2", "Ejecución de migraciones EF Core y datos semilla (seeders)", "2 días", "F2.1", "Elmer Tesorero", "Tablas 3FN inicializadas"),
        ("F3.1", "Publicación de Web API .NET 8 en Kestrel / Nginx", "1 día", "F2.2", "Elmer Tesorero", "API en línea (HTTP 200)"),
        ("F3.2", "Inspección de Swagger UI y verificación de tokens JWT", "1 día", "F3.1", "Bayron Díaz", "Endpoints auditados"),
        ("F4.1", "Compilación y firma de APK release Android", "1 día", "F1.1", "Jason Bautista", "APK v2.0 firmado"),
        ("F4.2", "Instalación en terminales POS y enlace Bluetooth con impresoras", "2 días", "F4.1", "Jason Bautista", "POS vinculados y probados"),
        ("F5.1", "Ejecución de batería de Smoke Testing en ambiente real", "2 días", "F3.2, F4.2", "Gerardo Batres", "Reporte Smoke Tests"),
        ("F5.2", "Simulación transaccional completa (Venta, IVA, Arqueo)", "1 día", "F5.1", "Equipo G06", "Caja cuadrada al 100%"),
        ("F6.1", "Programa de capacitación intensiva a cajeros y administradores", "4 días", "F5.2", "Bayron Díaz", "Personal certificado"),
        ("F6.2", "Pase a Producción (Go-Live) y firma del acta de recepción", "1 día", "F6.1", "G06 / Gerencia", "Acta Sign-off firmada"),
        ("F6.3", "Ventana de soporte intensivo en sitio (Hypercare)", "10 días", "F6.2", "Equipo G06", "Bitácora de soporte limpia")
    ]

    cron_table = doc.add_table(rows=len(cron_data) + 1, cols=6)
    cron_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cron_table, color="D0D7DE")
    cron_widths = [Inches(0.6), Inches(2.2), Inches(0.8), Inches(0.8), Inches(1.0), Inches(1.1)]
    format_table_headers(cron_table, ["ID", "Hito / Actividad", "Duración", "Predecesor", "Responsable", "Entregable"], cron_widths)
    format_table_data(cron_table, cron_data, cron_widths, [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    prevent_row_split(cron_table)
    repeat_header_row(cron_table)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECCIÓN 3: RECURSOS
    # -------------------------------------------------------------------------
    add_heading_styled(doc, "3. Recursos", level=1)
    
    add_heading_styled(doc, "3.1 Facilidades", level=2)
    add_body_paragraph(
        doc,
        "El proceso de implantación cuenta con un conjunto de ventajas competitivas sustanciales provistas por el equipo de "
        "desarrolladores del Grupo N° 06 y el ecosistema tecnológico institucional de ESFE - AGAPE:"
    )
    add_body_paragraph(
        doc,
        "En primer término, se destaca la experiencia técnica adquirida por el equipo durante el ciclo formativo en la instalación, "
        "prueba y despliegue de soluciones transaccionales .NET en plataformas locales y cloud, lo cual reduce drásticamente los "
        "tiempos de diagnóstico e instalación."
    )
    add_body_paragraph(
        doc,
        "Por otro lado, se dispone de la inmensa facilidad de que TiendaGo fue concebido y desarrollado íntegramente bajo la filosofía "
        "de software de código abierto (Open Source) y estándares libres:"
    )
    add_bullet_item(doc, "El backend corre sobre Microsoft .NET 8.0, un framework libre, moderno y multiplataforma que no requiere costos por licencias de servidor propietario.", bold_prefix="Cero Costo en Licenciamiento de Framework: ")
    add_bullet_item(doc, "La persistencia opera sobre PostgreSQL 15 en Supabase Cloud, el motor relacional libre más avanzado del mundo, eliminando pagos de licencias anuales de bases de datos propietarias y facilitando su comprensión y mantenimiento a largo plazo.", bold_prefix="Motor de Datos de Código Libre: ")
    add_bullet_item(doc, "El cliente móvil se construyó en Kotlin y Android SDK, permitiendo su despliegue libre sin pagos a intermediarios ni dependencia de tiendas privadas cerradas.", bold_prefix="Ecosistema Móvil Abierto: ")
    add_bullet_item(doc, "Disponibilidad integral de documentación técnica de arquitectura, casos de prueba trazados en Azure DevOps y manuales de usuario ilustrados paso a paso.", bold_prefix="Documentación Exhaustiva: ")
    add_bullet_item(doc, "Canal de comunicación directo y preferente entre los comerciantes y los ingenieros de desarrollo del Grupo N° 06, asegurando respuesta rápida e interactiva ante cualquier inquietud.", bold_prefix="Comunicación Directa: ")

    add_heading_styled(doc, "3.2 Hardware", level=2)
    add_body_paragraph(
        doc,
        "En cuanto a los requerimientos de hardware necesarios para la implantación del sistema desarrollado, se ha diseñado "
        "una solución tecnológica de alto rendimiento pero sumamente optimizada, evitando exigir hardware costoso o de última "
        "generación que limite la viabilidad económica del comercio. TiendaGo está concebido para un tráfico transaccional "
        "continuo, pero con un nivel de estrés computacional predecible y balanceado."
    )
    add_body_paragraph(
        doc,
        "La base de datos relacional demanda capacidad de almacenamiento persistente en disco sólido (SSD) ya que, aunque al comienzo "
        "se registre un catálogo moderado, con el tiempo se acumularán cientos de miles de transacciones de ventas, líneas de detalle, "
        "cortes de caja y registros de auditoría que deben conservarse intactos sin ser borrados para fines contables y de respaldo."
    )
    add_body_paragraph(
        doc,
        "La implantación previa de pruebas ejecutada por el Grupo N° 06 demostró que el entorno de desarrollo ofrece una referencia "
        "sólida sobre lo que se requiere en producción. A continuación, se detalla la comparativa técnica entre los requerimientos mínimos y recomendados:"
    )

    hw_specs = [
        ("Servidor de Aplicación (Host Web API Kestrel)", "Intel / AMD Dual-Core 2.0 GHz, 4 GB RAM, 25 GB SSD libre, Red 50 Mbps", "Intel / AMD Quad-Core 2.4 GHz+, 8 GB RAM DDR4, 50 GB SSD NVMe, Red 100 Mbps", "Aloja el Web API ASP.NET Core 8, proxy Nginx y genera tokens JWT."),
        ("Base de Datos (Supabase Cloud Infrastructure)", "Instancia Cloud AWS US-West-2, 1 GB RAM asignada, 10 GB Storage NVMe", "Instancia Pro Cloud AWS, 2 GB RAM, 20 GB Storage con backup diario continuo", "Persistencia ACID, pool PgBouncer en puerto 6543, replicación WAL."),
        ("Terminales POS Móviles (Cajeros)", "Smartphone Android 8.0+, Quad-Core 1.8 GHz, 3 GB RAM, Pantalla 5.5\", Cámara 8 MP", "Smartphone/Tablet Android 11+, Octa-Core 2.0 GHz, 4 GB RAM, Pantalla 6.5\" FHD, Batería 5000 mAh", "Ejecuta app móvil en Jetpack Compose, lectura óptica de código de barra."),
        ("Impresoras Térmicas de Tickets", "Mini Impresora Térmica 58 mm, Bluetooth 4.0, velocidad 70 mm/s, batería 1500 mAh", "Impresora Térmica 80 mm, Bluetooth 5.0 / USB, cortador automático, 200 mm/s", "Emisión rápida de tickets ESC/POS y comprobantes de corte de caja."),
        ("Estación Administrativa PC", "PC de escritorio / Laptop Dual-Core 2.0 GHz, 4 GB RAM, Pantalla 1366x768", "PC Intel Core i3/i5, 8 GB RAM, Pantalla FHD 1080p, SSD 120 GB", "Gestión administrativa, Dashboard analítico y auditoría técnica.")
    ]

    hw_table = doc.add_table(rows=len(hw_specs) + 1, cols=4)
    hw_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(hw_table, color="D0D7DE")
    hw_widths = [Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.1)]
    format_table_headers(hw_table, ["Componente de Hardware", "Especificación Mínima", "Especificación Recomendada", "Propósito en el Sistema"], hw_widths)
    format_table_data(hw_table, hw_specs, hw_widths)
    prevent_row_split(hw_table)
    repeat_header_row(hw_table)

    add_heading_styled(doc, "3.3 Unidad de Implantación", level=2)
    
    add_heading_styled(doc, "3.3.1 Software de Soporte", level=3)
    add_body_paragraph(
        doc,
        "El equipo de desarrolladores de TiendaGo considera que, para un funcionamiento óptimo, seguro y estable del sistema, "
        "es necesario que en el servidor y en los dispositivos clientes se disponga del software de base correspondiente a la "
        "pila tecnológica empleada en el desarrollo."
    )
    add_body_paragraph(
        doc,
        "A continuación, se detalla el software de soporte requerido para la implantación:"
    )

    sw_data = [
        ("Sistema Operativo Servidor", "Linux Ubuntu Server 22.04 LTS (o Windows Server 2022)", "Sistema operativo base para hospedar servicios de backend con alta disponibilidad."),
        ("Runtime de Backend", "Microsoft .NET 8.0 Runtime & ASP.NET Core Hosting Bundle", "Entorno de ejecución administrado para procesar las peticiones del Web API."),
        ("Servidor Web / Reverse Proxy", "Nginx v1.22+ (o IIS 10 en entornos Windows)", "Gestión de tráfico HTTPS, balanceo, compresión Gzip y terminación TLS 1.3."),
        ("Manejador de Base de Datos", "PostgreSQL 15.6+ (Cloud Supabase)", "Motor relacional ACID con extensiones uuid-ossp, pgcrypto y citext."),
        ("Herramientas de Desarrollo / Mantenimiento", "Visual Studio 2022, VS Code, Android Studio, DBeaver, Postman", "Herramientas empleadas durante la construcción para depuración y soporte."),
        ("Software Cliente Móvil", "Android 8.0 Oreo (API Level 26) o superior", "Plataforma cliente sobre la cual opera la aplicación móvil compilada en Kotlin."),
        ("Software de Navegación", "Google Chrome 110+, Microsoft Edge 110+, Firefox 110+", "Navegadores modernos para administradores y acceso a Swagger OpenAPI UI.")
    ]

    sw_table = doc.add_table(rows=len(sw_data) + 1, cols=3)
    sw_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sw_table, color="D0D7DE")
    sw_widths = [Inches(1.8), Inches(2.2), Inches(2.5)]
    format_table_headers(sw_table, ["Categoría de Software", "Nombre y Versión Certificada", "Función en el Ecosistema"], sw_widths)
    format_table_data(sw_table, sw_data, sw_widths)
    prevent_row_split(sw_table)
    repeat_header_row(sw_table)

    add_heading_styled(doc, "3.3.2 Documentación de Soporte", level=3)
    add_body_paragraph(
        doc,
        "Toda la documentación técnica requerida para el soporte y evolución del sistema se encuentra formalmente organizada y disponible:"
    )
    add_bullet_item(doc, "Documento de Arquitectura de Software TiendaGo (v3.0): Especifica el diseño de capas, interfaces de servicios, modelo entidad-relación y diagramas de paquetes.", bold_prefix="a) ")
    add_bullet_item(doc, "Manual de Despliegue Técnico y Configuración de Servidor: Detalla los pasos para publicar binarios de .NET 8, configurar appsettings.json, claves JWT y certificados SSL.", bold_prefix="b) ")
    add_bullet_item(doc, "Manual de Usuario del Administrador: Guía exhaustiva sobre creación de cuentas, asignación de roles RBAC, parametrización de IVA, gestión de catálogo y reportes de caja.", bold_prefix="c) ")
    add_bullet_item(doc, "Manual de Operación Rápida del Cajero (Cheat Sheet): Lámina plastificada con los pasos para apertura de turno, cobro rápido, cambio y arqueo de caja.", bold_prefix="d) ")
    add_bullet_item(doc, "Plan de Respaldos y Recuperación ante Desastres (Disaster Recovery): Guía para la restauración inmediata de snapshots de base de datos en Supabase Cloud.", bold_prefix="e) ")

    add_heading_styled(doc, "3.3.3 Personal de Soporte (Personas, Perfiles y Niveles de Escalamiento)", level=3)
    add_body_paragraph(
        doc,
        "El personal de soporte estará estructurado en tres niveles jerárquicos claramente delimitados, combinando al personal "
        "operativo de la tienda, la unidad institucional de TI y el equipo de desarrolladores de TiendaGo (Grupo N° 06):"
    )

    support_levels = [
        ("Nivel 1: Soporte Operativo Local", "Administrador / Supervisor de Tienda", "15 minutos", "Atención presencial en mostrador: cambio de rollos en impresoras térmicas, desbloqueo de usuarios, reseteo de contraseñas, reconexión de Bluetooth en terminales móviles y dudas de cobro."),
        ("Nivel 2: Soporte de Red e Infraestructura", "Personal de TI Institucional (ESFE - AGAPE)", "1 a 2 horas", "Monitoreo del enlace de Internet, configuración de switches y routers Wi-Fi en el local, verificación de apertura de puertos y renovación de certificados de seguridad TLS."),
        ("Nivel 3: Soporte Técnico Especializado", "Equipo de Desarrolladores TiendaGo (Grupo 06)", "30 min (Crítico) / 4 h (Normal)", "Mantenimiento del código fuente C# y Kotlin, parches de seguridad (hotfixes), depuración de excepciones en el Web API, optimización de queries SQL en Supabase y reversiones (Rollback).")
    ]

    sup_table = doc.add_table(rows=len(support_levels) + 1, cols=4)
    sup_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sup_table, color="D0D7DE")
    sup_widths = [Inches(1.8), Inches(1.5), Inches(1.0), Inches(2.2)]
    format_table_headers(sup_table, ["Nivel de Soporte", "Responsable / Perfil", "SLA / Respuesta", "Alcance y Responsabilidades Técnicas"], sup_widths)
    format_table_data(sup_table, support_levels, sup_widths)
    prevent_row_split(sup_table)
    repeat_header_row(sup_table)

    add_body_paragraph(
        doc,
        "En el sistema existirá un perfil de usuario exclusivo denominado Administrador, dotado de privilegios para asignar permisos "
        "RBAC, auditar turnos de caja en tiempo real y supervisar las métricas de rendimiento del sistema en intervalos regulares."
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECCIÓN 4: ENTRENAMIENTO
    # -------------------------------------------------------------------------
    add_heading_styled(doc, "4. Entrenamiento", level=1)
    
    add_heading_styled(doc, "4.1 Plan y Cronograma de Capacitación", level=2)
    add_body_paragraph(
        doc,
        "Es un factor de éxito crítico resaltar que el entrenamiento y la transferencia de competencias hacia el personal operativo "
        "y administrativo del comercio está coordinado conjuntamente por el equipo de desarrolladores de TiendaGo (Grupo N° 06) "
        "y los encargados de TI. Dado que el equipo de desarrollo no podrá brindar asistencia presencial permanente después del "
        "período de estabilización, el entrenamiento garantiza la total autosuficiencia operativa del cliente."
    )
    add_body_paragraph(
        doc,
        "El programa de capacitación está estructurado en 4 días intensivos (sesiones de 2 horas diarias), combinando teoría conceptual, "
        "demostraciones guiadas y práctica interactiva sobre terminales con datos simulados:"
    )

    train_data = [
        ("Día 1", "Introducción al Ecosistema y Gestión de Sesiones", "Cajeros, Supervisores y Administradores", "Familiarización con el hardware POS móvil, encendido de terminales, inicio de sesión seguro con credenciales individuales, comprensión de roles RBAC y procedimiento formal de apertura de turno de caja ingresando el fondo inicial en efectivo."),
        ("Día 2", "Operaciones de Venta en el POS Móvil y Emisión de Tickets", "Cajeros y Personal de Ventas", "Búsqueda en catálogo por nombre o categoría, escaneo óptico de códigos de barras mediante la cámara integrada, desglose automático del IVA (13%), cálculo en tiempo real del vuelto en pagos en efectivo, cobros con tarjeta y emisión de tickets térmicos Bluetooth."),
        ("Día 3", "Gestión de Inventario Express y Catálogo de Productos", "Supervisores de Almacén y Administradores", "Alta y modificación de productos, asignación de precios de costo y venta, control de existencias mínimas, configuración de alertas de bajo stock, ajuste de inventario por ingreso de mercancía y categorización del catálogo."),
        ("Día 4", "Cierre de Turno, Arqueo de Caja y Resolución de Incidentes", "Cajeros, Supervisores y Administradores", "Procedimiento de corte de caja, cálculo del balance esperado versus efectivo físico contado, documentación de discrepancias (faltantes/sobrantes), visualización del Dashboard analítico y protocolo de soporte ante fallas comunes (falta de papel, reinicio de Wi-Fi).")
    ]

    train_table = doc.add_table(rows=len(train_data) + 1, cols=4)
    train_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(train_table, color="D0D7DE")
    train_widths = [Inches(0.8), Inches(1.8), Inches(1.5), Inches(2.4)]
    format_table_headers(train_table, ["Jornada", "Módulo Temático", "Audiencia Destino", "Objetivos de Aprendizaje y Práctica"], train_widths)
    format_table_data(train_table, train_data, train_widths)
    prevent_row_split(train_table)
    repeat_header_row(train_table)

    add_heading_styled(doc, "4.2 Material Didáctico y Recursos de Apoyo", level=2)
    add_body_paragraph(doc, "Para garantizar la retención y disponibilidad de consulta permanente, se suministrarán los siguientes recursos educativos:")
    add_bullet_item(doc, "Manual de Usuario en Formato Digital PDF: Documento completo con capturas de pantalla, explicaciones de campos y diagramas de flujo.", bold_prefix="1. Manual Digital Interactivo: ")
    add_bullet_item(doc, "Guías Rápidas de Mostrador (Cheat Sheets): Láminas plastificadas de alta resistencia ubicadas junto a cada punto de cobro con los atajos y pasos críticos para realizar una venta en menos de 30 segundos.", bold_prefix="2. Guías de Referencia Rápida: ")
    add_bullet_item(doc, "Micro-videos de Capacitación (Píldoras Digitales): Clips audiovisuales de 2 minutos que demuestran flujos específicos: 'Cómo abrir turno', 'Cómo escanear un código de barras' y 'Cómo imprimir el corte de caja'.", bold_prefix="3. Cápsulas Audiovisuales: ")
    add_bullet_item(doc, "Base de Datos de Entrenamiento (Sandbox): Entorno de pruebas con productos y precios simulados para que los cajeros practiquen sin alterar los balances contables reales.", bold_prefix="4. Entorno de Práctica Controlada: ")

    add_heading_styled(doc, "4.3 Período de Adaptación, Práctica Asistida y Evaluación", level=2)
    add_body_paragraph(
        doc,
        "En la práctica real, el período de adaptación de los usuarios al sistema será sumamente ágil y natural, debido a que "
        "varios de los colaboradores del comercio y docentes evaluadores han tenido contacto visual previo con la solución "
        "y han presenciado las demostraciones funcionales del software durante las diferentes entregas de casos de uso y avances de sprint."
    )
    add_body_paragraph(
        doc,
        "Durante los primeros 5 días posteriores a la capacitación, el equipo de desarrollo implementará un acompañamiento asistido "
        "('shadowing') presencial durante las horas pico de venta. Finalmente, cada cajero realizará una prueba práctica obligatoria "
        "consistente en registrar 5 ventas consecutivas con diversos métodos de pago y un cierre de turno sin discrepancias, obteniendo "
        "así su acreditación formal para operar en el sistema productivo de TiendaGo."
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECCIÓN 5: GESTIÓN DE RIESGOS, ROLLBACK Y CALIDAD
    # -------------------------------------------------------------------------
    add_heading_styled(doc, "5. Plan de Contingencia, Rollback y Garantía de Calidad", level=1)
    
    add_heading_styled(doc, "5.1 Matriz de Riesgos y Mitigación", level=2)
    add_body_paragraph(
        doc,
        "Para anticipar y neutralizar posibles incidentes que puedan suscitarse durante el despliegue del sistema, se ha formulado "
        "la siguiente matriz de riesgos técnicos y operacionales con sus respectivas acciones de mitigación:"
    )

    risks = [
        ("R1", "Falla de conectividad a Internet en mostrador", "Media", "Alta", "Las terminales POS cuentan con datos móviles 4G/LTE de respaldo y almacenamiento temporal en caché SQLite para evitar interrupciones de venta."),
        ("R2", "Incompatibilidad de driver con impresora térmica", "Baja", "Media", "Homologación previa de impresoras estándar ESC/POS y disponibilidad de impresora térmica de repuesto conectable por cable USB."),
        ("R3", "Error en ejecución de migraciones EF Core en Supabase", "Baja", "Crítica", "Generación obligatoria de un snapshot de base de datos previo al despliegue y validación idéntica en ambiente de Staging."),
        ("R4", "Descuadre en corte de caja por error humano del cajero", "Media", "Media", "Acompañamiento presencial durante la primera semana y revisión de logs de auditoría en la tabla Ventas para conciliación."),
        ("R5", "Expiración inesperada de claves o tokens JWT", "Baja", "Alta", "Configuración centralizada de expiración a 8 horas con mecanismo de refresco automático documentado en appsettings.json.")
    ]

    r_table = doc.add_table(rows=len(risks) + 1, cols=5)
    r_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(r_table, color="D0D7DE")
    r_widths = [Inches(0.6), Inches(2.1), Inches(0.8), Inches(0.8), Inches(2.2)]
    format_table_headers(r_table, ["ID", "Riesgo Identificado", "Probab.", "Impacto", "Estrategia Preventiva y de Mitigación"], r_widths)
    format_table_data(r_table, risks, r_widths, [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])
    prevent_row_split(r_table)
    repeat_header_row(r_table)

    add_heading_styled(doc, "5.2 Procedimiento de Reversión (Rollback) Paso a Paso", level=2)
    add_body_paragraph(
        doc,
        "En caso de detectarse una anomalía crítica insalvable durante los primeros 45 minutos del despliegue en producción que afecte "
        "la integridad de las transacciones o impida la operación comercial, se activará de inmediato el siguiente protocolo de Rollback:"
    )
    add_bullet_item(doc, "El Líder de Proyecto (Gerardo Batres) declara formalmente el estado de reversión y notifica al personal de tienda suspender temporalmente el uso de la app.", bold_prefix="Paso 1 (Declaración de Reversión): ")
    add_bullet_item(doc, "Detención inmediata del servicio Kestrel en el host del backend mediante comando de servicio (systemctl stop tiendago-api o docker stop tiendago-core).", bold_prefix="Paso 2 (Detención de Servicios): ")
    add_bullet_item(doc, "Restauración inmediata del snapshot de base de datos generado en Supabase Cloud previo al inicio de la migración de versión.", bold_prefix="Paso 3 (Restauración de Base de Datos): ")
    add_bullet_item(doc, "Reemplazo de los binarios del Web API por los ejecutables de la versión estable anterior almacenada en el repositorio de respaldo seguro (/releases/stable_backup/).", bold_prefix="Paso 4 (Reversión de Binarios Backend): ")
    add_bullet_item(doc, "Reinstalación o reversión de versión del paquete APK en las terminales móviles Android de los cajeros.", bold_prefix="Paso 5 (Reversión de Terminales Móviles): ")
    add_bullet_item(doc, "Reinicio del servicio Kestrel, ejecución de pruebas de humo y reanudación controlada de operaciones bajo la versión previa estable.", bold_prefix="Paso 6 (Verificación y Reactivación): ")

    add_heading_styled(doc, "5.3 Pruebas de Humo (Smoke Testing) y Acta de Aceptación (Sign-off)", level=2)
    add_body_paragraph(
        doc,
        "Inmediatamente concluido el despliegue físico y lógico, el equipo ejecuta una batería de pruebas de humo de 10 puntos de control "
        "críticos para certificar que el sistema está 100% apto para operar:"
    )

    smoke_tests = [
        ("ST-01", "Verificación de salud del backend", "GET /swagger/v1/swagger.json", "HTTP 200 OK y esquema OpenAPI cargado"),
        ("ST-02", "Autenticación de Administrador", "POST /api/auth/login (Admin)", "HTTP 200 OK con Bearer JWT y Claims RBAC"),
        ("ST-03", "Rechazo de credenciales inválidas", "POST /api/auth/login (Erróneo)", "HTTP 401 Unauthorized sin fuga de datos"),
        ("ST-04", "Consulta de catálogo de productos", "GET /api/productos", "HTTP 200 OK con lista de productos y stock"),
        ("ST-05", "Apertura de turno de caja", "POST /api/turnos/abrir (Monto $50)", "HTTP 200 OK y turno registrado en estado Abierto"),
        ("ST-06", "Transacción de venta con IVA 13%", "POST /api/ventas (Efectivo)", "HTTP 200 OK, IVA exacto, vuelto y descuento de stock"),
        ("ST-07", "Prevención de venta sin existencias", "POST /api/ventas (Stock insuficiente)", "HTTP 400 Bad Request y rollback transaccional"),
        ("ST-08", "Enlace e impresión térmica Bluetooth", "Envío de bytes ESC/POS al dispositivo", "Impresión nítida de ticket físico en menos de 3 seg"),
        ("ST-09", "Cierre y arqueo de turno de caja", "POST /api/turnos/cerrar", "HTTP 200 OK, arqueo cuadrado y balance guardado"),
        ("ST-10", "Acceso denegado a rutas de Admin", "GET /api/usuarios desde rol Cajero", "HTTP 403 Forbidden certificando RBAC estricto")
    ]

    st_table = doc.add_table(rows=len(smoke_tests) + 1, cols=4)
    st_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(st_table, color="D0D7DE")
    st_widths = [Inches(0.8), Inches(2.2), Inches(1.8), Inches(1.7)]
    format_table_headers(st_table, ["Código", "Punto de Verificación", "Invocación / Operación", "Resultado Esperado de Conformidad"], st_widths)
    format_table_data(st_table, smoke_tests, st_widths)
    prevent_row_split(st_table)
    repeat_header_row(st_table)

    add_body_paragraph(
        doc,
        "Habiendo superado de forma unánime y conforme los 10 puntos de control de las pruebas de humo, se procede al acto formal "
        "de entrega, recepción y pase definitivo a producción mediante las firmas de los representantes institucionales y técnicos:"
    )

    # Tabla de Firmas de Conformidad
    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sig_table, color="CCCCCC")
    sig_widths = [Inches(3.2), Inches(3.2)]
    
    signatures = [
        ("________________________________________\nGerardo Antonio Batres Moreno\nLíder de Proyecto & Arquitecto de Software\nGrupo N° 06 — ESFE AGAPE",
         "________________________________________\nLic. Gerber Alexis Gómez Hidalgo\nDocente Evaluador de Proyecto\nESFE – AGAPE"),
        ("________________________________________\nElmer Antonio Tesorero Hernández\nIngeniero Backend & Administrador de BD\nGrupo N° 06 — ESFE AGAPE",
         "________________________________________\nRepresentante / Administrador Comercial\nEstablecimiento Comercial TiendaGo\nFirma y Sello de Recepción Conforme")
    ]
    
    for r_idx, (sig1, sig2) in enumerate(signatures):
        row = sig_table.rows[r_idx]
        for c_idx, sig_text in enumerate([sig1, sig2]):
            cell = row.cells[c_idx]
            cell.width = sig_widths[c_idx]
            set_cell_background(cell, "FBFCFD")
            set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(sig_text)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.color.rgb = COLOR_BODY

    # Guardado del archivo DOCX
    doc.save(OUTPUT_DOCX)
    print(f"Documento generado exitosamente en: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_implementation_plan()
