# service_layer_pattern.py

"""
SERVICE LAYER PATTERN — Lógica de negocio desacoplada
====================================================

Este patrón es el SIGUIENTE NIVEL tras Repository.
Si Repository separa DATOS,
Service Layer separa la LÓGICA DE NEGOCIO.

Si no entiendes este patrón, acabarás con:
❌ controladores gordos
❌ lógica duplicada
❌ reglas de negocio desperdigadas
❌ sistemas imposibles de mantener

Esto es arquitectura REAL de backend.
No teoría.
"""

# ============================================================
# ❌ PROBLEMA REAL SIN SERVICE LAYER
# ============================================================

class PedidoController_MAL:
    def crear_pedido(self, usuario_id: int, total: float):
        # validaciones
        if total <= 0:
            raise ValueError("Total inválido")

        # lógica de negocio
        print("Calculando impuestos")
        print("Aplicando descuentos")

        # persistencia
        print("INSERT INTO pedidos ...")

        # side effects
        print("Enviando email")


"""
Problemas:
- El controlador hace TODO
- No se puede reutilizar lógica
- No se puede testear sin framework web
- Mezcla capas (violación brutal de SRP)
"""

# ============================================================
# 🧠 IDEA CLAVE DEL SERVICE LAYER
# ============================================================

"""
Separar claramente:
- CONTROLADOR → entrada/salida (HTTP, CLI, API)
- SERVICE → reglas de negocio
- REPOSITORY → acceso a datos

El Service Layer:
✅ Contiene TODA la lógica de negocio
✅ Orquesta repositorios
✅ Aplica reglas
✅ NO sabe nada de HTTP, FastAPI, Flask, etc.
"""

# ============================================================
# 🧱 ENTIDADES DE DOMINIO
# ============================================================

class Pedido:
    def __init__(self, id_: int, usuario_id: int, total: float):
        self.id = id_
        self.usuario_id = usuario_id
        self.total = total

    def __repr__(self):
        return f"Pedido(id={self.id}, usuario={self.usuario_id}, total={self.total})"


# ============================================================
# 📜 REPOSITORIO (CONTRATO)
# ============================================================

from abc import ABC, abstractmethod


class PedidoRepository(ABC):

    @abstractmethod
    def guardar(self, pedido: Pedido) -> None:
        pass

    @abstractmethod
    def listar(self) -> list[Pedido]:
        pass


# ============================================================
# 🧩 IMPLEMENTACIÓN SIMPLE DEL REPOSITORIO
# ============================================================

class PedidoRepositoryInMemory(PedidoRepository):
    def __init__(self):
        self._data: list[Pedido] = []

    def guardar(self, pedido: Pedido) -> None:
        self._data.append(pedido)

    def listar(self) -> list[Pedido]:
        return self._data


# ============================================================
# 🚀 SERVICE LAYER (EL CORAZÓN)
# ============================================================

class PedidoService:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def crear_pedido(self, id_: int, usuario_id: int, total: float) -> Pedido:
        # 🔒 reglas de negocio
        self._validar_total(total)

        total_final = self._aplicar_impuestos(total)
        total_final = self._aplicar_descuentos(total_final)

        pedido = Pedido(id_, usuario_id, total_final)

        self.repo.guardar(pedido)

        self._notificar(pedido)

        return pedido

    # ----------------------------
    # Reglas privadas del dominio
    # ----------------------------

    def _validar_total(self, total: float):
        if total <= 0:
            raise ValueError("El total debe ser mayor que 0")

    def _aplicar_impuestos(self, total: float) -> float:
        return total * 1.21  # IVA 21%

    def _aplicar_descuentos(self, total: float) -> float:
        if total > 100:
            return total * 0.9
        return total

    def _notificar(self, pedido: Pedido):
        print(f"Notificando creación de pedido {pedido.id}")


"""
CLAVES IMPORTANTES:
- El Service NO sabe nada de HTTP
- El Service NO imprime JSON
- El Service NO maneja requests/responses
"""

# ============================================================
# 🌐 CONTROLADOR (MUY FINO)
# ============================================================

class PedidoController:
    def __init__(self, service: PedidoService):
        self.service = service

    def post_pedido(self, data: dict):
        pedido = self.service.crear_pedido(
            id_=data["id"],
            usuario_id=data["usuario_id"],
            total=data["total"]
        )
        return {
            "id": pedido.id,
            "total": pedido.total
        }


"""
El controlador ahora:
✅ Solo traduce entrada/salida
✅ No contiene lógica de negocio
"""

# ============================================================
# 🧪 TESTING (DONDE BRILLA EL SERVICE LAYER)
# ============================================================

def test_crear_pedido():
    repo = PedidoRepositoryInMemory()
    service = PedidoService(repo)

    pedido = service.crear_pedido(1, 99, 200)

    assert pedido.total > 0
    assert len(repo.listar()) == 1


"""
Este test:
- No necesita FastAPI
- No necesita BD
- No necesita mocks complejos
"""

# ============================================================
# 🧠 SERVICE LAYER EN BACKEND REAL
# ============================================================

"""
En backend profesional:
- 1 Service por caso de uso
- Nombres claros:
    - CrearPedidoService
    - ProcesarPagoService
    - RegistrarUsuarioService

NO:
- MegaService de 2000 líneas
"""

# ============================================================
# 🧠 SERVICE LAYER EN DATA / IA
# ============================================================

"""
En data:
- Service = pipeline lógico
- Repositorios = fuentes de datos
"""

class FeatureService:
    def __init__(self, dataset_repo):
        self.repo = dataset_repo

    def generar_features(self):
        datos = self.repo.cargar()
        return [x * 2 for x in datos]


"""
Esto te permite:
- cambiar datasets
- testear pipelines
- reutilizar lógica
"""

# ============================================================
# ⚠️ ERRORES COMUNES
# ============================================================

"""
❌ Meter lógica en el controlador
❌ Meter lógica en el repositorio
❌ Services demasiado genéricos
❌ Services que hacen IO directo
"""

# ============================================================
# 🎯 CONCLUSIÓN (CLARA Y DURA)
# ============================================================

"""
Service Layer es OBLIGATORIO en sistemas serios.

Si no lo usas:
- código frágil
- lógica duplicada
- infierno de mantenimiento

Si lo usas bien:
- dominio limpio
- tests fáciles
- arquitectura profesional
- escalabilidad real

Este patrón marca la diferencia entre:
👉 programar
👉 y diseñar software
"""

