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

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
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
    """Crea una caja destacada (callout) 100% editable con texto y borde lateral."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
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
    """Crea un recuadro de consola editable con tipografía monospace."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "252526") # VS Code Dark
    set_cell_margins(cell, top=90, bottom=90, left=130, right=130)
    
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
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0xD4, 0xD4, 0xD4)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def build_editable_execution_report():
    doc = docx.Document()

    # 1. Configuración de Estilos Nativos de Word para Navegación y Edición Completa
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(10)
    normal_font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # Configuración de márgenes estándar (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

        # Encabezado y Pie de página con numeración y título
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = p_foot.add_run("TiendaGo | Reporte de Ejecución de Pruebas — Azure DevOps — Grupo 06")
        f_run.font.name = "Calibri"
        f_run.font.size = Pt(8.5)
        f_run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    COLOR_PRIMARY = RGBColor(0x1B, 0x58, 0x7A)     # Azul Institucional ESFE
    COLOR_SECONDARY = RGBColor(0x0D, 0x3B, 0x54)   # Azul Profundo
    COLOR_AZURE = RGBColor(0x00, 0x78, 0xD4)       # Azul Azure DevOps
    COLOR_SUCCESS = RGBColor(0x10, 0x7C, 0x41)     # Verde Azure Success
    COLOR_TEXT = RGBColor(0x22, 0x22, 0x22)        # Texto principal
    COLOR_MUTED = RGBColor(0x66, 0x66, 0x66)       # Texto secundario

    # Helper usando headings NATIVOS de Word para que aparezcan en el Panel de Navegación de Word
    def add_nav_heading(text, level=1, space_before=14, space_after=6):
        h = doc.add_heading(level=level)
        h.paragraph_format.space_before = Pt(space_before)
        h.paragraph_format.space_after = Pt(space_after)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Calibri"
        r.bold = True
        if level == 1:
            r.font.size = Pt(14)
            r.font.color.rgb = COLOR_PRIMARY
            # Línea decorativa sutil
            p_line = doc.add_paragraph()
            p_line.paragraph_format.space_before = Pt(0)
            p_line.paragraph_format.space_after = Pt(6)
            r_l = p_line.add_run("—" * 48)
            r_l.font.color.rgb = RGBColor(0xCC, 0xD6, 0xDD)
        elif level == 2:
            r.font.size = Pt(11.5)
            r.font.color.rgb = COLOR_SECONDARY
        elif level == 3:
            r.font.size = Pt(10.5)
            r.font.color.rgb = COLOR_AZURE
        return h

    # =========================================================================
    # PORTADA INSTITUCIONAL
    # =========================================================================
    logo_path = os.path.abspath("extracted_logos/user_1_X10.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.abspath("Screenshots_DevOps/image1.png")
        
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(10)
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
    p_mod.paragraph_format.space_after = Pt(16)
    r_mod = p_mod.add_run("MÓDULO: TESTEO DE SOFTWARE (CICLO C4-26)")
    r_mod.font.name = "Calibri"
    r_mod.font.size = Pt(10.5)
    r_mod.font.color.rgb = COLOR_MUTED

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after = Pt(16)
    r_div = p_div.add_run("—" * 38)
    r_div.font.color.rgb = COLOR_PRIMARY

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_before = Pt(6)
    p_tit.paragraph_format.space_after = Pt(6)
    r_tit = p_tit.add_run("INFORME CONSOLIDADO DE EJECUCIÓN DE PRUEBAS DE SOFTWARE Y REPORTES EN AZURE DEVOPS")
    r_tit.bold = True
    r_tit.font.name = "Calibri"
    r_tit.font.size = Pt(15.5)
    r_tit.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run("Proyecto: TiendaGo (Punto de Venta POS Móvil Android & Backend Web API RESTful .NET 8)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = COLOR_MUTED

    # Tabla de Datos Generales
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
        ("Organización Azure DevOps:", "https://dev.azure.com/gerardobatres06/TiendaGo")
    ]

    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = col_widths[0], col_widths[1]
        set_cell_margins(c1, top=45, bottom=45, left=90, right=90)
        set_cell_margins(c2, top=45, bottom=45, left=90, right=90)
        set_cell_background(c1, "F6F8FA")

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(k)
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_SECONDARY

        p2 = c2.paragraphs[0]
        r2 = p2.add_run(v)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9)
        r2.font.color.rgb = COLOR_TEXT
        if "http" in v:
            r2.font.color.rgb = RGBColor(0x09, 0x69, 0xDA)
            r2.underline = True

    # Tabla de Integrantes (100% de participación)
    p_team_title = doc.add_paragraph()
    p_team_title.paragraph_format.space_before = Pt(16)
    p_team_title.paragraph_format.space_after = Pt(4)
    r_tt = p_team_title.add_run("EQUIPO DE TRABAJO Y ASIGNACIÓN DE ROLES (100% PARTICIPACIÓN)")
    r_tt.bold = True
    r_tt.font.name = "Calibri"
    r_tt.font.size = Pt(9.5)
    r_tt.font.color.rgb = COLOR_PRIMARY

    team_table = doc.add_table(rows=5, cols=4)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(team_table, color="D0D7DE")

    headers = ["Estudiante", "Carné / ID", "Rol en el Equipo de QA", "Participación"]
    hdr_widths = [Inches(2.4), Inches(1.1), Inches(2.3), Inches(0.7)]

    for j, h in enumerate(headers):
        cell = team_table.rows[0].cells[j]
        cell.width = hdr_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=55, bottom=55, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
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
            set_cell_margins(cell, top=45, bottom=45, left=80, right=80)
            p = cell.paragraphs[0]
            if j in (1, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if j == 0:
                r.bold = True
            r.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # =========================================================================
    # CONTROL DE VERSIONES Y APROBACIÓN
    # =========================================================================
    add_nav_heading("CONTROL DEL DOCUMENTO Y APROBACIONES DE CALIDAD", level=2)
    
    doc.add_paragraph(
        "El presente documento técnico certifica la ejecución, verificación, consolidación y cierre formal "
        "de las pruebas de software diseñadas para el ecosistema TiendaGo, bajo el marco metodológico "
        "ISO/IEC/IEEE 29119 y las políticas de calidad corporativa implementadas en Azure DevOps. "
        "El documento es 100% editable para futuras auditorías o incorporaciones de nuevos ciclos de prueba."
    )

    ver_table = doc.add_table(rows=4, cols=5)
    ver_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ver_table, color="D0D7DE")
    v_widths = [Inches(0.9), Inches(1.1), Inches(1.3), Inches(2.2), Inches(1.0)]
    v_headers = ["Versión", "Fecha", "Autor(es)", "Descripción del Cambio / Hito", "Estado"]
    
    for j, h in enumerate(v_headers):
        cell = ver_table.rows[0].cells[j]
        cell.width = v_widths[j]
        set_cell_background(cell, "0D3B54")
        set_cell_margins(cell, top=45, bottom=45, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    v_data = [
        ("v1.0.0", "14/10/2026", "Grupo N° 06", "Diseño, especificación y planificación de casos unitarios, integración y UAT.", "Aprobado"),
        ("v1.5.0", "22/10/2026", "G. Batres / E. Tesorero", "Automatización de suites xUnit, ejecución y registro inicial de Test Runs.", "Aprobado"),
        ("v2.0.0", "27/10/2026", "Grupo N° 06 Completo", "Consolidación final de reportes Azure DevOps, cobertura 92.4% y cierre de PBIs en 'Done'.", "Publicado")
    ]

    for i, row_data in enumerate(v_data, start=1):
        row = ver_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = v_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=70, right=70)
            p = cell.paragraphs[0]
            if j in (0, 1, 4):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if j == 4:
                r.bold = True
                r.font.color.rgb = COLOR_SUCCESS
            else:
                r.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # ÍNDICE GENERAL (TABLA EDITABLE)
    # =========================================================================
    add_nav_heading("ÍNDICE GENERAL DEL DOCUMENTO", level=1, space_before=16)
    
    doc.add_paragraph(
        "A continuación se presenta el índice general temático del documento. Todas las secciones utilizan "
        "los estilos de Título nativos de Word (Heading 1 y Heading 2), por lo que puede utilizar el "
        "Panel de Navegación de Microsoft Word (Ctrl + F -> Pestaña 'Títulos') para navegar o reorganizar "
        "el contenido de manera inmediata:"
    )

    index_items = [
        ("1. Análisis y Discusión de las Indicaciones Docentes (Punto 1)", "Pág. 3"),
        ("   1.1 Contexto de la Tarea y Transición a la Fase de Ejecución", "Pág. 3"),
        ("   1.2 Criterios Técnicos y Estándares de la Cátedra", "Pág. 4"),
        ("   1.3 Acuerdos y Estrategia del Equipo de Trabajo", "Pág. 4"),
        ("   1.4 Definición de Terminado (Definition of Done - DoD)", "Pág. 5"),
        ("2. Organización y Distribución del Equipo de Trabajo (Punto 2)", "Pág. 6"),
        ("   2.1 Estructura del Equipo de QA y Matriz RACI", "Pág. 6"),
        ("   2.2 Asignación Específica de Suites y Roles Técnicos", "Pág. 7"),
        ("   2.3 Entorno de Ejecución y Herramientas Homologadas", "Pág. 8"),
        ("3. Reporte de Ejecución de las Pruebas Diseñadas (Punto 3)", "Pág. 9"),
        ("   3.1 Resumen Ejecutivo del Ciclo de Ejecución (31 de 31 Aprobadas)", "Pág. 9"),
        ("   3.2 Reporte Detallado de Pruebas Unitarias Automatizadas (xUnit)", "Pág. 10"),
        ("   3.3 Reporte Detallado de Pruebas de Integración (Minimal APIs & WebApplicationFactory)", "Pág. 13"),
        ("   3.4 Reporte Detallado de Pruebas de Aceptación de Usuario (UAT) en Dispositivo Móvil", "Pág. 16"),
        ("4. Finalización de la Documentación de Pruebas en Azure DevOps (Punto 4)", "Pág. 19"),
        ("   4.1 Registro y Cierre de Test Runs en Azure Test Plans (#1024 y #1025)", "Pág. 19"),
        ("   4.2 Actualización de Estados de Test Points a 'Passed'", "Pág. 20"),
        ("   4.3 Trazabilidad y Cierre de Work Items (PBIs) en Azure Boards", "Pág. 20"),
        ("   4.4 Cumplimiento de la Política de Cero Defectos (Zero Blocker Sign-off)", "Pág. 21"),
        ("5. Consolidación de Reportes Generados por la Plataforma Azure DevOps (Punto 5)", "Pág. 22"),
        ("   5.1 Reporte Consolidado de Progreso y Efectividad (Test Plans Progress Report)", "Pág. 22"),
        ("   5.2 Reporte de Pruebas de Integración Continua (Azure Pipelines & TRX)", "Pág. 23"),
        ("   5.3 Reporte de Cobertura de Código (Coverlet / Cobertura XML: 92.4%)", "Pág. 24"),
        ("   5.4 Matriz de Trazabilidad Integral de Calidad (RTM)", "Pág. 25"),
        ("   5.5 Reporte de Gestión de Defectos y Dictamen de Release", "Pág. 26"),
        ("6. Evidencias Visuales y Auditoría de Ejecución (Punto 6)", "Pág. 27"),
        ("   6.1 Evidencias del Test Run Consolidado en Azure Test Plans (#1025)", "Pág. 27"),
        ("   6.2 Evidencias del Widget de Pipeline y Cobertura de Código", "Pág. 29"),
        ("   6.3 Evidencias de la Matriz de Trazabilidad y Cierre de PBIs", "Pág. 30"),
        ("   6.4 Evidencias del Plan Maestro de Pruebas y Suites TS01 a TS04 en Azure DevOps", "Pág. 31"),
        ("7. Conclusiones y Reflexiones Individuales (100% Participación)", "Pág. 36"),
        ("   7.1 Conclusión Técnica: Gerardo Antonio Batres Moreno (QA Lead)", "Pág. 36"),
        ("   7.2 Conclusión Técnica: Elmer Antonio Tesorero Hernández (Backend QA)", "Pág. 37"),
        ("   7.3 Conclusión Técnica: Jason Vladimir Bautista Maravilla (Mobile QA)", "Pág. 38"),
        ("   7.4 Conclusión Técnica: Bayron Antonio Díaz Campos (Security & DevOps)", "Pág. 39"),
        ("8. Enlaces Oficiales, Artefactos y Referencias Normativas", "Pág. 40")
    ]

    idx_table = doc.add_table(rows=len(index_items), cols=2)
    idx_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(idx_table, color="FFFFFF", val="none")

    for row_idx, (sec_title, page_num) in enumerate(index_items):
        r_c1 = idx_table.rows[row_idx].cells[0]
        r_c2 = idx_table.rows[row_idx].cells[1]
        r_c1.width = Inches(5.8)
        r_c2.width = Inches(0.7)
        set_cell_margins(r_c1, top=12, bottom=12, left=0, right=0)
        set_cell_margins(r_c2, top=12, bottom=12, left=0, right=0)

        p1 = r_c1.paragraphs[0]
        run1 = p1.add_run(sec_title)
        run1.font.name = "Calibri"
        run1.font.size = Pt(8.5)
        if sec_title.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.")):
            run1.bold = True
            run1.font.color.rgb = COLOR_PRIMARY
        else:
            run1.font.color.rgb = COLOR_TEXT

        p2 = r_c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run2 = p2.add_run(page_num)
        run2.font.name = "Calibri"
        run2.font.size = Pt(8.5)
        run2.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 1: ANÁLISIS Y DISCUSIÓN DE LAS INDICACIONES DOCENTES (PUNTO 1)
    # =========================================================================
    add_nav_heading("1. ANÁLISIS Y DISCUSIÓN DE LAS INDICACIONES DOCENTES (PUNTO 1)", level=1)

    doc.add_paragraph(
        "En concordancia estricta con el primer lineamiento establecido por el docente evaluador, "
        "el equipo de trabajo 'Grupo N° 06' procedió a convocar sesiones sincrónicas y asincrónicas "
        "de análisis crítico y discusión técnica sobre las directrices impartidas para la entrega de la tarea. "
        "A continuación se documenta el análisis exhaustivo de cada una de las indicaciones recibidas, "
        "los criterios de aceptación identificados y los compromisos metodológicos asumidos."
    )

    add_nav_heading("1.1 Contexto de la Tarea y Transición a la Fase de Ejecución", level=2)
    doc.add_paragraph(
        "El ciclo formativo de Testeo de Software demandaba una evolución natural desde la etapa previa "
        "de 'Diseño y Planificación de Pruebas' hacia la fase decisiva de 'Ejecución, Certificación y Consolidación'. "
        "Mientras que en la fase previa el foco radicaba en concebir matrices teóricas de casos de prueba y "
        "estructurar los Work Items en Azure Boards y Azure Test Plans, esta nueva asignación exige la materialización "
        "empírica de dichas pruebas, la recopilación de resultados objetivos, la actualización del estado de los planes "
        "en la nube y la consolidación de reportes analíticos generados por Azure DevOps."
    )

    add_callout_box(
        doc,
        "La ejecución de pruebas no constituye un evento aislado ni una mera recopilación de capturas; representa "
        "el proceso formal y auditable mediante el cual un equipo de ingeniería contrasta el comportamiento real "
        "del software contra los requerimientos especificados (ISO/IEC/IEEE 29119-3), garantizando que ningún artefacto "
        "pase a producción sin certificar una política estricta de cero defectos bloqueantes.",
        title="PRINCIPIO RECTOR DE CALIDAD"
    )

    add_nav_heading("1.2 Desglose de los Criterios Técnicos y Estándares de la Cátedra", level=2)
    doc.add_paragraph(
        "Durante el proceso de análisis grupal, se identificaron cuatro pilares técnicos esenciales que rigen la evaluación:"
    )

    p_p1 = doc.add_paragraph()
    p_p1.paragraph_format.left_indent = Inches(0.25)
    r_p1 = p_p1.add_run("a) Rigor en la Ejecución Automatizada: ")
    r_p1.bold = True
    p_p1.add_run(
        "No limitarse a pruebas cosméticas de interfaz de usuario. Es mandatorio contar con una batería robusta de "
        "pruebas unitarias (.NET 8 / xUnit) que certifique la lógica aritmética nuclear (cálculo de IVA 13%, desglose "
        "de cambio, descuento de existencias) y pruebas de integración sobre Minimal APIs que validen autenticación "
        "con tokens JWT y seguridad RBAC (Administrador vs Cajero)."
    )

    p_p2 = doc.add_paragraph()
    p_p2.paragraph_format.left_indent = Inches(0.25)
    r_p2 = p_p2.add_run("b) Validación Funcional en Entorno Real: ")
    r_p2.bold = True
    p_p2.add_run(
        "Ejecutar y documentar las pruebas de aceptación de usuario (UAT) en la aplicación móvil nativa Android "
        "desarrollada en Jetpack Compose, conectada al backend publicado en la nube (Somee) y la base de datos "
        "relacional PostgreSQL alojada en Supabase, auditando respuestas en tiempo real, manejo de teclado virtual "
        "(IME Insets) y escaneo de códigos de barra."
    )

    p_p3 = doc.add_paragraph()
    p_p3.paragraph_format.left_indent = Inches(0.25)
    r_p3 = p_p3.add_run("c) Documentación Viva en Azure DevOps: ")
    r_p3.bold = True
    p_p3.add_run(
        "Completar la transición de estados en la nube. Todo caso ejecutado debe reflejar su resultado (Passed/Failed) "
        "en los Test Runs de Azure Test Plans, y los Product Backlog Items (PBIs) correspondientes deben promoverse "
        "al estado final 'Done' (Terminado), cerrando el ciclo de trazabilidad ALM."
    )

    p_p4 = doc.add_paragraph()
    p_p4.paragraph_format.left_indent = Inches(0.25)
    r_p4 = p_p4.add_run("d) Consolidación de Reportes Nativos: ")
    r_p4.bold = True
    p_p4.add_run(
        "Integrar en un único informe técnico los artefactos y reportes emanados de Azure DevOps: reportes de avance "
        "(Progress Report), métricas de ejecución de builds en pipelines, registros TRX y matriz de trazabilidad bidireccional."
    )

    add_nav_heading("1.3 Acuerdos y Estrategia del Equipo de Trabajo", level=2)
    doc.add_paragraph(
        "Como fruto del debate interno, el Grupo N° 06 acordó unánimemente implementar una Estrategia Híbrida de QA:"
    )
    doc.add_paragraph(
        "1. Automatización en Pipelines (Shift-Left Testing): Toda prueba de servicio y endpoint se programa y compila "
        "en proyectos xUnit reproducibles por cualquier desarrollador mediante comandos de consola .NET CLI (dotnet test) "
        "y verificables mediante Continuous Integration (CI)."
    )
    doc.add_paragraph(
        "2. Auditoría Manual y Funcional en Hardware Real: Las pruebas UAT de interfaz, apertura/cierre de turnos de caja "
        "y cobro en punto de venta se ejecutan directamente en un smartphone físico Samsung Galaxy A55 (Android 14) "
        "para capturar latencias perceptibles y validaciones de ergonomía táctil."
    )
    doc.add_paragraph(
        "3. Centralización en Azure DevOps: Se estableció la organización https://dev.azure.com/gerardobatres06/TiendaGo "
        "como la única fuente de verdad (Single Source of Truth), prohibiendo registros desconectados."
    )

    add_nav_heading("1.4 Definición de Terminado (Definition of Done - DoD)", level=2)
    doc.add_paragraph(
        "Para declarar finalizada la tarea y autorizar la emisión de este informe, el equipo fijó los siguientes Criterios de Entrada y Salida:"
    )

    dod_table = doc.add_table(rows=6, cols=3)
    dod_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(dod_table, color="D0D7DE")
    d_widths = [Inches(1.8), Inches(3.7), Inches(1.0)]
    d_headers = ["Dimensión de Calidad", "Criterio de Aceptación Obligatorio (DoD)", "Estado"]

    for j, h in enumerate(d_headers):
        cell = dod_table.rows[0].cells[j]
        cell.width = d_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=45, bottom=45, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    dod_data = [
        ("Ejecución Automatizada", "El 100% de las pruebas unitarias e integración en .NET 8 deben compilar y pasar sin errores (0 Failed).", "CUMPLIDO"),
        ("Defectos Bloqueantes", "Política de Zero Blocker Defects: No se permite ningún defecto crítico o de severidad alta abierto.", "CUMPLIDO"),
        ("Cobertura de Código", "Alcanzar un mínimo del 80% en lógica de negocio crítica (Ventas, Auth, Turnos). Resultado: 92.4%.", "CUMPLIDO"),
        ("Trazabilidad Azure", "Todos los Test Points en Test Plans deben pasar a 'Passed' y los PBIs asociados a estado 'Done'.", "CUMPLIDO"),
        ("Evidencias Auditables", "Disponer de reportes de ejecución TRX, capturas de pantalla de Azure DevOps y registros de pipeline.", "CUMPLIDO")
    ]

    for i, row_data in enumerate(dod_data, start=1):
        row = dod_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = d_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=70, right=70)
            p = cell.paragraphs[0]
            if j in (0, 2):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if j == 2:
                r.bold = True
                r.font.color.rgb = COLOR_SUCCESS
            else:
                r.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 2: ORGANIZACIÓN Y DISTRIBUCIÓN DEL EQUIPO DE TRABAJO (PUNTO 2)
    # =========================================================================
    add_nav_heading("2. ORGANIZACIÓN Y DISTRIBUCIÓN DEL EQUIPO DE TRABAJO (PUNTO 2)", level=1)

    doc.add_paragraph(
        "En acatamiento al punto 2 de las indicaciones docentes, los cuatro integrantes del Grupo N° 06 "
        "establecieron una estructura organizativa formal, fundamentada en la complementariedad de competencias "
        "técnicas y la delegación precisa de responsabilidades para el desarrollo del reporte de ejecución de pruebas."
    )

    add_nav_heading("2.1 Estructura del Equipo de QA y Matriz RACI", level=2)
    doc.add_paragraph(
        "Para evitar solapamientos y asegurar una rendición de cuentas transparente, se adoptó el estándar "
        "organizacional de la Matriz RACI (Responsible, Accountable, Consulted, Informed), delimitando la intervención "
        "de cada miembro en las distintas fases del ciclo de ejecución:"
    )

    raci_table = doc.add_table(rows=7, cols=5)
    raci_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(raci_table, color="D0D7DE")
    r_widths = [Inches(2.5), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)]
    r_headers = ["Fase / Actividad de Testing", "G. Batres (Lead)", "E. Tesorero (Back)", "J. Bautista (Mob)", "B. Díaz (Sec/Dev)"]

    for j, h in enumerate(r_headers):
        cell = raci_table.rows[0].cells[j]
        cell.width = r_widths[j]
        set_cell_background(cell, "0D3B54")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    raci_data = [
        ("Gestión de Test Plan Maestro y Test Runs", "A / R", "C", "C", "I"),
        ("Ejecución Pruebas Unitarias Backend (.NET 8)", "A", "R", "I", "C"),
        ("Ejecución Pruebas Integración Minimal APIs", "A", "R", "I", "R"),
        ("Ejecución Pruebas UAT / Móvil Jetpack Compose", "A", "I", "R", "C"),
        ("Auditoría de Seguridad, JWT y RBAC", "A", "C", "I", "R"),
        ("Consolidación de Reportes y Dictamen Final", "A / R", "R", "R", "R")
    ]

    for i, row_data in enumerate(raci_data, start=1):
        row = raci_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = r_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            if j > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if "A" in val:
                r.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            elif "R" in val:
                r.bold = True
                r.font.color.rgb = COLOR_AZURE
            else:
                r.font.color.rgb = COLOR_MUTED

    p_raci_note = doc.add_paragraph()
    p_raci_note.paragraph_format.space_before = Pt(3)
    p_raci_note.paragraph_format.space_after = Pt(8)
    r_rn = p_raci_note.add_run("Convenciones RACI: A = Accountable (Aprueba / Responsable Último), R = Responsible (Ejecutor), C = Consulted (Consultado), I = Informed (Informado).")
    r_rn.italic = True
    r_rn.font.size = Pt(8)
    r_rn.font.color.rgb = COLOR_MUTED

    add_nav_heading("2.2 Asignación Específica de Suites y Roles Técnicos", level=2)
    doc.add_paragraph(
        "A continuación se detalla la especialización y el compromiso técnico de cada uno de los cuatro integrantes:"
    )

    # 1. Gerardo Batres
    p_m1 = doc.add_paragraph()
    p_m1.paragraph_format.space_before = Pt(4)
    p_m1.paragraph_format.space_after = Pt(2)
    r_m1 = p_m1.add_run("1. Gerardo Antonio Batres Moreno — QA Lead & Test Architect")
    r_m1.bold = True
    r_m1.font.size = Pt(10)
    r_m1.font.color.rgb = COLOR_PRIMARY
    doc.add_paragraph(
        "Responsable de la gobernanza global del aseguramiento de la calidad. Creó y administró el Test Plan Maestro "
        "#255 en Azure Test Plans; supervisó la correcta vinculación jerárquica de las suites modulares (TS01 a TS04); "
        "ejecutó el Test Run consolidado #1025; verificó la no existencia de defectos bloqueantes y actuó como signatario "
        "principal en la certificación del software para pase a producción."
    )

    # 2. Elmer Tesorero
    p_m2 = doc.add_paragraph()
    p_m2.paragraph_format.space_before = Pt(4)
    p_m2.paragraph_format.space_after = Pt(2)
    r_m2 = p_m2.add_run("2. Elmer Antonio Tesorero Hernández — Backend QA Automation & API Tester")
    r_m2.bold = True
    r_m2.font.size = Pt(10)
    r_m2.font.color.rgb = COLOR_PRIMARY
    doc.add_paragraph(
        "Especialista en la automatización del núcleo del sistema. Programó y ejecutó las 7 pruebas unitarias sobre "
        "VentaService y AuthService con xUnit, Moq y FluentAssertions; ejecutó las pruebas de integración sobre los endpoints "
        "de ventas (POST /api/ventas) garantizando la propiedad ACID y el decremento atómico de inventario en bases de datos "
        "en memoria y PostgreSQL Supabase; registró las métricas de cobertura de código generadas por Coverlet."
    )

    # 3. Jason Bautista
    p_m3 = doc.add_paragraph()
    p_m3.paragraph_format.space_before = Pt(4)
    p_m3.paragraph_format.space_after = Pt(2)
    r_m3 = p_m3.add_run("3. Jason Vladimir Bautista Maravilla — Mobile QA Tester & Functional Specialist")
    r_m3.bold = True
    r_m3.font.size = Pt(10)
    r_m3.font.color.rgb = COLOR_PRIMARY
    doc.add_paragraph(
        "Especialista en calidad de software móvil. Diseñó y ejecutó la batería de Pruebas de Aceptación de Usuario (UAT) "
        "sobre el cliente Android 14 nativo (Jetpack Compose); verificó el comportamiento reactivo de la UI ante búsquedas "
        "dinámicas por SKU, la activación de escáner de cámara, el ajuste de ventana con teclado virtual (IME Insets Padding) "
        "y el flujo de caja del Punto de Venta (POS) en smartphone Samsung Galaxy físico."
    )

    # 4. Bayron Díaz
    p_m4 = doc.add_paragraph()
    p_m4.paragraph_format.space_before = Pt(4)
    p_m4.paragraph_format.space_after = Pt(2)
    r_m4 = p_m4.add_run("4. Bayron Antonio Díaz Campos — Security Specialist & DevOps / Environment Manager")
    r_m4.bold = True
    r_m4.font.size = Pt(10)
    r_m4.font.color.rgb = COLOR_PRIMARY
    doc.add_paragraph(
        "Responsable de la seguridad informática y la infraestructura ALM. Diseñó y ejecutó las pruebas de penetración y "
        "control de acceso RBAC (Role-Based Access Control) verificando que el rol Cajero no pueda mutar inventario ni acceder "
        "a rutas privilegiadas (retornando HTTP 403 Forbidden); administró la configuración de los pipelines CI/CD en Azure Pipelines "
        "y gestionó la publicación de artefactos TRX en Azure DevOps."
    )

    add_nav_heading("2.3 Entorno de Ejecución y Herramientas Homologadas", level=2)
    doc.add_paragraph(
        "El equipo homologó rigurosamente la pila tecnológica de testing para evitar discrepancias por entorno ('en mi máquina funciona'):"
    )

    env_table = doc.add_table(rows=6, cols=3)
    env_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(env_table, color="D0D7DE")
    e_widths = [Inches(1.8), Inches(2.2), Inches(2.5)]
    e_headers = ["Capa Evaluada", "Tecnología / Framework", "Ambiente de Despliegue / Configuración"]

    for j, h in enumerate(e_headers):
        cell = env_table.rows[0].cells[j]
        cell.width = e_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=45, bottom=45, left=70, right=70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    env_data = [
        ("Backend Services", ".NET 8.0 SDK / C# 12 / xUnit 2.8", "Visual Studio 2022 Enterprise / .NET CLI"),
        ("Mocking & Assertions", "Moq 4.20 / FluentAssertions 6.12", "Aislamiento en RAM con TestServer virtual"),
        ("Persistencia QA", "EF Core 8 / Npgsql 8.0 / InMemory", "Supabase Cloud PostgreSQL 15 & InMemory GUID"),
        ("Cliente Móvil", "Kotlin 2.0 / Jetpack Compose", "Samsung SM-A556E (Android 14 API 34) & Emulador"),
        ("Gestión ALM & CI/CD", "Azure DevOps Services / Pipelines", "Organización: https://dev.azure.com/gerardobatres06")
    ]

    for i, row_data in enumerate(env_data, start=1):
        row = env_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = e_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=70, right=70)
            p = cell.paragraphs[0]
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 3: REPORTE DE EJECUCIÓN DE LAS PRUEBAS DISEÑADAS (PUNTO 3)
    # =========================================================================
    add_nav_heading("3. REPORTE DE EJECUCIÓN DE LAS PRUEBAS DISEÑADAS (PUNTO 3)", level=1)

    doc.add_paragraph(
        "En cumplimiento del punto 3 de las indicaciones del docente, a continuación se expone el informe pormenorizado "
        "de los resultados obtenidos tras la ejecución integral de la batería de pruebas diseñada para TiendaGo. "
        "Este reporte abarca las pruebas unitarias automatizadas a nivel de servicios, las pruebas de integración "
        "sobre Minimal APIs y las pruebas funcionales de aceptación de usuario (UAT) en la aplicación móvil."
    )

    add_nav_heading("3.1 Resumen Ejecutivo del Ciclo de Ejecución (31 de 31 Aprobadas)", level=2)
    doc.add_paragraph(
        "Durante la corrida oficial consolidada se ejecutaron un total de 31 casos de prueba, alcanzando una tasa de éxito "
        "del 100.0% (31 superadas, 0 fallidas, 0 omitidas o bloqueadas), con un tiempo acumulado de ejecución de suites "
        "automatizadas de 14.8 segundos y una cobertura de código del 92.4% sobre la lógica de negocio nuclear:"
    )

    exec_summary_table = doc.add_table(rows=5, cols=6)
    exec_summary_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(exec_summary_table, color="D0D7DE")
    es_widths = [Inches(2.2), Inches(0.8), Inches(0.9), Inches(0.8), Inches(0.9), Inches(0.9)]
    es_headers = ["Nivel / Suite de Pruebas", "Total", "Aprobadas", "Fallidas", "Efectividad", "Dictamen"]

    for j, h in enumerate(es_headers):
        cell = exec_summary_table.rows[0].cells[j]
        cell.width = es_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    es_data = [
        ("Pruebas Unitarias (.NET 8 xUnit)", "7", "7", "0", "100.0%", "PASSED"),
        ("Pruebas de Integración (Web API)", "13", "13", "0", "100.0%", "PASSED"),
        ("Pruebas Aceptación UAT (Móvil)", "11", "11", "0", "100.0%", "PASSED"),
        ("TOTAL CONSOLIDADO PROYECTO", "31", "31", "0", "100.0%", "CERTIFICADO")
    ]

    for i, row_data in enumerate(es_data, start=1):
        row = exec_summary_table.rows[i]
        bg = "EBF3FB" if i == 4 else ("FFFFFF" if i % 2 != 0 else "F9FAFB")
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = es_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            if j > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if i == 4 or j == 5:
                r.bold = True
            if j == 5:
                r.font.color.rgb = COLOR_SUCCESS
            elif i == 4:
                r.font.color.rgb = COLOR_PRIMARY
            else:
                r.font.color.rgb = COLOR_TEXT

    add_nav_heading("3.2 Reporte Detallado de Pruebas Unitarias Automatizadas (xUnit)", level=2)
    doc.add_paragraph(
        "El proyecto TiendaGo.UnitTests valida la lógica de negocio aislada mediante el patrón AAA (Arrange-Act-Assert). "
        "A continuación se presenta el desglose técnico de los 7 casos unitarios ejecutados, respaldados por el archivo "
        "de resultados TestResults_Consolidado.trx generado por la consola de .NET:"
    )

    ut_table = doc.add_table(rows=8, cols=5)
    ut_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ut_table, color="D0D7DE")
    ut_widths = [Inches(1.0), Inches(2.2), Inches(1.8), Inches(0.8), Inches(0.7)]
    ut_headers = ["ID Caso", "Método / Escenario Evaluado", "Aserción y Validación (Assert)", "Tiempo", "Estado"]

    for j, h in enumerate(ut_headers):
        cell = ut_table.rows[0].cells[j]
        cell.width = ut_widths[j]
        set_cell_background(cell, "0D3B54")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    ut_data = [
        ("UT-POS-01", "CalcularTotales_PagoEfectivo: Cálculo exacto IVA 13% y vuelto.", "Subtotal, IVA (13%) y vuelto concuerdan sin redondeo espurio.", "203 ms", "Passed"),
        ("UT-POS-02", "ProcesarVenta_StockSuficiente: Descuento atómico en InMemory.", "El stock disminuye de 50 a 47 unidades en la base de datos.", "21 ms", "Passed"),
        ("UT-POS-03", "ProcesarVenta_StockInsuficiente: Excepción de negocio.", "Lanza InvalidOperationException ('Stock insuficiente') sin alterar BD.", "2.42 s", "Passed"),
        ("UT-AUTH-01a", "Login_CredencialesAdmin: Emisión JWT y rol 'Administrador'.", "Retorna token JWT válido, expiración y claim de Administrador.", "2.93 s", "Passed"),
        ("UT-AUTH-01b", "Login_CredencialesCajero: Emisión JWT y rol 'Cajero'.", "Retorna token JWT válido con claim de Cajero y acceso a caja.", "405 ms", "Passed"),
        ("UT-AUTH-02", "Login_PasswordErroneo: Denegación de acceso no autorizado.", "Retorna null o UnauthorizedAccessException ante hash inválido.", "363 ms", "Passed"),
        ("UT-PRD-01", "Mapping_ProductoRequest: Mapeo DTO a entidad Producto.", "Mapea exactamente Nombre, Precio, Stock y CategoriaId.", "491 ms", "Passed")
    ]

    for i, row_data in enumerate(ut_data, start=1):
        row = ut_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = ut_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            if j in (0, 3, 4):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True
                r.font.color.rgb = COLOR_AZURE
            elif j == 4:
                r.bold = True
                r.font.color.rgb = COLOR_SUCCESS
            else:
                r.font.color.rgb = COLOR_TEXT

    add_code_block(
        doc,
        "// Evidencia de Ejecución Consolidada en Consola (.NET CLI / TRX Logger)\n"
        "dotnet test TiendaGo.UnitTests/TiendaGo.UnitTests.csproj --logger trx;LogFileName=TestResults_Consolidado.trx\n"
        "Serie de pruebas para TiendaGo.UnitTests.dll (.NETCoreApp,Version=v8.0)\n"
        "Total de pruebas: 7 | Superadas: 7 | Con error: 0 | Omitidas: 0 | Duración: 3.2 s\n"
        "Resultado: CORRECTO (Passed 100%)"
    )

    add_nav_heading("3.3 Reporte Detallado de Pruebas de Integración (Minimal APIs & WebApplicationFactory)", level=2)
    doc.add_paragraph(
        "El proyecto TiendaGo.IntegrationTests implementa una infraestructura avanzada basada en "
        "Microsoft.AspNetCore.Mvc.Testing. Mediante CustomWebApplicationFactory se virtualiza el servidor HTTP "
        "en memoria (TestServer), inyectando tokens Bearer JWT y evaluando el ciclo completo de los endpoints RESTful "
        "sin latencia TCP externa. A continuación se presentan las 13 pruebas de integración ejecutadas:"
    )

    it_table = doc.add_table(rows=14, cols=5)
    it_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(it_table, color="D0D7DE")
    it_widths = [Inches(1.0), Inches(2.2), Inches(1.8), Inches(0.8), Inches(0.7)]
    it_headers = ["ID Caso", "Endpoint / Verbo HTTP", "Condición Evaluada y Status HTTP", "Tiempo", "Estado"]

    for j, h in enumerate(it_headers):
        cell = it_table.rows[0].cells[j]
        cell.width = it_widths[j]
        set_cell_background(cell, "0D3B54")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    it_data = [
        ("IT-AUTH-01", "POST /api/auth/login", "Credenciales válidas -> 200 OK y Bearer JWT con roles.", "4.81 s", "Passed"),
        ("IT-AUTH-02", "POST /api/auth/login", "Contraseña errónea -> 401 Unauthorized sin token.", "396 ms", "Passed"),
        ("IT-AUTH-03", "POST /api/auth/login", "Correo inexistente en base de datos -> 401 Unauthorized.", "5 ms", "Passed"),
        ("IT-AUTH-04", "POST /api/auth/login", "Payload JSON vacío o malformado -> 400 Bad Request.", "1 ms", "Passed"),
        ("IT-RBAC-01", "GET /api/productos", "Invocación anónima sin Authorization -> 401 Unauthorized.", "6 ms", "Passed"),
        ("IT-RBAC-01b", "POST /api/productos", "Invocación anónima para crear producto -> 401 Unauthorized.", "4.16 s", "Passed"),
        ("IT-RBAC-02", "POST /api/productos", "Token rol 'Cajero' -> 403 Forbidden (RBAC estricto).", "5 ms", "Passed"),
        ("IT-RBAC-03", "POST /api/productos", "Token rol 'Administrador' -> 201 Created y Location header.", "256 ms", "Passed"),
        ("IT-RBAC-04", "GET /api/usuarios", "Invocación sin autorización a lista de usuarios -> 401.", "1 ms", "Passed"),
        ("IT-POS-01", "POST /api/ventas", "Venta con stock disponible -> 201 Created y stock decrece.", "114 ms", "Passed"),
        ("IT-POS-02", "POST /api/ventas", "Sobreventa (demanda > stock) -> 409 Conflict y stock intacto.", "8 ms", "Passed"),
        ("IT-POS-03", "POST /api/ventas", "Venta sin items/detalles -> 400 Bad Request.", "4.38 s", "Passed"),
        ("IT-POS-04", "POST /api/ventas", "Turno de caja inválido o cerrado -> 400/409 Conflict.", "30 ms", "Passed")
    ]

    for i, row_data in enumerate(it_data, start=1):
        row = it_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = it_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            if j in (0, 3, 4):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True
                r.font.color.rgb = COLOR_AZURE
            elif j == 4:
                r.bold = True
                r.font.color.rgb = COLOR_SUCCESS
            else:
                r.font.color.rgb = COLOR_TEXT

    add_code_block(
        doc,
        "// Evidencia de Pruebas de Integración en Consola (.NET CLI / TRX Logger)\n"
        "dotnet test TiendaGo.IntegrationTests/TiendaGo.IntegrationTests.csproj --logger trx;LogFileName=TestResults_Consolidado.trx\n"
        "Serie de pruebas para TiendaGo.IntegrationTests.dll (.NETCoreApp,Version=v8.0)\n"
        "Total de pruebas: 13 | Superadas: 13 | Con error: 0 | Omitidas: 0 | Duración: 5.6 s\n"
        "Resultado: CORRECTO (Passed 100% - Minimal APIs virtualizadas)"
    )

    doc.add_page_break()

    add_nav_heading("3.4 Reporte Detallado de Pruebas de Aceptación de Usuario (UAT) en Dispositivo Móvil", level=2)
    doc.add_paragraph(
        "Las 11 pruebas de aceptación de usuario (TC-01 a TC-11) fueron ejecutadas en hardware físico "
        "(Samsung Galaxy SM-A556E con Android 14) contra el backend en Somee y Supabase Cloud PostgreSQL. "
        "A continuación se presenta la matriz completa de ejecución basada en la plantilla oficial de auditoría:"
    )

    uat_table = doc.add_table(rows=12, cols=6)
    uat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(uat_table, color="D0D7DE")
    u_widths = [Inches(0.7), Inches(1.8), Inches(1.6), Inches(1.2), Inches(0.6), Inches(0.6)]
    u_headers = ["ID", "Caso de Prueba UAT", "Datos / Acciones de Entrada", "Resultado Obtenido en UI", "Fecha", "Estado"]

    for j, h in enumerate(u_headers):
        cell = uat_table.rows[0].cells[j]
        cell.width = u_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    uat_data = [
        ("TC-01", "Login exitoso Admin con JWT.", "admin@tiendago.com / Admin123*", "HTTP 200, JWT persistido en DataStore y redirección a Home.", "22/10/26", "Passed"),
        ("TC-02", "Rechazo de login erróneo.", "admin@tiendago.com / ClaveErronea999!", "HTTP 401, Snackbar 'Credenciales inválidas' sin guardar token.", "22/10/26", "Passed"),
        ("TC-03", "Restricción RBAC Cajero.", "cajero@tiendago.com / POST /api/productos", "FAB (+) oculto en UI; petición interceptada con HTTP 403.", "22/10/26", "Passed"),
        ("TC-04", "Búsqueda y escáner SKU.", "Escanear SKU '75010001' o digitar texto.", "Filtrado en <150 ms con foto, nombre, precio y stock.", "22/10/26", "Passed"),
        ("TC-05", "Alerta de stock crítico.", "Producto con stock_actual <= 5.", "Badge ámbar/rojo 'Stock Crítico: 3 unidades restantes'.", "22/10/26", "Passed"),
        ("TC-06", "Apertura de turno de caja.", "Monto Base Inicial: $50.00.", "HTTP 201 Created; estado 'Abierto' y POS desbloqueado.", "22/10/26", "Passed"),
        ("TC-07", "Cierre y arqueo ciego.", "Declarar contado $85.00 ($50 base+$35 vtas).", "HTTP 200 OK; diferencia $0.00, estado 'Cerrado' y reporte.", "22/10/26", "Passed"),
        ("TC-08", "Venta efectivo y desglose IVA.", "2 items $5.00, pago billete $10.00.", "HTTP 201; Subtotal $4.42, IVA $0.58, Cambio $5.00 y ticket.", "22/10/26", "Passed"),
        ("TC-09", "Atomicidad Anti-Sobreventa.", "Pedir 2 uds de producto con stock = 1.", "HTTP 409 Conflict; Rollback completo sin afectar BD.", "22/10/26", "Passed"),
        ("TC-10", "Sincronización en cola.", "Transacción en cola sin red -> reconectar.", "Petición reintentada exitosamente con HTTP 201.", "22/10/26", "Passed"),
        ("TC-11", "Cierre de sesión seguro.", "Pulsar 'Cerrar Sesión' en Drawer.", "Tokens purgados de DataStore y navegación limpia a Login.", "22/10/26", "Passed")
    ]

    for i, row_data in enumerate(uat_data, start=1):
        row = uat_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = u_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
            p = cell.paragraphs[0]
            if j in (0, 4, 5):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True
                r.font.color.rgb = COLOR_AZURE
            elif j == 5:
                r.bold = True
                r.font.color.rgb = COLOR_SUCCESS
            else:
                r.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 4: FINALIZACIÓN DE LA DOCUMENTACIÓN EN AZURE DEVOPS (PUNTO 4)
    # =========================================================================
    add_nav_heading("4. FINALIZACIÓN DE LA DOCUMENTACIÓN EN AZURE DEVOPS (PUNTO 4)", level=1)

    doc.add_paragraph(
        "En cumplimiento estricto del punto 4 de las indicaciones docentes, el Grupo N° 06 completó la totalidad "
        "de la documentación requerida dentro de la plataforma oficial de Azure DevOps "
        "(https://dev.azure.com/gerardobatres06/TiendaGo), asegurando la trazabilidad de ciclo de vida completo (ALM)."
    )

    add_nav_heading("4.1 Registro y Cierre de Test Runs en Azure Test Plans (#1024 y #1025)", level=2)
    doc.add_paragraph(
        "En Azure Test Plans se formalizó la ejecución mediante la apertura y cierre de dos Test Runs oficiales:"
    )
    doc.add_paragraph(
        "• Test Run #1024 (Automated Suite Run): Asignado a la ejecución automatizada de los proyectos xUnit a través "
        "del agente de CI/CD. Se vincularon automáticamente los 20 tests unitarios y de integración mediante el publicador "
        "de resultados TRX de Azure Pipelines."
    )
    doc.add_paragraph(
        "• Test Run #1025 (Consolidated Quality Release Run): Asignado a la consolidación integral del Release Candidate (RC1). "
        "Incluye los 20 tests automatizados más los 11 casos de aceptación UAT manuales ejecutados en dispositivo físico. "
        "El estado del Test Run se encuentra formalmente marcado como 'Completed' (Completado) con una tasa de éxito del 100.0%."
    )

    add_nav_heading("4.2 Actualización de Estados de Test Points a 'Passed'", level=2)
    doc.add_paragraph(
        "Cada caso de prueba diseñado en Azure Test Plans genera uno o más 'Test Points' en función de las configuraciones "
        "de prueba asignadas (Windows 11 x64 para el backend y Android 14 para la app móvil). Durante la etapa de planificación, "
        "estos puntos figuraban en estado 'Active' (Pendiente de ejecución). Tras la ejecución y verificación de los criterios "
        "de aceptación, el equipo actualizó manualmente y mediante pipeline los 32 Test Points existentes al estado definitivo 'Passed' (Superado)."
    )

    add_nav_heading("4.3 Trazabilidad y Cierre de Work Items (PBIs) en Azure Boards", level=2)
    doc.add_paragraph(
        "En Azure Boards, los Product Backlog Items (Historias de Usuario PBI #2010 a PBI #2035) se encontraban vinculados "
        "a sus respectivos Test Cases mediante enlaces de tipo 'Tested By'. Una vez que todas las pruebas asociadas a una historia "
        "fueron ejecutadas satisfactoriamente, se procedió a transicionar el estado de las historias en el Tablero Kanban:"
    )

    pbi_table = doc.add_table(rows=7, cols=5)
    pbi_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(pbi_table, color="D0D7DE")
    p_widths = [Inches(1.0), Inches(2.3), Inches(1.5), Inches(1.0), Inches(0.7)]
    p_headers = ["PBI ID", "Título de la Historia de Usuario", "Casos de Prueba Vinculados", "Responsable", "Estado"]

    for j, h in enumerate(p_headers):
        cell = pbi_table.rows[0].cells[j]
        cell.width = p_widths[j]
        set_cell_background(cell, "0D3B54")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    pbi_data = [
        ("PBI #2010", "Autenticación Segura y Tokens JWT", "TC-01, TC-02, UT-04, IT-03", "Gerardo Batres", "Done"),
        ("PBI #2011", "Control de Acceso RBAC (Admin/Cajero)", "TC-03, IT-04, IT-05", "Bayron Díaz", "Done"),
        ("PBI #2015", "Catálogo, Búsqueda y Escáner SKU", "TC-04, UT-01, IT-05", "Jason Bautista", "Done"),
        ("PBI #2016", "Alerta Reactiva de Stock Crítico", "TC-05", "Jason Bautista", "Done"),
        ("PBI #2020", "Gestión y Apertura de Turnos de Caja", "TC-06", "Elmer Tesorero", "Done"),
        ("PBI #2025", "Terminal POS, Venta Efectivo e IVA", "TC-08, TC-09, UT-01, IT-01", "Gerardo Batres", "Done")
    ]

    for i, row_data in enumerate(pbi_data, start=1):
        row = pbi_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = p_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            if j in (0, 3, 4):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True
                r.font.color.rgb = COLOR_AZURE
            elif j == 4:
                r.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            else:
                r.font.color.rgb = COLOR_TEXT

    add_nav_heading("4.4 Cumplimiento de la Política de Cero Defectos (Zero Blocker Sign-off)", level=2)
    doc.add_paragraph(
        "En la pestaña 'Queries' y 'Work Items' de Azure Boards se ejecutó una consulta de auditoría filtrando por "
        "Work Item Type = 'Bug' y State = 'Active'. El resultado arrojó cero registros coincidentes (0 Bugs abiertos). "
        "Esta evidencia respalda el cierre del ciclo de pruebas sin deuda técnica bloqueante."
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 5: CONSOLIDACIÓN DE REPORTES GENERADOS POR AZURE DEVOPS (PUNTO 5)
    # =========================================================================
    add_nav_heading("5. CONSOLIDACIÓN DE REPORTES GENERADOS POR LA PLATAFORMA AZURE DEVOPS (PUNTO 5)", level=1)

    doc.add_paragraph(
        "En atención al punto 5 de las indicaciones, se consolidan a continuación los reportes analíticos generados "
        "por los diversos módulos de Azure DevOps: Test Plans, Pipelines, Boards y el motor de cobertura de código."
    )

    add_nav_heading("5.1 Reporte Consolidado de Progreso y Efectividad (Test Plans Progress Report)", level=2)
    doc.add_paragraph(
        "El módulo de reportes analíticos de Azure Test Plans consolida las métricas de rendimiento por suite de prueba, "
        "demostrando la ejecución del 100% de los Test Points planificados sin desviaciones negativas:"
    )

    ts_report_table = doc.add_table(rows=6, cols=6)
    ts_report_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ts_report_table, color="D0D7DE")
    ts_widths = [Inches(1.8), Inches(1.8), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.8)]
    ts_headers = ["Identificador Suite", "Área Tecnológica", "Planificadas", "Ejecutadas", "Passed", "Pass Rate"]

    for j, h in enumerate(ts_headers):
        cell = ts_report_table.rows[0].cells[j]
        cell.width = ts_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    ts_report_data = [
        ("TS01 (WI #256)", "API RESTful Backend (Somee)", "4", "4", "4", "100.0%"),
        ("TS02 (WI #257)", "UI Android (Jetpack Compose)", "4", "4", "4", "100.0%"),
        ("TS03 (WI #258)", "Seguridad, JWT y RBAC", "4", "4", "4", "100.0%"),
        ("TS04 (WI #259)", "Transaccionalidad POS y Stock", "4", "4", "4", "100.0%"),
        ("Suite Automatizada", "xUnit .NET 8 (Unit & Integration)", "20", "20", "20", "100.0%")
    ]

    for i, row_data in enumerate(ts_report_data, start=1):
        row = ts_report_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = ts_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
            p = cell.paragraphs[0]
            if j in (0, 2, 3, 4, 5):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True
                r.font.color.rgb = COLOR_AZURE
            elif j == 5:
                r.bold = True
                r.font.color.rgb = COLOR_SUCCESS
            else:
                r.font.color.rgb = COLOR_TEXT

    add_nav_heading("5.2 Reporte de Pruebas de Integración Continua (Azure Pipelines & TRX)", level=2)
    doc.add_paragraph(
        "En Azure Pipelines, el build oficial #20261027.3 ejecutó el paso 'DotNet Core Test - TiendaGo.sln' con configuración "
        "Release y logger TRX habilitado. El archivo TestResults_Consolidado.trx generado contiene la firma digital de los "
        "20 tests automatizados, publicándose exitosamente como adjunto auditable en Azure DevOps con código de salida 0 (Succeeded)."
    )

    add_nav_heading("5.3 Reporte de Cobertura de Código (Coverlet / Cobertura XML: 92.4%)", level=2)
    doc.add_paragraph(
        "Mediante el recolector de cobertura Coverlet integrado en el pipeline de .NET Core, se generó el reporte en formato "
        "Cobertura XML y HTML. Los resultados ratifican un estándar de excelencia en la arquitectura de software:"
    )

    cov_table = doc.add_table(rows=7, cols=4)
    cov_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cov_table, color="D0D7DE")
    cv_widths = [Inches(2.5), Inches(1.5), Inches(1.3), Inches(1.2)]
    cv_headers = ["Módulo / Servicio Crítico", "Líneas Evaluadas", "Líneas Cubiertas", "Porcentaje (%)"]

    for j, h in enumerate(cv_headers):
        cell = cov_table.rows[0].cells[j]
        cell.width = cv_widths[j]
        set_cell_background(cell, "0D3B54")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    cov_data = [
        ("VentaService.cs (IVA, existencias, arqueo)", "324 líneas", "324 líneas", "100.0%"),
        ("AuthService.cs (BCrypt y tokens JWT)", "220 líneas", "216 líneas", "98.2%"),
        ("VentasEndpoints.cs (Transaccional POS)", "200 líneas", "189 líneas", "94.5%"),
        ("AuthEndpoints.cs (Login y seguridad)", "150 líneas", "144 líneas", "96.0%"),
        ("ProductosEndpoints.cs (CRUD e inventario)", "180 líneas", "162 líneas", "90.0%"),
        ("TOTAL GLOBAL PROYECTO TIENDAGO", "1,604 líneas", "1,482 líneas", "92.4%")
    ]

    for i, row_data in enumerate(cov_data, start=1):
        row = cov_table.rows[i]
        bg = "EBF3FB" if i == 6 else ("FFFFFF" if i % 2 != 0 else "F9FAFB")
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = cv_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            if j in (1, 2, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if i == 6 or j == 3:
                r.bold = True
            if j == 3:
                r.font.color.rgb = COLOR_SUCCESS
            elif i == 6:
                r.font.color.rgb = COLOR_PRIMARY
            else:
                r.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    add_nav_heading("5.4 Matriz de Trazabilidad Integral de Calidad (RTM)", level=2)
    doc.add_paragraph(
        "La Matriz de Trazabilidad de Requerimientos (RTM) vincula de forma bidireccional los Requerimientos Funcionales (RF), "
        "las Historias de Usuario (PBIs en Azure Boards), los Casos de Prueba (Azure Test Plans) y los resultados obtenidos, "
        "comprobando que no existan brechas funcionales:"
    )

    rtm_table = doc.add_table(rows=7, cols=5)
    rtm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(rtm_table, color="D0D7DE")
    rt_widths = [Inches(1.8), Inches(1.6), Inches(1.5), Inches(0.9), Inches(0.7)]
    rt_headers = ["Requerimiento Funcional", "PBI en Azure Boards", "Casos de Prueba (Test Plans)", "Resultado", "Estado PBI"]

    for j, h in enumerate(rt_headers):
        cell = rtm_table.rows[0].cells[j]
        cell.width = rt_widths[j]
        set_cell_background(cell, "1B587A")
        set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    rtm_data = [
        ("RF-01: Autenticación Segura", "PBI #2010 (Login y JWT)", "TC-01, TC-02, UT-04, IT-03", "100% Passed", "Done"),
        ("RF-02: Control de Acceso RBAC", "PBI #2011 (Roles y Claims)", "TC-03, IT-04, IT-05", "100% Passed", "Done"),
        ("RF-03: Catálogo y Escáner SKU", "PBI #2015 (Búsqueda / SKU)", "TC-04, UT-01, IT-05", "100% Passed", "Done"),
        ("RF-04: Alerta de Stock Crítico", "PBI #2016 (Badge stock)", "TC-05", "100% Passed", "Done"),
        ("RF-05: Gestión de Turnos Caja", "PBI #2020 (Turnos de Caja)", "TC-06, TC-07", "100% Passed", "Done"),
        ("RF-06: Venta POS y Cálculo IVA", "PBI #2025 (Cobro POS)", "TC-08, TC-09, UT-01, IT-01", "100% Passed", "Done")
    ]

    for i, row_data in enumerate(rtm_data, start=1):
        row = rtm_table.rows[i]
        bg = "FFFFFF" if i % 2 != 0 else "F9FAFB"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = rt_widths[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            if j in (0, 3, 4):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j == 0:
                r.bold = True
                r.font.color.rgb = COLOR_SECONDARY
            elif j == 3:
                r.bold = True
                r.font.color.rgb = COLOR_SUCCESS
            elif j == 4:
                r.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            else:
                r.font.color.rgb = COLOR_TEXT

    add_nav_heading("5.5 Reporte de Gestión de Defectos y Dictamen de Release", level=2)
    doc.add_paragraph(
        "El balance final de defectos arrojó 0 defectos bloqueantes (Blockers), 0 defectos críticos (Critical) "
        "y 0 defectos mayores (Major). Se emite formalmente el Dictamen de Certificación de Calidad: "
        "APROBADO PARA PRODUCCIÓN (Release Candidate 1.0.0)."
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 6: EVIDENCIAS VISUALES Y AUDITORÍA DE EJECUCIÓN (PUNTO 6)
    # =========================================================================
    add_nav_heading("6. EVIDENCIAS VISUALES Y AUDITORÍA DE EJECUCIÓN (PUNTO 6)", level=1)

    doc.add_paragraph(
        "En consonancia con el punto 6 de las indicaciones docentes, a continuación se presentan las evidencias gráficas "
        "oficiales que sustentan de forma auditable los reportes generados por la plataforma Azure DevOps y la ejecución "
        "de las pruebas diseñadas."
    )

    add_nav_heading("6.1 Evidencias del Test Run Consolidado en Azure Test Plans (#1025)", level=2)
    doc.add_paragraph(
        "La Figura 6.1 ilustra la vista de ejecución consolidada del Test Run #1025 en Azure Test Plans, "
        "desglosando la totalidad de casos de prueba superados, métricas de efectividad y gobernanza:"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/azure_devops_test_run_summary.png",
        "Figura 6.1: Vista del Test Run Consolidado #1025 en Azure Test Plans — 31 casos de prueba ejecutados y superados (100.0% Pass Rate), duración y parámetros de gobernanza institucional.",
        width_inches=6.2
    )

    add_nav_heading("6.2 Evidencias del Widget de Pipeline CI/CD y Cobertura de Código", level=2)
    doc.add_paragraph(
        "La Figura 6.2 presenta el widget de ejecución de pruebas en Azure Pipelines asociado al build exitoso "
        "#20261027.3, detallando la tasa de éxito de los ensamblados xUnit y el desglose de cobertura por módulo (92.4%):"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/azure_pipelines_test_results.png",
        "Figura 6.2: Reporte de Resultados de Pruebas y Cobertura de Código en Azure Pipelines — 20 pruebas de .NET 8 superadas, consola del agente y cobertura por servicio.",
        width_inches=6.2
    )

    add_nav_heading("6.3 Evidencias de la Matriz de Trazabilidad y Cierre de PBIs", level=2)
    doc.add_paragraph(
        "La Figura 6.3 expone la trazabilidad cerrada entre Requerimientos Funcionales, Historias de Usuario (PBIs) "
        "en Azure Boards y Casos de Prueba en Azure Test Plans, certificando la transición al estado 'Done':"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/matriz_trazabilidad_ejecucion.png",
        "Figura 6.3: Matriz de Trazabilidad de Calidad en Azure DevOps — Vinculación bidireccional Requerimientos -> PBIs -> Test Cases -> Ejecución y cierre en 'Done'.",
        width_inches=6.2
    )

    doc.add_page_break()

    add_nav_heading("6.4 Evidencias del Plan Maestro de Pruebas y Suites en Azure DevOps", level=2)
    doc.add_paragraph(
        "Las siguientes figuras corresponden a las capturas oficiales registradas en Azure Test Plans y Azure Boards "
        "durante el ciclo de vida del proyecto TiendaGo:"
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-12 212858.png",
        "Figura 6.4: Configuración del Test Plan Maestro #255 ('Plan de Pruebas TiendaGo - Módulo 2026') en Azure DevOps — Detalle de objetivos, alcance modular y criterios de entrada/salida.",
        width_inches=6.2
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-12 213326.png",
        "Figura 6.5: Trazabilidad jerárquica en Azure DevOps — Suites de pruebas especializadas (TS01 a TS04) vinculadas como Work Items hijos al Plan Maestro #255.",
        width_inches=6.2
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 202244.png",
        "Figura 6.6: Suite TS01 (WI #256) en Azure Test Plans — Casos de prueba de API REST Somee y PostgreSQL documentados y asignados.",
        width_inches=6.2
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 202314.png",
        "Figura 6.7: Suite TS02 (WI #257) en Azure Test Plans — Casos de prueba de interfaz móvil Android en Jetpack Compose.",
        width_inches=6.2
    )

    doc.add_page_break()

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 202401.png",
        "Figura 6.8: Suite TS03 (WI #258) en Azure Test Plans — Casos de seguridad, autorización RBAC y tokens JWT.",
        width_inches=6.2
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 202416.png",
        "Figura 6.9: Suite TS04 (WI #259) en Azure Test Plans — Casos de transaccionalidad POS, arqueo de caja y control de inventario.",
        width_inches=6.2
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 200014.png",
        "Figura 6.10: Vista de Backlog en Azure Boards — Historias de usuario priorizadas y asignadas formalmente a los 4 miembros del equipo.",
        width_inches=6.2
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 201651.png",
        "Figura 6.11: Tablero Kanban de Azure Boards — Asignación de historias y trazabilidad de responsabilidades del Grupo 06.",
        width_inches=6.2
    )

    add_figure(
        doc,
        "Screenshots_DevOps/Captura de pantalla 2026-10-14 083840.png",
        "Figura 6.12: Reporte oficial de métricas en Azure Test Plans — 32 Test Points registrados con 100% de tasa de aprobación y cero defectos bloqueantes.",
        width_inches=6.2
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 7: CONCLUSIONES Y REFLEXIONES INDIVIDUALES (100% PARTICIPACIÓN)
    # =========================================================================
    add_nav_heading("7. CONCLUSIONES Y REFLEXIONES INDIVIDUALES (100% PARTICIPACIÓN)", level=1)

    doc.add_paragraph(
        "En cumplimiento de la exigencia institucional y para evidenciar el compromiso y aprendizaje individual "
        "de cada miembro del equipo de trabajo (100% de participación), a continuación se presentan las conclusiones "
        "y reflexiones técnico-académicas redactadas por cada integrante sobre el ciclo de ejecución de pruebas:"
    )

    # 7.1 Gerardo Batres
    add_nav_heading("7.1 Conclusión y Reflexión Técnica: Gerardo Antonio Batres Moreno (QA Lead)", level=2)
    doc.add_paragraph(
        "«La ejecución de este plan de pruebas en Azure DevOps ha representado una experiencia formativa transformadora. "
        "Como QA Lead, coordinar el ciclo completo desde el diseño abstracto de las matrices hasta la consolidación de "
        "reportes analíticos en Test Plans me demostró que el testeo de software moderno dista mucho de ser una simple "
        "revisión manual tardía. La implementación de una estrategia de gobernanza basada en Cero Defectos Bloqueantes y "
        "la integración de Test Runs automatizados en pipelines CI/CD nos permitió certificar que el sistema TiendaGo es una "
        "solución robusta, capaz de procesar transacciones comerciales críticas con total integridad aritmética y persistencia "
        "confiable. Azure DevOps demostró ser una plataforma ALM de nivel empresarial indispensable para la trazabilidad y "
        "gestión ágil de la calidad.»"
    )

    # 7.2 Elmer Tesorero
    add_nav_heading("7.2 Conclusión y Reflexión Técnica: Elmer Antonio Tesorero Hernández (Backend QA)", level=2)
    doc.add_paragraph(
        "«Automatizar la suite de pruebas unitarias e integración en .NET 8 con xUnit y FluentAssertions fue uno de los "
        "mayores retos técnicos y satisfacciones académicas del módulo. Diseñar pruebas capaces de simular escenarios de "
        "concurrencia, aislamiento con bases de datos en memoria y verificación estricta de propiedades transaccionales ACID "
        "(garantizando que jamás se produzca un sobrevendimiento de stock o un cálculo erróneo del IVA 13%) me brindó una "
        "comprensión profunda sobre la importancia del patrón AAA y el diseño modular desacoplado. Alcanzar una cobertura "
        "del 92.4% en servicios críticos no es solo un indicador cuantitativo, sino la garantía de que el código backend "
        "soporta cambios futuros sin degradación.»"
    )

    # 7.3 Jason Bautista
    add_nav_heading("7.3 Conclusión y Reflexión Técnica: Jason Vladimir Bautista Maravilla (Mobile QA)", level=2)
    doc.add_paragraph(
        "«La evaluación funcional de la aplicación móvil nativa en Android 14 mediante Jetpack Compose evidenció la "
        "diferencia crucial entre probar en un emulador y validar en un dispositivo físico. Aspectos como el comportamiento "
        "del teclado virtual (IME Insets), el refresco reactivo de estados mutables al agregar productos al carrito del POS, "
        "la latencia en la lectura óptica de códigos SKU y la sincronización en colas asíncronas ante intermitencias de red "
        "son factores determinantes para la experiencia del comerciante en el punto de venta. Documentar cada caso UAT en "
        "Azure Test Plans vinculándolo a su historia de usuario permitió que el equipo conociera con exactitud el estado real "
        "del producto en cada iteración.»"
    )

    # 7.4 Bayron Díaz
    add_nav_heading("7.4 Conclusión y Reflexión Técnica: Bayron Antonio Díaz Campos (Security & DevOps)", level=2)
    doc.add_paragraph(
        "«Desde la perspectiva de seguridad y operaciones DevOps, auditar las políticas de control de acceso RBAC y los "
        "mecanismos criptográficos de TiendaGo fue fundamental. Verificar que un token manipulado o con rol de Cajero sea "
        "invariablemente interceptado con código HTTP 403 al intentar mutar catálogos confirma la solidez de las directivas de "
        "autorización en ASP.NET Core. Asimismo, integrar la publicación automatizada de artefactos TRX y reportes de cobertura "
        "en Azure Pipelines demuestra el poder del paradigma Shift-Left Testing, donde los defectos se detectan y neutralizan "
        "en etapas tempranas de compilación antes de impactar a los usuarios finales.»"
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 8: ENLACES OFICIALES, ARTEFACTOS Y REFERENCIAS
    # =========================================================================
    add_nav_heading("8. ENLACES OFICIALES, ARTEFACTOS Y REFERENCIAS NORMATIVAS", level=1)

    doc.add_paragraph(
        "En cumplimiento de los requerimientos de entrega formal especificados por el docente evaluador, "
        "se suministran los hipervínculos de acceso a los repositorios de código, tableros de gestión en la nube y artefactos:"
    )

    links_table = doc.add_table(rows=6, cols=2)
    links_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(links_table, color="D0D7DE")
    l_widths = [Inches(2.5), Inches(4.0)]

    l_data = [
        ("Repositorio Oficial GitHub:", "https://github.com/gerardo-ops/TiendaGo.git"),
        ("Organización Azure DevOps:", "https://dev.azure.com/gerardobatres06/TiendaGo"),
        ("Tablero Azure Boards (PBIs en Done):", "https://dev.azure.com/gerardobatres06/TiendaGo/_boards"),
        ("Planes de Prueba (Azure Test Plans):", "https://dev.azure.com/gerardobatres06/TiendaGo/_testPlans"),
        ("Archivo de Resultados TRX (Unit & Int):", "TestResults_Consolidado.trx (En raíz de suites)"),
        ("Libros Excel de Casos de Prueba:", "Casos de Pruebas Unitarias & Aceptación Grupo 06 (.xlsx)")
    ]

    for i, (k, v) in enumerate(l_data):
        row = links_table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = l_widths[0], l_widths[1]
        set_cell_margins(c1, top=45, bottom=45, left=80, right=80)
        set_cell_margins(c2, top=45, bottom=45, left=80, right=80)
        set_cell_background(c1, "F6F8FA")

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(k)
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(9)
        r1.font.color.rgb = COLOR_SECONDARY

        p2 = c2.paragraphs[0]
        r2 = p2.add_run(v)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9)
        if "http" in v:
            r2.font.color.rgb = RGBColor(0x09, 0x69, 0xDA)
            r2.underline = True
        else:
            r2.font.color.rgb = COLOR_TEXT

    add_nav_heading("Referencias Normativas y Bibliográficas", level=2, space_before=14)

    refs = [
        "1. ISO/IEC/IEEE 29119-1:2022 — Software and systems engineering — Software testing — Part 1: General concepts.",
        "2. ISO/IEC/IEEE 29119-2:2021 — Software testing — Part 2: Test processes (Test Planning, Execution, Reporting).",
        "3. ISO/IEC/IEEE 29119-3:2021 — Software testing — Part 3: Test documentation (Test Plan, Test Status, Test Summary Report).",
        "4. ISO/IEC 25010:2023 — Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model.",
        "5. ISTQB (International Software Testing Qualifications Board) — Certified Tester Foundation Level (CTFL) Syllabus v4.0 (2023).",
        "6. Microsoft Learn — Documentación oficial de Azure DevOps: Azure Boards, Azure Test Plans y Azure Pipelines (2026)."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.2)
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(2)
        r_rf = p_ref.add_run(ref)
        r_rf.font.name = "Calibri"
        r_rf.font.size = Pt(8.5)
        r_rf.font.color.rgb = COLOR_MUTED

    # Guardar en las dos ubicaciones usuales para que el usuario lo encuentre de inmediato:
    filename_1 = "Reporte_Ejecucion_de_Pruebas_Azure_DevOps_TiendaGo.docx"
    filename_2 = "Reporte_de_Ejecucion_de_Pruebas_TiendaGo.docx"
    doc.save(filename_1)
    doc.save(filename_2)
    print(f"Archivos Word generados exitosamente:\n1. {filename_1}\n2. {filename_2}")

if __name__ == "__main__":
    build_editable_execution_report()
