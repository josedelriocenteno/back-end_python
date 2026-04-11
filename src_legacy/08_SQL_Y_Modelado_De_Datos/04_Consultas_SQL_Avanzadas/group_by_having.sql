-- =============================================================================
-- SQL PROFESIONAL: AGREGACIONES - GROUP BY & HAVING
-- RESUMIENDO DATOS CON INTELIGENCIA
-- =============================================================================

/*
INTRODUCCIÓN A LAS AGREGACIONES
-----------------------------------------------------------------------------
Las funciones de agregación (SUM, AVG, COUNT, MIN, MAX) procesan múltiples 
filas para devolver un único resultado. 

GROUP BY es el motor que permite aplicar estas funciones a grupos específicos
(ej: total de ventas POR categoría).
*/

-- -----------------------------------------------------------------------------
-- 1. FUNCIONES ESTÁNDAR Y GROUP BY
-- -----------------------------------------------------------------------------

SELECT 
    category_id,
    COUNT(*) AS total_products,
    MIN(price) AS min_price,
    MAX(price) AS max_price,
    AVG(price) AS avg_price,
    SUM(price) AS stock_value
FROM products
GROUP BY category_id;

-- -----------------------------------------------------------------------------
-- 2. GROUP BY MULTI-COLUMNA
-- -----------------------------------------------------------------------------

SELECT 
    status,
    category_id,
    COUNT(*) as total
FROM products
GROUP BY status, category_id
ORDER BY status, total DESC;

-- -----------------------------------------------------------------------------
-- 3. HAVING: EL "WHERE" DE LOS GRUPOS
-- -----------------------------------------------------------------------------

/*
REGLA DE ORO:
- WHERE filtra FILAS antes de agrupar.
- HAVING filtra GRUPOS después de agrupar.
*/

-- Categorías que tienen más de 10 productos activos
SELECT category_id, COUNT(*)
FROM products
WHERE status = 'active'
GROUP BY category_id
HAVING COUNT(*) > 10;

-- -----------------------------------------------------------------------------
-- 4. COUNT(*) vs COUNT(column) vs COUNT(DISTINCT)
-- -----------------------------------------------------------------------------

/*
- COUNT(*): Cuenta todas las filas (incluyendo NULLs).
- COUNT(description): Cuenta solo las filas donde description NO es NULL.
- COUNT(DISTINCT user_id): Cuenta valores únicos (útil para "Usuarios únicos").
*/

SELECT 
    COUNT(*) as total_orders,
    COUNT(DISTINCT user_id) as unique_customers
FROM orders;

-- -----------------------------------------------------------------------------
-- 5. TRUCO DE BACKEND: GROUP BY CON EXPRESIONES
-- -----------------------------------------------------------------------------

-- Ventas agrupadas por año y mes (Formatos de fecha)
SELECT 
    DATE_TRUNC('month', created_at) AS month,
    SUM(total_amount) AS revenue
FROM orders
GROUP BY month
ORDER BY month DESC;

-- -----------------------------------------------------------------------------
-- 6. FILTRADO CONDICIONAL DENTRO DE AGREGACIÓN (FILTER)
-- -----------------------------------------------------------------------------

/*
Postgres permite una sintaxis super limpia para contar cosas diferentes
en una sola query sin usar múltiples subqueries.
*/

SELECT 
    category_id,
    COUNT(*) AS total_items,
    COUNT(*) FILTER (WHERE status = 'active') AS active_items,
    COUNT(*) FILTER (WHERE status = 'draft') AS draft_items
FROM products
GROUP BY category_id;

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEARROLLADOR:
-- -----------------------------------------------------------------------------
-- 1. No puedes usar alias de agregación en el WHERE (usa HAVING).
-- 2. Cualquier columna en el SELECT que no sea una función de agregación DEBE 
--    estar en el GROUP BY.
-- 3. DATE_TRUNC es tu mejor amigo para reportes temporales.
-- 4. Usa FILTER (WHERE...) para métricas complejas en una sola pasada.
-- 5. OJO con el rendimiento: GROUP BY sobre millones de filas sin índices 
--    en las columnas de agrupación puede ser muy lento.
-- -----------------------------------------------------------------------------
