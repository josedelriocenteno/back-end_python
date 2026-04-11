"""
SQLALCHEMY CORE: METADATA Y DEFINICIÓN DE TABLAS
-----------------------------------------------------------------------------
A diferencia del ORM, en Core definimos 'objetos Tabla' que representan 
directamente la estructura SQL sin vincularlos a una clase de Python.
"""

from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

# 1. EL OBJETO METADATA
# Contenedor que agrupa todas nuestras definiciones de tablas.
metadata_obj = MetaData()

# 2. DEFINICIÓN IMPERATIVA DE TABLAS
# Esto es código Python, pero SQLAlchemy sabe traducirlo a CREATE TABLE.
users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("email", String(100), unique=True),
    Column("created_at", DateTime, server_default=func.now())
)

addresses_table = Table(
    "addresses",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("street", String(100)),
    Column("city", String(50))
)

# 3. REFLECTION (Reflexión)
# Si la tabla ya existe en la DB, no hace falta definirla; podemos "leerla".
def reflect_table(engine):
    existing_table = Table("orders", metadata_obj, autoload_with=engine)
    print(f"Columnas reflejadas: {existing_table.columns.keys()}")

# 4. CREACIÓN FÍSICA (Solo para ejemplos/tests)
# En producción, usaríamos Alembic.
def create_all_tables(engine):
    metadata_obj.create_all(engine)

"""
RESUMEN PARA EL DESARROLLADOR:
1. MetaData() es el catálogo central de tus tablas.
2. Column() define el tipo, constraints y comportamiento (default).
3. 'ForeignKey' vincula tablas a nivel de esquema (Core detecta el tipo solo).
4. La reflexión es utilísima para Scripts de ETL que trabajan con DBs ya creadas.
"""
