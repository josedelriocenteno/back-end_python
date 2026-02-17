"""
DATA ENGINEERING: LECTURA MASIVA DE DATOS
-----------------------------------------------------------------------------
Cómo extraer millones de registros de la DB sin saturar la memoria y de 
forma eficiente.
"""

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session
from .modelos_orm import User

engine = create_engine("postgresql+psycopg://user:pass@localhost/db")

# 1. EL ERROR: fetchall() masivo
def bad_read_all():
    with Session(engine) as session:
        # Si la tabla tiene 10M de filas, esto crashea la app (Out Of Memory)
        users = session.scalars(select(User)).all()
        return users

# 2. SOLUCIÓN A: Stream Results (Server-side Cursor)
def streaming_read():
    with Session(engine) as session:
        # .yield_per() configura a SQLAlchemy para que pida los datos poco a poco
        # al servidor (usando cursores internos de Postgres).
        stmt = select(User).execution_options(yield_per=1000)
        
        for user in session.scalars(stmt):
            # Procesar un objeto a la vez
            print(user.username)
            
            # PRO TIP: Si no necesitas los objetos, usa session.expunge(user) 
            # para que SQLAlchemy no los guarde en su Identity Map y libere RAM.

# 3. SOLUCIÓN B: Paginación Keyset (Filtro por ID)
def keyset_pagination():
    """
    Forma más robusta de leer datos de forma incremental sin cursores abiertos.
    """
    last_id = 0
    batch_size = 5000
    
    with Session(engine) as session:
        while True:
            stmt = select(User).where(User.id > last_id).order_by(User.id).limit(batch_size)
            batch = session.scalars(stmt).all()
            
            if not batch:
                break
            
            for user in batch:
                # Procesar...
                last_id = user.id
            
            print(f"Procesado hasta ID: {last_id}")

"""
RESUMEN PARA EL DATA ENGINEER:
1. 'yield_per' es tu mejor amigo para streaming de datos.
2. Keyset pagination (filtrar por el último ID visto) es preferible a OFFSET 
   para grandes volúmenes.
3. Considera usar SQLAlchemy Core si tu proceso es puramente analítico; el overhead 
   de crear objetos ORM (instanciar clases) es significativo en millones de registros.
"""
