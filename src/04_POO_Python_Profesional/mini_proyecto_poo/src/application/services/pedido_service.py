from typing import List
from decimal import Decimal
from domain.entities.pedido import Pedido
from domain.entities.usuario import Usuario
from domain.entities.producto import Producto
from domain.value_objects.id_value import IDValue
from domain.strategies.descuento_strategy import (
    DescuentoFactory, TipoDescuento
)
from application.ports.usuario_repository import UsuarioRepository
from application.ports.producto_repository import ProductoRepository

class PedidoService:
    def __init__(
        self,
        usuario_repo: UsuarioRepository,
        producto_repo: ProductoRepository
    ):
        self.usuario_repo = usuario_repo
        self.producto_repo = producto_repo
    
    def crear_pedido(
        self, 
        usuario_id: IDValue['Usuario'],
        productos_ids: List[IDValue['Producto']],
        tipo_descuento: TipoDescuento | str = TipoDescuento.NORMAL
    ) -> Pedido:
        """Crea pedido (sin persistir)"""
        
        # 1. Obtener usuario
        usuario = self.usuario_repo.get(usuario_id)
        
        # 2. Obtener productos
        if not productos_ids:
            raise ValueError("Debe incluir al menos 1 producto")
        
        productos = [
            self.producto_repo.get(pid) 
            for pid in productos_ids
        ]
        
        # 3. Crear pedido
        pedido = Pedido(
            id=IDValue['Pedido'].generar(),
            usuario=usuario,
            productos=frozenset(productos)
        )
        
        # 4. Calcular con descuento
        strategy = DescuentoFactory.obtener(tipo_descuento)
        total_final = pedido.total(strategy)
        
        print(f"✅ Pedido creado: {pedido} | Total: {total_final:.2f} | {strategy.nombre()}")
        
        return pedido
    
    def calcular_total_previo(
        self, 
        usuario_id: IDValue['Usuario'], 
        productos_ids: List[IDValue['Producto']],
        tipo_descuento: str = "normal"
    ) -> Decimal:
        """Vista previa sin crear pedido"""
        usuario = self.usuario_repo.get(usuario_id)
        productos = [self.producto_repo.get(pid) for pid in productos_ids]
        pedido_temp = Pedido(
            id=IDValue['Pedido'].generar(),
            usuario=usuario,
            productos=frozenset(productos)
        )
        strategy = DescuentoFactory.obtener(tipo_descuento)
        return pedido_temp.total(strategy)
