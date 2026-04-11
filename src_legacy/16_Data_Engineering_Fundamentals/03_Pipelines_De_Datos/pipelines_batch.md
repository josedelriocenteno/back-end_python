# Pipelines Batch: Procesamiento por Lotes

El procesamiento batch es el modelo clásico: se procesan grandes volúmenes de datos en intervalos de tiempo programados (ej: cada hora, cada día).

## 1. Funcionamiento del Batch
El sistema espera a que se acumule una cantidad de datos ("lote") y luego los procesa todos a la vez. Es ideal para reportes diarios o procesamientos masivos que no requieren respuesta inmediata.

## 2. Ventajas del Batch
- **Cómputo Eficiente:** Procesar 1 millón de registros a la vez suele ser más barato que procesar un registro 1 millón de veces individuales.
- **Simplicidad:** Es más fácil depurar y monitorizar que los sistemas en tiempo real.
- **Tolerancia a errores:** Si el proceso falla, simplemente se vuelve a lanzar el lote completo.

## 3. Desventajas: El "Data Staleness" (Datos caducos)
El principal problema es el retraso. Si el pipeline corre cada 24 horas, tus decisiones de negocio siempre se basan en lo que pasó ayer.

## 4. Herramientas Estándar
- **Apache Spark:** El motor por excelencia para batch a gran escala.
- **SQL (BigQuery, Redshift):** Muchos procesos batch son simplemente queries programadas.
- **Airflow:** El orquestador que decide cuándo arranca cada lote.

## 5. Caso de Uso: Contabilidad
Cerrar las ventas del día. No necesitas saber el total de ventas del mes en tiempo real cada segundo. Basta con un proceso batch a las 00:01 cada noche.

## Resumen: El Caballo de Batalla
Aunque el tiempo real es atractivo, el procesamiento batch sigue siendo el responsable del 80% de los datos estructurados en el mundo corporativo por su robustez y bajo coste.
