# ESCUELA SUPERIOR FRANCISCANA ESPECIALIZADA – AGAPE
## CARRERA: TÉCNICO EN INGENIERÍA DE DESARROLLO DE SOFTWARE
### MÓDULO: TESTEO DE SOFTWARE (CICLO C4-26)

---

# INFORME CONSOLIDADO DE EJECUCIÓN DE PRUEBAS DE SOFTWARE Y REPORTES EN AZURE DEVOPS
## Sistema Punto de Venta POS Móvil y Gestión de Inventario Express: TiendaGo

---

### DATOS GENERALES DEL PROYECTO

| Campo | Detalle Institucional y Académico |
| :--- | :--- |
| **Institución Educativa:** | Escuela Superior Franciscana Especializada / AGAPE (ESFE - AGAPE) |
| **Carrera:** | Técnico en Ingeniería de Desarrollo de Software |
| **Módulo Formativo:** | Testeo de Software |
| **Proyecto Evaluado:** | **TiendaGo** (POS Móvil Android Jetpack Compose & Backend Web API RESTful .NET 8) |
| **Docente Evaluador:** | Lic. Gerber Alexis Gómez Hidalgo |
| **Ciclo Académico:** | C4-26 (Ciclo 04 / 2026) |
| **Fecha de Presentación:** | Octubre de 2026 |
| **Grupo de Trabajo:** | **Grupo N° 06** |
| **Repositorio Oficial de GitHub:** | [https://github.com/gerardo-ops/TiendaGo.git](https://github.com/gerardo-ops/TiendaGo.git) |
| **Entorno de Gestión (ALM):** | Azure DevOps ([https://dev.azure.com/gerardobatres06/TiendaGo](https://dev.azure.com/gerardobatres06/TiendaGo)) |

---

### INTEGRANTES DEL EQUIPO DE TRABAJO (100% PARTICIPACIÓN)

| N° | Nombre Completo del Estudiante | Carné / ID | Rol Asignado en QA | Participación |
| :-: | :--- | :---: | :--- | :---: |
| 1 | **Gerardo Antonio Batres Moreno** | BM-2026 | QA Lead & Test Architect | 100% |
| 2 | **Elmer Antonio Tesorero Hernández** | TH-2026 | Backend QA Automation & API Tester | 100% |
| 3 | **Jason Vladimir Bautista Maravilla** | BM-2026-2 | Mobile QA Tester & Functional Specialist | 100% |
| 4 | **Bayron Antonio Díaz Campos** | DC-2026 | Security Specialist & DevOps / Environment Manager | 100% |

---

## CONTROL DEL DOCUMENTO Y APROBACIONES DE CALIDAD

| Versión | Fecha | Autor(es) | Descripción del Cambio / Hito | Estado |
| :---: | :---: | :---: | :--- | :---: |
| **v1.0.0** | 14/10/2026 | Grupo N° 06 | Diseño, especificación y planificación de casos unitarios, integración y UAT. | Aprobado |
| **v1.5.0** | 22/10/2026 | G. Batres / E. Tesorero | Automatización de suites xUnit, ejecución y registro inicial de Test Runs. | Aprobado |
| **v2.0.0** | 27/10/2026 | Grupo N° 06 Completo | Consolidación final de reportes Azure DevOps, cobertura 92.4% y cierre de PBIs en 'Done'. | **Publicado / Certificado** |

---

## ÍNDICE GENERAL

1. [Análisis y Discusión de las Indicaciones Docentes (Punto 1)](#1-análisis-y-discusión-de-las-indicaciones-docentes-punto-1)
2. [Organización y Distribución del Equipo de Trabajo (Punto 2)](#2-organización-y-distribución-del-equipo-de-trabajo-punto-2)
3. [Reporte de Ejecución de las Pruebas Diseñadas (Punto 3)](#3-reporte-de-ejecución-de-las-pruebas-diseñadas-punto-3)
   - 3.1 [Resumen Ejecutivo de Ejecución (31 de 31 Aprobadas)](#31-resumen-ejecutivo-del-ciclo-de-ejecución)
   - 3.2 [Reporte de Pruebas Unitarias Automatizadas (.NET 8 xUnit)](#32-reporte-detallado-de-pruebas-unitarias-automatizadas-xunit)
   - 3.3 [Reporte de Pruebas de Integración (Minimal APIs & WebApplicationFactory)](#33-reporte-detallado-de-pruebas-de-integración-minimal-apis)
   - 3.4 [Reporte de Pruebas de Aceptación de Usuario (UAT) en Móvil](#34-reporte-detallado-de-pruebas-de-aceptación-de-usuario-uat-en-dispositivo-móvil)
4. [Finalización de la Documentación en Azure DevOps (Punto 4)](#4-finalización-de-la-documentación-en-azure-devops-punto-4)
5. [Consolidación de Reportes Generados por Azure DevOps (Punto 5)](#5-consolidación-de-reportes-generados-por-la-plataforma-azure-devops-punto-5)
   - 5.1 [Test Plans Progress Report](#51-reporte-consolidado-de-progreso-y-efectividad-test-plans-progress-report)
   - 5.2 [CI/CD Pipeline Test Results & TRX Attachments](#52-reporte-de-pruebas-de-integración-continua-azure-pipelines--trx)
   - 5.3 [Reporte de Cobertura de Código (92.4%)](#53-reporte-de-cobertura-de-código-coverlet--cobertura-xml-924)
   - 5.4 [Matriz de Trazabilidad Integral de Calidad (RTM)](#54-matriz-de-trazabilidad-integral-de-calidad-rtm)
   - 5.5 [Reporte de Gestión de Defectos (Cero Defectos Bloqueantes)](#55-reporte-de-gestión-de-defectos-y-dictamen-de-release)
6. [Evidencias Visuales y Auditoría de Ejecución (Punto 6)](#6-evidencias-visuales-y-auditoría-de-ejecución-punto-6)
7. [Conclusiones y Reflexiones Individuales (100% Participación)](#7-conclusiones-y-reflexiones-individuales-100-participación)
8. [Enlaces Oficiales, Artefactos y Referencias Normativas](#8-enlaces-oficiales-artefactos-y-referencias-normativas)

---

## 1. ANÁLISIS Y DISCUSIÓN DE LAS INDICACIONES DOCENTES (PUNTO 1)

El equipo sostuvo sesiones de trabajo estructuradas para desglosar y alinear el trabajo a las directrices de la entrega:
- **Transición de Fase:** Evolución de la planificación y diseño hacia la ejecución empírica en entornos reales y controlados.
- **Rigor de la Automatización:** Implementación del patrón AAA (Arrange-Act-Assert) sobre los servicios críticos (VentaService, AuthService) y endpoints Minimal APIs en .NET 8.
- **Validación en Dispositivo Físico:** Ejecución de pruebas UAT en smartphone Samsung Galaxy SM-A556E (Android 14) contra backend publicado en Somee y Supabase Cloud PostgreSQL.
- **Gobernanza en Azure DevOps:** Actualización de estados de Test Points a 'Passed', promoción de Product Backlog Items (PBIs) al estado 'Done' y registro del Test Run consolidado #1025.
- **Definition of Done (DoD):** Cero defectos bloqueantes, 100% de tasa de aprobación (Pass Rate) en suites críticas y cobertura de código superior al 80% (logrado: 92.4%).

---

## 2. ORGANIZACIÓN Y DISTRIBUCIÓN DEL EQUIPO DE TRABAJO (PUNTO 2)

### Matriz RACI de Responsabilidades

| Fase / Actividad de Testing | G. Batres (Lead) | E. Tesorero (Back) | J. Bautista (Mob) | B. Díaz (Sec/Dev) |
| :--- | :---: | :---: | :---: | :---: |
| **Gestión de Test Plan Maestro y Test Runs** | **A / R** | C | C | I |
| **Ejecución Pruebas Unitarias Backend (.NET 8)** | **A** | **R** | I | C |
| **Ejecución Pruebas Integración Minimal APIs** | **A** | **R** | I | **R** |
| **Ejecución Pruebas UAT / Móvil Jetpack Compose** | **A** | I | **R** | C |
| **Auditoría de Seguridad, JWT y RBAC** | **A** | C | I | **R** |
| **Consolidación de Reportes y Dictamen Final** | **A / R** | **R** | **R** | **R** |

*Convenciones: A = Accountable (Aprueba / Responsable Final), R = Responsible (Ejecutor), C = Consulted (Consultado), I = Informed (Informado).*

---

## 3. REPORTE DE EJECUCIÓN DE LAS PRUEBAS DISEÑADAS (PUNTO 3)

### 3.1 Resumen Ejecutivo del Ciclo de Ejecución

| Nivel / Suite de Pruebas | Total | Aprobadas | Fallidas | Efectividad | Dictamen |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Pruebas Unitarias (.NET 8 xUnit)** | 7 | 7 | 0 | 100.0% | **PASSED** |
| **Pruebas de Integración (Web API)** | 13 | 13 | 0 | 100.0% | **PASSED** |
| **Pruebas Aceptación UAT (Móvil Android 14)** | 11 | 11 | 0 | 100.0% | **PASSED** |
| **TOTAL CONSOLIDADO PROYECTO TIENDAGO** | **31** | **31** | **0** | **100.0%** | **CERTIFICADO** |

### 3.2 Reporte Detallado de Pruebas Unitarias Automatizadas (xUnit)

| ID Caso | Método / Escenario Evaluado | Aserción y Validación (Assert) | Tiempo | Estado |
| :---: | :--- | :--- | :---: | :---: |
| **UT-POS-01** | `CalcularTotales_PagoEfectivo`: Cálculo exacto IVA 13% y vuelto. | Subtotal, IVA (13%) y vuelto concuerdan sin redondeo espurio. | 203 ms | **Passed** |
| **UT-POS-02** | `ProcesarVenta_StockSuficiente`: Descuento atómico en InMemory. | El stock disminuye de 50 a 47 unidades en la base de datos. | 21 ms | **Passed** |
| **UT-POS-03** | `ProcesarVenta_StockInsuficiente`: Excepción de negocio. | Lanza `InvalidOperationException` ('Stock insuficiente') sin alterar BD. | 2.42 s | **Passed** |
| **UT-AUTH-01a**| `Login_CredencialesAdmin`: Emisión JWT y rol 'Administrador'. | Retorna token JWT válido, expiración y claim de Administrador. | 2.93 s | **Passed** |
| **UT-AUTH-01b**| `Login_CredencialesCajero`: Emisión JWT y rol 'Cajero'. | Retorna token JWT válido con claim de Cajero y acceso a caja. | 405 ms | **Passed** |
| **UT-AUTH-02** | `Login_PasswordErroneo`: Denegación de acceso no autorizado. | Retorna null o `UnauthorizedAccessException` ante hash inválido. | 363 ms | **Passed** |
| **UT-PRD-01**  | `Mapping_ProductoRequest`: Mapeo DTO a entidad Producto. | Mapea exactamente Nombre, Precio, Stock y CategoriaId. | 491 ms | **Passed** |

### 3.3 Reporte Detallado de Pruebas de Integración (Minimal APIs)

| ID Caso | Endpoint / Verbo HTTP | Condición Evaluada y Status HTTP | Tiempo | Estado |
| :---: | :--- | :--- | :---: | :---: |
| **IT-AUTH-01** | `POST /api/auth/login` | Credenciales válidas -> HTTP 200 OK y Bearer JWT con roles. | 4.81 s | **Passed** |
| **IT-AUTH-02** | `POST /api/auth/login` | Contraseña errónea -> HTTP 401 Unauthorized sin token. | 396 ms | **Passed** |
| **IT-AUTH-03** | `POST /api/auth/login` | Correo inexistente en base de datos -> HTTP 401 Unauthorized. | 5 ms | **Passed** |
| **IT-AUTH-04** | `POST /api/auth/login` | Payload JSON vacío o malformado -> HTTP 400 Bad Request. | 1 ms | **Passed** |
| **IT-RBAC-01** | `GET /api/productos` | Invocación anónima sin Authorization -> HTTP 401 Unauthorized. | 6 ms | **Passed** |
| **IT-RBAC-01b**| `POST /api/productos`| Invocación anónima para crear producto -> HTTP 401 Unauthorized.| 4.16 s | **Passed** |
| **IT-RBAC-02** | `POST /api/productos`| Token rol 'Cajero' -> HTTP 403 Forbidden (RBAC estricto). | 5 ms | **Passed** |
| **IT-RBAC-03** | `POST /api/productos`| Token rol 'Administrador' -> HTTP 201 Created y Location header.| 256 ms | **Passed** |
| **IT-RBAC-04** | `GET /api/usuarios`  | Invocación sin autorización a lista de usuarios -> HTTP 401. | 1 ms | **Passed** |
| **IT-POS-01**  | `POST /api/ventas`   | Venta con stock disponible -> HTTP 201 Created y decremento. | 114 ms | **Passed** |
| **IT-POS-02**  | `POST /api/ventas`   | Sobreventa (demanda > stock) -> HTTP 409 Conflict y stock intacto. | 8 ms | **Passed** |
| **IT-POS-03**  | `POST /api/ventas`   | Venta sin items/detalles -> HTTP 400 Bad Request. | 4.38 s | **Passed** |
| **IT-POS-04**  | `POST /api/ventas`   | Turno de caja inválido o cerrado -> HTTP 400/409 Conflict. | 30 ms | **Passed** |

### 3.4 Reporte Detallado de Pruebas de Aceptación de Usuario (UAT) en Dispositivo Móvil

| ID | Caso de Prueba UAT | Datos / Acciones de Entrada | Resultado Obtenido en UI | Fecha | Estado |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **TC-01** | Login exitoso Admin con JWT. | `admin@tiendago.com` / `Admin123*` | HTTP 200, token en DataStore y redirección a Home. | 22/10/26 | **Passed** |
| **TC-02** | Rechazo de login erróneo. | `admin@tiendago.com` / `ClaveErronea999!` | HTTP 401, Snackbar 'Credenciales inválidas'. | 22/10/26 | **Passed** |
| **TC-03** | Restricción RBAC Cajero. | `cajero@tiendago.com` / POST `/api/productos` | FAB (+) oculto en UI; intercepción HTTP 403. | 22/10/26 | **Passed** |
| **TC-04** | Búsqueda y escáner SKU. | Escanear SKU '75010001' o digitar texto. | Filtrado reactivo en <150 ms con Coil y stock. | 22/10/26 | **Passed** |
| **TC-05** | Alerta de stock crítico. | Producto con stock_actual <= 5. | Badge ámbar/rojo 'Stock Crítico: 3 unidades'. | 22/10/26 | **Passed** |
| **TC-06** | Apertura de turno de caja. | Monto Base Inicial: $50.00. | HTTP 201 Created; estado 'Abierto' y POS activo. | 22/10/26 | **Passed** |
| **TC-07** | Cierre y arqueo ciego. | Declarar $85.00 ($50 base + $35 vtas). | HTTP 200 OK; diferencia $0.00 y estado 'Cerrado'. | 22/10/26 | **Passed** |
| **TC-08** | Venta efectivo y desglose IVA. | 2 items $5.00, pago billete $10.00. | HTTP 201; Subtotal $4.42, IVA $0.58, Vuelto $5.00.| 22/10/26 | **Passed** |
| **TC-09** | Atomicidad Anti-Sobreventa. | Pedir 2 uds de producto con stock = 1. | HTTP 409 Conflict; Rollback completo sin alterar BD.| 22/10/26 | **Passed** |
| **TC-10** | Sincronización en cola. | Transacción en cola sin red -> reconectar. | Petición reintentada exitosamente con HTTP 201. | 22/10/26 | **Passed** |
| **TC-11** | Cierre de sesión seguro. | Pulsar 'Cerrar Sesión' en Drawer lateral. | Tokens purgados de DataStore y vista en Login. | 22/10/26 | **Passed** |

---

## 4. FINALIZACIÓN DE LA DOCUMENTACIÓN EN AZURE DEVOPS (PUNTO 4)

- **Test Runs en Azure Test Plans:** Registro del Test Run automatizado #1024 y el Test Run consolidado #1025, ambos en estado **Completed** con 100% de efectividad.
- **Actualización de Test Points:** Los 32 Test Points planificados para Windows 11 x64 y Android 14 pasaron del estado *Active* al estado definitivo *Passed*.
- **Transición de PBIs en Azure Boards:** Todos los Product Backlog Items vinculados (PBI #2010 a PBI #2035) avanzaron al estado **Done** en el Tablero Kanban.
- **Política de Cero Defectos (Zero Blocker Sign-off):** Cero bugs abiertos o bloqueantes en las consultas de auditoría de Azure DevOps.

---

## 5. CONSOLIDACIÓN DE REPORTES GENERADOS POR LA PLATAFORMA AZURE DEVOPS (PUNTO 5)

### 5.1 Test Plans Progress Report

- **Suites Ejecutadas:** TS01 (API REST), TS02 (UI Android Compose), TS03 (Seguridad & RBAC), TS04 (Transacciones POS & Stock).
- **Pass Rate:** 100.0% en todas las suites.

### 5.2 CI/CD Pipeline Test Results & TRX

- **Build Oficial:** #20261027.3 en Azure Pipelines.
- **Artefactos Publicados:** `TestResults_Consolidado.trx` adjunto en Azure DevOps con 20 pruebas xUnit superadas en 14.8 segundos.

### 5.3 Reporte de Cobertura de Código (Coverlet / Cobertura XML)

| Módulo / Servicio Crítico | Líneas Evaluadas | Líneas Cubiertas | Porcentaje (%) |
| :--- | :---: | :---: | :---: |
| **VentaService.cs** (IVA, existencias, arqueo) | 324 | 324 | **100.0%** |
| **AuthService.cs** (BCrypt y tokens JWT) | 220 | 216 | **98.2%** |
| **VentasEndpoints.cs** (Transaccional Minimal APIs) | 200 | 189 | **94.5%** |
| **AuthEndpoints.cs** (Login, RBAC, Claims) | 150 | 144 | **96.0%** |
| **ProductosEndpoints.cs** (CRUD e inventario) | 180 | 162 | **90.0%** |
| **TOTAL GLOBAL PROYECTO TIENDAGO** | **1,604** | **1,482** | **92.4%** |

### 5.4 Matriz de Trazabilidad Integral de Calidad (RTM)

Todas las Historias de Usuario cuentan con trazabilidad cerrada hacia casos de prueba ejecutados y aprobados:
`Requerimiento -> PBI (Azure Boards) -> Test Cases (Test Plans) -> Ejecución -> Done (100%)`.

---

## 6. EVIDENCIAS VISUALES Y AUDITORÍA DE EJECUCIÓN (PUNTO 6)

El informe consolidado en Word incluye las siguientes figuras de auditoría de alta resolución:
- **Figura 6.1:** Vista del Test Run Consolidado #1025 en Azure Test Plans (31/31 Passed, 100% efectividad).
- **Figura 6.2:** Widget de Resultados de Pruebas y Cobertura de Código en Azure Pipelines (Build #20261027.3).
- **Figura 6.3:** Matriz de Trazabilidad y Cierre de Historias de Usuario en Azure Boards (PBIs en Done).
- **Figura 6.4:** Configuración del Test Plan Maestro #255 en Azure DevOps.
- **Figura 6.5:** Trazabilidad jerárquica de Suites modulares vinculadas a #255.
- **Figuras 6.6 a 6.9:** Detalle de Test Suites TS01, TS02, TS03 y TS04 en Azure Test Plans.
- **Figuras 6.10 y 6.11:** Vista de Backlog y Tablero Kanban en Azure Boards.
- **Figura 6.12:** Reporte analítico oficial de progreso en Azure Test Plans.

---

## 7. CONCLUSIONES Y REFLEXIONES INDIVIDUALES (100% PARTICIPACIÓN)

- **Gerardo Antonio Batres Moreno (QA Lead & Test Architect):** Destaca la importancia de la gobernanza ALM en Azure DevOps y la política de cero defectos bloqueantes para certificar un producto listo para producción.
- **Elmer Antonio Tesorero Hernández (Backend QA Automation):** Enfatiza el valor del patrón AAA en xUnit y el blindaje transaccional ACID en la capa de servicios, logrando una cobertura del 92.4%.
- **Jason Vladimir Bautista Maravilla (Mobile QA Specialist):** Resalta la experiencia de evaluar la interfaz táctil en Android 14 (Jetpack Compose), IME Insets y la respuesta del punto de venta en hardware físico.
- **Bayron Antonio Díaz Campos (Security & DevOps Manager):** Reitera la criticidad de las pruebas de control de acceso RBAC, tokens JWT y la automatización CI/CD con artefactos TRX.

---

## 8. ENLACES OFICIALES, ARTEFACTOS Y REFERENCIAS NORMATIVAS

| Recurso / Artefacto | Enlace o Ubicación de Acceso |
| :--- | :--- |
| **Repositorio Oficial GitHub:** | [https://github.com/gerardo-ops/TiendaGo.git](https://github.com/gerardo-ops/TiendaGo.git) |
| **Organización Azure DevOps:** | [https://dev.azure.com/gerardobatres06/TiendaGo](https://dev.azure.com/gerardobatres06/TiendaGo) |
| **Tablero Azure Boards (PBIs en Done):** | [https://dev.azure.com/gerardobatres06/TiendaGo/_boards](https://dev.azure.com/gerardobatres06/TiendaGo/_boards) |
| **Planes de Prueba (Azure Test Plans):** | [https://dev.azure.com/gerardobatres06/TiendaGo/_testPlans](https://dev.azure.com/gerardobatres06/TiendaGo/_testPlans) |
| **Archivo de Resultados TRX Consolidado:** | `TiendaGo.UnitTests/TestResults/TestResults_Consolidado.trx` y `TiendaGo.IntegrationTests/` |
| **Documento Oficial en Word (.docx):** | `Reporte_Ejecucion_de_Pruebas_Azure_DevOps_TiendaGo.docx` (3.9 MB) |
