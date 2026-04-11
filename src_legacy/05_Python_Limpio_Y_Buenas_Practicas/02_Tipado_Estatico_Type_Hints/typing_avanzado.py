"""
typing_avanzado.py
==================

Este archivo cubre TIPADO AVANZADO en Python usando typing:
- Optional
- Union
- List
- Dict
- Tuple

Estas herramientas permiten describir mejor:
- casos límite
- datos incompletos
- estructuras complejas

Si usas Python profesionalmente,
ESTO no es opcional.
"""

from typing import Dict, List, Optional, Tuple, Union


# -------------------------------------------------------------------
# 1️⃣ Optional[T]
# -------------------------------------------------------------------
#
# Optional[T] significa:
# 👉 T O None
#
# Es equivalente a:
# Union[T, None]

# ❌ MAL (ambiguo)
def buscar_usuario_por_id(id_usuario: int):
    if id_usuario == 0:
        return None
    return "Juan"

# ¿Qué devuelve? ¿str? ¿None? No lo sabemos.


# ✅ BIEN
def buscar_usuario_por_id(id_usuario: int) -> Optional[str]:
    if id_usuario == 0:
        return None
    return "Juan"

# Ahora el contrato es claro:
# - o devuelve str
# - o devuelve None


# -------------------------------------------------------------------
# 2️⃣ Optional OBLIGA A PENSAR
# -------------------------------------------------------------------

usuario = buscar_usuario_por_id(0)

# ❌ MAL
# print(usuario.upper())  # posible error

# ✅ BIEN
if usuario is not None:
    print(usuario.upper())


# -------------------------------------------------------------------
# 3️⃣ Union[T1, T2]
# -------------------------------------------------------------------
#
# Union indica que algo puede ser de varios tipos.

def convertir_a_entero(valor: Union[str, int]) -> int:
    if isinstance(valor, int):
        return valor
    return int(valor)


# ¿Cuándo usar Union?
# - APIs
# - entrada de usuario
# - datos externos
# - parsing


# -------------------------------------------------------------------
# 4️⃣ List[T] vs list[T]
# -------------------------------------------------------------------
#
# Ambas son válidas en Python moderno (3.9+).
#
# list[int] → recomendado
# List[int] → compatible con versiones antiguas

numeros_1: list[int] = [1, 2, 3]
numeros_2: List[int] = [4, 5, 6]


# -------------------------------------------------------------------
# 5️⃣ Dict[K, V]
# -------------------------------------------------------------------

# Diccionario con claves string y valores float
precios: Dict[str, float] = {
    "producto_a": 10.5,
    "producto_b": 20.0,
}

# Diccionario más complejo
usuarios: Dict[int, Dict[str, str]] = {
    1: {"nombre": "Ana", "email": "ana@mail.com"},
    2: {"nombre": "Luis", "email": "luis@mail.com"},
}


# -------------------------------------------------------------------
# 6️⃣ Tuple[T1, T2, ...]
# -------------------------------------------------------------------
#
# Tuples:
# - tienen longitud fija
# - cada posición tiene significado

# ❌ MAL (lista para algo fijo)
coordenadas = [10.5, 20.3]

# ✅ BIEN
coordenadas: Tuple[float, float] = (10.5, 20.3)

# Ejemplo con retorno múltiple
def obtener_min_max(valores: list[int]) -> Tuple[int, int]:
    return min(valores), max(valores)


# -------------------------------------------------------------------
# 7️⃣ TIPADO DE ESTRUCTURAS COMPLEJAS
# -------------------------------------------------------------------

ResultadoBusqueda = Optional[Dict[str, Union[str, int]]]

def buscar_producto(id_producto: int) -> ResultadoBusqueda:
    if id_producto == 0:
        return None

    return {
        "id": id_producto,
        "nombre": "Producto X",
        "precio": 19,
    }

# Crear alias mejora la legibilidad y el mantenimiento.


# -------------------------------------------------------------------
# 8️⃣ ERRORES COMUNES
# -------------------------------------------------------------------

# ❌ MAL
def procesar(datos: list):
    pass

# No dice qué contiene la lista.


# ✅ BIEN
def procesar(datos: list[str]):
    pass


# -------------------------------------------------------------------
# 9️⃣ RELACIÓN CON BACKEND Y DATA / ML
# -------------------------------------------------------------------
#
# Backend:
# - respuestas HTTP opcionales
# - datos parciales
# - errores controlados
#
# Data / ML:
# - datasets incompletos
# - columnas opcionales
# - outputs variables
#
# El tipado hace todo esto explícito.


# -------------------------------------------------------------------
# 🔟 REGLA DE ORO
# -------------------------------------------------------------------
#
# Si usas None, DEBE aparecer en el tipo.
#
# Si algo puede fallar o faltar,
# el tipo debe reflejarlo.


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Tipado avanzado:
# - reduce errores silenciosos
# - mejora diseño
# - documenta casos límite
#
# No es burocracia.
# Es claridad.
