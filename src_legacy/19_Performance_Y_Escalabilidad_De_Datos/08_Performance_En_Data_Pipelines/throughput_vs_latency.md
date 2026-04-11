# Throughput vs. Latencia en Pipelines de Datos

En ingeniería de datos, optimizar para uno a menudo perjudica al otro. Entender esta eterna pelea es la base para diseñar el pipeline adecuado.

## 1. Latencia (Tiempo de respuesta)
Es el tiempo que tarda un **único dato** en viajar desde el origen hasta el destino.
*   **Métrica:** "Este mensaje de Kafka tarda 50ms en procesarse y guardarse".
*   **Objetivo:** Respuesta inmediata. Crítico en Streaming y APIs.

## 2. Throughput (Caudal / Volumen)
Es la cantidad de datos que el sistema puede procesar en un **periodo de tiempo** determinado.
*   **Métrica:** "Este pipeline procesa 10 millones de filas por hora".
*   **Objetivo:** Maximizar el volumen total procesado. Crítico en procesos Batch y Data Warehousing.

## 3. ¿Por qué están enfrentados?
*   Para ganar **Throughput**, solemos usar **Batching** (agrupar datos). Agrupar 10.000 filas y procesarlas de una vez es mucho más eficiente para la CPU y la base de datos que procesar 10.000 filas una a una.
*   Sin embargo, agrupar datos aumenta la **Latencia**, porque la primera fila del grupo tiene que esperar a que llegue la última para ser procesada.

## 4. El punto dulce: Micro-batching
Sistemas como Spark Streaming intentan equilibrar ambos mundos procesando lotes cada pocos segundos.
*   Consigues un **Throughput** muy alto (eficiencia de lote).
*   Mantienes una **Latencia** aceptable (segundos, no horas).

## 5. Cuándo priorizar qué
*   **Latencia prioritaria:** Detección de fraude, sistemas de alerta, recomendaciones en vivo en una web.
*   **Throughput prioritario:** Carga diaria de un Data Warehouse, entrenamiento de modelos de Machine Learning, reportes históricos financieros.

## Resumen: La balanza del Ingeniero
No intentes ser el más rápido en latencia y el más masivo en throughput al mismo tiempo sin justificación; será carísimo y complejo. Analiza la necesidad del negocio y ajusta tu arquitectura para ser eficiente en la métrica que realmente importa para ese proceso.
