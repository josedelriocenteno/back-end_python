# funciones_en_apis.py
"""
FUNCIONES EN BACKEND Y APIS
===========================

Objetivo:
- Aplicar todo lo visto sobre funciones a un contexto real de backend
- Crear endpoints claros, seguros y mantenibles
- Facilitar testing, escalabilidad y trazabilidad
"""

from typing import Dict, Any

# =========================================================
# 1. Función simple para un endpoint
# =========================================================
def obtener_usuario_endpoint(id_usuario: int) -> Dict[str, Any]:
    """
    Simula un endpoint que devuelve datos de un usuario.

    Args:
        id_usuario (int): ID del usuario a buscar.

    Returns:
        dict: Datos del usuario.
    """
    # Simulación de base de datos
    base_datos = {
        1: {"nombre": "Ana", "rol": "admin"},
        2: {"nombre": "Luis", "rol": "user"}
    }

    usuario = base_datos.get(id_usuario)
    if not usuario:
        return {"error": "Usuario no encontrado"}
    return usuario

# =========================================================
# 2. Función con validación y errores controlados
# =========================================================
def crear_usuario_endpoint(nombre: str, rol: str) -> Dict[str, Any]:
    """
    Endpoint para crear un usuario.

    Args:
        nombre (str): Nombre del usuario.
        rol (str): Rol asignado ('admin' o 'user').

    Returns:
        dict: Resultado de la creación.
    """
    roles_validos = {"admin", "user"}
    if rol not in roles_validos:
        return {"error": f"Rol inválido, debe ser uno de {roles_validos}"}

    # En un caso real, aquí insertamos en base de datos
    return {"mensaje": f"Usuario {nombre} creado con rol {rol}"}

# =========================================================
# 3. Función idempotente para endpoints
# =========================================================
def actualizar_usuario_endpoint(id_usuario: int, datos: dict) -> Dict[str, Any]:
    """
    Actualiza datos de usuario. Debe ser idempotente.

    Args:
        id_usuario (int): ID del usuario.
        datos (dict): Campos a actualizar.

    Returns:
        dict: Resultado de la operación.
    """
    # Simulación: si no hay cambios, sigue devolviendo el mismo resultado
    return {"mensaje": f"Usuario {id_usuario} actualizado", "datos_actualizados": datos}

# =========================================================
# 4. Buenas prácticas
# =========================================================
# - Funciones pequeñas y claras (Single Responsibility)
# - Tipado estricto (type hints)
# - Manejar errores explícitamente
# - Idempotencia cuando se aplican cambios
# - Preparadas para testing unitario y simulación de endpoints
# - Documentar claramente args y return
# - Separar lógica de negocio y presentación/API (DTOs, serialización)
