# Formatos Óptimos: ¿Por qué Parquet es el Rey?

Elegir el formato de archivo en tu Data Lake es probablemente la decisión que más afecta al rendimiento de tus pipelines de datos.

## 1. Formatos de Fila (CSV, JSON, Avro)
Los datos de una fila se guardan juntos.
*   **Uso:** Excelente para escribir datos nuevos (Ingesta) y para sistemas de mensajería (Kafka ama Avro).
*   **Problema:** Si quieres sumar una columna en un archivo de 100GB, tienes que leerlo todo.

## 2. Formatos Columnares (Parquet, ORC)
Los datos de una columna se guardan juntos. Es el estándar de oro en Data Engineering.
*   **Ventaja 1: Compresión.** Como todos los datos de una columna son del mismo tipo (ej: números), se comprimen de forma increíblemente eficiente.
*   **Ventaja 2: Proyección.** Si pides solo 2 columnas de 100, el motor solo lee físicamente los trozos del disco donde están esas 2 columnas. Ahorras el 98% del I/O.
*   **Ventaja 3: Metadatos.** Los archivos Parquet guardan el mínimo y máximo de cada columna. El motor puede ignorar archivos enteros si sabe que el valor que buscas no está en ese rango.

## 3. Comparativa Real
*   **CSV (1GB):** Lento de leer, ocupa mucho espacio, no tiene tipos de datos (todo es texto).
*   **Parquet (200MB):** Rápido de leer, tipos de datos integrados (Integer, Date, etc.), esquema definido.

## 4. Cuándo usar cada uno
*   **JSON:** Para intercambio de datos entre APIs o logs donde la flexibilidad es clave.
*   **Avro:** Para almacenamiento intermedio en Streaming donde necesitas escribir muy rápido.
*   **Parquet:** Siempre para almacenamiento final y analítica masiva.

## 5. Particionado en el Sistema de Archivos
En un Data Lake (S3/GCS), guardamos los archivos Parquet en carpetas: `year=2024/month=01/data.parquet`.
*   Esto permite al motor de procesamiento (Spark/Trino) ir directamente a la carpeta que necesita, emulando el comportamiento de las particiones de una base de datos SQL.

## Resumen: El lenguaje del Almacenamiento
Si quieres performance, deja de usar CSV y JSON para datos masivos. Migrar a un formato columnar como Parquet es la optimización más barata y efectiva que existe: ahorras espacio en disco, red y tiempo de CPU en cada consulta.
