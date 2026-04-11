"""
CASO DE USO: BACKEND (API)
-----------------------------------------------------------------------------
Cómo un ORM brilla en el desarrollo de APIs gracias a la asociación 
con Pydantic y el manejo de sesiones.
"""

from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .modelos_orm import User # Supongamos que importamos los modelos del tema anterior

# 1. Esquema Pydantic (Para respuesta de API)
class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True

# 2. Lógica de Servicio con ORM
# Nota la rapidez para recuperar, transformar y devolver
def get_active_users(db: Session) -> List[UserSchema]:
    # El ORM nos da una sintaxis limpia y orientada a objetos
    users = db.query(User).filter(User.is_active == True).all()
    
    # La integración ORM -> Pydantic es casi automática
    return [UserSchema.model_validate(u) for u in users]

def create_user_with_profile(db: Session, user_data: dict, profile_data: dict):
    # La gestión de transacciones y relaciones es sencilla
    new_user = User(**user_data)
    new_user.profile = Profile(**profile_data) # Relacionado automáticamente
    db.add(new_user)
    db.commit()
    return new_user

"""
POR QUÉ EL ORM AQUÍ:
1. Menos boilerplate: No hay que escribir INSERTs manuales.
2. Seguridad: Pydantic + ORM filtran inputs.
3. Consistencia: La sesión asegura que el usuario creado esté disponible.
"""
