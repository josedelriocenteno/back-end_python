# comparadores.py
# Cómo definir comparadores personalizados para ordenar objetos en Python

from functools import total_ordering

@total_ordering  # Simplifica al definir un comparador principal y __eq__
class Producto:
    def __init__(self, nombre: str, precio: float, stock: int):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def __eq__(self, other):
        if not isinstance(other, Producto):
            return NotImplemented
        # Igualdad basada en nombre único (puede ser SKU en un caso real)
        return self.nombre == other.nombre

    def __lt__(self, other):
        if not isinstance(other, Producto):
            return NotImplemented
        # Orden natural: primero por precio, luego por stock si precios iguales
        if self.precio != other.precio:
            return self.precio < other.precio
        return self.stock < other.stock

    def __repr__(self):
        return f"Producto({self.nombre!r}, {self.precio}, {self.stock})"


# ------------------------------------------------------------
# Uso práctico: ordenar listas de productos

productos = [
    Producto("Laptop", 1200.0, 5),
    Producto("Teclado", 50.0, 100),
    Producto("Monitor", 200.0, 10),
    Producto("Laptop", 1200.0, 2),  # mismo nombre, precio igual, stock diferente
]

# sorted() utiliza __lt__ automáticamente
productos_ordenados = sorted(productos)
print(productos_ordenados)
# Output: [
#   Producto('Teclado', 50.0, 100),
#   Producto('Monitor', 200.0, 10),
#   Producto('Laptop', 1200.0, 2),
#   Producto('Laptop', 1200.0, 5)
# ]

# ------------------------------------------------------------
# CONSEJOS:
# 1. @total_ordering permite definir solo __eq__ y un comparador, el resto se infiere.
# 2. El orden de atributos en __lt__ refleja la prioridad de ordenación real del dominio.
# 3. Crucial para listas de precios, reportes, ranking de usuarios o productos en backend.
