# Batch Prediction Pipelines: Inferencia Masiva

No todos los modelos necesitan responder al instante. En muchos casos empresariales, es mucho más eficiente procesar millones de predicciones de una sola vez durante la noche.

## 1. ¿Qué es el Batch Prediction?
Es un proceso donde tomamos un conjunto gigante de datos (ej: toda nuestra base de datos de usuarios), aplicamos el modelo a cada fila y guardamos los resultados de vuelta en la base de datos.
*   **Uso:** "Generar cada noche la lista de recomendaciones personalizadas para que el usuario las vea al entrar por la mañana".

## 2. Arquitectura de un Pipeline Batch
Suele seguir un flujo ETL clásico:
1.  **Extract:** Leemos los datos desde el Data Warehouse (BigQuery, Redshift) o Data Lake (S3).
2.  **Transform:** Aplicamos la limpieza y el feature engineering.
3.  **Predict:** Cargamos el modelo y realizamos las predicciones en masa.
4.  **Load:** Insertamos las predicciones en una tabla de resultados.

## 3. Escalado Horizontal con Spark/Ray
Para procesar TBs de datos, un solo servidor no es suficiente.
*   Usamos **Apache Spark** o **Ray** para repartir el modelo y los datos entre 100 servidores. Cada servidor procesa un trozo y al final se unen los resultados.

## 4. Orquestación (Airflow)
Los procesos batch de ML deben estar orquestados.
*   **Dependencia:** El proceso de Batch Prediction solo debe empezar cuando el proceso de Ingesta de Datos del día haya terminado con éxito.
*   **Reintentos:** Si la predicción falla por un problema de red, el orquestador lo reintenta automáticamente.

## 5. El "Offline Store"
Los resultados del batch se suelen guardar en el **Offline Store** del Feature Store, para que puedan ser usados después para analizar cómo de bien está funcionando el modelo a largo plazo.

## Resumen: Eficiencia y Volumen
La predicción batch es la forma más económica y escalable de aplicar Machine Learning a gran escala. Al no tener el requisito de la respuesta inmediata (latencia), podemos aprovechar al máximo la capacidad de cálculo y procesar volúmenes de datos que serían imposibles de manejar con una API tradicional.
