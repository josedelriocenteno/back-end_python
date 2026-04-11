"""
SEGURIDAD: EJEMPLOS REALES DE VULNERABILIDADES
-----------------------------------------------------------------------------
Este archivo muestra código inseguro 'de la vida real' y cómo arreglarlo.
"""

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- CASO 1: MASS ASSIGNMENT (VULNERABLE) ---
class UserDB(BaseModel):
    id: int
    username: str
    is_admin: bool = False

@app.put("/profile/vulnerable")
async def update_profile_vulnerable(payload: dict):
    # ¡MAL! El usuario puede enviar "is_admin": true y el código lo guarda.
    user_data = get_user_from_db()
    for key, value in payload.items():
        setattr(user_data, key, value)
    return {"message": "Profile updated"}

# --- CASO 1: ARREGLO (SEGURO) ---
class ProfileUpdate(BaseModel):
    # Solo definimos los campos que el usuario TIENE permitido tocar.
    display_name: str
    bio: str | None = None

@app.put("/profile/safe")
async def update_profile_safe(payload: ProfileUpdate):
    # Pydantic solo capturará display_name y bio. 
    # Nada más entrará en nuestro sistema.
    user_data = get_user_from_db()
    user_data.display_name = payload.display_name
    return {"message": "Profile updated safely"}


# --- CASO 2: DATA EXPOSURE (VULNERABLE) ---
@app.get("/users/vulnerable/{uid}")
def get_user_vulnerable(uid: int):
    user = db.query(User).get(uid)
    # ¡MAL! Devuelve todo el objeto de DB, incluyendo campos internos
    return user 

# --- CASO 2: ARREGLO (SEGURO) ---
class UserOutput(BaseModel):
    id: int
    username: str
    # NO incluimos password_hash ni is_admin

@app.get("/users/safe/{uid}", response_model=UserOutput)
def get_user_safe(uid: int):
    user = db.query(User).get(uid)
    # FastAPI filtrará automáticamente los campos según UserOutput
    return user

"""
LECCIONES APRENDIDAS:
-----------------------------------------------------------------------------
1. Usa siempre Esquemas de Pydantic específicos para ENTRADA y SALIDA.
2. NUNCA uses diccionarios genéricos (dict) para recibir datos de usuario.
3. El 'response_model' de FastAPI es tu mejor amigo para evitar fugas de datos.
"""
