# Índices Avanzados: Tipos y Estrategias

Un índice es como el índice al final de un libro: permite encontrar información sin leer todas las páginas. Pero no todos los índices son iguales.

## 1. B-Tree (El estándar)
Es el tipo por defecto en casi todas las bases de datos.
*   **Uso:** Comparaciones de igualdad (`=`) y rangos (`>`, `<`, `BETWEEN`).
*   **Funcionamiento:** Estructura de árbol balanceado. Muy eficiente para la mayoría de los casos.

## 2. Hash Index (Solo Igualdad)
*   **Uso:** Solo para comparaciones de igualdad exacta (`=`). No sirve para rangos.
*   **Ventaja:** En teoría es más rápido que B-Tree para búsquedas puntuales, pero menos flexible.

## 3. GIN (Generalized Inverted Index)
Vital para tipos de datos complejos.
*   **Uso:** Columnas **JSONB**, arrays o búsqueda de texto (Full Text Search).
*   **Ejemplo:** Buscar una clave dentro de un campo JSON en miles de filas.

## 4. GIST / SP-GIST (Datos Espaciales y Rangos)
*   **Uso:** Coordenadas GPS (Geometría), rangos de fechas solapados.
*   **Librería:** Muy usado con PostGIS.

## 5. Índices Parciales (Ahorrando espacio)
Solo indexan una parte de la tabla.
```sql
CREATE INDEX idx_pedidos_pendientes 
ON pedidos (fecha_creacion) 
WHERE estado = 'pendiente';
```
*   **Ventaja:** El índice es mucho más pequeño y rápido de actualizar porque ignora los millones de pedidos que ya están 'finalizados'.

## 6. Índices Compuestos (Multicolumna)
Un índice basado en varias columnas: `(apellido, nombre)`.
*   **REGLA DE ORO:** El orden importa. Este índice sirve para buscar por `apellido` solo, o por `apellido` + `nombre`. Pero NO sirve para buscar solo por `nombre`.

## 7. El coste oculto de los índices
Cada índice hace que las consultas `SELECT` sean más rápidas, pero que las operaciones `INSERT`, `UPDATE` y `DELETE` sean **más lentas** (porque la base de datos tiene que actualizar el índice también).
> [!TIP]
> No indexas todo por si acaso. Indexa solo lo que realmente usas en tus clausulas `WHERE` y `JOIN`.

## Resumen: La herramienta de precisión
Elige el tipo de índice que mejor se adapte a tus datos. Un índice `GIN` para JSON o un índice `Parcial` pueden transformar una consulta de minutos en milisegundos, optimizando drásticamente el rendimiento global.
