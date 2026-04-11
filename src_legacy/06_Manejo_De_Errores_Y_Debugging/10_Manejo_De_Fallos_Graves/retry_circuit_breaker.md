Retry y Circuit Breaker: Patrones de Resiliencia
1️⃣ Introducción

En sistemas distribuidos o microservicios, los errores temporales son inevitables: caídas de red, servicios externos lentos o sobrecargados.
Para manejar esto profesionalmente, usamos patrones de resiliencia:

Retry (Reintento): reintenta operaciones fallidas antes de fallar.

Circuit Breaker: previene que llamadas repetidas a servicios fallidos saturen el sistema.

2️⃣ Patrón Retry
Concepto

Reintenta una operación N veces antes de rendirse.

Útil para errores temporales, no para errores permanentes.

Reglas Profesionales

No usar retries infinitos → riesgo de saturar servicios.

Agregar delay y, opcionalmente, backoff exponencial.

Limitar a errores recuperables (p.ej., ConnectionError).

from functools import wraps
import time
import logging

def retry(max_intentos=3, delay=1, excepciones=(Exception,)):
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
                    time.sleep(delay)
        return wrapper
    return decorator

3️⃣ Patrón Circuit Breaker
Concepto

Evita llamar repetidamente a un servicio que está fallando.

Funciona como un interruptor:

Cerrado: todo funciona normalmente.

Abierto: corta llamadas al servicio durante un tiempo.

Semi-abierto: permite algunas pruebas para ver si el servicio volvió.

Reglas Profesionales

Definir número máximo de fallos antes de abrir el circuito.

Definir tiempo de espera para reintentar llamadas.

Loggear cada transición para trazabilidad.

Combinar con retry para máxima resiliencia.

class CircuitBreaker:
    def __init__(self, fallos_max=3, reset_time=5):
        self.fallos_max = fallos_max
        self.reset_time = reset_time
        self.fallos = 0
        self.abierto_hasta = None

    def llamar(self, func, *args, **kwargs):
        import time
        import logging

        if self.abierto_hasta and time.time() < self.abierto_hasta:
            raise RuntimeError("Circuito abierto: no llamar al servicio")

        try:
            resultado = func(*args, **kwargs)
            self.fallos = 0
            return resultado
        except Exception as e:
            self.fallos += 1
            logging.warning(f"Fallo {self.fallos}: {e}")
            if self.fallos >= self.fallos_max:
                self.abierto_hasta = time.time() + self.reset_time
                logging.error(f"Circuito abierto por {self.reset_time} segundos")
            raise

4️⃣ Combinando Retry + Circuit Breaker

Retry: intenta varias veces antes de considerar fallo definitivo.

Circuit Breaker: previene que los reintentos saturen servicios ya caídos.

Patrón profesional: retry sobre un servicio protegido por circuit breaker.

cb = CircuitBreaker(fallos_max=2, reset_time=3)

@retry(max_intentos=3, delay=0.5, excepciones=(RuntimeError,))
def llamada_resiliente():
    return cb.llamar(lambda: servicio_externo())

def servicio_externo():
    # Simula fallo aleatorio
    import random
    if random.random() < 0.5:
        raise RuntimeError("Fallo temporal en servicio externo")
    return "Éxito!"

5️⃣ Buenas Prácticas Profesionales

Usar retry solo para errores temporales.

Evitar saturar servicios con retries infinitos.

Combinar retry + circuit breaker para máxima resiliencia.

Loggear cada fallo con contexto (endpoint, payload, user_id).

Ajustar delay y backoff según criticidad y SLA.

Monitorear métricas de fallos, reintentos y tiempo de recuperación.

Mantener lógica desacoplada del resto del sistema.

Probar con fallos simulados para garantizar comportamiento en producción.

Este patrón es fundamental en microservicios y sistemas críticos, donde incluso un solo servicio externo puede afectar la disponibilidad global.