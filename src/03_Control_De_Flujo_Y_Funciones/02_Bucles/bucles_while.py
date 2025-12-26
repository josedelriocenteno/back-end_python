# bucles_while.py
"""
BÚCLES WHILE EN PYTHON
======================

Objetivo:
- Comprender cuándo usar while y cuándo evitarlo
- Prevenir bucles infinitos y problemas de rendimiento
- Aplicable a backend, pipelines y scripts de automatización
"""

# =========================================================
# 1. Sintaxis básica
# =========================================================

contador = 0

while contador < 5:
    print(f"Contador: {contador}")
    contador += 1  # Incremento imprescindible para evitar bucle infinito

# =========================================================
# 2. Cuándo usar while
# =========================================================

# a) Cuando no conocemos de antemano el número de iteraciones
import random

numero = 0
while numero != 5:
    numero = random.randint(0, 10)
    print(f"Número generado: {numero}")

# b) Cuando esperamos que ocurra un evento para detener el bucle
eventos = ["start", "process", "stop"]
i = 0
while eventos[i] != "stop":
    print(f"Evento actual: {eventos[i]}")
    i += 1

# =========================================================
# 3. Cuándo NO usar while
# =========================================================

# ❌ Evitar while si conocemos el número exacto de iteraciones
# Por ejemplo, usar for con range() es más legible y seguro
for i in range(5):
    print(f"Iteración con for: {i}")

# ❌ Evitar mutaciones complejas dentro de while que puedan causar bucles infinitos

# =========================================================
# 4. Buenas prácticas
# =========================================================

# - Siempre asegurar que la condición del while pueda volverse False
# - Evitar modificar listas/diccionarios mientras se itera
# - Preferir for cuando el número de iteraciones es conocido
# - Mantener el cuerpo del bucle claro y conciso

# =========================================================
# 5. Aplicación profesional
# =========================================================

# Backend/data pipelines: esperar eventos, procesar streams, leer datos hasta fin de archivo
data_stream = [1, 2, 3, 4, 5]
index = 0

while index < len(data_stream):
    valor = data_stream[index]
    print(f"Procesando valor: {valor}")
    index += 1
