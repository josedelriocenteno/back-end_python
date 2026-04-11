import pytest
import sys
from pathlib import Path

# PYTHONPATH src/
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.domain.value_objects.id_value import IDValue
from src.domain.value_objects.precio_value import PrecioValue
from src.domain.entities.usuario import Usuario
from src.domain.entities.producto import Producto
from src.domain.entities.pedido import Pedido
from src.domain.strategies.descuento_strategy import (
    DescuentoNormal, DescuentoPromo, DescuentoPremium
)

class TestPedido:
    """Tests unitarios Pedido"""
    
    def setup_method(self):
        """Datos de prueba"""
        self.user_id = IDValue['Usuario'].generar()
        self.usuario = Usuario(
            id=self.user_id,
            nombre="Ana López", 
            email="ana@test.com"
        )
        
        self.prod1 = Producto(
            IDValue['Producto'].generar(),
            "Laptop",
            PrecioValue.desde_float(1000.0)
        )
        self.prod2 = Producto(
            IDValue['Producto'].generar(),
            "Mouse", 
            PrecioValue.desde_float(25.0)
        )
    
    def test_creacion_pedido_valido(self):
        """Crea pedido con productos"""
        productos_fs = frozenset([self.prod1, self.prod2])
        pedido_id = IDValue['Pedido'].generar()
        
        pedido = Pedido(
            id=pedido_id,
            usuario=self.usuario,
            productos=productos_fs
        )
        
        assert pedido.id == pedido_id
        assert pedido.usuario == self.usuario
        assert len(pedido.productos) == 2
        assert pedido.cantidad_productos == 2
    
    def test_subtotal_correcto(self):
        """Calcula subtotal sin descuento"""
        productos_fs = frozenset([self.prod1, self.prod2])
        pedido = Pedido(
            IDValue['Pedido'].generar(),
            self.usuario,
            productos_fs
        )
        assert pedido.subtotal == 1025.0
    
    def test_total_con_descuentos(self):
        """Strategy diferentes descuentos"""
        productos_fs = frozenset([self.prod1])
        pedido = Pedido(
            IDValue['Pedido'].generar(),
            self.usuario,
            productos_fs
        )
        
        assert pedido.total(DescuentoNormal()) == 1000.0
        assert pedido.total(DescuentoPromo()) == 900.0   # 10%
        assert pedido.total(DescuentoPremium()) == 850.0 # 15%
    
    def test_pedido_vacio_error(self):
        """Sin productos falla"""
        with pytest.raises(ValueError, match="al menos 1 producto"):
            Pedido(
                IDValue['Pedido'].generar(),
                self.usuario,
                frozenset()  # ← VACÍO
            )
    
    def test_frozenset_elimina_duplicados(self):
        """FrozenSet elimina duplicados"""
        productos_con_duplicado = frozenset([self.prod1, self.prod2, self.prod1])
        pedido = Pedido(
            IDValue['Pedido'].generar(),
            self.usuario,
            productos_con_duplicado
        )
        assert len(pedido.productos) == 2  # Duplicado eliminado
    
    def test_tiene_producto_correcto(self):
        """Verifica productos específicos"""
        pedido = Pedido(
            IDValue['Pedido'].generar(),
            self.usuario,
            frozenset([self.prod1, self.prod2])
        )
        assert pedido.tiene_producto(self.prod1.id) is True
        assert pedido.tiene_producto(self.prod2.id) is True
        
        id_falso = IDValue['Producto'].generar()
        assert pedido.tiene_producto(id_falso) is False
    
    def test_frozen_inmutable(self):
        """No se puede modificar"""
        productos_fs = frozenset([self.prod1])
        pedido = Pedido(
            IDValue['Pedido'].generar(),
            self.usuario,
            productos_fs
        )
        
        with pytest.raises(AttributeError):
            pedido.productos = frozenset()  # ❌ BLOQUEADO!
        
        with pytest.raises(AttributeError):
            pedido.usuario = Usuario(...)   # ❌ BLOQUEADO!
    
    def test_str_repr_correcto(self):
        """Representaciones legibles"""
        pedido = Pedido(
            IDValue['Pedido'].generar(),
            self.usuario,
            frozenset([self.prod1])
        )
        assert "productos" in str(pedido)
        assert "Pedido" in repr(pedido)
        assert str(pedido.subtotal) in str(pedido)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
