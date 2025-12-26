# dataclasses_basico.py
# Uso básico de @dataclass en Python para simplificar clases

# ------------------------------------------------------------
# Las dataclasses permiten crear clases para almacenar datos
# sin escribir manualmente __init__, __repr__, __eq__, etc.
# Son ideales para DTOs, configuraciones, o entidades ligeras.
# ------------------------------------------------------------

from dataclasses import dataclass

# EJEMPLO 1: Clase normal (manual)
class ProductoManual:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __repr__(self):
        return f"ProductoManual(nombre={self.nombre}, precio={self.precio})"

producto = ProductoManual("Laptop", 1500)
print(producto)  # ProductoManual(nombre=Laptop, precio=1500)

# ------------------------------------------------------------
# EJEMPLO 2: Misma clase con @dataclass
@dataclass
class Producto:
    nombre: str
    precio: float

producto2 = Producto("Laptop", 1500)
print(producto2)  # Producto(nombre='Laptop', precio=1500)

# ------------------------------------------------------------
# EJEMPLO 3: Valores por defecto y tipos opcionales
@dataclass
class ProductoOpcional:
    nombre: str
    precio: float
    stock: int = 0  # valor por defecto

producto3 = ProductoOpcional("Teclado", 50)
print(producto3)  # ProductoOpcional(nombre='Teclado', precio=50, stock=0)

# ------------------------------------------------------------
# EJEMPLO 4: Comparaciones automáticas
@dataclass
class Punto:
    x: int
    y: int

p1 = Punto(1, 2)
p2 = Punto(1, 2)
p3 = Punto(2, 3)

print(p1 == p2)  # True
print(p1 == p3)  # False

# ------------------------------------------------------------
# CONSEJOS PRÁCTICOS PARA BACKEND/DATOS:
# 1. Úsalas para clases que solo guardan datos y no lógica pesada.
# 2. Combinadas con frozen=True se vuelven inmutables (ideal para DTOs).
# 3. Permiten tipado, comparaciones, y representaciones automáticas.
# 4. Evita mezclarlas con lógica de negocio compleja; separa responsabilidades.
# 5. Son tu mejor aliado para pipelines, APIs y pruebas unitarias.

# ------------------------------------------------------------
# EJEMPLO PRÁCTICO:
# Lista de productos para un endpoint de inventario
from typing import List

productos: List[Producto] = [
    Producto("Laptop", 1500),
    Producto("Teclado", 50),
    Producto("Mouse", 25)
]

for p in productos:
    print(f"{p.nombre} cuesta ${p.precio}")
