"""
docstrings_clases.py
====================

Este archivo enseña CÓMO documentar CLASES en Python usando docstrings
para crear APIs internas claras y mantenibles.

Los docstrings de clases:
- explican el propósito de la clase
- describen sus atributos y métodos principales
- ayudan a que otros desarrolladores entiendan la API sin leer todo el código
- funcionan con herramientas de documentación automática (Sphinx, MkDocs, pdoc)
"""

# -------------------------------------------------------------------
# 1️⃣ ESTRUCTURA DE UN DOCSTRING DE CLASE
# -------------------------------------------------------------------
#
# 1. Breve descripción de la clase
# 2. Atributos importantes (Attributes)
# 3. Métodos clave (Methods) opcional
#
# Estilo recomendado: Google o NumPy


# -------------------------------------------------------------------
# 2️⃣ EJEMPLO: ESTILO GOOGLE
# -------------------------------------------------------------------

class Usuario:
    """
    Representa un usuario del sistema.

    Attributes:
        id (int): Identificador único del usuario.
        nombre (str): Nombre completo del usuario.
        email (str): Dirección de correo electrónico.
    """

    def __init__(self, id: int, nombre: str, email: str):
        self.id = id
        self.nombre = nombre
        self.email = email

    def saludar(self) -> str:
        """
        Devuelve un saludo personalizado para el usuario.

        Returns:
            str: Mensaje de saludo.
        """
        return f"Hola, soy {self.nombre}"


# Uso:
usuario = Usuario(1, "Ana", "ana@mail.com")
print(usuario.saludar())  # "Hola, soy Ana"


# -------------------------------------------------------------------
# 3️⃣ EJEMPLO: ESTILO NUMPY
# -------------------------------------------------------------------

class Producto:
    """
    Representa un producto de la tienda.

    Attributes
    ----------
    id : int
        Identificador único del producto.
    nombre : str
        Nombre del producto.
    precio : float
        Precio del producto en USD.

    Methods
    -------
    aplicar_descuento(descuento: float) -> float
        Aplica un descuento al precio y devuelve el precio final.
    """

    def __init__(self, id: int, nombre: str, precio: float):
        self.id = id
        self.nombre = nombre
        self.precio = precio

    def aplicar_descuento(self, descuento: float) -> float:
        """
        Aplica un descuento al precio del producto.

        Parameters
        ----------
        descuento : float
            Valor del descuento a aplicar (0.0 a 1.0).

        Returns
        -------
        float
            Precio final después de aplicar el descuento.
        """
        return self.precio * (1 - descuento)


# -------------------------------------------------------------------
# 4️⃣ DOCSTRINGS PARA MÉTODOS ESENCIALES
# -------------------------------------------------------------------
#
# Métodos como __init__, __str__, __repr__, __eq__ también deben documentarse
# si aportan lógica relevante o afectan la API interna

class Pedido:
    """
    Representa un pedido realizado por un usuario.

    Attributes:
        id (int): Identificador único del pedido.
        usuario (Usuario): Usuario que realizó el pedido.
        productos (list[Producto]): Lista de productos incluidos en el pedido.
    """

    def __init__(self, id: int, usuario: Usuario, productos: list[Producto]):
        self.id = id
        self.usuario = usuario
        self.productos = productos

    def total(self) -> float:
        """
        Calcula el total del pedido sumando los precios de los productos.

        Returns:
            float: Total del pedido.
        """
        return sum(producto.precio for producto in self.productos)

    def __str__(self) -> str:
        """
        Representación legible del pedido.

        Returns:
            str: Resumen del pedido.
        """
        return f"Pedido {self.id} de {self.usuario.nombre}: {len(self.productos)} productos"


# -------------------------------------------------------------------
# 5️⃣ ERRORES COMUNES EN DOCSTRINGS DE CLASES
# -------------------------------------------------------------------

# ❌ MAL
class Cliente:
    """Clase Cliente"""
    # problema: no describe atributos ni propósito
    def __init__(self, nombre: str):
        self.nombre = nombre

# ❌ MAL
class ProductoMalo:
    """
    Representa un producto
    """
    # problema: atributos no documentados, métodos tampoco


# ✅ BIEN
class ClienteBueno:
    """
    Representa un cliente de la tienda.

    Attributes:
        id (int): Identificador único del cliente.
        nombre (str): Nombre completo del cliente.
        email (str): Email de contacto.
    """
    def __init__(self, id: int, nombre: str, email: str):
        self.id = id
        self.nombre = nombre
        self.email = email


# -------------------------------------------------------------------
# 6️⃣ REGLAS DE ORO
# -------------------------------------------------------------------
#
# - Documenta el propósito de la clase
# - Documenta atributos importantes (mínimo público)
# - Documenta métodos clave
# - Mantén estilo consistente (Google o NumPy)
# - No documentes cómo hace la clase lo que hace, eso se ve en el código
# - Las docstrings son parte de la API interna del equipo


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Docstrings de clase bien hechos:
# - facilitan el onboarding
# - permiten generar documentación automática
# - mejoran la mantenibilidad y calidad del código
# - son esenciales en proyectos profesionales de backend o ML
