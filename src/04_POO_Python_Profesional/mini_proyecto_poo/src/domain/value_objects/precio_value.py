from dataclasses import dataclass
from decimal import Decimal
from typing import Union

@dataclass(frozen=True)  # ← Inmutable!
class PrecioValue:
    value: Decimal
    
    @classmethod
    def desde_float(cls, precio: float) -> 'PrecioValue':
        """Convierte float → Decimal seguro"""
        return cls(Decimal(str(precio)))  # str() evita errores float
    
    @classmethod
    def desde_string(cls, precio_str: str) -> 'PrecioValue':
        """Desde JSON/input usuario"""
        return cls(Decimal(precio_str))
    
    @classmethod
    def cero(cls) -> 'PrecioValue':
        """Precio 0"""
        return cls(Decimal('0'))
    
    def __str__(self) -> str:
        """Formato dinero"""
        return f"${self.value:.2f}"
    
    def __repr__(self) -> str:
        return f"PrecioValue({self.value})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PrecioValue):
            return NotImplemented
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    # Operaciones matemáticas
    def sumar(self, otro: 'PrecioValue') -> 'PrecioValue':
        """Suma inmutable"""
        return PrecioValue(self.value + otro.value)
    
    def multiplicar(self, factor: Decimal) -> 'PrecioValue':
        """Multiplica (descuentos/taxes)"""
        return PrecioValue(self.value * factor)
    
    @property
    def cantidad(self) -> Decimal:
        """Valor numérico puro"""
        return self.value
    
    @property
    def es_cero(self) -> bool:
        return self.value == 0
