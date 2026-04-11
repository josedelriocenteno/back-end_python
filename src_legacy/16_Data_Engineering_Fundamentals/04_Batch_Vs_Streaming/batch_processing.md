# Batch Processing: El poder del volumen

Como vimos en la arquitectura de pipelines, el procesamiento por lotes (Batch) sigue siendo la forma más común de mover datos en las empresas. Vamos a profundizar en sus estrategias profesionales.

## 1. Ventanas de Tiempo (Batch Windows)
Un proceso batch no tiene por qué ser diario. Puede ser:
- **Micro-batch:** Cada 5-15 minutos. Intenta imitar el tiempo real sin la complejidad de Kafka.
- **Hourly/Daily:** El estándar para agregaciones de negocio.

## 2. Tipos de Carga Batch
- **Carga Incrementales (Delta):** Solo traes lo que ha cambiado desde el último éxito. Requiere una columna `updated_at` en el origen.
- **Carga de Captura de Cambios (CDC):** Leemos los logs de la base de datos origen para saber qué filas se han insertado o borrado. Es mucho más eficiente que consultar la tabla.

## 3. Retos Técnicos: El fallo en la partición
Si procesas datos por día, y el día 10 de Marzo falla, el sistema debe ser capaz de re-ejecutar solo ese día sin tocar el resto (idempotencia en acción).

## 4. Cuándo NO usar Batch
- Si el negocio necesita reaccionar en menos de 5 minutos.
- Si el volumen de datos por hora es tan grande que el proceso tarda más de una hora en terminar (el pipeline se "solapa" con el siguiente).

## Resumen: Fiabilidad Masiva
El Batch es excelente para situaciones donde la **veracidad del dato** es más importante que la **velocidad**. Es más fácil de auditar, más barato de procesar y la base de cualquier Data Warehouse profesional.
