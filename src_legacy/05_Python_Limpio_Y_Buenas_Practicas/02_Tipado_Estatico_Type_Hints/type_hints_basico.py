"""
type_hints_basico.py
====================

Este archivo introduce los TYPE HINTS básicos en Python:
- int
- str
- float
- bool
- list
- dict

Los type hints:
- NO cambian cómo se ejecuta el código
- SÍ cambian cómo se entiende, se mantiene y se valida

En proyectos serios (backend, data, ML),
no usar type hints hoy es mala señal.
"""

# -------------------------------------------------------------------
# 1️⃣ ¿QUÉ SON LOS TYPE HINTS?
# -------------------------------------------------------------------
#
# Los type hints son ANOTACIONES.
#
# Le dicen a:
# - otros desarrolladores
# - editores (VSCode, PyCharm)
# - herramientas de análisis (mypy, pylint)
#
# qué tipo de datos se espera.
#
# Python sigue siendo dinámico,
# pero el código se vuelve mucho más seguro.


# -------------------------------------------------------------------
# 2️⃣ TIPOS PRIMITIVOS
# -------------------------------------------------------------------

# ❌ SIN TYPE HINTS
def sumar(a, b):
    return a + b

# ¿a y b son int? float? str?
# No lo sabemos hasta ejecutar.


# ✅ CON TYPE HINTS
def sumar(a: int, b: int) -> int:
    return a + b

# Ahora:
# - el lector entiende la intención
# - el editor avisa si usas mal la función


# -------------------------------------------------------------------
# 3️⃣ str, float, bool
# -------------------------------------------------------------------

def crear_usuario(nombre: str, edad: int, activo: bool) -> str:
    estado = "activo" if activo else "inactivo"
    return f"{nombre} ({edad}) - {estado}"


def calcular_iva(precio: float) -> float:
    return precio * 1.21


# -------------------------------------------------------------------
# 4️⃣ VARIABLES CON TYPE HINTS
# -------------------------------------------------------------------

# También se pueden tipar variables.
# Esto NO crea la variable, solo la documenta.

total: float = 0.0
contador: int = 0
usuario_activo: bool = True
nombre_usuario: str = "Ana"


# -------------------------------------------------------------------
# 5️⃣ LISTAS (list)
# -------------------------------------------------------------------
#
# list[T] indica una lista cuyos elementos son de tipo T

# ❌ SIN TIPO
numeros = [1, 2, 3]

# ✅ CON TIPO
numeros: list[int] = [1, 2, 3]

# Ejemplo con funciones
def calcular_media(valores: list[float]) -> float:
    return sum(valores) / len(valores)


# -------------------------------------------------------------------
# 6️⃣ DICCIONARIOS (dict)
# -------------------------------------------------------------------
#
# dict[Clave, Valor]

# ❌ SIN TIPO
usuario = {"id": 1, "nombre": "Juan"}

# ✅ CON TIPO
usuario: dict[str, str] = {
    "id": "1",
    "nombre": "Juan",
}

# Función con diccionario tipado
def obtener_nombre_usuario(usuario: dict[str, str]) -> str:
    return usuario["nombre"]


# -------------------------------------------------------------------
# 7️⃣ TIPADO VS VALIDACIÓN (IMPORTANTE)
# -------------------------------------------------------------------
#
# Los type hints:
# - NO validan en tiempo de ejecución
# - solo ayudan al análisis estático

def dividir(a: int, b: int) -> float:
    return a / b

# Esto es válido para Python:
# dividir("10", "2")  ❌
#
# El error lo detecta:
# - el editor
# - el linter
# - el revisor de código


# -------------------------------------------------------------------
# 8️⃣ BENEFICIOS REALES EN PROYECTOS
# -------------------------------------------------------------------
#
# Con type hints:
# - menos bugs
# - refactors más seguros
# - mejor autocompletado
# - onboarding más rápido
#
# En data / ML:
# - pipelines más claros
# - menos errores silenciosos


# -------------------------------------------------------------------
# 9️⃣ CUÁNDO USAR TYPE HINTS
# -------------------------------------------------------------------
#
# Regla profesional:
# - siempre en código nuevo
# - siempre en funciones públicas
# - siempre en servicios, pipelines, lógica de negocio
#
# Se pueden omitir en:
# - scripts rápidos
# - prototipos descartables


# -------------------------------------------------------------------
# 🔟 REGLA DE ORO
# -------------------------------------------------------------------
#
# Si una función NO se puede tipar fácilmente,
# probablemente su diseño es malo.
#
# El tipado te obliga a pensar mejor.


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Los type hints no son ruido.
# Son documentación viva.
#
# Aprender a usarlos bien
# te pone varios niveles por encima.
