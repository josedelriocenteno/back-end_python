-- =============================================================================
-- SQL PROFESIONAL: SUBQUERIES (SUBCONSULTAS)
-- COMPOSICIÓN DE QUERIES COMPLEJAS
-- =============================================================================

/*
¿QUÉ ES UNA SUBQUERY?
-----------------------------------------------------------------------------
Es una consulta anidada dentro de otra consulta principal. 
Son potentes, flexibles y a veces necesarias cuando un JOIN no es suficiente
o es menos legible.

Tipos de Subqueries:
1. Escalares: Devuelven un solo valor (1 fila, 1 columna).
2. De Conjunto: Devuelven una lista de valores o múltiples filas.
3. Correlacionadas: La subquery depende de valores de la query externa.
*/

-- -----------------------------------------------------------------------------
-- 1. SUBQUERY ESCALAR (Valor único)
-- -----------------------------------------------------------------------------

-- Productos cuyo precio es superior a la media
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- -----------------------------------------------------------------------------
-- 2. EN LA CLÁUSULA 'IN' (Conjuntos)
-- -----------------------------------------------------------------------------

-- Usuarios que han realizado al menos una orden "Premium" (> 1000)
SELECT username, email
FROM users
WHERE id IN (
    SELECT DISTINCT user_id 
    FROM orders 
    WHERE total_amount > 1000
);

-- -----------------------------------------------------------------------------
-- 3. SUBQUERY CORRELACIONADA (Dependencia externa)
-- -----------------------------------------------------------------------------

/*
IMPORTANTE: Se ejecutan una vez por cada fila de la query principal.
Utilízalas con cuidado en tablas muy grandes.
*/

-- Nombre del producto y cuántas veces se ha vendido ese producto específico
SELECT 
    p.name,
    (SELECT COUNT(*) FROM order_items oi WHERE oi.product_id = p.id) AS sales_count
FROM products p;

-- -----------------------------------------------------------------------------
-- 4. EXISTS vs IN
-- -----------------------------------------------------------------------------

/*
EXISTS suele ser más eficiente que IN para comprobar existencia, 
especialmente si la subquery devuelve muchos datos, ya que Postgres para 
al encontrar la primera coincidencia.
*/

-- Usuarios que tienen al menos una orden
SELECT username
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- -----------------------------------------------------------------------------
-- 5. SUBQUERIES EN EL 'FROM' (Derive Tables)
-- -----------------------------------------------------------------------------

/*
Tratamos el resultado de una query como si fuera una tabla física.
Muy útil para hacer agregaciones de agregaciones.
*/

SELECT AVG(user_total_spent) as avg_customer_value
FROM (
    SELECT user_id, SUM(total_amount) as user_total_spent
    FROM orders
    GROUP BY user_id
) as user_spending_stats;

-- -----------------------------------------------------------------------------
-- 6. CTEs (Common Table Expressions) - EL ESTÁNDAR PRO
-- -----------------------------------------------------------------------------

/*
En lugar de subqueries anidadas imposibles de leer, usamos WITH.
Las CTEs hacen que el código sea modular, legible y fácil de debuguear.
*/

WITH regional_sales AS (
    SELECT region, SUM(amount) AS total_sales
    FROM orders
    GROUP BY region
),
top_regions AS (
    SELECT region
    FROM regional_sales
    WHERE total_sales > (SELECT SUM(total_sales)/10 FROM regional_sales)
)
SELECT * FROM regional_sales
WHERE region IN (SELECT region FROM top_regions);

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEVELOPER:
-- -----------------------------------------------------------------------------
-- 1. Si tu subquery es compleja, usa una CTE (WITH). Tu "yo" del futuro lo agradecerá.
-- 2. Usa EXISTS para comprobaciones de existencia por rendimiento.
-- 3. Evita subqueries correlacionadas en el SELECT si puedes usar un JOIN + GROUP BY.
-- 4. Recuerda que las subqueries en el FROM necesitan un ALIAS siempre.
-- -----------------------------------------------------------------------------
