from dataclasses import dataclass
import re
from domain.value_objects.id_value import IDValue

@dataclass
class Usuario:
    id: IDValue['Usuario']
    nombre: str
    email: str
    
    def __post_init__(self):
        if not self._validar_email():
            raise ValueError(f"Email inválido: {self.email}")
    
    def _validar_email(self) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, self.email))
    
    def __str__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}')"
