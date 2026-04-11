# Formatos de Archivo: CSV vs JSON vs Parquet

Elegir el formato de archivo correcto puede reducir el coste de tu infraestructura en un 90% y multiplicar la velocidad por 10. No es una decisión trivial.

## 1. Formatos de Fila (Row-based)
Guardan la información registro a registro.
- **CSV:** Muy simple, legible por humanos. Pésimo rendimiento (todo es texto, no tiene tipos).
- **JSON:** Muy flexible, estándar de web. Lento de procesar en volúmenes gigantes porque hay que parsear cada llave en cada fila.
- **Uso:** Intercambio de datos, configuración, ingesta inicial.

## 2. Formatos de Columna (Columnar-based)
Guardan la información columna a columna.
- **Parquet:** El estándar moderno de Big Data. Guarda los datos de forma comprimida y organizada por columnas.
- **ORC:** Similar a Parquet, muy optimizado para el ecosistema Hadoop/Hive.

## 3. Por qué Parquet es el Rey
Si tienes una tabla con 100 columnas y solo quieres sumar la columna "Ventas":
- En **CSV**: Tienes que leer TODAS las filas y TODAS las columnas (mucho I/O de disco innecesario).
- En **Parquet**: El sistema salta directamente a la zona del archivo donde están las ventas. Es órdenes de magnitud más rápido y barato.

## 4. Comparativa de Rendimiento
| Formato | Velocidad Lectura | Peso en Disco | Tipado Nativo |
| :--- | :--- | :--- | :--- |
| **CSV** | Lenta | Pesado | No |
| **JSON** | Media | Pesado | Sí (básico) |
| **Parquet** | Muy Rápida | Muy Ligero | Sí (fuerte) |

## 5. Avro: El equilibrio binario
Avro es binario y guarda el esquema, pero es de filas. Es excelente para sistemas de streaming (Kafka) donde envías mensajes uno a uno y necesitas que el receptor sepa qué campos esperar.

## Resumen: Columnas para Analítica
Para procesos de Ingeniería de Datos y Analítica, **Parquet** es casi siempre la respuesta correcta. Reduce el almacenamiento, acelera las queries y es compatible con todas las herramientas modernas (Spark, BigQuery, AWS Athena).
