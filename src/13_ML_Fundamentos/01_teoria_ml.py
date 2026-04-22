# ===========================================================================
# 01_teoria_ml.py
# ===========================================================================
# MODULO 13: ML FUNDAMENTOS
# ARCHIVO 01: Teoria de Machine Learning
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar los fundamentos teoricos de ML: tipos de aprendizaje,
# bias-variance tradeoff, overfitting, learning curves, y evaluacion.
#
# CONTENIDO:
#   1. Tipos de ML: supervised, unsupervised, reinforcement.
#   2. Bias-Variance Tradeoff.
#   3. Overfitting y Underfitting.
#   4. Regularizacion.
#   5. Cross-Validation.
#   6. Learning Curves.
#   7. Feature Scaling.
#   8. Gradient Descent.
#   9. Loss Functions.
#   10. Metrics fundamentales.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: TAXONOMIA DE ML
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: TAXONOMIA DE ML ===")
print("=" * 80)

"""
MACHINE LEARNING: aprender patrones de datos sin programar reglas explicitas.

TIPOS PRINCIPALES:

1. SUPERVISED LEARNING (Aprendizaje Supervisado)
   - Input: X (features) + y (labels/target)
   - Goal: aprender f(X) -> y
   - Tipos:
     a) Regression: y es continuo (precio, temperatura)
     b) Classification: y es discreto (spam/no-spam, digito 0-9)
   - Ejemplos: Linear Regression, Logistic Regression, Random Forest, SVM, Neural Networks

2. UNSUPERVISED LEARNING (Aprendizaje No Supervisado)
   - Input: X (features) SIN labels
   - Goal: encontrar estructura oculta
   - Tipos:
     a) Clustering: agrupar datos similares (K-Means, DBSCAN)
     b) Dimensionality Reduction: reducir features (PCA, t-SNE, UMAP)
     c) Anomaly Detection: detectar outliers
     d) Association Rules: reglas de asociacion (market basket)

3. REINFORCEMENT LEARNING (Aprendizaje por Refuerzo)
   - Input: environment + actions + rewards
   - Goal: aprender politica optima
   - Ejemplos: AlphaGo, robotica, trading

4. SEMI-SUPERVISED / SELF-SUPERVISED
   - Pocos labels + muchos datos sin label
   - Transfer learning, contrastive learning
   - Es el paradigma dominante en LLMs
"""

print("  Supervised: X + y -> f(X) = y")
print("  Unsupervised: X -> structure")
print("  Reinforcement: state + action -> reward")
print("  Self-supervised: pretrain (unlabeled) + finetune (labeled)")


# =====================================================================
#   PARTE 2: BIAS-VARIANCE TRADEOFF
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: BIAS-VARIANCE TRADEOFF ===")
print("=" * 80)

"""
ERROR TOTAL = Bias^2 + Variance + Irreducible Noise

BIAS: error por simplificaciones del modelo.
  - Alto bias = underfitting (modelo muy simple).
  - Ejemplo: usar linea recta para datos cuadraticos.

VARIANCE: error por sensibilidad a datos de entrenamiento.
  - Alta varianza = overfitting (modelo muy complejo).
  - Ejemplo: polinomio grado 20 para 10 puntos.

TRADEOFF:
  - Modelo simple: alto bias, baja varianza.
  - Modelo complejo: bajo bias, alta varianza.
  - Objetivo: encontrar el punto optimo.
"""

print("\n--- Simulacion bias-variance ---")

np.random.seed(42)

# Funcion verdadera: f(x) = sin(x)
def true_function(x):
    return np.sin(x)

# Generar datos con ruido
def generate_data(n=30, noise=0.3):
    x = np.sort(np.random.uniform(0, 2 * np.pi, n))
    y = true_function(x) + np.random.randn(n) * noise
    return x, y

# Polynomial fit con diferentes grados
x_train, y_train = generate_data(30)
x_test = np.linspace(0, 2 * np.pi, 100)

for degree in [1, 3, 15]:
    coeffs = np.polyfit(x_train, y_train, degree)
    y_pred = np.polyval(coeffs, x_test)
    
    # Error en train
    y_train_pred = np.polyval(coeffs, x_train)
    train_mse = np.mean((y_train - y_train_pred) ** 2)
    
    # Error vs true function
    true_y = true_function(x_test)
    test_mse = np.mean((true_y - y_pred) ** 2)
    
    label = {1: 'Underfitting', 3: 'Good fit', 15: 'Overfitting'}[degree]
    print(f"  Degree {degree:2d} ({label:12s}): train_MSE={train_mse:.4f}, test_MSE={test_mse:.4f}")


# =====================================================================
#   PARTE 3: OVERFITTING Y UNDERFITTING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: OVERFITTING ===")
print("=" * 80)

"""
OVERFITTING: el modelo memoriza el training data incluyendo el ruido.
Sintomas:
  - Train error << Test error
  - Gap grande entre train y test performance
  - Modelo se comporta bien en train, mal en produccion

UNDERFITTING: el modelo es demasiado simple.
Sintomas:
  - Train error alto
  - Test error alto
  - Ambos errores similares pero altos

SOLUCIONES OVERFITTING:
  1. Mas datos de entrenamiento
  2. Regularizacion (L1, L2, dropout)
  3. Reducir complejidad del modelo
  4. Early stopping
  5. Cross-validation
  6. Feature selection
  7. Data augmentation
  8. Ensemble methods

SOLUCIONES UNDERFITTING:
  1. Modelo mas complejo
  2. Mas features / feature engineering
  3. Menos regularizacion
  4. Entrenar mas tiempo
"""

print("\n--- Detectar overfitting ---")

# Simular learning curves
n_sizes = [10, 20, 50, 100, 200, 500]

print(f"  {'N':>5s} {'Train MSE':>10s} {'Test MSE':>10s} {'Gap':>8s} {'Status':>12s}")
for n in n_sizes:
    x, y = generate_data(n)
    
    # Modelo complejo (degree=8)
    coeffs = np.polyfit(x, y, min(8, n-1))
    y_train_pred = np.polyval(coeffs, x)
    train_mse = np.mean((y - y_train_pred) ** 2)
    
    x_t = np.linspace(0, 2*np.pi, 200)
    y_t = true_function(x_t)
    y_t_pred = np.polyval(coeffs, x_t)
    test_mse = np.mean((y_t - y_t_pred) ** 2)
    
    gap = test_mse - train_mse
    status = "OVERFIT" if gap > 0.1 else "OK"
    print(f"  {n:5d} {train_mse:10.4f} {test_mse:10.4f} {gap:8.4f} {status:>12s}")


# =====================================================================
#   PARTE 4: REGULARIZACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: REGULARIZACION ===")
print("=" * 80)

"""
Regularizacion: penalizar complejidad del modelo.

L2 (Ridge): Loss + lambda * sum(w^2)
  - Shrink weights toward zero (no a zero exacto).
  - Todos los features contribuyen un poco.

L1 (Lasso): Loss + lambda * sum(|w|)
  - Puede poner weights a zero exacto.
  - Feature selection automatica.

Elastic Net: Loss + alpha * (r * L1 + (1-r) * L2)
  - Combina L1 y L2.
  - r controla la mezcla.
"""

print("\n--- Ridge vs Lasso ---")

# Implementar Ridge regression manual
def ridge_regression(X, y, alpha=1.0):
    """Ridge: (X^T X + alpha*I)^-1 X^T y"""
    n_features = X.shape[1]
    I = np.eye(n_features)
    I[0, 0] = 0  # No regularizar el bias
    w = np.linalg.solve(X.T @ X + alpha * I, X.T @ y)
    return w

# Crear datos
np.random.seed(42)
n = 50
x = np.sort(np.random.uniform(0, 5, n))
y = 2 * x + 1 + np.random.randn(n) * 2

# Feature matrix con polynomial features
def poly_features(x, degree):
    return np.column_stack([x**i for i in range(degree+1)])

X_poly = poly_features(x, 10)

# Sin regularizacion
w_no_reg = np.linalg.lstsq(X_poly, y, rcond=None)[0]
y_no_reg = X_poly @ w_no_reg
mse_no_reg = np.mean((y - y_no_reg) ** 2)

# Con Ridge
for alpha in [0.001, 0.1, 1.0, 10.0, 100.0]:
    w_ridge = ridge_regression(X_poly, y, alpha)
    y_ridge = X_poly @ w_ridge
    mse_ridge = np.mean((y - y_ridge) ** 2)
    w_norm = np.sqrt(np.sum(w_ridge[1:]**2))
    print(f"  alpha={alpha:7.3f}: MSE={mse_ridge:.4f}, ||w||={w_norm:.4f}")


# =====================================================================
#   PARTE 5: CROSS-VALIDATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: CROSS-VALIDATION ===")
print("=" * 80)

"""
Cross-validation: evaluar modelo sin test set separado.

K-Fold:
  1. Dividir datos en K folds.
  2. Para cada fold i:
     - Train en los otros K-1 folds.
     - Test en fold i.
  3. Promediar los K scores.

Variantes:
  - Stratified K-Fold: mantener proporcion de clases.
  - Leave-One-Out (LOO): K = N (costoso).
  - Time Series Split: respetar temporalidad.
  - Repeated K-Fold: repetir K-Fold N veces.
"""

print("\n--- K-Fold manual ---")

def kfold_cv(X, y, k=5, degree=3):
    """K-Fold cross-validation para polynomial regression."""
    n = len(X)
    fold_size = n // k
    indices = np.arange(n)
    np.random.shuffle(indices)
    
    scores = []
    for i in range(k):
        start = i * fold_size
        end = start + fold_size if i < k-1 else n
        
        val_idx = indices[start:end]
        train_idx = np.concatenate([indices[:start], indices[end:]])
        
        X_train = poly_features(X[train_idx], degree)
        y_train = y[train_idx]
        X_val = poly_features(X[val_idx], degree)
        y_val = y[val_idx]
        
        w = np.linalg.lstsq(X_train, y_train, rcond=None)[0]
        y_pred = X_val @ w
        mse = np.mean((y_val - y_pred) ** 2)
        scores.append(mse)
    
    return np.array(scores)

for degree in [1, 2, 3, 5, 8]:
    scores = kfold_cv(x, y, k=5, degree=degree)
    print(f"  Degree {degree}: MSE={scores.mean():.4f} ± {scores.std():.4f}")


# =====================================================================
#   PARTE 6: LEARNING CURVES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: LEARNING CURVES ===")
print("=" * 80)

"""
Learning curves: performance vs training set size.

Diagnostico:
  - Alto bias: train y val convergen a error alto.
  - Alta varianza: gap grande entre train y val.
  - Buen fit: ambos convergen a error bajo.
"""

print("\n--- Learning curves ---")

def learning_curve(X, y, degree=3, sizes=None):
    """Calcular learning curves."""
    if sizes is None:
        sizes = [10, 20, 30, 50, 80, 120, 180]
    
    train_scores = []
    val_scores = []
    
    for size in sizes:
        if size >= len(X):
            break
        
        # Train on subset
        X_train = poly_features(X[:size], degree)
        y_train = y[:size]
        X_val = poly_features(X[size:], degree)
        y_val = y[size:]
        
        if len(y_val) < 5:
            break
        
        w = np.linalg.lstsq(X_train, y_train, rcond=None)[0]
        
        train_mse = np.mean((y_train - X_train @ w) ** 2)
        val_mse = np.mean((y_val - X_val @ w) ** 2)
        
        train_scores.append(train_mse)
        val_scores.append(val_mse)
    
    return train_scores, val_scores

# Generar mas datos
x_lc, y_lc = generate_data(200)

for degree, label in [(1, 'High Bias'), (3, 'Good'), (10, 'High Variance')]:
    train_s, val_s = learning_curve(x_lc, y_lc, degree)
    print(f"  Degree {degree:2d} ({label:13s}): train_final={train_s[-1]:.4f}, val_final={val_s[-1]:.4f}")


# =====================================================================
#   PARTE 7: GRADIENT DESCENT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: GRADIENT DESCENT ===")
print("=" * 80)

"""
Gradient Descent: optimizacion iterativa.

w = w - lr * gradient(Loss, w)

Variantes:
1. Batch GD: usa TODOS los datos cada step.
2. Stochastic GD (SGD): usa 1 muestra por step.
3. Mini-batch GD: usa un batch de muestras.
4. Adam: lr adaptativo por parametro.
"""

print("\n--- Batch Gradient Descent ---")

def gradient_descent_linear(X, y, lr=0.01, epochs=1000):
    """Linear regression via gradient descent."""
    n, d = X.shape
    w = np.zeros(d)
    
    history = []
    for epoch in range(epochs):
        y_pred = X @ w
        error = y_pred - y
        gradient = (2/n) * X.T @ error
        w = w - lr * gradient
        loss = np.mean(error ** 2)
        
        if epoch % 200 == 0:
            history.append((epoch, loss))
    
    return w, history

# Datos estandarizados
X_gd = np.column_stack([np.ones(len(x)), (x - x.mean()) / x.std()])
y_gd = y

w_gd, hist = gradient_descent_linear(X_gd, y_gd, lr=0.1, epochs=1000)
print(f"  Weights: {w_gd.round(4)}")
for epoch, loss in hist:
    print(f"    Epoch {epoch:4d}: loss={loss:.4f}")


print("\n--- SGD ---")

def sgd_linear(X, y, lr=0.01, epochs=100):
    """Stochastic Gradient Descent."""
    n, d = X.shape
    w = np.zeros(d)
    
    for epoch in range(epochs):
        indices = np.random.permutation(n)
        for i in indices:
            xi = X[i:i+1]
            yi = y[i:i+1]
            error = xi @ w - yi
            gradient = 2 * xi.T @ error
            w = w - lr * gradient
    
    return w

w_sgd = sgd_linear(X_gd, y_gd, lr=0.01, epochs=50)
print(f"  SGD weights: {w_sgd.round(4)}")


print("\n--- Mini-batch GD ---")

def minibatch_gd(X, y, lr=0.01, epochs=100, batch_size=16):
    """Mini-batch Gradient Descent."""
    n, d = X.shape
    w = np.zeros(d)
    
    for epoch in range(epochs):
        indices = np.random.permutation(n)
        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            batch_idx = indices[start:end]
            Xi = X[batch_idx]
            yi = y[batch_idx]
            
            error = Xi @ w - yi
            gradient = (2/len(yi)) * Xi.T @ error
            w = w - lr * gradient
    
    return w

w_mb = minibatch_gd(X_gd, y_gd, lr=0.05, epochs=50, batch_size=16)
print(f"  Mini-batch weights: {w_mb.round(4)}")


# =====================================================================
#   PARTE 8: LOSS FUNCTIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: LOSS FUNCTIONS ===")
print("=" * 80)

"""
REGRESSION:
  - MSE: Mean Squared Error = mean((y - y_hat)^2)
  - MAE: Mean Absolute Error = mean(|y - y_hat|)
  - RMSE: sqrt(MSE)
  - Huber: MSE para errores pequeños, MAE para grandes.
  - R^2: 1 - SS_res / SS_tot (coeficiente de determinacion)

CLASSIFICATION:
  - Cross-Entropy: -sum(y * log(p))
  - Binary CE: -[y*log(p) + (1-y)*log(1-p)]
  - Hinge Loss (SVM): max(0, 1 - y*f(x))
  - Focal Loss: -alpha * (1-p)^gamma * log(p)
"""

print("\n--- Implementaciones ---")

y_true = np.array([3.0, 5.0, 2.5, 7.0, 4.5])
y_pred_r = np.array([2.8, 5.2, 2.3, 6.5, 4.8])

mse = np.mean((y_true - y_pred_r) ** 2)
mae = np.mean(np.abs(y_true - y_pred_r))
rmse = np.sqrt(mse)
ss_res = np.sum((y_true - y_pred_r) ** 2)
ss_tot = np.sum((y_true - y_true.mean()) ** 2)
r2 = 1 - ss_res / ss_tot

print(f"  MSE:  {mse:.4f}")
print(f"  MAE:  {mae:.4f}")
print(f"  RMSE: {rmse:.4f}")
print(f"  R²:   {r2:.4f}")


print("\n--- Huber Loss ---")

def huber_loss(y_true, y_pred, delta=1.0):
    error = y_true - y_pred
    is_small = np.abs(error) <= delta
    squared = 0.5 * error ** 2
    linear = delta * np.abs(error) - 0.5 * delta ** 2
    return np.mean(np.where(is_small, squared, linear))

for delta in [0.5, 1.0, 2.0]:
    h = huber_loss(y_true, y_pred_r, delta)
    print(f"  Huber(delta={delta}): {h:.4f}")


print("\n--- Cross-Entropy ---")

def binary_cross_entropy(y_true, y_pred, eps=1e-15):
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

y_binary = np.array([1, 0, 1, 1, 0])
p_good = np.array([0.9, 0.1, 0.8, 0.7, 0.2])
p_bad = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
p_worst = np.array([0.1, 0.9, 0.2, 0.3, 0.8])

print(f"  BCE (good):  {binary_cross_entropy(y_binary, p_good):.4f}")
print(f"  BCE (bad):   {binary_cross_entropy(y_binary, p_bad):.4f}")
print(f"  BCE (worst): {binary_cross_entropy(y_binary, p_worst):.4f}")


# =====================================================================
#   PARTE 9: METRICS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: METRICS ===")
print("=" * 80)

"""
CLASSIFICATION METRICS:
  - Accuracy: (TP + TN) / (TP + TN + FP + FN)
  - Precision: TP / (TP + FP) -> "de los que dije positivo, cuantos lo eran"
  - Recall: TP / (TP + FN) -> "de los positivos, cuantos detecte"
  - F1 Score: 2 * P * R / (P + R) -> harmonic mean
  - AUC-ROC: area bajo curva ROC
  - Log Loss: cross-entropy promedio
"""

print("\n--- Confusion matrix metrics ---")

def classification_metrics(y_true, y_pred):
    """Calcular todas las metricas de clasificacion."""
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    return {
        'TP': tp, 'TN': tn, 'FP': fp, 'FN': fn,
        'Accuracy': accuracy, 'Precision': precision,
        'Recall': recall, 'F1': f1, 'Specificity': specificity,
    }

np.random.seed(42)
y_true_c = np.random.binomial(1, 0.3, 200)
y_pred_c = np.where(np.random.random(200) > 0.4, y_true_c, 1 - y_true_c)

metrics = classification_metrics(y_true_c, y_pred_c)
for name, value in metrics.items():
    if isinstance(value, float):
        print(f"  {name:12s}: {value:.4f}")
    else:
        print(f"  {name:12s}: {value}")


print("\n--- Precision vs Recall tradeoff ---")

scores = np.random.random(200)
for threshold in [0.3, 0.4, 0.5, 0.6, 0.7]:
    y_pred_t = (scores > threshold).astype(int)
    m = classification_metrics(y_true_c, y_pred_t)
    print(f"  threshold={threshold}: P={m['Precision']:.3f} R={m['Recall']:.3f} F1={m['F1']:.3f}")


# =====================================================================
#   PARTE 10: FEATURE SCALING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: FEATURE SCALING ===")
print("=" * 80)

"""
CUANDO ESCALAR:
  - Gradient-based: SIEMPRE (neural nets, logistic reg, SVM)
  - Distance-based: SIEMPRE (KNN, K-Means, PCA)
  - Tree-based: NO necesario (Random Forest, XGBoost)

TIPOS:
  - StandardScaler: (x - mean) / std -> mean=0, std=1
  - MinMaxScaler: (x - min) / (max - min) -> [0, 1]
  - RobustScaler: (x - median) / IQR -> resistente a outliers
  - MaxAbsScaler: x / max(|x|) -> [-1, 1]
"""

print("\n--- Comparacion ---")

data = np.array([1, 5, 10, 50, 100, 500, 1000], dtype=float)

# Standard
std_scaled = (data - data.mean()) / data.std()
# MinMax
mm_scaled = (data - data.min()) / (data.max() - data.min())
# Robust
median = np.median(data)
q1, q3 = np.percentile(data, [25, 75])
robust_scaled = (data - median) / (q3 - q1)

print(f"  Original:  {data}")
print(f"  Standard:  {std_scaled.round(3)}")
print(f"  MinMax:    {mm_scaled.round(3)}")
print(f"  Robust:    {robust_scaled.round(3)}")


print("\n--- Impacto en GD ---")

np.random.seed(42)
X_unscaled = np.column_stack([
    np.random.randn(100) * 1,
    np.random.randn(100) * 1000,
])
y_gd2 = 3 * X_unscaled[:, 0] + 0.005 * X_unscaled[:, 1] + np.random.randn(100)

X_with_bias = np.column_stack([np.ones(100), X_unscaled])
X_scaled_bias = np.column_stack([
    np.ones(100),
    (X_unscaled[:, 0] - X_unscaled[:, 0].mean()) / X_unscaled[:, 0].std(),
    (X_unscaled[:, 1] - X_unscaled[:, 1].mean()) / X_unscaled[:, 1].std(),
])

start = time.perf_counter()
w1, h1 = gradient_descent_linear(X_scaled_bias, y_gd2, lr=0.1, epochs=500)
t_scaled = time.perf_counter() - start

print(f"  Scaled GD: {t_scaled:.4f}s, final_loss={h1[-1][1]:.4f}")


# =====================================================================
#   PARTE 11: ADAM OPTIMIZER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: ADAM OPTIMIZER ===")
print("=" * 80)

"""
Adam: Adaptive Moment Estimation.
Combina momentum + RMSprop.
  m = beta1 * m + (1-beta1) * g         (first moment)
  v = beta2 * v + (1-beta2) * g^2       (second moment)
  m_hat = m / (1 - beta1^t)             (bias correction)
  v_hat = v / (1 - beta2^t)
  w = w - lr * m_hat / (sqrt(v_hat) + eps)
"""

def adam_optimizer(X, y, lr=0.001, epochs=500, beta1=0.9, beta2=0.999, eps=1e-8):
    """Adam optimizer for linear regression."""
    n, d = X.shape
    w = np.zeros(d)
    m = np.zeros(d)
    v = np.zeros(d)
    
    history = []
    for t in range(1, epochs + 1):
        grad = (2/n) * X.T @ (X @ w - y)
        
        m = beta1 * m + (1 - beta1) * grad
        v = beta2 * v + (1 - beta2) * grad**2
        
        m_hat = m / (1 - beta1**t)
        v_hat = v / (1 - beta2**t)
        
        w = w - lr * m_hat / (np.sqrt(v_hat) + eps)
        
        if t % 100 == 0:
            loss = np.mean((X @ w - y)**2)
            history.append((t, loss))
    
    return w, history

w_adam, hist_adam = adam_optimizer(X_scaled_bias, y_gd2, lr=0.01, epochs=500)
print(f"  Adam weights: {w_adam.round(4)}")
for t, loss in hist_adam:
    print(f"    Step {t:4d}: loss={loss:.4f}")


# =====================================================================
#   PARTE 12: LEARNING RATE SCHEDULES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: LR SCHEDULES ===")
print("=" * 80)

"""
Learning Rate Schedules:
1. Step decay: lr = lr * factor every N epochs.
2. Exponential: lr = lr_0 * exp(-k * t).
3. Cosine annealing: lr = lr_min + 0.5*(lr_max-lr_min)*(1+cos(pi*t/T)).
4. Warm-up + decay: linearly increase then decay.
"""

print("\n--- Schedule comparison ---")

def step_decay(lr0, epoch, drop=0.5, epochs_drop=100):
    return lr0 * (drop ** (epoch // epochs_drop))

def exp_decay(lr0, epoch, k=0.01):
    return lr0 * np.exp(-k * epoch)

def cosine_annealing(lr0, epoch, T=500, lr_min=1e-6):
    return lr_min + 0.5 * (lr0 - lr_min) * (1 + np.cos(np.pi * epoch / T))

lr0 = 0.1
for epoch in [0, 100, 200, 300, 400, 500]:
    s = step_decay(lr0, epoch)
    e = exp_decay(lr0, epoch)
    c = cosine_annealing(lr0, epoch)
    print(f"  Epoch {epoch:3d}: step={s:.5f} exp={e:.5f} cosine={c:.5f}")


# =====================================================================
#   PARTE 13: DATA LEAKAGE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: DATA LEAKAGE ===")
print("=" * 80)

"""
DATA LEAKAGE: informacion del test contamina el training.

CAUSAS COMUNES:
1. Scaling ANTES de split (usa stats de test).
2. Feature engineering con datos futuros.
3. Target leakage (feature correlada con target).
4. Duplicados entre train y test.

SOLUCION:
1. SIEMPRE split primero.
2. fit_transform(train), transform(test).
3. Pipeline que encapsule preprocessing.
"""

print("\n--- Ejemplo de leakage ---")

np.random.seed(42)
X_leak = np.random.randn(100, 5)
y_leak = (X_leak[:, 0] + X_leak[:, 1] > 0).astype(int)

# MAL: scale antes de split
X_bad_scaled = (X_leak - X_leak.mean(0)) / X_leak.std(0)
X_bad_train, X_bad_test = X_bad_scaled[:80], X_bad_scaled[80:]
print(f"  BAD: scaled with ALL data stats")

# BIEN: split, luego scale con train stats
X_good_train, X_good_test = X_leak[:80], X_leak[80:]
train_mean = X_good_train.mean(0)
train_std = X_good_train.std(0)
X_good_train_s = (X_good_train - train_mean) / train_std
X_good_test_s = (X_good_test - train_mean) / train_std
print(f"  GOOD: scaled with TRAIN-ONLY stats")


# =====================================================================
#   PARTE 14: STRATIFIED SPLIT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: STRATIFIED SPLIT ===")
print("=" * 80)

def stratified_split(X, y, test_frac=0.2, seed=42):
    """Split manteniendo proporcion de clases."""
    np.random.seed(seed)
    classes = np.unique(y)
    train_idx, test_idx = [], []
    
    for c in classes:
        c_idx = np.where(y == c)[0]
        np.random.shuffle(c_idx)
        split = int(len(c_idx) * (1 - test_frac))
        train_idx.extend(c_idx[:split])
        test_idx.extend(c_idx[split:])
    
    return np.array(train_idx), np.array(test_idx)

# Datos desbalanceados
y_imb = np.array([0]*900 + [1]*100)
train_i, test_i = stratified_split(np.zeros((1000, 1)), y_imb)

print(f"  Original ratio: {y_imb.mean():.3f}")
print(f"  Train ratio:    {y_imb[train_i].mean():.3f}")
print(f"  Test ratio:     {y_imb[test_i].mean():.3f}")
print(f"  Stratified: ratios preserved!")


# =====================================================================
#   PARTE 15: TRAIN / VAL / TEST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: TRAIN/VAL/TEST ===")
print("=" * 80)

"""
3-way split:
  - Train (60-70%): entrenar modelo.
  - Validation (15-20%): tuning hiperparametros.
  - Test (15-20%): evaluacion final (SOLO UNA VEZ).

REGLA CRITICA:
  NUNCA usar test set para decisiones de modelo.
  Test = evaluacion final, punto.
"""

def three_way_split(X, y, val_frac=0.15, test_frac=0.15):
    n = len(y)
    idx = np.random.permutation(n)
    test_n = int(n * test_frac)
    val_n = int(n * val_frac)
    
    test_idx = idx[:test_n]
    val_idx = idx[test_n:test_n + val_n]
    train_idx = idx[test_n + val_n:]
    
    return train_idx, val_idx, test_idx

np.random.seed(42)
tr, va, te = three_way_split(np.zeros(1000), np.zeros(1000))
print(f"  Train: {len(tr)} ({len(tr)/1000:.0%})")
print(f"  Val:   {len(va)} ({len(va)/1000:.0%})")
print(f"  Test:  {len(te)} ({len(te)/1000:.0%})")


# =====================================================================
#   PARTE 16: EARLY STOPPING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: EARLY STOPPING ===")
print("=" * 80)

"""
Early stopping: parar entrenamiento cuando val loss deja de mejorar.
Evita overfitting sin necesidad de regularizacion explicita.
"""

def train_with_early_stopping(X_train, y_train, X_val, y_val, 
                               lr=0.01, max_epochs=1000, patience=10):
    """GD con early stopping."""
    n, d = X_train.shape
    w = np.zeros(d)
    best_w = w.copy()
    best_val_loss = float('inf')
    no_improve = 0
    
    for epoch in range(max_epochs):
        grad = (2/n) * X_train.T @ (X_train @ w - y_train)
        w -= lr * grad
        
        val_loss = np.mean((X_val @ w - y_val)**2)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_w = w.copy()
            no_improve = 0
        else:
            no_improve += 1
        
        if no_improve >= patience:
            print(f"  Early stop at epoch {epoch}, best_val_loss={best_val_loss:.4f}")
            return best_w, epoch
    
    return best_w, max_epochs

# Demo
X_es = np.column_stack([np.ones(50), np.random.randn(50, 3)])
y_es = X_es @ np.array([1, 2, -1, 0.5]) + np.random.randn(50) * 0.5
X_es_val = np.column_stack([np.ones(20), np.random.randn(20, 3)])
y_es_val = X_es_val @ np.array([1, 2, -1, 0.5]) + np.random.randn(20) * 0.5

w_es, stopped = train_with_early_stopping(X_es, y_es, X_es_val, y_es_val, patience=50)


# =====================================================================
#   PARTE 17: HYPERPARAMETER TUNING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: HYPERPARAMETER TUNING ===")
print("=" * 80)

"""
Metodos:
1. Grid Search: probar todas las combinaciones.
2. Random Search: muestrear aleatorio (mejor para alta dimension).
3. Bayesian Optimization: modelo surrogate (TPE, GP).

REGLA: usar validation set, NUNCA test set.
"""

print("\n--- Grid search ---")

def grid_search_ridge(X_train, y_train, X_val, y_val, alphas):
    """Grid search para Ridge alpha."""
    best_alpha = None
    best_score = float('inf')
    
    for alpha in alphas:
        n, d = X_train.shape
        I = np.eye(d)
        I[0, 0] = 0
        w = np.linalg.solve(X_train.T @ X_train + alpha * I, X_train.T @ y_train)
        val_mse = np.mean((X_val @ w - y_val)**2)
        
        if val_mse < best_score:
            best_score = val_mse
            best_alpha = alpha
        
        print(f"    alpha={alpha:8.4f}: val_MSE={val_mse:.4f}")
    
    return best_alpha, best_score

alphas = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
best_a, best_s = grid_search_ridge(X_es, y_es, X_es_val, y_es_val, alphas)
print(f"  Best: alpha={best_a}, val_MSE={best_s:.4f}")


# =====================================================================
#   PARTE 18: NO FREE LUNCH THEOREM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: NO FREE LUNCH ===")
print("=" * 80)

"""
NO FREE LUNCH THEOREM:
  No existe un algoritmo universalmente superior.
  Todo algoritmo que funciona bien en un problema,
  funciona mal en otro.

IMPLICACIONES:
  1. SIEMPRE probar multiples modelos.
  2. El conocimiento del dominio es crucial.
  3. La "mejor" tecnica depende del dataset.
  4. Baselines simples primero (logistic regression, linear).
  5. Complejidad creciente solo si se justifica.

WORKFLOW RECOMENDADO:
  1. Baseline: LogisticRegression / LinearRegression.
  2. Tree-based: RandomForest / XGBoost.
  3. Si necesario: SVM, Neural Networks.
  4. Comparar con CV y significancia estadistica.
"""

print("  No Free Lunch: no universal best algorithm")
print("  Always try multiple models and compare")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE TEORIA ML:

1. ML = Supervised + Unsupervised + Reinforcement.
2. Bias-Variance Tradeoff: balance entre simplicidad y complejidad.
3. Overfitting: mas datos, regularizacion, early stopping.
4. L1 (Lasso) para feature selection, L2 (Ridge) para shrinkage.
5. K-Fold CV: evaluacion robusta sin test set separado.
6. Learning curves: diagnosticar bias vs variance.
7. Gradient descent: batch, SGD, mini-batch.
8. Loss: MSE (regression), Cross-Entropy (classification).
9. Metrics: Accuracy, Precision, Recall, F1, AUC.
10. Feature scaling: SIEMPRE para gradient/distance-based models.

Siguiente archivo: Regresion.
"""

print("\n FIN DE ARCHIVO 01_teoria_ml.")
print(" Teoria de ML ha sido dominada.")
