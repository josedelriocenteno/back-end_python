"""
MULTIPROCESSING: INTERCAMBIO DE DATOS (QUEUES Y PIPES)
-----------------------------------------------------------------------------
Como los procesos no comparten memoria, necesitamos canales de 
comunicación seguros para pasar información entre ellos.
"""

import multiprocessing

def consumidor(queue):
    """Recibe datos del proceso principal."""
    while True:
        item = queue.get()
        if item is None: # Señal de parada
            break
        print(f"  [Consumidor] Procesando: {item}")
    print("  [Consumidor] Finalizando...")

if __name__ == "__main__":
    # 1. QUEUE: Es segura para múltiples productores/consumidores.
    # Internamente usa Pipes y Locks para evitar corrupción de datos.
    cola = multiprocessing.Queue()

    p = multiprocessing.Process(target=consumidor, args=(cola,))
    p.start()

    # Enviamos datos
    for i in range(5):
        cola.put(f"Tarea {i}")
    
    # IMPORTANTE: Enviar señal de fin si no queremos que el worker 
    # se quede esperando eternamente.
    cola.put(None)
    
    p.join()

"""
OTRAS FORMAS DE COMPARTIR:
--------------------------
1. Value / Array: Memoria compartida real (C-style). Muy rápida pero 
   peligrosa; requiere manejar Locks manualmente.
2. Manager(): Crea objetos compartidos (listas, dicts) que funcionan 
   en red/procesos. Es más lento pero muy fácil de usar.
3. Pipes: Conexión directa uno-a-uno (bidireccional). Más rápida que 
   las Queues pero menos flexible.
"""

"""
ADVERTENCIA SENIOR:
-------------------
Evita pasar objetos gigantes (como un DataFrame de 2GB) a través de 
Queues/Pipes. Python tiene que serializarlos (pickle) para enviarlos, 
lo que consume mucha CPU y duplica la memoria RAM. En esos casos, es 
mejor leer del disco en cada proceso o usar memoria compartida.
"""
