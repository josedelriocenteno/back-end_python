"""
patrones_recurrentes_backend.py
===============================

Buenas prácticas: patrones recurrentes en backend

Objetivos:
- Mostrar patrones que aparecen en casi todos los proyectos backend
- Mejorar escalabilidad, mantenibilidad y profesionalidad
- Ejemplos claros en Python
"""

# -------------------------------------------------------------------
# 1️⃣ PATRÓN: SEPARACIÓN DE CAPAS
# -------------------------------------------------------------------

# Siempre separar:
# - Presentación / API
# - Dominio / lógica de negocio
# - Persistencia / infraestructura

# Ya vimos este patrón en 'capas_y_responsabilidades.py'

# Beneficio: legibilidad, testabilidad y escalabilidad


# -------------------------------------------------------------------
# 2️⃣ PATRÓN: INYECCIÓN DE DEPENDENCIAS
# -------------------------------------------------------------------

# Evitar “magia” al crear objetos dentro de clases
# Inyectar repositorios, servicios, config

class RepositorioPedido:
    def guardar(self, pedido: dict):
        print(f"Guardando pedido: {pedido}")

class PedidoService:
    def __init__(self, repo: RepositorioPedido):
        self._repo = repo  # inyección explícita

    def crear_pedido(self, pedido: dict):
        self._repo.guardar(pedido)


# -------------------------------------------------------------------
# 3️⃣ PATRÓN: CONFIGURACIÓN EXTERNA
# -------------------------------------------------------------------

import os
from dataclasses import dataclass

@dataclass
class ConfigDB:
    host: str
    port: int

def cargar_config_db() -> ConfigDB:
    return ConfigDB(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432))
    )


# -------------------------------------------------------------------
# 4️⃣ PATRÓN: LOGGING CONSISTENTE
# -------------------------------------------------------------------

import logging

# Configuración global de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def ejemplo_logging():
    try:
        logger.info("Inicio del proceso")
        # Simular operación
        x = 10 / 2
        logger.info(f"Resultado: {x}")
    except Exception as e:
        logger.error(f"Error en el proceso: {e}")


# -------------------------------------------------------------------
# 5️⃣ PATRÓN: MANEJO DE ERRORES CENTRALIZADO
# -------------------------------------------------------------------

class ErrorValidacion(Exception):
    pass

class ErrorPersistencia(Exception):
    pass

def procesar_pedido(pedido: dict):
    if "usuario" not in pedido:
        raise ErrorValidacion("Usuario obligatorio")
    if "productos" not in pedido:
        raise ErrorValidacion("Productos obligatorios")
    try:
        # Simular persistencia
        print(f"Guardando pedido: {pedido}")
    except Exception as e:
        raise ErrorPersistencia("Error al guardar") from e


# -------------------------------------------------------------------
# 6️⃣ PATRÓN: ORQUESTACIÓN DE SERVICIOS
# -------------------------------------------------------------------

class ServicioEmail:
    def enviar(self, destinatario: str, mensaje: str):
        print(f"Enviando email a {destinatario}: {mensaje}")

class PedidoOrquestador:
    def __init__(self, servicio_email: ServicioEmail, repo: RepositorioPedido):
        self._servicio_email = servicio_email
        self._repo = repo

    def procesar(self, pedido: dict):
        # Persistencia
        self._repo.guardar(pedido)
        # Notificación
        self._servicio_email.enviar(pedido["usuario"], f"Pedido recibido: {pedido}")


# -------------------------------------------------------------------
# 7️⃣ PATRÓN: USO DE VALUE OBJECTS Y ENTIDADES
# -------------------------------------------------------------------

from dataclasses import dataclass
from uuid import uuid4

@dataclass(frozen=True)
class IDValue:
    value: str

    @staticmethod
    def generar() -> "IDValue":
        return IDValue(str(uuid4()))

@dataclass
class Usuario:
    id: IDValue
    nombre: str


# -------------------------------------------------------------------
# 8️⃣ BENEFICIOS GENERALES
# -------------------------------------------------------------------

# 1. Código profesional y consistente
# 2. Fácil de testear y mantener
# 3. Escalable: añadir nuevas funcionalidades sin romper existentes
# 4. Menor riesgo de errores en producción
# 5. Facilita onboarding de nuevos desarrolladores en el proyecto


# -------------------------------------------------------------------
# 9️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Patrones recurrentes = atajos profesionales
# Claves:
# - Separación de capas
# - Inyección de dependencias
# - Configuración externa
# - Logging consistente
# - Manejo centralizado de errores
# - Orquestación clara de servicios
# - Uso de Value Objects y entidades para claridad
