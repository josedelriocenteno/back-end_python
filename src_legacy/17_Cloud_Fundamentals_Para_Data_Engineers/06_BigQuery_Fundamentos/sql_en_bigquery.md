# SQL en BigQuery: Big Data en una línea

BigQuery usa **GoogleSQL** (antes Standard SQL), un dialecto muy potente y compatible con el estándar ANSI. Pero tiene superpoderes diseñados para analítica masiva.

## 1. Common Table Expressions (CTEs)
Usa siempre `WITH` en lugar de subqueries anidadas. Hace el código mucho más legible para el resto del equipo.
```sql
WITH ventas_2024 AS (
  SELECT * FROM `proyecto.ds.ventas` WHERE date >= '2024-01-01'
)
SELECT tienda, SUM(total) FROM ventas_2024 GROUP BY 1
```

## 2. Window Functions (Funciones de Ventana)
Fundamentales para analítica temporal. Permiten comparar una fila con la anterior o calcular totales acumulados.
- `RANK()` / `ROW_NUMBER()`: Para encontrar el pedido más reciente de cada usuario.
- `LAG()` / `LEAD()`: Para comparar ventas de hoy con ventas de ayer.

## 3. Manejo de Arrays y Structs
BigQuery permite que una celda contenga una lista (`ARRAY`) u otro objeto denidado (`STRUCT`).
- Esto evita hacer `JOINs` innecesarios, haciendo las queries mucho más rápidas. Use `UNNEST` para "aplanar" estos datos cuando necesites analizarlos fila a fila.

## 4. Funciones de Usuario (UDF)
Si el SQL estándar no es suficiente, puedes escribir lógica compleja en **JavaScript** o SQL y guardarla como una función que puedes llamar desde cualquier query.

## 5. Scripting y Procedimientos Almacenados
BigQuery permite escribir scripts con variables, bucles y lógica condicional (`IF / ELSE`), lo que permite crear procesos ETL complejos totalmente dentro de la base de datos.

## Resumen: SQL es el lenguaje de datos
Dominar el SQL avanzado de BigQuery te permite mover la lógica de transformación del código (Python) a la base de datos (ELT), aprovechando la potencia de miles de máquinas de Google para procesar el dato donde reside.
