-- =============================================================================
-- SQL PROFESIONAL: TRANSACCIONES (TCL)
-- GARANTIZANDO LA INTEGRIDAD CON ACID
-- =============================================================================

/*
¿QUÉ ES UNA TRANSACCIÓN?
-----------------------------------------------------------------------------
Una transacción es una unidad de trabajo lógica que debe cumplirse "todo o nada".
Si tu API de pagos descuenta dinero pero falla al crear el recibo, la DB debe
ser capaz de volver atrás.

ACID:
- Atomicidad: Todo el bloque se ejecuta o nada.
- Consistencia: La DB pasa de un estado válido a otro válido.
- Aislamiento: Las transacciones no se pisan entre ellas.
- Durabilidad: Una vez confirmado (COMMIT), los datos no se pierden.
*/

-- -----------------------------------------------------------------------------
-- 1. FLUJO BÁSICO: BEGIN, COMMIT, ROLLBACK
-- -----------------------------------------------------------------------------

BEGIN; -- Inicia la transacción

    -- Paso 1: Restar saldo
    UPDATE accounts SET balance = balance - 100 WHERE user_id = 1;
    
    -- Paso 2: Sumar saldo al destino
    UPDATE accounts SET balance = balance + 100 WHERE user_id = 2;
    
    -- Paso 3: Registrar movimiento
    INSERT INTO trxs (from_id, to_id, amount) VALUES (1, 2, 100);

COMMIT; -- Confirma y guarda permanentemente los cambios

-- Si algo fallara en el medio, usamos:
-- ROLLBACK; -- Deshace todo lo hecho desde el BEGIN

-- -----------------------------------------------------------------------------
-- 2. SAVEPOINTS (Transacciones Anidadas Parciales)
-- -----------------------------------------------------------------------------

BEGIN;
    INSERT INTO users (username) VALUES ('master_user');
    
    SAVEPOINT sp1; -- Crea un "punto de retorno"
    
    INSERT INTO user_roles (user_id, role) VALUES (last_id, 'admin');
    -- Oh no, este rol no existe...
    
    ROLLBACK TO SAVEPOINT sp1; -- Solo deshace la inserción del rol
    
    -- Podemos seguir con otra cosa
    INSERT INTO user_roles (user_id, role) VALUES (last_id, 'standard');
    
COMMIT;

-- -----------------------------------------------------------------------------
-- 3. NIVELES DE AISLAMIENTO (ISOLATION LEVELS)
-- -----------------------------------------------------------------------------

/*
PostgreSQL usa por defecto "Read Committed".
Dependiendo de la criticidad, puedes cambiarlo:
*/

-- Previene que otros lean datos que aún no han hecho COMMIT.
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE; 
-- El nivel más alto. Garantiza que el resultado sea el mismo que si las 
-- transacciones se ejecutaran una tras otra. Evita "Phantom Reads".

-- -----------------------------------------------------------------------------
-- 4. TRANSACCIONES EN EL MUNDO REAL (BACKEND)
-- -----------------------------------------------------------------------------

/*
En Python (Psycopg3/SQLAlchemy), las transacciones suelen manejarse así:

# Psycopg3 Context Manager (Auto-commit/rollback)
with conn.transaction():
    cur.execute("UPDATE account SET balance = balance - 100 WHERE id = 1")
    cur.execute("UPDATE account SET balance = balance + 100 WHERE id = 2")
    # Si hay una excepción aquí, se hace ROLLBACK automático.
    # Si el bloque termina bien, se hace COMMIT.
*/

-- -----------------------------------------------------------------------------
-- 5. TRANSACCIONES DDL (PostgreSQL Power Feature)
-- -----------------------------------------------------------------------------

-- A diferencia de MySQL o Oracle, en Postgres puedes meter cambios de esquema
-- (DDL) dentro de transacciones. ¡ESTO ES ORO!

BEGIN;
    ALTER TABLE users ADD COLUMN phone_v2 TEXT;
    UPDATE users SET phone_v2 = phone; -- Migración de datos
    -- Si el UPDATE falla o es lento, podemos cancelar y la columna NO se crea.
COMMIT;

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEVELOPER:
-- -----------------------------------------------------------------------------
-- 1. Usa transacciones para cualquier operación que involucre más de una tabla.
-- 2. Mantén las transacciones CORTAS. No pongas llamadas a APIs externas o 
--    procesos pesados de Python dentro de un BEGIN/COMMIT de SQL (bloqueas filas).
-- 3. Entiende el Isolation Level de tu DB para evitar errores de concurrencia.
-- 4. Aprovecha las transacciones DDL para migraciones seguras.
-- -----------------------------------------------------------------------------
