import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

OUTPUT_PDF = os.path.abspath("Pruebas_de_Aceptacion_UAT_TiendaGo.pdf")

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
        
        # Running footer
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#666666"))
        self.drawString(36, 25, "TiendaGo POS Móvil & Web API | Matriz de Pruebas de Aceptación (UAT) - Azure DevOps")
        self.drawRightString(576, 25, f"Página {page_num} de {total_pages}")
        self.setStrokeColor(colors.HexColor("#d0d0d0"))
        self.setLineWidth(0.5)
        self.line(36, 35, 576, 35)
            
        self.restoreState()

def build_pdf():
    # 36 pt margins (0.5 in). Printable width = 612 - 72 = 540 pt.
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom typography
    style_main_title = ParagraphStyle(
        'MainTitle',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#111111"),
        spaceAfter=4
    )
    
    style_project_meta = ParagraphStyle(
        'ProjectMeta',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#222222"),
        spaceAfter=2
    )

    style_section_badge = ParagraphStyle(
        'SectionBadge',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1b587a"),
        spaceBefore=3,
        spaceAfter=6
    )

    style_th = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white,
        alignment=1  # Centered
    )

    style_td_center = ParagraphStyle(
        'TableCellCenter',
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#111111"),
        alignment=1
    )

    style_td_bold_center = ParagraphStyle(
        'TableCellBoldCenter',
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#111111"),
        alignment=1
    )

    style_td_left = ParagraphStyle(
        'TableCellLeft',
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#111111"),
        alignment=0  # Left
    )

    # Test cases dataset
    data_tc = [
        {
            "id": "TC-01",
            "caso": "Autenticación exitosa con JWT y claims de rol",
            "desc": "Validar verificación criptográfica de contraseña contra hash BCrypt y emisión de Bearer Token JWT con claims de usuario y rol Administrador.",
            "fecha": "14/10/2026",
            "area": "Seguridad y Acceso",
            "func": "Autenticación Segura y Claims (US-AUTH-01)",
            "entrada": "Navegar a Login; ingresar correo 'admin@tiendago.com', contraseña 'Admin123*' y presionar 'Iniciar Sesión'.",
            "esperado": "AuthService valida hash BCrypt, retorna HTTP 200 OK con Bearer Token JWT; la app persiste el token en DataStore Preferences y redirige al Dashboard.",
            "ambiente": ".NET 8, ASP.NET Core Web API, PostgreSQL (Supabase TiendaGo_DB_QA), Android 14 (Samsung SM-A556E / Emulador Pixel 8).",
            "procedimientos": "Usuario administrador semilla activo en BD TiendaGo_DB_QA con clave hasheada en BCrypt.",
            "dependencias": "Ninguna",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2010 en Azure Boards y Caso #2101 en Test Plan #2100 (Suite #2101)."
        },
        {
            "id": "TC-02",
            "caso": "Rechazo de autenticación con contraseña incorrecta",
            "desc": "Verificar denegación de acceso ante credenciales no concordantes impidiendo emisión de token y mostrando feedback al usuario.",
            "fecha": "14/10/2026",
            "area": "Seguridad y Acceso",
            "func": "Autenticación Segura y Claims (US-AUTH-01)",
            "entrada": "Ingresar correo 'admin@tiendago.com', contraseña 'ClaveErronea999!' y presionar 'Iniciar Sesión'.",
            "esperado": "La API retorna código HTTP 401 Unauthorized; la interfaz en Jetpack Compose muestra Snackbar de credenciales inválidas sin almacenar token.",
            "ambiente": ".NET 8, ASP.NET Core Web API, Cliente Móvil Android Compose.",
            "procedimientos": "Usuario registrado en BD; conexión de red activa hacia Somee / Backend local.",
            "dependencias": "TC-01",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2010 en Azure Boards y Caso #2102 en Test Plan #2100 (Suite #2101)."
        },
        {
            "id": "TC-03",
            "caso": "Restricción de permisos RBAC e intercepción HTTP 403 para Cajero",
            "desc": "Verificar control de acceso RBAC bloqueando mutación de catálogo y rutas administrativas a usuarios con rol Cajero.",
            "fecha": "14/10/2026",
            "area": "Seguridad y Acceso",
            "func": "Control de Acceso RBAC (US-SEC-02)",
            "entrada": "Autenticar usuario 'cajero@tiendago.com'; invocar POST /api/productos con payload de nuevo producto inyectando token de cajero.",
            "esperado": "Ocultamiento del FAB (+) en app móvil; middleware de autorización intercepta petición HTTP y retorna código 403 Forbidden.",
            "ambiente": ".NET 8, ASP.NET Core Authorization Policy, Postman / Thunder Client.",
            "procedimientos": "Usuario Cajero semilla activo en BD con rol ID 2.",
            "dependencias": "TC-01",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2011 en Azure Boards y Caso #2103 en Test Plan #2100 (Suite #2101). Criterio de seguridad no negociable."
        },
        {
            "id": "TC-04",
            "caso": "Búsqueda dinámica y escaneo óptico por SKU",
            "desc": "Validar localización inmediata de producto mediante lectura óptica de código de barras/QR y filtro dinámico por texto/SKU.",
            "fecha": "14/10/2026",
            "area": "Catálogo y Ocupación",
            "func": "Búsqueda y Escáner SKU (US-CAT-01)",
            "entrada": "Ingresar a Catálogo de Productos; activar escáner de cámara sobre código impreso o digitar SKU '75010001'.",
            "esperado": "El catálogo filtra en tiempo real y despliega la tarjeta del producto con foto (Coil), nombre, SKU, precio ($1.25) y stock disponible.",
            "ambiente": "Android 14 con cámara operativa, Jetpack Compose, Backend .NET 8 Somee.",
            "procedimientos": "Producto con SKU '75010001' registrado y activo en base de datos.",
            "dependencias": "Ninguna",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2015 en Azure Boards y Caso #2104 en Test Plan #2100 (Suite #2102)."
        },
        {
            "id": "TC-05",
            "caso": "Alerta visual de stock crítico (menor a 5 unidades)",
            "desc": "Verificar despliegue condicional de badge cromático de advertencia cuando las existencias igualan o descienden del umbral mínimo.",
            "fecha": "14/10/2026",
            "area": "Catálogo y Ocupación",
            "func": "Alerta de Stock Crítico (US-CAT-02)",
            "entrada": "Navegar a Catálogo de Productos; ubicar producto 'Leche Entera 1L' configurado con stock_actual = 3 y stock_minimo = 5.",
            "esperado": "La tarjeta del producto muestra un badge visual ámbar/rojo con texto 'Stock Crítico: 3 unidades restantes', alertando al operador.",
            "ambiente": "Android 14, Compose UI, BD PostgreSQL Supabase con datos semilla.",
            "procedimientos": "Producto configurado con stock_actual <= stock_minimo en tabla 'productos'.",
            "dependencias": "TC-04",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2016 en Azure Boards y Caso #2105 en Test Plan #2100 (Suite #2102)."
        },
        {
            "id": "TC-06",
            "caso": "Apertura de turno de caja con monto base inicial",
            "desc": "Validar registro de apertura de jornada de caja vinculando usuario cajero con monto base en efectivo para habilitar ventas.",
            "fecha": "14/10/2026",
            "area": "Operaciones / Reservas",
            "func": "Control de Turnos de Caja (US-TUR-01)",
            "entrada": "Ingresar a Gestión de Turno; ingresar Monto Base Inicial '$50.00' y presionar 'Abrir Turno de Caja'.",
            "esperado": "Retorna HTTP 201 Created con entidad TurnoCaja; estado cambia a 'Abierto' y se desbloquea el acceso a la Terminal POS.",
            "ambiente": ".NET 8, PostgreSQL (Supabase TiendaGo_DB_QA), Android Compose.",
            "procedimientos": "Cajero sin turno abierto previo en BD.",
            "dependencias": "TC-01",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2020 en Azure Boards y Caso #2106 en Test Plan #2100 (Suite #2103)."
        },
        {
            "id": "TC-07",
            "caso": "Cierre de turno, arqueo ciego y cuadre de caja",
            "desc": "Validar cálculo automatizado de arqueo de caja contrastando efectivo declarado contra ventas del sistema determinando diferencias.",
            "fecha": "14/10/2026",
            "area": "Operaciones / Reservas",
            "func": "Cierre y Arqueo Ciego (US-TUR-02)",
            "entrada": "Navegar a Cierre de Turno; ingresar Monto Declarado contado '$85.00' (Esperado: $50 base + $35 ventas) y presionar 'Finalizar Turno'.",
            "esperado": "Retorna HTTP 200 OK; diferencia_cuadre = $0.00 (cuadre exacto), estado pasa a 'Cerrado' y se inhabilitan nuevas ventas.",
            "ambiente": ".NET 8, PostgreSQL (Supabase TiendaGo_DB_QA).",
            "procedimientos": "Turno activo con ventas registradas durante el turno.",
            "dependencias": "TC-06",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2021 en Azure Boards y Caso #2107 en Test Plan #2100 (Suite #2103)."
        },
        {
            "id": "TC-08",
            "caso": "Venta en efectivo, cálculo de IVA y cambio exacto",
            "desc": "Validar flujo integral de compra en terminal POS con cálculo aritmético de impuestos (13%), cambio de efectivo y ticket correlativo.",
            "fecha": "14/10/2026",
            "area": "Tarifas y Facturación",
            "func": "Terminal POS y Venta Efectivo (US-POS-01)",
            "entrada": "Seleccionar 2 unidades de 'Bebida Energizante' ($2.50 c/u, Total: $5.00); cobrar con atajo de billete '$10.00' en efectivo y confirmar.",
            "esperado": "HTTP 201 Created; pantalla confirma venta con Subtotal: $4.42, IVA (13%): $0.58, Cambio: $5.00 y genera correlativo único (ej. TCK-2026-0001).",
            "ambiente": ".NET 8, PostgreSQL (Supabase TiendaGo_DB_QA), Android Jetpack Compose.",
            "procedimientos": "Turno de caja en estado 'Abierto' y stock disponible en catálogo.",
            "dependencias": "TC-06",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2025 en Azure Boards y Caso #2108 en Test Plan #2100 (Suite #2104). Criterio transaccional nuclear."
        },
        {
            "id": "TC-09",
            "caso": "Control transaccional ACID ante stock insuficiente",
            "desc": "Verificar que el servicio VentaService aborte la transacción con Rollback atómico si la cantidad demandada excede el stock disponible.",
            "fecha": "14/10/2026",
            "area": "Tarifas y Facturación",
            "func": "Atomicidad ACID y Anti-Sobrevendimiento (US-POS-02)",
            "entrada": "Producto con stock_actual = 1; enviar petición POST /api/ventas solicitando cantidad = 2 unidades del producto.",
            "esperado": "La API rechaza la venta retornando HTTP 409 Conflict con mensaje 'Stock insuficiente para el producto'; Rollback completo sin alteración de datos.",
            "ambiente": ".NET 8, Transacción atómica Npgsql / EF Core, PostgreSQL Supabase.",
            "procedimientos": "Registro de producto con exactamente 1 unidad en stock en BD QA.",
            "dependencias": "TC-08",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2026 en Azure Boards y Caso #2109 en Test Plan #2100 (Suite #2104). Verificación estricta de propiedad ACID."
        },
        {
            "id": "TC-10",
            "caso": "Decremento físico atómico de existencias en PostgreSQL",
            "desc": "Constatar consistencia de persistencia verificando que el stock en la tabla 'productos' se actualice exactamente restando unidades vendidas.",
            "fecha": "14/10/2026",
            "area": "Tarifas y Facturación",
            "func": "Persistencia y Descuento Atómico (US-POS-03)",
            "entrada": "Producto con stock inicial = 15; procesar venta confirmada de 3 unidades vía POS; consultar SELECT stock_actual FROM productos.",
            "esperado": "El registro en PostgreSQL refleja exactamente stock_actual = 12 unidades y se registra la línea correspondiente en detalles_venta.",
            "ambiente": "PostgreSQL 15 (Supabase TiendaGo_DB_QA), DBeaver / psql.",
            "procedimientos": "Producto con stock controlado previo a la prueba.",
            "dependencias": "TC-08",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2027 en Azure Boards y Caso #2110 en Test Plan #2100 (Suite #2104)."
        },
        {
            "id": "TC-11",
            "caso": "Retorno exitoso HTTP 200 en GET /api/dashboard/resumen",
            "desc": "Validar consolidación financiera del día retornando total facturado, órdenes procesadas y recuento de alertas de inventario.",
            "fecha": "14/10/2026",
            "area": "Reportes y Auditoría",
            "func": "Balance Diario y Métricas (US-DASH-01)",
            "entrada": "Petición GET a /api/dashboard/resumen con Bearer Token JWT de Administrador en cabecera Authorization.",
            "esperado": "Retorna HTTP 200 OK con payload JSON estructurado conteniendo totalVentas, cantidadTransacciones y lista de productosBajoStock.",
            "ambiente": ".NET 8 Runtime, BD TiendaGo_DB_QA, Postman / Thunder Client.",
            "procedimientos": "Ventas registradas en la fecha actual en la base de datos de pruebas.",
            "dependencias": "TC-08",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2030 en Azure Boards y Caso #2111 en Test Plan #2100 (Suite #2105)."
        },
        {
            "id": "TC-12",
            "caso": "Bloqueo de cobro en POS sin turno de caja activo",
            "desc": "Verificar regla de negocio que prohíbe facturar transacciones de venta si el operador no posee un turno de caja en estado Abierto.",
            "fecha": "14/10/2026",
            "area": "Operaciones / Reservas",
            "func": "Control de Turnos de Caja (US-TUR-03)",
            "entrada": "Con usuario cajero sin turno abierto, intentar confirmar cobro de $3.00 en TerminalCajaView o enviar POST /api/ventas con idTurno = 0.",
            "esperado": "Retorna HTTP 400 Bad Request / 409 Conflict con mensaje 'Se requiere un turno de caja abierto para registrar ventas'; la app bloquea el botón de cobro.",
            "ambiente": ".NET 8 Web API, Cliente Android Compose.",
            "procedimientos": "Cajero con estado de turno cerrado o nulo.",
            "dependencias": "TC-01",
            "obtenido": "Pendiente de ejecución (Fase de Planificación)",
            "estado": "En Planificación",
            "ult_fecha": "14/10/2026",
            "obs": "Planificado y trazado a PBI #2020 en Azure Boards y Caso #2112 en Test Plan #2100 (Suite #2103)."
        }
    ]

    story = []

    def build_header_block(section_subtitle):
        elems = []
        elems.append(Paragraph("Pruebas de Aceptación (UAT)", style_main_title))
        elems.append(Paragraph("<b>Proyecto:</b> TiendaGo (Punto de Venta POS Móvil y Gestión de Inventario Express)", style_project_meta))
        elems.append(Paragraph("<b>Ciclo de Pruebas:</b> Planificación de Casos de Aceptación en Azure DevOps", style_project_meta))
        elems.append(Paragraph(section_subtitle, style_section_badge))
        elems.append(Spacer(1, 4))
        return elems

    tbl_base_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1b587a")),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 3.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#444444")),
    ]

    # =========================================================================
    # SECCIÓN 1: Identificación y Clasificación (Columnas 1 - 5)
    # Total printable width = 540 pt
    # =========================================================================
    story.extend(build_header_block("Parte 1: Identificación de Casos, Descripción y Área Funcional"))

    headers_1 = [
        Paragraph("Id", style_th),
        Paragraph("Caso de Prueba", style_th),
        Paragraph("Descripción", style_th),
        Paragraph("Fecha", style_th),
        Paragraph("Área Funcional / Sub proceso", style_th)
    ]
    widths_1 = [38, 122, 210, 50, 120]  # Sum = 540 pt

    rows_1 = [headers_1]
    for tc in data_tc:
        rows_1.append([
            Paragraph(tc["id"], style_td_bold_center),
            Paragraph(tc["caso"], style_td_left),
            Paragraph(tc["desc"], style_td_left),
            Paragraph(tc["fecha"], style_td_center),
            Paragraph(tc["area"], style_td_left)
        ])

    table_1 = Table(rows_1, colWidths=widths_1, repeatRows=1)
    table_1.setStyle(TableStyle(tbl_base_style))
    story.append(table_1)
    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 2: Especificación y Entorno (Columnas 6 - 9)
    # =========================================================================
    story.extend(build_header_block("Parte 2: Requerimientos, Entradas, Resultados y Entorno de Prueba"))

    headers_2 = [
        Paragraph("Id", style_th),
        Paragraph("Funcionalidad / Característica", style_th),
        Paragraph("Datos / Acciones de Entrada", style_th),
        Paragraph("Resultado Esperado", style_th),
        Paragraph("Requerimientos de Ambiente de prueba", style_th)
    ]
    widths_2 = [35, 115, 145, 145, 100]  # Sum = 540 pt

    rows_2 = [headers_2]
    for tc in data_tc:
        rows_2.append([
            Paragraph(tc["id"], style_td_bold_center),
            Paragraph(tc["func"], style_td_left),
            Paragraph(tc["entrada"], style_td_left),
            Paragraph(tc["esperado"], style_td_left),
            Paragraph(tc["ambiente"], style_td_left)
        ])

    table_2 = Table(rows_2, colWidths=widths_2, repeatRows=1)
    table_2.setStyle(TableStyle(tbl_base_style))
    story.append(table_2)
    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 3: Procedimientos y Estado (Columnas 10 - 14)
    # =========================================================================
    story.extend(build_header_block("Parte 3: Procedimientos Especiales, Dependencias y Estado de Ejecución"))

    headers_3 = [
        Paragraph("Id", style_th),
        Paragraph("Procedimientos especiales requeridos", style_th),
        Paragraph("Dependencias con otros casos de prueba", style_th),
        Paragraph("Resultado Obtenido", style_th),
        Paragraph("Estado", style_th),
        Paragraph("Última Fecha de Estado", style_th)
    ]
    widths_3 = [35, 135, 75, 150, 75, 70]  # Sum = 540 pt

    rows_3 = [headers_3]
    for tc in data_tc:
        rows_3.append([
            Paragraph(tc["id"], style_td_bold_center),
            Paragraph(tc["procedimientos"], style_td_left),
            Paragraph(tc["dependencias"], style_td_center),
            Paragraph(tc["obtenido"], style_td_left),
            Paragraph(tc["estado"], style_td_center),
            Paragraph(tc["ult_fecha"], style_td_center)
        ])

    table_3 = Table(rows_3, colWidths=widths_3, repeatRows=1)
    table_3.setStyle(TableStyle(tbl_base_style))
    story.append(table_3)
    story.append(PageBreak())

    # =========================================================================
    # SECCIÓN 4: Trazabilidad y Observaciones (Columna 15 + Contexto)
    # =========================================================================
    story.extend(build_header_block("Parte 4: Trazabilidad Azure DevOps & Observaciones"))

    headers_4 = [
        Paragraph("Id", style_th),
        Paragraph("Caso de Prueba", style_th),
        Paragraph("Funcionalidad Vinculada", style_th),
        Paragraph("Observaciones / Trazabilidad Azure DevOps", style_th)
    ]
    widths_4 = [38, 142, 140, 220]  # Sum = 540 pt

    rows_4 = [headers_4]
    for tc in data_tc:
        rows_4.append([
            Paragraph(tc["id"], style_td_bold_center),
            Paragraph(tc["caso"], style_td_left),
            Paragraph(tc["func"], style_td_left),
            Paragraph(tc["obs"], style_td_left)
        ])

    table_4 = Table(rows_4, colWidths=widths_4, repeatRows=1)
    table_4.setStyle(TableStyle(tbl_base_style))
    story.append(table_4)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()
