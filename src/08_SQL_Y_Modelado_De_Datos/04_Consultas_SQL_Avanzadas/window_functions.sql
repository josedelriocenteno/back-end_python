-- =============================================================================
-- SQL PROFESIONAL: WINDOW FUNCTIONS (FUNCIONES DE VENTANA)
-- ANALÍTICA AVANZADA SIN "AGRUPAR" FILAS
-- =============================================================================

/*
¿QUÉ ES UNA WINDOW FUNCTION?
-----------------------------------------------------------------------------
A diferencia de GROUP BY, que "colapsa" las filas en una sola, las Window 
Functions realizan cálculos sobre un conjunto de filas relacionadas con la 
fila actual, pero MANTIENEN la identidad de cada fila.

Sintaxis básica:
FUNCTION_NAME() OVER (PARTITION BY ... ORDER BY ...)
*/

-- -----------------------------------------------------------------------------
-- 1. RANKING Y POSICIONAMIENTO (ROW_NUMBER, RANK)
-- -----------------------------------------------------------------------------

-- Enumerar órdenes por usuario ordenadas por fecha
SELECT 
    user_id,
    id as order_id,
    created_at,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at ASC) as order_sequence_number
FROM orders;

-- Encontrar los 3 productos más caros de cada categoría
WITH ranked_products AS (
    SELECT 
        name, 
        category_id, 
        price,
        DENSE_RANK() OVER (PARTITION BY category_id ORDER BY price DESC) as rnk
    FROM products
)
SELECT * FROM ranked_products WHERE rnk <= 3;

-- -----------------------------------------------------------------------------
-- 2. AGREGACIONES ACUMULATIVAS (Running Totals)
-- -----------------------------------------------------------------------------

-- Calcular el acumulado de ventas a lo largo del tiempo
SELECT 
    created_at::DATE as day,
    total_amount,
    SUM(total_amount) OVER (ORDER BY created_at) as running_total_revenue
FROM orders;

-- -----------------------------------------------------------------------------
-- 3. COMPARACIÓN CON FILAS ANTERIORES/POSTERIORES (LAG & LEAD)
-- -----------------------------------------------------------------------------

/*
Crucial para calcular variaciones porcentuales (Growth, MoM, WoW).
- LAG: Accede a la fila anterior.
- LEAD: Accede a la fila siguiente.
*/

SELECT 
    DATE_TRUNC('month', created_at) as month,
    SUM(total_amount) as monthly_revenue,
    LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', created_at)) as prev_month_revenue,
    (SUM(total_amount) - LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', created_at))) / 
        LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('month', created_at)) * 100 as growth_percentage
FROM orders
GROUP BY month;

-- -----------------------------------------------------------------------------
-- 4. DIFERENCIA ENTRE PARTITION BY Y GROUP BY
-- -----------------------------------------------------------------------------

-- Comparar el precio de un producto con el precio medio de su categoría
SELECT 
    name, 
    price,
    category_id,
    AVG(price) OVER (PARTITION BY category_id) as category_avg_price,
    price - AVG(price) OVER (PARTITION BY category_id) as difference_from_avg
FROM products;

-- -----------------------------------------------------------------------------
-- 5. WINDOWS FRAME (Filtros dinámicos dentro de la ventana)
-- -----------------------------------------------------------------------------

-- Media móvil de los últimos 7 días (Moving Average)
SELECT 
    created_at::DATE as date,
    total_amount,
    AVG(total_amount) OVER (
        ORDER BY created_at::DATE 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7d
FROM orders;

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEARROLLADOR:
-- -----------------------------------------------------------------------------
-- 1. Usa Window Functions para evitar JOINs innecesarios contra la misma tabla.
-- 2. ROW_NUMBER() es ideal para paginación compleja o deduplicación.
-- 3. LAG/LEAD son tus mejores amigos para dashboards y analítica de negocio.
-- 4. Recuerda que las Window Functions se ejecutan DESPUÉS del WHERE. Si quieres
--    filtrar por el resultado de una de ellas, debes usar una CTE o Subquery.
-- 5. No abuses: Window Functions complejas pueden ser costosas en CPU.
-- -----------------------------------------------------------------------------
