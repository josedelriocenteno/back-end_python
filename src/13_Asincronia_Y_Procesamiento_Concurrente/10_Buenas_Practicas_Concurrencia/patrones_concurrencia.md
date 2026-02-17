# Patrones de Concurrencia Saludables

La concurrencia añade una dimensión de complejidad al código que puede hacerlo ilegible. Aplicar patrones de diseño probados ayuda a mantener la claridad y la mantenibilidad.

## 1. Patrón "Worker Pool" (Piscina de Trabajadores)
Es el que vimos en la sección de Colas. En lugar de crear una tarea para cada ítem, creas un número fijo de trabajadores que reutilizan recursos.
- **Por qué:** Evitas la explosión de memoria y tienes un control total sobre la carga del sistema.

## 2. Patrón "Fan-Out / Fan-In"
Ideal para procesamiento de datos masivos. 
- **Fan-Out:** Un proceso reparte el trabajo.
- **Fan-In:** Un proceso recoge todos los resultados.
- **Consejo Senior:** Usa este patrón para paralelizar llamadas a APIs de terceros y consolidar la respuesta final para el usuario.

## 3. Patrón "Semaphore Choke" (Estrangulamiento)
Usar un semáforo global para limitar el acceso a un recurso físico limitado (ej: una impresora o un puerto serie).
- **Por qué:** Aseguras que no importa cuántas peticiones async lleguen, el recurso físico nunca se saturará.

## 4. Patrón "Request-Response Bridge"
Útil cuando tienes una App asíncrona pero debes comunicarte con un sistema de colas síncrono o externo.
- Consiste en asignar un `Future` a cada petición, enviarla a la cola externa y "despertar" el Future cuando la respuesta llegue por un canal diferente.

## 5. Patrón "Graceful Shutdown" (Cierre Elegante)
Un sistema concurrente senior sabe cómo morir. 
- Cuando el servidor recibe una señal de apagado (`SIGTERM`), debe dejar de aceptar tareas nuevas, esperar a que las colas se vacíen y cerrar las conexiones a DB de forma ordenada antes de salir.

## Resumen: Estructura sobre Improvisación
No lances tareas "a lo loco". Elige un patrón de diseño que se adapte a tu flujo de datos y mantente fiel a él. Un código concurrente predecible es mucho más valioso que uno marginalmente más rápido pero caótico.
