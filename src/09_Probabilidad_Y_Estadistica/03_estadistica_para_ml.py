# ===========================================================================
# 03_estadistica_para_ml.py
# ===========================================================================
# MODULO 09: PROBABILIDAD Y ESTADISTICA
# ARCHIVO 03: Estadistica para Machine Learning
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar conceptos estadisticos directamente aplicados a ML:
# KL divergence, entropia, MAP, Bayesian inference, regularizacion.
#
# CONTENIDO:
#   1. Entropia y teoria de la informacion.
#   2. Cross-entropy y KL divergence.
#   3. MAP vs MLE.
#   4. Regularizacion como prior Bayesiano.
#   5. Bias-variance tradeoff.
#   6. Cross-validation.
#   7. Bayesian inference.
#   8. Feature selection estadistica.
#   9. Metricas de clasificacion.
#   10. Calibracion de probabilidades.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: ENTROPIA
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: ENTROPIA ===")
print("=" * 80)

"""
Entropia: medida de incertidumbre de una distribucion.
H(X) = -Σ p(x) * log(p(x))

Alta entropia = mucha incertidumbre.
Baja entropia = poca incertidumbre.

EN ML: la entropia del output de un clasificador indica
cuanta confianza tiene el modelo.
"""

print("\n--- Entropia de distribuciones ---")

def entropy(probs):
    """Entropia de Shannon en bits."""
    probs = np.array(probs)
    probs = probs[probs > 0]  # Evitar log(0)
    return -np.sum(probs * np.log2(probs))

# Distribuciones con diferente entropia
dists = {
    "Segura [1,0,0]":           [1.0, 0.0, 0.0],
    "Casi segura [0.9,0.05,0.05]": [0.9, 0.05, 0.05],
    "Sesgada [0.7,0.2,0.1]":   [0.7, 0.2, 0.1],
    "Uniforme [1/3,1/3,1/3]":   [1/3, 1/3, 1/3],
}

for name, p in dists.items():
    H = entropy(p)
    print(f"  {name:35s}: H = {H:.4f} bits")

print(f"\n  Max entropia para 3 clases = log2(3) = {np.log2(3):.4f}")


print("\n--- Entropia condicional ---")

"""
H(Y|X) = Σ_x P(X=x) * H(Y|X=x)
H(Y|X) <= H(Y) (condicionar REDUCE entropia)
"""

# Ejemplo: Y = clase, X = feature
# P(Y|X=0) = [0.9, 0.1], P(Y|X=1) = [0.4, 0.6]
# P(X=0) = 0.6, P(X=1) = 0.4

H_Y = entropy([0.5, 0.5])
H_Y_X0 = entropy([0.9, 0.1])
H_Y_X1 = entropy([0.4, 0.6])
H_Y_given_X = 0.6 * H_Y_X0 + 0.4 * H_Y_X1

print(f"  H(Y) = {H_Y:.4f}")
print(f"  H(Y|X) = {H_Y_given_X:.4f}")
print(f"  Information Gain = H(Y) - H(Y|X) = {H_Y - H_Y_given_X:.4f}")


# =====================================================================
#   PARTE 2: CROSS-ENTROPY Y KL DIVERGENCE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: CROSS-ENTROPY Y KL DIVERGENCE ===")
print("=" * 80)

"""
Cross-entropy: H(p, q) = -Σ p(x) * log(q(x))
Mide cuantos bits necesitas con distribucion q para codificar p.

KL Divergence: D_KL(p || q) = Σ p(x) * log(p(x)/q(x))
             = H(p, q) - H(p)
Mide cuanto EXTRA necesitas. Siempre >= 0.

EN ML: Cross-entropy loss = constante + KL(true || predicted).
Minimizar CE = minimizar KL = acercar predicciones a verdad.
"""

print("\n--- Cross-entropy ---")

def cross_entropy(p, q, eps=1e-15):
    """Cross-entropy."""
    q = np.clip(q, eps, 1 - eps)
    return -np.sum(p * np.log(q))

def kl_divergence(p, q, eps=1e-15):
    """KL divergence."""
    p = np.array(p)
    q = np.clip(np.array(q), eps, 1 - eps)
    mask = p > 0
    return np.sum(p[mask] * np.log(p[mask] / q[mask]))

p_true = np.array([0.7, 0.2, 0.1])

predictions = {
    "Perfecta":    np.array([0.7, 0.2, 0.1]),
    "Buena":       np.array([0.6, 0.3, 0.1]),
    "Media":       np.array([0.4, 0.4, 0.2]),
    "Mala":        np.array([0.1, 0.2, 0.7]),
    "Uniforme":    np.array([1/3, 1/3, 1/3]),
}

print(f"  True: {p_true}")
print(f"\n  {'Prediccion':>15s}  {'CE':>8s}  {'KL':>8s}  {'H(p)':>8s}")
H_p = entropy(p_true) * np.log(2)  # convertir a nats
for name, q in predictions.items():
    ce = cross_entropy(p_true, q)
    kl = kl_divergence(p_true, q)
    print(f"  {name:>15s}  {ce:8.4f}  {kl:8.4f}  {H_p:8.4f}")


print("\n--- KL divergence es asimetrica ---")

p = np.array([0.9, 0.1])
q = np.array([0.1, 0.9])

print(f"  D_KL(p||q) = {kl_divergence(p, q):.4f}")
print(f"  D_KL(q||p) = {kl_divergence(q, p):.4f}")
print(f"  (NO son iguales! KL no es una distancia)")


# =====================================================================
#   PARTE 3: MAP vs MLE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: MAP vs MLE ===")
print("=" * 80)

"""
MLE: θ_MLE = argmax P(data|θ)
MAP: θ_MAP = argmax P(θ|data) = argmax P(data|θ) * P(θ)

MAP = MLE + prior. El prior REGULARIZA.

Ejemplo: si P(θ) = N(0, σ²), MAP = MLE + L2 regularization.
"""

print("\n--- MAP vs MLE para Normal ---")

# Prior: μ ~ N(0, τ²), Likelihood: data ~ N(μ, σ²)
# MAP: μ_MAP = (n * x̄ / σ² + 0 / τ²) / (n/σ² + 1/τ²)
#    = shrinkage towards prior mean

np.random.seed(42)
sigma = 2.0  # Likelihood std
tau = 1.0    # Prior std

for n in [1, 5, 10, 50, 100]:
    data = np.random.normal(3.0, sigma, n)
    x_bar = data.mean()
    
    mu_mle = x_bar
    mu_map = (n * x_bar / sigma**2) / (n / sigma**2 + 1 / tau**2)
    
    print(f"  n={n:3d}: MLE={mu_mle:7.4f}, MAP={mu_map:7.4f} (true=3.0)")

print(f"\n  Con mas datos, MAP -> MLE (prior importa menos)")


print("\n--- L2 regularization = Gaussian prior ---")

"""
MLE de regresion: argmin ||y - Xw||²
  = argmax P(y|X,w) con errores gaussianos

MAP con w ~ N(0, τ²I): argmin ||y - Xw||² + (σ²/τ²)||w||²
  = Ridge regression con λ = σ²/τ²

Conclusion: L2 reg equivale a un prior gaussiano sobre los pesos.
"""

np.random.seed(42)
n, d = 50, 10
X = np.random.randn(n, d)
w_true = np.array([1, -2, 0, 0, 0, 0, 0, 0, 0, 0.5])
y = X @ w_true + np.random.randn(n) * 0.5

# MLE (OLS)
w_mle = np.linalg.lstsq(X, y, rcond=None)[0]

# MAP (Ridge) para diferentes λ
print(f"\n  λ (=σ²/τ²)  ||w-w_true||  ||w||")
for lam in [0, 0.01, 0.1, 1.0, 10.0]:
    w_map = np.linalg.solve(X.T @ X + lam * np.eye(d), X.T @ y)
    err = np.linalg.norm(w_map - w_true)
    norm = np.linalg.norm(w_map)
    print(f"  {lam:8.2f}     {err:10.4f}     {norm:6.4f}")


# =====================================================================
#   PARTE 4: BIAS-VARIANCE TRADEOFF
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: BIAS-VARIANCE TRADEOFF ===")
print("=" * 80)

"""
Error total = Bias² + Varianza + Ruido irreducible

- Modelo simple (underfit): alto bias, baja varianza.
- Modelo complejo (overfit): bajo bias, alta varianza.

Regularizacion = aumentar bias un poco para reducir varianza mucho.
"""

print("\n--- Simulacion de bias-variance ---")

def bias_variance_decomposition(X_train_sets, y_train_sets, X_test, y_test, degree):
    """Calcular bias y varianza de regresion polinomial."""
    predictions = []
    
    for X_tr, y_tr in zip(X_train_sets, y_train_sets):
        # Features polinomiales
        X_poly = np.column_stack([X_tr**i for i in range(degree + 1)])
        X_test_poly = np.column_stack([X_test**i for i in range(degree + 1)])
        
        # Pseudoinversa para estabilidad
        try:
            w = np.linalg.lstsq(X_poly, y_tr, rcond=None)[0]
            y_pred = X_test_poly @ w
        except:
            y_pred = np.zeros_like(y_test)
        
        predictions.append(y_pred)
    
    predictions = np.array(predictions)
    mean_pred = predictions.mean(axis=0)
    
    bias_sq = np.mean((mean_pred - y_test)**2)
    variance = np.mean(predictions.var(axis=0))
    mse = np.mean((predictions - y_test)**2)
    
    return bias_sq, variance, mse

# Funcion real: sin(x)
np.random.seed(42)
f_true = lambda x: np.sin(x)

n_datasets = 200
n_train = 20
X_test = np.linspace(-3, 3, 50).reshape(-1, 1)
y_test = f_true(X_test.ravel())

X_trains = []
y_trains = []
for _ in range(n_datasets):
    X_tr = np.random.uniform(-3, 3, n_train).reshape(-1, 1)
    y_tr = f_true(X_tr.ravel()) + np.random.randn(n_train) * 0.3
    X_trains.append(X_tr)
    y_trains.append(y_tr)

print(f"  {'Degree':>8s}  {'Bias²':>8s}  {'Var':>8s}  {'MSE':>8s}")
for degree in [1, 3, 5, 7, 10, 15]:
    b, v, mse = bias_variance_decomposition(X_trains, y_trains, X_test, y_test, degree)
    print(f"  {degree:8d}  {b:8.4f}  {v:8.4f}  {mse:8.4f}")


# =====================================================================
#   PARTE 5: CROSS-VALIDATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: CROSS-VALIDATION ===")
print("=" * 80)

"""
CV: estimar rendimiento en datos no vistos.
1. K-Fold: dividir en K partes, entrenar en K-1.
2. Stratified K-Fold: mantener proporcion de clases.
3. Leave-One-Out: K = N (caro pero menos sesgo).
"""

print("\n--- K-Fold Cross Validation ---")

def k_fold_cv(X, y, k=5, degree=3, lam=0.0):
    """K-Fold CV para regresion polinomial."""
    n = len(X)
    indices = np.arange(n)
    np.random.shuffle(indices)
    fold_size = n // k
    
    scores = []
    for fold in range(k):
        val_idx = indices[fold * fold_size:(fold + 1) * fold_size]
        train_idx = np.concatenate([indices[:fold * fold_size],
                                     indices[(fold + 1) * fold_size:]])
        
        X_tr, X_val = X[train_idx], X[val_idx]
        y_tr, y_val = y[train_idx], y[val_idx]
        
        # Polinomial features
        X_tr_poly = np.column_stack([X_tr**i for i in range(degree + 1)])
        X_val_poly = np.column_stack([X_val**i for i in range(degree + 1)])
        
        # Ridge regression
        w = np.linalg.solve(
            X_tr_poly.T @ X_tr_poly + lam * np.eye(degree + 1),
            X_tr_poly.T @ y_tr
        )
        
        y_pred = X_val_poly @ w
        mse = np.mean((y_pred - y_val)**2)
        scores.append(mse)
    
    return np.mean(scores), np.std(scores)

# Datos
np.random.seed(42)
X_cv = np.random.uniform(-3, 3, 100).reshape(-1, 1)
y_cv = np.sin(X_cv.ravel()) + np.random.randn(100) * 0.3

print(f"  {'Degree':>8s}  {'λ':>8s}  {'CV MSE':>10s}  {'± std':>8s}")
for degree, lam in [(1, 0), (3, 0), (5, 0), (7, 0), (3, 0.1), (5, 0.1), (7, 1.0)]:
    mean_mse, std_mse = k_fold_cv(X_cv, y_cv, k=5, degree=degree, lam=lam)
    print(f"  {degree:8d}  {lam:8.2f}  {mean_mse:10.4f}  {std_mse:8.4f}")


# =====================================================================
#   PARTE 6: METRICAS DE CLASIFICACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: METRICAS DE CLASIFICACION ===")
print("=" * 80)

"""
Confusion matrix: TP, FP, TN, FN
Precision = TP / (TP + FP) — de los que dije SI, cuantos eran SI
Recall = TP / (TP + FN) — de los que eran SI, cuantos encontre
F1 = 2 * P * R / (P + R) — media armonica
"""

print("\n--- Metricas desde cero ---")

def confusion_matrix(y_true, y_pred):
    """Confusion matrix binaria."""
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return tp, fp, tn, fn

def classification_report(y_true, y_pred):
    """Reporte completo."""
    tp, fp, tn, fn = confusion_matrix(y_true, y_pred)
    
    accuracy = (tp + tn) / (tp + fp + tn + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn,
    }

# Datos desbalanceados (5% positivos)
np.random.seed(42)
n = 1000
y_true = (np.random.random(n) < 0.05).astype(int)
scores = np.random.normal(y_true * 2, 1, n)

# Diferentes thresholds
print(f"  Prevalencia: {y_true.mean():.2%}")
print(f"\n  {'Threshold':>10s}  {'Accuracy':>8s}  {'Precision':>9s}  {'Recall':>6s}  {'F1':>6s}")
for threshold in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]:
    y_pred = (scores > threshold).astype(int)
    r = classification_report(y_true, y_pred)
    print(f"  {threshold:10.1f}  {r['accuracy']:8.4f}  {r['precision']:9.4f}  "
          f"{r['recall']:6.4f}  {r['f1']:6.4f}")


print("\n--- ROC y AUC ---")

"""
ROC: Receiver Operating Characteristic.
Plot de True Positive Rate vs False Positive Rate para todos los thresholds.
AUC: area bajo la curva ROC. 1.0 = perfecto, 0.5 = random.
"""

def roc_auc(y_true, scores, n_thresholds=100):
    """Calcular ROC AUC."""
    thresholds = np.linspace(scores.max(), scores.min(), n_thresholds)
    tprs = []
    fprs = []
    
    for t in thresholds:
        y_pred = (scores >= t).astype(int)
        tp, fp, tn, fn = confusion_matrix(y_true, y_pred)
        
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        tprs.append(tpr)
        fprs.append(fpr)
    
    # AUC con trapezoidal rule
    auc = 0
    for i in range(1, len(fprs)):
        auc += (fprs[i] - fprs[i-1]) * (tprs[i] + tprs[i-1]) / 2
    
    return auc, fprs, tprs

auc_val, fprs, tprs = roc_auc(y_true, scores)
print(f"  AUC = {auc_val:.4f}")

# Modelo random
random_scores = np.random.random(n)
auc_random, _, _ = roc_auc(y_true, random_scores)
print(f"  AUC random = {auc_random:.4f} (esperado: ~0.5)")


# =====================================================================
#   PARTE 7: CALIBRACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: CALIBRACION DE PROBABILIDADES ===")
print("=" * 80)

"""
Un modelo esta CALIBRADO si P(y=1|modelo dice 0.8) ≈ 0.8.

Metodo Platt: logistic calibration sobre scores.
Metodo isotonic: regresion monotona.
"""

print("\n--- Verificar calibracion ---")

def calibration_curve(y_true, probs, n_bins=10):
    """Calcular curva de calibracion."""
    bin_edges = np.linspace(0, 1, n_bins + 1)
    mean_predicted = []
    fraction_positive = []
    
    for i in range(n_bins):
        mask = (probs >= bin_edges[i]) & (probs < bin_edges[i+1])
        if mask.sum() > 0:
            mean_predicted.append(probs[mask].mean())
            fraction_positive.append(y_true[mask].mean())
    
    return mean_predicted, fraction_positive

# Simular modelo calibrado vs no calibrado
np.random.seed(42)
n = 5000
y_true_cal = (np.random.random(n) < 0.3).astype(int)

# Modelo bien calibrado
probs_good = 0.3 * np.ones(n) + np.random.randn(n) * 0.1
probs_good = np.clip(probs_good + y_true_cal * 0.4, 0.01, 0.99)

# Modelo mal calibrado (sobre-confiado)
probs_bad = probs_good ** 0.3

pred_good, frac_good = calibration_curve(y_true_cal, probs_good)
pred_bad, frac_bad = calibration_curve(y_true_cal, probs_bad)

print(f"  {'Predicted':>10s}  {'Good':>8s}  {'Bad':>8s}  {'Perfect':>8s}")
for i in range(min(len(pred_good), len(pred_bad))):
    print(f"  {pred_good[i]:10.3f}  {frac_good[i]:8.3f}  {frac_bad[i]:8.3f}  "
          f"{pred_good[i]:8.3f}")


# =====================================================================
#   PARTE 8: BAYESIAN INFERENCE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: BAYESIAN INFERENCE ===")
print("=" * 80)

"""
Bayesian: actualizar creencias con datos.
P(θ|data) ∝ P(data|θ) * P(θ)
  posterior ∝ likelihood * prior

Con prior conjugado, el posterior tiene forma analitica.
Beta-Bernoulli: prior Beta, likelihood Bernoulli -> posterior Beta.
"""

print("\n--- Beta-Bernoulli conjugacy ---")

def bayesian_update(alpha_prior, beta_prior, successes, failures):
    """Actualizar Beta prior con datos Bernoulli."""
    alpha_post = alpha_prior + successes
    beta_post = beta_prior + failures
    
    mean_post = alpha_post / (alpha_post + beta_post)
    var_post = (alpha_post * beta_post) / (
        (alpha_post + beta_post)**2 * (alpha_post + beta_post + 1))
    
    return alpha_post, beta_post, mean_post, var_post

# Estimar tasa de clics
alpha, beta = 1, 1  # Prior uniforme
print(f"  Prior: Beta({alpha}, {beta}), mean = 0.5")

# Datos llegan secuencialmente
data_sequence = [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]

successes = 0
failures = 0
for i, obs in enumerate(data_sequence):
    if obs == 1:
        successes += 1
    else:
        failures += 1
    
    a_post, b_post, mean, var = bayesian_update(alpha, beta, successes, failures)
    
    if (i+1) % 5 == 0:
        print(f"  Despues de {i+1} obs: Beta({a_post}, {b_post}), "
              f"mean={mean:.4f}, 95% CI: [{mean - 1.96*np.sqrt(var):.4f}, "
              f"{mean + 1.96*np.sqrt(var):.4f}]")


print("\n--- Bayesian A/B testing ---")

"""
En vez de p-values, calcular P(p_B > p_A).
"""

def bayesian_ab_test(successes_a, total_a, successes_b, total_b, n_samples=100000):
    """Bayesian A/B test usando Monte Carlo."""
    failures_a = total_a - successes_a
    failures_b = total_b - successes_b
    
    # Posterior samples
    samples_a = np.random.beta(1 + successes_a, 1 + failures_a, n_samples)
    samples_b = np.random.beta(1 + successes_b, 1 + failures_b, n_samples)
    
    prob_b_better = (samples_b > samples_a).mean()
    expected_lift = ((samples_b - samples_a) / samples_a).mean()
    
    return prob_b_better, expected_lift

np.random.seed(42)
prob_b, lift = bayesian_ab_test(120, 1000, 150, 1000)
print(f"  A: 120/1000 = 12.0%")
print(f"  B: 150/1000 = 15.0%")
print(f"  P(B > A) = {prob_b:.4f}")
print(f"  Expected lift = {lift:.2%}")


# =====================================================================
#   PARTE 9: FEATURE SELECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: FEATURE SELECTION ESTADISTICA ===")
print("=" * 80)

"""
Seleccionar features relevantes usando tests estadisticos.
"""

print("\n--- Mutual Information ---")

def mutual_information(x, y, n_bins=10):
    """Mutual information discreta."""
    x_binned = np.digitize(x, np.linspace(x.min(), x.max(), n_bins))
    
    n = len(x)
    mi = 0.0
    
    for xi in np.unique(x_binned):
        for yi in np.unique(y):
            p_xy = np.sum((x_binned == xi) & (y == yi)) / n
            p_x = np.sum(x_binned == xi) / n
            p_y = np.sum(y == yi) / n
            
            if p_xy > 0 and p_x > 0 and p_y > 0:
                mi += p_xy * np.log2(p_xy / (p_x * p_y))
    
    return mi

# Features: algunas relevantes, algunas no
np.random.seed(42)
n = 500
X_feat = np.random.randn(n, 5)
y_feat = (X_feat[:, 0] + 2 * X_feat[:, 1] + np.random.randn(n) * 0.5 > 0).astype(int)

print(f"  Feature importance (MI):")
for i in range(5):
    mi = mutual_information(X_feat[:, i], y_feat)
    relevant = "RELEVANTE" if mi > 0.1 else "ruido"
    print(f"    Feature {i}: MI = {mi:.4f} ({relevant})")


print("\n--- Correlation-based selection ---")

correlations = [np.abs(np.corrcoef(X_feat[:, i], y_feat)[0, 1]) for i in range(5)]
print(f"\n  Correlacion con target:")
for i, corr in enumerate(correlations):
    print(f"    Feature {i}: |r| = {corr:.4f}")


# =====================================================================
#   PARTE 10: INFORMATION GAIN PARA ARBOLES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: INFORMATION GAIN ===")
print("=" * 80)

"""
Decision trees usan information gain para seleccionar splits.
IG(S, A) = H(S) - Σ (|S_v|/|S|) * H(S_v)
"""

print("\n--- Information Gain ---")

def information_gain(y, feature, threshold):
    """Calcular information gain para un split."""
    H_parent = entropy_binary(y)
    
    left = y[feature <= threshold]
    right = y[feature > threshold]
    
    if len(left) == 0 or len(right) == 0:
        return 0
    
    H_left = entropy_binary(left)
    H_right = entropy_binary(right)
    
    w_left = len(left) / len(y)
    w_right = len(right) / len(y)
    
    return H_parent - w_left * H_left - w_right * H_right

def entropy_binary(y):
    """Entropia binaria."""
    p = y.mean()
    if p == 0 or p == 1:
        return 0
    return -p * np.log2(p) - (1-p) * np.log2(1-p)

# Encontrar mejor split
best_ig = 0
best_feature = 0
best_threshold = 0

for feat_idx in range(X_feat.shape[1]):
    thresholds = np.percentile(X_feat[:, feat_idx], np.arange(10, 100, 10))
    for t in thresholds:
        ig = information_gain(y_feat, X_feat[:, feat_idx], t)
        if ig > best_ig:
            best_ig = ig
            best_feature = feat_idx
            best_threshold = t

print(f"  Mejor split:")
print(f"    Feature {best_feature}, threshold {best_threshold:.4f}")
print(f"    Information gain: {best_ig:.4f}")


# =====================================================================
#   PARTE 11: MCMC (METROPOLIS-HASTINGS)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: MCMC — METROPOLIS-HASTINGS ===")
print("=" * 80)

"""
MCMC: Markov Chain Monte Carlo.
Muestrear de distribuciones complejas sin conocer la constante de normalizacion.

Metropolis-Hastings:
1. Proponer nuevo estado x' desde q(x'|x).
2. Aceptar con probabilidad min(1, P(x')/P(x) * q(x|x')/q(x'|x)).
3. Si rechazo, quedarme en x.

EN ML: Bayesian inference, modelos generativos.
"""

print("\n--- Metropolis-Hastings ---")

def metropolis_hastings(target_log_prob, x0, proposal_std=1.0, n_samples=10000):
    """Metropolis-Hastings sampler."""
    samples = [x0]
    current = x0
    accepted = 0
    
    for _ in range(n_samples):
        # Proposal (symmetric: q(x'|x) = q(x|x'))
        proposal = current + np.random.normal(0, proposal_std)
        
        # Log acceptance ratio
        log_ratio = target_log_prob(proposal) - target_log_prob(current)
        
        if np.log(np.random.random()) < log_ratio:
            current = proposal
            accepted += 1
        
        samples.append(current)
    
    return np.array(samples), accepted / n_samples

# Target: mezcla de 2 normales
def target_log_prob(x):
    comp1 = np.exp(-0.5 * ((x - 2) / 0.5)**2)
    comp2 = np.exp(-0.5 * ((x + 2) / 1.0)**2)
    return np.log(0.3 * comp1 + 0.7 * comp2 + 1e-30)

np.random.seed(42)
samples_mh, accept_rate = metropolis_hastings(target_log_prob, 0.0, proposal_std=1.5)

# Burn-in
samples_mh = samples_mh[1000:]

print(f"  Target: 0.3*N(2, 0.5²) + 0.7*N(-2, 1²)")
print(f"  Acceptance rate: {accept_rate:.4f}")
print(f"  Sample mean: {samples_mh.mean():.4f}")
print(f"  Sample std: {samples_mh.std():.4f}")

# Verificar distribucion
bins = np.linspace(-5, 5, 20)
for i in range(len(bins)-1):
    count = np.sum((samples_mh >= bins[i]) & (samples_mh < bins[i+1]))
    bar = "█" * (count // 50)
    if bar:
        print(f"  [{bins[i]:+5.1f}, {bins[i+1]:+5.1f}): {bar}")


# =====================================================================
#   PARTE 12: DISTANCIAS ENTRE DISTRIBUCIONES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: DISTANCIAS ENTRE DISTRIBUCIONES ===")
print("=" * 80)

"""
Formas de medir distancia entre distribuciones:
1. KL divergence (no simetrica).
2. Jensen-Shannon (simetrica, bounded).
3. Wasserstein (Earth Mover's Distance).
4. Total Variation.

EN ML:
- GANs usan Wasserstein (WGAN).
- VAEs usan KL.
- Knowledge distillation usa KL.
"""

print("\n--- Jensen-Shannon divergence ---")

def js_divergence(p, q, eps=1e-15):
    """Jensen-Shannon divergence."""
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m, eps) + 0.5 * kl_divergence(q, m, eps)

p1 = np.array([0.9, 0.1])
p2 = np.array([0.1, 0.9])
p3 = np.array([0.5, 0.5])

print(f"  JS([0.9,0.1] || [0.1,0.9]) = {js_divergence(p1, p2):.4f}")
print(f"  JS([0.9,0.1] || [0.5,0.5]) = {js_divergence(p1, p3):.4f}")
print(f"  JS([0.5,0.5] || [0.5,0.5]) = {js_divergence(p3, p3):.4f}")
print(f"  (JS es simetrica y bounded)")


print("\n--- Wasserstein distance (1D) ---")

def wasserstein_1d(samples1, samples2):
    """Earth Mover's Distance para 1D."""
    s1 = np.sort(samples1)
    s2 = np.sort(samples2)
    # Si tamaños diferentes, interpolar
    n = max(len(s1), len(s2))
    s1_interp = np.interp(np.linspace(0, 1, n), 
                           np.linspace(0, 1, len(s1)), s1)
    s2_interp = np.interp(np.linspace(0, 1, n), 
                           np.linspace(0, 1, len(s2)), s2)
    return np.mean(np.abs(s1_interp - s2_interp))

np.random.seed(42)
dist_a = np.random.normal(0, 1, 1000)
dist_b = np.random.normal(0.5, 1, 1000)
dist_c = np.random.normal(3, 1, 1000)

print(f"  W(N(0,1), N(0.5,1)) = {wasserstein_1d(dist_a, dist_b):.4f}")
print(f"  W(N(0,1), N(3,1))   = {wasserstein_1d(dist_a, dist_c):.4f}")
print(f"  W(N(0,1), N(0,1))   = {wasserstein_1d(dist_a, dist_a):.4f}")


# =====================================================================
#   PARTE 13: LABEL SMOOTHING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: LABEL SMOOTHING ===")
print("=" * 80)

"""
Label smoothing: suavizar one-hot labels.
En vez de [1, 0, 0], usar [0.9, 0.05, 0.05].

y_smooth = (1 - ε) * y_onehot + ε / K

Beneficios: reduce overconfidence, mejora calibracion.
"""

print("\n--- Label smoothing ---")

def label_smooth(y_onehot, epsilon=0.1, n_classes=10):
    """Aplicar label smoothing."""
    return (1 - epsilon) * y_onehot + epsilon / n_classes

n_classes = 5
y_hard = np.array([1, 0, 0, 0, 0])

for eps in [0.0, 0.05, 0.1, 0.2]:
    y_smooth = label_smooth(y_hard.astype(float), eps, n_classes)
    ce = -np.sum(y_hard * np.log(np.clip(y_smooth, 1e-15, 1)))
    print(f"  ε={eps:.2f}: {y_smooth} (CE con perfecta pred: {ce:.4f})")


# =====================================================================
#   PARTE 14: KNOWLEDGE DISTILLATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: KNOWLEDGE DISTILLATION ===")
print("=" * 80)

"""
Knowledge Distillation: entrenar modelo pequeño (student) 
imitando modelo grande (teacher).

Loss = (1-α)*CE(student, hard_labels) + α*KL(teacher_soft || student_soft)

Softmax con temperatura T:
p_i = exp(z_i/T) / Σ exp(z_j/T)

T alto -> distribucion mas suave -> mas informacion.
"""

print("\n--- Temperature scaling ---")

def softmax_temperature(logits, T=1.0):
    """Softmax con temperatura."""
    scaled = logits / T
    exp_scaled = np.exp(scaled - np.max(scaled))
    return exp_scaled / exp_scaled.sum()

logits = np.array([5.0, 2.0, 0.5, -1.0])

print(f"  Logits: {logits}")
print(f"\n  {'T':>4s}  {'Prob 0':>8s}  {'Prob 1':>8s}  {'Prob 2':>8s}  {'Prob 3':>8s}  {'Entropy':>8s}")
for T in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    probs = softmax_temperature(logits, T)
    H = -np.sum(probs * np.log(probs + 1e-15))
    print(f"  {T:4.1f}  {probs[0]:8.4f}  {probs[1]:8.4f}  {probs[2]:8.4f}  {probs[3]:8.4f}  {H:8.4f}")


print("\n--- Distillation loss ---")

def distillation_loss(student_logits, teacher_logits, hard_labels, T=4.0, alpha=0.5):
    """Loss de knowledge distillation."""
    # Soft targets
    teacher_soft = softmax_temperature(teacher_logits, T)
    student_soft = softmax_temperature(student_logits, T)
    
    # KL divergence entre teacher y student
    kl = np.sum(teacher_soft * np.log((teacher_soft + 1e-15) / (student_soft + 1e-15)))
    
    # Hard loss (CE con one-hot)
    student_hard = softmax_temperature(student_logits, 1.0)
    ce = -np.log(student_hard[hard_labels] + 1e-15)
    
    return alpha * T**2 * kl + (1 - alpha) * ce

teacher = np.array([5.0, 2.0, 0.5, -1.0])
student = np.array([3.0, 1.0, 0.8, -0.5])
label = 0

for T in [1.0, 2.0, 4.0, 8.0]:
    loss = distillation_loss(student, teacher, label, T=T)
    print(f"  T={T:.0f}: distillation_loss = {loss:.4f}")


# =====================================================================
#   PARTE 15: DIAGNOSTICO DE DATOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: DIAGNOSTICO DE DATOS PARA ML ===")
print("=" * 80)

"""
Checklist estadistico antes de entrenar un modelo:
1. Distribucion de features (gaussiana? skewed?).
2. Missing values.
3. Outliers.
4. Correlaciones entre features.
5. Class balance.
6. Data leakage.
"""

print("\n--- Data audit automatico ---")

def data_audit(X, y, feature_names=None):
    """Audit estadistico completo de un dataset."""
    n, d = X.shape
    if feature_names is None:
        feature_names = [f"feat_{i}" for i in range(d)]
    
    print(f"\n  Dataset: {n} samples, {d} features")
    print(f"  Missing values: {np.isnan(X).sum()}")
    
    # Class balance
    classes, counts = np.unique(y, return_counts=True)
    print(f"  Classes: {dict(zip(classes.astype(int), counts))}")
    imbalance = max(counts) / min(counts)
    print(f"  Imbalance ratio: {imbalance:.1f}x")
    
    # Feature stats
    print(f"\n  {'Feature':>10s}  {'Mean':>8s}  {'Std':>8s}  {'Skew':>8s}  {'Outliers':>8s}")
    for i in range(min(d, 8)):
        col = X[:, i]
        mean = np.mean(col)
        std = np.std(col)
        skew = np.mean(((col - mean) / (std + 1e-15))**3)
        q1, q3 = np.percentile(col, [25, 75])
        iqr = q3 - q1
        outliers = np.sum((col < q1 - 1.5*iqr) | (col > q3 + 1.5*iqr))
        print(f"  {feature_names[i]:>10s}  {mean:8.4f}  {std:8.4f}  {skew:8.4f}  {outliers:8d}")

# Test con datos sinteticos
np.random.seed(42)
X_audit = np.column_stack([
    np.random.normal(0, 1, 500),
    np.random.exponential(2, 500),
    np.random.uniform(-3, 3, 500),
    np.random.normal(5, 0.1, 500),
])
y_audit = (X_audit[:, 0] + X_audit[:, 1] > 2).astype(int)

data_audit(X_audit, y_audit, ["normal", "exponential", "uniform", "constant-ish"])


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE ESTADISTICA PARA ML:

1. Entropia: mide incertidumbre. H alto = modelo inseguro.

2. Cross-entropy: loss function de clasificacion.

3. KL divergence: distancia entre distribuciones.

4. MAP vs MLE: MAP = MLE + regularizacion.

5. Bias-variance tradeoff: la tension fundamental en ML.

6. Cross-validation: estimar generalizacion.

7. Metricas: precision/recall/F1/AUC.

8. MCMC: sampling de distribuciones complejas.

9. Wasserstein/JS: distancias para GANs.

10. Label smoothing: regularizacion via targets suaves.

FIN DEL MODULO 09: PROBABILIDAD Y ESTADISTICA.
"""

print("\n FIN DE ARCHIVO 03_estadistica_para_ml.")
print(" Estadistica para ML ha sido dominada.")
print(" Siguiente modulo: NUMPY PROFUNDO.")
