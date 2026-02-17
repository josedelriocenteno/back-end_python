"""
DATA ENGINEERING: ESCRITURA INCREMENTAL Y UPSERT
-----------------------------------------------------------------------------
Cómo sincronizar datos entre orígenes utilizando la potencia de Postgres.
"""

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine, MetaData, Table
from .modelos_orm import User

engine = create_engine("postgresql+psycopg://user:pass@localhost/db")

def upsert_incremental(data_to_sync: list):
    """
    Implementación del patrón Upsert (Insert or Update) para sincronización.
    """
    # Usamos SQLAlchemy Core para máxima eficiencia
    with engine.begin() as conn:
        for chunk in [data_to_sync[i:i + 1000] for i in range(0, len(data_to_sync), 1000)]:
            
            # Construir el statement de Postgres 'ON CONFLICT'
            stmt = insert(User).values(chunk)
            
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=['username'], # O la columna UNIQUE
                set_={
                    "email": stmt.excluded.email,
                    "updated_at": stmt.excluded.updated_at
                }
            )
            
            conn.execute(upsert_stmt)

def delta_load_check(last_checkpoint):
    """
    Extraer solo lo que ha cambiado desde la última carga.
    """
    from sqlalchemy import select
    stmt = select(User).where(User.updated_at > last_checkpoint)
    # ... ejecutar y cargar ...

"""
RESUMEN PARA EL DATA ENGINEER:
1. El dialecto de Postgres en SQLAlchemy permite 'on_conflict_do_update'.
2. Divide tus datos en 'chunks' (lotes) de 1000-5000 registros para optimizar 
   el uso de red y memoria.
3. El uso de 'EXCLUDED' en el upsert permite referenciar los valores que 
   intentabas insertar sin tener que pasarlos dos veces.
"""
