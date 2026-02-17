import logging
import logging.config
import os

# 1. Definición de la configuración profesional (normalmente en un archivo YAML o JSON)
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'estandar': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detallado': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d (%(funcName)s) - %(message)s'
        },
    },
    'handlers': {
        'consola': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'estandar',
            'stream': 'ext://sys.stdout',
        },
        'archivo_errores': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detallado',
            'filename': 'errores.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['consola', 'archivo_errores'],
            'level': 'INFO',
            'propagate': True
        },
        'mi_app.db': {
            'level': 'DEBUG',
            'handlers': ['consola'],
            'propagate': False
        }
    }
}

# 2. Aplicar la configuración
logging.config.dictConfig(LOGGING_CONFIG)

# 3. Uso en el código
logger = logging.getLogger("mi_app.main")
db_logger = logging.getLogger("mi_app.db")

def simular_proceso():
    logger.info("Iniciando proceso principal")
    db_logger.debug("Conectando a la base de datos...")
    
    try:
        raise ValueError("Simulando un error de datos")
    except Exception:
        logger.error("Fallo en la lógica de negocio", exc_info=True)

if __name__ == "__main__":
    simular_proceso()
    print("\n--- Revisa el archivo 'errores.log' para ver el log detallado ---")
