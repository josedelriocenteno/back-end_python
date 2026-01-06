"""
logging_archivos.py
==================

Objetivo:
- Guardar logs de manera persistente en archivos
- Evitar saturar disco con rotación automática
- Mantener trazabilidad y seguridad en producción
"""

import logging
from logging.handlers import RotatingFileHandler
import os

# -------------------------------------------------------------------
# 1️⃣ CONFIGURACIÓN BÁSICA DE ARCHIVO DE LOGS
# -------------------------------------------------------------------

# Aseguramos que exista carpeta de logs
os.makedirs("logs", exist_ok=True)

# Logger principal
logger = logging.getLogger("mi_aplicacion")
logger.setLevel(logging.DEBUG)  # Captura todos los niveles

# Formato recomendado
formato = "%(levelname)s | %(asctime)s | %(name)s | %(funcName)s | %(message)s"
formatter = logging.Formatter(formato)

# -------------------------------------------------------------------
# 2️⃣ HANDLER DE ARCHIVO SIMPLE
# -------------------------------------------------------------------

file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.INFO)  # Solo INFO y superiores se guardan
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info("INFO: Logger de archivo inicializado")
logger.debug("DEBUG: Este mensaje no se guardará en app.log porque nivel=INFO")

# -------------------------------------------------------------------
# 3️⃣ ROTACIÓN DE ARCHIVOS
# -------------------------------------------------------------------

# Evita archivos gigantes, mantiene backups
rotating_handler = RotatingFileHandler(
    "logs/app_rotating.log",
    maxBytes=1024*1024,  # 1 MB
    backupCount=5,        # Mantener últimos 5 archivos
)
rotating_handler.setLevel(logging.WARNING)
rotating_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)

# -------------------------------------------------------------------
# 4️⃣ USO PROFESIONAL
# -------------------------------------------------------------------

logger.info("INFO: Inicio de proceso")
logger.warning("WARNING: Advertencia importante")
logger.error("ERROR: Fallo crítico que se guarda y rota")

# Ejemplo de función que loguea a archivo persistente
def procesar_datos(datos):
    if not datos:
        logger.warning("WARNING: No se recibieron datos")
        return
    try:
        resultado = 10 / datos.get("valor", 1)
        logger.info(f"INFO: Resultado calculado: {resultado}")
    except ZeroDivisionError as e:
        logger.error(f"ERROR: División por cero: {e}")
    except Exception as e:
        logger.critical(f"CRITICAL: Error inesperado: {e}")

procesar_datos({"valor": 0})
procesar_datos({"valor": 5})

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS DE LOGS PERSISTENTES
# -------------------------------------------------------------------

# 1. Mantener carpeta dedicada para logs
# 2. Configurar rotación para no saturar disco
# 3. Diferenciar niveles para archivo vs consola
# 4. Incluir timestamps y contexto (módulo, función, usuario)
# 5. Usar logging en lugar de print para producción
# 6. Registrar solo información relevante: no logs innecesarios
# 7. Monitorear tamaño de logs y automatizar backups si es necesario
