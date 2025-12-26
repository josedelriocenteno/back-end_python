# dunder_avanzados.py
# Ejemplos prácticos de métodos especiales avanzados en Python: __call__, __len__, __iter__

class CarritoCompras:
    """
    Clase que simula un carrito de compras para un ecommerce.
    Demuestra uso de métodos especiales avanzados.
    """

    def __init__(self):
        # Lista interna para almacenar tuplas de (producto, cantidad)
        self._items = []

    def agregar_producto(self, nombre: str, cantidad: int = 1):
        """Agrega un producto al carrito"""
        self._items.append((nombre, cantidad))

    # ------------------------------------------------------------
    # __len__: permite usar len(objeto)
    def __len__(self):
        # Retorna el número total de productos en el carrito (sumando cantidades)
        return sum(cantidad for _, cantidad in self._items)

    # __iter__: permite iterar directamente sobre el objeto
    def __iter__(self):
        # Devuelve un iterador de los nombres de los productos
        for producto, cantidad in self._items:
            for _ in range(cantidad):
                yield producto

    # __call__: permite que la instancia sea "llamable" como función
    def __call__(self):
        """
        Retorna un resumen del carrito cuando se llama la instancia
        como si fuera una función.
        """
        resumen = {}
        for producto, cantidad in self._items:
            if producto in resumen:
                resumen[producto] += cantidad
            else:
                resumen[producto] = cantidad
        return resumen

# ------------------------------------------------------------
# Uso práctico:

carrito = CarritoCompras()
carrito.agregar_producto("Laptop", 2)
carrito.agregar_producto("Mouse", 3)
carrito.agregar_producto("Laptop", 1)

# Usando __len__
print(f"Número total de productos: {len(carrito)}")  # Output: 6

# Usando __iter__
print("Iterando sobre productos:")
for p in carrito:
    print(p)
# Output:
# Laptop
# Laptop
# Mouse
# Mouse
# Mouse
# Laptop

# Usando __call__
print("Resumen del carrito:")
print(carrito())  
# Output: {'Laptop': 3, 'Mouse': 3}

# ------------------------------------------------------------
# CONCEPTOS CLAVE:
# 1. __len__: útil para colecciones personalizadas.
# 2. __iter__: permite usar objetos en bucles for y comprehensions.
# 3. __call__: convierte la instancia en un objeto callable, muy útil para 
#    configuraciones, validaciones o servicios ligeros que actúan como funciones.
