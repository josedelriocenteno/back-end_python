# ===========================================================================
# 03_linalg_y_aplicaciones_ml.py
# ===========================================================================
# MODULO 10: NUMPY PROFUNDO
# ARCHIVO 03: Algebra Lineal con NumPy y Aplicaciones ML
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar np.linalg, random, FFT, y patrones NumPy para ML:
# batch matmul, convolucion, PCA, SVD, regresion.
#
# CONTENIDO:
#   1. np.linalg: solve, inv, det, eig, svd, norm.
#   2. Least squares y regresion.
#   3. PCA desde cero con NumPy.
#   4. Convolucion con NumPy.
#   5. np.random: generadores y reproducibilidad.
#   6. FFT y procesamiento de señales.
#   7. Sparse patterns con NumPy.
#   8. Batch operations para ML.
#   9. Numerical stability patterns.
#   10. NumPy best practices checklist.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: NP.LINALG
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: NP.LINALG ===")
print("=" * 80)

"""
np.linalg: interfaz a LAPACK/BLAS (Fortran optimizado).
Las operaciones de algebra lineal MAS rapidas posibles en CPU.
"""

print("\n--- Sistemas lineales ---")

# Ax = b -> x = A^{-1}b
A = np.array([[3, 1], [1, 2]], dtype=np.float64)
b = np.array([9, 8], dtype=np.float64)

x = np.linalg.solve(A, b)
print(f"  A = {A.tolist()}")
print(f"  b = {b}")
print(f"  x = {x}")
print(f"  Verify A@x = {A @ x}")

# NUNCA usar inv para resolver sistemas
x_inv = np.linalg.inv(A) @ b
print(f"  Via inv: {x_inv} (mas lento y menos estable)")


print("\n--- Determinante y rango ---")

matrices = {
    "Invertible": np.array([[1, 2], [3, 4]]),
    "Singular": np.array([[1, 2], [2, 4]]),
    "Orthogonal": np.array([[0, 1], [-1, 0]]),
}

for name, M in matrices.items():
    det = np.linalg.det(M)
    rank = np.linalg.matrix_rank(M)
    print(f"  {name:12s}: det={det:+.4f}, rank={rank}")


print("\n--- Eigenvalues ---")

# Symmetric matrix (real eigenvalues)
S = np.array([[4, 2], [2, 3]], dtype=np.float64)
eigenvalues, eigenvectors = np.linalg.eigh(S)  # eigh for symmetric

print(f"  S = {S.tolist()}")
print(f"  Eigenvalues: {eigenvalues}")
print(f"  Eigenvectors:\n{eigenvectors}")
print(f"  Verify S@v = λ*v: {np.allclose(S @ eigenvectors, eigenvalues * eigenvectors)}")


print("\n--- SVD ---")

A = np.random.randn(4, 3)
U, s, Vt = np.linalg.svd(A, full_matrices=False)
print(f"  A shape: {A.shape}")
print(f"  U shape: {U.shape}")
print(f"  s: {s.round(4)}")
print(f"  Vt shape: {Vt.shape}")
print(f"  Reconstruction: {np.allclose(A, U * s @ Vt)}")


print("\n--- Norms ---")

v = np.array([3.0, 4.0])
M = np.random.randn(3, 3)

print(f"  L1 norm: {np.linalg.norm(v, 1)}")
print(f"  L2 norm: {np.linalg.norm(v, 2)}")
print(f"  Linf norm: {np.linalg.norm(v, np.inf)}")
print(f"  Frobenius: {np.linalg.norm(M, 'fro'):.4f}")
print(f"  Condition number: {np.linalg.cond(M):.4f}")


# =====================================================================
#   PARTE 2: LEAST SQUARES Y REGRESION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: LEAST SQUARES Y REGRESION ===")
print("=" * 80)

"""
Regresion lineal con NumPy:
w = (X^T X)^{-1} X^T y  (Normal equation)
w = np.linalg.lstsq(X, y)  (via SVD, mas estable)
"""

print("\n--- Regresion lineal ---")

np.random.seed(42)
n, d = 200, 5
X = np.random.randn(n, d)
w_true = np.array([2.0, -1.0, 0.5, 0.0, 3.0])
noise = np.random.randn(n) * 0.5
y = X @ w_true + noise

# Agregar bias
X_bias = np.column_stack([np.ones(n), X])

# Normal equation
w_normal = np.linalg.solve(X_bias.T @ X_bias, X_bias.T @ y)

# lstsq (preferred)
w_lstsq, residuals, rank, sv = np.linalg.lstsq(X_bias, y, rcond=None)

print(f"  True w:   {w_true}")
print(f"  Normal:   {w_normal[1:].round(4)}")
print(f"  lstsq:    {w_lstsq[1:].round(4)}")
print(f"  Bias:     {w_lstsq[0]:.4f}")

# R² score
y_pred = X_bias @ w_lstsq
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res / ss_tot
print(f"  R² = {r2:.6f}")


print("\n--- Ridge regression ---")

def ridge_regression(X, y, lam=1.0):
    """Ridge: (X^T X + λI)^{-1} X^T y"""
    d = X.shape[1]
    return np.linalg.solve(X.T @ X + lam * np.eye(d), X.T @ y)

print(f"  {'Lambda':>8s}  {'||w||':>8s}  {'MSE':>8s}")
for lam in [0, 0.01, 0.1, 1.0, 10.0, 100.0]:
    w = ridge_regression(X_bias, y, lam)
    mse = np.mean((y - X_bias @ w)**2)
    print(f"  {lam:8.2f}  {np.linalg.norm(w):8.4f}  {mse:8.4f}")


# =====================================================================
#   PARTE 3: PCA DESDE CERO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: PCA DESDE CERO ===")
print("=" * 80)

"""
PCA: proyectar datos en direcciones de maxima varianza.
1. Centrar datos.
2. Calcular matriz de covarianza.
3. Eigendecomposition.
4. Proyectar en top-k eigenvectors.
"""

print("\n--- PCA implementacion ---")

def pca(X, n_components):
    """PCA desde cero."""
    # 1. Centrar
    mean = X.mean(axis=0)
    X_centered = X - mean
    
    # 2. Covarianza
    cov = (X_centered.T @ X_centered) / (X.shape[0] - 1)
    
    # 3. Eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    
    # Ordenar de mayor a menor
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # 4. Top-k
    components = eigenvectors[:, :n_components]
    
    # Proyectar
    X_projected = X_centered @ components
    
    explained_variance = eigenvalues[:n_components] / eigenvalues.sum()
    
    return X_projected, components, explained_variance, mean

# Test con datos de alta dimension
np.random.seed(42)
n, d = 500, 20
# Datos con estructura: 3 componentes principales
latent = np.random.randn(n, 3)
W = np.random.randn(3, d)
X_pca = latent @ W + np.random.randn(n, d) * 0.5

X_reduced, components, explained_var, _ = pca(X_pca, 5)

print(f"  Original: {X_pca.shape}")
print(f"  Reduced: {X_reduced.shape}")
print(f"  Explained variance (top 5):")
for i, ev in enumerate(explained_var):
    bar = "█" * int(ev * 50)
    print(f"    PC{i+1}: {ev:.4f} {bar}")
print(f"  Total: {explained_var.sum():.4f}")


# =====================================================================
#   PARTE 4: CONVOLUCION CON NUMPY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: CONVOLUCION ===")
print("=" * 80)

"""
Convolucion 1D: y[n] = Σ x[n-k] * h[k]
Convolucion 2D: para imagenes (CNN).
"""

print("\n--- Convolucion 1D ---")

signal = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1], dtype=np.float64)
kernel = np.array([1, 0, -1], dtype=np.float64)

conv = np.convolve(signal, kernel, mode='valid')
print(f"  Signal: {signal}")
print(f"  Kernel: {kernel}")
print(f"  Conv (valid): {conv}")

# Modes
for mode in ['full', 'same', 'valid']:
    result = np.convolve(signal, kernel, mode=mode)
    print(f"  Conv ({mode:5s}): len={len(result)}, {result}")


print("\n--- Convolucion 2D manual ---")

def conv2d(image, kernel, padding=0, stride=1):
    """Convolucion 2D desde cero."""
    if padding > 0:
        image = np.pad(image, padding, mode='constant')
    
    h, w = image.shape
    kh, kw = kernel.shape
    out_h = (h - kh) // stride + 1
    out_w = (w - kw) // stride + 1
    
    output = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            patch = image[i*stride:i*stride+kh, j*stride:j*stride+kw]
            output[i, j] = np.sum(patch * kernel)
    
    return output

image = np.arange(25, dtype=np.float64).reshape(5, 5)
edge_kernel = np.array([[-1, -1, -1],
                         [0,  0,  0],
                         [1,  1,  1]], dtype=np.float64)

result = conv2d(image, edge_kernel, padding=0)
print(f"  Image (5x5) conv edge_detect (3x3):")
print(f"  Output shape: {result.shape}")
print(f"  Output:\n{result}")


# =====================================================================
#   PARTE 5: NP.RANDOM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: NP.RANDOM ===")
print("=" * 80)

"""
NumPy random: nuevo API con Generator (desde NumPy 1.17).
Usar np.random.default_rng() en vez de np.random.seed().
"""

print("\n--- New Generator API ---")

rng = np.random.default_rng(42)

print(f"  uniform:  {rng.uniform(0, 1, 5).round(4)}")
print(f"  normal:   {rng.standard_normal(5).round(4)}")
print(f"  integers: {rng.integers(0, 10, 5)}")
print(f"  choice:   {rng.choice(['a','b','c'], 5)}")

# Reproducible
rng1 = np.random.default_rng(42)
rng2 = np.random.default_rng(42)
print(f"\n  Reproducible: {np.array_equal(rng1.random(5), rng2.random(5))}")


print("\n--- Shuffling y permutaciones ---")

arr = np.arange(10)
rng = np.random.default_rng(42)

# shuffle modifica in-place
shuffled = arr.copy()
rng.shuffle(shuffled)
print(f"  Shuffled: {shuffled}")

# permutation retorna copia
perm = rng.permutation(10)
print(f"  Permutation: {perm}")


print("\n--- Sampling de distribuciones ML ---")

rng = np.random.default_rng(42)

# Xavier initialization
fan_in, fan_out = 512, 256
xavier = rng.normal(0, np.sqrt(2.0 / (fan_in + fan_out)), (fan_in, fan_out))
print(f"\n  Xavier init: mean={xavier.mean():.6f}, std={xavier.std():.6f}")
print(f"  Expected std: {np.sqrt(2.0 / (fan_in + fan_out)):.6f}")

# Kaiming initialization
kaiming = rng.normal(0, np.sqrt(2.0 / fan_in), (fan_in, fan_out))
print(f"  Kaiming init: mean={kaiming.mean():.6f}, std={kaiming.std():.6f}")


# =====================================================================
#   PARTE 6: FFT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: FFT ===")
print("=" * 80)

"""
FFT: transformada rapida de Fourier.
Descompone señal en frecuencias.
EN ML: data augmentation, feature extraction.
"""

print("\n--- FFT basico ---")

# Señal: suma de dos senos
t = np.linspace(0, 1, 1000)
freq1, freq2 = 5, 50
signal = np.sin(2 * np.pi * freq1 * t) + 0.5 * np.sin(2 * np.pi * freq2 * t)

fft_result = np.fft.fft(signal)
freqs = np.fft.fftfreq(len(t), t[1] - t[0])

# Top frequencies
magnitudes = np.abs(fft_result)[:len(t)//2]
top_freq_idx = np.argsort(magnitudes)[::-1][:5]
top_freqs = freqs[top_freq_idx]

print(f"  Signal: sin(2π*{freq1}t) + 0.5*sin(2π*{freq2}t)")
print(f"  Top frequencies: {np.abs(top_freqs[:3]).round(1)} Hz")


# =====================================================================
#   PARTE 7: NUMERICAL STABILITY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: NUMERICAL STABILITY ===")
print("=" * 80)

"""
Patrones para evitar errores numericos:
1. log-sum-exp para softmax.
2. Estabilidad en varianza.
3. Evitar division por cero.
"""

print("\n--- Welford's algorithm (varianza online) ---")

def welford_variance(data):
    """Varianza numericamente estable (online)."""
    n = 0
    mean = 0.0
    M2 = 0.0
    for x in data:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        M2 += delta * delta2
    return M2 / (n - 1) if n > 1 else 0.0

# Test con datos que causan problemas
data = np.array([1e8 + 1, 1e8 + 2, 1e8 + 3], dtype=np.float64)

var_naive = np.mean(data**2) - np.mean(data)**2  # Puede ser negativo!
var_welford = welford_variance(data)
var_numpy = np.var(data, ddof=1)

print(f"  Data: {data}")
print(f"  Naive variance: {var_naive:.6f} (puede ser negativo!)")
print(f"  Welford:        {var_welford:.6f}")
print(f"  NumPy (ddof=1): {var_numpy:.6f}")


print("\n--- Safe operations ---")

def safe_log(x, eps=1e-15):
    return np.log(np.maximum(x, eps))

def safe_divide(a, b, eps=1e-15):
    return a / np.maximum(np.abs(b), eps) * np.sign(b + eps)

def safe_sqrt(x):
    return np.sqrt(np.maximum(x, 0))

print(f"  safe_log(0) = {safe_log(0):.4f}")
print(f"  safe_divide(1, 0) = {safe_divide(1.0, 0.0):.4f}")
print(f"  safe_sqrt(-1e-10) = {safe_sqrt(-1e-10):.4f}")


# =====================================================================
#   PARTE 8: BATCH OPERATIONS PARA ML
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: BATCH OPERATIONS ===")
print("=" * 80)

"""
En ML todo es en batches. NumPy debe operar eficientemente.
"""

print("\n--- Batch matrix multiply ---")

batch = 32
n, m, k = 10, 20, 15
A = np.random.randn(batch, n, m)
B = np.random.randn(batch, m, k)

# Loop
start = time.perf_counter()
C_loop = np.array([A[i] @ B[i] for i in range(batch)])
t_loop = time.perf_counter() - start

# Einsum
start = time.perf_counter()
C_einsum = np.einsum('bij,bjk->bik', A, B)
t_einsum = time.perf_counter() - start

# np.matmul (@ operator)
start = time.perf_counter()
C_matmul = A @ B
t_matmul = time.perf_counter() - start

print(f"  Loop:    {t_loop:.6f}s")
print(f"  Einsum:  {t_einsum:.6f}s")
print(f"  Matmul:  {t_matmul:.6f}s")
print(f"  All equal: {np.allclose(C_loop, C_einsum) and np.allclose(C_loop, C_matmul)}")


print("\n--- Batch normalization ---")

def batch_norm(X, gamma, beta, eps=1e-5):
    """Batch normalization vectorizada."""
    mean = X.mean(axis=0)
    var = X.var(axis=0)
    X_norm = (X - mean) / np.sqrt(var + eps)
    return gamma * X_norm + beta

np.random.seed(42)
X_bn = np.random.randn(64, 128)
gamma = np.ones(128)
beta = np.zeros(128)

result = batch_norm(X_bn, gamma, beta)
print(f"  Input mean: {X_bn.mean():.4f}")
print(f"  Output mean: {result.mean():.6f}")
print(f"  Output std per feature: {result.std(axis=0).mean():.4f}")


print("\n--- One-hot encoding ---")

def one_hot(labels, n_classes):
    """One-hot encoding vectorizado."""
    n = len(labels)
    result = np.zeros((n, n_classes))
    result[np.arange(n), labels] = 1.0
    return result

labels = np.array([0, 2, 1, 4, 3, 0, 2])
oh = one_hot(labels, 5)
print(f"  Labels: {labels}")
print(f"  One-hot:\n{oh}")


# =====================================================================
#   PARTE 9: CROSS-ENTROPY LOSS VECTORIZADO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: LOSSES VECTORIZADOS ===")
print("=" * 80)

print("\n--- Cross-entropy loss ---")

def cross_entropy_loss(logits, targets):
    """CE loss completo: logits -> softmax -> CE."""
    # Stable softmax
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp_shifted = np.exp(shifted)
    probs = exp_shifted / exp_shifted.sum(axis=1, keepdims=True)
    
    # Pick correct class prob
    n = logits.shape[0]
    correct_probs = probs[np.arange(n), targets]
    
    loss = -np.log(correct_probs + 1e-15).mean()
    return loss, probs

np.random.seed(42)
batch_size, n_classes = 32, 10
logits = np.random.randn(batch_size, n_classes)
targets = np.random.randint(0, n_classes, batch_size)

loss, probs = cross_entropy_loss(logits, targets)
print(f"  Logits shape: {logits.shape}")
print(f"  CE Loss: {loss:.4f}")
print(f"  Random baseline: {-np.log(1/n_classes):.4f}")


print("\n--- MSE loss ---")

def mse_loss(predictions, targets):
    return np.mean((predictions - targets)**2)

y_pred = np.random.randn(100)
y_true = y_pred + np.random.randn(100) * 0.5
print(f"  MSE: {mse_loss(y_pred, y_true):.4f}")


# =====================================================================
#   PARTE 10: NUMPY BEST PRACTICES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: BEST PRACTICES ===")
print("=" * 80)

"""
CHECKLIST NUMPY PARA ML:

1. NUNCA iterar con for sobre arrays.
2. Usar broadcasting en vez de tile/repeat.
3. Pre-allocar arrays si no puedes vectorizar.
4. Usar einsum para operaciones tensoriales complejas.
5. Cuidado con views: .copy() si necesitas independencia.
6. float32 para GPU, float64 para precision.
7. Usar np.random.default_rng() (no np.random.seed).
8. keepdims=True para broadcasting correcto.
9. np.clip, np.where en vez de loops condicionales.
10. Verificar contiguidad antes de pasar a C/Fortran.
"""

print("\n--- Anti-patron vs patron correcto ---")

X = np.random.randn(1000, 100)

# BAD: loop para normalizar
start = time.perf_counter()
X_bad = np.empty_like(X)
for i in range(X.shape[0]):
    X_bad[i] = (X[i] - X[i].mean()) / (X[i].std() + 1e-8)
t_bad = time.perf_counter() - start

# GOOD: vectorizado
start = time.perf_counter()
means = X.mean(axis=1, keepdims=True)
stds = X.std(axis=1, keepdims=True)
X_good = (X - means) / (stds + 1e-8)
t_good = time.perf_counter() - start

print(f"  Loop normalize:  {t_bad:.4f}s")
print(f"  Vector normalize: {t_good:.6f}s")
print(f"  Speedup: {t_bad/t_good:.0f}x")
print(f"  Match: {np.allclose(X_bad, X_good)}")


# =====================================================================
#   PARTE 11: LOW-RANK APPROXIMATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: LOW-RANK APPROXIMATION ===")
print("=" * 80)

"""
SVD truncado: aproximar A ≈ U_k S_k V_k^T con k << rank.
Usado en: compresion, denoising, embeddings, recommendation.
"""

print("\n--- Truncated SVD ---")

np.random.seed(42)
# Matriz de rango bajo + ruido
A_low = np.random.randn(100, 3) @ np.random.randn(3, 50) + np.random.randn(100, 50) * 0.1

U, s, Vt = np.linalg.svd(A_low, full_matrices=False)

print(f"  Original shape: {A_low.shape}")
print(f"  Singular values (top 10): {s[:10].round(3)}")

for k in [1, 2, 3, 5, 10, 50]:
    A_approx = (U[:, :k] * s[:k]) @ Vt[:k, :]
    error = np.linalg.norm(A_low - A_approx, 'fro') / np.linalg.norm(A_low, 'fro')
    compression = (100 * k + k + k * 50) / (100 * 50)
    print(f"  k={k:2d}: relative_error={error:.4f}, compression={compression:.2%}")


print("\n--- Pseudoinverse ---")

"""
Moore-Penrose pseudoinverse: A+ = V S+ U^T
np.linalg.pinv usa SVD internamente.
Resuelve sistemas sobredeterminados e indeterminados.
"""

A_tall = np.random.randn(10, 3)  # Sobredeterminado
b_tall = np.random.randn(10)

x_lstsq = np.linalg.lstsq(A_tall, b_tall, rcond=None)[0]
x_pinv = np.linalg.pinv(A_tall) @ b_tall
print(f"  lstsq vs pinv match: {np.allclose(x_lstsq, x_pinv)}")


# =====================================================================
#   PARTE 12: CHOLESKY DECOMPOSITION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: CHOLESKY ===")
print("=" * 80)

"""
Cholesky: A = L L^T (para matrices simetricas positivas definidas).
2x mas rapido que LU. Usado en Gaussian Processes, sampling.
"""

print("\n--- Cholesky decomposition ---")

# Crear PD matrix
A_pd = np.random.randn(5, 5)
A_pd = A_pd @ A_pd.T + 5 * np.eye(5)  # Garantizar PD

L = np.linalg.cholesky(A_pd)
print(f"  A is symmetric PD: {np.allclose(A_pd, A_pd.T)}")
print(f"  L @ L^T == A: {np.allclose(L @ L.T, A_pd)}")
print(f"  L is lower triangular: {np.allclose(L, np.tril(L))}")

# Resolver via Cholesky (mas rapido que solve)
b = np.random.randn(5)
# Ly = b -> y = L^{-1}b
y = np.linalg.solve(L, b)
# L^T x = y -> x = (L^T)^{-1}y
x_chol = np.linalg.solve(L.T, y)
x_direct = np.linalg.solve(A_pd, b)
print(f"  Cholesky solve == direct: {np.allclose(x_chol, x_direct)}")


print("\n--- Sampling multivariante ---")

"""
Muestrear x ~ N(μ, Σ):
1. Cholesky: Σ = L L^T
2. z ~ N(0, I)
3. x = μ + L @ z
"""

mu = np.array([1.0, 2.0, 3.0])
Sigma = np.array([[1.0, 0.5, 0.3],
                   [0.5, 2.0, 0.4],
                   [0.3, 0.4, 1.5]])

L = np.linalg.cholesky(Sigma)
rng = np.random.default_rng(42)
z = rng.standard_normal((1000, 3))
samples = mu + z @ L.T

print(f"  Target mean: {mu}")
print(f"  Sample mean: {samples.mean(axis=0).round(4)}")
print(f"  Target cov diagonal: {np.diag(Sigma)}")
print(f"  Sample cov diagonal: {np.diag(np.cov(samples.T)).round(4)}")


# =====================================================================
#   PARTE 13: POLYNOMIAL FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: POLYNOMIAL FEATURES ===")
print("=" * 80)

"""
Generar features polinomiales para regresion no lineal.
"""

print("\n--- Polynomial features ---")

def polynomial_features(X, degree):
    """Generar features polinomiales hasta grado degree."""
    n, d = X.shape
    features = [np.ones((n, 1))]  # Bias
    
    for deg in range(1, degree + 1):
        for col in range(d):
            features.append(X[:, col:col+1] ** deg)
    
    # Cross terms (degree 2)
    if degree >= 2:
        for i in range(d):
            for j in range(i+1, d):
                features.append((X[:, i:i+1] * X[:, j:j+1]))
    
    return np.hstack(features)

np.random.seed(42)
X_poly = np.random.randn(100, 3)
X_expanded = polynomial_features(X_poly, 2)

print(f"  Original: {X_poly.shape}")
print(f"  Expanded (degree 2): {X_expanded.shape}")
print(f"  Features: bias + 3*2_degrees + 3_cross = {X_expanded.shape[1]}")


# =====================================================================
#   PARTE 14: K-MEANS CON NUMPY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: K-MEANS CON NUMPY ===")
print("=" * 80)

"""
K-means completamente vectorizado con NumPy.
"""

def kmeans(X, k, max_iters=100, tol=1e-4):
    """K-means clustering."""
    n, d = X.shape
    rng = np.random.default_rng(42)
    
    # Inicializar centroides aleatoriamente
    idx = rng.choice(n, k, replace=False)
    centroids = X[idx].copy()
    
    for iteration in range(max_iters):
        # Asignar clusters (pairwise distances vectorizadas)
        # ||x - c||² = ||x||² + ||c||² - 2*x·c
        X_sq = np.sum(X**2, axis=1, keepdims=True)
        C_sq = np.sum(centroids**2, axis=1, keepdims=True)
        dists = X_sq + C_sq.T - 2 * X @ centroids.T
        labels = np.argmin(dists, axis=1)
        
        # Actualizar centroides
        new_centroids = np.empty_like(centroids)
        for j in range(k):
            mask = labels == j
            if mask.sum() > 0:
                new_centroids[j] = X[mask].mean(axis=0)
            else:
                new_centroids[j] = centroids[j]
        
        # Convergencia
        shift = np.linalg.norm(new_centroids - centroids)
        centroids = new_centroids
        
        if shift < tol:
            break
    
    inertia = sum(np.sum((X[labels == j] - centroids[j])**2) for j in range(k))
    return labels, centroids, inertia, iteration + 1

# Test
np.random.seed(42)
# 3 clusters
X_km = np.vstack([
    np.random.randn(100, 2) + [0, 0],
    np.random.randn(100, 2) + [5, 5],
    np.random.randn(100, 2) + [0, 5],
])

labels, centroids, inertia, iters = kmeans(X_km, 3)
print(f"  Data: {X_km.shape}")
print(f"  Clusters: {np.bincount(labels)}")
print(f"  Centroids:\n{centroids.round(2)}")
print(f"  Inertia: {inertia:.2f}")
print(f"  Converged in {iters} iterations")


# =====================================================================
#   PARTE 15: GRADIENT CLIPPING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: GRADIENT CLIPPING ===")
print("=" * 80)

"""
Gradient clipping: limitar magnitud de gradientes.
Previene exploding gradients en RNNs/Transformers.
"""

print("\n--- Gradient clipping by norm ---")

def clip_grad_norm(grads, max_norm):
    """Clip gradients by global norm."""
    total_norm = np.sqrt(sum(np.sum(g**2) for g in grads))
    clip_coef = max_norm / (total_norm + 1e-6)
    if clip_coef < 1:
        grads = [g * clip_coef for g in grads]
    return grads, total_norm

# Simular gradientes grandes
grads = [np.random.randn(100, 50) * 10, np.random.randn(50) * 10]
total_norm_before = np.sqrt(sum(np.sum(g**2) for g in grads))

clipped, norm = clip_grad_norm(grads, max_norm=1.0)
total_norm_after = np.sqrt(sum(np.sum(g**2) for g in clipped))

print(f"  Norm before: {total_norm_before:.2f}")
print(f"  Norm after:  {total_norm_after:.4f}")
print(f"  Max norm:    1.0")


print("\n--- Gradient clipping by value ---")

def clip_grad_value(grads, clip_value):
    """Clip gradients by value."""
    return [np.clip(g, -clip_value, clip_value) for g in grads]

grads = [np.array([-5, 0.1, 10, -0.5, 3])]
clipped = clip_grad_value(grads, clip_value=1.0)
print(f"  Before: {grads[0]}")
print(f"  After:  {clipped[0]}")


# =====================================================================
#   PARTE 16: DATA MINI-BATCH ITERATOR
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: MINI-BATCH ITERATOR ===")
print("=" * 80)

def data_iterator(X, y, batch_size, shuffle=True):
    """Generador de mini-batches."""
    n = len(X)
    indices = np.arange(n)
    if shuffle:
        np.random.shuffle(indices)
    
    for start in range(0, n, batch_size):
        end = min(start + batch_size, n)
        batch_idx = indices[start:end]
        yield X[batch_idx], y[batch_idx]

# Test
X_iter = np.random.randn(100, 10)
y_iter = np.random.randint(0, 3, 100)

batch_sizes = []
for X_batch, y_batch in data_iterator(X_iter, y_iter, batch_size=32):
    batch_sizes.append(len(X_batch))

print(f"  Total samples: {len(X_iter)}")
print(f"  Batch size: 32")
print(f"  Num batches: {len(batch_sizes)}")
print(f"  Batch sizes: {batch_sizes}")
print(f"  Total processed: {sum(batch_sizes)}")


# =====================================================================
#   PARTE 17: LEARNING RATE SCHEDULES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: LEARNING RATE SCHEDULES ===")
print("=" * 80)

"""
Schedules de learning rate implementados con NumPy.
"""

print("\n--- LR Schedules ---")

def lr_step(base_lr, epoch, step_size=10, gamma=0.1):
    return base_lr * gamma ** (epoch // step_size)

def lr_cosine(base_lr, epoch, total_epochs):
    return base_lr * 0.5 * (1 + np.cos(np.pi * epoch / total_epochs))

def lr_warmup_cosine(base_lr, epoch, warmup_epochs, total_epochs):
    if epoch < warmup_epochs:
        return base_lr * epoch / warmup_epochs
    return lr_cosine(base_lr, epoch - warmup_epochs, total_epochs - warmup_epochs)

epochs = np.arange(100)
print(f"  {'Epoch':>5s}  {'Step':>8s}  {'Cosine':>8s}  {'Warmup+Cos':>10s}")
for e in [0, 5, 10, 20, 30, 50, 75, 99]:
    step = lr_step(0.01, e)
    cos = lr_cosine(0.01, e, 100)
    warm = lr_warmup_cosine(0.01, e, 10, 100)
    print(f"  {e:5d}  {step:8.6f}  {cos:8.6f}  {warm:10.6f}")


# =====================================================================
#   PARTE 18: STANDARD SCALER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: STANDARD SCALER ===")
print("=" * 80)

class StandardScaler:
    """Estandarizacion de features (mean=0, std=1)."""
    
    def __init__(self):
        self.mean_ = None
        self.std_ = None
    
    def fit(self, X):
        self.mean_ = X.mean(axis=0)
        self.std_ = X.std(axis=0)
        self.std_[self.std_ == 0] = 1.0  # Evitar division por 0
        return self
    
    def transform(self, X):
        return (X - self.mean_) / self.std_
    
    def fit_transform(self, X):
        return self.fit(X).transform(X)
    
    def inverse_transform(self, X_scaled):
        return X_scaled * self.std_ + self.mean_

np.random.seed(42)
X_raw = np.random.randn(200, 4) * [10, 0.01, 100, 1] + [5, -3, 50, 0]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)
X_recovered = scaler.inverse_transform(X_scaled)

print(f"  Original mean:  {X_raw.mean(axis=0).round(3)}")
print(f"  Original std:   {X_raw.std(axis=0).round(3)}")
print(f"  Scaled mean:    {X_scaled.mean(axis=0).round(6)}")
print(f"  Scaled std:     {X_scaled.std(axis=0).round(6)}")
print(f"  Recovery match: {np.allclose(X_raw, X_recovered)}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE LINALG Y APLICACIONES ML:

1. np.linalg: solve > inv, lstsq > normal equation.

2. Ridge regression: regularizacion con λI.

3. PCA: centrar + covarianza + eigendecomposition.

4. Convolucion: base de CNNs.

5. np.random: default_rng para reproducibilidad.

6. FFT: analisis frecuencial de señales.

7. Numerical stability: Welford, log-sum-exp, safe ops.

8. Batch ops: einsum, matmul para ML eficiente.

9. Losses vectorizados: CE, MSE sin loops.

10. Best practices: vectorizar siempre.

FIN DEL MODULO 10: NUMPY PROFUNDO.
"""

print("\n FIN DE ARCHIVO 03_linalg_y_aplicaciones_ml.")
print(" NumPy profundo ha sido dominado.")
print(" Siguiente modulo: PANDAS INGENIERIA.")
