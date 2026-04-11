"""
INYECCIÓN DE DEPENDENCIAS: CAPA DE SERVICIO
-----------------------------------------------------------------------------
Desacoplando la lógica de negocio del controlador. Inyectamos servicios 
que a su vez reciben la base de datos.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db_dependency import get_db

app = FastAPI()

# 1. LA CAPA DE SERVICIO
class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str):
        # Lógica de negocio real aquí...
        return {"id": 1, "name": name, "status": "Created in DB"}

# 2. FÁBRICA DE SERVICIO
# Una dependencia que a su vez depende de la base de datos.
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

# 3. ENDPOINT LIMPIO
# El controlador no sabe nada del ORM, solo habla con el servicio.
@app.post("/users/")
def register_user(
    name: str, 
    service: UserService = Depends(get_user_service)
):
    return service.create_user(name)

"""
VENTAJAS DE ESTE DISEÑO:
-----------------------------------------------------------------------------
1. Testeabilidad: En tus tests, puedes sobreescribir 'get_user_service' para 
   devolver un MockService que no use una base de datos real.
   'app.dependency_overrides[get_user_service] = my_mock'
2. Reutilización: El mismo 'UserService' puede ser usado por otros servicios 
   o incluso por scripts de CLI, inyectándole la sesión manualmente.
3. Legibilidad: El endpoint queda reducido a 1 o 2 líneas de código.
"""
