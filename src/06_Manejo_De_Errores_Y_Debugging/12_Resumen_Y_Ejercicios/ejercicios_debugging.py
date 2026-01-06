"""
ejercicios_debugging.py
========================

Objetivo:
- Proporcionar ejercicios prácticos de debugging
- Mostrar bugs reales y anti-patrones comunes
- Enseñar cómo aplicar buenas prácticas profesionales
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------------------------------------
# 1️⃣ EJERCICIO: División por cero silenciosa
# -------------------------------------------------------------------

def division_silenciosa(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        pass  # ❌ Anti-patrón: swallow exception

# Solución profesional:
# - Capturar la excepción y loggear contexto
# - Devolver valor de fallback o relanzar si crítico

def division_segura(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        logging.error(f"División por cero: a={a}, b={b}", exc_info=True)
        return None

# -------------------------------------------------------------------
# 2️⃣ EJERCICIO: Logging excesivo
# -------------------------------------------------------------------

def proceso_ruidoso():
    for i in range(1000):
        logging.info(f"Iteración {i}")  # ❌ Anti-patrón: log masivo innecesario

# Solución:
def proceso_profesional():
    for i in range(1000):
        if i % 100 == 0:
            logging.info(f"Checkpoint iteración {i}")  # Logging útil

# -------------------------------------------------------------------
# 3️⃣ EJERCICIO: Except genérico
# -------------------------------------------------------------------

def abrir_archivo(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except:  # ❌ Anti-patrón
        logging.error("Error leyendo archivo")
        return None

# Solución:
def abrir_archivo_seguro(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        logging.warning(f"Archivo no encontrado: {path}")
        return None
    except PermissionError:
        logging.error(f"Permiso denegado: {path}")
        return None
    except Exception as e:
        logging.critical(f"Error inesperado: {e}", exc_info=True)
        raise

# -------------------------------------------------------------------
# 4️⃣ EJERCICIO: Variables sin seguimiento (debugging caótico)
# -------------------------------------------------------------------

def proceso_caotico():
    x = 10
    y = 0
    print("Intentando dividir...")
    resultado = x / y  # ❌ Crash inesperado sin logging
    print("Resultado:", resultado)

# Solución profesional:
def proceso_debuggable():
    x = 10
    y = 0
    try:
        resultado = x / y
    except ZeroDivisionError as e:
        logging.error(f"División por cero: x={x}, y={y}", exc_info=True)
        resultado = None
    logging.info(f"Resultado final: {resultado}")
    return resultado

# -------------------------------------------------------------------
# 5️⃣ EJERCICIO: Fail fast sin contexto
# -------------------------------------------------------------------

def procesar_datos(data):
    if data is None:
        sys.exit(1)  # ❌ Anti-patrón: muere sin log

# Solución profesional:
def procesar_datos_profesional(data):
    if data is None:
        logging.critical("Datos ausentes, abortando proceso.")
        sys.exit(1)

# -------------------------------------------------------------------
# 6️⃣ EJERCICIO DE PRACTICA
# -------------------------------------------------------------------

# Instrucciones:
# 1. Ejecuta cada función con datos que provoquen fallos
# 2. Observa logs, errores y comportamientos
# 3. Aplica soluciones seguras: logging adecuado, excepciones específicas, valores de fallback
# 4. Intenta reproducir errores y validar que fixes no rompan otras partes del código

if __name__ == "__main__":
    logging.info("=== EJERCICIOS DE DEBUGGING ===")

    # 1️⃣ División silenciosa
    print("División silenciosa (anti-patrón):", division_silenciosa(10, 0))
    print("División segura:", division_segura(10, 0))

    # 2️⃣ Logging excesivo
    print("Ejecutando proceso ruidoso (anti-patrón)...")
    proceso_ruidoso()
    print("Ejecutando proceso profesional...")
    proceso_profesional()

    # 3️⃣ Except genérico
    print("Abrir archivo inseguro (anti-patrón):", abrir_archivo("inexistente.txt"))
    print("Abrir archivo seguro:", abrir_archivo_seguro("inexistente.txt"))

    # 4️⃣ Debugging caótico
    print("Proceso caótico (anti-patrón):")
    try:
        proceso_caotico()
    except Exception as e:
        logging.error(f"Crash detectado: {e}", exc_info=True)
    print("Proceso debuggable (profesional):")
    proceso_debuggable()

    # 5️⃣ Fail fast con contexto
    print("Fail fast profesional:")
    procesar_datos_profesional(None)
