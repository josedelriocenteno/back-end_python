# Esquemas Estrella y Copo de Nieve

Son los estándares de modelado en los Data Warehouses (OLAP). Organizan los datos de forma que las consultas analíticas sean lo más rápidas posible.

## 1. El Esquema Estrella (Star Schema)
Es el modelo preferido por su simplicidad y rendimiento. Se compone de:
*   **Tabla de Hechos (Fact Table):** La tabla central gigante que contiene los eventos numéricos (ej: `ventas`). Tiene muchas filas y pocas columnas (ID de producto, ID de fecha, cantidad, precio).
*   **Tablas de Dimensiones (Dimensions):** Tablas pequeñas alrededor de la de hechos que contienen los atributos (ej: `clientes`, `productos`, `tiendas`).
*   **Relación:** Se unen mediante una sola conexión (`JOIN`). Dibujado, parece una estrella.

## 2. El Esquema Copo de Nieve (Snowflake Schema)
Es una variación donde las dimensiones están normalizadas.
*   **Ejemplo:** La dimensión `producto` no tiene la categoría escrita, sino un `id_categoria` que apunta a otra tabla.
*   **Diferencia:** Es más ordenado pero requiere más `JOINS`, lo que puede penalizar el rendimiento en consultas masivas.

## 3. ¿Por qué Estrella es mejor para Performance?
*   **Menos saltos:** Casi cualquier pregunta se responde con un solo Join entre la tabla de Hechos y las Dimensiones necesarias.
*   **Simplicidad para BI:** Herramientas como Tableau o PowerBI entienden este modelo nativamente y generan queries muy eficientes.

## 4. Tablas de Hechos y Granularidad
Un error común es mezclar niveles de detalle.
*   **Granularidad Fina:** Un registro por cada ticket de compra.
*   **Granularidad Gruesa:** Un registro por el total de ventas diario de una tienda.
El diseño estrella debe tener una granularidad clara y consistente en su tabla de hechos central.

## 5. SCD (Slowly Changing Dimensions)
¿Qué pasa si un cliente cambia de ciudad?
*   **Tipo 1:** Sobre-escribes el valor (pierdes el histórico).
*   **Tipo 2:** Creas una fila nueva con una fecha de vigencia (mantienes el histórico de dónde vivía cuando compró cada producto). Es vital para la precisión del análisis.

## Resumen: Orden para el Análisis
El esquema estrella es el lenguaje universal de la ingeniería de datos analítica. Su diseño desnormalizado minimiza el esfuerzo computacional de los agregados pesados, permitiendo que millones de datos se transformen en información útil en segundos.
