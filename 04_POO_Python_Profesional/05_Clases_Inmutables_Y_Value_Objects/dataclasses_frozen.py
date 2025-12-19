# dataclasses_frozen.py
# Uso de dataclasses inmutables (frozen=True) para crear Value Objects

# ------------------------------------------------------------
# Los Value Objects representan entidades que se comparan
# por sus valores y no por identidad, son inmutables y predecibles.
# Ideal para IDs, coordenadas, configuraciones, DTOs.
# ------------------------------------------------------------

from dataclasses import dataclass

# EJEMPLO 1: Dataclass inmutable
@dataclass(frozen=True)
class Coordenada:
    x: float
    y: float

c1 = Coordenada(10.0, 20.0)
print(c1)  # Coordenada(x=10.0, y=20.0)

# Intentar modificar lanzará error
try:
    c1.x = 15.0
except Exception as e:
    print(f"Error: {e}")  # Error: cannot assign to field 'x'

# ------------------------------------------------------------
# EJEMPLO 2: Comparación de Value Objects
c2 = Coordenada(10.0, 20.0)
c3 = Coordenada(5.0, 5.0)

print(c1 == c2)  # True, porque los valores son iguales
print(c1 == c3)  # False

# ------------------------------------------------------------
# EJEMPLO 3: Uso de Value Object en Backend
@dataclass(frozen=True)
class UsuarioID:
    id: str

@dataclass(frozen=True)
class Usuario:
    id: UsuarioID
    nombre: str
    email: str

usuario1 = Usuario(UsuarioID("1234"), "Alice", "alice@mail.com")
usuario2 = Usuario(UsuarioID("1234"), "Alice", "alice@mail.com")

# Comparación basada en valores, no en referencias
print(usuario1 == usuario2)  # True

# ------------------------------------------------------------
# CONSEJOS PRÁCTICOS:
# 1. Frozen dataclasses son perfectas para datos que no deberían cambiar.
# 2. Úsalas para Value Objects, claves de negocio y DTOs.
# 3. Facilitan testing porque son predictibles y comparables.
# 4. Se integran bien en pipelines, caches y logs.
# 5. No mezclar con lógica mutable compleja; separa responsabilidades.
