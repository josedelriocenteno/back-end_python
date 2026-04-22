# ===========================================================================
# 02_feature_selection_pipelines.py
# ===========================================================================
# MODULO 15: FEATURE ENGINEERING
# ARCHIVO 02: Feature Selection y Pipelines de Feature Engineering
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar feature selection avanzada, pipelines de FE,
# automated feature engineering, y patrones de produccion.
#
# CONTENIDO:
#   1. Variance Threshold.
#   2. Univariate selection.
#   3. Recursive Feature Elimination.
#   4. L1-based selection.
#   5. Tree-based selection.
#   6. Boruta algorithm concept.
#   7. Mutual Information.
#   8. Feature clustering.
#   9. Automated FE (featuretools concept).
#   10. FE for different model types.
#   11. Data leakage patterns.
#   12. Production FE patterns.
#   13. Feature validation.
#   14. FE best practices.
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
    from sklearn.feature_selection import (
        VarianceThreshold, SelectKBest, f_classif,
        mutual_info_classif, RFE, RFECV, SelectFromModel,
    )
    from sklearn.preprocessing import StandardScaler, PolynomialFeatures
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.linear_model import LogisticRegression, Lasso
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.datasets import make_classification
    from sklearn.metrics import accuracy_score
    from sklearn.base import BaseEstimator, TransformerMixin
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# =====================================================================
#   PARTE 1: VARIANCE THRESHOLD
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: VARIANCE THRESHOLD ===")
print("=" * 80)

"""
Variance Threshold: eliminar features con varianza < threshold.
  - threshold=0: eliminar constantes.
  - threshold>0: eliminar near-constants.

Para features binarias: Var[X] = p(1-p)
  threshold=0.8*(1-0.8) = 0.16 elimina features con >80% un valor.
"""

if HAS_SKLEARN:
    np.random.seed(42)
    X, y = make_classification(
        n_samples=1000, n_features=20, n_informative=10,
        n_redundant=5, random_state=42
    )
    # Add constant and near-constant features
    X_aug = np.column_stack([
        X,
        np.ones(1000),                              # constant
        np.full(1000, 3.14),                         # constant
        np.random.choice([0, 1], 1000, p=[0.99, 0.01]),  # near-constant
        np.random.choice([0, 1], 1000, p=[0.95, 0.05]),  # low-var
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_aug, y, test_size=0.2, random_state=42
    )
    
    print(f"\n  Original: {X_aug.shape[1]} features")
    
    for thresh in [0.0, 0.01, 0.05, 0.1]:
        vt = VarianceThreshold(threshold=thresh)
        X_filtered = vt.fit_transform(X_aug)
        n_removed = X_aug.shape[1] - X_filtered.shape[1]
        print(f"  threshold={thresh:.2f}: {X_filtered.shape[1]} features ({n_removed} removed)")


# =====================================================================
#   PARTE 2: UNIVARIATE SELECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: UNIVARIATE ===")
print("=" * 80)

"""
Evaluar cada feature INDEPENDIENTEMENTE.
Metodos:
  - f_classif: ANOVA F-statistic (clasificacion).
  - chi2: chi-squared (features positivas).
  - f_regression: F-statistic (regresion).
  - mutual_info_classif: Mutual Information.

SelectKBest: seleccionar top-k features.
SelectPercentile: seleccionar top-p% features.
"""

if HAS_SKLEARN:
    print("\n--- ANOVA F-test ---")
    
    f_scores = f_classif(X_train[:, :20], y_train)
    
    ranking = np.argsort(f_scores[0])[::-1]
    print(f"  Top 10 features by F-score:")
    for i in range(10):
        idx = ranking[i]
        print(f"    Feature {idx:2d}: F={f_scores[0][idx]:.2f}, p={f_scores[1][idx]:.6f}")
    
    
    print("\n--- SelectKBest impact ---")
    
    for k in [3, 5, 10, 15, 20]:
        pipe = Pipeline([
            ('select', SelectKBest(f_classif, k=k)),
            ('scale', StandardScaler()),
            ('clf', LogisticRegression(max_iter=1000, random_state=42)),
        ])
        scores = cross_val_score(pipe, X_train[:, :20], y_train, cv=5)
        print(f"  k={k:2d}: CV={scores.mean():.4f} ± {scores.std():.4f}")


# =====================================================================
#   PARTE 3: MUTUAL INFORMATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: MUTUAL INFORMATION ===")
print("=" * 80)

"""
MI: mide dependencia NO-LINEAL entre feature y target.
  MI(X, Y) = 0 => independientes.
  MI > 0 => dependencia (mayor = mas informativa).

Ventaja sobre F-test: detecta relaciones no-lineales.
Desventaja: mas lento, requiere estimacion.
"""

if HAS_SKLEARN:
    mi_scores = mutual_info_classif(X_train[:, :20], y_train, random_state=42)
    mi_ranking = np.argsort(mi_scores)[::-1]
    
    print(f"  MI ranking:")
    for i in range(10):
        idx = mi_ranking[i]
        print(f"    Feature {idx:2d}: MI={mi_scores[idx]:.4f}")
    
    # Compare MI vs F-test rankings
    f_ranking = np.argsort(f_scores[0])[::-1][:10]
    mi_top10 = set(mi_ranking[:10])
    f_top10 = set(f_ranking)
    overlap = len(mi_top10 & f_top10)
    print(f"\n  MI vs F-test top-10 overlap: {overlap}/10")


# =====================================================================
#   PARTE 4: RFE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: RFE ===")
print("=" * 80)

"""
Recursive Feature Elimination:
1. Fit model con todas las features.
2. Ranking features por importancia (coef_ o feature_importances_).
3. Eliminar la menos importante.
4. Repetir hasta k features.

RFECV: automaticamente selecciona optimal k via CV.
"""

if HAS_SKLEARN:
    print("\n--- RFE ---")
    
    rfe = RFE(
        estimator=LogisticRegression(max_iter=1000, random_state=42),
        n_features_to_select=10,
        step=1,
    )
    rfe.fit(X_train[:, :20], y_train)
    
    selected = np.where(rfe.support_)[0]
    print(f"  RFE selected: {selected}")
    print(f"  RFE score: {rfe.score(X_test[:, :20], y_test):.4f}")
    
    
    print("\n--- RFECV ---")
    
    rfecv = RFECV(
        estimator=LogisticRegression(max_iter=1000, random_state=42),
        step=1, cv=3, scoring='accuracy',
        min_features_to_select=3,
    )
    rfecv.fit(X_train[:, :20], y_train)
    
    print(f"  Optimal n_features: {rfecv.n_features_}")
    print(f"  RFECV score: {rfecv.score(X_test[:, :20], y_test):.4f}")


# =====================================================================
#   PARTE 5: L1-BASED SELECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: L1 SELECTION ===")
print("=" * 80)

"""
L1 penalty (Lasso) produce SPARSE weights.
Features con weight=0 son eliminadas automaticamente.
"""

if HAS_SKLEARN:
    for C in [0.01, 0.1, 1.0, 10.0]:
        selector = SelectFromModel(
            LogisticRegression(C=C, penalty='l1', solver='saga', max_iter=2000, random_state=42),
            threshold='mean',
        )
        selector.fit(X_train[:, :20], y_train)
        n_selected = selector.get_support().sum()
        
        X_sel = selector.transform(X_train[:, :20])
        X_sel_test = selector.transform(X_test[:, :20])
        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(X_sel, y_train)
        score = lr.score(X_sel_test, y_test)
        
        print(f"  C={C:5.2f}: {n_selected:2d} features, accuracy={score:.4f}")


# =====================================================================
#   PARTE 6: TREE-BASED SELECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: TREE SELECTION ===")
print("=" * 80)

if HAS_SKLEARN:
    for threshold in ['mean', 'median', '0.5*mean']:
        selector_rf = SelectFromModel(
            RandomForestClassifier(100, random_state=42, n_jobs=-1),
            threshold=threshold,
        )
        selector_rf.fit(X_train[:, :20], y_train)
        n_selected = selector_rf.get_support().sum()
        print(f"  threshold='{threshold}': {n_selected} features selected")


# =====================================================================
#   PARTE 7: BORUTA CONCEPT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: BORUTA ===")
print("=" * 80)

"""
Boruta: All-relevant feature selection.
1. Crear "shadow features" (shuffle de cada feature).
2. Fit RF con originales + shadow features.
3. Comparar importancia de cada feature vs max(shadow).
4. Features con importancia > max(shadow) son "confirmed".
5. Repetir hasta convergencia.

Diferencia vs SelectFromModel:
  - Boruta selecciona TODAS las relevantes.
  - SelectFromModel selecciona un subset fijo.
"""

if HAS_SKLEARN:
    def simple_boruta(X, y, n_iterations=20, random_state=42):
        """Simplified Boruta implementation."""
        np.random.seed(random_state)
        n_features = X.shape[1]
        hits = np.zeros(n_features)
        
        for _ in range(n_iterations):
            # Create shadow features
            X_shadow = X.copy()
            for j in range(n_features):
                np.random.shuffle(X_shadow[:, j])
            
            X_combined = np.column_stack([X, X_shadow])
            
            rf = RandomForestClassifier(100, random_state=random_state, n_jobs=-1)
            rf.fit(X_combined, y)
            
            imp = rf.feature_importances_
            shadow_max = imp[n_features:].max()
            
            hits += (imp[:n_features] > shadow_max).astype(int)
        
        # Confirmed if hit > 50% of iterations
        confirmed = hits > n_iterations * 0.5
        return confirmed, hits
    
    confirmed, hits = simple_boruta(X_train[:, :20], y_train, n_iterations=10)
    print(f"  Boruta confirmed: {confirmed.sum()}/20 features")
    print(f"  Hit counts: {hits}")


# =====================================================================
#   PARTE 8: FEATURE CLUSTERING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: FEATURE CLUSTERING ===")
print("=" * 80)

"""
Feature clustering: agrupar features correlacionadas.
Seleccionar un representante de cada cluster.
Reduce redundancia.
"""

def cluster_features(X, n_clusters=5):
    """Cluster features by correlation."""
    corr = np.abs(np.corrcoef(X, rowvar=False))
    
    # Simple hierarchical: merge most correlated
    n_features = X.shape[1]
    labels = np.arange(n_features)
    
    for _ in range(n_features - n_clusters):
        # Find most correlated pair in different clusters
        best_corr = -1
        best_pair = (0, 1)
        for i in range(n_features):
            for j in range(i+1, n_features):
                if labels[i] != labels[j] and corr[i, j] > best_corr:
                    best_corr = corr[i, j]
                    best_pair = (i, j)
        
        old_label = labels[best_pair[1]]
        new_label = labels[best_pair[0]]
        labels[labels == old_label] = new_label
    
    # Renumber
    unique = np.unique(labels)
    mapping = {old: new for new, old in enumerate(unique)}
    return np.array([mapping[l] for l in labels])

cluster_labels = cluster_features(X_train[:, :20], n_clusters=5)
from collections import Counter
print(f"  Feature clusters: {dict(Counter(cluster_labels))}")


# =====================================================================
#   PARTE 9: FE FOR DIFFERENT MODELS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: FE PER MODEL ===")
print("=" * 80)

"""
Diferentes modelos necesitan diferente FE:

LINEAR MODELS:
  ✓ Scale features (StandardScaler)
  ✓ Handle skewness (log/box-cox)
  ✓ One-hot encode categoricals
  ✓ Create polynomial/interactions
  ✗ Trees can learn interactions

TREE-BASED:
  ✓ No need to scale
  ✓ Ordinal encode categoricals
  ✓ Can handle missing values (some)
  ✗ Don't benefit from polynomial features

DISTANCE-BASED (KNN/SVM):
  ✓ Scale features (critical!)
  ✓ Reduce dimensionality (PCA)
  ✗ High cardinality categoricals hurt

NEURAL NETWORKS:
  ✓ Scale to [0,1] or standardize
  ✓ Embeddings for categoricals
  ✓ Handle missing values
"""

if HAS_SKLEARN:
    print(f"  Model-specific FE comparison:")
    
    # Linear: needs scaling + polynomial
    pipe_linear = Pipeline([
        ('scale', StandardScaler()),
        ('poly', PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)),
        ('clf', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    
    # Tree: raw features
    pipe_tree = Pipeline([
        ('clf', RandomForestClassifier(100, random_state=42, n_jobs=-1)),
    ])
    
    for name, pipe in [('Linear+poly', pipe_linear), ('RF_raw', pipe_tree)]:
        scores = cross_val_score(pipe, X_train[:, :20], y_train, cv=5)
        print(f"    {name:>12s}: {scores.mean():.4f} ± {scores.std():.4f}")


# =====================================================================
#   PARTE 10: DATA LEAKAGE PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: DATA LEAKAGE ===")
print("=" * 80)

"""
DATA LEAKAGE: informacion del test se filtra al train.

TIPOS:
1. Target leakage: feature derivada del target.
2. Train-test leakage: fit scaler en test.
3. Temporal leakage: usar datos futuros.
4. Feature leakage: feature que no existe at prediction time.

PREVENCION:
  - SIEMPRE usar Pipeline.
  - fit en train, transform en test.
  - Validar con time-based splits para time series.
  - Revisar features sospechosamente informativas.
"""

if HAS_SKLEARN:
    print("\n--- Leakage demo ---")
    
    # WRONG: fit on all data
    scaler_wrong = StandardScaler()
    X_wrong = scaler_wrong.fit_transform(X_aug[:, :20])
    X_wrong_tr, X_wrong_te, y_wrong_tr, y_wrong_te = train_test_split(
        X_wrong, y, test_size=0.2, random_state=42
    )
    lr_wrong = LogisticRegression(max_iter=1000, random_state=42)
    lr_wrong.fit(X_wrong_tr, y_wrong_tr)
    score_wrong = lr_wrong.score(X_wrong_te, y_wrong_te)
    
    # CORRECT: fit only on train
    X_raw_tr, X_raw_te, y_raw_tr, y_raw_te = train_test_split(
        X_aug[:, :20], y, test_size=0.2, random_state=42
    )
    scaler_correct = StandardScaler()
    X_correct_tr = scaler_correct.fit_transform(X_raw_tr)
    X_correct_te = scaler_correct.transform(X_raw_te)
    lr_correct = LogisticRegression(max_iter=1000, random_state=42)
    lr_correct.fit(X_correct_tr, y_raw_tr)
    score_correct = lr_correct.score(X_correct_te, y_raw_te)
    
    print(f"  WRONG (scale all):  {score_wrong:.4f}")
    print(f"  CORRECT (pipeline): {score_correct:.4f}")
    print(f"  Difference may be small here but critical in production")


# =====================================================================
#   PARTE 11: CUSTOM TRANSFORMER PIPELINE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: CUSTOM PIPELINE ===")
print("=" * 80)

if HAS_SKLEARN:
    class SkewnessCorrector(BaseEstimator, TransformerMixin):
        """Auto-correct skewed features."""
        
        def __init__(self, threshold=0.75):
            self.threshold = threshold
        
        def fit(self, X, y=None):
            X = np.asarray(X, dtype=float)
            from scipy.stats import skew
            self.skewness_ = np.array([skew(X[:, i]) for i in range(X.shape[1])])
            self.skewed_cols_ = np.where(np.abs(self.skewness_) > self.threshold)[0]
            return self
        
        def transform(self, X):
            X = np.asarray(X, dtype=float).copy()
            for col in self.skewed_cols_:
                X[:, col] = np.log1p(np.abs(X[:, col])) * np.sign(X[:, col])
            return X
    
    class InteractionCreator(BaseEstimator, TransformerMixin):
        """Create top-k pairwise interactions."""
        
        def __init__(self, k=5):
            self.k = k
        
        def fit(self, X, y=None):
            self.n_features_ = X.shape[1]
            return self
        
        def transform(self, X):
            X = np.asarray(X)
            interactions = []
            count = 0
            for i in range(min(X.shape[1], 10)):
                for j in range(i+1, min(X.shape[1], 10)):
                    if count >= self.k:
                        break
                    interactions.append(X[:, i] * X[:, j])
                    count += 1
                if count >= self.k:
                    break
            
            if interactions:
                return np.column_stack([X] + [np.array(interactions).T])
            return X
    
    pipe_custom = Pipeline([
        ('skew', SkewnessCorrector(threshold=0.75)),
        ('interactions', InteractionCreator(k=10)),
        ('scale', StandardScaler()),
        ('clf', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    
    scores_custom = cross_val_score(pipe_custom, X_train[:, :20], y_train, cv=5)
    print(f"  Custom FE pipeline: {scores_custom.mean():.4f} ± {scores_custom.std():.4f}")


# =====================================================================
#   PARTE 12: FEATURE VALIDATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: VALIDATION ===")
print("=" * 80)

"""
Feature validation checks:
1. No NaN/Inf after transformation.
2. Consistent shape between train/test.
3. No constant features after transform.
4. Reasonable value ranges.
5. Feature correlations with target.
"""

def validate_features(X_train, X_test, feature_names=None):
    """Validate feature quality."""
    results = []
    
    # Check NaN
    nan_train = np.any(np.isnan(X_train))
    nan_test = np.any(np.isnan(X_test))
    results.append(('No NaN in train', not nan_train))
    results.append(('No NaN in test', not nan_test))
    
    # Check Inf
    inf_train = np.any(np.isinf(X_train))
    results.append(('No Inf in train', not inf_train))
    
    # Check shape
    results.append(('Same n_features', X_train.shape[1] == X_test.shape[1]))
    
    # Check constant
    variance = np.var(X_train, axis=0)
    n_constant = np.sum(variance < 1e-10)
    results.append(('No constant features', n_constant == 0))
    
    return results

results = validate_features(X_train[:, :20], X_test[:, :20])
print(f"  Feature validation:")
for name, passed in results:
    icon = "✓" if passed else "✗"
    print(f"    {icon} {name}")


# =====================================================================
#   PARTE 13: PRODUCTION PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: PRODUCTION ===")
print("=" * 80)

"""
PRODUCTION FE PATTERNS:

1. Feature computation should be DETERMINISTIC.
2. Same code for training and serving.
3. Feature versioning.
4. Feature monitoring (drift).
5. Feature lineage (track dependencies).
6. Cached features for expensive computations.
7. Real-time features: precompute what you can.
"""

class FeatureTransformRegistry:
    """Track feature transformations for reproducibility."""
    
    def __init__(self):
        self.transforms = []
    
    def add(self, name, input_cols, output_cols, transform_fn):
        self.transforms.append({
            'name': name,
            'input': input_cols,
            'output': output_cols,
            'fn': transform_fn,
        })
    
    def apply_all(self, data):
        result = data.copy()
        for t in self.transforms:
            result = t['fn'](result)
        return result
    
    def lineage(self):
        for t in self.transforms:
            print(f"    {t['input']} -> [{t['name']}] -> {t['output']}")

registry = FeatureTransformRegistry()
registry.add('log', ['income'], ['log_income'], lambda d: d)
registry.add('ratio', ['income', 'expenses'], ['savings_rate'], lambda d: d)
registry.add('binning', ['age'], ['age_bin'], lambda d: d)

print(f"  Feature lineage:")
registry.lineage()


# =====================================================================
#   PARTE 14: BEST PRACTICES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: BEST PRACTICES ===")
print("=" * 80)

"""
FEATURE ENGINEERING BEST PRACTICES:

GOLDEN RULES:
  1. Start simple, add complexity incrementally.
  2. ALWAYS use Pipeline (prevent leakage).
  3. Domain knowledge > automated methods.
  4. Validate features with cross-validation.
  5. Monitor feature importance over time.

FEATURE QUALITY CHECKLIST:
  ✓ No data leakage (feature exists at prediction time).
  ✓ No NaN/Inf after transformation.
  ✓ Reasonable cardinality for categoricals.
  ✓ Features are deterministic and reproducible.
  ✓ Features are documented.

ANTI-PATTERNS:
  ✗ Too many features (curse of dimensionality).
  ✗ Features derived from target (leakage).
  ✗ Unstable features (change semantics over time).
  ✗ Features that require future information.
"""

best_practices = [
    ("Pipeline always", "Prevent data leakage"),
    ("Domain knowledge", "Better than automated FE"),
    ("Validate with CV", "Don't look at test set"),
    ("Start simple", "Add complexity incrementally"),
    ("Monitor drift", "Features change over time"),
    ("Document", "Feature definitions and lineage"),
    ("Version", "Track feature set changes"),
    ("Test", "Validate no NaN/Inf/constant"),
]

print(f"\n  {'Practice':>20s} {'Reason':>30s}")
for practice, reason in best_practices:
    print(f"  {practice:>20s} {reason:>30s}")


# =====================================================================
#   PARTE 15: FORWARD SELECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: FORWARD SELECTION ===")
print("=" * 80)

"""
Forward selection (greedy):
1. Start with empty set.
2. Add feature that improves score most.
3. Repeat until no improvement.
"""

if HAS_SKLEARN:
    def forward_selection(X, y, max_features=10, cv=3):
        """Simple forward feature selection."""
        n_features = X.shape[1]
        selected = []
        remaining = list(range(n_features))
        
        for _ in range(min(max_features, n_features)):
            best_score = -np.inf
            best_feature = None
            
            for f in remaining:
                candidate = selected + [f]
                score = cross_val_score(
                    LogisticRegression(max_iter=1000, random_state=42),
                    X[:, candidate], y, cv=cv
                ).mean()
                
                if score > best_score:
                    best_score = score
                    best_feature = f
            
            if best_feature is not None:
                selected.append(best_feature)
                remaining.remove(best_feature)
        
        return selected
    
    fwd_selected = forward_selection(X_train[:, :20], y_train, max_features=8, cv=3)
    print(f"  Forward selected: {fwd_selected}")
    
    lr_fwd = LogisticRegression(max_iter=1000, random_state=42)
    lr_fwd.fit(X_train[:, fwd_selected], y_train)
    print(f"  Score: {lr_fwd.score(X_test[:, fwd_selected], y_test):.4f}")


# =====================================================================
#   PARTE 16: STABILITY SELECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: STABILITY ===")
print("=" * 80)

"""
Stability selection:
  Repeat selection on bootstrap samples.
  Features selected consistently = stable/important.
"""

if HAS_SKLEARN:
    n_bootstrap = 20
    selection_counts = np.zeros(20)
    
    for i in range(n_bootstrap):
        idx = np.random.choice(len(X_train), len(X_train), replace=True)
        X_boot = X_train[idx][:, :20]
        y_boot = y_train[idx]
        
        selector = SelectFromModel(
            LogisticRegression(C=0.1, penalty='l1', solver='saga', max_iter=2000, random_state=i),
            threshold='mean',
        )
        selector.fit(X_boot, y_boot)
        selection_counts += selector.get_support().astype(int)
    
    stability = selection_counts / n_bootstrap
    stable_features = np.where(stability > 0.7)[0]
    
    print(f"  Stable features (>70%): {stable_features}")
    print(f"  Stability scores: {stability.round(2)}")


# =====================================================================
#   PARTE 17: PERMUTATION IMPORTANCE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: PERMUTATION ===")
print("=" * 80)

if HAS_SKLEARN:
    from sklearn.inspection import permutation_importance
    
    rf_perm = RandomForestClassifier(100, random_state=42, n_jobs=-1)
    rf_perm.fit(X_train[:, :20], y_train)
    
    perm_result = permutation_importance(
        rf_perm, X_test[:, :20], y_test, n_repeats=10, random_state=42
    )
    
    perm_sorted = np.argsort(perm_result.importances_mean)[::-1]
    print(f"  Permutation importance (top 10):")
    for i in range(10):
        idx = perm_sorted[i]
        imp = perm_result.importances_mean[idx]
        std = perm_result.importances_std[idx]
        print(f"    Feature {idx:2d}: {imp:.4f} ± {std:.4f}")


# =====================================================================
#   PARTE 18: IMPORTANCE COMPARISON
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: IMPORTANCE COMPARE ===")
print("=" * 80)

if HAS_SKLEARN:
    # MDI vs Permutation vs L1
    mdi_imp = rf_perm.feature_importances_
    mdi_top = set(np.argsort(mdi_imp)[::-1][:10])
    
    perm_top = set(perm_sorted[:10])
    
    l1_model = LogisticRegression(C=0.1, penalty='l1', solver='saga', max_iter=2000, random_state=42)
    l1_model.fit(X_train[:, :20], y_train)
    l1_top = set(np.argsort(np.abs(l1_model.coef_[0]))[::-1][:10])
    
    print(f"  MDI vs Permutation overlap:  {len(mdi_top & perm_top)}/10")
    print(f"  MDI vs L1 overlap:           {len(mdi_top & l1_top)}/10")
    print(f"  Permutation vs L1 overlap:   {len(perm_top & l1_top)}/10")
    print(f"  All three agree:             {len(mdi_top & perm_top & l1_top)}/10")


# =====================================================================
#   PARTE 19: SEQUENTIAL FEATURE SELECTOR
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: SFS ===")
print("=" * 80)

if HAS_SKLEARN:
    from sklearn.feature_selection import SequentialFeatureSelector
    
    sfs = SequentialFeatureSelector(
        LogisticRegression(max_iter=1000, random_state=42),
        n_features_to_select=10,
        direction='forward',
        cv=3,
    )
    sfs.fit(X_train[:, :20], y_train)
    
    sfs_selected = np.where(sfs.get_support())[0]
    print(f"  SFS selected: {sfs_selected}")
    
    X_sfs_tr = sfs.transform(X_train[:, :20])
    X_sfs_te = sfs.transform(X_test[:, :20])
    lr_sfs = LogisticRegression(max_iter=1000, random_state=42)
    lr_sfs.fit(X_sfs_tr, y_train)
    print(f"  SFS score: {lr_sfs.score(X_sfs_te, y_test):.4f}")


# =====================================================================
#   PARTE 20: CORRELATION FILTERING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: CORRELATION FILTER ===")
print("=" * 80)

def drop_correlated(X, threshold=0.9):
    """Drop highly correlated features."""
    corr = np.abs(np.corrcoef(X, rowvar=False))
    n = corr.shape[0]
    to_drop = set()
    
    for i in range(n):
        if i in to_drop:
            continue
        for j in range(i+1, n):
            if corr[i, j] > threshold:
                to_drop.add(j)
    
    keep = sorted(set(range(n)) - to_drop)
    return keep

keep_cols = drop_correlated(X_train[:, :20], threshold=0.9)
print(f"  Original: 20 features")
print(f"  After r>0.9 filter: {len(keep_cols)} features")
print(f"  Kept: {keep_cols}")


# =====================================================================
#   PARTE 21: AUTOMATED FE CONCEPT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: AUTOMATED FE ===")
print("=" * 80)

"""
Automated Feature Engineering tools:
1. Featuretools: deep feature synthesis.
2. tsfresh: time series features.
3. AutoFeat: symbolic feature generation.

Featuretools pattern:
  import featuretools as ft
  es = ft.EntitySet()
  es.add_dataframe(...)
  features = ft.dfs(entityset=es, target_dataframe_name='...')
"""

print("  Automated FE tools:")
print("    Featuretools: entity-relationship based")
print("    tsfresh: 1000+ time series features")
print("    AutoFeat: symbolic regression + selection")
print("    CAUTION: always validate with CV, many features = overfitting risk")


# =====================================================================
#   PARTE 22: CHI-SQUARED
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 22: CHI-SQUARED ===")
print("=" * 80)

if HAS_SKLEARN:
    from sklearn.feature_selection import chi2
    from sklearn.preprocessing import MinMaxScaler
    
    # chi2 requires non-negative features
    X_pos = MinMaxScaler().fit_transform(X_train[:, :20])
    chi_scores, chi_pvals = chi2(X_pos, y_train)
    
    chi_ranking = np.argsort(chi_scores)[::-1]
    print(f"  Chi-squared ranking (top 10):")
    for i in range(10):
        idx = chi_ranking[i]
        print(f"    Feature {idx:2d}: chi2={chi_scores[idx]:.2f}, p={chi_pvals[idx]:.6f}")


# =====================================================================
#   PARTE 23: SELECTION COMPARISON
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 23: COMPARISON ===")
print("=" * 80)

if HAS_SKLEARN:
    methods = {
        'All (20)': list(range(20)),
        'ANOVA top-10': list(np.argsort(f_scores[0])[::-1][:10]),
        'MI top-10': list(mi_ranking[:10]),
        'RFE-10': list(np.where(rfe.support_)[0]),
        'L1': list(np.where(np.abs(l1_model.coef_[0]) > 0.01)[0]),
        'Boruta': list(np.where(confirmed)[0]),
    }
    
    print(f"  {'Method':>14s} {'N_feat':>7s} {'CV Score':>10s}")
    for name, features in methods.items():
        if len(features) == 0:
            continue
        scores = cross_val_score(
            LogisticRegression(max_iter=1000, random_state=42),
            X_train[:, features], y_train, cv=5
        )
        print(f"  {name:>14s} {len(features):7d} {scores.mean():10.4f}")


# =====================================================================
#   PARTE 24: SELECTION PIPELINE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 24: FULL PIPELINE ===")
print("=" * 80)

if HAS_SKLEARN:
    full_fe_pipe = Pipeline([
        ('variance', VarianceThreshold(threshold=0.01)),
        ('scale', StandardScaler()),
        ('select', SelectKBest(f_classif, k=10)),
        ('clf', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    
    full_scores = cross_val_score(full_fe_pipe, X_train[:, :20], y_train, cv=5)
    print(f"  Full FE pipeline: {full_scores.mean():.4f} ± {full_scores.std():.4f}")
    
    full_fe_pipe.fit(X_train[:, :20], y_train)
    print(f"  Test score: {full_fe_pipe.score(X_test[:, :20], y_test):.4f}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN FEATURE SELECTION & PIPELINES:

1. Variance Threshold: eliminar constantes.
2. Univariate: ANOVA, chi2, MI.
3. RFE/RFECV: recursive elimination.
4. L1/Embedded: automatic selection via regularization.
5. Boruta: all-relevant selection.
6. Feature clustering: reduce redundancy.
7. Model-specific FE: linear vs tree vs NN.
8. Data leakage: ALWAYS use Pipeline.
9. Custom transformers: fit/transform pattern.
10. Production: deterministic, versioned, monitored.

FIN DEL MODULO 15: FEATURE ENGINEERING.
"""

print("\n FIN DE ARCHIVO 02_feature_selection_pipelines.")
print(" Feature selection y pipelines dominados.")
print(" Siguiente modulo: EVALUACION Y VALIDACION.")
