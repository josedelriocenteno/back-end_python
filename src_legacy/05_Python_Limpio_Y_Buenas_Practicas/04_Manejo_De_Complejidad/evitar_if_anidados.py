"""
evitar_if_anidados.py
=====================

Este archivo enseña cómo reemplazar if anidados por "guard clauses"
para simplificar funciones y mejorar legibilidad.

Problema típico:
- Muchos if anidados crean código difícil de leer
- Difícil de testear y refactorizar
- Oculta la lógica principal de la función

Solución:
- Usar guard clauses (retornos tempranos, excepciones tempranas)
- Reduce indentación y hace la función más lineal
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO CLÁSICO: IF ANIDADO PROFUNDO
# -------------------------------------------------------------------

def procesar_usuario(usuario: dict) -> str:
    """
    Procesa un usuario solo si está activo y tiene email válido.
    """
    if usuario.get("activo"):
        if usuario.get("email") and "@" in usuario["email"]:
            if len(usuario["nombre"]) > 0:
                # Lógica principal
                return f"Usuario válido: {usuario['nombre']}"
    return "Usuario inválido"

# Problemas:
# - Difícil de leer a primera vista
# - Mucha indentación
# - Lógica principal oculta al fondo


# -------------------------------------------------------------------
# 2️⃣ SOLUCIÓN: GUARD CLAUSES
# -------------------------------------------------------------------

def procesar_usuario_guard(usuario: dict) -> str:
    """
    Procesa un usuario usando guard clauses para validar primero condiciones.
    """
    if not usuario.get("activo"):
        return "Usuario inválido"

    if not usuario.get("email") or "@" not in usuario["email"]:
        return "Usuario inválido"

    if not usuario.get("nombre"):
        return "Usuario inválido"

    # Lógica principal clara y sin indentaciones
    return f"Usuario válido: {usuario['nombre']}"


# -------------------------------------------------------------------
# 3️⃣ VENTAJAS DE GUARD CLAUSES
# -------------------------------------------------------------------
#
# - Reduce niveles de indentación
# - Destaca la lógica principal
# - Fácil de leer y mantener
# - Más seguro: las condiciones de error se detectan rápido
# - Compatible con testeo unitario


# -------------------------------------------------------------------
# 4️⃣ EJEMPLO PRÁCTICO: PROYECTO POO / PEDIDOS
# -------------------------------------------------------------------

def procesar_pedido_guard(pedido: dict) -> float:
    """
    Calcula total de pedido solo si cumple las condiciones básicas.
    """
    if not pedido.get("productos"):
        print("Pedido vacío")
        return 0.0

    if not pedido.get("usuario") or not pedido["usuario"].get("activo"):
        print("Usuario inválido")
        return 0.0

    # Lógica principal clara
    total = sum(p["precio"] for p in pedido["productos"])
    print(f"Total del pedido: ${total:.2f}")
    return total


# -------------------------------------------------------------------
# 5️⃣ GUARD CLAUSES CON EXCEPCIONES
# -------------------------------------------------------------------

def dividir(a: float, b: float) -> float:
    """
    Divide dos números usando guard clause para validar divisor.
    """
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b


# -------------------------------------------------------------------
# 6️⃣ REGLAS DE ORO
# -------------------------------------------------------------------
#
# - Valida errores o condiciones especiales al inicio
# - Retorna temprano o lanza excepción
# - Mantén la lógica principal sin indentación extra
# - Reduce anidamiento innecesario
# - Facilita comprensión y mantenimiento


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Guard clauses = cleaner, safer, more maintainable code
# Siempre aplica en funciones con múltiples condiciones
# Combínalas con funciones pequeñas para máxima claridad
