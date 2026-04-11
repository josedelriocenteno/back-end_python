# Anti-patrones de Programación Asíncrona

Escribir código `async` es fácil; escribir código `async` que funcione bien en producción es difícil. Evita estos errores clásicos que suelen cometer los desarrolladores que vienen del mundo síncrono.

## 1. Bloquear el Event Loop con I/O Síncrono
Es el error más común y destructivo.
- **Mal:** Usar `requests.get()` o `time.sleep()` dentro de una función `async`.
- **Por qué:** Estas funciones no tienen el mecanismo de "ceder el turno" (no tienen `await` interno). Bloquean a todos los demás usuarios de tu backend.
- **Solución:** Usa `httpx.get()` y `asyncio.sleep()`.

## 2. Bloquear el Event Loop con CPU Intenso
Hacer un cálculo matemático pesado (ej: procesar un CSV de 10GB) dentro de un `async def`.
- **Solución Senior:** Si tienes que hacer algo pesado, sácalo del hilo de async usando `asyncio.to_thread()` o `run_in_executor()`. Esto pasará la tarea a un hilo o proceso aparte para que el Event Loop siga libre.

## 3. El "Virus Async" (No ser 100% Async)
Tener una App asíncrona pero usar una librería de base de datos síncrona vieja. 
- **Problema:** En cuanto la App tenga 10 usuarios simultáneos, se comportará como una App síncrona lenta. Toda la infraestructura `async` será inútil si hay un solo cuello de botella síncrono en el camino del dato.

## 4. No gestionar errores en Tareas de fondo
Crear una tarea con `create_task()` y no envolverla en un `try/except`.
- **Consecuencia:** Si la tarea falla, Python registrará un error silencioso que es muy difícil de debuguear. Nunca dejes una tarea de fondo sin supervisión.

## 5. Abuso de `asyncio.gather()`
Meter 1.000 tareas en un `gather()` a la vez contra una base de datos.
- **Riesgo:** Vas a saturar el pool de conexiones de la DB o vas a agotar los descriptores de archivos del SO.
- **Solución:** Usa un **Semáforo** (`asyncio.Semaphore(10)`) para limitar cuántas tareas pueden estar activas simultáneamente.

## Resumen: Cooperación, no Egoísmo
El mundo asíncrono se basa en la cooperación. Cada función debe actuar pensando en las demás, soltando la CPU lo antes posible (`await`). Si una función es "egoísta" y se queda con la CPU demasiado tiempo, arruina el rendimiento de toda la arquitectura.
