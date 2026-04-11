# comprensiones_vs_bucles.py
"""
COMPREHENSIONS VS BUCLES
========================

Objetivo:
- Comparar comprensiones con bucles tradicionales
- Entender ventajas y límites de cada enfoque
- Aplicable a backend, pipelines y procesamiento de datos
"""

# =========================================================
# 1. Caso simple: crear lista de cuadrados
# =========================================================

# Bucle tradicional
cuadrados = []
for x in range(5):
    cuadrados.append(x**2)
print("Bucle:", cuadrados)

# Comprensión de listas
cuadrados_comp = [x**2 for x in range(5)]
print("Comprensión:", cuadrados_comp)

# =========================================================
# 2. Filtrado con condición
# =========================================================

# Bucle tradicional
pares = []
for x in range(10):
    if x % 2 == 0:
        pares.append(x)
print("Bucle filtrado:", pares)

# Comprensión de listas
pares_comp = [x for x in range(10) if x % 2 == 0]
print("Comprensión filtrada:", pares_comp)

# =========================================================
# 3. Diccionarios y sets
# =========================================================

# Bucle tradicional
cuadrados_dict = {}
for x in range(5):
    cuadrados_dict[x] = x**2
print("Dict bucle:", cuadrados_dict)

# Dict comprehension
cuadrados_dict_comp = {x: x**2 for x in range(5)}
print("Dict comprensión:", cuadrados_dict_comp)

# =========================================================
# 4. Legibilidad vs concisión
# =========================================================

# ❌ Evitar comprensiones demasiado largas
# resultado = [func(x) for x in data if cond1(x) if cond2(x)]

# ✅ Mejor bucle tradicional con comentarios
resultado = []
for x in range(10):
    if x % 2 == 0:
        resultado.append(x**2)

# =========================================================
# 5. Buenas prácticas
# =========================================================

# - Usa comprensiones para transformaciones simples y filtrado
# - Prefiere bucles explícitos cuando la lógica es compleja
# - Mantén legibilidad profesional: prioriza que otros devs lo entiendan
# - Documenta la intención
