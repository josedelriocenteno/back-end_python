"""
ASINCRONÍA: TAREAS BATCH Y JOBS
-----------------------------------------------------------------------------
Cómo gestionar procesos masivos desde una API de forma segura.
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
import uuid

app = FastAPI()

# Diccionario para seguir el estado de tareas largas
tasks_db = {}

def heavy_processing_job(task_id: str, data_size: int):
    tasks_db[task_id] = "processing"
    # Simulamos proceso masivo
    import time
    time.sleep(10) # 10 segundos de trabajo
    tasks_db[task_id] = "completed"

@app.post("/jobs/start-import")
async def start_import(data_count: int, background_tasks: BackgroundTasks):
    """
    Inicia un trabajo pesado y devuelve un ID para seguimiento.
    """
    task_id = str(uuid.uuid4())
    tasks_db[task_id] = "pending"
    
    background_tasks.add_task(heavy_processing_job, task_id, data_count)
    
    return {"job_id": task_id, "status": "started"}

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """
    Permite al cliente preguntar: "¿Cómo va mi tarea?" (Polling).
    """
    status = tasks_db.get(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="ID de trabajo no encontrado")
    
    return {"job_id": job_id, "status": status}

"""
RESUMEN PARA EL DESARROLLADOR:
1. En procesos de Data Engineering, JAMÁS hagas esperar al cliente más de 
   1 o 2 segundos en un request HTTP.
2. El patrón es: Start Job -> Return ID -> Client Polls Status.
3. Para implementaciones reales, usa Redis para guardar el estado de 'tasks_db', 
   ya que un diccionario en memoria se borra si reinicias la API.
"""
