# Particionado y Clustering: Velocidad y Ahorro

En BigQuery, el rendimiento y el coste están directamente unidos a cuántos datos lee tu query. El particionado y el clustering son tus armas principales para reducir esa lectura.

## 1. Particionado (Partitioning)
Divide una tabla grande en trozos basados en una columna (normalmente la fecha).
- **Cómo funciona:** Si particionas por día y haces una query de "Ventas de ayer", BigQuery **solo lee la partición de ayer** e ignora los otros 10 años de datos.
- **Tipos:** Por tiempo (`DAY`, `MONTH`, `YEAR`), por rango de enteros o por tiempo de ingesta.

## 2. Clustering
Ordena los datos dentro de cada partición basándose en el valor de ciertas columnas (ej: `id_tienda`).
- **Cómo funciona:** Los datos con el mismo ID de tienda se guardan físicamente juntos en el disco. Cuando buscas una tienda específica, BigQuery sabe exactamente qué trozo del archivo leer.
- Puedes elegir hasta 4 columnas para el clustering.

## 3. ¿Cuándo usar cada uno?
- **Particionado:** Para filtros de tiempo. Siempre que una tabla supere los 10-20GB, particiónala por fecha.
- **Clustering:** Para columnas que usas habitualmente en filtros (`WHERE`) o agrupaciones (`GROUP BY`). Funciona mejor si la columna tiene mucha variedad de valores (ej: IDs).

## 4. Partition Pruning (Poda de Particiones)
Para que el particionado funcione, **DEBES** usar la columna de partición en el `WHERE`.
- **MAL:** `SELECT * FROM ventas` (Lee toda la tabla).
- **BIEN:** `SELECT * FROM ventas WHERE fecha = '2024-03-15'` (Lee solo 1MB).

## 5. El impacto en la factura
Como BigQuery cobra por Terabytes leídos, una tabla bien particionada puede hacer que una query pase de costar 5€ a costar 0,01€. Es la optimización con mayor impacto que puede hacer un Data Engineer.

## Resumen: No leas lo que no necesitas
El particionado y el clustering no son opcionales en Big Data. Son la base para que BigQuery sea sostenible económicamente a largo plazo y para que tus dashboards carguen en milisegundos en lugar de minutos.
