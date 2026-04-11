-- =============================================================================
-- SQL PROFESIONAL: DML - INSERT & SELECT
-- EL ARTE DE ESCRIBIR Y RECUPERAR DATOS CON EFICIENCIA
-- =============================================================================

/*
INTRODUCCIÓN AL DML (Data Manipulation Language)
-----------------------------------------------------------------------------
Si el DDL es el plano de la casa, el DML es la vida dentro de ella.
Como desarrollador Backend, el 90% de tu interacción con SQL será DML.

Claves de un DML profesional:
1. Precisión: Insertar lo que toca, leer solo lo que necesitas.
2. Rendimiento: Evitar el temido "SELECT *".
3. Seguridad: Preparar el camino para evitar SQL Injection (visto en Tema 08.08).
*/

-- -----------------------------------------------------------------------------
-- 1. INSERT: MÁS ALLÁ DE LO BÁSICO
-- -----------------------------------------------------------------------------

-- Inserción estándar de una fila
INSERT INTO users (username, email, is_active)
VALUES ('jdoe', 'john@example.com', true);

-- Inserción múltiple (Bulk Insert) - Mucho más eficiente que múltiples INSERTS
INSERT INTO products (name, price, status)
VALUES 
    ('Laptop Pro', 1200.00, 'active'),
    ('Mouse Wireless', 25.50, 'active'),
    ('Monitor 4K', 450.00, 'draft');

-- RETURNING: La joya de la corona para Backend
-- Evita tener que hacer un SELECT después de un INSERT para saber el ID generado.
INSERT INTO users (username, email)
VALUES ('python_dev', 'dev@python.org')
RETURNING id, created_at;

-- -----------------------------------------------------------------------------
-- 2. "UPSERT" (Insert or Update): Manejo de Conflictos
-- -----------------------------------------------------------------------------

/*
Muy común en procesos de sincronización o APIs de integración.
Si el usuario existe (basado en una UNIQUE constraint), actualízalo en lugar de fallar.
*/

INSERT INTO users (username, email)
VALUES ('python_dev', 'new_email@python.org')
ON CONFLICT (username) 
DO UPDATE SET 
    email = EXCLUDED.email,
    updated_at = CURRENT_TIMESTAMP;

-- -----------------------------------------------------------------------------
-- 3. SELECT: RECUPERACIÓN DE DATOS PROFESIONAL
-- -----------------------------------------------------------------------------

-- REGLA DE ORO: Jamás uses SELECT * en producción.
-- 1. Sobrecargas la red. 
-- 2. Gastas memoria en tu app Python.
-- 3. Tu consulta es más lenta (Postgres lee más del disco).

SELECT id, username, email 
FROM users 
WHERE is_active = true 
ORDER BY created_at DESC;

-- ALIAS y Lógica Simple
SELECT 
    name, 
    price AS original_price,
    (price * 1.21) AS price_with_vat, -- Lógica simple en DB
    COALESCE(description, 'Sin descripción disponible') AS info -- Manejo de NULLs
FROM products;

-- -----------------------------------------------------------------------------
-- 4. FILTRADO AVANZADO (WHERE)
-- -----------------------------------------------------------------------------

SELECT * FROM products
WHERE 
    price BETWEEN 100 AND 1000
    AND status IN ('active', 'published')
    AND name ILIKE '%laptop%'; -- ILIKE es Case-Insensitive (Postgres)

-- Diferencia importante:
-- LIKE 'A%' -> Empieza por A (Case Sensitive)
-- ILIKE 'a%' -> Empieza por A o a (Case Insensitive)

-- -----------------------------------------------------------------------------
-- 5. LÍMITES Y PAGINACIÓN (Crucial para APIs)
-- -----------------------------------------------------------------------------

/*
Paginación básica (Offset-based pagination):
- LIMIT: Cuántos traer.
- OFFSET: Cuántos saltar.
OJO: OFFSET se vuelve lento en tablas gigantes (>100k filas).
*/

SELECT id, name 
FROM products 
ORDER BY id 
LIMIT 10 OFFSET 20; -- Tercera página de 10 elementos

-- -----------------------------------------------------------------------------
-- 6. INTERACCIÓN CON EL CÓDIGO (Python Snippet)
-- -----------------------------------------------------------------------------

/*
En Python (usando psycopg3):

# SELECT
rows = cur.execute("SELECT id, name FROM products WHERE price > %s", [100]).fetchall()
for id, name in rows:
    print(f"Producto: {name}")

# BULK INSERT desde lista de diccionarios
data = [('A', 10), ('B', 20)]
cur.executemany("INSERT INTO t(n, v) VALUES (%s, %s)", data)
*/

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEARROLLADOR:
-- -----------------------------------------------------------------------------
-- 1. Usa RETURNING para capturar IDs generados instantáneamente.
-- 2. ON CONFLICT es tu mejor amigo para evitar errores de duplicidad.
-- 3. SELECT explícito siempre. Especifica las columnas.
-- 4. ILIKE para búsquedas de texto amigables con el usuario.
-- 5. Maneja la paginación desde el día 1 en tus endpoints.
-- -----------------------------------------------------------------------------
