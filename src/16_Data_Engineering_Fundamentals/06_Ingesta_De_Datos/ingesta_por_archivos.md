# Ingesta por Archivos: CSV, JSON y más

Mover archivos parece sencillo, pero a gran escala requiere de un control riguroso para no perder información ni procesar lo mismo dos veces.

## 1. El flujo de trabajo
1. **Detección:** ¿Hay archivos nuevos en la carpeta?
2. **Validación:** ¿El archivo está completo o se está subiendo todavía? (Usa archivos `.done` o marcas de tiempo).
3. **Lectura:** Cargar el archivo en memoria (Python) o usar un comando `COPY` nativo del Warehouse (más rápido).
4. **Archivo:** Mover el archivo procesado a una carpeta de `ARCHIVE` o `PROCESSED`.

## 2. Ingesta masiva (Bulk Load)
Si tienes 10.000 archivos CSV:
- **MAL:** Hacer un bucle en Python y leer uno a uno.
- **BIEN:** Subir los archivos a S3 y usar una herramienta como **Snowpipe** (Snowflake) o **Cloud Storage Transfer** (BigQuery) que los carga en paralelo de forma masiva.

## 3. El reto del Schema-on-Read
Como vimos en los datos semi-estructurados, archivos como JSON pueden cambiar de esquema entre archivos. Tu pipeline de ingesta debe ser capaz de detectar y manejar estas variaciones sin detenerse.

## 4. Particionado en Ingesta
Organiza tus archivos por fecha en el almacenamiento de archivos:
`s3://my-bucket/orders/year=2024/month=03/day=15/batch_1.json`
Esto permite que el pipeline sepa exactamente qué procesar en cada ejecución batch.

## 5. Tip Senior: Ingesta Atómica
Asegúrate de que un archivo se procesa entero o no se procesa nada. Evita estados donde has cargado la mitad de las filas de un CSV y el sistema falla, dejando datos incompletos.

## Resumen: Orden en el Disco
La ingesta por archivos es el método más barato y común. Mantener una estructura de carpetas lógica y un sistema de archivado post-procesamiento es la clave para un pipeline ordenado.
