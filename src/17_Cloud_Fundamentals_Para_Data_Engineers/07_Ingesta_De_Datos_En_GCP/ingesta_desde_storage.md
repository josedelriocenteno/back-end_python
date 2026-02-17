# Ingesta desde Cloud Storage a BigQuery

La forma más común y barata de cargar datos en BigQuery es mover archivos desde un Bucket de Cloud Storage. Este proceso se conoce como "Batch Loading".

## 1. ¿Por qué Ingestar desde GCS?
- **Gratis:** Google no cobra por la ingesta de datos desde GCS a BigQuery. Solo pagas por el almacenamiento final.
- **Detección Automática:** BigQuery puede analizar el archivo y crear el esquema de la tabla automáticamente.
- **Gran Volumen:** Puedes cargar Terabytes de datos en una sola operación de forma muy rápida.

## 2. Formatos Soportados
De mejor a peor rendimiento:
1. **Avro / Parquet:** (Recomendado). Binarios, contienen el esquema y los tipos de datos.
2. **JSON (Newlines):** Cada fila es un objeto JSON en una línea nueva.
3. **CSV:** El más simple pero propenso a errores (comas dentro de textos, tipos de datos mal detectados).

## 3. Comandos de Ingesta (bq load)
Aunque puedes usar la consola web, el Data Engineer usa el comando `bq` en la terminal:
```bash
bq load --source_format=PARQUET mi_dataset.mi_tabla gs://mi-bucket/datos/ventas_*.parquet
```

## 4. Configuración de Carga
- **Write Mode:** `WRITE_APPEND` (Añadir al final) o `WRITE_TRUNCATE` (Borrar y volver a escribir).
- **Max Errors:** Número de errores permitidos antes de que la carga falle.
- **Schema Autodetect:** `-autodetect`. Muy útil para archivos JSON pero úsalo con cuidado en producción para evitar cambios de esquema inesperados.

## 5. Cargas Periódicas
Lo habitual es que un proceso (ej: Airflow) suba archivos a GCS cada hora y luego dispare un comando de carga a BigQuery. Esto mantiene el Data Warehouse actualizado de forma predecible y barata.

## Resumen: Fiabilidad Batch
Cargar desde GCS es la base del modelo ELT. Es una operación extremadamente robusta y eficiente que permite mover grandes históricos de datos hacia el motor analítico sin complicaciones técnicas ni costes sorpresa.
