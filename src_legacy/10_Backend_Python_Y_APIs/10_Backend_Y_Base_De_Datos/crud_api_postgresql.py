"""
BACKEND + DB: CRUD COMPLETO CON POSTGRESQL
-----------------------------------------------------------------------------
Integración final de FastAPI, SQLAlchemy y Pydantic para crear un 
gestor de usuarios real.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# 1. IMPORTACIONES SIMULADAS (Contexto de archivos anteriores)
# from .db import get_db, Base
# from .models import User as DBUser
# from .schemas import UserCreate, UserOut

app = FastAPI()

# 2. ENDPOINT: CREAR USUARIO
@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Recibe un Schema, lo guarda como un Modelo de DB y devuelve un Schema de salida.
    """
    # Verificamos si el usuario ya existe
    db_user = db.query(DBUser).filter(DBUser.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Creamos la instancia del modelo de SQLAlchemy
    new_user = DBUser(
        email=user_in.email,
        hashed_password=fake_hash_password(user_in.password), # No guardar en plano!
        username=user_in.username
    )
    
    db.add(new_user)
    db.commit() # Guardamos físicamente en Postgres
    db.refresh(new_user) # Obtenemos el ID generado por la DB
    return new_user

# 3. ENDPOINT: LISTAR CON PAGINACIÓN
@app.get("/users/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(DBUser).offset(skip).limit(limit).all()
    return users

"""
RESUMEN PARA EL DESARROLLADOR:
1. El flujo siempre es: Request (JSON) -> Pydantic Schema -> SQLAlchemy Model -> DB.
2. 'db.commit()' es lo que hace persistentes los cambios. Si no lo llamas, los 
   datos se pierden al cerrar la sesión.
3. 'db.refresh(obj)' es crucial después de un commit si necesitas leer campos 
   que la DB autogenera (como el ID o el created_at).
4. El manejo de errores (400 Bad Request) ocurre antes del commit.
"""
