# Acceso a BigQuery desde Python

Interactuar con BigQuery desde Python es la tarea diaria de un Data Engineer. Puedes lanzar queries, cargar datos y gestionar tablas de forma programática.

## 1. Lanzar una Query
```python
from google.cloud import bigquery

client = bigquery.Client()
query = """
    SELECT tienda, SUM(ventas) as total 
    FROM `mi-proyecto.dataset.tabla` 
    GROUP BY 1 LIMIT 10
"""
query_job = client.query(query)  # Lanza la query de forma asíncrona
results = query_job.result()     # Espera a que termine

for row in results:
    print(f"{row.tienda}: {row.total}")
```

## 2. Integración con Pandas
BigQuery se lleva de maravilla con Pandas. Puedes bajar el resultado de una query directamente a un DataFrame.
```python
df = query_job.to_dataframe()
```
*Nota: Requiere instalar `pandas` y `db-dtypes`.*

## 3. Carga de Datos (Load Job)
Puedes cargar un archivo local rápidamente:
```python
job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.CSV)
with open("datos_locales.csv", "rb") as source_file:
    job = client.load_table_from_file(source_file, "dataset.tabla", job_config=job_config)
job.result() # Espera a que la carga termine
```

## 4. Parameterized Queries (Seguridad)
Nunca uses F-strings para meter variables en una query SQL (peligro de SQL Injection). Usa parámetros:
```python
query = "SELECT * FROM tabla WHERE pais = @pais_id"
job_config = bigquery.QueryJobConfig(
    query_parameters=[bigquery.ScalarQueryParameter("pais_id", "STRING", "ES")]
)
client.query(query, job_config=job_config)
```

## 5. El objeto `Job`
Cuando lanzas algo en BigQuery, recibes un `Job`. No es el dato en sí, es el identificador del proceso. Puedes consultar su estado, ver cuánto ha costado y si ha tenido errores sin tener que esperar a que el dato cargue.

## Resumen: Poder Analítico en Código
La librería de BigQuery para Python te da todo el control del Data Warehouse. Te permite automatizar tareas repetitivas, crear reportes dinámicos y construir tuberías de datos inteligentes que reaccionan a los resultados de las consultas.
