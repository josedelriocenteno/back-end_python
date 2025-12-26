# servicios.py

"""
SERVICIOS — CASOS DE USO
========================

Objetivo:
---------
Implementar la capa de aplicación (Application Layer)
que utiliza los modelos de dominio para ejecutar
la lógica de negocio real.

No confundir con:
❌ Modelo de dominio (entidad)
❌ Infraestructura (DB, APIs externas)
"""

from modelos_dominio import Pedido, Dinero

# ============================================================
# 📌 CASO DE USO: GESTIÓN DE PEDIDOS
# ============================================================

class PedidoService:
    """
    Servicio que encapsula operaciones sobre pedidos
    sin exponer la implementación interna del dominio
    """

    def __init__(self):
        # Normalmente esto sería un repositorio externo
        self._pedidos = {}  # dict simple {id: Pedido}

    # ----------------------------
    # CREAR PEDIDO
    # ----------------------------

    def crear_pedido(self, id_: int, usuario_id: int, total_base: float) -> Pedido:
        """
        Crea un nuevo pedido y lo almacena en memoria
        """
        if id_ in self._pedidos:
            raise ValueError(f"Pedido con id {id_} ya existe")

        pedido = Pedido(id_, usuario_id, total_base)
        self._pedidos[id_] = pedido
        return pedido

    # ----------------------------
    # OBTENER PEDIDO
    # ----------------------------

    def obtener_pedido(self, id_: int) -> Pedido:
        """
        Devuelve un pedido por su id
        """
        try:
            return self._pedidos[id_]
        except KeyError:
            raise ValueError(f"Pedido con id {id_} no encontrado")

    # ----------------------------
    # APLICAR DESCUENTO
    # ----------------------------

    def aplicar_descuento(self, id_: int, porcentaje: float) -> Pedido:
        pedido = self.obtener_pedido(id_)
        pedido.aplicar_descuento(porcentaje)
        return pedido

    # ----------------------------
    # CALCULAR TOTAL CON IVA
    # ----------------------------

    def total_con_iva(self, id_: int) -> float:
        pedido = self.obtener_pedido(id_)
        return pedido.total_con_iva

# ============================================================
# 📌 CASO DE USO: PEDIDO CON VALUE OBJECT DINERO
# ============================================================

class PedidoConDineroService:
    """
    Servicio que trabaja con objetos de dominio más seguros
    usando Value Objects
    """

    def __init__(self):
        self._pedidos = {}  # {id: PedidoConDinero}

    def crear_pedido(self, id_: int, usuario_id: int, total: Dinero):
        if id_ in self._pedidos:
            raise ValueError(f"Pedido con id {id_} ya existe")
        from modelos_dominio import PedidoConDinero
        pedido = PedidoConDinero(id_, usuario_id, total)
        self._pedidos[id_] = pedido
        return pedido

    def total_con_iva(self, id_: int) -> Dinero:
        pedido = self._pedidos.get(id_)
        if not pedido:
            raise ValueError(f"Pedido con id {id_} no encontrado")
        return pedido.aplicar_iva()

# ============================================================
# 📌 EJEMPLO DE USO REAL
# ============================================================

if __name__ == "__main__":
    service = PedidoService()
    p1 = service.crear_pedido(1, 42, 100)
    print(p1)
    service.aplicar_descuento(1, 10)
    print(f"Total con IVA: {service.total_con_iva(1)} EUR")

    # Con Value Object
    dinero = Dinero(200, "EUR")
    service_vo = PedidoConDineroService()
    p2 = service_vo.crear_pedido(2, 99, dinero)
    print(p2)
    print(f"Total con IVA: {service_vo.total_con_iva(2)}")
