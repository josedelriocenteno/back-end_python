"""
PSYOOPG 3: CONEXIÓN BÁSICA Y SEGURA
-----------------------------------------------------------------------------
Psycopg 3 es el driver de facto para PostgreSQL. Permite conexiones tanto 
síncronas como asíncronas y maneja automáticamente la conversión de tipos 
entre Python y SQL.
"""

import os
import psycopg
from psycopg import Connection

# 1. DEFINICIÓN DE CREDENCIALES
# REGLA DE ORO: Nunca "hardcodees" credenciales. Usa variables de entorno.
DB_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")

def example_connect():
    """
    Forma básica de conectar. Es responsabilidad nuestra cerrar la conexión.
    """
    try:
        conn = psycopg.connect(DB_URL)
        print(f"Conexión exitosa a: {conn.info.dbname}")
        
        # Operaciones...
        
        conn.close()
    except psycopg.OperationalError as e:
        print(f"No se pudo conectar: {e}")

def professional_connect():
    """
    FORMA RECOMENDADA: Uso de Context Managers (with).
    Esto garantiza que la conexión SE CIERRE incluso si hay una excepción.
    """
    with psycopg.connect(DB_URL) as conn:
        print("Conexión segura establecida.")
        # 'conn' está disponible aquí. Al salir del bloque, se cierra sola.
        
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            print(f"Versión de Postgres: {cur.fetchone()[0]}")

def connection_info(conn: Connection):
    """
    Podemos inspeccionar metadatos de la sesión activa.
    """
    print(f"User: {conn.info.user}")
    print(f"Host: {conn.info.host}")
    print(f"Port: {conn.info.port}")
    print(f"DSN: {conn.info.dsn}")

"""
RESUMEN PARA EL DESARROLLADOR:
1. Usa siempre context managers ('with').
2. Las variables de entorno son obligatorias para la URL de conexión.
3. Psycopg 3 soporta el protocolo 'postgresql://', lo cual es muy cómodo.
4. Recuerda que cada llamada a connect() abre una conexión física (lenta).
   En aplicaciones web, usaremos un Pool (visto en temas posteriores).
"""

if __name__ == "__main__":
    professional_connect()
