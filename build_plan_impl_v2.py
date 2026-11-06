"""
Plan de Implementación - TiendaGo v2.1
Ajustes: cronograma 4 semanas, máximo 15 páginas,
portada limpia + tabla de contenidos.
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DIR_BASE = r"c:\Users\Admin\Documents\Proyectos\TiendaGo"
OUTPUT   = os.path.join(DIR_BASE, "Plan_de_Implementacion_TiendaGo_v2.docx")
LOGO     = os.path.join(DIR_BASE, "Screenshots_DevOps", "portada_logos.png")
DIAGRAMA = os.path.join(DIR_BASE, "Screenshots_DevOps", "diagrama_despliegue_tiendago.png")

C_TITULO = RGBColor(0x1F, 0x36, 0x64)
C_BODY   = RGBColor(0x00, 0x00, 0x00)
C_MUTED  = RGBColor(0x40, 0x40, 0x40)
C_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
HDR_HEX  = "1F3864"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
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

def heading(doc, text, level=1):
    p = doc.add_paragraph()
    sb = Pt(13) if level == 1 else Pt(9)
    p.paragraph_format.space_before  = sb
    p.paragraph_format.space_after   = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name  = "Times New Roman"
    run.font.size  = Pt(13) if level == 1 else Pt(11.5)
    run.font.color.rgb = C_TITULO
    return p

def body(doc, text, sa=5):
    """Párrafo justificado Times 12, interlineado 1.5 (compacto para <15 pág)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(sa)
    p.paragraph_format.line_spacing = Pt(18)   # ~1.5 líneas
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = C_BODY
    return p

def bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Inches(0.4)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.line_spacing = Pt(18)

    r0 = p.add_run("\u27a4  ")
    r0.font.name = "Times New Roman"; r0.font.size = Pt(12)
    r0.font.color.rgb = C_TITULO

    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.bold = True
        rb.font.name = "Times New Roman"; rb.font.size = Pt(12)
        rb.font.color.rgb = C_BODY

    r = p.add_run(text)
    r.font.name = "Times New Roman"; r.font.size = Pt(12)
    r.font.color.rgb = C_BODY
    return p

def add_figure(doc, img_path, caption, width=5.5):
    if not os.path.exists(img_path):
        body(doc, f"[Imagen no encontrada: {img_path}]")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(img_path, width=Inches(width))
    pc = doc.add_paragraph()
    pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pc.paragraph_format.space_before = Pt(1)
    pc.paragraph_format.space_after  = Pt(6)
    rc = pc.add_run(caption)
    rc.italic = True
    rc.font.name = "Times New Roman"; rc.font.size = Pt(9.5)
    rc.font.color.rgb = C_MUTED

def make_table(doc, headers, widths, rows_data, alt_col_idx=0):
    """Genera una tabla con cabecera azul y filas alternas."""
    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(table)

    # Cabecera
    for j, h in enumerate(headers):
        c = table.rows[0].cells[j]
        c.width = widths[j]
        set_cell_bg(c, HDR_HEX)
        set_cell_margins(c)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True; r.font.name = "Times New Roman"
        r.font.size = Pt(9.5); r.font.color.rgb = C_WHITE

    # Filas de datos
    for i, row_data in enumerate(rows_data):
        row = table.rows[i + 1]
        for j, val in enumerate(row_data):
            c = row.cells[j]
            c.width = widths[j]
            if i % 2 == 1:
                set_cell_bg(c, "EBF0F8")
            set_cell_margins(c)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == alt_col_idx else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after  = Pt(1)
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"; r.font.size = Pt(9.5)
            if j == 0: r.bold = (j == alt_col_idx)
    return table

# ---------------------------------------------------------------------------
# Construcción
# ---------------------------------------------------------------------------
def build():
    print("Generando Plan de Implementación TiendaGo v2.1 (≤15 pág)...")
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin    = Inches(1.0)
        section.bottom_margin = Inches(0.9)
        section.left_margin   = Inches(1.2)
        section.right_margin  = Inches(1.2)
        section.page_width    = Inches(8.5)
        section.page_height   = Inches(11.0)

        hdr = section.header
        ph = hdr.paragraphs[0]
        ph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        rh = ph.add_run("TiendaGo — Plan de Implantación  |  Versión 2.0")
        rh.font.name = "Times New Roman"; rh.font.size = Pt(9)
        rh.font.color.rgb = C_MUTED

        ftr = section.footer
        pf = ftr.paragraphs[0]
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rf = pf.add_run("ESFE - AGAPE  |  Desarrollo de Software  |  Ciclo C4-26")
        rf.font.name = "Times New Roman"; rf.font.size = Pt(9)
        rf.font.color.rgb = C_MUTED

    # =========================================================
    # PORTADA (página en blanco con datos mínimos)
    # =========================================================
    def cover(text, size=12, bold=False, sa=4, color=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(sa)
        r = p.add_run(text)
        r.bold = bold
        r.font.name  = "Times New Roman"
        r.font.size  = Pt(size)
        r.font.color.rgb = color or C_TITULO

    # Espacio superior
    for _ in range(3):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0)

    if os.path.exists(LOGO):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after  = Pt(14)
        p_logo.add_run().add_picture(LOGO, width=Inches(1.9))

    cover("ESCUELA SUPERIOR FRANCISCANA ESPECIALIZADA - AGAPE", 13, True, 3)
    cover("Carrera: Técnico en Ingeniería de Desarrollo de Software", 11, False, 3)
    cover("Módulo: Implantación de Sistemas de Software", 11, False, 22)
    cover("Plan de Implantación", 22, True, 6)
    cover("TiendaGo", 16, True, 4)
    cover("Sistema de Punto de Venta Móvil y Gestión de Inventario", 12, False, 24)
    cover("Versión 2.0", 12, True, 4)
    cover("Noviembre de 2026", 12, False, 6)
    cover("Docente: Lic. Gerber Alexis Gómez Hidalgo", 11, False, 4)
    cover("Grupo de Trabajo N° 06", 11, False, 4)

    doc.add_page_break()

    # =========================================================
    # TABLA DE CONTENIDOS (sola en su propia página)
    # =========================================================
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_before = Pt(6)
    p_toc.paragraph_format.space_after  = Pt(14)
    r_toc = p_toc.add_run("Tabla de Contenidos")
    r_toc.bold = True
    r_toc.font.name = "Times New Roman"; r_toc.font.size = Pt(16)
    r_toc.font.color.rgb = C_TITULO

    toc_entries = [
        ("1. Introducción", "3", True),
        ("    1.1 Propósito", "3", False),
        ("    1.2 Alcance", "3", False),
        ("    1.3 Definiciones, Acrónimos, y Abreviaciones", "4", False),
        ("    1.4 Referencias", "5", False),
        ("    1.5 Vista Global", "5", False),
        ("2. Planificación de la Entrega", "7", True),
        ("    2.1 Responsabilidades", "7", False),
        ("    2.2 Cronograma", "7", False),
        ("3. Recursos", "9", True),
        ("    3.1 Facilidades", "9", False),
        ("    3.2 Hardware", "9", False),
        ("    3.3 Unidad de Implantación", "10", False),
        ("        3.3.1 Software de Soporte", "10", False),
        ("        3.3.2 Documentación de Soporte", "11", False),
        ("        3.3.3 Personal de Soporte (personas, perfiles)", "11", False),
        ("4. Entrenamiento", "12", True),
    ]

    toc_table = doc.add_table(rows=len(toc_entries), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(toc_table, color="FFFFFF")  # Sin bordes
    toc_w = [Inches(5.0), Inches(0.7)]

    for idx, (title, pg, main) in enumerate(toc_entries):
        row = toc_table.rows[idx]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = toc_w[0]; c2.width = toc_w[1]
        set_cell_margins(c1, top=18, bottom=18, left=30, right=30)
        set_cell_margins(c2, top=18, bottom=18, left=30, right=30)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after  = Pt(0)
        r1 = p1.add_run(title)
        r1.bold = main
        r1.font.name = "Times New Roman"; r1.font.size = Pt(11)
        r1.font.color.rgb = C_TITULO if main else C_BODY

        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after  = Pt(0)
        r2 = p2.add_run(pg)
        r2.bold = main
        r2.font.name = "Times New Roman"; r2.font.size = Pt(11)
        r2.font.color.rgb = C_MUTED

    doc.add_page_break()

    # =========================================================
    # 1. INTRODUCCIÓN
    # =========================================================
    heading(doc, "1. Introducción")

    heading(doc, "1.1 Propósito", 2)
    body(doc,
        "El presente documento describe el conjunto de tareas necesarias para instalar y probar el sistema "
        "TiendaGo, con el fin de que la transición hacia los usuarios finales se realice de forma efectiva "
        "y eficiente. Provee una lista detallada de eventos, un cronograma de actividades y las dependencias "
        "requeridas, y formula la estrategia de implantación basada en el alcance y las limitaciones del "
        "sistema. La intención es complementar el diagrama de despliegue del Documento de Arquitectura de "
        "TiendaGo con las instrucciones operativas necesarias para llevar el sistema al ambiente de producción."
    )

    heading(doc, "1.2 Alcance", 2)
    body(doc,
        "Este documento se inicia en la fase de Elaboración y se concreta en la fase de Construcción, "
        "buscando definir la agenda de implantación que incluye la preparación del ambiente, el "
        "entrenamiento de los usuarios y los futuros procedimientos de soporte. También se definen "
        "las dependencias y recursos de software y hardware necesarios para instalar el sistema, "
        "determinando la factibilidad del proceso de implantación."
    )

    heading(doc, "1.3 Definiciones, Acrónimos, y Abreviaciones", 2)

    defs = [
        ("TiendaGo",
         "Sistema de Punto de Venta Móvil (POS) y Gestión de Inventario Express para establecimientos comerciales."),
        ("POS",
         "Point of Sale. Sistema que procesa transacciones de compra-venta directamente en el mostrador."),
        ("API",
         "Application Programming Interface. Componente que permite la comunicación entre la app móvil y el servidor."),
        ("ASP.NET Core 8",
         "Framework de código abierto de Microsoft utilizado para construir el backend del sistema TiendaGo."),
        ("JWT",
         "JSON Web Token. Estándar de seguridad para la autenticación de usuarios y protección de los endpoints."),
        ("RBAC",
         "Role-Based Access Control. Control de acceso basado en roles: Administrador y Cajero."),
        ("PostgreSQL",
         "Sistema gestor de base de datos relacional de código libre utilizado por TiendaGo."),
        ("Supabase",
         "Plataforma de base de datos como servicio (DBaaS) basada en PostgreSQL, usada para alojar la BD en la nube."),
        ("EF Core",
         "Entity Framework Core 8. ORM para .NET que permite la interacción entre el backend y la base de datos."),
        ("Kotlin / Jetpack Compose",
         "Lenguaje y toolkit de UI utilizados para la aplicación móvil nativa de TiendaGo en Android."),
        ("ESC/POS",
         "Protocolo para impresoras térmicas de tickets, utilizado para emitir comprobantes de venta."),
        ("IVA",
         "Impuesto al Valor Agregado (13%). TiendaGo calcula y desglosa el IVA en cada transacción."),
        ("Turno de Caja",
         "Período de operación de un cajero: apertura, registro de ventas y arqueo de cierre."),
        ("Diagrama de Implementación",
         "Diagrama UML que modela la distribución física del sistema en los nodos de hardware y red."),
        ("Stakeholders",
         "Individuos o entidades afectadas por el sistema: propietarios, cajeros, supervisores y administradores."),
        ("Licencia",
         "TiendaGo está construido sobre software de código libre, eliminando el pago de licencias propietarias."),
        ("Requerimientos",
         "Funcionalidades del sistema desde el punto de vista del usuario, expuestas en los casos de uso."),
        ("Restricción",
         "Limitaciones del sistema, como los requerimientos mínimos de conectividad a Internet y de hardware."),
    ]

    def_table = doc.add_table(rows=len(defs), cols=2)
    def_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(def_table)
    dw = [Inches(1.7), Inches(4.5)]

    for i, (term, dfn) in enumerate(defs):
        row = def_table.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = dw[0]; c2.width = dw[1]
        set_cell_bg(c1, "EBF0F8")
        set_cell_margins(c1); set_cell_margins(c2)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1); p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(term)
        r1.bold = True; r1.font.name = "Times New Roman"; r1.font.size = Pt(9.5)
        r1.font.color.rgb = C_TITULO
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p2.paragraph_format.space_before = Pt(1); p2.paragraph_format.space_after = Pt(1)
        r2 = p2.add_run(dfn)
        r2.font.name = "Times New Roman"; r2.font.size = Pt(9.5)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0); p_sp.paragraph_format.space_after = Pt(6)

    heading(doc, "1.4 Referencias", 2)
    refs = [
        "Documento de Arquitectura de TiendaGo versión 3.0",
        "Diagrama de Implementación de TiendaGo versión 1.1",
        "Diagrama de Implantación de TiendaGo versión 1.1",
        "Vista de Implantación de TiendaGo versión 1.2",
        "Repositorio oficial en GitHub: https://github.com/gerardo-ops/TiendaGo.git",
        "Organización en Azure DevOps: https://dev.azure.com/gerardobatres06/TiendaGo",
    ]
    for r in refs:
        bullet(doc, r)

    heading(doc, "1.5 Vista Global", 2)
    body(doc,
        "Se conforma el equipo de implantación determinando los recursos humanos necesarios para la "
        "instalación del sistema y para realizar las pruebas luego de implantado, así como la "
        "aceptación formal por parte de los usuarios del establecimiento."
    )
    body(doc,
        "La vista de implantación muestra el diagrama de despliegue donde se describe la distribución "
        "física del sistema en un ambiente de producción, indicando dónde se encuentran los "
        "componentes, en qué servidores y hardware. A continuación se muestra el Diagrama de "
        "Despliegue correspondiente al sistema TiendaGo:"
    )
    add_figure(
        doc, DIAGRAMA,
        "Figura 1: Diagrama de Despliegue del Sistema TiendaGo — Distribución física de componentes "
        "en los nodos: Terminales POS Android, Servidor Web API y Base de Datos Supabase Cloud.",
        width=5.6
    )
    body(doc,
        "El diagrama muestra tres nodos principales: los dispositivos móviles Android de los cajeros "
        "como terminales POS, el servidor que aloja la API en ASP.NET Core 8 y la base de datos "
        "PostgreSQL en Supabase. La comunicación entre nodos se realiza mediante HTTPS con "
        "autenticación JWT, garantizando la seguridad de cada transacción registrada."
    )

    doc.add_page_break()

    # =========================================================
    # 2. PLANIFICACIÓN DE LA ENTREGA
    # =========================================================
    heading(doc, "2. Planificación de la Entrega")

    heading(doc, "2.1 Responsabilidades", 2)
    body(doc,
        "Para llevar a cabo la implantación del sistema desarrollado, es necesario establecer un "
        "compromiso por parte de los stakeholders del establecimiento comercial y el Grupo N° 06 de "
        "desarrolladores. El equipo se enfocará en realizar pruebas en un servidor de prueba para "
        "asegurarse de que el sistema funcione correctamente fuera de las máquinas de desarrollo, "
        "comprometiéndose a instalar TiendaGo totalmente operativo en el establecimiento."
    )

    heading(doc, "2.2 Cronograma", 2)
    body(doc,
        "La implantación del sistema en el establecimiento comercial es responsabilidad del Grupo N° 06 de desarrolladores de TiendaGo. A continuación vamos a proponer un cronograma aproximado de las actividades, el cual contempla un tiempo estimado de cuatro semanas:"
    )

    bullet(doc,
        "Primero que nada el equipo de desarrolladores de TiendaGo terminará todo lo relacionado con la documentación del sistema."
    )
    bullet(doc,
        "Posteriormente, se visualizarán todos los recursos necesarios de software y los recursos de hardware mínimos necesarios para que el sistema pueda implantarse de manera correcta en el establecimiento comercial. El tiempo estimado para esta actividad sería de una semana."
    )
    bullet(doc,
        "Una vez que se tienen los requisitos tanto de software como de hardware, se notifica al encargado y administrador del establecimiento comercial los espacios que se van a necesitar para la instalación del servidor, los dispositivos móviles y la red en general (en caso de que hagan falta). Esto se realiza en conjunto entre el encargado del establecimiento y el equipo de TiendaGo."
    )
    bullet(doc,
        "Posteriormente de tener a la disposición el espacio geográfico necesario para toda la implantación del sistema se instalarán los equipos (si se requieren más de los que ya están) y a su vez el software dentro de ellos, incluyendo la base de datos en Supabase, el Web API y la aplicación móvil en las terminales POS, y se realizarán una serie de pruebas para probar que el sistema está totalmente operativo en ese ambiente. Esta actividad tiene un tiempo estimado de dos semanas."
    )
    bullet(doc,
        "Luego de tener el sistema totalmente operativo en el establecimiento se realizaría el proceso de entrenamiento del personal, es decir, los usuarios reales del sistema desarrollado (cajeros y administradores). Se tiene un tiempo estimado de 1 semana."
    )
    bullet(doc,
        "Finalmente tenemos el soporte, donde tanto el personal del establecimiento como el grupo de desarrolladores del sistema TiendaGo pueden asistir a los usuarios en el uso correcto del sistema, y de corregir las fallas que se presenten durante el tiempo de vida de uso del sistema."
    )

    doc.add_page_break()

    # =========================================================
    # 3. RECURSOS
    # =========================================================
    heading(doc, "3. Recursos")

    heading(doc, "3.1 Facilidades", 2)
    body(doc,
        "La implantación de TiendaGo cuenta con una serie de ventajas por parte del equipo de "
        "desarrollo y del personal del establecimiento. Se destaca la experiencia acumulada "
        "por el equipo en la instalación y prueba del sistema en diferentes ambientes durante "
        "todo el proceso de desarrollo del proyecto."
    )
    body(doc,
        "El sistema fue implementado en su totalidad con software libre y de código abierto, lo "
        "que reduce considerablemente los costos de implantación y facilita el entendimiento y "
        "mantenimiento a largo plazo. Además, se dispone de documentación completa y de un canal "
        "de comunicación directo con los desarrolladores de TiendaGo para resolver dudas con rapidez."
    )

    heading(doc, "3.2 Hardware", 2)
    body(doc,
        "Los requerimientos de hardware son moderados, adecuados para el volumen transaccional "
        "propio de un establecimiento comercial de pequeño o mediano tamaño. La base de datos "
        "necesita capacidad de almacenamiento ya que, a lo largo del tiempo, se acumularán "
        "registros de ventas, turnos y usuarios que deben conservarse para respaldo contable."
    )

    hw_data = [
        ("Servidor de Aplicaciones",
         "Dual-Core 2.0 GHz, 2 GB RAM, 20 GB SSD, conexión a Internet de 10 Mbps"),
        ("Base de Datos en la Nube",
         "Instancia de Supabase Cloud. No se requiere hardware físico local adicional"),
        ("Terminales POS (Cajeros)",
         "Smartphone Android 8.0+, 2 GB RAM mínimo, cámara de al menos 8 MP"),
        ("Impresoras Térmicas",
         "Impresora de 58 mm o 80 mm compatible con Bluetooth y protocolo ESC/POS"),
        ("Estación Administrativa",
         "PC con navegador web moderno: Chrome, Edge o Firefox"),
    ]
    make_table(
        doc,
        ["Componente", "Especificación Mínima Requerida"],
        [Inches(2.0), Inches(4.2)],
        hw_data
    )

    p_sp4 = doc.add_paragraph()
    p_sp4.paragraph_format.space_before = Pt(0); p_sp4.paragraph_format.space_after = Pt(8)

    heading(doc, "3.3 Unidad de Implantación", 2)

    heading(doc, "3.3.1 Software de Soporte", 2)
    body(doc,
        "El equipo de TiendaGo considera que para un funcionamiento correcto del sistema, es "
        "necesario instalar en el servidor el software utilizado durante el desarrollo. "
        "El software requerido es el siguiente:"
    )
    sw_items = [
        ("Sistema Operativo:", "Linux Ubuntu Server 22.04 LTS o Windows Server 2022."),
        ("Runtime de Aplicación:", "Microsoft .NET 8.0 Runtime y el ASP.NET Core Hosting Bundle."),
        ("Servidor Web:", "Nginx (Linux) o IIS 10 (Windows) como proxy inverso para el servicio Kestrel."),
        ("Base de Datos:", "PostgreSQL gestionado a través de Supabase Cloud (no requiere instalación local)."),
        ("Dispositivos Móviles:", "Android 8.0 Oreo o superior en cada terminal POS."),
    ]
    for bp, text in sw_items:
        bullet(doc, text, bold_prefix=bp + "  ")
    body(doc,
        "Los usuarios que accedan desde computadoras de escritorio deberán contar con un navegador "
        "web actualizado (Chrome, Edge o Firefox) para las funciones administrativas del sistema.",
        sa=5
    )

    heading(doc, "3.3.2 Documentación de Soporte", 2)
    body(doc,
        "Toda la documentación de soporte del sistema se encuentra disponible en el Documento de "
        "Arquitectura de TiendaGo y en el manual de usuario. Los documentos de soporte disponibles son:"
    )
    bullet(doc, "Documento de Arquitectura de Software de TiendaGo (versión 3.0).")
    bullet(doc, "Manual de Instalación y Configuración del Servidor y la API.")
    bullet(doc, "Manual de Usuario del Administrador del Sistema.")
    bullet(doc, "Manual de Operación del Cajero (Guía Rápida).")
    bullet(doc, "Repositorio de código fuente en GitHub con historial de versiones.")

    heading(doc, "3.3.3 Personal de Soporte (personas, perfiles)", 2)
    body(doc,
        "El personal de soporte estará conformado por personal de TI del establecimiento y por el "
        "equipo de desarrolladores del Grupo N° 06. El equipo de TiendaGo brindará soporte directo "
        "durante las primeras semanas, mientras que el personal de TI del local asumirá el soporte "
        "auxiliar en casos de fallas a largo plazo."
    )
    body(doc,
        "En el sistema existirá un perfil de usuario Administrador, con la responsabilidad de "
        "asignar privilegios a los demás usuarios, crear cuentas de cajeros y examinar el "
        "comportamiento del sistema en intervalos de tiempo determinados."
    )

    doc.add_page_break()

    # =========================================================
    # 4. ENTRENAMIENTO
    # =========================================================
    heading(doc, "4. Entrenamiento")
    body(doc,
        "Es importante resaltar que el entrenamiento del personal del establecimiento está en "
        "manos del equipo de desarrolladores de TiendaGo, ya que el Grupo N° 06 no podrá brindar "
        "soporte presencial de manera indefinida después de la implantación."
    )
    body(doc,
        "Se tiene pensado realizar el entrenamiento de los usuarios durante cuatro días —incluidos "
        "dentro de la cuarta semana del cronograma— y que posteriormente continúen practicando "
        "para profundizar en el uso del sistema. Los temas a cubrir durante el entrenamiento son:"
    )
    bullet(doc, "Inicio de sesión, gestión de roles y apertura del turno de caja con monto inicial.")
    bullet(doc, "Registro de ventas: búsqueda por nombre o código de barras, cálculo automático del IVA (13%) y cobro al cliente.")
    bullet(doc, "Emisión de tickets de venta a través de la impresora térmica Bluetooth.")
    bullet(doc, "Gestión de inventario: registro de productos, actualización de precios y control de existencias.")
    bullet(doc, "Cierre de turno y arqueo de caja: balance esperado versus efectivo físico contado.")
    bullet(doc, "Consulta del panel administrativo para visualizar reportes y actividad del sistema.")

    body(doc,
        "El período de adaptación de los usuarios al sistema no debería ser prolongado, ya que "
        "varios de los que trabajan en el establecimiento han tenido contacto visual con el sistema "
        "y han estado presentes en demostraciones funcionales durante las diferentes entregas del proyecto.",
        sa=5
    )
    body(doc,
        "Es fundamental que durante el entrenamiento y el soporte inicial, el equipo de "
        "desarrolladores de TiendaGo esté presente junto al personal del establecimiento para "
        "resolver en tiempo real cualquier duda que se presente y garantizar una adopción exitosa "
        "del sistema por parte de todos los usuarios."
    )

    # =========================================================
    # GUARDAR
    # =========================================================
    doc.save(OUTPUT)
    print(f"Generado: {OUTPUT}")

if __name__ == "__main__":
    build()
