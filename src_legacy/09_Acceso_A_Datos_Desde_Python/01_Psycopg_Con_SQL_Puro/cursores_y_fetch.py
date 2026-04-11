"""
PSYOOPG 3: CURSORES Y RECUPERACIÓN DE DATOS (FETCH)
-----------------------------------------------------------------------------
Un cursor es el objeto que nos permite iterar sobre los resultados de una query.
Es importante saber cuándo traer todos los datos a RAM y cuándo ir uno a uno.
"""

import psycopg
from psycopg.rows import dict_row # Crucial para APIs

DB_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

def fetch_examples():
    with psycopg.connect(DB_URL) as conn:
        
        # 1. CURSOR ESTÁNDAR (Devuelve Tuplas)
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, email FROM users LIMIT 5")
            
            # Traer solo uno
            first_user = cur.fetchone()
            print(f"User 1 (Tupla): {first_user}") # (1, 'alice', '...')
            
            # Traer el resto
            other_users = cur.fetchall()
            print(f"Resto (Lista de Tuplas): {other_users}")

        # 2. CURSOR DE DICCIONARIO (Recomendado para Backend)
        # Transforma las filas en diccionarios Python automáticamente.
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT id, username FROM users LIMIT 1")
            user_dict = cur.fetchone()
            print(f"User (Dict): {user_dict['username']}")

        # 3. ITERACIÓN DIRECTA (Memoria Eficiente)
        # En lugar de castigar la RAM con fetchall(), el cursor es un iterable.
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM big_table")
            for row in cur:
                # Proceso fila a fila sin cargar toda la tabla en memoria
                pass

        # 4. SERVER-SIDE CURSORS (Para tablas de Millones de filas)
        # Por defecto, psycopg pide todos los datos al servidor y los guarda en el cliente.
        # Con un nombre en el cursor, el servidor mantiene el estado y enviamos lo que pedimos.
        with conn.cursor(name="my_large_query") as cur:
            cur.execute("SELECT * FROM massive_log_table")
            while True:
                chunk = cur.fetchmany(1000) # Pedimos de 1000 en 1000
                if not chunk:
                    break
                # procesar chunk...

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'fetchone()' -> un registro o None.
2. 'fetchall()' -> lista de registros (cuidado con la memoria).
3. 'row_factory=dict_row' -> ideal para serializar a JSON en FastAPI/Flask.
4. Para Data Engineering o tablas gigantes, usa iteradores o cursores de servidor.
"""

if __name__ == "__main__":
    fetch_examples()
