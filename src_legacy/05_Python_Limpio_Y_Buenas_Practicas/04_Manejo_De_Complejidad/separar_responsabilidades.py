"""
separar_responsabilidades.py
============================

Este archivo enseña cómo aplicar el principio de **Responsabilidad Única (SRP)**
a funciones y clases en Python.

Problema típico:
- Funciones que hacen demasiadas cosas
- Clases que mezclan lógica de negocio, presentación e I/O
- Código difícil de testear y mantener

Solución:
- Dividir funciones y clases en unidades con una sola responsabilidad
- Cada función/clase debe tener un motivo único para cambiar
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO CLÁSICO: FUNCIÓN CON MULTIPLES RESPONSABILIDADES
# -------------------------------------------------------------------

# ❌ MAL
def procesar_y_guardar_pedido(pedido: dict) -> float:
    """
    1. Valida pedido
    2. Calcula total
    3. Aplica descuentos
    4. Guarda en base de datos
    5. Imprime resumen
    """
    # Validación
    if not pedido.get("productos"):
        print("Pedido vacío")
        return 0.0

    # Cálculo total
    total = sum(p["precio"] for p in pedido["productos"])

    # Aplicar descuento
    if pedido.get("tipo_usuario") == "premium":
        total *= 0.85
    elif pedido.get("tipo_usuario") == "promo":
        total *= 0.9

    # Guardar en base de datos
    print("Guardando pedido en DB...")  # Simulación

    # Imprimir resumen
    print(f"Total final: ${total:.2f}")

    return total

# Problema:
# - Mezcla validación, cálculo, I/O y persistencia
# - Difícil de testear y refactorizar


# -------------------------------------------------------------------
# 2️⃣ SOLUCIÓN: SEPARAR RESPONSABILIDADES
# -------------------------------------------------------------------

def validar_pedido(pedido: dict) -> bool:
    """Valida que el pedido tenga productos válidos."""
    return bool(pedido.get("productos"))

def calcular_total(pedido: dict) -> float:
    """Calcula el total del pedido."""
    return sum(p["precio"] for p in pedido["productos"])

def aplicar_descuento(total: float, tipo_usuario: str) -> float:
    """Aplica descuento según tipo de usuario."""
    if tipo_usuario == "premium":
        return total * 0.85
    elif tipo_usuario == "promo":
        return total * 0.9
    return total

def guardar_pedido(pedido: dict) -> None:
    """Guarda el pedido en la base de datos (simulado)."""
    print("Guardando pedido en DB...")

def imprimir_resumen(total: float) -> None:
    """Imprime resumen del pedido."""
    print(f"Total final: ${total:.2f}")


def procesar_pedido(pedido: dict) -> float:
    """Orquesta todas las funciones pequeñas, aplicando SRP."""
    if not validar_pedido(pedido):
        print("Pedido inválido")
        return 0.0

    total = calcular_total(pedido)
    total = aplicar_descuento(total, pedido.get("tipo_usuario", "normal"))
    guardar_pedido(pedido)
    imprimir_resumen(total)
    return total


# -------------------------------------------------------------------
# 3️⃣ SRP A NIVEL DE CLASES
# -------------------------------------------------------------------

# ❌ MAL: clase que hace todo
class PedidoMalo:
    def __init__(self, productos: list[dict], tipo_usuario: str):
        self.productos = productos
        self.tipo_usuario = tipo_usuario

    def procesar(self):
        # valida, calcula, aplica descuento, guarda, imprime
        pass

# ✅ BIEN: dividir responsabilidades en varias clases
class ValidadorPedido:
    """Valida pedidos según reglas de negocio."""
    def validar(self, pedido: dict) -> bool:
        return bool(pedido.get("productos"))

class CalculadorTotal:
    """Calcula totales de pedidos."""
    def calcular(self, pedido: dict) -> float:
        return sum(p["precio"] for p in pedido["productos"])

class Descuento:
    """Aplica descuentos según tipo de usuario."""
    def aplicar(self, total: float, tipo_usuario: str) -> float:
        if tipo_usuario == "premium":
            return total * 0.85
        elif tipo_usuario == "promo":
            return total * 0.9
        return total

class PedidoService:
    """Orquesta todas las responsabilidades del pedido."""
    def procesar(self, pedido: dict) -> float:
        if not ValidadorPedido().validar(pedido):
            print("Pedido inválido")
            return 0.0
        total = CalculadorTotal().calcular(pedido)
        total = Descuento().aplicar(total, pedido.get("tipo_usuario", "normal"))
        # Aquí podríamos agregar guardar/imprimir con clases separadas
        return total


# -------------------------------------------------------------------
# 4️⃣ REGLAS DE ORO SRP
# -------------------------------------------------------------------
#
# - Cada función/clase debe tener un único motivo para cambiar
# - No mezclar validación, cálculo, persistencia e I/O en la misma unidad
# - Funciones pequeñas + SRP = código mantenible y testeable
# - Facilita aplicar patrones como Strategy, Factory o Repository
# - Reduce acoplamiento y facilita refactorizaciones


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Separar responsabilidades es clave en clean code profesional
# Siempre pregunta:
# - ¿Esta función / clase tiene más de una razón para cambiar?
# Si la respuesta es sí → dividir en unidades más pequeñas y especializadas
