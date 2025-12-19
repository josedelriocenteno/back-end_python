# deque_explicacion.py
"""
COLLECTIONS.DEQUE EN PYTHON — USO PROFESIONAL
=============================================

Objetivo:
- Entender qué es deque y por qué es más eficiente que listas para colas/pilas
- Operaciones básicas y avanzadas
- Casos de uso en backend, pipelines y algoritmos
"""

from collections import deque

# ------------------------------------------------------------
# 1. CREACIÓN DE DEQUE
# ------------------------------------------------------------

d = deque()  # vacío
d2 = deque([1,2,3])
print("Deque inicial:", d2)


# ------------------------------------------------------------
# 2. OPERACIONES BÁSICAS
# ------------------------------------------------------------

# Añadir elementos
d2.append(4)        # añadir al final
d2.appendleft(0)    # añadir al inicio
print("Después de append y appendleft:", d2)

# Eliminar elementos
ultimo = d2.pop()       # elimina final
primero = d2.popleft()  # elimina inicio
print("Después de pop y popleft:", d2)
print("Elemento final:", ultimo, "Elemento inicial:", primero)

# Acceso a elementos
print("Primer elemento:", d2[0])
print("Último elemento:", d2[-1])


# ------------------------------------------------------------
# 3. OTROS MÉTODOS ÚTILES
# ------------------------------------------------------------

d2.extend([5,6,7])         # añadir varios al final
d2.extendleft([-2,-1])     # añadir varios al inicio (orden inverso)
print("Después de extend y extendleft:", d2)

d2.rotate(2)   # rota a la derecha 2 posiciones
print("Después de rotate(2):", d2)
d2.rotate(-3)  # rota a la izquierda 3 posiciones
print("Después de rotate(-3):", d2)

d2.clear()     # vaciar deque
print("Después de clear():", d2)


# ------------------------------------------------------------
# 4. CUÁNDO USAR DEQUE PROFESIONALMENTE
# ------------------------------------------------------------

"""
✔ FIFO: colas de tareas, buffers, job queues
✔ LIFO: pilas con append/pop
✔ Rotación: scheduling, round-robin
✔ Extensiones rápidas a ambos lados
✔ Evitar listas cuando pop(0) sería O(n)
"""

# Ejemplo: buffer circular
buffer = deque(maxlen=5)  # tamaño limitado, elimina más antiguo automáticamente
for i in range(10):
    buffer.append(i)
    print("Buffer actual:", list(buffer))


# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar lista para pop(0) → O(n) lento
❌ No usar maxlen si necesitas buffer limitado
❌ Confundir appendleft y extendleft (orden inverso)
❌ Modificar deque mientras iteras
"""


# ------------------------------------------------------------
# 6. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Usar deque para colas/pilas grandes
✔ Usar maxlen para buffers circulares
✔ Documentar qué representa cada deque
✔ Prefiere métodos internos para eficiencia
✔ Evitar modificar mientras iteras
"""

print("collections.deque dominado profesionalmente")
