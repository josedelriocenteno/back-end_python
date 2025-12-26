# sets_como_hash_sets.py
"""
Sets en Backend Python – Hash Sets Reales

Este módulo cubre:
- Qué es un set a nivel de implementación
- Por qué son O(1) en pertenencia
- Casos reales de backend y data
- Errores comunes de juniors
- Decisiones de rendimiento profesionales
"""

# -------------------------------------------------
# 1. Qué es un set realmente
# -------------------------------------------------
# - Colección NO ordenada
# - Elementos ÚNICOS
# - Basado en HASH TABLE
# - Pertenencia O(1) promedio

ids = {1, 2, 3, 4, 5}


# -------------------------------------------------
# 2. Caso real: evitar duplicados
# -------------------------------------------------

emails = [
    "a@test.com",
    "b@test.com",
    "a@test.com",
    "c@test.com",
]

emails_unicos = set(emails)

# ✔️ Eliminación automática de duplicados


# -------------------------------------------------
# 3. Comparación de rendimiento
# -------------------------------------------------

ids_lista = list(range(1_000_000))
ids_set = set(ids_lista)

# ❌ Lento
# 999_999 in ids_lista  # O(n)

# ✔️ Rápido
# 999_999 in ids_set    # O(1)


# -------------------------------------------------
# 4. Sets en validaciones backend
# -------------------------------------------------

ROLES_VALIDOS = {"admin", "user", "moderator"}

def validar_rol(rol: str) -> bool:
    return rol in ROLES_VALIDOS


# -------------------------------------------------
# 5. Sets como filtros
# -------------------------------------------------

usuarios = [
    {"id": 1, "activo": True},
    {"id": 2, "activo": False},
    {"id": 3, "activo": True},
]

ids_activos = {u["id"] for u in usuarios if u["activo"]}


# -------------------------------------------------
# 6. Operaciones matemáticas reales
# -------------------------------------------------

a = {1, 2, 3, 4}
b = {3, 4, 5}

a | b   # unión
a & b   # intersección
a - b   # diferencia
a ^ b   # diferencia simétrica


# -------------------------------------------------
# 7. Error común: confiar en el orden
# -------------------------------------------------

s = {"ana", "juan", "lucia"}

# ❌ No hay orden garantizado
# print(s[0])  # ERROR

for nombre in s:
    print(nombre)


# -------------------------------------------------
# 8. Sets NO aceptan mutables
# -------------------------------------------------

# ❌ Error
# s = {[1,2,3]}

# ✔️ Solo hashables
s = {(1, 2), "hola", 42}


# -------------------------------------------------
# 9. Sets como caché simple
# -------------------------------------------------

procesados = set()

def procesar(id_evento):
    if id_evento in procesados:
        return
    procesados.add(id_evento)
    print("Procesando", id_evento)


# -------------------------------------------------
# 10. Mutabilidad del set
# -------------------------------------------------

s = {1, 2, 3}
s.add(4)
s.remove(2)

# ⚠️ remove lanza error si no existe
# ✔️ discard no
s.discard(99)


# -------------------------------------------------
# 11. frozenset (nivel pro)
# -------------------------------------------------

# Inmutable, hashable
PERMISOS_ADMIN = frozenset({"read", "write", "delete"})

# ✔️ Puede ser clave de dict
config_permisos = {
    PERMISOS_ADMIN: "nivel_maximo"
}


# -------------------------------------------------
# 12. Error típico de estudiante
# -------------------------------------------------

# ❌ Usar lista para pertenencia
usuarios_ids = [1, 2, 3, 4]

if 3 in usuarios_ids:  # lento
    pass

# ✔️ Forma profesional
usuarios_ids = set(usuarios_ids)


# -------------------------------------------------
# 13. Sets vs listas vs dicts
# -------------------------------------------------
# LISTA → orden, duplicados, recorrido
# SET   → unicidad, pertenencia rápida
# DICT  → clave-valor


# -------------------------------------------------
# 14. Regla de oro backend
# -------------------------------------------------
"""
Si la operación principal es:
'¿Está esto aquí?'

NO uses una lista.
"""
