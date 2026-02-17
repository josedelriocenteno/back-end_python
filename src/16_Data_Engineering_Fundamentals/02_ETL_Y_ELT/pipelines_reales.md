# Pipelines Reales: Casos de uso prácticos

Para entender la teoría, veamos cómo se aplican estos patrones en el día a día de una empresa tecnológica.

## 1. Caso: E-commerce (Ingesta de Pedidos)
- **Extract:** Un script Python consulta la API de Shopify cada 15 minutos.
- **Transform:** Convierte la moneda de USD a EUR usando el tipo de cambio del día. Elimina datos personales (GDPR).
- **Load:** Se inserta en una tabla de BigQuery llamada `raw_orders` de forma incremental.
- **Patrón:** ETL (porque limpias datos personales antes de que toquen el Warehouse).

## 2. Caso: Análisis de Logs de Servidor
- **Extract:** Los servidores escriben miles de líneas por segundo en archivos `.log`.
- **Load:** Un proceso mueve esos archivos "crudos" a un cubo de AWS S3.
- **Transform:** Una query de SQL en el Data Warehouse parsea el texto del log para contar cuántos errores 500 hubo.
- **Patrón:** ELT (el Warehouse tiene potencia de sobra para parsear texto).

## 3. Caso: Marketing (Atribución de Ventas)
- **Extract:** Datos de Facebook Ads, Google Ads y base de datos propia.
- **Transform:** Cruce complejo de miles de registros para saber qué anuncio causó qué venta. Requiere uniones (Joins) masivas.
- **Load:** Tabla final `marketing_performance`.
- **Patrón:** ELT con dbt (el cruce de datos es mucho más eficiente en SQL que en memoria de Python).

## 4. La importancia del DAG
En todos estos casos, las tareas se organizan en un **DAG** (Directed Acyclic Graph). Es el mapa que dice: "Primero extrae de las 3 fuentes, luego mézclalas, y finalmente genera el reporte".

## 5. Tip Senior: Empieza por el final
A la hora de diseñar un pipeline, pregunta primero: "¿Qué pregunta quiere responder el negocio?". A partir de ahí, trabaja hacia atrás para saber qué datos necesitas extraer y cómo transformarlos.

## Resumen: Soluciones a medida
No hay un patrón único. Los mejores Data Engineers eligen ETL o ELT basándose en la seguridad de los datos, la tecnología disponible y la complejidad de las uniones requeridas.
