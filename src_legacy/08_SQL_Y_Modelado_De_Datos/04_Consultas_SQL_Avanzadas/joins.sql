-- =============================================================================
-- SQL PROFESIONAL: CONSULTAS AVANZADAS - JOINs
-- RELACIONANDO DATOS COMO UN ARQUITECTO DE BACKEND
-- =============================================================================

/*
¿POR QUÉ JOINs?
-----------------------------------------------------------------------------
En una DB relacional, la información está dispersa para evitar redundancia
(Normalización). Los JOINs son la herramienta para unir esas piezas y 
presentar información coherente a tu aplicación Python.

Claves de un JOIN profesional:
1. Claridad: Usa alias cortos pero descriptivos.
2. Rendimiento: Une solo lo necesario.
3. Precisión: Elige el tipo de JOIN correcto para no perder datos.
*/

-- -----------------------------------------------------------------------------
-- 1. INNER JOIN: LA UNIÓN ESTÁNDAR
-- -----------------------------------------------------------------------------

/*
Devuelve solo las filas que tienen coincidencia en AMBAS tablas.
Es el JOIN más común y el más eficiente.
*/

SELECT 
    u.username, 
    o.id AS order_id, 
    o.total_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.is_active = true;

-- -----------------------------------------------------------------------------
-- 2. LEFT JOIN (LEFT OUTER JOIN): LA UNIÓN INCLUSIVA
-- -----------------------------------------------------------------------------

/*
Devuelve todas las filas de la tabla de la IZQUIERDA, y las coincidencias 
de la derecha. Si no hay coincidencia, devuelve NULL.
Muy útil para encontrar "huérfanos" o registrar "ceros".
*/

-- Ejemplo: Usuarios y cuántas órdenes tienen (incluyendo los que no tienen ninguna)
SELECT 
    u.username, 
    COUNT(o.id) AS total_orders
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.username;

-- -----------------------------------------------------------------------------
-- 3. RIGHT JOIN & FULL OUTER JOIN
-- -----------------------------------------------------------------------------

-- RIGHT JOIN: Inverso al LEFT. Rara vez se usa, se suele preferir reordenar
-- las tablas y usar LEFT JOIN por legibilidad.

-- FULL OUTER JOIN: Devuelve todo lo de ambas tablas, con NULLs donde no hay match.
-- Útil para reconciliación de datos pesada.

SELECT 
    u.username, 
    p.name AS profile_name
FROM users u
FULL OUTER JOIN profiles p ON u.id = p.user_id;

-- -----------------------------------------------------------------------------
-- 4. CROSS JOIN: PRODUCTO CARTESIANO
-- -----------------------------------------------------------------------------

/*
Une cada fila de A con cada fila de B. Genera A x B filas.
CUIDADO: En tablas grandes, esto puede tumbar tu DB.
Útil para generar combinaciones (ej: todas las tallas x todos los colores).
*/

SELECT 
    colors.name AS color, 
    sizes.name AS size
FROM colors
CROSS JOIN sizes;

-- -----------------------------------------------------------------------------
-- 5. SELF JOIN: LA TABLA SE UNE A SÍ MISMA
-- -----------------------------------------------------------------------------

/*
Crucial para estructuras jerárquicas (Categorías padre-hijo, Managers-Empleados).
*/

SELECT 
    child.name AS category, 
    parent.name AS parent_category
FROM categories child
LEFT JOIN categories parent ON child.parent_id = parent.id;

-- -----------------------------------------------------------------------------
-- 6. MÚLTIPLES JOINs Y OPTIMIZACIÓN
-- -----------------------------------------------------------------------------

/*
El orden de los JOINs importa para la legibilidad, aunque el optimizador 
de Postgres suele decidir el mejor plan de ejecución.
*/

SELECT 
    u.username,
    p.name AS product_name,
    c.name AS category_name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE o.status = 'completed';

-- -----------------------------------------------------------------------------
-- 7. JOINs CON FILTROS EN LA CLÁUSULA 'ON' VS 'WHERE'
-- -----------------------------------------------------------------------------

/*
Diferencia sutil pero vital en LEFT JOINs:
- El filtro en ON se aplica ANTES de la unión.
- El filtro en WHERE se aplica DESPUÉS de la unión.
*/

-- Trae todos los usuarios, pero solo las órdenes de hoy
SELECT u.username, o.id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id AND o.created_at >= CURRENT_DATE;

-- Trae solo usuarios que tienen órdenes de hoy (se comporta como un INNER JOIN)
SELECT u.username, o.id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= CURRENT_DATE;

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEVELOPER:
-- -----------------------------------------------------------------------------
-- 1. Usa alias coherentes (u, o, p) para no perderte en queries largas.
-- 2. Prefiere el INNER JOIN por defecto por rendimiento.
-- 3. Usa LEFT JOIN cuando la relación sea opcional (0 a N).
-- 4. Evita CROSS JOIN a menos que sepas exactamente qué haces.
-- 5. No abuses de los JOINs; a veces es mejor hacer dos queries simples desde
--    Python si el JOIN es demasiado complejo y el volumen de datos es pequeño.
-- -----------------------------------------------------------------------------
