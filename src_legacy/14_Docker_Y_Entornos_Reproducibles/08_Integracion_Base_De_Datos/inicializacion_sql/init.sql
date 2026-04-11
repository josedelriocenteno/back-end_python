-- ARCHIVO DE INICIALIZACIÓN AUTOMÁTICA
-- -----------------------------------------------------------------------------
-- Este script se ejecutará solo la primera vez que se cree el volumen de la DB.

-- 1. Crear esquemas adicionales si es necesario
CREATE SCHEMA IF NOT EXISTS data_warehouse;

-- 2. Crear tablas iniciales
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Insertar datos semilla (Seed Data) para desarrollo
INSERT INTO users (username, email) VALUES 
('admin', 'admin@miempresa.com'),
('developer', 'dev@miempresa.com')
ON CONFLICT DO NOTHING;

-- 4. Ajustes de permisos prioritarios
-- GRANT ALL PRIVILEGES ON DATABASE mi_db TO mi_usuario;
