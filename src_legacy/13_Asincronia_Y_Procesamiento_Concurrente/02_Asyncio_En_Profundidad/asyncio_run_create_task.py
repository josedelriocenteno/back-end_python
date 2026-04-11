"""
ASYNCIO: GESTIÓN AVANZADA DE TAREAS
-----------------------------------------------------------------------------
Cómo crear tareas, obtener sus resultados y gestionar su ciclo de vida.
"""

import asyncio

async def tarea_con_resultado(n):
    await asyncio.sleep(n)
    return f"Resultado de {n}"

async def main():
    # 1. CREAR TAREA
    # Inmediatamente se pone en cola para ejecutarse.
    task1 = asyncio.create_task(tarea_con_resultado(1))
    task2 = asyncio.create_task(tarea_con_resultado(2))

    print("Haciendo otras cosas mientras las tareas corren...")
    await asyncio.sleep(0.1)

    # 2. ESPERAR RESULTADOS
    # Si la tarea ya terminó, 'await' devuelve el valor al instante.
    res1 = await task1
    res2 = await task2
    print(f"Finalizado: {res1}, {res2}")

    # 3. CANCELACIÓN
    task3 = asyncio.create_task(asyncio.sleep(10))
    await asyncio.sleep(0.5)
    print("Tarea 3 tarda mucho, la cancelamos...")
    task3.cancel()

    try:
        await task3
    except asyncio.CancelledError:
        print("✅ Tarea 3 cancelada correctamente")

if __name__ == "__main__":
    asyncio.run(main())

"""
CONSEJO SENIOR:
---------------
A partir de Python 3.11+, usa 'asyncio.TaskGroup()' para gestionar grupos 
de tareas. Es mucho más seguro (si una falla, cancela todas las demás 
automáticamente, evitando tareas huérfanas).
"""
