"""
SQLALCHEMY CORE: TRANSACCIONES Y COMMIT "AS YOU GO" vs "BEGIN ONCE"
-----------------------------------------------------------------------------
Manejo profesional de la atomicidad en SQLAlchemy Core.
"""

from sqlalchemy import insert, update
from .metadata_y_tablas import users_table

def transaction_begin_once(engine):
    """
    ESTILO RECOMENDADO: Abrir transacción al conectar.
    Si el bloque 'with' termina sin errores, hace COMMIT. Si falla, ROLLBACK.
    """
    with engine.begin() as conn:
        conn.execute(insert(users_table).values(name="Alice"))
        conn.execute(insert(users_table).values(name="Bob"))
        # Si aquí ocurre un error, 'Alice' tampoco se guarda.

def transaction_explicit(engine):
    """
    ESTILO MANUAL: Tienes control total de cuándo hacer commit.
    """
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(update(users_table).where(users_table.c.id == 1).values(name="New Name"))
            # Confirmar cambios
            trans.commit()
        except:
            # Deshacer cambios
            trans.rollback()
            raise

def error_handling_core(engine):
    from sqlalchemy.exc import IntegrityError
    
    with engine.begin() as conn:
        try:
            conn.execute(insert(users_table).values(name="Dup", email="same@test.com"))
            conn.execute(insert(users_table).values(name="Dup", email="same@test.com"))
        except IntegrityError:
            print("Capturado error de integridad de SQLAlchemy")

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'engine.begin()' es el atajo más seguro y profesional para transacciones.
2. SQLAlchemy traduce los errores nativos de Postgres a excepciones propias 
   (IntegrityError, OperationalError, DataError).
3. Nunca olvides que 'engine.connect()' NO inicia una transacción por defecto 
   en modo autocommit=False; necesitas llamar a .begin() o usar .begin() directamente.
"""
