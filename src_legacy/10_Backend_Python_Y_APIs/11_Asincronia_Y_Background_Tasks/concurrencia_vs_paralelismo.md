# Concurrencia vs Paralelismo: Conceptos de Infraestructura

Estos dos términos suelen usarse como sinónimos, pero en el bajo nivel del Backend son conceptos radicalmente distintos. Entenderlos te ayudará a elegir entre `asyncio`, `threading` o `multiprocessing`.

## 1. Concurrencia (Manage many things at once)
Es la capacidad de lidiar con muchas tareas al mismo tiempo, pero no necesariamente ejecutándolas en el mismo instante exacto.
*   **Analogía:** Un camarero atendiendo 5 mesas. Toma nota en la mesa 1, mientras el cliente de la mesa 1 piensa, va a la mesa 2.
*   **En Python:** Se logra con **`asyncio`**. Es ideal para tareas de I/O (esperar a la base de datos, a una API externa o a un archivo).

## 2. Paralelismo (Do many things at once)
Es la capacidad de ejecutar múltiples tareas exactamente en el mismo nanosegundo.
*   **Analogía:** 5 camareros atendiendo 5 mesas simultáneamente.
*   **En Python:** Se logra con el módulo **`multiprocessing`**. Es necesario para tareas de cálculo intensivo (CPU Bound) donde queremos usar todos los núcleos del procesador.

## 3. El gran obstáculo: El GIL (Global Interpreter Lock)
Python tiene un mecanismo llamado GIL que impide que un proceso ejecute código Python en más de un hilo a la vez.
*   **Impacto en Concurrencia:** No afecta mucho, porque en I/O el hilo está parado esperando y el GIL se cede.
*   **Impacto en Paralelismo:** El `threading` de Python no es paralelismo real para cálculos. Si tienes 2 hilos haciendo cálculos matemáticos, tardarán LO MISMO que uno solo porque el GIL les obliga a turnarse. Por eso usamos procesos (`multiprocessing`), que crean intérpretes de Python independientes.

## 4. Cuándo usar qué en tu API

| Caso de Uso | Herramienta | Por qué |
| :--- | :--- | :--- |
| Consultas a DB / APIs | `asyncio` | Máxima eficiencia, poco consumo de RAM. |
| Generación de PDFs / Imágenes | `BackgroundTasks` | Evita bloquear el request principal. |
| Procesamiento de Video / ML | `Celery + Workers` | Sacas la carga fuera del servidor web. |
| Análisis de datos masivo (CPU) | `Multiprocessing` | Usas todos los cores de tu servidor. |

## 5. El Futuro: Proyectos No-GIL
Versiones recientes de Python están trabajando para eliminar el GIL. En el futuro, el paralelismo real en Python será mucho más sencillo y eficiente.

## Resumen: Diseña para la escala
Como desarrollador senior, tu responsabilidad es identificar dónde está el cuello de botella. ¿Es espera (I/O)? Usa concurrencia. ¿Es esfuerzo (CPU)? Usa paralelismo o saca la tarea a un worker externo.
