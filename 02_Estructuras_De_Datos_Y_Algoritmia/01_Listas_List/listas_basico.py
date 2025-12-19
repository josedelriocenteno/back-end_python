# listas_basico.py
"""
LISTAS EN PYTHON — FUNDAMENTOS PROFESIONALES
===========================================

Las listas son:
- Mutables
- Ordenadas
- Indexadas
- Dinámicas

Son la estructura MÁS usada en Python backend.
Si no dominas esto, todo lo demás se te cae.
"""

# ------------------------------------------------------------
# 1. CREACIÓN DE LISTAS
# ------------------------------------------------------------

# Lista vacía
lista_vacia = []

# Lista con elementos
numeros = [1, 2, 3, 4, 5]

# Lista heterogénea (permitido, pero ojo en backend)
mixta = [1, "hola", True, 3.14]

# Lista desde iterable
desde_rango = list(range(5))  # [0, 1, 2, 3, 4]

print(lista_vacia, numeros, mixta, desde_rango)


# ------------------------------------------------------------
# 2. ACCESO A ELEMENTOS (INDEXACIÓN)
# ------------------------------------------------------------

datos = ["a", "b", "c", "d"]

print(datos[0])   # primer elemento
print(datos[2])   # tercer elemento
print(datos[-1])  # último elemento
print(datos[-2])  # penúltimo

"""
Regla:
- Índices empiezan en 0
- Índices negativos recorren desde el final
"""


# ------------------------------------------------------------
# 3. MODIFICACIÓN DE ELEMENTOS (MUTABILIDAD)
# ------------------------------------------------------------

datos[1] = "B"
print(datos)  # ['a', 'B', 'c', 'd']

"""
Esto NO crea una lista nueva.
Modifica la existente.
"""


# ------------------------------------------------------------
# 4. SLICING (SUBLISTAS)
# ------------------------------------------------------------

numeros = [0, 1, 2, 3, 4, 5]

print(numeros[1:4])   # [1, 2, 3]
print(numeros[:3])    # [0, 1, 2]
print(numeros[3:])    # [3, 4, 5]
print(numeros[:])     # copia superficial
print(numeros[::2])   # salto de 2
print(numeros[::-1])  # lista invertida

"""
Slicing:
- NO incluye el índice final
- Devuelve una NUEVA lista (shallow copy)
"""


# ------------------------------------------------------------
# 5. MÉTODOS PRINCIPALES DE LISTAS
# ------------------------------------------------------------

items = [1, 2, 3]

# Añadir elementos
items.append(4)          # al final
items.extend([5, 6])     # varios
items.insert(0, 0)       # posición específica

print(items)

# Eliminar elementos
items.remove(3)          # por valor
ultimo = items.pop()     # último
segundo = items.pop(1)   # por índice

print(items)
print("pop:", ultimo, segundo)

# Otros métodos útiles
print(items.index(2))    # índice del valor
print(items.count(2))    # cuántas veces aparece
items.reverse()          # invierte in-place
items.sort()             # ordena in-place

print(items)


# ------------------------------------------------------------
# 6. LISTAS Y BUCLES (PATRÓN BÁSICO BACKEND)
# ------------------------------------------------------------

usuarios = ["ana", "luis", "maria"]

for usuario in usuarios:
    print("Usuario:", usuario)

"""
NO modifiques una lista mientras la recorres.
Es un error clásico.
"""


# ------------------------------------------------------------
# 7. COPIAS DE LISTAS (ERROR FRECUENTE)
# ------------------------------------------------------------

a = [1, 2, 3]
b = a          # MISMA referencia
c = a.copy()   # copia superficial

a.append(4)

print(a)  # [1, 2, 3, 4]
print(b)  # [1, 2, 3, 4] ❌
print(c)  # [1, 2, 3]    ✅


# ------------------------------------------------------------
# 8. COMPROBACIONES COMUNES
# ------------------------------------------------------------

print(2 in a)        # True
print(99 in a)       # False
print(len(a))        # tamaño de la lista


# ------------------------------------------------------------
# 9. LISTAS COMO ACUMULADORES (MUY COMÚN)
# ------------------------------------------------------------

resultado = []

for i in range(5):
    resultado.append(i * 2)

print(resultado)  # [0, 2, 4, 6, 8]


# ------------------------------------------------------------
# 10. MALAS PRÁCTICAS A EVITAR
# ------------------------------------------------------------

"""
❌ Usar listas gigantes sin pensar en coste
❌ Mezclar tipos sin necesidad
❌ Copiar referencias creyendo que copias valores
❌ Mutar listas compartidas sin documentarlo
"""


# ------------------------------------------------------------
# 11. CUÁNDO USAR LISTAS
# ------------------------------------------------------------

"""
Usa list cuando:
- Necesitas orden
- Necesitas mutabilidad
- Acceso por índice
- Iteración frecuente
"""

print("Listas dominadas a nivel básico")
