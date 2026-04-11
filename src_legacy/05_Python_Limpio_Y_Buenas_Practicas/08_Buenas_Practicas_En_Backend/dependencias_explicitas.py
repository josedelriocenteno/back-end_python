"""
dependencias_explicitas.py
==========================

Buenas prácticas: dependencias explícitas

Objetivos:
- Evitar “magia” al crear o usar objetos en Python
- Mejorar testabilidad, mantenibilidad y legibilidad
- Usar inyección de dependencias de forma clara
"""

# -------------------------------------------------------------------
# 1️⃣ PROBLEMA: DEPENDENCIAS IMPLÍCITAS
# -------------------------------------------------------------------

# ❌ MAL: la clase crea internamente dependencias
class PedidoServiceMagico:
    def __init__(self):
        self._repo = RepositorioPedidoMagico()  # depende directamente de la clase

    def crear_pedido(self, usuario: dict, productos: list[dict]) -> dict:
        total = sum(p["precio"] for p in productos)
        pedido = {"usuario": usuario["nombre"], "total": total}
        self._repo.guardar(pedido)
        return pedido

class RepositorioPedidoMagico:
    def guardar(self, pedido: dict):
        print(f"Guardando pedido en DB (magia): {pedido}")

# Problemas:
# 1. Difícil de testear: no puedes cambiar repo fácilmente
# 2. Acoplamiento fuerte: PedidoService depende de implementación concreta
# 3. Difícil de extender: si quieres cambiar la DB, debes tocar PedidoService


# -------------------------------------------------------------------
# 2️⃣ SOLUCIÓN: DEPENDENCIAS EXPLÍCITAS
# -------------------------------------------------------------------

# Definimos interfaz para repositorio (opcional, mejora claridad)
from abc import ABC, abstractmethod
from typing import Protocol, List, Dict

class RepositorioPedido(Protocol):
    """Interfaz de repositorio de pedidos."""
    @abstractmethod
    def guardar(self, pedido: Dict) -> None:
        ...

# Implementación concreta
class RepositorioPedidoDB:
    """Persistencia real (simulada)."""
    def __init__(self):
        self._almacen: List[Dict] = []

    def guardar(self, pedido: Dict) -> None:
        self._almacen.append(pedido)
        print(f"Pedido guardado en DB: {pedido}")

    def listar(self) -> List[Dict]:
        return self._almacen


# Servicio con dependencia explícita
class PedidoService:
    """Servicio de pedidos con inyección de dependencias clara."""
    def __init__(self, repo: RepositorioPedido):
        self._repo = repo  # dependencia inyectada desde afuera

    def crear_pedido(self, usuario: Dict, productos: List[Dict]) -> Dict:
        total = sum(p["precio"] for p in productos)
        pedido = {"usuario": usuario["nombre"], "total": total, "productos": productos}
        self._repo.guardar(pedido)
        return pedido


# -------------------------------------------------------------------
# 3️⃣ USO
# -------------------------------------------------------------------

# Crear repositorio explícitamente
repo = RepositorioPedidoDB()

# Inyectar dependencia en el servicio
pedido_service = PedidoService(repo)

usuario = {"nombre": "Ana"}
productos = [{"nombre": "Camisa", "precio": 20}, {"nombre": "Pantalón", "precio": 35}]

pedido_final = pedido_service.crear_pedido(usuario, productos)
print(pedido_final)

# Listar pedidos guardados
print(repo.listar())


# -------------------------------------------------------------------
# 4️⃣ BENEFICIOS
# -------------------------------------------------------------------

# 1. Código más testable: puedes inyectar un mock fácilmente
# 2. Menor acoplamiento: PedidoService no depende de implementación concreta
# 3. Más fácil de mantener y extender
# 4. Legible y explícito: se ve claramente qué dependencias necesita cada clase
# 5. Preparado para producción y equipos grandes


# -------------------------------------------------------------------
# 5️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Evitar magia = dependencias explícitas
# Principio:
# - Nunca crees dependencias dentro de la clase si se pueden inyectar
# - Usa inyección de dependencias para testabilidad y flexibilidad
# - Prefiere interfaces o protocolos para desacoplar implementación
