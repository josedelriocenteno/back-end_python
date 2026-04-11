# ===========================================================================
# 03_eigenvalues_svd_y_aplicaciones.py
# ===========================================================================
# MODULO 07: ALGEBRA LINEAL CON PYTHON
# ARCHIVO 03: Eigenvalues, SVD, PCA y Aplicaciones en ML
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar eigenvalues/eigenvectors, SVD, PCA, y aplicaciones
# directas en ML: reduccion de dimension, compresion, analisis.
#
# CONTENIDO:
#   1. Eigenvalues y eigenvectors: concepto e intuicion.
#   2. Diagonalizacion.
#   3. SVD (Singular Value Decomposition).
#   4. PCA (Principal Component Analysis) desde cero.
#   5. Compresion con SVD trucado.
#   6. Matrices especiales: simetrica, positiva definida.
#   7. Aplicaciones: regularizacion, whitening, analisis.
#   8. Ejercicio: PCA completo sobre dataset.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: EIGENVALUES Y EIGENVECTORS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: EIGENVALUES Y EIGENVECTORS ===")
print("=" * 80)

"""
Dado A (n x n), un eigenvector v y eigenvalue lambda cumplen:
  A @ v = lambda * v

El eigenvector NO CAMBIA DE DIRECCION al transformar con A.
Solo se escala por lambda.

EN ML:
- PCA: eigenvectors de la matriz de covarianza = componentes principales.
- PageRank: eigenvector dominante de la matriz de transicion.
- Estabilidad: eigenvalues de la Hessiana indican curvatura del loss.
"""

print("\n--- Calcular eigenvalues/eigenvectors ---")

A = np.array([[4, 2],
               [1, 3]], dtype=float)

eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"  A:\n{A}")
print(f"  Eigenvalues: {eigenvalues}")
print(f"  Eigenvectors (columnas):\n{eigenvectors}")

# Verificar: A @ v = lambda * v
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    Av = A @ v
    lam_v = lam * v
    print(f"\n  Verificar eigenvector {i}:")
    print(f"    A @ v = {Av}")
    print(f"    λ * v = {lam_v}")
    print(f"    Iguales: {np.allclose(Av, lam_v)}")


print("\n--- Interpretacion geometrica ---")

"""
Eigenvalues dicen CUANTO estira/comprime A en cada direccion.
- lambda > 1: estira
- 0 < lambda < 1: comprime
- lambda < 0: invierte
- lambda = 0: colapsa esa dimension
"""

for lam in eigenvalues:
    if lam > 1:
        efecto = "estira"
    elif lam > 0:
        efecto = "comprime"
    elif lam < 0:
        efecto = "invierte"
    else:
        efecto = "colapsa"
    print(f"  λ = {lam:.2f}: {efecto}")


print("\n--- Propiedades ---")

print(f"  sum(eigenvalues) = {sum(eigenvalues):.2f}")
print(f"  trace(A) = {np.trace(A):.2f}")
print(f"  Son iguales: {np.isclose(sum(eigenvalues), np.trace(A))}")

print(f"\n  prod(eigenvalues) = {np.prod(eigenvalues):.2f}")
print(f"  det(A) = {np.linalg.det(A):.2f}")
print(f"  Son iguales: {np.isclose(np.prod(eigenvalues), np.linalg.det(A))}")


# =====================================================================
#   PARTE 2: DIAGONALIZACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: DIAGONALIZACION ===")
print("=" * 80)

"""
Si A tiene n eigenvectors independientes:
  A = V @ D @ V^-1

Donde:
  V: matriz de eigenvectors (en columnas)
  D: matriz diagonal de eigenvalues

Usar: A^k = V @ D^k @ V^-1 (potencias eficientes)
"""

print("\n--- Diagonalizacion ---")

V = eigenvectors
D = np.diag(eigenvalues)
V_inv = np.linalg.inv(V)

# Reconstruir A
A_recons = V @ D @ V_inv
print(f"  A original:\n{A}")
print(f"  V @ D @ V^-1:\n{A_recons}")
print(f"  Son iguales: {np.allclose(A, A_recons)}")


print("\n--- Potencia de matrices ---")

# A^5 usando diagonalizacion
k = 5
D_k = np.diag(eigenvalues ** k)
A_k = V @ D_k @ V_inv

# Verificar con multiplicacion directa
A_k_direct = np.linalg.matrix_power(A, k)

print(f"\n  A^{k} (diagonalizacion):\n{A_k}")
print(f"  A^{k} (directo):\n{A_k_direct}")
print(f"  Son iguales: {np.allclose(A_k, A_k_direct)}")


# =====================================================================
#   PARTE 3: MATRICES SIMETRICAS Y POSITIVAS DEFINIDAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: MATRICES SIMETRICAS Y POSITIVAS DEFINIDAS ===")
print("=" * 80)

"""
Simetrica: A = A^T
- Eigenvalues SIEMPRE reales.
- Eigenvectors SIEMPRE ortogonales.
- EN ML: matrices de covarianza son simetricas.

Positiva definida: x^T A x > 0 para todo x != 0
- Eigenvalues TODOS positivos.
- EN ML: covarianza bien definida, Choleksy factorizacion.
"""

print("\n--- Matriz simetrica ---")

# Construir simetrica: A^T A es siempre simetrica
np.random.seed(42)
X = np.random.randn(50, 3)
Cov = (X.T @ X) / len(X)  # Matriz de covarianza

print(f"  Cov:\n{Cov}")
print(f"  Simetrica (A == A^T): {np.allclose(Cov, Cov.T)}")

# Eigendecomposition de simetrica (usar eigh, mas eficiente)
eigenvals_sym, eigenvecs_sym = np.linalg.eigh(Cov)

print(f"\n  Eigenvalues: {eigenvals_sym}")
print(f"  Todos positivos: {all(eigenvals_sym > 0)}")
print(f"  -> Positiva definida: {all(eigenvals_sym > 0)}")


print("\n--- Cholesky factorizacion ---")

"""
Si A es positiva definida: A = L @ L^T
Donde L es triangular inferior.
Mas rapido que LU. Util para sampling.
"""

L = np.linalg.cholesky(Cov)
print(f"\n  L (cholesky):\n{L}")
print(f"  L @ L^T == Cov: {np.allclose(L @ L.T, Cov)}")


# =====================================================================
#   PARTE 4: SVD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: SVD (SINGULAR VALUE DECOMPOSITION) ===")
print("=" * 80)

"""
CUALQUIER matriz A (m x n) se descompone como:
  A = U @ S @ V^T

Donde:
  U: (m x m) vectores singulares izquierdos (ortonormales)
  S: (m x n) diagonal de valores singulares (no negativos, decrecientes)
  V^T: (n x n) vectores singulares derechos (ortonormales)

EN ML:
- Compresion de matrices (SVD truncado)
- PCA (SVD de la matriz centrada)
- LSA (Latent Semantic Analysis en NLP)
- Pseudo-inversa
"""

print("\n--- SVD basico ---")

A = np.array([[1, 2],
               [3, 4],
               [5, 6]], dtype=float)  # 3x2

U, S, Vt = np.linalg.svd(A)

print(f"  A (3x2):\n{A}")
print(f"  U (3x3):\n{U}")
print(f"  S: {S}")
print(f"  Vt (2x2):\n{Vt}")

# Reconstruir
S_full = np.zeros((3, 2))
S_full[:2, :2] = np.diag(S)
A_recons = U @ S_full @ Vt

print(f"\n  Reconstruccion:\n{A_recons}")
print(f"  Original == Reconstruccion: {np.allclose(A, A_recons)}")


print("\n--- SVD truncado (low-rank approximation) ---")

"""
Mantener solo los k valores singulares mas grandes.
Mejor aproximacion de rango k (teorema de Eckart-Young).
"""

np.random.seed(42)
M = np.random.randn(10, 8)
U, S, Vt = np.linalg.svd(M, full_matrices=False)

print(f"  M shape: {M.shape}")
print(f"  Valores singulares: {S}")

# Aproximacion de rango k
for k in [1, 2, 4, 8]:
    M_k = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
    error = np.linalg.norm(M - M_k) / np.linalg.norm(M)
    compresion = (10 * k + k + k * 8) / (10 * 8)
    print(f"  Rango {k}: error={error:.4f}, "
          f"params={10*k + k + k*8}/{10*8} ({compresion:.0%})")


# =====================================================================
#   PARTE 5: PCA DESDE CERO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: PCA (Principal Component Analysis) ===")
print("=" * 80)

"""
PCA: encontrar las direcciones de maxima varianza.

Algoritmo:
1. Centrar los datos (restar media).
2. Calcular matriz de covarianza.
3. Eigendecomposition.
4. Seleccionar top-k eigenvectors.
5. Proyectar datos.

Equivalente a SVD de la matriz centrada.
"""

print("\n--- PCA paso a paso ---")

np.random.seed(42)
n_samples = 200
n_features = 5

# Datos con estructura: 2 componentes principales + ruido
t = np.linspace(0, 4 * np.pi, n_samples)
X = np.column_stack([
    np.sin(t),
    np.cos(t),
    np.sin(t) * 0.5 + np.random.randn(n_samples) * 0.1,
    np.random.randn(n_samples) * 0.1,
    np.random.randn(n_samples) * 0.05,
])

print(f"  Datos: {X.shape}")

# Paso 1: Centrar
X_mean = X.mean(axis=0)
X_centered = X - X_mean
print(f"  Media (pre-centering): {X_mean}")
print(f"  Media (post-centering): {X_centered.mean(axis=0)}")

# Paso 2: Covarianza
Cov = (X_centered.T @ X_centered) / (n_samples - 1)
print(f"  Covarianza shape: {Cov.shape}")

# Paso 3: Eigendecomposition
eigenvalues, eigenvectors = np.linalg.eigh(Cov)

# Ordenar de mayor a menor
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

print(f"  Eigenvalues: {eigenvalues}")

# Varianza explicada
varianza_total = eigenvalues.sum()
varianza_explicada = eigenvalues / varianza_total
varianza_acumulada = np.cumsum(varianza_explicada)

print(f"\n  Varianza explicada:")
for i, (ve, va) in enumerate(zip(varianza_explicada, varianza_acumulada)):
    barra = "█" * int(ve * 50)
    print(f"    PC{i+1}: {ve:.4f} ({va:.4f} acum) {barra}")

# Paso 4: Seleccionar componentes
n_components = 2
V_k = eigenvectors[:, :n_components]

# Paso 5: Proyectar
X_pca = X_centered @ V_k
print(f"\n  Proyeccion: {X.shape} -> {X_pca.shape}")
print(f"  Varianza retenida: {varianza_acumulada[n_components-1]:.4f}")


print("\n--- PCA via SVD (mas eficiente) ---")

U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)

# Los componentes principales son las filas de Vt
X_pca_svd = X_centered @ Vt[:n_components].T
# Equivalente: X_pca_svd = U[:, :n_components] * S[:n_components]

print(f"  PCA via eigendecomposition y SVD son iguales:")
print(f"  {np.allclose(np.abs(X_pca), np.abs(X_pca_svd))}")
print(f"  (Pueden diferir en signo, pero la info es la misma)")


# =====================================================================
#   PARTE 6: PCA CLASE COMPLETA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: PCA — IMPLEMENTACION COMPLETA ===")
print("=" * 80)

class PCA:
    """PCA implementado desde cero con NumPy."""
    
    def __init__(self, n_components: int = None, variance_threshold: float = None):
        self.n_components = n_components
        self.variance_threshold = variance_threshold
        self.components_ = None
        self.mean_ = None
        self.eigenvalues_ = None
        self.explained_variance_ratio_ = None
    
    def fit(self, X):
        n, d = X.shape
        self.mean_ = X.mean(axis=0)
        X_c = X - self.mean_
        
        # SVD
        U, S, Vt = np.linalg.svd(X_c, full_matrices=False)
        
        # Eigenvalues de la covarianza
        self.eigenvalues_ = (S ** 2) / (n - 1)
        total_var = self.eigenvalues_.sum()
        self.explained_variance_ratio_ = self.eigenvalues_ / total_var
        
        # Determinar n_components
        if self.variance_threshold is not None:
            cumvar = np.cumsum(self.explained_variance_ratio_)
            self.n_components = np.searchsorted(cumvar, self.variance_threshold) + 1
        elif self.n_components is None:
            self.n_components = d
        
        self.components_ = Vt[:self.n_components]
        return self
    
    def transform(self, X):
        X_c = X - self.mean_
        return X_c @ self.components_.T
    
    def fit_transform(self, X):
        return self.fit(X).transform(X)
    
    def inverse_transform(self, X_pca):
        return X_pca @ self.components_ + self.mean_
    
    def reconstruction_error(self, X):
        X_pca = self.transform(X)
        X_recons = self.inverse_transform(X_pca)
        return np.mean(np.sum((X - X_recons) ** 2, axis=1))

# Usar
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

print(f"  PCA n_components=2:")
print(f"    Input: {X.shape}")
print(f"    Output: {X_pca.shape}")
print(f"    Varianza explicada: {pca.explained_variance_ratio_[:2]}")
print(f"    Varianza total: {sum(pca.explained_variance_ratio_[:2]):.4f}")

# Reconstruccion
X_recons = pca.inverse_transform(X_pca)
error = pca.reconstruction_error(X)
print(f"    Error de reconstruccion: {error:.6f}")


print("\n--- PCA con threshold de varianza ---")

pca_auto = PCA(variance_threshold=0.95)
X_auto = pca_auto.fit_transform(X)
print(f"  PCA con 95% varianza: {X_auto.shape[1]} componentes")

pca_auto99 = PCA(variance_threshold=0.99)
X_auto99 = pca_auto99.fit_transform(X)
print(f"  PCA con 99% varianza: {X_auto99.shape[1]} componentes")


# =====================================================================
#   PARTE 7: APLICACIONES AVANZADAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: APLICACIONES AVANZADAS ===")
print("=" * 80)

print("\n--- Pseudo-inversa (Moore-Penrose) ---")

"""
Para matrices no cuadradas o singulares:
A+ = V @ S+ @ U^T

Donde S+ invierte los valores singulares no nulos.
"""

A = np.array([[1, 2],
               [3, 4],
               [5, 6]], dtype=float)

A_pinv = np.linalg.pinv(A)
print(f"  A (3x2):\n{A}")
print(f"  A+ (2x3):\n{A_pinv}")
print(f"  A+ @ A:\n{A_pinv @ A}")
print(f"  Es ~identidad: {np.allclose(A_pinv @ A, np.eye(2))}")


print("\n--- Whitening ---")

"""
Whitening: transformar datos para que tengan covarianza = I.
X_white = X_pca / sqrt(eigenvalues)

EN ML: normalizar features para que gradientes sean uniformes.
"""

np.random.seed(42)
X_raw = np.random.randn(200, 3) @ np.array([[2, 1, 0], [1, 3, 0.5], [0, 0.5, 1]])

pca_w = PCA()
pca_w.fit(X_raw)
X_pca_w = pca_w.transform(X_raw)

# Whitening
X_white = X_pca_w / np.sqrt(pca_w.eigenvalues_)

cov_raw = np.cov(X_raw.T)
cov_white = np.cov(X_white.T)

print(f"  Covarianza original (diagonal): {np.diag(cov_raw)}")
print(f"  Covarianza whitened (diagonal): {np.diag(cov_white)}")
print(f"  Whitened es ~I: {np.allclose(cov_white, np.eye(3), atol=0.1)}")


print("\n--- Compresion con SVD ---")

"""
Simular compresion de una "imagen" (matriz grande).
"""

# Simular imagen como matriz
imagen = np.random.randn(100, 80)

U, S, Vt = np.linalg.svd(imagen, full_matrices=False)

print(f"\n  'Imagen' original: {imagen.shape}")
print(f"  Tamano original: {imagen.size} valores")

for k in [5, 10, 20, 40]:
    img_k = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
    error = np.linalg.norm(imagen - img_k) / np.linalg.norm(imagen)
    size_k = k * (100 + 80 + 1)
    ratio = size_k / imagen.size
    print(f"  k={k:2d}: error={error:.4f}, tamano={size_k:5d} ({ratio:.1%})")


# =====================================================================
#   PARTE 8: EJERCICIO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: EJERCICIO — ANALISIS COMPLETO DE DATASET ===")
print("=" * 80)

"""
Analisis completo de un dataset simulado usando toda
el algebra lineal vista.
"""

print("\n--- Dataset simulado ---")

np.random.seed(42)
n = 300

# 3 clusters con features correlacionadas
cluster_1 = np.random.randn(n // 3, 6) + np.array([2, 0, 1, 0, 0.5, -1])
cluster_2 = np.random.randn(n // 3, 6) + np.array([-1, 2, 0, 1, -0.5, 1])
cluster_3 = np.random.randn(n // 3, 6) + np.array([0, -2, -1, 2, 0, 0])

X_full = np.vstack([cluster_1, cluster_2, cluster_3])
labels = np.array([0] * 100 + [1] * 100 + [2] * 100)

print(f"  Dataset: {X_full.shape}")
print(f"  Clusters: 3 x {n // 3}")

# 1. Estadisticas basicas
print(f"\n  1. Estadisticas")
print(f"     Media por feature: {X_full.mean(axis=0)}")
print(f"     Std por feature:   {X_full.std(axis=0)}")

# 2. Correlaciones
corr = np.corrcoef(X_full.T)
print(f"\n  2. Correlaciones altas (>0.3):")
for i in range(6):
    for j in range(i + 1, 6):
        if abs(corr[i, j]) > 0.3:
            print(f"     Features {i}-{j}: {corr[i, j]:.3f}")

# 3. PCA
pca_full = PCA(n_components=6)
pca_full.fit(X_full)

print(f"\n  3. PCA — Varianza explicada:")
cum = 0
for i, ve in enumerate(pca_full.explained_variance_ratio_):
    cum += ve
    print(f"     PC{i+1}: {ve:.4f} (acum: {cum:.4f})")

# 4. Reducir a 2D
X_2d = PCA(n_components=2).fit_transform(X_full)

# 5. Distancias entre centroides
centroids = np.array([X_2d[labels == k].mean(axis=0) for k in range(3)])
print(f"\n  4. Centroides 2D:")
for k, c in enumerate(centroids):
    print(f"     Cluster {k}: [{c[0]:.2f}, {c[1]:.2f}]")

print(f"\n  5. Distancias entre centroides:")
for i in range(3):
    for j in range(i + 1, 3):
        dist = np.linalg.norm(centroids[i] - centroids[j])
        print(f"     Cluster {i}-{j}: {dist:.2f}")

# 6. Rango
rank = np.linalg.matrix_rank(X_full)
print(f"\n  6. Rango de la matriz: {rank} (de {X_full.shape[1]})")


# =====================================================================
#   PARTE 9: PAGERANK
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: PAGERANK ===")
print("=" * 80)

"""
PageRank: el eigenvector dominante de la matriz de transicion.
Google lo usa para rankear paginas web.

M @ v = v  (eigenvector con eigenvalue = 1)
"""

print("\n--- PageRank desde cero ---")

def pagerank(adj_matrix, damping=0.85, max_iter=100, tol=1e-8):
    """PageRank usando power iteration."""
    n = adj_matrix.shape[0]
    
    # Normalizar columnas (matriz de transicion)
    col_sums = adj_matrix.sum(axis=0)
    col_sums[col_sums == 0] = 1  # Evitar division por cero
    M = adj_matrix / col_sums
    
    # Power iteration con damping
    v = np.ones(n) / n
    
    for i in range(max_iter):
        v_new = damping * M @ v + (1 - damping) / n
        v_new = v_new / v_new.sum()
        
        if np.linalg.norm(v_new - v) < tol:
            print(f"  Convergido en iteracion {i}")
            break
        v = v_new
    
    return v

# Grafo de 5 paginas
adj = np.array([
    [0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [1, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
], dtype=float)

ranks = pagerank(adj)

page_names = ["A", "B", "C", "D", "E"]
sorted_idx = np.argsort(ranks)[::-1]

print(f"\n  Rankings:")
for idx in sorted_idx:
    barra = "█" * int(ranks[idx] * 100)
    print(f"    Pagina {page_names[idx]}: {ranks[idx]:.4f} {barra}")


# =====================================================================
#   PARTE 10: LATENT SEMANTIC ANALYSIS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: LSA (LATENT SEMANTIC ANALYSIS) ===")
print("=" * 80)

"""
LSA: aplicar SVD truncado a una matriz termino-documento.
Captura relaciones semanticas entre palabras.
"""

print("\n--- LSA desde cero ---")

# Simular matriz termino-documento
documentos = [
    "machine learning python",
    "deep learning neural network",
    "python programming data",
    "neural network training",
    "data science machine learning",
]

# Construir vocabulario
vocab = sorted(set(word for doc in documentos for word in doc.split()))
word_to_idx = {w: i for i, w in enumerate(vocab)}

# Matriz termino-documento (TF)
td_matrix = np.zeros((len(vocab), len(documentos)))
for j, doc in enumerate(documentos):
    for word in doc.split():
        td_matrix[word_to_idx[word], j] += 1

print(f"  Vocabulario: {len(vocab)} palabras")
print(f"  Documentos: {len(documentos)}")
print(f"  Matriz T-D: {td_matrix.shape}")

# SVD truncado
U, S, Vt = np.linalg.svd(td_matrix, full_matrices=False)

k = 2  # 2 conceptos latentes
U_k = U[:, :k]
S_k = np.diag(S[:k])
Vt_k = Vt[:k, :]

# Representacion de documentos en espacio latente
doc_vectors = (S_k @ Vt_k).T  # (n_docs, k)

print(f"\n  Espacio latente ({k} dims):")
for i, doc in enumerate(documentos):
    print(f"    Doc {i}: [{doc_vectors[i, 0]:.2f}, {doc_vectors[i, 1]:.2f}] - '{doc[:30]}'")

# Similaridad en espacio latente
from numpy.linalg import norm
for i in range(len(documentos)):
    for j in range(i + 1, len(documentos)):
        sim = np.dot(doc_vectors[i], doc_vectors[j]) / (
            norm(doc_vectors[i]) * norm(doc_vectors[j]))
        if abs(sim) > 0.5:
            print(f"    Docs {i}-{j}: sim={sim:.3f}")


# =====================================================================
#   PARTE 11: K-MEANS CLUSTERING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: K-MEANS CON ALGEBRA LINEAL ===")
print("=" * 80)

"""
K-Means: clustering iterativo usando distancias.
Todo es algebra lineal: distancias, medias, asignaciones.
"""

print("\n--- K-Means desde cero ---")

class KMeans:
    """K-Means implementado con NumPy vectorizado."""
    
    def __init__(self, k: int, max_iter: int = 100, seed: int = 42):
        self.k = k
        self.max_iter = max_iter
        self.seed = seed
        self.centroids = None
        self.labels_ = None
        self.inertia_ = None
    
    def fit(self, X):
        np.random.seed(self.seed)
        n, d = X.shape
        
        # Inicializacion: k puntos aleatorios
        idx = np.random.choice(n, self.k, replace=False)
        self.centroids = X[idx].copy()
        
        for iteration in range(self.max_iter):
            # Asignar: calcular distancias a centroides
            # (n, d) vs (k, d) -> (n, k)
            dists = np.sum(
                (X[:, None, :] - self.centroids[None, :, :]) ** 2,
                axis=2
            )
            self.labels_ = np.argmin(dists, axis=1)
            
            # Actualizar: media de puntos asignados
            new_centroids = np.array([
                X[self.labels_ == c].mean(axis=0) if np.sum(self.labels_ == c) > 0
                else self.centroids[c]
                for c in range(self.k)
            ])
            
            # Convergencia
            shift = np.linalg.norm(new_centroids - self.centroids)
            self.centroids = new_centroids
            
            if shift < 1e-6:
                print(f"  Convergido en iteracion {iteration}")
                break
        
        # Inertia
        self.inertia_ = sum(
            np.sum((X[self.labels_ == c] - self.centroids[c]) ** 2)
            for c in range(self.k)
        )
        
        return self
    
    def predict(self, X):
        dists = np.sum(
            (X[:, None, :] - self.centroids[None, :, :]) ** 2,
            axis=2
        )
        return np.argmin(dists, axis=1)

# Usar con dataset anterior
kmeans = KMeans(k=3)
kmeans.fit(X_full)

print(f"\n  K-Means resultados:")
print(f"    Inertia: {kmeans.inertia_:.2f}")

# Comparar con labels reales
for c in range(3):
    mask = kmeans.labels_ == c
    real_labels = labels[mask]
    values, counts = np.unique(real_labels, return_counts=True)
    majority = values[np.argmax(counts)]
    purity = np.max(counts) / np.sum(counts)
    print(f"    Cluster {c}: {np.sum(mask)} puntos, "
          f"mayoria=clase {majority}, pureza={purity:.2f}")


# =====================================================================
#   PARTE 12: POWER ITERATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: POWER ITERATION ===")
print("=" * 80)

"""
Power iteration: encontrar el eigenvector dominante
multiplicando repetidamente por A.

v_{n+1} = A @ v_n / ||A @ v_n||

Converge al eigenvector con mayor |eigenvalue|.
"""

print("\n--- Power iteration desde cero ---")

def power_iteration(A, n_iter=100, tol=1e-8):
    """Encontrar eigenvector dominante."""
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)
    
    for i in range(n_iter):
        Av = A @ v
        eigenvalue = np.dot(v, Av)
        v_new = Av / np.linalg.norm(Av)
        
        if np.linalg.norm(v_new - v) < tol:
            print(f"  Convergido en iteracion {i}")
            break
        v = v_new
    
    return eigenvalue, v

A_test = np.array([[4, 2],
                     [1, 3]], dtype=float)

eigenval_pi, eigenvec_pi = power_iteration(A_test)

# Comparar con numpy
eigenvals_np, eigenvecs_np = np.linalg.eig(A_test)
max_idx = np.argmax(np.abs(eigenvals_np))

print(f"\n  Power iteration: λ = {eigenval_pi:.6f}")
print(f"  numpy.linalg.eig: λ = {eigenvals_np[max_idx]:.6f}")
print(f"  Iguales: {np.isclose(eigenval_pi, eigenvals_np[max_idx])}")


print("\n--- Inverse power iteration (eigenvalue mas pequeño) ---")

def inverse_power_iteration(A, n_iter=100, tol=1e-8):
    """Encontrar eigenvalue mas pequeño."""
    n = A.shape[0]
    v = np.random.randn(n)
    v = v / np.linalg.norm(v)
    
    A_inv = np.linalg.inv(A)
    
    for i in range(n_iter):
        Av = A_inv @ v
        v_new = Av / np.linalg.norm(Av)
        
        if np.linalg.norm(v_new - v) < tol:
            break
        v = v_new
    
    eigenvalue = np.dot(v, A @ v) / np.dot(v, v)
    return eigenvalue, v

eigenval_inv, _ = inverse_power_iteration(A_test)
min_idx = np.argmin(np.abs(eigenvals_np))
print(f"  Inverse PI: λ_min = {eigenval_inv:.6f}")
print(f"  numpy:      λ_min = {eigenvals_np[min_idx]:.6f}")


# =====================================================================
#   PARTE 13: MATRIX EXPONENTIAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: EXPONENCIAL DE MATRICES ===")
print("=" * 80)

"""
exp(A) = I + A + A^2/2! + A^3/3! + ...

EN ML: flujos normalizadores, ecuaciones diferenciales neuronales.
"""

print("\n--- Matrix exponential ---")

from scipy.linalg import expm

A_exp = np.array([[0, 1],
                    [-1, 0]], dtype=float)  # Generador de rotaciones

print(f"  A:\n{A_exp}")
print(f"  exp(A):\n{expm(A_exp)}")
print(f"  Es rotacion (det=1): {np.isclose(np.linalg.det(expm(A_exp)), 1)}")

# exp(t*A) para diferentes t = rotaciones
for t in [0, np.pi/4, np.pi/2, np.pi]:
    R = expm(t * A_exp)
    angulo = np.degrees(np.arctan2(R[1, 0], R[0, 0]))
    print(f"  t={t:.2f}: rotacion de {angulo:.1f}°")


# =====================================================================
#   PARTE 14: SPECTRAL CLUSTERING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: SPECTRAL CLUSTERING ===")
print("=" * 80)

"""
Spectral clustering: usar eigenvectors del Laplaciano del grafo
para encontrar clusters.

1. Construir grafo de similaridad.
2. Calcular Laplaciano: L = D - W.
3. Eigenvectors del Laplaciano mas pequeños.
4. K-Means en el espacio de eigenvectors.
"""

print("\n--- Spectral Clustering simplificado ---")

def spectral_clustering(X, k=2, sigma=1.0):
    """Spectral clustering basico."""
    n = X.shape[0]
    
    # 1. Matriz de afinidad (RBF kernel)
    dists_sq = np.sum((X[:, None] - X[None, :]) ** 2, axis=2)
    W = np.exp(-dists_sq / (2 * sigma ** 2))
    np.fill_diagonal(W, 0)
    
    # 2. Laplaciano normalizado
    D = np.diag(W.sum(axis=1))
    D_inv_sqrt = np.diag(1.0 / np.sqrt(W.sum(axis=1) + 1e-10))
    L = np.eye(n) - D_inv_sqrt @ W @ D_inv_sqrt
    
    # 3. k eigenvectors mas pequeños
    eigenvals, eigenvecs = np.linalg.eigh(L)
    V = eigenvecs[:, :k]
    
    # Normalizar filas
    row_norms = np.linalg.norm(V, axis=1, keepdims=True)
    V_norm = V / (row_norms + 1e-10)
    
    # 4. K-Means en espacio espectral
    km = KMeans(k=k)
    km.fit(V_norm)
    
    return km.labels_, eigenvals[:k+2]

# Datos: dos circulos concentricos (KMeans falla, spectral no)
np.random.seed(42)
n_inner = 50
n_outer = 50

theta_inner = np.linspace(0, 2*np.pi, n_inner, endpoint=False)
theta_outer = np.linspace(0, 2*np.pi, n_outer, endpoint=False)

X_circles = np.vstack([
    np.column_stack([np.cos(theta_inner), np.sin(theta_inner)]) * 1 + np.random.randn(n_inner, 2) * 0.1,
    np.column_stack([np.cos(theta_outer), np.sin(theta_outer)]) * 3 + np.random.randn(n_outer, 2) * 0.2,
])
y_circles = np.array([0]*n_inner + [1]*n_outer)

labels_spec, eigenvals_spec = spectral_clustering(X_circles, k=2, sigma=0.5)

# Evaluar
acc_spec = max(
    np.mean(labels_spec == y_circles),
    np.mean(labels_spec != y_circles)  # Labels pueden estar invertidos
)

print(f"  Spectral clustering accuracy: {acc_spec:.4f}")
print(f"  Eigenvalues pequeños: {eigenvals_spec}")


print("\n" + "=" * 80)
print("=== CAPITULO 15: HESSIANA Y CURVATURA ===")
print("=" * 80)

"""
La Hessiana H (matriz de segundas derivadas) indica la curvatura
del loss landscape.

Eigenvalues de H:
- Todos positivos -> minimo local.
- Mixtos -> saddle point.
- Ratio max/min -> condicionamiento.

EN ML: explica por que Adam > SGD en muchos casos.
"""

print("\n--- Analisis de Hessiana ---")

def compute_hessian_2d(f, x, h=1e-5):
    """Calcular Hessiana numericamente para f: R^2 -> R."""
    n = len(x)
    H = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            x_pp = x.copy(); x_pp[i] += h; x_pp[j] += h
            x_pm = x.copy(); x_pm[i] += h; x_pm[j] -= h
            x_mp = x.copy(); x_mp[i] -= h; x_mp[j] += h
            x_mm = x.copy(); x_mm[i] -= h; x_mm[j] -= h
            
            H[i, j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4 * h * h)
    
    return H

# Loss function: f(x, y) = x^2 + 10*y^2 (elongada)
def loss_fn(x):
    return x[0]**2 + 10 * x[1]**2

punto = np.array([1.0, 1.0])
H = compute_hessian_2d(loss_fn, punto)

eigenvals_H = np.linalg.eigvalsh(H)
condition = max(eigenvals_H) / min(eigenvals_H)

print(f"  Loss: x^2 + 10*y^2")
print(f"  Hessiana en {punto}:\n{H}")
print(f"  Eigenvalues: {eigenvals_H}")
print(f"  Condicion: {condition:.1f}")
print(f"  {'Minimo' if all(eigenvals_H > 0) else 'Saddle point'}")

# Rosenbrock (mas dificil)
def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

H_rosen = compute_hessian_2d(rosenbrock, np.array([1.0, 1.0]))
eigenvals_rosen = np.linalg.eigvalsh(H_rosen)
cond_rosen = max(eigenvals_rosen) / min(eigenvals_rosen)

print(f"\n  Rosenbrock en (1,1):")
print(f"  Eigenvalues: {eigenvals_rosen}")
print(f"  Condicion: {cond_rosen:.1f}")
print(f"  (Alta condicion = dificil para SGD)")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE EIGENVALUES, SVD Y PCA:

1. Eigenvalues/eigenvectors: A @ v = λ * v. Base de PCA.

2. Propiedades: sum(λ) = trace, prod(λ) = det.

3. SVD: A = U @ S @ V^T. Funciona para CUALQUIER matriz.

4. PCA: eigenvectors de covarianza = componentes principales.

5. Whitening: normalizar covarianza a identidad.

6. PageRank: eigenvector dominante de la transicion.

7. LSA: SVD truncado sobre matrices termino-documento.

8. K-Means: clustering con distancias vectorizadas.

9. Spectral clustering: eigenvectors del Laplaciano.

10. Hessiana: eigenvalues = curvatura del loss landscape.

FIN DEL MODULO 07: ALGEBRA LINEAL CON PYTHON.
"""

print("\n FIN DE ARCHIVO 03_eigenvalues_svd_y_aplicaciones.")
print(" Eigenvalues, SVD y PCA han sido dominados.")
