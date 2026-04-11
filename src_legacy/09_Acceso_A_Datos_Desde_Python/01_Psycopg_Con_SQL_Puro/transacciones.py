"""
PSYOOPG 3: GESTIÓN DE TRANSACCIONES (ACID)
-----------------------------------------------------------------------------
Las transacciones aseguran que un conjunto de operaciones se ejecute 
totalmente o no se ejecute nada.
"""

import psycopg

DB_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

def transaction_examples():
    # 1. EL BLOQUE 'WITH CONN' COMO TRANSACCIÓN
    # En Psycopg 3, si entras en un context manager de conexión, 
    # se inicia una transacción. Si hay una excepción, hace ROLLBACK. 
    # Si todo va bien, hace COMMIT.
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                # Paso 1: Descontar saldo
                cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
                
                # Paso 2: Aumentar saldo
                # Si esto falla (ej: id 2 no existe o error de red)
                cur.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
                
        # Al salir del scope de 'with conn', se hizo commit automáticamente.
        print("Transferencia completada con éxito.")

    except Exception as e:
        print(f"Error en la transacción. Se hizo ROLLBACK automático: {e}")

    # 2. TRANSACCIONES EXPLÍCITAS
    # Útil si ya tienes una conexión abierta y quieres varios bloques atómicos.
    with psycopg.connect(DB_URL) as conn:
        
        # Bloque 1
        with conn.transaction():
            conn.execute("INSERT INTO logs (msg) VALUES ('Inicio Proceso')")
            
        # Bloque 2 (Independiente del 1)
        with conn.transaction():
            conn.execute("UPDATE users SET last_login = now()")

    # 3. AUTOCOMMIT (Para comandos especiales)
    # Comandos como 'CREATE DATABASE' o 'VACUUM' no pueden correr en transacciones.
    with psycopg.connect(DB_URL, autocommit=True) as conn:
        conn.execute("VACUUM ANALYZE users")

"""
RESUMEN PARA EL DESARROLLADOR:
1. Usa el context manager 'with conn' para transacciones implícitas sencillas.
2. Usa 'with conn.transaction()' para mayor control granular.
3. Recuerda: Una transacción abierta demasiado tiempo bloquea recursos en la DB. 
   ¡Mantenlas cortas!
"""

if __name__ == "__main__":
    transaction_examples()
