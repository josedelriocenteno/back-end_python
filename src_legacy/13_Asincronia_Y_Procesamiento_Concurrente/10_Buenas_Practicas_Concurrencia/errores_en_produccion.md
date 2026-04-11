# Errores en Producción: Lecciones Aprendidas

Aquí recopilamos incidentes reales que han ocurrido en sistemas backend de alta escala relacionados con la concurrencia. Aprender de los errores ajenos es lo que te hace un arquitecto senior rápidamente.

## 1. El Incidente de la "Cascada de Fallos"
- **Qué pasó:** Una API externa empezó a tardar 30s en responder. El backend async no tenía timeouts.
- **Resultado:** En 5 minutos, miles de peticiones se acumularon en el Event Loop esperando. El servidor se quedó sin RAM y explotó.
- **Lección:** **Siempre pon timeouts** en todas las llamadas de red, sin excepción.

## 2. La base de datos "Muerta por Mil Cortes"
- **Qué pasó:** Se migró una App de síncrona a asíncrona. De repente, la base de datos empezó a rechazar conexiones.
- **Resultado:** La App async era tan eficiente que lanzaba 500 queries por segundo (antes solo 10). La base de datos no pudo aguantar tal cantidad de conexiones simultáneas.
- **Lección:** Usa pools de conexiones limitados y semáforos para no "asesinar" a tus infraestructuras de datos.

## 3. El Bug del "Usuario Cruzado"
- **Qué pasó:** Un desarrollador usó una variable global para guardar temporalmente el ID del usuario en una App async.
- **Resultado:** Bajo carga, el Usuario A veía los datos del Usuario B porque el Event Loop intercambió las tareas a mitad de ejecución y sobrescribió la variable global.
- **Lección:** **Nunca uses estado global mutable** en aplicaciones concurrentes.

## 4. El "Zombie Memory Leak"
- **Qué pasó:** Se creaban tareas en segundo plano para enviar notificaciones, pero algunas tareas tenían un bug que las hacía entrar en un bucle infinito.
- **Resultado:** Al cabo de una semana, el servidor tenía 50.000 tareas "zombies" consumiendo toda la CPU.
- **Lección:** Monitoriza el número de tareas activas en tu Event Loop y usa alertas si sube de forma anormal.

## 5. El fallo del "Reintento Infinito"
- **Qué pasó:** Una tarea que fallaba por un error de lógica se reintentaba infinitamente cada 1 segundo.
- **Resultado:** Los logs se llenaron de terabytes de basura en una hora, agotando el espacio en disco del servidor.
- **Lección:** Implementa siempre un **límite máximo de reintentos** y una Dead Letter Queue (DLQ).

## Resumen: La Experiencia es el nombre que damos a nuestros errores
La concurrencia magnifica los pequeños errores. Lo que en un script pequeño es una curiosidad, en un backend distribuido es una catástrofe. Diseña siempre pensando en el "Peor Caso Posible" y blinda tus procesos contra la latencia, el fallo y la sobrecarga.
