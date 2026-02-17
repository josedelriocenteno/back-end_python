# Stack Moderno de Datos (Modern Data Stack)

El ecosistema de herramientas de datos cambia rápido, pero hay un grupo de tecnologías que dominan el mercado profesional actual.

## 1. El lenguaje base: Python
Python es el pegamento de todo. Se usa para escribir procesos ETL, orquestar tareas y manipular datos en memoria.

## 2. El motor de consulta: SQL
A pesar de la moda "NoSQL", el mundo analítico vive y muere en SQL. Cualquier base de datos de datos masivos (BigQuery, Snowflake) usa SQL como interfaz principal.

## 3. Orquestación: Airflow / Prefect
Para gestionar dependencias entre tareas. "No ejecutes la limpieza hasta que la descarga de archivos haya terminado".

## 4. Procesamiento Distribuido: Spark
Cuando los datos no caben en la RAM de un solo servidor, usamos clústeres de máquinas. Apache Spark es el estándar para procesamiento masivo distribuido.

## 5. Transformación en el Almacén: dbt
Permite escribir transformaciones complejas usando solo SQL pero con las mejores prácticas de ingeniería de software (versionado, tests, documentación).

## 6. Almacenamiento: El Data Lakehouse
Una mezcla de:
- **Data Lake (S3 / GCS):** Ficheros crudos baratos (CSV, Parquet).
- **Data Warehouse (BigQuery):** Tablas estructuradas y rápidas para negocio.

## Resumen: Tu caja de herramientas
Como Data Engineer, no necesitas ser experto en TODO, pero debes entender cómo se conectan estas piezas: el dato entra por una **API (Python)**, se guarda en un **Lake (S3)**, se procesa con **Spark**, se carga en un **Warehouse (BigQuery)** y se visualiza en un **Dashboard**.
