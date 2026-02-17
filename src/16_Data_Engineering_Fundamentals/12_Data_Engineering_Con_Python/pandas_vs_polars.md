# Pandas vs. Polars: El cambio de guardia

Durante una década, **Pandas** fue la única opción. Ahora, **Polars** ha llegado para reclamar el trono con un enfoque centrado en la velocidad y el Big Data.

## 1. Pandas: La vieja confiable
- **Pros:** Ecosistema gigantesco, documentación infinita, funciona en cualquier sitio.
- **Contras:** Ejecución en un solo núcleo (Single-threaded). Consume el doble o triple de RAM de lo que pesa el dato. Muy lento con datasets de más de 5GB.

## 2. Polars: La nueva potencia (Escrito en Rust)
- **Pros:** Procesamiento paralelo (usa todos tus núcleos de CPU). Multihilo por defecto. "Lazy Evaluation" (optimiza la query antes de ejecutarla).
- **Contras:** Sintaxis un poco diferente, ecosistema aún en crecimiento.

## 3. Lazy Evaluation: El superpoder de Polars
En Pandas, si haces esto:
1. Lee todo el CSV de 10GB.
2. Filtra por `pais == 'ES'`.
Pandas lee los 10GB enteros.

En **Polars (Lazy)**:
1. "Tengo que leer el CSV y filtrar por ES".
2. Polars mira dentro del archivo y **solo lee** las filas de España. Es infinitamente más rápido.

## 4. ¿Cuándo usar cada uno?
- **Pandas:** Para scripts rápidos, análisis exploratorios de datos pequeños o integración con librerías de ML antiguas.
- **Polars:** Para pipelines de producción que manejan millones de filas y donde el tiempo de ejecución importa.

## 5. Comparativa de Código
```python
# Polars (Sintaxis fluida)
import polars as pl
df = (
    pl.read_parquet("datos.parquet")
    .filter(pl.col("ventas") > 100)
    .group_by("tienda")
    .agg(pl.sum("ventas"))
)
```

## Resumen: Aprende ambos
Pandas no va a desaparecer, pero Polars es el futuro de la ingeniería de datos en Python. Un ingeniero versátil domina ambos para elegir la herramienta adecuada según el volumen de datos.
