-- =============================================================================
-- SQL PROFESIONAL: EXPLAIN ANALYZE
-- LEYENDO LA MENTE DEL OPTIMIZADOR DE POSTGRES
-- =============================================================================

/*
¿QUÉ ES UN QUERY PLAN?
-----------------------------------------------------------------------------
Antes de ejecutar una query, Postgres decide la mejor estrategia: qué índices 
usar, cómo unir tablas y qué algoritmos aplicar.

El comando EXPLAIN te muestra ese plan sin ejecutar la query.
EXPLAIN ANALYZE ejecuta la query y te da los tiempos reales.

CLAVE: El costo se mide en "unidades de I/O de página", no en milisegundos.
*/

-- -----------------------------------------------------------------------------
-- 1. USO BÁSICO
-- -----------------------------------------------------------------------------

EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- -----------------------------------------------------------------------------
-- 2. EXPLAIN ANALYZE (Tiempos reales)
-- -----------------------------------------------------------------------------

EXPLAIN ANALYZE 
SELECT u.username, COUNT(o.id) 
FROM users u 
JOIN orders o ON u.id = o.user_id 
GROUP BY u.username;

-- -----------------------------------------------------------------------------
-- 3. TÉRMINOS QUE DEBES CONOCER (The Vocabulary)
-- -----------------------------------------------------------------------------

/*
A. Sequential Scan (Seq Scan): 
   - Malo en tablas grandes. Postgres lee toda la tabla del disco.
   
B. Index Scan: 
   - Bueno. Postgres usa un índice para saltar a las filas correctas.
   
C. Index Only Scan: 
   - Excelente. Postgres responde la query leyendo SOLO el índice.
   
D. Bitmap Index Scan: 
   - Híbrido. Postgres marca las páginas que contienen datos y luego las lee masivamente.
   
E. Nested Loop vs Hash Join vs Merge Join:
   - Nested Loop: Bueno para tablas pequeñas o muy indexadas.
   - Hash Join: Bueno para grandes volúmenes de datos.
*/

-- -----------------------------------------------------------------------------
-- 4. BUFFER USAGE (¿Cuánta memoria estamos usando?)
-- -----------------------------------------------------------------------------

-- Muy útil para saber si la query está cargando datos del disco o de la caché (shared buffers)
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM products WHERE price > 500;

-- -----------------------------------------------------------------------------
-- 5. TRUCO DE OPTIMIZACIÓN EN BACKEND
-- -----------------------------------------------------------------------------

/*
Si ves un Seq Scan en una columna que tiene índice, puede ser porque:
1. La tabla es tan pequeña que Postgres decide que es más rápido leerla entera.
2. Has usado una función sobre la columna (ej: WHERE LOWER(email) = ...).
3. Las estadísticas de la DB están obsoletas.
*/

-- Forzar actualización de estadísticas
-- ANALYZE users;

-- -----------------------------------------------------------------------------
-- 6. VISUALIZADORES (The Pro Toolset)
-- -----------------------------------------------------------------------------

/*
A veces el output de texto de EXPLAIN es difícil de leer. 
Herramienta recomendada: PEV (Postgres Explain Visualizer) o explain.dalibo.com.
*/

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEARROLLADOR:
-- -----------------------------------------------------------------------------
-- 1. EXPLAIN ANALYZE es tu mejor amigo cuando una query tarda > 200ms.
-- 2. Busca "Seq Scan" en tablas grandes; es tu primer objetivo de optimización.
-- 3. "Actual time" es el tiempo real que tardó el nodo en ejecutarse.
-- 4. Fíjate en la diferencia entre "Rows" estimadas y reales. Si es muy grande,
--    Postgres está tomando decisiones basadas en datos falsos/viejos.
-- -----------------------------------------------------------------------------
