"""
MULTITHREADING: LOCKS Y SEMAPHORES
-----------------------------------------------------------------------------
Como los hilos comparten memoria, debemos proteger los datos 
para evitar que dos hilos los modifiquen a la vez.
"""

import threading
import time

# Recurso compartido
contador = 0
# El LOCK (Cero o Uno): Solo un hilo puede tenerlo a la vez.
cerrojo = threading.Lock()

def incrementar():
    global contador
    for _ in range(100000):
        # 1. USO DEL LOCK
        # El bloque 'with' asegura que el lock se libere aunque haya un error.
        with cerrojo:
            contador += 1

if __name__ == "__main__":
    # Lanzamos dos hilos que incrementan el mismo contador
    hilos = []
    for i in range(2):
        t = threading.Thread(target=incrementar)
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    print(f"Resultado final del contador: {contador}")
    # Si quitamos el LOCK, el resultado NO será 200,000 debido 
    # a la interferencia entre hilos.

"""
SEMAPHORE (Contador Granular):
-------------------------------
A diferencia del Lock (que es binario), el Semaphore permite que N 
hilos entren a la vez. Muy útil para limitar el acceso a recursos 
finitos (ej: solo 5 hilos pueden conectarse a la impresora).

sem = threading.Semaphore(5)
with sem:
    hacer_algo()
"""

"""
DEADLOCKS (Bloqueo Mutuo):
--------------------------
Ocurre cuando el Hilo A tiene el Lock 1 y espera el Lock 2, mientras 
el Hilo B tiene el Lock 2 y espera el Lock 1. Ambos se quedan parados 
para siempre. Evita anidar Locks siempre que puedas.
"""
