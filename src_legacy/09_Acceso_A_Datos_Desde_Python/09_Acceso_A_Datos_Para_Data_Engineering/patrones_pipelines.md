# Patrones de Pipelines de Datos con SQL

En Data Engineering, SQL y Python no son solo herramientas de consulta; son los eslabones de una cadena de transformación llamada **Pipeline** o **Workflow**.

## 1. El Patrón ELT (Extract, Load, Transform)

Tradicionalmente se usaba ETL, pero con bases de datos modernas preferimos ELT:
1.  **Extract:** Sacamos datos del origen (API, CSV, otra DB).
2.  **Load:** Los cargamos tal cual ("Raw") en una tabla de `staging` de nuestra base de datos Postgres.
3.  **Transform:** Usamos la potencia de SQL (CTEs, Window Functions, Triggers) para limpiar y modelar los datos dentro de la propia base de datos.

*   **Por qué:** Postgres suele ser más rápido transformando datos que cargándolos en la memoria de Python.

## 2. Idempotencia: La Regla de Oro

Un pipeline debe ser **Idempotente**: si lo ejecutas dos veces con los mismos datos, el resultado final en la base de datos debe ser el mismo (sin duplicados ni errores).
*   **Herramienta:** El `UPSERT` (ON CONFLICT) es la clave para la idempotencia.

## 3. Manejo de Estados (Checkpointing)

Para las cargas incrementales, necesitamos guardar "dónde nos quedamos".
*   **Patrón:** Tabla de `pipelines_metadata` con los campos: `pipeline_name`, `last_success_ts`, `rows_processed`.
```sql
SELECT * FROM source WHERE updated_at > (SELECT last_success_ts FROM pipelines_metadata WHERE name = 'user_sync');
```

## 4. El Patrón "Dead Letter Queue" (DLQ) en BD

Si una fila de datos está corrupta y hace que el pipeline falle:
1.  Captura el error en Python.
2.  Inserta la fila fallida en una tabla de `quarantine_logs` con el motivo del error.
3.  Continúa procesando el resto de las filas.

## 5. Orquestación: De Python a la Nube

Para pipelines complejos, no basta con un script de Python. Se usan orquestadores como:
*   **Apache Airflow:** Define workflows como grafos (DAGs) de tareas Python/SQL.
*   **Prefect / Dagster:** Versiones modernas y más amigables del mismo concepto.

## Resumen: SQL como Motor de Procesamiento

Como Data Engineer, tu objetivo es mover la menor cantidad de datos posible y hacerlo de la forma más fiable. SQL es tu mejor lenguaje para transformar, y Python es tu mejor pegamento para orquestar.
