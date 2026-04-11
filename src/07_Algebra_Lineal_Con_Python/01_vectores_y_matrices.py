# ===========================================================================
# 01_vectores_y_matrices.py
# ===========================================================================
# MODULO 07: ALGEBRA LINEAL CON PYTHON
# ARCHIVO 01: Vectores, Matrices y Operaciones Fundamentales
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar vectores y matrices con NumPy: creacion, operaciones,
# broadcasting, algebra lineal basica. Todo orientado a ML/IA.
#
# CONTENIDO:
#   1. Escalares, vectores, matrices, tensores.
#   2. Creacion de arrays con NumPy.
#   3. Operaciones vectoriales: suma, producto punto, normas.
#   4. Operaciones matriciales: multiplicacion, transpuesta, inversa.
#   5. Broadcasting: reglas y aplicaciones.
#   6. Indexacion avanzada.
#   7. Aplicaciones ML: similaridad coseno, distancias.
#   8. Ejercicio: operaciones sobre embeddings.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: ESCALARES, VECTORES, MATRICES, TENSORES
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: JERARQUIA DE OBJETOS MATEMATICOS ===")
print("=" * 80)

"""
Escalar:  0 dimensiones. Un numero.          np.array(5)
Vector:   1 dimension. Lista de numeros.      np.array([1, 2, 3])
Matriz:   2 dimensiones. Tabla de numeros.    np.array([[1,2],[3,4]])
Tensor:   N dimensiones. Generalizacion.      np.array([[[1,2],[3,4]]])

EN ML:
- Escalar: learning rate, loss.
- Vector: embedding de una palabra, features de una muestra.
- Matriz: batch de embeddings, pesos de una capa.
- Tensor 3D: secuencia de embeddings (batch, seq_len, embed_dim).
- Tensor 4D: imagen (batch, channels, height, width).
"""

print("\n--- Dimensiones ---")

escalar = np.array(3.14)
vector = np.array([1.0, 2.0, 3.0])
matriz = np.array([[1, 2, 3], [4, 5, 6]])
tensor_3d = np.random.randn(2, 3, 4)  # batch=2, seq=3, dim=4

for nombre, arr in [("Escalar", escalar), ("Vector", vector),
                     ("Matriz", matriz), ("Tensor 3D", tensor_3d)]:
    print(f"  {nombre}: shape={arr.shape}, ndim={arr.ndim}, "
          f"dtype={arr.dtype}, size={arr.size}")


# =====================================================================
#   PARTE 2: CREACION DE ARRAYS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: CREACION DE ARRAYS CON NUMPY ===")
print("=" * 80)

"""
NumPy ofrece multiples formas de crear arrays optimizados.
"""

print("\n--- Funciones de creacion ---")

# Zeros, ones, full
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
full = np.full((2, 2), 7.0)

print(f"  zeros(3,4): shape={zeros.shape}")
print(f"  ones(2,3):\n{ones}")
print(f"  full(2,2, 7.0):\n{full}")

# Identity y eye
identidad = np.eye(3)
print(f"\n  Identidad 3x3:\n{identidad}")

# Rangos
rango = np.arange(0, 10, 2)
linspace = np.linspace(0, 1, 5)
logspace = np.logspace(-3, 0, 4)  # 10^-3 a 10^0

print(f"\n  arange(0,10,2): {rango}")
print(f"  linspace(0,1,5): {linspace}")
print(f"  logspace(-3,0,4): {logspace}")

# Random
np.random.seed(42)
uniform = np.random.uniform(0, 1, (2, 3))
normal = np.random.randn(2, 3)
randint = np.random.randint(0, 10, (3, 3))

print(f"\n  uniform(0,1):\n{uniform}")
print(f"\n  randn(2,3):\n{normal}")
print(f"\n  randint(0,10):\n{randint}")


print("\n--- Tipos de datos ---")

print("""
+----------+-----------+-----------------------------+
| DTYPE    | BYTES     | USO EN ML                   |
+----------+-----------+-----------------------------+
| float32  | 4         | Pesos de modelo (GPU)       |
| float64  | 8         | Calculos de precision       |
| int32    | 4         | Indices, labels             |
| int64    | 8         | Contadores grandes          |
| bool     | 1         | Mascaras                    |
| float16  | 2         | Mixed precision training    |
+----------+-----------+-----------------------------+
""")

f32 = np.array([1.0, 2.0], dtype=np.float32)
f64 = np.array([1.0, 2.0], dtype=np.float64)
print(f"  float32: {f32.nbytes} bytes")
print(f"  float64: {f64.nbytes} bytes")
print(f"  Ratio: {f64.nbytes / f32.nbytes}x")


# =====================================================================
#   PARTE 3: OPERACIONES VECTORIALES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: OPERACIONES VECTORIALES ===")
print("=" * 80)

"""
Operaciones fundamentales sobre vectores:
- Suma/resta elemento a elemento
- Producto escalar (dot product)
- Normas (L1, L2, Linf)
- Producto exterior
"""

print("\n--- Suma y resta ---")

a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])

print(f"  a = {a}")
print(f"  b = {b}")
print(f"  a + b = {a + b}")
print(f"  a - b = {a - b}")
print(f"  a * b (elemento) = {a * b}")  # NO es producto matricial
print(f"  a / b (elemento) = {a / b}")


print("\n--- Producto escalar (dot product) ---")

"""
dot(a, b) = sum(a_i * b_i) = |a| * |b| * cos(theta)

EN ML: similaridad entre embeddings.
"""

dot = np.dot(a, b)  # = 1*4 + 2*5 + 3*6 = 32
dot_alt = a @ b     # Operador @ es lo mismo

print(f"  a · b = {dot}")
print(f"  a @ b = {dot_alt}")
print(f"  Manual: {sum(ai * bi for ai, bi in zip(a, b))}")


print("\n--- Normas ---")

"""
L1 (Manhattan): sum(|x_i|)
L2 (Euclidea):  sqrt(sum(x_i^2))
Linf (Max):     max(|x_i|)

EN ML: regularizacion L1 (sparsity), L2 (weight decay).
"""

v = np.array([3.0, -4.0, 5.0])

l1 = np.linalg.norm(v, ord=1)
l2 = np.linalg.norm(v, ord=2)
linf = np.linalg.norm(v, ord=np.inf)

print(f"  v = {v}")
print(f"  ||v||_1 (L1): {l1}")
print(f"  ||v||_2 (L2): {l2}")
print(f"  ||v||_inf:     {linf}")

# Normalizar a norma unitaria
v_norm = v / np.linalg.norm(v)
print(f"\n  v normalizado: {v_norm}")
print(f"  ||v_norm||_2 = {np.linalg.norm(v_norm):.10f}")


print("\n--- Producto exterior ---")

"""
outer(a, b) produce una MATRIZ: resultado[i,j] = a[i] * b[j]
"""

a_small = np.array([1, 2, 3])
b_small = np.array([4, 5])

outer = np.outer(a_small, b_small)
print(f"  a = {a_small}, b = {b_small}")
print(f"  outer(a, b):\n{outer}")
print(f"  Shape: {outer.shape}")


# =====================================================================
#   PARTE 4: OPERACIONES MATRICIALES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: OPERACIONES MATRICIALES ===")
print("=" * 80)

print("\n--- Multiplicacion de matrices ---")

"""
C = A @ B  (o np.matmul(A, B))
(m x n) @ (n x p) = (m x p)

REGLA: columnas de A = filas de B.
"""

A = np.array([[1, 2], [3, 4], [5, 6]])  # 3x2
B = np.array([[7, 8, 9], [10, 11, 12]])  # 2x3

C = A @ B  # 3x3
print(f"  A (3x2):\n{A}")
print(f"  B (2x3):\n{B}")
print(f"  A @ B (3x3):\n{C}")

# Verificar manualmente primer elemento
print(f"\n  C[0,0] = 1*7 + 2*10 = {1*7 + 2*10}")
print(f"  C[0,1] = 1*8 + 2*11 = {1*8 + 2*11}")


print("\n--- Transpuesta ---")

M = np.array([[1, 2, 3], [4, 5, 6]])
print(f"  M (2x3):\n{M}")
print(f"  M.T (3x2):\n{M.T}")

# Propiedad: (A @ B).T = B.T @ A.T
D = np.random.randn(2, 3)
E = np.random.randn(3, 4)
assert np.allclose((D @ E).T, E.T @ D.T)
print(f"\n  (A @ B).T == B.T @ A.T: True")


print("\n--- Inversa ---")

"""
A @ A^-1 = I (identidad)
Solo existe para matrices CUADRADAS y SINGULARES (det != 0).
"""

M_sq = np.array([[2.0, 1.0], [1.0, 3.0]])
M_inv = np.linalg.inv(M_sq)

print(f"\n  M:\n{M_sq}")
print(f"  M^-1:\n{M_inv}")
print(f"  M @ M^-1:\n{M_sq @ M_inv}")
print(f"  Es identidad: {np.allclose(M_sq @ M_inv, np.eye(2))}")


print("\n--- Determinante ---")

det = np.linalg.det(M_sq)
print(f"\n  det(M) = {det}")
print(f"  det != 0: matriz es invertible")

# Matriz singular (no invertible)
singular = np.array([[1, 2], [2, 4]])
det_s = np.linalg.det(singular)
print(f"  det([[1,2],[2,4]]) = {det_s:.1f} (singular)")


print("\n--- Traza ---")

traza = np.trace(M_sq)
print(f"\n  trace(M) = {traza} (suma de diagonal)")


# =====================================================================
#   PARTE 5: BROADCASTING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: BROADCASTING ===")
print("=" * 80)

"""
Broadcasting: NumPy expande automaticamente dimensiones para
operar entre arrays de diferentes shapes.

REGLAS:
1. Si ndim difiere, el array menor se expande con dims de 1.
2. Las dims deben ser iguales O una debe ser 1.
3. Se expande la dim de tamaño 1 para coincidir.

EJEMPLO:
  (3, 4) + (4,)     -> (3, 4) + (1, 4) -> OK
  (3, 4) + (3, 1)   -> OK
  (3, 4) + (3,)     -> ERROR (4 != 3)
"""

print("\n--- Escalar + matriz ---")

M = np.ones((2, 3))
print(f"  M + 5:\n{M + 5}")  # (2,3) + () -> broadcasting


print("\n--- Vector + matriz ---")

M = np.array([[1, 2, 3], [4, 5, 6]])  # (2, 3)
v = np.array([10, 20, 30])            # (3,) -> (1, 3) -> (2, 3)

print(f"  M (2x3):\n{M}")
print(f"  v: {v}")
print(f"  M + v:\n{M + v}")


print("\n--- Normalizacion por columna (broadcasting) ---")

# Restar media por columna (muy comun en ML)
datos = np.random.randn(5, 3)  # 5 muestras, 3 features

media = datos.mean(axis=0)   # shape (3,)
std = datos.std(axis=0)      # shape (3,)

normalizado = (datos - media) / std  # Broadcasting!

print(f"  Datos shape: {datos.shape}")
print(f"  Media: {media}")
print(f"  Std: {std}")
print(f"  Media tras norm: {normalizado.mean(axis=0)}")
print(f"  Std tras norm: {normalizado.std(axis=0)}")


print("\n--- Softmax con broadcasting ---")

def softmax(x):
    """Softmax numericamente estable."""
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / e_x.sum(axis=-1, keepdims=True)

logits = np.array([[2.0, 1.0, 0.1],
                    [1.0, 3.0, 0.5]])

probs = softmax(logits)
print(f"\n  Logits:\n{logits}")
print(f"  Softmax:\n{probs}")
print(f"  Suma por fila: {probs.sum(axis=1)}")


# =====================================================================
#   PARTE 6: INDEXACION AVANZADA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: INDEXACION AVANZADA ===")
print("=" * 80)

"""
NumPy soporta indexacion muy flexible:
- Slicing: a[1:3]
- Fancy indexing: a[[0, 2, 4]]
- Boolean indexing: a[a > 0]
- np.where: condiciones
"""

print("\n--- Slicing ---")

M = np.arange(20).reshape(4, 5)
print(f"  M (4x5):\n{M}")
print(f"  M[1:3, 2:4]:\n{M[1:3, 2:4]}")
print(f"  M[:, ::2] (columnas pares):\n{M[:, ::2]}")
print(f"  M[-1] (ultima fila): {M[-1]}")


print("\n--- Boolean indexing ---")

datos = np.random.randn(10)
print(f"\n  datos: {datos}")
print(f"  datos > 0: {datos[datos > 0]}")
print(f"  |datos| > 1: {datos[np.abs(datos) > 1]}")


print("\n--- np.where ---")

x = np.array([1, -2, 3, -4, 5])
resultado = np.where(x > 0, x, 0)  # ReLU!
print(f"\n  x: {x}")
print(f"  ReLU(x) = np.where(x>0, x, 0): {resultado}")


print("\n--- Fancy indexing para embedding lookup ---")

# Simular embedding table
vocab_size = 10
embed_dim = 4
embedding_table = np.random.randn(vocab_size, embed_dim)

# Lookup: obtener embeddings para indices [2, 5, 7]
indices = np.array([2, 5, 7])
embeddings = embedding_table[indices]  # Fancy indexing

print(f"\n  Embedding table: {embedding_table.shape}")
print(f"  Indices: {indices}")
print(f"  Lookup result: {embeddings.shape}")
print(f"  Embedding[2]:\n    {embeddings[0]}")


# =====================================================================
#   PARTE 7: SIMILARIDAD Y DISTANCIAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: SIMILARIDAD COSENO Y DISTANCIAS ===")
print("=" * 80)

"""
Similaridad coseno: mide el angulo entre dos vectores.
cos(a, b) = (a · b) / (||a|| * ||b||)
Rango: [-1, 1]. 1 = identicos, 0 = ortogonales, -1 = opuestos.

EN ML: comparar embeddings, busqueda semantica, recomendaciones.
"""

print("\n--- Similaridad coseno ---")

def cosine_similarity(a, b):
    """Similaridad coseno entre dos vectores."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Simular embeddings de palabras
np.random.seed(42)
emb_rey = np.random.randn(8)
emb_reina = emb_rey + np.random.randn(8) * 0.3  # Similar
emb_gato = np.random.randn(8)  # Diferente

print(f"  cos(rey, reina): {cosine_similarity(emb_rey, emb_reina):.4f}")
print(f"  cos(rey, gato):  {cosine_similarity(emb_rey, emb_gato):.4f}")
print(f"  cos(rey, rey):   {cosine_similarity(emb_rey, emb_rey):.4f}")


print("\n--- Distancia euclidea ---")

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

print(f"  dist(rey, reina): {euclidean_distance(emb_rey, emb_reina):.4f}")
print(f"  dist(rey, gato):  {euclidean_distance(emb_rey, emb_gato):.4f}")


print("\n--- Matriz de similaridad (batch) ---")

# N embeddings, calcular similaridad NxN
n_docs = 5
embed_dim = 8
embeddings = np.random.randn(n_docs, embed_dim)

# Normalizar
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
embeddings_norm = embeddings / norms

# Similaridad coseno: dot product de vectores normalizados
sim_matrix = embeddings_norm @ embeddings_norm.T

print(f"  {n_docs} embeddings de dim {embed_dim}")
print(f"  Matriz de similaridad ({sim_matrix.shape}):")
print(f"{np.array2string(sim_matrix, precision=2, suppress_small=True)}")
print(f"  Diagonal (auto-similaridad): {np.diag(sim_matrix)}")


# =====================================================================
#   PARTE 8: OPERACIONES ESTADISTICAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: OPERACIONES ESTADISTICAS ===")
print("=" * 80)

print("\n--- Estadisticas por eje ---")

datos = np.random.randn(100, 5)  # 100 muestras, 5 features
print(f"  Shape: {datos.shape}")
print(f"  Media por feature:    {datos.mean(axis=0)}")
print(f"  Std por feature:      {datos.std(axis=0)}")
print(f"  Min por feature:      {datos.min(axis=0)}")
print(f"  Max por feature:      {datos.max(axis=0)}")
print(f"  Media global:         {datos.mean():.4f}")

print("\n--- Correlacion ---")

# Matriz de correlacion (muy util en EDA)
corr = np.corrcoef(datos.T)  # Transponer: features como filas
print(f"  Correlacion matrix shape: {corr.shape}")
print(f"  Correlacion features 0-1: {corr[0, 1]:.4f}")
print(f"  Auto-correlacion: {corr[0, 0]:.4f}")


# =====================================================================
#   PARTE 9: EJERCICIO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: EJERCICIO — MOTOR DE BUSQUEDA SEMANTICA ===")
print("=" * 80)

"""
Construir un mini motor de busqueda usando embeddings y
similaridad coseno. Esto es la BASE de RAG.
"""

print("\n--- Mini search engine ---")

class SemanticSearch:
    """Motor de busqueda basado en embeddings."""
    
    def __init__(self, embed_dim: int = 16):
        self.embed_dim = embed_dim
        self.documentos = []
        self.embeddings = None
        self.rng = np.random.RandomState(42)
    
    def _embed(self, texto: str) -> np.ndarray:
        """Embedding simulado (hash-based para reproducibilidad)."""
        np.random.seed(hash(texto) % 2**31)
        return np.random.randn(self.embed_dim)
    
    def indexar(self, documentos: list[str]):
        """Indexar documentos."""
        self.documentos = documentos
        embs = np.array([self._embed(doc) for doc in documentos])
        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        self.embeddings = embs / norms  # Normalizar
        print(f"  Indexados {len(documentos)} documentos ({self.embeddings.shape})")
    
    def buscar(self, query: str, top_k: int = 3) -> list:
        """Buscar documentos similares."""
        q_emb = self._embed(query)
        q_emb = q_emb / np.linalg.norm(q_emb)
        
        # Similaridad coseno: dot con embeddings normalizados
        scores = self.embeddings @ q_emb
        
        # Top-K
        top_idx = np.argsort(scores)[::-1][:top_k]
        
        return [(self.documentos[i], float(scores[i])) for i in top_idx]

search = SemanticSearch(embed_dim=32)

docs = [
    "Python es un lenguaje de programacion",
    "Machine learning usa algoritmos estadisticos",
    "Los transformers revolucionaron NLP",
    "Docker facilita el despliegue",
    "NumPy es la base del calculo numerico",
    "PyTorch implementa redes neuronales",
    "FastAPI sirve modelos en produccion",
    "Los embeddings representan texto como vectores",
]

search.indexar(docs)

queries = ["redes neuronales", "despliegue de modelos", "algebra lineal"]
for q in queries:
    resultados = search.buscar(q, top_k=3)
    print(f"\n  Query: '{q}'")
    for doc, score in resultados:
        print(f"    [{score:.3f}] {doc}")


print("\n" + "=" * 80)
print("=== CAPITULO 10: BENCHMARK NUMPY VS PYTHON ===")
print("=" * 80)

print("\n--- Velocidad de NumPy vs listas ---")

N = 100_000
a_list = list(range(N))
b_list = list(range(N))
a_np = np.arange(N)
b_np = np.arange(N)

# Python puro
start = time.perf_counter()
c_list = [a + b for a, b in zip(a_list, b_list)]
t_python = time.perf_counter() - start

# NumPy
start = time.perf_counter()
c_np = a_np + b_np
t_numpy = time.perf_counter() - start

print(f"  Suma de {N:,} elementos:")
print(f"    Python: {t_python*1000:.2f} ms")
print(f"    NumPy:  {t_numpy*1000:.2f} ms")
if t_numpy > 0:
    print(f"    Speedup: {t_python/t_numpy:.0f}x")

# Dot product
start = time.perf_counter()
dot_py = sum(a * b for a, b in zip(a_list, b_list))
t_dot_py = time.perf_counter() - start

start = time.perf_counter()
dot_np = np.dot(a_np, b_np)
t_dot_np = time.perf_counter() - start

print(f"\n  Dot product de {N:,} elementos:")
print(f"    Python: {t_dot_py*1000:.2f} ms")
print(f"    NumPy:  {t_dot_np*1000:.2f} ms")


print("\n" + "=" * 80)
print("=== CAPITULO 11: PRODUCTOS ESPECIALES ===")
print("=" * 80)

"""
Otros productos importantes en ML.
"""

print("\n--- Hadamard product (elemento a elemento) ---")

"""
a ⊙ b = element-wise multiplication.
EN ML: gating en LSTMs, attention masks.
"""

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
hadamard = a * b  # Elemento a elemento, NO matricial

print(f"  a:\n{a}")
print(f"  b:\n{b}")
print(f"  a ⊙ b (Hadamard):\n{hadamard}")
print(f"  a @ b (Matricial):\n{a @ b}")

# Masking con Hadamard
mask = np.array([[1, 0], [1, 1]])
masked = a * mask
print(f"\n  mask:\n{mask}")
print(f"  a * mask:\n{masked}")


print("\n--- Cross product (producto vectorial) ---")

"""
Solo en 3D: a × b = vector perpendicular a ambos.
||a × b|| = ||a|| ||b|| sin(theta)
"""

a_3d = np.array([1, 0, 0])
b_3d = np.array([0, 1, 0])
cross = np.cross(a_3d, b_3d)

print(f"  a = {a_3d}")
print(f"  b = {b_3d}")
print(f"  a × b = {cross}")
print(f"  Perpendicular a ambos: {np.dot(cross, a_3d)}, {np.dot(cross, b_3d)}")


print("\n" + "=" * 80)
print("=== CAPITULO 12: NORMAS MATRICIALES ===")
print("=" * 80)

"""
Normas para matrices (no solo vectores):
- Frobenius: sqrt(sum(a_ij^2))
- Nuclear: sum(sigma_i) (suma valores singulares)
- Spectral: max(sigma_i) (maximo valor singular)
"""

M = np.array([[1, 2, 3],
               [4, 5, 6]], dtype=float)

frob = np.linalg.norm(M, 'fro')
nuc = np.linalg.norm(M, 'nuc')
spec = np.linalg.norm(M, 2)

print(f"  M:\n{M}")
print(f"  ||M||_F (Frobenius): {frob:.4f}")
print(f"  ||M||_* (Nuclear):   {nuc:.4f}")
print(f"  ||M||_2 (Spectral):  {spec:.4f}")

# Verificar Frobenius
frob_manual = np.sqrt(np.sum(M**2))
print(f"\n  Frobenius manual: {frob_manual:.4f}")
print(f"  Iguales: {np.isclose(frob, frob_manual)}")


print("\n" + "=" * 80)
print("=== CAPITULO 13: RESHAPE, STACKING Y MEMORIA ===")
print("=" * 80)

"""
Manipulacion de forma: reshape, stack, concatenate.
Crucial para preparar datos para modelos.
"""

print("\n--- Reshape ---")

a = np.arange(12)
print(f"  Original: {a} (shape={a.shape})")
print(f"  reshape(3,4):\n{a.reshape(3, 4)}")
print(f"  reshape(2,2,3):\n{a.reshape(2, 2, 3)}")

# -1 para inferir dimension
print(f"  reshape(-1, 3): {a.reshape(-1, 3).shape}")  # (4, 3)
print(f"  reshape(3, -1): {a.reshape(3, -1).shape}")  # (3, 4)


print("\n--- Stack y concatenate ---")

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

vstack = np.vstack([a, b])
hstack = np.hstack([a, b])
stack_0 = np.stack([a, b], axis=0)
stack_1 = np.stack([a, b], axis=1)

print(f"  a = {a}, b = {b}")
print(f"  vstack: {vstack.shape}\n{vstack}")
print(f"  hstack: {hstack.shape} = {hstack}")
print(f"  stack(axis=0): {stack_0.shape}\n{stack_0}")
print(f"  stack(axis=1): {stack_1.shape}\n{stack_1}")


print("\n--- Memory layout: C vs F order ---")

a_c = np.array([[1, 2, 3], [4, 5, 6]], order='C')  # Row-major
a_f = np.array([[1, 2, 3], [4, 5, 6]], order='F')  # Column-major

print(f"  C-order (row-major): {a_c.flags['C_CONTIGUOUS']}")
print(f"  F-order (col-major): {a_f.flags['F_CONTIGUOUS']}")

# Flat iteration
print(f"  C-order flat: {a_c.ravel()}")
print(f"  F-order flat: {a_f.ravel(order='F')}")

# Contiguous memory matters for performance
print(f"\n  C-contiguous es lo que espera NumPy/PyTorch")
print(f"  Usar np.ascontiguousarray() si es necesario")


print("\n" + "=" * 80)
print("=== CAPITULO 14: K-NEAREST NEIGHBORS CON NUMPY ===")
print("=" * 80)

"""
KNN implementado con operaciones vectorizadas de NumPy.
Demuestra como el algebra lineal permite ML eficiente.
"""

print("\n--- KNN desde cero ---")

class KNNClassifier:
    """KNN usando distancia euclidea con NumPy vectorizado."""
    
    def __init__(self, k: int = 3):
        self.k = k
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        self.X_train = X
        self.y_train = y
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        # Calcular distancias: ||a - b||^2 = ||a||^2 + ||b||^2 - 2*a·b
        # Esto es mucho mas rapido que loops
        dists_sq = (
            np.sum(X**2, axis=1, keepdims=True)    # ||a||^2
            + np.sum(self.X_train**2, axis=1)       # ||b||^2
            - 2 * X @ self.X_train.T                # -2*a·b
        )
        
        # K vecinos mas cercanos
        k_nearest = np.argsort(dists_sq, axis=1)[:, :self.k]
        
        # Voto mayoritario
        preds = []
        for neighbors in k_nearest:
            labels = self.y_train[neighbors]
            values, counts = np.unique(labels, return_counts=True)
            preds.append(values[np.argmax(counts)])
        
        return np.array(preds)
    
    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        preds = self.predict(X)
        return np.mean(preds == y)

# Generar datos de 3 clases
np.random.seed(42)
n_per_class = 50
X_train = np.vstack([
    np.random.randn(n_per_class, 2) + [2, 2],
    np.random.randn(n_per_class, 2) + [-2, 2],
    np.random.randn(n_per_class, 2) + [0, -2],
])
y_train = np.array([0]*n_per_class + [1]*n_per_class + [2]*n_per_class)

X_test = np.vstack([
    np.random.randn(20, 2) + [2, 2],
    np.random.randn(20, 2) + [-2, 2],
    np.random.randn(20, 2) + [0, -2],
])
y_test = np.array([0]*20 + [1]*20 + [2]*20)

knn = KNNClassifier(k=5)
knn.fit(X_train, y_train)

acc = knn.score(X_test, y_test)
print(f"  KNN (k=5) accuracy: {acc:.4f}")

# Probar diferentes k
for k in [1, 3, 5, 7, 11]:
    knn_k = KNNClassifier(k=k)
    knn_k.fit(X_train, y_train)
    acc_k = knn_k.score(X_test, y_test)
    print(f"  k={k:2d}: accuracy={acc_k:.4f}")


print("\n" + "=" * 80)
print("=== CAPITULO 15: EINSUM ===")
print("=" * 80)

"""
np.einsum: notacion Einstein para operaciones tensoriales.
Permite expresar operaciones complejas de forma concisa.
"""

print("\n--- Einsum basico ---")

# Dot product: i,i -> (suma sobre i)
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
dot_ein = np.einsum('i,i->', a, b)
print(f"  dot(a,b) einsum: {dot_ein}")

# Matrix multiply: ij,jk -> ik
A = np.random.randn(3, 4)
B = np.random.randn(4, 5)
C_ein = np.einsum('ij,jk->ik', A, B)
print(f"  matmul einsum: {np.allclose(C_ein, A @ B)}")

# Trace: ii ->
M = np.random.randn(4, 4)
trace_ein = np.einsum('ii->', M)
print(f"  trace einsum: {trace_ein:.4f} == {np.trace(M):.4f}")

# Batch dot product: bi,bi -> b
batch_a = np.random.randn(10, 8)
batch_b = np.random.randn(10, 8)
batch_dot = np.einsum('bi,bi->b', batch_a, batch_b)
print(f"  batch dot product shape: {batch_dot.shape}")

# Attention: (batch, seq, dim) @ (batch, dim, seq) -> (batch, seq, seq)
Q = np.random.randn(2, 5, 8)
K = np.random.randn(2, 5, 8)
scores_ein = np.einsum('bsd,btd->bst', Q, K)
print(f"  attention scores einsum: {scores_ein.shape}")


print("\n" + "=" * 80)
print("=== CAPITULO 16: MATRICES DISPERSAS ===")
print("=" * 80)

"""
Sparse matrices: la mayoria de elementos son 0.
EN ML: TF-IDF, one-hot encoding, grafos grandes.
Almacenar solo los no-ceros ahorra memoria.
"""

print("\n--- Sparse vs Dense ---")

from scipy import sparse

# Crear matriz dispersa
n = 1000
density = 0.01  # Solo 1% de elementos no-ceros
data = np.random.randn(int(n * n * density))
rows = np.random.randint(0, n, int(n * n * density))
cols = np.random.randint(0, n, int(n * n * density))

sp = sparse.csr_matrix((data, (rows, cols)), shape=(n, n))
dense = sp.toarray()

print(f"  Matriz {n}x{n}, densidad={density}")
print(f"  Dense: {dense.nbytes:,} bytes")
print(f"  Sparse: ~{sp.data.nbytes + sp.indices.nbytes + sp.indptr.nbytes:,} bytes")
print(f"  No-ceros: {sp.nnz:,} de {n*n:,}")

# Operacion sparse vs dense
v = np.random.randn(n)

start = time.perf_counter()
r_dense = dense @ v
t_dense = time.perf_counter() - start

start = time.perf_counter()
r_sparse = sp @ v
t_sparse = time.perf_counter() - start

print(f"\n  Multiplicacion matrix-vector:")
print(f"    Dense:  {t_dense*1000:.2f} ms")
print(f"    Sparse: {t_sparse*1000:.2f} ms")
print(f"    Resultados iguales: {np.allclose(r_dense, r_sparse)}")


print("\n--- TF-IDF como matriz dispersa ---")

# Simular TF-IDF: vocab=5000, docs=100, la mayoria de palabras no aparecen
vocab_size = 5000
n_docs = 100
# Cada doc tiene ~50 palabras unicas
tfidf_data = []
tfidf_rows = []
tfidf_cols = []

np.random.seed(42)
for doc_id in range(n_docs):
    n_words = np.random.randint(30, 80)
    word_ids = np.random.choice(vocab_size, n_words, replace=False)
    values = np.random.uniform(0.1, 1.0, n_words)
    tfidf_data.extend(values)
    tfidf_rows.extend([doc_id] * n_words)
    tfidf_cols.extend(word_ids)

tfidf = sparse.csr_matrix(
    (tfidf_data, (tfidf_rows, tfidf_cols)),
    shape=(n_docs, vocab_size)
)

print(f"  TF-IDF matrix: {tfidf.shape}")
print(f"  Non-zeros: {tfidf.nnz:,} de {n_docs * vocab_size:,}")
print(f"  Densidad: {tfidf.nnz / (n_docs * vocab_size):.4f}")
print(f"  Memoria sparse: ~{tfidf.data.nbytes // 1024} KB")
print(f"  Memoria dense:  ~{n_docs * vocab_size * 8 // 1024} KB")


print("\n" + "=" * 80)
print("=== CAPITULO 17: PAIRWISE DISTANCE MATRIX ===")
print("=" * 80)

"""
Calcular todas las distancias entre N puntos.
Fundamental en clustering (K-means), KNN, DBSCAN.
"""

print("\n--- Distancia pairwise vectorizada ---")

def pairwise_distances(X):
    """Distancia euclidea entre todos los pares. O(N^2)."""
    # ||a - b||^2 = ||a||^2 + ||b||^2 - 2*a·b
    sq_norms = np.sum(X**2, axis=1)
    dists_sq = sq_norms[:, None] + sq_norms[None, :] - 2 * X @ X.T
    # Corregir posibles negativos por precision numerica
    dists_sq = np.maximum(dists_sq, 0)
    return np.sqrt(dists_sq)

np.random.seed(42)
X_dist = np.random.randn(100, 10)

start = time.perf_counter()
D = pairwise_distances(X_dist)
t_vec = time.perf_counter() - start

print(f"  {X_dist.shape[0]} puntos en {X_dist.shape[1]}D")
print(f"  Matriz de distancias: {D.shape}")
print(f"  Tiempo: {t_vec*1000:.2f} ms")
print(f"  D[0,0] = {D[0,0]:.4f} (auto-distancia)")
print(f"  D[0,1] = {D[0,1]:.4f}")
print(f"  Simetrica: {np.allclose(D, D.T)}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE VECTORES Y MATRICES:

1. Escalar -> Vector -> Matriz -> Tensor. ML usa todos.

2. NumPy: creacion eficiente con zeros, ones, randn, arange.

3. Producto punto: a @ b. Base de similaridad coseno.

4. Normas vectoriales y matriciales (Frobenius, spectral).

5. Multiplicacion matricial: (m,n) @ (n,p) = (m,p).

6. Broadcasting: reglas para operar arrays diferentes.

7. Indexacion: slicing, boolean, fancy. Embedding lookup.

8. Similaridad coseno: base de busqueda semantica y RAG.

9. einsum: notacion Einstein para operaciones tensoriales.

10. KNN vectorizado: distancias sin loops.

11. Sparse matrices: TF-IDF, one-hot, grafos.

12. Pairwise distances: base de clustering.

Siguiente archivo: Transformaciones y sistemas de ecuaciones.
"""

print("\n FIN DE ARCHIVO 01_vectores_y_matrices.")
print(" Vectores y matrices han sido dominados.")
