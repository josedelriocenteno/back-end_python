"""
MULTIPROCESSING: POOLS Y WORKERS
-----------------------------------------------------------------------------
La forma profesional de gestionar múltiples procesos: el Pool.
"""

import multiprocessing
import time

def calcular_cuadrado(n):
    """Tarea intensiva simple."""
    time.sleep(0.5) # Simula carga
    return n * n

if __name__ == "__main__":
    numeros = [1, 2, 3, 4, 5, 6, 7, 8]

    # 1. CREACIÓN DEL POOL
    # Por defecto, selecciona el número de núcleos de tu CPU.
    # Un Pool mantiene los procesos "vivos" y les va enviando tareas, 
    # evitando el coste de crear/destruir procesos constantemente.
    with multiprocessing.Pool(processes=4) as pool:
        
        print("[Pool] Repartiendo tareas entre 4 workers...")
        
        # 2. MAP: Aplica la función a toda la lista en paralelo
        # Es bloqueante hasta que todos terminan.
        resultados = pool.map(calcular_cuadrado, numeros)
        print(f"Resultados (map): {resultados}")

        # 3. APPLY_ASYNC: Lanza una sola tarea y sigue
        # No es bloqueante, devuelve un objeto AsyncResult.
        async_res = pool.apply_async(calcular_cuadrado, (10,))
        print("Esperando a la tarea asíncrona individual...")
        print(f"Resultado (apply_async): {async_res.get()}")

"""
CONSEJO SENIOR:
---------------
Usa siempre el contexto 'with' para asegurar que el Pool se cierra y 
limpia los procesos al terminar. Si no lo haces, podrías dejar procesos 
"zombie" consumiendo memoria en el servidor después de que tu script acabe.
"""

"""
¿CUÁNTOS PROCESSES PONER?
-------------------------
- Tareas CPU-Bound: Pon el número de núcleos físicos de tu CPU (ej: 4 u 8). 
  Poner más solo hará que el SO pierda tiempo intercambiando procesos.
- Tareas mixtas: Puedes probar con Nx2 núcleos, pero vigila la RAM.
"""
