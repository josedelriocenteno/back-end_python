-- =============================================================================
-- SQL PROFESIONAL: ÍNDICES BÁSICOS
-- ACELERANDO LAS QUERIES DESDE EL DISCO
-- =============================================================================

/*
¿QUÉ ES UN ÍNDICE?
-----------------------------------------------------------------------------
Un índice es una estructura de datos (generalmente un B-Tree) que permite a la
base de datos encontrar filas rápidamente sin tener que escanear toda la tabla
(Sequential Scan).

Pensar en un índice es como el índice de un libro técnico: no lees todo el 
libro para encontrar "Capítulo 5", vas al índice y saltas a la página correcta.

PRECIO A PAGAR:
- Espacio en disco extra.
- Escrituras más lentas (INSERT/UPDATE/DELETE deben actualizar el índice).
*/

-- -----------------------------------------------------------------------------
-- 1. B-TREE: EL ÍNDICE POR DEFECTO
-- -----------------------------------------------------------------------------

/*
Es el tipo de índice más versátil. Soporta consultas de igualdad (=) y 
de rango (<, >, <=, >=, BETWEEN).
*/

CREATE INDEX idx_users_email ON users(email);

-- -----------------------------------------------------------------------------
-- 2. HASH INDEX
-- -----------------------------------------------------------------------------

/*
Solo soporta comparaciones de igualdad (=). Es ligeramente más rápido que 
B-Tree para igualdades puras, pero no soporta rangos ni ordenación.
En Postgres moderno, se usa poco frente a B-Tree.
*/

CREATE INDEX idx_products_sku_hash ON products USING HASH (sku);

-- -----------------------------------------------------------------------------
-- 3. UNIQUE INDEX
-- -----------------------------------------------------------------------------

/*
Garantiza que no haya valores duplicados y, de paso, acelera las búsquedas.
Nota: Una PRIMARY KEY crea automáticamente un UNIQUE INDEX.
*/

CREATE UNIQUE INDEX idx_users_username ON users(username);

-- -----------------------------------------------------------------------------
-- 4. ÍNDICES PARCIALES (Optimization Trick)
-- -----------------------------------------------------------------------------

/*
Solo indexas una parte de la tabla. Muy útil para mejorar el rendimiento sin 
gastar tanto espacio en disco.
*/

-- Ejemplo: Indexar solo los productos activos para que sean rápidos de encontrar
CREATE INDEX idx_active_products_price 
ON products(price) 
WHERE status = 'active';

-- -----------------------------------------------------------------------------
-- 5. ÍNDICES SOBRE EXPRESIONES (Functional Indexes)
-- -----------------------------------------------------------------------------

/*
Indexas el resultado de una función. Vital si tu código Python suele 
filtrar por transformaciones.
*/

-- Ejemplo: Búsquedas insensibles a mayúsculas/minúsculas eficientes
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- -----------------------------------------------------------------------------
-- 6. GESTIÓN Y MANTENIMIENTO
-- -----------------------------------------------------------------------------

-- Ver todos los índices de una tabla (Comando psql)
-- \d table_name

-- Eliminar un índice
-- DROP INDEX idx_users_email;

-- REINDEX: Útil si el índice se ha corrompido o ha crecido demasiado (bloat)
-- REINDEX TABLE users;

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEARROLLADOR:
-- -----------------------------------------------------------------------------
-- 1. Indexa las columnas que aparecen frecuentemente en el WHERE y en los JOINs.
-- 2. No indexas TODO. Demasiados índices matan el rendimiento de inserción.
-- 3. Usa índices parciales para tablas gigantes con estados (ej: orders_open).
-- 4. Recuerda que Postgres ignora el índice si la columna está dentro de una 
--    función, a menos que uses un índice de expresión.
-- 5. Monitoriza el tamaño: un índice puede llegar a ser más grande que la tabla.
-- -----------------------------------------------------------------------------
