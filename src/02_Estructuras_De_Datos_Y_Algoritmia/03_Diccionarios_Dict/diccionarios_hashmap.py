# diccionarios_hashmap.py
"""
DICCIONARIOS COMO HASH MAPS EN PYTHON
====================================

Los diccionarios en Python son implementaciones de hash map.
Esto explica:
✔ Acceso rápido O(1) promedio
✔ Por qué las claves deben ser inmutables y hashables
✔ Comportamientos sutiles al colisionar o redimensionar
"""

# ------------------------------------------------------------
# 1. CONCEPTO DE HASH MAP
# ------------------------------------------------------------

"""
Un hash map:
- Asocia clave → valor
- Calcula hash(clave) → índice en tabla
- Maneja colisiones con técnicas internas (open addressing)
- Permite acceso rápido sin recorrer todos los elementos
"""

# ------------------------------------------------------------
# 2. HASH EN PYTHON
# ------------------------------------------------------------

clave1 = (1, 2)
clave2 = (2, 1)

print("hash(clave1):", hash(clave1))
print("hash(clave2):", hash(clave2))

# Claves mutables ❌
# hash([1,2])  # TypeError


# ------------------------------------------------------------
# 3. ACCESO O(1) PROMEDIO
# ------------------------------------------------------------

d = {"a": 1, "b": 2, "c": 3}

# Acceso directo
print(d["b"])  # O(1)

# Insertar
d["d"] = 4     # O(1) promedio

# Delete
del d["a"]     # O(1) promedio


# ------------------------------------------------------------
# 4. COLISIONES
# ------------------------------------------------------------

"""
Python maneja colisiones internamente.
- Dos claves diferentes pueden tener el mismo hash
- Python usa probing interno para resolverlo
- Para el usuario, esto es transparente
"""


# ------------------------------------------------------------
# 5. REDIMENSIONAMIENTO AUTOMÁTICO
# ------------------------------------------------------------

"""
- Los dicts crecen dinámicamente
- Cuando se alcanza cierto load factor
- Python redistribuye elementos
- Operación costosa, pero rara
"""


# ------------------------------------------------------------
# 6. USO EFICIENTE DE DICCIONARIOS
# ------------------------------------------------------------

# Evitar recalcular hashes innecesarios
# Usar claves simples y hashables
# Evitar mutar elementos dentro de tuplas que sean claves

cache = {}
for i in range(1000):
    key = (i, i+1)
    cache[key] = i*i


# ------------------------------------------------------------
# 7. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Claves mutables → TypeError
❌ Depender de orden de diccionario (antes de Python 3.7)
❌ Modificar diccionario mientras iteras
❌ Insertar claves que se parezcan a otras sin control
"""

# Ejemplo: clave mutable ❌
# d[[1,2]] = "valor"  # TypeError


# ------------------------------------------------------------
# 8. DICCIONARIOS ANIDADOS Y HASH MAPS
# ------------------------------------------------------------

usuarios = {
    "user_1": {"nombre": "Juan", "edad": 30},
    "user_2": {"nombre": "Ana", "edad": 25},
}

# Acceso rápido O(1)
print(usuarios["user_2"]["nombre"])


# ------------------------------------------------------------
# 9. CONSEJOS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Prefiere tuplas inmutables como claves compuestas
✔ Documenta qué representa cada clave
✔ Usa diccionarios para lookups frecuentes
✔ Evita modificaciones de claves después de insertarlas
✔ Entiende que dicts son hash map subyacentes → diseño consciente
"""

print("Diccionarios como hash map dominados")
