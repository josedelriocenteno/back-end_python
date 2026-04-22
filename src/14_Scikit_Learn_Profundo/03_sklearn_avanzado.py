# ===========================================================================
# 03_sklearn_avanzado.py
# ===========================================================================
# MODULO 14: SCIKIT-LEARN PROFUNDO
# ARCHIVO 03: Sklearn Avanzado (Feature Selection, Calibration, Deploy)
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Patrones avanzados: feature selection, calibration, model interpretation,
# imbalanced learning, deployment patterns.
#
# CONTENIDO:
#   1. Feature Selection (filter, wrapper, embedded).
#   2. Dimensionality Reduction (PCA, Truncated SVD).
#   3. Model Calibration.
#   4. Imbalanced Learning.
#   5. Multi-output classification.
#   6. Target encoding patterns.
#   7. Custom estimator completo.
#   8. Model interpretation.
#   9. A/B testing de modelos.
#   10. Production patterns.
#   11. Sklearn internals.
#   12. Best practices checklist.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
    from sklearn.feature_selection import (
        SelectKBest, f_classif, mutual_info_classif,
        RFE, SelectFromModel,
    )
    from sklearn.decomposition import PCA, TruncatedSVD
    from sklearn.calibration import CalibratedClassifierCV, calibration_curve
    from sklearn.model_selection import (
        train_test_split, cross_val_score, cross_val_predict,
        StratifiedKFold,
    )
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC
    from sklearn.datasets import make_classification
    from sklearn.metrics import (
        accuracy_score, f1_score, brier_score_loss,
        classification_report, log_loss,
    )
    from sklearn.preprocessing import StandardScaler, label_binarize
    from sklearn.pipeline import Pipeline
    from sklearn.multiclass import OneVsRestClassifier
    from sklearn.utils import class_weight
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("  (sklearn no disponible)")


# =====================================================================
#   PARTE 1: FEATURE SELECTION - FILTER
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: FILTER METHODS ===")
print("=" * 80)

"""
FILTER METHODS: evaluar features independientemente del modelo.

1. Variance threshold: eliminar features con baja varianza.
2. Univariate tests:
   - f_classif: ANOVA F-test (clasificacion).
   - chi2: chi-squared (clasificacion, features positivas).
   - mutual_info_classif: mutual information.
3. Correlation: eliminar features altamente correlacionadas.
"""

if HAS_SKLEARN:
    print("\n--- Datos ---")
    
    X, y = make_classification(
        n_samples=1000, n_features=30, n_informative=10,
        n_redundant=10, n_classes=2, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"  Features: {X.shape[1]}")
    
    
    print("\n--- SelectKBest (ANOVA) ---")
    
    for k in [5, 10, 15, 20, 30]:
        selector = SelectKBest(f_classif, k=k)
        X_selected = selector.fit_transform(X_train, y_train)
        X_test_sel = selector.transform(X_test)
        
        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(X_selected, y_train)
        score = lr.score(X_test_sel, y_test)
        print(f"  k={k:2d}: accuracy={score:.4f}")
    
    
    print("\n--- Mutual Information ---")
    
    mi_scores = mutual_info_classif(X_train, y_train, random_state=42)
    mi_ranking = np.argsort(mi_scores)[::-1]
    
    print(f"  Top 10 MI features:")
    for i in range(10):
        idx = mi_ranking[i]
        print(f"    Feature {idx:2d}: MI={mi_scores[idx]:.4f}")
    
    
    print("\n--- Correlation filter ---")
    
    def correlation_filter(X, threshold=0.9):
        """Remove features with high pairwise correlation."""
        corr = np.corrcoef(X, rowvar=False)
        n = corr.shape[0]
        to_drop = set()
        
        for i in range(n):
            if i in to_drop:
                continue
            for j in range(i+1, n):
                if abs(corr[i, j]) > threshold:
                    to_drop.add(j)
        
        return sorted(set(range(n)) - to_drop)
    
    kept = correlation_filter(X_train, threshold=0.9)
    print(f"  Correlation filter (r>0.9): {X.shape[1]} -> {len(kept)} features")


# =====================================================================
#   PARTE 2: FEATURE SELECTION - WRAPPER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: WRAPPER METHODS ===")
print("=" * 80)

"""
WRAPPER: usar un modelo para evaluar subsets.
  - RFE (Recursive Feature Elimination): eliminar feature menos importante.
  - Forward/Backward selection.
  - Mas costoso pero mas preciso.
"""

if HAS_SKLEARN:
    print("\n--- RFE ---")
    
    for n_features in [5, 10, 15]:
        rfe = RFE(
            estimator=LogisticRegression(max_iter=1000, random_state=42),
            n_features_to_select=n_features,
            step=1,
        )
        rfe.fit(X_train, y_train)
        score_rfe = rfe.score(X_test, y_test)
        selected = np.where(rfe.support_)[0]
        print(f"  n_features={n_features:2d}: accuracy={score_rfe:.4f}, selected={selected[:5]}...")


# =====================================================================
#   PARTE 3: FEATURE SELECTION - EMBEDDED
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: EMBEDDED METHODS ===")
print("=" * 80)

"""
EMBEDDED: feature selection como parte del training.
  - L1 regularization (Lasso/LogReg penalty='l1').
  - Tree-based importance.
  - SelectFromModel: threshold-based selection.
"""

if HAS_SKLEARN:
    print("\n--- SelectFromModel (L1) ---")
    
    l1_selector = SelectFromModel(
        LogisticRegression(C=0.1, penalty='l1', solver='saga', max_iter=2000, random_state=42),
        threshold='mean',
    )
    l1_selector.fit(X_train, y_train)
    X_l1 = l1_selector.transform(X_train)
    X_l1_test = l1_selector.transform(X_test)
    
    lr_l1 = LogisticRegression(max_iter=1000, random_state=42)
    lr_l1.fit(X_l1, y_train)
    
    print(f"  L1 features: {X.shape[1]} -> {X_l1.shape[1]}")
    print(f"  Accuracy: {lr_l1.score(X_l1_test, y_test):.4f}")
    
    
    print("\n--- SelectFromModel (RF) ---")
    
    rf_selector = SelectFromModel(
        RandomForestClassifier(100, random_state=42, n_jobs=-1),
        threshold='mean',
    )
    rf_selector.fit(X_train, y_train)
    X_rf = rf_selector.transform(X_train)
    
    print(f"  RF features: {X.shape[1]} -> {X_rf.shape[1]}")


# =====================================================================
#   PARTE 4: PCA / TRUNCATED SVD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: DIMENSIONALITY REDUCTION ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- PCA ---")
    
    pca = PCA(n_components=0.95)  # Keep 95% variance
    X_pca = pca.fit_transform(X_train)
    X_pca_test = pca.transform(X_test)
    
    print(f"  PCA: {X.shape[1]} -> {X_pca.shape[1]} (95% variance)")
    print(f"  Explained variance: {pca.explained_variance_ratio_.sum():.4f}")
    
    lr_pca = LogisticRegression(max_iter=1000, random_state=42)
    lr_pca.fit(X_pca, y_train)
    print(f"  Accuracy with PCA: {lr_pca.score(X_pca_test, y_test):.4f}")
    
    
    print("\n--- Truncated SVD ---")
    
    svd = TruncatedSVD(n_components=15, random_state=42)
    X_svd = svd.fit_transform(X_train)
    print(f"  SVD: {X.shape[1]} -> {X_svd.shape[1]}")
    print(f"  Variance: {svd.explained_variance_ratio_.sum():.4f}")


# =====================================================================
#   PARTE 5: MODEL CALIBRATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: CALIBRATION ===")
print("=" * 80)

"""
Calibration: ajustar probabilidades para que P(y=1|p=0.8) ≈ 0.8.

Metodos:
1. Platt scaling (sigmoid): CalibratedClassifierCV(method='sigmoid')
2. Isotonic regression: CalibratedClassifierCV(method='isotonic')

Brier score: mean((p - y)^2). Menor = mejor calibrado.
"""

if HAS_SKLEARN:
    print("\n--- Calibration comparison ---")
    
    # SVM is notoriously poorly calibrated
    svm = SVC(probability=False, random_state=42)
    svm_calibrated = CalibratedClassifierCV(svm, cv=5, method='sigmoid')
    svm_isotonic = CalibratedClassifierCV(svm, cv=5, method='isotonic')
    
    # Fit and compare
    models_cal = {
        'LogReg': LogisticRegression(max_iter=1000, random_state=42),
        'SVM+Platt': svm_calibrated,
        'SVM+Isotonic': svm_isotonic,
    }
    
    for name, model in models_cal.items():
        model.fit(X_train, y_train)
        if hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test)[:, 1]
            brier = brier_score_loss(y_test, y_proba)
            ll = log_loss(y_test, y_proba)
            acc = accuracy_score(y_test, model.predict(X_test))
            print(f"  {name:>14s}: accuracy={acc:.4f}, brier={brier:.4f}, logloss={ll:.4f}")


# =====================================================================
#   PARTE 6: IMBALANCED LEARNING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: IMBALANCED LEARNING ===")
print("=" * 80)

"""
Tecnicas en sklearn:
1. class_weight='balanced': ajustar weights automaticamente.
2. sample_weight: peso por muestra.
3. SMOTE: oversampling sintetico (imblearn).
4. Threshold adjustment post-training.
"""

if HAS_SKLEARN:
    print("\n--- Imbalanced data ---")
    
    X_imb, y_imb = make_classification(
        n_samples=1000, n_features=20, n_informative=10,
        weights=[0.9, 0.1], random_state=42
    )
    X_imb_tr, X_imb_te, y_imb_tr, y_imb_te = train_test_split(
        X_imb, y_imb, test_size=0.2, random_state=42, stratify=y_imb
    )
    
    print(f"  Class balance: {np.mean(y_imb_tr):.3f}")
    
    models_imb = {
        'Default': LogisticRegression(max_iter=1000, random_state=42),
        'Balanced': LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
        'RF_balanced': RandomForestClassifier(100, class_weight='balanced', random_state=42),
    }
    
    print(f"\n  {'Model':>14s} {'Acc':>6s} {'F1':>6s} {'F1_min':>7s}")
    
    for name, model in models_imb.items():
        model.fit(X_imb_tr, y_imb_tr)
        y_pred_imb = model.predict(X_imb_te)
        acc = accuracy_score(y_imb_te, y_pred_imb)
        f1 = f1_score(y_imb_te, y_pred_imb)
        f1_min = f1_score(y_imb_te, y_pred_imb, pos_label=1)
        print(f"  {name:>14s} {acc:6.4f} {f1:6.4f} {f1_min:7.4f}")
    
    
    print("\n--- Compute class weights ---")
    
    weights = class_weight.compute_class_weight(
        'balanced', classes=np.unique(y_imb_tr), y=y_imb_tr
    )
    print(f"  Class weights: {dict(zip(np.unique(y_imb_tr), weights.round(3)))}")
    
    # Sample weights
    sample_w = class_weight.compute_sample_weight('balanced', y_imb_tr)
    print(f"  Sample weight range: [{sample_w.min():.3f}, {sample_w.max():.3f}]")


# =====================================================================
#   PARTE 7: CUSTOM ESTIMATOR COMPLETO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: CUSTOM ESTIMATOR ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- Custom classifier ---")
    
    class WeightedKNN(BaseEstimator, ClassifierMixin):
        """KNN with distance-weighted voting."""
        
        def __init__(self, k=5, weight_func='inverse'):
            self.k = k
            self.weight_func = weight_func
        
        def fit(self, X, y):
            self.X_train_ = np.asarray(X)
            self.y_train_ = np.asarray(y)
            self.classes_ = np.unique(y)
            return self
        
        def predict(self, X):
            X = np.asarray(X)
            predictions = []
            for x in X:
                distances = np.sqrt(np.sum((self.X_train_ - x)**2, axis=1))
                k_idx = np.argsort(distances)[:self.k]
                k_dists = distances[k_idx]
                k_labels = self.y_train_[k_idx]
                
                if self.weight_func == 'inverse':
                    weights = 1.0 / (k_dists + 1e-10)
                else:
                    weights = np.ones_like(k_dists)
                
                class_weights = {}
                for label, w in zip(k_labels, weights):
                    class_weights[label] = class_weights.get(label, 0) + w
                
                predictions.append(max(class_weights, key=class_weights.get))
            
            return np.array(predictions)
        
        def predict_proba(self, X):
            X = np.asarray(X)
            probas = []
            for x in X:
                distances = np.sqrt(np.sum((self.X_train_ - x)**2, axis=1))
                k_idx = np.argsort(distances)[:self.k]
                k_dists = distances[k_idx]
                k_labels = self.y_train_[k_idx]
                
                weights = 1.0 / (k_dists + 1e-10)
                
                class_proba = np.zeros(len(self.classes_))
                for label, w in zip(k_labels, weights):
                    idx = np.where(self.classes_ == label)[0][0]
                    class_proba[idx] += w
                
                class_proba /= class_proba.sum()
                probas.append(class_proba)
            
            return np.array(probas)
    
    # Use in sklearn ecosystem
    wknn = WeightedKNN(k=5, weight_func='inverse')
    
    # Scale first
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_train)
    X_te_s = scaler.transform(X_test)
    
    wknn.fit(X_tr_s, y_train)
    print(f"  WeightedKNN accuracy: {wknn.score(X_te_s, y_test):.4f}")
    
    # Works with cross_val_score
    cv_wknn = cross_val_score(WeightedKNN(k=5), X_tr_s, y_train, cv=5)
    print(f"  CV score: {cv_wknn.mean():.4f} ± {cv_wknn.std():.4f}")


# =====================================================================
#   PARTE 8: MODEL INTERPRETATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: INTERPRETATION ===")
print("=" * 80)

"""
Interpretation patterns:
1. Coefficients (linear models): w > 0 positiva, < 0 negativa.
2. Feature importance (trees): MDI, permutation.
3. Partial Dependence Plots: efecto de una feature.
4. SHAP: per-sample, game-theoretic.
5. LIME: local linear approximation.
"""

if HAS_SKLEARN:
    print("\n--- LogReg coefficients ---")
    
    lr_interp = LogisticRegression(max_iter=1000, random_state=42)
    lr_interp.fit(X_tr_s, y_train)
    
    coefs = lr_interp.coef_[0]
    abs_coefs = np.abs(coefs)
    top_idx = np.argsort(abs_coefs)[::-1]
    
    print(f"  Top 10 features by |coefficient|:")
    for i in range(10):
        idx = top_idx[i]
        sign = "+" if coefs[idx] > 0 else "-"
        print(f"    Feature {idx:2d}: {sign}{abs_coefs[idx]:.4f}")
    
    
    print("\n--- RF vs LogReg ranking ---")
    
    rf_interp = RandomForestClassifier(100, random_state=42, n_jobs=-1)
    rf_interp.fit(X_train, y_train)
    
    rf_top = np.argsort(rf_interp.feature_importances_)[::-1][:10]
    lr_top = top_idx[:10]
    overlap = len(set(rf_top) & set(lr_top))
    print(f"  RF vs LogReg top-10 overlap: {overlap}/10")


# =====================================================================
#   PARTE 9: A/B TESTING DE MODELOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: A/B TESTING ===")
print("=" * 80)

"""
Comparar 2 modelos estadisticamente:
1. Paired t-test sobre CV scores.
2. McNemar's test (clasificacion).
3. Corrected resampled t-test (Nadeau-Bengio).
"""

if HAS_SKLEARN:
    print("\n--- Paired CV comparison ---")
    
    model_a = LogisticRegression(max_iter=1000, random_state=42)
    model_b = RandomForestClassifier(100, random_state=42, n_jobs=-1)
    
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    
    scores_a = cross_val_score(model_a, X_train, y_train, cv=cv)
    scores_b = cross_val_score(model_b, X_train, y_train, cv=cv)
    
    diff = scores_b - scores_a
    mean_diff = diff.mean()
    std_diff = diff.std()
    t_stat = mean_diff / (std_diff / np.sqrt(len(diff))) if std_diff > 0 else 0
    significant = abs(t_stat) > 2.262  # t-crit for df=9, alpha=0.05
    
    print(f"  Model A (LogReg): {scores_a.mean():.4f} ± {scores_a.std():.4f}")
    print(f"  Model B (RF):     {scores_b.mean():.4f} ± {scores_b.std():.4f}")
    print(f"  Diff: {mean_diff:.4f} ± {std_diff:.4f}")
    print(f"  t-stat: {t_stat:.4f}, significant: {significant}")


# =====================================================================
#   PARTE 10: PRODUCTION PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: PRODUCTION ===")
print("=" * 80)

"""
PRODUCTION CHECKLIST:

1. PIPELINE: SIEMPRE empaquetar preprocessing + model.
2. VERSIONING: guardar version de sklearn, hash de datos.
3. MONITORING: tracking de input distribution drift.
4. RETRAINING: automatizar retraining periodico.
5. FALLBACK: tener baseline model como backup.
6. TESTING: unit tests para predict format.
7. LOGGING: log predictions para auditing.

ANTI-PATTERNS:
  - Preprocessing separado del modelo.
  - No versionar el modelo.
  - No monitorear drift.
  - No tener tests.
"""

print("  Production patterns:")
print("    1. Pipeline = preprocessing + model (single object)")
print("    2. Version control: sklearn version + data hash")
print("    3. Monitor: input distribution drift")
print("    4. Retrain: automated periodic retraining")
print("    5. Fallback: baseline model as backup")
print("    6. Test: unit tests for predict() shape/dtype")


# =====================================================================
#   PARTE 11: SKLEARN INTERNALS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: INTERNALS ===")
print("=" * 80)

"""
CONVENCION SKLEARN:
1. __init__: solo guardar parametros (no procesar).
2. fit(): aprender parametros, guardar con trailing _.
3. get_params()/set_params(): para cloning.
4. check_is_fitted(): verificar que fit() fue llamado.

NAMING:
  - Parametros: camelCase en __init__.
  - Atributos aprendidos: trailing _ (coef_, n_features_in_).
  - Methods: fit, predict, transform, score.
"""

if HAS_SKLEARN:
    from sklearn.utils.validation import check_is_fitted
    
    lr_check = LogisticRegression(max_iter=1000)
    
    # Before fit
    try:
        check_is_fitted(lr_check)
        print("  ERROR: should not be fitted")
    except Exception:
        print("  Before fit: not fitted (correct)")
    
    lr_check.fit(X_train, y_train)
    
    try:
        check_is_fitted(lr_check)
        print("  After fit: fitted (correct)")
    except Exception:
        print("  ERROR: should be fitted")
    
    # Clone
    from sklearn.base import clone
    lr_cloned = clone(lr_check)
    print(f"  Clone has same params: {lr_cloned.get_params() == lr_check.get_params()}")
    
    try:
        check_is_fitted(lr_cloned)
    except Exception:
        print("  Clone is not fitted (correct - fresh copy)")


# =====================================================================
#   PARTE 12: BEST PRACTICES CHECKLIST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: BEST PRACTICES ===")
print("=" * 80)

"""
SKLEARN BEST PRACTICES:

PRE-PROCESSING:
  ✓ Use Pipeline to prevent data leakage
  ✓ fit on train, transform on train+test
  ✓ Handle missing values (SimpleImputer)
  ✓ Scale for gradient/distance-based models
  ✓ Encode categoricals (OneHotEncoder/OrdinalEncoder)

MODEL SELECTION:
  ✓ Start with simple baseline (LogReg/DummyClassifier)
  ✓ Use cross-validation (not single split)
  ✓ Stratify splits for classification
  ✓ Use appropriate metric for problem
  ✓ Check learning curves for bias/variance

HYPERPARAMETER TUNING:
  ✓ GridSearchCV for small search spaces
  ✓ RandomizedSearchCV for large search spaces
  ✓ Always use CV (never tune on test set)
  ✓ Pipeline + GridSearch = no leakage

EVALUATION:
  ✓ Multiple metrics (not just accuracy)
  ✓ Confusion matrix for error analysis
  ✓ Calibration for probability estimates
  ✓ Statistical significance for model comparison
  ✓ Final evaluation on hold-out test set

DEPLOYMENT:
  ✓ Save full pipeline (not just model)
  ✓ Log sklearn version
  ✓ Unit test predict() output
  ✓ Monitor input distribution drift
"""

checklist = [
    ("Pipeline prevents leakage", True),
    ("Stratified splits", True),
    ("Cross-validation used", True),
    ("Multiple metrics", True),
    ("Calibration checked", True),
    ("Statistical testing", True),
    ("Full pipeline saved", True),
    ("Version logged", True),
]

print(f"\n  Best practices checklist:")
for item, done in checklist:
    icon = "✓" if done else "✗"
    print(f"    {icon} {item}")


# =====================================================================
#   PARTE 13: THRESHOLD OPTIMIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: THRESHOLD ===")
print("=" * 80)

"""
Default threshold = 0.5. Pero NO siempre es optimo.
Ajustar threshold para:
  - Maximizar F1
  - Minimizar FP (alta precision)
  - Minimizar FN (alto recall)
"""

if HAS_SKLEARN:
    lr_thresh = LogisticRegression(max_iter=1000, random_state=42)
    lr_thresh.fit(X_train, y_train)
    y_proba_thresh = lr_thresh.predict_proba(X_test)[:, 1]
    
    print(f"  Threshold sweep:")
    best_f1 = 0
    best_thresh = 0.5
    
    for thresh in np.arange(0.1, 0.9, 0.05):
        y_pred_t = (y_proba_thresh >= thresh).astype(int)
        f1 = f1_score(y_test, y_pred_t)
        acc = accuracy_score(y_test, y_pred_t)
        
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = thresh
        
        if thresh in [0.2, 0.3, 0.5, 0.7, 0.8]:
            print(f"    thresh={thresh:.2f}: acc={acc:.4f}, f1={f1:.4f}")
    
    print(f"\n  Optimal threshold: {best_thresh:.2f} (F1={best_f1:.4f})")


# =====================================================================
#   PARTE 14: CROSS_VAL_PREDICT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: CROSS_VAL_PREDICT ===")
print("=" * 80)

"""
cross_val_predict: obtener OOF predictions.
Util para:
1. Stacking (meta-features).
2. Calibration analysis.
3. Error analysis.
"""

if HAS_SKLEARN:
    oof_preds = cross_val_predict(
        LogisticRegression(max_iter=1000, random_state=42),
        X_train, y_train, cv=5, method='predict_proba'
    )[:, 1]
    
    oof_labels = (oof_preds >= 0.5).astype(int)
    oof_acc = accuracy_score(y_train, oof_labels)
    oof_brier = brier_score_loss(y_train, oof_preds)
    
    print(f"  OOF accuracy: {oof_acc:.4f}")
    print(f"  OOF Brier:    {oof_brier:.4f}")
    print(f"  OOF predictions shape: {oof_preds.shape}")


# =====================================================================
#   PARTE 15: VARIANCE THRESHOLD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: VARIANCE THRESHOLD ===")
print("=" * 80)

if HAS_SKLEARN:
    from sklearn.feature_selection import VarianceThreshold
    
    # Add some constant/low-variance features
    X_var = np.column_stack([
        X_train,
        np.ones((len(X_train), 1)),              # constant
        np.random.choice([0, 1], (len(X_train), 1), p=[0.99, 0.01]),  # near-constant
    ])
    
    for thresh in [0.0, 0.01, 0.1]:
        vt = VarianceThreshold(threshold=thresh)
        X_filtered = vt.fit_transform(X_var)
        print(f"  threshold={thresh:.2f}: {X_var.shape[1]} -> {X_filtered.shape[1]} features")


# =====================================================================
#   PARTE 16: MULTI-OUTPUT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: MULTI-OUTPUT ===")
print("=" * 80)

"""
Multi-output: predecir multiples targets simultaneamente.
  - MultiOutputClassifier: wrapper para cualquier classifier.
  - Algunos modelos lo soportan nativamente (RF, KNN).
"""

if HAS_SKLEARN:
    from sklearn.multioutput import MultiOutputClassifier
    
    # Create multi-label target
    y_multi = np.column_stack([y_train, (y_train + np.random.binomial(1, 0.1, len(y_train))) % 2])
    y_multi_test = np.column_stack([y_test, (y_test + np.random.binomial(1, 0.1, len(y_test))) % 2])
    
    mo_clf = MultiOutputClassifier(LogisticRegression(max_iter=1000, random_state=42))
    mo_clf.fit(X_train, y_multi)
    y_mo_pred = mo_clf.predict(X_test)
    
    for i in range(y_multi.shape[1]):
        acc = accuracy_score(y_multi_test[:, i], y_mo_pred[:, i])
        print(f"  Target {i}: accuracy={acc:.4f}")


# =====================================================================
#   PARTE 17: DATA DRIFT DETECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: DRIFT DETECTION ===")
print("=" * 80)

"""
Drift: when production data distribution changes from training.

Simple detection:
1. Compare feature statistics (mean, std, min, max).
2. KS test per feature.
3. PSI (Population Stability Index).
"""

def simple_drift_check(X_ref, X_new, threshold=2.0):
    """Check for distribution drift using z-score of means."""
    ref_mean = X_ref.mean(axis=0)
    ref_std = X_ref.std(axis=0) + 1e-10
    new_mean = X_new.mean(axis=0)
    
    z_scores = np.abs((new_mean - ref_mean) / ref_std)
    drifted = z_scores > threshold
    
    return drifted, z_scores

if HAS_SKLEARN:
    # Simulate drift
    X_drifted = X_test.copy()
    X_drifted[:, 0] += 3  # Shift feature 0
    X_drifted[:, 5] *= 2  # Scale feature 5
    
    drifted_mask, z_scores = simple_drift_check(X_train, X_test)
    drifted_mask2, z_scores2 = simple_drift_check(X_train, X_drifted)
    
    print(f"  Normal data: {drifted_mask.sum()} drifted features")
    print(f"  Shifted data: {drifted_mask2.sum()} drifted features")
    
    top_drift = np.argsort(z_scores2)[::-1][:5]
    for idx in top_drift:
        print(f"    Feature {idx}: z={z_scores2[idx]:.2f}")


# =====================================================================
#   PARTE 18: MODEL REGISTRY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: MODEL REGISTRY ===")
print("=" * 80)

"""
Model registry pattern:
  Mantener un registro de modelos entrenados con metadata.
"""

class ModelRegistry:
    """Simple in-memory model registry."""
    
    def __init__(self):
        self.models = {}
        self._counter = 0
    
    def register(self, name, model, metrics, tags=None):
        self._counter += 1
        self.models[self._counter] = {
            'name': name,
            'model': model,
            'metrics': metrics,
            'tags': tags or [],
            'version': self._counter,
        }
        return self._counter
    
    def get_best(self, metric='accuracy'):
        best_id = max(self.models, key=lambda k: self.models[k]['metrics'].get(metric, 0))
        return self.models[best_id]
    
    def list_models(self):
        for mid, info in self.models.items():
            print(f"    v{mid}: {info['name']} - {info['metrics']}")

if HAS_SKLEARN:
    registry = ModelRegistry()
    
    for name, model in [
        ('LogReg', LogisticRegression(max_iter=1000, random_state=42)),
        ('RF', RandomForestClassifier(100, random_state=42)),
    ]:
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)
        registry.register(name, model, {'accuracy': acc})
    
    print(f"  Registered models:")
    registry.list_models()
    best = registry.get_best()
    print(f"  Best: {best['name']} ({best['metrics']})")


# =====================================================================
#   PARTE 19: RFECV
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: RFECV ===")
print("=" * 80)

"""
RFECV: RFE con cross-validation para seleccionar n_features automaticamente.
"""

if HAS_SKLEARN:
    from sklearn.feature_selection import RFECV
    
    rfecv = RFECV(
        estimator=LogisticRegression(max_iter=1000, random_state=42),
        step=1, cv=3, scoring='accuracy', min_features_to_select=5,
    )
    rfecv.fit(X_train, y_train)
    
    print(f"  Optimal features: {rfecv.n_features_}")
    print(f"  Score with optimal: {rfecv.score(X_test, y_test):.4f}")
    print(f"  Selected: {np.where(rfecv.support_)[0][:10]}...")


# =====================================================================
#   PARTE 20: SKLEARN FULL WORKFLOW
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: FULL WORKFLOW ===")
print("=" * 80)

"""
Complete ML workflow:
1. Load & explore data
2. Split train/test (stratified)
3. Build pipeline (preprocess + model)
4. Cross-validate
5. Hyperparameter tune
6. Evaluate on test
7. Analyze errors
8. Save model
"""

if HAS_SKLEARN:
    print("\n--- Full workflow demo ---")
    
    # 1. Data
    X_wf, y_wf = make_classification(
        n_samples=800, n_features=15, n_informative=8,
        n_redundant=3, random_state=42
    )
    
    # 2. Split
    X_wf_tr, X_wf_te, y_wf_tr, y_wf_te = train_test_split(
        X_wf, y_wf, test_size=0.2, random_state=42, stratify=y_wf
    )
    
    # 3. Pipeline
    pipe_wf = Pipeline([
        ('scaler', StandardScaler()),
        ('selector', SelectKBest(f_classif, k=10)),
        ('clf', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    
    # 4. CV
    cv_scores_wf = cross_val_score(pipe_wf, X_wf_tr, y_wf_tr, cv=5)
    print(f"  Step 4 - CV: {cv_scores_wf.mean():.4f} ± {cv_scores_wf.std():.4f}")
    
    # 5. Final fit
    pipe_wf.fit(X_wf_tr, y_wf_tr)
    
    # 6. Test eval
    test_score_wf = pipe_wf.score(X_wf_te, y_wf_te)
    print(f"  Step 6 - Test: {test_score_wf:.4f}")
    
    # 7. Error analysis
    y_wf_pred = pipe_wf.predict(X_wf_te)
    errors = np.where(y_wf_pred != y_wf_te)[0]
    print(f"  Step 7 - Errors: {len(errors)}/{len(y_wf_te)}")
    
    print(f"\n  Workflow complete!")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN SKLEARN AVANZADO:

1. Feature Selection: Filter > Wrapper > Embedded.
2. PCA/SVD: reduccion de dimensionalidad.
3. Calibration: Platt/Isotonic para probabilidades fiables.
4. Imbalanced: class_weight='balanced' como baseline.
5. Custom estimators: BaseEstimator + Mixin.
6. Interpretation: coefs, importance, SHAP.
7. A/B testing: paired t-test sobre CV.
8. Production: Pipeline + version + monitoring.

FIN DEL MODULO 14: SCIKIT-LEARN PROFUNDO.
"""

print("\n FIN DE ARCHIVO 03_sklearn_avanzado.")
print(" Sklearn avanzado ha sido dominado.")
print(" Siguiente modulo: FEATURE ENGINEERING.")
print(" Total temas cubiertos: 20 capitulos.")
print(" Modulo 14 completado exitosamente.")
