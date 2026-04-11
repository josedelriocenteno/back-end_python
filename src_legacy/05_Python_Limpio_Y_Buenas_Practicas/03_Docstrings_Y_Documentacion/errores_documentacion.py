"""
errores_documentacion.py
========================

Este archivo muestra los ERRORES más frecuentes en documentación
y comentarios en Python, y cómo evitarlos.

Documentación inútil:
- confunde más que ayuda
- hace que linters y revisores pierdan tiempo
- reduce la mantenibilidad

Se cubre:
- comentarios redundantes
- docstrings vacíos o obvios
- documentar el "cómo" en lugar del "qué" o "por qué"
"""

# -------------------------------------------------------------------
# 1️⃣ COMENTARIOS OBVIOS O REDUNDANTES
# -------------------------------------------------------------------

# ❌ MAL
x = 10  # asigna 10 a x
y = x + 5  # suma 5 a x

# ✅ BIEN
x = 10  # límite máximo permitido por la API externa
y = x + 5  # ajustando valor según reglas de negocio

# Clave: los comentarios deben explicar **decisión**, **contexto**, **restricciones**, no repetir el código


# -------------------------------------------------------------------
# 2️⃣ DOCSTRINGS VACÍOS O CONFUSOS
# -------------------------------------------------------------------

# ❌ MAL
def foo():
    """Función foo"""
    return 42

# ❌ MAL
class Bar:
    """Clase Bar"""
    pass

# Problema:
# - No aportan información sobre propósito, uso, retorno o excepciones

# ✅ BIEN
def foo_correcta() -> int:
    """
    Calcula el valor máximo permitido según la política interna.

    Returns:
        int: Valor máximo permitido.
    """
    return 42

class BarCorrecta:
    """
    Clase que gestiona la cola de pedidos en memoria.

    Attributes:
        pedidos (list[Pedido]): Lista de pedidos pendientes.
    """
    def __init__(self):
        self.pedidos = []


# -------------------------------------------------------------------
# 3️⃣ DOCUMENTAR EL "CÓMO" EN LUGAR DEL "QUÉ"
# -------------------------------------------------------------------

# ❌ MAL
def dividir(a: int, b: int) -> float:
    """
    Divide a entre b usando / (división float)
    """
    return a / b

# Problema: el docstring dice lo que el código ya muestra, no aporta valor.

# ✅ BIEN
def dividir_segura(a: int, b: int) -> float:
    """
    Divide `a` entre `b`.

    Args:
        a (int): Dividendo.
        b (int): Divisor.

    Returns:
        float: Resultado de la división.

    Raises:
        ValueError: Si `b` es 0.
    """
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b


# -------------------------------------------------------------------
# 4️⃣ COMENTARIOS QUE SE VUELVEN OBSTÁCULOS
# -------------------------------------------------------------------

# ❌ MAL
# TODO: arreglar esto después
# FIXME: hack temporal
# NOTE: esto es raro
# (sin contexto ni plan de acción)
def procesar():
    pass

# ✅ BIEN
# TODO: migrar esta función al servicio de pedidos
# Se planea hacerlo en la versión 1.2 para unificar lógica
def procesar_correcto():
    pass


# -------------------------------------------------------------------
# 5️⃣ ERRORES COMUNES EN EQUIPOS
# -------------------------------------------------------------------
#
# - Documentar TODO sin contexto
# - Usar comentarios en otro idioma que el equipo no entiende
# - Escribir comentarios largos que repiten el código
# - Olvidar actualizar docstrings después de refactors


# -------------------------------------------------------------------
# 6️⃣ REGLAS DE ORO
# -------------------------------------------------------------------
#
# 1. Comenta **decisiones**, **contexto**, **restricciones**, nunca lo obvio
# 2. Docstrings = API y contrato, no implementación
# 3. Actualiza docstrings y comentarios con cada cambio
# 4. Usa estilo consistente (Google / NumPy)
# 5. Evita comentarios vacíos o redundantes


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Documentación inútil = ruido y pérdida de tiempo
# Buena documentación = claridad, mantenibilidad y profesionalidad
# Siempre documenta **qué hace**, **por qué**, **cómo usarlo**, pero nunca **cómo internamente**
