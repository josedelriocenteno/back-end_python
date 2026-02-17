"""
PSYOOPG 3: CONSULTAS PARAMETRIZADAS (SEGURIDAD)
-----------------------------------------------------------------------------
NUNCA uses f-strings o concatenación para tus queries. 
Este archivo muestra cómo pasar datos de forma segura para evitar SQL Injection.
"""

import psycopg

DB_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

def security_examples():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            
            # 1. PARÁMETROS POSICIONALES (%s)
            # Nota: Los datos se pasan como el segundo argumento de execute().
            # Psycopg se encarga de escapar comillas y tipos.
            user_input = "alice' OR 1=1; --" # Intento de inyección
            cur.execute("SELECT * FROM users WHERE username = %s", (user_input,))
            # La query final será segura porque escapará el input.

            # 2. SEGUNDO ARGUMENTO SIEMPRE ES UNA TUPLA O LISTA
            user_id = 99
            cur.execute("SELECT * FROM users WHERE id = %s", [user_id])

            # 3. PARÁMETROS NOMBRADOS (DICCIONARIO)
            # Mucho mejor cuando hay muchas variables.
            search_params = {
                "min_age": 18,
                "status": "active",
                "limit": 10
            }
            query = """
                SELECT * FROM users 
                WHERE age >= %(min_age)s 
                  AND status = %(status)s 
                LIMIT %(limit)s
            """
            cur.execute(query, search_params)

            # 4. BATCH INSERT (executemany)
            # Mucho más rápido que llamar a execute() en un loop.
            users_to_create = [
                ("tom", "tom@test.com"),
                ("jerry", "jerry@test.com"),
                ("spike", "spike@test.com")
            ]
            cur.executemany(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                users_to_create
            )

"""
RESUMEN PARA EL DESARROLLADOR:
1. Usa marcadores %s (posicional) o %(key)s (nombrado).
2. Pasa los datos como una tupla o diccionario independiente.
3. Jamás hagas: f"SELECT ... WHERE id = {id}". Estás a un paso de ser hackeado.
4. Para insertar miles de filas, usa 'executemany()' para optimizar el round-trip.
"""

if __name__ == "__main__":
    security_examples()
