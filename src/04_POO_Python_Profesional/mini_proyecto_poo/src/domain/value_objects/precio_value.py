from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class PrecioValue:
    value: Decimal
    
    @classmethod
    def desde_float(cls, precio: float) -> 'PrecioValue':
        return cls(Decimal(str(precio)))
    
    def __str__(self) -> str:
        return f"${self.value:.2f}"