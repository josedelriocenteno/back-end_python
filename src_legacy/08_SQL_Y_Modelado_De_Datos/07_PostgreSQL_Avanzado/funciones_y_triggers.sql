-- =============================================================================
-- SQL PROFESIONAL: FUNCIONES Y TRIGGERS (LÓGICA EN DB)
-- AUTOMATIZACIÓN E INTEGRIDAD PROGRAMADA
-- =============================================================================

/*
¿POR QUÉ LÓGICA EN LA DB?
-----------------------------------------------------------------------------
A veces, la lógica de negocio es tan crítica para la integridad que no puede
depender solo del backend Python. Los Triggers y Funciones (PL/pgSQL) aseguran 
que las reglas se cumplan siempre, independientemente de quién acceda a la DB.
*/

-- -----------------------------------------------------------------------------
-- 1. FUNCIONES EN PL/pgSQL
-- -----------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION calculate_vat(price NUMERIC, vat_rate NUMERIC DEFAULT 0.21)
RETURNS NUMERIC AS $$
BEGIN
    RETURN price * (1 + vat_rate);
END;
$$ LANGUAGE plpgsql;

-- Uso:
-- SELECT name, calculate_vat(price) FROM products;

-- -----------------------------------------------------------------------------
-- 2. TRIGGERS: AUTOMATIZANDO LA AUDITORÍA
-- -----------------------------------------------------------------------------

/*
Ejemplo Clásico: Mantener la columna 'updated_at' siempre al día.
*/

-- 1. Creamos la función que ejecutará el Trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. Vinculamos la función a la tabla
CREATE TRIGGER trg_update_users_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- -----------------------------------------------------------------------------
-- 3. TRIGGERS PARA REGLAS DE NEGOCIO CRÍTICAS
-- -----------------------------------------------------------------------------

/*
Ejemplo: No permitir que el saldo de una cuenta sea negativo.
(Aunque ya tengamos un CHECK, un Trigger permite lógica más compleja).
*/

CREATE OR REPLACE FUNCTION check_account_balance()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.balance < 0 THEN
        RAISE EXCEPTION 'El saldo no puede ser negativo: %', NEW.balance;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_balance
BEFORE INSERT OR UPDATE ON accounts
FOR EACH ROW
EXECUTE FUNCTION check_account_balance();

-- -----------------------------------------------------------------------------
-- 4. PROCEDURES (Procedimientos Almacenados)
-- -----------------------------------------------------------------------------

/*
A diferencia de las funciones, los PROCEDURES pueden manejar transacciones 
(COMMIT/ROLLBACK) internamente. Disponibles desde Postgres 11.
*/

CREATE OR REPLACE PROCEDURE transfer_funds(
    sender_id INT, 
    receiver_id INT, 
    amount NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE accounts SET balance = balance - amount WHERE id = sender_id;
    UPDATE accounts SET balance = balance + amount WHERE id = receiver_id;
    
    INSERT INTO trxs_log(sender, receiver, val) VALUES (sender_id, receiver_id, amount);
    
    -- COMMIT; -- Opcional, el llamador suele controlar la transacción
END;
$$;

-- Ejecución:
-- CALL transfer_funds(1, 2, 50.00);

-- -----------------------------------------------------------------------------
-- RESUMEN PARA EL DEARROLLADOR:
-- -----------------------------------------------------------------------------
-- 1. No abuses de los Triggers. Son "magia" oculta que puede dificultar el 
--    seguimiento de bugs en tu código Python.
-- 2. Úsalos para: Auditoría (updated_at), sincronización de caché interna y 
--    reglas de integridad extrema.
-- 3. Las funciones son geniales para cálculos que se repiten en muchos SELECTs.
-- 4. Recuerda que los Triggers añaden latencia a cada escritura.
-- -----------------------------------------------------------------------------
