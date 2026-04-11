# diccionarios_como_hash_maps.py
"""
Diccionarios en Backend Python – Hash Maps Profesionales

Este módulo cubre:
- Qué es un diccionario realmente (hash map)
- Costes reales de operaciones
- Casos críticos de backend y data
- Errores comunes de juniors
- Patrones profesionales
"""

# -------------------------------------------------
# 1. Qué es un diccionario en backend
# -------------------------------------------------
# - Estructura CLAVE → VALOR
# - Basado en HASH TABLE
# - Acceso, inserción y borrado O(1) promedio
# - Columna vertebral del backend moderno

usuario = {
    "id": 1,
    "email": "a@test.com",
    "activo": True,
}


# -------------------------------------------------
# 2. Acceso seguro a datos
# -------------------------------------------------

# ❌ Forma peligrosa
# email = usuario["email"]

# ✔️ Forma profesional
email = usuario.get("email")

if email is None:
    print("Usuario sin email")


# -------------------------------------------------
# 3. Diccionarios como modelo de datos
# -------------------------------------------------

usuarios = {
    1: {"email": "a@test.com", "rol": "admin"},
    2: {"email": "b@test.com", "rol": "user"},
}

# ✔️ Acceso rápido por ID
usuario_1 = usuarios.get(1)


# -------------------------------------------------
# 4. Coste real de operaciones
# -------------------------------------------------

# Acceso por clave → O(1)
# Inserción → O(1)
# Eliminación → O(1)
# Recorrido → O(n)

# ⚠️ El hash debe ser bueno (clave inmutable)


# -------------------------------------------------
# 5. Diccionarios para conteo (caso real)
# -------------------------------------------------

logs = ["INFO", "ERROR", "INFO", "WARNING", "ERROR"]

contador = {}

for nivel in logs:
    contador[nivel] = contador.get(nivel, 0) + 1


# -------------------------------------------------
# 6. defaultdict (nivel profesional)
# -------------------------------------------------

from collections import defaultdict

contador = defaultdict(int)

for nivel in logs:
    contador[nivel] += 1


# -------------------------------------------------
# 7. Actualización segura
# -------------------------------------------------

usuario = {"id": 1, "email": "a@test.com"}

# ✔️ update
usuario.update({"email": "nuevo@test.com"})


# -------------------------------------------------
# 8. Iterar correctamente
# -------------------------------------------------

for clave in usuario:
    print(clave)

for clave, valor in usuario.items():
    print(clave, valor)


# -------------------------------------------------
# 9. Diccionarios como caché
# -------------------------------------------------

cache = {}

def obtener_usuario(id_usuario):
    if id_usuario in cache:
        return cache[id_usuario]

    # Simula acceso a BD
    usuario = {"id": id_usuario, "email": "x@test.com"}
    cache[id_usuario] = usuario
    return usuario


# -------------------------------------------------
# 10. Error crítico: claves mutables
# -------------------------------------------------

# ❌ NO hacer esto
# d = {[1,2]: "valor"}

# ✔️ Claves válidas
d = {
    (1, 2): "ok",
    "clave": "ok",
    42: "ok",
}


# -------------------------------------------------
# 11. Diccionarios anidados (realidad backend)
# -------------------------------------------------

config = {
    "db": {
        "host": "localhost",
        "port": 5432,
    },
    "debug": True,
}

# ✔️ Acceso seguro
db_host = config.get("db", {}).get("host")


# -------------------------------------------------
# 12. Merge de diccionarios (Python moderno)
# -------------------------------------------------

base = {"a": 1, "b": 2}
override = {"b": 99, "c": 3}

config = base | override  # Python 3.9+


# -------------------------------------------------
# 13. Errores comunes de juniors
# -------------------------------------------------
# ❌ Acceder sin comprobar
# ❌ Usar dict cuando un objeto sería mejor
# ❌ Claves inconsistentes ("id" vs "ID")
# ❌ No validar estructura
# ❌ Mutar diccionarios compartidos


# -------------------------------------------------
# 14. Diccionarios vs otros tipos
# -------------------------------------------------
# LISTA → orden
# SET   → unicidad
# TUPLA → contrato
# DICT  → acceso rápido por clave


# -------------------------------------------------
# 15. Regla de oro backend
# -------------------------------------------------
"""
Si necesitas acceder a algo por una clave,
un diccionario es casi siempre la respuesta correcta.
"""
