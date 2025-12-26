# enumerate_zip_range.py
"""
ITERACIÓN PROFESIONAL CON ENUMERATE, ZIP Y RANGE
================================================

Objetivo:
- Iterar sobre listas y otras estructuras de manera profesional
- Usar enumerate para índices, zip para combinar colecciones, range para secuencias
- Aplicable a backend, pipelines de datos y procesamiento eficiente
"""

# =========================================================
# 1. Enumerate
# =========================================================

usuarios = ["Ana", "Luis", "Marta"]

# Obtener índice y valor
for i, nombre in enumerate(usuarios):
    print(f"Índice {i}: {nombre}")

# Empezar desde un índice distinto
for i, nombre in enumerate(usuarios, start=1):
    print(f"Usuario {i}: {nombre}")

# =========================================================
# 2. ZIP
# =========================================================

edades = [25, 17, 30]

# Iterar simultáneamente sobre dos listas
for nombre, edad in zip(usuarios, edades):
    print(f"{nombre} tiene {edad} años")

# Con más de dos listas
ciudades = ["Madrid", "Barcelona", "Valencia"]
for nombre, edad, ciudad in zip(usuarios, edades, ciudades):
    print(f"{nombre}, {edad} años, vive en {ciudad}")

# =========================================================
# 3. RANGE
# =========================================================

# Iterar sobre índices
for i in range(len(usuarios)):
    print(f"{i}: {usuarios[i]}")

# Secuencia con pasos
for n in range(0, 10, 2):
    print(f"Número par: {n}")

# =========================================================
# 4. Buenas prácticas
# =========================================================

# - Usar enumerate en lugar de range(len(lista)) cuando necesites índices
# - Usar zip para combinar colecciones relacionadas, evita anidamientos
# - Usar range para secuencias de números, con start, stop y step
# - Mantener el bucle limpio y legible

# =========================================================
# 5. Aplicación profesional
# =========================================================

# Backend/data pipelines: recorrer datos de registros, combinar atributos de varias fuentes
usuarios_data = [
    {"nombre": "Ana", "edad": 25, "ciudad": "Madrid"},
    {"nombre": "Luis", "edad": 17, "ciudad": "Barcelona"},
    {"nombre": "Marta", "edad": 30, "ciudad": "Valencia"}
]

for i, usuario in enumerate(usuarios_data, start=1):
    print(f"{i}. {usuario['nombre']} ({usuario['edad']} años) vive en {usuario['ciudad']})")
