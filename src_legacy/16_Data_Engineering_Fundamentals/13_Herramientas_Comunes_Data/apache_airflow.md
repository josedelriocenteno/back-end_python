# Apache Airflow: El orquestador estándar

Como vimos en la sección de orquestación, Airflow es la herramienta más utilizada para programar, monitorizar y gestionar las dependencias de tus pipelines.

## 1. "Configuration as Code"
En Airflow, los flujos (DAGs) no se crean haciendo clicks en una web. Se escriben en archivos de Python. Esto permite que el flujo de datos sea versionable en Git y testeable.

## 2. Operadores (Operators)
Son las piezas de construcción de Airflow:
- **PythonOperator:** Ejecuta una función de Python.
- **SQLExecuteQueryOperator:** Lanza una query en BigQuery, Snowflake o Postgres.
- **BashOperator:** Ejecuta un comando en la terminal.

## 3. Gestión de la Infraestructura
Airflow es el "Director". No debería hacer el trabajo pesado.
- **MAL:** Leer un archivo de 10GB dentro de un `PythonOperator`. Saturarás el servidor de Airflow.
- **BIEN:** Usar Airflow para decirle a Spark que procese el archivo, o decirle a BigQuery que ejecute la query. Airflow solo espera a que el otro sistema termine.

## 4. Backfilling y Catchup
Si un pipeline falla durante 3 días, Airflow puede "ponerse al día" (Catchup) automáticamente ejecutando las tareas pendientes una por una para cada día que faltó el dato.

## 5. Interfaz Visual
Airflow ofrece una web donde puedes ver tus DAGs, qué tareas han fallado, los logs de cada paso y cuánto tiempo tarda cada ejecución. Es la ventana principal del Data Engineer a la salud de sus sistemas.

## Resumen: El Control Central
Airflow es el pegamento que une todas las piezas (Python, SQL, Spark, APIs). Sin un orquestador como Airflow, la ingeniería de datos sería una colección de scripts manuales imposibles de escalar.
