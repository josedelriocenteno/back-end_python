# ===========================================================================
# 01_sklearn_api.py
# ===========================================================================
# MODULO 14: SCIKIT-LEARN PROFUNDO
# ARCHIVO 01: API de Scikit-Learn, Estimators, Pipelines
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar la API de sklearn: estimators, transformers, pipelines,
# custom estimators, y patrones de produccion.
#
# CONTENIDO:
#   1. Estimator API (fit/predict/transform).
#   2. Preprocessing: scalers, encoders.
#   3. Pipeline y ColumnTransformer.
#   4. Custom transformers.
#   5. FeatureUnion.
#   6. Cloning y parameter inspection.
#   7. Cross-validation avanzado.
#   8. GridSearchCV / RandomizedSearchCV.
#   9. Scoring functions.
#   10. Model persistence.
#   11. Reproducibility patterns.
#   12. Production patterns.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import warnings
warnings.filterwarnings('ignore')

try:
    import sklearn
    from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
    from sklearn.pipeline import Pipeline, FeatureUnion
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import (
        StandardScaler, MinMaxScaler, RobustScaler,
        LabelEncoder, OrdinalEncoder, OneHotEncoder,
        PolynomialFeatures, FunctionTransformer,
    )
    from sklearn.impute import SimpleImputer
    from sklearn.model_selection import (
        train_test_split, cross_val_score, KFold, StratifiedKFold,
        GridSearchCV, RandomizedSearchCV, learning_curve,
    )
    from sklearn.linear_model import LogisticRegression, Ridge, Lasso
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        classification_report, confusion_matrix, roc_auc_score,
        make_scorer, mean_squared_error, r2_score,
    )
    from sklearn.datasets import make_classification, make_regression
    from sklearn.feature_selection import SelectKBest, f_classif
    import sklearn.utils
    HAS_SKLEARN = True
    print(f"  sklearn version: {sklearn.__version__}")
except ImportError:
    HAS_SKLEARN = False
    print("  (sklearn no disponible, modo documentacion)")

import pandas as pd


# =====================================================================
#   PARTE 1: ESTIMATOR API
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: ESTIMATOR API ===")
print("=" * 80)

"""
SKLEARN ESTIMATOR API:
  Todo en sklearn sigue 3 patrones:

1. ESTIMATOR (fit):
   model.fit(X, y)  # Aprender parametros
   
2. PREDICTOR (predict):
   model.predict(X)        # Clasificacion/Regresion
   model.predict_proba(X)  # Probabilidades
   
3. TRANSFORMER (transform):
   scaler.fit(X_train)
   X_scaled = scaler.transform(X_test)
   # o combinado:
   X_scaled = scaler.fit_transform(X_train)

REGLA DE ORO:
  fit en TRAIN, transform en TRAIN+TEST.
  NUNCA fit en test.
"""

if HAS_SKLEARN:
    print("\n--- Crear datos ---")
    
    X, y = make_classification(
        n_samples=1000, n_features=20, n_informative=10,
        n_redundant=5, n_classes=2, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"  Train: {X_train.shape}, Test: {X_test.shape}")
    print(f"  Class balance: {np.mean(y_train):.2f}")
    
    
    print("\n--- Estimator basics ---")
    
    lr = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    
    # Inspect parameters
    print(f"  Parameters: {lr.get_params()}")
    
    # Fit
    lr.fit(X_train, y_train)
    
    # After fit, attributes end with _
    print(f"  Coef shape: {lr.coef_.shape}")
    print(f"  Intercept: {lr.intercept_}")
    print(f"  Classes: {lr.classes_}")
    
    # Predict
    y_pred = lr.predict(X_test)
    y_proba = lr.predict_proba(X_test)
    
    print(f"  Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Proba shape: {y_proba.shape}")
else:
    print("  (sklearn required for demos)")


# =====================================================================
#   PARTE 2: PREPROCESSING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: PREPROCESSING ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- Scalers ---")
    
    scalers = {
        'StandardScaler': StandardScaler(),
        'MinMaxScaler': MinMaxScaler(),
        'RobustScaler': RobustScaler(),
    }
    
    for name, scaler in scalers.items():
        X_scaled = scaler.fit_transform(X_train[:5])
        print(f"  {name:>15s}: mean={X_scaled.mean():.3f}, std={X_scaled.std():.3f}, "
              f"min={X_scaled.min():.3f}, max={X_scaled.max():.3f}")
    
    
    print("\n--- Encoders ---")
    
    # Categorical data
    df_cat = pd.DataFrame({
        'color': ['red', 'blue', 'green', 'red', 'blue'],
        'size': ['S', 'M', 'L', 'XL', 'M'],
        'price': [10.5, 20.3, 15.0, 12.5, 18.0],
    })
    
    # LabelEncoder (single column, ordinal)
    le = LabelEncoder()
    encoded = le.fit_transform(df_cat['color'])
    print(f"  LabelEncoder: {df_cat['color'].tolist()} -> {encoded.tolist()}")
    print(f"    Classes: {le.classes_}")
    
    # OneHotEncoder
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_ohe = ohe.fit_transform(df_cat[['color']])
    print(f"  OneHot shape: {encoded_ohe.shape}")
    print(f"    Categories: {ohe.categories_}")
    
    
    print("\n--- Imputation ---")
    
    X_missing = X_train[:10].copy()
    X_missing[0, 0] = np.nan
    X_missing[2, 3] = np.nan
    X_missing[5, 7] = np.nan
    
    imputers = {
        'mean': SimpleImputer(strategy='mean'),
        'median': SimpleImputer(strategy='median'),
        'constant': SimpleImputer(strategy='constant', fill_value=-999),
    }
    
    for name, imp in imputers.items():
        X_imp = imp.fit_transform(X_missing)
        n_missing_after = np.sum(np.isnan(X_imp))
        print(f"  {name:>8s}: missing_after={n_missing_after}")


# =====================================================================
#   PARTE 3: PIPELINE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: PIPELINE ===")
print("=" * 80)

"""
Pipeline: encadenar transformaciones + modelo.
Ventajas:
1. Evita data leakage (fit solo en train).
2. Codigo limpio y reproducible.
3. Compatible con GridSearchCV.
4. Facil deploy (pickle pipeline completo).
"""

if HAS_SKLEARN:
    print("\n--- Simple pipeline ---")
    
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    
    pipe.fit(X_train, y_train)
    score = pipe.score(X_test, y_test)
    print(f"  Pipeline accuracy: {score:.4f}")
    
    # Access steps
    print(f"  Steps: {[name for name, _ in pipe.steps]}")
    print(f"  Scaler mean (first 3): {pipe['scaler'].mean_[:3].round(3)}")
    
    
    print("\n--- Complex pipeline ---")
    
    complex_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('poly', PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)),
        ('selector', SelectKBest(f_classif, k=50)),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    
    complex_pipe.fit(X_train, y_train)
    complex_score = complex_pipe.score(X_test, y_test)
    print(f"  Complex pipeline accuracy: {complex_score:.4f}")
    print(f"  Features after poly: {complex_pipe['poly'].n_output_features_}")
    print(f"  Features after select: {complex_pipe['selector'].k}")


# =====================================================================
#   PARTE 4: COLUMNTRANSFORMER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: COLUMNTRANSFORMER ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- Mixed data types ---")
    
    np.random.seed(42)
    n_mixed = 500
    df_mixed = pd.DataFrame({
        'age': np.random.randint(18, 65, n_mixed),
        'income': np.random.lognormal(10, 1, n_mixed),
        'education': np.random.choice(['HS', 'BS', 'MS', 'PhD'], n_mixed),
        'department': np.random.choice(['Eng', 'Sales', 'Mkt'], n_mixed),
        'years_exp': np.random.randint(0, 30, n_mixed),
    })
    y_mixed = np.random.binomial(1, 0.3, n_mixed)
    
    numeric_features = ['age', 'income', 'years_exp']
    categorical_features = ['education', 'department']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler()),
            ]), numeric_features),
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
            ]), categorical_features),
        ],
        remainder='drop',
    )
    
    full_pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    
    X_mixed_train, X_mixed_test, y_mixed_train, y_mixed_test = train_test_split(
        df_mixed, y_mixed, test_size=0.2, random_state=42
    )
    
    full_pipe.fit(X_mixed_train, y_mixed_train)
    mixed_score = full_pipe.score(X_mixed_test, y_mixed_test)
    print(f"  Mixed data pipeline accuracy: {mixed_score:.4f}")
    
    # Get feature names
    cat_features = full_pipe['preprocessor'].transformers_[1][1]['onehot'].get_feature_names_out(categorical_features)
    all_features = list(numeric_features) + list(cat_features)
    print(f"  Total features: {len(all_features)}")
    print(f"  Cat features: {list(cat_features)}")


# =====================================================================
#   PARTE 5: CUSTOM TRANSFORMER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: CUSTOM TRANSFORMER ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- Custom transformer ---")
    
    class OutlierClipper(BaseEstimator, TransformerMixin):
        """Clip outliers based on IQR."""
        
        def __init__(self, factor=1.5):
            self.factor = factor
        
        def fit(self, X, y=None):
            X = np.asarray(X)
            self.q1_ = np.percentile(X, 25, axis=0)
            self.q3_ = np.percentile(X, 75, axis=0)
            self.iqr_ = self.q3_ - self.q1_
            self.lower_ = self.q1_ - self.factor * self.iqr_
            self.upper_ = self.q3_ + self.factor * self.iqr_
            return self
        
        def transform(self, X):
            X = np.asarray(X).copy()
            return np.clip(X, self.lower_, self.upper_)
    
    clipper = OutlierClipper(factor=1.5)
    X_clipped = clipper.fit_transform(X_train)
    
    print(f"  Before: min={X_train.min():.2f}, max={X_train.max():.2f}")
    print(f"  After:  min={X_clipped.min():.2f}, max={X_clipped.max():.2f}")
    
    
    class LogTransformer(BaseEstimator, TransformerMixin):
        """Log1p transform for positive-skewed features."""
        
        def __init__(self, columns=None):
            self.columns = columns
        
        def fit(self, X, y=None):
            return self
        
        def transform(self, X):
            X = np.asarray(X).copy().astype(float)
            if self.columns is not None:
                X[:, self.columns] = np.log1p(np.abs(X[:, self.columns]))
            else:
                X = np.log1p(np.abs(X))
            return X
    
    print(f"  LogTransformer: works in pipeline!")


# =====================================================================
#   PARTE 6: CROSS-VALIDATION AVANZADO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: CROSS-VALIDATION ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- cross_val_score ---")
    
    cv_scores = cross_val_score(
        LogisticRegression(max_iter=1000, random_state=42),
        X_train, y_train, cv=5, scoring='accuracy'
    )
    print(f"  5-Fold CV: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"  Per fold: {cv_scores.round(4)}")
    
    
    print("\n--- StratifiedKFold ---")
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores_skf = cross_val_score(
        LogisticRegression(max_iter=1000), X_train, y_train, cv=skf
    )
    print(f"  Stratified 5-Fold: {scores_skf.mean():.4f} ± {scores_skf.std():.4f}")
    
    
    print("\n--- Multiple metrics ---")
    
    from sklearn.model_selection import cross_validate
    
    cv_results = cross_validate(
        LogisticRegression(max_iter=1000, random_state=42),
        X_train, y_train, cv=5,
        scoring=['accuracy', 'f1', 'roc_auc'],
        return_train_score=True,
    )
    
    for metric in ['accuracy', 'f1', 'roc_auc']:
        train = cv_results[f'train_{metric}'].mean()
        test = cv_results[f'test_{metric}'].mean()
        print(f"  {metric:>10s}: train={train:.4f}, test={test:.4f}")


# =====================================================================
#   PARTE 7: GRIDSEARCHCV
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: GRIDSEARCHCV ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- Grid search ---")
    
    param_grid = {
        'C': [0.01, 0.1, 1, 10],
        'penalty': ['l1', 'l2'],
        'solver': ['saga'],
    }
    
    grid = GridSearchCV(
        LogisticRegression(max_iter=2000, random_state=42),
        param_grid, cv=3, scoring='accuracy', n_jobs=-1, verbose=0,
    )
    grid.fit(X_train, y_train)
    
    print(f"  Best params: {grid.best_params_}")
    print(f"  Best CV score: {grid.best_score_:.4f}")
    print(f"  Test score: {grid.score(X_test, y_test):.4f}")
    
    
    print("\n--- RandomizedSearchCV ---")
    
    from scipy.stats import uniform, randint
    
    param_dist = {
        'n_estimators': randint(50, 300),
        'max_depth': randint(3, 15),
        'min_samples_split': randint(2, 20),
    }
    
    random_search = RandomizedSearchCV(
        RandomForestClassifier(random_state=42),
        param_dist, n_iter=20, cv=3, scoring='accuracy',
        random_state=42, n_jobs=-1, verbose=0,
    )
    random_search.fit(X_train, y_train)
    
    print(f"  Best params: {random_search.best_params_}")
    print(f"  Best CV score: {random_search.best_score_:.4f}")
    print(f"  Test score: {random_search.score(X_test, y_test):.4f}")


# =====================================================================
#   PARTE 8: PIPELINE + GRIDSEARCH
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: PIPELINE + GRIDSEARCH ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- Grid search over pipeline ---")
    
    pipe_gs = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=2000, random_state=42)),
    ])
    
    # Note: use __ to access pipeline step params
    param_grid_pipe = {
        'scaler': [StandardScaler(), MinMaxScaler(), RobustScaler()],
        'clf__C': [0.01, 0.1, 1, 10],
        'clf__penalty': ['l2'],
    }
    
    grid_pipe = GridSearchCV(pipe_gs, param_grid_pipe, cv=3, scoring='accuracy', verbose=0)
    grid_pipe.fit(X_train, y_train)
    
    print(f"  Best scaler: {grid_pipe.best_params_['scaler'].__class__.__name__}")
    print(f"  Best C: {grid_pipe.best_params_['clf__C']}")
    print(f"  Best CV: {grid_pipe.best_score_:.4f}")
    print(f"  Test: {grid_pipe.score(X_test, y_test):.4f}")


# =====================================================================
#   PARTE 9: CUSTOM SCORING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: CUSTOM SCORING ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- Custom scorer ---")
    
    # F-beta score (beta=2 favors recall)
    def fbeta_score(y_true, y_pred, beta=2):
        p = precision_score(y_true, y_pred, zero_division=0)
        r = recall_score(y_true, y_pred, zero_division=0)
        return (1 + beta**2) * p * r / (beta**2 * p + r) if (p + r) > 0 else 0
    
    fbeta_scorer = make_scorer(fbeta_score, beta=2)
    
    scores_fbeta = cross_val_score(
        LogisticRegression(max_iter=1000), X_train, y_train,
        cv=5, scoring=fbeta_scorer
    )
    print(f"  F-beta(2) CV: {scores_fbeta.mean():.4f}")
    
    # Business metric
    def profit_score(y_true, y_pred):
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        return tp * 100 - fp * 50 - fn * 200
    
    profit_scorer = make_scorer(profit_score)
    scores_profit = cross_val_score(
        LogisticRegression(max_iter=1000), X_train, y_train,
        cv=5, scoring=profit_scorer
    )
    print(f"  Profit CV: {scores_profit.mean():.0f}")


# =====================================================================
#   PARTE 10: LEARNING CURVES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: LEARNING CURVES ===")
print("=" * 80)

if HAS_SKLEARN:
    print("\n--- sklearn learning_curve ---")
    
    train_sizes, train_scores, val_scores = learning_curve(
        LogisticRegression(max_iter=1000, random_state=42),
        X_train, y_train,
        train_sizes=[0.1, 0.2, 0.4, 0.6, 0.8, 1.0],
        cv=5, scoring='accuracy',
    )
    
    print(f"  {'Size':>6s} {'Train':>8s} {'Val':>8s} {'Gap':>6s}")
    for size, tr, val in zip(train_sizes, train_scores.mean(axis=1), val_scores.mean(axis=1)):
        print(f"  {size:6d} {tr:8.4f} {val:8.4f} {tr-val:6.4f}")


# =====================================================================
#   PARTE 11: MODEL PERSISTENCE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: PERSISTENCE ===")
print("=" * 80)

"""
Model persistence:
  1. pickle: built-in, pero fragil entre versiones.
  2. joblib: mas eficiente para arrays grandes.
  3. ONNX: formato interoperable.
  
Patron produccion:
  import joblib
  joblib.dump(pipeline, 'model.joblib')
  pipeline = joblib.load('model.joblib')
"""

print("  Persistence patterns:")
print("    joblib.dump(pipeline, 'model.joblib')  # Save")
print("    pipeline = joblib.load('model.joblib')  # Load")
print("    Always save FULL pipeline (not just model)")
print("    Include sklearn version in metadata")


# =====================================================================
#   PARTE 12: REPRODUCIBILITY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: REPRODUCIBILITY ===")
print("=" * 80)

"""
REGLAS:
1. random_state en TODOS los estimators.
2. random_state en train_test_split.
3. np.random.seed al inicio.
4. Fijar PYTHONHASHSEED=0.
5. Logging de versiones: sklearn, numpy, pandas.
6. Guardar metadata: params, scores, timestamps.
"""

if HAS_SKLEARN:
    print(f"\n  Environment:")
    print(f"    sklearn: {sklearn.__version__}")
    print(f"    numpy:   {np.__version__}")
    print(f"    pandas:  {pd.__version__}")

    # Reproducibility check
    scores_1 = cross_val_score(LogisticRegression(max_iter=1000, random_state=42),
                                X_train, y_train, cv=KFold(5, shuffle=True, random_state=42))
    scores_2 = cross_val_score(LogisticRegression(max_iter=1000, random_state=42),
                                X_train, y_train, cv=KFold(5, shuffle=True, random_state=42))
    print(f"\n  Reproducibility: {np.allclose(scores_1, scores_2)}")


# =====================================================================
#   PARTE 13: FEATUREUNION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: FEATUREUNION ===")
print("=" * 80)

"""
FeatureUnion: combinar multiples transformers en paralelo.
Concatena outputs horizontalmente.
"""

if HAS_SKLEARN:
    from sklearn.decomposition import PCA
    
    union = FeatureUnion([
        ('pca', PCA(n_components=5)),
        ('kbest', SelectKBest(f_classif, k=10)),
    ])
    
    X_union = union.fit_transform(X_train, y_train)
    print(f"  PCA(5) + KBest(10) = {X_union.shape[1]} features")
    
    # In pipeline
    pipe_union = Pipeline([
        ('features', union),
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    pipe_union.fit(X_train, y_train)
    print(f"  FeatureUnion pipeline: {pipe_union.score(X_test, y_test):.4f}")


# =====================================================================
#   PARTE 14: FUNCTIONTRANSFORMER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: FUNCTIONTRANSFORMER ===")
print("=" * 80)

if HAS_SKLEARN:
    log_transformer = FunctionTransformer(np.log1p, validate=True)
    abs_transformer = FunctionTransformer(np.abs, validate=True)
    
    pipe_func = Pipeline([
        ('abs', abs_transformer),
        ('log', log_transformer),
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=1000, random_state=42)),
    ])
    pipe_func.fit(X_train, y_train)
    print(f"  FunctionTransformer pipeline: {pipe_func.score(X_test, y_test):.4f}")


# =====================================================================
#   PARTE 15: DUMMY BASELINE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: DUMMY BASELINE ===")
print("=" * 80)

if HAS_SKLEARN:
    from sklearn.dummy import DummyClassifier
    
    strategies = ['most_frequent', 'stratified', 'uniform']
    
    print(f"  {'Strategy':>15s} {'Accuracy':>10s}")
    for strategy in strategies:
        dummy = DummyClassifier(strategy=strategy, random_state=42)
        dummy.fit(X_train, y_train)
        score = dummy.score(X_test, y_test)
        print(f"  {strategy:>15s} {score:10.4f}")
    
    # Compare with real model
    lr_baseline = LogisticRegression(max_iter=1000, random_state=42)
    lr_baseline.fit(X_train, y_train)
    print(f"  {'LogisticReg':>15s} {lr_baseline.score(X_test, y_test):10.4f}")
    print(f"  Model MUST beat dummy baseline!")


# =====================================================================
#   PARTE 16: CLASSIFICATION REPORT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: CLASSIFICATION REPORT ===")
print("=" * 80)

if HAS_SKLEARN:
    y_pred_report = lr_baseline.predict(X_test)
    report = classification_report(y_test, y_pred_report)
    print(f"\n{report}")
    
    cm = confusion_matrix(y_test, y_pred_report)
    print(f"  Confusion Matrix:")
    print(f"    TN={cm[0,0]:3d}  FP={cm[0,1]:3d}")
    print(f"    FN={cm[1,0]:3d}  TP={cm[1,1]:3d}")
    
    # Normalized
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
    print(f"\n  Normalized:")
    print(f"    {cm_norm[0,0]:.3f}  {cm_norm[0,1]:.3f}")
    print(f"    {cm_norm[1,0]:.3f}  {cm_norm[1,1]:.3f}")


# =====================================================================
#   PARTE 17: MULTI-MODEL GRIDSEARCH
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: MULTI-MODEL SEARCH ===")
print("=" * 80)

"""
Pattern: buscar sobre multiples modelos con un solo GridSearchCV.
"""

if HAS_SKLEARN:
    pipe_multi = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression()),
    ])
    
    param_grid_multi = [
        {
            'clf': [LogisticRegression(max_iter=1000, random_state=42)],
            'clf__C': [0.1, 1, 10],
        },
        {
            'clf': [RandomForestClassifier(random_state=42, n_jobs=-1)],
            'clf__n_estimators': [50, 100],
            'clf__max_depth': [5, 10],
        },
        {
            'clf': [KNeighborsClassifier()],
            'clf__n_neighbors': [3, 5, 11],
        },
    ]
    
    grid_multi = GridSearchCV(pipe_multi, param_grid_multi, cv=3, scoring='accuracy', verbose=0)
    grid_multi.fit(X_train, y_train)
    
    print(f"  Best model: {grid_multi.best_params_['clf'].__class__.__name__}")
    print(f"  Best CV: {grid_multi.best_score_:.4f}")
    print(f"  Test: {grid_multi.score(X_test, y_test):.4f}")


# =====================================================================
#   PARTE 18: TRAIN/TEST GAP ANALYSIS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: GAP ANALYSIS ===")
print("=" * 80)

if HAS_SKLEARN:
    import time
    
    models_gap = {
        'LogReg': LogisticRegression(max_iter=1000, random_state=42),
        'DTree_deep': DecisionTreeClassifier(max_depth=None, random_state=42),
        'DTree_shallow': DecisionTreeClassifier(max_depth=3, random_state=42),
        'RF': RandomForestClassifier(100, random_state=42, n_jobs=-1),
        'GB': GradientBoostingClassifier(100, random_state=42),
    }
    
    print(f"  {'Model':>14s} {'Train':>7s} {'Test':>7s} {'Gap':>6s} {'Diagnosis':>12s}")
    for name, model in models_gap.items():
        model.fit(X_train, y_train)
        tr = model.score(X_train, y_train)
        te = model.score(X_test, y_test)
        gap = tr - te
        
        if tr < 0.7:
            diag = "UNDERFIT"
        elif gap > 0.1:
            diag = "OVERFIT"
        else:
            diag = "OK"
        
        print(f"  {name:>14s} {tr:7.4f} {te:7.4f} {gap:6.4f} {diag:>12s}")


# =====================================================================
#   PARTE 19: DATA VALIDATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: DATA VALIDATION ===")
print("=" * 80)

"""
Pre-predict validation:
1. Check input shape matches training.
2. Check no NaN/Inf.
3. Check feature ranges are reasonable.
4. Check dtypes match expected.
"""

if HAS_SKLEARN:
    class ValidatedPipeline:
        """Pipeline wrapper with input validation."""
        
        def __init__(self, pipeline):
            self.pipeline = pipeline
            self.n_features_ = None
            self.feature_stats_ = None
        
        def fit(self, X, y):
            X = np.asarray(X)
            self.n_features_ = X.shape[1]
            self.feature_stats_ = {
                'mean': X.mean(axis=0),
                'std': X.std(axis=0),
                'min': X.min(axis=0),
                'max': X.max(axis=0),
            }
            self.pipeline.fit(X, y)
            return self
        
        def predict(self, X):
            X = np.asarray(X)
            self._validate(X)
            return self.pipeline.predict(X)
        
        def _validate(self, X):
            assert X.shape[1] == self.n_features_, f"Expected {self.n_features_} features"
            assert not np.any(np.isnan(X)), "NaN values detected"
            assert not np.any(np.isinf(X)), "Inf values detected"
    
    vpipe = ValidatedPipeline(Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=1000, random_state=42)),
    ]))
    vpipe.fit(X_train, y_train)
    preds = vpipe.predict(X_test)
    print(f"  Validated pipeline: {len(preds)} predictions OK")


# =====================================================================
#   PARTE 20: COMPARISON TABLE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: FULL COMPARISON ===")
print("=" * 80)

if HAS_SKLEARN:
    all_models = {
        'LogReg': LogisticRegression(max_iter=1000, random_state=42),
        'KNN(5)': KNeighborsClassifier(5),
        'DTree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'RF(100)': RandomForestClassifier(100, random_state=42, n_jobs=-1),
        'GB(100)': GradientBoostingClassifier(100, random_state=42),
        'NaiveBayes': GaussianNB(),
    }
    
    print(f"  {'Model':>12s} {'Acc':>6s} {'F1':>6s} {'AUC':>6s} {'Time':>7s}")
    for name, model in all_models.items():
        start = time.perf_counter()
        model.fit(X_train, y_train)
        t = time.perf_counter() - start
        
        y_p = model.predict(X_test)
        acc = accuracy_score(y_test, y_p)
        f1 = f1_score(y_test, y_p)
        
        if hasattr(model, 'predict_proba'):
            y_prob = model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, y_prob)
        else:
            auc = 0
        
        print(f"  {name:>12s} {acc:6.4f} {f1:6.4f} {auc:6.4f} {t:7.4f}s")


# =====================================================================
#   PARTE 21: MAKE_PIPELINE SHORTCUT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: MAKE_PIPELINE ===")
print("=" * 80)

if HAS_SKLEARN:
    from sklearn.pipeline import make_pipeline
    
    # Auto-names steps
    quick_pipe = make_pipeline(
        StandardScaler(),
        SelectKBest(f_classif, k=10),
        LogisticRegression(max_iter=1000, random_state=42),
    )
    quick_pipe.fit(X_train, y_train)
    print(f"  make_pipeline: {quick_pipe.score(X_test, y_test):.4f}")
    print(f"  Auto step names: {[name for name, _ in quick_pipe.steps]}")


# =====================================================================
#   PARTE 22: BAYESIAN SEARCH
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 22: BAYESIAN SEARCH ===")
print("=" * 80)

"""
BayesSearchCV (scikit-optimize):
  Usa procesos gaussianos para modelar la funcion objetivo.
  Mas eficiente que grid/random para grandes search spaces.

  pip install scikit-optimize
  from skopt import BayesSearchCV
"""

print("  Bayesian optimization:")
print("    - Models objective function with Gaussian Process")
print("    - Trades off exploration vs exploitation")
print("    - Much more efficient than grid for large spaces")
print("    - Libraries: scikit-optimize, Optuna, Hyperopt")


# =====================================================================
#   PARTE 23: TARGET ENCODING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 23: TARGET ENCODING ===")
print("=" * 80)

"""
Target encoding: encode categorical feature as mean of target.
  category -> mean(y | category)

DANGER: data leakage si no se usa CV.
SIEMPRE: calcular en folds de CV, no en todo el dataset.
"""

if HAS_SKLEARN:
    try:
        from sklearn.preprocessing import TargetEncoder
        
        categories = np.random.choice(['A', 'B', 'C', 'D'], size=len(y_train))
        te = TargetEncoder(smooth=10)
        encoded = te.fit_transform(categories.reshape(-1, 1), y_train)
        print(f"  TargetEncoder: {encoded.shape}")
    except ImportError:
        print("  TargetEncoder available in sklearn >= 1.3")
        print("  Pattern: encode category as mean(target|category)")


# =====================================================================
#   PARTE 24: SCORE INTERNALS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 24: SCORE INTERNALS ===")
print("=" * 80)

"""
model.score(X, y) internamente hace:
  - Classifier: accuracy_score(y, self.predict(X))
  - Regressor: r2_score(y, self.predict(X))

Se puede overridear en custom estimators.
"""

if HAS_SKLEARN:
    lr_score = LogisticRegression(max_iter=1000, random_state=42)
    lr_score.fit(X_train, y_train)
    
    # These are equivalent
    score_method = lr_score.score(X_test, y_test)
    score_manual = accuracy_score(y_test, lr_score.predict(X_test))
    
    print(f"  model.score(): {score_method:.4f}")
    print(f"  manual acc:    {score_manual:.4f}")
    print(f"  Equal: {np.isclose(score_method, score_manual)}")


# =====================================================================
#   PARTE 25: COMMON PITFALLS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 25: PITFALLS ===")
print("=" * 80)

pitfalls = [
    ("Data leakage", "fit scaler on full data", "Pipeline with fit on train only"),
    ("Feature scaling", "forget to scale for KNN/SVM", "StandardScaler in pipeline"),
    ("Label leakage", "target info in features", "Check feature correlations"),
    ("Tune on test", "select model by test score", "Use CV, test only ONCE"),
    ("Class imbalance", "ignore in accuracy", "Use F1, class_weight, SMOTE"),
    ("Overfitting", "train >> test score", "Regularization, less depth"),
]

print(f"\n  {'Pitfall':>16s} {'Problem':>28s} {'Solution':>32s}")
for name, problem, solution in pitfalls:
    print(f"  {name:>16s} {problem:>28s} {solution:>32s}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN:
1. Estimator API: fit/predict/transform.
2. Pipeline: encadenar steps, evitar leakage.
3. ColumnTransformer: manejar mixed types.
4. Custom transformers: BaseEstimator + TransformerMixin.
5. GridSearchCV: busqueda exhaustiva.
6. RandomizedSearchCV: mas eficiente.
7. Pipeline + GridSearch: buscar sobre todo el pipeline.
8. Custom scoring: make_scorer para metricas de negocio.
9. Persistence: joblib > pickle.
10. Reproducibility: random_state everywhere.
"""

print("\n FIN DE ARCHIVO 01_sklearn_api.")
print(" API de sklearn ha sido dominada.")
