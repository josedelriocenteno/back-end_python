from dataclasses import dataclass
from typing import FrozenSet
from decimal import Decimal
from domain.value_objects.id_value import IDValue
from domain.entities.usuario import Usuario
from domain.entities.producto import Producto
from domain.strategies.descuento_strategy import DescuentoStrategy

@dataclass(frozen=True)
class Pedido:
    id: IDValue['Pedido']
    usuario: Usuario
    productos: FrozenSet[Producto]  # ← Inmutable + únicos!
    
    def __post_init__(self):
        if not self.productos:
            raise ValueError("Pedido debe tener al menos 1 producto")
    
    @property
    def cantidad_productos(self) -> int:
        return len(self.productos)
    
    @property
    def subtotal(self) -> Decimal:
        """Precio sin descuento"""
        return sum(producto.precio.value for producto in self.productos)
    
    def total(self, strategy: DescuentoStrategy) -> Decimal:
        """Precio final con descuento"""
        return strategy.aplicar(self.subtotal)
    
    def tiene_producto(self, producto_id: IDValue['Producto']) -> bool:
        """Verifica si contiene producto específico"""
        return any(p.id == producto_id for p in self.productos)
    
    def __str__(self) -> str:
        subtotal_str = f"{self.subtotal:.2f}"
        return f"Pedido(id={self.id}, {len(self.productos)} productos, ${subtotal_str})"
    
    def __repr__(self) -> str:
        return f"Pedido(id={self.id.value}, usuario={self.usuario.nombre}, n_productos={len(self.productos)})"
