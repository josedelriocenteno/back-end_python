# diccionarios_patrones.py
"""
PATRONES DE USO DE DICCIONARIOS EN BACKEND Y DATA ENGINEERING
=============================================================

Objetivo:
- Aprender patrones prácticos de diccionarios
- Acumular resultados
- Construir lookup tables
- Indexar datos para acceso rápido
"""

# ------------------------------------------------------------
# 1. CONTADORES
# ------------------------------------------------------------

# Contar ocurrencias de elementos
letras = ["a","b","a","c","b","a"]

contador = {}
for letra in letras:
    contador[letra] = contador.get(letra, 0) + 1

print("Contador:", contador)
# Salida: {'a': 3, 'b': 2, 'c': 1}

# Alternativa con collections.Counter
from collections import Counter
contador2 = Counter(letras)
print("Counter:", contador2)


# ------------------------------------------------------------
# 2. LOOKUP TABLES
# ------------------------------------------------------------

# Mapear valores a funciones o datos precomputados
def cuadrado(x): return x*x
def cubo(x): return x*x*x

lookup = {
    "cuadrado": cuadrado,
    "cubo": cubo
}

print(lookup )  # 25
print(lookup )      # 27


# ------------------------------------------------------------
# 3. ÍNDICES PARA ACCESO RÁPIDO
# ------------------------------------------------------------

# Dataset simulado
usuarios = [
    {"id": "user_1", "nombre": "Juan", "edad": 30},
    {"id": "user_2", "nombre": "Ana", "edad": 25},
    {"id": "user_3", "nombre": "Luis", "edad": 40},
]

# Crear índice por id
indice = {u["id"]: u for u in usuarios}

print(indice["user_2"])  # {'id': 'user_2', 'nombre': 'Ana', 'edad': 25}


# ------------------------------------------------------------
# 4. AGRUPACIÓN DE ELEMENTOS (GROUP BY)
# ------------------------------------------------------------

transacciones = [
    {"user": "u1", "importe": 100},
    {"user": "u2", "importe": 50},
    {"user": "u1", "importe": 200},
]

grouped = {}
for t in transacciones:
    user = t["user"]
    grouped.setdefault(user, []).append(t)

print(grouped)
# {'u1': [{'user': 'u1', 'importe': 100}, {'user': 'u1', 'importe': 200}], 'u2': [{'user': 'u2', 'importe': 50}]}


# ------------------------------------------------------------
# 5. TABLAS DE BÚSQUEDA RÁPIDAS (LOOKUPS)
# ------------------------------------------------------------

# Convertir lista de dicts en diccionario para acceso O(1)
productos = [
    {"sku": "p1", "precio": 10},
    {"sku": "p2", "precio": 20},
]

lookup_sku = {p["sku"]: p["precio"] for p in productos}

print(lookup_sku["p2"])  # 20


# ------------------------------------------------------------
# 6. MANEJO DE VALORES POR DEFECTO
# ------------------------------------------------------------

# Evita KeyError
ventas = {"enero": 100, "febrero": 120}
print(ventas.get("marzo", 0))  # 0


# ------------------------------------------------------------
# 7. PATRONES MIXTOS
# ------------------------------------------------------------

# Combinar contadores y lookup
logs = [
    {"user": "u1", "event": "login"},
    {"user": "u2", "event": "login"},
    {"user": "u1", "event": "logout"},
]

event_count = {}
for log in logs:
    key = (log["user"], log["event"])
    event_count[key] = event_count.get(key, 0) + 1

print(event_count)
# {('u1', 'login'): 1, ('u2', 'login'): 1, ('u1', 'logout'): 1}


# ------------------------------------------------------------
# 8. BUENAS PRÁCTICAS
# ------------------------------------------------------------

"""
✔ Usar claves claras y únicas
✔ Evitar mutar diccionarios mientras se iteran
✔ Usar defaultdict o setdefault para simplificar código
✔ Documentar estructura de diccionario
✔ Prefiere comprensión de dicts para patrones simples
"""

# Ejemplo de defaultdict
from collections import defaultdict
grouped_dd = defaultdict(list)
for t in transacciones:
    grouped_dd[t["user"]].append(t)

print(grouped_dd)

print("Patrones de diccionarios dominados")
