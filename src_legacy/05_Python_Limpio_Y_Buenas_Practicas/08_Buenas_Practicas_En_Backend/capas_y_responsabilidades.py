"""
capas_y_responsabilidades.py
=============================

Buenas prácticas en backend: separación clara de capas

Objetivos:
- Aplicar SRP en arquitectura backend
- Separar responsabilidades: presentación, dominio, persistencia
- Facilitar mantenimiento, escalabilidad y testabilidad
- Ejemplo práctico de un micro-backend de pedidos
"""

# -------------------------------------------------------------------
# 1️⃣ CAPAS CLÁSICAS EN BACKEND
# -------------------------------------------------------------------

# 1. Capa de presentación / API
#    - Interactúa con el cliente (HTTP, CLI, etc.)
#    - No contiene lógica de negocio
# 2. Capa de dominio / negocio
#    - Contiene lógica del negocio (reglas, cálculos, validaciones)
#    - SRP: cada clase o función hace solo lo que le corresponde
# 3. Capa de persistencia / infraestructura
#    - Base de datos, repositorios, almacenamiento
#    - No debe contener lógica de negocio


# -------------------------------------------------------------------
# 2️⃣ EJEMPLO DE CLASES Y CAPAS
# -------------------------------------------------------------------

# Capa de dominio
class Usuario:
    """Representa un usuario del sistema."""
    def __init__(self, nombre: str, activo: bool = True):
        self.nombre = nombre
        self.activo = activo

class Producto:
    """Representa un producto del sistema."""
    def __init__(self, nombre: str, precio: float, disponible: bool = True):
        self.nombre = nombre
        self.precio = precio
        self.disponible = disponible

class CalculadoraTotal:
    """Lógica de negocio: calcular total de productos válidos."""
    @staticmethod
    def calcular(productos: list[Producto], usuario: Usuario) -> float:
        return sum(p.precio for p in productos if p.disponible and usuario.activo)

# Capa de persistencia
class RepositorioPedido:
    """Encapsula persistencia de pedidos."""
    def __init__(self):
        self._almacen = []

    def guardar(self, pedido: dict):
        self._almacen.append(pedido)
        print(f"Pedido guardado: {pedido}")

    def listar(self) -> list[dict]:
        return self._almacen

# Capa de presentación / servicio
class PedidoService:
    """Orquesta operaciones: interactúa con dominio y persistencia."""
    def __init__(self, repo: RepositorioPedido):
        self._repo = repo

    def crear_pedido(self, usuario: Usuario, productos: list[Producto]) -> dict:
        total = CalculadoraTotal.calcular(productos, usuario)
        pedido = {
            "usuario": usuario.nombre,
            "total": total,
            "productos": [p.nombre for p in productos]
        }
        self._repo.guardar(pedido)
        return pedido

# -------------------------------------------------------------------
# 3️⃣ USO DEL SISTEMA
# -------------------------------------------------------------------

# Repositorio de pedidos
repo = RepositorioPedido()

# Servicio de pedidos
pedido_service = PedidoService(repo)

# Crear usuario y productos
usuario = Usuario("Juan")
productos = [Producto("Camisa", 20.0), Producto("Pantalón", 35.0)]

# Crear pedido usando servicio
pedido_final = pedido_service.crear_pedido(usuario, productos)
print(pedido_final)

# Listar pedidos guardados
print(repo.listar())


# -------------------------------------------------------------------
# 4️⃣ BENEFICIOS DE ESTA SEPARACIÓN
# -------------------------------------------------------------------

# 1. SRP aplicado: cada clase hace solo una cosa
# 2. Mantenibilidad: cambios en persistencia no afectan lógica
# 3. Testabilidad: se pueden testear dominio, persistencia y servicio por separado
# 4. Escalabilidad: fácil añadir nuevas capas (caching, logging, APIs)
# 5. Legibilidad: cada capa tiene responsabilidades claras
# 6. Preparado para equipos grandes y proyectos de producción


# -------------------------------------------------------------------
# 5️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Separar capas = código profesional
# Principio:
# - Presentación / API = interacción con usuario
# - Dominio = lógica de negocio
# - Persistencia = almacenamiento / DB
# Cada capa independiente = fácil de mantener, testear y escalar
