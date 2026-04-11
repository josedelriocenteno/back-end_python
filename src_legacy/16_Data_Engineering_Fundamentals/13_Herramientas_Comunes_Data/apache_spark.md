# Apache Spark: El gigante del procesamiento distribuido

Spark es el motor de procesamiento de datos más potente y utilizado en el mundo del Big Data. Su gran ventaja es que puede procesar Petabytes de información repartiendo el trabajo entre cientos de servidores.

## 1. El concepto de Computación Distribuida
Si una query tarda 10 horas en un servidor, Spark la divide en 10 trozos y la ejecuta en 10 servidores a la vez. En teoría, tardaría solo 1 hora.

## 2. RDDs y DataFrames
- **RDD (Resilient Distributed Dataset):** La unidad básica de datos en Spark. Difícil de usar pero muy potente.
- **DataFrame (Estandar):** Una tabla distribuida con columnas, muy similar a un DataFrame de Pandas pero que vive en muchos servidores a la vez. Es lo que usarás el 99% del tiempo.

## 3. PySpark: Python + Spark
PySpark es el puente que nos permite usar toda la potencia de Spark escribiendo código Python. Es el lenguaje preferido por los ingenieros de datos para procesos ETL/ELT pesados.

## 4. Lazy Evaluation en Spark
Igual que Polars, Spark no hace nada hasta que le pides el resultado final (`Action`). Hasta entonces, solo construye un plan lógico de ejecución (`DAG`) para optimizar el acceso al disco y la memoria.

## 5. Cuándo usar Spark
- Si tus datos no caben en la RAM de un solo servidor potente (más de 100GB-200GB).
- Si necesitas procesar datos de forma masiva en la nube (AWS EMR, Databricks, Google Dataproc).

## Resumen: Escalabilidad Infinita
Spark es la herramienta que te permite decir "sí" a cualquier volumen de datos. Dominar PySpark es pasar de ser un programador de scripts a ser un Ingeniero de Big Data capaz de manejar infraestructuras masivas.
