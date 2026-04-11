"""
docstrings_funciones.py
======================

Este archivo explica CÓMO documentar funciones en Python usando docstrings
con estilo Google o NumPy.

Los docstrings:
- describen la función, sus argumentos y retorno
- sirven para autocompletado y documentación automática
- reducen la necesidad de comentarios dentro de la función

Es diferente de comentar el código: un docstring explica la **API**, no el "cómo".
"""

# -------------------------------------------------------------------
# 1️⃣ REGLA GENERAL
# -------------------------------------------------------------------
#
# Una función debería tener un docstring si:
# - es pública
# - hace algo no trivial
# - es parte de una librería o módulo reutilizable

# Sintaxis recomendada: estilo Google o NumPy


# -------------------------------------------------------------------
# 2️⃣ EJEMPLO: ESTILO GOOGLE
# -------------------------------------------------------------------

def sumar(a: int, b: int) -> int:
    """
    Suma dos números enteros.

    Args:
        a (int): Primer número a sumar.
        b (int): Segundo número a sumar.

    Returns:
        int: La suma de `a` y `b`.

    Raises:
        ValueError: Si alguno de los valores no es entero.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Ambos valores deben ser enteros")
    return a + b


# -------------------------------------------------------------------
# 3️⃣ EJEMPLO: ESTILO NUMPY
# -------------------------------------------------------------------

def calcular_media(valores: list[float]) -> float:
    """
    Calcula la media aritmética de una lista de valores.

    Parameters
    ----------
    valores : list of float
        Lista de números a promediar.

    Returns
    -------
    float
        Media aritmética de los valores.

    Raises
    ------
    ValueError
        Si la lista está vacía.
    """
    if len(valores) == 0:
        raise ValueError("La lista no puede estar vacía")
    return sum(valores) / len(valores)


# -------------------------------------------------------------------
# 4️⃣ CUÁNDO USAR CADA ESTILO
# -------------------------------------------------------------------
#
# - Google: muy legible, usado en Google y muchos proyectos backend
# - NumPy: preferido en Data Science y ML, porque encaja con numpy, pandas y scikit-learn

# Lo importante: CONSISTENCIA en TODO el proyecto.


# -------------------------------------------------------------------
# 5️⃣ DOCSTRINGS Y TYPE HINTS
# -------------------------------------------------------------------
#
# Cuando tienes type hints, no es obligatorio repetirlos en el docstring,
# pero puedes añadir detalles adicionales.

def entrenar_modelo(datos: list[float], epochs: int) -> dict[str, float]:
    """
    Entrena un modelo de ejemplo sobre una lista de datos.

    Args:
        datos: Lista de números de entrenamiento.
        epochs: Número de iteraciones de entrenamiento.

    Returns:
        dict[str, float]: Diccionario con métricas de entrenamiento.
    """
    # Ejemplo simulado
    return {"loss_final": 0.05, "accuracy": 0.98}


# -------------------------------------------------------------------
# 6️⃣ ERRORES COMUNES
# -------------------------------------------------------------------

# ❌ MAL: docstring confuso o redundante
def dividir(a: int, b: int) -> float:
    """Divide a entre b y devuelve el resultado de la división"""
    return a / b

# Problema:
# - no aporta información nueva
# - no documenta excepciones
# - no explica parámetros


# ✅ BIEN: docstring claro y completo
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
# 7️⃣ REGLA DE ORO
# -------------------------------------------------------------------
#
# Un docstring debe responder:
# - Qué hace la función
# - Qué espera (args)
# - Qué devuelve (return)
# - Qué errores puede lanzar (raises)
#
# No documentes "cómo" hace la función, eso lo hace el código mismo.


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Buenas prácticas en docstrings:
# - consistencia en el estilo
# - incluir args, returns y raises
# - usar estilo Google o NumPy según el proyecto
# - no repetir información obvia del código
#
# Documentar bien = código más mantenible, colaborativo y profesional
