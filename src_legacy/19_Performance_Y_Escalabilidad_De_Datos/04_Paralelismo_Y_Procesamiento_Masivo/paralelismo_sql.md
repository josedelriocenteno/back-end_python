# Paralelismo en SQL: Multi-Worker Processing

Los motores de bases de datos modernos pueden usar varios núcleos de la CPU para ejecutar una sola consulta SQL, reduciendo drásticamente el tiempo de respuesta.

## 1. ¿Cómo funciona el Paralelismo en SQL?
El optimizador divide la query en tareas más pequeñas que se ejecutan en paralelo por varios **Workers** (trabajadores). Al final, un proceso "líder" recoge los resultados y los une.
*   **Ejemplo:** En lugar de leer una tabla de 100GB con un hilo, usa 4 hilos para leer 25GB cada uno de forma simultánea.

## 2. Operaciones que se benefician del Paralelismo
*   **Parallel Sequential Scan:** Leer tablas gigantes.
*   **Parallel Aggregates:** Calcular `SUM`, `AVG`, `COUNT` sobre millones de filas.
*   **Parallel Hash Join:** Unir dos tablas grandes usando varios núcleos.
*   **Parallel Index Build:** Crear un índice nuevo mucho más rápido.

## 3. Limitaciones del Paralelismo
*   **Overhead de Gestión:** Dividir la tarea y recoger los resultados consume algo de tiempo. Si la tabla es pequeña, el paralelismo puede ser MÁS lento que la ejecución normal.
*   **Recueros de CPU:** Si tu servidor tiene 8 núcleos y lanzas una query con 8 workers, el resto de usuarios o tareas se quedarán sin CPU.
*   **Escritura:** Tradicionalmente, las operaciones `INSERT`, `UPDATE` y `DELETE` no se ejecutaban en paralelo en muchos motores, aunque esto está cambiando en las versiones más recientes.

## 4. Configuración en PostgreSQL
Puedes controlar cuántos hilos usar mediante parámetros:
*   `max_parallel_workers_per_gather`: Máximo número de hilos para una query.
*   `min_parallel_table_scan_size`: Tamaño mínimo de la tabla para activar el paralelismo.

## 5. Cuándo saber que está funcionando
Mira tu `EXPLAIN`. Si ves operaciones como `Gather` o `Parallel Seq Scan`, felicidades: tu base de datos está aprovechando toda la potencia de tu hardware.

## Resumen: Potencia Oculta
El paralelismo SQL permite que las bases de datos relacionales manejen volúmenes de datos que antes solo eran posibles con sistemas de Big Data especializados. Entender cómo y cuándo el motor decide usar varios núcleos es fundamental para optimizar queries masivas.
