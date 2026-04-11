-- =============================================================================
-- SQL PROFESIONAL: DML - UPDATE & DELETE
-- MODIFICAR Y ELIMINAR CON RED DE SEGURIDAD
-- =============================================================================

/*
EL GRAN RIESGO DEL DML MODIFICADOR
-----------------------------------------------------------------------------
Un UPDATE o DELETE sin WHERE en producción es el fin de una carrera (y de una DB).
Como desarrollador Backend, tu código debe ser robusto para nunca ejecutar 
estas acciones sobre el conjunto de datos completo por accidente.

Reglas de oro:
1. Jamás escribas un UPDATE/DELETE sin escribir primero el WHERE.
2. Usa transacciones (visto en el siguiente archivo).
3. Usa la cláusula RETURNING para verificar qué has cambiado.
*/

-- -----------------------------------------------------------------------------
-- 1. UPDATE: MODIFICANDO DATOS CON PRECISIÓN
-- -----------------------------------------------------------------------------

-- Update básico
UPDATE users 
SET is_active = false, 
    updated_at = CURRENT_TIMESTAMP
WHERE id = '550e8400-e29b-41d4-a716-446655440000';

-- Update con aritmética (ej: subida de precios)
UPDATE products 
SET price = price * 1.10 
WHERE status = 'active' AND price < 100;

-- RETURNING en UPDATE (Crucial para Backend)
-- Obtener los nuevos valores tras la actualización sin hacer un SELECT extra.
UPDATE users
SET username = 'pro_coder'
WHERE id = '550e8400-e29b-41d4-a716-446655440000'
RETURNING username, updated_at;

-- -----------------------------------------------------------------------------
-- 2. UPDATE BASADO EN OTRA TABLA (UPDATE JOIN)
-- -----------------------------------------------------------------------------

/*
Quieres actualizar el estado de los productos basándote en su categoría.
*/
UPDATE products p
SET status = 'archived'
FROM categories c
WHERE p.category_id = c.id
  AND c.name = 'Legacy Products';

-- -----------------------------------------------------------------------------
-- 3. DELETE: ELIMINACIÓN DE DATOS
-- -----------------------------------------------------------------------------

-- Delete básico
DELETE FROM system_events 
WHERE created_at < NOW() - INTERVAL '30 days';

-- RETURNING en DELETE
-- Muy útil para saber qué registros hemos borrado para logs de aplicación.
DELETE FROM users 
WHERE is_verified = false AND created_at < NOW() - INTERVAL '1 year'
RETURNING id, email;

-- -----------------------------------------------------------------------------
-- 4. ESTRATEGIAS DE SEGURIDAD EN PRODUCCIÓN
-- -----------------------------------------------------------------------------

/*
A. El modo "Precavido":
Antes de ejecutar un DELETE, ejecuta el mismo filtro con un SELECT.
Si el SELECT devuelve 5 filas y esperas borrar 5, el filtro es correcto.
*/
-- 1. Verificar: SELECT count(*) FROM users WHERE condition...
-- 2. Ejecutar: DELETE FROM users WHERE condition...

/*
B. Limitando el daño:
Aunque Postgres no permite LIMIT directamente en DELETE (como MySQL), puedes usar 
una subquery si quieres borrar en "lotes" pequeños para no bloquear la DB.
*/
DELETE FROM logs 
WHERE id IN (
    SELECT id FROM logs 
    WHERE level = 'debug' 
    LIMIT 1000
);

-- -----------------------------------------------------------------------------
-- 5. SOFT DELETE (LA MEJOR PRÁCTICA)
-- -----------------------------------------------------------------------------

/*
En lugar de DELETE, usamos una columna de estado. 
Ventajas: Podemos recuperar datos y mantenemos integridad referencial.
*/

-- Primero, añadimos la columna (DDL)
-- ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;

-- "Borrado" lógico (UPDATE)
UPDATE users 
SET deleted_at = NOW() 
WHERE id = '...';

-- Consulta filtrando borrados
SELECT * FROM users WHERE deleted_at IS NULL;

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEVELOPER:
-- -----------------------------------------------------------------------------
-- 1. WHERE es obligatorio por ética profesional.
-- 2. RETURNING ahorra latencia de red y código Python.
-- 3. Prefiere Soft Delete sobre Hard Delete en datos críticos de usuario.
-- 4. Para borrar millones de filas, usa TRUNCATE (DDL) o borra en lotes (DML).
-- -----------------------------------------------------------------------------
