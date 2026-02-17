import logging
import sys

# 1. Configuración básica del logging
# El nivel determina qué mensajes se muestran (DEBUG < INFO < WARNING < ERROR < CRITICAL)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

logger = logging.getLogger("mi_aplicacion")

def dividir(a, b):
    logger.debug(f"Intentando dividir {a} entre {b}")
    try:
        resultado = a / b
        logger.info(f"División realizada con éxito: {resultado}")
        return resultado
    except ZeroDivisionError:
        # exc_info=True añade el traceback completo al log, vital para debugging
        logger.error("Error crítico: División por cero detectada", exc_info=True)
    except Exception as e:
        logger.warning(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    logger.info("Iniciando el script de ejemplo")
    dividir(10, 2)
    dividir(10, 0)
    logger.info("Script finalizado")
