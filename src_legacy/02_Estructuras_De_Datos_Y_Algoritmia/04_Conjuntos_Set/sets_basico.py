# sets_basico.py
"""
SETS EN PYTHON — FUNDAMENTOS PROFESIONALES
==========================================

Objetivo:
- Crear sets
- Operar sobre ellos
- Entender sus métodos y características
- Uso frecuente en backend y data pipelines
"""

# ------------------------------------------------------------
# 1. CREACIÓN DE SETS
# ------------------------------------------------------------

# Set vacío
s = set()
print(s)  # set()

# Set con elementos
frutas = {"manzana", "naranja", "pera"}
print(frutas)

# Desde lista (elimina duplicados)
nums = [1,2,2,3,3,3]
nums_set = set(nums)
print(nums_set)  # {1,2,3}

# ❌ No usar {} para vacío → crea dict
vacio = {}
print(type(vacio))  # dict


# ------------------------------------------------------------
# 2. OPERACIONES BÁSICAS
# ------------------------------------------------------------

s.add("plátano")        # añadir
s.remove("pera")        # eliminar, KeyError si no existe
s.discard("kiwi")       # eliminar seguro, no falla si no existe
print(s)

# Comprobar existencia
print("manzana" in s)    # True
print("pera" in s)       # False


# ------------------------------------------------------------
# 3. MÉTODOS IMPORTANTES
# ------------------------------------------------------------

print(len(s))            # tamaño
print(s.pop())           # elimina y devuelve un elemento arbitrario
s.clear()                # elimina todo
print(s)


# ------------------------------------------------------------
# 4. OPERACIONES CONJUNTAS
# ------------------------------------------------------------

a = {1,2,3,4}
b = {3,4,5,6}

print(a | b)   # unión {1,2,3,4,5,6}
print(a & b)   # intersección {3,4}
print(a - b)   # diferencia {1,2}
print(a ^ b)   # diferencia simétrica {1,2,5,6}


# ------------------------------------------------------------
# 5. ITERACIÓN
# ------------------------------------------------------------

for elem in a:
    print(elem)


# ------------------------------------------------------------
# 6. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar listas como elementos → TypeError
❌ Depender del orden (sets no son ordenados)
❌ Convertir repetidamente entre list/set sin necesidad
"""

# ❌ lista como elemento
# s = {[1,2], [3,4]}  # TypeError

# ✔ tuple como elemento
s = {(1,2), (3,4)}
print(s)


# ------------------------------------------------------------
# 7. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Usar sets para membership test rápido O(1)
✔ Evitar modificar mientras iteras
✔ Prefiere operaciones conjuntas sobre loops manuales
✔ Elimina duplicados con set()
✔ Documenta qué contiene cada set
"""

print("Sets básicos dominados")
