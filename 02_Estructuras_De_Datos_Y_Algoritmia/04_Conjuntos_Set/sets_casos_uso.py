# sets_casos_uso.py
"""
SETS EN PYTHON — CASOS DE USO REALES
====================================

Objetivo:
- Aplicar sets en problemas prácticos
- Deduplicación de datos
- Membership test rápido
- Filtrado eficiente en pipelines y backend
"""

# ------------------------------------------------------------
# 1. ELIMINACIÓN DE DUPLICADOS
# ------------------------------------------------------------

emails = [
    "juan@mail.com", "ana@mail.com", "juan@mail.com", "luis@mail.com"
]

# Método eficiente con set
emails_unicos = list(set(emails))
print("Emails únicos:", emails_unicos)


# ------------------------------------------------------------
# 2. MEMBERSHIP TEST
# ------------------------------------------------------------

usuarios_permitidos = {"u1", "u2", "u3"}
usuarios_actuales = ["u1", "u4", "u2", "u5"]

# Filtrado rápido
usuarios_validados = [u for u in usuarios_actuales if u in usuarios_permitidos]
print("Usuarios permitidos:", usuarios_validados)
# O(1) por cada lookup, mucho más rápido que lista


# ------------------------------------------------------------
# 3. FILTRADO EFICIENTE EN DATA PIPELINES
# ------------------------------------------------------------

# Dataset simulado
transacciones = [
    {"user": "u1", "importe": 100},
    {"user": "u2", "importe": 200},
    {"user": "u3", "importe": 150},
    {"user": "u4", "importe": 300}
]

usuarios_activos = {"u1", "u3"}

# Filtrar solo transacciones de usuarios activos
transacciones_activas = [t for t in transacciones if t["user"] in usuarios_activos]
print("Transacciones activas:", transacciones_activas)


# ------------------------------------------------------------
# 4. COMBINACIÓN DE SETS PARA ANALÍTICA
# ------------------------------------------------------------

ventas_online = {"p1", "p2", "p3", "p5"}
ventas_tienda = {"p2", "p3", "p4"}

# Productos vendidos en ambos canales
comunes = ventas_online & ventas_tienda
print("Comunes:", comunes)

# Productos exclusivos de online
solo_online = ventas_online - ventas_tienda
print("Solo online:", solo_online)


# ------------------------------------------------------------
# 5. USO DE SETS PARA VALIDACIÓN DE DATOS
# ------------------------------------------------------------

# Evitar duplicados en IDs de usuarios
ids = [101, 102, 103, 101, 104]
if len(ids) != len(set(ids)):
    print("Warning: IDs duplicados detectados")


# ------------------------------------------------------------
# 6. ERRORES COMUNES
# ------------------------------------------------------------

"""
❌ Usar lista para membership test en datos grandes → O(n)
❌ Depender del orden de los elementos del set
❌ Modificar set mientras iteras
"""

# ❌ lento
usuarios_permitidos_lista = ["u1","u2","u3"]
validos = [u for u in usuarios_actuales if u in usuarios_permitidos_lista]  # O(n*m)

# ✔ rápido
usuarios_permitidos_set = {"u1","u2","u3"}
validos = [u for u in usuarios_actuales if u in usuarios_permitidos_set]  # O(m)


# ------------------------------------------------------------
# 7. BUENAS PRÁCTICAS PROFESIONALES
# ------------------------------------------------------------

"""
✔ Usa set() para membership tests rápidos
✔ Deduplicación eficiente con set()
✔ Combina sets para operaciones de análisis
✔ Documenta claramente qué representa cada set
✔ Iterar sobre copia si vas a modificar
"""

print("Casos de uso de sets dominados")
