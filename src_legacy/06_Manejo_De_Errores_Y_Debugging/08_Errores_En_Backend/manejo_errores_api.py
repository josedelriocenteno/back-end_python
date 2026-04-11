"""
manejo_errores_api.py
======================

Objetivo:
- Centralizar el manejo de errores en un backend
- Devolver respuestas HTTP limpias y consistentes
- Mejorar mantenibilidad y trazabilidad de errores
"""

import json
import datetime
import logging

# -------------------------------------------------------------------
# 1️⃣ FUNCIONES DE RESPUESTA ESTANDARIZADA
# -------------------------------------------------------------------

def respuesta_ok(data: dict):
    """
    Respuesta exitosa (HTTP 200)
    """
    return json.dumps({
        "status": 200,
        "data": data,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200

def respuesta_error(mensaje: str, codigo: int):
    """
    Respuesta de error estructurada (HTTP 4xx o 5xx)
    """
    return json.dumps({
        "status": codigo,
        "error": mensaje,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), codigo

# -------------------------------------------------------------------
# 2️⃣ DECORADOR CENTRAL DE ERRORES
# -------------------------------------------------------------------

def manejar_errores_api(func):
    """
    Decorador para envolver endpoints de API
    y centralizar manejo de errores
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            # Error de cliente → 400 Bad Request
            logging.warning(f"Error de cliente: {ve}")
            return respuesta_error(str(ve), 400)
        except KeyError as ke:
            # Error de cliente → recurso no encontrado → 404
            logging.warning(f"Recurso no encontrado: {ke}")
            return respuesta_error(f"Recurso no encontrado: {ke}", 404)
        except Exception as e:
            # Error interno → 500 Internal Server Error
            logging.error("Error interno del servidor", exc_info=True)
            return respuesta_error("Error interno del servidor", 500)
    return wrapper

# -------------------------------------------------------------------
# 3️⃣ EJEMPLO DE USO EN ENDPOINTS
# -------------------------------------------------------------------

@manejar_errores_api
def obtener_usuario_api(user_id):
    usuarios = {1: "Alice", 2: "Bob"}
    
    if not isinstance(user_id, int):
        raise ValueError("user_id debe ser un entero")
    
    if user_id not in usuarios:
        raise KeyError(user_id)
    
    return respuesta_ok({"user_id": user_id, "nombre": usuarios[user_id]})

# -------------------------------------------------------------------
# 4️⃣ PRUEBAS
# -------------------------------------------------------------------

print(obtener_usuario_api(1))  # ✅ Devuelve 200 OK
print(obtener_usuario_api("abc"))  # ❌ Devuelve 400 Bad Request
print(obtener_usuario_api(5))  # ❌ Devuelve 404 Not Found

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1. Centralizar manejo de errores para no repetir lógica
# 2. Diferenciar claramente errores de cliente vs servidor
# 3. Devolver JSON consistente con status, mensaje y timestamp
# 4. Loggear siempre errores internos con exc_info
# 5. Evitar exponer stack traces o datos sensibles al cliente
# 6. Usar decoradores o middleware para endpoints REST
# 7. Mantener endpoints predecibles y fáciles de testear
