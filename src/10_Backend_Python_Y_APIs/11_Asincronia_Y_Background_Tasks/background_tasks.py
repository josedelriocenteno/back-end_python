"""
ASINCRONÍA: BACKGROUND TASKS
-----------------------------------------------------------------------------
Cómo ejecutar tareas después de enviar la respuesta al cliente. Ideal para 
enviar emails, limpiar archivos o procesar logs.
"""

from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def write_notification(email: str, message: str):
    """
    Función de ayuda que simula un proceso lento (ej: enviar email).
    """
    with open("log.txt", mode="a") as log:
        # Simulamos que enviar el email tarda 5 segundos
        time.sleep(5) 
        log.write(f"Notificación enviada a {email}: {message}\n")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    """
    El cliente recibe la respuesta 202 INMEDIATAMENTE. 
    La función 'write_notification' se ejecutará después en segundo plano.
    """
    background_tasks.add_task(write_notification, email, message="Bienvenido a la App")
    
    return {"message": "La notificación se enviará en segundo plano"}

"""
CUÁNDO USAR BACKGROUND TASKS vs CELERY:
-----------------------------------------------------------------------------
- BackgroundTasks (FastAPI): 
    * PROS: Muy simple, no requiere infraestructura extra.
    * CONTRAS: Las tareas viven en la memoria de tu API. Si el servidor se apaga, 
      las tareas pendientes se pierden. No sirve para tareas de horas.
      
- Celery / RabbitMQ / Redis:
    * PROS: Persistente, escalable (puedes tener 10 servidores solo para tareas), 
      permite reintentos y programación (cron).
    * CONTRAS: Configuración compleja.
"""

"""
RESUMEN PARA EL DESARROLLADOR:
1. Usa BackgroundTasks para cosas pequeñas que no importa si fallan 
   ocasionalmente (ej: analítica, logs de auditoría).
2. Pasa los argumentos de la función a 'add_task', no llames a la función directamente.
3. Puedes añadir múltiples tareas a un mismo request.
"""
