"""
refactor_funciones.py
=====================

Ejemplos prácticos de refactorización de funciones paso a paso.

Objetivos:
- Reducir complejidad ciclomática
- Aplicar SRP (una función = una responsabilidad)
- Mejorar nombres y legibilidad
- Usar guard clauses y técnicas de clean code
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO CLÁSICO: FUNCIÓN GIGANTE
# -------------------------------------------------------------------

# ❌ MAL: función que hace demasiadas cosas
def procesar_pedido_mal(pedido: dict) -> float:
    total = 0
    if pedido.get("productos"):
        for p in pedido["productos"]:
            if p.get("disponible"):
                if p.get("precio", 0) > 0:
                    if pedido.get("usuario") and pedido["usuario"].get("activo"):
                        total += p["precio"]
    # aplicar descuento
    if pedido.get("tipo_usuario") == "premium":
        total *= 0.85
    elif pedido.get("tipo_usuario") == "promo":
        total *= 0.9
    # imprimir resumen
    print(f"Total final: ${total:.2f}")
    return total

# Problemas:
# - Muy difícil de leer
# - Mezcla validación, cálculo, descuento e I/O
# - Difícil de testear


# -------------------------------------------------------------------
# 2️⃣ REFACTOR PASO 1: EXTRAER FUNCIONES PEQUEÑAS
# -------------------------------------------------------------------

def producto_valido(p: dict, usuario: dict) -> bool:
    """Valida si un producto puede agregarse al total."""
    return p.get("disponible", False) and p.get("precio", 0) > 0 and usuario.get("activo", False)

def calcular_total(productos: list[dict], usuario: dict) -> float:
    """Calcula el total de productos válidos."""
    return sum(p["precio"] for p in productos if producto_valido(p, usuario))

def aplicar_descuento(total: float, tipo_usuario: str) -> float:
    """Aplica descuento según tipo de usuario."""
    if tipo_usuario == "premium":
        return total * 0.85
    elif tipo_usuario == "promo":
        return total * 0.9
    return total

def imprimir_resumen(total: float) -> None:
    """Imprime resumen del pedido."""
    print(f"Total final: ${total:.2f}")


# -------------------------------------------------------------------
# 3️⃣ REFACTOR PASO 2: FUNCIÓN PRINCIPAL LIMPIA
# -------------------------------------------------------------------

def procesar_pedido(pedido: dict) -> float:
    """Orquesta todas las funciones pequeñas, limpio y legible."""
    usuario = pedido.get("usuario", {})
    productos = pedido.get("productos", [])

    # Guard clause: pedido vacío
    if not productos or not usuario.get("activo", False):
        print("Pedido inválido")
        return 0.0

    total = calcular_total(productos, usuario)
    total = aplicar_descuento(total, pedido.get("tipo_usuario", "normal"))
    imprimir_resumen(total)
    return total


# -------------------------------------------------------------------
# 4️⃣ REFACTOR PASO 3: USANDO STRATEGY PARA DESCUENTOS
# -------------------------------------------------------------------

from abc import ABC, abstractmethod

class DescuentoStrategy(ABC):
    @abstractmethod
    def aplicar(self, total: float) -> float:
        pass

class DescuentoNormal(DescuentoStrategy):
    def aplicar(self, total: float) -> float:
        return total

class DescuentoPromo(DescuentoStrategy):
    def aplicar(self, total: float) -> float:
        return total * 0.9

class DescuentoPremium(DescuentoStrategy):
    def aplicar(self, total: float) -> float:
        return total * 0.85

# Uso:
def procesar_pedido_strategy(pedido: dict, estrategia: DescuentoStrategy) -> float:
    usuario = pedido.get("usuario", {})
    productos = pedido.get("productos", [])

    if not productos or not usuario.get("activo", False):
        print("Pedido inválido")
        return 0.0

    total = calcular_total(productos, usuario)
    total = estrategia.aplicar(total)
    imprimir_resumen(total)
    return total


# -------------------------------------------------------------------
# 5️⃣ BENEFICIOS DE REFACTORIZAR FUNCIONES
# -------------------------------------------------------------------

# 1. Código más legible y profesional
# 2. Fácil de testear cada función por separado
# 3. Funciones pequeñas = menos complejidad
# 4. Fácil de extender (añadir nuevos tipos de descuento)
# 5. Aplicación clara de SRP
# 6. Guard clauses reducen anidamiento y confusión
# 7. Preparado para producción y mantenimiento en equipo


# -------------------------------------------------------------------
# 6️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Refactorizar funciones paso a paso = clean code real
# Siempre pregunta:
# - Esta función hace una sola cosa?
# - Se puede dividir en unidades más pequeñas?
# - La función principal queda clara y lineal?
# Si la respuesta es sí, el código está listo para producción y escalable
