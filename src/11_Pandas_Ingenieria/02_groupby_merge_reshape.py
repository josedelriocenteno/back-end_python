# ===========================================================================
# 02_groupby_merge_reshape.py
# ===========================================================================
# MODULO 11: PANDAS INGENIERIA
# ARCHIVO 02: GroupBy, Merge, Join, Pivot, Melt
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar agrupacion, combinacion de DataFrames, y reshaping.
#
# CONTENIDO:
#   1. GroupBy: split-apply-combine.
#   2. Aggregation: agg, transform, filter.
#   3. Window functions: rolling, expanding, ewm.
#   4. Merge y Join.
#   5. Concatenation.
#   6. Pivot y Melt.
#   7. Cross tabulation.
#   8. Stack y Unstack.
#   9. Patrones de feature engineering.
#   10. Performance: vectorizado vs groupby.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import pandas as pd
import numpy as np


# =====================================================================
#   PARTE 1: GROUPBY BASICO
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: GROUPBY ===")
print("=" * 80)

"""
GroupBy: split-apply-combine.
1. SPLIT: dividir datos por grupo.
2. APPLY: aplicar funcion a cada grupo.
3. COMBINE: unir resultados.
"""

print("\n--- GroupBy basico ---")

np.random.seed(42)
df = pd.DataFrame({
    'departamento': np.random.choice(['Engineering', 'Marketing', 'Sales'], 20),
    'nivel': np.random.choice(['Junior', 'Senior', 'Lead'], 20),
    'salario': np.random.randint(40000, 120000, 20),
    'experiencia': np.random.randint(1, 15, 20),
    'proyectos': np.random.randint(1, 10, 20),
})

print(df.head(10))

# Groupby single column
grouped = df.groupby('departamento')
print(f"\n  Groups: {list(grouped.groups.keys())}")
print(f"  Group sizes: {grouped.size().to_dict()}")

# Aggregaciones basicas
print(f"\n  Mean salario por dept:\n{grouped['salario'].mean()}")
print(f"\n  Sum proyectos por dept:\n{grouped['proyectos'].sum()}")


print("\n--- Groupby multiple columns ---")

multi_group = df.groupby(['departamento', 'nivel'])
print(f"  Mean salario:\n{multi_group['salario'].mean().round(0)}")


# =====================================================================
#   PARTE 2: AGG AVANZADO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: AGG AVANZADO ===")
print("=" * 80)

print("\n--- Multiple aggregations ---")

agg_result = df.groupby('departamento').agg(
    salario_mean=('salario', 'mean'),
    salario_max=('salario', 'max'),
    salario_min=('salario', 'min'),
    experiencia_mean=('experiencia', 'mean'),
    count=('salario', 'count'),
)
print(f"  Named agg:\n{agg_result.round(0)}")


print("\n--- Custom aggregation ---")

def salary_range(x):
    return x.max() - x.min()

def cv(x):
    """Coefficient of variation."""
    return x.std() / x.mean() if x.mean() != 0 else 0

custom_agg = df.groupby('departamento')['salario'].agg(
    [('mean', 'mean'), ('range', salary_range), ('cv', cv)]
)
print(f"  Custom agg:\n{custom_agg.round(3)}")


# =====================================================================
#   PARTE 3: TRANSFORM Y FILTER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: TRANSFORM Y FILTER ===")
print("=" * 80)

"""
transform: retorna Series del MISMO tamaño que input.
Perfecto para feature engineering.
"""

print("\n--- transform ---")

# Normalizar dentro de cada grupo
df_t = df.copy()
df_t['salario_norm'] = df.groupby('departamento')['salario'].transform(
    lambda x: (x - x.mean()) / x.std()
)
print(f"  Normalized within group:\n{df_t[['departamento','salario','salario_norm']].head(8)}")

# Rank dentro de grupo
df_t['rank_in_dept'] = df.groupby('departamento')['salario'].transform('rank', ascending=False)
print(f"\n  Rank within dept:\n{df_t[['departamento','salario','rank_in_dept']].head(8)}")

# Porcentaje del total del grupo
df_t['pct_of_dept'] = df.groupby('departamento')['salario'].transform(lambda x: x / x.sum())
print(f"\n  Pct of dept total:\n{df_t[['departamento','salario','pct_of_dept']].head(5)}")


print("\n--- filter ---")

# Filtrar grupos completos
large_depts = df.groupby('departamento').filter(lambda x: len(x) >= 5)
print(f"  Original rows: {len(df)}")
print(f"  After filter (dept >= 5): {len(large_depts)}")


# =====================================================================
#   PARTE 4: WINDOW FUNCTIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: WINDOW FUNCTIONS ===")
print("=" * 80)

"""
rolling: ventana deslizante.
expanding: ventana que crece.
ewm: exponentially weighted.
"""

print("\n--- Rolling ---")

ts = pd.Series(
    np.random.randn(20).cumsum() + 100,
    index=pd.date_range('2024-01-01', periods=20, freq='D'),
    name='price',
)

df_ts = pd.DataFrame({
    'price': ts,
    'MA_3': ts.rolling(3).mean(),
    'MA_7': ts.rolling(7).mean(),
    'STD_5': ts.rolling(5).std(),
})
print(f"  Rolling stats:\n{df_ts.head(10).round(2)}")


print("\n--- EWM ---")

ewm = ts.ewm(span=5).mean()
print(f"\n  EWM(span=5) last 5: {ewm.tail(5).round(2).tolist()}")


print("\n--- Rolling con groupby ---")

df_rolling = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D').tolist() * 2,
    'product': ['A'] * 30 + ['B'] * 30,
    'sales': np.random.randint(10, 100, 60),
})
df_rolling = df_rolling.sort_values(['product', 'date'])

df_rolling['MA_7'] = df_rolling.groupby('product')['sales'].transform(
    lambda x: x.rolling(7).mean()
)
print(f"  Rolling by group (head):\n{df_rolling.head(10)}")


# =====================================================================
#   PARTE 5: MERGE Y JOIN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: MERGE Y JOIN ===")
print("=" * 80)

"""
Merge = SQL JOIN.
- inner: solo matches.
- left: todos de left + matches de right.
- right: todos de right + matches de left.
- outer: todos de ambos.
"""

print("\n--- Merge types ---")

employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'dept_id': [10, 20, 10, 30, 20],
})

departments = pd.DataFrame({
    'dept_id': [10, 20, 40],
    'dept_name': ['Engineering', 'Marketing', 'Research'],
})

for how in ['inner', 'left', 'right', 'outer']:
    result = employees.merge(departments, on='dept_id', how=how)
    print(f"\n  {how.upper()} JOIN ({len(result)} rows):\n{result}")


print("\n--- Merge on multiple keys ---")

df1 = pd.DataFrame({
    'year': [2023, 2023, 2024, 2024],
    'quarter': [1, 2, 1, 2],
    'revenue': [100, 150, 200, 250],
})

df2 = pd.DataFrame({
    'year': [2023, 2024],
    'quarter': [1, 2],
    'budget': [90, 230],
})

merged = df1.merge(df2, on=['year', 'quarter'], how='left')
print(f"  Multi-key merge:\n{merged}")


print("\n--- Merge validation ---")

"""
validate='one_to_one': asegura que no hay duplicados.
indicator=True: muestra de donde viene cada fila.
"""

result = employees.merge(
    departments, on='dept_id', how='outer', indicator=True
)
print(f"\n  With indicator:\n{result}")


# =====================================================================
#   PARTE 6: CONCATENATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: CONCATENATION ===")
print("=" * 80)

print("\n--- concat vertical ---")

df_q1 = pd.DataFrame({'month': [1, 2, 3], 'sales': [100, 200, 150]})
df_q2 = pd.DataFrame({'month': [4, 5, 6], 'sales': [180, 220, 190]})

combined = pd.concat([df_q1, df_q2], ignore_index=True)
print(f"  Vertical concat:\n{combined}")

# Con keys (multi-level index)
combined_keys = pd.concat([df_q1, df_q2], keys=['Q1', 'Q2'])
print(f"\n  With keys:\n{combined_keys}")


print("\n--- concat horizontal ---")

features = pd.DataFrame({'feature_1': [1, 2], 'feature_2': [3, 4]})
labels = pd.DataFrame({'label': [0, 1]})

combined_h = pd.concat([features, labels], axis=1)
print(f"  Horizontal:\n{combined_h}")


# =====================================================================
#   PARTE 7: PIVOT Y MELT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: PIVOT Y MELT ===")
print("=" * 80)

"""
pivot: long -> wide.
melt: wide -> long.
pivot_table: pivot con aggregation.
"""

print("\n--- pivot_table ---")

df_sales = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=12, freq='MS').tolist() * 2,
    'product': ['Widget'] * 12 + ['Gadget'] * 12,
    'region': ['North', 'South'] * 12,
    'sales': np.random.randint(50, 200, 24),
})

pivot = df_sales.pivot_table(
    values='sales',
    index='product',
    columns='region',
    aggfunc=['mean', 'sum'],
)
print(f"  Pivot table:\n{pivot.round(0)}")


print("\n--- melt ---")

df_wide = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'math': [90, 80],
    'science': [85, 95],
    'english': [88, 78],
})

df_long = df_wide.melt(
    id_vars=['name'],
    var_name='subject',
    value_name='score',
)
print(f"  Wide:\n{df_wide}")
print(f"\n  Long (melted):\n{df_long}")


# =====================================================================
#   PARTE 8: CROSSTAB Y STACK/UNSTACK
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: CROSSTAB ===")
print("=" * 80)

print("\n--- pd.crosstab ---")

ct = pd.crosstab(df['departamento'], df['nivel'], margins=True)
print(f"  Crosstab:\n{ct}")


print("\n--- stack/unstack ---")

stacked = ct.stack()
print(f"\n  Stacked (top 5):\n{stacked.head(5)}")

unstacked = stacked.unstack()
print(f"\n  Unstacked:\n{unstacked}")


# =====================================================================
#   PARTE 9: FEATURE ENGINEERING PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: FEATURE ENGINEERING ===")
print("=" * 80)

"""
Patrones comunes de feature engineering con Pandas.
"""

print("\n--- Lag features ---")

df_feat = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=10, freq='D'),
    'value': np.random.randint(10, 100, 10),
})

df_feat['lag_1'] = df_feat['value'].shift(1)
df_feat['lag_7'] = df_feat['value'].shift(7)
df_feat['diff_1'] = df_feat['value'].diff(1)
df_feat['pct_change'] = df_feat['value'].pct_change()
print(f"  Lag features:\n{df_feat}")


print("\n--- Binning ---")

ages = pd.Series([22, 25, 30, 35, 40, 45, 50, 55, 60, 65])
bins_age = pd.cut(ages, bins=[0, 30, 45, 60, 100], labels=['Young', 'Mid', 'Senior', 'Veteran'])
print(f"  Ages: {ages.tolist()}")
print(f"  Binned: {bins_age.tolist()}")

# qcut (equal-frequency bins)
qbins = pd.qcut(ages, q=3, labels=['Low', 'Mid', 'High'])
print(f"  Qcut: {qbins.tolist()}")


print("\n--- One-hot encoding ---")

dummies = pd.get_dummies(df['departamento'], prefix='dept')
print(f"  One-hot:\n{dummies}")


print("\n--- Target encoding (manual) ---")

df_te = df.copy()
target = np.random.randint(0, 2, len(df))
df_te['target'] = target

te_map = df_te.groupby('departamento')['target'].mean()
df_te['dept_target_enc'] = df_te['departamento'].map(te_map)
print(f"\n  Target encoding:\n{df_te[['departamento','target','dept_target_enc']].head()}")


# =====================================================================
#   PARTE 10: PERFORMANCE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: PERFORMANCE ===")
print("=" * 80)

print("\n--- Vectorized vs apply ---")

import time

n = 100000
df_perf = pd.DataFrame({
    'a': np.random.randn(n),
    'b': np.random.randn(n),
})

# Vectorized
start = time.perf_counter()
df_perf['c_vec'] = df_perf['a'] ** 2 + df_perf['b'] ** 2
t_vec = time.perf_counter() - start

# Apply
start = time.perf_counter()
df_perf['c_apply'] = df_perf.apply(lambda r: r['a']**2 + r['b']**2, axis=1)
t_apply = time.perf_counter() - start

print(f"  Vectorized: {t_vec:.4f}s")
print(f"  Apply:      {t_apply:.4f}s")
print(f"  Speedup:    {t_apply/t_vec:.0f}x")


print("\n--- eval() para expresiones complejas ---")

start = time.perf_counter()
df_perf['d_eval'] = df_perf.eval('a ** 2 + b ** 2 + a * b')
t_eval = time.perf_counter() - start
print(f"  eval: {t_eval:.4f}s")


# =====================================================================
#   PARTE 11: EXPANDING WINDOW
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: EXPANDING WINDOW ===")
print("=" * 80)

"""
expanding: ventana que crece desde el inicio.
Util para cumulative statistics.
"""

print("\n--- expanding ---")

s = pd.Series([10, 20, 15, 30, 25, 40, 35])
print(f"  Data: {s.tolist()}")
print(f"  expanding mean:  {s.expanding().mean().round(2).tolist()}")
print(f"  expanding std:   {s.expanding().std().round(2).tolist()}")
print(f"  expanding min:   {s.expanding().min().tolist()}")
print(f"  expanding max:   {s.expanding().max().tolist()}")

# Cumulative operations (equivalentes pero mas rapido)
print(f"\n  cumsum:  {s.cumsum().tolist()}")
print(f"  cummax:  {s.cummax().tolist()}")
print(f"  cummin:  {s.cummin().tolist()}")
print(f"  cumprod: {(s/10).cumprod().round(4).tolist()}")


# =====================================================================
#   PARTE 12: RESAMPLE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: RESAMPLE ===")
print("=" * 80)

"""
resample: re-muestreo temporal.
Downsampling: alta freq -> baja freq (ej: diario a mensual).
Upsampling: baja freq -> alta freq (ej: mensual a diario).
"""

print("\n--- Resample ---")

ts_hourly = pd.Series(
    np.random.randn(24 * 30),  # 30 dias hourly
    index=pd.date_range('2024-01-01', periods=24*30, freq='h'),
)

# Downsample a diario
daily = ts_hourly.resample('D').agg(['mean', 'min', 'max'])
print(f"  Hourly -> Daily (head):\n{daily.head(5).round(3)}")

# Downsample a semanal
weekly = ts_hourly.resample('W').mean()
print(f"\n  Weekly mean (first 4):\n{weekly.head(4).round(3)}")

# OHLC (Open-High-Low-Close)
ohlc = ts_hourly.resample('D').ohlc()
print(f"\n  Daily OHLC (head):\n{ohlc.head(3).round(3)}")


# =====================================================================
#   PARTE 13: MERGE_ASOF
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: MERGE_ASOF ===")
print("=" * 80)

"""
merge_asof: merge por valor MAS CERCANO (no exacto).
Perfecto para: trades con quotes, eventos con timestamps.
"""

print("\n--- merge_asof ---")

trades = pd.DataFrame({
    'time': pd.to_datetime(['10:00:01', '10:00:03', '10:00:05']),
    'ticker': ['AAPL', 'AAPL', 'AAPL'],
    'price': [150.0, 151.0, 149.5],
})

quotes = pd.DataFrame({
    'time': pd.to_datetime(['10:00:00', '10:00:02', '10:00:04']),
    'ticker': ['AAPL', 'AAPL', 'AAPL'],
    'bid': [149.5, 150.5, 149.0],
    'ask': [150.5, 151.5, 150.0],
})

merged = pd.merge_asof(trades, quotes, on='time', by='ticker')
print(f"  Trades:\n{trades}")
print(f"\n  Quotes:\n{quotes}")
print(f"\n  merge_asof:\n{merged}")


# =====================================================================
#   PARTE 14: EXPLODE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: EXPLODE ===")
print("=" * 80)

"""
explode: expandir listas en filas individuales.
Util para datos desnormalizados.
"""

print("\n--- explode ---")

df_lists = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'skills': [['Python', 'SQL'], ['Java'], ['Python', 'R', 'SQL']],
    'scores': [[90, 85], [80], [95, 88, 92]],
})

print(f"  Original:\n{df_lists}")
exploded = df_lists.explode(['skills', 'scores'])
print(f"\n  Exploded:\n{exploded}")


# =====================================================================
#   PARTE 15: COMBINE_FIRST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: COMBINE_FIRST ===")
print("=" * 80)

"""
combine_first: rellenar NaN de un DF con valores de otro.
Como un COALESCE de SQL.
"""

print("\n--- combine_first ---")

df1 = pd.DataFrame({'A': [1, np.nan, 3], 'B': [np.nan, 5, 6]})
df2 = pd.DataFrame({'A': [10, 20, 30], 'B': [40, 50, 60]})

result = df1.combine_first(df2)
print(f"  df1:\n{df1}")
print(f"\n  df2:\n{df2}")
print(f"\n  combine_first:\n{result}")


# =====================================================================
#   PARTE 16: GROUPBY ITERATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: GROUPBY ITERATION ===")
print("=" * 80)

print("\n--- Iterar sobre grupos ---")

for name, group in df.groupby('departamento'):
    print(f"  Group '{name}': {len(group)} rows, mean salary={group['salario'].mean():.0f}")


print("\n--- GroupBy con apply ---")

def top_earner(group):
    """Retornar el top earner de cada grupo."""
    return group.nlargest(1, 'salario')

top_earners = df.groupby('departamento').apply(top_earner, include_groups=False)
print(f"\n  Top earners:\n{top_earners}")


print("\n--- GroupBy + nth/first/last ---")

print(f"  First of each group:\n{df.groupby('departamento').first()}")
print(f"\n  Last of each group:\n{df.groupby('departamento').last()}")


# =====================================================================
#   PARTE 17: CUMULATIVE OPS POR GRUPO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: CUMULATIVE POR GRUPO ===")
print("=" * 80)

print("\n--- cumsum, cumcount por grupo ---")

df_cum = df[['departamento', 'salario']].copy()
df_cum['cum_salary'] = df_cum.groupby('departamento')['salario'].cumsum()
df_cum['count_in_group'] = df_cum.groupby('departamento').cumcount()
df_cum['running_avg'] = df_cum.groupby('departamento')['salario'].transform(
    lambda x: x.expanding().mean()
)

print(f"  Cumulative ops:\n{df_cum.head(10)}")


# =====================================================================
#   PARTE 18: WINDOW CON MIN_PERIODS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: ROLLING AVANZADO ===")
print("=" * 80)

print("\n--- min_periods y center ---")

s_sparse = pd.Series([1, np.nan, 3, np.nan, 5, 6, 7])

print(f"  Data: {s_sparse.tolist()}")
print(f"  rolling(3).mean():            {s_sparse.rolling(3).mean().tolist()}")
print(f"  rolling(3, min_periods=1):    {s_sparse.rolling(3, min_periods=1).mean().round(2).tolist()}")
print(f"  rolling(3, center=True):      {s_sparse.rolling(3, center=True).mean().tolist()}")


print("\n--- Rolling con funcion custom ---")

def rolling_zscore(x):
    return (x.iloc[-1] - x.mean()) / (x.std() + 1e-8)

s_data = pd.Series(np.random.randn(20).cumsum())
z_scores = s_data.rolling(5).apply(rolling_zscore)
print(f"  Rolling z-scores (last 5): {z_scores.tail(5).round(3).tolist()}")


# =====================================================================
#   PARTE 19: SQL COMPARISON
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: PANDAS vs SQL ===")
print("=" * 80)

"""
Equivalencias SQL -> Pandas:

SELECT col1, col2 FROM table       -> df[['col1', 'col2']]
SELECT * WHERE col > val           -> df[df['col'] > val]
SELECT * ORDER BY col DESC         -> df.sort_values('col', ascending=False)
SELECT col, COUNT(*) GROUP BY col  -> df.groupby('col').size()
SELECT * LIMIT 10                  -> df.head(10)
SELECT DISTINCT col                -> df['col'].unique()
INNER JOIN                         -> df1.merge(df2, on='key')
LEFT JOIN                          -> df1.merge(df2, on='key', how='left')
UNION ALL                          -> pd.concat([df1, df2])
CASE WHEN                          -> np.select / np.where
WINDOW FUNCTIONS                   -> df.groupby().transform()
"""

print("  SQL equivalences documented above.")
print("  Pandas can replace most SQL for data analysis.")


# =====================================================================
#   PARTE 20: MULTI-TABLE PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: MULTI-TABLE PATTERNS ===")
print("=" * 80)

print("\n--- Star schema join ---")

# Fact table
fact = pd.DataFrame({
    'order_id': range(1, 11),
    'product_id': [1, 2, 1, 3, 2, 1, 3, 2, 1, 3],
    'customer_id': [101, 102, 101, 103, 102, 104, 103, 101, 102, 104],
    'amount': np.random.randint(10, 100, 10),
})

# Dimension tables
dim_product = pd.DataFrame({
    'product_id': [1, 2, 3],
    'product_name': ['Widget', 'Gadget', 'Doohickey'],
})

dim_customer = pd.DataFrame({
    'customer_id': [101, 102, 103, 104],
    'customer_name': ['Alice', 'Bob', 'Charlie', 'Diana'],
})

# Join all
result = (
    fact
    .merge(dim_product, on='product_id')
    .merge(dim_customer, on='customer_id')
)

# Analyze
summary = result.groupby('product_name')['amount'].agg(['sum', 'mean', 'count'])
print(f"  Star schema analysis:\n{summary.round(1)}")

by_customer = result.groupby('customer_name')['amount'].sum().sort_values(ascending=False)
print(f"\n  Revenue by customer:\n{by_customer}")


# =====================================================================
#   PARTE 21: ANTI-JOIN Y SEMI-JOIN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: ANTI-JOIN Y SEMI-JOIN ===")
print("=" * 80)

"""
Anti-join: filas en A que NO estan en B.
Semi-join: filas en A que SI estan en B (sin duplicar).
No existen nativamente, pero se simulan.
"""

print("\n--- Anti-join ---")

# Employees sin departamento
anti = employees.merge(departments, on='dept_id', how='left', indicator=True)
anti_join = anti[anti['_merge'] == 'left_only'].drop('_merge', axis=1)
print(f"  Employees without dept:\n{anti_join}")


print("\n--- Semi-join ---")

# Solo employees que tienen departamento valido
semi_join = employees[employees['dept_id'].isin(departments['dept_id'])]
print(f"  Employees with valid dept:\n{semi_join}")


# =====================================================================
#   PARTE 22: CONDITIONAL AGGREGATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 22: CONDITIONAL AGGREGATION ===")
print("=" * 80)

"""
Equivalente a CASE WHEN dentro de aggregation.
"""

print("\n--- Conditional counts ---")

df_cond = df.copy()
cond_agg = df_cond.groupby('departamento').agg(
    total=('salario', 'count'),
    high_salary=('salario', lambda x: (x > 80000).sum()),
    avg_senior=('salario', lambda x: x[df_cond.loc[x.index, 'experiencia'] > 5].mean()),
)
print(f"  Conditional agg:\n{cond_agg.round(0)}")


print("\n--- np.where en aggregation ---")

df_cond['salary_tier'] = np.where(df_cond['salario'] > 80000, 'High', 'Low')
tier_stats = df_cond.groupby(['departamento', 'salary_tier']).size().unstack(fill_value=0)
print(f"\n  Salary tier by dept:\n{tier_stats}")


# =====================================================================
#   PARTE 23: SELF-JOIN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 23: SELF-JOIN ===")
print("=" * 80)

"""
Self-join: merge un DataFrame consigo mismo.
Util para relaciones jerarquicas (manager-employee).
"""

print("\n--- Self-join: employee-manager ---")

org = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['CEO', 'VP_Eng', 'VP_Sales', 'Dev_1', 'Dev_2'],
    'manager_id': [None, 1, 1, 2, 2],
})

org_with_mgr = org.merge(
    org[['emp_id', 'name']].rename(columns={'emp_id': 'manager_id', 'name': 'manager_name'}),
    on='manager_id',
    how='left',
)
print(f"  Org with managers:\n{org_with_mgr}")


# =====================================================================
#   PARTE 24: GROUPBY + NGROUP/CUMCOUNT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 24: NGROUP Y CUMCOUNT ===")
print("=" * 80)

print("\n--- ngroup ---")

df_ng = df.copy()
df_ng['group_id'] = df_ng.groupby('departamento').ngroup()
print(f"  Group IDs:\n{df_ng[['departamento','group_id']].drop_duplicates()}")


print("\n--- cumcount ---")

df_ng['item_in_group'] = df_ng.groupby('departamento').cumcount()
print(f"  Item numbers:\n{df_ng[['departamento','item_in_group']].head(10)}")


# =====================================================================
#   PARTE 25: PIVOT FROM SCRATCH
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 25: PIVOT AVANZADO ===")
print("=" * 80)

print("\n--- pivot_table con margins ---")

np.random.seed(42)
df_pivot = pd.DataFrame({
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'product': np.random.choice(['A', 'B', 'C'], 100),
    'sales': np.random.randint(10, 200, 100),
    'quantity': np.random.randint(1, 20, 100),
})

pt = df_pivot.pivot_table(
    values=['sales', 'quantity'],
    index='region',
    columns='product',
    aggfunc='sum',
    margins=True,
    margins_name='TOTAL',
)
print(f"  Pivot with margins:\n{pt}")


print("\n--- Pivot con percentages ---")

pt_pct = pt['sales'].div(pt['sales']['TOTAL'], axis=0).round(3)
print(f"\n  Sales percentages:\n{pt_pct}")


# =====================================================================
#   PARTE 26: COMPARISON OPERATORS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 26: COMPARISON Y COMBINE ===")
print("=" * 80)

print("\n--- DataFrame.compare ---")

df_v1 = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df_v2 = pd.DataFrame({'a': [1, 20, 3], 'b': [4, 5, 60]})

diff = df_v1.compare(df_v2)
print(f"  v1:\n{df_v1}")
print(f"  v2:\n{df_v2}")
print(f"  Differences:\n{diff}")


print("\n--- update ---")

df_base = pd.DataFrame({'a': [1, np.nan, 3], 'b': [4, 5, np.nan]})
df_update = pd.DataFrame({'a': [10, 20, 30], 'b': [40, 50, 60]})

df_base.update(df_update, overwrite=False)  # Solo rellena NaN
print(f"  Update (only NaN):\n{df_base}")


# =====================================================================
#   PARTE 27: GROUPBY + PIPE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 27: GROUPBY PIPE ===")
print("=" * 80)

"""
pipe() en GroupBy: encadenar funciones custom.
"""

print("\n--- GroupBy pipe ---")

def normalize_within_group(grouped):
    return grouped.transform(lambda x: (x - x.mean()) / (x.std() + 1e-8))

normalized = (
    df.groupby('departamento')['salario']
    .pipe(normalize_within_group)
)
print(f"  Normalized salaries (first 5):\n{normalized.head(5).round(3)}")


# =====================================================================
#   PARTE 28: PERCENTILE AGGREGATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 28: PERCENTILE AGG ===")
print("=" * 80)

print("\n--- Percentiles por grupo ---")

percentile_agg = df.groupby('departamento')['salario'].agg(
    p25=lambda x: x.quantile(0.25),
    p50='median',
    p75=lambda x: x.quantile(0.75),
    p90=lambda x: x.quantile(0.90),
)
print(f"  Percentiles:\n{percentile_agg.round(0)}")


print("\n--- describe() por grupo ---")

desc = df.groupby('departamento')['salario'].describe()
print(f"  Describe:\n{desc.round(0)}")


# =====================================================================
#   PARTE 29: SCD TYPE 2 PATTERN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 29: SCD TYPE 2 ===")
print("=" * 80)

"""
Slowly Changing Dimension Type 2:
Mantener historial de cambios con valid_from/valid_to.
Patron clave en data warehousing.
"""

print("\n--- SCD Type 2 ---")

# Current state
scd = pd.DataFrame({
    'emp_id': [1, 1, 1, 2, 2],
    'name': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob'],
    'dept': ['Eng', 'Sales', 'Eng', 'Mkt', 'Eng'],
    'valid_from': pd.to_datetime(['2020-01-01', '2021-06-01', '2023-01-01', '2020-01-01', '2022-03-01']),
    'valid_to': pd.to_datetime(['2021-05-31', '2022-12-31', '2099-12-31', '2022-02-28', '2099-12-31']),
})

print(f"  SCD table:\n{scd}")

# Get current state
current = scd[scd['valid_to'] == pd.Timestamp('2099-12-31')]
print(f"\n  Current state:\n{current[['emp_id','name','dept']]}")

# Get state at a specific date
point_in_time = pd.Timestamp('2021-07-01')
historical = scd[(scd['valid_from'] <= point_in_time) & (scd['valid_to'] >= point_in_time)]
print(f"\n  State at {point_in_time.date()}:\n{historical[['emp_id','name','dept']]}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE GROUPBY, MERGE, RESHAPE:

1. GroupBy = split-apply-combine. transform mantiene shape.
2. agg() con named aggregations para legibilidad.
3. Rolling/expanding/ewm para time series.
4. merge = SQL JOIN. Usar validate para seguridad.
5. concat para apilar DataFrames.
6. pivot_table (long->wide), melt (wide->long).
7. Lag features, binning, one-hot para ML.
8. NUNCA usar apply(axis=1) si hay alternativa vectorizada.

Siguiente archivo: Pipeline de datos para ML.
"""

print("\n FIN DE ARCHIVO 02_groupby_merge_reshape.")
print(" GroupBy, Merge y Reshape han sido dominados.")
