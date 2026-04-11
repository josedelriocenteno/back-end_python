"""
ASINCRONÍA: ASYNC / AWAIT EN FASTAPI
-----------------------------------------------------------------------------
Entender por qué y cuándo usar 'async def' es la clave para que tu API 
pueda manejar miles de peticiones simultáneas con pocos recursos.
"""

import asyncio
from fastapi import FastAPI
import httpx # Cliente HTTP asíncrono

app = FastAPI()

# 1. FUNCIÓN ASÍNCRONA BÁSICA
# Se usa 'async def' cuando la función tiene que esperar a algo externo (I/O)
@app.get("/external-data")
async def get_external_data():
    """
    Ejemplo de llamada a una API externa. 
    Mientras esperamos la respuesta, el servidor puede procesar otros requests.
    """
    async with httpx.AsyncClient() as client:
        # 'await' cede el control al event loop de Python
        response = await client.get("https://api.example.com/data")
        return response.json()

# 2. ESPERAR MÚLTIPLES COSAS A LA VEZ
@app.get("/multi-task")
async def multi_task():
    # Lanzamos dos tareas en paralelo y esperamos a que ambas terminen
    task1 = asyncio.create_task(some_io_operation(1))
    task2 = asyncio.create_task(some_io_operation(2))
    
    res1, res2 = await asyncio.gather(task1, task2)
    return {"results": [res1, res2]}

async def some_io_operation(id: int):
    await asyncio.sleep(1) # Simulamos espera de red
    return f"Data {id}"

# 3. ¿CUÁNDO USAR 'def' NORMAL?
@app.get("/sync-calculation")
def sync_calculation():
    """
    Si tu función hace cálculos matemáticos intensos (CPU Bound) y NO tiene 
    ningún 'await', usa 'def' normal. 
    FastAPI la ejecutará en un hilo aparte para no bloquear el Event Loop.
    """
    result = sum(i*i for i in range(1000000))
    return {"result": result}

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'asyncio' es como un malabarista: solo tiene dos manos (1 hilo), pero 
   mientras una bola está en el aire (esperando I/O), puede mover las otras.
2. NUNCA uses funciones síncronas bloqueantes (como 'time.sleep()' o 
   'requests.get()') dentro de una función 'async def'. Bloquearás a TODOS 
   los usuarios de la API.
3. Si usas SQLAlchemy, asegúrate de usar el motor asíncrono 
   ('postgresql+asyncpg') si vas a definir tus endpoints como 'async def'.
"""
