# repositorios.py

"""
REPOSITORIOS — PERSISTENCIA DESACOPLADA
=======================================

Objetivo:
---------
Definir una capa que abstraiga la persistencia de datos,
permitiendo cambiar la fuente de datos sin afectar la
lógica de negocio. Esto facilita testeo y mantenimiento.

Principios:
-----------
- Cada repositorio se centra en un agregado o entidad
- Uso de interfaces o clases base para desacoplar
- Métodos CRUD claros y predecibles
"""

from modelos_dominio import Pedido, Usuario
from typing import List, Optional

# ============================================================
# 📌 REPOSITORIO DE PEDIDOS
# ============================================================

class PedidoRepository:
    """
    Repositorio para la entidad Pedido.
    Puede adaptarse a base de datos, memoria, o API externa.
    """

    def __init__(self):
        # Para simplicidad, usamos un diccionario en memoria
        self._almacen: dict[int, Pedido] = {}

    def guardar(self, pedido: Pedido) -> None:
        """
        Guarda o actualiza un pedido
        """
        self._almacen[pedido.id] = pedido

    def obtener_por_id(self, id_: int) -> Optional[Pedido]:
        """
        Recupera un pedido por su ID
        """
        return self._almacen.get(id_)

    def listar_todos(self) -> List[Pedido]:
        """
        Devuelve todos los pedidos
        """
        return list(self._almacen.values())

    def eliminar(self, id_: int) -> bool:
        """
        Elimina un pedido si existe
        """
        if id_ in self._almacen:
            del self._almacen[id_]
            return True
        return False

# ============================================================
# 📌 REPOSITORIO DE USUARIOS
# ============================================================

class UsuarioRepository:
    """
    Repositorio para la entidad Usuario.
    """

    def __init__(self):
        self._almacen: dict[int, Usuario] = {}

    def guardar(self, usuario: Usuario) -> None:
        self._almacen[usuario.id] = usuario

    def obtener_por_id(self, id_: int) -> Optional[Usuario]:
        return self._almacen.get(id_)

    def listar_todos(self) -> List[Usuario]:
        return list(self._almacen.values())

    def eliminar(self, id_: int) -> bool:
        if id_ in self._almacen:
            del self._almacen[id_]
            return True
        return False

# ============================================================
# 📌 EJEMPLO DE USO REAL
# ============================================================

if __name__ == "__main__":
    from modelos_dominio import Pedido, Usuario, Dinero

    repo_pedidos = PedidoRepository()
    repo_usuarios = UsuarioRepository()

    # Crear y guardar usuarios
    u1 = Usuario(1, "Alice")
    u2 = Usuario(2, "Bob")
    repo_usuarios.guardar(u1)
    repo_usuarios.guardar(u2)

    # Crear y guardar pedidos
    p1 = Pedido(1, u1.id, 150)
    p2 = Pedido(2, u2.id, 200)
    repo_pedidos.guardar(p1)
    repo_pedidos.guardar(p2)

    print("Todos los usuarios:", repo_usuarios.listar_todos())
    print("Todos los pedidos:", repo_pedidos.listar_todos())
