"""
ASYNCIO: COLAS DE TAREAS (QUEUES)
-----------------------------------------------------------------------------
Cómo implementar un sistema de colas en memoria para procesar trabajos 
de forma ordenada y controlada.
"""

import asyncio
import random

async def productor(cola, id):
    """Genera trabajos y los mete en la cola."""
    for i in range(3):
        item = f"Job-{id}-{i}"
        await asyncio.sleep(random.uniform(0.1, 0.4))
        await cola.put(item)
        print(f"[Productor {id}] Enecoló: {item}")

async def consumidor(cola, id):
    """Extrae trabajos de la cola y los procesa."""
    while True:
        # Esperamos a que haya algo en la cola
        item = await cola.get()
        
        # Procesamos el ítem
        await asyncio.sleep(random.uniform(0.5, 1.0))
        print(f"  [Consumidor {id}] ✅ PROCESADO: {item}")
        
        # Le decimos a la cola que el trabajo está hecho
        cola.task_done()

async def main():
    cola = asyncio.Queue(maxsize=10)

    # 1. LANZAMOS CONSUMIDORES (Workers)
    # Se quedan esperando en bucle infinito
    consumidores = [
        asyncio.create_task(consumidor(cola, i)) for i in range(2)
    ]

    # 2. LANZAMOS PRODUCTORES
    await asyncio.gather(
        productor(cola, "A"),
        productor(cola, "B")
    )

    # 3. ESPERAR A QUE LA COLA SE VACÍE
    # join() espera a que haya tantos task_done() como put()
    await cola.join()

    # 4. LIMPIEZA: Cancelamos los consumidores que se quedaron en el get()
    for c in consumidores:
        c.cancel()

    print("\n[Main] Todos los trabajos terminados satisfactoriamente.")

if __name__ == "__main__":
    asyncio.run(main())

"""
POR QUÉ USAR COLAS EN LUGAR DE GATHER():
-----------------------------------------
Si tienes 10.000 fotos para procesar, 'gather' intentará procesar las 
10.000 a la vez, agotando la RAM. Con una 'Queue' y 10 workers, solo se 
procesarán 10 fotos simultáneamente, manteniendo la RAM estable y el 
sistema bajo control.
"""
