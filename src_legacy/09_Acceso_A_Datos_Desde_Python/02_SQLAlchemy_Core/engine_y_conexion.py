"""
SQLALCHEMY CORE: EL MOTOR Y LA CONEXIÓN
-----------------------------------------------------------------------------
SQLAlchemy es mucho más que un ORM. Su base es el 'Engine', que gestiona 
el dialecto de SQL y el Pool de conexiones de forma transparente.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# 1. CREACIÓN DEL ENGINE
# El engine es el punto de entrada central. NO abre una conexión inmediata;
# la abre solo cuando se le pide.
DATABASE_URL = "postgresql+psycopg://user:password@localhost:5432/dbname"

# echo=True imprime todo el SQL generado en la consola (útil para desarrollo)
engine = create_engine(DATABASE_URL, echo=True)

def basic_execution(eng: Engine):
    """
    Ejecutar SQL textual usando el Engine.
    """
    with eng.connect() as conn:
        # En SQLAlchemy 2.0, el SQL textual debe envolverse en text()
        result = conn.execute(text("SELECT 'Hello from Core'"))
        print(result.all())

def metadata_inspection(eng: Engine):
    """
    Podemos inspeccionar la base de datos a través del motor.
    """
    from sqlalchemy import inspect
    inspector = inspect(eng)
    print(f"Tablas encontradas: {inspector.get_table_names()}")

"""
CONFIGURACIÓN PROFESIONAL DEL POOL:
-----------------------------------------------------------------------------
SQLAlchemy gestiona un pool de conexiones automáticamente. Puedes ajustarlo:
"""
engine_pro = create_engine(
    DATABASE_URL,
    pool_size=10,        # Conexiones mantenidas abiertas
    max_overflow=20,     # Conexiones extra si el pool está lleno
    pool_timeout=30,     # Segundos a esperar antes de dar error
    pool_recycle=1800    # Segundos antes de regenerar una conexión vieja
)

"""
RESUMEN PARA EL DESARROLLADOR:
1. El Engine es GLOBAL y debe crearse una sola vez en tu app.
2. Usa 'postgresql+psycopg' como driver para aprovechar Psycopg 3.
3. El context manager 'with engine.connect()' gestiona la devolución al pool.
4. 'echo=True' es tu mejor amigo para debuguear pero JAMÁS en producción.
"""

if __name__ == "__main__":
    basic_execution(engine)
