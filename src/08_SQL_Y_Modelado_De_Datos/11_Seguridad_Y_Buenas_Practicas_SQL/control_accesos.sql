-- =============================================================================
-- SQL PROFESIONAL: CONTROL DE ACCESOS (Roles y Permisos)
-- EL PRINCIPIO DE MENOR PRIVILEGIO (PoLP)
-- =============================================================================

/*
SEGURIDAD EN LA BASE DE DATOS
-----------------------------------------------------------------------------
Como desarrollador Backend, la seguridad no termina en tu API. 
Si el usuario de tu base de datos tiene permisos de "Superusuario", un solo 
bug de SQL Injection podría permitir que alguien borre toda la instancia.

Regla de Oro: Tu aplicación debe usar un usuario con los permisos MÍNIMOS 
necesarios para funcionar.
*/

-- -----------------------------------------------------------------------------
-- 1. CREACIÓN DE ROLES (Proceso del Administrador)
-- -----------------------------------------------------------------------------

-- Crear un rol que no puede loguearse (Plantilla/Grupo)
CREATE ROLE read_only_users;

-- Crear el usuario real que usará nuestra App
CREATE USER app_user WITH PASSWORD 'shhh_secret_pwd';

-- -----------------------------------------------------------------------------
-- 2. GESTIÓN DE PERMISOS (GRANT)
-- -----------------------------------------------------------------------------

-- 1. Dar acceso al esquema
GRANT USAGE ON SCHEMA public TO read_only_users;

-- 2. Dar acceso de lectura a todas las tablas del esquema
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only_users;

-- 3. Hacer que el usuario de la App herede de ese grupo
GRANT read_only_users TO app_user;

-- -----------------------------------------------------------------------------
-- 3. PERMISOS GRANULARES (The Backend Way)
-- -----------------------------------------------------------------------------

/*
Tu App solo necesita INSERT, UPDATE y SELECT en ciertas tablas.
No necesita permisos de DDL (DROP, ALTER) en producción.
*/

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE orders, users TO app_user;

-- ¡IMPORTANTE! Para columnas SERIAL/IDENTITY, necesitas dar permiso sobre la secuencia
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- -----------------------------------------------------------------------------
-- 4. PERMISOS A NIVEL DE COLUMNA
-- -----------------------------------------------------------------------------

-- Puedes restringir que el usuario de analítica no vea la columna 'password_hash'
-- GRANT SELECT (id, email, username) ON TABLE users TO analytics_user;

-- -----------------------------------------------------------------------------
-- 5. RLS (Row Level Security) - SEGURIDAD NIVEL FILA
-- -----------------------------------------------------------------------------

/*
Súper potente: La DB misma filtra los datos basándose en quién hace la query.
Útil para aplicaciones Multitenant.
*/

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Solo puedes ver las órdenes si tu user_id coincide con el de la orden
-- (Requiere setear una variable de sesión en la conexión desde Python)
CREATE POLICY user_orders_policy ON orders
    FOR SELECT 
    USING (user_id = current_setting('app.current_user_id')::uuid);

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEARROLLADOR:
-- -----------------------------------------------------------------------------
-- 1. Jamás uses el usuario 'postgres' en tu código Python.
-- 2. Crea un usuario específico para tu App con permisos limitados.
-- 3. Usa Roles para organizar permisos si tienes varios microservicios.
-- 4. No olvides dar permisos sobre las SEQUENCES si usas IDs incrementales.
-- 5. Considera RLS para capas extra de seguridad en apps sensibles.
-- -----------------------------------------------------------------------------
