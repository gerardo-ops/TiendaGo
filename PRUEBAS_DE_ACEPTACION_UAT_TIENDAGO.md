# ESCUELA SUPERIOR FRANCISCANA ESPECIALIZADA – AGAPE
## CARRERA: TÉCNICO EN INGENIERÍA DE DESARROLLO DE SOFTWARE
### MÓDULO: TESTEO DE SOFTWARE (CICLO C4-26)

---

# MATRIZ DE PRUEBAS DE ACEPTACIÓN DE USUARIO (UAT)
## Proyecto: TiendaGo (Punto de Venta POS Móvil y Gestión de Inventario Express)
### Ciclo de Pruebas: Planificación de Casos de Aceptación en Azure DevOps

---

### DATOS GENERALES DEL PROYECTO Y GOBERNANZA QA

| Parámetro | Detalle Institucional y Técnico |
| :--- | :--- |
| **Institución Educativa:** | Escuela Superior Franciscana Especializada / AGAPE (ESFE - AGAPE) |
| **Carrera Profesional:** | Técnico en Ingeniería de Desarrollo de Software |
| **Módulo Formativo:** | Testeo de Software |
| **Nombre del Sistema:** | **TiendaGo** (POS Móvil & Web API RESTful) |
| **Docente Evaluador:** | Lic. Gerber Alexis Gómez Hidalgo |
| **Ciclo Académico:** | C4-26 (Ciclo 04 / 2026) |
| **Fecha de Emisión:** | 14 de Octubre de 2026 |
| **Versión del Artefacto:** | 1.0.0 (Release Candidate - RC1) |
| **Marco Metodológico:** | ISO/IEC/IEEE 29119 & Azure DevOps Test Plans |
| **Entorno de Pruebas (QA):** | Somee Hosting (`http://TiendaGO.somee.com/`), Supabase Cloud PostgreSQL 15, Android 14 |

### EQUIPO DE TRABAJO Y ASIGNACIÓN (100%)

| Estudiante | Carné / ID | Participación | Rol en el Equipo de Pruebas |
| :--- | :---: | :---: | :--- |
| **Gerardo Antonio Batres Moreno** | BM-2026 | 100% | QA Lead & Test Architect |
| **Elmer Antonio Tesorero Hernández** | TH-2026 | 100% | Backend QA Automation & API Tester |
| **Jason Vladimir Bautista Maravilla** | BM-2026-2 | 100% | Mobile QA Tester & Functional Specialist |
| **Bayron Antonio Díaz Campos** | DC-2026 | 100% | Security Specialist & DevOps / Environment Manager |

---

## 1. INTRODUCCIÓN Y OBJETIVO DE LAS PRUEBAS UAT

El presente documento formaliza el diseño y planificación de las **Pruebas de Aceptación del Usuario (User Acceptance Testing - UAT)** para la plataforma **TiendaGo**.

El propósito fundamental de esta batería de pruebas es certificar con criterios objetivos y auditables que el sistema cumple cabalmente con las expectativas de negocio, requerimientos funcionales y requisitos no funcionales definidos por los stakeholders (pequeños comercios, tiendas de conveniencia y administradores de bazares), así como validar los contratos de servicio entre la aplicación cliente móvil en **Android (Jetpack Compose / Kotlin)** y el backend **ASP.NET Core (.NET 8)** persistido en **PostgreSQL (Supabase Cloud)**.

Todos los casos han sido concebidos y trazados directamente hacia los **Product Backlog Items (PBI)** y **Test Cases** configurados en **Azure Boards** y **Azure Test Plans**.

---

## 2. MATRIZ INTEGRAL DE PRUEBAS DE ACEPTACIÓN (UAT) — PLANTILLA AZURE DEVOPS

A continuación se presenta la matriz completa de 15 columnas basada en la plantilla estándar de planificación y auditoría de pruebas de aceptación:

| Id | Caso de Prueba | Descripción | Fecha | Área Funcional / Sub proceso | Funcionalidad / Característica | Datos / Acciones de Entrada | Resultado Esperado | Requerimientos de Ambiente de prueba | Procedimientos especiales requeridos | Dependencias | Resultado Obtenido | Estado | Última Fecha de Estado | Observaciones / Trazabilidad Azure DevOps |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **TC-01** | Autenticación exitosa de Administrador con JWT y claims de rol | Validar verificación criptográfica de contraseña contra hash BCrypt y emisión de Bearer Token JWT con claims de usuario y rol 'Administrador'. | 14/10/2026 | Seguridad y Acceso | Autenticación Segura y Claims (US-AUTH-01) | Navegar a Login; ingresar correo 'admin@tiendago.com', contraseña 'Admin123*' y presionar 'Iniciar Sesión'. | AuthService valida hash BCrypt, retorna HTTP 200 OK con Bearer Token JWT; la app persiste el token en DataStore Preferences y redirige al Dashboard. | .NET 8, ASP.NET Core Web API, PostgreSQL (Supabase TiendaGo_DB_QA), Android 14 (Samsung SM-A556E / Emulador Pixel 8). | Usuario administrador semilla activo en BD TiendaGo_DB_QA con clave hasheada en BCrypt. | Ninguna | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2010 en Azure Boards y Caso #2101 en Test Plan #2100 (Suite #2101). |
| **TC-02** | Rechazo de autenticación con contraseña incorrecta | Verificar denegación de acceso ante credenciales no concordantes impidiendo emisión de token y mostrando feedback al usuario. | 14/10/2026 | Seguridad y Acceso | Autenticación Segura y Claims (US-AUTH-01) | Ingresar correo 'admin@tiendago.com', contraseña 'ClaveErronea999!' y presionar 'Iniciar Sesión'. | La API retorna código HTTP 401 Unauthorized; la interfaz en Jetpack Compose muestra Snackbar de credenciales inválidas sin almacenar token. | .NET 8, ASP.NET Core Web API, Cliente Móvil Android Compose. | Usuario registrado en BD; conexión de red activa hacia Somee / Backend local. | TC-01 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2010 en Azure Boards y Caso #2102 en Test Plan #2100 (Suite #2101). |
| **TC-03** | Restricción de permisos RBAC e intercepción HTTP 403 para rol Cajero | Verificar control de acceso RBAC bloqueando mutación de catálogo y rutas administrativas a usuarios con rol Cajero. | 14/10/2026 | Seguridad y Acceso | Control de Acceso RBAC (US-SEC-02) | Autenticar usuario 'cajero@tiendago.com'; invocar POST /api/productos con payload de nuevo producto inyectando token de cajero. | Ocultamiento del FAB (+) en app móvil; middleware de autorización intercepta petición HTTP y retorna código 403 Forbidden. | .NET 8, ASP.NET Core Authorization Policy, Postman / Thunder Client. | Usuario Cajero semilla activo en BD con rol ID 2. | TC-01 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2011 en Azure Boards y Caso #2103 en Test Plan #2100 (Suite #2101). Criterio de seguridad no negociable. |
| **TC-04** | Búsqueda dinámica y escaneo óptico de producto por SKU | Validar localización inmediata de producto mediante lectura óptica de código de barras/QR y filtro dinámico por texto/SKU. | 14/10/2026 | Catálogo y Ocupación | Búsqueda y Escáner SKU (US-CAT-01) | Ingresar a Catálogo de Productos; activar escáner de cámara sobre código impreso o digitar SKU '75010001'. | El catálogo filtra en tiempo real y despliega la tarjeta del producto con foto (Coil), nombre, SKU, precio ($1.25) y stock disponible. | Android 14 con cámara operativa, Jetpack Compose, Backend .NET 8 Somee. | Producto con SKU '75010001' registrado y activo en base de datos. | Ninguna | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2015 en Azure Boards y Caso #2104 en Test Plan #2100 (Suite #2102). |
| **TC-05** | Alerta visual reactiva de stock crítico (menor a 5 unidades) | Verificar despliegue condicional de badge cromático de advertencia cuando las existencias igualan o descienden del umbral mínimo. | 14/10/2026 | Catálogo y Ocupación | Alerta de Stock Crítico (US-CAT-02) | Navegar a Catálogo de Productos; ubicar producto 'Leche Entera 1L' configurado con stock_actual = 3 y stock_minimo = 5. | La tarjeta del producto muestra un badge visual ámbar/rojo con texto 'Stock Crítico: 3 unidades restantes', alertando al operador. | Android 14, Compose UI, BD PostgreSQL Supabase con datos semilla. | Producto configurado con stock_actual <= stock_minimo en tabla 'productos'. | TC-04 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2016 en Azure Boards y Caso #2105 en Test Plan #2100 (Suite #2102). |
| **TC-06** | Apertura de turno de caja con monto base inicial | Validar registro de apertura de jornada de caja vinculando usuario cajero con monto base en efectivo para habilitar ventas. | 14/10/2026 | Operaciones / Reservas | Control de Turnos de Caja (US-TUR-01) | Ingresar a Gestión de Turno; ingresar Monto Base Inicial '$50.00' y presionar 'Abrir Turno de Caja'. | Retorna HTTP 201 Created con entidad TurnoCaja; estado cambia a 'Abierto' y se desbloquea el acceso a la Terminal POS. | .NET 8, PostgreSQL (Supabase TiendaGo_DB_QA), Android Compose. | Cajero sin turno abierto previo en BD. | TC-01 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2020 en Azure Boards y Caso #2106 en Test Plan #2100 (Suite #2103). |
| **TC-07** | Cierre de turno de caja, arqueo ciego y cuadre de caja | Validar cálculo automatizado de arqueo de caja contrastando efectivo declarado contra ventas del sistema determinando diferencias. | 14/10/2026 | Operaciones / Reservas | Cierre y Arqueo Ciego (US-TUR-02) | Navegar a Cierre de Turno; ingresar Monto Declarado contado '$85.00' (Esperado: $50 base + $35 ventas) y presionar 'Finalizar Turno'. | Retorna HTTP 200 OK; diferencia_cuadre = $0.00 (cuadre exacto), estado pasa a 'Cerrado' y se inhabilitan nuevas ventas. | .NET 8, PostgreSQL (Supabase TiendaGo_DB_QA). | Turno activo con ventas registradas durante el turno. | TC-06 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2021 en Azure Boards y Caso #2107 en Test Plan #2100 (Suite #2103). |
| **TC-08** | Venta exitosa en efectivo, desglose de IVA y cálculo de cambio | Validar flujo integral de compra en terminal POS con cálculo aritmético de impuestos (13%), cambio de efectivo y ticket correlativo. | 14/10/2026 | Tarifas y Facturación | Terminal POS y Venta Efectivo (US-POS-01) | Seleccionar 2 unidades de 'Bebida Energizante' ($2.50 c/u, Total: $5.00); cobrar con atajo de billete '$10.00' en efectivo y confirmar. | HTTP 201 Created; pantalla confirma venta con Subtotal: $4.42, IVA (13%): $0.58, Cambio: $5.00 y genera correlativo único (ej. TCK-2026-0001). | .NET 8, PostgreSQL (Supabase TiendaGo_DB_QA), Android Jetpack Compose. | Turno de caja en estado 'Abierto' y stock disponible en catálogo. | TC-06 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2025 en Azure Boards y Caso #2108 en Test Plan #2100 (Suite #2104). Criterio transaccional nuclear. |
| **TC-09** | Control transaccional ACID y prevención de sobreventa ante stock insuficiente | Verificar que el servicio VentaService aborte la transacción con Rollback atómico si la cantidad demandada excede el stock disponible. | 14/10/2026 | Tarifas y Facturación | Atomicidad ACID y Anti-Sobrevendimiento (US-POS-02) | Producto con stock_actual = 1; enviar petición POST /api/ventas solicitando cantidad = 2 unidades del producto. | La API rechaza la venta retornando HTTP 409 Conflict con mensaje 'Stock insuficiente para el producto'; Rollback completo sin alteración de datos. | .NET 8, Transacción atómica Npgsql / EF Core, PostgreSQL Supabase. | Registro de producto con exactamente 1 unidad en stock en BD QA. | TC-08 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2026 en Azure Boards y Caso #2109 en Test Plan #2100 (Suite #2104). Verificación estricta de propiedad ACID. |
| **TC-10** | Decremento físico atómico de existencias en PostgreSQL post-venta | Constatar consistencia de persistencia verificando que el stock en la tabla 'productos' se actualice exactamente restando unidades vendidas. | 14/10/2026 | Tarifas y Facturación | Persistencia y Descuento Atómico (US-POS-03) | Producto con stock inicial = 15; procesar venta confirmada de 3 unidades vía POS; consultar SELECT stock_actual FROM productos. | El registro en PostgreSQL refleja exactamente stock_actual = 12 unidades y se registra la línea correspondiente en detalles_venta. | PostgreSQL 15 (Supabase TiendaGo_DB_QA), DBeaver / psql. | Producto con stock controlado previo a la prueba. | TC-08 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2027 en Azure Boards y Caso #2110 en Test Plan #2100 (Suite #2104). |
| **TC-11** | Retorno exitoso HTTP 200 en endpoint GET /api/dashboard/resumen | Validar consolidación financiera del día retornando total facturado, órdenes procesadas y recuento de alertas de inventario. | 14/10/2026 | Reportes y Auditoría | Balance Diario y Métricas (US-DASH-01) | Petición GET a /api/dashboard/resumen con Bearer Token JWT de Administrador en cabecera Authorization. | Retorna HTTP 200 OK con payload JSON estructurado conteniendo totalVentas, cantidadTransacciones y lista de productosBajoStock. | .NET 8 Runtime, BD TiendaGo_DB_QA, Postman / Thunder Client. | Ventas registradas en la fecha actual en la base de datos de pruebas. | TC-08 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2030 en Azure Boards y Caso #2111 en Test Plan #2100 (Suite #2105). |
| **TC-12** | Bloqueo de cobro en terminal POS sin turno de caja activo | Verificar regla de negocio que prohíbe facturar transacciones de venta si el operador no posee un turno de caja en estado 'Abierto'. | 14/10/2026 | Operaciones / Reservas | Control de Turnos de Caja (US-TUR-03) | Con usuario cajero sin turno abierto, intentar confirmar cobro de $3.00 en TerminalCajaView o enviar POST /api/ventas con idTurno = 0. | Retorna HTTP 400 Bad Request / 409 Conflict con mensaje 'Se requiere un turno de caja abierto para registrar ventas'; la app bloquea el botón de cobro. | .NET 8 Web API, Cliente Android Compose. | Cajero con estado de turno cerrado o nulo. | TC-01 | Pendiente de ejecución (Fase de Planificación) | En Planificación | 14/10/2026 | Planificado y trazado a PBI #2020 en Azure Boards y Caso #2112 en Test Plan #2100 (Suite #2103). |

---

## 3. DESGLOSE DETALLADO DE CASOS DE PRUEBA UAT (ESPECIFICACIÓN GHERKIN)

A continuación se detalla la especificación paso a paso bajo el formato formal de aceptación **Dado / Cuando / Entonces** (*Given / When / Then*):

```gherkin
Característica: Autenticación Segura y RBAC (US-AUTH-01 & US-SEC-02)

  Escenario: TC-01 - Autenticación válida de Administrador
    Dado que el usuario "admin@tiendago.com" existe activo en la base de datos PostgreSQL
    Y su clave hasheada con BCrypt corresponde a "Admin123*"
    Cuando ingresa sus credenciales en la vista de Login móvil y pulsa "Iniciar Sesión"
    Entonces el backend responde con código HTTP 200 OK y un Bearer Token JWT
    Y la aplicación almacena de forma cifrada el token en DataStore Preferences
    Y redirige automáticamente al usuario hacia el Dashboard principal.

  Escenario: TC-03 - Aislamiento estricto de privilegios para rol Cajero
    Dado que el usuario se encuentra autenticado con rol Cajero (id_rol = 2)
    Cuando navega al catálogo de productos en la aplicación Android
    Entonces el botón flotante (+) para agregar productos permanece oculto
    Y si envía una petición directa POST /api/productos inyectando su token JWT
    Entonces el middleware de autorización de ASP.NET Core rechaza la petición con HTTP 403 Forbidden.
```

```gherkin
Característica: Gestión de Turnos de Caja (US-TUR-01 & US-TUR-02)

  Escenario: TC-06 - Apertura formal de turno de caja
    Dado que el cajero activo no posee ningún turno abierto en la tabla "turnos_caja"
    Cuando digita el monto base de apertura de "$50.00" y presiona "Abrir Turno de Caja"
    Entonces el sistema registra el turno en estado "Abierto" con código HTTP 201 Created
    Y desbloquea de inmediato las funciones de venta en la Terminal POS.

  Escenario: TC-07 - Arqueo ciego y cuadre de caja
    Dado que el cajero posee un turno abierto con $50.00 de base y $35.00 en ventas registradas
    Cuando ingresa a Cierre de Turno y digita un conteo físico de "$85.00"
    Entonces el sistema calcula una diferencia de cuadre de "$0.00" (cuadre exacto)
    Y actualiza el estado del turno a "Cerrado", impidiendo registrar nuevas órdenes.
```

```gherkin
Característica: Transaccionalidad POS y Atomicidad ACID (US-POS-01 & US-POS-02)

  Escenario: TC-08 - Venta en efectivo con cálculo exacto de cambio
    Dado que el cajero cuenta con un turno abierto y existen 10 unidades de "Bebida Energizante" a $2.50 c/u
    Cuando añade 2 unidades al carrito (Total: $5.00) y selecciona pago en efectivo con billete de "$10.00"
    Entonces el sistema calcula un desglose de Subtotal $4.42 e IVA (13%) $0.58
    Y registra la venta retornando HTTP 201 Created, cambio exacto de "$5.00" y número de ticket correlativo.

  Escenario: TC-09 - Prevención de sobreventa ante inventario insuficiente (ACID)
    Dado que el producto seleccionado tiene exactamente 1 unidad disponible en inventario
    Cuando se solicita procesar una orden de venta por 2 unidades
    Entonces el servicio transaccional detecta el déficit de stock y aborta la operación
    Y emite un Rollback completo en PostgreSQL retornando HTTP 409 Conflict sin descontar inventario.
```

---

## 4. MATRIZ DE TRAZABILIDAD EN AZURE DEVOPS

| PBI (Azure Boards) | Título de la Historia de Usuario | Caso de Prueba UAT | Test Plan | Test Suite |
| :---: | :--- | :---: | :---: | :---: |
| **PBI #2010** | US-AUTH-01: Autenticación Segura y Gestión de Sesión | TC-01, TC-02 | Test Plan #2100 | Suite #2101 (Seguridad y Acceso) |
| **PBI #2011** | US-SEC-02: Control de Acceso Basado en Roles (RBAC) | TC-03 | Test Plan #2100 | Suite #2101 (Seguridad y Acceso) |
| **PBI #2015** | US-CAT-01: Explorador de Catálogo y Búsqueda por SKU/QR | TC-04 | Test Plan #2100 | Suite #2102 (Catálogo e Inventario) |
| **PBI #2016** | US-CAT-02: Alerta Visual de Inventario Crítico | TC-05 | Test Plan #2100 | Suite #2102 (Catálogo e Inventario) |
| **PBI #2020** | US-TUR-01: Apertura y Control Obligatorio de Turnos | TC-06, TC-12 | Test Plan #2100 | Suite #2103 (Turnos de Caja) |
| **PBI #2021** | US-TUR-02: Cierre de Turno y Arqueo Ciego | TC-07 | Test Plan #2100 | Suite #2103 (Turnos de Caja) |
| **PBI #2025** | US-POS-01: Terminal POS, Facturación e Impuestos | TC-08 | Test Plan #2100 | Suite #2104 (Punto de Venta POS) |
| **PBI #2026** | US-POS-02: Atomicidad ACID y Anti-Sobrevendimiento | TC-09 | Test Plan #2100 | Suite #2104 (Punto de Venta POS) |
| **PBI #2027** | US-POS-03: Persistencia y Descuento Físico en BD | TC-10 | Test Plan #2100 | Suite #2104 (Punto de Venta POS) |
| **PBI #2030** | US-DASH-01: Resumen Diario y Métricas Financieras | TC-11 | Test Plan #2100 | Suite #2105 (Dashboard y Auditoría) |

---

## 5. ARTEFACTOS Y ARCHIVOS GENERADOS

Para máxima interoperabilidad académica y profesional, este trabajo cuenta con los siguientes entregables listos para su uso:

1. **Documento PDF Oficial:** [`Pruebas_de_Aceptacion_UAT_TiendaGo.pdf`](file:///c:/Users/Admin/Documents/Proyectos/TiendaGo/Pruebas_de_Aceptacion_UAT_TiendaGo.pdf)
   - Diseñado siguiendo estrictamente la plantilla proporcionada (títulos, encabezados azul acero `#1B587A`, bordes definidos y distribución en 4 secciones lógicas con numeración de páginas).
2. **Libro de Trabajo Microsoft Excel (.xlsx):** [`Pruebas_de_Aceptacion_UAT_TiendaGo.xlsx`](file:///c:/Users/Admin/Documents/Proyectos/TiendaGo/Pruebas_de_Aceptacion_UAT_TiendaGo.xlsx)
   - Contiene la matriz completa y unificada de 15 columnas con estilos corporativos, ancho de columnas optimizado, texto autoajustable y formato compatible con importación en Azure DevOps.
3. **Scripts de Automatización y Generación:**
   - [`generate_uat_excel.py`](file:///c:/Users/Admin/Documents/Proyectos/TiendaGo/generate_uat_excel.py): Generador programático del Excel con OpenPyXL.
   - [`generate_uat_pdf.py`](file:///c:/Users/Admin/Documents/Proyectos/TiendaGo/generate_uat_pdf.py): Generador programático del PDF de alta calidad con ReportLab.

---

### AVAL DE ASEGURAMIENTO DE CALIDAD

* **QA Lead & Test Architect:** Gerardo Antonio Batres Moreno
* **Equipo de Aseguramiento de Calidad:** Elmer Tesorero, Jason Bautista, Bayron Díaz
* **Fecha de Formalización:** 14 de Octubre de 2026
* **Institución:** Escuela Superior Franciscana Especializada / AGAPE (ESFE - AGAPE)
