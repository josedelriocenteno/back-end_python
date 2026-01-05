from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import uuid4, UUID

# Genérico para tipado: IDValue['Producto'], IDValue['Usuario'], etc.
T = TypeVar('T')

@dataclass(frozen=True)  # ← INMUTABLE!
class IDValue(Generic[T]):
    value: UUID
    
    @classmethod
    def generar(cls) -> 'IDValue[T]':
        """Genera nuevo UUID único"""
        return cls(uuid4())
    
    @classmethod
    def desde_string(cls, id_str: str) -> 'IDValue[T]':
        """Crea desde string (JSON/DB)"""
        return cls(UUID(id_str))
    
    @classmethod
    def desde_uuid(cls, uuid_obj: UUID) -> 'IDValue[T]':
        """Crea desde UUID directo"""
        return cls(uuid_obj)
    
    def __str__(self) -> str:
        """Para print/JSON"""
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"IDValue[{self.value}]"
    
    def __eq__(self, other: object) -> bool:
        """Compara IDs"""
        if not isinstance(other, IDValue):
            return False
        return self.value == other.value
    
    def __hash__(self) -> int:
        """Para sets/dicts"""
        return hash(self.value)
    
    @property
    def uuid(self) -> UUID:
        """Acceso directo"""
        return self.value
