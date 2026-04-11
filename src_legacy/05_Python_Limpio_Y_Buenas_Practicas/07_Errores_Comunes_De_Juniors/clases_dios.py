"""
clases_dios.py
===============

Anti-patrón: Clases Dios (God Objects)

Objetivos:
- Identificar clases que hacen demasiado
- Mostrar problemas de acoplamiento y testabilidad
- Enseñar refactorización paso a paso usando SRP y composición
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO DE CLASE DIOS
# -------------------------------------------------------------------

# ❌ MAL: esta clase mezcla demasiadas responsabilidades
class PedidoDios:
    def __init__(self, usuario: dict, productos: list[dict]):
        self.usuario = usuario
        self.productos = productos

    def validar_usuario(self):
        return self.usuario.get("activo", False)

    def calcular_total(self):
        return sum(p.get("precio", 0) for p in self.productos if p.get("disponible"))

    def aplicar_descuento(self):
        total = self.calcular_total()
        tipo = self.usuario.get("tipo")
        if tipo == "premium":
            total *= 0.85
        elif tipo == "promo":
            total *= 0.9
        return total

    def guardar_db(self):
        print(f"Guardando pedido de {self.usuario['nombre']} con total {self.aplicar_descuento()}")

    def enviar_email(self):
        print(f"Enviando email a {self.usuario['email']}")

    def imprimir_resumen(self):
        print(f"Resumen: Total {self.aplicar_descuento()}, Usuario {self.usuario['nombre']}")


# Problemas:
# - Mezcla validación, cálculo, persistencia, comunicación y presentación
# - Difícil de testear
# - Difícil de extender sin romper otras partes
# - Violación clara de SRP


# -------------------------------------------------------------------
# 2️⃣ REFACTOR PASO 1: CLASES PEQUEÑAS CON SRP
# -------------------------------------------------------------------

class Usuario:
    """Representa un usuario del sistema."""
    def __init__(self, nombre: str, email: str, tipo: str, activo: bool = True):
        self.nombre = nombre
        self.email = email
        self.tipo = tipo
        self.activo = activo

class Producto:
    """Representa un producto en la tienda."""
    def __init__(self, nombre: str, precio: float, disponible: bool = True):
        self.nombre = nombre
        self.precio = precio
        self.disponible = disponible

class CalculadoraTotal:
    """Calcula el total de productos válidos."""
    @staticmethod
    def calcular(productos: list[Producto], usuario: Usuario) -> float:
        return sum(p.precio for p in productos if p.disponible and usuario.activo)

class EstrategiaDescuento:
    """Aplica descuento según tipo de usuario."""
    @staticmethod
    def aplicar(total: float, tipo_usuario: str) -> float:
        if tipo_usuario == "premium":
            return total * 0.85
        elif tipo_usuario == "promo":
            return total * 0.9
        return total

class RepositorioPedido:
    """Encapsula la persistencia del pedido."""
    @staticmethod
    def guardar(pedido: dict):
        print(f"Guardando pedido: {pedido}")

class ServicioEmail:
    """Encapsula envío de emails."""
    @staticmethod
    def enviar(usuario: Usuario, total: float):
        print(f"Enviando email a {usuario.email} con total {total}")


# -------------------------------------------------------------------
# 3️⃣ REFACTOR PASO 2: CLASE ORQUESTADORA (COMPOSICIÓN)
# -------------------------------------------------------------------

class Pedido:
    """Orquesta el procesamiento de pedidos usando composición."""
    def __init__(self, usuario: Usuario, productos: list[Producto]):
        self._usuario = usuario
        self._productos = productos
        self._total = 0.0

    def procesar(self):
        self._total = CalculadoraTotal.calcular(self._productos, self._usuario)
        self._total = EstrategiaDescuento.aplicar(self._total, self._usuario.tipo)
        RepositorioPedido.guardar(self._resumen())
        ServicioEmail.enviar(self._usuario, self._total)
        self._imprimir_resumen()

    def _resumen(self) -> dict:
        return {
            "usuario": self._usuario.nombre,
            "tipo": self._usuario.tipo,
            "total": self._total,
            "productos": [p.nombre for p in self._productos]
        }

    def _imprimir_resumen(self):
        print(f"Pedido procesado para {self._usuario.nombre}: Total ${self._total:.2f}")


# -------------------------------------------------------------------
# 4️⃣ BENEFICIOS DEL REFACTOR
# -------------------------------------------------------------------

# 1. Cada clase tiene una única responsabilidad
# 2. Pedido actúa como orquestador usando composición
# 3. Fácil de testear clases individualmente:
#    - Usuario
#    - Producto
#    - CalculadoraTotal
#    - EstrategiaDescuento
#    - RepositorioPedido
#    - ServicioEmail
# 4. Fácil de extender:
#    - Nuevas estrategias de descuento
#    - Nuevos servicios de comunicación
# 5. Código más legible, mantenible y profesional
# 6. Preparado para equipos grandes y producción

# -------------------------------------------------------------------
# 5️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Evitar clases dios = clean code profesional
# Principio:
# - Una clase = una sola responsabilidad (SRP)
# - Para nuevas funcionalidades, crear clases separadas o usar composición
# - Mantener orquestación en una clase controladora o servicio
