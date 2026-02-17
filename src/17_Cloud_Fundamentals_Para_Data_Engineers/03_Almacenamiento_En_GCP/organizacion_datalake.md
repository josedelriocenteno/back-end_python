# Organización del Data Lake en GCS

Un Data Lake sin estructura se convierte rápidamente en un "Pantano de Datos" (Data Swamp). La organización de carpetas y nombres es vital para que tus pipelines funcionen.

## 1. Arquitectura de Capas (Medallion Architecture)
Es el estándar de la industria:
- `gs://mi-bucket/bronze/` (Crudo): Datos tal cual vienen de la fuente. Inmutables.
- `gs://mi-bucket/silver/` (Limpio): Datos filtrados, enriquecidos y con tipos de datos corregidos.
- `gs://mi-bucket/gold/` (Negocio): Datos agregados listos para analítica o modelos de ML.

## 2. Particionado por Fecha
Siempre organiza tus datos de ingesta por año, mes y día. Esto permite que tus procesos solo lean lo que necesitan.
- **BIEN:** `gs://bucket/ingesta/ventas/year=2024/month=03/day=15/datos.parquet`
- **MAL:** `gs://bucket/ventas_totales.csv` (Este archivo pesará gigas y será imposible de leer por partes).

## 3. Nomenclatura de Archivos
- Usa formatos binarios como **Parquet** o **Avro** para las capas Silver y Gold.
- Incluye el timestamp en el nombre si es posible: `ventas_20240315_1000.parquet`.

## 4. Buckets Separados vs. Carpetas
- **Buckets Separados:** Si necesitas seguridad muy estricta (ej: el equipo de Marketing no debe tener permiso ni de ver la carpeta de Finanzas).
- **Carpetas en el mismo Bucket:** Más fácil de gestionar si el equipo es pequeño y todos trabajan sobre la misma base de datos.

## 5. Metadata Tagging
Usa etiquetas en los buckets para saber a qué departamento pertenecen y quién es el responsable de los costes.

## Resumen: Diseño Limpio
Dedica tiempo a diseñar tu estructura de carpetas antes de subir el primer archivo. Un Data Lake ordenado facilita la automatización, mejora la seguridad y hace que los nuevos miembros del equipo sean productivos en minutos.
