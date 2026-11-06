import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Hoja 1'

header_fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
title_font = Font(name='Calibri', size=14, bold=True, color='1F4E79')
bold_font = Font(name='Calibri', size=11, bold=True)
white_bold = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
regular_font = Font(name='Calibri', size=10)

ws['A1'] = 'Plantilla de Casos de Pruebas de Software'
ws['A1'].font = title_font
ws['A2'] = 'Proyecto: TiendaGo - Pruebas de API REST (Minimal APIs / ASP.NET Core) - Grupo 06'
ws['A2'].font = bold_font
ws['A3'] = 'Ciclo de Pruebas: Ciclo 1 de Integración y Seguridad RBAC en Azure DevOps'
ws['A3'].font = regular_font

headers = [
    'Id', 'Caso de Prueba', 'Descripción', 'Fecha', 'Área Funcional / Sub proceso',
    'Funcionalidad / Característica', 'Datos / Acciones de Entrada', 'Resultado Esperado',
    'Requerimientos de Ambiente de prueba', 'Procedimientos especiales requeridos',
    'Dependencias con otros casos de prueba', 'Resultado Obtenido', 'Estado',
    'Última Fecha de Estado', 'Observaciones'
]

for col_num, h in enumerate(headers, 1):
    c = ws.cell(row=5, column=col_num, value=h)
    c.fill = header_fill
    c.font = white_bold
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

api_cases = [
    ('CP01', 'Autenticación exitosa de Administrador con JWT', 'Validar endpoint POST /api/auth/login con credenciales de Administrador válidas', '14/10/2026', 'Seguridad y Acceso', 'Autenticación API', 'POST /api/auth/login payload: admin@tiendago.com / Admin123*', 'HTTP 200 OK, Bearer JWT con claim rol=Administrador', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'Ninguna', 'HTTP 200 OK y token emitido', 'Passed', '22/10/2026', 'Validado con xUnit y REST Client'),
    ('CP02', 'Autenticación exitosa de Cajero con JWT', 'Validar endpoint POST /api/auth/login con credenciales de Cajero válidas', '14/10/2026', 'Seguridad y Acceso', 'Autenticación API', 'POST /api/auth/login payload: cajero@tiendago.com / Cajero123*', 'HTTP 200 OK, Bearer JWT con claim rol=Cajero', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'Ninguna', 'HTTP 200 OK y token emitido', 'Passed', '22/10/2026', 'Permisos de caja habilitados'),
    ('CP03', 'Rechazo de autenticación con credenciales erróneas', 'Verificar denegación de acceso ante contraseña inválida retornando 401', '14/10/2026', 'Seguridad y Acceso', 'Autenticación API', 'POST /api/auth/login payload: admin@tiendago.com / ClaveMala999', 'HTTP 401 Unauthorized sin emisión de token', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'Ninguna', 'HTTP 401 Unauthorized', 'Passed', '22/10/2026', 'Acceso denegado correctamente'),
    ('CP04', 'Rechazo de autenticación por usuario no registrado', 'Verificar denegación ante email no registrado en base de datos', '14/10/2026', 'Seguridad y Acceso', 'Autenticación API', 'POST /api/auth/login payload: noexiste@tiendago.com / Clave123*', 'HTTP 401 Unauthorized', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'Ninguna', 'HTTP 401 Unauthorized', 'Passed', '22/10/2026', 'Usuario inexistente controlado'),
    ('CP05', 'Obligatoriedad de campos requeridos en Login', 'Verificar validación de modelo ante payload con campos vacíos', '14/10/2026', 'Seguridad y Acceso', 'Validación de DTOs', 'POST /api/auth/login con payload vacío', 'HTTP 400 Bad Request con detalles de validación', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'Ninguna', 'HTTP 400 Bad Request', 'Passed', '22/10/2026', 'Validación FluentValidation activa'),
    ('CP06', 'Denegación de acceso a endpoints protegidos sin token', 'Verificar intercepción de peticiones anónimas a recursos protegidos', '14/10/2026', 'Seguridad y Acceso', 'Middleware JWT', 'GET /api/productos sin encabezado Authorization', 'HTTP 401 Unauthorized', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'Ninguna', 'HTTP 401 Unauthorized', 'Passed', '22/10/2026', 'Middleware intercepta sin Bearer'),
    ('CP07', 'Intento de alta de producto sin autorización', 'Verificar intercepción ante intento anónimo de invocar POST de productos', '14/10/2026', 'Seguridad y Acceso', 'Middleware JWT', 'POST /api/productos sin token Bearer', 'HTTP 401 Unauthorized', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'Ninguna', 'HTTP 401 Unauthorized', 'Passed', '22/10/2026', 'Protección de mutaciones verificada'),
    ('CP08', 'Control RBAC estricto - Rechazo 403 a Cajero en alta de producto', 'Verificar restricción de permisos para usuario con rol Cajero en POST de productos', '14/10/2026', 'Seguridad RBAC', 'Políticas de Rol', 'POST /api/productos con Bearer Token de rol Cajero', 'HTTP 403 Forbidden', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'CP02', 'HTTP 403 Forbidden', 'Passed', '22/10/2026', 'Aislamiento de privilegios exitoso'),
    ('CP09', 'Control RBAC estricto - Rechazo 403 a Cajero en alta de categoría', 'Verificar restricción de permisos para rol Cajero en mutación de categorías', '14/10/2026', 'Seguridad RBAC', 'Políticas de Rol', 'POST /api/categorias con Bearer Token de rol Cajero', 'HTTP 403 Forbidden', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'CP02', 'HTTP 403 Forbidden', 'Passed', '22/10/2026', 'Rutas de configuración protegidas'),
    ('CP10', 'Alta exitosa de producto por usuario Administrador', 'Validar creación de producto con rol Administrador y persistencia en BD', '14/10/2026', 'Catálogo de Productos', 'CRUD Catálogo', 'POST /api/productos con Bearer Admin y datos de nuevo producto', 'HTTP 201 Created con cabecera Location y entidad creada', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'CP01', 'HTTP 201 Created', 'Passed', '22/10/2026', 'Producto persistido en PostgreSQL'),
    ('CP11', 'Restricción de consulta de usuarios del sistema a rol Cajero', 'Verificar que Cajero no tenga acceso a endpoints de auditoría de usuarios', '14/10/2026', 'Seguridad RBAC', 'Políticas de Rol', 'GET /api/usuarios con token de rol Cajero', 'HTTP 403 Forbidden', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'CP02', 'HTTP 403 Forbidden', 'Passed', '22/10/2026', 'Información administrativa privada'),
    ('CP12', 'Registro transaccional exitoso de venta POS con stock suficiente', 'Validar creación de venta, descuento de inventario y generación de ticket', '14/10/2026', 'Punto de Venta POS', 'Transacciones POS', 'POST /api/ventas con 2 items y pago en efectivo', 'HTTP 201 Created con entidad Venta y stock decrementado', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'CP01', 'HTTP 201 Created', 'Passed', '22/10/2026', 'Transacción ACID confirmada'),
    ('CP13', 'Bloqueo transaccional de sobreventa ante existencias insuficientes', 'Verificar rechazo y rollback atómico cuando la demanda excede stock actual', '14/10/2026', 'Punto de Venta POS', 'Control de Stock ACID', 'POST /api/ventas solicitando cantidad mayor al stock disponible', 'HTTP 409 Conflict con mensaje descriptivo de stock insuficiente', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'CP01', 'HTTP 409 Conflict', 'Passed', '22/10/2026', 'Rollback ejecutado sin alteración'),
    ('CP14', 'Rechazo de solicitud de venta sin items o detalles', 'Verificar validación de negocio que impide procesar tickets vacíos', '14/10/2026', 'Punto de Venta POS', 'Validación de Venta', 'POST /api/ventas con lista DetalleVenta vacía', 'HTTP 400 Bad Request', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'Ninguna', 'HTTP 400 Bad Request', 'Passed', '22/10/2026', 'Venta vacía prevenida'),
    ('CP15', 'Bloqueo de facturación en Terminal POS sin jornada de caja activa', 'Verificar que no se puedan emitir ventas sin un turno de caja abierto', '14/10/2026', 'Turnos de Caja', 'Control Operativo', 'POST /api/ventas cuando no existe un turno de caja en estado Abierto', 'HTTP 409 Conflict requiriendo apertura de caja', 'ASP.NET Core Web API, PostgreSQL', 'Ninguno', 'Ninguna', 'HTTP 409 Conflict', 'Passed', '22/10/2026', 'Apertura de turno obligatoria')
]

for row_idx, data in enumerate(api_cases, 6):
    for col_idx, val in enumerate(data, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.font = regular_font
        if col_idx in [1, 4, 13, 14]:
            cell.alignment = Alignment(horizontal='center', vertical='center')
        else:
            cell.alignment = Alignment(horizontal='left', vertical='center')

for col in ws.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = openpyxl.utils.get_column_letter(col[0].column)
    ws.column_dimensions[col_letter].width = min(max(max_len + 2, 10), 40)

wb.save('Casos de Pruebas de API_Grupo06.xlsx')
print('Created Casos de Pruebas de API_Grupo06.xlsx successfully!')
