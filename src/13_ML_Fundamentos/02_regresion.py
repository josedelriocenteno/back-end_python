# ===========================================================================
# 02_regresion.py
# ===========================================================================
# MODULO 13: ML FUNDAMENTOS
# ARCHIVO 02: Regresion (Linear, Polynomial, Regularized)
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Implementar regresion desde cero: OLS, polynomial,
# Ridge, Lasso, y diagnosticos.
#
# CONTENIDO:
#   1. Linear Regression (OLS).
#   2. Normal equation.
#   3. Polynomial Regression.
#   4. Ridge Regression.
#   5. Lasso Regression.
#   6. Elastic Net.
#   7. Diagnosticos de regresion.
#   8. Feature importance.
#   9. Multicollinearity (VIF).
#   10. Regression completa end-to-end.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: LINEAR REGRESSION (OLS)
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: LINEAR REGRESSION ===")
print("=" * 80)

"""
Ordinary Least Squares (OLS):
  min sum((y - X@w)^2)
  
Solucion analitica (Normal Equation):
  w = (X^T X)^{-1} X^T y

Complejidad: O(n * d^2 + d^3)
  - n: numero de muestras
  - d: numero de features
"""

print("\n--- Datos sinteticos ---")

np.random.seed(42)
n = 200
X_raw = np.random.randn(n, 3)
true_w = np.array([3.0, -1.5, 0.5])
true_b = 2.0
y = X_raw @ true_w + true_b + np.random.randn(n) * 0.5

print(f"  Shape: X={X_raw.shape}, y={y.shape}")
print(f"  True weights: {true_w}, bias: {true_b}")


print("\n--- Normal Equation ---")

# Agregar bias (columna de 1s)
X = np.column_stack([np.ones(n), X_raw])

start = time.perf_counter()
w_ols = np.linalg.solve(X.T @ X, X.T @ y)
t_ols = time.perf_counter() - start

print(f"  OLS weights: {w_ols.round(4)}")
print(f"  Time: {t_ols:.6f}s")

# Metricas
y_pred = X @ w_ols
mse = np.mean((y - y_pred) ** 2)
ss_res = np.sum((y - y_pred) ** 2)
ss_tot = np.sum((y - y.mean()) ** 2)
r2 = 1 - ss_res / ss_tot

print(f"  MSE: {mse:.4f}")
print(f"  R²:  {r2:.4f}")


print("\n--- Gradient Descent comparison ---")

def gd_linear(X, y, lr=0.01, epochs=1000):
    w = np.zeros(X.shape[1])
    for _ in range(epochs):
        grad = (2/len(y)) * X.T @ (X @ w - y)
        w -= lr * grad
    return w

start = time.perf_counter()
w_gd = gd_linear(X, y, lr=0.01, epochs=2000)
t_gd = time.perf_counter() - start

print(f"  GD weights:  {w_gd.round(4)}")
print(f"  GD time:     {t_gd:.4f}s")
print(f"  Match OLS:   {np.allclose(w_ols, w_gd, atol=0.01)}")


# =====================================================================
#   PARTE 2: POLYNOMIAL REGRESSION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: POLYNOMIAL REGRESSION ===")
print("=" * 80)

"""
Polynomial: y = w0 + w1*x + w2*x^2 + ... + wd*x^d
Es LINEAR regression con features no-lineales.
"""

print("\n--- Generar datos no-lineales ---")

np.random.seed(42)
x_nl = np.sort(np.random.uniform(-3, 3, 100))
y_nl = 0.5 * x_nl**3 - 2 * x_nl**2 + x_nl + 3 + np.random.randn(100) * 2

def polynomial_features(x, degree):
    """Crear features polinomiales."""
    return np.column_stack([x**i for i in range(degree + 1)])

print(f"  Data: {len(x_nl)} points, cubic function + noise")


print("\n--- Fit con diferentes grados ---")

for degree in [1, 2, 3, 5, 10, 15]:
    X_poly = polynomial_features(x_nl, degree)
    w = np.linalg.lstsq(X_poly, y_nl, rcond=None)[0]
    y_pred_p = X_poly @ w
    
    mse_train = np.mean((y_nl - y_pred_p) ** 2)
    
    # Test en nuevos puntos
    x_test = np.linspace(-3, 3, 200)
    y_true_test = 0.5 * x_test**3 - 2 * x_test**2 + x_test + 3
    X_test = polynomial_features(x_test, degree)
    y_pred_test = X_test @ w
    mse_test = np.mean((y_true_test - y_pred_test) ** 2)
    
    status = ""
    if degree <= 2:
        status = "(underfit)"
    elif degree == 3:
        status = "(optimal)"
    elif degree >= 10:
        status = "(overfit)"
    
    print(f"  Degree {degree:2d}: train_MSE={mse_train:8.3f}, test_MSE={mse_test:8.3f} {status}")


# =====================================================================
#   PARTE 3: RIDGE REGRESSION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: RIDGE REGRESSION ===")
print("=" * 80)

"""
Ridge (L2 Regularization):
  min sum((y - X@w)^2) + alpha * sum(w^2)

Solucion: w = (X^T X + alpha*I)^{-1} X^T y

Efecto: shrink weights toward zero.
"""

class RidgeRegression:
    """Ridge regression from scratch."""
    
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.weights = None
    
    def fit(self, X, y):
        n, d = X.shape
        I = np.eye(d)
        I[0, 0] = 0  # Don't regularize bias
        self.weights = np.linalg.solve(
            X.T @ X + self.alpha * I,
            X.T @ y
        )
        return self
    
    def predict(self, X):
        return X @ self.weights
    
    def score(self, X, y):
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        return 1 - ss_res / ss_tot

print("\n--- Ridge path (alpha sweep) ---")

X_poly15 = polynomial_features(x_nl, 15)

print(f"  {'Alpha':>10s} {'Train R²':>10s} {'||w||':>10s}")
for alpha in [0, 0.001, 0.01, 0.1, 1, 10, 100, 1000]:
    ridge = RidgeRegression(alpha=alpha).fit(X_poly15, y_nl)
    r2_train = ridge.score(X_poly15, y_nl)
    w_norm = np.sqrt(np.sum(ridge.weights[1:]**2))
    print(f"  {alpha:10.3f} {r2_train:10.4f} {w_norm:10.2f}")


# =====================================================================
#   PARTE 4: LASSO REGRESSION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: LASSO REGRESSION ===")
print("=" * 80)

"""
Lasso (L1 Regularization):
  min sum((y - X@w)^2) + alpha * sum(|w|)

No tiene solucion analitica. Usar coordinate descent.

Efecto: puede poner weights a ZERO (feature selection).
"""

class LassoRegression:
    """Lasso via coordinate descent."""
    
    def __init__(self, alpha=1.0, max_iter=1000, tol=1e-4):
        self.alpha = alpha
        self.max_iter = max_iter
        self.tol = tol
        self.weights = None
    
    def _soft_threshold(self, x, threshold):
        return np.sign(x) * max(abs(x) - threshold, 0)
    
    def fit(self, X, y):
        n, d = X.shape
        self.weights = np.zeros(d)
        
        for iteration in range(self.max_iter):
            w_old = self.weights.copy()
            
            for j in range(d):
                residual = y - X @ self.weights + X[:, j] * self.weights[j]
                rho = X[:, j] @ residual / n
                
                if j == 0:  # Don't regularize bias
                    self.weights[j] = rho
                else:
                    norm_j = np.sum(X[:, j] ** 2) / n
                    self.weights[j] = self._soft_threshold(rho, self.alpha) / norm_j
            
            if np.max(np.abs(self.weights - w_old)) < self.tol:
                break
        
        return self
    
    def predict(self, X):
        return X @ self.weights
    
    def n_nonzero(self):
        return np.sum(np.abs(self.weights[1:]) > 1e-8)

print("\n--- Lasso feature selection ---")

np.random.seed(42)
n_lasso = 100
d_lasso = 20
X_lasso = np.column_stack([np.ones(n_lasso), np.random.randn(n_lasso, d_lasso)])
true_w_lasso = np.zeros(d_lasso + 1)
true_w_lasso[0] = 1.0  # bias
true_w_lasso[1] = 3.0
true_w_lasso[3] = -2.0
true_w_lasso[5] = 1.5
y_lasso = X_lasso @ true_w_lasso + np.random.randn(n_lasso) * 0.5

print(f"  True non-zero features: {np.sum(np.abs(true_w_lasso[1:]) > 0)}")

for alpha in [0.001, 0.01, 0.1, 0.5, 1.0]:
    lasso = LassoRegression(alpha=alpha).fit(X_lasso, y_lasso)
    y_pred_l = lasso.predict(X_lasso)
    mse_l = np.mean((y_lasso - y_pred_l) ** 2)
    print(f"  alpha={alpha:.3f}: non-zero={lasso.n_nonzero():2d}/{d_lasso}, MSE={mse_l:.4f}")


# =====================================================================
#   PARTE 5: ELASTIC NET
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: ELASTIC NET ===")
print("=" * 80)

"""
Elastic Net: L1 + L2
  min sum((y - X@w)^2) + alpha * (r * L1 + (1-r)/2 * L2)

r=1: Lasso puro
r=0: Ridge puro
"""

print("\n--- Elastic Net ---")

class ElasticNet:
    def __init__(self, alpha=1.0, l1_ratio=0.5, max_iter=1000, tol=1e-4):
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.max_iter = max_iter
        self.tol = tol
        self.weights = None
    
    def fit(self, X, y):
        n, d = X.shape
        self.weights = np.zeros(d)
        l1 = self.alpha * self.l1_ratio
        l2 = self.alpha * (1 - self.l1_ratio)
        
        for _ in range(self.max_iter):
            w_old = self.weights.copy()
            for j in range(d):
                residual = y - X @ self.weights + X[:, j] * self.weights[j]
                rho = X[:, j] @ residual / n
                norm_j = np.sum(X[:, j]**2) / n + l2
                
                if j == 0:
                    self.weights[j] = rho / (np.sum(X[:, j]**2) / n)
                else:
                    self.weights[j] = np.sign(rho) * max(abs(rho) - l1, 0) / norm_j
            
            if np.max(np.abs(self.weights - w_old)) < self.tol:
                break
        return self
    
    def predict(self, X):
        return X @ self.weights

for ratio in [0.0, 0.25, 0.5, 0.75, 1.0]:
    en = ElasticNet(alpha=0.1, l1_ratio=ratio).fit(X_lasso, y_lasso)
    n_nz = np.sum(np.abs(en.weights[1:]) > 1e-8)
    y_pred_en = en.predict(X_lasso)
    mse_en = np.mean((y_lasso - y_pred_en) ** 2)
    label = {0.0: 'Ridge', 0.5: 'Mixed', 1.0: 'Lasso'}.get(ratio, '')
    print(f"  l1_ratio={ratio:.2f} {label:>5s}: nonzero={n_nz:2d}, MSE={mse_en:.4f}")


# =====================================================================
#   PARTE 6: DIAGNOSTICOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: DIAGNOSTICOS ===")
print("=" * 80)

print("\n--- Residual analysis ---")

y_pred_diag = X @ w_ols
residuals = y - y_pred_diag

print(f"  Residual mean:    {residuals.mean():.6f} (should be ~0)")
print(f"  Residual std:     {residuals.std():.4f}")
print(f"  Residual skew:    {((residuals - residuals.mean())**3).mean() / residuals.std()**3:.4f}")
print(f"  Residual kurtosis:{((residuals - residuals.mean())**4).mean() / residuals.std()**4:.4f} (normal=3)")


print("\n--- Durbin-Watson (autocorrelation) ---")

def durbin_watson(residuals):
    diff = np.diff(residuals)
    return np.sum(diff**2) / np.sum(residuals**2)

dw = durbin_watson(residuals)
print(f"  Durbin-Watson: {dw:.4f}")
print(f"  Interpretation: {'No autocorrelation' if 1.5 < dw < 2.5 else 'Possible autocorrelation'}")


print("\n--- VIF (Variance Inflation Factor) ---")

def calculate_vif(X):
    """Calcular VIF para detectar multicollinearity."""
    vifs = []
    for i in range(X.shape[1]):
        y_i = X[:, i]
        X_other = np.delete(X, i, axis=1)
        X_other = np.column_stack([np.ones(len(y_i)), X_other])
        
        w = np.linalg.lstsq(X_other, y_i, rcond=None)[0]
        y_pred_i = X_other @ w
        ss_res = np.sum((y_i - y_pred_i) ** 2)
        ss_tot = np.sum((y_i - y_i.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        
        vif = 1 / (1 - r2) if r2 < 1 else float('inf')
        vifs.append(vif)
    
    return vifs

vifs = calculate_vif(X_raw)
for i, vif in enumerate(vifs):
    status = "OK" if vif < 5 else "⚠ HIGH" if vif < 10 else "✗ CRITICAL"
    print(f"  Feature {i}: VIF={vif:.2f} {status}")


# =====================================================================
#   PARTE 7: PIPELINE COMPLETO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: PIPELINE COMPLETO ===")
print("=" * 80)

def regression_pipeline(X, y, test_frac=0.2, alpha=0.1):
    """Pipeline completo de regresion."""
    n = len(y)
    
    # 1. Split
    idx = np.random.permutation(n)
    split = int(n * (1 - test_frac))
    train_idx, test_idx = idx[:split], idx[split:]
    
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]
    
    # 2. Scale
    mean = X_train[:, 1:].mean(axis=0)
    std = X_train[:, 1:].std(axis=0)
    std[std == 0] = 1
    
    X_train_s = X_train.copy()
    X_test_s = X_test.copy()
    X_train_s[:, 1:] = (X_train[:, 1:] - mean) / std
    X_test_s[:, 1:] = (X_test[:, 1:] - mean) / std
    
    # 3. Fit models
    results = {}
    
    # OLS
    w_ols_p = np.linalg.lstsq(X_train_s, y_train, rcond=None)[0]
    y_pred_ols = X_test_s @ w_ols_p
    results['OLS'] = np.mean((y_test - y_pred_ols) ** 2)
    
    # Ridge
    ridge = RidgeRegression(alpha=alpha).fit(X_train_s, y_train)
    y_pred_ridge = ridge.predict(X_test_s)
    results['Ridge'] = np.mean((y_test - y_pred_ridge) ** 2)
    
    return results

results = regression_pipeline(X, y)
print(f"  Pipeline results:")
for model, mse in results.items():
    print(f"    {model}: test_MSE={mse:.4f}")


# =====================================================================
#   PARTE 8: INTERACTION FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: INTERACTION FEATURES ===")
print("=" * 80)

"""
Interactions: x1*x2, x1*x3, etc.
Capturan efectos combinados de features.
"""

def interaction_features(X):
    """Generar interaction features (pairwise)."""
    n, d = X.shape
    interactions = []
    names = []
    for i in range(d):
        for j in range(i+1, d):
            interactions.append(X[:, i] * X[:, j])
            names.append(f"x{i}*x{j}")
    return np.column_stack(interactions) if interactions else np.empty((n, 0)), names

X_inter, inter_names = interaction_features(X_raw)
X_with_inter = np.column_stack([X, X_inter])

w_inter = np.linalg.lstsq(X_with_inter, y, rcond=None)[0]
y_pred_inter = X_with_inter @ w_inter
mse_inter = np.mean((y - y_pred_inter) ** 2)

print(f"  Original features: {X_raw.shape[1]}")
print(f"  Interaction features: {X_inter.shape[1]} ({inter_names})")
print(f"  MSE without interactions: {mse:.4f}")
print(f"  MSE with interactions:    {mse_inter:.4f}")


# =====================================================================
#   PARTE 9: QUANTILE REGRESSION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: QUANTILE REGRESSION ===")
print("=" * 80)

"""
Quantile regression: predecir cuantiles, no la media.
Loss: pinball loss = max(q*(y-pred), (q-1)*(y-pred))
"""

def pinball_loss(y_true, y_pred, quantile=0.5):
    error = y_true - y_pred
    return np.mean(np.maximum(quantile * error, (quantile - 1) * error))

def quantile_regression_gd(X, y, quantile=0.5, lr=0.001, epochs=1000):
    """Quantile regression via subgradient descent."""
    n, d = X.shape
    w = np.zeros(d)
    
    for _ in range(epochs):
        residual = y - X @ w
        gradient = np.where(residual > 0, -quantile, -(quantile - 1))
        grad = -(1/n) * X.T @ gradient
        w -= lr * grad
    
    return w

print("\n--- Quantile predictions ---")

for q in [0.1, 0.25, 0.5, 0.75, 0.9]:
    w_q = quantile_regression_gd(X, y, quantile=q, lr=0.001, epochs=2000)
    y_pred_q = X @ w_q
    loss = pinball_loss(y, y_pred_q, q)
    print(f"  Q{q:.2f}: pinball_loss={loss:.4f}, mean_pred={y_pred_q.mean():.2f}")


# =====================================================================
#   PARTE 10: ROBUST REGRESSION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: ROBUST REGRESSION ===")
print("=" * 80)

"""
Robust regression: resistente a outliers.
Metodos:
1. Huber regression (Huber loss).
2. RANSAC (Random Sample Consensus).
3. Theil-Sen estimator.
"""

print("\n--- RANSAC ---")

def ransac_regression(X, y, n_iterations=100, sample_size=None, threshold=1.0):
    """RANSAC regression."""
    n, d = X.shape
    if sample_size is None:
        sample_size = d + 1
    
    best_w = None
    best_inliers = 0
    
    for _ in range(n_iterations):
        # Random sample
        idx = np.random.choice(n, sample_size, replace=False)
        X_sample = X[idx]
        y_sample = y[idx]
        
        # Fit on sample
        w = np.linalg.lstsq(X_sample, y_sample, rcond=None)[0]
        
        # Count inliers
        residuals = np.abs(y - X @ w)
        inliers = np.sum(residuals < threshold)
        
        if inliers > best_inliers:
            best_inliers = inliers
            best_w = w
    
    return best_w, best_inliers

# Add outliers
np.random.seed(42)
y_dirty = y.copy()
outlier_idx = np.random.choice(n, 20, replace=False)
y_dirty[outlier_idx] += np.random.randn(20) * 20

# OLS on dirty data
w_dirty = np.linalg.lstsq(X, y_dirty, rcond=None)[0]
mse_dirty = np.mean((y - X @ w_dirty) ** 2)

# RANSAC
w_ransac, n_inliers = ransac_regression(X, y_dirty, threshold=2.0)
mse_ransac = np.mean((y - X @ w_ransac) ** 2)

print(f"  With 20 outliers:")
print(f"    OLS MSE:    {mse_dirty:.4f}")
print(f"    RANSAC MSE: {mse_ransac:.4f} (inliers: {n_inliers}/{n})")


# =====================================================================
#   PARTE 11: COOK'S DISTANCE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: COOK'S DISTANCE ===")
print("=" * 80)

"""
Cook's Distance: medir influencia de cada punto.
D_i = (y_hat - y_hat_{-i})^T (y_hat - y_hat_{-i}) / (p * MSE)

Regla: D_i > 4/n es influyente.
"""

def cooks_distance(X, y):
    """Calcular Cook's distance para cada punto."""
    n, d = X.shape
    H = X @ np.linalg.inv(X.T @ X) @ X.T  # Hat matrix
    h = np.diag(H)
    
    w = np.linalg.lstsq(X, y, rcond=None)[0]
    residuals = y - X @ w
    mse = np.sum(residuals**2) / (n - d)
    
    cooks = (residuals**2 / (d * mse)) * (h / (1 - h)**2)
    return cooks

cooks = cooks_distance(X, y)
threshold = 4 / n
influential = np.sum(cooks > threshold)
print(f"  Cook's Distance threshold: {threshold:.4f}")
print(f"  Influential points: {influential}/{n}")
print(f"  Max Cook's D: {cooks.max():.4f}")
print(f"  Top 5: {np.sort(cooks)[-5:][::-1].round(4)}")


# =====================================================================
#   PARTE 12: CONFIDENCE INTERVALS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: CONFIDENCE INTERVALS ===")
print("=" * 80)

"""
CI para coeficientes:
  SE(w_j) = sqrt(MSE * (X^T X)^{-1}_{jj})
  CI = w_j ± t_{alpha/2, n-d} * SE(w_j)
"""

def coefficient_ci(X, y, alpha=0.05):
    """Confidence intervals for OLS coefficients."""
    n, d = X.shape
    w = np.linalg.lstsq(X, y, rcond=None)[0]
    residuals = y - X @ w
    mse = np.sum(residuals**2) / (n - d)
    
    cov_matrix = mse * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov_matrix))
    
    # Approx t-value for 95% CI
    t_val = 1.96
    lower = w - t_val * se
    upper = w + t_val * se
    
    return w, se, lower, upper

w_ci, se_ci, lower_ci, upper_ci = coefficient_ci(X, y)
print(f"  95% Confidence Intervals:")
names = ['bias', 'x1', 'x2', 'x3']
for i in range(len(w_ci)):
    sig = "*" if (lower_ci[i] > 0 or upper_ci[i] < 0) else " "
    print(f"    {names[i]:5s}: {w_ci[i]:7.4f} ± {se_ci[i]:.4f}  [{lower_ci[i]:7.4f}, {upper_ci[i]:7.4f}] {sig}")


# =====================================================================
#   PARTE 13: FEATURE ENGINEERING PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: FEATURE ENGINEERING ===")
print("=" * 80)

"""
Patrones de feature engineering para regresion:
1. Log transform: para datos con skew positivo.
2. Square root: suavizar grandes valores.
3. Binning: discretizar variables continuas.
4. Polynomial: capturar no-linealidades.
5. Interactions: efectos combinados.
"""

print("\n--- Transforms ---")

np.random.seed(42)
x_skewed = np.random.exponential(2, 200)

print(f"  Original:  mean={x_skewed.mean():.2f}, std={x_skewed.std():.2f}, skew={((x_skewed - x_skewed.mean())**3).mean() / x_skewed.std()**3:.2f}")

x_log = np.log1p(x_skewed)
print(f"  Log(1+x):  mean={x_log.mean():.2f}, std={x_log.std():.2f}, skew={((x_log - x_log.mean())**3).mean() / x_log.std()**3:.2f}")

x_sqrt = np.sqrt(x_skewed)
print(f"  sqrt(x):   mean={x_sqrt.mean():.2f}, std={x_sqrt.std():.2f}, skew={((x_sqrt - x_sqrt.mean())**3).mean() / x_sqrt.std()**3:.2f}")


print("\n--- Binning ---")

def create_bins(x, n_bins=5):
    """Equal-width binning."""
    bins = np.linspace(x.min(), x.max(), n_bins + 1)
    binned = np.digitize(x, bins[:-1]) - 1
    return binned, bins

binned, bins = create_bins(x_skewed, n_bins=5)
for b in range(5):
    count = np.sum(binned == b)
    print(f"    Bin {b}: [{bins[b]:.2f}, {bins[b+1]:.2f}) count={count}")


# =====================================================================
#   PARTE 14: REGULARIZATION PATH
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: REGULARIZATION PATH ===")
print("=" * 80)

"""
Regularization path: como cambian los coeficientes con alpha.
"""

print("\n--- Ridge path ---")

alphas_path = np.logspace(-3, 3, 15)
print(f"  {'Alpha':>10s}", end="")
for i in range(min(5, X_raw.shape[1])):
    print(f"  {'w'+str(i):>8s}", end="")
print()

for alpha in alphas_path:
    ridge_p = RidgeRegression(alpha=alpha).fit(X, y)
    line = f"  {alpha:10.3f}"
    for i in range(min(5, len(ridge_p.weights))):
        line += f"  {ridge_p.weights[i]:8.4f}"
    print(line)


# =====================================================================
#   PARTE 15: BENCHMARK COMPARISON
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: BENCHMARK ===")
print("=" * 80)

print("\n--- Model comparison ---")

np.random.seed(42)
idx_bench = np.random.permutation(n)
split_b = int(n * 0.8)
X_tr_b, X_te_b = X[idx_bench[:split_b]], X[idx_bench[split_b:]]
y_tr_b, y_te_b = y[idx_bench[:split_b]], y[idx_bench[split_b:]]

models_bench = {}

# OLS
w_b = np.linalg.lstsq(X_tr_b, y_tr_b, rcond=None)[0]
models_bench['OLS'] = np.mean((y_te_b - X_te_b @ w_b)**2)

# Ridge
for a in [0.01, 0.1, 1.0]:
    r_b = RidgeRegression(alpha=a).fit(X_tr_b, y_tr_b)
    models_bench[f'Ridge(a={a})'] = np.mean((y_te_b - r_b.predict(X_te_b))**2)

# Mean baseline
models_bench['Mean'] = np.mean((y_te_b - y_tr_b.mean())**2)

print(f"  {'Model':>15s} {'Test MSE':>10s}")
for model, mse_b in sorted(models_bench.items(), key=lambda x: x[1]):
    print(f"  {model:>15s} {mse_b:10.4f}")


# =====================================================================
#   PARTE 16: WEIGHTED LEAST SQUARES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: WEIGHTED LEAST SQUARES ===")
print("=" * 80)

"""
WLS: cada observacion tiene un peso diferente.
  min sum(w_i * (y_i - x_i^T beta)^2)
  
Solucion: beta = (X^T W X)^{-1} X^T W y
donde W = diag(weights)

Util cuando la varianza NO es constante (heteroscedasticity).
"""

def wls_regression(X, y, weights):
    """Weighted Least Squares."""
    W = np.diag(weights)
    return np.linalg.solve(X.T @ W @ X, X.T @ W @ y)

np.random.seed(42)
n_wls = 100
x_wls = np.sort(np.random.uniform(1, 10, n_wls))
# Varianza crece con x
y_wls = 2 * x_wls + 3 + np.random.randn(n_wls) * x_wls * 0.5
X_wls = np.column_stack([np.ones(n_wls), x_wls])

# OLS
w_ols_wls = np.linalg.lstsq(X_wls, y_wls, rcond=None)[0]
# WLS con peso inversamente proporcional a varianza
weights = 1.0 / (x_wls ** 2)
w_wls = wls_regression(X_wls, y_wls, weights)

print(f"  OLS: intercept={w_ols_wls[0]:.3f}, slope={w_ols_wls[1]:.3f}")
print(f"  WLS: intercept={w_wls[0]:.3f}, slope={w_wls[1]:.3f}")
print(f"  True: intercept=3.0, slope=2.0")


# =====================================================================
#   PARTE 17: STEPWISE SELECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: STEPWISE SELECTION ===")
print("=" * 80)

"""
Forward stepwise: agregar features de a uno.
1. Empezar sin features.
2. Para cada feature no seleccionada, evaluar modelo.
3. Agregar la que mas mejore el score.
4. Repetir hasta que no mejore.
"""

def forward_stepwise(X, y, max_features=None):
    """Forward stepwise feature selection."""
    n, d = X.shape
    if max_features is None:
        max_features = d
    
    selected = [0]  # Always include bias
    remaining = list(range(1, d))
    
    best_scores = []
    
    while len(selected) < max_features + 1 and remaining:
        best_score = float('inf')
        best_feat = None
        
        for feat in remaining:
            trial = selected + [feat]
            X_trial = X[:, trial]
            w = np.linalg.lstsq(X_trial, y, rcond=None)[0]
            mse = np.mean((y - X_trial @ w) ** 2)
            
            if mse < best_score:
                best_score = mse
                best_feat = feat
        
        selected.append(best_feat)
        remaining.remove(best_feat)
        best_scores.append((len(selected) - 1, best_score, best_feat))
    
    return selected, best_scores

np.random.seed(42)
n_sw = 100
X_sw = np.column_stack([np.ones(n_sw)] + [np.random.randn(n_sw) for _ in range(10)])
y_sw = 3*X_sw[:, 1] - 2*X_sw[:, 3] + 0.5*X_sw[:, 5] + np.random.randn(n_sw) * 0.5

selected, scores = forward_stepwise(X_sw, y_sw, max_features=6)
print(f"  Forward stepwise:")
for n_feat, mse, feat_idx in scores:
    print(f"    +Feature {feat_idx}: MSE={mse:.4f} ({n_feat} features)")


# =====================================================================
#   PARTE 18: PREDICTION INTERVALS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: PREDICTION INTERVALS ===")
print("=" * 80)

"""
Confidence Interval: incertidumbre sobre la MEDIA de y.
Prediction Interval: incertidumbre sobre un NUEVO y.

PI es siempre mas ancho que CI porque incluye ruido.
PI = y_hat ± t * sqrt(MSE * (1 + x^T (X^T X)^{-1} x))
"""

def prediction_interval(X_train, y_train, x_new, alpha=0.05):
    """Compute prediction interval for new point."""
    w = np.linalg.lstsq(X_train, y_train, rcond=None)[0]
    y_hat = x_new @ w
    
    residuals = y_train - X_train @ w
    n, d = X_train.shape
    mse = np.sum(residuals**2) / (n - d)
    
    XtX_inv = np.linalg.inv(X_train.T @ X_train)
    h = x_new @ XtX_inv @ x_new
    
    t_val = 1.96  # ~95%
    se_pred = np.sqrt(mse * (1 + h))
    
    return y_hat, y_hat - t_val * se_pred, y_hat + t_val * se_pred

x_new = np.array([1.0, 0.5, -0.3, 1.2])
y_hat, lower, upper = prediction_interval(X, y, x_new)
print(f"  New point prediction: {y_hat:.3f}")
print(f"  95% PI: [{lower:.3f}, {upper:.3f}]")
print(f"  Width: {upper - lower:.3f}")


# =====================================================================
#   PARTE 19: HETEROSCEDASTICITY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: HETEROSCEDASTICITY ===")
print("=" * 80)

"""
Heteroscedasticity: varianza de residuales no es constante.
Test: Breusch-Pagan (simplificado).
"""

def breusch_pagan_test(X, y):
    """Simplified Breusch-Pagan test."""
    w = np.linalg.lstsq(X, y, rcond=None)[0]
    residuals = y - X @ w
    residuals_sq = residuals ** 2
    
    # Regress squared residuals on X
    w_bp = np.linalg.lstsq(X, residuals_sq, rcond=None)[0]
    fitted = X @ w_bp
    
    ss_reg = np.sum((fitted - residuals_sq.mean()) ** 2)
    ss_tot = np.sum((residuals_sq - residuals_sq.mean()) ** 2)
    r2 = ss_reg / ss_tot if ss_tot > 0 else 0
    
    n = len(y)
    bp_stat = n * r2
    
    return bp_stat, r2

bp, r2_bp = breusch_pagan_test(X, y)
print(f"  Breusch-Pagan stat: {bp:.4f}")
print(f"  R² of residuals²: {r2_bp:.4f}")
print(f"  Interpretation: {'Heteroscedastic' if bp > 10 else 'Homoscedastic'}")


# =====================================================================
#   PARTE 20: MULTIVARIATE REGRESSION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: MULTIVARIATE ===")
print("=" * 80)

"""
Multiple targets: Y = X @ W, donde Y es (n, k).
Cada columna de Y es un target independiente.
"""

np.random.seed(42)
n_mv = 100
X_mv = np.column_stack([np.ones(n_mv), np.random.randn(n_mv, 3)])
true_W = np.array([[1, 2], [3, -1], [-0.5, 0.5], [2, 1]])
Y_mv = X_mv @ true_W + np.random.randn(n_mv, 2) * 0.3

W_mv = np.linalg.lstsq(X_mv, Y_mv, rcond=None)[0]
Y_pred_mv = X_mv @ W_mv
mse_mv = np.mean((Y_mv - Y_pred_mv) ** 2, axis=0)

print(f"  Targets: {Y_mv.shape[1]}")
for i in range(Y_mv.shape[1]):
    print(f"    Target {i}: MSE={mse_mv[i]:.4f}")
    print(f"      True W:  {true_W[:, i]}")
    print(f"      Fitted W: {W_mv[:, i].round(3)}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE REGRESION:

1. OLS: solucion analitica, baseline obligatoria.
2. Normal equation: O(d^3), preferir para d < 10k.
3. GD: para d grande, necesita feature scaling.
4. Polynomial: features no-lineales, cuidado overfitting.
5. Ridge (L2): shrink weights, no elimina features.
6. Lasso (L1): feature selection automatica.
7. Elastic Net: combina L1+L2.
8. Diagnosticos: residuales, Durbin-Watson, VIF.
9. SIEMPRE: scale -> split -> fit(train) -> eval(test).

Siguiente archivo: Clasificacion.
"""

print("\n FIN DE ARCHIVO 02_regresion.")
print(" Regresion ha sido dominada.")
