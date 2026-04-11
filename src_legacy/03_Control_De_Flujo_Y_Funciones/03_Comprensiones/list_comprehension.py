# list_comprehension.py
"""
LIST COMPREHENSIONS EN PYTHON
=============================

Objetivo:
- Aprender a crear listas de manera concisa y eficiente
- Evitar abusos que dañen legibilidad
- Aplicable a backend, pipelines y procesamiento de datos
"""

# =========================================================
# 1. Sintaxis básica
# =========================================================

# Crear una lista de cuadrados
cuadrados = [x**2 for x in range(5)]
print(cuadrados)  # [0, 1, 4, 9, 16]

# =========================================================
# 2. Con condición (if)
# =========================================================

# Filtrar solo números pares
numeros = range(10)
pares = [x for x in numeros if x % 2 == 0]
print(pares)  # [0, 2, 4, 6, 8]

# =========================================================
# 3. Con if-else (condicionales dentro de la comprensión)
# =========================================================

# Marcar como par o impar
paridad = ["par" if x % 2 == 0 else "impar" for x in numeros]
print(paridad)

# =========================================================
# 4. Comprehension anidada
# =========================================================

# Matriz 3x3
matriz = [[i*j for j in range(3)] for i in range(3)]
print(matriz)  # [[0,0,0],[0,1,2],[0,2,4]]

# =========================================================
# 5. Buenas prácticas
# =========================================================

# - Mantener comprensiones legibles; si se vuelve compleja, usar bucles
# - Evitar múltiples niveles anidados en producción
# - Ideal para transformaciones de listas, filtrado y mapeo
# - No usar para efectos secundarios (print, append externo, logging)

# =========================================================
# 6. Aplicación profesional
# =========================================================

# Backend/data: transformar datos, limpiar listas, preparar batches
usuarios = [
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Luis", "edad": 17},
    {"nombre": "Marta", "edad": 30}
]

# Nombres de mayores de edad
mayores = [u["nombre"] for u in usuarios if u["edad"] >= 18]
print(mayores)  # ['Ana', 'Marta']
