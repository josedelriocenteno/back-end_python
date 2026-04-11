# bucles_for.py
"""
BÚCLES FOR EN PYTHON
====================

Objetivo:
- Iterar correctamente sobre cualquier estructura de datos
- Evitar errores comunes como mutaciones peligrosas o indices incorrectos
- Preparar código profesional para backend y pipelines de datos
"""

# =========================================================
# 1. Sintaxis básica
# =========================================================

numeros = [1, 2, 3, 4, 5]

for n in numeros:
    print(n)

# =========================================================
# 2. Iteración con índice
# =========================================================

# Usando range()
for i in range(len(numeros)):
    print(f"Índice {i}, valor {numeros[i]}")

# Usando enumerate() → profesional
for i, n in enumerate(numeros):
    print(f"Índice {i}, valor {n}")

# =========================================================
# 3. Iteración sobre diccionarios
# =========================================================

usuario = {"nombre": "Juan", "edad": 30}

# Iterar sobre claves
for clave in usuario:
    print(clave, usuario[clave])

# Iterar sobre items
for clave, valor in usuario.items():
    print(clave, valor)

# =========================================================
# 4. Buenas prácticas
# =========================================================

# - Evitar modificar la lista mientras iteras sobre ella
# ❌ Malo
for n in numeros:
    if n % 2 == 0:
        numeros.remove(n)

# ✅ Mejor: usar comprensión de listas o iterar sobre copia
numeros = [1, 2, 3, 4, 5]
numeros_filtrados = [n for n in numeros if n % 2 != 0]
print(numeros_filtrados)

# - Siempre preferir for sobre while para iteración sobre estructuras conocidas
# - Usar enumerate() para índices, items() para diccionarios
# - Mantener el cuerpo del bucle limpio y conciso

# =========================================================
# 5. Aplicación profesional
# =========================================================

# Backend/data: recorrer endpoints, listas de registros, batches
usuarios = [
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Luis", "edad": 17},
    {"nombre": "Marta", "edad": 30}
]

for usuario in usuarios:
    if usuario["edad"] >= 18:
        print(f"{usuario['nombre']} es mayor de edad")
