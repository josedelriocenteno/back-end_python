# definicion_clases.py
# class, __init__, atributos
# Orientado a backend y proyectos reales de datos

"""
Este archivo introduce la definición de clases en Python y cómo crear objetos con estado y comportamiento.
En tu caso, vas a modelar entidades como Usuarios, Pedidos o Productos, cada una con sus atributos y métodos.
"""

# -------------------------------------------------
# 1. Definición básica de una clase
# -------------------------------------------------
# Sintaxis general:
# class NombreClase:
#     def __init__(self, atributos):
#         self.atributo = valor_inicial

class Usuario:
    """
    Clase que representa un usuario de un sistema.
    Atributos:
        nombre: str -> nombre del usuario
        email: str -> correo electrónico
    Métodos:
        saludar() -> devuelve un saludo personalizado
    """
    def __init__(self, nombre: str, email: str):
        # self.nombre y self.email son atributos de instancia
        self.nombre = nombre
        self.email = email

    def saludar(self) -> str:
        # Método de instancia
        return f"Hola, soy {self.nombre} y mi email es {self.email}"

# -------------------------------------------------
# 2. Crear objetos (instancias)
# -------------------------------------------------
usuario1 = Usuario("Ana", "ana@email.com")
usuario2 = Usuario("Luis", "luis@email.com")

print(usuario1.saludar())  # Hola, soy Ana y mi email es ana@email.com
print(usuario2.saludar())  # Hola, soy Luis y mi email es luis@email.com

# -------------------------------------------------
# 3. Explicación orientada a tu caso
# -------------------------------------------------
"""
- Cada usuario es un objeto independiente, con su propio estado.
- En sistemas backend, estas clases te permiten:
    1. Representar modelos de datos (Usuarios, Pedidos, Productos)
    2. Encapsular lógica dentro de métodos (ej: calcular total de un pedido)
    3. Mantener el código organizado y legible
"""

# -------------------------------------------------
# 4. Ejemplo extendido: Pedido
# -------------------------------------------------
class Pedido:
    """
    Clase para representar un pedido de un usuario.
    Atributos:
        usuario: Usuario -> quién realiza el pedido
        productos: list[float] -> lista de precios de productos
    Métodos:
        total() -> devuelve el total del pedido
    """
    def __init__(self, usuario: Usuario, productos: list[float]):
        self.usuario = usuario
        self.productos = productos

    def total(self) -> float:
        # Calcula el total del pedido
        return sum(self.productos)

pedido1 = Pedido(usuario1, [10, 20, 30])
pedido2 = Pedido(usuario2, [5, 15, 25, 35])

print(f"Total pedido1: {pedido1.total()}")  # 60
print(f"Total pedido2: {pedido2.total()}")  # 80

# -------------------------------------------------
# 5. Buenas prácticas y recomendaciones
# -------------------------------------------------
"""
1. Documenta siempre tus clases y métodos con docstrings.
2. Usa nombres claros y coherentes para atributos y métodos.
3. Evita colocar lógica compleja fuera de las clases; encapsula comportamiento dentro de métodos.
4. Python permite agregar atributos dinámicamente, pero es mejor definirlos en __init__ para claridad y mantenibilidad.
5. En backend y pipelines de datos, modela entidades como clases para luego integrarlas con bases de datos, repositorios y servicios.
"""
