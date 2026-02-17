"""
SQLALCHEMY ORM: SESIONES Y EL CICLO DE VIDA DE LOS OBJETOS
-----------------------------------------------------------------------------
La 'Session' es el objeto que gestiona la persistencia. Implementa el patrón 
'Unit of Work' y 'Identity Map'.
"""

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from .modelos_orm import User

engine = create_engine("postgresql+psycopg://user:password@localhost:5432/postgres")

# 1. FACTORÍA DE SESIONES
# Configurada una vez al inicio del proyecto.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def basic_operations():
    # 2. USO CON CONTEXT MANAGER
    with SessionLocal() as session:
        # INSERT
        new_user = User(username="alice", email="alice@test.com")
        session.add(new_user) 
        # En este punto el objeto está en estado 'PENDING'.
        
        session.commit() 
        # Ahora está en estado 'PERSISTENT' y tiene ID asignado.

        # SELECT
        # Estilo 2.0: Usamos select() igual que en Core
        stmt = select(User).where(User.username == "alice")
        user = session.execute(stmt).scalar_one()
        print(f"Encontrado: {user.username}")

        # UPDATE
        user.email = "new_alice@test.com"
        # No hace falta llamar a session.add(), SQLAlchemy detecta el cambio!
        session.commit()

        # DELETE
        session.delete(user)
        session.commit()

"""
EL CICLO DE VIDA (ESTADOS):
-----------------------------------------------------------------------------
- Transient: Objeto creado (`user = User()`), no está en la sesión.
- Pending: Tras `session.add(user)`, espera al flush/commit.
- Persistent: Está en la DB y en la sesión. Sincronizado.
- Detached: La sesión se cerró pero el objeto sigue vivo. Peligroso (Lazy Load Error).
"""

"""
RESUMEN PARA EL DESARROLLADOR:
1. La sesión debe ser corta (un request de API = una sesión).
2. 'session.commit()' confirma los cambios, 'session.rollback()' los deshace.
3. El 'Identity Map' asegura que si pides el mismo ID dos veces, recibas la 
   misma instancia de objeto en memoria.
4. 'scalar_one()' devuelve el objeto directamente; 'scalars().all()' una lista.
"""
