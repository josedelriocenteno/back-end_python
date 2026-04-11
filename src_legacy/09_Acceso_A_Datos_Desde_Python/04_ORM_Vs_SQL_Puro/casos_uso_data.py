"""
CASO DE USO: DATA ENGINEERING (ETL)
-----------------------------------------------------------------------------
Por qué el SQL Puro es superior para cargar grandes volúmenes de datos.
"""

import psycopg
from psycopg import sql

# 1. CARGA MASIVA (UPSERT)
# En Data Engineering, a menudo recibimos archivos CSV/JSON con miles de filas.
def bulk_load_users(conn, data_list: list):
    """
    data_list es una lista de tuplas [(name, email, age), ...]
    """
    with conn.cursor() as cur:
        # El comando 'copy' de psycopg es la forma más rápida de insertar en Postgres
        # Supera por mucho a cualquier sesión de ORM
        with cur.copy("COPY users (name, email, age) FROM STDIN") as copy:
            for row in data_list:
                copy.write_row(row)

# 2. AGREGACIONES COMPLEJAS PARA REPORTES
def generate_monthly_report(conn):
    query = """
    SELECT 
        DATE_TRUNC('month', created_at) as month,
        category,
        SUM(amount) as total,
        AVG(amount) as avg_ticket,
        COUNT(DISTINCT user_id) as unique_users
    FROM orders
    GROUP BY 1, 2
    ORDER BY 1 DESC
    """
    # Intentar hacer esto en un ORM resulta en código Python ilegible.
    # En SQL puro es estándar y optimizable por el DB Admin.
    return conn.execute(query).fetchall()

"""
POR QUÉ SQL PURO AQUÍ:
1. Eficiencia de memoria: No creamos miles de objetos Python pesados.
2. Velocidad: 'COPY' es hasta 20 veces más rápido que INSERTs individuales.
3. Poder: Aprovechamos funciones analíticas de PostgreSQL al 100%.
"""
if __name__ == "__main__":
    # bulk_load_users(conn, my_massive_list)
    pass
