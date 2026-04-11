"""
MULTIPROCESSING: BASES Y PROCESOS
-----------------------------------------------------------------------------
Cómo crear procesos reales del SO para paralelismo verdadero en Python.
"""

import multiprocessing
import os
import time

def tarea_pesada(nombre):
    """Función que corre en un proceso separado."""
    print(f"  [Proceso {os.getpid()}] Iniciando tarea: {nombre}")
    # Simulamos un cálculo intensivo
    resultado = 0
    for i in range(10**7):
        resultado += i
    print(f"  [Proceso {os.getpid()}] Tarea {nombre} finalizada.")

if __name__ == "__main__":
    # IMPORTANTE: En Windows/macOS el bloque 'if __name__ == "__main__":' 
    # es OBLIGATORIO para evitar bucles infinitos de creación de procesos.
    
    print(f"[Main {os.getpid()}] Arrancando procesos...")

    # 1. CREACIÓN DE PROCESOS
    p1 = multiprocessing.Process(target=tarea_pesada, args=("Alpha",))
    p2 = multiprocessing.Process(target=tarea_pesada, args=("Beta",))

    # 2. ARRANQUE (No bloqueante)
    p1.start()
    p2.start()

    print(f"[Main] Los procesos están corriendo de fondo...")

    # 3. UNIÓN (Bloqueante)
    # join() espera a que el proceso termine antes de seguir.
    p1.join()
    p2.join()

    print(f"[Main] Todos los procesos han terminado.")

"""
¿POR QUÉ USAR PROCESOS? (Explicación Senior)
--------------------------------------------
A diferencia de los hilos (threads), cada proceso de 'multiprocessing':
1. Tiene su propia instancia del intérprete de Python.
2. Tiene su propio espacio de memoria (no comparten variables!).
3. Tiene su propio GIL.
Esto permite que Python use el 100% de varios núcleos de la CPU 
simultáneamente para tareas de cálculo intenso.
"""

"""
EL COSTE DEL PROCESO:
---------------------
Crear un proceso es "caro" en términos de RAM y tiempo del SO. No uses 
esto para tareas de microsegundos; úsalo para tareas que duren al menos 
unos cientos de milisegundos.
"""
