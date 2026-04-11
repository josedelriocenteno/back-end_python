"""
ASYNCIO: EL EVENT LOOP (EL MOTOR)
-----------------------------------------------------------------------------
El Event Loop es el corazón de la asincronía. Es un bucle infinito que 
gestiona qué tarea se ejecuta en cada momento.
"""

import asyncio
import time

async def tarea_rapida(id):
    print(f"  [Task {id}] Empezando...")
    # 'await' le devuelve el control al Event Loop diciendo: 
    # "Me voy a esperar, usa la CPU para otra cosa mientras tanto".
    await asyncio.sleep(0.5) 
    print(f"  [Task {id}] ¡Terminada!")

async def main():
    print("[Main] Arrancando el motor...")
    start_time = time.perf_counter()

    # Ejecutamos 3 tareas de forma concurrente
    # gather() las mete todas en el Event Loop y espera a que terminen.
    await asyncio.gather(
        tarea_rapida(1),
        tarea_rapida(2),
        tarea_rapida(3)
    )

    end_time = time.perf_counter()
    # Aunque cada tarea dura 0.5s, las 3 juntas duran lo mismo (~0.5s)
    print(f"[Main] Todo terminado en {end_time - start_time:.2f} segundos")

if __name__ == "__main__":
    # asyncio.run() crea el Event Loop, corre la función y lo cierra al final.
    asyncio.run(main())

"""
¿QUÉ PASA POR DENTRO? (Explicación Senior)
------------------------------------------
1. main() se registra en el Event Loop.
2. gather() registra 3 corrutinas de 'tarea_rapida'.
3. El Loop ejecuta la 1, llega al 'await asyncio.sleep'. La 1 se pausa.
4. El Loop dice "¿Hay alguien más listo?". Sí, la 2. La ejecuta. Se pausa.
5. Ejecuta la 3. Se pausa.
6. El Loop se queda esperando ("Polling") hasta que el temporizador de 
   alguna de las tareas venza.
7. En cuanto pasa el tiempo, el Loop despierta a las tareas y termina su ejecución.
"""

"""
REGLA DE ORO:
-------------
Si metes un código que BLOQUEE el hilo (ej: un loop infinito o un cálculo 
pesado sin await), el Event Loop SE DETIENE. Ninguna otra tarea avanzará. 
Es como si el semáforo se quedara en rojo para siempre.
"""
