import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Agrega números de página oficiales (excepto portada e índice)"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            # Solo numerar a partir de la página 3 (o no mostrar en portada)
            # En la plantilla del docente:
            # Página 1 (Portada): sin número
            # Página 2 (Índice): sin número
            # Página 3: INTRODUCCIÓN ...
            # Si queremos ser 100% fieles a la plantilla del profesor, en la plantilla del profesor
            # la numeración en el índice marca 3 a 8.
            self.draw_page_decorations()
            super().showPage()
        super().save()

    def draw_page_decorations(self):
        pass # La plantilla del docente es de diseño limpio sin pie de página invasivo

def build_pdf(filename="Reporte_de_Ejecucion_de_Pruebas_TiendaGo.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,  # 0.75 in
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    # Colores
    c_blue = colors.HexColor("#1F4E79")
    c_dark = colors.HexColor("#111111")
    c_gray = colors.HexColor("#555555")
    c_white = colors.white
    c_alt_row = colors.HexColor("#F2F5F9")

    # Estilos
    s_title_cover = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=11, leading=15, alignment=1, textColor=c_dark)
    s_lead_cover = ParagraphStyle('CoverLead', fontName='Helvetica-Bold', fontSize=10.5, leading=14, alignment=1, textColor=c_dark)
    s_sub_cover = ParagraphStyle('CoverSub', fontName='Helvetica', fontSize=9.5, leading=13, alignment=1, textColor=c_gray)

    s_idx_title = ParagraphStyle('IdxTitle', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=1, textColor=c_dark)
    s_idx_h1 = ParagraphStyle('IdxH1', fontName='Helvetica-Bold', fontSize=9.5, leading=14, textColor=c_dark)
    s_idx_h2 = ParagraphStyle('IdxH2', fontName='Helvetica', fontSize=9, leading=13, textColor=c_dark)

    s_heading_center = ParagraphStyle('HeadingCenter', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=1, textColor=c_dark)
    s_heading_left = ParagraphStyle('HeadingLeft', fontName='Helvetica-Bold', fontSize=11.5, leading=15, alignment=0, textColor=c_dark)
    s_subheading = ParagraphStyle('SubHeading', fontName='Helvetica-Bold', fontSize=10.5, leading=14, alignment=0, textColor=c_dark)
    s_body = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=9.5, leading=13.5, alignment=4, textColor=c_dark) # 4 = Justified
    s_bullet = ParagraphStyle('BulletText', fontName='Helvetica', fontSize=9, leading=13, alignment=4, textColor=c_dark, leftIndent=14, firstLineIndent=-10)

    s_tbl_header = ParagraphStyle('TblHdr', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=c_white)
    s_tbl_cell = ParagraphStyle('TblCell', fontName='Helvetica', fontSize=8.5, leading=11, textColor=c_dark)
    s_tbl_cell_bold = ParagraphStyle('TblCellB', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_dark)

    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("ESCUELA SUPERIOR FRANCISCANA ESPECIALIZADA / AGAPE", s_title_cover))
    story.append(Spacer(1, 24))

    logo_path = os.path.abspath("Screenshots_DevOps/portada_logos.png")
    if os.path.exists(logo_path):
        story.append(RLImage(logo_path, width=150, height=82))
    story.append(Spacer(1, 24))

    story.append(Paragraph("CARRERA", s_lead_cover))
    story.append(Paragraph("TÉCNICO EN INGENIERÍA DE DESARROLLO DE SOFTWARE", s_sub_cover))
    story.append(Spacer(1, 16))

    story.append(Paragraph("MÓDULO", s_lead_cover))
    story.append(Paragraph("TESTEO DE SOFTWARE", s_sub_cover))
    story.append(Spacer(1, 16))

    story.append(Paragraph("TÍTULO", s_lead_cover))
    story.append(Paragraph("Reporte de Ejecución de Pruebas.", s_sub_cover))
    story.append(Spacer(1, 18))

    story.append(Paragraph("ESTUDIANTE(S)", s_lead_cover))
    story.append(Paragraph("GERARDO ANTONIO BATRES MORENO 100%", s_sub_cover))
    story.append(Paragraph("ELMER ANTONIO TESORERO HERNÁNDEZ 100%", s_sub_cover))
    story.append(Paragraph("JASON VLADIMIR BAUTISTA MARAVILLA 100%", s_sub_cover))
    story.append(Paragraph("BAYRON ANTONIO DÍAZ CAMPOS 100%", s_sub_cover))
    story.append(Spacer(1, 18))

    story.append(Paragraph("FECHA DE PRESENTACIÓN", s_lead_cover))
    story.append(Paragraph("28/10/26", s_sub_cover))
    story.append(Spacer(1, 16))

    story.append(Paragraph("DOCENTE", s_lead_cover))
    story.append(Paragraph("GERBER ALEXIS GÓMEZ", s_sub_cover))
    story.append(Spacer(1, 16))

    story.append(Paragraph("CICLO", s_lead_cover))
    story.append(Paragraph("C4-26", s_sub_cover))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: ÍNDICE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("INDICE", s_idx_title))
    story.append(Spacer(1, 20))

    toc_rows = [
        ("INTRODUCCIÓN.....................................................................................................................", "3", True, 0),
        ("PRUEBAS APLICADAS..........................................................................................................", "4", True, 0),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Pruebas Unitarias...............................................................................................................", "4", False, 1),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Pruebas de API..................................................................................................................", "4", False, 1),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Pruebas de Aceptación......................................................................................................", "5", False, 1),
        ("RESULTADOS OBTENIDOS...................................................................................................", "5", True, 0),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Pruebas de Aceptación......................................................................................................", "5", False, 1),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Pruebas de API..................................................................................................................", "6", False, 1),
        ("&nbsp;&nbsp;&nbsp;&nbsp;Pruebas Unitarias...............................................................................................................", "7", False, 1),
        ("CONCLUSIONES....................................................................................................................", "8", True, 0),
        ("RECOMENDACIONES............................................................................................................", "8", True, 0)
    ]

    t_data = []
    for t_text, t_pg, is_b, lvl in toc_rows:
        p_st = s_idx_h1 if is_b else s_idx_h2
        p1 = Paragraph(t_text, p_st)
        p2 = Paragraph(f"<b>{t_pg}</b>" if is_b else t_pg, p_st)
        t_data.append([p1, p2])

    t_toc = Table(t_data, colWidths=[470, 30])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    story.append(t_toc)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: INTRODUCCIÓN
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("INTRODUCCIÓN", s_heading_center))
    story.append(Spacer(1, 16))

    p1_text = (
        "El presente informe formaliza y documenta los resultados del Ciclo 1 de Pruebas de "
        "Software realizado sobre el sistema \"TiendaGo\", una plataforma moderna orientada al "
        "punto de venta (POS) móvil y a la gestión ágil de inventario express para comercios "
        "minoristas y tiendas de conveniencia. La solución comprende una arquitectura desacoplada "
        "compuesta por un backend RESTful de alta disponibilidad desarrollado sobre .NET 8 (C#) con "
        "Entity Framework Core y PostgreSQL en Supabase Cloud, articulado con una aplicación "
        "móvil nativa desarrollada en Android con Jetpack Compose orientada a la operativa táctil "
        "de cajeros y administradores de tienda."
    )
    story.append(Paragraph(p1_text, s_body))
    story.append(Spacer(1, 12))

    p2_text = (
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
    story.append(Paragraph(p2_text, s_body))
    story.append(Spacer(1, 12))

    p3_text = (
        "Para garantizar un proceso formal y reproducible, el equipo aplicó el estándar internacional "
        "ISO/IEC/IEEE 29119 para la especificación y documentación de pruebas, implementando "
        "una pirámide de testing balanceada que articula pruebas unitarias de servicios, pruebas de "
        "integración sobre endpoints de Web API y pruebas funcionales de aceptación basadas en el "
        "comportamiento (BDD) estructuradas en sintaxis Gherkin y matrices de trazabilidad. Este "
        "informe expone de forma clara la tipología de pruebas aplicadas, el consolidado de resultados "
        "métricos obtenidos en Azure DevOps y las conclusiones técnicas derivadas del ciclo."
    )
    story.append(Paragraph(p3_text, s_body))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: PRUEBAS APLICADAS
    # =========================================================================
    story.append(Spacer(1, 5))
    story.append(Paragraph("PRUEBAS APLICADAS", s_heading_left))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Conforme a las directrices de aseguramiento de calidad y la rúbrica de evaluación, se "
        "aplicaron tres categorías fundamentales de pruebas de software, cubriendo desde la lógica "
        "atómica de los servicios hasta la validación de la experiencia del usuario final.", s_body
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Pruebas Unitarias", s_subheading))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "Las pruebas unitarias tuvieron como objetivo aislar y examinar el comportamiento lógico de "
        "los métodos que componen la capa de servicios de aplicación (Application Layer) de "
        "TiendaGo, verificando la adecuada respuesta ante datos válidos y el lanzamiento preciso de "
        "excepciones de dominio ante transgresiones de las reglas de negocio.", s_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("● <b>Entorno y Tecnologías:</b> Implementadas en C# bajo .NET 8 utilizando el framework xUnit 2.5, la biblioteca de dobles de prueba Moq 4.20 para la simulación de repositorios y Entity Framework Core In-Memory / SQLite para la persistencia transitoria y aislamiento de pruebas.", s_bullet))
    story.append(Spacer(1, 4))
    story.append(Paragraph("● <b>Servicio VentaService (Casos 2001-2003):</b> Verificación del cálculo contable de subtotales, determinación precisa del impuesto al valor agregado (IVA 13%) y cálculo de vuelto en liquidación en efectivo, decremento atómico de existencias ante ventas exitosas, e intercepción con lanzamiento estricto de InvalidOperationException ante intentos de sobreventa con inventario insuficiente.", s_bullet))
    story.append(Spacer(1, 4))
    story.append(Paragraph("● <b>Servicio AuthService (Casos 2004-2006):</b> Comprobación de la verificación criptográfica de contraseñas contra hash seguro (BCrypt / SHA-256), emisión de tokens JWT con claims de identidad y rol (Administrador y Cajero), políticas de expiración y denegación de credenciales inválidas.", s_bullet))
    story.append(Spacer(1, 4))
    story.append(Paragraph("● <b>Servicio ProductoMapping y DTOs (Casos 2007-2010):</b> Validación del mapeo bidireccional entre DTOs de transferencia y entidades del modelo de dominio, validación de reglas de datos de catálogo y consistencia en el identificador de categoría.", s_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Total de pruebas unitarias declaradas: 10 casos de prueba (identificadores 2001 al 2010), registrados en Azure DevOps en la suite con ID 255.", s_body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Pruebas de API", s_subheading))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "Las pruebas de API evaluaron la integración funcional de los controladores y Minimal APIs "
        "alojados en ASP.NET Core Web API, comprobando la comunicación cliente-servidor mediante "
        "solicitudes HTTP sobre los endpoints expuestos.", s_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("● <b>Enfoque de Verificación:</b> Validación de códigos de estado HTTP (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 409 Conflict), estructura de los DTOs en formato JSON, políticas de autorización basadas en encabezados \"Authorization: Bearer &lt;Token&gt;\" y persistencia relacional evaluada mediante WebApplicationFactory.", s_bullet))
    story.append(Spacer(1, 4))
    story.append(Paragraph("● <b>Endpoints de Autenticación (/api/auth/login - CP01 a CP05):</b> Pruebas de autenticación exitosa para administradores y cajeros con retorno de DTO con Bearer Token JWT, validación de credenciales inválidas (401), cuentas no registradas y obligatoriedad de campos requeridos (400).", s_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: PRUEBAS DE API (cont.) & ACEPTACIÓN & RESULTADOS
    # =========================================================================
    story.append(Spacer(1, 5))
    story.append(Paragraph("● <b>Endpoints de Control de Acceso y Catálogo (/api/productos, /api/categorias - CP06 a CP11):</b> Listado de catálogo de productos activo, consulta individual por ID o SKU, creación de productos por administradores con respuesta 201 Created, intercepción de peticiones anónimas sin token (401) y rechazo estricto con código 403 Forbidden ante intentos de mutación de catálogo por usuarios con rol Cajero.", s_bullet))
    story.append(Spacer(1, 4))
    story.append(Paragraph("● <b>Endpoints de Ventas y Turnos (/api/ventas, /api/turnos - CP12 a CP15):</b> Registro transaccional de ventas en Terminal POS con decremento atómico de stock, bloqueo y retorno de código 409 Conflict ante sobreventa o stock insuficiente, rechazo de ventas sin artículos (400 Bad Request) y control de bloqueo de operaciones de cobro si no existe un turno de caja activo.", s_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Total de pruebas de API declaradas: 15 casos de prueba (identificadores CP01 al CP15), registrados en Azure DevOps en la suite con ID 256.", s_body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Pruebas de Aceptación", s_subheading))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "Las pruebas de aceptación validaron la conformidad del software con respecto a las "
        "expectativas de los usuarios clave y los criterios de aceptación acordados en el Product "
        "Backlog (PBIs #2010 al #2035).", s_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("● <b>Metodología y Estándar:</b> Basadas en el estándar ISO/IEC/IEEE 29119 y especificadas en lenguaje natural estructurado Gherkin (escenarios BDD en historias de usuario con Dado, Cuando, Entonces), respaldadas con suites de pruebas en dispositivos móviles Android y matrices de trazabilidad.", s_bullet))
    story.append(Spacer(1, 4))
    story.append(Paragraph("● <b>Módulos de Usuario Validados:</b> 1) Autenticación y Seguridad (TC-01 a TC-02); 2) Control de Acceso RBAC y Visibilidad de UI (TC-03); 3) Catálogo, Búsqueda Rápida y Escáner SKU (TC-04); 4) Alerta Visual Reactiva de Stock Crítico (TC-05); 5) Control de Turnos de Caja y Arqueo Ciego (TC-06 a TC-07); 6) Terminal POS, Venta en Efectivo e Impuestos (TC-08); 7) Atomicidad Anti-Sobreventa y Persistencia (TC-09 a TC-10); 8) Resumen de Dashboard Gerencial (TC-11); 9) Bloqueo de POS sin Turno Activo (TC-12).", s_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Total de pruebas de aceptación declaradas: 12 casos de prueba (identificadores TC-01 al TC-12), registrados en Azure DevOps en la suite con ID 257.", s_body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("RESULTADOS OBTENIDOS", s_heading_left))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "A continuación se detallan de forma resumida y consolidada los resultados obtenidos en "
        "cada una de las suites de prueba ejecutadas en el marco del Ciclo 1 en Azure DevOps.", s_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Pruebas de Aceptación", s_subheading))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Resumen métrico de la Suite de Aceptación (Suite ID 257 en Azure DevOps):", s_body))
    story.append(Spacer(1, 4))

    def make_rl_table(hdr_title, rows_list):
        data = [[Paragraph(hdr_title, s_tbl_header), Paragraph("Valor Registrado", s_tbl_header)]]
        for r_name, r_val in rows_list:
            is_bold = "100%" in r_val or "superados" in r_val or "exitosas" in r_val
            st_val = s_tbl_cell_bold if is_bold else s_tbl_cell
            data.append([Paragraph(r_name, s_tbl_cell), Paragraph(r_val, st_val)])
        t = Table(data, colWidths=[240, 260])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), c_blue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, c_blue),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [c_white, c_alt_row]),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        return t

    metric_uat_data = [
        ("Número de pruebas declaradas:", "12 casos (IDs TC-01 a TC-12)"),
        ("Número de pruebas ejecutadas:", "12 casos (validadas en diseño y criterios BDD)"),
        ("Número de pruebas exitosas:", "12 casos (100% de conformidad)"),
        ("Número de pruebas pendientes (fallidas):", "0 casos fallidos (0 Bugs generados)")
    ]
    story.append(make_rl_table("Métrica de Aceptación", metric_uat_data))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 6: CAPTURA ACEPTACIÓN + TABLA API + CAPTURA API
    # =========================================================================
    story.append(Spacer(1, 2))
    img_uat = os.path.abspath("Screenshots_DevOps/captura_excel_aceptacion.png")
    if os.path.exists(img_uat):
        story.append(RLImage(img_uat, width=500, height=210))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Pruebas de API", s_subheading))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Resumen métrico de la Suite de Integración de API (Suite ID 256 en Azure DevOps):", s_body))
    story.append(Spacer(1, 4))

    metric_api_data = [
        ("Número de pruebas declaradas:", "15 casos (IDs CP01 a CP15)"),
        ("Número de pruebas ejecutadas:", "15 casos (ejecutadas vía REST Client / Test Runner)"),
        ("Número de pruebas exitosas:", "15 casos (100% de respuestas esperadas)"),
        ("Número de pruebas pendientes (fallidas):", "0 casos fallidos (0 Bugs generados)")
    ]
    story.append(make_rl_table("Métrica de API REST", metric_api_data))
    story.append(Spacer(1, 8))

    img_api = os.path.abspath("Screenshots_DevOps/captura_excel_api.png")
    if os.path.exists(img_api):
        story.append(RLImage(img_api, width=500, height=210))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 7: TABLA UNITARIAS + CAPTURA UNITARIAS + CONCLUSIONES (1 y 2)
    # =========================================================================
    story.append(Spacer(1, 2))
    story.append(Paragraph("Pruebas Unitarias", s_subheading))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Resumen métrico de la Suite de Pruebas Unitarias (Suite ID 255 en Azure DevOps):", s_body))
    story.append(Spacer(1, 4))

    metric_ut_data = [
        ("Número de pruebas declaradas:", "10 casos (IDs 2001 a 2010)"),
        ("Número de pruebas ejecutadas:", "10 casos (ejecutadas mediante xUnit en .NET 8)"),
        ("Número de pruebas exitosas:", "10 casos superados satisfactoriamente"),
        ("Número de pruebas pendientes (fallidas):", "0 casos fallidos (0 Bugs generados)")
    ]
    story.append(make_rl_table("Métrica Unitaria", metric_ut_data))
    story.append(Spacer(1, 6))

    img_ut = os.path.abspath("Screenshots_DevOps/captura_devops_unitarias.png")
    if os.path.exists(img_ut):
        story.append(RLImage(img_ut, width=490, height=210))
    story.append(Spacer(1, 8))

    story.append(Paragraph("CONCLUSIONES", s_heading_left))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "A partir de la ejecución sistemática de las pruebas de software y el análisis de los resultados "
        "obtenidos, se establecen las siguientes conclusiones formales:", s_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("● <b>1. Integridad y Blindaje de las Reglas de Negocio Operativas:</b> Las pruebas unitarias y de API verificaron que el núcleo de validaciones del sistema previene eficazmente anomalías críticas en la gestión del inventario y el punto de venta. Específicamente, se comprobó que el sistema bloquea con certeza absoluta cualquier intento de sobreventa cuando la demanda excede las existencias disponibles, rechaza operaciones de facturación si no existe una jornada de caja debidamente aperturada con monto base, y garantiza la inviolabilidad de las rutas administrativas mediante control de acceso RBAC estricto, impidiendo que usuarios con rol Cajero ejecuten alteraciones no autorizadas en el catálogo de productos.", s_bullet))
    story.append(Spacer(1, 4))

    story.append(Paragraph("● <b>2. Exactitud Algorítmica en Transacciones y Liquidación Financiera:</b> La suite de pruebas confirmó la solidez y consistencia matemática de los algoritmos de cobro en el Terminal POS, calculando con exactitud decimal el subtotal, el desglose impositivo del IVA (13%) y el cálculo de vuelto en operaciones en efectivo sin incurrir en desajustes por redondeo. Asimismo, el mecanismo de arqueo ciego implementado para el cierre de turno demostró registrar fielmente los balances reales frente a los cálculos teóricos del sistema, garantizando la trazabilidad contable y la conciliación antes de formalizar el cierre definitivo de la sesión de caja.", s_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 8: CONCLUSIÓN (3) + RECOMENDACIONES
    # =========================================================================
    story.append(Spacer(1, 5))
    story.append(Paragraph("● <b>3. Trazabilidad Total y Madurez del Proceso de QA en Azure DevOps:</b> Se consolidó una trazabilidad bidireccional del 100% entre las Historias de Usuario de los PBIs (#2010 al #2035) y los casos de prueba registrados en Azure DevOps mediante relaciones formales de tipo \"Tests / Tested By\". La estandarización de las suites (Unitarias, Integración y Aceptación) conforme al estándar internacional ISO/IEC/IEEE 29119 dota al proyecto TiendaGo de un marco de calidad transparente, reproducible y preparado para escalar a futuros ciclos de desarrollo.", s_bullet))
    story.append(Spacer(1, 14))

    story.append(Paragraph("RECOMENDACIONES", s_heading_left))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Con base en las observaciones recopiladas a lo largo del proceso de pruebas, se formulan "
        "las siguientes recomendaciones estratégicas y técnicas para optimizar los ciclos venideros:", s_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("● <b>1. Automatización de Pruebas en el Pipeline de CI/CD (Azure Pipelines):</b> Se recomienda configurar un pipeline de integración continua mediante archivo YAML en Azure DevOps que ejecute automáticamente la totalidad de la suite de pruebas unitarias y de integración en cada Pull Request hacia las ramas \"develop\" y \"main\". Esto garantizará que ninguna modificación de código introduzca regresiones en la lógica de negocio ni degrade la cobertura actual de pruebas.", s_bullet))
    story.append(Spacer(1, 5))

    story.append(Paragraph("● <b>2. Ejecución de Pruebas de Carga y Rendimiento en Endpoints Críticos:</b> Dado que el módulo de terminal de punto de venta y catálogo opera bajo transacciones concurrentes en horas pico de atención comercial, es prioritario implementar pruebas de rendimiento y estrés utilizando herramientas como k6 o Apache JMeter. Esto permitirá modelar la concurrencia simultánea esperada durante aperturas de jornada o promociones especiales, validando los tiempos de respuesta del backend en la nube y el comportamiento de bloqueo de concurrencia en PostgreSQL.", s_bullet))
    story.append(Spacer(1, 5))

    story.append(Paragraph("● <b>3. Implementación de Pruebas E2E Automatizadas para la Aplicación Móvil Android:</b> Se sugiere incorporar herramientas de automatización de interfaz móvil como Appium o Maestro para evaluar los flujos de interacción táctil del cajero en dispositivos Android. En particular, se debe automatizar la verificación del escaneo de códigos de barra (SKU) mediante la cámara, corroborando que la lectura óptica pueble reactivamente el carrito de compras, así como el correcto ajuste de la vista (imePadding) ante el despliegue del teclado virtual en diferentes resoluciones y versiones de sistema operativo.", s_bullet))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF: {filename}")

if __name__ == "__main__":
    build_pdf()
