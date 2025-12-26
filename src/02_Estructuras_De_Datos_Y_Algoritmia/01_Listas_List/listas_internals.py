# listas_internals.py
"""
LISTAS EN PYTHON — FUNCIONAMIENTO INTERNO (ARRAY DINÁMICO)
==========================================================

Python implementa las listas como ARRAYS DINÁMICOS.
No son listas enlazadas.

Entender esto explica:
- Por qué append() es rápido
- Por qué insert() es caro
- Por qué las listas crecen "a saltos"
- Por qué a veces gastan más memoria de la esperada
"""

# ------------------------------------------------------------
# 1. QUÉ ES UN ARRAY DINÁMICO
# ------------------------------------------------------------

"""
Un array dinámico es:
- Un bloque contiguo de memoria
- Capaz de crecer automáticamente
- Redimensionado cuando se queda sin espacio

Python reserva MÁS memoria de la necesaria
para evitar realocar en cada append().
"""


# ------------------------------------------------------------
# 2. CAPACIDAD VS TAMAÑO
# ------------------------------------------------------------

"""
Conceptos clave:

- size (len(lista)): elementos reales
- capacity: espacio reservado en memoria

capacity >= size SIEMPRE
"""

import sys

lista = []
print("Size | Memoria")
for i in range(20):
    lista.append(i)
    print(len(lista), sys.getsizeof(lista))


# ------------------------------------------------------------
# 3. POR QUÉ append() ES O(1) AMORTIZADO
# ------------------------------------------------------------

"""
append():
- Si hay espacio → escribe y listo (O(1))
- Si NO hay espacio → crea un array nuevo más grande
  - Copia todos los elementos
  - Libera el anterior

Esto es caro, pero ocurre pocas veces.
Por eso se dice O(1) amortizado.
"""

datos = []
for i in range(1000):
    datos.append(i)


# ------------------------------------------------------------
# 4. QUÉ PASA CUANDO SE REDIMENSIONA
# ------------------------------------------------------------

"""
Redimensionar implica:
1. Reservar memoria nueva (más grande)
2. Copiar todos los punteros
3. Liberar el bloque anterior

Costo real: O(n)
"""


# ------------------------------------------------------------
# 5. POR QUÉ insert() ES O(n)
# ------------------------------------------------------------

numeros = [1, 2, 3, 4, 5]
numeros.insert(0, 99)

"""
insert(pos, valor):
- Desplaza TODOS los elementos a la derecha
- Cuanto más al inicio, más caro

Nunca usar insert() en bucles grandes.
"""


# ------------------------------------------------------------
# 6. remove() y pop() — DIFERENCIAS IMPORTANTES
# ------------------------------------------------------------

"""
remove(valor):
- Busca el valor → O(n)
- Desplaza elementos → O(n)

pop():
- pop() final → O(1)
- pop(indice) → O(n)
"""

a = [1, 2, 3, 4]
a.pop()       # rápido
a.pop(0)      # caro


# ------------------------------------------------------------
# 7. LISTAS NO GUARDAN VALORES, GUARDAN REFERENCIAS
# ------------------------------------------------------------

"""
La lista almacena punteros a objetos,
NO los objetos directamente.
"""

x = [1, 2, 3]
y = x

x.append(4)

print(x)  # [1, 2, 3, 4]
print(y)  # [1, 2, 3, 4] MISMA referencia


# ------------------------------------------------------------
# 8. COSTE DE MEMORIA REAL
# ------------------------------------------------------------

"""
Una lista con 1 millón de enteros:
- No ocupa solo 1 millón * 4 bytes
- Cada int es un objeto (~28 bytes)

Esto importa en:
- Data Engineering
- Procesamiento masivo
"""

grande = list(range(10**5))
print(sys.getsizeof(grande))


# ------------------------------------------------------------
# 9. COMPARACIÓN CON OTRAS ESTRUCTURAS
# ------------------------------------------------------------

"""
Lista:
- Acceso por índice: O(1)
- append final: O(1) amortizado
- insert/delete medio: O(n)

Deque:
- append/pop ambos lados: O(1)
- acceso por índice: O(n)

Linked list (NO usada en Python estándar):
- insert rápido
- acceso lento
"""


# ------------------------------------------------------------
# 10. CUÁNDO LAS LISTAS SON MALA IDEA
# ------------------------------------------------------------

"""
❌ Inserciones frecuentes al inicio
❌ Eliminaciones en medio a gran escala
❌ Procesamiento de millones de elementos sin pensar en memoria
"""


# ------------------------------------------------------------
# 11. REGLAS DE ORO BACKEND
# ------------------------------------------------------------

"""
✔ append siempre que puedas
✔ evita insert en bucles
✔ usa deque para colas
✔ entiende que copiar listas cuesta O(n)
"""

print("Internals de listas dominados")
