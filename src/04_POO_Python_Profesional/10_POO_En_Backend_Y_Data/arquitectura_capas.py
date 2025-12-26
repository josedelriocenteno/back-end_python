# arquitectura_capas.py

"""
ARQUITECTURA POR CAPAS — DOMAIN / APPLICATION / INFRASTRUCTURE
=============================================================

Objetivo:
---------
Organizar el backend en capas claras para separar responsabilidades,
mejorar mantenibilidad y facilitar pruebas.

Capas:
------
1. DOMAIN: Modelo de negocio puro, reglas y entidades.
2. APPLICATION: Casos de uso, lógica de negocio específica.
3. INFRASTRUCTURE: Persistencia, APIs externas, servicios de terceros.
"""

# ============================================================
# 📌 DOMAIN
# ============================================================

from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Usuario:
    id: int
    nombre: str

@dataclass(frozen=True)
class Pedido:
    id: int
    usuario_id: int
    total: float

# ============================================================
# 📌 INFRASTRUCTURE
# ============================================================

class UsuarioRepository:
    """Capa de infraestructura para acceso a datos de Usuario"""
    def __init__(self):
        self._almacen = {}

    def guardar(self, usuario: Usuario):
        self._almacen[usuario.id] = usuario

    def obtener_por_id(self, id_: int):
        return self._almacen.get(id_)

    def listar_todos(self) -> List[Usuario]:
        return list(self._almacen.values())

class PedidoRepository:
    """Capa de infraestructura para acceso a datos de Pedido"""
    def __init__(self):
        self._almacen = {}

    def guardar(self, pedido: Pedido):
        self._almacen[pedido.id] = pedido

    def obtener_por_id(self, id_: int):
        return self._almacen.get(id_)

    def listar_todos(self) -> List[Pedido]:
        return list(self._almacen.values())

# ============================================================
# 📌 APPLICATION
# ============================================================

class PedidoService:
    """
    Capa de aplicación que maneja casos de uso de pedidos,
    sin depender de la implementación interna de repositorios.
    """
    def __init__(self, pedido_repo: PedidoRepository, usuario_repo: UsuarioRepository):
        self.pedido_repo = pedido_repo
        self.usuario_repo = usuario_repo

    def crear_pedido(self, usuario_id: int, total: float) -> Pedido:
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError(f"Usuario con id {usuario_id} no encontrado")
        nuevo_id = len(self.pedido_repo.listar_todos()) + 1
        pedido = Pedido(nuevo_id, usuario_id, total)
        self.pedido_repo.guardar(pedido)
        return pedido

    def obtener_pedidos_usuario(self, usuario_id: int) -> List[Pedido]:
        return [p for p in self.pedido_repo.listar_todos() if p.usuario_id == usuario_id]

# ============================================================
# 📌 EJEMPLO DE USO
# ============================================================

if __name__ == "__main__":
    # Infraestructura
    usuario_repo = UsuarioRepository()
    pedido_repo = PedidoRepository()

    # Crear usuarios
    usuario_repo.guardar(Usuario(1, "Alice"))
    usuario_repo.guardar(Usuario(2, "Bob"))

    # Aplicación
    servicio_pedidos = PedidoService(pedido_repo, usuario_repo)

    # Crear pedidos
    servicio_pedidos.crear_pedido(1, 100.0)
    servicio_pedidos.crear_pedido(2, 200.0)
    servicio_pedidos.crear_pedido(1, 50.0)

    # Listar pedidos de Alice
    pedidos_alice = servicio_pedidos.obtener_pedidos_usuario(1)
    print("Pedidos de Alice:", pedidos_alice)

    # Listar todos los pedidos
    print("Todos los pedidos:", pedido_repo.listar_todos())
