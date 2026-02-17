# SQL para Machine Learning (ML)

Muchos científicos de datos saltan directamente a Python/Pandas para procesar datos, pero un Data Engineer senior sabe que gran parte del trabajo de ML (Feature Engineering y Preparación de Datasets) es más eficiente en SQL.

## 1. Feature Engineering en SQL

Las "Features" son las variables de entrada para un modelo de ML. SQL es excelente para calcularlas a escala.

### Agregaciones Históricas:
```sql
-- Feature: Gasto total del usuario en los últimos 3 meses
SELECT 
    user_id,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at RANGE BETWEEN '3 months' PRECEDING AND CURRENT ROW) as total_spent_3m
FROM orders;
```

### Codificación de Categorías (One-Hot Encoding Simple):
```sql
SELECT 
    user_id,
    MAX(CASE WHEN category = 'Electronics' THEN 1 ELSE 0 END) as bought_electronics,
    MAX(CASE WHEN category = 'Books' THEN 1 ELSE 0 END) as bought_books
FROM orders
GROUP BY user_id;
```

## 2. Creación de Datasets de Entrenamiento

Para entrenar un modelo, necesitas una "Foto fija" de los datos en un momento dado. 

```sql
CREATE TABLE training_dataset_v1 AS
SELECT 
    target_variable,
    feature_1,
    feature_2,
    ...
FROM features_table
WHERE date < '2023-01-01'; -- Evitar "Data Leakage" (ver datos del futuro)
```

## 3. Manejo de Outliers (Valores Atípicos)

Puedes usar Window Functions para identificar valores que se alejan demasiado de la media y filtrarlos antes de entrenar tu modelo.

```sql
WITH stats AS (
    SELECT 
        amount,
        AVG(amount) OVER () as avg_amount,
        STDDEV(amount) OVER () as stddev_amount
    FROM raw_data
)
SELECT * FROM stats
WHERE amount < (avg_amount + 3 * stddev_amount); -- Filtra el 99.7% de la distribución
```

## 4. Muestreo de Datos (Sampling)

Si tienes miles de millones de filas, no puedes entrenar con todas. Necesitas una muestra aleatoria.

```sql
-- Muestra aleatoria del 10% de los datos
SELECT * FROM massive_table
WHERE RANDOM() < 0.1;

-- Muestreo Estratificado (manteniendo proporciones de clase)
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY RANDOM()) as rn
    FROM massive_table
) t WHERE rn <= 1000;
```

## 5. Inferencia en la Base de Datos

Algunas bases de datos modernas (y extensiones de Postgres) permiten cargar modelos de ML y hacer predicciones directamente en SQL sin sacar los datos a Python.

*   *Ejemplo:* `SELECT predict_churn(user_id) FROM users;`

## Resumen: SQL es la Base de tu Modelo

Cuanto más Feature Engineering hagas en SQL, menos memoria consumirá tu script de entrenamiento de Python y más rápido será el ciclo de experimentación. SQL no es solo para guardar datos, es el motor de pre-procesamiento de tu IA.
