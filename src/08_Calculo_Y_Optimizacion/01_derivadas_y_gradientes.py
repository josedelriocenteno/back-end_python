# ===========================================================================
# 01_derivadas_y_gradientes.py
# ===========================================================================
# MODULO 08: CALCULO Y OPTIMIZACION
# ARCHIVO 01: Derivadas, Gradientes y Diferenciacion
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar derivadas, derivadas parciales, gradientes, Jacobianos,
# Hessianas, y diferenciacion numerica/simbolica para ML.
#
# CONTENIDO:
#   1. Derivadas: concepto, interpretacion geometrica.
#   2. Derivadas parciales y gradientes.
#   3. Diferenciacion numerica: forward, backward, central.
#   4. Regla de la cadena (CRITICA para backprop).
#   5. Jacobiano y Hessiana.
#   6. Gradiente de funciones ML: MSE, cross-entropy, softmax.
#   7. Verificacion de gradientes (gradient checking).
#   8. Ejercicio: derivadas de un mini-MLP.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: DERIVADAS — CONCEPTO
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: DERIVADAS — CONCEPTO E INTUICION ===")
print("=" * 80)

"""
Derivada: tasa de cambio instantanea de una funcion.
f'(x) = lim(h->0) [f(x+h) - f(x)] / h

EN ML:
- La derivada nos dice COMO CAMBIAR los pesos para reducir el loss.
- Si dL/dw > 0: w es demasiado grande, reducirlo.
- Si dL/dw < 0: w es demasiado pequeño, aumentarlo.
- Si dL/dw = 0: estamos en un minimo (o maximo o saddle point).
"""

print("\n--- Derivada como pendiente ---")

def f(x):
    return x**2 + 3*x + 1

def derivada_numerica(f, x, h=1e-7):
    """Derivada numerica (diferencia central)."""
    return (f(x + h) - f(x - h)) / (2 * h)

# f(x) = x^2 + 3x + 1, f'(x) = 2x + 3
x = 2.0
df = derivada_numerica(f, x)
df_analitico = 2 * x + 3

print(f"  f(x) = x² + 3x + 1")
print(f"  f'(2) numerico:   {df:.8f}")
print(f"  f'(2) analitico:  {df_analitico:.8f}")
print(f"  Error: {abs(df - df_analitico):.2e}")


print("\n--- Tabla de derivadas comunes ---")

print("""
+------------------+-------------------+----------------------------+
| f(x)             | f'(x)             | USO EN ML                  |
+------------------+-------------------+----------------------------+
| x^n              | n*x^(n-1)         | Polinomios, regularizacion |
| e^x              | e^x               | Softmax, activaciones      |
| ln(x)            | 1/x               | Cross-entropy loss         |
| 1/(1+e^(-x))     | σ(x)*(1-σ(x))    | Sigmoid activation         |
| max(0, x)        | 1 si x>0, 0 sino  | ReLU activation            |
| tanh(x)          | 1 - tanh²(x)      | Tanh activation            |
| ||x||²           | 2x                | L2 regularization          |
+------------------+-------------------+----------------------------+
""")


print("\n--- Derivadas de activaciones comunes ---")

def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def sigmoid_deriv(x):
    s = sigmoid(x)
    return s * (1 - s)

def relu(x):
    return np.maximum(0, x)

def relu_deriv(x):
    return (x > 0).astype(float)

def tanh_deriv(x):
    return 1 - np.tanh(x)**2

x_vals = np.array([-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0])

print("  x      sigmoid   sig'     ReLU    ReLU'   tanh    tanh'")
for x in x_vals:
    print(f"  {x:5.1f}  {sigmoid(x):.4f}   {sigmoid_deriv(x):.4f}   "
          f"{relu(x):5.2f}   {relu_deriv(x):.2f}     "
          f"{np.tanh(x):.4f}  {tanh_deriv(x):.4f}")


# =====================================================================
#   PARTE 2: DIFERENCIACION NUMERICA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: DIFERENCIACION NUMERICA ===")
print("=" * 80)

"""
Tres metodos:
1. Forward:  (f(x+h) - f(x)) / h           -> O(h)
2. Backward: (f(x) - f(x-h)) / h           -> O(h)
3. Central:  (f(x+h) - f(x-h)) / (2h)      -> O(h²)  <-- preferido

El central es mas preciso por un factor de h.
"""

print("\n--- Comparacion de metodos ---")

def forward_diff(f, x, h): return (f(x + h) - f(x)) / h
def backward_diff(f, x, h): return (f(x) - f(x - h)) / h
def central_diff(f, x, h): return (f(x + h) - f(x - h)) / (2 * h)

# f(x) = sin(x), f'(x) = cos(x)
x = 1.0
true_deriv = np.cos(x)

print(f"  f(x) = sin(x), f'(1) = cos(1) = {true_deriv:.10f}")
print(f"\n  {'h':>12s}  {'Forward':>12s}  {'Backward':>12s}  {'Central':>12s}")

for h in [0.1, 0.01, 0.001, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]:
    fwd = abs(forward_diff(np.sin, x, h) - true_deriv)
    bwd = abs(backward_diff(np.sin, x, h) - true_deriv)
    cnt = abs(central_diff(np.sin, x, h) - true_deriv)
    print(f"  {h:12.0e}  {fwd:12.2e}  {bwd:12.2e}  {cnt:12.2e}")

print("\n  Central es siempre mas preciso (error ~ h²)")


# =====================================================================
#   PARTE 3: DERIVADAS PARCIALES Y GRADIENTES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: DERIVADAS PARCIALES Y GRADIENTES ===")
print("=" * 80)

"""
Derivada parcial: derivada respecto a UNA variable.
∂f/∂x_i = lim(h->0) [f(x + h*e_i) - f(x)] / h

Gradiente: vector de TODAS las derivadas parciales.
∇f(x) = [∂f/∂x_1, ∂f/∂x_2, ..., ∂f/∂x_n]

El gradiente apunta en la DIRECCION DE MAXIMO CRECIMIENTO.
Para minimizar: ir en la direccion OPUESTA al gradiente.
"""

print("\n--- Gradiente numerico ---")

def numerical_gradient(f, x, h=1e-5):
    """Gradiente numerico con diferencia central."""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * h)
    return grad

# f(x, y) = x^2 + 2*y^2 + x*y
def f_2d(x):
    return x[0]**2 + 2*x[1]**2 + x[0]*x[1]

# Gradiente analitico: [2x + y, 4y + x]
punto = np.array([1.0, 2.0])
grad_num = numerical_gradient(f_2d, punto)
grad_ana = np.array([2*punto[0] + punto[1], 4*punto[1] + punto[0]])

print(f"  f(x,y) = x² + 2y² + xy")
print(f"  Punto: {punto}")
print(f"  ∇f numerico:   {grad_num}")
print(f"  ∇f analitico:  {grad_ana}")
print(f"  Error: {np.linalg.norm(grad_num - grad_ana):.2e}")


print("\n--- Gradiente como direccion de maximo crecimiento ---")

# Verificar que la norma del gradiente es la tasa maxima de cambio
grad = grad_ana
grad_dir = grad / np.linalg.norm(grad)

# Evaluamos en varias direcciones
print(f"\n  Tasa de cambio en diferentes direcciones:")
for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
    theta = np.radians(angle)
    direction = np.array([np.cos(theta), np.sin(theta)])
    rate = np.dot(grad, direction)
    marker = " <-- MAX" if angle == int(np.degrees(np.arctan2(grad[1], grad[0]))) else ""
    print(f"    {angle:3d}°: {rate:.4f}{marker}")

print(f"\n  Direccion del gradiente: {np.degrees(np.arctan2(grad[1], grad[0])):.1f}°")


# =====================================================================
#   PARTE 4: REGLA DE LA CADENA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: REGLA DE LA CADENA ===")
print("=" * 80)

"""
Si y = f(g(x)), entonces dy/dx = f'(g(x)) * g'(x)

!!! ESTO ES LA BASE DE BACKPROPAGATION !!!

En una red neuronal:
  loss = L(σ(W₃ σ(W₂ σ(W₁ x + b₁) + b₂) + b₃))
  
  La cadena: dL/dW₁ = dL/dy ... * dy/dz ... * dz/dW₁
"""

print("\n--- Regla de la cadena simple ---")

# y = (3x + 2)^4
# dy/dx = 4*(3x+2)^3 * 3 = 12*(3x+2)^3

def inner(x): return 3*x + 2
def outer(u): return u**4

x = 1.0
chain_analytic = 12 * (3*x + 2)**3
chain_numeric = derivada_numerica(lambda x: (3*x + 2)**4, x)

print(f"  y = (3x + 2)⁴")
print(f"  dy/dx analitico: {chain_analytic}")
print(f"  dy/dx numerico:  {chain_numeric:.4f}")


print("\n--- Cadena con multiples capas ---")

"""
z = x              (input)
a = 2*z + 1        (capa 1: lineal)
b = σ(a)           (capa 1: activacion)
c = 3*b - 0.5      (capa 2: lineal)
y = c^2            (loss)

dy/dx = dy/dc * dc/db * db/da * da/dz

forward: calcular z -> a -> b -> c -> y
backward: propagar dy/dc -> dc/db -> db/da -> da/dz
"""

x = 0.5

# Forward pass
z = x
a = 2*z + 1        # a = 2
b = sigmoid(a)      # b ≈ 0.88
c = 3*b - 0.5       # c ≈ 2.14
y = c**2            # y ≈ 4.58

print(f"  Forward pass:")
print(f"    x={x} -> a={a:.4f} -> b={b:.4f} -> c={c:.4f} -> y={y:.4f}")

# Backward pass (derivadas locales)
dy_dc = 2 * c           # d(c²)/dc = 2c
dc_db = 3               # d(3b-0.5)/db = 3
db_da = sigmoid_deriv(a) # σ'(a) = σ(a)*(1-σ(a))
da_dz = 2               # d(2z+1)/dz = 2

# Cadena completa
dy_dx = dy_dc * dc_db * db_da * da_dz

# Verificar numericamente
dy_dx_num = derivada_numerica(
    lambda x: (3*sigmoid(2*x+1) - 0.5)**2, x
)

print(f"\n  Backward pass:")
print(f"    dy/dc={dy_dc:.4f}, dc/db={dc_db}, db/da={db_da:.4f}, da/dx={da_dz}")
print(f"    dy/dx (cadena): {dy_dx:.6f}")
print(f"    dy/dx (numerico): {dy_dx_num:.6f}")
print(f"    Error: {abs(dy_dx - dy_dx_num):.2e}")


# =====================================================================
#   PARTE 5: JACOBIANO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: JACOBIANO ===")
print("=" * 80)

"""
Jacobiano: generalizacion del gradiente para funciones vectoriales.
Si f: R^n -> R^m, el Jacobiano J es una matriz m x n:
  J[i,j] = ∂f_i / ∂x_j

EN ML: Jacobiano de la capa lineal y = W @ x es W.
Jacobiano de softmax es una matriz densa.
"""

print("\n--- Jacobiano numerico ---")

def numerical_jacobian(f, x, h=1e-5):
    """Jacobiano numerico."""
    y0 = f(x)
    m = len(y0)
    n = len(x)
    J = np.zeros((m, n))
    
    for j in range(n):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[j] += h
        x_minus[j] -= h
        J[:, j] = (f(x_plus) - f(x_minus)) / (2 * h)
    
    return J

# f([x, y]) = [x^2 + y, x*y^2]
def f_vec(x):
    return np.array([x[0]**2 + x[1], x[0] * x[1]**2])

punto = np.array([2.0, 3.0])
J_num = numerical_jacobian(f_vec, punto)

# Jacobiano analitico:
# [[2x, 1], [y^2, 2xy]]
J_ana = np.array([
    [2*punto[0], 1],
    [punto[1]**2, 2*punto[0]*punto[1]]
])

print(f"  f(x,y) = [x²+y, xy²]")
print(f"  Punto: {punto}")
print(f"  J numerico:\n{J_num}")
print(f"  J analitico:\n{J_ana}")
print(f"  Error: {np.linalg.norm(J_num - J_ana):.2e}")


print("\n--- Jacobiano de softmax ---")

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def softmax_jacobian(x):
    """Jacobiano analitico de softmax."""
    s = softmax(x)
    # J[i,j] = s[i] * (δ[i,j] - s[j])
    return np.diag(s) - np.outer(s, s)

x = np.array([2.0, 1.0, 0.5])
J_softmax_num = numerical_jacobian(softmax, x)
J_softmax_ana = softmax_jacobian(x)

print(f"  x = {x}")
print(f"  softmax(x) = {softmax(x)}")
print(f"  J numerico:\n{J_softmax_num}")
print(f"  J analitico:\n{J_softmax_ana}")
print(f"  Error: {np.linalg.norm(J_softmax_num - J_softmax_ana):.2e}")


# =====================================================================
#   PARTE 6: GRADIENTES DE FUNCIONES ML
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: GRADIENTES DE FUNCIONES ML ===")
print("=" * 80)

print("\n--- Gradiente de MSE Loss ---")

"""
MSE = (1/n) Σ (y_pred - y_true)²
∂MSE/∂y_pred = (2/n) * (y_pred - y_true)
"""

y_true = np.array([1.0, 0.0, 1.0, 0.0])
y_pred = np.array([0.9, 0.1, 0.8, 0.3])

def mse_loss(y_pred, y_true):
    return np.mean((y_pred - y_true)**2)

grad_mse_analytic = (2 / len(y_true)) * (y_pred - y_true)
grad_mse_numeric = numerical_gradient(lambda yp: mse_loss(yp, y_true), y_pred)

print(f"  y_true: {y_true}")
print(f"  y_pred: {y_pred}")
print(f"  MSE: {mse_loss(y_pred, y_true):.6f}")
print(f"  ∂MSE/∂y_pred (analitico): {grad_mse_analytic}")
print(f"  ∂MSE/∂y_pred (numerico):  {grad_mse_numeric}")


print("\n--- Gradiente de Binary Cross-Entropy ---")

"""
BCE = -(1/n) Σ [y*log(ŷ) + (1-y)*log(1-ŷ)]
∂BCE/∂ŷ = -(1/n) * [y/ŷ - (1-y)/(1-ŷ)]
"""

def bce_loss(y_pred, y_true):
    eps = 1e-15
    yp = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(yp) + (1 - y_true) * np.log(1 - yp))

grad_bce_analytic = -(1/len(y_true)) * (
    y_true / np.clip(y_pred, 1e-15, None) -
    (1 - y_true) / np.clip(1 - y_pred, 1e-15, None)
)
grad_bce_numeric = numerical_gradient(lambda yp: bce_loss(yp, y_true), y_pred)

print(f"  BCE: {bce_loss(y_pred, y_true):.6f}")
print(f"  ∂BCE/∂ŷ (analitico): {grad_bce_analytic}")
print(f"  ∂BCE/∂ŷ (numerico):  {grad_bce_numeric}")


print("\n--- Gradiente de Cross-Entropy con Softmax ---")

"""
CE = -Σ y_true * log(softmax(logits))
∂CE/∂logits = softmax(logits) - y_true  (resultado simple!)
"""

logits = np.array([2.0, 1.0, 0.1])
y_one_hot = np.array([1.0, 0.0, 0.0])

probs = softmax(logits)
grad_ce = probs - y_one_hot

def ce_loss(logits, y):
    p = softmax(logits)
    return -np.sum(y * np.log(p + 1e-15))

grad_ce_numeric = numerical_gradient(lambda l: ce_loss(l, y_one_hot), logits)

print(f"  logits: {logits}")
print(f"  softmax: {probs}")
print(f"  ∂CE/∂logits (analitico): {grad_ce}")
print(f"  ∂CE/∂logits (numerico):  {grad_ce_numeric}")
print(f"  Error: {np.linalg.norm(grad_ce - grad_ce_numeric):.2e}")


# =====================================================================
#   PARTE 7: GRADIENT CHECKING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: GRADIENT CHECKING ===")
print("=" * 80)

"""
Verificar que tu implementacion analitica es correcta
comparandola con la numerica.

Criterio: |grad_ana - grad_num| / (|grad_ana| + |grad_num|) < 1e-5
"""

print("\n--- Gradient checker ---")

def gradient_check(f, grad_f, x, h=1e-5, threshold=1e-5):
    """Verifica gradiente analitico vs numerico."""
    grad_ana = grad_f(x)
    grad_num = numerical_gradient(f, x, h)
    
    numerator = np.linalg.norm(grad_ana - grad_num)
    denominator = np.linalg.norm(grad_ana) + np.linalg.norm(grad_num)
    
    if denominator == 0:
        return 0, True
    
    relative_error = numerator / denominator
    passed = relative_error < threshold
    
    return relative_error, passed

# Test: f(w) = w^T @ X^T @ X @ w (cuadratica)
np.random.seed(42)
X_check = np.random.randn(10, 3)

def f_quad(w):
    return w @ X_check.T @ X_check @ w

def grad_quad(w):
    return 2 * X_check.T @ X_check @ w

w = np.random.randn(3)
error, passed = gradient_check(f_quad, grad_quad, w)
print(f"  Cuadratica: error={error:.2e}, {'PASS' if passed else 'FAIL'}")

# Test: sigmoid cross-entropy composicion
def f_sig_ce(w):
    z = X_check @ w
    s = sigmoid(z)
    y = np.ones(10) * 0.5
    return -np.mean(y * np.log(s + 1e-15) + (1 - y) * np.log(1 - s + 1e-15))

def grad_sig_ce(w):
    z = X_check @ w
    s = sigmoid(z)
    y = np.ones(10) * 0.5
    return (1/10) * X_check.T @ (s - y)

error2, passed2 = gradient_check(f_sig_ce, grad_sig_ce, w)
print(f"  Sigmoid CE: error={error2:.2e}, {'PASS' if passed2 else 'FAIL'}")


# =====================================================================
#   PARTE 8: EJERCICIO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: EJERCICIO — FORWARD/BACKWARD DE MLP ===")
print("=" * 80)

"""
Implementar forward y backward pass completo de un MLP de 2 capas.
"""

print("\n--- MLP 2 capas: forward + backward ---")

class MiniMLP:
    """MLP de 2 capas con backpropagation manual."""
    
    def __init__(self, input_dim, hidden_dim, output_dim):
        np.random.seed(42)
        scale1 = np.sqrt(2.0 / input_dim)
        scale2 = np.sqrt(2.0 / hidden_dim)
        
        self.W1 = np.random.randn(input_dim, hidden_dim) * scale1
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, output_dim) * scale2
        self.b2 = np.zeros(output_dim)
    
    def forward(self, X):
        """Forward pass guardando activaciones."""
        self.X = X
        self.z1 = X @ self.W1 + self.b1       # Pre-activacion capa 1
        self.a1 = np.maximum(0, self.z1)       # ReLU
        self.z2 = self.a1 @ self.W2 + self.b2  # Pre-activacion capa 2
        
        # Softmax output
        exp_z = np.exp(self.z2 - np.max(self.z2, axis=1, keepdims=True))
        self.probs = exp_z / exp_z.sum(axis=1, keepdims=True)
        
        return self.probs
    
    def backward(self, y_true):
        """Backward pass: calcular gradientes."""
        n = len(y_true)
        
        # Gradiente de cross-entropy + softmax
        dz2 = self.probs.copy()
        dz2[range(n), y_true] -= 1
        dz2 /= n
        
        # Gradientes capa 2
        self.dW2 = self.a1.T @ dz2
        self.db2 = dz2.sum(axis=0)
        
        # Propagar a capa 1
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (self.z1 > 0)  # ReLU backward
        
        # Gradientes capa 1
        self.dW1 = self.X.T @ dz1
        self.db1 = dz1.sum(axis=0)
    
    def loss(self, y_true):
        n = len(y_true)
        correct_probs = self.probs[range(n), y_true]
        return -np.mean(np.log(correct_probs + 1e-15))
    
    def update(self, lr=0.01):
        self.W1 -= lr * self.dW1
        self.b1 -= lr * self.db1
        self.W2 -= lr * self.dW2
        self.b2 -= lr * self.db2

# Datos de 3 clases
np.random.seed(42)
N = 150
X_train = np.vstack([
    np.random.randn(50, 4) + [1, 0, 0, 0],
    np.random.randn(50, 4) + [0, 1, 0, 0],
    np.random.randn(50, 4) + [0, 0, 1, 0],
])
y_train = np.array([0]*50 + [1]*50 + [2]*50)

mlp = MiniMLP(input_dim=4, hidden_dim=16, output_dim=3)

# Gradient checking
probs = mlp.forward(X_train[:5])
mlp.backward(y_train[:5])

# Verificar dW1 numericamente
def loss_fn_w1(w1_flat):
    mlp_copy_W1 = w1_flat.reshape(mlp.W1.shape)
    z1 = X_train[:5] @ mlp_copy_W1 + mlp.b1
    a1 = np.maximum(0, z1)
    z2 = a1 @ mlp.W2 + mlp.b2
    exp_z = np.exp(z2 - np.max(z2, axis=1, keepdims=True))
    probs = exp_z / exp_z.sum(axis=1, keepdims=True)
    return -np.mean(np.log(probs[range(5), y_train[:5]] + 1e-15))

grad_W1_num = numerical_gradient(loss_fn_w1, mlp.W1.flatten())
grad_W1_ana = mlp.dW1.flatten()

error_w1 = np.linalg.norm(grad_W1_ana - grad_W1_num) / (
    np.linalg.norm(grad_W1_ana) + np.linalg.norm(grad_W1_num) + 1e-15)

print(f"  Gradient check W1: error = {error_w1:.2e} {'PASS' if error_w1 < 1e-5 else 'FAIL'}")

# Entrenar
print(f"\n  Training MLP:")
for epoch in range(201):
    probs = mlp.forward(X_train)
    loss = mlp.loss(y_train)
    mlp.backward(y_train)
    mlp.update(lr=0.1)
    
    if epoch % 50 == 0:
        preds = np.argmax(probs, axis=1)
        acc = np.mean(preds == y_train)
        print(f"    Epoch {epoch:3d}: loss={loss:.4f}, accuracy={acc:.4f}")


print("\n" + "=" * 80)
print("=== CAPITULO 9: DIVERGENCIA Y CONVERGENCIA ===")
print("=" * 80)

"""
Conceptos criticos para optimizacion:
- Learning rate demasiado alto -> divergencia.
- Learning rate demasiado bajo -> convergencia lenta.
- Loss landscape: convexo vs no-convexo.
"""

print("\n--- Efecto del learning rate ---")

def train_with_lr(X, y, lr, epochs=100):
    n, d = X.shape
    w = np.zeros(d)
    losses = []
    
    for _ in range(epochs):
        y_pred = X @ w
        loss = np.mean((y_pred - y) ** 2)
        losses.append(loss)
        
        if np.isnan(loss) or loss > 1e10:
            break
        
        grad = (2/n) * X.T @ (y_pred - y)
        w -= lr * grad
    
    return losses

np.random.seed(42)
X_lr = np.random.randn(50, 3)
y_lr = X_lr @ np.array([1, 2, 3]) + np.random.randn(50) * 0.5

for lr in [0.001, 0.01, 0.1, 0.5, 1.0, 2.0]:
    losses = train_with_lr(X_lr, y_lr, lr, epochs=100)
    final = losses[-1] if not np.isnan(losses[-1]) else float('inf')
    status = "DIVERGE" if final > 1e5 else f"{final:.4f}"
    print(f"  lr={lr:.3f}: loss final = {status} ({len(losses)} epochs)")


print("\n" + "=" * 80)
print("=== CAPITULO 10: HESSIANA Y CURVATURA ===")
print("=" * 80)

"""
Hessiana H: matriz de segundas derivadas parciales.
H[i,j] = ∂²f / (∂x_i ∂x_j)

Eigenvalues de H en un punto critico:
- Todos > 0: minimo local.
- Todos < 0: maximo local.
- Mixtos: saddle point.

EN ML: el ratio max_eigenval/min_eigenval determina dificultad
de optimizacion. Alto ratio = mal condicionado.
"""

print("\n--- Hessiana numerica ---")

def numerical_hessian(f, x, h=1e-5):
    """Hessiana con diferencias finitas."""
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

# Funcion cuadratica f = x^2 + 5y^2 + 2xy
def f_hess(x):
    return x[0]**2 + 5*x[1]**2 + 2*x[0]*x[1]

punto = np.array([1.0, 1.0])
H = numerical_hessian(f_hess, punto)

# Hessiana analitica: [[2, 2], [2, 10]]
H_ana = np.array([[2, 2], [2, 10]])

eigenvals = np.linalg.eigvalsh(H)
condition = max(eigenvals) / min(eigenvals)

print(f"  f = x² + 5y² + 2xy")
print(f"  H numerica:\n{H}")
print(f"  H analitica:\n{H_ana}")
print(f"  Eigenvalues: {eigenvals}")
print(f"  Condicion: {condition:.2f}")
print(f"  Tipo: {'Minimo' if all(eigenvals > 0) else 'Saddle' if any(eigenvals < 0) else 'Indefinido'}")


print("\n--- Hessiana y tasa de convergencia ---")

"""
La tasa de convergencia de GD depende de la condicion de la Hessiana.
lr optimo = 2 / (lambda_max + lambda_min)
Convergencia: proporcion = (k-1)/(k+1), donde k = lambda_max/lambda_min
"""

for func_name, func, grad_func, x0 in [
    ("x² + y²",         lambda x: x[0]**2 + x[1]**2,
                         lambda x: np.array([2*x[0], 2*x[1]]),
                         np.array([5.0, 5.0])),
    ("x² + 100y²",      lambda x: x[0]**2 + 100*x[1]**2,
                         lambda x: np.array([2*x[0], 200*x[1]]),
                         np.array([5.0, 5.0])),
]:
    H_test = numerical_hessian(func, np.array([0.0, 0.0]))
    eigs = np.linalg.eigvalsh(H_test)
    ratio = max(eigs) / min(eigs)
    
    # Entrenar
    x = x0.copy()
    lr = 2 / (max(eigs) + min(eigs))
    for _ in range(50):
        x -= lr * grad_func(x)
    
    print(f"  {func_name:12s}: κ={ratio:6.1f}, lr_opt={lr:.4f}, "
          f"loss_50={func(x):.2e}")


print("\n" + "=" * 80)
print("=== CAPITULO 11: SERIES DE TAYLOR ===")
print("=" * 80)

"""
Aproximacion de Taylor: f(x+h) ≈ f(x) + f'(x)*h + f''(x)*h²/2 + ...

EN ML:
- Justifica por que GD funciona (linealizacion local).
- Metodo de Newton: usar hasta orden 2 (Hessiana).
- Explica regularizacion L2 (expansion alrededor del optimo).
"""

print("\n--- Aproximaciones de Taylor ---")

def taylor_approx(f, x0, h, order=1):
    """Aproximacion de Taylor de orden 1 o 2."""
    if order == 1:
        df = derivada_numerica(f, x0)
        return f(x0) + df * h
    elif order == 2:
        df = derivada_numerica(f, x0)
        d2f = (f(x0 + 1e-5) - 2*f(x0) + f(x0 - 1e-5)) / (1e-5)**2
        return f(x0) + df * h + 0.5 * d2f * h**2

f_taylor = lambda x: np.exp(x)
x0 = 0.0

print(f"  f(x) = e^x, x0 = {x0}")
print(f"  {'h':>6s}  {'Exacto':>10s}  {'Taylor1':>10s}  {'Taylor2':>10s}  {'Err1':>10s}  {'Err2':>10s}")

for h in [0.01, 0.1, 0.5, 1.0, 2.0]:
    exact = f_taylor(x0 + h)
    t1 = taylor_approx(f_taylor, x0, h, order=1)
    t2 = taylor_approx(f_taylor, x0, h, order=2)
    print(f"  {h:6.2f}  {exact:10.4f}  {t1:10.4f}  {t2:10.4f}  "
          f"{abs(exact-t1):10.2e}  {abs(exact-t2):10.2e}")


print("\n--- Newton's method (2do orden) ---")

"""
Newton: x_{n+1} = x_n - H^{-1} @ ∇f(x_n)
Usa la Hessiana para convergencia cuadratica.
En ML: muy caro (Hessiana de millones de params).
"""

def newtons_method(f, grad_f, x0, epochs=10):
    x = x0.copy()
    losses = [f(x)]
    
    for _ in range(epochs):
        g = grad_f(x)
        H = numerical_hessian(f, x)
        
        try:
            delta = np.linalg.solve(H, g)
            x = x - delta
        except np.linalg.LinAlgError:
            x = x - 0.01 * g
        
        losses.append(f(x))
    
    return x, losses

x_newton, losses_newton = newtons_method(
    f_hess,
    lambda x: numerical_gradient(f_hess, x),
    np.array([5.0, 5.0]),
    epochs=5
)

print(f"\n  Newton (5 pasos): loss = {losses_newton[-1]:.2e}")
print(f"  GD vanilla (5 pasos): loss = {train_with_lr(np.eye(2), np.zeros(2), 0.1, 5)[-1]:.2e}")
print(f"  Newton converge en ~5 pasos vs ~50+ de GD")


print("\n" + "=" * 80)
print("=== CAPITULO 12: INTEGRALES Y AREAS ===")
print("=" * 80)

"""
Integral: area bajo la curva. Operacion inversa de la derivada.

EN ML:
- Probabilidades: P(a < X < b) = integral de PDF.
- Expectation: E[X] = integral de x * p(x).
- KL divergence: integral de p(x) * log(p(x)/q(x)).
"""

print("\n--- Integracion numerica ---")

def trapezoidal(f, a, b, n):
    """Regla del trapecio."""
    x = np.linspace(a, b, n + 1)
    y = np.array([f(xi) for xi in x])
    h = (b - a) / n
    return h * (y[0]/2 + y[-1]/2 + y[1:-1].sum())

def simpsons(f, a, b, n):
    """Regla de Simpson."""
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n + 1)
    y = np.array([f(xi) for xi in x])
    h = (b - a) / n
    return (h/3) * (y[0] + y[-1] + 4*y[1::2].sum() + 2*y[2:-1:2].sum())

# Integral de sin(x) de 0 a pi = 2
print(f"  ∫sin(x)dx de 0 a π = 2.0")
for n in [10, 100, 1000]:
    trap = trapezoidal(np.sin, 0, np.pi, n)
    simp = simpsons(np.sin, 0, np.pi, n)
    print(f"    n={n:4d}: trapecio={trap:.8f}, simpson={simp:.8f}")

# Integral gaussiana
print(f"\n  ∫N(0,1)dx de -∞ a 0 ≈ 0.5")
gaussian = lambda x: np.exp(-x**2/2) / np.sqrt(2*np.pi)
result = simpsons(gaussian, -10, 0, 1000)
print(f"    Simpson: {result:.6f}")


print("\n" + "=" * 80)
print("=== CAPITULO 13: DIFERENCIACION AUTOMATICA ===")
print("=" * 80)

"""
Tipos de diferenciacion:
1. Numerica: f'(x) ≈ (f(x+h) - f(x-h)) / 2h. Lenta, imprecisa.
2. Simbolica: reglas algebraicas (como Mathematica). Exacta pero lenta.
3. AUTOMATICA: registrar operaciones, aplicar chain rule. EXACTA y RAPIDA.

PyTorch usa autograd: diferenciacion automatica en modo reverse.

Modo Forward: eficiente cuando hay pocas entradas.
Modo Reverse: eficiente cuando hay pocas salidas (1 loss -> millones de params).
Por eso ML usa reverse mode.
"""

print("\n--- Forward vs Reverse mode ---")

print("""
  Forward mode AD:
    - Propaga derivadas DE input A output.
    - 1 pasada por cada input variable.
    - Eficiente: pocas inputs, muchas outputs.
    
  Reverse mode AD (backprop):
    - Propaga derivadas DE output A input.
    - 1 pasada para TODAS las derivadas.
    - Eficiente: 1 loss, millones de params.
    - = BACKPROPAGATION.

  EN ML: Reverse mode SIEMPRE.
  Loss es 1 escalar, params son millones.
""")

# Comparar costo computacional
n_params = [100, 1000, 10000, 100000, 1000000]
print(f"  {'Params':>10s}  {'Forward (pasadas)':>18s}  {'Reverse (pasadas)':>18s}")
for n in n_params:
    print(f"  {n:10,d}  {n:18,d}  {'1':>18s}")


print("\n" + "=" * 80)
print("=== CAPITULO 14: DERIVADA DIRECCIONAL ===")
print("=" * 80)

"""
Derivada direccional: tasa de cambio en una direccion ARBITRARIA.
D_u f(x) = ∇f(x) · u, donde u es vector unitario.

Maxima cuando u = ∇f / ||∇f|| (direccion del gradiente).
Minima cuando u = -∇f / ||∇f|| (opuesta).
"""

print("\n--- Derivada direccional ---")

def directional_derivative(f, x, direction, h=1e-5):
    """Derivada direccional numerica."""
    u = direction / np.linalg.norm(direction)
    return (f(x + h * u) - f(x - h * u)) / (2 * h)

# f(x,y) = x^2 + 4y^2
def f_dir(x):
    return x[0]**2 + 4*x[1]**2

punto = np.array([1.0, 1.0])
grad_f = np.array([2*punto[0], 8*punto[1]])  # [2, 8]

# Derivada en varias direcciones
direcciones = {
    "gradiente":     grad_f / np.linalg.norm(grad_f),
    "-gradiente":    -grad_f / np.linalg.norm(grad_f),
    "eje x":         np.array([1.0, 0.0]),
    "eje y":         np.array([0.0, 1.0]),
    "diagonal":      np.array([1.0, 1.0]) / np.sqrt(2),
}

for name, d in direcciones.items():
    dd = directional_derivative(f_dir, punto, d)
    dd_analitico = np.dot(grad_f, d)
    print(f"  {name:12s}: D_u f = {dd:.4f} (analitico: {dd_analitico:.4f})")

print(f"\n  Max cambio: {np.linalg.norm(grad_f):.4f} (= ||∇f||)")



print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE DERIVADAS Y GRADIENTES:

1. Derivada: tasa de cambio. dL/dw dice como ajustar pesos.

2. Diferencia central: O(h²), mas precisa.

3. Gradiente: vector de parciales. Apunta a max crecimiento.

4. Regla de la cadena: BASE de backpropagation.

5. Jacobiano: generalizacion para funciones vectoriales.

6. Hessiana: curvatura, condicionamiento, Newton's method.

7. Taylor: justifica gradient descent (linealizacion local).

8. Integrales: probabilidades, expectation, KL divergence.

9. Autograd: reverse mode = backprop, exacto y eficiente.

10. Gradient checking: verificar implementacion analitica.

Siguiente archivo: Optimizacion y variantes de gradient descent.
"""

print("\n FIN DE ARCHIVO 01_derivadas_y_gradientes.")
print(" Derivadas y gradientes han sido dominados.")
