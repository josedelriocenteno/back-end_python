# ===========================================================================
# 02_transformaciones_y_sistemas.py
# ===========================================================================
# MODULO 07: ALGEBRA LINEAL CON PYTHON
# ARCHIVO 02: Transformaciones Lineales y Sistemas de Ecuaciones
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar transformaciones lineales, sistemas de ecuaciones,
# proyecciones, y sus aplicaciones directas en ML/IA.
#
# CONTENIDO:
#   1. Transformaciones lineales: concepto geometrico.
#   2. Rotaciones, escalado, reflexiones.
#   3. Sistemas de ecuaciones: Ax = b.
#   4. Minimos cuadrados (OLS).
#   5. Proyecciones y subespacios.
#   6. Rango, espacio nulo, independencia lineal.
#   7. Aplicaciones: regresion lineal, PCA geometrico.
#   8. Ejercicio: regresion lineal desde cero.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: TRANSFORMACIONES LINEALES
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: TRANSFORMACIONES LINEALES ===")
print("=" * 80)

"""
Una transformacion lineal T: R^n -> R^m cumple:
  T(a + b) = T(a) + T(b)
  T(c * a) = c * T(a)

TODA transformacion lineal se puede representar como una MATRIZ.
T(x) = A @ x

EN ML: una capa lineal (nn.Linear) ES una transformacion lineal.
y = W @ x + b
"""

print("\n--- Transformacion como multiplicacion matricial ---")

# Transformacion: R^2 -> R^2
A = np.array([[2, 0],
               [0, 3]])

# Aplicar a vector
x = np.array([1, 1])
y = A @ x

print(f"  A = {A.tolist()}")
print(f"  x = {x}")
print(f"  T(x) = A @ x = {y}")
print(f"  Efecto: escala x por 2, y por 3")


print("\n--- Transformacion: R^3 -> R^2 (reduccion de dimension) ---")

W = np.array([[1, 0, 0.5],
               [0, 1, -0.5]])  # 2x3

x_3d = np.array([1, 2, 3])
x_2d = W @ x_3d

print(f"  W (2x3):\n{W}")
print(f"  x (3D): {x_3d}")
print(f"  W @ x (2D): {x_2d}")
print(f"  Dimension: {x_3d.shape[0]} -> {x_2d.shape[0]}")


# =====================================================================
#   PARTE 2: ROTACIONES Y TRANSFORMACIONES GEOMETRICAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: ROTACIONES, ESCALADO, REFLEXIONES ===")
print("=" * 80)

print("\n--- Rotacion 2D ---")

"""
Rotacion por angulo theta:
R = [[cos(t), -sin(t)],
     [sin(t),  cos(t)]]
"""

def rotation_matrix(theta_degrees):
    """Crea matriz de rotacion 2D."""
    theta = np.radians(theta_degrees)
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

punto = np.array([1.0, 0.0])

for angulo in [0, 45, 90, 180, 270]:
    R = rotation_matrix(angulo)
    rotado = R @ punto
    print(f"  Rotar {angulo}°: {punto} -> [{rotado[0]:.2f}, {rotado[1]:.2f}]")


print("\n--- Escalado ---")

def scale_matrix(sx, sy):
    return np.array([[sx, 0], [0, sy]])

S = scale_matrix(2, 0.5)
punto = np.array([1.0, 1.0])
escalado = S @ punto
print(f"\n  S = {S.tolist()}")
print(f"  {punto} -> {escalado}")


print("\n--- Reflexion ---")

# Reflexion respecto al eje X
Rx = np.array([[1, 0], [0, -1]])
# Reflexion respecto al eje Y
Ry = np.array([[-1, 0], [0, 1]])

punto = np.array([3.0, 4.0])
print(f"\n  Punto: {punto}")
print(f"  Reflexion eje X: {Rx @ punto}")
print(f"  Reflexion eje Y: {Ry @ punto}")


print("\n--- Composicion de transformaciones ---")

"""
Componer = multiplicar matrices.
Primero rotar 45°, luego escalar 2x.
T = S @ R  (nota: se lee de derecha a izquierda)
"""

R = rotation_matrix(45)
S = scale_matrix(2, 2)

T = S @ R  # Primero R, luego S
punto = np.array([1.0, 0.0])
resultado = T @ punto

print(f"\n  Rotar 45° y escalar 2x:")
print(f"  {punto} -> [{resultado[0]:.3f}, {resultado[1]:.3f}]")

# Verificar: el orden importa
T2 = R @ S
resultado2 = T2 @ punto
print(f"  Escalar 2x y rotar 45° (orden inverso):")
print(f"  {punto} -> [{resultado2[0]:.3f}, {resultado2[1]:.3f}]")
print(f"  Son diferentes: {not np.allclose(resultado, resultado2)}")


# =====================================================================
#   PARTE 3: SISTEMAS DE ECUACIONES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: SISTEMAS DE ECUACIONES (Ax = b) ===")
print("=" * 80)

"""
Sistema de ecuaciones lineales:
  2x + y = 5
  x + 3y = 7

En forma matricial: A @ x = b
  A = [[2, 1], [1, 3]]
  b = [5, 7]
  x = ?
"""

print("\n--- Resolver sistema ---")

A = np.array([[2, 1], [1, 3]], dtype=float)
b = np.array([5, 7], dtype=float)

x = np.linalg.solve(A, b)
print(f"  A:\n{A}")
print(f"  b: {b}")
print(f"  x = solve(A, b) = {x}")

# Verificar
residuo = A @ x - b
print(f"  Verificar: A @ x - b = {residuo}")
print(f"  ||residuo|| = {np.linalg.norm(residuo):.1e}")


print("\n--- Sistema 3x3 ---")

"""
x + 2y + 3z = 14
4x + 5y + 6z = 32
7x + 8y + 10z = 53
"""

A3 = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 10]], dtype=float)
b3 = np.array([14, 32, 53], dtype=float)

x3 = np.linalg.solve(A3, b3)
print(f"  Solucion: x={x3[0]:.1f}, y={x3[1]:.1f}, z={x3[2]:.1f}")
print(f"  Verificar: ||A@x - b|| = {np.linalg.norm(A3 @ x3 - b3):.1e}")

# Condicion del sistema
cond = np.linalg.cond(A3)
print(f"  Numero de condicion: {cond:.1f}")
print(f"  {'Bien condicionado' if cond < 100 else 'Mal condicionado'}")


# =====================================================================
#   PARTE 4: MINIMOS CUADRADOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: MINIMOS CUADRADOS (OLS) ===")
print("=" * 80)

"""
Cuando hay MAS ecuaciones que incognitas (sobredeterminado),
no hay solucion exacta. Buscamos x que minimiza ||Ax - b||^2.

Solucion: x = (A^T A)^-1 A^T b  (ecuaciones normales)

!!! ESTO ES REGRESION LINEAL !!!
"""

print("\n--- Regresion lineal = minimos cuadrados ---")

# Datos: y = 2x + 1 + ruido
np.random.seed(42)
n = 50
x_data = np.random.uniform(0, 10, n)
y_data = 2 * x_data + 1 + np.random.randn(n) * 0.5

# Construir matriz A (con columna de 1s para intercepto)
A = np.column_stack([x_data, np.ones(n)])  # (50, 2)

# Resolver por ecuaciones normales
# x = (A^T A)^-1 A^T b
ATA = A.T @ A
ATb = A.T @ y_data
params = np.linalg.solve(ATA, ATb)

print(f"  Datos: {n} puntos")
print(f"  Pendiente real: 2.0, estimada: {params[0]:.4f}")
print(f"  Intercepto real: 1.0, estimado: {params[1]:.4f}")

# Verificar con np.linalg.lstsq
params_lstsq, residuals, rank, sv = np.linalg.lstsq(A, y_data, rcond=None)
print(f"\n  lstsq: pendiente={params_lstsq[0]:.4f}, intercepto={params_lstsq[1]:.4f}")
print(f"  Son iguales: {np.allclose(params, params_lstsq)}")


print("\n--- Regresion polinomial ---")

# y = 0.5x^2 - 2x + 3 + ruido
y_poly = 0.5 * x_data**2 - 2 * x_data + 3 + np.random.randn(n) * 1.0

# Matriz con x^0, x^1, x^2
A_poly = np.column_stack([x_data**2, x_data, np.ones(n)])

params_poly = np.linalg.lstsq(A_poly, y_poly, rcond=None)[0]
print(f"  Coeficientes reales: [0.5, -2.0, 3.0]")
print(f"  Coeficientes estimados: [{params_poly[0]:.3f}, {params_poly[1]:.3f}, {params_poly[2]:.3f}]")

# R^2
y_pred = A_poly @ params_poly
ss_res = np.sum((y_poly - y_pred)**2)
ss_tot = np.sum((y_poly - np.mean(y_poly))**2)
r2 = 1 - ss_res / ss_tot
print(f"  R² = {r2:.4f}")


# =====================================================================
#   PARTE 5: PROYECCIONES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: PROYECCIONES ===")
print("=" * 80)

"""
Proyeccion de b sobre a:
  proj_a(b) = (a · b / a · a) * a

EN ML: PCA es una proyeccion sobre los componentes principales.
"""

print("\n--- Proyeccion sobre un vector ---")

a = np.array([1.0, 0.0])
b = np.array([3.0, 4.0])

# Proyeccion de b sobre a
proj = (np.dot(a, b) / np.dot(a, a)) * a
print(f"  a = {a}")
print(f"  b = {b}")
print(f"  proj_a(b) = {proj}")

# Componente perpendicular
perp = b - proj
print(f"  Componente perp = {perp}")
print(f"  Verificar ortogonalidad: a · perp = {np.dot(a, perp):.1e}")


print("\n--- Proyeccion sobre un subespacio ---")

"""
Proyeccion de b sobre un subespacio definido por columnas de A:
  P = A @ (A^T A)^-1 @ A^T
  proj = P @ b
"""

A_sub = np.array([[1, 0],
                    [0, 1],
                    [0, 0]], dtype=float)  # Plano xy en R^3

b_3d = np.array([3.0, 4.0, 5.0])

P = A_sub @ np.linalg.inv(A_sub.T @ A_sub) @ A_sub.T
proj_3d = P @ b_3d

print(f"\n  b = {b_3d}")
print(f"  Proyeccion al plano xy: {proj_3d}")


# =====================================================================
#   PARTE 6: RANGO E INDEPENDENCIA LINEAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: RANGO, ESPACIO NULO, INDEPENDENCIA LINEAL ===")
print("=" * 80)

"""
Rango: numero de filas/columnas linealmente independientes.
Determina:
- Si un sistema tiene solucion unica (rango = n).
- Si una transformacion pierde informacion (rango < n).

EN ML: rango de la matriz de features indica features redundantes.
"""

print("\n--- Rango ---")

M1 = np.array([[1, 2],
                [3, 6]])  # Fila 2 = 3 * fila 1

M2 = np.array([[1, 2],
                [3, 4]])  # Independientes

print(f"  M1:\n{M1}")
print(f"  rank(M1) = {np.linalg.matrix_rank(M1)}")

print(f"\n  M2:\n{M2}")
print(f"  rank(M2) = {np.linalg.matrix_rank(M2)}")

# Rango de una matriz de features
np.random.seed(42)
features = np.random.randn(100, 5)  # 5 features independientes
features_dep = np.column_stack([features, features[:, 0] + features[:, 1]])

print(f"\n  {features.shape}: rank = {np.linalg.matrix_rank(features)}")
print(f"  {features_dep.shape}: rank = {np.linalg.matrix_rank(features_dep)}")
print(f"  (6ta columna = col0 + col1 -> dependiente)")


print("\n--- Espacio nulo ---")

"""
Espacio nulo de A: todos los x tales que A @ x = 0.
Si el espacio nulo es {0}, las columnas son independientes.
"""

M_singular = np.array([[1, 2, 3],
                         [4, 5, 6],
                         [7, 8, 9]], dtype=float)

# SVD para encontrar espacio nulo
U, S, Vt = np.linalg.svd(M_singular)
null_mask = S < 1e-10
null_space = Vt[null_mask]

print(f"\n  M (singular):\n{M_singular}")
print(f"  Valores singulares: {S}")
print(f"  rank = {np.sum(S > 1e-10)}")
if null_space.size > 0:
    print(f"  Espacio nulo (dimension {null_space.shape[0]}):")
    for v in null_space:
        print(f"    {v}")
        print(f"    Verificar: M @ v = {M_singular @ v}")


# =====================================================================
#   PARTE 7: APLICACIONES ML
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: APLICACIONES EN ML ===")
print("=" * 80)

print("\n--- Capa lineal (nn.Linear) ---")

"""
Una capa lineal de red neuronal:
  y = W @ x + b

Donde:
  W: (output_dim, input_dim) - pesos
  b: (output_dim,) - bias
  x: (input_dim,) - entrada
  y: (output_dim,) - salida
"""

input_dim = 768    # BERT embedding size
output_dim = 128   # Reduced dimension

W = np.random.randn(output_dim, input_dim) * 0.01
b = np.zeros(output_dim)

x_input = np.random.randn(input_dim)
y_output = W @ x_input + b

print(f"  Linear layer: {input_dim} -> {output_dim}")
print(f"  W shape: {W.shape}")
print(f"  Input shape: {x_input.shape}")
print(f"  Output shape: {y_output.shape}")
print(f"  Parametros: {W.size + b.size:,}")


print("\n--- Batch processing ---")

batch_size = 32
X_batch = np.random.randn(batch_size, input_dim)

# (batch, input) @ (input, output) = (batch, output)
Y_batch = X_batch @ W.T + b  # Nota: W.T porque x esta en filas

print(f"\n  Batch processing:")
print(f"  Input: {X_batch.shape}")
print(f"  Output: {Y_batch.shape}")


print("\n--- Attention score (simplificado) ---")

"""
Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V

Q, K, V: (seq_len, d_model)
"""

seq_len = 10
d_model = 64

Q = np.random.randn(seq_len, d_model)
K = np.random.randn(seq_len, d_model)
V = np.random.randn(seq_len, d_model)

# Attention scores
scores = Q @ K.T / np.sqrt(d_model)  # (seq, seq)

# Softmax
def softmax(x):
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / e_x.sum(axis=-1, keepdims=True)

attention_weights = softmax(scores)
output = attention_weights @ V  # (seq, d_model)

print(f"\n  Attention simplificado:")
print(f"    Q, K, V: ({seq_len}, {d_model})")
print(f"    Scores: {scores.shape}")
print(f"    Weights: {attention_weights.shape}")
print(f"    Output: {output.shape}")
print(f"    Weights sum per row: {attention_weights.sum(axis=1)[:3]}...")


# =====================================================================
#   PARTE 8: EJERCICIO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: EJERCICIO — REGRESION LINEAL DESDE CERO ===")
print("=" * 80)

"""
Implementar regresion lineal usando solo NumPy.
"""

class LinearRegression:
    """Regresion lineal con ecuaciones normales."""
    
    def __init__(self):
        self.weights = None
        self.bias = None
    
    def fit(self, X, y):
        n, d = X.shape
        # Agregar columna de 1s
        X_aug = np.column_stack([X, np.ones(n)])
        # Ecuaciones normales: (X^T X)^-1 X^T y
        params = np.linalg.lstsq(X_aug, y, rcond=None)[0]
        self.weights = params[:-1]
        self.bias = params[-1]
    
    def predict(self, X):
        return X @ self.weights + self.bias
    
    def score(self, X, y):
        """R^2 score."""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        return 1 - ss_res / ss_tot

# Generar datos
np.random.seed(42)
n_samples = 200
n_features = 3

X = np.random.randn(n_samples, n_features)
true_weights = np.array([2.0, -1.0, 0.5])
true_bias = 3.0
y = X @ true_weights + true_bias + np.random.randn(n_samples) * 0.2

# Entrenar
model = LinearRegression()
model.fit(X, y)

print(f"  Pesos reales:    {true_weights}")
print(f"  Pesos estimados: {model.weights}")
print(f"  Bias real: {true_bias}")
print(f"  Bias estimado: {model.bias:.4f}")
print(f"  R²: {model.score(X, y):.6f}")

# Test set
X_test = np.random.randn(50, n_features)
y_test = X_test @ true_weights + true_bias + np.random.randn(50) * 0.2
print(f"  R² test: {model.score(X_test, y_test):.6f}")


print("\n" + "=" * 80)
print("=== CAPITULO 9: FACTORIZACIONES LU Y QR ===")
print("=" * 80)

"""
LU: A = L @ U (triangular inferior x superior)
QR: A = Q @ R (ortogonal x triangular superior)

LU: resolver multiples sistemas con la misma A.
QR: base de minimos cuadrados (mas estable que ecuaciones normales).
"""

print("\n--- Factorizacion LU ---")

from scipy.linalg import lu

A_lu = np.array([[2, 1, 1],
                   [4, 3, 3],
                   [8, 7, 9]], dtype=float)

P, L, U = lu(A_lu)

print(f"  A:\n{A_lu}")
print(f"  L (triangular inferior):\n{L}")
print(f"  U (triangular superior):\n{U}")
print(f"  P @ L @ U == A: {np.allclose(P @ L @ U, A_lu)}")


print("\n--- Factorizacion QR ---")

A_qr = np.array([[1, 1],
                   [1, 2],
                   [1, 3]], dtype=float)

Q, R = np.linalg.qr(A_qr)

print(f"\n  A (3x2):\n{A_qr}")
print(f"  Q (ortogonal):\n{Q}")
print(f"  R (triangular):\n{R}")
print(f"  Q @ R == A: {np.allclose(Q @ R, A_qr)}")
print(f"  Q^T @ Q == I: {np.allclose(Q.T @ Q, np.eye(2))}")

# Minimos cuadrados via QR (mas estable)
b_qr = np.array([1, 3, 5], dtype=float)
x_qr = np.linalg.solve(R, Q.T @ b_qr)
x_lstsq = np.linalg.lstsq(A_qr, b_qr, rcond=None)[0]
print(f"\n  Solucion QR:    {x_qr}")
print(f"  Solucion lstsq: {x_lstsq}")
print(f"  Iguales: {np.allclose(x_qr, x_lstsq)}")


print("\n" + "=" * 80)
print("=== CAPITULO 10: GRAM-SCHMIDT ===")
print("=" * 80)

"""
Gram-Schmidt: crear una base ortonormal a partir de vectores.
Base de QR decomposition.
"""

print("\n--- Gram-Schmidt desde cero ---")

def gram_schmidt(V):
    """Ortogonalizar columnas de V."""
    n, k = V.shape
    U = np.zeros_like(V, dtype=float)
    
    for i in range(k):
        u = V[:, i].copy().astype(float)
        for j in range(i):
            # Restar proyeccion
            u -= np.dot(U[:, j], V[:, i]) * U[:, j]
        # Normalizar
        norm = np.linalg.norm(u)
        if norm > 1e-10:
            U[:, i] = u / norm
    
    return U

V = np.array([[1, 1],
               [1, 0],
               [0, 1]], dtype=float)

Q_gs = gram_schmidt(V)
print(f"  Vectores originales:\n{V}")
print(f"  Base ortonormal:\n{Q_gs}")
print(f"  Q^T @ Q:\n{Q_gs.T @ Q_gs}")
print(f"  Ortogonal: {np.allclose(Q_gs.T @ Q_gs, np.eye(2))}")


print("\n" + "=" * 80)
print("=== CAPITULO 11: DESCENSO DE GRADIENTE ===")
print("=" * 80)

"""
Alternativa a ecuaciones normales: descenso de gradiente.
Minimizar loss = ||X @ w - y||^2

Gradiente: dL/dw = 2 * X^T @ (X @ w - y) / n

EN ML: TODA optimizacion es descenso de gradiente.
"""

print("\n--- Regresion lineal con gradient descent ---")

class LinearRegressionGD:
    """Regresion lineal con descenso de gradiente."""
    
    def __init__(self, lr=0.01, epochs=100):
        self.lr = lr
        self.epochs = epochs
        self.weights = None
        self.bias = None
        self.loss_history = []
    
    def fit(self, X, y):
        n, d = X.shape
        self.weights = np.zeros(d)
        self.bias = 0.0
        
        for epoch in range(self.epochs):
            # Forward pass
            y_pred = X @ self.weights + self.bias
            
            # Loss (MSE)
            loss = np.mean((y_pred - y) ** 2)
            self.loss_history.append(loss)
            
            # Gradientes
            error = y_pred - y
            dw = (2 / n) * X.T @ error
            db = (2 / n) * np.sum(error)
            
            # Update
            self.weights -= self.lr * dw
            self.bias -= self.lr * db
    
    def predict(self, X):
        return X @ self.weights + self.bias

# Entrenar con GD
model_gd = LinearRegressionGD(lr=0.01, epochs=200)
model_gd.fit(X, y)

print(f"  Pesos reales:    {true_weights}")
print(f"  Pesos GD:        {model_gd.weights}")
print(f"  Bias real: {true_bias}, GD: {model_gd.bias:.4f}")
print(f"  Loss final: {model_gd.loss_history[-1]:.6f}")
print(f"  Loss inicial: {model_gd.loss_history[0]:.4f}")
print(f"  Reduccion: {model_gd.loss_history[0] / model_gd.loss_history[-1]:.0f}x")


print("\n" + "=" * 80)
print("=== CAPITULO 12: RIDGE REGRESSION ===")
print("=" * 80)

"""
Ridge: regresion lineal con regularizacion L2.
Minimiza: ||X @ w - y||^2 + alpha * ||w||^2

Solucion: w = (X^T X + alpha * I)^-1 X^T y

Previene overfitting cuando features > samples o hay
multicolinealidad.
"""

print("\n--- Ridge Regression ---")

class RidgeRegression:
    """Ridge regression con solucion cerrada."""
    
    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
    
    def fit(self, X, y):
        n, d = X.shape
        X_aug = np.column_stack([X, np.ones(n)])
        # Regularizacion (no regularizar bias)
        I = np.eye(d + 1)
        I[-1, -1] = 0  # No regularizar bias
        
        params = np.linalg.solve(
            X_aug.T @ X_aug + self.alpha * I,
            X_aug.T @ y
        )
        self.weights = params[:-1]
        self.bias = params[-1]
    
    def predict(self, X):
        return X @ self.weights + self.bias
    
    def score(self, X, y):
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        return 1 - ss_res / ss_tot

# Comparar OLS vs Ridge con diferentes alpha
print(f"\n  OLS weights:   {model.weights}")
print(f"  OLS ||w||²:    {np.sum(model.weights**2):.4f}")

for alpha in [0.01, 0.1, 1.0, 10.0]:
    ridge = RidgeRegression(alpha=alpha)
    ridge.fit(X, y)
    r2 = ridge.score(X_test, y_test)
    w_norm = np.sum(ridge.weights**2)
    print(f"  Ridge(α={alpha:5.2f}): R²={r2:.6f}, ||w||²={w_norm:.4f}")


print("\n" + "=" * 80)
print("=== CAPITULO 13: MULTI-HEAD ATTENTION COMPLETO ===")
print("=" * 80)

"""
Multi-Head Attention como operaciones de algebra lineal.
"""

print("\n--- Multi-Head Attention ---")

def multi_head_attention(Q, K, V, n_heads):
    """Multi-head attention con splits."""
    batch, seq_len, d_model = Q.shape
    d_head = d_model // n_heads
    
    # Split heads: (batch, seq, d_model) -> (batch, n_heads, seq, d_head)
    Q_h = Q.reshape(batch, seq_len, n_heads, d_head).transpose(0, 2, 1, 3)
    K_h = K.reshape(batch, seq_len, n_heads, d_head).transpose(0, 2, 1, 3)
    V_h = V.reshape(batch, seq_len, n_heads, d_head).transpose(0, 2, 1, 3)
    
    # Scaled dot-product attention per head
    scores = Q_h @ K_h.transpose(0, 1, 3, 2) / np.sqrt(d_head)
    
    # Softmax
    exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    weights = exp_scores / exp_scores.sum(axis=-1, keepdims=True)
    
    # Weighted sum of values
    out = weights @ V_h  # (batch, n_heads, seq, d_head)
    
    # Concatenate heads
    out = out.transpose(0, 2, 1, 3).reshape(batch, seq_len, d_model)
    
    return out, weights

# Test
batch, seq_len, d_model = 2, 8, 64
n_heads = 4

Q = np.random.randn(batch, seq_len, d_model)
K = np.random.randn(batch, seq_len, d_model)
V = np.random.randn(batch, seq_len, d_model)

out, attn = multi_head_attention(Q, K, V, n_heads)

print(f"  Input: Q,K,V = ({batch}, {seq_len}, {d_model})")
print(f"  Heads: {n_heads}, d_head: {d_model // n_heads}")
print(f"  Output: {out.shape}")
print(f"  Attention: {attn.shape}")
print(f"  Weights sum: {attn[0, 0, 0].sum():.4f}")


print("\n" + "=" * 80)
print("=== CAPITULO 14: REGRESION LOGISTICA ===")
print("=" * 80)

"""
Logistic regression: clasificacion binaria con algebra lineal.
P(y=1|x) = sigmoid(W @ x + b)
Loss: binary cross-entropy.
"""

print("\n--- Logistic Regression desde cero ---")

def sigmoid(z):
    """Sigmoid numericamente estable."""
    return np.where(z >= 0,
                     1 / (1 + np.exp(-z)),
                     np.exp(z) / (1 + np.exp(z)))

class LogisticRegression:
    """Regresion logistica con gradient descent."""
    
    def __init__(self, lr=0.01, epochs=200):
        self.lr = lr
        self.epochs = epochs
    
    def fit(self, X, y):
        n, d = X.shape
        self.weights = np.zeros(d)
        self.bias = 0.0
        self.loss_history = []
        
        for epoch in range(self.epochs):
            # Forward
            z = X @ self.weights + self.bias
            y_hat = sigmoid(z)
            
            # Binary cross-entropy
            eps = 1e-15
            loss = -np.mean(y * np.log(y_hat + eps) + (1 - y) * np.log(1 - y_hat + eps))
            self.loss_history.append(loss)
            
            # Gradientes
            error = y_hat - y
            dw = (1 / n) * X.T @ error
            db = (1 / n) * np.sum(error)
            
            self.weights -= self.lr * dw
            self.bias -= self.lr * db
    
    def predict_proba(self, X):
        return sigmoid(X @ self.weights + self.bias)
    
    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)
    
    def accuracy(self, X, y):
        return np.mean(self.predict(X) == y)

# Datos binarios
np.random.seed(42)
n_samples = 200
X_bin = np.random.randn(n_samples, 2)
y_bin = (X_bin[:, 0] + X_bin[:, 1] + np.random.randn(n_samples) * 0.3 > 0).astype(float)

log_reg = LogisticRegression(lr=0.1, epochs=300)
log_reg.fit(X_bin, y_bin)

print(f"  Weights: {log_reg.weights}")
print(f"  Bias: {log_reg.bias:.4f}")
print(f"  Accuracy: {log_reg.accuracy(X_bin, y_bin):.4f}")
print(f"  Loss final: {log_reg.loss_history[-1]:.4f}")
print(f"  Loss reduccion: {log_reg.loss_history[0]:.4f} -> {log_reg.loss_history[-1]:.4f}")


print("\n" + "=" * 80)
print("=== CAPITULO 15: SGD CON MOMENTUM ===")
print("=" * 80)

"""
Momentum: acumular velocidad para acelerar convergencia.
v = beta * v + (1 - beta) * gradient
w = w - lr * v

EN ML: Adam, RMSprop, AdaGrad todos usan variantes.
"""

print("\n--- SGD con Momentum ---")

class SGDMomentum:
    """Optimizador SGD con momentum."""
    
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.velocity_w = None
        self.velocity_b = None
    
    def step(self, weights, bias, dw, db):
        if self.velocity_w is None:
            self.velocity_w = np.zeros_like(weights)
            self.velocity_b = 0.0
        
        self.velocity_w = self.momentum * self.velocity_w + (1 - self.momentum) * dw
        self.velocity_b = self.momentum * self.velocity_b + (1 - self.momentum) * db
        
        weights -= self.lr * self.velocity_w
        bias -= self.lr * self.velocity_b
        
        return weights, bias

# Comparar SGD vs SGD+Momentum
def train_linear(X, y, optimizer, epochs=100):
    n, d = X.shape
    w = np.zeros(d)
    b = 0.0
    losses = []
    
    for epoch in range(epochs):
        y_pred = X @ w + b
        loss = np.mean((y_pred - y) ** 2)
        losses.append(loss)
        
        error = y_pred - y
        dw = (2 / n) * X.T @ error
        db = (2 / n) * np.sum(error)
        
        w, b = optimizer.step(w, b, dw, db)
    
    return losses

sgd = SGDMomentum(lr=0.01, momentum=0.0)
sgd_mom = SGDMomentum(lr=0.01, momentum=0.9)

losses_sgd = train_linear(X, y, sgd, epochs=200)
losses_mom = train_linear(X, y, sgd_mom, epochs=200)

print(f"  SGD      loss (epoch 200): {losses_sgd[-1]:.6f}")
print(f"  Momentum loss (epoch 200): {losses_mom[-1]:.6f}")
print(f"  Mejora: {losses_sgd[-1] / max(losses_mom[-1], 1e-10):.1f}x")


print("\n" + "=" * 80)
print("=== CAPITULO 16: ESTABILIDAD NUMERICA ===")
print("=" * 80)

"""
Errores numericos comunes y como evitarlos.
"""

print("\n--- Log-sum-exp trick ---")

# Problema: softmax overflow
logits_bad = np.array([1000, 1001, 1002])
# np.exp(1000) = inf!

# Solucion: restar max
logits_safe = logits_bad - np.max(logits_bad)
exp_safe = np.exp(logits_safe)
softmax_safe = exp_safe / exp_safe.sum()

print(f"  Logits: {logits_bad}")
print(f"  Softmax (estable): {softmax_safe}")

# Log-sum-exp
def logsumexp(x):
    c = np.max(x)
    return c + np.log(np.sum(np.exp(x - c)))

print(f"  logsumexp({logits_bad}): {logsumexp(logits_bad):.4f}")


print("\n--- Condicion numerica ---")

# Sistema mal condicionado
A_bad = np.array([[1, 1], [1, 1.0001]])
b_bad = np.array([2, 2.0001])

x_sol = np.linalg.solve(A_bad, b_bad)
cond = np.linalg.cond(A_bad)

print(f"\n  Sistema mal condicionado:")
print(f"  Condicion: {cond:.0f}")
print(f"  Solucion: {x_sol}")

# Pequeña perturbacion cambia solucion
b_perturbed = np.array([2, 2.0002])
x_perturbed = np.linalg.solve(A_bad, b_perturbed)
print(f"  Solucion perturbada: {x_perturbed}")
print(f"  Cambio en b: {np.linalg.norm(b_perturbed - b_bad):.4f}")
print(f"  Cambio en x: {np.linalg.norm(x_perturbed - x_sol):.4f}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE TRANSFORMACIONES Y SISTEMAS:

1. Transformacion lineal = multiplicacion matricial.

2. nn.Linear ES una transformacion: y = W @ x + b.

3. Rotacion, escalado, reflexion: matrices especiales.

4. Ax = b: solve(), LU, QR decomposition.

5. Minimos cuadrados: lstsq() = regresion lineal.

6. Gram-Schmidt: construir bases ortonormales.

7. Descenso de gradiente: alternativa a ecuaciones normales.

8. Ridge y Logistic regression con algebra lineal.

9. SGD con momentum: aceleracion de convergencia.

10. Estabilidad numerica: log-sum-exp, condicion.

Siguiente archivo: Eigenvalues, SVD y PCA.
"""

print("\n FIN DE ARCHIVO 02_transformaciones_y_sistemas.")
print(" Transformaciones lineales han sido dominadas.")
