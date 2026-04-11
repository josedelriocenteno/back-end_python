from abc import ABC, abstractmethod
from typing import Protocol
from decimal import Decimal
from enum import Enum

class TipoDescuento(str, Enum):
    """Tipos de descuento"""
    NORMAL = "normal"
    PROMO = "promo" 
    PREMIUM = "premium"

class DescuentoStrategy(Protocol):
    """Interface Strategy"""
    @abstractmethod
    def aplicar(self, subtotal: Decimal) -> Decimal:
        """Aplica descuento → precio final"""
        pass
    
    @abstractmethod
    def nombre(self) -> str:
        """Nombre legible"""
        pass

class DescuentoNormal(DescuentoStrategy):
    """0% descuento"""
    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal
    
    def nombre(self) -> str:
        return "Normal (0%)"

class DescuentoPromo(DescuentoStrategy):
    """10% descuento"""
    FACTOR = Decimal('0.90')  # 10% OFF
    
    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal * self.FACTOR
    
    def nombre(self) -> str:
        return "Promoción (10%)"

class DescuentoPremium(DescuentoStrategy):
    """15% descuento"""
    FACTOR = Decimal('0.85')  # 15% OFF
    
    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal * self.FACTOR
    
    def nombre(self) -> str:
        return "Premium (15%)"

# Factory para fácil uso
class DescuentoFactory:
    @staticmethod
    def obtener(tipo: TipoDescuento | str) -> DescuentoStrategy:
        """Crea strategy por tipo"""
        tipo_str = tipo.value if isinstance(tipo, TipoDescuento) else tipo
        strategies = {
            TipoDescuento.NORMAL: DescuentoNormal(),
            TipoDescuento.PROMO: DescuentoPromo(), 
            TipoDescuento.PREMIUM: DescuentoPremium()
        }
        return strategies.get(tipo_str, DescuentoNormal())
