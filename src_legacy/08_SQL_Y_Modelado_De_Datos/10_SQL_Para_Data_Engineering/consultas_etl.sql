-- =============================================================================
-- SQL PROFESIONAL: CONSULTAS ETL (Extract, Transform, Load)
-- TRANSFORMANDO DATOS EN LA "COCINA" DE LA BASE DE DATOS
-- =============================================================================

/*
¿QUÉ ES ETL EN SQL?
-----------------------------------------------------------------------------
Aunque existen herramientas como Spark o Pandas, muchas transformaciones de 
datos son más eficientes si se ejecutan directamente en SQL (ELT - Extract, 
Load, Transform). 

Aprovechas la potencia de cómputo del servidor de la base de datos y evitas 
mover gigabytes de datos por la red hacia tu script de Python.
*/

-- -----------------------------------------------------------------------------
-- 1. LIMPIEZA Y NORMALIZACIÓN DE STRINGS
-- -----------------------------------------------------------------------------

SELECT 
    UPPER(TRIM(username)) as clean_username,
    COALESCE(email, 'N/A') as email_fixed, -- Manejo de nulos
    REGEXP_REPLACE(phone, '[^0-9]', '', 'g') as numeric_phone -- Limpieza regex
FROM raw_users;

-- -----------------------------------------------------------------------------
-- 2. CASTING Y TRANSFORMACIÓN DE TIPOS
-- -----------------------------------------------------------------------------

SELECT 
    event_id,
    payload->>'value'::NUMERIC as value_numeric,
    (payload->>'timestamp')::TIMESTAMPTZ as event_ts,
    CASE 
        WHEN status = 1 THEN 'Active'
        WHEN status = 0 THEN 'Inactive'
        ELSE 'Unknown'
    END as status_label
FROM logs_staging;

-- -----------------------------------------------------------------------------
-- 3. AGREGACIONES PARA DATA MARTS
-- -----------------------------------------------------------------------------

-- Creación de una tabla agregada para analítica
INSERT INTO daily_sales_summary (day, total_sales, unique_customers)
SELECT 
    DATE_TRUNC('day', created_at) as day,
    SUM(total_amount),
    COUNT(DISTINCT user_id)
FROM orders
WHERE created_at >= '2023-01-01'
GROUP BY 1;

-- -----------------------------------------------------------------------------
-- 4. DEDUPLICACIÓN DE DATOS (The Pro Way)
-- -----------------------------------------------------------------------------

/*
A veces recibes datos duplicados de un origen externo.
Este patrón usa una CTE y ROW_NUMBER para quedarse solo con el registro más reciente.
*/

WITH ranked_rows AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY external_id 
            ORDER BY imported_at DESC
        ) as rn
    FROM staging_table
)
DELETE FROM staging_table
WHERE id IN (SELECT id FROM ranked_rows WHERE rn > 1);

-- -----------------------------------------------------------------------------
-- 5. UPSERT MASIVO (Conflict Management)
-- -----------------------------------------------------------------------------

/*
Cargar datos de una tabla temporal a la final actualizando si ya existen.
*/
INSERT INTO production_users (id, email, last_login)
SELECT id, email, last_login FROM staging_users
ON CONFLICT (id) 
DO UPDATE SET 
    last_login = EXCLUDED.last_login,
    email = EXCLUDED.email;

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DATA ENGINEER:
-- -----------------------------------------------------------------------------
-- 1. Filtra pronto: Usa el WHERE para reducir el dataset lo antes posible.
-- 2. Aprovecha los tipos nativos (jsonb_to_record, etc.) para aplanar datos.
-- 3. Usa CTEs para que tus pipelines de ETL sean legibles y testeables.
-- 4. Recuerda que las transformaciones en SQL son, por lo general, más rápidas 
--    que procesar fila a fila en un bucle 'for' de Python.
-- -----------------------------------------------------------------------------
