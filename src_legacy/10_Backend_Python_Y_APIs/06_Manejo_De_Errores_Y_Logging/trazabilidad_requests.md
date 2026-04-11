# Trazabilidad de Requests: Rastreando el problema

Imagina que tienes 100 usuarios usando tu API al mismo tiempo y uno recibe un error 500. Revisas los logs y ves miles de líneas mezcladas. ¿Cuál de todas pertenece a ese usuario específico?

## 1. El ID de Correlación (Correlation ID / Request ID)
La solución es asignar un identificador único (UUID) a cada petición en cuanto entra en tu servidor.

### Cómo funciona:
1.  **Middleware:** Crea un middleware que genere un `X-Request-ID` para cada petición.
2.  **Propagación:** Ese ID se añade a cada línea de log que se genere durante ese request.
3.  **Respuesta:** Se devuelve el ID al cliente en las cabeceras.

## 2. Ventajas en Producción
*   **Debugging Veloz:** Si el cliente reporta un error, te dará su `Request-ID`. Vas a tus logs, filtras por ese ID y ves exactamente qué pasó desde la autenticación hasta la query fallida.
*   **Microservicios:** Si tu backend llama a otro servidor, pásale el `Request-ID`. Así podrás rastrear la petición a través de todo tu ecosistema (Distributed Tracing).

## 3. Implementación Sugerida
Aunque FastAPI no lo trae por defecto, es fácil de añadir con middlewares:
```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request_id = str(uuid.uuid4())
    # Guardamos en un ContextVar para que el logger lo recoja automáticamente
    # ...
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

## 4. ContextVars: El ingrediente secreto
En Python `asyncio`, para que el ID sea accesible en cualquier función profunda sin tener que pasarlo como argumento, usamos `contextvars`. Esto asegura que cada "hilo" asíncrono tenga su propio contexto de logs.

## 5. Herramientas Especializadas
*   **Sentry:** Una plataforma que agrupa errores similares y te da toda la trazabilidad y variables de entorno del momento del fallo.
*   **OpenTelemetry:** El estándar de la industria para trazas y métricas distribuidas.

## Resumen: No dejes migas de pan, deja un GPS
Un backend serio debe ser capaz de explicar exactamente qué pasó en una transacción específica hace 3 días. Sin trazabilidad, estás adivinando. Con trazabilidad, estás diagnosticando.
