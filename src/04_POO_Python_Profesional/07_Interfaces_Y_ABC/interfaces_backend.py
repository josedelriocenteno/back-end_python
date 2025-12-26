# interfaces_backend.py
# Definición de interfaces para backend: repositorios y servicios
# Orientado a tu caso: backend de gestión de usuarios y roles

from abc import ABC, abstractmethod
from typing import List, Dict

# ------------------------------------------------------------
# INTERFACE DE REPOSITORIO
class RepositorioUsuarios(ABC):
    """
    Contrato para cualquier repositorio de usuarios.
    Permite intercambiar implementaciones sin modificar la lógica del servicio.
    """

    @abstractmethod
    def agregar(self, usuario: Dict) -> int:
        """Agrega un usuario y devuelve su ID"""
        pass

    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Dict:
        """Obtiene un usuario por ID"""
        pass

    @abstractmethod
    def listar(self) -> List[Dict]:
        """Lista todos los usuarios"""
        pass

# ------------------------------------------------------------
# INTERFACE DE SERVICIO
class ServicioUsuarios(ABC):
    """
    Contrato para la capa de servicios. 
    Define operaciones de negocio sin atarse a la implementación concreta del repositorio.
    """

    @abstractmethod
    def crear_usuario(self, nombre: str, rol: str) -> int:
        pass

    @abstractmethod
    def obtener_usuario(self, usuario_id: int) -> Dict:
        pass

    @abstractmethod
    def obtener_todos_los_usuarios(self) -> List[Dict]:
        pass

# ------------------------------------------------------------
# IMPLEMENTACIÓN CONCRETA EN MEMORIA
class RepositorioUsuariosMemoria(RepositorioUsuarios):
    def __init__(self):
        self._usuarios = {}
        self._contador = 1

    def agregar(self, usuario: Dict) -> int:
        usuario_id = self._contador
        usuario['id'] = usuario_id
        self._usuarios[usuario_id] = usuario
        self._contador += 1
        return usuario_id

    def obtener_por_id(self, usuario_id: int) -> Dict:
        return self._usuarios.get(usuario_id)

    def listar(self) -> List[Dict]:
        return list(self._usuarios.values())

class ServicioUsuariosImpl(ServicioUsuarios):
    """
    Servicio que implementa lógica de negocio para usuarios
    usando cualquier repositorio que cumpla el contrato.
    """
    def __init__(self, repo: RepositorioUsuarios):
        self.repo = repo

    def crear_usuario(self, nombre: str, rol: str) -> int:
        usuario = {"nombre": nombre, "rol": rol}
        return self.repo.agregar(usuario)

    def obtener_usuario(self, usuario_id: int) -> Dict:
        return self.repo.obtener_por_id(usuario_id)

    def obtener_todos_los_usuarios(self) -> List[Dict]:
        return self.repo.listar()

# ------------------------------------------------------------
# EJEMPLO DE USO PROFESIONAL
repo = RepositorioUsuariosMemoria()
servicio = ServicioUsuariosImpl(repo)

id_ana = servicio.crear_usuario("Ana", "admin")
id_luis = servicio.crear_usuario("Luis", "user")

print("Usuarios en el sistema:")
for u in servicio.obtener_todos_los_usuarios():
    print(u)

# ------------------------------------------------------------
# CONCEPTOS CLAVE:
# 1. Separación de capas: repositorio y servicio desacoplados.
# 2. Intercambiabilidad: se puede cambiar RepositorioUsuariosMemoria por SQL o NoSQL sin tocar ServicioUsuariosImpl.
# 3. Interfaces claras mejoran mantenibilidad y testing.
# 4. Patrón Dependency Injection aplicado: servicio recibe repositorio externo.
