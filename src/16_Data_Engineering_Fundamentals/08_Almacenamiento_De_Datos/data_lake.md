# Data Lake: El océano de datos crudos

Un Data Lake (Lago de Datos) es un repositorio centralizado que permite almacenar todos tus datos, tanto estructurados como no estructurados, a cualquier escala.

## 1. Filosofía: Guardar Primero, Estructurar Después
A diferencia del Data Warehouse, en un Data Lake no necesitas definir el esquema antes de guardar el dato. Esto permite capturar información de la que aún no sabes el valor.

## 2. Tecnologías Comunes
- **Cloud Object Storage:** AWS S3, Google Cloud Storage, Azure Data Lake Storage (ADLS).
- **On-Premise:** HDFS (Hadoop Distributed File System).

## 3. Capas del Data Lake (Medallion Architecture)
Para evitar que el lago se convierta en un **Data Swamp** (Pantano de Datos), se organiza en capas:
1. **Bronze (Raw):** Datos crudos, tal cual vienen de la fuente. Sin limpiar.
2. **Silver (Cleansed):** Datos filtrados, unidos y normalizados. Listos para analítica técnica.
3. **Gold (Curated):** Datos agregados y modelados por negocio. Listos para dashboards.

## 4. Ventajas
- **Bajo Coste:** Guardar archivos en S3 es infinitamente más barato que guardarlos en una base de datos relacional.
- **Flexibilidad:** Puedes guardar imágenes, vídeos, JSONs y CSVs en el mismo sitio.
- **Histórico Infinito:** Puedes mantener versiones crudas de los datos de hace años por un coste mínimo.

## 5. El peligro del Data Swamp
Si no hay gobierno (documentación, metadatos y limpieza), el Data Lake se vuelve inútil porque nadie sabe qué hay dentro ni si los datos son fiables.

## Resumen: El primer hogar del dato
El Data Lake es el punto de aterrizaje universal. Es la memoria a largo plazo de la empresa y la base sobre la que se construyen todos los procesos de Machine Learning y Big Data.
