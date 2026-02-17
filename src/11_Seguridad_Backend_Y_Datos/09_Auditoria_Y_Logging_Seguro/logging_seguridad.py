"""
SEGURIDAD: LOGGING SEGURO (ANONIMIZACIÓN)
-----------------------------------------------------------------------------
Cómo registrar eventos sin filtrar datos sensibles de los usuarios.
"""

import logging
import json
import re

# 1. LISTA DE CAMPOS SENSIBLES (PII/Secretos)
SENSITIVE_FIELDS = {"password", "token", "access_token", "credit_card", "ssn"}

class SecurityFilter(logging.Filter):
    """
    Este filtro limpia los datos sensibles de los logs antes de que 
    lleguen al archivo o a la consola.
    """
    def filter(self, record):
        if hasattr(record, "msg") and isinstance(record.msg, str):
            # Ejemplo simplificado de limpieza por Regex
            for field in SENSITIVE_FIELDS:
                pattern = rf'"{field}"\s*:\s*"[^"]+"'
                record.msg = re.sub(pattern, f'"{field}": "[REDACTED]"', record.msg)
        return True

# 2. CONFIGURACIÓN DEL LOGGER
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("security_logger")
logger.addFilter(SecurityFilter())

def log_api_call(user_id: int, request_data: dict):
    """
    Registra una llamada a la API de forma segura.
    """
    # Convertimos a JSON para el log estructurado
    message = json.dumps({
        "event": "api_call",
        "user_id": user_id,
        "payload": request_data
    })
    
    # El filtro entrará en acción y limpiará el 'password'
    logger.info(message)

# --- PRUEBA ---
datos_sucios = {
    "username": "jose_dev",
    "password": "mi_secreto_muy_largo_123",
    "email": "jose@example.com"
}

log_api_call(user_id=101, request_data=datos_sucios)

"""
REGLA DE ORO PARA EL DESARROLLADOR:
-----------------------------------------------------------------------------
1. Nunca loguees el header 'Authorization' completo.
2. Los logs son para depurar y para auditoría, no son una base de datos 
   de usuarios.
3. Si un dato está cifrado en la DB, también debería estarlo (o redactado) 
   en los logs.
"""

"""
RESUMEN:
Un logging seguro es la diferencia entre que un 'error 500' sea un bug 
o una brecha de seguridad accidental. Usa siempre filtros centrales para 
no depender de que cada desarrollador se acuerde de limpiar sus propios logs.
"""
