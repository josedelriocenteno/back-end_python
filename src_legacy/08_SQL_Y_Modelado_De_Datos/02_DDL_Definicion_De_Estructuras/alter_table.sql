-- =============================================================================
-- SQL PROFESIONAL: DDL - ALTER TABLE
-- MODIFICACIONES SEGURAS EN ENTORNOS DE PRODUCCIÓN
-- =============================================================================

/*
EL PELIGRO DEL ALTER TABLE
-----------------------------------------------------------------------------
Modificar una tabla en desarrollo es fácil. En producción, con millones de
filas, un ALTER TABLE mal ejecutado puede:
1. Bloquear la tabla para lecturas/escrituras (Locking).
2. Causar un "Downtime" no planificado.
3. Corromper la lógica si no se maneja la retrocompatibilidad.
*/

-- -----------------------------------------------------------------------------
-- 1. OPERACIONES BÁSICAS (Añadir/Eliminar/Renombrar)
-- -----------------------------------------------------------------------------

-- Añadir una columna (Cuidado si tiene DEFAULT y la tabla es grande)
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);

-- Renombrar una columna
ALTER TABLE users RENAME COLUMN username TO handle;

-- Eliminar una columna (Proceso destructivo, ¡ojo!)
-- ALTER TABLE users DROP COLUMN oauth_token;

-- Renombrar una tabla
-- ALTER TABLE products RENAME TO catalog_items;

-- -----------------------------------------------------------------------------
-- 2. MODIFICAR TIPOS DE DATOS
-- -----------------------------------------------------------------------------

-- Cambiar de VARCHAR(50) a VARCHAR(100)
ALTER TABLE users ALTER COLUMN handle TYPE VARCHAR(100);

-- Cambiar tipo con conversión explícita (Uso de USING)
-- Ejemplo: convertir un string que contiene números a un entero real.
ALTER TABLE orders 
    ALTER COLUMN status_code TYPE INT 
    USING status_code::integer;

-- -----------------------------------------------------------------------------
-- 3. GESTIÓN DE VALORES POR DEFECTO Y NULLABILITY
-- -----------------------------------------------------------------------------

-- Poner un nuevo DEFAULT
ALTER TABLE products ALTER COLUMN status SET DEFAULT 'draft';

-- Quitar un DEFAULT
ALTER TABLE products ALTER COLUMN status DROP DEFAULT;

-- Hacer una columna NOT NULL
-- (Solo funciona si no existen NULLs previos en la tabla)
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- -----------------------------------------------------------------------------
-- 4. ALTER TABLE "THE PRO WAY" (Zero Downtime Patterns)
-- -----------------------------------------------------------------------------

/*
A. Añadir columnas con DEFAULT:
En versiones antiguas de Postgres, añadir una columna con un DEFAULT 
reescribía toda la tabla (bloqueo total). Desde Postgres 11, esto es instantáneo
si el valor por defecto es constante.
*/

-- B. Añadir una Constraint sin bloquear (NOT VALID):
-- 1. Añadimos la constraint. Los nuevos registros deben cumplirla. 
--    Postgres NO valida los registros antiguos todavía, por lo que es rápido.
ALTER TABLE users 
    ADD CONSTRAINT ck_valid_role 
    CHECK (role IN ('admin', 'user', 'guest')) 
    NOT VALID;

-- 2. Validamos los datos antiguos en un proceso separado que no bloquea escrituras.
ALTER TABLE users VALIDATE CONSTRAINT ck_valid_role;

-- -----------------------------------------------------------------------------
-- 5. TRUCOS DE INTEGRIDAD REFERENCIAL
-- -----------------------------------------------------------------------------

-- Cambiar cómo se comporta una Foreign Key (Eliminar y Volver a Crear)
ALTER TABLE orders DROP CONSTRAINT fk_user;

ALTER TABLE orders 
    ADD CONSTRAINT fk_user_new 
    FOREIGN KEY (user_id) 
    REFERENCES users(id) 
    ON DELETE SET DEFAULT;

-- -----------------------------------------------------------------------------
-- 6. RELACIÓN CON HERRAMIENTAS DE MIGRACIÓN (Alembic/Django)
-- -----------------------------------------------------------------------------

/*
Aunque escribas este SQL a mano ahora, en el mundo real usarás migraciones:
- Alembic (SQLAlchemy)
- Django Migrations

Entender el SQL subyacente de un ALTER TABLE te permite revisar los archivos
de migración autogenerados y evitar bloqueos de base de datos desastrosos.
*/

-- -----------------------------------------------------------------------------
-- RESUMEN DE SEGURIDAD:
-- -----------------------------------------------------------------------------
-- 1. Siempre haz backup antes de un ALTER TABLE masivo.
-- 2. Si la tabla tiene >1M de filas, prueba el tiempo de ejecución en Staging.
-- 3. Usa transacciones si vas a encadenar varios ALTER TABLE.
-- -----------------------------------------------------------------------------
