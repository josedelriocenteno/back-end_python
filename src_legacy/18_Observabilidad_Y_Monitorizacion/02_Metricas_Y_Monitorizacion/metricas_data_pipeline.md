# Métricas de Data Pipelines: Midiendo el flujo de datos

Para un Data Engineer, las métricas de sistema (CPU/Mem) no son suficientes. Necesitamos saber si el **dato** fluye correctamente y con calidad.

## 1. Volumen de Datos (Throughput)
*   **Records Processed:** ¿Cuántas filas hemos ingerido en total? 
*   **Bytes Processed:** Útil para controlar costes en BigQuery o Dataflow.
*   **Métrica Senior:** "Filas por segundo". Ayuda a detectar si una transformación es más lenta de lo esperado.

## 2. Frescura del Dato (Data Freshness / Lag)
Es la métrica más importante de un pipeline.
*   **Wall Time Lag:** ¿Cuánto tiempo ha pasado desde que el dato ocurrió en el mundo real hasta que llegó a nuestra tabla final?
*   **Pipeline Duration:** ¿Cuánto tarda el proceso de Airflow en completarse? Si antes tardaba 20 min y ahora tarda 2 horas, vas a fallar tu SLA (Service Level Agreement).

## 3. Calidad y Rechazo (Error Rate)
*   **Rejected Records:** ¿Cuántas filas han fallado la validación de esquema o de negocio?
*   **Null Ratio:** % de nulos en columnas críticas. Un aumento repentino indica que algo se ha roto en el origen.

## 4. Salud de la Infraestructura de Datos
*   **Task Success Rate:** En Airflow, ¿qué porcentaje de tareas terminan en Success vs Fail?
*   **Retries Count:** ¿Cuántas veces tiene que reintentarse una tarea antes de funcionar? Muchos reintentos indican inestabilidad en la red o en la base de datos de origen.

## 5. Costes del Pipeline
*   **Cost per Run:** ¿Cuánto dinero ha gastado esta ejecución concreta del pipeline?
*   **Slot Consumption (BigQuery):** ¿Cuánta potencia de CPU estamos consumiendo del clúster compartido?

## Ejemplo de Dashboard para Data
*   Gráfico 1: "Filas ingeridas hoy vs ayer".
*   Gráfico 2: "Tiempo de ejecución de los últimos 7 días".
*   Gráfico 3: "Top 5 tablas con más filas rechazadas".

## Resumen: Operando con Datos
Las métricas de pipelines te dan la seguridad de que el negocio está viendo datos actualizados y fiables. Un aumento en el Lag o en la tasa de registros rechazados es a menudo la primera señal de un problema mayor que está por venir.
