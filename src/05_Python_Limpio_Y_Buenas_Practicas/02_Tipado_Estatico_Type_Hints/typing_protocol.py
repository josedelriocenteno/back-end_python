"""
typing_protocol.py
==================

Este archivo introduce PROTOCOLS de Python:

- Permiten definir "interfaces" sin herencia estricta
- Permiten tipado estático seguro
- Clave para diseño orientado a contratos

En Python 3.8+ se usan desde `typing.Protocol`.
En 3.11+ también se puede usar `from typing import Protocol` directamente.

Ventaja:
- cualquier objeto que cumpla el "contrato" funciona
- no requiere herencia explícita
"""

from typing import Protocol, runtime_checkable


# -------------------------------------------------------------------
# 1️⃣ EJEMPLO SIMPLE DE PROTOCOL
# -------------------------------------------------------------------

class SaludoProtocol(Protocol):
    """
    Define la interfaz para un objeto que puede saludar.
    """

    def saludar(self) -> str:
        ...


# Clase que cumple el protocolo
class Persona:
    def __init__(self, nombre: str):
        self.nombre = nombre

    def saludar(self) -> str:
        return f"Hola, soy {self.nombre}"


# Clase que NO cumple el protocolo
class ObjetoInvalido:
    def hablar(self) -> str:
        return "No saludo"


# -------------------------------------------------------------------
# 2️⃣ FUNCIONES QUE USAN PROTOCOLS
# -------------------------------------------------------------------

def presentar(entidad: SaludoProtocol) -> str:
    """
    Función que recibe cualquier objeto que cumpla SaludoProtocol
    """
    return entidad.saludar()


persona = Persona("Ana")
print(presentar(persona))  # ✅ "Hola, soy Ana"

# ❌ Objeto que no cumple
# objeto = ObjetoInvalido()
# print(presentar(objeto))  # mypy o linter avisa


# -------------------------------------------------------------------
# 3️⃣ BENEFICIO PRINCIPAL
# -------------------------------------------------------------------
#
# Protocols permiten:
# - escribir código flexible
# - tipar sin depender de herencia
# - evitar clases base vacías ("ABC" solo para tipado)


# -------------------------------------------------------------------
# 4️⃣ @runtime_checkable
# -------------------------------------------------------------------
#
# Permite comprobar en tiempo de ejecución si un objeto cumple un Protocol

@runtime_checkable
class VoladorProtocol(Protocol):
    def volar(self) -> None:
        ...


class Pajaro:
    def volar(self) -> None:
        print("El pájaro está volando")


class Avion:
    def volar(self) -> None:
        print("El avión está volando")


# Comprobación en tiempo de ejecución
print(isinstance(Pajaro(), VoladorProtocol))  # True
print(isinstance(Avion(), VoladorProtocol))   # True


# -------------------------------------------------------------------
# 5️⃣ PROTOCOLS Y GENERICS
# -------------------------------------------------------------------
#
# Se pueden combinar para contratos genéricos.

from typing import TypeVar, Generic

T = TypeVar("T")

class RepositorioProtocol(Protocol[T]):
    """
    Protocolo para un repositorio genérico.
    """

    def agregar(self, item: T) -> None:
        ...

    def listar(self) -> list[T]:
        ...


# Clase que cumple el protocolo
class RepositorioMemoria(Generic[T]):
    def __init__(self):
        self._items: list[T] = []

    def agregar(self, item: T) -> None:
        self._items.append(item)

    def listar(self) -> list[T]:
        return self._items


# Uso:
repo: RepositorioProtocol[int] = RepositorioMemoria[int]()
repo.agregar(1)
repo.agregar(2)
print(repo.listar())  # [1, 2]


# -------------------------------------------------------------------
# 6️⃣ CUÁNDO USAR PROTOCOLS
# -------------------------------------------------------------------
#
# - Cuando quieras definir un contrato, no heredar de ABC
# - Cuando múltiples clases diferentes puedan cumplir la misma API
# - En tests, para mocks y stubs tipados
# - En repositorios genéricos (como tu PedidoService)


# -------------------------------------------------------------------
# 7️⃣ REGLA DE ORO
# -------------------------------------------------------------------
#
# Si puedes definir un contrato y no necesitas herencia,
# usa Protocol.
#
# Combínalo con Generic para máxima flexibilidad.


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Protocols = Interfaces modernas y seguras en Python
# Mejoran tipado, testabilidad y mantenimiento
# Son la forma recomendada de "tipar por contrato" en proyectos profesionales
