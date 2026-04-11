"""
ASYNCIO: TIMEOUTS Y CANCELACIÓN
-----------------------------------------------------------------------------
Cómo evitar que una tarea lenta bloquee recursos eternamente.
"""

import asyncio

async def peticion_lenta():
    try:
        print("[API] Iniciando petición...")
        await asyncio.sleep(10) # Imagina que la API externa no responde
        return "Éxito"
    except asyncio.CancelledError:
        print("[API] ¡Limpieza interna tras cancelación!")
        raise # Es buena práctica re-lanzar la excepción

async def main():
    # 1. ASYNCIO.WAIT_FOR
    # Envuelve una tarea y lanza TimeoutError si supera el tiempo.
    try:
        # Solo le damos 1 segundo a la petición de 10 segundos
        print("intentando petición con timeout de 1s...")
        resultado = await asyncio.wait_for(peticion_lenta(), timeout=1.0)
    except asyncio.TimeoutError:
        print("❌ Error: La petición tardó demasiado")

    # 2. CANCELACIÓN MANUAL (MECANISMO COOPERATIVO)
    # La cancelación en Python no es "matar" el proceso. Es enviarle 
    # una señal al código para que se detenga cuando él quiera.
    tarea = asyncio.create_task(peticion_lenta())
    await asyncio.sleep(0.2)
    tarea.cancel()
    
    # Es obligatorio hacer await de una tarea cancelada para gestionar 
    # su salida o limpiar.
    try:
        await tarea
    except asyncio.CancelledError:
        print("Tarea cancelada y limpia.")

if __name__ == "__main__":
    asyncio.run(main())

"""
RECOMENDACIÓN SENIOR:
---------------------
Nunca hagas una llamada a red sin un timeout. Un servidor externo lento puede 
agotar todos tus workers de backend si no cortas la conexión a tiempo.
"""
