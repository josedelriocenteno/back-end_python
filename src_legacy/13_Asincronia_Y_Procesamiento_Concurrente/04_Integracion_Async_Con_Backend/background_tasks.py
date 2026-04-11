"""
FASTAPI: BACKGROUND TASKS (TAREAS EN SEGUNDO PLANO)
-----------------------------------------------------------------------------
Cómo responder al usuario inmediatamente y dejar un proceso pesado 
corriendo de fondo sin necesidad de Celery/Redis para casos simples.
"""

from fastapi import FastAPI, BackgroundTasks
import asyncio

app = FastAPI()

def escribir_en_log(mensaje: str):
    """Acción pesada que no queremos que el usuario espere."""
    import time
    time.sleep(2) # Simula escritura lenta en disco
    print(f"  [Worker] Log guardado: {mensaje}")

@app.post("/send-notification/{user_id}")
async def notify_user(user_id: int, tasks: BackgroundTasks):
    """
    El usuario recibe su 202 inmediatamente, y la tarea se ejecuta 
    cuando el servidor tiene un hueco libre.
    """
    # Programamos la tarea
    tasks.add_task(escribir_en_log, f"Usuario {user_id} notificado")
    
    return {"message": "Notificación en proceso, no esperes..."}

"""
DIFERENCIAS CON CELERY:
-----------------------
- BackgroundTasks: Ocurren en el MISMO proceso de Python que tu API. 
  Si el servidor se apaga, la tarea se pierde. Ideal para tareas cortas 
  como enviar un email o escribir un log.
- Celery: Ocurren en procesos (Workers) totalmente separados. Son 
  resistentes a fallos y escalan en máquinas distintas. Ideal para 
  procesar vídeos, generar reportes pesados, etc.
"""

"""
TESTABILITY:
------------
Testear BackgroundTasks es sencillo con TestClient, ya que puedes 
verificar si el efecto secundario ocurrió tras el test.
"""
