# ===========================================================================
# 02_modelos_ensemble.py
# ===========================================================================
# MODULO 14: SCIKIT-LEARN PROFUNDO
# ARCHIVO 02: Ensemble Methods (Bagging, Boosting, Stacking)
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar Random Forest, AdaBoost, Gradient Boosting, XGBoost, Stacking.
#
# CONTENIDO:
#   1. Bagging conceptual.
#   2. Random Forest en detalle.
#   3. Feature importance (MDI, permutation).
#   4. AdaBoost.
#   5. Gradient Boosting.
#   6. XGBoost / LightGBM conceptual.
#   7. Stacking.
#   8. Voting.
#   9. Out-of-Bag estimation.
#   10. Hyperparameter tuning ensembles.
#   11. Comparison benchmark.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.ensemble import (
        RandomForestClassifier, RandomForestRegressor,
        GradientBoostingClassifier, GradientBoostingRegressor,
        AdaBoostClassifier, BaggingClassifier,
        StackingClassifier, VotingClassifier,
    )
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.linear_model import LogisticRegression, RidgeClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.model_selection import (
        train_test_split, cross_val_score, GridSearchCV,
    )
    from sklearn.datasets import make_classification, make_regression
    from sklearn.metrics import (
        accuracy_score, classification_report, f1_score,
        mean_squared_error, r2_score,
    )
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.inspection import permutation_importance
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("  (sklearn no disponible)")


# =====================================================================
#   PARTE 1: BAGGING
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: BAGGING ===")
print("=" * 80)

"""
BAGGING (Bootstrap Aggregating):
1. Crear N bootstrap samples (muestreo con reemplazo).
2. Entrenar un modelo en cada sample.
3. Combinar predicciones:
   - Clasificacion: voto mayoritario.
   - Regresion: promedio.

Reduce VARIANZA sin aumentar bias.
Funciona mejor con modelos de alta varianza (e.g. decision trees).
"""

if HAS_SKLEARN:
    print("\n--- Datos ---")
    
    X, y = make_classification(
        n_samples=2000, n_features=20, n_informative=12,
        n_redundant=4, n_classes=2, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"  Train: {X_train.shape}, Test: {X_test.shape}")
    
    
    print("\n--- BaggingClassifier ---")
    
    for n_estimators in [5, 10, 50, 100]:
        bag = BaggingClassifier(
            estimator=DecisionTreeClassifier(),
            n_estimators=n_estimators,
            max_samples=0.8,
            max_features=0.8,
            bootstrap=True,
            random_state=42,
            n_jobs=-1,
        )
        
        start = time.perf_counter()
        bag.fit(X_train, y_train)
        t = time.perf_counter() - start
        
        score = bag.score(X_test, y_test)
        print(f"  n={n_estimators:3d}: accuracy={score:.4f}, time={t:.3f}s")


# =====================================================================
#   PARTE 2: RANDOM FOREST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: RANDOM FOREST ===")
print("=" * 80)

"""
Random Forest = Bagging + Feature Subsampling.

Diferencia clave con Bagging:
  En cada split, solo considerar sqrt(d) features aleatorias.
  Esto DECORRELACIONA los arboles, reduciendo varianza aun mas.

Hiperparametros clave:
  - n_estimators: mas = mejor (diminishing returns).
  - max_depth: controlar overfitting.
  - min_samples_split/leaf: regularizacion.
  - max_features: 'sqrt' (clf) o 'log2'.
  - bootstrap: True (default).
"""

if HAS_SKLEARN:
    print("\n--- Random Forest basic ---")
    
    rf = RandomForestClassifier(
        n_estimators=100, max_depth=10, min_samples_split=5,
        max_features='sqrt', bootstrap=True, oob_score=True,
        random_state=42, n_jobs=-1,
    )
    
    start = time.perf_counter()
    rf.fit(X_train, y_train)
    t_rf = time.perf_counter() - start
    
    print(f"  Train accuracy: {rf.score(X_train, y_train):.4f}")
    print(f"  Test accuracy:  {rf.score(X_test, y_test):.4f}")
    print(f"  OOB score:      {rf.oob_score_:.4f}")
    print(f"  Time:           {t_rf:.3f}s")
    
    
    print("\n--- n_estimators sweep ---")
    
    for n_est in [10, 25, 50, 100, 200, 500]:
        rf_n = RandomForestClassifier(
            n_estimators=n_est, max_depth=10, random_state=42, n_jobs=-1
        )
        rf_n.fit(X_train, y_train)
        print(f"  n_estimators={n_est:3d}: test={rf_n.score(X_test, y_test):.4f}")
    
    
    print("\n--- max_depth sweep ---")
    
    for depth in [3, 5, 10, 15, 20, None]:
        rf_d = RandomForestClassifier(
            n_estimators=100, max_depth=depth, random_state=42, n_jobs=-1
        )
        rf_d.fit(X_train, y_train)
        train_s = rf_d.score(X_train, y_train)
        test_s = rf_d.score(X_test, y_test)
        d_str = f"{depth}" if depth else "None"
        print(f"  max_depth={d_str:>4s}: train={train_s:.4f}, test={test_s:.4f}, gap={train_s-test_s:.4f}")


# =====================================================================
#   PARTE 3: FEATURE IMPORTANCE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: FEATURE IMPORTANCE ===")
print("=" * 80)

"""
3 metodos:
1. MDI (Mean Decrease Impurity): .feature_importances_
   - Rapido, pero sesgado hacia features con alta cardinalidad.
2. Permutation importance: mezclar una feature y medir drop.
   - Mas fiable, pero mas lento.
3. SHAP: game-theoretic, per-sample.
"""

if HAS_SKLEARN:
    print("\n--- MDI importance ---")
    
    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    print(f"  Top 10 features:")
    for i in range(10):
        idx = indices[i]
        bar = "█" * int(importances[idx] * 100)
        print(f"    Feature {idx:2d}: {importances[idx]:.4f} {bar}")
    
    
    print("\n--- Permutation importance ---")
    
    perm_imp = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42)
    perm_sorted = np.argsort(perm_imp.importances_mean)[::-1]
    
    print(f"  Top 10 (permutation):")
    for i in range(10):
        idx = perm_sorted[i]
        imp = perm_imp.importances_mean[idx]
        std = perm_imp.importances_std[idx]
        print(f"    Feature {idx:2d}: {imp:.4f} ± {std:.4f}")
    
    # Compare rankings
    mdi_top5 = set(indices[:5])
    perm_top5 = set(perm_sorted[:5])
    overlap = len(mdi_top5 & perm_top5)
    print(f"\n  MDI vs Permutation top-5 overlap: {overlap}/5")


# =====================================================================
#   PARTE 4: ADABOOST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: ADABOOST ===")
print("=" * 80)

"""
AdaBoost (Adaptive Boosting):
1. Inicializar weights uniformes.
2. Entrenar weak learner en datos con weights.
3. Calcular error ponderado.
4. Dar mas peso a misclassified samples.
5. Repetir.

Prediccion: voto ponderado de weak learners.
"""

if HAS_SKLEARN:
    print("\n--- AdaBoost ---")
    
    for n_est in [10, 50, 100, 200]:
        ada = AdaBoostClassifier(
            estimator=DecisionTreeClassifier(max_depth=1),  # stumps
            n_estimators=n_est,
            learning_rate=1.0,
            random_state=42,
        )
        ada.fit(X_train, y_train)
        train_s = ada.score(X_train, y_train)
        test_s = ada.score(X_test, y_test)
        print(f"  n={n_est:3d}: train={train_s:.4f}, test={test_s:.4f}")
    
    
    print("\n--- Learning rate impact ---")
    
    for lr in [0.01, 0.1, 0.5, 1.0, 2.0]:
        ada_lr = AdaBoostClassifier(
            n_estimators=100, learning_rate=lr, random_state=42,
        )
        ada_lr.fit(X_train, y_train)
        print(f"  lr={lr:.2f}: test={ada_lr.score(X_test, y_test):.4f}")


# =====================================================================
#   PARTE 5: GRADIENT BOOSTING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: GRADIENT BOOSTING ===")
print("=" * 80)

"""
Gradient Boosting:
  Construir modelo additivamente: F(x) = sum(alpha_m * h_m(x))
  Cada h_m se ajusta al RESIDUO del modelo anterior.
  
  En cada step:
  1. Calcular pseudo-residuos (gradiente negativo de la loss).
  2. Fit un tree a los pseudo-residuos.
  3. Update: F(x) += lr * tree(x).

HIPERPARAMETROS:
  - n_estimators: numero de boosting stages.
  - learning_rate: shrinkage (tipico 0.01-0.1).
  - max_depth: profundidad de cada tree (tipico 3-8).
  - subsample: fraccion de datos por step (stochastic GB).
  - min_samples_leaf: regularizacion.
"""

if HAS_SKLEARN:
    print("\n--- Gradient Boosting ---")
    
    gb = GradientBoostingClassifier(
        n_estimators=200, learning_rate=0.1, max_depth=3,
        subsample=0.8, random_state=42,
    )
    
    start = time.perf_counter()
    gb.fit(X_train, y_train)
    t_gb = time.perf_counter() - start
    
    print(f"  Train: {gb.score(X_train, y_train):.4f}")
    print(f"  Test:  {gb.score(X_test, y_test):.4f}")
    print(f"  Time:  {t_gb:.3f}s")
    
    
    print("\n--- Staged performance ---")
    
    test_scores = list(gb.staged_score(X_test, y_test))
    print(f"  Performance at different stages:")
    for stage in [10, 50, 100, 150, 200]:
        if stage <= len(test_scores):
            print(f"    Stage {stage:3d}: {test_scores[stage-1]:.4f}")


# =====================================================================
#   PARTE 6: XGBOOST / LIGHTGBM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: XGBOOST / LIGHTGBM ===")
print("=" * 80)

"""
XGBOOST:
  - Regularized Gradient Boosting.
  - L1 + L2 regularizacion en leaf weights.
  - Newton-Raphson (2nd order gradient).
  - Missing values handled natively.
  - Column subsampling.
  - Parallel tree construction.

LIGHTGBM:
  - Gradient-based One-Side Sampling (GOSS).
  - Exclusive Feature Bundling (EFB).
  - Leaf-wise growth (vs level-wise XGBoost).
  - Faster training, handles large datasets.

CATBOOST:
  - Native categorical feature support.
  - Ordered Target Statistics.
  - Symmetric trees.
"""

try:
    import xgboost as xgb
    
    xgb_clf = xgb.XGBClassifier(
        n_estimators=200, max_depth=6, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        reg_alpha=0.1, reg_lambda=1.0,
        random_state=42, use_label_encoder=False, eval_metric='logloss',
    )
    xgb_clf.fit(X_train, y_train, verbose=False)
    
    print(f"  XGBoost test: {xgb_clf.score(X_test, y_test):.4f}")
except ImportError:
    print("  XGBoost not installed (pip install xgboost)")
    print("  Conceptual: XGB adds L1/L2 reg + 2nd order gradients")

try:
    import lightgbm as lgb
    
    lgb_clf = lgb.LGBMClassifier(
        n_estimators=200, max_depth=6, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8, verbose=-1,
        random_state=42,
    )
    lgb_clf.fit(X_train, y_train)
    
    print(f"  LightGBM test: {lgb_clf.score(X_test, y_test):.4f}")
except ImportError:
    print("  LightGBM not installed (pip install lightgbm)")
    print("  Conceptual: LGBM uses GOSS + EFB for speed")


# =====================================================================
#   PARTE 7: STACKING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: STACKING ===")
print("=" * 80)

"""
Stacking:
1. Train multiple base models.
2. Usar sus predictions como features para un meta-model.
3. El meta-model aprende a combinar optimamente.

REGLA: usar CV predictions como features para evitar leakage.
"""

if HAS_SKLEARN:
    print("\n--- StackingClassifier ---")
    
    estimators = [
        ('rf', RandomForestClassifier(n_estimators=50, random_state=42)),
        ('gb', GradientBoostingClassifier(n_estimators=50, random_state=42)),
        ('knn', KNeighborsClassifier(n_neighbors=5)),
    ]
    
    stacking = StackingClassifier(
        estimators=estimators,
        final_estimator=LogisticRegression(max_iter=1000),
        cv=5,
    )
    
    start = time.perf_counter()
    stacking.fit(X_train, y_train)
    t_stack = time.perf_counter() - start
    
    print(f"  Stacking test: {stacking.score(X_test, y_test):.4f}")
    print(f"  Time: {t_stack:.2f}s")
    
    # Individual base models
    for name, est in estimators:
        est.fit(X_train, y_train)
        print(f"    {name:>4s} alone: {est.score(X_test, y_test):.4f}")


# =====================================================================
#   PARTE 8: VOTING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: VOTING ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- VotingClassifier ---")
    
    voting_hard = VotingClassifier(
        estimators=[
            ('rf', RandomForestClassifier(n_estimators=50, random_state=42)),
            ('gb', GradientBoostingClassifier(n_estimators=50, random_state=42)),
            ('lr', LogisticRegression(max_iter=1000, random_state=42)),
        ],
        voting='hard',
    )
    
    voting_soft = VotingClassifier(
        estimators=[
            ('rf', RandomForestClassifier(n_estimators=50, random_state=42)),
            ('gb', GradientBoostingClassifier(n_estimators=50, random_state=42)),
            ('lr', LogisticRegression(max_iter=1000, random_state=42)),
        ],
        voting='soft',
    )
    
    voting_hard.fit(X_train, y_train)
    voting_soft.fit(X_train, y_train)
    
    print(f"  Hard voting: {voting_hard.score(X_test, y_test):.4f}")
    print(f"  Soft voting: {voting_soft.score(X_test, y_test):.4f}")


# =====================================================================
#   PARTE 9: OOB ESTIMATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: OOB ===")
print("=" * 80)

"""
Out-of-Bag:
  ~37% de datos no se usan en cada bootstrap sample.
  Usarlos como validation set GRATIS.
  
  OOB score ≈ CV score, pero sin costo adicional.
"""

if HAS_SKLEARN:
    rf_oob = RandomForestClassifier(
        n_estimators=200, oob_score=True, random_state=42, n_jobs=-1
    )
    rf_oob.fit(X_train, y_train)
    
    cv_score = cross_val_score(
        RandomForestClassifier(n_estimators=200, random_state=42),
        X_train, y_train, cv=5
    ).mean()
    
    print(f"  OOB score: {rf_oob.oob_score_:.4f}")
    print(f"  CV score:  {cv_score:.4f}")
    print(f"  Test score: {rf_oob.score(X_test, y_test):.4f}")
    print(f"  OOB ≈ CV (free validation!)")


# =====================================================================
#   PARTE 10: BENCHMARK
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: BENCHMARK ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- Model comparison ---")
    
    models = {
        'LogReg': LogisticRegression(max_iter=1000, random_state=42),
        'DecTree': DecisionTreeClassifier(max_depth=10, random_state=42),
        'RF': RandomForestClassifier(100, random_state=42, n_jobs=-1),
        'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=42),
        'GradBoost': GradientBoostingClassifier(100, random_state=42),
        'KNN': KNeighborsClassifier(5),
        'NaiveBayes': GaussianNB(),
    }
    
    print(f"  {'Model':>12s} {'Train':>7s} {'Test':>7s} {'CV':>7s} {'Time':>6s}")
    
    for name, model in models.items():
        start = time.perf_counter()
        model.fit(X_train, y_train)
        t = time.perf_counter() - start
        
        train_s = model.score(X_train, y_train)
        test_s = model.score(X_test, y_test)
        cv_s = cross_val_score(model, X_train, y_train, cv=3).mean()
        
        print(f"  {name:>12s} {train_s:7.4f} {test_s:7.4f} {cv_s:7.4f} {t:6.3f}s")


# =====================================================================
#   PARTE 11: ENSEMBLE REGRESSION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: ENSEMBLE REGRESSION ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- Regression ensembles ---")
    
    X_reg, y_reg = make_regression(
        n_samples=1000, n_features=10, n_informative=5, noise=10, random_state=42
    )
    X_reg_tr, X_reg_te, y_reg_tr, y_reg_te = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )
    
    reg_models = {
        'RF_Reg': RandomForestRegressor(100, random_state=42, n_jobs=-1),
        'GB_Reg': GradientBoostingRegressor(100, random_state=42),
    }
    
    for name, model in reg_models.items():
        model.fit(X_reg_tr, y_reg_tr)
        y_pred_reg = model.predict(X_reg_te)
        rmse = np.sqrt(mean_squared_error(y_reg_te, y_pred_reg))
        r2 = r2_score(y_reg_te, y_pred_reg)
        print(f"  {name:>10s}: RMSE={rmse:.2f}, R²={r2:.4f}")


# =====================================================================
#   PARTE 12: HISTGRADIENTBOOSTING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: HISTGRADIENTBOOSTING ===")
print("=" * 80)

"""
HistGradientBoosting: version optimizada de GB.
  - Bins features en histogramas (256 bins).
  - Mucho mas rapido que GradientBoosting.
  - Soporte nativo de NaN.
  - Similar a LightGBM.
"""

if HAS_SKLEARN:
    from sklearn.ensemble import HistGradientBoostingClassifier
    
    hgb = HistGradientBoostingClassifier(
        max_iter=200, learning_rate=0.1, max_depth=6,
        random_state=42,
    )
    
    start = time.perf_counter()
    hgb.fit(X_train, y_train)
    t_hgb = time.perf_counter() - start
    
    print(f"  HistGB test: {hgb.score(X_test, y_test):.4f}")
    print(f"  Time: {t_hgb:.3f}s (vs GB: {t_gb:.3f}s)")
    print(f"  Speedup: {t_gb/t_hgb:.1f}x")


# =====================================================================
#   PARTE 13: MAX_FEATURES COMPARISON
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: MAX_FEATURES ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- max_features impact ---")
    
    for mf in ['sqrt', 'log2', 0.3, 0.5, 0.8, 1.0]:
        rf_mf = RandomForestClassifier(
            n_estimators=100, max_features=mf, random_state=42, n_jobs=-1
        )
        rf_mf.fit(X_train, y_train)
        tr = rf_mf.score(X_train, y_train)
        te = rf_mf.score(X_test, y_test)
        print(f"  max_features={str(mf):>5s}: train={tr:.4f}, test={te:.4f}")


# =====================================================================
#   PARTE 14: WARM START
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: WARM START ===")
print("=" * 80)

"""
warm_start=True: continuar entrenamiento desde donde quedo.
Util para:
1. Incrementar n_estimators gradualmente.
2. Early stopping manual.
3. Monitorear convergencia.
"""

if HAS_SKLEARN:
    rf_warm = RandomForestClassifier(
        n_estimators=10, warm_start=True, random_state=42, n_jobs=-1
    )
    
    print(f"  Incremental training:")
    for n_est in [10, 50, 100, 200, 300]:
        rf_warm.n_estimators = n_est
        rf_warm.fit(X_train, y_train)
        score = rf_warm.score(X_test, y_test)
        print(f"    n_est={n_est:3d}: test={score:.4f}")


# =====================================================================
#   PARTE 15: ENSEMBLE IMBALANCED
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: IMBALANCED ===")
print("=" * 80)

if HAS_SKLEARN:
    X_imb, y_imb = make_classification(
        n_samples=2000, n_features=20, n_informative=10,
        weights=[0.9, 0.1], random_state=42
    )
    X_imb_tr, X_imb_te, y_imb_tr, y_imb_te = train_test_split(
        X_imb, y_imb, test_size=0.2, random_state=42, stratify=y_imb
    )
    
    imb_models = {
        'RF_default': RandomForestClassifier(100, random_state=42),
        'RF_balanced': RandomForestClassifier(100, class_weight='balanced', random_state=42),
        'RF_subsample': RandomForestClassifier(100, class_weight='balanced_subsample', random_state=42),
        'GB_default': GradientBoostingClassifier(100, random_state=42),
    }
    
    print(f"  {'Model':>16s} {'Acc':>6s} {'F1':>6s}")
    for name, model in imb_models.items():
        model.fit(X_imb_tr, y_imb_tr)
        y_p = model.predict(X_imb_te)
        acc = accuracy_score(y_imb_te, y_p)
        f1 = f1_score(y_imb_te, y_p)
        print(f"  {name:>16s} {acc:6.4f} {f1:6.4f}")


# =====================================================================
#   PARTE 16: EARLY STOPPING GB
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: EARLY STOPPING ===")
print("=" * 80)

if HAS_SKLEARN:
    gb_es = GradientBoostingClassifier(
        n_estimators=500, learning_rate=0.1, max_depth=3,
        validation_fraction=0.15, n_iter_no_change=10,
        random_state=42,
    )
    gb_es.fit(X_train, y_train)
    
    print(f"  Requested: 500 estimators")
    print(f"  Actual:    {gb_es.n_estimators_} (early stopped)")
    print(f"  Test:      {gb_es.score(X_test, y_test):.4f}")


# =====================================================================
#   PARTE 17: BLENDING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: BLENDING ===")
print("=" * 80)

"""
Blending: version simplificada de stacking.
1. Split train en train1 + val.
2. Fit base models en train1.
3. Predict en val -> meta features.
4. Fit meta model en meta features.
"""

if HAS_SKLEARN:
    # Split
    X_tr1, X_val, y_tr1, y_val = train_test_split(
        X_train, y_train, test_size=0.3, random_state=42
    )
    
    base_models = [
        RandomForestClassifier(100, random_state=42, n_jobs=-1),
        GradientBoostingClassifier(100, random_state=42),
        LogisticRegression(max_iter=1000, random_state=42),
    ]
    
    # Level 1
    meta_train = np.zeros((len(X_val), len(base_models)))
    meta_test = np.zeros((len(X_test), len(base_models)))
    
    for i, model in enumerate(base_models):
        model.fit(X_tr1, y_tr1)
        meta_train[:, i] = model.predict_proba(X_val)[:, 1]
        meta_test[:, i] = model.predict_proba(X_test)[:, 1]
    
    # Level 2
    meta_lr = LogisticRegression(max_iter=1000)
    meta_lr.fit(meta_train, y_val)
    blend_score = meta_lr.score(meta_test, y_test)
    
    print(f"  Blending test: {blend_score:.4f}")
    print(f"  Meta-model weights: {meta_lr.coef_.round(3)}")


# =====================================================================
#   PARTE 18: DIVERSITY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: DIVERSITY ===")
print("=" * 80)

"""
Ensemble diversity: los modelos deben hacer DIFERENTES errores.
Si todos predicen lo mismo, el ensemble no ayuda.

Medir: correlation entre predictions.
"""

if HAS_SKLEARN:
    div_models = [
        ('RF', RandomForestClassifier(100, random_state=42, n_jobs=-1)),
        ('GB', GradientBoostingClassifier(100, random_state=42)),
        ('LR', LogisticRegression(max_iter=1000, random_state=42)),
        ('KNN', KNeighborsClassifier(5)),
    ]
    
    predictions = {}
    for name, model in div_models:
        model.fit(X_train, y_train)
        predictions[name] = model.predict(X_test)
    
    # Pairwise agreement
    names = list(predictions.keys())
    print(f"  Pairwise agreement:")
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            agree = np.mean(predictions[names[i]] == predictions[names[j]])
            print(f"    {names[i]:>3s} vs {names[j]:>3s}: {agree:.4f}")


# =====================================================================
#   PARTE 19: TUNING GUIDE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: TUNING GUIDE ===")
print("=" * 80)

"""
RANDOM FOREST TUNING:
  1. n_estimators: mas es mejor (100-500).
  2. max_depth: None o 10-30.
  3. min_samples_split: 2-20.
  4. max_features: 'sqrt' (clasificacion), 0.3 (regresion).

GRADIENT BOOSTING TUNING:
  1. n_estimators + learning_rate: inversamente proporcionales.
  2. max_depth: 3-8 (shallow trees!).
  3. subsample: 0.5-0.9.
  4. min_samples_leaf: 5-50.
  5. Early stopping: validation_fraction + n_iter_no_change.
"""

print("  Tuning priorities:")
print("    RF:  n_estimators > max_depth > min_samples_split")
print("    GB:  lr*n_est > max_depth > subsample > min_samples_leaf")
print("    XGB: lr*n_est > max_depth > colsample > reg_alpha/lambda")


# =====================================================================
#   PARTE 20: ENSEMBLE CHEATSHEET
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: CHEATSHEET ===")
print("=" * 80)

"""
| Metodo     | Reduce | Speed  | Interpret | Best for          |
|------------|--------|--------|-----------|-------------------|
| Bagging    | Var    | Fast   | Low       | High-var models   |
| RF         | Var    | Fast   | Medium    | General baseline  |
| AdaBoost   | Bias   | Medium | Low       | Weak learners     |
| GB         | Bias   | Slow   | Medium    | Best performance  |
| XGBoost    | Bias   | Fast   | Medium    | Kaggle winner     |
| LightGBM   | Bias   | Fast   | Medium    | Large datasets    |
| Stacking   | Both   | Slow   | Low       | Final push        |
| Voting     | Var    | Fast   | Medium    | Simple ensemble   |
"""

cheat = [
    ("Bagging", "Variance", "Parallel", "RF baseline"),
    ("RF", "Variance", "Parallel", "Best baseline"),
    ("AdaBoost", "Bias", "Sequential", "Weak learners"),
    ("GB/XGB", "Bias", "Sequential", "Best performance"),
    ("Stacking", "Both", "2-level", "Final squeeze"),
]

print(f"\n  {'Method':>10s} {'Reduces':>10s} {'Training':>12s} {'Best for':>18s}")
for m, r, t, b in cheat:
    print(f"  {m:>10s} {r:>10s} {t:>12s} {b:>18s}")


# =====================================================================
#   PARTE 21: MIN_SAMPLES_LEAF SWEEP
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: MIN_SAMPLES_LEAF ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- RF min_samples_leaf ---")
    
    for msl in [1, 2, 5, 10, 20, 50]:
        rf_msl = RandomForestClassifier(
            n_estimators=100, min_samples_leaf=msl, random_state=42, n_jobs=-1
        )
        rf_msl.fit(X_train, y_train)
        tr = rf_msl.score(X_train, y_train)
        te = rf_msl.score(X_test, y_test)
        print(f"  min_samples_leaf={msl:2d}: train={tr:.4f}, test={te:.4f}, gap={tr-te:.4f}")


# =====================================================================
#   PARTE 22: REGRESSION BENCHMARK
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 22: REGRESSION BENCHMARK ===")
print("=" * 80)

if HAS_SKLEARN:
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    
    reg_bench = {
        'Linear': LinearRegression(),
        'Ridge': Ridge(alpha=1.0),
        'Lasso': Lasso(alpha=0.1),
        'RF_Reg': RandomForestRegressor(100, random_state=42, n_jobs=-1),
        'GB_Reg': GradientBoostingRegressor(100, random_state=42),
    }
    
    print(f"  {'Model':>10s} {'RMSE':>8s} {'R²':>7s}")
    for name, model in reg_bench.items():
        model.fit(X_reg_tr, y_reg_tr)
        y_pred_rb = model.predict(X_reg_te)
        rmse = np.sqrt(mean_squared_error(y_reg_te, y_pred_rb))
        r2 = r2_score(y_reg_te, y_pred_rb)
        print(f"  {name:>10s} {rmse:8.2f} {r2:7.4f}")


# =====================================================================
#   PARTE 23: ISOLATION FOREST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 23: ISOLATION FOREST ===")
print("=" * 80)

if HAS_SKLEARN:
    from sklearn.ensemble import IsolationForest
    
    # Add anomalies
    np.random.seed(42)
    X_normal = X_train[:200]
    X_anom = np.random.uniform(-10, 10, (20, X_train.shape[1]))
    X_with_anom = np.vstack([X_normal, X_anom])
    
    iso = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    labels = iso.fit_predict(X_with_anom)
    
    n_inliers = np.sum(labels == 1)
    n_outliers = np.sum(labels == -1)
    print(f"  Inliers: {n_inliers}, Outliers: {n_outliers}")
    print(f"  Expected outliers: ~22 (20 injected + ~2 natural)")


# =====================================================================
#   PARTE 24: FEATURE INTERACTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 24: FEATURE INTERACTION ===")
print("=" * 80)

"""
RF captures feature interactions naturally.
Detect interactions by measuring importance in pairs.
"""

if HAS_SKLEARN:
    rf_int = RandomForestClassifier(100, random_state=42, n_jobs=-1)
    rf_int.fit(X_train, y_train)
    
    # Top pairs by combined importance
    imp = rf_int.feature_importances_
    top5 = np.argsort(imp)[::-1][:5]
    
    print(f"  Top feature pairs (by combined importance):")
    for i in range(len(top5)):
        for j in range(i+1, len(top5)):
            fi, fj = top5[i], top5[j]
            combined = imp[fi] + imp[fj]
            print(f"    F{fi} x F{fj}: combined_imp={combined:.4f}")


# =====================================================================
#   PARTE 25: CONFIDENCE ESTIMATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 25: CONFIDENCE ===")
print("=" * 80)

"""
RF prediction confidence:
  predict_proba = fraction of trees voting for each class.
  Higher max probability = more confident.
"""

if HAS_SKLEARN:
    rf_conf = RandomForestClassifier(200, random_state=42, n_jobs=-1)
    rf_conf.fit(X_train, y_train)
    probas = rf_conf.predict_proba(X_test)
    max_proba = probas.max(axis=1)
    
    # Accuracy by confidence bin
    bins = [(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]
    y_pred_conf = rf_conf.predict(X_test)
    
    print(f"  Accuracy by confidence:")
    for lo, hi in bins:
        mask = (max_proba >= lo) & (max_proba < hi)
        if mask.sum() > 0:
            acc = accuracy_score(y_test[mask], y_pred_conf[mask])
            print(f"    [{lo:.1f}, {hi:.1f}): n={mask.sum():3d}, acc={acc:.4f}")
    
    print(f"\n  Higher confidence -> higher accuracy (expected)")
    print(f"  Mean confidence: {max_proba.mean():.4f}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN ENSEMBLE:

1. Bagging: reduce varianza (RF es bagging + feature subsampling).
2. Boosting: reduce bias (AdaBoost, GradBoost, XGBoost).
3. Random Forest: robusto, parallelizable, baseline excelente.
4. Gradient Boosting: mejor performance, mas tuning.
5. XGBoost/LightGBM: estado del arte para tabular data.
6. Stacking: combina modelos heterogeneos.
7. Voting: simple pero efectivo.
8. OOB: validacion gratuita en bagging.

REGLA DE ORO:
  Tabular data -> Random Forest o XGBoost.
  Deep Learning NO suele superar a GB en tabular.
"""

print("\n FIN DE ARCHIVO 02_modelos_ensemble.")
print(" Ensemble methods han sido dominados.")
