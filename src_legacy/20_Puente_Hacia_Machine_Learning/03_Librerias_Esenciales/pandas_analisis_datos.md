# Pandas: Excel con esteroides para ingenieros

**Pandas** es la librería líder para la manipulación y análisis de datos tabulares (hojas de cálculo, tablas SQL). Es la herramienta donde pasarás la mayor parte de tu tiempo preparando datos para ML.

## 1. Estructuras de Datos
*   **Series:** Un array unidimensional (como una columna).
*   **DataFrame:** Una tabla bidimensional (como una hoja de Excel o tabla SQL).

## 2. Operaciones de Limpieza con Pandas
Pandas hace que limpiar datos sea extremadamente sencillo:
```python
import pandas as pd

df = pd.read_csv("datos.csv")

# 1. Ver las primeras filas
print(df.head())

# 2. Manejar nulos
df['edad'] = df['edad'].fillna(df['edad'].mean())

# 3. Filtrar datos
jovenes = df[df['edad'] < 30]

# 4. Agrupar (como SQL)
resumen = df.groupby('ciudad')['ventas'].sum()
```

## 3. Integración Directa
Pandas puede leer y escribir en casi cualquier formato:
*   `read_sql()`, `to_sql()`: Conexión directa con bases de datos.
*   `read_parquet()`, `to_parquet()`: Formato columnar optimizado.
*   `read_json()`, `read_excel()`.

## 4. Análisis de Datos (EDA) rápido
*   `df.describe()`: Nos da la media, desviación, min, max de todas las columnas numéricas de un golpe.
*   `df.info()`: Nos dice cuántos nulos hay y el tipo de cada columna.

## 5. El "Pandas Way" (Vectorización)
Al igual que NumPy, evita los bucles `for` sobre las filas. 
*   **Mal:** `for row in df: row['precio'] *= 1.2`
*   **Bien:** `df['precio'] *= 1.2` (Es 100 veces más rápido).

## Resumen: La navaja suiza del dato
Pandas es el puente entre los datos brutos y la inteligencia. Su capacidad para filtrar, agrupar y transformar información masiva de forma legible y eficiente la convierte en una habilidad obligatoria para cualquier profesional que trabaje con Python y datos.
