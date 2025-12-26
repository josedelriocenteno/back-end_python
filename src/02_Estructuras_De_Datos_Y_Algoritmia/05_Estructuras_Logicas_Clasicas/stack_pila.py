# stack_pila.py
"""
PILAS (STACKS) EN PYTHON
========================

Objetivo:
- Implementar una pila usando list
- Entender operaciones básicas: push, pop, peek
- Aplicación en algoritmos y backend
"""

# ------------------------------------------------------------
# 1. CREACIÓN DE UNA PILA
# ------------------------------------------------------------

# Usando lista
stack = []

# ------------------------------------------------------------
# 2. OPERACIONES BÁSICAS
# ------------------------------------------------------------

# PUSH: añadir al final
stack.append("tarea1")
stack.append("tarea2")
stack.append("tarea3")
print("Stack después de push:", stack)

# POP: eliminar último elemento (LIFO)
ultimo = stack.pop()
print("Elemento removido:", ultimo)
print("Stack después de pop:", stack)

# PEEK: ver el último elemento sin eliminar
ultimo = stack[-1] if stack else None
print("Último elemento (peek):", ultimo)


# ------------------------------------------------------------
# 3. COMPROBACIONES
# ------------------------------------------------------------

# Saber si la pila está vacía
if not stack:
    print("Stack vacía")
else:
    print("Stack tiene elementos:", stack)


# ------------------------------------------------------------
# 4. USOS COMUNES
# ------------------------------------------------------------

"""
- Undo/Redo en editores
- Backtracking en algoritmos (DFS)
- Evaluación de expresiones matemáticas
- Parsing de estructuras anidadas (paréntesis, JSON)
"""

# Ejemplo rápido: invertir lista usando stack
lista = [1,2,3,4,5]
stack = []
for elem in lista:
    stack.append(elem)

invertida = [stack.pop() for _ in range(len(stack))]
print("Lista invertida:", invertida)


# ------------------------------------------------------------
# 5. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar pop(0) en lista para stack → O(n) lento
❌ No verificar si la pila está vacía antes de pop
❌ Confundir pila con cola (FIFO)
"""

# ✔ Correcto
stack = []
if stack:
    stack.pop()  # seguro

# ❌ Incorrecto
# stack.pop(0)  # lento, no usar para stack


# ------------------------------------------------------------
# 6. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Usar list.append() y list.pop() para stack
✔ Evitar pop(0) → usar deque si necesitas FIFO
✔ Documentar uso de stack en tu proyecto
✔ Limitar tamaño de stack si es crítico para memoria
"""

print("Pilas con list dominadas")
