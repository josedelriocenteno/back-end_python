"""
HELLO WORLD: TU PRIMERA API CON FASTAPI
-----------------------------------------------------------------------------
FastAPI utiliza decoradores para definir rutas y tipos de Python para la 
validación automática y generación de documentación.
"""

from fastapi import FastAPI
from typing import Dict

# 1. CREACIÓN DE LA INSTANCIA
# Aquí se configura el título y la versión que aparecerán en Swagger
app = FastAPI(
    title="Mi Primera API Profesional",
    description="Backend moderno para el curso de Python",
    version="1.0.0"
)

# 2. DEFINICIÓN DE UNA RUTA (ENDPOINT)
# @app.get("/") es el decorador que asocia la URL con la función
@app.get("/")
async def root() -> Dict[str, str]:
    """
    Endpoint de bienvenida.
    FastAPI convierte automáticamente este diccionario en un JSON.
    """
    return {"message": "Hello Backend Python!"}

# 3. ENDPOINT CON PARÁMETROS
@app.get("/hello/{name}")
async def say_hello(name: str):
    """
    Parámetro de ruta (Path Parameter).
    FastAPI valida automáticamente que sea el tipo solicitado.
    """
    return {"message": f"Hola, {name}!"}

"""
CÓMO EJECUTAR ESTO:
-----------------------------------------------------------------------------
Desde la terminal, usa uvicorn apuntando al archivo y a la instancia:
$ uvicorn hello_api:app --reload

--reload: Reinicia el servidor automáticamente cuando guardas cambios (solo para dev).
"""

"""
LOGS DE FASTAPI AL INICIAR:
-----------------------------------------------------------------------------
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Application startup complete.
"""

if __name__ == "__main__":
    # También puedes ejecutarlo programáticamente (pero no es lo común)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
