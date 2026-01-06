"""
refactor_clases.py
==================

Ejemplos de refactorización de clases complejas y simplificación de diseño.

Objetivos:
- Aplicar SRP (una clase = una sola responsabilidad)
- Usar encapsulación (_protected / __private)
- Preferir composición sobre herencia innecesaria
- Reducir acoplamiento y mejorar testabilidad
- Código limpio y profesional
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO CLÁSICO: CLASE DIOS
# -------------------------------------------------------------------

# ❌ MAL: clase que hace demasiado
class PedidoMal:
    def __init__(self, usuario: dict, productos: list[dict]):
        self.usuario = usuario
        self.productos = productos

    def validar_usuario(self):
        return self.usuario.get("activo", False)

    def calcular_total(self):
        total = 0
        for p in self.productos:
            if p.get("disponible") and p.get("precio", 0) > 0:
                total += p["precio"]
        return total

    def aplicar_descuento(self):
        if self.usuario.get("tipo") == "premium":
            return self.calcular_total() * 0.85
        elif self.usuario.get("tipo") == "promo":
            return self.calcular_total() * 0.9
        return self.calcular_total()

    def guardar_db(self):
        print("Guardando pedido en DB...")  # mezcla de lógica y persistencia

    def imprimir_resumen(self):
        print(f"Total: ${self.aplicar_descuento():.2f}")


# Problemas:
# - Mezcla validación, cálculo, descuento, persistencia e I/O
# - Difícil de testear
# - Difícil de extender
# - Violación de SRP


# -------------------------------------------------------------------
# 2️⃣ REFACTOR PASO 1: CLASES PEQUEÑAS Y RESPONSABILIDADES CLARAS
# -------------------------------------------------------------------

class Usuario:
    """Representa un usuario del sistema."""
    def __init__(self, nombre: str, tipo: str, activo: bool = True):
        self.nombre = nombre
        self.tipo = tipo
        self.activo = activo

class Producto:
    """Representa un producto de la tienda."""
    def __init__(self, nombre: str, precio: float, disponible: bool = True):
        self.nombre = nombre
        self.precio = precio
        self.disponible = disponible

class CalculadoraTotal:
    """Calcula total de productos válidos."""
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
    """Encapsula persistencia de pedidos."""
    @staticmethod
    def guardar(pedido: dict):
        print(f"Guardando pedido: {pedido}")


# -------------------------------------------------------------------
# 3️⃣ REFACTOR PASO 2: CLASE ORQUESTADORA (COMPOSICIÓN)
# -------------------------------------------------------------------

class Pedido:
    """Orquesta toda la operación de un pedido usando composición."""
    def __init__(self, usuario: Usuario, productos: list[Producto]):
        self._usuario = usuario              # encapsulado
        self._productos = productos          # encapsulado
        self._total = 0.0

    def procesar(self):
        """Procesa pedido: calcular total, aplicar descuento y persistir."""
        self._total = CalculadoraTotal.calcular(self._productos, self._usuario)
        self._total = EstrategiaDescuento.aplicar(self._total, self._usuario.tipo)
        RepositorioPedido.guardar(self._resumen())
        self._imprimir_resumen()

    def _resumen(self) -> dict:
        """Devuelve diccionario resumen del pedido (para persistencia)."""
        return {
            "usuario": self._usuario.nombre,
            "tipo": self._usuario.tipo,
            "total": self._total,
            "productos": [p.nombre for p in self._productos]
        }

    def _imprimir_resumen(self):
        """Imprime resumen del pedido en consola."""
        print(f"Pedido procesado para {self._usuario.nombre}: ${self._total:.2f}")


# -------------------------------------------------------------------
# 4️⃣ BENEFICIOS DEL REFACTOR
# -------------------------------------------------------------------

# 1. Cada clase tiene una sola responsabilidad
# 2. Fácil de testear de manera independiente:
#    - Usuario
#    - Producto
#    - CalculadoraTotal
#    - EstrategiaDescuento
#    - RepositorioPedido
# 3. Pedido actúa como orquestador, usando composición
# 4. Encapsulación protege atributos internos
# 5. Código limpio, legible y profesional
# 6. Fácil de extender: nuevas estrategias de descuento, nuevas fuentes de persistencia


# -------------------------------------------------------------------
# 5️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Refactorizar clases grandes = clean code real
# Siempre pregunta:
# - Esta clase tiene una sola responsabilidad?
# - Se pueden extraer partes en clases pequeñas?
# - Los métodos internos son privados si no deben usarse externamente?
# - Se usa composición en lugar de herencia innecesaria?
# Respuesta afirmativa = diseño profesional, limpio y escalable
