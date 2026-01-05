from dataclasses import dataclass
from value_objects.precio_value import PrecioValue
from domain.value_objects.id_value import IDValue

@dataclass
class Producto:
    _id: IDValue['Producto']
    nombre: str
    precio: PrecioValue

    def __repr__(self):
        return f'Producto(id={self._id}, nombre={self.nombre}, precio={self.precio})'