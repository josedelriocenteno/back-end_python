# Normalización de Bases de Datos: El Fundamento de la Integridad

La normalización es el proceso de organizar los datos en una base de datos relacional para reducir la redundancia y mejorar la integridad. Su objetivo es asegurar que cada dato esté exactamente donde debe estar: ni más, ni menos.

## 1. ¿Por qué normalizar?

En un backend profesional, una base de datos no normalizada causa:
*   **Anomalías de Inserción:** No puedes insertar un dato si falta otro relacionado (ej: no puedes crear un curso si no hay alumnos).
*   **Anomalías de Actualización:** Tienes que cambiar el nombre de un cliente en 50 facturas diferentes. Si fallas en una, el dato es inconsistente.
*   **Anomalías de Borrado:** Al borrar un registro, pierdes información valiosa que no querías borrar (ej: borras el último pedido y desaparece el producto).

## 2. Las Tres Formas Normales (1NF, 2NF, 3NF)

Para considerar una base de datos "profesional", debe cumplir al menos hasta la 3NF.

### Primera Forma Normal (1NF): Atomicidad
*   **Regla:** Cada columna debe contener un solo valor atómico (indivisible) y no debe haber grupos de valores repetidos.
*   **Mal diseño:** Una columna `telefonos` con valor `"666111, 777222"`.
*   **Solución:** Mueve los teléfonos a una tabla hija o usa una columna por teléfono (si el número es fijo).

### Segunda Forma Normal (2NF): Dependencia Funcional Completa
*   **Regla:** Debe cumplir la 1NF y todas las columnas que no son parte de la Clave Primaria (PK) deben depender de la PK completa.
*   **Mal diseño:** Tabla `Pedidos_Productos` con `pedido_id`, `producto_id`, `cantidad` y `nombre_producto`.
    *   `nombre_producto` depende de `producto_id`, no de `pedido_id`. Si cambia el nombre, tienes un lío.
*   **Solución:** El `nombre_producto` va a la tabla `Productos`.

### Tercera Forma Normal (3NF): Independencia de Tránsito
*   **Regla:** Debe cumplir la 2NF y ninguna columna "no-clave" debe depender de otra columna "no-clave".
*   **Mal diseño:** Tabla `Usuarios` con `id`, `nombre`, `zip_code`, `ciudad`.
    *   La `ciudad` depende del `zip_code`. El `zip_code` depende del `id`. Hay una dependencia transitiva.
*   **Solución:** Crea una tabla de `CodigosPostales` con `zip_code` y `ciudad`.

## 3. Ejemplo Práctico: De Caos a 3NF

### Tabla Desastrosa (No Normalizada):
| ID_Pedido | Cliente | Email | Producto | Precio | Cat_Nombre | Cat_Desc |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Juan | j@a.com | Laptop | 1000 | Electrónica | Gadgets etc |

### Diseño Normalizado (3NF):
1.  **Tablas de Entidad:** `Clientes` (id, nombre, email).
2.  **Tablas de Clasificación:** `Categorias` (id, nombre, descripcion).
3.  **Tablas de Producto:** `Productos` (id, nombre, precio, categoria_id).
4.  **Tablas de Transacción:** `Pedidos` (id, cliente_id, fecha).
5.  **Tablas de Detalle:** `Lineas_Pedido` (id, pedido_id, producto_id, cantidad, precio_unitario).

## 4. Beneficios para el Código Python

1.  **Modelos Limpios:** Tus clases de SQLAlchemy o Pydantic reflejan entidades únicas y claras.
2.  **Menos Bugs:** Al no haber datos duplicados, no hay riesgo de que "el email del usuario X sea diferente en la tabla A y en la B".
3.  **Flexibilidad:** Añadir una nueva característica (ej: múltiples direcciones de envío) es fácil porque la estructura ya es modular.

## 5. El Límite de la Normalización

Normalizar demasiado (ej: 4NF, 5NF o BCNF) puede llevar a una fragmentación excesiva, obligándote a hacer 15 JOINs para una consulta simple. Esto afecta al rendimiento. Por eso, en el siguiente tema veremos cuándo es bueno "romper las reglas".
