# value_objects_backend.py
# Ejemplos de Value Objects aplicados en un contexto backend: IDs, DTOs y configuraciones

from dataclasses import dataclass, field
from typing import List, Optional

# ------------------------------------------------------------
# EJEMPLO 1: Value Object para un ID de usuario
@dataclass(frozen=True)
class UsuarioID:
    valor: str

# Uso en entidad
@dataclass(frozen=True)
class Usuario:
    id: UsuarioID
    nombre: str
    email: str

usuario = Usuario(UsuarioID("u1234"), "Alice", "alice@mail.com")
print(usuario)  # Usuario(id=UsuarioID(valor='u1234'), nombre='Alice', email='alice@mail.com')

# ------------------------------------------------------------
# EJEMPLO 2: Value Object para configuración inmutable
@dataclass(frozen=True)
class ConfiguracionApp:
    host: str
    puerto: int
    debug: bool = False

config = ConfiguracionApp(host="localhost", puerto=8080, debug=True)
print(config)  # ConfiguracionApp(host='localhost', puerto=8080, debug=True)

# ------------------------------------------------------------
# EJEMPLO 3: Value Object como DTO para transferencia de datos
@dataclass(frozen=True)
class ProductoDTO:
    sku: str
    nombre: str
    precio: float
    etiquetas: Optional[List[str]] = field(default_factory=list)

producto = ProductoDTO(sku="p001", nombre="Laptop", precio=1500.0, etiquetas=["Electrónica", "Computación"])
print(producto)

# ------------------------------------------------------------
# EJEMPLO 4: Comparación basada en valores
producto2 = ProductoDTO(sku="p001", nombre="Laptop", precio=1500.0, etiquetas=["Electrónica", "Computación"])
print(producto == producto2)  # True, porque todos los campos son iguales

# ------------------------------------------------------------
# CONSEJOS PRÁCTICOS:
# 1. Usa Value Objects para IDs, DTOs y configuraciones inmutables.
# 2. Facilitan testing porque los objetos son predecibles.
# 3. Ayudan a evitar efectos colaterales en pipelines y servicios backend.
# 4. Mantén la lógica de negocio separada de los Value Objects.
