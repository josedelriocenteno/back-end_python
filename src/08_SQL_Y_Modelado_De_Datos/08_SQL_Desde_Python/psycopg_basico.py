"""
SQL PROFESIONAL: PSYCOPG BÁSICO
EL DRIVER ESTÁNDAR PARA POSTGRESQL EN PYTHON
-----------------------------------------------------------------------------
Psycopg (versión 3) es el adaptador de base de datos PostgreSQL más popular para Python.
Es rápido, seguro y está diseñado para aplicaciones modernas y asíncronas.

Instalación:
    pip install "psycopg[binary]"
"""

import psycopg
from psycopg.rows import dict_row

# 1. CONEXIÓN BÁSICA (The Pro Way)
# Siempre usa un Context Manager (with) para asegurar que la conexión se cierre.
CONN_INFO = "host=localhost dbname=postgres user=postgres password=postgres"

def main():
    try:
        # El context manager de 'connect' cierra la conexión al terminar el bloque
        with psycopg.connect(CONN_INFO) as conn:
            
            # 2. CURSORES
            # Un cursor es el objeto que usamos para ejecutar SQL y recuperar resultados.
            with conn.cursor() as cur:
                
                # Ejecutar una query simple
                cur.execute("SELECT 'Hello World' as greeting")
                
                # Recuperar una sola fila
                row = cur.fetchone()
                print(f"Resultado directo: {row[0]}")

            # 3. CURSORES DE DICCIONARIO (Muy útil para APIs)
            # Por defecto, psycopg devuelve tuplas. dict_row devuelve diccionarios.
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT 1 as id, 'Alice' as name")
                user = cur.fetchone()
                print(f"Diccionario: {user['name']} (ID: {user['id']})")

    except psycopg.OperationalError as e:
        print(f"Error de conexión: {e}")

# 4. MEJORES PRÁCTICAS DE CONFIGURACIÓN
# En producción, nunca pongas las credenciales en el código.
# Usa variables de entorno o una URL de conexión de Postgres.
# SQLALCHEMY_DATABASE_URL = "postgresql://user:pass@host:port/dbname"

"""
RESUMEN PARA EL DEVELOPER:
1. Usa siempre context managers (with) tanto para conexiones como para cursores.
2. row_factory=dict_row es tu mejor amigo para convertir SQL en JSON/Objetos Pydantic.
3. Separa la lógica de conexión de la lógica de negocio.
4. Aprende a manejar excepciones específicas de Psycopg (OperationalError, DataError).
"""

if __name__ == "__main__":
    main()
