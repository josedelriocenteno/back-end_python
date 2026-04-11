# Trazas en Pipelines: El linaje del dato en acción

En Ingeniería de Datos, el tracing no solo mide tiempo, mide el **viaje del dato**. Queremos saber "de qué padre viene este hijo". Esto se conoce a menudo como **Data Lineage** o trazabilidad de pipelines.

## 1. Identificando la "Unidad de Carga"
En lugar de una petición HTTP, nuestra traza es el **Job ID** o el **Batch ID**.
- Traza `Batch_2024_03_15`:
  - Span 1: Extraction from API (2 min)
  - Span 2: Validation Check (30 seg)
  - Span 3: Transformation in Sparks (15 min)
  - Span 4: Load to BigQuery (2 min)

## 2. Propagando el ID entre herramientas
Este es el mayor reto. ¿Cómo sabe BigQuery que la tabla que está escribiendo viene del Spark de antes?
*   Añadiendo una columna `metadata_trace_id` a todas tus tablas.
*   Pasando el ID como parámetro en los jobs de Airflow o los scripts de Python.

## 3. Trazabilidad a nivel de fila (Row-level Tracing)
Para sistemas ultra-críticos (finanzas, salud), a veces necesitamos saber de dónde viene **cada fila**.
- **Solución:** Una columna extra en el DataFrame llamada `source_file` o `ingestion_timestamp`.
- Esto permite que, si un mes después detectamos un error, sepamos exactamente qué archivo de origen causó ese problema.

## 4. Herramientas Especializadas
*   **OpenLineage / Marquez:** Son el estándar actual para recoger automáticamente estas trazas entre Airflow, Spark y BigQuery.
*   **Datafold / Monte Carlo:** Herramientas de "observabilidad de datos" que dibujan el mapa de dependencias de tus tablas automáticamente.

## 5. El beneficio: Debugging Retrospectivo
Si un analista dice: "El total de ventas de ayer no cuadra", con trazabilidad puedes:
1. Buscar el ID de la ejecución de ayer.
2. Ver que en el paso de "Validación" se descartaron 500 filas por formato incorrecto.
3. Identificar que el error vino del archivo del proveedor "X".

## Resumen: El mapa del tesoro
Las trazas en pipelines transforman una "caja negra" de procesos en un mapa claro de dependencias. Te permiten responder preguntas sobre el origen y la transformación del dato con total precisión y transparencia.
