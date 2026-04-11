# queue_cola.py
"""
COLAS (QUEUE) EN PYTHON
=======================

Objetivo:
- Implementar cola FIFO usando deque
- Entender operaciones básicas: enqueue, dequeue, peek
- Aplicación en backend, pipelines y buffers
"""

from collections import deque

# ------------------------------------------------------------
# 1. CREACIÓN DE UNA COLA
# ------------------------------------------------------------

cola = deque()  # deque vacío
print("Cola inicial:", cola)

# ------------------------------------------------------------
# 2. OPERACIONES BÁSICAS
# ------------------------------------------------------------

# ENQUEUE: añadir al final
cola.append("tarea1")
cola.append("tarea2")
cola.append("tarea3")
print("Cola después de enqueue:", list(cola))

# DEQUEUE: eliminar desde el inicio
primero = cola.popleft()
print("Elemento removido:", primero)
print("Cola después de dequeue:", list(cola))

# PEEK: ver el primer elemento sin eliminar
primero = cola[0] if cola else None
print("Primer elemento (peek):", primero)


# ------------------------------------------------------------
# 3. COMPROBACIONES
# ------------------------------------------------------------

# Saber si la cola está vacía
if not cola:
    print("Cola vacía")
else:
    print("Cola tiene elementos:", list(cola))


# ------------------------------------------------------------
# 4. USOS COMUNES
# ------------------------------------------------------------

"""
- Tareas en segundo plano / job queues
- Buffers de datos en streaming
- Breadth-first search (BFS)
- Mensajería entre procesos
"""

# Ejemplo rápido: procesar tareas en orden
tareas = deque(["t1", "t2", "t3"])
while tareas:
    tarea = tareas.popleft()
    print("Procesando:", tarea)


# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar lista para queue → pop(0) O(n) lento
❌ No verificar si la cola está vacía antes de popleft()
❌ Confundir FIFO con LIFO
"""

# ✔ Correcto
cola = deque()
if cola:
    cola.popleft()  # seguro

# ❌ Incorrecto
# lista.pop(0)  # lento para colas grandes


# ------------------------------------------------------------
# 6. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Usar deque para colas
✔ Evitar listas si necesitas O(1) en popleft()
✔ Documentar qué contiene cada cola
✔ Iterar sobre copia si vas a modificar mientras procesas
✔ Limitar tamaño de cola si es crítico para memoria
"""

print("Colas con deque dominadas")
