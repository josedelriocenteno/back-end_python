"""
MULTITHREADING: BASES Y HILOS
-----------------------------------------------------------------------------
Cómo usar hilos para tareas de I/O que no soportan asincronía nativa.
"""

import threading
import time

def tarea_io(nombre, segundos):
    """Simula una tarea de espera (ej: consulta a una API vieja)."""
    print(f"  [Thread {threading.current_thread().name}] Iniciando {nombre}...")
    time.sleep(segundos)
    print(f"  [Thread {threading.current_thread().name}] {nombre} finalizada.")

if __name__ == "__main__":
    print("[Main] Arrancando hilos...")

    # 1. CREACIÓN DE HILOS
    # Los hilos comparten la MISMA memoria que el proceso principal.
    t1 = threading.Thread(target=tarea_io, args=("Petición A", 2), name="Worker-A")
    t2 = threading.Thread(target=tarea_io, args=("Petición B", 1), name="Worker-B")

    # 2. ARRANQUE
    t1.start()
    t2.start()

    print("[Main] Hilos lanzados, haciendo otras cosas...")

    # 3. UNIÓN
    t1.join()
    t2.join()

    print("[Main] Todos los hilos terminados.")

"""
¿CUÁNDO USAR THREADING FRENTE A ASYNCIO?
-----------------------------------------
- Asyncio: Cuando tienes miles de conexiones ultra-rápidas y la librería 
  es asíncrona (ej: httpx, asyncpg). Es mucho más eficiente en memoria.
- Threading: Cuando tienes pocas tareas lentas y la librería es síncrona 
  (ej: requests, librerías de conexión industrial, wrappers antiguos de C).
"""

"""
HILOS DAEMON (DAEMON THREADS):
------------------------------
Si marcas un hilo como 'daemon=True', el hilo morirá automáticamente 
en cuanto el programa principal termine, sin esperar su ejecución. Útil 
para tareas de monitorización de fondo que no importan si mueren.
"""
