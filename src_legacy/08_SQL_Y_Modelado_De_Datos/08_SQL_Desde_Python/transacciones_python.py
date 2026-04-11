"""
SQL PROFESIONAL: TRANSACCIONES DESDE PYTHON
CONTROL TOTAL DE LA INTEGRIDAD EN TU APP
-----------------------------------------------------------------------------
Por defecto, Psycopg 3 abre una transacción al primer comando y espera a un commit.
Sin embargo, la forma más profesional de manejarlo es usar context managers
explícitos para delimitar tus bloques de negocio.
"""

import psycopg

def main():
    conn_info = "postgresql://postgres:postgres@localhost:5432/postgres"

    try:
        with psycopg.connect(conn_info) as conn:
            
            # 1. TRANSACCIÓN AUTOMÁTICA (Context Manager de Conn)
            # En Psycopg 3, el bloque 'with conn:' hace COMMIT al final 
            # o ROLLBACK si ocurre una excepción.
            with conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
                    cur.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
                    # Si algo falla aquí, Python lanza una excepción, 
                    # el bloque 'with conn' captura el error y hace ROLLBACK.

            # 2. TRANSACCIONES EXPLÍCITAS (Transaction Context Manager)
            # Recomendado para mayor claridad en lógica compleja.
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO audit_log (msg) VALUES (%s)", ("Iniciando proceso",))
                    # Lógica pesada...
                    cur.execute("INSERT INTO audit_log (msg) VALUES (%s)", ("Proceso terminado",))

            # 3. MANEJO DE NIVEL DE AISLAMIENTO
            # Puedes definir cuán estricta es la transacción antes de empezar.
            # conn.isolation_level = psycopg.IsolationLevel.SERIALIZABLE

            # 4. AUTOCOMMIT MODE
            # Útil para logs o tareas donde no importa si fallan otras partes,
            # o para comandos que NO pueden ejecutarse dentro de una transacción 
            # (como 'VACUUM' o 'CREATE DATABASE').
            with psycopg.connect(conn_info, autocommit=True) as conn_fast:
                conn_fast.execute("INSERT INTO simple_logs (msg) VALUES ('Logging fast')")

    except Exception as e:
        print(f"La transacción falló y se hizo ROLLBACK automáticamente: {e}")

"""
RESUMEN PARA EL DEARROLLADOR:
1. Encapsula siempre las operaciones que deban ser atómicas en un bloque 'with conn:'.
2. No mezcles lógica de base de datos con llamadas a APIs externas lentas dentro 
   de una transacción (mantienes bloqueos en la DB demasiado tiempo).
3. Entiende la diferencia entre el estado de la conexión y el estado del cursor.
4. Usa 'autocommit=True' solo cuando sepas exactamente por qué lo necesitas.
"""

if __name__ == "__main__":
    main()
