"""
niveles_logging.py
==================

Objetivo:
- Conocer los niveles de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Aprender cuándo usar cada nivel
- Mejorar trazabilidad y mantenimiento del código
"""

import logging

# -------------------------------------------------------------------
# 1️⃣ CONFIGURACIÓN BÁSICA
# -------------------------------------------------------------------

logging.basicConfig(
    level=logging.DEBUG,  # Mostrar logs desde DEBUG en adelante
    format="%(levelname)s - %(asctime)s - %(message)s"
)

# -------------------------------------------------------------------
# 2️⃣ NIVELES DE LOGGING
# -------------------------------------------------------------------

# 1. DEBUG
#    - Mensajes detallados para debugging
#    - No se usan en producción generalmente
logging.debug("DEBUG: valor de variable x = 42")

# 2. INFO
#    - Mensajes informativos de flujo normal
#    - Ej: inicio/fin de procesos, operaciones completadas
logging.info("INFO: Proceso de carga de datos iniciado")

# 3. WARNING
#    - Indica que algo inesperado ocurrió pero no detiene el programa
#    - Ej: valores nulos, deprecated functions, warnings de configuración
logging.warning("WARNING: campo 'email' vacío, se usará valor por defecto")

# 4. ERROR
#    - Indica que ocurrió un fallo que afecta la operación actual
#    - Ej: división por cero, fallo en query, excepción capturada
try:
    10 / 0
except ZeroDivisionError as e:
    logging.error(f"ERROR: fallo crítico al dividir: {e}")

# 5. CRITICAL
#    - Fallos graves que podrían detener todo el sistema
#    - Ej: fallo de conexión a DB, pérdida de datos críticos
logging.critical("CRITICAL: base de datos inaccesible, detener servicio")

# -------------------------------------------------------------------
# 3️⃣ RESUMEN DE USO PROFESIONAL
# -------------------------------------------------------------------

# Nivel          | Uso
# -------------- | -------------------------------------------
# DEBUG          | Información detallada para desarrolladores
# INFO           | Flujo normal del programa
# WARNING        | Situaciones inesperadas pero recuperables
# ERROR          | Fallos que afectan operaciones actuales
# CRITICAL       | Fallos graves que requieren atención inmediata

# Buenas prácticas:
# 1. DEBUG → solo en desarrollo
# 2. INFO → mostrar inicio/fin de procesos, métricas
# 3. WARNING → advertir problemas que no detienen ejecución
# 4. ERROR → capturar excepciones críticas y loguearlas
# 5. CRITICAL → alertas de fallos que requieren intervención inmediata

# -------------------------------------------------------------------
# 4️⃣ EJEMPLO COMPLETO
# -------------------------------------------------------------------

def procesar_registro(registro):
    logging.debug(f"DEBUG: procesando registro {registro}")
    if "email" not in registro:
        logging.warning("WARNING: registro sin email, asignando default")
        registro["email"] = "default@example.com"
    try:
        resultado = 10 / registro.get("valor", 1)
        logging.info(f"INFO: resultado = {resultado}")
    except ZeroDivisionError as e:
        logging.error(f"ERROR: división por cero para registro {registro}")
        raise
    except Exception as e:
        logging.critical(f"CRITICAL: error inesperado: {e}")
        raise

# -------------------------------------------------------------------
# 5️⃣ RESUMEN PRÁCTICO
# -------------------------------------------------------------------

# - Combinar niveles con try/except/fail-fast aumenta robustez
# - Siempre agregar contexto en mensajes (registro, usuario, función)
# - Evitar prints en producción: usar logging configurado
# - Ajustar level según entorno: DEBUG en dev, INFO/WARNING en prod
