"""
excepciones_en_servicios.py
============================

Objetivo:
- Manejar errores dentro de la capa de servicios
- Separar lógica de negocio de la capa de presentación o API
- Facilitar pruebas unitarias y mantenibilidad
"""

import logging

# -------------------------------------------------------------------
# 1️⃣ EXCEPCIONES PERSONALIZADAS DE NEGOCIO
# -------------------------------------------------------------------

class ServicioError(Exception):
    """Error genérico en la capa de servicios"""
    pass

class UsuarioNoEncontrado(ServicioError):
    """Usuario no encontrado en base de datos o repositorio"""
    pass

class ValidacionFallida(ServicioError):
    """Validación de datos fallida"""
    pass

# -------------------------------------------------------------------
# 2️⃣ EJEMPLO DE SERVICIO
# -------------------------------------------------------------------

class UsuarioService:
    """
    Capa de servicios para manejar usuarios
    """

    def __init__(self):
        # Simulación de base de datos
        self.usuarios = {1: "Alice", 2: "Bob"}

    def obtener_usuario(self, user_id: int) -> str:
        """
        Obtiene usuario por ID
        Lanza UsuarioNoEncontrado si no existe
        """
        if not isinstance(user_id, int):
            raise ValidacionFallida("user_id debe ser un entero")

        if user_id not in self.usuarios:
            raise UsuarioNoEncontrado(f"Usuario con ID {user_id} no encontrado")

        return self.usuarios[user_id]

    def crear_usuario(self, user_id: int, nombre: str):
        """
        Crea un nuevo usuario
        Lanza ValidacionFallida si datos incorrectos
        """
        if not nombre or not isinstance(nombre, str):
            raise ValidacionFallida("Nombre inválido")

        if user_id in self.usuarios:
            raise ValidacionFallida(f"Usuario con ID {user_id} ya existe")

        self.usuarios[user_id] = nombre
        return nombre

# -------------------------------------------------------------------
# 3️⃣ MANEJO PROFESIONAL DE EXCEPCIONES
# -------------------------------------------------------------------

def procesar_servicio(service: UsuarioService, user_id: int):
    try:
        nombre = service.obtener_usuario(user_id)
        print(f"Usuario encontrado: {nombre}")
    except UsuarioNoEncontrado as e:
        logging.warning(e)
        # Aquí podemos propagar al controlador HTTP o devolver código de error
    except ValidacionFallida as e:
        logging.warning(e)
    except ServicioError as e:
        logging.error("Error genérico en la capa de servicio", exc_info=True)
    except Exception as e:
        # Nunca atrapar Exception genérica sin log
        logging.critical("Error inesperado", exc_info=True)

# -------------------------------------------------------------------
# 4️⃣ PRUEBAS
# -------------------------------------------------------------------

service = UsuarioService()

procesar_servicio(service, 1)      # ✅ Usuario encontrado
procesar_servicio(service, 99)     # ⚠️ UsuarioNoEncontrado
procesar_servicio(service, "abc")  # ⚠️ ValidacionFallida

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1. Definir excepciones específicas por tipo de fallo
# 2. No mezclar excepciones de negocio con HTTP directamente
# 3. Loggear errores internos para trazabilidad
# 4. Permitir que la capa de presentación (API) transforme estas excepciones
#    en respuestas limpias (JSON, códigos HTTP)
# 5. Facilitar tests unitarios, simulando excepciones sin tocar HTTP
# 6. Mantener separada la lógica de negocio de la infraestructura
