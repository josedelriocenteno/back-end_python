"""
SQL PROFESIONAL: CONSULTAS PARAMETRIZADAS
SEGURIDAD EXTREMA CONTRA SQL INJECTION
-----------------------------------------------------------------------------
REGLA DE ORO #1: Jamás uses f-strings o concatenación manual para construir
tus queries de SQL con datos que vienen del usuario.

MAL: f"SELECT * FROM users WHERE id = {user_id}"
BIEN: cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
"""

import psycopg

def main():
    conn_info = "postgresql://postgres:postgres@localhost:5432/postgres"
    
    with psycopg.connect(conn_info) as conn:
        with conn.cursor() as cur:

            # 1. PASO DE PARÁMETROS POSICIONALES (%s)
            # Nota: Siempre pasa los parámetros como una TUPLA o LISTA, incluso si es solo uno.
            user_id = 101
            cur.execute(
                "SELECT username, email FROM users WHERE id = %s", 
                (user_id,)
            )

            # 2. PASO DE PARÁMETROS NOMBRADOS (Diccionario)
            # Más legible cuando tienes muchos parámetros.
            user_data = {
                "min_price": 100,
                "status": "active",
                "limit": 5
            }
            query = """
                SELECT name, price 
                FROM products 
                WHERE price > %(min_price)s 
                  AND status = %(status)s 
                LIMIT %(limit)s
            """
            cur.execute(query, user_data)

            # 3. BULK INSERT (executemany) - El multiplicador de velocidad
            # Enviar 1000 filas en una sola llamada es 100x más rápido que 1000 llamadas individuales.
            items_to_insert = [
                ("Laptop", 1200),
                ("Mouse", 25),
                ("Keyboard", 80)
            ]
            cur.executemany(
                "INSERT INTO products (name, price) VALUES (%s, %s)", 
                items_to_insert
            )

            # 4. TRUCO DE COMPOSICIÓN DE QUERIES (sql.SQL)
            # A veces necesitas parametrizar NOMBRES de tablas o columnas (que %s no permite).
            # Usa el módulo sql de psycopg para hacerlo de forma segura.
            from psycopg import sql
            
            table_name = "users"
            column_name = "email"
            
            safe_query = sql.SQL("SELECT {col} FROM {table} WHERE id = %s").format(
                col=sql.Identifier(column_name),
                table=sql.Identifier(table_name)
            )
            cur.execute(safe_query, (101,))

"""
RESUMEN PARA EL DEARROLLADOR:
1. %s es un marcador de posición, no un formateador de strings de Python. 
   Psycopg se encarga de escapar las comillas y prevenir ataques.
2. Usa parámetros nombrados %(key)s para queries complejas.
3. executemany() es obligatorio para inserciones masivas (ETLs, migraciones).
4. Jamás intentes escapar strings manualmente. Deja que el driver lo haga.
"""

if __name__ == "__main__":
    main()
