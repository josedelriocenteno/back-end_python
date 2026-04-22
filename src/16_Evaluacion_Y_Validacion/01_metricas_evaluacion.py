# ===========================================================================
# 01_metricas_evaluacion.py - MODULO 16: EVALUACION Y VALIDACION
# ===========================================================================
import numpy as np, warnings
warnings.filterwarnings('ignore')
try:
    from sklearn.metrics import *
    from sklearn.model_selection import *
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.svm import SVC
    from sklearn.datasets import make_classification, make_regression
    from sklearn.preprocessing import StandardScaler, label_binarize
    from sklearn.pipeline import Pipeline
    from sklearn.calibration import calibration_curve
    from sklearn.dummy import DummyClassifier
    HAS = True
except ImportError:
    HAS = False

# =====================================================================
#   PARTE 1: CLASSIFICATION METRICS
# =====================================================================
print("\n" + "="*80)
print("=== CAPITULO 1: CLASSIFICATION METRICS ===")
print("="*80)

"""
METRICAS DE CLASIFICACION:
1. Accuracy: (TP+TN)/(TP+TN+FP+FN). Useless con imbalanced.
2. Precision: TP/(TP+FP). De los predichos positivos, cuantos son correctos.
3. Recall (Sensitivity): TP/(TP+FN). De los positivos reales, cuantos detectamos.
4. F1: 2*P*R/(P+R). Harmonic mean de precision y recall.
5. F-beta: (1+b²)*P*R / (b²*P + R). beta>1 favors recall.
6. Specificity: TN/(TN+FP). Rate de negativos correctamente identificados.
7. MCC: Matthews Correlation Coefficient. [-1, 1]. Bueno para imbalanced.
8. Cohen's Kappa: acuerdo corregido por azar.
"""

if HAS:
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=10,
                                n_redundant=5, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_tr, y_tr)
    y_pred = lr.predict(X_te)
    y_proba = lr.predict_proba(X_te)[:, 1]
    
    print(f"\n  Accuracy:    {accuracy_score(y_te, y_pred):.4f}")
    print(f"  Precision:   {precision_score(y_te, y_pred):.4f}")
    print(f"  Recall:      {recall_score(y_te, y_pred):.4f}")
    print(f"  F1:          {f1_score(y_te, y_pred):.4f}")
    print(f"  MCC:         {matthews_corrcoef(y_te, y_pred):.4f}")
    print(f"  Cohen Kappa: {cohen_kappa_score(y_te, y_pred):.4f}")

# =====================================================================
#   PARTE 2: CONFUSION MATRIX
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 2: CONFUSION MATRIX ===")
print("="*80)

"""
Confusion Matrix:
              Predicted
              Neg    Pos
Actual  Neg [ TN     FP ]
        Pos [ FN     TP ]

TN: True Negative, FP: False Positive (Type I error)
FN: False Negative (Type II error), TP: True Positive
"""

if HAS:
    cm = confusion_matrix(y_te, y_pred)
    print(f"\n  Confusion Matrix:")
    print(f"    TN={cm[0,0]:3d}  FP={cm[0,1]:3d}")
    print(f"    FN={cm[1,0]:3d}  TP={cm[1,1]:3d}")
    
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
    print(f"\n  Normalized:")
    print(f"    {cm_norm[0,0]:.3f}  {cm_norm[0,1]:.3f}")
    print(f"    {cm_norm[1,0]:.3f}  {cm_norm[1,1]:.3f}")
    
    report = classification_report(y_te, y_pred)
    print(f"\n{report}")

# =====================================================================
#   PARTE 3: ROC / AUC
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 3: ROC / AUC ===")
print("="*80)

"""
ROC Curve: True Positive Rate vs False Positive Rate at all thresholds.
AUC: Area Under ROC Curve. 0.5 = random, 1.0 = perfect.

Ventajas:
  - Threshold-independent.
  - Funciona bien con balanced/imbalanced.
"""

if HAS:
    fpr, tpr, thresholds = roc_curve(y_te, y_proba)
    auc_score = roc_auc_score(y_te, y_proba)
    
    print(f"  AUC: {auc_score:.4f}")
    print(f"\n  ROC curve points:")
    for i in range(0, len(fpr), max(1, len(fpr)//8)):
        print(f"    FPR={fpr[i]:.3f}, TPR={tpr[i]:.3f}, thresh={thresholds[min(i, len(thresholds)-1)]:.3f}")

# =====================================================================
#   PARTE 4: PRECISION-RECALL CURVE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 4: PR CURVE ===")
print("="*80)

"""
PR Curve: Precision vs Recall at different thresholds.
Average Precision (AP): area under PR curve.

Mejor que ROC para datos MUY imbalanced.
"""

if HAS:
    prec_curve, rec_curve, _ = precision_recall_curve(y_te, y_proba)
    ap = average_precision_score(y_te, y_proba)
    print(f"  Average Precision: {ap:.4f}")

# =====================================================================
#   PARTE 5: THRESHOLD OPTIMIZATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 5: THRESHOLD ===")
print("="*80)

if HAS:
    best_f1, best_t = 0, 0.5
    print(f"  {'Thresh':>7s} {'Prec':>6s} {'Rec':>6s} {'F1':>6s}")
    for t in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
        yp = (y_proba >= t).astype(int)
        p = precision_score(y_te, yp, zero_division=0)
        r = recall_score(y_te, yp, zero_division=0)
        f = f1_score(y_te, yp, zero_division=0)
        if f > best_f1: best_f1, best_t = f, t
        print(f"  {t:7.2f} {p:6.4f} {r:6.4f} {f:6.4f}")
    print(f"\n  Best threshold: {best_t:.2f} (F1={best_f1:.4f})")

# =====================================================================
#   PARTE 6: CROSS-VALIDATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 6: CROSS-VALIDATION ===")
print("="*80)

"""
CV Strategies:
1. KFold: k particiones, cada una como test.
2. StratifiedKFold: mantiene class balance.
3. RepeatedStratifiedKFold: repetir para reducir varianza.
4. LeaveOneOut: n-1 train, 1 test. Costoso.
5. TimeSeriesSplit: respeta orden temporal.
6. GroupKFold: grupos no se mezclan entre train/test.
"""

if HAS:
    strategies = {
        'KFold(5)': KFold(5, shuffle=True, random_state=42),
        'Stratified(5)': StratifiedKFold(5, shuffle=True, random_state=42),
        'Stratified(10)': StratifiedKFold(10, shuffle=True, random_state=42),
    }
    
    print(f"  {'Strategy':>16s} {'Mean':>7s} {'Std':>7s}")
    for name, cv in strategies.items():
        scores = cross_val_score(LogisticRegression(max_iter=1000, random_state=42),
                                  X_tr, y_tr, cv=cv, scoring='accuracy')
        print(f"  {name:>16s} {scores.mean():7.4f} {scores.std():7.4f}")

# =====================================================================
#   PARTE 7: CROSS_VALIDATE (multiple metrics)
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 7: CROSS_VALIDATE ===")
print("="*80)

if HAS:
    cv_res = cross_validate(
        LogisticRegression(max_iter=1000, random_state=42),
        X_tr, y_tr, cv=5,
        scoring=['accuracy', 'f1', 'roc_auc'],
        return_train_score=True,
    )
    
    for m in ['accuracy', 'f1', 'roc_auc']:
        tr = cv_res[f'train_{m}'].mean()
        te = cv_res[f'test_{m}'].mean()
        print(f"  {m:>10s}: train={tr:.4f}, test={te:.4f}")

# =====================================================================
#   PARTE 8: TIMESERIESSPLIT
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 8: TIMESERIESSPLIT ===")
print("="*80)

"""
TimeSeriesSplit: expanding window CV.
  Split 1: [train] [test]
  Split 2: [train     ] [test]
  Split 3: [train          ] [test]
  
NUNCA datos futuros en training.
"""

if HAS:
    tscv = TimeSeriesSplit(n_splits=5)
    print(f"  TimeSeriesSplit folds:")
    for i, (tr_idx, te_idx) in enumerate(tscv.split(X_tr)):
        print(f"    Fold {i}: train={len(tr_idx)}, test={len(te_idx)}")

# =====================================================================
#   PARTE 9: REGRESSION METRICS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 9: REGRESSION METRICS ===")
print("="*80)

"""
1. MAE: Mean Absolute Error. Robusto a outliers.
2. MSE: Mean Squared Error. Penaliza outliers mas.
3. RMSE: sqrt(MSE). Mismas unidades que target.
4. R²: 1 - SS_res/SS_tot. 1=perfecto, 0=media, <0=peor que media.
5. MAPE: Mean Absolute Percentage Error. Interpretable.
6. Adjusted R²: R² corregido por n_features.
"""

if HAS:
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.ensemble import RandomForestRegressor
    
    X_reg, y_reg = make_regression(n_samples=500, n_features=10, noise=10, random_state=42)
    Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    
    reg = LinearRegression()
    reg.fit(Xr_tr, yr_tr)
    yr_pred = reg.predict(Xr_te)
    
    print(f"  MAE:  {mean_absolute_error(yr_te, yr_pred):.4f}")
    print(f"  MSE:  {mean_squared_error(yr_te, yr_pred):.4f}")
    print(f"  RMSE: {np.sqrt(mean_squared_error(yr_te, yr_pred)):.4f}")
    print(f"  R²:   {r2_score(yr_te, yr_pred):.4f}")
    
    # MAPE manual
    mape = np.mean(np.abs((yr_te - yr_pred) / (yr_te + 1e-10))) * 100
    print(f"  MAPE: {mape:.2f}%")

# =====================================================================
#   PARTE 10: MODEL COMPARISON
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 10: MODEL COMPARISON ===")
print("="*80)

if HAS:
    models = {
        'Dummy': DummyClassifier(strategy='stratified', random_state=42),
        'LogReg': LogisticRegression(max_iter=1000, random_state=42),
        'DTree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'RF': RandomForestClassifier(100, random_state=42, n_jobs=-1),
        'GB': GradientBoostingClassifier(100, random_state=42),
        'KNN': KNeighborsClassifier(5),
        'NB': GaussianNB(),
    }
    
    print(f"  {'Model':>8s} {'Acc':>6s} {'F1':>6s} {'AUC':>6s}")
    for name, model in models.items():
        model.fit(X_tr, y_tr)
        yp = model.predict(X_te)
        acc = accuracy_score(y_te, yp)
        f1 = f1_score(y_te, yp)
        auc = roc_auc_score(y_te, model.predict_proba(X_te)[:,1]) if hasattr(model,'predict_proba') else 0
        print(f"  {name:>8s} {acc:6.4f} {f1:6.4f} {auc:6.4f}")

# =====================================================================
#   PARTE 11: STATISTICAL COMPARISON
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 11: STATISTICAL TEST ===")
print("="*80)

if HAS:
    cv = StratifiedKFold(10, shuffle=True, random_state=42)
    s_a = cross_val_score(LogisticRegression(max_iter=1000,random_state=42), X_tr, y_tr, cv=cv)
    s_b = cross_val_score(RandomForestClassifier(100,random_state=42), X_tr, y_tr, cv=cv)
    diff = s_b - s_a
    t = diff.mean() / (diff.std()/np.sqrt(len(diff))) if diff.std()>0 else 0
    print(f"  LogReg: {s_a.mean():.4f} ± {s_a.std():.4f}")
    print(f"  RF:     {s_b.mean():.4f} ± {s_b.std():.4f}")
    print(f"  t-stat: {t:.4f}, significant: {abs(t) > 2.262}")

# =====================================================================
#   PARTE 12: LEARNING CURVES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 12: LEARNING CURVES ===")
print("="*80)

"""
Learning curves diagnostican:
  - High bias (underfit): train y val ambos bajos.
  - High variance (overfit): train alto, val bajo, gap grande.
  - Good fit: ambos altos, gap pequeño.
"""

if HAS:
    sizes, tr_scores, val_scores = learning_curve(
        LogisticRegression(max_iter=1000, random_state=42),
        X_tr, y_tr, train_sizes=[0.1, 0.3, 0.5, 0.7, 1.0], cv=5)
    
    print(f"  {'Size':>6s} {'Train':>7s} {'Val':>7s} {'Gap':>6s}")
    for s, t, v in zip(sizes, tr_scores.mean(1), val_scores.mean(1)):
        print(f"  {s:6d} {t:7.4f} {v:7.4f} {t-v:6.4f}")

# =====================================================================
#   PARTE 13: CALIBRATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 13: CALIBRATION ===")
print("="*80)

if HAS:
    models_cal = {
        'LogReg': LogisticRegression(max_iter=1000, random_state=42),
        'RF': RandomForestClassifier(100, random_state=42),
        'GB': GradientBoostingClassifier(100, random_state=42),
    }
    
    print(f"  {'Model':>8s} {'Brier':>7s} {'LogLoss':>8s}")
    for name, m in models_cal.items():
        m.fit(X_tr, y_tr)
        prob = m.predict_proba(X_te)[:,1]
        b = brier_score_loss(y_te, prob)
        ll = log_loss(y_te, prob)
        print(f"  {name:>8s} {b:7.4f} {ll:8.4f}")

# =====================================================================
#   PARTE 14: IMBALANCED METRICS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 14: IMBALANCED ===")
print("="*80)

if HAS:
    X_imb, y_imb = make_classification(n_samples=1000, weights=[0.9,0.1], random_state=42)
    Xi_tr, Xi_te, yi_tr, yi_te = train_test_split(X_imb, y_imb, test_size=0.2, stratify=y_imb, random_state=42)
    
    for name, m in [('Default', LogisticRegression(max_iter=1000,random_state=42)),
                     ('Balanced', LogisticRegression(max_iter=1000,class_weight='balanced',random_state=42))]:
        m.fit(Xi_tr, yi_tr)
        yp = m.predict(Xi_te)
        print(f"  {name:>10s}: acc={accuracy_score(yi_te,yp):.4f}, f1={f1_score(yi_te,yp):.4f}, "
              f"mcc={matthews_corrcoef(yi_te,yp):.4f}")

# =====================================================================
#   PARTE 15: REGRESSION COMPARISON
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 15: REG COMPARISON ===")
print("="*80)

if HAS:
    regs = {'Linear': LinearRegression(), 'Ridge': Ridge(1.0),
            'RF_Reg': RandomForestRegressor(100,random_state=42)}
    
    print(f"  {'Model':>8s} {'RMSE':>8s} {'R²':>7s}")
    for name, m in regs.items():
        m.fit(Xr_tr, yr_tr)
        yp = m.predict(Xr_te)
        rmse = np.sqrt(mean_squared_error(yr_te, yp))
        r2 = r2_score(yr_te, yp)
        print(f"  {name:>8s} {rmse:8.2f} {r2:7.4f}")

# =====================================================================
#   PARTE 16: VALIDATION STRATEGIES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 16: VALIDATION ===")
print("="*80)

"""
VALIDATION STRATEGIES:
1. Hold-out: simple split. Fast, high variance.
2. K-Fold CV: k splits. Standard.
3. Stratified K-Fold: preserve class balance.
4. Repeated CV: reduce variance.
5. Nested CV: unbiased estimate with tuning.
6. Time-based: for temporal data.
7. Group-based: groups don't leak.
"""

print("  Strategy guide:")
strategies = [
    ("Hold-out", "Fast", "High variance", "Prototyping"),
    ("K-Fold", "Standard", "Moderate", "Default"),
    ("Stratified", "Standard", "Low", "Imbalanced"),
    ("Repeated", "Slow", "Very low", "Final eval"),
    ("Nested CV", "Very slow", "Minimal", "With tuning"),
    ("TimeSeries", "Standard", "Low", "Temporal data"),
]
print(f"  {'Method':>12s} {'Speed':>8s} {'Variance':>10s} {'Use':>14s}")
for m, s, v, u in strategies:
    print(f"  {m:>12s} {s:>8s} {v:>10s} {u:>14s}")

# =====================================================================
#   PARTE 17: NESTED CV
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 17: NESTED CV ===")
print("="*80)

"""
Nested CV: outer loop evaluates, inner loop tunes.
Gives unbiased performance estimate even with hyperparameter tuning.
"""

if HAS:
    from sklearn.model_selection import GridSearchCV
    
    inner_cv = StratifiedKFold(3, shuffle=True, random_state=42)
    outer_cv = StratifiedKFold(5, shuffle=True, random_state=42)
    
    param_grid = {'C': [0.1, 1, 10]}
    grid = GridSearchCV(LogisticRegression(max_iter=1000,random_state=42),
                         param_grid, cv=inner_cv, scoring='accuracy')
    
    nested_scores = cross_val_score(grid, X_tr, y_tr, cv=outer_cv)
    print(f"  Nested CV: {nested_scores.mean():.4f} ± {nested_scores.std():.4f}")

# =====================================================================
#   PARTE 18: CUSTOM SCORING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 18: CUSTOM SCORING ===")
print("="*80)

if HAS:
    def profit(y_true, y_pred):
        tp = np.sum((y_true==1)&(y_pred==1))
        fp = np.sum((y_true==0)&(y_pred==1))
        fn = np.sum((y_true==1)&(y_pred==0))
        return tp*100 - fp*50 - fn*200
    
    profit_scorer = make_scorer(profit)
    scores_p = cross_val_score(LogisticRegression(max_iter=1000,random_state=42),
                                X_tr, y_tr, cv=5, scoring=profit_scorer)
    print(f"  Profit score: {scores_p.mean():.0f}")

# =====================================================================
#   PARTE 19: MULTICLASS METRICS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 19: MULTICLASS ===")
print("="*80)

if HAS:
    X_mc, y_mc = make_classification(n_samples=500, n_features=15, n_informative=8,
                                      n_classes=3, n_clusters_per_class=1, random_state=42)
    Xm_tr, Xm_te, ym_tr, ym_te = train_test_split(X_mc, y_mc, test_size=0.2, random_state=42)
    
    lr_mc = LogisticRegression(max_iter=1000, random_state=42)
    lr_mc.fit(Xm_tr, ym_tr)
    ym_pred = lr_mc.predict(Xm_te)
    
    for avg in ['micro', 'macro', 'weighted']:
        f1 = f1_score(ym_te, ym_pred, average=avg)
        print(f"  F1 ({avg:>8s}): {f1:.4f}")

# =====================================================================
#   PARTE 20: BEST PRACTICES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 20: BEST PRACTICES ===")
print("="*80)

"""
EVALUATION BEST PRACTICES:

1. ALWAYS start with dummy baseline.
2. Use MULTIPLE metrics (not just accuracy).
3. Use STRATIFIED CV for classification.
4. Report mean ± std from CV.
5. Use NESTED CV when tuning hyperparameters.
6. Check CALIBRATION for probability estimates.
7. Use PAIRED tests for model comparison.
8. Final evaluation on HOLD-OUT test set (once!).
9. For imbalanced: use F1, MCC, PR-AUC.
10. For regression: RMSE + R² + residual analysis.
"""

checklist = [
    ("Dummy baseline", True), ("Multiple metrics", True),
    ("Stratified CV", True), ("Mean ± std", True),
    ("Nested CV for tuning", True), ("Calibration", True),
    ("Statistical tests", True), ("Hold-out final", True),
]
print(f"\n  Evaluation checklist:")
for item, done in checklist:
    print(f"    {'✓' if done else '✗'} {item}")


# =====================================================================
#   PARTE 21: RESIDUAL ANALYSIS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 21: RESIDUAL ANALYSIS ===")
print("="*80)

"""
Residual analysis (regresion):
1. Residuals should be normally distributed.
2. No pattern in residuals vs predicted.
3. Constant variance (homoscedasticity).
4. No autocorrelation.
"""

if HAS:
    residuals = yr_te - yr_pred
    print(f"  Residual stats:")
    print(f"    Mean: {residuals.mean():.4f} (should be ~0)")
    print(f"    Std:  {residuals.std():.4f}")
    print(f"    Skew: {float(np.mean(((residuals - residuals.mean())/residuals.std())**3)):.4f}")
    
    # Residuals by prediction quartile
    quartiles = np.percentile(yr_pred, [25, 50, 75])
    q_labels = ['Q1', 'Q2', 'Q3', 'Q4']
    bounds = [-np.inf] + list(quartiles) + [np.inf]
    print(f"\n  Residuals by prediction quartile:")
    for i in range(4):
        mask = (yr_pred >= bounds[i]) & (yr_pred < bounds[i+1])
        if mask.sum() > 0:
            print(f"    {q_labels[i]}: mean={residuals[mask].mean():.2f}, std={residuals[mask].std():.2f}")


# =====================================================================
#   PARTE 22: ADJUSTED R²
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 22: ADJUSTED R² ===")
print("="*80)

if HAS:
    n = len(yr_te)
    p = Xr_te.shape[1]
    r2 = r2_score(yr_te, yr_pred)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    print(f"  R²:          {r2:.4f}")
    print(f"  Adjusted R²: {adj_r2:.4f}")
    print(f"  Difference:  {r2 - adj_r2:.4f}")
    print(f"  n={n}, p={p}")


# =====================================================================
#   PARTE 23: OVERFITTING DETECTION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 23: OVERFITTING ===")
print("="*80)

if HAS:
    print(f"\n  Overfitting detection:")
    for name, m in [('DTree_d3', DecisionTreeClassifier(max_depth=3,random_state=42)),
                     ('DTree_d10', DecisionTreeClassifier(max_depth=10,random_state=42)),
                     ('DTree_none', DecisionTreeClassifier(max_depth=None,random_state=42)),
                     ('RF_100', RandomForestClassifier(100,random_state=42))]:
        m.fit(X_tr, y_tr)
        tr_acc = m.score(X_tr, y_tr)
        te_acc = m.score(X_te, y_te)
        gap = tr_acc - te_acc
        status = "OVERFIT" if gap > 0.05 else "OK"
        print(f"    {name:>12s}: train={tr_acc:.4f}, test={te_acc:.4f}, gap={gap:.4f} [{status}]")


# =====================================================================
#   PARTE 24: F-BETA SWEEP
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 24: F-BETA ===")
print("="*80)

"""
F-beta: generalisation of F1.
  beta=0.5: precision-weighted (fraud detection, spam)
  beta=1.0: balanced (F1)
  beta=2.0: recall-weighted (medical diagnosis)
"""

if HAS:
    print(f"  {'Beta':>6s} {'F-beta':>7s}")
    for beta in [0.5, 1.0, 1.5, 2.0, 3.0]:
        fb = fbeta_score(y_te, y_pred, beta=beta)
        print(f"  {beta:6.1f} {fb:7.4f}")


# =====================================================================
#   PARTE 25: GROUPKFOLD
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 25: GROUPKFOLD ===")
print("="*80)

"""
GroupKFold: groups never split between train/test.
Use when: same customer in train and test = leakage.
"""

if HAS:
    groups = np.random.randint(0, 20, len(X_tr))
    gkf = GroupKFold(n_splits=5)
    
    print(f"  GroupKFold splits:")
    for i, (tr_idx, te_idx) in enumerate(gkf.split(X_tr, y_tr, groups)):
        tr_groups = set(groups[tr_idx])
        te_groups = set(groups[te_idx])
        overlap = tr_groups & te_groups
        print(f"    Fold {i}: train_groups={len(tr_groups)}, test_groups={len(te_groups)}, overlap={len(overlap)}")


# =====================================================================
#   PARTE 26: REPEATED CV
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 26: REPEATED CV ===")
print("="*80)

if HAS:
    rcv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
    scores_rcv = cross_val_score(LogisticRegression(max_iter=1000,random_state=42),
                                  X_tr, y_tr, cv=rcv, scoring='accuracy')
    print(f"  Repeated 5x3 CV: {scores_rcv.mean():.4f} ± {scores_rcv.std():.4f}")
    print(f"  Total fits: {len(scores_rcv)}")


# =====================================================================
#   PARTE 27: VALIDATION CURVES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 27: VALIDATION CURVES ===")
print("="*80)

if HAS:
    param_range = [0.001, 0.01, 0.1, 1, 10, 100]
    train_sc, test_sc = validation_curve(
        LogisticRegression(max_iter=1000,random_state=42),
        X_tr, y_tr, param_name='C', param_range=param_range, cv=5)
    
    print(f"  {'C':>7s} {'Train':>7s} {'Test':>7s} {'Gap':>6s}")
    for c, tr, te in zip(param_range, train_sc.mean(1), test_sc.mean(1)):
        print(f"  {c:7.3f} {tr:7.4f} {te:7.4f} {tr-te:6.4f}")


# =====================================================================
#   PARTE 28: ERROR ANALYSIS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 28: ERROR ANALYSIS ===")
print("="*80)

if HAS:
    errors = y_te != y_pred
    correct = ~errors
    
    print(f"  Error analysis:")
    print(f"    Total errors: {errors.sum()}/{len(y_te)}")
    print(f"    Error rate: {errors.mean():.4f}")
    
    # Confidence on errors
    y_prob_max = np.max(lr.predict_proba(X_te), axis=1)
    print(f"\n  Confidence analysis:")
    print(f"    Correct: mean_conf={y_prob_max[correct].mean():.4f}")
    print(f"    Errors:  mean_conf={y_prob_max[errors].mean():.4f}")
    
    # High confidence errors
    high_conf_errors = errors & (y_prob_max > 0.8)
    print(f"    High-confidence errors: {high_conf_errors.sum()}")


# =====================================================================
#   PARTE 29: COST MATRIX
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 29: COST MATRIX ===")
print("="*80)

"""
Cost matrix: assign different costs to different errors.
  
           Pred=0  Pred=1
Actual=0 [  0      c_fp ]    (cost of false alarm)
Actual=1 [ c_fn     0   ]    (cost of missing positive)

Total cost = FP * c_fp + FN * c_fn
"""

if HAS:
    cm_eval = confusion_matrix(y_te, y_pred)
    
    scenarios = [
        ("Equal cost", 1, 1),
        ("FN costly (medical)", 1, 10),
        ("FP costly (spam)", 10, 1),
    ]
    
    print(f"  {'Scenario':>20s} {'FP':>4s} {'FN':>4s} {'Cost':>6s}")
    for name, c_fp, c_fn in scenarios:
        cost = cm_eval[0,1]*c_fp + cm_eval[1,0]*c_fn
        print(f"  {name:>20s} {cm_eval[0,1]:4d} {cm_eval[1,0]:4d} {cost:6d}")


# =====================================================================
#   PARTE 30: YOUDEN INDEX
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 30: YOUDEN INDEX ===")
print("="*80)

"""
Youden's J = Sensitivity + Specificity - 1 = TPR - FPR
Optimal threshold maximizes J.
"""

if HAS:
    j_scores = tpr - fpr
    best_idx = np.argmax(j_scores)
    best_j = j_scores[best_idx]
    best_j_thresh = thresholds[min(best_idx, len(thresholds)-1)]
    
    print(f"  Youden's J: {best_j:.4f}")
    print(f"  Optimal threshold: {best_j_thresh:.4f}")
    print(f"  At this point: TPR={tpr[best_idx]:.4f}, FPR={fpr[best_idx]:.4f}")


# =====================================================================
#   PARTE 31: LIFT / GAIN
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 31: LIFT / GAIN ===")
print("="*80)

"""
Cumulative Gain: % of positives captured by top-k% predictions.
Lift: gain / baseline (random model).
"""

if HAS:
    sorted_idx = np.argsort(y_proba)[::-1]
    y_sorted = y_te[sorted_idx]
    cumsum = np.cumsum(y_sorted)
    total_pos = y_te.sum()
    
    print(f"  Cumulative gain:")
    for pct in [10, 20, 30, 50, 100]:
        n = int(len(y_te) * pct / 100)
        gain = cumsum[n-1] / total_pos * 100
        lift = gain / pct
        print(f"    Top {pct:3d}%: captures {gain:.1f}% of positives (lift={lift:.2f}x)")


# =====================================================================
#   PARTE 32: MULTI-METRIC DASHBOARD
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 32: DASHBOARD ===")
print("="*80)

if HAS:
    def model_dashboard(name, y_true, y_pred, y_proba):
        """Print comprehensive evaluation dashboard."""
        print(f"\n  === {name} ===")
        print(f"    Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
        print(f"    Precision: {precision_score(y_true, y_pred):.4f}")
        print(f"    Recall:    {recall_score(y_true, y_pred):.4f}")
        print(f"    F1:        {f1_score(y_true, y_pred):.4f}")
        print(f"    MCC:       {matthews_corrcoef(y_true, y_pred):.4f}")
        print(f"    AUC:       {roc_auc_score(y_true, y_proba):.4f}")
        print(f"    Brier:     {brier_score_loss(y_true, y_proba):.4f}")
        print(f"    LogLoss:   {log_loss(y_true, y_proba):.4f}")
    
    for name, m in [('LogReg', LogisticRegression(max_iter=1000,random_state=42)),
                     ('RF', RandomForestClassifier(100,random_state=42))]:
        m.fit(X_tr, y_tr)
        model_dashboard(name, y_te, m.predict(X_te), m.predict_proba(X_te)[:,1])


# =====================================================================
#   PARTE 33: CROSS_VAL_PREDICT
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 33: CROSS_VAL_PREDICT ===")
print("="*80)

if HAS:
    oof_pred = cross_val_predict(LogisticRegression(max_iter=1000,random_state=42),
                                  X_tr, y_tr, cv=5, method='predict_proba')[:,1]
    oof_acc = accuracy_score(y_tr, (oof_pred >= 0.5).astype(int))
    oof_auc = roc_auc_score(y_tr, oof_pred)
    print(f"  OOF accuracy: {oof_acc:.4f}")
    print(f"  OOF AUC:      {oof_auc:.4f}")


# =====================================================================
#   PARTE 34: METRIC CHEATSHEET
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 34: CHEATSHEET ===")
print("="*80)

guide = [
    ("Balanced clf", "Accuracy + F1 + AUC"),
    ("Imbalanced clf", "F1 + MCC + PR-AUC"),
    ("Ranking", "AUC + NDCG"),
    ("Probability", "Brier + LogLoss + calibration"),
    ("Regression", "RMSE + R² + MAE"),
    ("Business", "Custom scorer (profit/cost)"),
    ("Medical", "Recall + F2 + specificity"),
    ("Fraud", "Precision + F0.5 + lift"),
]

print(f"\n  {'Use Case':>16s} {'Metrics':>30s}")
for case, metrics in guide:
    print(f"  {case:>16s} {metrics:>30s}")


# =====================================================================
#   PARTE 35: FINAL EVALUATION PROTOCOL
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 35: PROTOCOL ===")
print("="*80)

"""
PRODUCTION EVALUATION PROTOCOL:

1. Split data: train (70%) / validation (15%) / test (15%).
2. Feature engineering on train only.
3. Model selection with CV on train.
4. Hyperparameter tuning with nested CV.
5. Final model: retrain on train+validation.
6. Evaluate ONCE on test set.
7. Report confidence intervals.
8. Compare against baseline.
9. Document everything.
"""

protocol = [
    "1. Holdout test set (NEVER touch during development)",
    "2. Use CV for model selection and tuning",
    "3. Report multiple metrics",
    "4. Include dummy baseline",
    "5. Statistical significance testing",
    "6. Error analysis on misclassifications",
    "7. Calibration check if using probabilities",
    "8. Learning curves for bias/variance diagnosis",
    "9. Final evaluation on test (ONE time only)",
    "10. Document metric choices and rationale",
]

print(f"\n  Evaluation protocol:")
for step in protocol:
    print(f"    ✓ {step}")


# =====================================================================
#   PARTE 36: CONFIDENCE INTERVALS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 36: CONFIDENCE INTERVALS ===")
print("="*80)

"""
Bootstrap confidence intervals for metrics.
1. Resample test set with replacement.
2. Compute metric on each resample.
3. Report percentile CI.
"""

if HAS:
    def bootstrap_ci(y_true, y_pred, metric_fn, n_bootstrap=1000, ci=0.95):
        scores = []
        for _ in range(n_bootstrap):
            idx = np.random.choice(len(y_true), len(y_true), replace=True)
            scores.append(metric_fn(y_true[idx], y_pred[idx]))
        lower = np.percentile(scores, (1-ci)/2 * 100)
        upper = np.percentile(scores, (1+ci)/2 * 100)
        return np.mean(scores), lower, upper
    
    for name, fn in [('Accuracy', accuracy_score), ('F1', f1_score)]:
        mean, lo, hi = bootstrap_ci(y_te, y_pred, fn, n_bootstrap=500)
        print(f"  {name}: {mean:.4f} [{lo:.4f}, {hi:.4f}]")


# =====================================================================
#   PARTE 37: STRATIFIED COMPARISON
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 37: STRATIFIED COMPARE ===")
print("="*80)

if HAS:
    # Compare models across different data subsets
    X_feature_0 = X_te[:, 0]
    median_f0 = np.median(X_feature_0)
    
    for subset_name, mask in [('F0 < median', X_feature_0 < median_f0),
                               ('F0 >= median', X_feature_0 >= median_f0)]:
        if mask.sum() > 10:
            acc = accuracy_score(y_te[mask], y_pred[mask])
            print(f"  {subset_name}: n={mask.sum()}, acc={acc:.4f}")


# =====================================================================
#   PARTE 38: MULTICLASS ROC
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 38: MULTICLASS ROC ===")
print("="*80)

"""
Multiclass ROC: One-vs-Rest (OvR) strategy.
Compute ROC for each class vs all others.
Average: macro, micro, weighted.
"""

if HAS:
    ym_proba = lr_mc.predict_proba(Xm_te)
    
    # OvR AUC
    ym_bin = label_binarize(ym_te, classes=[0, 1, 2])
    
    for i in range(3):
        auc_i = roc_auc_score(ym_bin[:, i], ym_proba[:, i])
        print(f"  Class {i} AUC: {auc_i:.4f}")
    
    # Macro average
    macro_auc = roc_auc_score(ym_bin, ym_proba, average='macro', multi_class='ovr')
    print(f"  Macro AUC: {macro_auc:.4f}")


# =====================================================================
#   PARTE 39: CALIBRATION CURVE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 39: CALIBRATION CURVE ===")
print("="*80)

"""
Calibration: predicted probability should match actual frequency.
If model says P=0.8, then ~80% should be positive.

Perfectly calibrated: line y=x.
RF tends to push probabilities to 0 and 1 (overconfident).
LogReg is well calibrated by default.
"""

if HAS:
    for name, m in [('LogReg', LogisticRegression(max_iter=1000,random_state=42)),
                     ('RF', RandomForestClassifier(100,random_state=42))]:
        m.fit(X_tr, y_tr)
        prob = m.predict_proba(X_te)[:, 1]
        fraction_pos, mean_predicted = calibration_curve(y_te, prob, n_bins=5)
        
        print(f"\n  {name} calibration:")
        print(f"    {'Predicted':>10s} {'Actual':>8s} {'Gap':>6s}")
        for mp, fp in zip(mean_predicted, fraction_pos):
            print(f"    {mp:10.3f} {fp:8.3f} {abs(mp-fp):6.3f}")


# =====================================================================
#   PARTE 40: PERMUTATION TEST
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 40: PERMUTATION TEST ===")
print("="*80)

"""
Permutation test: shuffle labels to create null distribution.
If model score > 95% of permuted scores, it's significant.
"""

if HAS:
    real_score = cross_val_score(LogisticRegression(max_iter=1000,random_state=42),
                                  X_tr[:200], y_tr[:200], cv=3).mean()
    
    n_perms = 50
    perm_scores = []
    for _ in range(n_perms):
        y_perm = np.random.permutation(y_tr[:200])
        s = cross_val_score(LogisticRegression(max_iter=1000,random_state=42),
                             X_tr[:200], y_perm, cv=3).mean()
        perm_scores.append(s)
    
    p_value = np.mean(np.array(perm_scores) >= real_score)
    print(f"  Real score: {real_score:.4f}")
    print(f"  Perm mean:  {np.mean(perm_scores):.4f}")
    print(f"  p-value:    {p_value:.4f}")
    print(f"  Significant: {p_value < 0.05}")


# =====================================================================
#   PARTE 41: BOOTSTRAP EVALUATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 41: BOOTSTRAP EVAL ===")
print("="*80)

if HAS:
    n_boot = 100
    boot_scores = {'acc': [], 'f1': [], 'auc': []}
    
    for _ in range(n_boot):
        idx = np.random.choice(len(X_te), len(X_te), replace=True)
        boot_scores['acc'].append(accuracy_score(y_te[idx], y_pred[idx]))
        boot_scores['f1'].append(f1_score(y_te[idx], y_pred[idx]))
        boot_scores['auc'].append(roc_auc_score(y_te[idx], y_proba[idx]))
    
    print(f"  Bootstrap evaluation (n={n_boot}):")
    for metric, scores in boot_scores.items():
        scores = np.array(scores)
        print(f"    {metric:>4s}: {scores.mean():.4f} ± {scores.std():.4f} "
              f"[{np.percentile(scores,2.5):.4f}, {np.percentile(scores,97.5):.4f}]")


# =====================================================================
#   PARTE 42: SUMMARY TABLE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 42: SUMMARY ===")
print("="*80)

"""
RESUMEN MODULO 16:

CLASIFICACION:
  Accuracy, Precision, Recall, F1, F-beta, MCC, Cohen Kappa
  ROC/AUC, PR/AP, Brier, LogLoss, Calibration
  Confusion Matrix, Cost Matrix, Youden, Lift/Gain

REGRESION:
  MAE, MSE, RMSE, R², Adjusted R², MAPE
  Residual analysis

VALIDACION:
  K-Fold, Stratified, Repeated, Nested, TimeSeries, Group
  Learning curves, Validation curves
  Bootstrap CI, Permutation test

COMPARACION:
  Paired t-test, Cross-validated comparison
  Multi-metric dashboard

FIN DE FASE 3: MACHINE LEARNING CLASICO.
"""

summary = [
    ("Clasificacion", "20+ metricas cubiertas"),
    ("Regresion", "6 metricas + residual analysis"),
    ("CV strategies", "7 estrategias implementadas"),
    ("Model comparison", "Statistical + visual"),
    ("Calibration", "Brier + calibration curves"),
    ("Production", "Protocol + CI + bootstrap"),
]

print(f"\n  {'Area':>16s} {'Coverage':>30s}")
for area, coverage in summary:
    print(f"  {area:>16s} {coverage:>30s}")



print("\n" + "="*80)
print("=== CONCLUSION ===")
print("="*80)
print("\n FIN DE ARCHIVO 01_metricas_evaluacion.")
print(" Evaluacion y validacion dominados.")
print(" FIN MODULO 16 / FIN FASE 3: ML CLASICO.")
