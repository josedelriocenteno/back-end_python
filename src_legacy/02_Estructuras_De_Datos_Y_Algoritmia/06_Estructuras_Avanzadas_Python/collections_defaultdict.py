# collections_defaultdict.py
"""
COLLECTIONS.DEFAULTDICT EN PYTHON — INICIALIZACIÓN AUTOMÁTICA
=============================================================

Objetivo:
- Usar defaultdict para evitar checks manuales de existencia de claves
- Aplicaciones en backend, pipelines y análisis de datos
- Inicialización automática de listas, sets, contadores, etc.
"""

from collections import defaultdict, Counter

# ------------------------------------------------------------
# 1. CREACIÓN DE UN DEFAULTDICT
# ------------------------------------------------------------

# Lista como valor por defecto
dd_list = defaultdict(list)
print("DefaultDict lista inicial:", dd_list)

# Añadir elementos sin check manual
dd_list["frutas"].append("manzana")
dd_list["frutas"].append("banana")
dd_list["verduras"].append("zanahoria")
print("DefaultDict con listas:", dd_list)

# Set como valor por defecto
dd_set = defaultdict(set)
dd_set["usuarios"].add("u1")
dd_set["usuarios"].add("u2")
print("DefaultDict con sets:", dd_set)


# ------------------------------------------------------------
# 2. USOS COMUNES
# ------------------------------------------------------------

# Contar elementos agrupados
data = [
    {"categoria": "A", "valor": 10},
    {"categoria": "B", "valor": 20},
    {"categoria": "A", "valor": 15}
]

grouped = defaultdict(list)
for item in data:
    grouped[item["categoria"]].append(item["valor"])
print("Agrupamiento por categoría:", grouped)

# Conteo automático
counts = defaultdict(int)
items = ["x","y","x","z","x","y"]
for item in items:
    counts[item] += 1
print("Conteo con defaultdict:", counts)


# ------------------------------------------------------------
# 3. OPERACIONES AVANZADAS
# ------------------------------------------------------------

# Combinación con Counter
dd_counter = defaultdict(Counter)
dd_counter["logs"].update(["login","logout","login"])
print("Counter dentro de defaultdict:", dd_counter)

# Mezcla de listas y sets
dd_mix = defaultdict(lambda: {"lista": [], "set": set()})
dd_mix["grupo"]["lista"].append(1)
dd_mix["grupo"]["set"].add(1)
print("DefaultDict mixto:", dd_mix)


# ------------------------------------------------------------
# 4. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar dict normal y chequear si clave existe → más código, más errores
❌ Confundir tipo de valor por defecto (list vs set)
❌ Sobrescribir defaultdict accidentalmente
❌ Usar mutable por defecto sin intención → puede modificar accidentalmente todas las claves
"""

# ✔ Correcto
dd_safe = defaultdict(list)
dd_safe["a"].append(1)
dd_safe["b"].append(2)


# ------------------------------------------------------------
# 5. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Prefiere defaultdict para valores por defecto
✔ Documenta claramente tipo de valor que espera
✔ Evita mutable por defecto si no es necesario
✔ Combina con Counter para conteo eficiente
✔ Útil en pipelines, logs y agrupamientos de datos
"""

print("collections.defaultdict dominado profesionalmente")
