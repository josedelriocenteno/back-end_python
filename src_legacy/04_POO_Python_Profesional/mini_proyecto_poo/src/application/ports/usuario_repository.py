from abc import ABC, abstractmethod
from typing import Optional, List
from domain.value_objects.id_value import IDValue
from domain.entities.usuario import Usuario

class UsuarioRepository(ABC):
    """Interface para acceso a usuarios"""
    
    @abstractmethod
    def add(self, usuario: Usuario) -> None:
        """
        Guarda nuevo usuario
        Raises: ValueError si ya existe
        """
        pass
    
    @abstractmethod
    def get(self, id: IDValue['Usuario']) -> Usuario:
        """
        Obtiene usuario por ID
        Raises: ValueError si no existe
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Busca por email único"""
        pass
    
    @abstractmethod
    def update(self, usuario: Usuario) -> None:
        """Actualiza usuario existente"""
        pass
    
    @abstractmethod
    def delete(self, id: IDValue['Usuario']) -> bool:
        """Elimina usuario. True si existía"""
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Usuario]:
        """Todos los usuarios"""
        pass
    
    @abstractmethod
    def contar(self) -> int:
        """Total usuarios"""
        pass
