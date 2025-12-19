# listas_errores_comunes.py
"""
ERRORES COMUNES CON LISTAS EN PYTHON
==================================

Estos errores NO suelen lanzar excepciones.
Funcionan “mal en silencio”.
Por eso son tan peligrosos en backend y data.
"""

# ------------------------------------------------------------
# 1. CONFUNDIR COPIA CON REFERENCIA
# ------------------------------------------------------------

a = [1, 2, 3]
b = a

b.append(4)

print("a:", a)
print("b:", b)

"""
❌ ERROR:
Pensar que b es una copia.

✔ REALIDAD:
a y b apuntan a la MISMA lista en memoria.
"""


# ------------------------------------------------------------
# 2. COPIA SUPERFICIAL (SHALLOW COPY)
# ------------------------------------------------------------

a = [1, 2, [3, 4]]
b = a.copy()

b[2].append(5)

print("a:", a)
print("b:", b)

"""
❌ ERROR:
Pensar que copy() copia todo.

✔ REALIDAD:
Solo copia el primer nivel.
Las listas internas siguen compartidas.
"""


# ------------------------------------------------------------
# 3. COPIA PROFUNDA (DEEP COPY)
# ------------------------------------------------------------

import copy

a = [1, 2, [3, 4]]
b = copy.deepcopy(a)

b[2].append(5)

print("a:", a)
print("b:", b)

"""
✔ deepcopy():
- Copia TODO el árbol de objetos
- Más segura
- Más costosa en tiempo y memoria
"""


# ------------------------------------------------------------
# 4. LISTAS ANIDADAS MAL CREADAS
# ------------------------------------------------------------

# ❌ ERROR CLÁSICO
matrix = [[0] * 3] * 3

matrix[0][0] = 1

print(matrix)

"""
Todas las filas apuntan a la MISMA lista.
"""


# ------------------------------------------------------------
# 5. FORMA CORRECTA DE CREAR LISTAS ANIDADAS
# ------------------------------------------------------------

matrix = [[0 for _ in range(3)] for _ in range(3)]
matrix[0][0] = 1

print(matrix)

"""
✔ Cada fila es una lista independiente.
"""


# ------------------------------------------------------------
# 6. MODIFICAR LISTAS MIENTRAS SE ITERA
# ------------------------------------------------------------

nums = [1, 2, 3, 4, 5]

for n in nums:
    if n % 2 == 0:
        nums.remove(n)

print(nums)

"""
❌ ERROR:
Modificar la lista durante la iteración
rompe la lógica.

✔ SOLUCIONES:
- Iterar sobre copia
- Usar comprensión
"""


# ------------------------------------------------------------
# 7. SOLUCIÓN CORRECTA AL PROBLEMA ANTERIOR
# ------------------------------------------------------------

nums = [1, 2, 3, 4, 5]
nums = [n for n in nums if n % 2 != 0]

print(nums)


# ------------------------------------------------------------
# 8. USAR LISTAS COMO DEFAULT ARGUMENT
# ------------------------------------------------------------

def agregar(x, lista=[]):
    lista.append(x)
    return lista

print(agregar(1))
print(agregar(2))

"""
❌ ERROR GRAVE:
El default se evalúa UNA sola vez.

✔ SOLUCIÓN:
Usar None
"""

def agregar(x, lista=None):
    if lista is None:
        lista = []
    lista.append(x)
    return lista

print(agregar(1))
print(agregar(2))


# ------------------------------------------------------------
# 9. COMPARAR LISTAS POR IDENTIDAD
# ------------------------------------------------------------

a = [1, 2]
b = [1, 2]

print(a == b)   # True
print(a is b)   # False

"""
✔ ==  → contenido
❌ is → identidad (misma referencia)
"""


# ------------------------------------------------------------
# 10. COPIAR LISTAS GRANDES SIN NECESIDAD
# ------------------------------------------------------------

"""
❌ Copiar listas grandes “por seguridad”
❌ Pasar listas enormes entre funciones sin pensar

✔ Entender cuándo mutas y cuándo no
✔ Documentar claramente
"""


# ------------------------------------------------------------
# 11. RESUMEN DE ERRORES CRÍTICOS
# ------------------------------------------------------------

"""
❌ Confundir referencia con copia
❌ Copias superficiales mal entendidas
❌ Listas anidadas mal creadas
❌ Mutar mientras iteras
❌ Defaults mutables
❌ Comparar con is
"""

print("Errores comunes con listas dominados")
