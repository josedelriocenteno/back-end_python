"""
typing_generics.py
==================

Este archivo explica el uso de TYPEVAR y GENERIC en Python.

Los generics permiten crear clases y funciones REUTILIZABLES,
con tipado explícito y seguro.

Útil para:
- Repositorios genéricos
- Colecciones de objetos del mismo tipo
- Funciones universales
"""

from typing import TypeVar, Generic, List

# -------------------------------------------------------------------
# 1️⃣ TypeVar: DEFINICIÓN
# -------------------------------------------------------------------
#
# TypeVar crea un marcador de tipo genérico.
# Es como decir:
# "Este valor puede ser de cualquier tipo T"
#
# Se usa para tipado en clases y funciones.

T = TypeVar("T")  # puede ser cualquier tipo
U = TypeVar("U")  # otro tipo independiente

# Ejemplo simple de función genérica
def repetir(valor: T, veces: int) -> List[T]:
    return [valor] * veces

# ✅ Uso:
lista_enteros = repetir(5, 3)        # [5, 5, 5], T=int
lista_strings = repetir("hola", 2)   # ["hola", "hola"], T=str


# -------------------------------------------------------------------
# 2️⃣ Generic: CLASES GENÉRICAS
# -------------------------------------------------------------------
#
# Se usa TypeVar + Generic para clases que funcionan con cualquier tipo.
# Ejemplo: Repositorio genérico

class Repositorio(Generic[T]):
    """
    Repositorio genérico para almacenar elementos de tipo T.
    """
    def __init__(self):
        self._items: List[T] = []

    def agregar(self, item: T) -> None:
        self._items.append(item)

    def listar(self) -> List[T]:
        return self._items

    def contar(self) -> int:
        return len(self._items)


# -------------------------------------------------------------------
# 3️⃣ USO DE LA CLASE GENÉRICA
# -------------------------------------------------------------------

# Repositorio de enteros
repo_enteros = Repositorio[int]()
repo_enteros.agregar(10)
repo_enteros.agregar(20)
print(repo_enteros.listar())  # [10, 20]

# Repositorio de strings
repo_strings = Repositorio[str]()
repo_strings.agregar("hola")
repo_strings.agregar("mundo")
print(repo_strings.listar())  # ["hola", "mundo"]


# -------------------------------------------------------------------
# 4️⃣ FUNCIONES GENÉRICAS MÁS COMPLEJAS
# -------------------------------------------------------------------

V = TypeVar("V")
K = TypeVar("K")

def intercambiar(tupla: tuple[K, V]) -> tuple[V, K]:
    """
    Invierte los elementos de una tupla.
    """
    return tupla[1], tupla[0]


# Uso:
resultado = intercambiar(("clave", 100))  # (100, "clave")


# -------------------------------------------------------------------
# 5️⃣ RESTRICCIONES DE TYPEVAR
# -------------------------------------------------------------------
#
# Puedes restringir los tipos que admite un TypeVar:

from numbers import Number

N = TypeVar("N", bound=Number)  # solo tipos numéricos

def sumar(a: N, b: N) -> N:
    return a + b

# ❌ Mal uso:
# sumar("hola", "mundo")  # type checker avisa

# ✅ Bien:
total = sumar(10, 5)  # 15


# -------------------------------------------------------------------
# 6️⃣ BENEFICIOS DE GENERICS
# -------------------------------------------------------------------
#
# - Reutilización de código sin perder tipado
# - Evita duplicar repositorios o contenedores
# - Mejora autocompletado y análisis estático
# - Facilita mantenimiento y refactor seguro


# -------------------------------------------------------------------
# 7️⃣ RELACIÓN CON POO PROFESIONAL
# -------------------------------------------------------------------
#
# En tus proyectos POO / IA:
# - IDValue[T] usa generics para tipar IDs de Usuario, Producto, Pedido
# - Repositorios genéricos evitan código repetido
# - Funciones genéricas permiten pipelines más seguras


# -------------------------------------------------------------------
# 8️⃣ REGLA DE ORO
# -------------------------------------------------------------------
#
# Si repites código para distintos tipos:
# 👉 probablemente necesites un Generic
#
# No lo hagas manualmente: usa TypeVar + Generic


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# TypeVar + Generic = tipado profesional
# Hace tu código flexible, seguro y fácil de mantener
# Se vuelve indispensable en proyectos medianos y grandes.
