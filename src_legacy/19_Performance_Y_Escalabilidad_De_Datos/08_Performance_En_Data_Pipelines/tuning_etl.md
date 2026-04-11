# Tuning de procesos ETL: Estrategias de Afinamiento

Un proceso ETL (Extract, Transform, Load) mal afinado puede tardar horas en hacer lo que uno bien optimizado hace en minutos. Aquí tienes técnicas para "trucar" tus pipelines.

## 1. Filtrado Temprano (Pushdown)
Nunca traigas datos que vas a descartar después.
*   **Mal:** Lees toda la tabla SQL -> La pasas a Python -> Filtas por `pais = 'ES'`.
*   **Bien (Predicate Pushdown):** Haces la query `SELECT * FROM tabla WHERE pais = 'ES'`. La base de datos, que es experta en filtrar, te envía solo lo que necesitas, ahorrando red y memoria.

## 2. Proyección de Columnas
Pide solo lo que uses.
*   Si solo necesitas la `id` y el `total`, no pidas las 50 columnas de la tabla. Reducir el ancho de banda es la forma más rápida de acelerar una ETL.

## 3. Caché de Pasos Intermedios
Si tu pipeline tiene 10 etapas y la etapa 5 es carísima (ej: un Join complejo):
*   Guarda el resultado de la etapa 5 en un archivo temporal (Parquet) o en memoria (Spark Cache).
*   Si la etapa 6 falla y tienes que reintentar, no tendrás que volver a ejecutar las etapas 1 a 5.

## 4. El peligro de los Joins en Python
Python es lento uniendo tablas gigantes en memoria comparado con los motores de bases de datos.
*   Si puedes hacer el `JOIN` en la base de datos de origen (Postgres/BigQuery), hazlo allí.
*   Si tienes que hacerlo en Python, usa librerías vectorizadas como **Polars** o **Pandas** (con `merge` optimizado) en lugar de bucles `for`.

## 5. Escritura Masiva (Bulk Load)
Nunca insertes filas de una en una (`INSERT INTO...`).
*   **Acción:** Genera un archivo CSV/Parquet y usa el comando `COPY` (Postgres) o herramientas de carga masiva del proveedor. Es órdenes de magnitud más rápido y menos propenso a bloqueos.

## Resumen: Eficiencia en cada paso
Optimizar una ETL es un juego de eliminación de desperdicios: menos datos por la red, menos columnas en memoria y menos operaciones redundantes. Aplica estas técnicas y verás cómo tus pipelines no solo son más rápidos, sino también mucho más fiables y económicos.
