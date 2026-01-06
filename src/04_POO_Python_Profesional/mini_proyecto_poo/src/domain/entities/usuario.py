from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from domain.value_objects.id_value import IDValue
import re
from decimal import Decimal

@dataclass
class Usuario:
    id: IDValue['Usuario']
    nombre: str
    email: str
    
    def __post_init__(self):
        """Valida al crear"""
        self._validar_nombre()
        self._validar_email()
        print(f"✅ Usuario validado: {self.nombre}")
    
    def _validar_nombre(self) -> None:
        nombre = self.nombre.strip()
        if len(nombre) < 2:
            raise ValueError("Nombre debe tener al menos 2 caracteres")
        if len(nombre) > 100:
            raise ValueError("Nombre muy largo (máx 100)")
        self._nombre = nombre  # Guardar limpio
    
    def _validar_email(self) -> None:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.email):
            raise ValueError(f"Email inválido: {self.email}")
    
    def cambiar_nombre(self, nuevo_nombre: str) -> 'Usuario':
        """Inmutabilidad: devuelve NUEVO usuario"""
        return Usuario(
            id=self.id,
            nombre=nuevo_nombre.strip(),
            email=self.email
        )
    
    @property
    def nombre(self) -> str:
        return getattr(self, '_nombre', self.nombre.strip())
    
    def __str__(self) -> str:
        return f"Usuario(id={self.id}, {self.nombre} <{self.email}>)"
    
    def __repr__(self) -> str:
        return f"Usuario(id={self.id.value}, nombre='{self.nombre}')"
