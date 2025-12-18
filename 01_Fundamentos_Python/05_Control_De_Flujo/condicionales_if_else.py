# condicionales_if_else.py
"""
Condicionales if / elif / else en Backend Python – Uso Profesional

Este módulo cubre:
- Cómo tomar decisiones correctas en backend
- Errores lógicos reales
- Patrones profesionales
- Código claro vs código peligroso
"""

# -------------------------------------------------
# 1. Qué es un condicional en backend
# -------------------------------------------------
# Un condicional:
# - Decide flujo de ejecución
# - Controla reglas de negocio
# - Protege el sistema de datos inválidos

# Un if mal hecho rompe lógica, no solo código.


# -------------------------------------------------
# 2. Comparaciones correctas
# -------------------------------------------------

edad = 18

# ❌ Error común
# if edad == True:

# ✔️ Correcto
if edad >= 18:
    print("Mayor de edad")


# -------------------------------------------------
# 3. Orden de condiciones IMPORTA
# -------------------------------------------------

nota = 8

# ❌ Lógica incorrecta
# if nota >= 5:
#     print("Aprobado")
# elif nota >= 9:
#     print("Excelente")

# ✔️ Forma correcta
if nota >= 9:
    print("Excelente")
elif nota >= 5:
    print("Aprobado")
else:
    print("Suspenso")


# -------------------------------------------------
# 4. Evitar condiciones redundantes
# -------------------------------------------------

# ❌ Verboso y propenso a errores
if edad >= 18 and edad < 65:
    print("Adulto")

# ✔️ Limpio
if 18 <= edad < 65:
    print("Adulto")


# -------------------------------------------------
# 5. Truthy y Falsy (zona peligrosa)
# -------------------------------------------------

datos = []

# ❌ Ambiguo en backend
# if datos:

# ✔️ Explícito
if len(datos) > 0:
    print("Hay datos")

# ✔️ O mejor aún
if not datos:
    print("Lista vacía")


# -------------------------------------------------
# 6. Comparar con None SIEMPRE explícito
# -------------------------------------------------

resultado = None

# ❌ MAL
# if resultado == None:

# ✔️ BIEN
if resultado is None:
    print("No hay resultado")


# -------------------------------------------------
# 7. Condicionales con strings (muy común)
# -------------------------------------------------

estado = "Activo"

# ❌ Frágil
# if estado == "activo":

# ✔️ Normalizar
if estado.lower() == "activo":
    print("Usuario activo")


# -------------------------------------------------
# 8. Guard clauses (patrón profesional)
# -------------------------------------------------

def procesar_pago(monto):
    if monto <= 0:
        raise ValueError("Monto inválido")

    if monto > 10_000:
        raise ValueError("Monto sospechoso")

    # Lógica principal clara
    print("Procesando pago")


# -------------------------------------------------
# 9. Evitar if anidados (código infierno)
# -------------------------------------------------

# ❌ Difícil de leer
def acceso_malo(usuario):
    if usuario:
        if usuario["activo"]:
            if usuario["rol"] == "admin":
                return True
    return False

# ✔️ Profesional
def acceso_bueno(usuario):
    if not usuario:
        return False
    if not usuario.get("activo"):
        return False
    return usuario.get("rol") == "admin"


# -------------------------------------------------
# 10. Condicionales como expresiones
# -------------------------------------------------

# ✔️ Útil cuando es SIMPLE
estado = "activo" if edad >= 18 else "menor"


# -------------------------------------------------
# 11. Error común: usar if para todo
# -------------------------------------------------

# ❌ No escalable
def rol_texto(rol):
    if rol == 1:
        return "admin"
    elif rol == 2:
        return "user"
    elif rol == 3:
        return "moderator"
    else:
        return "desconocido"

# ✔️ Profesional
ROLES = {
    1: "admin",
    2: "user",
    3: "moderator",
}

def rol_texto(rol):
    return ROLES.get(rol, "desconocido")


# -------------------------------------------------
# 12. Condicionales y seguridad
# -------------------------------------------------

def eliminar_usuario(usuario):
    if not usuario.get("es_admin"):
        raise PermissionError("No autorizado")

    print("Usuario eliminado")


# -------------------------------------------------
# 13. Checklist mental backend
# -------------------------------------------------
# ✔️ ¿El orden importa? → REVISA
# ✔️ ¿Es explícito? → BIEN
# ✔️ ¿Hay anidamiento profundo? → MAL
# ✔️ ¿Puedo usar estructuras? → MEJOR
# ✔️ ¿Esto protege el sistema? → OBLIGATORIO


# -------------------------------------------------
# 14. Regla de oro
# -------------------------------------------------
"""
Un if mal pensado no lanza errores,
lanza bugs silenciosos.
"""
