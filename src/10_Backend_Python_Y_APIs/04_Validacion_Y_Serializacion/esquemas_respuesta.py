"""
DISEÑO DE APIS: ESQUEMAS DE RESPUESTA (DTOs)
-----------------------------------------------------------------------------
Nunca devuelvas tus modelos de base de datos directamente. Usa Schemas de 
salida para filtrar y transformar la información que ve el cliente.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

# 1. MODELO DE "ENTRADA" (Lo que el cliente envía)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str # El cliente envía la contraseña

# 2. MODELO DE "SALIDA" (Lo que el cliente recibe)
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    # NOTA: No incluimos 'password' por seguridad.

    # Esto permite que Pydantic lea datos de objetos de SQLAlchemy o diccionarios
    model_config = ConfigDict(from_attributes=True)

# 3. MODELO DE "LISTADO"
# A veces para una lista no quieres todos los campos, solo un resumen.
class UserSummary(BaseModel):
    username: str
    
    model_config = ConfigDict(from_attributes=True)

# 4. EJEMPLO EN API
from fastapi import FastAPI

app = FastAPI()

@app.post("/users/", response_model=UserOut)
async def create_user(user_in: UserCreate):
    # Imaginemos que guardamos en DB y obtenemos un objeto con ID y Password Hash
    db_user_obj = {
        "id": 1,
        "username": user_in.username,
        "email": user_in.email,
        "password_hash": "argon2$hashed_pass",
        "created_at": datetime.now()
    }
    
    # Al declarar 'response_model=UserOut', FastAPI filtra automáticamente 
    # el 'password_hash' y solo devuelve lo definido en UserOut.
    return db_user_obj

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'from_attributes=True' es la antigua opción 'orm_mode=True'.
2. Crear un Schema de salida diferente al de entrada protege la privacidad de los datos.
3. Mantén los nombres de atributos iguales entre tu DB y tu Schema para que 
   el mapeo sea instantáneo.
"""
