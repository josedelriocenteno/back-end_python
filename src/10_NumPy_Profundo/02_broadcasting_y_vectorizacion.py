# ===========================================================================
# 02_broadcasting_y_vectorizacion.py
# ===========================================================================
# MODULO 10: NUMPY PROFUNDO
# ARCHIVO 02: Broadcasting, Vectorizacion y Operaciones Avanzadas
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar broadcasting, vectorizacion, ufuncs, einsum,
# y todas las operaciones que eliminan loops de Python.
#
# CONTENIDO:
#   1. Broadcasting rules y mecanismo interno.
#   2. Vectorizacion: eliminar loops.
#   3. Universal functions (ufuncs).
#   4. Reduccion, acumulacion, outer.
#   5. np.einsum: la navaja suiza.
#   6. Fancy indexing avanzado.
#   7. np.where, np.select, np.piecewise.
#   8. Operaciones de conjuntos.
#   9. Sorting y partitioning.
#   10. Performance: vectorizado vs loops.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: BROADCASTING
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: BROADCASTING ===")
print("=" * 80)

"""
Broadcasting: operar arrays de diferente shape sin copiar datos.

Reglas:
1. Si ndim difiere, el menor se PADDING con 1s a la izquierda.
2. Dimensiones de tamaño 1 se ESTIRAN para igualar.
3. Si dos dimensiones no son 1 y son distintas -> ERROR.

Ejemplo: (3,4) + (4,) -> (3,4) + (1,4) -> (3,4)
         (3,1) + (1,4) -> (3,4)
"""

print("\n--- Broadcasting basico ---")

a = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [10, 20, 30, 40]])  # (3, 4)
b = np.array([100, 200, 300, 400])  # (4,)

result = a + b
print(f"  a shape: {a.shape}")
print(f"  b shape: {b.shape}")
print(f"  a + b shape: {result.shape}")
print(f"  Result:\n{result}")


print("\n--- Broadcasting 2D ---")

col = np.array([[1], [2], [3]])  # (3, 1)
row = np.array([10, 20, 30, 40])  # (4,) -> (1, 4)

outer = col * row  # (3, 1) * (1, 4) -> (3, 4)
print(f"  col shape: {col.shape}")
print(f"  row shape: {row.shape}")
print(f"  col * row:\n{outer}")


print("\n--- Broadcasting: errores comunes ---")

try:
    x = np.ones((3, 4))
    y = np.ones((3, 5))
    _ = x + y
except ValueError as e:
    print(f"  (3,4) + (3,5) -> ERROR: {e}")


print("\n--- Broadcasting: normalizacion ---")

"""
EN ML: normalizar features por columna.
X_norm = (X - mean) / std
mean tiene shape (n_features,), X tiene (n_samples, n_features).
Broadcasting hace la resta y division por filas automaticamente.
"""

np.random.seed(42)
X = np.random.randn(100, 5) * np.array([1, 10, 100, 0.1, 50])

mean = X.mean(axis=0)  # (5,)
std = X.std(axis=0)    # (5,)
X_norm = (X - mean) / std  # Broadcasting: (100,5) - (5,) / (5,)

print(f"  Original mean: {X.mean(axis=0).round(2)}")
print(f"  Original std:  {X.std(axis=0).round(2)}")
print(f"  Normalized mean: {X_norm.mean(axis=0).round(4)}")
print(f"  Normalized std:  {X_norm.std(axis=0).round(4)}")


# =====================================================================
#   PARTE 2: VECTORIZACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: VECTORIZACION ===")
print("=" * 80)

"""
REGLA DE ORO: NUNCA usar for-loop sobre elementos numpy.
Cada operacion numpy opera en C sobre todo el array.
"""

print("\n--- Loop vs vectorizado ---")

n = 1000000
a = np.random.randn(n)
b = np.random.randn(n)

# Loop Python
start = time.perf_counter()
c_loop = np.empty(n)
for i in range(n):
    c_loop[i] = a[i] + b[i]
t_loop = time.perf_counter() - start

# Vectorizado
start = time.perf_counter()
c_vec = a + b
t_vec = time.perf_counter() - start

print(f"  Loop:       {t_loop:.4f}s")
print(f"  Vectorized: {t_vec:.6f}s")
print(f"  Speedup:    {t_loop/t_vec:.0f}x")


print("\n--- Ejemplo: distancia euclidiana ---")

def euclidean_loop(X, y):
    """Distancias con loops."""
    n = X.shape[0]
    dists = np.empty(n)
    for i in range(n):
        dists[i] = np.sqrt(np.sum((X[i] - y)**2))
    return dists

def euclidean_vectorized(X, y):
    """Distancias vectorizadas."""
    return np.sqrt(np.sum((X - y)**2, axis=1))

X = np.random.randn(10000, 50)
y = np.random.randn(50)

start = time.perf_counter()
d_loop = euclidean_loop(X, y)
t_loop = time.perf_counter() - start

start = time.perf_counter()
d_vec = euclidean_vectorized(X, y)
t_vec = time.perf_counter() - start

print(f"  Loop:       {t_loop:.4f}s")
print(f"  Vectorized: {t_vec:.6f}s")
print(f"  Speedup:    {t_loop/t_vec:.0f}x")
print(f"  Results match: {np.allclose(d_loop, d_vec)}")


print("\n--- Pairwise distances (fully vectorized) ---")

def pairwise_distances(X):
    """Todas las distancias entre pares. O(n²) pero sin loops."""
    # ||x-y||² = ||x||² + ||y||² - 2*x·y
    sq_norms = np.sum(X**2, axis=1)
    D = sq_norms[:, None] + sq_norms[None, :] - 2 * X @ X.T
    return np.sqrt(np.maximum(D, 0))

X_small = np.random.randn(500, 10)
start = time.perf_counter()
D = pairwise_distances(X_small)
t = time.perf_counter() - start
print(f"  500 points, 10D: {t:.4f}s")
print(f"  D shape: {D.shape}")
print(f"  D[0,0] = {D[0,0]:.6f} (should be 0)")


# =====================================================================
#   PARTE 3: UFUNCS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: UNIVERSAL FUNCTIONS (UFUNCS) ===")
print("=" * 80)

"""
ufunc: funcion que opera elemento a elemento sobre arrays.
Implementada en C, soporta broadcasting.

Tipos: unary (sin, exp), binary (+, *), reduce (sum), accumulate (cumsum).
"""

print("\n--- ufuncs matematicas ---")

x = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
print(f"  x = {x.round(4)}")
print(f"  sin(x) = {np.sin(x).round(4)}")
print(f"  cos(x) = {np.cos(x).round(4)}")
print(f"  exp(x) = {np.exp(x).round(4)}")
print(f"  log(exp(x)) = {np.log(np.exp(x)).round(4)}")


print("\n--- ufunc.reduce ---")

a = np.array([1, 2, 3, 4, 5])
print(f"  a = {a}")
print(f"  np.add.reduce(a) = {np.add.reduce(a)}  (= sum)")
print(f"  np.multiply.reduce(a) = {np.multiply.reduce(a)}  (= product)")
print(f"  np.maximum.reduce(a) = {np.maximum.reduce(a)}  (= max)")


print("\n--- ufunc.accumulate ---")

print(f"  np.add.accumulate(a) = {np.add.accumulate(a)}  (= cumsum)")
print(f"  np.multiply.accumulate(a) = {np.multiply.accumulate(a)}  (= cumprod)")


print("\n--- ufunc.outer ---")

b = np.array([10, 20, 30])
c = np.array([1, 2, 3, 4])
outer = np.multiply.outer(b, c)
print(f"  multiply.outer([10,20,30], [1,2,3,4]):\n{outer}")


print("\n--- Custom ufunc con np.frompyfunc ---")

def relu(x):
    return max(0, x)

relu_ufunc = np.frompyfunc(relu, 1, 1)
x = np.array([-2, -1, 0, 1, 2], dtype=np.float64)
print(f"  relu({x}) = {relu_ufunc(x)}")


print("\n--- np.vectorize (NO es mas rapido) ---")

"""
ADVERTENCIA: np.vectorize NO acelera. Es solo conveniencia.
Sigue llamando la funcion Python por cada elemento.
"""

@np.vectorize
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Vectorize real
def sigmoid_real(x):
    return 1 / (1 + np.exp(-x))

x = np.random.randn(100000)
start = time.perf_counter()
_ = sigmoid(x)
t_fake = time.perf_counter() - start

start = time.perf_counter()
_ = sigmoid_real(x)
t_real = time.perf_counter() - start

print(f"  np.vectorize: {t_fake:.4f}s")
print(f"  Real vectorized: {t_real:.6f}s")
print(f"  Real is {t_fake/t_real:.0f}x faster")


# =====================================================================
#   PARTE 4: EINSUM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: NP.EINSUM ===")
print("=" * 80)

"""
einsum: Einstein summation notation.
La herramienta MAS PODEROSA de NumPy.
Puede expresar CUALQUIER operacion tensorencial.

Sintaxis: np.einsum('indices_input->indices_output', arrays)
Indices repetidos en input = sumados.
"""

print("\n--- Operaciones basicas con einsum ---")

A = np.random.randn(3, 4)
B = np.random.randn(4, 5)
v = np.random.randn(4)

# Traza
M = np.random.randn(3, 3)
trace = np.einsum('ii->', M)
print(f"  Trace: einsum={trace:.4f}, np.trace={np.trace(M):.4f}")

# Diagonal
diag = np.einsum('ii->i', M)
print(f"  Diagonal: {diag.round(4)}")

# Sum
total = np.einsum('ij->', A)
print(f"  Sum: einsum={total:.4f}, np.sum={np.sum(A):.4f}")

# Column sum
col_sum = np.einsum('ij->j', A)
print(f"  Col sum: {np.allclose(col_sum, A.sum(axis=0))}")

# Matrix-vector
Av = np.einsum('ij,j->i', A, v)
print(f"  Mat-vec: {np.allclose(Av, A @ v)}")

# Matrix-matrix
AB = np.einsum('ij,jk->ik', A, B)
print(f"  Mat-mat: {np.allclose(AB, A @ B)}")

# Outer product
outer = np.einsum('i,j->ij', v[:3], v[:3])
print(f"  Outer: {np.allclose(outer, np.outer(v[:3], v[:3]))}")

# Hadamard (element-wise)
C = np.random.randn(3, 4)
hadamard = np.einsum('ij,ij->ij', A, C)
print(f"  Hadamard: {np.allclose(hadamard, A * C)}")


print("\n--- Einsum para batched operations ---")

"""
EN ML: batch de matrices. einsum maneja la dimension batch.
"""

batch_size = 16
seq_len = 10
d_model = 64

Q = np.random.randn(batch_size, seq_len, d_model)
K = np.random.randn(batch_size, seq_len, d_model)

# Batched Q @ K^T (attention scores)
scores = np.einsum('bqd,bkd->bqk', Q, K)
print(f"  Q shape: {Q.shape}")
print(f"  K shape: {K.shape}")
print(f"  Scores shape: {scores.shape}")

# Verificar contra loop
scores_loop = np.array([Q[i] @ K[i].T for i in range(batch_size)])
print(f"  Match loop: {np.allclose(scores, scores_loop)}")


print("\n--- Einsum: multi-head attention ---")

n_heads = 8
d_k = d_model // n_heads

Q_mh = np.random.randn(batch_size, n_heads, seq_len, d_k)
K_mh = np.random.randn(batch_size, n_heads, seq_len, d_k)

scores_mh = np.einsum('bhqd,bhkd->bhqk', Q_mh, K_mh)
print(f"  Multi-head scores: {scores_mh.shape}")


# =====================================================================
#   PARTE 5: FANCY INDEXING AVANZADO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: FANCY INDEXING AVANZADO ===")
print("=" * 80)

print("\n--- Integer array indexing ---")

a = np.arange(20).reshape(4, 5)
print(f"  Array:\n{a}")

# Seleccionar elementos especificos
rows = np.array([0, 1, 3])
cols = np.array([1, 3, 4])
print(f"  a[{rows}, {cols}] = {a[rows, cols]}")

# Reordenar filas
perm = np.array([3, 0, 2, 1])
print(f"  Reordenado:\n{a[perm]}")


print("\n--- Boolean indexing ---")

# Filtrado condicional
mask = a > 10
print(f"  a > 10:\n{mask}")
print(f"  a[a > 10] = {a[mask]}")

# Multiples condiciones
mask2 = (a > 5) & (a < 15)
print(f"  5 < a < 15: {a[mask2]}")


print("\n--- np.take, np.put, np.choose ---")

arr = np.arange(10) * 10
indices = np.array([2, 5, 7])
print(f"  take: {np.take(arr, indices)}")

# np.take_along_axis (sorting)
matrix = np.random.randn(3, 5)
sort_idx = np.argsort(matrix, axis=1)
sorted_matrix = np.take_along_axis(matrix, sort_idx, axis=1)
print(f"  take_along_axis sorts correctly: "
      f"{np.allclose(sorted_matrix, np.sort(matrix, axis=1))}")


# =====================================================================
#   PARTE 6: WHERE, SELECT, PIECEWISE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: WHERE, SELECT, PIECEWISE ===")
print("=" * 80)

print("\n--- np.where ---")

x = np.array([-3, -1, 0, 1, 3])

# Vectorized if-else
result = np.where(x > 0, x, 0)  # ReLU!
print(f"  ReLU({x}) = {result}")

# Find indices
idx = np.where(x > 0)
print(f"  Indices > 0: {idx[0]}")


print("\n--- np.select ---")

"""
np.select: multiples condiciones -> multiples valores.
Como un switch/case vectorizado.
"""

x = np.linspace(-5, 5, 11)
conditions = [x < -2, (x >= -2) & (x <= 2), x > 2]
choices = [-1, 0, 1]  # sign-like

result = np.select(conditions, choices, default=np.nan)
print(f"  x:      {x}")
print(f"  select: {result}")


print("\n--- np.clip ---")

x = np.array([-5, -2, 0, 3, 7, 10])
clipped = np.clip(x, 0, 5)
print(f"  clip({x}, 0, 5) = {clipped}")


# =====================================================================
#   PARTE 7: OPERACIONES DE CONJUNTOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: OPERACIONES DE CONJUNTOS ===")
print("=" * 80)

a = np.array([1, 2, 3, 4, 5, 5, 3])
b = np.array([3, 4, 5, 6, 7])

print(f"  a: {a}")
print(f"  b: {b}")
print(f"  unique(a): {np.unique(a)}")
print(f"  union: {np.union1d(a, b)}")
print(f"  intersect: {np.intersect1d(a, b)}")
print(f"  setdiff(a,b): {np.setdiff1d(a, b)}")
print(f"  in1d: {np.in1d(a, b)}")


# =====================================================================
#   PARTE 8: SORTING Y PARTITIONING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: SORTING Y PARTITIONING ===")
print("=" * 80)

print("\n--- Sort algorithms ---")

arr = np.random.randn(100000)

for kind in ['quicksort', 'mergesort', 'heapsort']:
    start = time.perf_counter()
    _ = np.sort(arr, kind=kind)
    t = time.perf_counter() - start
    print(f"  {kind:10s}: {t:.4f}s")


print("\n--- argsort ---")

scores = np.array([0.8, 0.3, 0.95, 0.6, 0.1])
ranking = np.argsort(scores)[::-1]
print(f"  Scores: {scores}")
print(f"  Ranking (best first): {ranking}")
print(f"  Sorted: {scores[ranking]}")


print("\n--- partition (partial sort) ---")

"""
np.partition: O(n) para encontrar los k menores.
Mucho mas rapido que sort completo si solo necesitas top-k.
"""

big_arr = np.random.randn(1000000)

start = time.perf_counter()
top10_sort = np.sort(big_arr)[-10:]
t_sort = time.perf_counter() - start

start = time.perf_counter()
top10_part = big_arr[np.argpartition(big_arr, -10)[-10:]]
t_part = time.perf_counter() - start

print(f"  Full sort for top-10: {t_sort:.4f}s")
print(f"  Partition for top-10: {t_part:.4f}s")
print(f"  Speedup: {t_sort/t_part:.1f}x")


# =====================================================================
#   PARTE 9: OPERACIONES SOBRE EJES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: OPERACIONES SOBRE EJES ===")
print("=" * 80)

"""
axis=0: opera SOBRE filas (colapsa filas).
axis=1: opera SOBRE columnas (colapsa columnas).
axis=None: opera sobre todo el array.
keepdims=True: mantiene la dimension para broadcasting.
"""

print("\n--- axis y keepdims ---")

M = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print(f"  M:\n{M}")
print(f"  sum(axis=0): {M.sum(axis=0)}  (suma por columna)")
print(f"  sum(axis=1): {M.sum(axis=1)}  (suma por fila)")
print(f"  sum(): {M.sum()}")

# keepdims para broadcasting
mean_cols = M.mean(axis=0, keepdims=True)
print(f"\n  mean(axis=0, keepdims=True) shape: {mean_cols.shape}")
centered = M - mean_cols
print(f"  Centered:\n{centered}")

# Multiple axes
batch = np.random.randn(8, 10, 64)
print(f"\n  batch shape: {batch.shape}")
print(f"  mean(axis=(0,1)) shape: {batch.mean(axis=(0,1)).shape}")
print(f"  mean(axis=(1,2)) shape: {batch.mean(axis=(1,2)).shape}")


# =====================================================================
#   PARTE 10: RESHAPE, STACK, SPLIT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: RESHAPE, STACK, SPLIT ===")
print("=" * 80)

print("\n--- reshape, ravel, flatten ---")

a = np.arange(12)
print(f"  a: {a}")
print(f"  reshape(3,4):\n{a.reshape(3, 4)}")
print(f"  reshape(2,-1):\n{a.reshape(2, -1)}  (-1 = infer)")
print(f"  reshape(-1,1) shape: {a.reshape(-1, 1).shape}  (column vector)")

# ravel = view, flatten = copy
r = a.reshape(3, 4)
print(f"\n  ravel is view: {r.ravel().base is r}")
print(f"  flatten is copy: {r.flatten().base is None}")


print("\n--- stack, concatenate, split ---")

x = np.array([1, 2, 3])
y = np.array([4, 5, 6])

print(f"  hstack: {np.hstack([x, y])}")
print(f"  vstack:\n{np.vstack([x, y])}")
print(f"  stack(axis=0):\n{np.stack([x, y], axis=0)}")
print(f"  stack(axis=1):\n{np.stack([x, y], axis=1)}")

# Split
big = np.arange(12)
parts = np.split(big, 3)
print(f"\n  split into 3: {[p.tolist() for p in parts]}")


print("\n--- expand_dims, squeeze, newaxis ---")

v = np.array([1, 2, 3])
print(f"  v shape: {v.shape}")
print(f"  v[None, :] shape: {v[None, :].shape}  (row)")
print(f"  v[:, None] shape: {v[:, None].shape}  (column)")
print(f"  expand_dims(v, 0): {np.expand_dims(v, 0).shape}")

# squeeze
s = np.array([[[1, 2, 3]]])
print(f"  {s.shape} -> squeeze -> {s.squeeze().shape}")


# =====================================================================
#   PARTE 11: SOFTMAX Y LOGSUMEXP VECTORIZADOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: SOFTMAX VECTORIZADO ===")
print("=" * 80)

def softmax(logits, axis=-1):
    """Softmax numericamente estable."""
    shifted = logits - logits.max(axis=axis, keepdims=True)
    exp_shifted = np.exp(shifted)
    return exp_shifted / exp_shifted.sum(axis=axis, keepdims=True)

def log_softmax(logits, axis=-1):
    """Log-softmax numericamente estable."""
    shifted = logits - logits.max(axis=axis, keepdims=True)
    return shifted - np.log(np.exp(shifted).sum(axis=axis, keepdims=True))

# Batch softmax
logits = np.random.randn(4, 10)
probs = softmax(logits)
log_probs = log_softmax(logits)

print(f"  Logits shape: {logits.shape}")
print(f"  Probs sum per sample: {probs.sum(axis=1).round(4)}")
print(f"  All positive: {(probs > 0).all()}")
print(f"  log_softmax consistent: {np.allclose(np.log(probs), log_probs)}")

# Big logits (test numerical stability)
big_logits = np.array([1000, 1001, 1002], dtype=np.float64)
print(f"\n  Big logits: {big_logits}")
print(f"  Softmax: {softmax(big_logits)}")
print(f"  (No overflow!)")


# =====================================================================
#   PARTE 12: PERFORMANCE PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: PERFORMANCE PATTERNS ===")
print("=" * 80)

print("\n--- Pre-allocation vs append ---")

n = 100000

# BAD: append
start = time.perf_counter()
result_list = []
for i in range(n):
    result_list.append(i**2)
result_bad = np.array(result_list)
t_bad = time.perf_counter() - start

# GOOD: pre-allocate
start = time.perf_counter()
result_good = np.empty(n)
for i in range(n):
    result_good[i] = i**2
t_good = time.perf_counter() - start

# BEST: vectorize
start = time.perf_counter()
result_best = np.arange(n)**2
t_best = time.perf_counter() - start

print(f"  Append:       {t_bad:.4f}s")
print(f"  Pre-allocate: {t_good:.4f}s")
print(f"  Vectorized:   {t_best:.6f}s")


print("\n--- In-place operations ---")

a = np.random.randn(1000000)

start = time.perf_counter()
b = a + 1  # Creates new array
t_new = time.perf_counter() - start

start = time.perf_counter()
a += 1  # In-place
t_inplace = time.perf_counter() - start

print(f"  New array: {t_new:.6f}s")
print(f"  In-place:  {t_inplace:.6f}s")


# =====================================================================
#   PARTE 13: MESHGRID Y GRIDS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: MESHGRID Y GRIDS ===")
print("=" * 80)

"""
np.meshgrid: crear grids para evaluacion de funciones 2D.
Usado en: visualizacion, decision boundaries, generacion de datos.
"""

print("\n--- np.meshgrid ---")

x = np.linspace(-2, 2, 5)
y = np.linspace(-1, 1, 3)
X, Y = np.meshgrid(x, y)

print(f"  x: {x}")
print(f"  y: {y}")
print(f"  X shape: {X.shape}")
print(f"  Y shape: {Y.shape}")
print(f"  X:\n{X}")
print(f"  Y:\n{Y}")

# Evaluar funcion en grid
Z = np.sin(X) * np.cos(Y)
print(f"  sin(X)*cos(Y) shape: {Z.shape}")


print("\n--- np.mgrid y np.ogrid ---")

# mgrid: como meshgrid pero con slices
grid = np.mgrid[0:3, 0:4]
print(f"  mgrid shape: {grid.shape}")

# ogrid: open grid (broadcasting-ready)
ox, oy = np.ogrid[0:3, 0:4]
print(f"  ogrid shapes: {ox.shape}, {oy.shape}")
print(f"  Broadcast result: {(ox + oy).shape}")


# =====================================================================
#   PARTE 14: COSINE SIMILARITY VECTORIZADO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: COSINE SIMILARITY ===")
print("=" * 80)

"""
cos_sim(a, b) = (a · b) / (||a|| * ||b||)

Fundamental en: embeddings, NLP, retrieval, recommendation.
"""

print("\n--- Cosine similarity vectorizado ---")

def cosine_similarity_matrix(X):
    """Cosine similarity entre todas las filas."""
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    X_normalized = X / (norms + 1e-15)
    return X_normalized @ X_normalized.T

np.random.seed(42)
embeddings = np.random.randn(5, 128)

cos_sim = cosine_similarity_matrix(embeddings)
print(f"  Embeddings: {embeddings.shape}")
print(f"  Similarity matrix:\n{cos_sim.round(3)}")
print(f"  Diagonal (self-sim): {np.diag(cos_sim).round(3)}")


print("\n--- Top-k nearest neighbors ---")

def topk_similar(query_idx, sim_matrix, k=3):
    """Encontrar top-k mas similares."""
    sims = sim_matrix[query_idx]
    # Excluir self
    sims[query_idx] = -np.inf
    top_k = np.argpartition(sims, -k)[-k:]
    top_k = top_k[np.argsort(sims[top_k])[::-1]]
    return top_k, sims[top_k]

indices, scores = topk_similar(0, cos_sim.copy(), k=3)
print(f"  Query: item 0")
print(f"  Top-3 similar: {indices} with scores {scores.round(4)}")


# =====================================================================
#   PARTE 15: ATTENTION WEIGHTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: ATTENTION WEIGHTS CON NUMPY ===")
print("=" * 80)

"""
Scaled dot-product attention completo con NumPy puro.
"""

def scaled_dot_product_attention(Q, K, V, mask=None):
    """Attention: softmax(QK^T / sqrt(d)) * V"""
    d_k = Q.shape[-1]
    scores = np.einsum('...qd,...kd->...qk', Q, K) / np.sqrt(d_k)
    
    if mask is not None:
        scores = np.where(mask, scores, -1e9)
    
    # Stable softmax
    scores_max = scores.max(axis=-1, keepdims=True)
    exp_scores = np.exp(scores - scores_max)
    attn_weights = exp_scores / exp_scores.sum(axis=-1, keepdims=True)
    
    output = np.einsum('...qk,...kd->...qd', attn_weights, V)
    return output, attn_weights

np.random.seed(42)
batch, heads, seq, dk = 2, 4, 8, 16
Q = np.random.randn(batch, heads, seq, dk)
K = np.random.randn(batch, heads, seq, dk)
V = np.random.randn(batch, heads, seq, dk)

# Causal mask
causal_mask = np.tril(np.ones((seq, seq), dtype=bool))

output, weights = scaled_dot_product_attention(Q, K, V, causal_mask)
print(f"  Q,K,V shape: ({batch},{heads},{seq},{dk})")
print(f"  Output shape: {output.shape}")
print(f"  Attention weights shape: {weights.shape}")
print(f"  Weights sum per query: {weights[0,0].sum(axis=-1).round(4)}")
print(f"  Causal mask works: {(weights[0,0] * ~causal_mask).sum() < 1e-6}")


# =====================================================================
#   PARTE 16: GRADIENT PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: GRADIENT PATTERNS ===")
print("=" * 80)

"""
Patterns comunes para computar gradientes con NumPy.
"""

print("\n--- Numerical gradient ---")

def numerical_gradient(f, x, eps=1e-5):
    """Gradiente numerico (central differences)."""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * eps)
    return grad

# Test: f(x) = ||x||² -> grad = 2x
f = lambda x: np.sum(x**2)
x = np.array([1.0, 2.0, 3.0])
grad_num = numerical_gradient(f, x)
grad_exact = 2 * x

print(f"  f(x) = ||x||²")
print(f"  x = {x}")
print(f"  Numerical grad: {grad_num.round(6)}")
print(f"  Exact grad:     {grad_exact}")
print(f"  Match: {np.allclose(grad_num, grad_exact, atol=1e-4)}")


print("\n--- Gradient of softmax-CE ---")

def softmax_ce_gradient(logits, target):
    """Gradiente de softmax + cross-entropy."""
    shifted = logits - logits.max()
    exp_l = np.exp(shifted)
    probs = exp_l / exp_l.sum()
    
    # El gradiente es simplemente: probs - one_hot(target)
    grad = probs.copy()
    grad[target] -= 1.0
    return grad, probs

logits = np.array([2.0, 1.0, 0.1])
target = 0

grad, probs = softmax_ce_gradient(logits, target)
print(f"  Logits: {logits}")
print(f"  Probs: {probs.round(4)}")
print(f"  Target: {target}")
print(f"  Gradient: {grad.round(4)}")
print(f"  (probs[target] - 1 is negative: push UP correct class)")


# =====================================================================
#   PARTE 17: NP.PAD Y DATA AUGMENTATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: NP.PAD ===")
print("=" * 80)

print("\n--- Padding modes ---")

arr = np.array([[1, 2, 3],
                [4, 5, 6]])

for mode in ['constant', 'edge', 'reflect', 'wrap']:
    padded = np.pad(arr, 1, mode=mode)
    print(f"  {mode:10s}:\n{padded}\n")


# =====================================================================
#   PARTE 18: HISTOGRAM, BINCOUNT, DIGITIZE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: HISTOGRAM Y BINCOUNT ===")
print("=" * 80)

"""
Herramientas para analisis de distribuciones.
np.histogram: contar en bins.
np.bincount: contar ocurrencias de enteros.
np.digitize: asignar bin a cada valor.
"""

print("\n--- np.histogram ---")

np.random.seed(42)
data = np.random.randn(10000)
counts, edges = np.histogram(data, bins=10)

print(f"  Data: {len(data)} samples")
for i in range(len(counts)):
    bar = "█" * (counts[i] // 50)
    print(f"  [{edges[i]:+5.2f}, {edges[i+1]:+5.2f}): {counts[i]:4d} {bar}")


print("\n--- np.bincount ---")

labels = np.array([0, 1, 1, 2, 0, 2, 2, 1, 0, 3, 3, 3, 3])
counts = np.bincount(labels)
print(f"  Labels: {labels}")
print(f"  Counts: {counts}")

# Con pesos (util para class-weighted loss)
weights = np.array([1.0, 0.5, 0.5, 0.3, 1.0, 0.3, 0.3, 0.5, 1.0, 0.2, 0.2, 0.2, 0.2])
weighted_counts = np.bincount(labels, weights=weights)
print(f"  Weighted: {weighted_counts.round(2)}")


print("\n--- np.digitize ---")

values = np.array([0.1, 0.5, 1.5, 2.5, 3.5, 4.5])
bins = np.array([1, 2, 3, 4])
indices = np.digitize(values, bins)
print(f"  Values: {values}")
print(f"  Bins:   {bins}")
print(f"  Indices: {indices}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE BROADCASTING Y VECTORIZACION:

1. Broadcasting: operar arrays de diferente shape sin copias.

2. Vectorizacion: 100-1000x mas rapido que loops Python.

3. ufuncs: reduce, accumulate, outer para operaciones.

4. einsum: CUALQUIER operacion tensorial en una linea.

5. Fancy indexing: seleccion flexible (crea copias).

6. np.where/select: condicionales vectorizados.

7. partition: O(n) para top-k vs O(n log n) de sort.

8. axis + keepdims: operaciones por dimension.

9. softmax estable: shift por max antes de exp.

10. Performance: pre-allocate > append, in-place > new.

Siguiente archivo: Algebra lineal con NumPy.
"""

print("\n FIN DE ARCHIVO 02_broadcasting_y_vectorizacion.")
print(" Broadcasting y vectorizacion han sido dominados.")
