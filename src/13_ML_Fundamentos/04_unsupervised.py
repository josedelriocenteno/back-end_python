# ===========================================================================
# 04_unsupervised.py
# ===========================================================================
# MODULO 13: ML FUNDAMENTOS
# ARCHIVO 04: Unsupervised Learning (Clustering, PCA, Anomaly)
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar clustering, reduccion de dimensionalidad, y anomaly detection.
#
# CONTENIDO:
#   1. K-Means.
#   2. DBSCAN conceptual.
#   3. Hierarchical clustering.
#   4. PCA.
#   5. t-SNE conceptual.
#   6. Anomaly detection.
#   7. Silhouette score.
#   8. Elbow method.
#   9. Gaussian Mixture Models.
#   10. Association rules conceptual.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time
from collections import Counter


# =====================================================================
#   PARTE 1: K-MEANS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: K-MEANS ===")
print("=" * 80)

"""
K-Means: particionar N puntos en K clusters.

Algoritmo:
1. Inicializar K centroids (random).
2. Assign: cada punto al centroid mas cercano.
3. Update: mover centroids al mean de su cluster.
4. Repetir 2-3 hasta convergencia.

Complejidad: O(n * k * d * iterations)
"""

class KMeans:
    """K-Means from scratch."""
    
    def __init__(self, k=3, max_iter=100, tol=1e-4, n_init=10):
        self.k = k
        self.max_iter = max_iter
        self.tol = tol
        self.n_init = n_init
        self.centroids = None
        self.labels = None
        self.inertia = None
    
    def _init_centroids(self, X):
        """K-Means++ initialization."""
        n = len(X)
        centroids = [X[np.random.randint(n)]]
        
        for _ in range(1, self.k):
            distances = np.min([np.sum((X - c)**2, axis=1) for c in centroids], axis=0)
            probs = distances / distances.sum()
            idx = np.random.choice(n, p=probs)
            centroids.append(X[idx])
        
        return np.array(centroids)
    
    def _assign(self, X, centroids):
        distances = np.array([np.sum((X - c)**2, axis=1) for c in centroids])
        return np.argmin(distances, axis=0)
    
    def _update(self, X, labels):
        centroids = np.array([X[labels == k].mean(axis=0) if np.sum(labels == k) > 0
                              else X[np.random.randint(len(X))]
                              for k in range(self.k)])
        return centroids
    
    def _fit_once(self, X):
        centroids = self._init_centroids(X)
        
        for _ in range(self.max_iter):
            labels = self._assign(X, centroids)
            new_centroids = self._update(X, labels)
            
            if np.max(np.abs(new_centroids - centroids)) < self.tol:
                break
            centroids = new_centroids
        
        inertia = sum(np.sum((X[labels == k] - centroids[k])**2)
                      for k in range(self.k))
        return centroids, labels, inertia
    
    def fit(self, X):
        best_inertia = float('inf')
        
        for _ in range(self.n_init):
            centroids, labels, inertia = self._fit_once(X)
            if inertia < best_inertia:
                best_inertia = inertia
                self.centroids = centroids
                self.labels = labels
                self.inertia = inertia
        
        return self
    
    def predict(self, X):
        return self._assign(X, self.centroids)


print("\n--- Datos sinteticos ---")

np.random.seed(42)
# 3 clusters
c1 = np.random.randn(100, 2) * 0.5 + np.array([0, 0])
c2 = np.random.randn(100, 2) * 0.5 + np.array([4, 4])
c3 = np.random.randn(100, 2) * 0.5 + np.array([0, 4])
X_cluster = np.vstack([c1, c2, c3])
y_true_cluster = np.array([0]*100 + [1]*100 + [2]*100)

print(f"  Data: {X_cluster.shape}, 3 true clusters")


print("\n--- K-Means fit ---")

km = KMeans(k=3, n_init=10)
start = time.perf_counter()
km.fit(X_cluster)
t_km = time.perf_counter() - start

print(f"  Inertia: {km.inertia:.2f}")
print(f"  Time: {t_km:.4f}s")
print(f"  Centroids:")
for i, c in enumerate(km.centroids):
    n_points = np.sum(km.labels == i)
    print(f"    Cluster {i}: center=({c[0]:.2f}, {c[1]:.2f}), n={n_points}")


# =====================================================================
#   PARTE 2: ELBOW METHOD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: ELBOW METHOD ===")
print("=" * 80)

"""
Elbow method: encontrar K optimo.
Plot inertia vs K. El "codo" indica el K optimo.
"""

print("\n--- Inertia vs K ---")

inertias = []
for k in range(1, 11):
    km_k = KMeans(k=k, n_init=5)
    km_k.fit(X_cluster)
    inertias.append(km_k.inertia)
    print(f"  K={k:2d}: inertia={km_k.inertia:10.2f}")

# Detect elbow (simple method)
diffs = np.diff(inertias)
diffs2 = np.diff(diffs)
elbow_k = np.argmax(diffs2) + 2
print(f"\n  Suggested K (elbow): {elbow_k}")


# =====================================================================
#   PARTE 3: SILHOUETTE SCORE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: SILHOUETTE ===")
print("=" * 80)

"""
Silhouette score: medir calidad del clustering.
  s(i) = (b(i) - a(i)) / max(a(i), b(i))
  
  a(i): distancia promedio intra-cluster.
  b(i): distancia promedio al cluster mas cercano.
  
  Rango: [-1, 1]. 1 = perfecto, 0 = overlap, -1 = misassigned.
"""

def silhouette_score(X, labels):
    """Silhouette score from scratch."""
    n = len(X)
    unique_labels = np.unique(labels)
    scores = np.zeros(n)
    
    for i in range(n):
        # a(i): mean intra-cluster distance
        same = labels == labels[i]
        same[i] = False
        if same.sum() > 0:
            a_i = np.mean(np.sqrt(np.sum((X[same] - X[i])**2, axis=1)))
        else:
            a_i = 0
        
        # b(i): min mean distance to other clusters
        b_i = float('inf')
        for label in unique_labels:
            if label == labels[i]:
                continue
            other = labels == label
            if other.sum() > 0:
                mean_dist = np.mean(np.sqrt(np.sum((X[other] - X[i])**2, axis=1)))
                b_i = min(b_i, mean_dist)
        
        scores[i] = (b_i - a_i) / max(a_i, b_i) if max(a_i, b_i) > 0 else 0
    
    return np.mean(scores)

print("\n--- Silhouette for different K ---")

for k in [2, 3, 4, 5]:
    km_s = KMeans(k=k, n_init=5).fit(X_cluster)
    # Use subset for speed
    sample_idx = np.random.choice(len(X_cluster), min(100, len(X_cluster)), replace=False)
    score = silhouette_score(X_cluster[sample_idx], km_s.labels[sample_idx])
    print(f"  K={k}: silhouette={score:.4f}")


# =====================================================================
#   PARTE 4: PCA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: PCA ===")
print("=" * 80)

"""
PCA (Principal Component Analysis):
  Reducir dimensionalidad preservando maxima varianza.

Algoritmo:
1. Centrar datos (restar media).
2. Calcular covariance matrix.
3. Eigendecomposition.
4. Seleccionar top-k eigenvectors.
5. Proyectar datos.
"""

class PCA:
    """PCA from scratch."""
    
    def __init__(self, n_components=2):
        self.n_components = n_components
        self.components = None
        self.mean = None
        self.explained_variance = None
        self.explained_variance_ratio = None
    
    def fit(self, X):
        self.mean = X.mean(axis=0)
        X_centered = X - self.mean
        
        # Covariance matrix
        cov = np.cov(X_centered, rowvar=False)
        
        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        
        # Sort by eigenvalue (descending)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        self.components = eigenvectors[:, :self.n_components]
        self.explained_variance = eigenvalues[:self.n_components]
        self.explained_variance_ratio = eigenvalues[:self.n_components] / eigenvalues.sum()
        
        return self
    
    def transform(self, X):
        X_centered = X - self.mean
        return X_centered @ self.components
    
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    
    def inverse_transform(self, X_reduced):
        return X_reduced @ self.components.T + self.mean


print("\n--- PCA en datos de alta dimension ---")

np.random.seed(42)
# 10D data con 3 componentes reales
n_pca = 200
real_data = np.random.randn(n_pca, 3)
mixing = np.random.randn(3, 10)
X_high = real_data @ mixing + np.random.randn(n_pca, 10) * 0.1

print(f"  Original: {X_high.shape}")

pca = PCA(n_components=10).fit(X_high)
print(f"\n  Explained variance ratio:")
cumulative = 0
for i, ratio in enumerate(pca.explained_variance_ratio):
    cumulative += ratio
    bar = "█" * int(ratio * 50)
    print(f"    PC{i+1:2d}: {ratio:.4f} (cum: {cumulative:.4f}) {bar}")

# Reduce to 3D
pca3 = PCA(n_components=3).fit_transform(X_high)
print(f"\n  Reduced: {pca3.shape}")
print(f"  Variance retained: {sum(PCA(3).fit(X_high).explained_variance_ratio):.4f}")


# =====================================================================
#   PARTE 5: ANOMALY DETECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: ANOMALY DETECTION ===")
print("=" * 80)

"""
Metodos:
1. Z-Score: |z| > 3 es anomalo.
2. IQR: < Q1-1.5*IQR o > Q3+1.5*IQR.
3. Isolation Forest (conceptual).
4. LOF (Local Outlier Factor) conceptual.
5. Mahalanobis distance.
"""

print("\n--- Z-Score ---")

np.random.seed(42)
normal_data = np.random.randn(1000, 2)
anomalies = np.random.uniform(-5, 5, (20, 2))
X_anom = np.vstack([normal_data, anomalies])

mean = X_anom.mean(axis=0)
std = X_anom.std(axis=0)
z_scores = np.abs((X_anom - mean) / std)
z_anomalies = np.any(z_scores > 3, axis=1)
print(f"  Z-Score anomalies: {z_anomalies.sum()}/{len(X_anom)}")


print("\n--- Mahalanobis distance ---")

def mahalanobis_distance(X, mean=None, cov_inv=None):
    if mean is None:
        mean = X.mean(axis=0)
    if cov_inv is None:
        cov = np.cov(X, rowvar=False)
        cov_inv = np.linalg.inv(cov)
    
    diff = X - mean
    distances = np.sqrt(np.sum(diff @ cov_inv * diff, axis=1))
    return distances

distances = mahalanobis_distance(X_anom)
threshold = np.percentile(distances, 97)
mah_anomalies = distances > threshold
print(f"  Mahalanobis anomalies: {mah_anomalies.sum()}/{len(X_anom)}")
print(f"  Threshold (97th pct): {threshold:.2f}")


# =====================================================================
#   PARTE 6: GAUSSIAN MIXTURE MODEL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: GMM ===")
print("=" * 80)

"""
GMM: soft clustering con distribucion gaussiana.
A diferencia de K-Means, asigna probabilidades.

EM Algorithm:
1. E-step: calcular responsibilidades (P(z|x)).
2. M-step: actualizar parametros (means, covariances, weights).
"""

class GaussianMixture:
    """Simple GMM with diagonal covariance."""
    
    def __init__(self, n_components=3, max_iter=100, tol=1e-4):
        self.n_components = n_components
        self.max_iter = max_iter
        self.tol = tol
    
    def fit(self, X):
        n, d = X.shape
        
        # Initialize
        idx = np.random.choice(n, self.n_components, replace=False)
        self.means = X[idx].copy()
        self.covs = np.array([np.eye(d)] * self.n_components)
        self.weights = np.ones(self.n_components) / self.n_components
        
        for iteration in range(self.max_iter):
            # E-step
            resp = self._e_step(X)
            
            # M-step
            old_means = self.means.copy()
            self._m_step(X, resp)
            
            if np.max(np.abs(self.means - old_means)) < self.tol:
                break
        
        self.labels = np.argmax(resp, axis=1)
        return self
    
    def _gaussian_pdf(self, X, mean, cov):
        d = len(mean)
        diff = X - mean
        det = np.linalg.det(cov)
        inv = np.linalg.inv(cov)
        norm = 1.0 / (np.sqrt((2*np.pi)**d * det) + 1e-300)
        exponent = -0.5 * np.sum(diff @ inv * diff, axis=1)
        return norm * np.exp(exponent)
    
    def _e_step(self, X):
        resp = np.zeros((len(X), self.n_components))
        for k in range(self.n_components):
            resp[:, k] = self.weights[k] * self._gaussian_pdf(X, self.means[k], self.covs[k])
        resp /= resp.sum(axis=1, keepdims=True) + 1e-300
        return resp
    
    def _m_step(self, X, resp):
        n = len(X)
        for k in range(self.n_components):
            Nk = resp[:, k].sum()
            self.weights[k] = Nk / n
            self.means[k] = (resp[:, k:k+1] * X).sum(axis=0) / (Nk + 1e-300)
            diff = X - self.means[k]
            self.covs[k] = (diff.T @ (diff * resp[:, k:k+1])) / (Nk + 1e-300)
            self.covs[k] += np.eye(X.shape[1]) * 1e-6

print("\n--- GMM fit ---")

gmm = GaussianMixture(n_components=3).fit(X_cluster)
print(f"  GMM clusters:")
for i in range(3):
    n_pts = np.sum(gmm.labels == i)
    print(f"    Cluster {i}: center=({gmm.means[i][0]:.2f}, {gmm.means[i][1]:.2f}), n={n_pts}, weight={gmm.weights[i]:.3f}")


# =====================================================================
#   PARTE 7: HIERARCHICAL CLUSTERING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: HIERARCHICAL ===")
print("=" * 80)

"""
Hierarchical Clustering:
  Agglomerative (bottom-up): merge clusters.
  Linkage:
  - Single: min distance between clusters.
  - Complete: max distance.
  - Average: mean distance.
  - Ward: minimize variance increase.
"""

def agglomerative(X, n_clusters=3, linkage='single'):
    """Simple agglomerative clustering."""
    n = len(X)
    labels = np.arange(n)
    
    # Distance matrix
    dist = np.full((n, n), np.inf)
    for i in range(n):
        for j in range(i+1, n):
            d = np.sqrt(np.sum((X[i] - X[j])**2))
            dist[i, j] = d
            dist[j, i] = d
    
    current_clusters = n
    
    while current_clusters > n_clusters:
        # Find closest pair
        i, j = np.unravel_index(np.argmin(dist), dist.shape)
        
        # Merge: relabel j -> i
        labels[labels == labels[j]] = labels[i]
        
        # Update distances
        for k in range(n):
            if labels[k] != labels[i]:
                if linkage == 'single':
                    dist[i, k] = dist[k, i] = min(dist[i, k], dist[j, k])
                elif linkage == 'complete':
                    dist[i, k] = dist[k, i] = max(dist[i, k], dist[j, k])
        
        dist[j, :] = np.inf
        dist[:, j] = np.inf
        dist[i, i] = np.inf
        
        current_clusters = len(np.unique(labels))
    
    # Renumber labels
    unique = np.unique(labels)
    label_map = {old: new for new, old in enumerate(unique)}
    return np.array([label_map[l] for l in labels])

print("\n--- Agglomerative (subset) ---")

sample = X_cluster[np.random.choice(len(X_cluster), 50, replace=False)]
labels_agg = agglomerative(sample, n_clusters=3)
print(f"  Clusters: {Counter(labels_agg)}")


# =====================================================================
#   PARTE 8: DBSCAN CONCEPTUAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: DBSCAN ===")
print("=" * 80)

"""
DBSCAN: Density-Based Spatial Clustering.
  - No necesita K (numero de clusters).
  - Detecta clusters de forma arbitraria.
  - Detecta outliers (noise points).

Parametros:
  - eps: radio de vecindad.
  - min_samples: minimo puntos para core point.

Tipos de puntos:
  - Core: >= min_samples en su eps-vecindad.
  - Border: en vecindad de un core pero no es core.
  - Noise: ni core ni border.
"""

class DBSCAN:
    """DBSCAN from scratch."""
    
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
    
    def fit(self, X):
        n = len(X)
        labels = np.full(n, -1)  # -1 = unvisited/noise
        cluster_id = 0
        
        for i in range(n):
            if labels[i] != -1:
                continue
            
            # Find neighbors
            neighbors = self._region_query(X, i)
            
            if len(neighbors) < self.min_samples:
                continue  # Noise
            
            # Expand cluster
            labels[i] = cluster_id
            seed_set = list(neighbors)
            
            j = 0
            while j < len(seed_set):
                q = seed_set[j]
                
                if labels[q] == -1:
                    labels[q] = cluster_id
                
                if labels[q] != -1 and labels[q] != cluster_id:
                    j += 1
                    continue
                
                labels[q] = cluster_id
                q_neighbors = self._region_query(X, q)
                
                if len(q_neighbors) >= self.min_samples:
                    seed_set.extend([n for n in q_neighbors if n not in seed_set])
                
                j += 1
            
            cluster_id += 1
        
        self.labels = labels
        self.n_clusters = cluster_id
        self.n_noise = np.sum(labels == -1)
        return self
    
    def _region_query(self, X, idx):
        distances = np.sqrt(np.sum((X - X[idx])**2, axis=1))
        return list(np.where(distances <= self.eps)[0])

print("\n--- DBSCAN fit ---")

db = DBSCAN(eps=1.0, min_samples=5).fit(X_cluster)
print(f"  Clusters found: {db.n_clusters}")
print(f"  Noise points: {db.n_noise}")
for c in range(db.n_clusters):
    print(f"    Cluster {c}: {np.sum(db.labels == c)} points")


# =====================================================================
#   PARTE 9: T-SNE CONCEPTUAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: t-SNE ===")
print("=" * 80)

"""
t-SNE (t-distributed Stochastic Neighbor Embedding):
  Reduccion de dimensionalidad NO-LINEAL para visualizacion.

1. Calcular probabilidades pairwise en alta dimension (Gaussian).
2. Calcular probabilidades pairwise en baja dimension (t-Student).
3. Minimizar KL divergence entre ambas distribuciones.

Parametros:
  - perplexity: ~5-50, controla el "vecindario" efectivo.
  - learning_rate: ~100-1000.
  - n_iter: ~1000.

REGLAS:
  - SOLO para visualizacion (2D/3D), NO para analisis.
  - Las distancias globales NO son significativas.
  - Solo distancias locales son confiables.
  - Perplexity afecta la forma de los clusters.
  - Correr varias veces con diferentes seeds.
"""

print("  t-SNE: non-linear dimensionality reduction")
print("  Key: perplexity controls neighborhood size")
print("  Warning: global distances are NOT meaningful")
print("  Use: UMAP as faster alternative")


# =====================================================================
#   PARTE 10: IQR ANOMALY DETECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: IQR ANOMALY ===")
print("=" * 80)

def iqr_anomalies(X, factor=1.5):
    """IQR-based anomaly detection per feature."""
    anomalies = np.zeros(len(X), dtype=bool)
    
    for j in range(X.shape[1]):
        q1 = np.percentile(X[:, j], 25)
        q3 = np.percentile(X[:, j], 75)
        iqr = q3 - q1
        lower = q1 - factor * iqr
        upper = q3 + factor * iqr
        anomalies |= (X[:, j] < lower) | (X[:, j] > upper)
    
    return anomalies

iqr_anom = iqr_anomalies(X_anom)
print(f"  IQR anomalies: {iqr_anom.sum()}/{len(X_anom)}")

# Compare methods
print(f"\n  Method comparison:")
print(f"    Z-Score:      {z_anomalies.sum()} anomalies")
print(f"    Mahalanobis:  {mah_anomalies.sum()} anomalies")
print(f"    IQR:          {iqr_anom.sum()} anomalies")


# =====================================================================
#   PARTE 11: ISOLATION FOREST CONCEPT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: ISOLATION FOREST ===")
print("=" * 80)

"""
Isolation Forest:
  Anomalias son mas faciles de "aislar" que datos normales.

Algoritmo:
1. Seleccionar feature random.
2. Seleccionar split random entre min y max.
3. Recursivamente particionar.
4. Anomalias: menos splits para aislar = path mas corto.

Score = 2^(-E(h(x)) / c(n))
  h(x): path length
  c(n): average path length in BST

Score ~1: anomalia
Score ~0.5: normal
Score ~0: definitivamente normal
"""

class SimpleIsolationTree:
    """Simplified Isolation Tree."""
    
    def __init__(self, max_depth=10):
        self.max_depth = max_depth
    
    def fit(self, X, depth=0):
        n, d = X.shape
        self.size = n
        
        if depth >= self.max_depth or n <= 1:
            return self
        
        # Random feature and split
        self.feature = np.random.randint(d)
        min_val = X[:, self.feature].min()
        max_val = X[:, self.feature].max()
        
        if min_val == max_val:
            return self
        
        self.threshold = np.random.uniform(min_val, max_val)
        
        left_mask = X[:, self.feature] < self.threshold
        self.left = SimpleIsolationTree(self.max_depth)
        self.left.fit(X[left_mask], depth + 1)
        self.right = SimpleIsolationTree(self.max_depth)
        self.right.fit(X[~left_mask], depth + 1)
        
        return self
    
    def path_length(self, x, depth=0):
        if depth >= self.max_depth or not hasattr(self, 'feature'):
            return depth
        
        if x[self.feature] < self.threshold:
            return self.left.path_length(x, depth + 1)
        return self.right.path_length(x, depth + 1)

# Build forest
n_trees = 20
trees = []
for _ in range(n_trees):
    sample_idx = np.random.choice(len(X_anom), 256, replace=False)
    tree = SimpleIsolationTree(max_depth=8).fit(X_anom[sample_idx])
    trees.append(tree)

# Score
avg_paths = np.array([np.mean([t.path_length(x) for t in trees]) for x in X_anom[:100]])
print(f"  Isolation Forest (100 samples):")
print(f"    Mean path (normal): {avg_paths[:50].mean():.2f}")
print(f"    Short paths likely anomalies")


# =====================================================================
#   PARTE 12: MINI-BATCH K-MEANS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: MINI-BATCH K-MEANS ===")
print("=" * 80)

"""
Mini-Batch K-Means: version escalable para datasets grandes.
En lugar de usar TODOS los datos cada iteracion,
usar un mini-batch random.
"""

class MiniBatchKMeans:
    def __init__(self, k=3, batch_size=100, max_iter=100):
        self.k = k
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.centroids = None
    
    def fit(self, X):
        n = len(X)
        # Init with K-Means++
        idx = np.random.choice(n, self.k, replace=False)
        self.centroids = X[idx].copy()
        counts = np.ones(self.k)
        
        for _ in range(self.max_iter):
            # Sample batch
            batch_idx = np.random.choice(n, min(self.batch_size, n), replace=False)
            batch = X[batch_idx]
            
            # Assign
            dists = np.array([np.sum((batch - c)**2, axis=1) for c in self.centroids])
            labels = np.argmin(dists, axis=0)
            
            # Update
            for k in range(self.k):
                mask = labels == k
                if mask.sum() > 0:
                    counts[k] += mask.sum()
                    lr = 1.0 / counts[k]
                    self.centroids[k] = (1 - lr) * self.centroids[k] + lr * batch[mask].mean(axis=0)
        
        # Final labels
        dists = np.array([np.sum((X - c)**2, axis=1) for c in self.centroids])
        self.labels = np.argmin(dists, axis=0)
        self.inertia = sum(np.sum((X[self.labels == k] - self.centroids[k])**2)
                          for k in range(self.k))
        return self

start = time.perf_counter()
mbkm = MiniBatchKMeans(k=3, batch_size=50).fit(X_cluster)
t_mb = time.perf_counter() - start

print(f"  Mini-Batch K-Means:")
print(f"    Inertia: {mbkm.inertia:.2f}")
print(f"    Time: {t_mb:.4f}s (vs full: {t_km:.4f}s)")


# =====================================================================
#   PARTE 13: K-MEDOIDS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: K-MEDOIDS ===")
print("=" * 80)

"""
K-Medoids: como K-Means pero centroids son puntos reales del dataset.
Mas robusto a outliers.
"""

class KMedoids:
    def __init__(self, k=3, max_iter=50):
        self.k = k
        self.max_iter = max_iter
    
    def fit(self, X):
        n = len(X)
        # Init random medoids
        medoid_idx = np.random.choice(n, self.k, replace=False)
        
        for _ in range(self.max_iter):
            # Assign
            dists = np.array([np.sqrt(np.sum((X - X[m])**2, axis=1)) for m in medoid_idx])
            labels = np.argmin(dists, axis=0)
            
            # Update medoids
            new_medoids = medoid_idx.copy()
            for k in range(self.k):
                cluster_points = np.where(labels == k)[0]
                if len(cluster_points) > 0:
                    # Find point that minimizes total distance within cluster
                    best_cost = float('inf')
                    for p in cluster_points:
                        cost = np.sum(np.sqrt(np.sum((X[cluster_points] - X[p])**2, axis=1)))
                        if cost < best_cost:
                            best_cost = cost
                            new_medoids[k] = p
            
            if np.array_equal(medoid_idx, new_medoids):
                break
            medoid_idx = new_medoids
        
        dists = np.array([np.sqrt(np.sum((X - X[m])**2, axis=1)) for m in medoid_idx])
        self.labels = np.argmin(dists, axis=0)
        self.medoids = X[medoid_idx]
        return self

# Use small subset for K-Medoids (slow)
X_small = X_cluster[np.random.choice(len(X_cluster), 60, replace=False)]
kmed = KMedoids(k=3).fit(X_small)
print(f"  K-Medoids clusters: {Counter(kmed.labels)}")


# =====================================================================
#   PARTE 14: CLUSTER EVALUATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: CLUSTER EVALUATION ===")
print("=" * 80)

"""
Metricas EXTERNAS (requieren true labels):
  - ARI: Adjusted Rand Index. [-1, 1], 1=perfecto.
  - NMI: Normalized Mutual Information. [0, 1].

Metricas INTERNAS (no requieren labels):
  - Silhouette: [-1, 1].
  - Calinski-Harabasz: ratio between-cluster / within-cluster variance.
  - Davies-Bouldin: promedio de similarity entre clusters.
"""

def adjusted_rand_index(labels_true, labels_pred):
    """ARI simplificado."""
    n = len(labels_true)
    
    # Contingency table
    classes = np.unique(labels_true)
    clusters = np.unique(labels_pred)
    
    contingency = np.zeros((len(classes), len(clusters)))
    for i, c in enumerate(classes):
        for j, k in enumerate(clusters):
            contingency[i, j] = np.sum((labels_true == c) & (labels_pred == k))
    
    # Compute ARI components
    sum_comb_c = sum(ni * (ni - 1) / 2 for ni in contingency.sum(axis=1))
    sum_comb_k = sum(nj * (nj - 1) / 2 for nj in contingency.sum(axis=0))
    sum_comb_n = sum(nij * (nij - 1) / 2 for nij in contingency.flatten())
    
    total_comb = n * (n - 1) / 2
    expected = sum_comb_c * sum_comb_k / total_comb if total_comb > 0 else 0
    max_idx = (sum_comb_c + sum_comb_k) / 2
    
    if max_idx == expected:
        return 1.0
    return (sum_comb_n - expected) / (max_idx - expected)

ari = adjusted_rand_index(y_true_cluster, km.labels)
print(f"  ARI (K-Means vs true): {ari:.4f}")


# =====================================================================
#   PARTE 15: PCA FOR DENOISING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: PCA DENOISING ===")
print("=" * 80)

"""
PCA denoising: proyectar a k componentes y reconstruir.
Elimina ruido en componentes menores.
"""

np.random.seed(42)
signal = np.column_stack([np.sin(np.linspace(0, 4*np.pi, 100)),
                          np.cos(np.linspace(0, 4*np.pi, 100))])
noise = np.random.randn(100, 2) * 0.3
noisy = signal + noise

# Denoise with PCA
pca_dn = PCA(n_components=1).fit(noisy)
projected = pca_dn.transform(noisy)
denoised = pca_dn.inverse_transform(projected)

mse_noisy = np.mean((signal - noisy)**2)
mse_denoised = np.mean((signal - denoised)**2)
print(f"  MSE (noisy vs signal):    {mse_noisy:.4f}")
print(f"  MSE (denoised vs signal): {mse_denoised:.4f}")
print(f"  Improvement: {(1 - mse_denoised/mse_noisy)*100:.1f}%")


# =====================================================================
#   PARTE 16: ASSOCIATION RULES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: ASSOCIATION RULES ===")
print("=" * 80)

"""
Market Basket Analysis:
  "Customers who bought X also bought Y"

Metricas:
  - Support: freq(X ∪ Y) / N
  - Confidence: freq(X ∪ Y) / freq(X)
  - Lift: confidence / support(Y). Lift > 1 = asociacion positiva.

Algoritmo: Apriori
1. Encontrar itemsets frecuentes (support >= min_support).
2. Generar reglas con confidence >= min_confidence.
"""

# Simular transacciones
np.random.seed(42)
items = ['bread', 'butter', 'milk', 'eggs', 'cheese']
n_transactions = 200

transactions = []
for _ in range(n_transactions):
    basket = [item for item in items if np.random.random() < 0.4]
    if basket:
        transactions.append(set(basket))

# Compute support for pairs
print(f"  {n_transactions} transactions, {len(items)} items")
print(f"\n  Top associations:")

for i in range(len(items)):
    for j in range(i+1, len(items)):
        a, b = items[i], items[j]
        support_ab = sum(1 for t in transactions if a in t and b in t) / len(transactions)
        support_a = sum(1 for t in transactions if a in t) / len(transactions)
        support_b = sum(1 for t in transactions if b in t) / len(transactions)
        confidence = support_ab / support_a if support_a > 0 else 0
        lift = confidence / support_b if support_b > 0 else 0
        
        if support_ab > 0.1:
            print(f"    {a} -> {b}: supp={support_ab:.3f}, conf={confidence:.3f}, lift={lift:.2f}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE UNSUPERVISED:

1. K-Means: simple, rapido, necesita K, asume clusters esfericos.
2. K-Means++: mejor inicializacion.
3. Elbow + Silhouette: seleccionar K optimo.
4. PCA: reduccion lineal, preservar varianza.
5. Anomaly: Z-score, Mahalanobis, Isolation Forest.
6. GMM: soft clustering, probabilistico.
7. Hierarchical: dendrogram, no necesita K a priori.
8. DBSCAN: density-based, detecta outliers, forma arbitraria.

FIN DEL MODULO 13: ML FUNDAMENTOS.
"""

print("\n FIN DE ARCHIVO 04_unsupervised.")
print(" Unsupervised learning ha sido dominado.")
print(" Siguiente modulo: ENSEMBLE METHODS.")
