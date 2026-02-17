"""
ARQUITECTURA: PATRÓN REPOSITORIO
-----------------------------------------------------------------------------
El repositorio media entre la lógica de negocio y el mapeo de datos, 
actuando como una colección de objetos en memoria.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from .modelos_orm import User

class UserRepository:
    """
    Encapsula toda la lógica de consultas de la entidad Usuario.
    """
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.execute(stmt).scalar_one_or_none()

    def list_active(self, limit: int = 100) -> List[User]:
        stmt = select(User).where(User.is_active == True).limit(limit)
        return list(self.session.scalars(stmt).all())

    def add(self, user: User) -> None:
        self.session.add(user)

    def delete(self, user: User) -> None:
        self.session.delete(user)

"""
VENTAJAS DEL REPOSITORIO:
-----------------------------------------------------------------------------
1. Desacoplamiento: Si mañana decides filtrar los usuarios activos de otra 
   forma, solo cambias el método 'list_active'.
2. Testeabilidad: Es fácil crear un 'FakeUserRepository' que use una lista 
   en memoria para tus tests unitarios.
3. Centralización: Las consultas complejas (JOINs, filtros pesados) no están 
   regadas por todo el código.
"""

# Uso en un servicio
def deactivate_user_service(user_id: int, db_session: Session):
    repo = UserRepository(db_session)
    user = repo.get_by_id(user_id)
    if user:
        user.is_active = False
        # Nota: El repo no debería hacer commit, eso es trabajo del Unit of Work.
        db_session.commit()
