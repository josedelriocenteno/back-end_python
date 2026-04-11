# dict_set_comprehension.py
"""
DICT Y SET COMPREHENSIONS EN PYTHON
===================================

Objetivo:
- Transformar datos de manera eficiente
- Crear diccionarios y sets de manera concisa
- Aplicable a backend, pipelines y preparación de datos
"""

# =========================================================
# 1. Diccionarios por comprensión
# =========================================================

# Crear un diccionario con números y sus cuadrados
cuadrados_dict = {x: x**2 for x in range(5)}
print(cuadrados_dict)  # {0:0, 1:1, 2:4, 3:9, 4:16}

# Filtrar con condición
pares_dict = {x: x**2 for x in range(10) if x % 2 == 0}
print(pares_dict)  # {0:0, 2:4, 4:16, 6:36, 8:64}

# =========================================================
# 2. Sets por comprensión
# =========================================================

numeros = [1, 2, 2, 3, 4, 4, 5]

# Crear un set único de cuadrados
cuadrados_set = {x**2 for x in numeros}
print(cuadrados_set)  # {1, 4, 9, 16, 25}

# =========================================================
# 3. Buenas prácticas
# =========================================================

# - Usar comprensiones para transformar datos de forma limpia y legible
# - Evitar lógica compleja dentro de la comprensión
# - Prefiere diccionarios y sets por comprensión cuando se necesite crear estructuras nuevas a partir de iterables
# - No usar para efectos secundarios

# =========================================================
# 4. Aplicación profesional
# =========================================================

# Backend/data: crear lookup tables, índices, sets de IDs únicos
usuarios = [
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Luis", "edad": 17},
    {"nombre": "Marta", "edad": 30}
]

# Diccionario nombre -> edad solo de mayores de edad
mayores_dict = {u["nombre"]: u["edad"] for u in usuarios if u["edad"] >= 18}
print(mayores_dict)  # {'Ana': 25, 'Marta': 30}

# Set de nombres únicos
nombres_set = {u["nombre"] for u in usuarios}
print(nombres_set)  # {'Ana', 'Luis', 'Marta'}
