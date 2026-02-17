# Manejo de Excepciones en el Mundo Asíncrono

Gestionar errores en `asyncio` es más complejo que en el código síncrono. Un error en una tarea de fondo no capturado puede tirar abajo todo tu sistema o quedar oculto para siempre.

## 1. El error "Silencioso"
Si lanzas una tarea con `create_task` y tiene un error interno:
- La aplicación seguirá corriendo.
- No verás ningún log de error inmediatamente.
- Solo verás el error si en algún momento haces `await` de esa tarea o si el Event Loop se cierra.

## 2. Excepciones en Grupos de Tareas (Gather)
`asyncio.gather(..., return_exceptions=True)`
- **False (Defecto):** La primera tarea que falle lanzará la excepción al `gather`. El resto de tareas siguen corriendo pero ya no tienes sus resultados.
- **True:** `gather` no lanza excepciones. Devuelve una lista donde algunos elementos son los resultados y otros son los objetos de la Excepción. Esto te permite procesar los éxitos y loguear los fallos uno a uno.

## 3. Python 3.11+: `ExceptionGroup`
Cuando usas `TaskGroup()`, es posible que fallen varias tareas a la vez. Python ahora permite lanzar un "Grupo de Excepciones".
- **Sintaxis:** `except* ValueError as eg:` (Nota el asterisco). Te permite manejar selectivamente diferentes tipos de errores que ocurrieron simultáneamente.

## 4. El "Last Resort" (Exception Handler)
Puedes configurar un manejador global para errores que se escapen de tus `try/except`.
```python
def global_exception_handler(loop, context):
    msg = context.get("exception", context["message"])
    logger.error(f"Fallo crítico asíncrono: {msg}")

loop = asyncio.get_event_loop()
loop.set_exception_handler(global_exception_handler)
```

## 5. Limpieza tras Error
Si una tarea falla, asegúrate de cerrar sus recursos (sockets, archivos). Usa siempre bloques `finally:` dentro de tus corrutinas.

## Resumen: Supervisión Activa
Un desarrollador backend senior nunca "lanza y olvida" (Fire and Forget) una tarea sin una estrategia de captura de errores. Cada tarea es un hilo lógico de ejecución que debe estar bajo control, ya sea mediante `gather`, `TaskGroup` o un manejador global.
