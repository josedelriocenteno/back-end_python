import pytest
from unittest.mock import Mock, MagicMock
from typing import List, Dict
from src.application.ports.usuario_repository import UsuarioRepository
from src.application.ports.producto_repository import ProductoRepository
from src.domain.value_objects.id_value import IDValue
from src.domain.entities.usuario import Usuario
from src.domain.entities.producto import Producto
from src.domain.value_objects.precio_value import PrecioValue

class MockUsuarioRepository(UsuarioRepository):
    """Mock reutilizable UsuarioRepository"""
    
    def __init__(self):
        self.usuarios_db: Dict[str, Usuario] = {}
        self.llamadas: List = []
    
    def add(self, usuario: Usuario) -> None:
        self.llamadas.append(("add", usuario.id))
        self.usuarios_db[str(usuario.id)] = usuario
    
    def get(self, id: IDValue['Usuario']) -> Usuario:
        self.llamadas.append(("get", id))
        usuario = self.usuarios_db.get(str(id))
        if not usuario:
            raise ValueError(f"Usuario no encontrado: {id}")
        return usuario
    
    def get_by_email(self, email: str) -> Usuario | None:
        self.llamadas.append(("get_by_email", email))
        for usuario in self.usuarios_db.values():
            if usuario.email == email:
                return usuario
        return None
    
    def update(self, usuario: Usuario) -> None:
        self.llamadas.append(("update", usuario.id))
        self.usuarios_db[str(usuario.id)] = usuario
    
    def delete(self, id: IDValue['Usuario']) -> bool:
        self.llamadas.append(("delete", id))
        return str(id) in self.usuarios_db.pop(str(id), None)
    
    def listar_todos(self) -> List[Usuario]:
        self.llamadas.append("listar_todos")
        return list(self.usuarios_db.values())
    
    def contar(self) -> int:
        self.llamadas.append("contar")
        return len(self.usuarios_db)

class MockProductoRepository(ProductoRepository):
    """Mock reutilizable ProductoRepository"""
    
    def __init__(self):
        self.productos_db: Dict[str, Producto] = {}
        self.llamadas: List = []
    
    def add(self, producto: Producto) -> None:
        self.llamadas.append(("add", producto.id))
        self.productos_db[str(producto.id)] = producto
    
    def get(self, id: IDValue['Producto']) -> Producto:
        self.llamadas.append(("get", id))
        producto = self.productos_db.get(str(id))
        if not producto:
            raise ValueError(f"Producto no encontrado: {id}")
        return producto
    
    def get_by_nombre(self, nombre: str, exacto: bool = False) -> List[Producto]:
        self.llamadas.append(("get_by_nombre", nombre, exacto))
        if exacto:
            return [p for p in self.productos_db.values() if p.nombre == nombre]
        return [p for p in self.productos_db.values() if nombre.lower() in p.nombre.lower()]
    
    def update_precio(self, id: IDValue['Producto'], nuevo_precio: PrecioValue) -> Producto:
        self.llamadas.append(("update_precio", id, nuevo_precio))
        if str(id) not in self.productos_db:
            raise ValueError(f"Producto no encontrado: {id}")
        # Crear nuevo producto con precio actualizado
        viejo = self.productos_db[str(id)]
        nuevo = Producto(viejo.id, viejo.nombre, nuevo_precio)
        self.productos_db[str(id)] = nuevo
        return nuevo
    
    def delete(self, id: IDValue['Producto']) -> bool:
        self.llamadas.append(("delete", id))
        return str(id) in self.productos_db.pop(str(id), None)
    
    def listar_todos(self) -> List[Producto]:
        self.llamadas.append("listar_todos")
        return list(self.productos_db.values())
    
    def listar_activos(self) -> List[Producto]:
        self.llamadas.append("listar_activos")
        return self.listar_todos()
    
    def contar(self) -> int:
        self.llamadas.append("contar")
        return len(self.productos_db)
    
    def assert_llamadas(self, esperadas: List):
        """Verifica secuencia llamadas"""
        assert self.llamadas == esperadas

# Fixtures pytest reutilizables
@pytest.fixture
def mock_usuario_repo():
    return MockUsuarioRepository()

@pytest.fixture
def mock_producto_repo():
    return MockProductoRepository()

@pytest.fixture
def usuario_test(mock_usuario_repo):
    user_id = IDValue['Usuario'].generar()
    usuario = Usuario(user_id, "Test User", "test@test.com")
    mock_usuario_repo.add(usuario)
    return usuario

@pytest.fixture
def producto_test(mock_producto_repo):
    prod_id = IDValue['Producto'].generar()
    producto = Producto(prod_id, "Test Product", PrecioValue.desde_float(99.99))
    mock_producto_repo.add(producto)
    return producto
