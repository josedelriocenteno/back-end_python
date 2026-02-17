-- =============================================================================
-- SQL PROFESIONAL: JSONB EN POSTGRESQL
-- UNIENDO EL MUNDO RELACIONAL Y DOCUMENTAL (NoSQL)
-- =============================================================================

/*
¿QUÉ ES JSONB?
-----------------------------------------------------------------------------
PostgreSQL ofrece dos tipos de datos JSON:
1. JSON: Almacenamiento de texto plano. Rápido de insertar, lento de consultar.
2. JSONB (Binary): Almacena el JSON descompuesto en binario. Un poco más lento 
   de insertar, pero MUCHO más rápido de consultar y permite INDEXACIÓN.

En Backend moderno, JSONB es la herramienta elegida para "Metadatos" o campos 
que cambian frecuentemente sin querer modificar el esquema.
*/

-- -----------------------------------------------------------------------------
-- 1. OPERACIONES BÁSICAS DE LECTURA
-- -----------------------------------------------------------------------------

-- -> Obtiene el objeto/valor como JSON
-- ->> Obtiene el valor como TEXTO (Más común)

SELECT 
    metadata->'settings' as settings_json,
    metadata->>'theme' as theme_name
FROM products;

-- Acceso anidado
SELECT metadata->'details'->>'color' 
FROM products;

-- -----------------------------------------------------------------------------
-- 2. FILTRADO CON OPERADORES ESPECIALES
-- -----------------------------------------------------------------------------

-- @> (Contención): ¿El JSON contiene este par clave:valor?
SELECT * FROM products 
WHERE metadata @> '{"brand": "Apple"}';

-- ? (Existencia de clave): ¿Existe la clave 'tags'?
SELECT * FROM products 
WHERE metadata ? 'on_sale';

-- -----------------------------------------------------------------------------
-- 3. MODIFICACIÓN DE DATOS (jsonb_set)
-- -----------------------------------------------------------------------------

-- Actualizar un valor anidado
UPDATE products 
SET metadata = jsonb_set(metadata, '{details, color}', '"blue"', true)
WHERE id = 1;

-- Eliminar una clave (-)
UPDATE products 
SET metadata = metadata - 'old_key'
WHERE id = 1;

-- Concatenar JSONs (||) - Muy útil para merges
UPDATE products 
SET metadata = metadata || '{"new_attr": 123}'::jsonb
WHERE id = 1;

-- -----------------------------------------------------------------------------
-- 4. AGREGACIONES Y FUNCIONES ÚTILES
-- -----------------------------------------------------------------------------

-- Convertir un JSON de array a filas (Explode)
SELECT jsonb_array_elements_text(metadata->'tags') as tag
FROM products;

-- Crear un JSON a partir de una query (Aggregates)
SELECT jsonb_build_object('id', id, 'user', username) 
FROM users;

-- -----------------------------------------------------------------------------
-- 5. INDEXACIÓN GIN (Performance)
-- -----------------------------------------------------------------------------

/*
Busca en todo el documento JSON instantáneamente.
*/
CREATE INDEX idx_products_metadata_gin ON products USING GIN (metadata);

/*
Indexar solo una clave específica (Más eficiente en espacio)
*/
CREATE INDEX idx_products_theme ON products ((metadata->>'theme'));

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEARROLLADOR:
-- -----------------------------------------------------------------------------
-- 1. Usa JSONB por defecto, evita el tipo JSON plano.
-- 2. No abuses: si todos tus objetos tienen las mismas claves, usa columnas 
--    normales (SQL puro es más rápido y ocupa menos).
-- 3. Usa JSONB para: Metadatos, logs, campos dinámicos de formularios.
-- 4. Recuerda el operador @> para filtros rápidos con índices GIN.
-- 5. En Python, puedes pasar diccionarios directamente y Psycopg los convertirá.
-- -----------------------------------------------------------------------------
