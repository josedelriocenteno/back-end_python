# Errores Reales con FastAPI y Asyncio

En el desarrollo de APIs profesionales, no todo es color de rosa. Estos son los incidentes de producción más comunes relacionados con la asincronía y cómo evitarlos.

## 1. El Bloqueo Silencioso (Starvation)
- **Escenario:** Un endpoint `async def` usa una librería de procesamiento de imágenes síncrona.
- **Resultado:** Mientras se procesa una imagen, el servidor parece estar "caído" para todos los demás.
- **Debugging:** Mira los logs. Si ves que las peticiones se encolan y tardan exactamente lo mismo que el tiempo de procesamiento de la imagen, tienes un bloqueo de hilo.

## 2. Gotas de Memoria (Tasks Fantasma)
- **Escenario:** Crear tareas con `asyncio.create_task()` en un endpoint sin guardarlas en ninguna parte ni esperar su resultado.
- **Resultado:** Las tareas pueden quedarse "vivas" indefinidamente si tienen un bug, consumiendo RAM poco a poco hasta que el servidor explota (OOM - Out of Memory).

## 3. Context Variables Perdidas
- **Escenario:** Usar variables globales o el contexto de la petición para guardar datos del usuario.
- **Problema:** En el mundo async, el contexto puede perderse o mezclarse si no usas `ContextVars`.
- **Solución:** FastAPI gestiona esto bien con su inyección de dependencias, pero ten cuidado si usas hilos manuales dentro de una App async.

## 4. Timeouts de Base de Datos Inesperados
- **Escenario:** Tienes 500 tareas async intentando entrar a una DB con un pool de 20 conexiones.
- **Resultado:** La mayoría de tareas lanzarán un error de timeout al intentar obtener la conexión.
- **Solución Senior:** Implementa semáforos o aumenta el tamaño del pool basándote en la capacidad real de tu base de datos.

## 5. El error del "Doble Respuesta"
- **Escenario:** Intentar devolver una respuesta al cliente y luego seguir haciendo cosas que también intentan modificar la respuesta o lanzar errores.
- **Resultado:** Errores de "Headers already sent" o comportamiento errático en los middlewares.

## Resumen: Producción es diferente
Desarrollar en local con un solo usuario es fácil. El verdadero desafío de la asincronía surge cuando tienes 100 peticiones por segundo. La clave es monitorizar siempre el Event Loop y tener alertas para cuando detectes que una tarea está tardando demasiado tiempo en ceder el turno (Blocking calls detection).
