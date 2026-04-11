"""
INYECCIÓN DE DEPENDENCIAS: SESIÓN DE BASE DE DATOS
-----------------------------------------------------------------------------
Este es el caso de uso más común en Backend. Proporcionamos una sesión 
de DB limpia para cada request y aseguramos que se cierre al terminar.
"""

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 1. LA FUNCIÓN GENERADORA (Yield)
# Al usar 'yield', FastAPI sabe que hay código que debe ejecutarse DESPUÉS 
# de que el endpoint termine (el cierre de la sesión).
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        # Aquí la sesión se entrega al endpoint
        yield db
    finally:
        # Este código corre siempre después de que se envía la respuesta al cliente
        db.close()
        print("Sesión de base de datos cerrada.")

app = FastAPI()

# 2. USO EN EL ENDPOINT
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Cada vez que alguien llama a este endpoint, FastAPI llama a 'get_db', 
    abre una conexión, nos la pasa en la variable 'db', y la cierra cuando 
    terminamos.
    """
    # user = db.query(User).filter(User.id == user_id).first()
    return {"user_id": user_id, "db_status": "Connected"}

"""
RESUMEN PARA EL DESARROLLADOR:
1. El patrón 'yield' es vital para evitar memory leaks (fugas de conexión).
2. Si el endpoint lanza una excepción, el bloque 'finally' de 'get_db' se 
   ejecuta de todos modos, cerrando la conexión.
3. Esto es mil veces mejor que abrir y cerrar la DB manualmente en cada ruta.
"""
