import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_uat_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pruebas de Aceptación (UAT)"
    
    # Ensure grid lines are visible
    ws.views.sheetView[0].showGridLines = True

    # Palette
    HEADER_FILL = PatternFill(start_color="1B587A", end_color="1B587A", fill_type="solid")
    WHITE_BOLD = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    TITLE_FONT = Font(name="Calibri", size=14, bold=True, color="111111")
    META_BOLD = Font(name="Calibri", size=10, bold=True, color="222222")
    META_REGULAR = Font(name="Calibri", size=10, bold=False, color="333333")
    CELL_FONT = Font(name="Calibri", size=9, color="111111")
    CELL_BOLD = Font(name="Calibri", size=9, bold=True, color="111111")

    THIN_BORDER = Border(
        left=Side(style='thin', color='777777'),
        right=Side(style='thin', color='777777'),
        top=Side(style='thin', color='777777'),
        bottom=Side(style='thin', color='777777')
    )

    # 1. Header Information
    ws["B2"] = "Pruebas de Aceptación (UAT)"
    ws["B2"].font = TITLE_FONT

    ws["B3"] = "Proyecto: TiendaGo (Punto de Venta POS Móvil y Gestión de Inventario Express)"
    ws["B3"].font = META_BOLD

    ws["B4"] = "Ciclo de Pruebas: Planificación de Casos de Aceptación en Azure DevOps"
    ws["B4"].font = META_BOLD

    # 2. Table Headers (Row 6)
    headers = [
        "Id",
        "Caso de Prueba",
        "Descripción",
        "Fecha",
        "Área Funcional / Sub proceso",
        "Funcionalidad / Característica",
        "Datos / Acciones de Entrada",
        "Resultado Esperado",
        "Requerimientos de Ambiente de prueba",
        "Procedimientos especiales requeridos",
        "Dependencias con otros casos de prueba",
        "Resultado Obtenido",
        "Estado",
        "Última Fecha de Estado",
        "Observaciones"
    ]

    header_row = 6
    start_col = 2  # Column B

    for idx, header in enumerate(headers):
        col_num = start_col + idx
        cell = ws.cell(row=header_row, column=col_num, value=header)
        cell.fill = HEADER_FILL
        cell.font = WHITE_BOLD
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER

    ws.row_dimensions[header_row].height = 36

    # 3. Data Rows
    test_cases = [
        [
            "TC-01",
            "Autenticación exitosa de Administrador con JWT y claims de rol",
            "Validar verificación criptográfica de contraseña contra hash BCrypt y emisión de Bearer Token JWT con claims de usuario y rol 'Administrador'.",
            "14/10/2026",
            "Seguridad y Acceso",
            "Autenticación Segura y Claims (US-AUTH-01)",
            "Navegar a Login; ingresar correo 'admin@tiendago.com', contraseña 'Admin123*' y presionar 'Iniciar Sesión'.",
            "AuthService valida hash BCrypt, retorna HTTP 200 OK con Bearer Token JWT; la app persiste el token en DataStore Preferences y redirige al Dashboard.",
            ".NET 8, ASP.NET Core Web API, PostgreSQL (Supabase TiendaGo_DB_QA), Android 14 (Samsung SM-A556E / Emulador Pixel 8 Pro).",
            "Usuario administrador semilla activo en BD TiendaGo_DB_QA con clave hasheada en BCrypt.",
            "Ninguna",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2010 en Azure Boards y Caso #2101 en Test Plan #2100 (Suite #2101)."
        ],
        [
            "TC-02",
            "Rechazo de autenticación con contraseña incorrecta",
            "Verificar denegación de acceso ante credenciales no concordantes impidiendo emisión de token y mostrando feedback al usuario.",
            "14/10/2026",
            "Seguridad y Acceso",
            "Autenticación Segura y Claims (US-AUTH-01)",
            "Ingresar correo 'admin@tiendago.com', contraseña 'ClaveErronea999!' y presionar 'Iniciar Sesión'.",
            "La API retorna código HTTP 401 Unauthorized; la interfaz en Jetpack Compose muestra Snackbar de credenciales inválidas sin almacenar token.",
            ".NET 8, ASP.NET Core Web API, Cliente Móvil Android Compose.",
            "Usuario registrado en BD; conexión de red activa hacia Somee / Backend local.",
            "TC-01",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2010 en Azure Boards y Caso #2102 en Test Plan #2100 (Suite #2101)."
        ],
        [
            "TC-03",
            "Restricción de permisos RBAC e intercepción HTTP 403 para rol Cajero",
            "Verificar control de acceso RBAC bloqueando mutación de catálogo y rutas administrativas a usuarios con rol Cajero.",
            "14/10/2026",
            "Seguridad y Acceso",
            "Control de Acceso RBAC (US-SEC-02)",
            "Autenticar usuario 'cajero@tiendago.com'; invocar POST /api/productos con payload de nuevo producto inyectando token de cajero.",
            "Ocultamiento del FAB (+) en app móvil; middleware de autorización intercepta petición HTTP y retorna código 403 Forbidden.",
            ".NET 8, ASP.NET Core Authorization Policy, Postman / Thunder Client.",
            "Usuario Cajero semilla activo en BD con rol ID 2.",
            "TC-01",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2011 en Azure Boards y Caso #2103 en Test Plan #2100 (Suite #2101). Criterio de seguridad no negociable."
        ],
        [
            "TC-04",
            "Búsqueda dinámica y escaneo óptico de producto por SKU",
            "Validar localización inmediata de producto mediante lectura óptica de código de barras/QR y filtro dinámico por texto/SKU.",
            "14/10/2026",
            "Catálogo e Inventario",
            "Búsqueda y Escáner SKU (US-CAT-01)",
            "Ingresar a Catálogo de Productos; activar escáner de cámara sobre código impreso o digitar SKU '75010001'.",
            "El catálogo filtra en tiempo real y despliega la tarjeta del producto con foto (Coil), nombre, SKU, precio ($1.25) y stock disponible.",
            "Android 14 con cámara operativa, Jetpack Compose, Backend .NET 8 Somee.",
            "Producto con SKU '75010001' registrado y activo en base de datos.",
            "Ninguna",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2015 en Azure Boards y Caso #2104 en Test Plan #2100 (Suite #2102)."
        ],
        [
            "TC-05",
            "Alerta visual reactiva de stock crítico (menor a 5 unidades)",
            "Verificar despliegue condicional de badge cromático de advertencia cuando las existencias igualan o descienden del umbral mínimo.",
            "14/10/2026",
            "Catálogo e Inventario",
            "Alerta de Stock Crítico (US-CAT-02)",
            "Navegar a Catálogo de Productos; ubicar producto 'Leche Entera 1L' configurado con stock_actual = 3 y stock_minimo = 5.",
            "La tarjeta del producto muestra un badge visual ámbar/rojo con texto 'Stock Crítico: 3 unidades restantes', alertando al operador.",
            "Android 14, Compose UI, BD PostgreSQL Supabase con datos semilla.",
            "Producto configurado con stock_actual <= stock_minimo en tabla 'productos'.",
            "TC-04",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2016 en Azure Boards y Caso #2105 en Test Plan #2100 (Suite #2102)."
        ],
        [
            "TC-06",
            "Apertura de turno de caja con monto base inicial",
            "Validar registro de apertura de jornada de caja vinculando usuario cajero con monto base en efectivo para habilitar ventas.",
            "14/10/2026",
            "Turnos de Caja",
            "Control de Turnos de Caja (US-TUR-01)",
            "Ingresar a Gestión de Turno; ingresar Monto Base Inicial '$50.00' y presionar 'Abrir Turno de Caja'.",
            "Retorna HTTP 201 Created con entidad TurnoCaja; estado cambia a 'Abierto' y se desbloquea el acceso a la Terminal POS.",
            ".NET 8, PostgreSQL (Supabase TiendaGo_DB_QA), Android Compose.",
            "Cajero sin turno abierto previo en BD.",
            "TC-01",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2020 en Azure Boards y Caso #2106 en Test Plan #2100 (Suite #2103)."
        ],
        [
            "TC-07",
            "Cierre de turno de caja, arqueo ciego y cuadre de caja",
            "Validar cálculo automatizado de arqueo de caja contrastando efectivo declarado contra ventas del sistema determinando diferencias.",
            "14/10/2026",
            "Turnos de Caja",
            "Cierre y Arqueo Ciego (US-TUR-02)",
            "Navegar a Cierre de Turno; ingresar Monto Declarado contado '$85.00' (Esperado: $50 base + $35 ventas) y presionar 'Finalizar Turno'.",
            "Retorna HTTP 200 OK; diferencia_cuadre = $0.00 (cuadre exacto), estado pasa a 'Cerrado' y se inhabilitan nuevas ventas.",
            ".NET 8, PostgreSQL (Supabase TiendaGo_DB_QA).",
            "Turno activo con ventas registradas durante el turno.",
            "TC-06",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2021 en Azure Boards y Caso #2107 en Test Plan #2100 (Suite #2103)."
        ],
        [
            "TC-08",
            "Venta exitosa en efectivo, desglose de IVA y cálculo de cambio",
            "Validar flujo integral de compra en terminal POS con cálculo aritmético de impuestos (13%), cambio de efectivo y ticket correlativo.",
            "14/10/2026",
            "Punto de Venta / Facturación",
            "Terminal POS y Venta Efectivo (US-POS-01)",
            "Seleccionar 2 unidades de 'Bebida Energizante' ($2.50 c/u, Total: $5.00); cobrar con atajo de billete '$10.00' en efectivo y confirmar.",
            "HTTP 201 Created; pantalla confirma venta con Subtotal: $4.42, IVA (13%): $0.58, Cambio: $5.00 y genera correlativo único (ej. TCK-2026-0001).",
            ".NET 8, PostgreSQL (Supabase TiendaGo_DB_QA), Android Jetpack Compose.",
            "Turno de caja en estado 'Abierto' y stock disponible en catálogo.",
            "TC-06",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2025 en Azure Boards y Caso #2108 en Test Plan #2100 (Suite #2104). Criterio transaccional nuclear."
        ],
        [
            "TC-09",
            "Control transaccional ACID y prevención de sobreventa ante stock insuficiente",
            "Verificar que el servicio VentaService aborte la transacción con Rollback atómico si la cantidad demandada excede el stock disponible.",
            "14/10/2026",
            "Catálogo y Ocupación",
            "Atomicidad ACID y Anti-Sobrevendimiento (US-POS-02)",
            "Producto con stock_actual = 1; enviar petición POST /api/ventas solicitando cantidad = 2 unidades del producto.",
            "La API rechaza la venta retornando HTTP 409 Conflict con mensaje 'Stock insuficiente para el producto'; Rollback completo sin alteración de datos.",
            ".NET 8, Transacción atómica Npgsql / EF Core, PostgreSQL Supabase.",
            "Registro de producto con exactamente 1 unidad en stock en BD QA.",
            "TC-08",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2026 en Azure Boards y Caso #2109 en Test Plan #2100 (Suite #2104). Verificación estricta de propiedad ACID."
        ],
        [
            "TC-10",
            "Decremento físico atómico de existencias en PostgreSQL post-venta",
            "Constatar consistencia de persistencia verificando que el stock en la tabla 'productos' se actualice exactamente restando unidades vendidas.",
            "14/10/2026",
            "Tarifas y Facturación",
            "Persistencia y Descuento Atómico (US-POS-03)",
            "Producto con stock inicial = 15; procesar venta confirmada de 3 unidades vía POS; consultar SELECT stock_actual FROM productos.",
            "El registro en PostgreSQL refleja exactamente stock_actual = 12 unidades y se registra la línea correspondiente en detalles_venta.",
            "PostgreSQL 15 (Supabase TiendaGo_DB_QA), DBeaver / psql.",
            "Producto con stock controlado previo a la prueba.",
            "TC-08",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2027 en Azure Boards y Caso #2110 en Test Plan #2100 (Suite #2104)."
        ],
        [
            "TC-11",
            "Retorno exitoso HTTP 200 en endpoint GET /api/dashboard/resumen",
            "Validar consolidación financiera del día retornando total facturado, órdenes procesadas y recuento de alertas de inventario.",
            "14/10/2026",
            "Reportes y Auditoría",
            "Balance Diario y Métricas (US-DASH-01)",
            "Petición GET a /api/dashboard/resumen con Bearer Token JWT de Administrador en cabecera Authorization.",
            "Retorna HTTP 200 OK con payload JSON estructurado conteniendo totalVentas, cantidadTransacciones y lista de productosBajoStock.",
            ".NET 8 Runtime, BD TiendaGo_DB_QA, Postman / Thunder Client.",
            "Ventas registradas en la fecha actual en la base de datos de pruebas.",
            "TC-08",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2030 en Azure Boards y Caso #2111 en Test Plan #2100 (Suite #2105)."
        ],
        [
            "TC-12",
            "Bloqueo de cobro en terminal POS sin turno de caja activo",
            "Verificar regla de negocio que prohíbe facturar transacciones de venta si el operador no posee un turno de caja en estado 'Abierto'.",
            "14/10/2026",
            "Operaciones / Reservas",
            "Control de Turnos de Caja (US-TUR-03)",
            "Con usuario cajero sin turno abierto, intentar confirmar cobro de $3.00 en TerminalCajaView o enviar POST /api/ventas con idTurno = 0.",
            "Retorna HTTP 400 Bad Request / 409 Conflict con mensaje 'Se requiere un turno de caja abierto para registrar ventas'; la app bloquea el botón de cobro.",
            ".NET 8 Web API, Cliente Android Compose.",
            "Cajero con estado de turno cerrado o nulo.",
            "TC-01",
            "Pendiente de ejecución (Fase de Planificación)",
            "En Planificación",
            "14/10/2026",
            "Planificado y trazado a PBI #2020 en Azure Boards y Caso #2112 en Test Plan #2100 (Suite #2103)."
        ]
    ]

    current_row = header_row + 1
    for row_data in test_cases:
        for idx, val in enumerate(row_data):
            col_num = start_col + idx
            cell = ws.cell(row=current_row, column=col_num, value=val)
            cell.font = CELL_BOLD if idx == 0 else CELL_FONT
            cell.border = THIN_BORDER
            
            # Alignments
            if idx in [0, 3, 10, 12, 13]:
                cell.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

        ws.row_dimensions[current_row].height = 48
        current_row += 1

    # Column Widths
    col_widths = {
        2: 10,  # Id
        3: 26,  # Caso de Prueba
        4: 32,  # Descripción
        5: 12,  # Fecha
        6: 22,  # Área Funcional / Sub proceso
        7: 24,  # Funcionalidad / Característica
        8: 34,  # Datos / Acciones de Entrada
        9: 34,  # Resultado Esperado
        10: 28, # Requerimientos de Ambiente
        11: 28, # Procedimientos especiales
        12: 15, # Dependencias
        13: 24, # Resultado Obtenido
        14: 16, # Estado
        15: 14, # Última Fecha de Estado
        16: 32  # Observaciones
    }

    for col_idx, width in col_widths.items():
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width

    # Margin column A width
    ws.column_dimensions["A"].width = 3

    output_path = "Pruebas_de_Aceptacion_UAT_TiendaGo.xlsx"
    wb.save(output_path)
    print(f"Excel guardado exitosamente en: {output_path}")

if __name__ == "__main__":
    create_uat_excel()
