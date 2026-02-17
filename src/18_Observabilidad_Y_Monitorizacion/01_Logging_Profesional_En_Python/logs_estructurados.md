# Logs Estructurados: Hablando el lenguaje de las máquinas

En sistemas modernos y cloud, los logs de texto plano ("Ocurrió un error") están obsoletos. El estándar hoy es el **Logging Estructurado**, normalmente en formato **JSON**.

## 1. ¿Por qué usar JSON para los logs?
Imagínate que tienes 1 millón de líneas de logs y quieres saber cuántas veces falló el usuario `ID: 456` en el servidor de `Barcelona`.
*   **Texto plano:** Tendrías que hacer `grep` complejos y lentos que a menudo fallan si el formato cambia un poco.
*   **Estructurado:** Haces una query: `SELECT count(*) FROM logs WHERE user_id = 456 AND city = 'Barcelona'`. Es instantáneo y preciso.

## 2. Ejemplo de un Log Estructurado
```json
{
  "timestamp": "2024-03-15T10:00:01Z",
  "level": "ERROR",
  "logger": "ingesta_ventas",
  "message": "Fallo al conectar a la API",
  "context": {
    "provider": "Stripe",
    "attempt": 3,
    "timeout_ms": 5000,
    "trace_id": "a8f9-b2c3-d4e5"
  }
}
```

## 3. Cómo implementarlo en Python
Puedes usar librerías como `structlog` o `python-json-logger`.
```python
# Ejemplo rápido con python-json-logger
from pythonjsonlogger import jsonlogger
import logging

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

logger.error("Error crítico", extra={'user_id': 123, 'ip': '1.1.1.1'})
```

## 4. Contexto Everywhere (Trace IDs)
El mayor beneficio del log estructurado es poder añadir un `trace_id` o `correlation_id` a cada línea. Esto permite "unir" logs de diferentes servicios que pertenecen a la misma petición de usuario.

## 5. Integración Cloud
Servicios como **Google Cloud Logging** o **Datadog** adoran el JSON. Automáticamente crean filtros y gráficos basados en las claves de tu JSON sin que tú tengas que configurar nada.

## Resumen: Preparado para la Escala
El logging estructurado es la diferencia entre un script "casero" y un sistema preparado para operar en la nube a gran escala. Deja de escribir frases y empieza a emitir datos.
