"""
SQLALCHEMY ORM: ERRORES COMUNES Y SOLUCIONES
-----------------------------------------------------------------------------
Identificar los errores típicos del ORM nos ahorra horas de frustración.
"""

from sqlalchemy import select
from .modelos_orm import User, Post

def common_mistakes(session):
    
    # 1. EL ERROR DEL 'DETACHED INSTANCE'
    # Sucede al acceder a un atributo 'lazy' después de que la sesión se cerró.
    def get_user():
        with session_factory() as s:
            return s.get(User, 1)

    u = get_user()
    try:
        print(u.posts) # CRASH! La sesión ya no existe.
    except Exception as e:
        print(f"Error esperado: {e}")

    # 2. NO USAR SCALARS()
    # execute() devuelve una fila (Row), scalars() extrae el objeto del ORM.
    stmt = select(User)
    result = session.execute(stmt)
    # MAL: row = result.first(); print(row.User.name)
    # BIEN: user = result.scalars().first(); print(user.name)

    # 3. FILTRAR POR EL OBJETO EN LUGAR DEL ID
    # SQLAlchemy lo maneja bien, pero es más eficiente ser explícito.
    post = session.get(Post, 1)
    # Menos óptimo: select(Post).where(Post.author == my_user_obj)
    # Mejor: select(Post).where(Post.user_id == my_user_id)

    # 4. OLVIDAR EL FLUSH ANTES DE NECESITAR EL ID
    # Si dependes de un ID generado por la DB para una lógica posterior...
    new_user = User(username="temp")
    session.add(new_user)
    # print(new_user.id) -> None o error
    session.flush() # Envía a la DB pero NO confirma la transacción todavía.
    print(f"ID asignado temporalmente: {new_user.id}")

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'session.flush()' sincroniza cambios con la DB sin terminar la transacción.
2. 'scalars()' es indispensable para recibir objetos en lugar de tuplas.
3. Si recibes DetachedInstanceError, te falta un joinedload/selectinload.
4. Jamás hagas queries pesadas en el __init__ de tus modelos.
"""
