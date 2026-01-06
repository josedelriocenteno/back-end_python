"""
errores_y_reintentos.py
========================

Objetivo:
- Implementar estrategias de retry y resiliencia en backend
- Manejar errores temporales de forma profesional
- Evitar saturar servicios y mantener estabilidad
"""

import time
import random
import logging
from functools import wraps

# -------------------------------------------------------------------
# 1️⃣ PATRÓN RETRY BÁSICO
# -------------------------------------------------------------------

def retry(max_intentos=3, delay=1, excepciones=(Exception,)):
    """
    Decorador para reintentar función en caso de errores temporales
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            intentos = 0
            while intentos < max_intentos:
                try:
                    return func(*args, **kwargs)
                except excepciones as e:
                    intentos += 1
                    logging.warning(f"Intento {intentos} fallido: {e}")
                    if intentos == max_intentos:
                        logging.error("Máximo de reintentos alcanzado", exc_info=True)
                        raise
                    time.sleep(delay)  # esperar antes del próximo intento
        return wrapper
    return decorator

# -------------------------------------------------------------------
# 2️⃣ EJEMPLO DE USO
# -------------------------------------------------------------------

@retry(max_intentos=5, delay=0.5, excepciones=(ConnectionError,))
def llamada_api_simulada():
    """
    Simula una API que falla aleatoriamente
    """
    if random.random() < 0.7:
        # Simulamos fallo temporal
        raise ConnectionError("Error de conexión temporal")
    return "Éxito!"

# Ejecutar prueba
try:
    resultado = llamada_api_simulada()
    print("Resultado:", resultado)
except ConnectionError:
    print("No se pudo completar la operación después de reintentos")

# -------------------------------------------------------------------
# 3️⃣ PATRÓN CIRCUIT BREAKER BÁSICO
# -------------------------------------------------------------------

class CircuitBreaker:
    """
    Evita llamar repetidamente a un servicio que está fallando
    """
    def __init__(self, fallos_max=3, reset_time=5):
        self.fallos_max = fallos_max
        self.reset_time = reset_time
        self.fallos = 0
        self.abierto_hasta = None

    def llamar(self, func, *args, **kwargs):
        # Si circuito abierto, fallar rápido
        if self.abierto_hasta and time.time() < self.abierto_hasta:
            raise RuntimeError("Circuito abierto: no llamar al servicio")
        
        try:
            resultado = func(*args, **kwargs)
            # Reseteamos contador si hay éxito
            self.fallos = 0
            return resultado
        except Exception as e:
            self.fallos += 1
            logging.warning(f"Fallo {self.fallos}: {e}")
            if self.fallos >= self.fallos_max:
                self.abierto_hasta = time.time() + self.reset_time
                logging.error(f"Circuito abierto por {self.reset_time} segundos")
            raise

# -------------------------------------------------------------------
# 4️⃣ EJEMPLO CIRCUIT BREAKER
# -------------------------------------------------------------------

cb = CircuitBreaker(fallos_max=2, reset_time=3)

for _ in range(5):
    try:
        print(cb.llamar(llamada_api_simulada))
    except Exception as e:
        print("Llamada fallida:", e)
    time.sleep(1)

# -------------------------------------------------------------------
# 5️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1. Usar retry solo para errores temporales y predecibles
# 2. Evitar retries infinitos → puede saturar servicios
# 3. Combinar retry con circuit breaker para resiliencia
# 4. Loggear cada fallo con contexto (endpoint, parámetros)
# 5. Ajustar delay y número de intentos según criticidad y SLA
# 6. Mantener la lógica desacoplada del resto de la aplicación
# 7. Monitorear métricas de fallos y reintentos para optimizar
