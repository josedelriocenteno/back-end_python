# ===========================================================================
# 03_pipeline_datos_ml.py
# ===========================================================================
# MODULO 11: PANDAS INGENIERIA
# ARCHIVO 03: Pipeline de Datos para ML
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar la preparacion de datos end-to-end para ML:
# limpieza, validacion, feature engineering, splitting.
#
# CONTENIDO:
#   1. Data loading y formatos (CSV, Parquet, JSON).
#   2. Data profiling automatico.
#   3. Data cleaning pipeline.
#   4. Feature engineering avanzado.
#   5. Train/val/test split con Pandas.
#   6. Data validation y quality checks.
#   7. Handling imbalanced data.
#   8. Feature scaling y encoding.
#   9. Pipeline completo end-to-end.
#   10. Anti-patterns y best practices.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import pandas as pd
import numpy as np
import time
import os
import tempfile


# =====================================================================
#   PARTE 1: DATA LOADING
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: DATA LOADING ===")
print("=" * 80)

"""
Formatos comunes:
- CSV: universal, lento, grande.
- Parquet: columnar, rapido, comprimido.
- JSON: flexible, para APIs.
- Feather: rapido para interop Python/R.
"""

print("\n--- CSV ---")

# Crear datos de ejemplo
np.random.seed(42)
n = 10000
df_sample = pd.DataFrame({
    'id': np.arange(n),
    'feature_1': np.random.randn(n),
    'feature_2': np.random.randn(n) * 10,
    'category': np.random.choice(['A', 'B', 'C', 'D'], n),
    'target': np.random.randint(0, 2, n),
    'timestamp': pd.date_range('2024-01-01', periods=n, freq='h'),
})

tmpdir = tempfile.mkdtemp()

# CSV
csv_path = os.path.join(tmpdir, 'data.csv')
start = time.perf_counter()
df_sample.to_csv(csv_path, index=False)
t_write_csv = time.perf_counter() - start

start = time.perf_counter()
df_csv = pd.read_csv(csv_path, parse_dates=['timestamp'])
t_read_csv = time.perf_counter() - start

csv_size = os.path.getsize(csv_path)
print(f"  CSV write: {t_write_csv:.3f}s")
print(f"  CSV read:  {t_read_csv:.3f}s")
print(f"  CSV size:  {csv_size:,} bytes")


print("\n--- Parquet ---")

parquet_path = os.path.join(tmpdir, 'data.parquet')
try:
    start = time.perf_counter()
    df_sample.to_parquet(parquet_path, index=False)
    t_write_pq = time.perf_counter() - start
    
    start = time.perf_counter()
    df_pq = pd.read_parquet(parquet_path)
    t_read_pq = time.perf_counter() - start
    
    pq_size = os.path.getsize(parquet_path)
    print(f"  Parquet write: {t_write_pq:.3f}s")
    print(f"  Parquet read:  {t_read_pq:.3f}s")
    print(f"  Parquet size:  {pq_size:,} bytes")
    print(f"  Compression: {csv_size/pq_size:.1f}x vs CSV")
except ImportError:
    print("  (pyarrow no disponible, skip parquet)")


print("\n--- read_csv avanzado ---")

"""
Parametros criticos de read_csv:
- dtype: especificar tipos (evita inferencia lenta).
- usecols: solo columnas necesarias.
- nrows: limitar filas (para exploration).
- chunksize: procesar por chunks (datasets grandes).
- parse_dates: parsear columnas de fecha.
"""

# Con dtype explicito (mas rapido)
start = time.perf_counter()
df_typed = pd.read_csv(csv_path, dtype={
    'id': np.int32,
    'feature_1': np.float32,
    'feature_2': np.float32,
    'category': 'category',
    'target': np.int8,
}, parse_dates=['timestamp'], usecols=['id', 'feature_1', 'category', 'target'])
t_typed = time.perf_counter() - start
print(f"  Typed read: {t_typed:.3f}s (vs {t_read_csv:.3f}s generic)")
print(f"  Memory: {df_typed.memory_usage(deep=True).sum():,} bytes")

# Cleanup
for f in [csv_path, parquet_path]:
    if os.path.exists(f):
        os.remove(f)
os.rmdir(tmpdir)


# =====================================================================
#   PARTE 2: DATA PROFILING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: DATA PROFILING ===")
print("=" * 80)

"""
Antes de modelar: CONOCER tus datos.
"""

print("\n--- Profiling automatico ---")

def data_profile(df):
    """Perfil completo de un DataFrame."""
    print(f"\n  Shape: {df.shape}")
    print(f"  Memory: {df.memory_usage(deep=True).sum():,} bytes")
    
    print(f"\n  {'Column':<15s} {'Type':<12s} {'NonNull':>7s} {'Null':>5s} {'Unique':>6s} {'Example':<15s}")
    print(f"  {'-'*65}")
    
    for col in df.columns:
        dtype = str(df[col].dtype)[:11]
        non_null = df[col].notna().sum()
        null = df[col].isna().sum()
        unique = df[col].nunique()
        example = str(df[col].dropna().iloc[0])[:14] if non_null > 0 else 'N/A'
        print(f"  {col:<15s} {dtype:<12s} {non_null:>7d} {null:>5d} {unique:>6d} {example:<15s}")
    
    # Numeric stats
    numeric = df.select_dtypes(include=[np.number])
    if len(numeric.columns) > 0:
        print(f"\n  Numeric stats:")
        print(numeric.describe().round(3).to_string())
    
    # Correlations
    if len(numeric.columns) > 1:
        corr = numeric.corr()
        # Find high correlations
        high_corr = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                if abs(corr.iloc[i, j]) > 0.5:
                    high_corr.append((corr.columns[i], corr.columns[j], corr.iloc[i, j]))
        if high_corr:
            print(f"\n  High correlations (|r| > 0.5):")
            for c1, c2, r in high_corr:
                print(f"    {c1} <-> {c2}: {r:.3f}")

data_profile(df_sample)


# =====================================================================
#   PARTE 3: DATA CLEANING PIPELINE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: DATA CLEANING ===")
print("=" * 80)

print("\n--- Crear datos sucios ---")

np.random.seed(42)
df_dirty = pd.DataFrame({
    'name': ['Alice', '  Bob  ', 'CHARLIE', None, 'eve', 'Alice', 'frank'],
    'age': [30, 25, 200, 28, -5, 30, 45],  # 200 y -5 son outliers
    'email': ['alice@test.com', 'bob@test', 'charlie@test.com', None, 'eve@test.com', 'alice@test.com', None],
    'salary': [70000, 55000, np.nan, 65000, 80000, 70000, np.nan],
    'dept': ['Eng', 'Mkt', 'eng', 'Sales', 'ENG', 'Eng', 'mkt'],
})

print(f"  Dirty data:\n{df_dirty}")


print("\n--- Pipeline de limpieza ---")

def clean_pipeline(df):
    """Pipeline de limpieza completo."""
    df = df.copy()
    initial = len(df)
    
    # 1. Strip y normalizar strings
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip().str.lower()
    
    # 2. Estandarizar categorias
    dept_map = {'eng': 'engineering', 'mkt': 'marketing', 'sales': 'sales'}
    df['dept'] = df['dept'].map(dept_map)
    
    # 3. Validar rangos
    df.loc[df['age'] < 0, 'age'] = np.nan
    df.loc[df['age'] > 150, 'age'] = np.nan
    
    # 4. Validar emails
    valid_email = df['email'].str.match(r'^[\w.]+@[\w.]+\.\w{2,}$', na=False)
    df.loc[~valid_email, 'email'] = np.nan
    
    # 5. Imputar missing numericos
    df['salary'] = df['salary'].fillna(df['salary'].median())
    df['age'] = df['age'].fillna(df['age'].median())
    
    # 6. Eliminar duplicados
    df = df.drop_duplicates(subset=['name'], keep='first')
    
    print(f"  Rows: {initial} -> {len(df)}")
    print(f"  Missing after: {df.isna().sum().sum()}")
    
    return df

df_clean = clean_pipeline(df_dirty)
print(f"\n  Clean data:\n{df_clean}")


# =====================================================================
#   PARTE 4: FEATURE ENGINEERING AVANZADO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: FEATURE ENGINEERING ===")
print("=" * 80)

print("\n--- Datetime features ---")

df_dt = pd.DataFrame({
    'timestamp': pd.date_range('2024-01-01', periods=1000, freq='h'),
    'value': np.random.randn(1000).cumsum() + 100,
})

df_dt['hour'] = df_dt['timestamp'].dt.hour
df_dt['day_of_week'] = df_dt['timestamp'].dt.dayofweek
df_dt['is_weekend'] = df_dt['day_of_week'].isin([5, 6]).astype(int)
df_dt['month'] = df_dt['timestamp'].dt.month
df_dt['is_business_hours'] = df_dt['hour'].between(9, 17).astype(int)

# Cyclical encoding
df_dt['hour_sin'] = np.sin(2 * np.pi * df_dt['hour'] / 24)
df_dt['hour_cos'] = np.cos(2 * np.pi * df_dt['hour'] / 24)
df_dt['dow_sin'] = np.sin(2 * np.pi * df_dt['day_of_week'] / 7)
df_dt['dow_cos'] = np.cos(2 * np.pi * df_dt['day_of_week'] / 7)

print(f"  Datetime features:\n{df_dt[['timestamp','hour','hour_sin','hour_cos','is_weekend']].head(6)}")


print("\n--- Interaction features ---")

df_inter = df_sample[['feature_1', 'feature_2']].copy()
df_inter['f1_x_f2'] = df_inter['feature_1'] * df_inter['feature_2']
df_inter['f1_div_f2'] = df_inter['feature_1'] / (df_inter['feature_2'].abs() + 1e-8)
df_inter['f1_plus_f2'] = df_inter['feature_1'] + df_inter['feature_2']
df_inter['f1_sq'] = df_inter['feature_1'] ** 2

print(f"  Interaction features (head):\n{df_inter.head(5).round(4)}")


print("\n--- Aggregation features ---")

# Features de grupo (muy comunes en Kaggle)
df_agg = df_sample.copy()
group_stats = df_agg.groupby('category')['feature_1'].agg(['mean', 'std', 'min', 'max'])
group_stats.columns = [f'cat_f1_{c}' for c in group_stats.columns]

df_agg = df_agg.merge(group_stats, left_on='category', right_index=True)
df_agg['f1_vs_cat_mean'] = df_agg['feature_1'] - df_agg['cat_f1_mean']

print(f"  Agg features:\n{df_agg[['category','feature_1','cat_f1_mean','f1_vs_cat_mean']].head(5).round(4)}")


# =====================================================================
#   PARTE 5: TRAIN/VAL/TEST SPLIT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: TRAIN/VAL/TEST SPLIT ===")
print("=" * 80)

print("\n--- Random split ---")

def train_val_test_split(df, train_frac=0.7, val_frac=0.15, seed=42):
    """Split respetando proporciones."""
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    n = len(df)
    train_end = int(n * train_frac)
    val_end = int(n * (train_frac + val_frac))
    
    return df[:train_end], df[train_end:val_end], df[val_end:]

train, val, test = train_val_test_split(df_sample)
print(f"  Train: {len(train)} ({len(train)/len(df_sample):.1%})")
print(f"  Val:   {len(val)} ({len(val)/len(df_sample):.1%})")
print(f"  Test:  {len(test)} ({len(test)/len(df_sample):.1%})")


print("\n--- Stratified split ---")

def stratified_split(df, target_col, train_frac=0.8, seed=42):
    """Split manteniendo distribucion del target."""
    train_dfs = []
    test_dfs = []
    
    for _, group in df.groupby(target_col):
        group = group.sample(frac=1, random_state=seed)
        n_train = int(len(group) * train_frac)
        train_dfs.append(group[:n_train])
        test_dfs.append(group[n_train:])
    
    return pd.concat(train_dfs), pd.concat(test_dfs)

train_s, test_s = stratified_split(df_sample, 'target')
print(f"\n  Original target dist: {df_sample['target'].value_counts(normalize=True).to_dict()}")
print(f"  Train target dist:   {train_s['target'].value_counts(normalize=True).to_dict()}")
print(f"  Test target dist:    {test_s['target'].value_counts(normalize=True).to_dict()}")


print("\n--- Time-based split ---")

def temporal_split(df, date_col, train_end, val_end):
    """Split temporal (no shuffle!)."""
    train = df[df[date_col] < train_end]
    val = df[(df[date_col] >= train_end) & (df[date_col] < val_end)]
    test = df[df[date_col] >= val_end]
    return train, val, test

train_t, val_t, test_t = temporal_split(
    df_sample, 'timestamp', '2024-07-01', '2024-10-01'
)
print(f"  Temporal split: train={len(train_t)}, val={len(val_t)}, test={len(test_t)}")


# =====================================================================
#   PARTE 6: DATA VALIDATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: DATA VALIDATION ===")
print("=" * 80)

def validate_dataset(df, schema):
    """Validar DataFrame contra un schema."""
    errors = []
    
    # Check required columns
    missing_cols = set(schema['required_columns']) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")
    
    # Check dtypes
    for col, expected_type in schema.get('dtypes', {}).items():
        if col in df.columns and not pd.api.types.is_dtype_equal(df[col].dtype, expected_type):
            errors.append(f"Column '{col}' type: {df[col].dtype} != {expected_type}")
    
    # Check no nulls
    for col in schema.get('no_nulls', []):
        if col in df.columns and df[col].isna().any():
            errors.append(f"Column '{col}' has {df[col].isna().sum()} nulls")
    
    # Check ranges
    for col, (low, high) in schema.get('ranges', {}).items():
        if col in df.columns:
            out = ((df[col] < low) | (df[col] > high)).sum()
            if out > 0:
                errors.append(f"Column '{col}': {out} values outside [{low}, {high}]")
    
    # Check unique
    for col in schema.get('unique', []):
        if col in df.columns and df[col].duplicated().any():
            errors.append(f"Column '{col}' has {df[col].duplicated().sum()} duplicates")
    
    if errors:
        print("  VALIDATION FAILED:")
        for e in errors:
            print(f"    ✗ {e}")
    else:
        print("  ✓ All validations passed!")
    
    return len(errors) == 0

schema = {
    'required_columns': ['id', 'feature_1', 'feature_2', 'target'],
    'no_nulls': ['id', 'target'],
    'unique': ['id'],
    'ranges': {'target': (0, 1)},
}

validate_dataset(df_sample, schema)


# =====================================================================
#   PARTE 7: HANDLING IMBALANCED DATA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: IMBALANCED DATA ===")
print("=" * 80)

print("\n--- Undersampling ---")

def undersample(df, target_col, seed=42):
    """Undersample clase mayoritaria."""
    counts = df[target_col].value_counts()
    min_count = counts.min()
    
    balanced = pd.concat([
        group.sample(min_count, random_state=seed)
        for _, group in df.groupby(target_col)
    ])
    return balanced.sample(frac=1, random_state=seed)

# Crear dataset imbalanced
df_imb = df_sample.copy()
df_imb['rare_target'] = (np.random.random(len(df_imb)) < 0.05).astype(int)

print(f"  Original: {df_imb['rare_target'].value_counts().to_dict()}")
df_under = undersample(df_imb, 'rare_target')
print(f"  Undersampled: {df_under['rare_target'].value_counts().to_dict()}")


print("\n--- Oversampling ---")

def oversample(df, target_col, seed=42):
    """Oversample clase minoritaria."""
    counts = df[target_col].value_counts()
    max_count = counts.max()
    
    balanced = pd.concat([
        group.sample(max_count, replace=True, random_state=seed)
        for _, group in df.groupby(target_col)
    ])
    return balanced.sample(frac=1, random_state=seed)

df_over = oversample(df_imb, 'rare_target')
print(f"  Oversampled: {df_over['rare_target'].value_counts().to_dict()}")


# =====================================================================
#   PARTE 8: FEATURE SCALING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: FEATURE SCALING ===")
print("=" * 80)

print("\n--- Standard scaling con Pandas ---")

def standard_scale(train_df, test_df, cols):
    """Fit en train, transform ambos."""
    means = train_df[cols].mean()
    stds = train_df[cols].std()
    stds[stds == 0] = 1
    
    train_scaled = train_df.copy()
    test_scaled = test_df.copy()
    train_scaled[cols] = (train_df[cols] - means) / stds
    test_scaled[cols] = (test_df[cols] - means) / stds
    
    return train_scaled, test_scaled, means, stds

feature_cols = ['feature_1', 'feature_2']
train_sc, test_sc, means, stds = standard_scale(train, test, feature_cols)

print(f"  Train mean: {train_sc[feature_cols].mean().round(6).to_dict()}")
print(f"  Train std:  {train_sc[feature_cols].std().round(4).to_dict()}")
print(f"  Test mean:  {test_sc[feature_cols].mean().round(4).to_dict()}")


print("\n--- MinMax scaling ---")

def minmax_scale(train_df, test_df, cols):
    """MinMax [0, 1] scaling."""
    mins = train_df[cols].min()
    maxs = train_df[cols].max()
    ranges = maxs - mins
    ranges[ranges == 0] = 1
    
    train_scaled = train_df.copy()
    test_scaled = test_df.copy()
    train_scaled[cols] = (train_df[cols] - mins) / ranges
    test_scaled[cols] = (test_df[cols] - mins) / ranges
    
    return train_scaled, test_scaled

train_mm, test_mm = minmax_scale(train, test, feature_cols)
print(f"  Train min: {train_mm[feature_cols].min().round(4).to_dict()}")
print(f"  Train max: {train_mm[feature_cols].max().round(4).to_dict()}")


# =====================================================================
#   PARTE 9: ANTI-PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: ANTI-PATTERNS ===")
print("=" * 80)

"""
ERRORES COMUNES EN PANDAS:

1. DATA LEAKAGE: scaling/encoding ANTES de split.
   MAL: scale(todo) -> split
   BIEN: split -> fit(train) -> transform(train, test)

2. CHAINED INDEXING:
   MAL: df['col'][0] = val
   BIEN: df.loc[0, 'col'] = val

3. ITERROWS:
   MAL: for _, row in df.iterrows(): ...
   BIEN: vectorized operations o apply

4. APPEND IN LOOP:
   MAL: for x in data: df = df.append(x)
   BIEN: results = []; ... ; pd.concat(results)

5. COPY vs VIEW:
   MAL: df2 = df; df2['new'] = 1  (modifica df!)
   BIEN: df2 = df.copy(); df2['new'] = 1
"""

print("\n--- Data leakage demo ---")

# WRONG: fit on all data
all_mean = df_sample['feature_1'].mean()
all_std = df_sample['feature_1'].std()

# RIGHT: fit only on train
train_mean = train['feature_1'].mean()
train_std = train['feature_1'].std()

print(f"  All data mean:  {all_mean:.4f}")
print(f"  Train mean:     {train_mean:.4f}")
print(f"  Difference:     {abs(all_mean - train_mean):.4f}")
print(f"  (Using all data = data leakage!)")


print("\n--- Append in loop (bad) vs concat (good) ---")

# BAD
start = time.perf_counter()
results_bad = pd.DataFrame()
for i in range(100):
    row = pd.DataFrame({'a': [i], 'b': [i**2]})
    results_bad = pd.concat([results_bad, row])
t_bad = time.perf_counter() - start

# GOOD
start = time.perf_counter()
rows = [{'a': i, 'b': i**2} for i in range(100)]
results_good = pd.DataFrame(rows)
t_good = time.perf_counter() - start

print(f"  Concat in loop: {t_bad:.4f}s")
print(f"  Build list:     {t_good:.6f}s")
print(f"  Speedup:        {t_bad/t_good:.0f}x")


# =====================================================================
#   PARTE 10: OUTLIER DETECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: OUTLIER DETECTION ===")
print("=" * 80)

print("\n--- IQR method ---")

def detect_outliers_iqr(series, factor=1.5):
    """Detectar outliers con IQR."""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - factor * IQR
    upper = Q3 + factor * IQR
    outliers = (series < lower) | (series > upper)
    return outliers, lower, upper

outliers, lower, upper = detect_outliers_iqr(df_sample['feature_1'])
print(f"  Feature_1 outliers: {outliers.sum()} / {len(df_sample)}")
print(f"  Range: [{lower:.3f}, {upper:.3f}]")


print("\n--- Z-score method ---")

def detect_outliers_zscore(series, threshold=3):
    """Outliers por z-score."""
    z = (series - series.mean()) / series.std()
    return z.abs() > threshold

outliers_z = detect_outliers_zscore(df_sample['feature_1'])
print(f"  Z-score outliers (|z|>3): {outliers_z.sum()}")


print("\n--- Percentile capping ---")

def percentile_cap(series, lower_pct=1, upper_pct=99):
    """Cap outliers a percentiles."""
    lower = series.quantile(lower_pct / 100)
    upper = series.quantile(upper_pct / 100)
    return series.clip(lower, upper)

f1_capped = percentile_cap(df_sample['feature_1'])
print(f"  Before: min={df_sample['feature_1'].min():.3f}, max={df_sample['feature_1'].max():.3f}")
print(f"  After:  min={f1_capped.min():.3f}, max={f1_capped.max():.3f}")


# =====================================================================
#   PARTE 11: FEATURE SELECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: FEATURE SELECTION ===")
print("=" * 80)

print("\n--- Correlation-based selection ---")

def drop_high_correlation(df, threshold=0.95):
    """Eliminar features con alta correlacion."""
    numeric = df.select_dtypes(include=[np.number])
    corr_matrix = numeric.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]
    return to_drop

# Crear features correlacionadas
df_corr = df_sample[['feature_1', 'feature_2', 'target']].copy()
df_corr['feature_1_copy'] = df_corr['feature_1'] * 1.01 + np.random.randn(len(df_corr)) * 0.001
df_corr['feature_2_noisy'] = df_corr['feature_2'] + np.random.randn(len(df_corr)) * 0.01

to_drop = drop_high_correlation(df_corr, threshold=0.95)
print(f"  Columns to drop (corr > 0.95): {to_drop}")


print("\n--- Variance threshold ---")

def low_variance_features(df, threshold=0.01):
    """Detectar features con varianza cercana a 0."""
    numeric = df.select_dtypes(include=[np.number])
    variances = numeric.var()
    low_var = variances[variances < threshold].index.tolist()
    return low_var, variances

low_var, variances = low_variance_features(df_sample)
print(f"  Low variance features: {low_var}")
print(f"  Variances:\n{variances.round(4)}")


# =====================================================================
#   PARTE 12: LABEL ENCODING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: LABEL ENCODING ===")
print("=" * 80)

print("\n--- Label encoding manual ---")

class LabelEncoder:
    """Label encoder compatible con train/test split."""
    
    def __init__(self):
        self.mapping = {}
        self.inverse_mapping = {}
    
    def fit(self, series):
        unique = sorted(series.dropna().unique())
        self.mapping = {val: idx for idx, val in enumerate(unique)}
        self.inverse_mapping = {idx: val for val, idx in self.mapping.items()}
        return self
    
    def transform(self, series):
        return series.map(self.mapping)
    
    def inverse_transform(self, series):
        return series.map(self.inverse_mapping)

le = LabelEncoder()
le.fit(df_sample['category'])
encoded = le.transform(df_sample['category'])
decoded = le.inverse_transform(encoded)

print(f"  Mapping: {le.mapping}")
print(f"  Original: {df_sample['category'].head(5).tolist()}")
print(f"  Encoded:  {encoded.head(5).tolist()}")
print(f"  Decoded:  {decoded.head(5).tolist()}")


# =====================================================================
#   PARTE 13: K-FOLD CROSS VALIDATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: K-FOLD ===")
print("=" * 80)

def kfold_split(df, k=5, seed=42):
    """K-fold cross-validation splits."""
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    fold_size = len(df) // k
    
    folds = []
    for i in range(k):
        start = i * fold_size
        end = start + fold_size if i < k - 1 else len(df)
        
        val_idx = list(range(start, end))
        train_idx = [j for j in range(len(df)) if j not in val_idx]
        
        folds.append((train_idx, val_idx))
    
    return folds

folds = kfold_split(df_sample, k=5)
for i, (train_idx, val_idx) in enumerate(folds):
    print(f"  Fold {i+1}: train={len(train_idx)}, val={len(val_idx)}")


# =====================================================================
#   PARTE 14: CHUNKED PROCESSING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: CHUNKED PROCESSING ===")
print("=" * 80)

"""
Para datasets que no caben en RAM.
read_csv(chunksize=N) retorna un iterador.
"""

print("\n--- Chunk processing ---")

# Simular procesamiento por chunks
tmpdir = tempfile.mkdtemp()
csv_path = os.path.join(tmpdir, 'big_data.csv')
df_sample.to_csv(csv_path, index=False)

chunk_stats = []
for chunk in pd.read_csv(csv_path, chunksize=2000):
    stats = {
        'n_rows': len(chunk),
        'mean_f1': chunk['feature_1'].mean(),
        'std_f1': chunk['feature_1'].std(),
    }
    chunk_stats.append(stats)

df_stats = pd.DataFrame(chunk_stats)
print(f"  Chunks: {len(df_stats)}")
print(f"  Rows per chunk: {df_stats['n_rows'].tolist()}")
print(f"  Global mean (approx): {df_stats['mean_f1'].mean():.4f}")
print(f"  Actual mean: {df_sample['feature_1'].mean():.4f}")

os.remove(csv_path)
os.rmdir(tmpdir)


# =====================================================================
#   PARTE 15: END-TO-END PIPELINE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: END-TO-END PIPELINE ===")
print("=" * 80)

def ml_pipeline(df, target_col, feature_cols, cat_cols=None):
    """Pipeline completo de datos para ML."""
    print("\n  [1/6] Profiling...")
    print(f"    Shape: {df.shape}, Missing: {df.isna().sum().sum()}")
    
    print("  [2/6] Cleaning...")
    df = df.dropna(subset=[target_col])
    for col in feature_cols:
        df[col] = df[col].fillna(df[col].median())
    
    print("  [3/6] Encoding categoricals...")
    if cat_cols:
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
        feature_cols = [c for c in df.columns if c != target_col and c != 'id' and c != 'timestamp']
    
    print("  [4/6] Splitting...")
    train, test = stratified_split(df, target_col, train_frac=0.8)
    
    print("  [5/6] Scaling...")
    num_cols = [c for c in feature_cols if df[c].dtype in ['float64', 'float32', 'int64', 'int32']]
    if num_cols:
        means = train[num_cols].mean()
        stds = train[num_cols].std()
        stds[stds == 0] = 1
        train[num_cols] = (train[num_cols] - means) / stds
        test[num_cols] = (test[num_cols] - means) / stds
    
    print("  [6/6] Done!")
    print(f"    Train: {train.shape}, Test: {test.shape}")
    
    return train, test

train_final, test_final = ml_pipeline(
    df_sample.copy(), 'target', ['feature_1', 'feature_2'], cat_cols=['category']
)


# =====================================================================
#   PARTE 16: DATA QUALITY REPORT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: DATA QUALITY REPORT ===")
print("=" * 80)

def data_quality_report(df):
    """Generar reporte de calidad de datos."""
    report = pd.DataFrame({
        'dtype': df.dtypes,
        'non_null': df.notna().sum(),
        'null_pct': (df.isna().sum() / len(df) * 100).round(2),
        'unique': df.nunique(),
        'unique_pct': (df.nunique() / len(df) * 100).round(2),
    })
    
    # Score de calidad (0-100)
    completeness = (1 - df.isna().sum().sum() / df.size) * 100
    uniqueness = (1 - df.duplicated().sum() / len(df)) * 100
    
    print(f"  Quality Report:")
    print(report.to_string())
    print(f"\n  Completeness: {completeness:.1f}%")
    print(f"  Uniqueness: {uniqueness:.1f}%")
    print(f"  Quality Score: {(completeness + uniqueness) / 2:.1f}%")

data_quality_report(df_sample)


# =====================================================================
#   PARTE 17: ROBUST SCALER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: ROBUST SCALER ===")
print("=" * 80)

"""
RobustScaler: usa median e IQR en vez de mean/std.
Resistente a outliers.
"""

def robust_scale(train_df, test_df, cols):
    """Robust scaling (median, IQR)."""
    medians = train_df[cols].median()
    q1 = train_df[cols].quantile(0.25)
    q3 = train_df[cols].quantile(0.75)
    iqr = q3 - q1
    iqr[iqr == 0] = 1
    
    train_scaled = train_df.copy()
    test_scaled = test_df.copy()
    train_scaled[cols] = (train_df[cols] - medians) / iqr
    test_scaled[cols] = (test_df[cols] - medians) / iqr
    
    return train_scaled, test_scaled

train_rb, test_rb = robust_scale(train, test, feature_cols)
print(f"  Robust scaled train median: {train_rb[feature_cols].median().round(4).to_dict()}")
print(f"  Robust scaled train IQR:    {(train_rb[feature_cols].quantile(0.75) - train_rb[feature_cols].quantile(0.25)).round(4).to_dict()}")


# =====================================================================
#   PARTE 18: FREQUENCY ENCODING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: FREQUENCY ENCODING ===")
print("=" * 80)

"""
Frequency encoding: reemplazar categoria con su frecuencia.
Mantiene informacion sobre popularidad.
"""

print("\n--- Frequency encoding ---")

def frequency_encode(train_df, test_df, col):
    """Fit on train, transform both."""
    freq = train_df[col].value_counts(normalize=True)
    train_enc = train_df.copy()
    test_enc = test_df.copy()
    train_enc[f'{col}_freq'] = train_df[col].map(freq)
    test_enc[f'{col}_freq'] = test_df[col].map(freq).fillna(0)
    return train_enc, test_enc

train_fe, test_fe = frequency_encode(train, test, 'category')
print(f"  Frequency encoding:\n{train_fe[['category','category_freq']].drop_duplicates().sort_values('category')}")


# =====================================================================
#   PARTE 19: WOE / IV
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: WOE ENCODING ===")
print("=" * 80)

"""
Weight of Evidence (WOE): encoding basado en target.
IV (Information Value): mide poder predictivo de una feature.

WOE_i = ln(Distribution_Good_i / Distribution_Bad_i)
IV = Σ (Dist_Good_i - Dist_Bad_i) * WOE_i
"""

print("\n--- WOE encoding ---")

def woe_encode(df, feature, target, eps=1e-4):
    """Calcular WOE e IV."""
    total_good = (df[target] == 0).sum()
    total_bad = (df[target] == 1).sum()
    
    groups = df.groupby(feature)[target].agg(['sum', 'count'])
    groups.columns = ['bad', 'total']
    groups['good'] = groups['total'] - groups['bad']
    
    groups['dist_good'] = groups['good'] / total_good
    groups['dist_bad'] = groups['bad'] / total_bad
    
    groups['woe'] = np.log((groups['dist_good'] + eps) / (groups['dist_bad'] + eps))
    groups['iv'] = (groups['dist_good'] - groups['dist_bad']) * groups['woe']
    
    iv = groups['iv'].sum()
    
    return groups[['woe', 'iv']], iv

woe_result, iv = woe_encode(df_sample, 'category', 'target')
print(f"  WOE by category:\n{woe_result.round(4)}")
print(f"  Information Value: {iv:.4f}")
print(f"  IV interpretation: {'Weak' if iv < 0.1 else 'Medium' if iv < 0.3 else 'Strong'}")


# =====================================================================
#   PARTE 20: FEATURE IMPORTANCE (PERMUTATION)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: FEATURE IMPORTANCE ===")
print("=" * 80)

"""
Permutation importance: medir importancia permutando features.
Sin necesidad de modelo complejo.
"""

print("\n--- Correlation-based importance ---")

numeric_features = df_sample.select_dtypes(include=[np.number]).columns.drop('target')
correlations = df_sample[numeric_features].corrwith(df_sample['target']).abs().sort_values(ascending=False)

print(f"  Feature importance (|correlation with target|):")
for feat, corr in correlations.items():
    bar = "█" * int(corr * 50)
    print(f"    {feat:<15s}: {corr:.4f} {bar}")


# =====================================================================
#   PARTE 21: DATA DRIFT DETECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: DATA DRIFT ===")
print("=" * 80)

"""
Detectar si la distribucion de datos cambia entre train y test.
"""

print("\n--- Distribution comparison ---")

def detect_drift(train_series, test_series, threshold=0.1):
    """Detectar drift comparando estadisticas."""
    train_mean = train_series.mean()
    test_mean = test_series.mean()
    train_std = train_series.std()
    test_std = test_series.std()
    
    # PSI (Population Stability Index) simplificado
    mean_shift = abs(train_mean - test_mean) / (train_std + 1e-8)
    std_ratio = max(train_std, test_std) / (min(train_std, test_std) + 1e-8)
    
    drift = mean_shift > threshold or std_ratio > 1.5
    
    return {
        'train_mean': train_mean,
        'test_mean': test_mean,
        'mean_shift': mean_shift,
        'std_ratio': std_ratio,
        'drift': drift,
    }

for col in feature_cols:
    result = detect_drift(train[col], test[col])
    status = "⚠ DRIFT" if result['drift'] else "✓ OK"
    print(f"  {col:<15s}: shift={result['mean_shift']:.4f}, ratio={result['std_ratio']:.3f} {status}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE PIPELINE DE DATOS PARA ML:

1. Parquet >> CSV para produccion.
2. Siempre hacer data profiling antes de modelar.
3. Pipeline de limpieza: strip, normalize, validate, impute.
4. Features: datetime cyclical, interactions, aggregations.
5. Split: random, stratified, o temporal.
6. Validation: schema checks automaticos.
7. Imbalanced: under/oversample, class weights.
8. Scaling: fit en train, transform en test.
9. NUNCA data leakage. NUNCA iterrows.
10. Prefer list comprehension + concat sobre append.

FIN DEL MODULO 11: PANDAS INGENIERIA.
"""

print("\n FIN DE ARCHIVO 03_pipeline_datos_ml.")
print(" Pipeline de datos para ML ha sido dominado.")
print(" Siguiente modulo: SQL Y VISUALIZACION.")
