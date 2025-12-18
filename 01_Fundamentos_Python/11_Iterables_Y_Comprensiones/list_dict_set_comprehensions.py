# list_dict_set_comprehensions.py
"""
List, Dict y Set Comprehensions en Python – Nivel Backend Profesional

Este módulo cubre:
- List comprehensions
- Dict comprehensions
- Set comprehensions
- Filtrado y transformación de datos
- Buenas prácticas para backend y pipelines
"""

# -------------------------------------------------
# 1. List comprehension
# -------------------------------------------------
# Crear listas de forma concisa y eficiente
numeros = [1, 2, 3, 4, 5]

# Tradicional
cuadrados = []
for n in numeros:
    cuadrados.append(n**2)

# Con comprehension (profesional)
cuadrados = [n**2 for n in numeros]
print(cuadrados)  # [1, 4, 9, 16, 25]

# Filtrar elementos
pares = [n for n in numeros if n % 2 == 0]
print(pares)  # [2, 4]

# Transformación y condición
pares_cuadrados = [n**2 for n in numeros if n % 2 == 0]
print(pares_cuadrados)  # [4, 16]

# -------------------------------------------------
# 2. Dict comprehension
# -------------------------------------------------
usuarios = ["juan", "pedro", "maria"]
edades = [25, 30, 22]

# Tradicional
usuarios_dict = {}
for u, e in zip(usuarios, edades):
    usuarios_dict[u] = e

# Con comprehension (profesional)
usuarios_dict = {u: e for u, e in zip(usuarios, edades)}
print(usuarios_dict)  # {'juan': 25, 'pedro': 30, 'maria': 22}

# Filtrar
usuarios_mayores = {u: e for u, e in zip(usuarios, edades) if e >= 25}
print(usuarios_mayores)  # {'juan': 25, 'pedro': 30}

# -------------------------------------------------
# 3. Set comprehension
# -------------------------------------------------
numeros_repetidos = [1,2,2,3,3,3,4]
numeros_unicos = {n for n in numeros_repetidos}
print(numeros_unicos)  # {1,2,3,4}

# -------------------------------------------------
# 4. Comprehensions en backend y datos
# -------------------------------------------------
# Procesar logs
logs = [
    "INFO | Usuario juan creado",
    "ERROR | Fallo de DB",
    "INFO | Usuario pedro creado"
]

# Filtrar solo logs de INFO
logs_info = [log for log in logs if log.startswith("INFO")]
print(logs_info)

# Extraer nombres de usuario
usuarios_creados = [log.split()[2] for log in logs_info]
print(usuarios_creados)  # ['juan', 'pedro']

# -------------------------------------------------
# 5. Errores comunes de juniors
# -------------------------------------------------
# ❌ Usar bucles tradicionales innecesarios
# ❌ Comprehensions demasiado largas y difíciles de leer
# ❌ No usar filtrado interno → código más largo y lento
# ❌ Confundir dict/set comprehensions con list comprehension

# -------------------------------------------------
# 6. Buenas prácticas profesionales
# -------------------------------------------------
# ✔️ Mantener comprehensions cortas y legibles
# ✔️ Usar filtrado interno en lugar de bucles externos
# ✔️ Preferir comprehensions sobre map/filter en Python moderno
# ✔️ Documentar transformaciones complejas
# ✔️ Evitar efectos secundarios dentro de comprehensions

# -------------------------------------------------
# 7. Checklist mental backend
# -------------------------------------------------
# ✔️ Comprehensions usadas para transformar/filtrar datos?  
# ✔️ Código legible y limpio?  
# ✔️ Memoria y eficiencia optimizadas?  
# ✔️ Transformaciones claras y reproducibles?

# -------------------------------------------------
# 8. Regla de oro
# -------------------------------------------------
"""
En backend profesional:
- Comprehensions = código más limpio, eficiente y legible
- Filtra y transforma datos de manera concisa
- Evita bucles y append innecesarios
- Esto garantiza pipelines y procesamiento de datos robustos y profesionales
"""
