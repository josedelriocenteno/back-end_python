"""
errores_tipado_comunes.py
=========================

Este archivo muestra los ERRORES más frecuentes al usar type hints en Python
y cómo evitarlos.

Tipado mal usado = falsas seguridades + bugs silenciosos.

Se cubre:
- anotaciones incompletas
- usar Any sin control
- confundir Optional
- ignorar listas y diccionarios genéricos
"""

from typing import Any, List, Optional, Dict


# -------------------------------------------------------------------
# 1️⃣ USAR Any EN EXCESO
# -------------------------------------------------------------------

# ❌ MAL
def procesar_datos(datos: Any) -> Any:
    return datos

# Problemas:
# - pierde todo el beneficio del tipado
# - linter no avisa errores
# - confunde a otros devs

# ✅ BIEN
def procesar_datos_listas(datos: List[int]) -> List[int]:
    return [x * 2 for x in datos]


# -------------------------------------------------------------------
# 2️⃣ NO ESPECIFICAR CONTENIDO DE LISTAS / DICCIONARIOS
# -------------------------------------------------------------------

# ❌ MAL
numeros: list = [1, 2, 3]
usuarios: dict = {"id": 1, "nombre": "Ana"}

# Tipo ambiguo:
# - cualquier elemento es válido
# - pierde autocompletado y análisis estático

# ✅ BIEN
numeros: list[int] = [1, 2, 3]
usuarios: dict[str, str] = {"id": "1", "nombre": "Ana"}


# -------------------------------------------------------------------
# 3️⃣ CONFUNDIR Optional
# -------------------------------------------------------------------

# ❌ MAL
def obtener_usuario(id: int) -> str | None:  # Python 3.10+ ok, pero linter antiguo falla
    if id == 0:
        return None
    return "Juan"

# ❌ MAL: Optional pero sin manejar None
usuario: Optional[str] = None
# usuario.upper()  # crash si usuario es None

# ✅ BIEN
def obtener_usuario_seguro(id: int) -> Optional[str]:
    if id == 0:
        return None
    return "Juan"

usuario: Optional[str] = obtener_usuario_seguro(0)
if usuario is not None:
    print(usuario.upper())


# -------------------------------------------------------------------
# 4️⃣ TIPADO DE FUNCIONES CON MULTIPLES POSIBLES TIPOS
# -------------------------------------------------------------------

# ❌ MAL
def convertir(valor):
    return int(valor) if isinstance(valor, int) else str(valor)

# Sin type hints, no sabes qué devuelve

# ✅ BIEN
from typing import Union

def convertir_seguro(valor: Union[int, str]) -> Union[int, str]:
    if isinstance(valor, int):
        return valor
    return str(valor)


# -------------------------------------------------------------------
# 5️⃣ RETORNOS MAL TIPADOS
# -------------------------------------------------------------------

# ❌ MAL
def sumar(a: int, b: int):
    return str(a + b)  # type hint dice int, devuelve str

# Esto genera alertas en mypy o pylint

# ✅ BIEN
def sumar_correcto(a: int, b: int) -> int:
    return a + b


# -------------------------------------------------------------------
# 6️⃣ IGNORAR TYPE VARS EN FUNCIONES GENÉRICAS
# -------------------------------------------------------------------

from typing import TypeVar, Generic

T = TypeVar("T")

# ❌ MAL
def duplicar_lista(lista: list) -> list:
    return lista * 2

# ✅ BIEN
def duplicar_lista_generica(lista: list[T]) -> list[T]:
    return lista * 2


# -------------------------------------------------------------------
# 7️⃣ NO TIPAR CLAVES Y VALORES DE DICCIONARIOS
# -------------------------------------------------------------------

# ❌ MAL
config = {"timeout": 30, "modo": "dev"}

# ✅ BIEN
config: dict[str, int | str] = {"timeout": 30, "modo": "dev"}


# -------------------------------------------------------------------
# 8️⃣ CONFUNDIR LIST vs TUPLE
# -------------------------------------------------------------------

# ❌ MAL: lista para algo que no cambia
coordenadas = [10.0, 20.0]  # mutable

# ✅ BIEN: tuple para datos fijos
coordenadas: tuple[float, float] = (10.0, 20.0)


# -------------------------------------------------------------------
# 9️⃣ NO TIPAR VARIABLES LOCALES
# -------------------------------------------------------------------

# ❌ MAL
resultado = 0.0
valores = [1.0, 2.0]

# ✅ BIEN
resultado: float = 0.0
valores: list[float] = [1.0, 2.0]


# -------------------------------------------------------------------
# 🔟 REGLA DE ORO
# -------------------------------------------------------------------
#
# Siempre piensa:
# - Qué tipo debe entrar
# - Qué tipo debe salir
# - Qué pasa si es None o datos incompletos
#
# Nunca dejes Any salvo que sea estrictamente necesario.
# Un buen tipado = código más seguro, mantenible y profesional


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Los errores de tipado comunes:
# - confunden al equipo
# - generan bugs silenciosos
# - reducen la utilidad de linters y mypy
#
# Evitarlos = calidad profesional desde la base
