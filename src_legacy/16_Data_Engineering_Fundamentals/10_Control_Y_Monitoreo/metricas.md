# Métricas: Midiendo la salud del dato

Mientras que los logs dicen "qué pasó", las métricas dicen "cómo de bien (o mal) está funcionando el sistema" a lo largo del tiempo.

## 1. Métricas de Rendimiento (Infrastructure Metrics)
- **Latencia:** Tiempo total de ejecución del pipeline.
- **Uso de CPU/RAM:** ¿Estamos saturando el servidor de Spark?
- **Tiempo de espera en colas:** ¿Están los mensajes de Kafka acumulándose más rápido de lo que podemos leerlos? (Consumer Lag).

## 2. Métricas de Datos (Data Quality Metrics)
Aquí es donde el Data Engineer se diferencia del DevOps:
- **Volumen (Volume):** ¿Cuántas filas hemos cargado hoy? Si la media es 1M y hoy han llegado 10k, algo va mal.
- **Nulidad (Null Rate):** Porcentaje de nulos en columnas críticas.
- **Freshness:** ¿Cuánto tiempo ha pasado desde el dato más reciente en la tabla hasta ahora?

## 3. Métricas de Negocio (Business Context)
- **Suma total de ventas:** Si de repente es 0, el pipeline puede estar "funcionando" técnicamente pero cargando basura.

## 4. Visualización: El Dashboard Operativo
Crea un dashboard (en Grafana, Datadog o CloudWatch) que muestre estas métricas de forma visual. Te permite detectar anomalías de un vistazo antes de que nadie se queje.

## 5. Service Level Indicators (SLI)
Define qué es un "buen servicio" para tu equipo:
- "El 99% de los pipelines deben terminar en menos de 1 hora".
- "Ninguna tabla maestra debe tener datos con más de 12 horas de antigüedad".

## Resumen: Datos sobre los Datos
Sin métricas, estás volando a ciegas. Medir el volumen, la calidad y el tiempo es lo que permite pasar de una actitud reactiva (arreglar cuando se rompe) a una proactiva (optimizar antes de que falle).
