# contratos_clases.py
# Cómo diseñar APIs internas claras y seguras usando clases en Python
# Orientado a tu caso: backend de gestión de usuarios y roles

from abc import ABC, abstractmethod
from typing import List, Dict

# ------------------------------------------------------------
# Interfaz / Contrato para un repositorio de usuarios

class RepositorioUsuarios(ABC):
    """
    Define el contrato que cualquier implementación de repositorio de usuarios debe cumplir.
    Esto asegura que distintas implementaciones (en memoria, SQL, NoSQL) sean intercambiables.
    """

    @abstractmethod
    def agregar_usuario(self, usuario: Dict) -> None:
        """Agrega un usuario al repositorio"""
        pass

    @abstractmethod
    def obtener_usuario(self, usuario_id: int) -> Dict:
        """Retorna la información de un usuario por su ID"""
        pass

    @abstractmethod
    def listar_usuarios(self) -> List[Dict]:
        """Devuelve la lista de todos los usuarios"""
        pass

# ------------------------------------------------------------
# Implementación concreta en memoria

class RepositorioUsuariosMemoria(RepositorioUsuarios):
    def __init__(self):
        self._usuarios = {}
        self._id_counter = 1

    def agregar_usuario(self, usuario: Dict) -> None:
        usuario['id'] = self._id_counter
        self._usuarios[self._id_counter] = usuario
        self._id_counter += 1
        print(f"Usuario agregado: {usuario}")

    def obtener_usuario(self, usuario_id: int) -> Dict:
        return self._usuarios.get(usuario_id, None)

    def listar_usuarios(self) -> List[Dict]:
        return list(self._usuarios.values())

# ------------------------------------------------------------
# Uso de la API interna de manera profesional

def crear_y_listar_usuarios(repo: RepositorioUsuarios):
    repo.agregar_usuario({"nombre": "Ana", "rol": "admin"})
    repo.agregar_usuario({"nombre": "Luis", "rol": "user"})
    
    print("Lista de usuarios:")
    for usuario in repo.listar_usuarios():
        print(usuario)

# Probando
repo_memoria = RepositorioUsuariosMemoria()
crear_y_listar_usuarios(repo_memoria)

# ------------------------------------------------------------
# CONCEPTOS CLAVE:
# 1. Contratos claros evitan errores cuando múltiples desarrolladores trabajan sobre el mismo backend.
# 2. Polimorfismo: cualquier implementación de RepositorioUsuarios puede ser intercambiada sin romper la lógica.
# 3. Facilita testing: se pueden crear mocks de la interfaz sin tocar la lógica real.
# 4. Promueve mantenibilidad y escalabilidad del sistema.
