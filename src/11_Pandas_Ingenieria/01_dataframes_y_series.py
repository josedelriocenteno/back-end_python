# ===========================================================================
# 01_dataframes_y_series.py
# ===========================================================================
# MODULO 11: PANDAS INGENIERIA
# ARCHIVO 01: DataFrames, Series y Operaciones Fundamentales
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar la estructura interna de Pandas, indexing, dtypes,
# missing values, y todas las operaciones core.
#
# CONTENIDO:
#   1. Series y DataFrame: internals.
#   2. Indexing: loc, iloc, at, iat.
#   3. Dtypes de Pandas: Categorical, nullable, string.
#   4. Missing values: NaN, None, pd.NA.
#   5. Operaciones basicas: sort, filter, assign.
#   6. String operations.
#   7. Datetime operations.
#   8. Memory optimization.
#   9. MultiIndex.
#   10. Pipes y method chaining.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import pandas as pd
import numpy as np
import sys


# =====================================================================
#   PARTE 1: SERIES
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: SERIES ===")
print("=" * 80)

"""
Series: array 1D con index. Internamente es un ndarray + un Index.
Es la columna fundamental de un DataFrame.
"""

print("\n--- Crear Series ---")

# Desde lista
s1 = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'], name='valores')
print(f"  Series:\n{s1}\n")
print(f"  dtype: {s1.dtype}")
print(f"  index: {s1.index.tolist()}")
print(f"  values (numpy): {s1.values}")
print(f"  name: {s1.name}")

# Desde dict
s2 = pd.Series({'x': 100, 'y': 200, 'z': 300})
print(f"\n  Desde dict:\n{s2}")

# Desde scalar
s3 = pd.Series(42, index=range(5))
print(f"\n  Scalar broadcast:\n{s3}")


print("\n--- Operaciones vectorizadas ---")

s = pd.Series([1, 2, 3, 4, 5])
print(f"  s * 2:     {(s * 2).tolist()}")
print(f"  s ** 2:    {(s ** 2).tolist()}")
print(f"  s > 3:     {(s > 3).tolist()}")
print(f"  s.sum():   {s.sum()}")
print(f"  s.mean():  {s.mean()}")
print(f"  s.std():   {s.std():.4f}")
print(f"  s.cumsum():{s.cumsum().tolist()}")


print("\n--- Alignment por index ---")

s_a = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s_b = pd.Series([10, 20, 30], index=['b', 'c', 'd'])

result = s_a + s_b
print(f"  s_a + s_b (auto-aligned):\n{result}")
print(f"  (NaN donde no hay match)")


# =====================================================================
#   PARTE 2: DATAFRAME
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: DATAFRAME ===")
print("=" * 80)

"""
DataFrame: tabla 2D con index de filas y columnas.
Internamente: dict de Series (columnas) con index compartido.
"""

print("\n--- Crear DataFrame ---")

df = pd.DataFrame({
    'nombre': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'edad': [30, 25, 35, 28, 32],
    'salario': [70000, 55000, 90000, 65000, 80000],
    'departamento': ['Engineering', 'Marketing', 'Engineering', 'Sales', 'Engineering'],
})

print(df)
print(f"\n  shape: {df.shape}")
print(f"  dtypes:\n{df.dtypes}")
print(f"  columns: {df.columns.tolist()}")
print(f"  index: {df.index.tolist()}")
print(f"  memory: {df.memory_usage(deep=True).sum():,} bytes")


print("\n--- Info y describe ---")

print(df.describe())
print(f"\n  Non-null counts:\n{df.count()}")


# =====================================================================
#   PARTE 3: INDEXING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: INDEXING ===")
print("=" * 80)

"""
4 formas de indexar:
- df['col']: seleccionar columna (retorna Series).
- df.loc[row, col]: label-based.
- df.iloc[row, col]: position-based.
- df.at[row, col]: scalar label-based (rapido).
- df.iat[row, col]: scalar position-based (rapido).

REGLA: siempre usar loc/iloc explicitamente. Evitar chained indexing.
"""

print("\n--- loc (label-based) ---")

print(f"  loc[0, 'nombre']: {df.loc[0, 'nombre']}")
print(f"  loc[0:2, ['nombre','edad']]:\n{df.loc[0:2, ['nombre','edad']]}")
print(f"  loc con mask:\n{df.loc[df['edad'] > 30, ['nombre','salario']]}")


print("\n--- iloc (position-based) ---")

print(f"  iloc[0, 0]: {df.iloc[0, 0]}")
print(f"  iloc[0:3, 1:3]:\n{df.iloc[0:3, 1:3]}")
print(f"  iloc[-1]: {df.iloc[-1].tolist()}")


print("\n--- at/iat (scalar, rapido) ---")

print(f"  at[0, 'nombre']: {df.at[0, 'nombre']}")
print(f"  iat[0, 0]: {df.iat[0, 0]}")


print("\n--- PELIGRO: chained indexing ---")

"""
NUNCA hacer: df['col'][0] = valor  (puede no modificar el original)
SIEMPRE: df.loc[0, 'col'] = valor
"""

df_copy = df.copy()
df_copy.loc[0, 'edad'] = 99
print(f"  Modificado con loc: edad[0] = {df_copy.at[0, 'edad']}")


# =====================================================================
#   PARTE 4: DTYPES DE PANDAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: DTYPES DE PANDAS ===")
print("=" * 80)

"""
Pandas tiene sus propios dtypes ademas de NumPy:
- 'category': variables categoricas (menos memoria).
- 'string' (pd.StringDtype): strings nullable.
- 'Int64' (nullable integer): soporta NA en integers.
- 'boolean' (nullable boolean).
- 'datetime64[ns]': timestamps.
"""

print("\n--- Categorical ---")

df_cat = df.copy()
df_cat['departamento'] = df_cat['departamento'].astype('category')

mem_before = df['departamento'].memory_usage(deep=True)
mem_after = df_cat['departamento'].memory_usage(deep=True)

print(f"  Object memory:     {mem_before:,} bytes")
print(f"  Category memory:   {mem_after:,} bytes")
print(f"  Savings: {(1 - mem_after/mem_before):.1%}")
print(f"  Categories: {df_cat['departamento'].cat.categories.tolist()}")
print(f"  Codes: {df_cat['departamento'].cat.codes.tolist()}")


print("\n--- Nullable integers ---")

s_nullable = pd.array([1, 2, None, 4, 5], dtype=pd.Int64Dtype())
print(f"  Nullable int: {s_nullable}")
print(f"  dtype: {s_nullable.dtype}")
print(f"  Sum (ignores NA): {s_nullable.sum()}")


print("\n--- String dtype ---")

s_str = pd.Series(['hello', 'world', None], dtype=pd.StringDtype())
print(f"  String Series: {s_str.tolist()}")
print(f"  dtype: {s_str.dtype}")
print(f"  upper: {s_str.str.upper().tolist()}")


# =====================================================================
#   PARTE 5: MISSING VALUES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: MISSING VALUES ===")
print("=" * 80)

"""
NaN (float), None (object), pd.NA (nullable).
NaN != NaN (por IEEE 754).

Estrategias:
1. dropna(): eliminar filas/columnas.
2. fillna(): rellenar con valor.
3. interpolate(): interpolar.
4. isna()/notna(): detectar.
"""

print("\n--- Detectar missing ---")

df_miss = pd.DataFrame({
    'A': [1, np.nan, 3, np.nan, 5],
    'B': [10, 20, np.nan, 40, 50],
    'C': ['x', None, 'z', 'w', None],
})

print(f"  DataFrame:\n{df_miss}")
print(f"\n  isna():\n{df_miss.isna()}")
print(f"\n  isna().sum():\n{df_miss.isna().sum()}")
print(f"\n  Total missing: {df_miss.isna().sum().sum()}")


print("\n--- Estrategias de imputacion ---")

# fillna con valor
print(f"  fillna(0):\n{df_miss['A'].fillna(0).tolist()}")

# fillna con media
mean_a = df_miss['A'].mean()
print(f"  fillna(mean={mean_a:.1f}):\n{df_miss['A'].fillna(mean_a).tolist()}")

# Forward/backward fill
print(f"  ffill: {df_miss['A'].ffill().tolist()}")
print(f"  bfill: {df_miss['A'].bfill().tolist()}")

# Interpolate
print(f"  interpolate: {df_miss['A'].interpolate().tolist()}")

# dropna
print(f"\n  dropna(how='any'): {len(df_miss.dropna())} rows")
print(f"  dropna(how='all'): {len(df_miss.dropna(how='all'))} rows")
print(f"  dropna(subset=['A']): {len(df_miss.dropna(subset=['A']))} rows")


# =====================================================================
#   PARTE 6: SORT, FILTER, ASSIGN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: SORT, FILTER, ASSIGN ===")
print("=" * 80)

print("\n--- Sorting ---")

print(f"  Sort by edad:\n{df.sort_values('edad')[['nombre','edad']]}")
print(f"\n  Sort by salario desc:\n{df.sort_values('salario', ascending=False)[['nombre','salario']]}")
print(f"\n  Sort by multiple:\n{df.sort_values(['departamento','salario'], ascending=[True,False])[['nombre','departamento','salario']]}")


print("\n--- Filtering ---")

# Boolean mask
mask = (df['edad'] > 28) & (df['departamento'] == 'Engineering')
print(f"  Engineers > 28:\n{df.loc[mask, ['nombre','edad']]}")

# isin
print(f"\n  isin(['Marketing','Sales']):\n{df[df['departamento'].isin(['Marketing','Sales'])][['nombre','departamento']]}")

# query (string-based)
result = df.query("salario > 60000 and edad < 33")
print(f"\n  query('salario > 60000 and edad < 33'):\n{result[['nombre','salario','edad']]}")


print("\n--- Assign (inmutable) ---")

df_new = df.assign(
    salario_mensual=df['salario'] / 12,
    senior=df['edad'] >= 30,
)
print(f"  Columns: {df_new.columns.tolist()}")
print(f"  Original unchanged: {df.columns.tolist()}")


# =====================================================================
#   PARTE 7: STRING OPERATIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: STRING OPERATIONS ===")
print("=" * 80)

"""
df['col'].str.method(): operaciones vectorizadas sobre strings.
"""

print("\n--- String methods ---")

names = pd.Series(['  Alice Smith  ', 'bob jones', 'CHARLIE BROWN', 'diana_prince'])

print(f"  strip:      {names.str.strip().tolist()}")
print(f"  lower:      {names.str.lower().tolist()}")
print(f"  upper:      {names.str.upper().tolist()}")
print(f"  title:      {names.str.title().tolist()}")
print(f"  contains:   {names.str.contains('a', case=False).tolist()}")
print(f"  len:         {names.str.len().tolist()}")
print(f"  split(' '): {names.str.strip().str.split(' ').tolist()}")
print(f"  replace:    {names.str.replace('_', ' ').tolist()}")


print("\n--- Regex ---")

emails = pd.Series(['alice@gmail.com', 'bob@company.org', 'invalid', 'charlie@yahoo.es'])
pattern = r'^[\w.]+@[\w.]+\.\w{2,}$'
print(f"  Valid emails: {emails.str.match(pattern).tolist()}")
print(f"  Extract domain: {emails.str.extract(r'@([\w.]+)')[0].tolist()}")


# =====================================================================
#   PARTE 8: DATETIME OPERATIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: DATETIME ===")
print("=" * 80)

print("\n--- Crear datetime ---")

dates = pd.to_datetime(['2024-01-15', '2024-03-20', '2024-06-01', '2024-12-25'])
df_dates = pd.DataFrame({
    'fecha': dates,
    'ventas': [100, 200, 150, 300],
})

print(f"  Dates:\n{df_dates}")
print(f"  dtype: {df_dates['fecha'].dtype}")


print("\n--- Componentes ---")

print(f"  year:       {df_dates['fecha'].dt.year.tolist()}")
print(f"  month:      {df_dates['fecha'].dt.month.tolist()}")
print(f"  day:        {df_dates['fecha'].dt.day.tolist()}")
print(f"  dayofweek:  {df_dates['fecha'].dt.dayofweek.tolist()}")
print(f"  day_name:   {df_dates['fecha'].dt.day_name().tolist()}")
print(f"  quarter:    {df_dates['fecha'].dt.quarter.tolist()}")


print("\n--- Date ranges ---")

rng = pd.date_range('2024-01-01', periods=12, freq='MS')
print(f"  Monthly start: {rng[:4].tolist()}")

biz = pd.bdate_range('2024-01-01', periods=5)
print(f"  Business days: {biz.tolist()}")


# =====================================================================
#   PARTE 9: MEMORY OPTIMIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: MEMORY OPTIMIZATION ===")
print("=" * 80)

"""
Pandas por defecto usa int64 y float64. Casi siempre puedes reducir.
"""

print("\n--- Downcast automatico ---")

def optimize_df(df):
    """Optimizar memoria de un DataFrame."""
    result = df.copy()
    initial = result.memory_usage(deep=True).sum()
    
    for col in result.columns:
        col_type = result[col].dtype
        
        if col_type == 'object':
            n_unique = result[col].nunique()
            n_total = len(result[col])
            if n_unique / n_total < 0.5:
                result[col] = result[col].astype('category')
        
        elif col_type == 'int64':
            result[col] = pd.to_numeric(result[col], downcast='integer')
        
        elif col_type == 'float64':
            result[col] = pd.to_numeric(result[col], downcast='float')
    
    final = result.memory_usage(deep=True).sum()
    print(f"  Before: {initial:,} bytes")
    print(f"  After:  {final:,} bytes")
    print(f"  Saved:  {(1 - final/initial):.1%}")
    return result

np.random.seed(42)
df_big = pd.DataFrame({
    'id': np.arange(10000),
    'value': np.random.randn(10000),
    'category': np.random.choice(['A', 'B', 'C'], 10000),
    'flag': np.random.randint(0, 2, 10000),
})

df_optimized = optimize_df(df_big)
print(f"\n  Dtypes after:\n{df_optimized.dtypes}")


# =====================================================================
#   PARTE 10: MULTIINDEX
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: MULTIINDEX ===")
print("=" * 80)

"""
MultiIndex: indices jerarquicos. Filas o columnas con multiples niveles.
"""

print("\n--- Crear MultiIndex ---")

arrays = [
    ['Engineering', 'Engineering', 'Marketing', 'Marketing', 'Sales'],
    ['Alice', 'Charlie', 'Bob', 'Eve', 'Diana'],
]
index = pd.MultiIndex.from_arrays(arrays, names=['dept', 'name'])
df_multi = pd.DataFrame({
    'salario': [70000, 90000, 55000, 80000, 65000],
    'edad': [30, 35, 25, 32, 28],
}, index=index)

print(f"  MultiIndex DataFrame:\n{df_multi}")
print(f"\n  Levels: {df_multi.index.names}")

# Seleccionar por nivel
print(f"\n  loc['Engineering']:\n{df_multi.loc['Engineering']}")
print(f"\n  xs('Alice', level='name'):\n{df_multi.xs('Alice', level='name')}")


# =====================================================================
#   PARTE 11: METHOD CHAINING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: METHOD CHAINING Y PIPE ===")
print("=" * 80)

"""
Method chaining: encadenar operaciones sin variables intermedias.
pipe(): aplicar funciones custom en la cadena.
"""

print("\n--- Method chaining ---")

result = (
    df
    .assign(salario_anual=lambda x: x['salario'])
    .query("edad >= 28")
    .sort_values('salario', ascending=False)
    .reset_index(drop=True)
    [['nombre', 'salario', 'edad']]
)
print(f"  Chained result:\n{result}")


print("\n--- pipe() ---")

def add_salary_rank(df):
    return df.assign(rank=df['salario'].rank(ascending=False).astype(int))

def filter_top_n(df, n=3):
    return df.nsmallest(n, 'rank')

result_piped = (
    df
    .pipe(add_salary_rank)
    .pipe(filter_top_n, n=3)
    [['nombre', 'salario', 'rank']]
)
print(f"  Piped result:\n{result_piped}")


# =====================================================================
#   PARTE 12: APPLY, MAP, APPLYMAP
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: APPLY, MAP ===")
print("=" * 80)

"""
- Series.map(): elemento a elemento.
- Series.apply(): elemento a elemento (mas flexible).
- DataFrame.apply(): por fila o columna.
- EVITAR cuando hay alternativa vectorizada.
"""

print("\n--- map ---")

dept_map = {'Engineering': 'ENG', 'Marketing': 'MKT', 'Sales': 'SLS'}
df_mapped = df.assign(dept_code=df['departamento'].map(dept_map))
print(f"  Mapped:\n{df_mapped[['nombre','dept_code']]}")


print("\n--- apply (Series) ---")

df_applied = df.assign(
    nombre_len=df['nombre'].apply(len),
    salario_cat=df['salario'].apply(
        lambda x: 'alto' if x > 70000 else 'medio' if x > 55000 else 'bajo'
    ),
)
print(f"  Applied:\n{df_applied[['nombre','nombre_len','salario_cat']]}")


print("\n--- apply (DataFrame) ---")

# Por columna (axis=0)
numeric_cols = df[['edad', 'salario']]
print(f"  Range per col:\n{numeric_cols.apply(lambda x: x.max() - x.min())}")

# Por fila (axis=1) — LENTO, evitar
df_row = df.assign(
    info=df.apply(lambda row: f"{row['nombre']}({row['edad']})", axis=1)
)
print(f"\n  Per-row apply:\n{df_row[['info']]}")


# =====================================================================
#   PARTE 13: DUPLICADOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: DUPLICADOS ===")
print("=" * 80)

print("\n--- Detectar y eliminar duplicados ---")

df_dup = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob'],
    'score': [90, 80, 90, 70, 85],
})

print(f"  Original:\n{df_dup}")
print(f"  Duplicated: {df_dup.duplicated().tolist()}")
print(f"  Duplicated (subset='name'): {df_dup.duplicated(subset=['name']).tolist()}")
print(f"  drop_duplicates:\n{df_dup.drop_duplicates(subset=['name'], keep='first')}")
print(f"  drop_duplicates(keep='last'):\n{df_dup.drop_duplicates(subset=['name'], keep='last')}")


# =====================================================================
#   PARTE 14: VALUE_COUNTS Y ESTADISTICAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: VALUE_COUNTS ===")
print("=" * 80)

print("\n--- value_counts ---")

print(f"  value_counts:\n{df['departamento'].value_counts()}")
print(f"\n  normalize:\n{df['departamento'].value_counts(normalize=True)}")

# Con bins para numericos
print(f"\n  edad bins:\n{pd.cut(df['edad'], bins=3).value_counts()}")


print("\n--- nlargest / nsmallest ---")

print(f"  Top 3 salarios:\n{df.nlargest(3, 'salario')[['nombre','salario']]}")
print(f"\n  Bottom 2 edades:\n{df.nsmallest(2, 'edad')[['nombre','edad']]}")


# =====================================================================
#   PARTE 15: REPLACE Y CLIP
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: REPLACE, CLIP, WHERE ===")
print("=" * 80)

print("\n--- replace ---")

s = pd.Series([1, 2, 3, 4, 5, -999, 7, -999])
print(f"  Original: {s.tolist()}")
print(f"  replace(-999, np.nan): {s.replace(-999, np.nan).tolist()}")
print(f"  replace(dict): {s.replace({1: 'one', 2: 'two'}).tolist()}")


print("\n--- clip ---")

print(f"  clip(2, 4): {s.clip(2, 4).tolist()}")


print("\n--- where / mask ---")

s = pd.Series([10, 20, 30, 40, 50])
print(f"  where(s > 25): {s.where(s > 25, other=-1).tolist()}")
print(f"  mask(s > 25):  {s.mask(s > 25, other=-1).tolist()}")


# =====================================================================
#   PARTE 16: RANK Y SAMPLE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: RANK Y SAMPLE ===")
print("=" * 80)

print("\n--- rank ---")

scores = pd.Series([80, 90, 80, 70, 95], name='score')
print(f"  Scores: {scores.tolist()}")
print(f"  rank(average): {scores.rank().tolist()}")
print(f"  rank(min):     {scores.rank(method='min').tolist()}")
print(f"  rank(dense):   {scores.rank(method='dense').tolist()}")
print(f"  rank(pct):     {scores.rank(pct=True).tolist()}")


print("\n--- sample ---")

print(f"  sample(3):\n{df.sample(3, random_state=42)[['nombre','edad']]}")
print(f"\n  sample(frac=0.4):\n{df.sample(frac=0.4, random_state=42)[['nombre']]}")

# Weighted sampling
weights = [0.1, 0.1, 0.5, 0.1, 0.2]
print(f"\n  weighted sample (Charlie=0.5):\n{df.sample(3, weights=weights, random_state=42)[['nombre']]}")


# =====================================================================
#   PARTE 17: ITERACION (Y POR QUE EVITARLA)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: ITERACION ===")
print("=" * 80)

"""
REGLA: NUNCA iterar sobre un DataFrame si hay alternativa.
Orden de preferencia:
1. Vectorizado (numpy/pandas ops)
2. apply()
3. itertuples()
4. iterrows()  <- MAS LENTO, evitar siempre
"""

import time

print("\n--- Benchmark: vectorized vs itertuples vs iterrows ---")

n = 50000
df_bench = pd.DataFrame({
    'a': np.random.randn(n),
    'b': np.random.randn(n),
})

# Vectorized
start = time.perf_counter()
result_vec = df_bench['a'] ** 2 + df_bench['b'] ** 2
t_vec = time.perf_counter() - start

# itertuples
start = time.perf_counter()
result_tuples = []
for row in df_bench.itertuples():
    result_tuples.append(row.a ** 2 + row.b ** 2)
t_tuples = time.perf_counter() - start

# iterrows
start = time.perf_counter()
result_rows = []
for _, row in df_bench.head(5000).iterrows():  # Solo 5k por velocidad
    result_rows.append(row['a'] ** 2 + row['b'] ** 2)
t_rows = time.perf_counter() - start

print(f"  Vectorized ({n:,}):    {t_vec:.4f}s")
print(f"  itertuples ({n:,}):    {t_tuples:.4f}s ({t_tuples/t_vec:.0f}x slower)")
print(f"  iterrows (5,000):      {t_rows:.4f}s (extrapolated: {t_rows*10:.1f}s)")


# =====================================================================
#   PARTE 18: ACCESSORS AVANZADOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: ACCESSORS AVANZADOS ===")
print("=" * 80)

"""
Accessors de Pandas:
- .str: operaciones de strings.
- .dt: operaciones de datetime.
- .cat: operaciones de categoricos.
- .plot: visualizacion (matplotlib backend).
"""

print("\n--- .cat accessor ---")

s_cat = pd.Categorical(['A', 'B', 'C', 'A', 'B'], ordered=True, categories=['C', 'B', 'A'])
s = pd.Series(s_cat)

print(f"  Categories: {s.cat.categories.tolist()}")
print(f"  Ordered: {s.cat.ordered}")
print(f"  Codes: {s.cat.codes.tolist()}")

# Reorder
s_reordered = s.cat.reorder_categories(['A', 'B', 'C'])
print(f"  Reordered: {s_reordered.cat.categories.tolist()}")

# Add/remove
s_added = s.cat.add_categories(['D'])
print(f"  Added 'D': {s_added.cat.categories.tolist()}")


print("\n--- Timedelta operations ---")

td = pd.to_timedelta(['1 days', '2 days 3 hours', '1 hours 30 min'])
print(f"  Timedeltas: {td.tolist()}")
print(f"  Total seconds: {td.total_seconds().tolist()}")
print(f"  Components days: {td.days.tolist()}")


# =====================================================================
#   PARTE 19: COPY SEMANTICS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: COPY SEMANTICS ===")
print("=" * 80)

"""
CRITICO entender cuando Pandas copia vs referencia.

COPIA: .copy(), boolean indexing, fancy indexing, la mayoria de ops.
REFERENCIA: posible con slicing simple, pero NO garantizado.

REGLA: si vas a modificar, SIEMPRE .copy() explicito.
"""

print("\n--- Copy vs Reference ---")

df_orig = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

# SAFE: explicit copy
df_safe = df_orig.copy()
df_safe['a'] = 99
print(f"  After modifying copy, original 'a': {df_orig['a'].tolist()}")

# DANGER: potential reference
df_slice = df_orig[['a']]  # May or may not be copy
print(f"  Slice is copy: depends on Pandas version/CoW")


print("\n--- Copy-on-Write (CoW) ---")

"""
Pandas 2.0+ tiene Copy-on-Write:
pd.options.mode.copy_on_write = True

Con CoW, las views se copian automaticamente al modificar.
Elimina el SettingWithCopyWarning.
"""

try:
    cow_status = pd.options.mode.copy_on_write
    print(f"  CoW enabled: {cow_status}")
except AttributeError:
    print(f"  CoW not available in this Pandas version")

print(f"  Pandas version: {pd.__version__}")


# =====================================================================
#   PARTE 20: INTERVAL Y PERIOD INDEX
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: INTERVAL Y PERIOD ===")
print("=" * 80)

print("\n--- IntervalIndex ---")

intervals = pd.interval_range(start=0, end=5, periods=5)
print(f"  Intervals: {intervals.tolist()}")
print(f"  Contains 2.5: {[2.5 in iv for iv in intervals]}")

# Cut crea intervalos
ages = pd.Series([22, 35, 48, 55, 67])
bins = pd.cut(ages, bins=[0, 30, 50, 70])
print(f"\n  Age bins: {bins.tolist()}")
print(f"  Codes: {bins.cat.codes.tolist()}")


print("\n--- PeriodIndex ---")

periods = pd.period_range('2024-01', periods=6, freq='M')
print(f"  Monthly periods: {periods.tolist()}")

ts_period = pd.Series(range(6), index=periods)
print(f"  Q1 2024: {ts_period['2024Q1'].tolist()}")


# =====================================================================
#   PARTE 21: DATAFRAME FROM RECORDS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: CREATION PATTERNS ===")
print("=" * 80)

print("\n--- From records ---")

records = [
    {'name': 'Alice', 'score': 90},
    {'name': 'Bob', 'score': 85},
    {'name': 'Charlie', 'score': 92},
]
df_rec = pd.DataFrame.from_records(records)
print(f"  From records:\n{df_rec}")


print("\n--- From dict of lists vs list of dicts ---")

# Dict of lists (columnar - preferred, faster)
df_col = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

# List of dicts (row-wise)
df_row = pd.DataFrame([{'a': 1, 'b': 4}, {'a': 2, 'b': 5}, {'a': 3, 'b': 6}])

print(f"  Both equal: {df_col.equals(df_row)}")


print("\n--- to_dict patterns ---")

df_small = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
print(f"  to_dict('dict'):   {df_small.to_dict()}")
print(f"  to_dict('list'):   {df_small.to_dict('list')}")
print(f"  to_dict('records'):{df_small.to_dict('records')}")
print(f"  to_dict('index'):  {df_small.to_dict('index')}")


# =====================================================================
#   PARTE 22: EVAL Y QUERY INTERNALS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 22: EVAL Y QUERY ===")
print("=" * 80)

"""
eval/query: expresiones string evaluadas eficientemente.
- Menos memoria temporal (no crea arrays intermedios).
- Sintaxis mas legible para condiciones complejas.
- Variables locales con @variable.
"""

print("\n--- query con variables locales ---")

min_edad = 28
dept = 'Engineering'
result = df.query("edad >= @min_edad and departamento == @dept")
print(f"  query with @locals:\n{result[['nombre','edad','departamento']]}")


print("\n--- eval para crear columnas ---")

df_eval = pd.DataFrame({'a': [1.0, 2.0, 3.0], 'b': [4.0, 5.0, 6.0]})
df_eval = df_eval.eval("""
    c = a + b
    d = a * b
    e = (a + b) / 2
""")
print(f"  Multi-column eval:\n{df_eval}")


# =====================================================================
#   PARTE 23: SPARSE DTYPES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 23: SPARSE DTYPES ===")
print("=" * 80)

"""
Sparse: arrays con muchos ceros/NaN.
Ahorra memoria al no almacenar los fill_values.
"""

print("\n--- Sparse arrays ---")

# Crear one-hot sparse (comun despues de get_dummies)
np.random.seed(42)
sparse_data = np.zeros(10000)
sparse_data[np.random.choice(10000, 100, replace=False)] = 1

s_dense = pd.Series(sparse_data)
s_sparse = s_dense.astype(pd.SparseDtype(float, fill_value=0))

print(f"  Dense memory:  {s_dense.memory_usage():,} bytes")
print(f"  Sparse memory: {s_sparse.memory_usage():,} bytes")
print(f"  Savings: {(1 - s_sparse.memory_usage()/s_dense.memory_usage()):.1%}")
print(f"  Sparse density: {s_sparse.sparse.density:.4f}")


# =====================================================================
#   PARTE 24: TESTING DATAFRAMES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 24: TESTING ===")
print("=" * 80)

"""
pd.testing: funciones para unit tests con DataFrames.
"""

print("\n--- pd.testing ---")

df1 = pd.DataFrame({'a': [1.0, 2.0], 'b': [3.0, 4.0]})
df2 = pd.DataFrame({'a': [1.0, 2.0], 'b': [3.0, 4.0]})
df3 = pd.DataFrame({'a': [1.0, 2.0], 'b': [3.0, 4.001]})

try:
    pd.testing.assert_frame_equal(df1, df2)
    print("  df1 == df2: PASS")
except AssertionError as e:
    print(f"  df1 == df2: FAIL - {e}")

try:
    pd.testing.assert_frame_equal(df1, df3, atol=0.01)
    print("  df1 ≈ df3 (atol=0.01): PASS")
except AssertionError as e:
    print(f"  df1 ≈ df3: FAIL")

# Series testing
s1 = pd.Series([1, 2, 3])
s2 = pd.Series([1, 2, 3])
try:
    pd.testing.assert_series_equal(s1, s2)
    print("  s1 == s2: PASS")
except AssertionError:
    print("  s1 == s2: FAIL")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE DATAFRAMES Y SERIES:

1. Series = ndarray + Index. DataFrame = dict de Series.
2. loc (label) vs iloc (position). NUNCA chained indexing.
3. Categorical dtype: menos memoria para variables repetidas.
4. Missing values: isna, fillna, interpolate.
5. query() para filtros legibles.
6. .str accessor para operaciones de strings vectorizadas.
7. .dt accessor para componentes datetime.
8. Downcast dtypes para reducir memoria 50-80%.
9. MultiIndex para datos jerarquicos.
10. Method chaining + pipe() para codigo limpio.
11. Evitar apply() cuando hay alternativa vectorizada.

Siguiente archivo: GroupBy, Merge y Reshape.
"""

print("\n FIN DE ARCHIVO 01_dataframes_y_series.")
print(" DataFrames y Series han sido dominados.")
