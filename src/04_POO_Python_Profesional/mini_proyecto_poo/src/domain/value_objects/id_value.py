from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import uuid4, UUID

# Genérico para tipado fuerte
T = TypeVar('T')

@dataclass(frozen=True)  # ← Inmutable!
class IDValue(Generic[T]):
    value: UUID
    
    @classmethod
    def generar(cls) -> 'IDValue[T]':
        """Genera UUID único"""
        return cls(uuid4())
    
    @classmethod
    def desde_string(cls, id_str: str) -> 'IDValue[T]':
        """Desde JSON/DB"""
        return cls(UUID(id_str))
    
    @classmethod
    def desde_uuid(cls, uuid_obj: UUID) -> 'IDValue[T]':
        """Desde UUID directo"""
        return cls(uuid_obj)
    
    def __str__(self) -> str:
        """Para print/JSON"""
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}[{self.value}]"
    
    def __eq__(self, other: object) -> bool:
        """Compara valores"""
        if not isinstance(other, IDValue):
            return NotImplemented
        return self.value == other.value
    
    def __hash__(self) -> int:
        """Para dict/set"""
        return hash(self.value)
    
    @property
    def uuid(self) -> UUID:
        """Acceso directo"""
        return self.value
    
    @property
    def string(self) -> str:
        """Para DB/JSON"""
        return str(self.value)
