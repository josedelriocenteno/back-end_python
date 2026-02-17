-- =============================================================================
-- SQL PROFESIONAL: DDL - CONSTRAINTS (RESTRICCIONES)
-- PROTEGIENDO LA INTEGRIDAD DE LOS DATOS DESDE LA RAÍZ
-- =============================================================================

/*
¿POR QUÉ CONSTRAINTS?
-----------------------------------------------------------------------------
En el desarrollo Backend, solemos validar datos con Pydantic o Marshmallow.
Sin embargo, las aplicaciones escalan, cambian de versión o tienen procesos
batch independientes.

Las CONSTRAINTS en la DB son la ÚNICA GARANTÍA real de que los datos serán
consistentes, independientemente de quién o qué inserte los datos.
*/

-- -----------------------------------------------------------------------------
-- 1. PRIMARY KEY (PK) - Identidad Única
-- -----------------------------------------------------------------------------

-- Una PK garantiza que no haya filas duplicadas y crea un índice automáticamente.
-- TIP: Usa nombres explícitos para tus PKs para facilitar el debugging.

CREATE TABLE example_pk (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT
);

-- -----------------------------------------------------------------------------
-- 2. NOT NULL - Presencia Obligatoria
-- -----------------------------------------------------------------------------

-- El error más común en Backend es el "NoneType" o "AttributeError".
-- Forzar NOT NULL en la DB elimina gran parte de estos bugs.

CREATE TABLE example_null (
    id SERIAL PRIMARY KEY,
    required_field TEXT NOT NULL,
    optional_field TEXT -- Por defecto permite NULL
);

-- -----------------------------------------------------------------------------
-- 3. UNIQUE - No Duplicidad
-- -----------------------------------------------------------------------------

/*
Útil para emails, usernames, SKUs de productos o slugs de URLs.
Postgres implementa UNIQUE mediante un índice B-Tree.
*/

CREATE TABLE example_unique (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100),
    
    -- Constraint con nombre explícito (Recomendado)
    CONSTRAINT uk_slug UNIQUE (slug)
);

-- -----------------------------------------------------------------------------
-- 4. CHECK - Validación de Lógica de Negocio
-- -----------------------------------------------------------------------------

/*
Los CHECK constraints permiten ejecutar expresiones booleanas antes de insertar.
Es como tener "Middlewares" o "Validators" dentro de la propia DB.
*/

CREATE TABLE example_check (
    id SERIAL PRIMARY KEY,
    age INT,
    price NUMERIC(10, 2),
    discount_price NUMERIC(10, 2),
    status TEXT,
    
    -- Validación de rango
    CONSTRAINT ck_age CHECK (age >= 18 AND age <= 120),
    
    -- Validación de lógica relacional entre columnas
    CONSTRAINT ck_price_logic CHECK (discount_price < price),
    
    -- Validación de lista de valores (Alternativa a ENUM)
    CONSTRAINT ck_status_values CHECK (status IN ('active', 'inactive', 'pending'))
);

-- -----------------------------------------------------------------------------
-- 5. FOREIGN KEY (FK) - Integridad Referencial
-- -----------------------------------------------------------------------------

/*
Garantiza que el valor de una columna exista en otra tabla.
Crucial para evitar "Datos Huérfanos".
*/

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE subcategories (
    id SERIAL PRIMARY KEY,
    category_id INT,
    name TEXT NOT NULL,
    
    -- Definición profesional de FK
    CONSTRAINT fk_category 
        FOREIGN KEY (category_id) 
        REFERENCES categories(id) 
        ON DELETE CASCADE -- Si se borra la categoría, se borran las subcategorías
);

-- -----------------------------------------------------------------------------
-- 6. GESTIÓN DE RESTRICCIONES EN TABLAS EXISTENTES
-- -----------------------------------------------------------------------------

-- A veces necesitamos añadir una restricción a una tabla que ya tiene datos.

-- 1. Añadir NOT NULL
-- ALTER TABLE users ALTER COLUMN username SET NOT NULL;

-- 2. Añadir CHECK (CON VALIDADOR)
-- VALIDATE CONSTRAINT asegura que los nuevos datos cumplan, 
-- pero añade la constraint sin bloquear la tabla por mucho tiempo.
-- ALTER TABLE orders ADD CONSTRAINT ck_total_positive CHECK (total > 0) NOT VALID;
-- ALTER TABLE orders VALIDATE CONSTRAINT ck_total_positive;

-- -----------------------------------------------------------------------------
-- 7. CONSTRAINTS MULTI-COLUMNA (Composites)
-- -----------------------------------------------------------------------------

CREATE TABLE user_permissions (
    user_id UUID,
    permission_id INT,
    
    -- Un usuario no puede tener el mismo permiso dos veces
    PRIMARY KEY (user_id, permission_id)
);

-- -----------------------------------------------------------------------------
-- RESUMEN DE IMPACTO EN EL CÓDIGO (Python):
-- -----------------------------------------------------------------------------
-- 1. Menos validaciones repetitivas en el código de aplicación.
-- 2. Manejo de excepciones: Cuando una constraint falla, Postgres lanza un 
--    código de error específico (ej: 23505 para UNIQUE).
-- 3. Ejemplo en Python (Psycopg):
--    try:
--        cursor.execute("INSERT INTO users (email) VALUES (%s)", (email,))
--    except errors.UniqueViolation:
--        print("El usuario ya existe")
-- -----------------------------------------------------------------------------
