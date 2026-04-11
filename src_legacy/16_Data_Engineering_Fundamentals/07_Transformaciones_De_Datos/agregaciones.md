# Agregaciones: Resumiendo la realidad

Las agregaciones son transformaciones matemáticas que agrupan miles de registros en unos pocos valores clave (KPIs).

## 1. Funciones Comunes
- **SUM:** Ventas totales.
- **AVG:** Ticket medio.
- **COUNT:** Número de usuarios únicos (`COUNT DISTINCT`).
- **MIN/MAX:** Rango de precios.

## 2. Granularidad del Dato
Elegir la granularidad correcta es vital:
- **Low Granularity:** Un registro por cada venta individual. (Mucho detalle, archivos grandes).
- **High Granularity:** Un registro por total de ventas por tienda y por día. (Poco detalle, muy rápido de consultar).

## 3. El peligro de las Medias de Medias
Nunca hagas el promedio de una columna que ya es un promedio.
- **Error:** Promedio de (Promedio Tienda A + Promedio Tienda B).
- **Solución:** Suma total de ventas / Suma total de pedidos de ambas tiendas.

## 4. Agregaciones en Batch vs Streaming
- **Batch:** Fácil. Tienes todos los datos del día, haces un `GROUP BY` y listo.
- **Streaming:** Difícil. Como los datos nunca terminan de llegar, las agregaciones se hacen sobre **ventanas de tiempo** (ver sección 04).

## 5. Pre-agregación (Cubos OLAP)
Para que los dashboards carguen instantáneamente, el Data Engineer calcula las agregaciones por la noche y las guarda en tablas maestras. El dashboard no consulta el dato crudo, consulta la tabla agregada.

## Resumen: El lenguaje del Negocio
Al negocio no le importa cada click individual; le importa el porcentaje de conversión. Las agregaciones son la herramienta para traducir trillones de eventos técnicos en el lenguaje del dinero y la estrategia.
