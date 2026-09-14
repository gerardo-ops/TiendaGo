# ESPECIFICACIÓN TÉCNICA Y REQUERIMIENTOS: TIENDAGO

## 1. Rol y Contexto del Proyecto
Actúa como un arquitecto de software y desarrollador Full Stack sénior.
El proyecto se denomina **TiendaGo**, una solución integral compuesta por:
1. **Cliente Móvil (Mobile-First):** Aplicación para dispositivos móviles enfocada en pequeños comercios y bazares, diseñada para sustituir terminales físicas de punto de venta (POS) y lectores láser mediante interfaces táctiles ergonómicas y uso de la cámara del teléfono[cite: 3].
2. **Backend (Web API RESTful):** Capa de servicios web encargada de la persistencia de datos, validaciones de reglas de negocio, seguridad de acceso y transaccionalidad[cite: 3].
3. **Base de Datos:** PostgreSQL en la nube alojado en **Supabase**.

---

## 2. Arquitectura de Alto Nivel
- **Arquitectura:** Cliente-Servidor desacoplado mediante servicios Web RESTful[cite: 3].
- **Formato de Comunicación:** Exclusivamente `application/json`[cite: 1, 2].
- **Seguridad y Autorización:** Endpoints protegidos mediante Bearer Tokens con estándar JWT (JSON Web Tokens)[cite: 1, 3].
- **Consistencia de Inventario:** Operaciones de cobro y descuento de stock ejecutadas bajo transacciones atómicas (propiedades ACID) para evitar inconsistencias y lecturas fantasma.

---

## 3. Estructura de Vistas Móviles (UI/UX)
El cliente móvil opera bajo un flujo centrado en navegación inferior (`BottomNavigationBar`) posterior al inicio de sesión[cite: 3]:
* **W-01 (LoginView):** Pantalla de acceso mediante correo y contraseña para obtener token JWT[cite: 3].
* **W-02 (DashboardView):** Métricas de balance del día en tiempo real (monto facturado, transacciones ejecutadas, alertas de stock bajo) y accesos directos de acción[cite: 3].
* **W-03 (CatalogoProductosView):** Explorador de inventario con filtros por categoría, búsqueda dinámica, badge de advertencia visual para existencias críticas (< 5 unidades) y botón flotante de adición[cite: 2].
* **W-04 (FormularioProductoView):** Modal/Formulario de alta y edición con campos de nombre, código de barras/SKU, costos, precios y stock mínimo[cite: 3].
* **W-05 (TerminalCajaView):** Terminal POS táctil ágil con controles (+/-) para selección de artículos y visor totalizador inferior diseñado para registrar transacciones en menos de 4 toques[cite: 3].
* **W-06 (ConfirmacionPagoView):** Modal de cobro con cálculo en vivo de cambio, selección de método de pago (Efectivo / Transferencia QR) y atajos de billetes táctiles ($10, $20, $50)[cite: 3].
* **W-07 (HistorialVentasView):** Historial cronológico de tickets emitidos agrupados por turno de trabajo con desglose emergente[cite: 3].

---

## 4. Matriz de Endpoints (Web API)
Toda solicitud hacia la API debe adherirse a los siguientes contratos REST:

| Recurso | Método | Endpoint | Descripción | Código Éxito |
| :--- | :---: | :--- | :--- | :---: |
| Autenticación | `POST` | `/api/auth/login` | Valida credenciales de usuario y genera token JWT[cite: 3]. | 200 OK |
| Dashboard | `GET` | `/api/dashboard/resumen` | Retorna total facturado, órdenes del día y alertas[cite: 3]. | 200 OK[cite: 3] |
| Productos | `GET` | `/api/productos` | Consulta el catálogo paginado con soporte a query params (`?buscar=`, `?categoria=`)[cite: 3]. | 200 OK[cite: 3] |
| Productos Activos | `GET` | `/api/productos/activos` | Consulta únicamente productos con existencias para la terminal POS[cite: 3]. | 200 OK |
| Detalle Producto | `GET` | `/api/productos/{id}` | Retorna la ficha técnica de un producto individual[cite: 2]. | 200 OK |
| Crear Producto | `POST` | `/api/productos` | Registra un nuevo producto en catálogo con stock inicial[cite: 1]. | 201 Created[cite: 1, 2] |
| Editar Producto | `PUT` | `/api/productos/{id}` | Actualiza datos, existencias o precios del ítem[cite: 1]. | 200 OK[cite: 2] |
| Eliminar Producto | `DELETE`| `/api/productos/{id}` | Baja lógica o eliminación física del recurso[cite: 1, 2]. | 204 No Content[cite: 2] |
| Procesar Venta | `POST` | `/api/ventas` | Registra cabecera de orden, líneas de detalle y descuenta stock atómicamente[cite: 1]. | 201 Created[cite: 1, 2] |
| Historial Ventas | `GET` | `/api/ventas` | Retorna tickets paginados con filtros temporales. | 200 OK |

---

## 5. Esquema Relacional de Base de Datos (Supabase / PostgreSQL)
Las tablas estructuradas en 3FN a considerar son:
1. `roles` (`id_rol` PK, `nombre_rol`, `descripcion`)
2. `usuarios` (`id_usuario` PK, `id_rol` FK, `nombre_completo`, `correo_electronico` UNIQUE, `clave_hash`, `estado_activo`, `fecha_registro`)
3. `categorias` (`id_categoria` PK, `nombre_categoria` UNIQUE, `descripcion`, `estado_activo`)
4. `productos` (`id_producto` PK, `id_categoria` FK, `nombre_producto`, `codigo_sku` UNIQUE, `costo_compra`, `precio_venta`, `stock_actual`, `stock_minimo`, `url_imagen`, `estado_activo`, `fecha_creacion`)
5. `metodos_pago` (`id_metodo_pago` PK, `nombre_metodo`, `estado_activo`)
6. `turnos_caja` (`id_turno` PK, `id_usuario` FK, `fecha_apertura`, `fecha_cierre`, `monto_base_inicial`, `total_ventas_efectivo`, `total_ventas_digital`, `monto_declarado`, `diferencia_cuadre`, `estado_turno`)
7. `ventas` (`id_venta` PK, `id_turno` FK, `id_usuario` FK, `id_metodo_pago` FK, `numero_ticket` UNIQUE, `fecha_hora`, `subtotal`, `total_iva`, `total_venta`, `monto_recibido`, `cambio_entregado`, `estado_venta`)
8. `detalles_venta` (`id_detalle` PK, `id_venta` FK, `id_producto` FK, `cantidad`, `precio_unitario_historico`, `subtotal_linea`)

---

## 6. Instrucciones Directas para el Asistente
- Prioriza siempre código modular, limpio y tipado.
- La aplicación cliente es **móvil**; diseña componentes adaptables a pantallas táctiles evitando patrones de escritorio[cite: 3].
- Al generar servicios de red en el cliente móvil, utiliza clientes HTTP asíncronos desacoplados con manejo estricto de excepciones y almacenamiento seguro del token JWT[cite: 3].
- Al generar controladores o servicios de backend, asegura que las operaciones sobre el inventario verifiquen stock disponible antes de persistir cualquier venta.