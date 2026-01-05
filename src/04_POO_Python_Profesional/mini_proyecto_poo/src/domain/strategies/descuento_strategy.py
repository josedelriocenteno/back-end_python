from typing import Protocol
from decimal import Decimal
from abc import abstractmethod

class DescuentoStrategy(Protocol):
    @abstractmethod
    def aplicar(self, subtotal: Decimal) -> Decimal:
        pass
    
class DescuentoNormal(DescuentoStrategy):
    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal

class DescuentoPromo(DescuentoStrategy):
    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal * Decimal('0.90')

class DescuentoPremium(DescuentoStrategy):
    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal * Decimal('0.85')