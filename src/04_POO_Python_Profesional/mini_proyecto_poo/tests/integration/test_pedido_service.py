import pytest
import sys
from pathlib import Path

# PYTHONPATH src/
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from unittest.mock import Mock, MagicMock
from src.application.services.pedido_service import PedidoService
from src.application.ports.usuario_repository import UsuarioRepository
from src.application.ports.producto_repository import ProductoRepository
from src.domain.value_objects.id_value import IDValue
from src.domain.entities.usuario import Usuario
from src.domain.entities.producto import Producto
from src.domain.value_objects.precio_value import PrecioValue
from src.domain.strategies.descuento_strategy import TipoDescuento

class TestPedidoService:
    """Tests integración PedidoService con mocks"""
    
    @pytest.fixture
    def usuario_mock(self):
        """Usuario mock"""
        user_id = IDValue['Usuario'].generar()
        return Usuario(
            id=user_id,
            nombre="Ana Test",
            email="ana@test.com"
        )
    
    @pytest.fixture
    def productos_mock(self):
        """Productos mock"""
        prod1 = Producto(
            IDValue['Producto'].generar(),
            "Laptop Test",
            PrecioValue.desde_float(1000.0)
        )
        prod2 = Producto(
            IDValue['Producto'].generar(),
            "Mouse Test", 
            PrecioValue.desde_float(50.0)
        )
        return [prod1, prod2]
    
    @pytest.fixture
    def usuario_repo_mock(self) -> UsuarioRepository:
        """Mock repositorio usuario"""
        mock = Mock(spec=UsuarioRepository)
        return mock
    
    @pytest.fixture
    def producto_repo_mock(self) -> ProductoRepository:
        """Mock repositorio producto"""
        mock = Mock(spec=ProductoRepository)
        return mock
    
    @pytest.fixture
    def service(self, usuario_repo_mock, producto_repo_mock):
        """Service con mocks"""
        return PedidoService(usuario_repo_mock, producto_repo_mock)
    
    def test_crear_pedido_exitoso(self, service, usuario_mock, productos_mock):
        """Crea pedido válido"""
        # Configurar mocks
        service.usuario_repo.get.return_value = usuario_mock
        service.producto_repo.get.side_effect = productos_mock
        
        resultado = service.crear_pedido(
            usuario_id=usuario_mock.id,
            productos_ids=[p.id for p in productos_mock],
            tipo_descuento="normal"
        )
        
        # Verificar
        assert resultado.usuario == usuario_mock
        assert len(resultado.productos) == 2
        service.usuario_repo.get.assert_called_once_with(usuario_mock.id)
        service.producto_repo.get.assert_has_calls([
            pytest.call(productos_mock[0].id),
            pytest.call(productos_mock[1].id)
        ])
    
    def test_calcular_total_previo(self, service, usuario_mock, productos_mock):
        """Vista previa sin crear"""
        service.usuario_repo.get.return_value = usuario_mock
        service.producto_repo.get.side_effect = productos_mock
        
        total = service.calcular_total_previo(
            usuario_id=usuario_mock.id,
            productos_ids=[productos_mock[0].id],
            tipo_descuento="promo"
        )
        
        assert total == 900.0  # 1000 * 0.9
        service.producto_repo.get.assert_called_once_with(productos_mock[0].id)
    
    def test_crear_pedido_sin_productos_error(self, service, usuario_mock):
        """Lista vacía falla"""
        service.usuario_repo.get.return_value = usuario_mock
        
        with pytest.raises(ValueError, match="al menos 1 producto"):
            service.crear_pedido(
                usuario_id=usuario_mock.id,
                productos_ids=[]  # ← VACÍO
            )
    
    def test_pedido_con_descuento_premium(self, service, usuario_mock, productos_mock):
        """Verifica descuento premium"""
        service.usuario_repo.get.return_value = usuario_mock
        service.producto_repo.get.side_effect = productos_mock
        
        resultado = service.crear_pedido(
            usuario_id=usuario_mock.id,
            productos_ids=[p.id for p in productos_mock],
            tipo_descuento=TipoDescuento.PREMIUM
        )
        
        # 1050 * 0.85 = 892.50
        assert resultado.subtotal == 1050.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
