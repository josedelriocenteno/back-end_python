"""
resumen_errores_debugging.py
=============================

Objetivo:
- Sintetizar todo lo aprendido sobre manejo de errores y debugging
- Servir como referencia rápida y profesional
- Combinar buenas prácticas, patrones y anti-patrones
"""

import logging
import sys
import time

# -------------------------------------------------------------------
# 1️⃣ TIPOS DE ERRORES
# -------------------------------------------------------------------

# SyntaxError: error de sintaxis
# RuntimeError: error durante la ejecución
# LogicalError: error en la lógica, programa corre pero resultados son incorrectos

# -------------------------------------------------------------------
# 2️⃣ MANEJO BÁSICO DE EXCEPCIONES
# -------------------------------------------------------------------

def ejemplo_try_except(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logging.warning("División por cero detectada")
        return None
    finally:
        logging.info("Finalizando intento de división")

# -------------------------------------------------------------------
# 3️⃣ LÓGICA PROFESIONAL: RAISE Y EXCEPCIONES PERSONALIZADAS
# -------------------------------------------------------------------

class MiErrorCritico(Exception):
    pass

def funcion_critica(valor):
    if valor < 0:
        raise MiErrorCritico("Valor crítico negativo detectado")

# -------------------------------------------------------------------
# 4️⃣ FAIL FAST Y NO OCULTAR ERRORES
# -------------------------------------------------------------------

def fail_fast_demo(data):
    if data is None:
        logging.critical("Datos críticos ausentes. Abortando proceso.")
        sys.exit(1)

# -------------------------------------------------------------------
# 5️⃣ CONTEXT MANAGERS
# -------------------------------------------------------------------

from contextlib import contextmanager

@contextmanager
def abrir_archivo(path, modo="r"):
    f = None
    try:
        f = open(path, modo)
        yield f
    finally:
        if f:
            f.close()
            logging.info(f"Archivo {path} cerrado correctamente")

# -------------------------------------------------------------------
# 6️⃣ LOGGING PROFESIONAL
# -------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def ejemplo_logging():
    logging.debug("Debug → desarrollo")
    logging.info("Info → producción")
    logging.warning("Warning → advertencia")
    logging.error("Error → fallo recuperable")
    logging.critical("Critical → fallo irrecuperable")

# -------------------------------------------------------------------
# 7️⃣ DEBUGGING ORGANIZADO
# -------------------------------------------------------------------

def division_segura(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        logging.error(f"División por cero: a={a}, b={b}", exc_info=True)
        return None

# -------------------------------------------------------------------
# 8️⃣ PATRONES DE RESILIENCIA
# -------------------------------------------------------------------

def retry(func, max_intentos=3, delay=1):
    for intento in range(max_intentos):
        try:
            return func()
        except Exception as e:
            logging.warning(f"Intento {intento+1} fallido: {e}")
            time.sleep(delay)
    raise RuntimeError("Máximo de reintentos alcanzado")

# -------------------------------------------------------------------
# 9️⃣ ANTI-PATRONES CLÁSICOS
# -------------------------------------------------------------------

# - except: genérico
# - swallow exceptions (ignorar errores)
# - logging excesivo
# - debugging sin método
# - ocultar errores críticos

# -------------------------------------------------------------------
# 10️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Capturar solo excepciones esperadas
# 2️⃣ Loggear siempre con contexto
# 3️⃣ Fail fast para errores críticos
# 4️⃣ Usar context managers para recursos
# 5️⃣ Combinar retry y circuit breaker para resiliencia
# 6️⃣ Mantener debugging organizado y reproducible
# 7️⃣ Diferenciar errores recuperables vs irrecuperables
# 8️⃣ Documentar y centralizar manejo de errores
# 9️⃣ Testear escenarios de fallo para asegurar comportamiento
# 10️⃣ Evitar anti-patrones clásicos

# -------------------------------------------------------------------
# 11️⃣ EJEMPLO DE USO COMPLETO
# -------------------------------------------------------------------

def proceso_completo(data):
    fail_fast_demo(data)
    with abrir_archivo("archivo.txt", "w") as f:
        f.write("Prueba\n")
    resultado = division_segura(10, 0)
    logging.info(f"Resultado final: {resultado}")

if __name__ == "__main__":
    ejemplo_logging()
    proceso_completo([1, 2, 3])
