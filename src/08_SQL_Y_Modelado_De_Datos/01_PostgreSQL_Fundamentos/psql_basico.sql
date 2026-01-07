/*
psql_basico.sql
================
Consola profesional PostgreSQL usando SOLO SQL.

Este archivo sirve para:
- Ver dónde estás conectado
- Inspeccionar la base de datos
- Explorar tablas, columnas, índices y constraints
- Trabajar de forma segura y profesional

TODO el contenido es SQL válido.
Las explicaciones están SOLO en comentarios.
*/

/* =========================================================
   1. CONTEXTO DE CONEXIÓN
   Nunca trabajes sin saber:
   - qué base de datos usas
   - con qué usuario
   - qué versión de PostgreSQL
   ========================================================= */

-- Base de datos actual
SELECT current_database() AS database_name;

-- Usuario actual
SELECT current_user AS user_name;

-- Versión del servidor PostgreSQL
SELECT version();


/* =========================================================
   2. ESQUEMAS DISPONIBLES
   Equivalente profesional a "\dn"
   ========================================================= */

SELECT schema_name
FROM information_schema.schemata
ORDER BY schema_name;


/* =========================================================
   3. TABLAS EXISTENTES
   Ver todas las tablas visibles
   ========================================================= */

SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
ORDER BY table_schema, table_name;


/* =========================================================
   4. TABLAS DEL ESQUEMA PUBLIC
   Lo más común en proyectos pequeños/medios
   ========================================================= */

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;


/* =========================================================
   5. ESTRUCTURA DE UNA TABLA
   Sustituto SQL real de "\d tabla"
   ========================================================= */

-- Cambia 'usuarios' por la tabla que quieras inspeccionar
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'usuarios'
ORDER BY ordinal_position;


/* =========================================================
   6. CONSTRAINTS
   PK, FK, UNIQUE, CHECK
   Las reglas que NO puedes ignorar
   ========================================================= */

SELECT
    tc.constraint_type,
    tc.constraint_name,
    kcu.column_name
FROM information_schema.table_constraints tc
LEFT JOIN information_schema.key_column_usage kcu
       ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_schema = 'public'
  AND tc.table_name = 'usuarios';


/* =========================================================
   7. ÍNDICES
   Clave para rendimiento
   ========================================================= */

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'usuarios';


/* =========================================================
   8. CONSULTAS SEGURAS
   Nunca empieces con SELECT *
   ========================================================= */

SELECT id, nombre, email
FROM usuarios
ORDER BY id
LIMIT 10;


/* =========================================================
   9. FILTRADO REAL
   ILIKE = case-insensitive (PostgreSQL)
   ========================================================= */

SELECT id, nombre, email
FROM usuarios
WHERE email ILIKE '%gmail.com';


/* =========================================================
   10. SANITY CHECKS
   Cuenta antes de tocar datos
   ========================================================= */

SELECT COUNT(*) AS total_usuarios
FROM usuarios;


/* =========================================================
   11. TRANSACCIONES
   Control total de cambios
   ========================================================= */

BEGIN;

INSERT INTO usuarios (nombre, email)
VALUES ('Usuario Prueba', 'test@demo.com');

-- Verifica antes de confirmar
SELECT *
FROM usuarios
WHERE email = 'test@demo.com';

-- Deshacer cambios (modo seguro)
ROLLBACK;

-- Si todo es correcto, usar:
-- COMMIT;


/* =========================================================
   12. DETECCIÓN DE PROBLEMAS
   Ejemplo: duplicados
   ========================================================= */

SELECT email, COUNT(*)
FROM usuarios
GROUP BY email
HAVING COUNT(*) > 1;


/* =========================================================
   13. TAMAÑO DE TABLAS
   Importante en producción
   ========================================================= */

SELECT
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;


/* =========================================================
   14. RECORDATORIOS PROFESIONALES
   ========================================================= */

-- ❌ No trabajar sin BEGIN en cambios críticos
-- ❌ No asumir esquemas
-- ❌ No ignorar constraints
-- ✅ Usar LIMIT
-- ✅ Inspeccionar metadatos
-- ✅ Pensar en rendimiento desde el inicio
