# Métricas con Prometheus y Grafana: Midiendo el Pulso

Si los logs son "el pasado" (qué ocurrió), las métricas son "el presente" (qué está ocurriendo ahora mismo).

## 1. El estándar de oro: RED (Rate, Errors, Duration)
Un backend senior monitoriza estas tres cosas en cada endpoint:
*   **Rate (Tasa):** Peticiones por segundo. ¿Estamos recibiendo un ataque?
*   **Errors (Errores):** ¿Cuántos 4xx y 5xx estamos lanzando?
*   **Duration (Duración/Latencia):** ¿Cuánto tarda el percentil 95 (P95) de mis usuarios? No mires la media, mira a los que más sufren.

## 2. Prometheus: La Base de Datos de Tiempo
Prometheus no "recibe" datos, sino que los "recolecta" (Pull). Tu API expone un endpoint `/metrics` con datos en formato texto:
```text
http_requests_total{method="GET", endpoint="/users"} 1450
http_request_duration_seconds_bucket{le="0.5"} 1200
```

## 3. Grafana: El Cuadro de Mandos (Dashboard)
Grafana se conecta a Prometheus y dibuja gráficas bonitas. Te permite ver visualmente si un despliegue ha causado un aumento de errores o de lentitud.

## 4. Instrumentación en FastAPI
Usamos la librería `prometheus-fastapi-instrumentator`.
```python
from prometheus_fastapi_instrumentator import Instrumentator

# Al iniciar la app
Instrumentator().instrument(app).expose(app)
```

## 5. Métricas de Negocio (Custom Metrics)
Además de las técnicas, puedes medir cosas del negocio:
*   "Usuarios registrados hoy".
*   "Pagos completados con éxito".
*   "Stock crítico en almacén".

## Resumen: Si no se mide, no se puede mejorar
Las métricas te permiten pasar de la intuición ("creo que la API va lenta") a los datos ("la latencia ha subido un 20% tras el último commit"). Es la herramienta fundamental para cumplir los SLAs (Service Level Agreements) con tus clientes.
