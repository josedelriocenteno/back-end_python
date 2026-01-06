from abc import ABC, abstractmethod
from typing import List, Optional
from domain.value_objects.id_value import IDValue
from domain.entities.producto import Producto

class ProductoRepository(ABC):
    """Interface para acceso a productos"""
    
    @abstractmethod
    def add(self, producto: Producto) -> None:
        """
        Guarda nuevo producto
        Raises: ValueError si ya existe
        """
        pass
    
    @abstractmethod
    def get(self, id: IDValue['Producto']) -> Producto:
        """
        Obtiene producto por ID
        Raises: ValueError si no existe
        """
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str, exacto: bool = False) -> List[Producto]:
        """
        Busca productos por nombre
        exacto=True → nombre exacto
        """
        pass
    
    @abstractmethod
    def update_precio(self, id: IDValue['Producto'], nuevo_precio: PrecioValue) -> Producto:
        """
        Actualiza SOLO precio (inmutable)
        Returns: Producto actualizado
        """
        pass
    
    @abstractmethod
    def delete(self, id: IDValue['Producto']) -> bool:
        """Elimina producto. True si existía"""
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Producto]:
        """Todos los productos"""
        pass
    
    @abstractmethod
    def listar_activos(self) -> List[Producto]:
        """Productos disponibles (sin deleted)"""
        pass
    
    @abstractmethod
    def contar(self) -> int:
        """Total productos"""
        pass
