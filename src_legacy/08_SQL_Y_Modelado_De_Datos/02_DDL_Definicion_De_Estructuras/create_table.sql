-- =============================================================================
-- SQL PROFESIONAL: DDL - CREATE TABLE
-- CONCEPTOS AVANZADOS Y MEJORES PRÁCTICAS PARA BACKEND PYTHON
-- =============================================================================

/*
INTRODUCCIÓN AL DDL PROFESIONAL
-----------------------------------------------------------------------------
Data Definition Language (DDL) es la parte de SQL que se encarga de definir
la estructura de la base de datos. No se trata solo de "crear tablas", sino 
de diseñar el "Contrato de Datos" que tu aplicación Backend va a respetar.

Un buen diseño DDL evita:
1. Inconsistencias de datos (Data Integrity).
2. Deuda técnica en el código Python (evitas validaciones complejas en la App).
3. Problemas de rendimiento antes de que ocurran.
*/

-- -----------------------------------------------------------------------------
-- 1. ESTRUCTURA BÁSICA VS ESTRUCTURA PROFESIONAL
-- -----------------------------------------------------------------------------

-- Lo que hace un junior:
-- CREATE TABLE usuarios (id INT, nombre TEXT);

-- Lo que hace un Senior Backend Engineer (PostgreSQL):
CREATE TABLE IF NOT EXISTS users (
    -- PK con UUID (Recomendado para sistemas distribuidos y seguridad)
    -- Requiere: CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Identificadores legibles (opcional pero útil)
    username VARCHAR(50) UNIQUE NOT NULL,
    
    -- Email con validación de formato básica (Check Constraint)
    email VARCHAR(255) UNIQUE NOT NULL 
        CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    
    -- Flags con valores por defecto
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    
    -- Timestamps automáticos (Vital para Auditoría y Data Engineering)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE users IS 'Tabla maestra de usuarios con auditoría básica y validación de email.';

-- -----------------------------------------------------------------------------
-- 2. TIPOS DE DATOS CRÍTICOS EN BACKEND
-- -----------------------------------------------------------------------------

/*
En Python manejamos diccionarios, objetos y listas. 
En SQL debemos elegir el tipo que mejor represente y proteja esos datos.
*/

CREATE TABLE products (
    id SERIAL PRIMARY KEY, -- Serial autoincremental (Clásico pero menos flexible que UUID)
    
    -- TEXT vs VARCHAR: 
    -- En PostgreSQL no hay diferencia de rendimiento real. 
    -- Usa VARCHAR(n) si quieres limitar la entrada, TEXT si es contenido libre.
    name TEXT NOT NULL,
    description TEXT,
    
    -- NUMERIC vs DOUBLE PRECISION:
    -- CRÍTICO: Para dinero SIEMPRE usa NUMERIC o DECIMAL.
    -- Evita FLOAT/REAL/DOUBLE PRECISION para finanzas por errores de redondeo.
    price NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    
    -- JSONB: La potencia de NoSQL dentro de SQL.
    -- B = Binary. Mucho más eficiente que JSON plano para indexación.
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Enums modernos (PostgreSQL permite crear tipos custom)
    -- CREATE TYPE product_status AS ENUM ('draft', 'published', 'archived');
    -- status product_status DEFAULT 'draft'
    status TEXT CHECK (status IN ('draft', 'active', 'inactive')) DEFAULT 'draft'
);

-- -----------------------------------------------------------------------------
-- 3. RELACIONES (Foreign Keys)
-- -----------------------------------------------------------------------------

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    
    -- On Delete Cascade vs Set Null vs Restrict
    -- CASCADE: Si borras el usuario, se borran sus órdenes (Peligroso).
    -- RESTRICT: No permite borrar el usuario si tiene órdenes (Seguro).
    -- SET NULL: Si borras el usuario, la orden queda "huérfana" pero existe.
    CONSTRAINT fk_user 
        FOREIGN KEY (user_id) 
        REFERENCES users(id) 
        ON DELETE RESTRICT,
        
    order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(15, 2) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 4. TABLAS DE UNIÓN (Many-to-Many)
-- -----------------------------------------------------------------------------

CREATE TABLE order_items (
    order_id UUID NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL,
    
    -- PK compuesta
    PRIMARY KEY (order_id, product_id),
    
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 5. MEJORES PRÁCTICAS "PRODUCTION READY"
-- -----------------------------------------------------------------------------

/*
A. Convención de Nombres:
   - Tablas en plural (users, products) o singular (user, product). 
     Lo importante es la CONSISTENCIA.
   - Columnas en snake_case (created_at).

B. Timezones:
   - SIEMPRE usa 'TIMESTAMP WITH TIME ZONE' (timestamptz). 
     Guardar fechas sin zona horaria es el error #1 en Backend.

C. Constraints:
   - No confíes solo en Python (Pydantic/Django/SQLAlchemy).
   - Las reglas de negocio críticas deben estar en la DB (NOT NULL, CHECK, UNIQUE).
   - "La DB es la última línea de defensa".

D. Documentación (Self-Documenting Schema):
   - Usa COMMENT ON para explicar columnas complejas.
*/

COMMENT ON COLUMN products.metadata IS 'Datos extra variables: dimensiones, colores, specs técnicos en formato JSON.';

-- -----------------------------------------------------------------------------
-- EJEMPLO COMPLETO: TABLA DE EVENTOS (LOGS/AUDITORÍA)
-- -----------------------------------------------------------------------------

CREATE TABLE system_events (
    id BIGSERIAL PRIMARY KEY, -- BIGSERIAL para tablas que crecen masivamente
    event_type VARCHAR(100) NOT NULL,
    actor_id UUID, -- Referencia opcional a users(id)
    payload JSONB NOT NULL,
    ip_address INET, -- Tipo de dato nativo para IPs
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Índice sugerido para rendimiento (se verá en el tema 06)
    -- CREATE INDEX idx_events_type ON system_events(event_type);
    -- CREATE INDEX idx_events_created ON system_events(created_at DESC);
    
    CONSTRAINT fk_actor FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE SET NULL
);

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEVELOPER:
-- -----------------------------------------------------------------------------
-- 1. Diseña pensando en los datos, no solo en los objetos de tu código.
-- 2. Elige el tipo de dato más restrictivo posible (numeric > float).
-- 3. Usa Timezones siempre.
-- 4. Nombra tus constraints para que los errores sean legibles.
-- 5. IF NOT EXISTS es tu amigo en scripts de inicialización manual.
-- -----------------------------------------------------------------------------
