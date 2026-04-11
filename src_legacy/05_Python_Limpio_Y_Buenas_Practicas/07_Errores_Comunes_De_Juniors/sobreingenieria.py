"""
sobreingenieria.py
==================

Anti-patrón: Sobreingeniería

Objetivos:
- Detectar cuando el código se hace más complejo de lo necesario
- Mostrar ejemplos de complicación innecesaria
- Enseñar estrategias de simplificación profesional
"""

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO DE SOBREINGENIERÍA
# -------------------------------------------------------------------

# ❌ MAL: usar patrones, clases y herencia innecesaria para algo simple

from abc import ABC, abstractmethod

class CalculadoraDescuento(ABC):
    @abstractmethod
    def aplicar(self, total: float) -> float:
        pass

class DescuentoNormal(CalculadoraDescuento):
    def aplicar(self, total: float) -> float:
        return total

class DescuentoPromo(CalculadoraDescuento):
    def aplicar(self, total: float) -> float:
        return total * 0.9

class DescuentoPremium(CalculadoraDescuento):
    def aplicar(self, total: float) -> float:
        return total * 0.85

# Uso innecesario de herencia para un simple cálculo de descuento
def procesar_pedido(pedido: dict, estrategia: CalculadoraDescuento) -> float:
    total = sum(p.get("precio", 0) for p in pedido.get("productos", []))
    return estrategia.aplicar(total)

# Problema: simple descuento podría haberse hecho con una función simple:
def aplicar_descuento_simple(total: float, tipo: str) -> float:
    if tipo == "premium":
        return total * 0.85
    elif tipo == "promo":
        return total * 0.9
    return total

# -------------------------------------------------------------------
# 2️⃣ SÍNTOMAS DE SOBREINGENIERÍA
# -------------------------------------------------------------------

# 1. Clases y patrones aplicados sin necesidad real
# 2. Funciones complejas que podrían ser simples
# 3. Herencia o interfaces donde con composición o funciones basta
# 4. Configuración o abstracción excesiva para casos triviales
# 5. Dificultad de entender el flujo del código

# -------------------------------------------------------------------
# 3️⃣ RECOMENDACIONES PROFESIONALES
# -------------------------------------------------------------------

# 1. KISS (Keep It Simple, Stupid):
#    - No compliques lo que puede resolverse simple
# 2. YAGNI (You Ain’t Gonna Need It):
#    - No prepares funcionalidad para el futuro si no la necesitas ahora
# 3. Refactoriza hacia funciones pequeñas y claras
# 4. Prefiere composición sobre herencia innecesaria
# 5. Usa patrones de diseño **solo cuando aporten claridad**
# 6. Mantén código legible y fácil de testear

# -------------------------------------------------------------------
# 4️⃣ EJEMPLO DE REFACTORIZACIÓN SIMPLE
# -------------------------------------------------------------------

def procesar_pedido_limpio(pedido: dict) -> float:
    """
    Total final con descuento aplicado, sin complicaciones innecesarias.
    """
    productos = pedido.get("productos", [])
    total = sum(p.get("precio", 0) for p in productos)
    tipo_usuario = pedido.get("tipo_usuario", "normal")

    if tipo_usuario == "premium":
        return total * 0.85
    elif tipo_usuario == "promo":
        return total * 0.9
    return total

# Beneficios:
# - Código directo y legible
# - Fácil de testear
# - Menos mantenimiento
# - Evita sobreingeniería innecesaria

# -------------------------------------------------------------------
# 5️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Sobreingeniería = complejidad sin beneficio real
# Principios clave:
# - Mantén código simple (KISS)
# - No añadas abstracciones que no aporten valor (YAGNI)
# - Refactoriza para claridad y mantenibilidad
# - Aplica patrones de diseño **solo cuando resuelven un problema real**
