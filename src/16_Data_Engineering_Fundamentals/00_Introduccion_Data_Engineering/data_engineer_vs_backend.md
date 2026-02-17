# Data Engineer vs. Backend Developer

Si eres desarrollador de Backend, ya tienes el 60% del camino hecho. Sin embargo, hay cambios de mentalidad cruciales cuando pasas al mundo del dato.

## 1. Diferencia de Objetivo
- **Backend:** Se centra en la **latencia por petición**. Quieres que un usuario reciba su respuesta en milisegundos.
- **Data Engineer:** Se centra en el **throughput (caudal)**. Quieres procesar millones de registros de forma eficiente, aunque la tarea tarde 10 minutos en completarse.

## 2. Estado vs. Flujo
- **Backend:** Gestionas el "estado actual" de un objeto (ej: cambiar el password de un usuario en un registro de la DB).
- **Data Engineer:** Gestionas el historial de cambios (ej: analizar cómo han cambiado los passwords de todos los usuarios en los últimos 2 años).

## 3. Herramientas y Bases de Datos
- **Backend:** Bases de datos **OLTP** (PostgreSQL, MySQL). Optimizadas para escritura rápida y lectura de registros individuales.
- **Data Engineer:** Bases de datos **OLAP** (BigQuery, Snowflake, Redshift). Optimizadas para agrupar y sumar millones de filas a la vez.

## 4. El concepto de "Falla-Seguro"
- **Backend:** Si falla un endpoint, el usuario ve un error.
- **Data Engineer:** Si falla un pipeline a las 3 AM con 10TB de datos, necesitas mecanismos de reintento, idempotencia y auditoría para que el sistema se recupere solo sin duplicar datos.

## 5. El solapamiento
Ambos necesitan:
- Dominio de Python y SQL.
- Conocimiento de Docker y Cloud.
- Prácticas de código limpio (Clean Code) y Testing.

## Resumen: De Micro a Macro
Pasar de Backend a Data Engineering es dejar de mirar el "objeto individual" para empezar a mirar la "población de datos" completa, optimizando el sistema para el procesamiento masivo y la integridad histórica.
