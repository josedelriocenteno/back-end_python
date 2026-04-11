"""
RENDIMIENTO: BATCHING Y OPERACIONES BULK
-----------------------------------------------------------------------------
Cómo insertar o actualizar miles de registros sin bloquear el servidor.
"""

from sqlalchemy import insert
from .modelos_orm import User

def slow_insert(session, users_data):
    """
    ANTI-PATRÓN: Crear objetos uno a uno.
    Muy lento (1000 inserts = 1000 fotos de la sesión).
    """
    for data in users_data:
        u = User(**data)
        session.add(u)
    session.commit()

def fast_insert_orm(session, users_data):
    """
    OPCIÓN ORM: bulk_insert_mappings (SQLAlchemy 1.4/2.0 legacy)
    O simplemente pasar una lista al método add_all.
    """
    session.add_all([User(**d) for d in users_data])
    session.commit()

def super_fast_insert_core(engine, users_data):
    """
    OPCIÓN CORE: executemany implícito.
    La más rápida en SQLAlchemy. Se salta la creación de objetos Python.
    """
    with engine.begin() as conn:
        conn.execute(
            insert(User),
            users_data # Lista de diccionarios
        )

def process_in_batches(session, large_dataset, batch_size=1000):
    """
    Estrategia para Data Engineering: Procesar en bloques para no saturar la RAM.
    """
    for i in range(0, len(large_dataset), batch_size):
        batch = large_dataset[i : i + batch_size]
        # Insertar bloque
        session.execute(insert(User), batch)
        # Commit parcial si es un proceso largo (o gestiona transacciones)
        session.commit()
        # Limpiar la sesión para liberar memoria de objetos hidratados
        session.expunge_all()

"""
RESUMEN PARA EL DESARROLLADOR:
1. Usa 'add_all' para lotes pequeños/medianos en el ORM.
2. Usa 'insert(Table).values(list_of_dicts)' en Core para máxima velocidad.
3. El 'batching' es vital para evitar que tu aplicación se quede sin memoria (OOM).
4. Recuerda que PostgreSQL tiene un límite de parámetros por query (~65535). 
   Si tu tabla tiene 100 columnas, no puedes insertar más de 655 filas de golpe.
"""
