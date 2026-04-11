# Tracing en APIs: FastAPI + OpenTelemetry

Implementar trazabilidad en una API moderna es sorprendentemente fácil gracias a la instrumentación automática. Vamos a ver cómo se hace con **FastAPI**.

## 1. Instalación de librerías
Necesitamos el SDK de OpenTelemetry para Python.
```bash
pip install opentelemetry-api opentelemetry-sdk \
            opentelemetry-instrumentation-fastapi \
            opentelemetry-exporter-otlp
```

## 2. Instrumentación automática
No necesitas añadir código a cada función. OpenTelemetry puede "envolver" tu app de FastAPI automáticamente.

```python
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola Mundo"}

# Esto añade automáticamente tracing a todas las rutas
FastAPIInstrumentor.instrument_app(app)
```

## 3. Añadiendo Spans personalizados
Si una función es muy crítica, puedes crear una "sub-traza" para ver cuánto tarda esa parte específica.
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@app.get("/data")
async def get_data():
    with tracer.start_as_current_span("proceso_pesado_db"):
        # Tu lógica aquí
        pass
    return {"status": "ok"}
```

## 4. Visualización: Jaeger o Datadog
Las trazas se envían a un recolector. **Jaeger** es la plataforma Open Source más común para visualizar este árbol de peticiones.
*   En Jaeger verás cada petición HTTP y cuánto tiempo tardó cada capa de tu API.

## 5. Integración con Logs
Lo más potente es que el `trace_id` de OpenTelemetry aparezca automáticamente en tus logs (que vimos en el sub-tema 01). Así puedes buscar un log de error y saltar directamente a ver la traza completa de esa petición.

## Resumen: Rayos X para tu API
Añadir tracing a tu API de Python es como ponerle una cámara a cada petición. Te permite dejar de adivinar por qué la web va lenta y empezar a ver exactamente qué milisegundo se pierde en cada línea de código.
