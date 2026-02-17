# Métricas de Backend: Midiendo la API y el Servidor

Cuando construyes un Backend con Python (FastAPI, Flask), hay métricas específicas que debes vigilar para asegurar que la experiencia del usuario sea fluida y el servidor no explote.

## 1. Métricas de Rendimiento (Performance)
*   **Response Time (P95/P99):** No mires la media; mira los percentiles. Si la media es 100ms pero el 5% de usuarios sufre 5 segundos de espera, tienes un problema grave.
*   **Throughput (RPS):** Requests Per Second. ¿Cuánta carga estamos soportando? ¿Hay picos inusuales que sugieren un ataque o una campaña de marketing?

## 2. Métricas de Fiabilidad (Reliability)
*   **Error Rate (%):** Porcentaje de peticiones fallidas frente al total. Un 0.1% es normal; un 5% requiere atención inmediata.
*   **Uptime:** El tiempo que el servicio ha estado disponible. El famoso "99.9%".

## 3. Métricas de Recursos (System)
*   **Uso de CPU:** Si está siempre al 90%, el sistema no tendrá margen para responder a picos de carga.
*   **Memory Leak:** Si el uso de memoria sube linealmente sin bajar nunca, tienes una fuga de memoria en tu código Python.
*   **Connection Pool:** ¿Cuántas conexiones a la base de datos están abiertas? ¿Se están liberando correctamente?

## 4. Métricas de Dependencias Externas
Si tu backend llama a BigQuery o a una API de terceros (ej: OpenAI):
*   **External Latency:** ¿Cuánto tarda la API externa en respondernos? A veces tu código es rápido pero tu proveedor es lento.
*   **External Errors:** ¿Cuántas veces nos devuelve un 429 (Rate Limit) el proveedor?

## 5. Cómo capturarlas en Python
Existen librerías como `prometheus-client` que se integran fácilmente con FastAPI.
```python
# Ejemplo conceptual con FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```
Esto crea automáticamente un endpoint `/metrics` que tu sistema de monitorización leerá periódicamente.

## Resumen: Visibilidad del Servicio
Las métricas de backend te permiten pasar del "Creo que la web va lenta" al "La latencia en el endpoint /users ha subido de 150ms a 2s debido a un bloqueo en la base de datos". Esa es la diferencia entre un amateur y un profesional.
