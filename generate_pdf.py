import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

HEADER_LOGO = os.path.abspath("extracted_logos/user_1_X10.png")
CENTER_LOGO = os.path.abspath("extracted_logos/user_0_X7.png")
OUTPUT_PDF = os.path.abspath("Planificacion_de_pruebas_TiendaGo.pdf")

class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page_num = self._pageNumber
        self.saveState()
        
        # Running header on every page
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#222222"))
        self.drawString(54, 755, "ESCUELA SUPERIOR FRANCISCANA ESPECIALIZADA – AGAPE")
        
        if os.path.exists(HEADER_LOGO):
            self.drawImage(HEADER_LOGO, 434, 744, width=124, height=22, preserveAspectRatio=True, mask='auto')
        
        self.setStrokeColor(colors.HexColor("#bbbbbb"))
        self.setLineWidth(0.6)
        self.line(54, 738, 558, 738)
        
        # Footer on page 2 and onwards
        if page_num > 1:
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#666666"))
            self.drawString(54, 32, "Planificación de pruebas de software: TiendaGo Mobile & API | ESFE AGAPE")
            self.drawRightString(558, 32, f"Página {page_num} de {total_pages}")
            self.setStrokeColor(colors.HexColor("#e0e0e0"))
            self.setLineWidth(0.5)
            self.line(54, 42, 558, 42)
            
        self.restoreState()

def build_pdf():
    # 54 pt margins = 0.75 in. Printable width = 612 - 108 = 504 pt.
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=66,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()

    # Typography styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#111111")
    )
    
    style_cover_label = ParagraphStyle(
        'CoverLabel',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#111111")
    )
    
    style_cover_text = ParagraphStyle(
        'CoverText',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#222222")
    )
    
    style_cover_student = ParagraphStyle(
        'CoverStudent',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        alignment=1,
        textColor=colors.HexColor("#222222")
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0f2d59"),
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True
    )
    
    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor("#1c4273"),
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True
    )
    
    style_h3 = ParagraphStyle(
        'Heading3_Custom',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2d558a"),
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor("#222222"),
        spaceAfter=4
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        fontName='Helvetica',
        fontSize=8.3,
        leading=11.3,
        textColor=colors.HexColor("#222222"),
        leftIndent=12,
        spaceAfter=2.5
    )

    style_tbl_header = ParagraphStyle(
        'TableHdr',
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.black,
        alignment=0
    )

    style_tbl_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.4,
        textColor=colors.HexColor("#222222"),
        alignment=0
    )

    style_tbl_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.4,
        leading=9.4,
        textColor=colors.HexColor("#111111"),
        alignment=0
    )

    story = []

    def create_table(data, col_widths):
        t = Table(data, colWidths=col_widths, repeatRows=1)
        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#bce4f7")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4.5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4.5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#444444")),
        ]
        t.setStyle(TableStyle(t_style))
        return t

    # ================= PAGE 1: PORTADA =================
    story.append(Spacer(1, 25))
    story.append(Paragraph("ESCUELA SUPERIOR FRANCISCANA", style_cover_title))
    story.append(Paragraph("ESPECIALIZADA / AGAPE", style_cover_title))
    story.append(Spacer(1, 15))
    
    if os.path.exists(CENTER_LOGO):
        story.append(Image(CENTER_LOGO, width=82, height=74))
    story.append(Spacer(1, 18))

    story.append(Paragraph("CARRERA", style_cover_label))
    story.append(Paragraph("Técnico en ingeniería de Desarrollo de Software.", style_cover_text))
    story.append(Spacer(1, 15))

    story.append(Paragraph("MÓDULO", style_cover_label))
    story.append(Paragraph("Testeo de Software.", style_cover_text))
    story.append(Spacer(1, 15))

    story.append(Paragraph("TÍTULO", style_cover_label))
    story.append(Paragraph("Planificación de pruebas a aplicar al proyecto", style_cover_title))
    story.append(Paragraph("TiendaGo: POS Móvil & Web API RESTful", style_cover_text))
    story.append(Spacer(1, 15))

    story.append(Paragraph("ESTUDIANTE(S)", style_cover_label))
    story.append(Paragraph("Gerardo Antonio Batres Moreno 100%", style_cover_student))
    story.append(Paragraph("Elmer Antonio Tesorero Hernández 100%", style_cover_student))
    story.append(Paragraph("Jason Vladimir Bautista Maravilla 100%", style_cover_student))
    story.append(Paragraph("Bayron Antonio Díaz Campos 100%", style_cover_student))
    story.append(Spacer(1, 15))

    story.append(Paragraph("DOCENTE", style_cover_label))
    story.append(Paragraph("Gerber Alexis Gómez", style_cover_text))
    story.append(Spacer(1, 15))

    story.append(Paragraph("FECHA DE PRESENTACIÓN", style_cover_label))
    story.append(Paragraph("14/10/2026.", style_cover_text))
    story.append(Spacer(1, 15))

    story.append(Paragraph("CICLO", style_cover_label))
    story.append(Paragraph("C4-26.", style_cover_text))
    story.append(PageBreak())

    # ================= PAGE 2: 1. INTRODUCCIÓN Y 1.1 ALCANCE =================
    story.append(Paragraph("1. Introducción", style_h1))
    story.append(Paragraph(
        "El presente Plan de Pruebas prescribe el alcance, el enfoque, los recursos y el cronograma de ejecución "
        "de todas las actividades de Aseguramiento de Calidad (QA) del proyecto <b>TiendaGo</b>, una plataforma de punto "
        "de venta (POS) y gestión de inventario express orientada a dispositivos móviles Android y servicios REST en la nube. "
        "Identifica las características que se probarán, los tipos de pruebas que se realizarán, el personal responsable "
        "y los riesgos asociados.",
        style_body
    ))
    story.append(Paragraph(
        "El documento rige la validación de la versión <b>1.0.0 (Release Candidate)</b> y toma como referencia formal "
        "de redacción la familia de normas <b>ISO/IEC/IEEE 29119</b>: la parte 3 (documentación de pruebas) para la "
        "estructura de este plan, la parte 2 (procesos de prueba) para el ciclo de planificación, ejecución y cierre, "
        "y la parte 4 (técnicas de prueba) para el diseño de casos, en particular el análisis de valores límite (BVA), "
        "las particiones de equivalencia (EP), pruebas de transición de estados y matriz de roles (RBAC).",
        style_body
    ))
    story.append(Paragraph(
        "La aplicación está construida sobre una arquitectura desacoplada Cliente-Servidor N-Capas (Presentación Móvil, "
        "Lógica de Negocio en Servicios REST, Acceso a Datos y Entidades con persistencia en PostgreSQL). Por ello la "
        "estrategia busca validar rigurosamente la separación de responsabilidades, la seguridad perimetral mediante JWT, "
        "el control de acceso según roles y la integridad transaccional (ACID) en el flujo de ventas e inventario.",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Ficha técnica AUT
    data_aut = [
        [Paragraph("Dato", style_tbl_header), Paragraph("Descripción", style_tbl_header)],
        [Paragraph("Aplicación bajo prueba (AUT)", style_tbl_cell_bold), Paragraph("TiendaGo Mobile & API, versión 1.0.0 (Release Candidate)", style_tbl_cell)],
        [Paragraph("Tecnología Cliente Móvil", style_tbl_cell_bold), Paragraph("Android Nativo (Jetpack Compose, Kotlin 1.9+), Retrofit 2, OkHttp 4, Coil (imágenes), DataStore Preferences", style_tbl_cell)],
        [Paragraph("Tecnología Backend Web API", style_tbl_cell_bold), Paragraph(".NET 8.0, ASP.NET Core Web API (Minimal APIs y Controllers), Entity Framework Core 8.0, Supabase C# SDK, BCrypt.Net", style_tbl_cell)],
        [Paragraph("Componentes de interfaz y UX", style_tbl_cell_bold), Paragraph("Material 3 Compose, soporte de teclado virtual con imePadding/adjustResize, scanner de códigos de barras/QR", style_tbl_cell)],
        [Paragraph("Gestión del proyecto y control", style_tbl_cell_bold), Paragraph("GitHub (Ramas main, develop, feature branches bajo Git Flow, Pull Requests y Code Review)", style_tbl_cell)],
        [Paragraph("Norma de referencia", style_tbl_cell_bold), Paragraph("ISO/IEC/IEEE 29119 (Partes 2, 3 y 4)", style_tbl_cell)],
        [Paragraph("Base de datos de pruebas", style_tbl_cell_bold), Paragraph("PostgreSQL 15 en Supabase Cloud (instancia aislada TiendaGo_QA con seeders automatizados)", style_tbl_cell)],
        [Paragraph("Hosting / Despliegue", style_tbl_cell_bold), Paragraph("Servidor Somee Hosting (http://TiendaGO.somee.com/) y Supabase Cloud Services", style_tbl_cell)],
    ]
    story.append(create_table(data_aut, [154, 350]))
    story.append(Spacer(1, 6))

    # 1.1 Alcance
    story.append(Paragraph("1.1 Alcance", style_h2))
    story.append(Paragraph("<b>1.1.1 Módulos y Funcionalidades Dentro de Alcance:</b>", style_h3))
    alcance_items = [
        "<b>Módulo de Autenticación y Sesión (US-AUTH):</b> Inicio de sesión con credenciales válidas e inválidas, emisión de token JWT con expiración, almacenamiento seguro en DataStore y cierre de sesión con reseteo total de pila de navegación (backstack).",
        "<b>Control de Acceso Basado en Roles (RBAC):</b> Administrador (acceso total a inventario, creación/edición de productos, precios y monitoreo) vs Cajero (acceso restringido a lectura de catálogo, terminal POS y apertura/cierre de su propio turno; botón flotante de adición FAB oculto y bloqueo 403 Forbidden en endpoints administrativos).",
        "<b>Módulo de Inventario y Catálogo (US-CAT):</b> Listado paginado de productos, filtros por categoría, búsqueda dinámica por texto y escaneo óptico por SKU/código de barras; badges de alerta ante stock crítico (< 5 unidades) y renderizado adaptativo de imágenes con Coil.",
        "<b>Módulo de Turnos de Caja (US-TUR):</b> Apertura de turno con monto base en efectivo, asignación estricta cajero-turno-ventas, arqueo ciego al cierre y cálculo de diferencia de cuadre.",
        "<b>Módulo de Terminal POS y Transaccionalidad (US-POS):</b> Carrito ágil, cálculo automático de subtotales, IVA (13%), atajos táctiles de billetes ($10, $20, $50), cálculo de cambio y descuento atómico de existencias con transacciones ACID en PostgreSQL.",
        "<b>Interacción y Usabilidad UI/UX Móvil:</b> Comportamiento de insets de teclado virtual (adjustResize e imePadding) evitando solapamiento en formularios de cobro y registro."
    ]
    for it in alcance_items:
        story.append(Paragraph(f"• {it}", style_bullet))
    story.append(PageBreak())

    # ================= PAGE 3: 1.1.2 FUERA DE ALCANCE Y 1.2 OBJETIVO DE CALIDAD =================
    story.append(Paragraph("1.1.2 Fuera de Alcance", style_h2))
    story.append(Paragraph("Quedan explícitamente excluidos del ciclo de pruebas de la presente versión:", style_body))
    fuera_items = [
        "Integración con hardware bancario externo físico (lectores de tarjeta POS chip/contactless).",
        "Operatividad 100% offline con sincronización diferida bidireccional (requiere conectividad para validar stock centralizado).",
        "Compatibilidad con sistemas operativos Apple iOS (alcance exclusivo Android).",
        "Pruebas de resistencia ante ataques distribuidos de denegación de servicio (DDoS) sobre el servidor Somee.",
        "Impresión física por Bluetooth o cable de tickets térmicos (se valida la generación del comprobante y ticket correlativo digital)."
    ]
    for it in fuera_items:
        story.append(Paragraph(f"• {it}", style_bullet))
    story.append(Spacer(1, 8))

    # 1.2 Objetivo de Calidad
    story.append(Paragraph("1.2 Objetivo de Calidad", style_h2))
    story.append(Paragraph(
        "La meta del plan es certificar, con evidencia auditable, que la Aplicación Bajo Prueba (AUT) está lista "
        "para el paso a producción. Los objetivos específicos son garantizar la prevención absoluta de ventas sin stock, "
        "la consistencia transaccional ACID en PostgreSQL, la exactitud de los cálculos de cambio y la hermeticidad del control RBAC.",
        style_body
    ))
    story.append(Spacer(1, 4))

    data_kpi = [
        [Paragraph("Indicador", style_tbl_header), Paragraph("Meta", style_tbl_header), Paragraph("Observación", style_tbl_header)],
        [Paragraph("Cobertura de ejecución", style_tbl_cell_bold), Paragraph("100% de los 10 casos de prueba oficiales", style_tbl_cell), Paragraph("Ejecución y registro completo en suite de pruebas", style_tbl_cell)],
        [Paragraph("Tasa de aprobación general", style_tbl_cell_bold), Paragraph("Mínimo 95%", style_tbl_cell), Paragraph("El 5% restante solo puede ser de defectos Low/Medium con solución alternativa documentada", style_tbl_cell)],
        [Paragraph("Aprobación en casos Blocker y Critical", style_tbl_cell_bold), Paragraph("100% (obligatorio)", style_tbl_cell), Paragraph("Aplica a login (TC-01), RBAC (TC-03), venta en efectivo (TC-07), bloqueo sin stock (TC-08) y decremento en BD (TC-09)", style_tbl_cell)],
        [Paragraph("Defectos críticos abiertos al cierre", style_tbl_cell_bold), Paragraph("0", style_tbl_cell), Paragraph("Cero defectos de severidad Blocker o Critical pendientes de solución", style_tbl_cell)],
        [Paragraph("Vulnerabilidades de control de acceso (RBAC)", style_tbl_cell_bold), Paragraph("0", style_tbl_cell), Paragraph("Se verifica aislamiento total en cliente móvil y bloqueo HTTP 403 en API", style_tbl_cell)],
        [Paragraph("Trazabilidad de Requisitos (RTM)", style_tbl_cell_bold), Paragraph("100% de requerimientos", style_tbl_cell), Paragraph("100% de los PBI y requerimientos funcionales RF01-RF07 vinculados", style_tbl_cell)],
        [Paragraph("Estabilidad móvil (Crashes / ANR)", style_tbl_cell_bold), Paragraph("0%", style_tbl_cell), Paragraph("Cero cierres forzados por memoria/Coil o bloqueos en hilo principal de UI", style_tbl_cell)],
    ]
    story.append(create_table(data_kpi, [134, 110, 260]))
    story.append(PageBreak())

    # ================= PAGE 4: 1.3 ROLES Y RESPONSABILIDADES =================
    story.append(Paragraph("1.3 Roles y Responsabilidades", style_h1))
    story.append(Paragraph(
        "El equipo de QA es multidisciplinario y trabaja de forma colaborativa mediante GitHub y entornos locales/cloud. "
        "Las responsabilidades se distribuyen formalmente de la siguiente manera:",
        style_body
    ))
    story.append(Spacer(1, 6))

    data_roles = [
        [Paragraph("Integrante", style_tbl_header), Paragraph("Rol", style_tbl_header), Paragraph("Responsabilidades", style_tbl_header), Paragraph("Áreas a cargo", style_tbl_header)],
        [
            Paragraph("Gerardo Antonio Batres Moreno", style_tbl_cell_bold),
            Paragraph("QA Lead / Administrador del proyecto", style_tbl_cell),
            Paragraph("Define la estrategia y arquitectura de pruebas bajo ISO 29119; administra GitHub y políticas de ramas (Branch Protection); revisa Pull Requests y RTM; configura entornos y autoriza el Sign-off final.", style_tbl_cell),
            Paragraph("Estrategia general, trazabilidad, gobernanza y dictamen de cierre.", style_tbl_cell)
        ],
        [
            Paragraph("Elmer Antonio Tesorero Hernández", style_tbl_cell_bold),
            Paragraph("QA Automation & Backend Tester", style_tbl_cell),
            Paragraph("Diseña y ejecuta pruebas de integración sobre la API REST (.NET 8) con Postman; valida transacciones ACID en Supabase/PostgreSQL; audita tokens JWT, headers y tiempos de respuesta.", style_tbl_cell),
            Paragraph("Endpoints REST, persistencia PostgreSQL, concurrencia y transacciones.", style_tbl_cell)
        ],
        [
            Paragraph("Jason Vladimir Bautista Maravilla", style_tbl_cell_bold),
            Paragraph("Mobile QA Tester & Functional Specialist", style_tbl_cell),
            Paragraph("Ejecuta pruebas funcionales E2E en dispositivos Android reales y emuladores; valida interfaces Jetpack Compose, escaneo de códigos de barra, flujo POS de cobro y comportamiento del teclado (imePadding).", style_tbl_cell),
            Paragraph("Cliente Móvil Android, UI/UX, terminal POS, caja y catálogo.", style_tbl_cell)
        ],
        [
            Paragraph("Bayron Antonio Díaz Campos", style_tbl_cell_bold),
            Paragraph("Security Specialist & Environment Manager", style_tbl_cell),
            Paragraph("Define la metodología de pruebas de penetración y RBAC (Admin vs Cajero); gestiona la base de datos de pruebas y datos semilla (SeedAdmin.sql); genera y firma APKs en Android Studio y monitorea Somee.", style_tbl_cell),
            Paragraph("Seguridad RBAC, seeders de BD, empaquetado de APKs y despliegue.", style_tbl_cell)
        ],
    ]
    story.append(create_table(data_roles, [100, 94, 180, 130]))
    story.append(PageBreak())

    # ================= PAGE 5: 2. METODOLOGÍA DE PRUEBA =================
    story.append(Paragraph("2. Metodología de prueba", style_h1))
    story.append(Paragraph("2.1 Compendio Metodológico", style_h2))
    story.append(Paragraph(
        "Se implementa el proceso de pruebas dinámicas definido en <b>ISO/IEC/IEEE 29119-2</b>, el cual articula cuatro fases: "
        "diseño, implementación, ejecución y gestión de incidentes. Las técnicas de diseño se basan en <b>ISO/IEC/IEEE 29119-4</b> "
        "aplicando métodos de caja negra y basados en riesgos:",
        style_body
    ))
    metodo_items = [
        "<b>Partición de Equivalencia y Análisis de Valores Límite:</b> Aplicados a cantidades de stock (0, 1, stock mínimo umbral 5, stock normal), campos numéricos de precios ($0.01 vs 0), montos de pago recibidos y validación de sintaxis de credenciales.",
        "<b>Transición de Estados:</b> Evaluación del ciclo de vida de la sesión (Login -> Sesión Activa -> Cierre con backstack limpio), del turno de caja (Cerrado -> Abierto -> Arqueo Ciego -> Cerrado) y de inventario (Disponible -> Stock Crítico -> Agotado).",
        "<b>Pruebas de Roles (RBAC Matrix):</b> Verificación exhaustiva de visibilidad de componentes visuales en la app móvil y denegación de endpoints API (HTTP 403) según claims del token JWT.",
        "<b>Pruebas de Transaccionalidad Concurrente (ACID):</b> Verificación de exclusión mutua al vender el último producto en stock para evitar sobreventa o inventario negativo en PostgreSQL."
    ]
    for it in metodo_items:
        story.append(Paragraph(f"• {it}", style_bullet))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.2 Niveles de prueba", style_h2))
    niveles_items = [
        "<b>Pruebas Unitarias:</b> Verificación de funciones lógicas de cálculo de subtotales, IVA (13%), cambio de efectivo, validadores de SKU y mapeo de DTOs con AutoMapper en .NET 8.",
        "<b>Pruebas de Integración:</b> Validación de la capa de red con Retrofit 2: endpoints /api/auth/login, /api/productos, /api/ventas, /api/turnoscaja consumiendo payloads JSON contra ASP.NET Core y PostgreSQL en Supabase.",
        "<b>Pruebas de Sistema (End-to-End):</b> Pruebas funcionales en smartphone físico cubriendo flujos continuos desde el arranque en Login, apertura de turno de caja, selección de ítems en POS hasta el registro y descuento de stock en BD.",
        "<b>Pruebas de Usabilidad / Interfaz:</b> Verificación de renderizado adaptable, scroll automático con imePadding ante apertura de teclado virtual, responsividad y visualización clara de alertas.",
        "<b>Pruebas de Seguridad:</b> Verificación de hashing seguro de contraseñas, validación de firma y expiración de tokens JWT Bearer y protección ante peticiones no autenticadas (HTTP 401/403)."
    ]
    for it in niveles_items:
        story.append(Paragraph(f"• {it}", style_bullet))
    story.append(PageBreak())

    # ================= PAGE 6: 2.3 CASOS DE PRUEBA ESENCIALES =================
    story.append(Paragraph("2.3 Matriz de Casos de Prueba Esenciales", style_h1))
    story.append(Paragraph(
        "Casos nucleares diseñados bajo ISO/IEC/IEEE 29119-4 para validar los flujos más críticos de TiendaGo:",
        style_body
    ))
    story.append(Spacer(1, 4))

    data_tc = [
        [
            Paragraph("ID", style_tbl_header),
            Paragraph("Módulo", style_tbl_header),
            Paragraph("Nombre del Caso", style_tbl_header),
            Paragraph("Precondiciones / Pasos", style_tbl_header),
            Paragraph("Resultado Esperado", style_tbl_header),
            Paragraph("Prioridad", style_tbl_header)
        ],
        [
            Paragraph("TC-01", style_tbl_cell_bold),
            Paragraph("Autenticación", style_tbl_cell),
            Paragraph("Login exitoso con emisión JWT", style_tbl_cell),
            Paragraph("Usuario admin activo en BD.<br/>Paso: Ingresar credenciales válidas y pulsar 'Ingresar'.", style_tbl_cell),
            Paragraph("HTTP 200. Token JWT generado y guardado en DataStore. Navegación fluida a Dashboard.", style_tbl_cell),
            Paragraph("Crítica", style_tbl_cell_bold)
        ],
        [
            Paragraph("TC-02", style_tbl_cell_bold),
            Paragraph("Autenticación", style_tbl_cell),
            Paragraph("Rechazo de login inválido", style_tbl_cell),
            Paragraph("Usuario existe.<br/>Paso: Ingresar clave incorrecta en pantalla Login.", style_tbl_cell),
            Paragraph("HTTP 401 Unauthorized. Notificación visual de error. No se persiste sesión.", style_tbl_cell),
            Paragraph("Alta", style_tbl_cell)
        ],
        [
            Paragraph("TC-03", style_tbl_cell_bold),
            Paragraph("Seguridad / RBAC", style_tbl_cell),
            Paragraph("Restricción de vistas y API a Cajero", style_tbl_cell),
            Paragraph("Cajero autenticado.<br/>Paso: Entrar a Catálogo e intentar invocar POST /api/productos.", style_tbl_cell),
            Paragraph("Botón (+) de adición oculto en UI. Solicitud a API responde HTTP 403 Forbidden.", style_tbl_cell),
            Paragraph("Bloqueante", style_tbl_cell_bold)
        ],
        [
            Paragraph("TC-04", style_tbl_cell_bold),
            Paragraph("Catálogo", style_tbl_cell),
            Paragraph("Búsqueda y escaneo por SKU", style_tbl_cell),
            Paragraph("Producto SKU '75010001' activo.<br/>Paso: Escanear código con cámara o buscar texto.", style_tbl_cell),
            Paragraph("Producto encontrado al instante mostrando imagen, precio y stock disponible.", style_tbl_cell),
            Paragraph("Media", style_tbl_cell)
        ],
        [
            Paragraph("TC-05", style_tbl_cell_bold),
            Paragraph("Catálogo", style_tbl_cell),
            Paragraph("Alerta visual de stock crítico", style_tbl_cell),
            Paragraph("Producto con stock = 3 (menor a 5).<br/>Paso: Consultar catálogo de productos.", style_tbl_cell),
            Paragraph("Badge de advertencia visual en rojo/ámbar indicando 'Stock Crítico'.", style_tbl_cell),
            Paragraph("Media", style_tbl_cell)
        ],
        [
            Paragraph("TC-06", style_tbl_cell_bold),
            Paragraph("Turnos Caja", style_tbl_cell),
            Paragraph("Apertura de turno de caja", style_tbl_cell),
            Paragraph("Cajero sin turno abierto.<br/>Paso: Ingresar base $50.00 y presionar 'Abrir Turno'.", style_tbl_cell),
            Paragraph("HTTP 201 Created. Registro insertado en turnos_caja. POS habilitado.", style_tbl_cell),
            Paragraph("Alta", style_tbl_cell)
        ],
        [
            Paragraph("TC-07", style_tbl_cell_bold),
            Paragraph("Punto Venta", style_tbl_cell),
            Paragraph("Venta en efectivo con cálculo de cambio", style_tbl_cell),
            Paragraph("Turno abierto. Carrito con $5.00.<br/>Paso: Seleccionar Efectivo, billete $10 y cobrar.", style_tbl_cell),
            Paragraph("HTTP 201 Created. Venta confirmada, cambio exacto de $5.00 y ticket generado.", style_tbl_cell),
            Paragraph("Bloqueante", style_tbl_cell_bold)
        ],
        [
            Paragraph("TC-08", style_tbl_cell_bold),
            Paragraph("Integridad ACID", style_tbl_cell),
            Paragraph("Bloqueo de venta ante stock insuficiente", style_tbl_cell),
            Paragraph("Producto con stock = 1.<br/>Paso: Intentar procesar venta por 2 unidades.", style_tbl_cell),
            Paragraph("HTTP 400/409 con error de stock insuficiente. Transacción abortada en PostgreSQL.", style_tbl_cell),
            Paragraph("Bloqueante", style_tbl_cell_bold)
        ],
        [
            Paragraph("TC-09", style_tbl_cell_bold),
            Paragraph("Persistencia", style_tbl_cell),
            Paragraph("Decremento atómico en PostgreSQL", style_tbl_cell),
            Paragraph("Stock inicial = 20.<br/>Paso: Completar venta exitosa de 4 unidades.", style_tbl_cell),
            Paragraph("En PostgreSQL el stock_actual del producto disminuye inmediatamente a 16.", style_tbl_cell),
            Paragraph("Crítica", style_tbl_cell_bold)
        ],
        [
            Paragraph("TC-10", style_tbl_cell_bold),
            Paragraph("Turnos Caja", style_tbl_cell),
            Paragraph("Cierre de turno y cuadre de arqueo", style_tbl_cell),
            Paragraph("Turno con ventas registradas.<br/>Paso: Ingresar monto físico contado y cerrar turno.", style_tbl_cell),
            Paragraph("HTTP 200 OK. Cálculo de diferencia (faltante/sobrante) y bloqueo de nuevas ventas.", style_tbl_cell),
            Paragraph("Alta", style_tbl_cell)
        ],
    ]
    # colWidths sum = 36 + 62 + 102 + 123 + 123 + 58 = 504 pt. Priority fits on single line.
    story.append(create_table(data_tc, [36, 62, 102, 123, 123, 58]))
    story.append(PageBreak())

    # ================= PAGE 7: 2.4 SUSPENSIÓN Y 2.5 COMPLETITUD =================
    story.append(Paragraph("2.4 Criterios de suspensión y requisitos de reanudación", style_h1))
    story.append(Paragraph("<b>Criterios de Suspensión:</b>", style_h3))
    suspension_items = [
        "Indisponibilidad del backend alojado en Somee (errores HTTP 500, 502 o caídas del servicio de base de datos PostgreSQL).",
        "Incapacidad de instalar o compilar el APK debido a errores de empaquetado, dependencias o conflictos de firma criptográfica.",
        "Bloqueo total del módulo de autenticación (/api/auth/login) que impida ingresar tanto a Administradores como a Cajeros.",
        "Inconsistencia grave de base de datos que impida la apertura de turnos de caja o el cálculo de inventario."
    ]
    for it in suspension_items:
        story.append(Paragraph(f"• {it}", style_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Requisitos de Reanudación:</b>", style_h3))
    reanudacion_items = [
        "Restablecimiento de la conectividad y validación del endpoint base mediante health check con respuesta HTTP 200.",
        "Entrega de una nueva versión ejecutable (APK) corregida, limpia y firmada por el equipo de desarrollo.",
        "Reversión y reinicio de la base de datos a un estado de datos de prueba conocido y consistente mediante script SeedAdmin.sql."
    ]
    for it in reanudacion_items:
        story.append(Paragraph(f"• {it}", style_bullet))
    story.append(Spacer(1, 8))

    # 2.5 Completitud de la prueba
    story.append(Paragraph("2.5 Completitud de la prueba", style_h1))
    story.append(Paragraph(
        "La fase de pruebas se declarará completa y se concederá el Sign-off cuando se cumplan todas las condiciones siguientes:",
        style_body
    ))
    story.append(Spacer(1, 4))

    data_comp = [
        [Paragraph("Criterio", style_tbl_header), Paragraph("Condición de cumplimiento", style_tbl_header)],
        [Paragraph("Ejecución", style_tbl_cell_bold), Paragraph("100% de los 10 casos de la Suite Oficial ejecutados y documentados con evidencia auditable.", style_tbl_cell)],
        [Paragraph("Aprobación de casos Core", style_tbl_cell_bold), Paragraph("100% en casos Blocker/Critical: TC-01, TC-03, TC-07, TC-08 y TC-09 (autenticación, RBAC, cobro y stock ACID).", style_tbl_cell)],
        [Paragraph("Aprobación general", style_tbl_cell_bold), Paragraph("Mínimo 95%, con el 5% restante limitado a defectos Medium o Low con solución alternativa documentada.", style_tbl_cell)],
        [Paragraph("Defectos críticos", style_tbl_cell_bold), Paragraph("Cero bugs Blocker o Critical abiertos en el seguimiento de incidentes de GitHub.", style_tbl_cell)],
        [Paragraph("Trazabilidad", style_tbl_cell_bold), Paragraph("100% de los requerimientos funcionales (RF01 a RF07) con relación de prueba verificada.", style_tbl_cell)],
        [Paragraph("Código fuente", style_tbl_cell_bold), Paragraph("Cambios estabilizados en la rama main de GitHub, sin conflictos de fusión y probados con el APK homologado.", style_tbl_cell)],
        [Paragraph("Documentación", style_tbl_cell_bold), Paragraph("Entregables completos y Test Summary Report formalmente aprobado y firmado por el QA Lead.", style_tbl_cell)],
    ]
    story.append(create_table(data_comp, [154, 350]))
    story.append(PageBreak())

    # ================= PAGE 8: 3. MATRIZ DE TRAZABILIDAD RTM =================
    story.append(Paragraph("3. Matriz de Trazabilidad de Requisitos (RTM)", style_h1))
    story.append(Paragraph(
        "La matriz vincula directamente los requerimientos funcionales y no funcionales del sistema TiendaGo con los casos de prueba diseñados:",
        style_body
    ))
    story.append(Spacer(1, 6))

    data_rtm = [
        [
            Paragraph("ID Requisito", style_tbl_header),
            Paragraph("Descripción del Requerimiento", style_tbl_header),
            Paragraph("Casos Asoc.", style_tbl_header),
            Paragraph("Nivel", style_tbl_header),
            Paragraph("Severidad", style_tbl_header),
            Paragraph("Técnica", style_tbl_header)
        ],
        [
            Paragraph("RF01", style_tbl_cell_bold),
            Paragraph("Control de Acceso, Autenticación JWT y Roles", style_tbl_cell),
            Paragraph("TC-01, TC-02, TC-03", style_tbl_cell),
            Paragraph("Integración / Seguridad", style_tbl_cell),
            Paragraph("Bloqueante", style_tbl_cell_bold),
            Paragraph("Partición Eq. / RBAC Matrix", style_tbl_cell)
        ],
        [
            Paragraph("RF02", style_tbl_cell_bold),
            Paragraph("Dashboard con Balance Diario y Métricas en Vivo", style_tbl_cell),
            Paragraph("TC-05", style_tbl_cell),
            Paragraph("Sistema / UI", style_tbl_cell),
            Paragraph("Media", style_tbl_cell),
            Paragraph("Transición de Estados", style_tbl_cell)
        ],
        [
            Paragraph("RF03", style_tbl_cell_bold),
            Paragraph("Catálogo con Búsqueda, Filtro y Alerta Crítica", style_tbl_cell),
            Paragraph("TC-04, TC-05", style_tbl_cell),
            Paragraph("Sistema / Funcional", style_tbl_cell),
            Paragraph("Alta", style_tbl_cell),
            Paragraph("Valores Límite (< 5)", style_tbl_cell)
        ],
        [
            Paragraph("RF04", style_tbl_cell_bold),
            Paragraph("Gestión de Productos (Creación, Edición, SKU)", style_tbl_cell),
            Paragraph("TC-03, TC-04, TC-09", style_tbl_cell),
            Paragraph("Integración / API", style_tbl_cell),
            Paragraph("Crítica", style_tbl_cell_bold),
            Paragraph("Partición Eq. / Valores Lím.", style_tbl_cell)
        ],
        [
            Paragraph("RF05", style_tbl_cell_bold),
            Paragraph("Terminal POS, Venta ACID y Descuento de Stock", style_tbl_cell),
            Paragraph("TC-07, TC-08, TC-09", style_tbl_cell),
            Paragraph("E2E / Transaccional", style_tbl_cell),
            Paragraph("Bloqueante", style_tbl_cell_bold),
            Paragraph("Valores Lím. / Concurrencia", style_tbl_cell)
        ],
        [
            Paragraph("RF06", style_tbl_cell_bold),
            Paragraph("Control de Turnos de Caja (Apertura y Cuadre)", style_tbl_cell),
            Paragraph("TC-06, TC-10", style_tbl_cell),
            Paragraph("Sistema / Transaccional", style_tbl_cell),
            Paragraph("Alta", style_tbl_cell),
            Paragraph("Transición de Estados", style_tbl_cell)
        ],
        [
            Paragraph("RF07", style_tbl_cell_bold),
            Paragraph("Historial de Ventas y Emisión de Tickets", style_tbl_cell),
            Paragraph("TC-07", style_tbl_cell),
            Paragraph("Sistema / Funcional", style_tbl_cell),
            Paragraph("Media", style_tbl_cell),
            Paragraph("Pruebas de Persistencia", style_tbl_cell)
        ],
        [
            Paragraph("RNF01", style_tbl_cell_bold),
            Paragraph("Seguridad: Protección con Bearer Token JWT", style_tbl_cell),
            Paragraph("TC-01, TC-03", style_tbl_cell),
            Paragraph("Seguridad / API", style_tbl_cell),
            Paragraph("Bloqueante", style_tbl_cell_bold),
            Paragraph("Análisis de Claims", style_tbl_cell)
        ],
        [
            Paragraph("RNF02", style_tbl_cell_bold),
            Paragraph("Integridad y Atomicidad ACID de Inventario", style_tbl_cell),
            Paragraph("TC-08, TC-09", style_tbl_cell),
            Paragraph("Persistencia / BD", style_tbl_cell),
            Paragraph("Bloqueante", style_tbl_cell_bold),
            Paragraph("Verificación Transaccional", style_tbl_cell)
        ],
    ]
    story.append(create_table(data_rtm, [48, 178, 80, 78, 58, 62]))
    story.append(PageBreak())

    # ================= PAGE 9: 4. NECESIDADES DE RECURSOS =================
    story.append(Paragraph("4. Necesidades de recursos y medio ambiente", style_h1))
    story.append(Paragraph("4.1 Herramientas de prueba", style_h2))
    
    data_tools = [
        [Paragraph("Categoría", style_tbl_header), Paragraph("Herramienta", style_tbl_header), Paragraph("Uso en el proyecto", style_tbl_header)],
        [
            Paragraph("Gestión del ciclo de vida (ALM)", style_tbl_cell_bold),
            Paragraph("Git / GitHub (Repos, Issues, Pull Requests)", style_tbl_cell),
            Paragraph("Control de versiones con Git Flow, ramas develop/feature, revisión obligatoria de código y seguimiento de bugs.", style_tbl_cell)
        ],
        [
            Paragraph("Pruebas de API y Contratos", style_tbl_cell_bold),
            Paragraph("Postman / Thunder Client", style_tbl_cell),
            Paragraph("Validación de endpoints REST (.NET 8), validación de status codes (200, 201, 400, 401, 403), cargas JSON y tokens Bearer JWT.", style_tbl_cell)
        ],
        [
            Paragraph("Desarrollo y Diagnóstico Móvil", style_tbl_cell_bold),
            Paragraph("Android Studio (Logcat, Layout Inspector)", style_tbl_cell),
            Paragraph("Monitoreo de excepciones en tiempo de ejecución, inspección de jerarquía UI en Jetpack Compose e inspección de insets de teclado.", style_tbl_cell)
        ],
        [
            Paragraph("Persistencia y Base de Datos", style_tbl_cell_bold),
            Paragraph("Supabase Dashboard & DBeaver / pgAdmin", style_tbl_cell),
            Paragraph("Inspección de datos relacionales en PostgreSQL, validación de transacciones de stock y ejecución de scripts de reinicio (SeedAdmin.sql).", style_tbl_cell)
        ],
        [
            Paragraph("Automatización y Pruebas Unitarias", style_tbl_cell_bold),
            Paragraph("xUnit / NUnit & Compose UI Test", style_tbl_cell),
            Paragraph("Pruebas unitarias sobre servicios de cálculo (.NET 8) y pruebas automatizadas de interfaz sobre componentes táctiles en Android.", style_tbl_cell)
        ],
        [
            Paragraph("Proyección y Evidencias de UI", style_tbl_cell_bold),
            Paragraph("Scrcpy", style_tbl_cell),
            Paragraph("Visualización, duplicación y grabación en alta definición de la pantalla del smartphone físico para documentar evidencias de prueba.", style_tbl_cell)
        ],
    ]
    story.append(create_table(data_tools, [114, 120, 270]))
    story.append(Spacer(1, 6))

    # 4.2 Entorno de prueba
    story.append(Paragraph("4.2 Entorno de prueba", style_h2))
    data_env = [
        [Paragraph("Componente", style_tbl_header), Paragraph("Requisito", style_tbl_header)],
        [Paragraph("Plataforma Cliente Móvil (Física)", style_tbl_cell_bold), Paragraph("Smartphone Samsung Galaxy (SM-A556E) con Android 14 / One UI 6, y dispositivo Xiaomi Redmi Note con Android 13.", style_tbl_cell)],
        [Paragraph("Emulador de Soporte Virtual", style_tbl_cell_bold), Paragraph("Android Studio Virtual Device (Pixel 8 Pro - API Level 34 / Android 14).", style_tbl_cell)],
        [Paragraph("Servidor de Aplicación (Backend)", style_tbl_cell_bold), Paragraph("ASP.NET Core Web API 8.0, runtime .NET 8 alojado en servidor Somee (http://TiendaGO.somee.com/) y Kestrel local de contingencia.", style_tbl_cell)],
        [Paragraph("Base de Datos", style_tbl_cell_bold), Paragraph("PostgreSQL 15 en la nube alojado en Supabase (AWS us-west-2 pooler con SSL Mode Require). Instancia aislada TiendaGo_QA.", style_tbl_cell)],
        [Paragraph("Datos semilla actuales", style_tbl_cell_bold), Paragraph("Roles Administrador (1) y Cajero (2). Usuario admin@tiendago.com y cajero@tiendago.com. Catálogo con 20 productos de prueba y stock conocido.", style_tbl_cell)],
        [Paragraph("Estación de trabajo QA", style_tbl_cell_bold), Paragraph("Procesador de 64 bits a 3.4 GHz, 16 GB de RAM, disco SSD NVMe y conexión estable de banda ancha a Internet.", style_tbl_cell)],
    ]
    story.append(create_table(data_env, [154, 350]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Dependencias y riesgos del entorno:</b>", style_h3))
    data_risk = [
        [Paragraph("Riesgo", style_tbl_header), Paragraph("Probabilidad", style_tbl_header), Paragraph("Impacto", style_tbl_header), Paragraph("Mitigación", style_tbl_header)],
        [
            Paragraph("Indisponibilidad del hosting Somee (Timeouts HTTP 500 / 502)", style_tbl_cell_bold),
            Paragraph("Media", style_tbl_cell),
            Paragraph("Alto", style_tbl_cell),
            Paragraph("Configuración de servidor de contingencia local mediante Kestrel / IIS Express en red local para pruebas.", style_tbl_cell)
        ],
        [
            Paragraph("Corrupción de datos por pruebas destructivas anteriores", style_tbl_cell_bold),
            Paragraph("Media", style_tbl_cell),
            Paragraph("Alto", style_tbl_cell),
            Paragraph("Base de datos aislada TiendaGo_QA, scripts seeders automatizados y reinicio rápido antes de cada suite.", style_tbl_cell)
        ],
        [
            Paragraph("Bloqueo del teclado virtual sobre inputs en pantallas pequeñas", style_tbl_cell_bold),
            Paragraph("Alta", style_tbl_cell),
            Paragraph("Medio", style_tbl_cell),
            Paragraph("Implementación y verificación estricta de modificadores imePadding() y rememberScrollState() en Compose.", style_tbl_cell)
        ],
        [
            Paragraph("Falla de compilación o firma de APKs móviles", style_tbl_cell_bold),
            Paragraph("Baja", style_tbl_cell),
            Paragraph("Alto", style_tbl_cell),
            Paragraph("Proceso de compilación estandarizado mediante Gradle wrapper en Android Studio y verificación de firma SHA-256.", style_tbl_cell)
        ],
    ]
    story.append(create_table(data_risk, [144, 70, 60, 230]))
    story.append(PageBreak())

    # ================= PAGE 10: 5. TÉRMINOS / ACRÓNIMOS =================
    story.append(Paragraph("Términos / Acrónimos", style_h1))
    story.append(Paragraph("Glosario de terminología y conceptos técnicos empleados a lo largo del documento:", style_body))
    story.append(Spacer(1, 4))

    data_terms = [
        [Paragraph("Término", style_tbl_header), Paragraph("Definición", style_tbl_header)],
        [Paragraph("ACID", style_tbl_cell_bold), Paragraph("Atomicity, Consistency, Isolation, Durability: conjunto de propiedades que garantizan transacciones seguras en BD sin inconsistencias de stock.", style_tbl_cell)],
        [Paragraph("ALM", style_tbl_cell_bold), Paragraph("Application Lifecycle Management: gestión integral del ciclo de vida de la aplicación.", style_tbl_cell)],
        [Paragraph("ANR", style_tbl_cell_bold), Paragraph("Application Not Responding: bloqueo del hilo principal de Android que detiene la interactividad de la interfaz.", style_tbl_cell)],
        [Paragraph("API", style_tbl_cell_bold), Paragraph("Application Programming Interface: interfaz que permite la comunicación entre la app móvil y el servidor backend.", style_tbl_cell)],
        [Paragraph("APK", style_tbl_cell_bold), Paragraph("Android Package Kit: paquete comprimido ejecutable instalable en el sistema operativo Android.", style_tbl_cell)],
        [Paragraph("AUT", style_tbl_cell_bold), Paragraph("Application Under Test: aplicación bajo prueba (TiendaGo Mobile & API).", style_tbl_cell)],
        [Paragraph("Boundary Value Analysis", style_tbl_cell_bold), Paragraph("Análisis de valores límite: técnica de prueba de caja negra que evalúa los extremos de rangos (ej. stock 0, 1 y umbral mínimo 5).", style_tbl_cell)],
        [Paragraph("Coil", style_tbl_cell_bold), Paragraph("Biblioteca de carga y renderizado reactivo de imágenes en Android optimizada para Jetpack Compose y corrutinas de Kotlin.", style_tbl_cell)],
        [Paragraph("DataStore", style_tbl_cell_bold), Paragraph("Solución moderna de almacenamiento local seguro de pares clave-valor en Android, empleada para persistir el token JWT.", style_tbl_cell)],
        [Paragraph("DoD", style_tbl_cell_bold), Paragraph("Definition of Done: criterios formales para considerar finalizada una tarea o historia de usuario.", style_tbl_cell)],
        [Paragraph("DTO", style_tbl_cell_bold), Paragraph("Data Transfer Object: objeto simple utilizado para encapsular y transportar datos entre cliente y servidor.", style_tbl_cell)],
        [Paragraph("EF Core", style_tbl_cell_bold), Paragraph("Entity Framework Core: ORM de Microsoft para mapeo objeto-relacional y acceso a datos en .NET 8.", style_tbl_cell)],
        [Paragraph("IME", style_tbl_cell_bold), Paragraph("Input Method Editor: mecanismo del sistema operativo que gestiona el teclado virtual en pantalla.", style_tbl_cell)],
        [Paragraph("ISO/IEC/IEEE 29119", style_tbl_cell_bold), Paragraph("Familia de normas internacionales que rigen el vocabulario, procesos, documentación y técnicas de prueba de software.", style_tbl_cell)],
        [Paragraph("Jetpack Compose", style_tbl_cell_bold), Paragraph("Kit de herramientas declarativo moderno de Google para el desarrollo de interfaces nativas en Android.", style_tbl_cell)],
        [Paragraph("JWT", style_tbl_cell_bold), Paragraph("JSON Web Token: estándar abierto para autenticación y transmisión compacta y segura de información mediante tokens firmados.", style_tbl_cell)],
        [Paragraph("PBI / US", style_tbl_cell_bold), Paragraph("Product Backlog Item / User Story: elemento del backlog o historia de usuario del proyecto.", style_tbl_cell)],
        [Paragraph("POS", style_tbl_cell_bold), Paragraph("Point of Sale: terminal de punto de venta utilizado para facturación y cobros comerciales en comercios.", style_tbl_cell)],
        [Paragraph("QA", style_tbl_cell_bold), Paragraph("Quality Assurance: aseguramiento de la calidad del software.", style_tbl_cell)],
        [Paragraph("RBAC", style_tbl_cell_bold), Paragraph("Role-Based Access Control: control de acceso basado en roles asignados al usuario (Administrador vs Cajero).", style_tbl_cell)],
        [Paragraph("RLS", style_tbl_cell_bold), Paragraph("Row Level Security: políticas de seguridad a nivel de fila en el motor PostgreSQL de Supabase.", style_tbl_cell)],
        [Paragraph("RTM", style_tbl_cell_bold), Paragraph("Requirements Traceability Matrix: matriz de trazabilidad que vincula requisitos con casos de prueba.", style_tbl_cell)],
        [Paragraph("Sign-off", style_tbl_cell_bold), Paragraph("Aprobación técnica formal de cierre y autorización de liberación de la fase de pruebas emitida por el QA Lead.", style_tbl_cell)],
        [Paragraph("Supabase", style_tbl_cell_bold), Paragraph("Plataforma Backend-as-a-Service basada en PostgreSQL que provee la persistencia en la nube para TiendaGo.", style_tbl_cell)],
    ]
    story.append(create_table(data_terms, [134, 370]))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generated successfully:", OUTPUT_PDF)

if __name__ == "__main__":
    build_pdf()
