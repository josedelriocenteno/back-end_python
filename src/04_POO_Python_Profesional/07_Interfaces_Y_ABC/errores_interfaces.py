# errores_interfaces.py
# Ejemplos de malas prácticas al definir interfaces en Python
# Orientado a tu caso: backend y data, para que veas qué evitar

from abc import ABC, abstractmethod
from typing import List, Dict

# ------------------------------------------------------------
# ERROR 1: Interface con lógica implementada
class RepositorioMal(ABC):
    """
    Mala práctica: una interfaz no debería contener lógica de negocio concreta.
    Esto acopla la implementación a la interfaz y dificulta testing.
    """
    _usuarios = []  # ❌ estado compartido en la interfaz

    @abstractmethod
    def agregar(self, usuario: Dict) -> int:
        # ❌ implementación aquí mezcla contrato con lógica
        self._usuarios.append(usuario)
        return len(self._usuarios)

# ------------------------------------------------------------
# ERROR 2: Interface incompleta o confusa
class ServicioMal(ABC):
    """
    Mala práctica: métodos que no indican claramente sus parámetros ni su retorno.
    Esto provoca que las implementaciones puedan ser inconsistentes.
    """
    @abstractmethod
    def crear_usuario(self):
        pass  # ❌ qué parámetros? qué retorna?

    @abstractmethod
    def obtener_usuario(self):
        pass  # ❌ mismo problema

# ------------------------------------------------------------
# ERROR 3: Interface no desacoplada
class ServicioAcoplado(ABC):
    """
    Mala práctica: la interfaz depende de una implementación concreta.
    Esto rompe el principio de inversión de dependencias (DIP).
    """
    def __init__(self):
        self.repositorio = []  # ❌ la interfaz no debería conocer detalles de almacenamiento

    @abstractmethod
    def crear_usuario(self, nombre: str):
        self.repositorio.append(nombre)  # ❌ lógica dentro de la interfaz

# ------------------------------------------------------------
# CLAVES PARA INTERFACES BIEN DEFINIDAS:
# 1. No contener estado ni lógica de negocio concreta.
# 2. Métodos claros, con parámetros y tipos explícitos.
# 3. Total desacoplamiento: no depender de implementaciones concretas.
# 4. Facilitar testing y mantenimiento en backend y data pipelines.
