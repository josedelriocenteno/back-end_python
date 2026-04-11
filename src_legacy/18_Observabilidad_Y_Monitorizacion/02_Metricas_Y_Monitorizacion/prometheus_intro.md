# Prometheus: El estándar de las métricas

Mostramos cómo recoger métricas, pero ¿dónde se guardan y cómo se consultan? **Prometheus** es la herramienta líder del mercado (Open Source) para la recolección y consulta de métricas.

## 1. ¿Cómo funciona? El modelo PULL
A diferencia de otros sistemas donde la app "envía" datos, Prometheus es quien "tira" del dato.
*   Tu App abre un puerto (ej: `:8000/metrics`) con una lista de textos.
*   Prometheus visita esa URL cada X segundos (Scraping) y guarda lo que lee en su base de datos de series temporales (TSDB).

## 2. Tipos de Datos en Prometheus
Usa los tres que vimos antes: **Counters** (incrementales), **Gauges** (sube/baja) e **Histograms** (cubos de distribución).

## 3. PromQL: El lenguaje de consulta
Igual que usas SQL para tablas, usas **PromQL** para métricas. Es muy potente para calcular porcentajes y tasas de cambio.
*   **Tasa de errores en los últimos 5 min:** `rate(http_errors_total[5m])`
*   **Uso de memoria medio por servidor:** `avg(node_memory_usage_bytes) by (instance)`

## 4. Etiquetas (Labels) y Filtros
Prometheus basa todo su poder informativo en las etiquetas.
*   `peticiones{service="ventas", status="200"}`
Puedes sumar todas las peticiones de "ventas" ignorando el status, o ver el status "200" de todos los servicios.

## 5. Exporters: Monitorizando lo que no es tuyo
¿Cómo monitorizas una base de datos Postgres o un clúster de Spark que tú no has programado? Usando un **Exporter**. Es un pequeño programa que lee los internos de Postgres y los "traduce" al lenguaje que Prometheus entiende.

## Resumen: La Piedra Angular
Aprender los fundamentos de Prometheus y PromQL es esencial. Es la herramienta que te permitirá transformar miles de números sueltos en información útil para saber si tu sistema está operando correctamente o si necesita intervención.
