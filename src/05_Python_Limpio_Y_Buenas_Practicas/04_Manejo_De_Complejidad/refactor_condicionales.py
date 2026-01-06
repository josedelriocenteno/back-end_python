"""
refactor_condicionales.py
=========================

Este archivo muestra estrategias para refactorizar condicionales complejos
y mejorar la legibilidad, mantenibilidad y testabilidad del código.

Problema:
- if/elif/else largos y anidados
- lógica difícil de entender
- difícil de extender y probar

Soluciones:
- Guard clauses
- Diccionarios de dispatch
- Polimorfismo / Strategy Pattern
- Extracción a funciones pequeñas
"""

# -------------------------------------------------------------------
# 1️⃣ PROBLEMA: IF / ELIF LARGO
# -------------------------------------------------------------------

def calcular_descuento(tipo_usuario: str, total: float) -> float:
    """
    Calcula descuento según tipo de usuario.
    """
    if tipo_usuario == "normal":
        return total
    elif tipo_usuario == "promo":
        return total * 0.9
    elif tipo_usuario == "premium":
        return total * 0.85
    else:
        return total

# Problemas:
# - Difícil de mantener si agregamos nuevos tipos
# - Lógica dispersa
# - Más propenso a errores


# -------------------------------------------------------------------
# 2️⃣ SOLUCIÓN: USO DE DICCIONARIO DE DESPATCH
# -------------------------------------------------------------------

def calcular_descuento_dispatch(tipo_usuario: str, total: float) -> float:
    """
    Refactor usando diccionario de funciones (dispatch table)
    """
    descuentos = {
        "normal": lambda t: t,
        "promo": lambda t: t * 0.9,
        "premium": lambda t: t * 0.85,
    }

    # Retorna total si tipo no está en el diccionario
    return descuentos.get(tipo_usuario, lambda t: t)(total)


# -------------------------------------------------------------------
# 3️⃣ SOLUCIÓN: POLIMORFISMO / STRATEGY
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
def calcular_descuento_strategy(strategy: DescuentoStrategy, total: float) -> float:
    return strategy.aplicar(total)


# -------------------------------------------------------------------
# 4️⃣ EXTRACCIÓN A FUNCIONES PEQUEÑAS
# -------------------------------------------------------------------

# ❌ MAL: condicional gigante dentro de una función
def procesar_pedido_mal(pedido: dict) -> float:
    total = 0.0
    if pedido.get("productos"):
        for p in pedido["productos"]:
            if p["precio"] > 0:
                if p["disponible"]:
                    total += p["precio"]
    return total

# ✅ BIEN: separar responsabilidades en funciones pequeñas
def producto_valido(p: dict) -> bool:
    return p.get("precio", 0) > 0 and p.get("disponible", False)

def calcular_total_pedido(productos: list[dict]) -> float:
    return sum(p["precio"] for p in productos if producto_valido(p))


# -------------------------------------------------------------------
# 5️⃣ REGLAS DE ORO PARA REFACTORIZAR CONDICIONALES
# -------------------------------------------------------------------
#
# 1. Evita if/elif/else largos
# 2. Usa guard clauses para casos excepcionales
# 3. Considera diccionarios de dispatch para múltiples casos
# 4. Considera Strategy / Polimorfismo si la lógica varía por tipo
# 5. Extrae funciones pequeñas para cada condicional complejo
# 6. Mantén la función principal clara y lineal


# -------------------------------------------------------------------
# 6️⃣ BENEFICIOS
# -------------------------------------------------------------------
#
# - Código más legible y mantenible
# - Más fácil de testear
# - Fácil de extender para nuevos casos
# - Reduce bugs silenciosos


# -------------------------------------------------------------------
# CONCLUSIÓN
# -------------------------------------------------------------------
#
# Refactorizar condicionales = clean code profesional
# Siempre piensa en legibilidad, testabilidad y separación de responsabilidades
