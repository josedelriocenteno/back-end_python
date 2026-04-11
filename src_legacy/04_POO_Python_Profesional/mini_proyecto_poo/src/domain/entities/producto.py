from dataclasses import dataclass
from domain.value_objects.id_value import IDValue
from domain.value_objects.precio_value import PrecioValue

@dataclass(frozen=True)  # ← TOTALMENTE inmutable!
class Producto:
    id: IDValue['Producto']
    nombre: str
    precio: PrecioValue
    
    def __post_init__(self):
        self._validar_nombre()
    
    def _validar_nombre(self) -> None:
        nombre = self.nombre.strip()
        if len(nombre) < 1:
            raise ValueError("Nombre no puede estar vacío")
        if len(nombre) > 200:
            raise ValueError("Nombre muy largo (máx 200)")
    
    @property
    def nombre_limpio(self) -> str:
        """Nombre sin espacios extra"""
        return self.nombre.strip()
    
    def __str__(self) -> str:
        return f"{self.nombre_limpio} (${self.precio})"
    
    def __repr__(self) -> str:
        return (f"Producto(id={self.id.value}, "
                f"nombre='{self.nombre_limpio}', "
                f"precio={self.precio.value})")
