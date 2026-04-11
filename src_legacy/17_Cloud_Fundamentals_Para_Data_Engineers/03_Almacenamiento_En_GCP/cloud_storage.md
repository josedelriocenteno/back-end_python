# Cloud Storage (GCS): El disco duro de la nube

Google Cloud Storage (GCS) es un servicio de almacenamiento de objetos diseñado para guardar cualquier cantidad de datos de forma segura, duradera y escalable. Es la base de cualquier Data Lake en Google Cloud.

## 1. Conceptos Fundamentales
- **Bucket (Cubo):** Es el contenedor raíz donde guardas tus datos. El nombre del bucket debe ser **único a nivel mundial** en todo Google Cloud.
- **Objeto:** Es el archivo individual (un .csv, un .jpg, un .parquet). Puede tener un tamaño de hasta 5 Terabytes.
- **Metadatos:** Información adicional sobre el objeto (ej: quién lo subió, tipo de contenido).

## 2. No es un Sistema de Archivos tradicional
Aunque GCS permite usar barras (`/`) en los nombres de los archivos para simular carpetas (ej: `logs/2024/03/datos.txt`), en realidad es un almacenamiento "plano".
- **Ventaja:** Puedes leer millones de archivos en paralelo mucho más rápido que en un disco duro tradicional.

## 3. Durabilidad y Disponibilidad
- **Durabilidad:** Google garantiza el **99.999999999%** (11 nueves). Es casi imposible perder un dato por un fallo de Google.
- **Disponibilidad:** Depende de si eliges un bucket Regional, Multi-regional o Zonal.

## 4. Ingesta de Datos a GCS
- **Consola Web:** Para archivos pequeños.
- **gsutil / gcloud:** Herramientas de terminal para subidas masivas.
- **Storage Transfer Service:** Para mover Petabytes desde AWS S3, Azure o servidores locales de forma automática.

## 5. El rol del Data Engineer
Para nosotros, GCS es el lugar donde aterrizan los datos crudos (Landing Zone). Es el primer paso de cualquier pipeline antes de enviarlos a BigQuery o procesarlos con Spark.

## Resumen: Fiabilidad Total
GCS es el servicio más estable de GCP. Aprender a organizar buckets y objetos de forma eficiente es el primer paso para construir una arquitectura de datos profesional y escalable.
