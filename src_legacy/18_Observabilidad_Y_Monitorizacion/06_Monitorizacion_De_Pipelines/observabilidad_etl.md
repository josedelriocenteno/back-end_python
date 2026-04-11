# Observabilidad en ETL: El ciclo de vida del dato

Un proceso ETL (Extract, Transform, Load) es el flujo circulatorio de una empresa. Si se detiene o se contamina, los órganos (los departamentos de negocio) dejan de funcionar.

## 1. Monitorizando la Extracción (Extract)
*   **Disponibilidad de la fuente:** ¿La API de origen responde? ¿La base de datos de producción nos deja conectar?
*   **Volumen esperado:** ¿Ha llegado el archivo que esperábamos a las 8 AM?
*   **Timeouts:** Si la extracción suele tardar 5 min y hoy lleva 30 min, probablemente la fuente está saturada o hay un problema de red.

## 2. Monitorizando la Transformación (Transform)
*   **Uso de memoria y CPU:** Los procesos Spark o Pandas pueden ser muy pesados. Hay que vigilar que no se queden sin memoria (`OOM - Out of Memory`).
*   **Tiempos de cómputo por etapa:** ¿Qué paso de la transformación es el cuello de botella?
*   **Registros descartados:** Cada vez que filtras datos, debes loguear cuántos has quitado y por qué (ej: "50 filas descartadas por valor nulo en email").

## 3. Monitorizando la Carga (Load)
*   **Latencia de escritura:** ¿Cuánto tarda BigQuery o Postgres en aceptar los datos?
*   **Errores de inserción:** Duplicados, fallos de clave foránea o de tipo de dato.
*   **Post-load checks:** Hacer un `count(*)` en origen y otro en destino para asegurar que no se han perdido datos por el camino.

## 4. El concepto de "Data Lineage"
Monitorizar no es solo ver el fallo hoy, es poder ver la historia. Si una tabla Gold está mal, la observabilidad debe permitirte viajar hacia atrás hasta la tabla Silver y Bronze para encontrar dónde se introdujo el error.

## 5. Metadata de ejecución
Cada vez que corras el ETL, guarda el resultado en una tabla de metadatos:
- `job_id`, `start_time`, `end_time`, `status`, `rows_inserted`, `rows_failed`.
Esta tabla es la mejor fuente para crear dashboards de rendimiento a largo plazo.

## Resumen: Control total del flujo
La observabilidad en ETL transforma un proceso oscuro en una tubería transparente donde puedes ver exactamente dónde está el dato, cuánto tiempo tarda en moverse y si mantiene su integridad en cada paso.
