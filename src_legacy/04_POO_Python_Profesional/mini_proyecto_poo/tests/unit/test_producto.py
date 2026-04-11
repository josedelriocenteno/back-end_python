import pytest
import sys
import os
from pathlib import Path

# PYTHONPATH para estructura src/
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.domain.value_objects.id_value import IDValue
from src.domain.value_objects.precio_value import PrecioValue
from src.domain.entities.producto import Producto

class TestProducto:
    """Tests unitarios Producto"""
    
    def test_creacion_producto_valido(self):
        """Crea producto válido"""
        producto = Producto(
            id=IDValue['Producto'].generar(),
            nombre="Laptop Dell",
            precio=PrecioValue.desde_float(1299.99)
        )
        assert producto.nombre == "Laptop Dell"
        assert producto.precio.value == 1299.99
    
    def test_nombre_se_autolimpi(self):
        """Propiedad limpia espacios"""
        producto = Producto(
            IDValue['Producto'].generar(),
            "  Laptop Dell  ",
            PrecioValue.desde_float(1299.99)
        )
        assert producto.nombre_limpio == "Laptop Dell"
        assert producto.nombre == "  Laptop Dell  "  # Original intacto
    
    def test_str_repr_correcto(self):
        """__str__ y __repr__ perfectos"""
        producto = Producto(
            IDValue['Producto'].generar(),
            "Mouse Logitech",
            PrecioValue.desde_float(29.99)
        )
        assert "Mouse Logitech ($29.99)" in str(producto)
        assert "Producto(id=" in repr(producto)
    
    def test_nombre_vacio_error(self):
        """Nombre vacío falla"""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            Producto(
                IDValue['Producto'].generar(),
                "",  # ← VACÍO
                PrecioValue.desde_float(10.0)
            )
    
    def test_nombre_muy_largo_error(self):
        """Nombre >200 falla"""
        nombre_largo = "A" * 201
        with pytest.raises(ValueError, match="muy largo"):
            Producto(
                IDValue['Producto'].generar(),
                nombre_largo,
                PrecioValue.desde_float(10.0)
            )
    
    def test_precio_cero_valido(self):
        """Precio 0 OK (regalo/promo)"""
        producto = Producto(
            IDValue['Producto'].generar(),
            "Regalo",
            PrecioValue.cero()
        )
        assert producto.precio.value == 0
    
    def test_frozen_inmutable(self):
        """No se puede modificar (frozen=True)"""
        producto = Producto(
            IDValue['Producto'].generar(),
            "Test",
            PrecioValue.desde_float(100.0)
        )
        
        with pytest.raises(AttributeError):
            producto.nombre = "Nuevo"  # ❌ BLOQUEADO!
        
        with pytest.raises(AttributeError):
            producto.precio = PrecioValue.desde_float(200.0)  # ❌ BLOQUEADO!
    
    def test_productos_diferentes_ids(self):
        """IDs diferentes → productos diferentes"""
        id1 = IDValue['Producto'].generar()
        id2 = IDValue['Producto'].generar()
        
        p1 = Producto(id1, "Test", PrecioValue.desde_float(10.0))
        p2 = Producto(id2, "Test", PrecioValue.desde_float(10.0))
        
        assert p1 != p2
    
    def test_mismo_precio_diferentes_objetos(self):
        """Comparación por valor"""
        p1 = Producto(
            IDValue['Producto'].generar(),
            "Test1",
            PrecioValue.desde_float(10.0)
        )
        p2 = Producto(
            IDValue['Producto'].generar(), 
            "Test2",
            PrecioValue.desde_float(10.0)
        )
        # Diferentes por ID/nombre aunque mismo precio

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
