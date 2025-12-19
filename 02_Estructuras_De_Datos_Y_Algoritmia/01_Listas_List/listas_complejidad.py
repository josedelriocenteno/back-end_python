# listas_complejidad.py
"""
COMPLEJIDAD DE LISTAS EN PYTHON
==============================

Este archivo explica el COSTE TEMPORAL REAL de las operaciones más comunes
sobre listas en Python, y cómo esto impacta en backend, data y rendimiento.

No memorices Big-O: ENTIÉNDELO.
"""

# ------------------------------------------------------------
# 1. RECORDATORIO: QUÉ ES BIG-O (APLICADO A LISTAS)
# ------------------------------------------------------------

"""
Big-O mide cómo crece el tiempo de ejecución
cuando crece el tamaño de la lista (n).

No mide segundos reales, mide ESCALABILIDAD.
"""

# O(1)    → constante (rápido, estable)
# O(n)    → lineal (crece con el tamaño)
# O(n^2)  → prohibido en producción


# ------------------------------------------------------------
# 2. append() → O(1) AMORTIZADO
# ------------------------------------------------------------

lista = []

for i in range(10000):
    lista.append(i)

"""
append():
- O(1) la mayoría del tiempo
- O(n) solo cuando hay resize interno
- Coste promedio → O(1) amortizado

✔ Operación FAVORITA en backend
"""


# ------------------------------------------------------------
# 3. insert(index, value) → O(n)
# ------------------------------------------------------------

lista = [1, 2, 3, 4, 5]
lista.insert(0, 99)

"""
insert():
- Desplaza elementos a la derecha
- Cuantos más elementos después del índice, más coste

Casos:
- insert(0, x)      → O(n) (el peor)
- insert(len, x)    → similar a append (pero usa append mejor)

❌ Nunca usar insert en bucles grandes
"""


# ------------------------------------------------------------
# 4. pop() → DEPENDE DEL ÍNDICE
# ------------------------------------------------------------

lista = [10, 20, 30, 40]

lista.pop()      # O(1)
lista.pop(0)     # O(n)

"""
pop():
- pop() final → O(1)
- pop(i) intermedio → O(n)

✔ pop() final = stack
❌ pop(0) repetido = desastre de rendimiento
"""


# ------------------------------------------------------------
# 5. remove(value) → O(n)
# ------------------------------------------------------------

lista = [1, 2, 3, 4, 5]
lista.remove(3)

"""
remove():
1. Busca el valor → O(n)
2. Desplaza elementos → O(n)

Coste total → O(n)

❌ remove dentro de bucles grandes
"""


# ------------------------------------------------------------
# 6. acceso por índice → O(1)
# ------------------------------------------------------------

lista = [10, 20, 30, 40]

x = lista[2]   # O(1)
lista[2] = 99  # O(1)

"""
Acceso directo:
- Gracias al array contiguo
- Extremadamente rápido

✔ Ideal para datos indexados
"""


# ------------------------------------------------------------
# 7. búsqueda por valor → O(n)
# ------------------------------------------------------------

lista = [10, 20, 30, 40]

existe = 30 in lista  # O(n)

"""
Búsqueda lineal:
- Recorre uno a uno
- No hay índices internos

✔ Aceptable para listas pequeñas
❌ No usar como lookup table
"""


# ------------------------------------------------------------
# 8. recorrer lista completa → O(n)
# ------------------------------------------------------------

for elemento in lista:
    pass

"""
Recorrer:
- Coste proporcional al tamaño
- Normal y aceptable

Problema real:
- Recorrer listas DENTRO de otros bucles
"""


# ------------------------------------------------------------
# 9. COPIAR LISTAS → O(n)
# ------------------------------------------------------------

a = [1, 2, 3, 4]
b = a.copy()       # O(n)
c = a[:]           # O(n)

"""
Copiar listas cuesta tiempo y memoria.
No copies listas grandes "por si acaso".
"""


# ------------------------------------------------------------
# 10. RESUMEN DE COMPLEJIDADES IMPORTANTES
# ------------------------------------------------------------

"""
OPERACIÓN                 COSTE
------------------------------------
append()                  O(1) amort.
insert(i, x)              O(n)
pop() final               O(1)
pop(i)                    O(n)
remove(x)                 O(n)
acceso por índice         O(1)
búsqueda (x in lista)     O(n)
copiar lista              O(n)
recorrer lista            O(n)
"""


# ------------------------------------------------------------
# 11. ERRORES TÍPICOS DE JUNIOR
# ------------------------------------------------------------

"""
❌ Usar insert(0, x) en bucles
❌ Usar listas como colas
❌ Buscar valores frecuentemente en listas grandes
❌ Copiar listas sin pensar
"""


# ------------------------------------------------------------
# 12. DECISIONES PROFESIONALES
# ------------------------------------------------------------

"""
✔ append + pop() → stack
✔ deque → colas
✔ dict/set → búsquedas rápidas
✔ piensa en Big-O ANTES de escribir el bucle
"""

print("Complejidad de listas dominada")
