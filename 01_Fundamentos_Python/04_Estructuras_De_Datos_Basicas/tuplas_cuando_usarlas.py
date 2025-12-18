# tuplas_cuando_usarlas.py
"""
Tuplas en Backend Python – Cuándo Usarlas de Verdad

Este módulo explica:
- Qué es una tupla a nivel práctico
- Por qué la inmutabilidad importa en backend
- Casos reales donde una tupla es MEJOR que una lista
- Errores comunes de juniors
- Patrones profesionales
"""

# -------------------------------------------------
# 1. Qué es una tupla (realidad backend)
# -------------------------------------------------
# - Estructura ORDENADA
# - INMUTABLE
# - Más segura para contratos
# - Ligera y ligeramente más rápida que listas

coordenadas = (40.4168, -3.7038)  # lat, lon


# -------------------------------------------------
# 2. Inmutabilidad = seguridad
# -------------------------------------------------

config = ("localhost", 5432)

# ❌ Esto falla (y eso es BUENO)
# config[0] = "127.0.0.1"

# ✔️ Evita bugs accidentales en producción


# -------------------------------------------------
# 3. Tuplas como contratos de datos
# -------------------------------------------------

def obtener_usuario():
    # Retorno con estructura fija
    return (1, "ana", True)

usuario_id, nombre, activo = obtener_usuario()

# ✔️ El orden IMPORTA y está garantizado


# -------------------------------------------------
# 4. Devolver múltiples valores (patrón real)
# -------------------------------------------------

def dividir(a, b):
    if b == 0:
        return None, "division_por_cero"
    return a / b, None

resultado, error = dividir(10, 2)

if error:
    print("Error:", error)


# -------------------------------------------------
# 5. Tuplas como claves de diccionario
# -------------------------------------------------

# ❌ Listas no son hashables
# dic = {[1,2]: "valor"}

# ✔️ Tuplas sí
cache = {
    ("users", 1): {"id": 1, "email": "a@test.com"},
    ("users", 2): {"id": 2, "email": "b@test.com"},
}


# -------------------------------------------------
# 6. Iterar con tuplas
# -------------------------------------------------

registros = [
    (1, "ana"),
    (2, "juan"),
    (3, "lucia"),
]

for user_id, nombre in registros:
    print(user_id, nombre)


# -------------------------------------------------
# 7. Tuplas vs listas (decisión profesional)
# -------------------------------------------------

# ✔️ Usa TUPLA cuando:
# - La estructura NO debe cambiar
# - Representa un registro fijo
# - Es un contrato entre funciones
# - Se usa como clave de dict
# - Quieres evitar errores

# ✔️ Usa LISTA cuando:
# - Necesitas modificar contenido
# - Agregar / eliminar elementos
# - Tamaño variable


# -------------------------------------------------
# 8. Error común: usar lista por costumbre
# -------------------------------------------------

# ❌ Mala práctica
usuario = ["ana", "admin", True]

# ✔️ Mejor
usuario = ("ana", "admin", True)


# -------------------------------------------------
# 9. Named tuples (nivel pro)
# -------------------------------------------------

from collections import namedtuple

Usuario = namedtuple("Usuario", ["id", "nombre", "activo"])

u = Usuario(id=1, nombre="ana", activo=True)

print(u.id, u.nombre)


# -------------------------------------------------
# 10. Inmutabilidad no es absoluta
# -------------------------------------------------

# ⚠️ Cuidado:
tupla_con_lista = (1, [2, 3])

# ❌ Esto SÍ cambia
tupla_con_lista[1].append(4)

# La tupla es inmutable, su contenido puede no serlo


# -------------------------------------------------
# 11. Performance y memoria
# -------------------------------------------------

# Tuplas:
# - Menor overhead
# - Mejor cache friendliness
# - Útiles para grandes cantidades de registros fijos


# -------------------------------------------------
# 12. Checklist mental backend
# -------------------------------------------------
# ✔️ ¿Puede cambiar? → LISTA
# ✔️ ¿Es un contrato? → TUPLA
# ✔️ ¿Clave de dict? → TUPLA
# ✔️ ¿Evitar bugs? → TUPLA
# ✔️ ¿Datos fijos? → TUPLA


# -------------------------------------------------
# 13. Regla de oro
# -------------------------------------------------
"""
Si algo NO debería cambiar,
NO lo representes con algo que pueda cambiar.
"""
