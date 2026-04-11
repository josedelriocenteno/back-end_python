# Correlation IDs: Uniendo los puntos

El **Correlation ID** (o Trace ID) es el pegamento que mantiene unida toda tu estrategia de observabilidad. Es un identificador único y universal para una operación completa.

## 1. El problema de los logs sueltos
Imagina 100 usuarios usando tu API a la vez. Tus logs se verán así:
```text
10:00:01 - Peticion recibida
10:00:01 - Peticion recibida
10:00:02 - Error en base de datos
10:00:02 - Usuario logueado con éxito
```
¿De quién es el error de base de datos? Es imposible saberlo.

## 2. La solución: El ID único
Si cada petición genera un ID al entrar (`req-abc`), los logs se ven así:
```text
10:00:01 [req-abc] - Peticion recibida
10:00:01 [req-xyz] - Peticion recibida
10:00:02 [req-abc] - Error en base de datos
```
¡Ahora sí! Sabemos que el error pertenece al usuario `req-abc`.

## 3. Cómo implementarlo en Python (ContextVars)
Para no tener que pasar el `corelation_id` como argumento en todas tus funciones, Python usa `contextvars`. Las librerías de logging modernas leen de ahí automáticamente.

```python
import uuid
from contextvars import ContextVar

# Definimos la variable de contexto
correlation_id = ContextVar("correlation_id", default="no-id")

def procesar_dato():
    # El logger leerá automáticamente el valor actual de la variable
    print(f"[{correlation_id.get()}] Procesando...")

# Al inicio de la petición generamos el ID
correlation_id.set(str(uuid.uuid4()))
procesar_dato()
```

## 4. Propagación en la Red
Cuando tu script llama a otro microservicio o a una base de datos, debes enviar ese ID.
*   **En HTTP:** Cabecera `X-Correlation-Id`.
*   **En SQL:** Añadiendo un comentario al inicio de la query: `/* correlation_id: req-abc */ SELECT * FROM...`. Así aparecerá incluso en los logs de la base de datos.

## 5. El "Buscador Pro"
Cuando un cliente se queja, te dará su `order_id` o `user_id`. Tú buscas ese ID en tus logs, encuentras el `Correlation ID` asociado, y luego buscas TODAS las líneas con ese ID. Verás toda la historia de esa transacción a través de todos tus sistemas.

## Resumen: El hilo conductor
Los Correlation IDs son la herramienta más sencilla y poderosa para depurar sistemas complejos. Son la diferencia entre buscar una aguja en un pajar y tener un imán que atrae todos los datos relevantes de forma instantánea.
