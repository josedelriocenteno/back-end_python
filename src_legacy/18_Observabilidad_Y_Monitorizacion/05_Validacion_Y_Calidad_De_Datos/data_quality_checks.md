# Data Quality Checks: Estrategias de implementación

No todas las validaciones deben ocurrir en el mismo momento. Para ser eficiente, debes aplicar diferentes niveles de chequeo según la fase de tu pipeline.

## 1. Validaciones en Ingesta (Nivel 1)
Ocurren nada más recibir el dato (Bronze/Raw).
*   **Objetivo:** Detectar si el archivo está corrupto o si el esquema ha cambiado drásticamente.
*   **Acción:** Si falla aquí, solemos parar el pipeline (**Stop the world**). No queremos basura en nuestro lago de datos.

## 2. Validaciones en Transformación (Nivel 2)
Ocurren mientras limpiamos y unimos datos (Silver).
*   **Objetivo:** Asegurar la lógica de negocio.
*   **Chequeos:** ¿Hay muchos nulos tras el Join? ¿Las sumas cuadran?
*   **Acción:** Alertar (Warning). El pipeline puede seguir, pero hay que investigar por qué hay pérdida de datos.

## 3. Validaciones en Consumo (Nivel 3)
Ocurren en las tablas finales (Gold) antes de que el BI las lea.
*   **Objetivo:** Garantizar el SLA con el cliente interno.
*   **Chequeos:** ¿La tabla se ha actualizado hoy? ¿Los valores extremos (outliers) son razonables?
*   **Acción:** Alerta crítica y marcar el dato como "pendientes de validación" en el dashboard.

## 4. Tipos de Tests de Calidad
*   **Unit Tests de Datos:** Validar una muestra pequeña y estática (fija).
*   **Data Profiling:** Comparar las estadísticas de hoy (media, max, min) con las de los últimos 7 días. Si la media de ventas cae un 90% de repente, hay un problema de calidad.
*   **Anomaly Detection:** Uso de algoritmos sencillos para detectar datos que se salen de lo normal automáticamente.

## 5. Automatización de la Respuesta
¿Qué haces cuando falla un chequeo de calidad?
*   **Quarantine (Cuarentena):** Mueve las filas malas a una tabla de errores y deja que las filas buenas sigan su camino.
*   **Dead Letter Office:** Guarda los archivos originales fallidos en una carpeta especial para que un humano los revise y los vuelva a procesar tras arreglar el script.

## Resumen: Calidad en capas
Un sistema de calidad robusto es aquel que protege el dato en cada paso del camino. No confíes en un único chequeo al final; valida temprano, valida a menudo y valida siempre pensando en el impacto que tendrá el error en el usuario final.
