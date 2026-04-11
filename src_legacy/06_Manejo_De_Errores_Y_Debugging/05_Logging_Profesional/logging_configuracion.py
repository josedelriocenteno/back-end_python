"""
logging_configuracion.py
========================

Objetivo:
- Configurar logging de manera profesional
- Usar formatos claros y consistentes
- Redirigir logs a consola, archivos o sistemas externos
- Diferenciar entornos: desarrollo, testing, producción
"""

import logging
import logging.handlers

# -------------------------------------------------------------------
# 1️⃣ FORMATO DE LOGS
# -------------------------------------------------------------------

# Formato recomendado: incluir nivel, timestamp, módulo, función y mensaje
formato = "%(levelname)s | %(asctime)s | %(name)s | %(funcName)s | %(message)s"

logging.basicConfig(
    level=logging.DEBUG,     # Mostrar logs desde DEBUG en adelante
    format=formato
)

logger = logging.getLogger("mi_proyecto")

logger.debug("DEBUG: inicio de la aplicación")
logger.info("INFO: aplicación corriendo")
logger.warning("WARNING: variable vacía")
logger.error("ERROR: fallo crítico")
logger.critical("CRITICAL: sistema detenido")

# -------------------------------------------------------------------
# 2️⃣ HANDLERS: SALIDA DE LOGS
# -------------------------------------------------------------------

# 2a. Consola (ya cubierta por basicConfig)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(formato))

# 2b. Archivo simple
file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(logging.Formatter(formato))

# 2c. Rotación de archivos (logs diarios o por tamaño)
rotating_handler = logging.handlers.RotatingFileHandler(
    "logs/app_rotating.log",
    maxBytes=1024*1024,  # 1 MB por archivo
    backupCount=5
)
rotating_handler.setLevel(logging.ERROR)
rotating_handler.setFormatter(logging.Formatter(formato))

# Agregamos handlers al logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(rotating_handler)

# -------------------------------------------------------------------
# 3️⃣ USO PROFESIONAL
# -------------------------------------------------------------------

logger.debug("DEBUG: mensaje de desarrollo")
logger.info("INFO: mensaje informativo")
logger.warning("WARNING: advertencia visible en consola y archivo")
logger.error("ERROR: error crítico, se rota archivo si es grande")
logger.critical("CRITICAL: alerta máxima")

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS
# -------------------------------------------------------------------

# 1. Usar distintos handlers según necesidad (consola, archivo, remoto)
# 2. Filtrar por nivel para no saturar logs en producción
# 3. Incluir timestamps y contexto (módulo, función, usuario si aplica)
# 4. Rotar logs para evitar archivos gigantes
# 5. No usar print en producción, todo debe pasar por logging
# 6. Configurar logging antes de iniciar la aplicación principal

# -------------------------------------------------------------------
# 5️⃣ EJEMPLO COMPLETO CON FUNCIONES
# -------------------------------------------------------------------

def procesar_registro(registro: dict):
    logger.info(f"Procesando registro {registro.get('id', 'N/A')}")
    try:
        if registro.get("valor", 1) == 0:
            raise ZeroDivisionError("Valor no puede ser 0")
        resultado = 10 / registro["valor"]
        logger.debug(f"Resultado calculado: {resultado}")
    except ZeroDivisionError as e:
        logger.error(f"ERROR: {e}")
    except Exception as e:
        logger.critical(f"CRITICAL: error inesperado: {e}")
