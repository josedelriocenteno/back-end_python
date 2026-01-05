from domain.entities.usuario import Usuario
from domain.entities.producto import Producto
from domain.value_objects.id_value import IDValue


class Pedido:
    def __init__(self, usuario: Usuario, lista_productos: list[Producto]):
        self._id = IDValue['Pedido'].generar()
        self.usuario = usuario
        self.lista_productos = lista_productos or []
        
    def total(self):
        return sum(producto.precio for producto in self.lista_productos)
    
    def agregar_producto(self, nuevo_producto: Producto):
        self.lista_productos.append(nuevo_producto)