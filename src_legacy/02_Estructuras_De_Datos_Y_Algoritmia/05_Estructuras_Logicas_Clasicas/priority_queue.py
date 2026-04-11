# priority_queue.py
"""
COLAS DE PRIORIDAD EN PYTHON — heapq
====================================

Objetivo:
- Implementar colas de prioridad con heapq
- Entender operaciones push/pop eficientes
- Aplicación en backend, algoritmos y pipelines
"""

import heapq

# ------------------------------------------------------------
# 1. CREACIÓN DE UNA COLA DE PRIORIDAD
# ------------------------------------------------------------

pq = []  # lista vacía que actuará como heap
print("Priority queue inicial:", pq)

# ------------------------------------------------------------
# 2. OPERACIONES BÁSICAS
# ------------------------------------------------------------

# HEAP PUSH: añadir elementos (prioridad implícita por primer valor)
heapq.heappush(pq, (2, "tarea_media"))
heapq.heappush(pq, (1, "tarea_alta"))
heapq.heappush(pq, (3, "tarea_baja"))
print("Priority queue después de heappush:", pq)

# HEAP POP: extrae el elemento con menor valor de prioridad
prioridad, tarea = heapq.heappop(pq)
print("Elemento removido:", (prioridad, tarea))
print("Priority queue actual:", pq)

# HEAP PEEK: ver el elemento con menor prioridad sin remover
if pq:
    print("Primer elemento (peek):", pq[0])


# ------------------------------------------------------------
# 3. USOS COMUNES
# ------------------------------------------------------------

"""
- Scheduler de tareas en backend
- Procesamiento de jobs con prioridad
- Algoritmos: Dijkstra, A*, Huffman
- Buffers ordenados por coste o tiempo
"""

# Ejemplo: procesamiento ordenado de jobs
jobs = [(5, "job5"), (1, "job1"), (3, "job3")]
heapq.heapify(jobs)  # convierte lista en heap en O(n)
while jobs:
    prioridad, job = heapq.heappop(jobs)
    print(f"Procesando {job} con prioridad {prioridad}")


# ------------------------------------------------------------
# 4. ACTUALIZACIÓN DE PRIORIDADES
# ------------------------------------------------------------

"""
heapq no tiene decrease-key directo.
Se puede:
✔ añadir nuevo elemento con menor valor y marcar antiguo como inválido
✔ usar heapq + diccionario para seguimiento
"""

# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar lista simple y ordenar manualmente cada vez → O(n log n) repetido
❌ No usar tupla (prioridad, elemento) → ambiguo si elementos comparables
❌ Modificar heap directamente sin heapify → rompe propiedad de heap
"""

# ✔ Correcto
pq = []
heapq.heappush(pq, (2, "tarea_media"))
heapq.heappush(pq, (1, "tarea_alta"))
heapq.heappush(pq, (3, "tarea_baja"))


# ------------------------------------------------------------
# 6. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Siempre usar tuplas (prioridad, elemento)
✔ Usar heapify para inicializar heaps grandes
✔ Evitar modificar heap directamente
✔ Documentar claramente la prioridad de cada elemento
✔ Combinar heapq con diccionario si necesitas actualización eficiente
"""

print("Cola de prioridad con heapq dominada profesionalmente")
