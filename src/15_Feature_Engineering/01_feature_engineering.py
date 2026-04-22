# ===========================================================================
# 01_feature_engineering.py
# ===========================================================================
# MODULO 15: FEATURE ENGINEERING
# ARCHIVO 01: Transformacion, Creacion, y Encoding de Features
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar feature engineering: transformaciones, encoding,
# creacion de features, interacciones, y feature stores.
#
# CONTENIDO:
#   1. Numeric transformations (log, sqrt, box-cox, yeo-johnson).
#   2. Binning / Discretization.
#   3. Polynomial features.
#   4. Date/time features.
#   5. Text features (bag of words, TF-IDF).
#   6. Categorical encoding avanzado.
#   7. Target encoding.
#   8. Frequency encoding.
#   9. Feature hashing.
#   10. Interaction features.
#   11. Domain-specific features.
#   12. Missing value features.
#   13. Aggregation features.
#   14. Lag features (time series).
#   15. Feature generation pipeline.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import warnings
warnings.filterwarnings('ignore')

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    from sklearn.preprocessing import (
        StandardScaler, MinMaxScaler, PolynomialFeatures,
        KBinsDiscretizer, OneHotEncoder, OrdinalEncoder,
        PowerTransformer, FunctionTransformer,
    )
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.datasets import make_classification
    from sklearn.metrics import accuracy_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# =====================================================================
#   PARTE 1: NUMERIC TRANSFORMATIONS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: NUMERIC TRANSFORMS ===")
print("=" * 80)

"""
Transformaciones numericas:
1. Log: log(x+1), reduce skewness positiva.
2. Sqrt: suaviza valores grandes.
3. Box-Cox: familia parametrica, requiere x > 0.
4. Yeo-Johnson: extension de Box-Cox, permite negativos.
5. Reciprocal: 1/x.
6. Square: x^2, amplifica diferencias.

REGLA: aplicar DESPUES de split, ANTES de scaling.
"""

np.random.seed(42)
# Skewed data
x_skewed = np.random.lognormal(2, 1, 1000)

transforms = {
    'original': x_skewed,
    'log1p': np.log1p(x_skewed),
    'sqrt': np.sqrt(x_skewed),
    'reciprocal': 1.0 / (x_skewed + 1),
}

print(f"\n  {'Transform':>12s} {'Mean':>8s} {'Std':>8s} {'Skew':>8s}")
for name, data in transforms.items():
    from scipy.stats import skew as calc_skew
    sk = calc_skew(data)
    print(f"  {name:>12s} {data.mean():8.2f} {data.std():8.2f} {sk:8.2f}")

if HAS_SKLEARN:
    print("\n--- PowerTransformer ---")
    
    pt_yj = PowerTransformer(method='yeo-johnson')
    pt_bc = PowerTransformer(method='box-cox')
    
    x_yj = pt_yj.fit_transform(x_skewed.reshape(-1, 1))
    x_bc = pt_bc.fit_transform(x_skewed.reshape(-1, 1))
    
    print(f"  Yeo-Johnson lambda: {pt_yj.lambdas_[0]:.4f}")
    print(f"  Box-Cox lambda:     {pt_bc.lambdas_[0]:.4f}")
    print(f"  YJ skew:  {calc_skew(x_yj.flatten()):.4f}")
    print(f"  BC skew:  {calc_skew(x_bc.flatten()):.4f}")


# =====================================================================
#   PARTE 2: BINNING / DISCRETIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: BINNING ===")
print("=" * 80)

"""
Binning: convertir continuo a categorico.
Estrategias:
1. Uniform: bins de igual ancho.
2. Quantile: bins con igual cantidad de puntos.
3. K-Means: bins basados en clustering.
4. Custom: basado en dominio.
"""

if HAS_SKLEARN:
    print("\n--- KBinsDiscretizer ---")
    
    age = np.random.randint(18, 80, 500).reshape(-1, 1).astype(float)
    
    for strategy in ['uniform', 'quantile', 'kmeans']:
        kbd = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy=strategy)
        binned = kbd.fit_transform(age)
        edges = kbd.bin_edges_[0]
        print(f"  {strategy:>8s}: edges={edges.round(1)}")
    
    
    print("\n--- Custom binning ---")
    
    def custom_age_bins(age):
        """Domain-specific age binning."""
        bins = np.zeros_like(age)
        bins[age < 25] = 0    # Young
        bins[(age >= 25) & (age < 35)] = 1  # Young adult
        bins[(age >= 35) & (age < 50)] = 2  # Adult
        bins[(age >= 50) & (age < 65)] = 3  # Senior
        bins[age >= 65] = 4   # Elderly
        return bins
    
    binned_custom = custom_age_bins(age.flatten())
    from collections import Counter
    print(f"  Custom bins: {dict(Counter(binned_custom.astype(int)))}")


# =====================================================================
#   PARTE 3: POLYNOMIAL FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: POLYNOMIAL ===")
print("=" * 80)

if HAS_SKLEARN:
    X_poly = np.random.randn(100, 3)
    
    for degree in [2, 3]:
        for interaction in [False, True]:
            pf = PolynomialFeatures(degree=degree, interaction_only=interaction, include_bias=False)
            X_expanded = pf.fit_transform(X_poly)
            names = pf.get_feature_names_out()
            print(f"  degree={degree}, interaction_only={interaction}: "
                  f"{X_poly.shape[1]} -> {X_expanded.shape[1]} features")
    
    print(f"\n  Feature names (degree=2): {list(names[:10])}...")


# =====================================================================
#   PARTE 4: DATE/TIME FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: DATE/TIME ===")
print("=" * 80)

"""
Date features:
  - year, month, day, day_of_week, hour, minute
  - is_weekend, is_holiday
  - quarter, week_of_year
  - sin/cos encoding para ciclicidad
  - days_since_event
  - time_to_event
"""

if HAS_PANDAS:
    dates = pd.date_range('2024-01-01', periods=365, freq='D')
    df_dates = pd.DataFrame({'date': dates})
    
    # Extract features
    df_dates['year'] = df_dates['date'].dt.year
    df_dates['month'] = df_dates['date'].dt.month
    df_dates['day'] = df_dates['date'].dt.day
    df_dates['day_of_week'] = df_dates['date'].dt.dayofweek
    df_dates['is_weekend'] = df_dates['day_of_week'].isin([5, 6]).astype(int)
    df_dates['quarter'] = df_dates['date'].dt.quarter
    df_dates['week'] = df_dates['date'].dt.isocalendar().week.astype(int)
    df_dates['day_of_year'] = df_dates['date'].dt.dayofyear
    
    # Cyclical encoding
    df_dates['month_sin'] = np.sin(2 * np.pi * df_dates['month'] / 12)
    df_dates['month_cos'] = np.cos(2 * np.pi * df_dates['month'] / 12)
    df_dates['dow_sin'] = np.sin(2 * np.pi * df_dates['day_of_week'] / 7)
    df_dates['dow_cos'] = np.cos(2 * np.pi * df_dates['day_of_week'] / 7)
    
    print(f"  Date features: {df_dates.shape[1] - 1} features from 1 date column")
    print(f"  Columns: {list(df_dates.columns[1:])}")
    print(f"\n  Cyclical encoding preserves proximity:")
    print(f"    Dec sin: {np.sin(2*np.pi*12/12):.3f}, Jan sin: {np.sin(2*np.pi*1/12):.3f}")
    print(f"    This shows Dec and Jan are close (unlike ordinal 12 vs 1)")


# =====================================================================
#   PARTE 5: TEXT FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: TEXT FEATURES ===")
print("=" * 80)

"""
Text feature engineering:
1. Bag of Words (CountVectorizer).
2. TF-IDF (TfidfVectorizer).
3. N-grams.
4. Text statistics: length, word_count, avg_word_length.
5. Sentiment (conceptual).
"""

if HAS_SKLEARN:
    texts = [
        "machine learning is great for prediction",
        "deep learning uses neural networks",
        "random forest is a ensemble method",
        "gradient boosting wins competitions",
        "neural networks need lots of data",
        "sklearn makes machine learning easy",
    ]
    
    # Count Vectorizer
    cv = CountVectorizer()
    X_bow = cv.fit_transform(texts)
    print(f"  BoW: {X_bow.shape} (docs x vocab)")
    print(f"  Vocab: {list(cv.vocabulary_.keys())[:10]}...")
    
    # TF-IDF
    tfidf = TfidfVectorizer(max_features=20, ngram_range=(1, 2))
    X_tfidf = tfidf.fit_transform(texts)
    print(f"  TF-IDF: {X_tfidf.shape}")
    
    # Text statistics
    print(f"\n  Text statistics:")
    for text in texts[:3]:
        words = text.split()
        print(f"    len={len(text):3d}, words={len(words)}, avg_word={np.mean([len(w) for w in words]):.1f}")


# =====================================================================
#   PARTE 6: CATEGORICAL ENCODING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: CATEGORICAL ENCODING ===")
print("=" * 80)

"""
Encoding strategies:
1. OneHot: nominal, low cardinality (< 15 categories).
2. Ordinal: ordinal (size: S < M < L < XL).
3. Label: binary target.
4. Target: mean of target per category.
5. Frequency: count of category / total.
6. Binary: binary representation.
7. Hash: feature hashing.
8. WOE: Weight of Evidence (credit scoring).
"""

if HAS_PANDAS and HAS_SKLEARN:
    np.random.seed(42)
    n = 500
    df_enc = pd.DataFrame({
        'city': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao'], n),
        'education': np.random.choice(['HS', 'BS', 'MS', 'PhD'], n),
        'target': np.random.binomial(1, 0.3, n),
    })
    
    print(f"\n--- OneHot ---")
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_ohe = ohe.fit_transform(df_enc[['city']])
    print(f"  city (5 cats) -> {X_ohe.shape[1]} features")
    
    print(f"\n--- Ordinal ---")
    oe = OrdinalEncoder(categories=[['HS', 'BS', 'MS', 'PhD']])
    X_ord = oe.fit_transform(df_enc[['education']])
    print(f"  education -> {np.unique(X_ord.flatten())}")
    
    print(f"\n--- Frequency encoding ---")
    freq = df_enc['city'].value_counts(normalize=True).to_dict()
    df_enc['city_freq'] = df_enc['city'].map(freq)
    print(f"  Frequencies: {freq}")


# =====================================================================
#   PARTE 7: TARGET ENCODING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: TARGET ENCODING ===")
print("=" * 80)

"""
Target encoding: reemplazar categoria con mean(target|category).
PELIGRO: data leakage.
SOLUCION: calcular en K folds de CV.
"""

if HAS_PANDAS:
    def target_encode_cv(df, col, target, n_folds=5):
        """Target encoding with CV to prevent leakage."""
        encoded = pd.Series(np.nan, index=df.index)
        global_mean = df[target].mean()
        
        from sklearn.model_selection import KFold
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
        
        for train_idx, val_idx in kf.split(df):
            means = df.iloc[train_idx].groupby(col)[target].mean()
            encoded.iloc[val_idx] = df.iloc[val_idx][col].map(means)
        
        # Fill NaN with global mean
        encoded.fillna(global_mean, inplace=True)
        return encoded
    
    df_enc['city_target'] = target_encode_cv(df_enc, 'city', 'target')
    print(f"  Target encoded (city):")
    for city in df_enc['city'].unique():
        te_val = df_enc[df_enc['city'] == city]['city_target'].mean()
        actual = df_enc[df_enc['city'] == city]['target'].mean()
        print(f"    {city:>12s}: te={te_val:.4f}, actual={actual:.4f}")


# =====================================================================
#   PARTE 8: MISSING VALUE FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: MISSING VALUE FEATURES ===")
print("=" * 80)

"""
Missing values pueden ser informativas:
1. is_missing: flag binario.
2. n_missing: count de NaN por fila.
3. missing_pattern: combinacion de columnas missing.
"""

if HAS_PANDAS:
    np.random.seed(42)
    df_miss = pd.DataFrame({
        'age': np.where(np.random.random(200) > 0.1, np.random.randint(18, 80, 200), np.nan),
        'income': np.where(np.random.random(200) > 0.2, np.random.lognormal(10, 1, 200), np.nan),
        'score': np.where(np.random.random(200) > 0.05, np.random.randn(200), np.nan),
    })
    
    # Missing indicators
    for col in df_miss.columns:
        df_miss[f'{col}_missing'] = df_miss[col].isna().astype(int)
    
    # Count missing per row
    df_miss['n_missing'] = df_miss[['age', 'income', 'score']].isna().sum(axis=1)
    
    print(f"  Missing rates:")
    for col in ['age', 'income', 'score']:
        rate = df_miss[col].isna().mean()
        print(f"    {col}: {rate:.2%}")
    print(f"  n_missing distribution: {dict(Counter(df_miss['n_missing']))}")
    
    from collections import Counter


# =====================================================================
#   PARTE 9: AGGREGATION FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: AGGREGATION ===")
print("=" * 80)

"""
Group-level features:
  Per-group statistics joined back to row level.
  
  Ejemplo: para cada customer, calcular:
  - mean_purchase, max_purchase, count_purchases
  - std_purchase, median_purchase
"""

if HAS_PANDAS:
    np.random.seed(42)
    df_agg = pd.DataFrame({
        'customer_id': np.random.choice(['A', 'B', 'C', 'D', 'E'], 200),
        'amount': np.random.lognormal(3, 1, 200),
        'category': np.random.choice(['food', 'tech', 'clothes'], 200),
    })
    
    # Customer-level aggregations
    agg_features = df_agg.groupby('customer_id')['amount'].agg(
        ['mean', 'std', 'min', 'max', 'count', 'median']
    ).add_prefix('customer_amount_')
    
    df_agg = df_agg.merge(agg_features, left_on='customer_id', right_index=True)
    
    # Relative features
    df_agg['amount_vs_customer_mean'] = df_agg['amount'] / df_agg['customer_amount_mean']
    df_agg['amount_zscore'] = (
        (df_agg['amount'] - df_agg['customer_amount_mean']) / 
        (df_agg['customer_amount_std'] + 1e-10)
    )
    
    print(f"  Original: {3} features")
    print(f"  After agg: {df_agg.shape[1]} features")
    print(f"  New features: {[c for c in df_agg.columns if 'customer_' in c or 'vs_' in c or 'zscore' in c]}")


# =====================================================================
#   PARTE 10: LAG FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: LAG FEATURES ===")
print("=" * 80)

"""
Time series features:
1. Lag: valor en t-1, t-2, ...
2. Rolling: mean/std de ventana.
3. Expanding: mean acumulativa.
4. Diff: cambio vs periodo anterior.
5. Ratio: ratio vs periodo anterior.
"""

if HAS_PANDAS:
    np.random.seed(42)
    ts = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'value': np.cumsum(np.random.randn(100)) + 50,
    })
    
    # Lags
    for lag in [1, 3, 7]:
        ts[f'lag_{lag}'] = ts['value'].shift(lag)
    
    # Rolling
    for window in [3, 7, 14]:
        ts[f'rolling_mean_{window}'] = ts['value'].rolling(window).mean()
        ts[f'rolling_std_{window}'] = ts['value'].rolling(window).std()
    
    # Expanding
    ts['expanding_mean'] = ts['value'].expanding().mean()
    
    # Diff & ratio
    ts['diff_1'] = ts['value'].diff(1)
    ts['ratio_1'] = ts['value'] / ts['value'].shift(1)
    
    ts_features = [c for c in ts.columns if c not in ['date', 'value']]
    print(f"  Generated {len(ts_features)} time features from 1 column:")
    for f in ts_features:
        print(f"    - {f}")


# =====================================================================
#   PARTE 11: INTERACTION FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: INTERACTIONS ===")
print("=" * 80)

"""
Feature interactions:
  - Multiplicacion: x1 * x2
  - Division: x1 / x2 (ratios)
  - Sum: x1 + x2
  - Differencia: x1 - x2
  - Interaction con domain knowledge

BMI = weight / height^2
Price per sqft = price / sqft
Income ratio = income / expenses
"""

np.random.seed(42)
n_int = 200
height = np.random.normal(170, 10, n_int)
weight = np.random.normal(70, 15, n_int)
income = np.random.lognormal(10, 0.5, n_int)
expenses = income * np.random.uniform(0.5, 0.9, n_int)

# Domain features
bmi = weight / (height / 100) ** 2
savings_rate = (income - expenses) / income
log_income = np.log1p(income)
income_per_kg = income / weight

print(f"  Domain features:")
print(f"    BMI: mean={bmi.mean():.1f}, std={bmi.std():.1f}")
print(f"    Savings rate: mean={savings_rate.mean():.3f}")
print(f"    Log income: mean={log_income.mean():.2f}")


# =====================================================================
#   PARTE 12: FEATURE HASHING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: FEATURE HASHING ===")
print("=" * 80)

"""
Feature hashing (hashing trick):
  Map high-cardinality categoricals to fixed-size vector.
  No need to maintain vocabulary.
  Collisions are acceptable with enough dimensions.
"""

def simple_hash_encode(values, n_features=16):
    """Simple feature hashing."""
    result = np.zeros((len(values), n_features))
    for i, val in enumerate(values):
        h = hash(str(val)) % n_features
        result[i, h] = 1
    return result

categories = ['cat_' + str(i) for i in range(100)]
selected = np.random.choice(categories, 500)
hashed = simple_hash_encode(selected, n_features=32)

print(f"  100 categories -> {hashed.shape[1]} hashed features")
print(f"  Sparsity: {(hashed == 0).mean():.2%}")


# =====================================================================
#   PARTE 13: FEATURE GENERATION PIPELINE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: GENERATION PIPELINE ===")
print("=" * 80)

"""
Automated feature generation:
1. Apply transforms to all numeric features.
2. Create pairwise interactions.
3. Create aggregations.
4. Select best features.
"""

if HAS_SKLEARN:
    X_gen, y_gen = make_classification(
        n_samples=500, n_features=5, n_informative=3,
        random_state=42
    )
    
    # Manual feature expansion
    X_expanded = np.column_stack([
        X_gen,
        X_gen ** 2,
        np.log1p(np.abs(X_gen)),
        X_gen[:, 0:1] * X_gen[:, 1:2],
        X_gen[:, 0:1] * X_gen[:, 2:3],
        X_gen[:, 1:2] * X_gen[:, 2:3],
    ])
    
    X_tr, X_te, y_tr, y_te = train_test_split(X_expanded, y_gen, test_size=0.2, random_state=42)
    
    # Compare
    lr_orig = LogisticRegression(max_iter=1000, random_state=42)
    lr_orig.fit(X_gen[:400], y_gen[:400])
    score_orig = lr_orig.score(X_gen[400:], y_gen[400:])
    
    lr_exp = LogisticRegression(max_iter=1000, random_state=42)
    lr_exp.fit(X_tr, y_tr)
    score_exp = lr_exp.score(X_te, y_te)
    
    print(f"  Original ({X_gen.shape[1]} feats): {score_orig:.4f}")
    print(f"  Expanded ({X_expanded.shape[1]} feats): {score_exp:.4f}")


# =====================================================================
#   PARTE 14: FEATURE STORE PATTERN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: FEATURE STORE ===")
print("=" * 80)

"""
Feature Store: repositorio centralizado de features.

Componentes:
1. Feature definitions (transformaciones).
2. Feature computation (batch/streaming).
3. Feature serving (online/offline).
4. Feature registry (metadata, lineage).

Herramientas: Feast, Tecton, Hopsworks.

PATRON:
  features = feature_store.get_features(
      entity_id='customer_123',
      feature_names=['avg_purchase', 'n_transactions', 'days_since_last']
  )
"""

class SimpleFeatureStore:
    """In-memory feature store pattern."""
    
    def __init__(self):
        self.features = {}
        self.metadata = {}
    
    def register(self, name, compute_fn, description=""):
        self.features[name] = compute_fn
        self.metadata[name] = {'description': description}
    
    def compute(self, name, data):
        return self.features[name](data)
    
    def compute_all(self, data):
        result = {}
        for name, fn in self.features.items():
            result[name] = fn(data)
        return result

store = SimpleFeatureStore()
store.register('log_income', lambda d: np.log1p(d.get('income', 0)), 'Log-transformed income')
store.register('bmi', lambda d: d.get('weight', 70) / (d.get('height', 170) / 100)**2, 'Body Mass Index')

sample = {'income': 50000, 'weight': 75, 'height': 175}
features = store.compute_all(sample)
print(f"  Feature store output: {features}")


# =====================================================================
#   PARTE 15: FEATURE IMPORTANCE ANALYSIS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: IMPORTANCE ANALYSIS ===")
print("=" * 80)

if HAS_SKLEARN:
    X_imp, y_imp = make_classification(
        n_samples=500, n_features=20, n_informative=8,
        n_redundant=5, random_state=42
    )
    
    # RF importance
    rf_imp = RandomForestClassifier(100, random_state=42, n_jobs=-1)
    rf_imp.fit(X_imp, y_imp)
    
    importances = rf_imp.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    
    print(f"  Feature importance (RF):")
    cumulative = 0
    for i in range(min(10, len(sorted_idx))):
        idx = sorted_idx[i]
        cumulative += importances[idx]
        bar = "█" * int(importances[idx] * 100)
        print(f"    F{idx:2d}: {importances[idx]:.4f} (cum: {cumulative:.4f}) {bar}")
    
    # Find redundant features
    corr_matrix = np.corrcoef(X_imp, rowvar=False)
    high_corr = []
    for i in range(20):
        for j in range(i+1, 20):
            if abs(corr_matrix[i, j]) > 0.8:
                high_corr.append((i, j, corr_matrix[i, j]))
    
    print(f"\n  High correlation pairs (|r| > 0.8): {len(high_corr)}")
    for i, j, r in high_corr[:5]:
        print(f"    F{i} - F{j}: r={r:.3f}")


# =====================================================================
#   PARTE 16: WOE ENCODING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: WOE ENCODING ===")
print("=" * 80)

"""
Weight of Evidence (WOE):
  WOE = ln(% events / % non-events)
  
  Used in credit scoring.
  Related to Information Value (IV):
    IV = sum((% events - % non-events) * WOE)
    IV < 0.02: useless
    IV 0.02-0.1: weak
    IV 0.1-0.3: medium
    IV > 0.3: strong
"""

if HAS_PANDAS:
    def woe_encode(df, feature, target):
        """Calculate WOE for a categorical feature."""
        total_events = df[target].sum()
        total_non_events = len(df) - total_events
        
        woe_dict = {}
        iv = 0
        
        for cat in df[feature].unique():
            mask = df[feature] == cat
            events = df.loc[mask, target].sum()
            non_events = mask.sum() - events
            
            pct_events = (events + 0.5) / (total_events + 1)
            pct_non_events = (non_events + 0.5) / (total_non_events + 1)
            
            woe = np.log(pct_events / pct_non_events)
            woe_dict[cat] = woe
            iv += (pct_events - pct_non_events) * woe
        
        return woe_dict, iv
    
    woe_city, iv_city = woe_encode(df_enc, 'city', 'target')
    print(f"  WOE encoding:")
    for city, woe in woe_city.items():
        print(f"    {city:>12s}: WOE={woe:.4f}")
    print(f"  IV(city): {iv_city:.4f}")


# =====================================================================
#   PARTE 17: RANK FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: RANK FEATURES ===")
print("=" * 80)

"""
Rank transform: reemplazar valor con su rank (posicion en el ordenamiento).
Ventajas:
  - Robusto a outliers.
  - Distribucion uniforme.
  - Preserva orden.
"""

np.random.seed(42)
x_outlier = np.concatenate([np.random.randn(95), [100, 200, -50, -100, 500]])

from scipy.stats import rankdata
x_ranked = rankdata(x_outlier) / len(x_outlier)  # Normalize to [0, 1]

print(f"  Original: mean={x_outlier.mean():.1f}, std={x_outlier.std():.1f}")
print(f"  Ranked:   mean={x_ranked.mean():.3f}, std={x_ranked.std():.3f}")
print(f"  Max outlier {x_outlier.max():.0f} -> rank {x_ranked[np.argmax(x_outlier)]:.3f}")


# =====================================================================
#   PARTE 18: COUNT ENCODING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: COUNT ENCODING ===")
print("=" * 80)

if HAS_PANDAS:
    count_map = df_enc['city'].value_counts().to_dict()
    df_enc['city_count'] = df_enc['city'].map(count_map)
    
    print(f"  Count encoding:")
    for city, count in sorted(count_map.items()):
        print(f"    {city:>12s}: count={count}")


# =====================================================================
#   PARTE 19: WINDOW FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: WINDOW FEATURES ===")
print("=" * 80)

if HAS_PANDAS:
    np.random.seed(42)
    ts2 = pd.DataFrame({
        'value': np.cumsum(np.random.randn(200)) + 100,
    })
    
    # EWM (Exponential Weighted Mean)
    for span in [5, 10, 20]:
        ts2[f'ewm_{span}'] = ts2['value'].ewm(span=span).mean()
    
    # Bollinger bands
    ts2['bb_mid'] = ts2['value'].rolling(20).mean()
    ts2['bb_std'] = ts2['value'].rolling(20).std()
    ts2['bb_upper'] = ts2['bb_mid'] + 2 * ts2['bb_std']
    ts2['bb_lower'] = ts2['bb_mid'] - 2 * ts2['bb_std']
    ts2['bb_width'] = ts2['bb_upper'] - ts2['bb_lower']
    ts2['bb_position'] = (ts2['value'] - ts2['bb_lower']) / (ts2['bb_width'] + 1e-10)
    
    # Momentum
    ts2['momentum_5'] = ts2['value'] - ts2['value'].shift(5)
    ts2['pct_change_5'] = ts2['value'].pct_change(5)
    
    feat_names = [c for c in ts2.columns if c != 'value']
    print(f"  Window features ({len(feat_names)}):")
    for f in feat_names:
        print(f"    - {f}")


# =====================================================================
#   PARTE 20: OUTLIER-BASED FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: OUTLIER FEATURES ===")
print("=" * 80)

"""
Outlier indicators as features:
  - is_outlier_iqr: beyond IQR * 1.5
  - z_score: distance from mean in std units
  - is_extreme: beyond 3 std
"""

np.random.seed(42)
data_out = np.random.randn(500)

q1, q3 = np.percentile(data_out, [25, 75])
iqr = q3 - q1
is_outlier = ((data_out < q1 - 1.5*iqr) | (data_out > q3 + 1.5*iqr)).astype(int)
z_score = (data_out - data_out.mean()) / data_out.std()
is_extreme = (np.abs(z_score) > 3).astype(int)

print(f"  IQR outliers: {is_outlier.sum()}/500")
print(f"  Extreme (3σ): {is_extreme.sum()}/500")
print(f"  Z-score range: [{z_score.min():.2f}, {z_score.max():.2f}]")


# =====================================================================
#   PARTE 21: EMBEDDING CONCEPT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: EMBEDDINGS ===")
print("=" * 80)

"""
Entity embeddings (from deep learning):
  Map categorical variable to dense vector.
  
  city: 'Madrid' -> [0.1, -0.3, 0.8, ...]
  
  Ventajas sobre OneHot:
  - Dimensionalidad fija (independiente de cardinality).
  - Captures similarity between categories.
  - Learned representation.
  
  Implementacion: nn.Embedding en PyTorch/Keras.
"""

print("  Embedding concept:")
print("    OneHot: 'Madrid' -> [1, 0, 0, 0, 0]  (sparse, 5D)")
print("    Embed:  'Madrid' -> [0.1, -0.3, 0.8]  (dense, 3D)")
print("    Rule: embedding_dim ≈ min(50, cardinality // 2)")


# =====================================================================
#   PARTE 22: FEATURE CROSSES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 22: FEATURE CROSSES ===")
print("=" * 80)

"""
Feature crosses: combine categoricals.
  city + education -> 'Madrid_PhD', 'Barcelona_BS'
  Captures interactions that individual features miss.
"""

if HAS_PANDAS:
    df_enc['city_edu'] = df_enc['city'] + '_' + df_enc['education']
    n_combos = df_enc['city_edu'].nunique()
    print(f"  city (5) x education (4) = {n_combos} crosses")
    print(f"  Top 5 crosses:")
    for cross, count in df_enc['city_edu'].value_counts().head(5).items():
        print(f"    {cross:>20s}: {count}")


# =====================================================================
#   PARTE 23: SEASONAL DECOMPOSITION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 23: SEASONAL ===")
print("=" * 80)

"""
Seasonal features for time series:
  - Trend component.
  - Seasonal component.
  - Residual.
  
  statsmodels.tsa.seasonal.seasonal_decompose
"""

if HAS_PANDAS:
    np.random.seed(42)
    t = np.arange(365)
    trend = t * 0.05
    seasonal = 10 * np.sin(2 * np.pi * t / 365)
    noise = np.random.randn(365) * 2
    ts_seasonal = trend + seasonal + noise + 50
    
    # Manual decomposition
    ts_trend = pd.Series(ts_seasonal).rolling(30, center=True).mean()
    ts_detrended = ts_seasonal - ts_trend.values
    
    print(f"  Original: mean={ts_seasonal.mean():.1f}, std={ts_seasonal.std():.1f}")
    print(f"  Trend: mean={np.nanmean(ts_trend):.1f}")
    print(f"  Detrended: mean={np.nanmean(ts_detrended):.1f}")


# =====================================================================
#   PARTE 24: FEATURE COMPARISON
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 24: COMPARISON ===")
print("=" * 80)

if HAS_SKLEARN:
    X_cmp, y_cmp = make_classification(
        n_samples=500, n_features=10, n_informative=5,
        n_redundant=3, random_state=42
    )
    X_cmp_tr, X_cmp_te, y_cmp_tr, y_cmp_te = train_test_split(
        X_cmp, y_cmp, test_size=0.2, random_state=42
    )
    
    # Different FE strategies
    strategies = {
        'Raw': X_cmp_tr,
        'Scaled': StandardScaler().fit_transform(X_cmp_tr),
        'Log+Scale': StandardScaler().fit_transform(np.log1p(np.abs(X_cmp_tr))),
        'Poly2': PolynomialFeatures(2, include_bias=False).fit_transform(X_cmp_tr[:, :5]),
    }
    
    print(f"  {'Strategy':>12s} {'Features':>10s} {'CV Score':>10s}")
    for name, X_s in strategies.items():
        lr = LogisticRegression(max_iter=1000, random_state=42)
        try:
            scores = cross_val_score(lr, X_s, y_cmp_tr, cv=3)
            print(f"  {name:>12s} {X_s.shape[1]:10d} {scores.mean():10.4f}")
        except Exception:
            print(f"  {name:>12s} {X_s.shape[1]:10d} {'error':>10s}")


# =====================================================================
#   PARTE 25: ENCODING CHEATSHEET
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 25: CHEATSHEET ===")
print("=" * 80)

encoding_guide = [
    ("Numeric continuous", "StandardScaler / log / Box-Cox"),
    ("Numeric skewed", "log1p / Yeo-Johnson"),
    ("Nominal (low card)", "OneHotEncoder"),
    ("Nominal (high card)", "Target / Frequency / Hash"),
    ("Ordinal", "OrdinalEncoder"),
    ("Date", "Extract + cyclical sin/cos"),
    ("Text", "TF-IDF / Count / embeddings"),
    ("Missing", "Indicator + impute"),
    ("Time series", "Lags + rolling + diff"),
]

print(f"\n  {'Feature Type':>22s} {'Encoding':>35s}")
for ftype, enc in encoding_guide:
    print(f"  {ftype:>22s} {enc:>35s}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN FEATURE ENGINEERING:

1. Transforms: log, sqrt, Box-Cox, Yeo-Johnson.
2. Binning: uniform, quantile, kmeans, custom.
3. Polynomial: degree, interaction_only.
4. Date/Time: extract + cyclical encoding.
5. Text: BoW, TF-IDF, n-grams, statistics.
6. Categorical: OneHot, Ordinal, Target, Frequency.
7. Missing: indicators + count.
8. Aggregation: group-level statistics.
9. Lag: time series features.
10. Interactions: domain-specific ratios.

FIN DEL ARCHIVO 01.
"""

print("\n FIN DE ARCHIVO 01_feature_engineering.")
print(" Feature engineering ha sido dominado.")
