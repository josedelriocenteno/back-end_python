"""
graceful_shutdown.py
=====================

Objetivo:
- Manejar apagados controlados de servicios y procesos
- Evitar corrupción de datos o pérdidas de información
- Garantizar consistencia y limpieza de recursos
"""

import signal
import time
import logging
import threading

# -------------------------------------------------------------------
# 1️⃣ SEÑALES DEL SISTEMA
# -------------------------------------------------------------------

shutdown_flag = threading.Event()

def handle_shutdown(signum, frame):
    """
    Maneja señales del sistema (SIGINT, SIGTERM)
    """
    logging.info(f"Señal recibida: {signum}. Iniciando shutdown controlado...")
    shutdown_flag.set()

# Registrar señales
signal.signal(signal.SIGINT, handle_shutdown)   # Ctrl+C
signal.signal(signal.SIGTERM, handle_shutdown)  # Kill desde sistema

# -------------------------------------------------------------------
# 2️⃣ SERVICIO SIMULADO
# -------------------------------------------------------------------

def servicio_largo():
    """
    Servicio que procesa tareas continuamente
    """
    contador = 0
    while not shutdown_flag.is_set():
        logging.info(f"Procesando tarea {contador}...")
        time.sleep(1)  # Simula trabajo
        contador += 1
    logging.info("Servicio detenido correctamente. Limpiando recursos...")

# -------------------------------------------------------------------
# 3️⃣ EJECUCIÓN CONTROLADA
# -------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Servicio iniciado. Presiona Ctrl+C para detenerlo.")
    try:
        servicio_largo()
    finally:
        # Cleanup adicional si fuese necesario
        logging.info("Todos los recursos liberados. Apagado completo.")

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Escuchar señales del sistema SIGINT/SIGTERM para shutdown controlado
# 2️⃣ Usar flags o eventos para detener loops de forma segura
# 3️⃣ Limpiar recursos críticos (archivos abiertos, conexiones, locks)
# 4️⃣ Loggear inicio y fin del shutdown para trazabilidad
# 5️⃣ Evitar interrupciones abruptas que puedan corromper datos
# 6️⃣ Mantener bloques try/finally para garantizar limpieza
# 7️⃣ Diseñar servicios idempotentes, que puedan reiniciarse sin problemas
