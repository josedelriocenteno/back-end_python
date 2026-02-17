# Jobs en Segundo Plano (Background Jobs) y Diferidos

En una arquitectura de backend profesional, no todo ocurre "ahora". Existen trabajos que deben ejecutarse en el futuro o de forma recurrente (Cron).

## 1. Diferencia entre Tarea Async y Background Job
- **Tarea Async (`create_task`):** Vive y muere con la petición HTTP o el proceso actual.
- **Background Job (Celery/RQ):** Es una unidad de trabajo que se guarda en una DB (Redis/Postgres) y que sobrevive aunque el servidor se reinicie.

## 2. Tipos de Trabajos
- **Inmediatos:** "Haz esto en cuanto puedas" (ej: redimensionar foto tras subirla).
- **Diferidos (Delayed):** "Haz esto dentro de 2 horas" (ej: enviar recordatorio de carrito abandonado).
- **Recurrentes (Periodic):** "Haz esto cada lunes a las 8:00 AM" (ej: generar facturas mensuales).

## 3. Visibilidad y Retries
Un Background Job profesional debe tener:
- **Estados:** Pending, Working, Success, Failed.
- **Auto-Retry:** Si el worker se cae, el sistema detecta que la tarea no se terminó y la vuelve a encolar automáticamente.
- **Visibilidad:** Una interfaz (Dashboard como Flower para Celery) donde ver cuántas tareas hay pendientes.

## 4. El "Payload" del Job
- **NUNCA:** Pases objetos complejos (instancias de clases de Python) a un Job.
- **SIEMPRE:** Pasa IDs (strings o enteros). El worker leerá el ID y buscará los datos frescos en la base de datos en el momento de la ejecución. Esto evita inconsistencias de datos.

## 5. El problema del "Zombie Job"
Si un job tarda más de lo previsto, el sistema de colas puede pensar que el worker ha muerto y lanzar la misma tarea en otro worker.
- **Solución:** Bloqueos distribuidos (Locks de Redis) o asegurar que tus tareas son **idempotentes**.

## Resumen: Fuera del Ciclo de Vida
Mover la lógica pesada a Background Jobs es la forma número uno de mejorar la experiencia de usuario (la App se siente instantánea) y la estabilidad del servidor. Aprender a gestionar estas tareas "fuera de la vista" es una marca distintiva de un desarrollador backend de alto nivel.
