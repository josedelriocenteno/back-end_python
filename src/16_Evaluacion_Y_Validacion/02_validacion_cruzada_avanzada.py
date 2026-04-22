# ===========================================================================
# 02_validacion_cruzada_avanzada.py
# ===========================================================================
# MODULO 16: EVALUACION Y VALIDACION
# ARCHIVO 02: Validacion Cruzada Avanzada, Diagnostico, Comparacion
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar validacion cruzada mas alla de KFold basico:
# nested CV, group-aware splits, time series splits,
# learning curves, diagnostico de overfitting, y comparacion
# estadistica rigurosa de modelos.
#
# CONTENIDO:
#   1. Repaso rapido: por que cross-validation.
#   2. StratifiedKFold, RepeatedStratifiedKFold.
#   3. GroupKFold: cuando hay grupos (pacientes, usuarios).
#   4. TimeSeriesSplit: datos temporales.
#   5. Leave-One-Out (LOO): caso extremo.
#   6. Nested Cross-Validation: la forma CORRECTA de evaluar.
#   7. Learning Curves: diagnostico visual.
#   8. Validation Curves: efecto de hiperparametros.
#   9. Comparacion estadistica de modelos.
#   10. Permutation test: es mi modelo mejor que azar?
#   11. Calibration: las probabilidades son confiables?
#   12. Patrones de produccion: CV reproducible.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import warnings
warnings.filterwarnings("ignore")

try:
    from sklearn.model_selection import (
        cross_val_score, cross_validate,
        StratifiedKFold, RepeatedStratifiedKFold,
        GroupKFold, LeaveOneGroupOut,
        TimeSeriesSplit, LeaveOneOut,
        learning_curve, validation_curve,
        permutation_test_score,
    )
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.ensemble import (
        RandomForestClassifier, GradientBoostingClassifier,
        AdaBoostClassifier
    )
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.datasets import make_classification, make_regression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import (
        accuracy_score, f1_score, make_scorer,
        roc_auc_score, mean_squared_error
    )
    from scipy import stats
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("  sklearn no disponible.")


# =====================================================================
#   PARTE 1: POR QUE CROSS-VALIDATION
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: POR QUE CROSS-VALIDATION ===")
print("=" * 80)

"""
EL PROBLEMA de un solo train/test split:

1. Tu score depende de QUE datos cayeron en test.
   Cambia random_state y el accuracy cambia ±5%.
   → No puedes confiar en un solo numero.

2. Desperdicias datos. Si tienes 1000 muestras y usas 200 para test,
   entrenas con solo 800. Con pocos datos, esto duele.

3. No mides VARIANZA del modelo. Un accuracy de 0.85 puede ser:
   - Consistente: 0.83, 0.85, 0.86, 0.85, 0.84 → confiable.
   - Inestable: 0.70, 0.95, 0.80, 0.90, 0.75 → NO confiable.

CROSS-VALIDATION resuelve todo:
  - Cada dato se usa para train Y test (en distintos folds).
  - Obtienes media ± std del score.
  - Con K=5: 5 modelos, 5 scores, 1 estimacion robusta.

REGLA DE ORO:
  NUNCA reportes un score sin intervalo de confianza.
  "Accuracy: 0.85" → MALO.
  "Accuracy: 0.85 ± 0.03 (5-fold CV)" → BIEN.
"""

if HAS_SKLEARN:
    # Crear datos
    X, y = make_classification(
        n_samples=1000, n_features=20, n_informative=10,
        n_redundant=5, n_classes=2, random_state=42
    )

    print("\n--- Inestabilidad de un solo split ---")
    from sklearn.model_selection import train_test_split

    scores_single = []
    for seed in range(20):
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=0.2, random_state=seed
        )
        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(X_tr, y_tr)
        scores_single.append(lr.score(X_te, y_te))

    print(f"  20 splits diferentes:")
    print(f"    Min:  {min(scores_single):.4f}")
    print(f"    Max:  {max(scores_single):.4f}")
    print(f"    Mean: {np.mean(scores_single):.4f}")
    print(f"    Std:  {np.std(scores_single):.4f}")
    print(f"    Rango: {max(scores_single) - min(scores_single):.4f}")
    print(f"  → Un solo split puede dar resultados MUY diferentes")

    print("\n--- Cross-validation: estimacion estable ---")
    cv_scores = cross_val_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X, y, cv=5, scoring='accuracy'
    )
    print(f"  5-Fold CV: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"  Per fold:  {cv_scores.round(4)}")


# =====================================================================
#   PARTE 2: STRATIFIEDKFOLD Y REPEATEDSTRATIFIEDKFOLD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: STRATIFIED Y REPEATED ===")
print("=" * 80)

"""
STRATIFIED: mantiene la proporcion de clases en cada fold.
  Si tu dataset tiene 70% clase 0 y 30% clase 1,
  CADA fold tendra ~70%/30%.

  SIN stratify: un fold podria tener 90%/10% → score sesgado.
  SIEMPRE usa StratifiedKFold para clasificacion.

REPEATED: repite el proceso M veces con distintas particiones.
  RepeatedStratifiedKFold(n_splits=5, n_repeats=3) = 15 scores.
  Mas estable, especialmente con datasets pequenos.
"""

if HAS_SKLEARN:
    # Dataset desbalanceado
    X_imb, y_imb = make_classification(
        n_samples=500, n_features=20, n_informative=10,
        weights=[0.85, 0.15], random_state=42
    )

    print(f"\n  Balance de clases: {np.mean(y_imb):.2%} positivos")

    # KFold normal vs Stratified
    from sklearn.model_selection import KFold

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    print("\n  Proporcion clase 1 por fold:")
    print(f"  {'Fold':<6} {'KFold':>8} {'Stratified':>10}")
    for i, ((tr_k, te_k), (tr_s, te_s)) in enumerate(
        zip(kf.split(X_imb), skf.split(X_imb, y_imb))
    ):
        pct_kf = y_imb[te_k].mean()
        pct_sf = y_imb[te_s].mean()
        print(f"  {i+1:<6} {pct_kf:8.2%} {pct_sf:10.2%}")

    print(f"\n  → StratifiedKFold mantiene balance consistente")

    # RepeatedStratifiedKFold
    rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
    scores_repeated = cross_val_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X_imb, y_imb, cv=rskf, scoring='f1'
    )
    print(f"\n  RepeatedStratified (5×3=15 scores):")
    print(f"    F1: {scores_repeated.mean():.4f} ± {scores_repeated.std():.4f}")
    print(f"    → Mas estable que 5-fold simple")


# =====================================================================
#   PARTE 3: GROUPKFOLD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: GROUPKFOLD — DATOS CON GRUPOS ===")
print("=" * 80)

"""
PROBLEMA: datos medicos. Tienes 100 pacientes, 10 muestras por paciente.
Si un paciente aparece en train Y test, el modelo memoriza al paciente,
no aprende la enfermedad. → DATA LEAKAGE POR GRUPOS.

SOLUCION: GroupKFold. Cada grupo (paciente) esta COMPLETO en train O test.
  Nunca partido entre los dos.

CUANDO USARLO:
- Datos medicos (pacientes).
- Datos de usuarios (un usuario = un grupo).
- Datos geospaciales (una ciudad = un grupo).
- Datos temporales agrupados por sesion.
"""

if HAS_SKLEARN:
    # Simular datos medicos: 50 pacientes, 20 muestras cada uno
    np.random.seed(42)
    n_patients = 50
    samples_per = 20
    n_total = n_patients * samples_per

    X_group = np.random.randn(n_total, 10)
    groups = np.repeat(np.arange(n_patients), samples_per)

    # Efecto paciente: cada paciente tiene un "bias"
    patient_effect = np.random.randn(n_patients) * 2
    for i in range(n_patients):
        mask = groups == i
        X_group[mask] += patient_effect[i]

    y_group = (X_group[:, 0] + X_group[:, 1] > 0).astype(int)

    print(f"\n  Datos: {n_total} muestras, {n_patients} pacientes")

    # Sin GroupKFold (leakage)
    scores_leak = cross_val_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X_group, y_group, cv=5, scoring='accuracy'
    )
    print(f"\n  Sin GroupKFold (leakage): {scores_leak.mean():.4f} ± {scores_leak.std():.4f}")

    # Con GroupKFold
    gkf = GroupKFold(n_splits=5)
    scores_group = cross_val_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X_group, y_group, cv=gkf, groups=groups, scoring='accuracy'
    )
    print(f"  Con GroupKFold:           {scores_group.mean():.4f} ± {scores_group.std():.4f}")
    print(f"\n  → Score sin groups esta INFLADO por leakage")
    print(f"  → GroupKFold da la estimacion REAL de generalizacion")


# =====================================================================
#   PARTE 4: TIMESERIESSPLIT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: TIMESERIESSPLIT ===")
print("=" * 80)

"""
DATOS TEMPORALES: no puedes mezclar pasado y futuro!

KFold normal puede poner datos de enero en train y diciembre en test,
pero TAMBIEN diciembre en train y enero en test.
→ El modelo "ve el futuro" → leakage temporal.

TimeSeriesSplit: siempre entrena en el PASADO, testea en el FUTURO.
  Split 1: train=[0:200], test=[200:300]
  Split 2: train=[0:300], test=[300:400]
  Split 3: train=[0:400], test=[400:500]
  El training set CRECE, como en la realidad.
"""

if HAS_SKLEARN:
    # Datos con tendencia temporal
    np.random.seed(42)
    n_ts = 500
    X_ts = np.column_stack([
        np.linspace(0, 5, n_ts),  # Tendencia
        np.random.randn(n_ts, 4),  # Ruido
    ])
    y_ts = (X_ts[:, 0] + X_ts[:, 1] > 2.5).astype(int)

    tscv = TimeSeriesSplit(n_splits=5)

    print(f"\n  TimeSeriesSplit (5 splits):")
    scores_ts = []
    for i, (train_idx, test_idx) in enumerate(tscv.split(X_ts)):
        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(X_ts[train_idx], y_ts[train_idx])
        score = lr.score(X_ts[test_idx], y_ts[test_idx])
        scores_ts.append(score)
        print(f"    Split {i+1}: train=[0:{len(train_idx)}], "
              f"test=[{train_idx[-1]+1}:{test_idx[-1]+1}], "
              f"acc={score:.4f}")

    print(f"\n  Mean: {np.mean(scores_ts):.4f} ± {np.std(scores_ts):.4f}")

    # Gap entre train y test (para evitar leakage de features lag)
    tscv_gap = TimeSeriesSplit(n_splits=5, gap=10)
    print(f"\n  Con gap=10 (evita leakage de lag features):")
    for i, (train_idx, test_idx) in enumerate(tscv_gap.split(X_ts)):
        gap_size = test_idx[0] - train_idx[-1] - 1
        print(f"    Split {i+1}: train ends {train_idx[-1]}, "
              f"test starts {test_idx[0]}, gap={gap_size}")


# =====================================================================
#   PARTE 5: LEAVE-ONE-OUT (LOO)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: LEAVE-ONE-OUT ===")
print("=" * 80)

"""
LOO: K = N (cada muestra es un fold de test).
  - Entrena N modelos, cada uno con N-1 muestras.
  - Maximo uso de datos para entrenamiento.
  - Estimacion casi insesgada del error.

PERO:
  - LENTO: N entrenamientos.
  - Alta varianza: cada test set tiene 1 sola muestra.
  - Solo practico con datasets muy pequenos (< 200).

CUANDO USARLO:
  - Datasets medicos pequenos (50-100 pacientes).
  - Cuando cada muestra es MUY costosa de obtener.
  - NUNCA con datasets grandes.
"""

if HAS_SKLEARN:
    # LOO solo con dataset pequeno
    X_small = X[:100]
    y_small = y[:100]

    loo = LeaveOneOut()
    print(f"\n  LOO con {len(X_small)} muestras: {loo.get_n_splits(X_small)} splits")

    scores_loo = cross_val_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X_small, y_small, cv=loo, scoring='accuracy'
    )
    print(f"  LOO accuracy: {scores_loo.mean():.4f} ± {scores_loo.std():.4f}")

    # Comparar con 5-fold en el mismo dataset
    scores_5f = cross_val_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X_small, y_small, cv=5, scoring='accuracy'
    )
    print(f"  5-Fold accuracy: {scores_5f.mean():.4f} ± {scores_5f.std():.4f}")
    print(f"\n  LOO tiene mayor varianza pero menor sesgo")


# =====================================================================
#   PARTE 6: NESTED CROSS-VALIDATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: NESTED CV — LA FORMA CORRECTA ===")
print("=" * 80)

"""
EL PROBLEMA CON GRIDSEARCHCV + CV:

  GridSearchCV(model, param_grid, cv=5)
  → Selecciona los mejores hiperparametros.
  → El score que reporta es OPTIMISTA.
  → Por que? Porque eligio los params que MEJOR funcionaron en esos folds.
  → Es como elegir la mejor tirada de dados y decir "siempre saco 6".

SOLUCION: NESTED CV (doble loop).

  OUTER LOOP (evalua el MODELO):
    Para cada outer fold:
      INNER LOOP (selecciona HIPERPARAMETROS):
        GridSearchCV en los datos de training del outer fold.
      Evalua el mejor modelo en el test del outer fold.

  Resultado: score NO sesgado del proceso completo
  (incluyendo la seleccion de hiperparametros).

REGLA:
  - Inner CV: para ELEGIR hiperparametros.
  - Outer CV: para EVALUAR el modelo final.
  - NUNCA uses el score del inner CV como estimacion final.
"""

if HAS_SKLEARN:
    from sklearn.model_selection import GridSearchCV

    print("\n--- Nested CV vs Non-Nested ---")

    # Non-nested: score optimista
    param_grid = {'C': [0.01, 0.1, 1, 10, 100]}
    gs = GridSearchCV(
        LogisticRegression(max_iter=1000, random_state=42),
        param_grid, cv=5, scoring='accuracy'
    )
    gs.fit(X, y)
    non_nested_score = gs.best_score_
    print(f"  Non-nested (GridSearchCV.best_score_): {non_nested_score:.4f}")
    print(f"  → OPTIMISTA: elegimos el mejor C de 5 opciones")

    # Nested: score honesto
    outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    nested_scores = []
    for i, (train_idx, test_idx) in enumerate(outer_cv.split(X, y)):
        X_train_outer, X_test_outer = X[train_idx], X[test_idx]
        y_train_outer, y_test_outer = y[train_idx], y[test_idx]

        # Inner loop: elegir hiperparametros
        gs_inner = GridSearchCV(
            LogisticRegression(max_iter=1000, random_state=42),
            param_grid, cv=inner_cv, scoring='accuracy'
        )
        gs_inner.fit(X_train_outer, y_train_outer)

        # Evaluar en outer test
        outer_score = gs_inner.score(X_test_outer, y_test_outer)
        nested_scores.append(outer_score)
        print(f"    Outer fold {i+1}: best_C={gs_inner.best_params_['C']}, "
              f"score={outer_score:.4f}")

    print(f"\n  Nested CV: {np.mean(nested_scores):.4f} ± {np.std(nested_scores):.4f}")
    print(f"  Non-nested: {non_nested_score:.4f}")
    print(f"  Diferencia: {non_nested_score - np.mean(nested_scores):.4f} (sesgo optimista)")


# =====================================================================
#   PARTE 7: LEARNING CURVES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: LEARNING CURVES ===")
print("=" * 80)

"""
LEARNING CURVE: como cambia el score al AUMENTAR datos de training.

DIAGNOSTICO:
  1. UNDERFITTING (high bias):
     - Train score BAJO.
     - Train y val convergen... pero en un valor BAJO.
     - Solucion: modelo mas complejo, mas features.

  2. OVERFITTING (high variance):
     - Train score ALTO (cercano a 1.0).
     - Val score MUCHO mas bajo que train.
     - GAP grande entre train y val.
     - Solucion: mas datos, regularizacion, modelo mas simple.

  3. BUEN FIT:
     - Train score alto.
     - Val score cercano a train.
     - Gap pequeno.
     - Ambos mejoran con mas datos (o se estabilizan alto).
"""

if HAS_SKLEARN:
    print("\n--- Learning Curves: Diagnostico ---")

    models_lc = {
        'Logistic (underfit?)': LogisticRegression(max_iter=1000, random_state=42),
        'DecisionTree (overfit?)': DecisionTreeClassifier(max_depth=None, random_state=42),
        'RF (buen fit?)': RandomForestClassifier(100, max_depth=10, random_state=42),
    }

    train_sizes_abs = [50, 100, 200, 400, 600, 800]

    for name, model in models_lc.items():
        sizes, train_sc, val_sc = learning_curve(
            model, X, y,
            train_sizes=train_sizes_abs,
            cv=5, scoring='accuracy',
            n_jobs=-1,
        )

        print(f"\n  {name}:")
        print(f"    {'Size':>6} {'Train':>8} {'Val':>8} {'Gap':>6} {'Dx':>12}")
        for s, tr, va in zip(sizes, train_sc.mean(1), val_sc.mean(1)):
            gap = tr - va
            if tr < 0.75:
                dx = "UNDERFIT"
            elif gap > 0.10:
                dx = "OVERFIT"
            else:
                dx = "OK"
            print(f"    {s:6d} {tr:8.4f} {va:8.4f} {gap:6.3f} {dx:>12}")


# =====================================================================
#   PARTE 8: VALIDATION CURVES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: VALIDATION CURVES ===")
print("=" * 80)

"""
VALIDATION CURVE: como cambia el score al variar UN hiperparametro.

Es el "learning curve" pero variando complejidad en vez de datos.

Si el hiperparametro controla complejidad (ej: max_depth, C, n_estimators):
  - Valor bajo → underfitting (modelo demasiado simple).
  - Valor alto → overfitting (modelo demasiado complejo).
  - Punto optimo → donde val score es maximo.
"""

if HAS_SKLEARN:
    print("\n--- Validation Curve: C de LogisticRegression ---")

    param_range_c = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    train_vc, val_vc = validation_curve(
        LogisticRegression(max_iter=2000, random_state=42),
        X, y, param_name='C', param_range=param_range_c,
        cv=5, scoring='accuracy',
    )

    print(f"  {'C':>8} {'Train':>8} {'Val':>8} {'Gap':>6}")
    best_val = -1
    best_c = None
    for c, tr, va in zip(param_range_c, train_vc.mean(1), val_vc.mean(1)):
        gap = tr - va
        marker = ""
        if va > best_val:
            best_val = va
            best_c = c
        print(f"  {c:8.3f} {tr:8.4f} {va:8.4f} {gap:6.3f}")
    print(f"\n  Mejor C: {best_c} (val={best_val:.4f})")

    print("\n--- Validation Curve: max_depth de DecisionTree ---")

    param_range_depth = [1, 2, 3, 5, 7, 10, 15, 20, None]
    # None no funciona con validation_curve, usamos loop manual
    print(f"  {'depth':>6} {'Train':>8} {'Val':>8} {'Gap':>6}")
    for depth in [1, 2, 3, 5, 7, 10, 15, 20]:
        dt = DecisionTreeClassifier(max_depth=depth, random_state=42)
        cv_res = cross_validate(dt, X, y, cv=5, scoring='accuracy',
                                return_train_score=True)
        tr = cv_res['train_score'].mean()
        va = cv_res['test_score'].mean()
        print(f"  {depth:6d} {tr:8.4f} {va:8.4f} {tr-va:6.3f}")


# =====================================================================
#   PARTE 9: COMPARACION ESTADISTICA DE MODELOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: COMPARACION ESTADISTICA ===")
print("=" * 80)

"""
PREGUNTA CLAVE: "El modelo A es REALMENTE mejor que B,
o simplemente tuvo suerte en estos folds?"

NO BASTA con comparar medias:
  Modelo A: 0.85 ± 0.03
  Modelo B: 0.83 ± 0.04
  → No es claro que A sea mejor.

TESTS ESTADISTICOS:
1. Paired t-test: compara scores fold a fold.
   H0: no hay diferencia entre modelos.
   p < 0.05 → diferencia significativa.

2. Wilcoxon signed-rank: version no-parametrica del t-test.
   Mejor cuando los scores no son normales.

3. McNemar test: compara errores individuales (no scores).
   Mas potente para clasificacion.

CORRECCION IMPORTANTE:
  El t-test asume independencia, pero los folds de CV
  comparten datos de training → sobreestima significancia.
  Usar CORRECCION de Nadeau & Bengio (2003).
"""

if HAS_SKLEARN:
    print("\n--- Comparando modelos con test estadistico ---")

    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)

    models_compare = {
        'LogReg': LogisticRegression(max_iter=1000, random_state=42),
        'RF': RandomForestClassifier(100, random_state=42, n_jobs=-1),
        'GBM': GradientBoostingClassifier(100, random_state=42),
        'KNN': KNeighborsClassifier(5),
        'SVM': SVC(random_state=42),
    }

    all_scores = {}
    for name, model in models_compare.items():
        scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
        all_scores[name] = scores
        print(f"  {name:>8}: {scores.mean():.4f} ± {scores.std():.4f}")

    # Paired t-test entre los dos mejores
    print("\n--- Paired t-test ---")
    sorted_models = sorted(all_scores.items(), key=lambda x: x[1].mean(), reverse=True)
    best_name, best_scores = sorted_models[0]
    second_name, second_scores = sorted_models[1]

    t_stat, p_value = stats.ttest_rel(best_scores, second_scores)
    print(f"\n  {best_name} vs {second_name}:")
    print(f"    t-statistic: {t_stat:.4f}")
    print(f"    p-value:     {p_value:.4f}")
    if p_value < 0.05:
        print(f"    → Diferencia SIGNIFICATIVA (p < 0.05)")
    else:
        print(f"    → Diferencia NO significativa (p >= 0.05)")

    # Wilcoxon (no-parametrico)
    w_stat, w_pvalue = stats.wilcoxon(best_scores, second_scores)
    print(f"\n  Wilcoxon: stat={w_stat:.4f}, p={w_pvalue:.4f}")

    # Comparacion completa (todos vs todos)
    print("\n--- Matriz de p-values (paired t-test) ---")
    model_names = list(all_scores.keys())
    print(f"  {'':>8}", end="")
    for n in model_names:
        print(f" {n:>8}", end="")
    print()

    for n1 in model_names:
        print(f"  {n1:>8}", end="")
        for n2 in model_names:
            if n1 == n2:
                print(f" {'---':>8}", end="")
            else:
                _, p = stats.ttest_rel(all_scores[n1], all_scores[n2])
                marker = "*" if p < 0.05 else " "
                print(f" {p:7.3f}{marker}", end="")
        print()


# =====================================================================
#   PARTE 10: PERMUTATION TEST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: PERMUTATION TEST ===")
print("=" * 80)

"""
PREGUNTA: "Mi modelo es mejor que puro AZAR?"

Permutation test:
1. Entrena el modelo normalmente → score real.
2. Permuta y (rompe la relacion X→y) → score aleatorio.
3. Repite 100+ veces → distribucion de scores aleatorios.
4. p-value = % de scores aleatorios >= score real.

Si p < 0.05: el modelo captura una senal REAL.
Si p >= 0.05: el modelo NO es mejor que azar (preocupante).
"""

if HAS_SKLEARN:
    print("\n--- Permutation test ---")

    # Modelo real (deberia tener senal)
    score_real, perm_scores, pvalue = permutation_test_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X, y, cv=5, scoring='accuracy',
        n_permutations=100, random_state=42,
    )

    print(f"  Score real:       {score_real:.4f}")
    print(f"  Scores aleatorios: {perm_scores.mean():.4f} ± {perm_scores.std():.4f}")
    print(f"  p-value:          {pvalue:.4f}")
    if pvalue < 0.05:
        print(f"  → El modelo captura senal REAL (p < 0.05)")
    else:
        print(f"  → El modelo NO es mejor que azar!")

    # Datos sin senal (deberia fallar)
    X_noise = np.random.randn(500, 20)
    y_noise = np.random.binomial(1, 0.5, 500)

    score_noise, perm_noise, pval_noise = permutation_test_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X_noise, y_noise, cv=5, scoring='accuracy',
        n_permutations=50, random_state=42,
    )

    print(f"\n  Datos sin senal:")
    print(f"    Score: {score_noise:.4f}, p-value: {pval_noise:.4f}")
    print(f"    → {'NO mejor que azar (correcto!)' if pval_noise >= 0.05 else 'Falso positivo'}")


# =====================================================================
#   PARTE 11: CROSS_VALIDATE MULTI-METRICA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: MULTI-METRICA Y ANALISIS COMPLETO ===")
print("=" * 80)

"""
cross_validate permite evaluar MULTIPLES metricas de una vez,
y tambien retornar tiempos de entrenamiento e inferencia.

Esto te da un perfil COMPLETO del modelo:
- Accuracy, F1, AUC: calidad.
- Fit time: cuanto tarda en entrenar.
- Score time: cuanto tarda en predecir.
"""

if HAS_SKLEARN:
    print("\n--- Perfil completo de modelos ---")

    scoring = ['accuracy', 'f1', 'roc_auc']

    models_profile = {
        'LogReg': LogisticRegression(max_iter=1000, random_state=42),
        'RF_100': RandomForestClassifier(100, random_state=42, n_jobs=-1),
        'GBM_100': GradientBoostingClassifier(100, random_state=42),
        'KNN_5': KNeighborsClassifier(5),
    }

    print(f"  {'Model':>10} {'Acc':>8} {'F1':>8} {'AUC':>8} "
          f"{'Fit(s)':>8} {'Pred(ms)':>10}")

    for name, model in models_profile.items():
        cv_res = cross_validate(
            model, X, y, cv=5, scoring=scoring,
            return_train_score=False,
        )
        acc = cv_res['test_accuracy'].mean()
        f1 = cv_res['test_f1'].mean()
        auc = cv_res['test_roc_auc'].mean()
        fit_t = cv_res['fit_time'].mean()
        score_t = cv_res['score_time'].mean() * 1000

        print(f"  {name:>10} {acc:8.4f} {f1:8.4f} {auc:8.4f} "
              f"{fit_t:8.3f} {score_t:10.2f}")

    print(f"\n  → Elige modelo balanceando calidad Y velocidad")


# =====================================================================
#   PARTE 12: PATRONES DE PRODUCCION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: CV EN PRODUCCION — PATRONES ===")
print("=" * 80)

"""
PATRONES CLAVE:

1. SIEMPRE pipeline dentro de CV:
   Pipeline([scaler, model]) dentro de cross_val_score.
   NUNCA escalar fuera de CV (leakage!).

2. STRATIFY para clasificacion, SIEMPRE.

3. GROUPS si hay estructura de grupos.

4. TIMESERIES si hay temporalidad.

5. NESTED CV para reportar score final honesto.

6. SEMILLA fija para reproducibilidad.

7. Guardar TODOS los scores, no solo la media.

8. Comparacion estadistica antes de elegir modelo.
"""

if HAS_SKLEARN:
    print("\n--- Patron correcto: Pipeline dentro de CV ---")

    # MAL: escalar fuera de CV
    scaler = StandardScaler()
    X_scaled_bad = scaler.fit_transform(X)  # LEAKAGE: test ve estadisticas de train
    scores_bad = cross_val_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X_scaled_bad, y, cv=5
    )

    # BIEN: pipeline dentro de CV
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    scores_good = cross_val_score(pipe, X, y, cv=5)

    print(f"  MAL (scale fuera): {scores_bad.mean():.4f} ± {scores_bad.std():.4f}")
    print(f"  BIEN (pipeline):   {scores_good.mean():.4f} ± {scores_good.std():.4f}")
    print(f"  → La diferencia puede ser pequena aqui, pero con")
    print(f"    datos reales y menos muestras, el leakage es grave.")

    print("\n--- Patron: Resultados reproducibles ---")

    # Funcion de evaluacion robusta
    def evaluate_model(model, X, y, cv_strategy='stratified',
                       n_splits=5, n_repeats=1, groups=None,
                       scoring='accuracy', random_state=42):
        """Evaluacion robusta con CV configurable."""
        if cv_strategy == 'stratified':
            if n_repeats > 1:
                cv = RepeatedStratifiedKFold(
                    n_splits=n_splits, n_repeats=n_repeats,
                    random_state=random_state)
            else:
                cv = StratifiedKFold(
                    n_splits=n_splits, shuffle=True,
                    random_state=random_state)
        elif cv_strategy == 'group':
            cv = GroupKFold(n_splits=n_splits)
        elif cv_strategy == 'timeseries':
            cv = TimeSeriesSplit(n_splits=n_splits)
        else:
            cv = n_splits

        scores = cross_val_score(
            model, X, y, cv=cv, scoring=scoring,
            groups=groups,
        )

        return {
            'mean': float(scores.mean()),
            'std': float(scores.std()),
            'scores': scores.tolist(),
            'ci_95': (
                float(scores.mean() - 1.96 * scores.std()),
                float(scores.mean() + 1.96 * scores.std()),
            ),
            'n_splits': len(scores),
            'strategy': cv_strategy,
        }

    result = evaluate_model(
        Pipeline([('scaler', StandardScaler()),
                  ('clf', LogisticRegression(max_iter=1000, random_state=42))]),
        X, y, cv_strategy='stratified', n_splits=5, n_repeats=3
    )

    print(f"\n  Resultado robusto:")
    print(f"    Mean ± Std: {result['mean']:.4f} ± {result['std']:.4f}")
    print(f"    95% CI: [{result['ci_95'][0]:.4f}, {result['ci_95'][1]:.4f}]")
    print(f"    N splits: {result['n_splits']}")
    print(f"    Strategy: {result['strategy']}")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: VALIDACION CRUZADA AVANZADA ===")
print("=" * 80)

print("""
  DECISION TREE DE CV:

  Datos temporales? ──→ TimeSeriesSplit
       │ NO
  Hay grupos? ──→ GroupKFold
       │ NO
  Clasificacion? ──→ StratifiedKFold (SIEMPRE)
       │ NO
  Regresion ──→ KFold

  Dataset pequeno (< 200)? ──→ RepeatedStratifiedKFold o LOO
  Seleccion de hiperparametros? ──→ Nested CV

  REGLAS DE ORO:
  1. Pipeline DENTRO de CV (nunca preprocesar fuera).
  2. Stratify para clasificacion.
  3. Groups si hay estructura.
  4. Nested CV para score honesto con tuning.
  5. Comparacion estadistica (t-test) antes de elegir modelo.
  6. Permutation test para verificar que hay senal.
  7. SIEMPRE reportar mean ± std, nunca un solo numero.
""")

print("=" * 80)
print("=== FIN MODULO 16, ARCHIVO 02 ===")
print("=" * 80)