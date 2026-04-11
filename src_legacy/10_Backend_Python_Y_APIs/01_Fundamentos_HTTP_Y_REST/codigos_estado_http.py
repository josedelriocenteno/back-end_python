"""
FALCÁCULOS Y USO DE CÓDIGOS DE ESTADO HTTP EN PYTHON
-----------------------------------------------------------------------------
Como desarrollador backend, usar el código de estado correcto es la mejor 
forma de documentar tu código sin escribir una sola palabra.
"""

from enum import IntEnum

class HttpStatus(IntEnum):
    # 2xx: Éxito
    OK = 200                # Petición exitosa estándar
    CREATED = 201           # Recurso creado con éxito (usar en POST)
    ACCEPTED = 202          # Tarea aceptada para procesamiento asíncrono
    NO_CONTENT = 204        # Éxito pero no hay nada que devolver (usar en DELETE)

    # 3xx: Redirección
    MOVED_PERMANENTLY = 301
    FOUND = 302

    # 4xx: Error del Cliente (El usuario hizo algo mal)
    BAD_REQUEST = 400       # Error de validación (JSON mal formado)
    UNAUTHORIZED = 401      # El usuario no se ha autenticado
    FORBIDDEN = 403         # Autenticado pero no tiene permisos para ESTO
    NOT_FOUND = 404         # El recurso no existe
    METHOD_NOT_ALLOWED = 405 # Usaste GET en un endpoint de solo POST
    CONFLICT = 409          # Error de lógica (ej: el email ya existe)
    UNPROCESSABLE_ENTITY = 422 # Petición bien formada pero inválida (usado por FastAPI)

    # 5xx: Error del Servidor (Tú hiciste algo mal)
    INTERNAL_SERVER_ERROR = 500 # El código explotó (Exception no capturada)
    NOT_IMPLEMENTED = 501       # Funcionalidad planeada pero no lista
    BAD_GATEWAY = 502           # El server de upstream falló (ej: error en Nginx/DB)
    SERVICE_UNAVAILABLE = 503   # El servidor está saturado o en mantenimiento

# EJEMPLOS DE USO EN LÓGICA DE BACKEND
def save_user(email: str):
    if not "@" in email:
        return {"error": "Email inválido"}, HttpStatus.BAD_REQUEST
    
    # ... lógica de guardado ...
    return {"id": 1}, HttpStatus.CREATED

"""
CONSEJOS SENIOR:
1. Nunca devuelvas un 200 para errores ("Error 200"). Es confuso para los clientes.
2. '401 Unauthorized' significa 'no te conozco'; '403 Forbidden' significa 
   'sé quién eres pero no tienes permiso'.
3. '422 Unprocessable Entity' es el estándar moderno para fallos de validación 
   de formularios.
4. Un '500' en producción debe disparar una alerta inmediata en tu sistema 
   de monitorización.
"""

if __name__ == "__main__":
    msg, code = save_user("invalid")
    print(f"Respuesta: {msg}, Status: {code}")
