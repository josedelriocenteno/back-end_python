# str_repr.py
# Diferencia entre __str__ y __repr__ y cómo aplicarlo en un contexto backend profesional

class Producto:
    def __init__(self, sku: str, nombre: str, precio: float):
        self.sku = sku
        self.nombre = nombre
        self.precio = precio

    def __repr__(self):
        # Representación oficial, debe ser precisa y útil para desarrolladores
        return f"Producto(sku={self.sku!r}, nombre={self.nombre!r}, precio={self.precio!r})"

    def __str__(self):
        # Representación legible, para usuarios o logs
        return f"{self.nombre} (${self.precio})"

# ------------------------------------------------------------
# Uso práctico en backend
producto = Producto("p001", "Laptop", 1500.0)

# __repr__ se usa por ejemplo al inspeccionar objetos en consola o logs de debugging
print(repr(producto))  
# Output: Producto(sku='p001', nombre='Laptop', precio=1500.0)

# __str__ se usa en interfaces de usuario, logs de negocio o respuestas amigables
print(str(producto))   
# Output: Laptop ($1500.0)

# También se usa automáticamente en f-strings o print
print(f"Detalle del producto: {producto}")  
# Output: Detalle del producto: Laptop ($1500.0)

# ------------------------------------------------------------
# CONSEJOS:
# 1. Implementa siempre __repr__ para debugging y pruebas.
# 2. Implementa __str__ si el objeto será mostrado a usuarios o en logs de negocio.
# 3. Para dataclasses, __repr__ se genera automáticamente, pero __str__ puede personalizarse.
# 4. En backend, __repr__ es crucial para logs y trazabilidad de errores.
