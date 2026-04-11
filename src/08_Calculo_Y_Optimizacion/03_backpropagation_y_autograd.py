# ===========================================================================
# 03_backpropagation_y_autograd.py
# ===========================================================================
# MODULO 08: CALCULO Y OPTIMIZACION
# ARCHIVO 03: Backpropagation, Grafo Computacional y Autograd
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar backpropagation desde cero: grafos computacionales,
# autograd engine, y como PyTorch calcula gradientes.
#
# CONTENIDO:
#   1. Grafo computacional: nodos y aristas.
#   2. Forward pass: evaluar el grafo.
#   3. Backward pass: propagar gradientes.
#   4. Autograd engine desde cero.
#   5. Backprop para capas comunes: Linear, ReLU, Softmax.
#   6. Gradientes de batch normalization.
#   7. Vanishing/exploding gradients.
#   8. Ejercicio: entrenar un MLP completo con autograd.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: GRAFO COMPUTACIONAL
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: GRAFO COMPUTACIONAL ===")
print("=" * 80)

"""
Un grafo computacional es un DAG (Directed Acyclic Graph) donde:
- Nodos hoja: inputs y parametros.
- Nodos internos: operaciones.
- Aristas: flujo de datos.

Forward: recorrer de hojas a output.
Backward: recorrer de output a hojas (gradientes).

PyTorch construye este grafo automaticamente.
"""

print("\n--- Ejemplo conceptual ---")

print("""
  Ejemplo: loss = (W @ x + b - y)^2

  Grafo:
    x, W ---[matmul]---> z1
    z1, b ---[add]-----> z2
    z2, y ---[sub]-----> z3
    z3 ------[square]---> loss

  Forward: x,W -> z1 -> z2 -> z3 -> loss
  Backward: dloss -> dz3 -> dz2 -> dz1 -> dW, dx
""")


# =====================================================================
#   PARTE 2: AUTOGRAD ENGINE DESDE CERO
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 2: AUTOGRAD ENGINE DESDE CERO ===")
print("=" * 80)

"""
Implementamos un Tensor con soporte de gradientes automaticos.
Similar a torch.Tensor pero minimalista.
"""

print("\n--- Clase Value (escalar con autograd) ---")

class Value:
    """Escalar con autograd. Inspirado en micrograd de Karpathy."""
    
    def __init__(self, data, _children=(), _op='', label=''):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
        self.label = label
    
    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"
    
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
        return out
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __neg__(self):
        return self * (-1)
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return Value(other) + (-self)
    
    def __pow__(self, n):
        assert isinstance(n, (int, float))
        out = Value(self.data ** n, (self,), f'**{n}')
        
        def _backward():
            self.grad += n * (self.data ** (n - 1)) * out.grad
        out._backward = _backward
        return out
    
    def __truediv__(self, other):
        return self * (other ** -1)
    
    def exp(self):
        x = self.data
        out = Value(np.exp(x), (self,), 'exp')
        
        def _backward():
            self.grad += out.data * out.grad
        out._backward = _backward
        return out
    
    def log(self):
        x = self.data
        out = Value(np.log(x + 1e-15), (self,), 'log')
        
        def _backward():
            self.grad += (1.0 / (x + 1e-15)) * out.grad
        out._backward = _backward
        return out
    
    def relu(self):
        out = Value(max(0, self.data), (self,), 'relu')
        
        def _backward():
            self.grad += (self.data > 0) * out.grad
        out._backward = _backward
        return out
    
    def tanh(self):
        t = np.tanh(self.data)
        out = Value(t, (self,), 'tanh')
        
        def _backward():
            self.grad += (1 - t**2) * out.grad
        out._backward = _backward
        return out
    
    def backward(self):
        """Backpropagation usando ordenamiento topologico."""
        topo = []
        visited = set()
        
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        
        build_topo(self)
        
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()


# =====================================================================
#   PARTE 3: DEMOSTRAR AUTOGRAD
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 3: AUTOGRAD EN ACCION ===")
print("=" * 80)

print("\n--- Ejemplo simple ---")

# f = (a + b) * c
a = Value(2.0, label='a')
b = Value(3.0, label='b')
c = Value(4.0, label='c')

d = a + b        # d = 5
f = d * c         # f = 20

f.backward()

print(f"  a = {a.data}, b = {b.data}, c = {c.data}")
print(f"  f = (a + b) * c = {f.data}")
print(f"  df/da = {a.grad} (analitico: c = {c.data})")
print(f"  df/db = {b.grad} (analitico: c = {c.data})")
print(f"  df/dc = {c.grad} (analitico: a+b = {a.data + b.data})")


print("\n--- Ejemplo con regla de la cadena ---")

x = Value(0.5, label='x')
w = Value(2.0, label='w')
b = Value(1.0, label='b')

# Neurona: y = tanh(w*x + b)
z = w * x + b
y = z.tanh()

y.backward()

print(f"  z = w*x + b = {z.data:.4f}")
print(f"  y = tanh(z) = {y.data:.4f}")
print(f"  dy/dw = {w.grad:.6f}")
print(f"  dy/db = {b.grad:.6f}")
print(f"  dy/dx = {x.grad:.6f}")

# Verificar numericamente
h = 1e-5
w_plus = np.tanh((2.0 + h) * 0.5 + 1.0)
w_minus = np.tanh((2.0 - h) * 0.5 + 1.0)
dw_num = (w_plus - w_minus) / (2 * h)
print(f"  dy/dw numerico: {dw_num:.6f}")


print("\n--- Ejemplo de loss completo ---")

# loss = (y_pred - y_true)^2, donde y_pred = sigmoid(w*x + b)
x = Value(1.0, label='x')
w = Value(0.5, label='w')
b = Value(-0.3, label='b')
y_true = Value(1.0, label='y_true')

# Forward
z = w * x + b
# Sigmoid: 1 / (1 + exp(-z))
neg_z = z * (-1)
exp_neg_z = neg_z.exp()
denom = exp_neg_z + 1
y_pred = denom ** (-1)

# MSE loss
diff = y_pred - y_true
loss = diff ** 2

loss.backward()

print(f"\n  y_pred = sigmoid(w*x + b) = {y_pred.data:.6f}")
print(f"  loss = (y_pred - y_true)^2 = {loss.data:.6f}")
print(f"  dloss/dw = {w.grad:.6f}")
print(f"  dloss/db = {b.grad:.6f}")


# =====================================================================
#   PARTE 4: AUTOGRAD CON TENSORES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: AUTOGRAD CON TENSORES (NumPy) ===")
print("=" * 80)

"""
Extendemos el concepto a tensores (arrays).
Cada operacion tiene forward y backward.
"""

print("\n--- Tensor con autograd ---")

class Tensor:
    """Tensor con autograd basico."""
    
    def __init__(self, data, requires_grad=False):
        self.data = np.array(data, dtype=np.float64)
        self.requires_grad = requires_grad
        self.grad = np.zeros_like(self.data) if requires_grad else None
        self._backward_fn = None
        self._parents = []
    
    @property
    def shape(self):
        return self.data.shape
    
    def __repr__(self):
        return f"Tensor({self.data}, grad={self.grad is not None})"
    
    def zero_grad(self):
        if self.grad is not None:
            self.grad = np.zeros_like(self.data)
    
    def backward(self, grad=None):
        if grad is None:
            grad = np.ones_like(self.data)
        if self.grad is not None:
            self.grad += grad
        if self._backward_fn:
            self._backward_fn(grad)


def tensor_matmul(A, B):
    """Matrix multiplication con backward."""
    out = Tensor(A.data @ B.data)
    
    def _backward(grad):
        if A.requires_grad:
            A.backward(grad @ B.data.T)
        if B.requires_grad:
            B.backward(A.data.T @ grad)
    
    out._backward_fn = _backward
    out._parents = [A, B]
    return out

def tensor_add(A, B):
    """Addition con backward y broadcasting."""
    out = Tensor(A.data + B.data)
    
    def _backward(grad):
        if A.requires_grad:
            g = grad
            while g.ndim > A.data.ndim:
                g = g.sum(axis=0)
            A.backward(g)
        if B.requires_grad:
            g = grad
            while g.ndim > B.data.ndim:
                g = g.sum(axis=0)
            for i, (s1, s2) in enumerate(zip(B.data.shape, g.shape)):
                if s1 == 1 and s2 > 1:
                    g = g.sum(axis=i, keepdims=True)
            B.backward(g)
    
    out._backward_fn = _backward
    out._parents = [A, B]
    return out

def tensor_relu(A):
    """ReLU con backward."""
    out = Tensor(np.maximum(0, A.data))
    
    def _backward(grad):
        if A.requires_grad:
            A.backward(grad * (A.data > 0))
    
    out._backward_fn = _backward
    return out

def tensor_mse_loss(pred, target):
    """MSE Loss con backward."""
    diff = pred.data - target.data
    loss_val = np.mean(diff ** 2)
    out = Tensor(np.array(loss_val))
    
    def _backward(grad):
        n = pred.data.size
        g = 2 * diff / n * grad
        if pred.requires_grad:
            pred.backward(g)
    
    out._backward_fn = _backward
    return out


print("\n--- Test tensor autograd ---")

# y = ReLU(X @ W + b)
X = Tensor(np.array([[1.0, 2.0], [3.0, 4.0]]))
W = Tensor(np.random.randn(2, 3) * 0.1, requires_grad=True)
b = Tensor(np.zeros(3), requires_grad=True)
y_true = Tensor(np.array([[1.0, 0.0, 0.5], [0.0, 1.0, 0.5]]))

# Forward
z = tensor_matmul(X, W)
z_b = tensor_add(z, b)
a = tensor_relu(z_b)
loss = tensor_mse_loss(a, y_true)

# Backward
loss.backward()

print(f"  X shape: {X.shape}")
print(f"  W shape: {W.shape}")
print(f"  Loss: {loss.data:.6f}")
print(f"  dL/dW:\n{W.grad}")
print(f"  dL/db: {b.grad}")


# =====================================================================
#   PARTE 5: BACKPROP PARA CAPAS COMUNES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: BACKPROP PARA CAPAS COMUNES ===")
print("=" * 80)

"""
Derivadas de capas usadas en redes neuronales.
Cada capa tiene forward y backward.
"""

print("\n--- Linear layer backward ---")

class LinearLayer:
    """Capa lineal con forward y backward."""
    
    def __init__(self, in_dim, out_dim):
        self.W = np.random.randn(in_dim, out_dim) * np.sqrt(2.0 / in_dim)
        self.b = np.zeros(out_dim)
        self.dW = None
        self.db = None
    
    def forward(self, X):
        self.X = X
        return X @ self.W + self.b
    
    def backward(self, dout):
        n = self.X.shape[0]
        self.dW = self.X.T @ dout
        self.db = dout.sum(axis=0)
        dX = dout @ self.W.T
        return dX


print("\n--- BatchNorm backward ---")

class BatchNormLayer:
    """Batch normalization con forward y backward."""
    
    def __init__(self, dim, eps=1e-5, momentum=0.1):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)
        self.eps = eps
        self.momentum = momentum
        self.running_mean = np.zeros(dim)
        self.running_var = np.ones(dim)
    
    def forward(self, X, training=True):
        if training:
            self.mean = X.mean(axis=0)
            self.var = X.var(axis=0)
            self.X_norm = (X - self.mean) / np.sqrt(self.var + self.eps)
            self.X = X
            
            # Running stats
            self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * self.mean
            self.running_var = (1 - self.momentum) * self.running_var + self.momentum * self.var
        else:
            self.X_norm = (X - self.running_mean) / np.sqrt(self.running_var + self.eps)
        
        return self.gamma * self.X_norm + self.beta
    
    def backward(self, dout):
        n = dout.shape[0]
        
        # Gradientes de gamma y beta
        self.dgamma = (dout * self.X_norm).sum(axis=0)
        self.dbeta = dout.sum(axis=0)
        
        # Gradiente de X
        dX_norm = dout * self.gamma
        dvar = (-0.5 * dX_norm * (self.X - self.mean) *
                (self.var + self.eps) ** (-1.5)).sum(axis=0)
        dmean = (-dX_norm / np.sqrt(self.var + self.eps)).sum(axis=0) + \
                dvar * (-2 * (self.X - self.mean)).mean(axis=0)
        
        dX = (dX_norm / np.sqrt(self.var + self.eps) +
              dvar * 2 * (self.X - self.mean) / n +
              dmean / n)
        
        return dX


print("\n--- Dropout backward ---")

class DropoutLayer:
    """Dropout con forward y backward."""
    
    def __init__(self, p=0.5):
        self.p = p
        self.mask = None
    
    def forward(self, X, training=True):
        if training:
            self.mask = (np.random.rand(*X.shape) > self.p) / (1 - self.p)
            return X * self.mask
        return X
    
    def backward(self, dout):
        return dout * self.mask


# Demostrar
np.random.seed(42)
X_demo = np.random.randn(4, 3)

linear = LinearLayer(3, 5)
bn = BatchNormLayer(5)
dropout = DropoutLayer(0.3)

# Forward
z1 = linear.forward(X_demo)
z2 = bn.forward(z1)
z3 = np.maximum(0, z2)  # ReLU
z4 = dropout.forward(z3)

print(f"  Input: {X_demo.shape}")
print(f"  Linear: {z1.shape}")
print(f"  BatchNorm: {z2.shape}")
print(f"  ReLU+Dropout: {z4.shape}")

# Backward (gradient de ceros excepto primera posicion)
dout = np.random.randn(*z4.shape)
dout_drop = dropout.backward(dout)
dout_relu = dout_drop * (z2 > 0)
dout_bn = bn.backward(dout_relu)
dout_linear = linear.backward(dout_bn)

print(f"  dX shape: {dout_linear.shape}")
print(f"  dW shape: {linear.dW.shape}")
print(f"  dgamma shape: {bn.dgamma.shape}")


# =====================================================================
#   PARTE 6: VANISHING/EXPLODING GRADIENTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: VANISHING/EXPLODING GRADIENTS ===")
print("=" * 80)

"""
Problema: gradientes se hacen 0 o infinito en redes profundas.

Vanishing: sigmoid/tanh squash gradientes. Capas profundas no aprenden.
Exploding: gradientes crecen exponencialmente. Training diverge.

SOLUCIONES:
1. ReLU (no satura para x > 0).
2. Inicializacion correcta (He, Xavier).
3. Batch normalization.
4. Residual connections (ResNet).
5. Gradient clipping.
"""

print("\n--- Demostrar vanishing con sigmoid ---")

def simulate_deep_network(n_layers, activation='sigmoid'):
    """Simular propagacion de gradientes en red profunda."""
    np.random.seed(42)
    dim = 10
    
    # Inicializar pesos
    weights = [np.random.randn(dim, dim) * 0.1 for _ in range(n_layers)]
    
    # Forward con activacion
    x = np.random.randn(1, dim)
    activations = [x]
    
    for W in weights:
        z = activations[-1] @ W
        if activation == 'sigmoid':
            a = 1 / (1 + np.exp(-z))
        elif activation == 'relu':
            a = np.maximum(0, z)
        elif activation == 'tanh':
            a = np.tanh(z)
        activations.append(a)
    
    # Backward: propagar gradiente = 1
    grad = np.ones_like(activations[-1])
    grad_norms = [np.linalg.norm(grad)]
    
    for i in range(n_layers - 1, -1, -1):
        a = activations[i + 1]
        if activation == 'sigmoid':
            local_grad = a * (1 - a)
        elif activation == 'relu':
            local_grad = (activations[i] @ weights[i] > 0).astype(float)
        elif activation == 'tanh':
            local_grad = 1 - a**2
        
        grad = grad * local_grad @ weights[i].T
        grad_norms.append(np.linalg.norm(grad))
    
    return grad_norms

for act in ['sigmoid', 'tanh', 'relu']:
    norms = simulate_deep_network(20, act)
    print(f"  {act:8s}: grad_norm final = {norms[-1]:.2e} "
          f"(ratio = {norms[-1]/max(norms[0], 1e-30):.2e})")


print("\n--- Gradient clipping ---")

def clip_grad_norm(grads, max_norm):
    """Gradient clipping por norma."""
    total_norm = np.sqrt(sum(np.sum(g**2) for g in grads))
    clip_coeff = max_norm / (total_norm + 1e-6)
    if clip_coeff < 1:
        grads = [g * clip_coeff for g in grads]
    return grads, total_norm

# Simular gradientes exploding
grads = [np.random.randn(10, 10) * 100 for _ in range(5)]
clipped, norm_before = clip_grad_norm(grads, max_norm=1.0)
norm_after = np.sqrt(sum(np.sum(g**2) for g in clipped))

print(f"\n  Norma antes: {norm_before:.2f}")
print(f"  Norma despues clip(1.0): {norm_after:.2f}")


print("\n--- Inicializacion correcta ---")

print("""
+------------------+---------------------------+---------------------------+
| METODO           | FORMULA                   | CUANDO USAR               |
+------------------+---------------------------+---------------------------+
| Xavier/Glorot    | std = sqrt(2/(fan_in+out)) | Sigmoid, Tanh             |
| He/Kaiming       | std = sqrt(2/fan_in)       | ReLU                      |
| LeCun            | std = sqrt(1/fan_in)       | SELU                      |
+------------------+---------------------------+---------------------------+
""")

fan_in, fan_out = 768, 256
xavier_std = np.sqrt(2.0 / (fan_in + fan_out))
he_std = np.sqrt(2.0 / fan_in)

W_xavier = np.random.randn(fan_in, fan_out) * xavier_std
W_he = np.random.randn(fan_in, fan_out) * he_std

print(f"  Xavier std: {xavier_std:.6f}, W std: {W_xavier.std():.6f}")
print(f"  He std:     {he_std:.6f}, W std: {W_he.std():.6f}")


# =====================================================================
#   PARTE 7: RESIDUAL CONNECTIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: RESIDUAL CONNECTIONS ===")
print("=" * 80)

"""
ResNet: y = F(x) + x

El gradiente fluye DIRECTAMENTE por el shortcut:
dy/dx = dF/dx + 1

El "+1" previene vanishing gradients.
"""

print("\n--- Residual block ---")

class ResidualBlock:
    def __init__(self, dim):
        self.linear1 = LinearLayer(dim, dim)
        self.linear2 = LinearLayer(dim, dim)
    
    def forward(self, x):
        self.x = x
        z = self.linear1.forward(x)
        z = np.maximum(0, z)  # ReLU
        z = self.linear2.forward(z)
        return z + x  # Residual connection
    
    def backward(self, dout):
        # Gradiente fluye por el shortcut directamente
        dz = self.linear2.backward(dout)
        dz = dz * (self.linear1.forward(self.x) > 0)  # ReLU backward
        dx_block = self.linear1.backward(dz)
        return dx_block + dout  # +dout es el gradiente del shortcut

# Comparar gradientes: con y sin residual
np.random.seed(42)
dim = 10
x_res = np.random.randn(1, dim)

# Sin residual (10 capas)
grad_no_res = np.ones((1, dim))
for _ in range(10):
    W = np.random.randn(dim, dim) * 0.5
    grad_no_res = grad_no_res @ W.T

# Con residual (10 capas)
grad_res = np.ones((1, dim))
for _ in range(10):
    W = np.random.randn(dim, dim) * 0.5
    grad_res = grad_res @ W.T + grad_res  # +grad_res es el shortcut

print(f"  Sin residual (10 capas): grad norm = {np.linalg.norm(grad_no_res):.6f}")
print(f"  Con residual (10 capas): grad norm = {np.linalg.norm(grad_res):.6f}")


# =====================================================================
#   PARTE 8: EJERCICIO — MLP COMPLETO CON AUTOGRAD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: EJERCICIO — MLP CON AUTOGRAD ===")
print("=" * 80)

"""
MLP completo: Linear -> ReLU -> Linear -> Softmax + CE Loss.
Con gradient checking.
"""

print("\n--- MLP completo ---")

class FullMLP:
    """MLP de 2 capas con forward/backward completo."""
    
    def __init__(self, dims):
        self.layers = []
        for i in range(len(dims) - 1):
            self.layers.append(LinearLayer(dims[i], dims[i + 1]))
    
    def forward(self, X):
        self.activations = [X]
        h = X
        for i, layer in enumerate(self.layers[:-1]):
            h = layer.forward(h)
            h = np.maximum(0, h)  # ReLU
            self.activations.append(h)
        
        # Ultima capa sin activacion (logits)
        logits = self.layers[-1].forward(h)
        
        # Softmax
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
        self.probs = exp_logits / exp_logits.sum(axis=1, keepdims=True)
        
        return self.probs
    
    def loss(self, y_true):
        n = len(y_true)
        correct_probs = self.probs[range(n), y_true]
        return -np.mean(np.log(correct_probs + 1e-15))
    
    def backward(self, y_true):
        n = len(y_true)
        
        # dL/d(logits) = probs - one_hot
        dlogits = self.probs.copy()
        dlogits[range(n), y_true] -= 1
        dlogits /= n
        
        # Backward por capas (en reversa)
        dh = self.layers[-1].backward(dlogits)
        
        for i in range(len(self.layers) - 2, -1, -1):
            # ReLU backward
            dh = dh * (self.activations[i + 1] > 0)
            dh = self.layers[i].backward(dh)
    
    def update(self, lr=0.01):
        for layer in self.layers:
            layer.W -= lr * layer.dW
            layer.b -= lr * layer.db
    
    def get_params(self):
        return [(l.W.copy(), l.b.copy()) for l in self.layers]

# Datos de clasificacion
np.random.seed(42)
N = 300
X_train = np.vstack([
    np.random.randn(100, 4) + [2, 0, 0, 0],
    np.random.randn(100, 4) + [0, 2, 0, 0],
    np.random.randn(100, 4) + [0, 0, 2, 0],
])
y_train = np.array([0]*100 + [1]*100 + [2]*100)

# Crear y entrenar
mlp = FullMLP([4, 32, 16, 3])

print(f"  Arquitectura: 4 -> 32 -> 16 -> 3")
print(f"  Parametros: {sum(l.W.size + l.b.size for l in mlp.layers)}")

for epoch in range(301):
    probs = mlp.forward(X_train)
    loss = mlp.loss(y_train)
    mlp.backward(y_train)
    mlp.update(lr=0.05)
    
    if epoch % 50 == 0:
        preds = np.argmax(probs, axis=1)
        acc = np.mean(preds == y_train)
        print(f"    Epoch {epoch:3d}: loss={loss:.4f}, acc={acc:.4f}")


print("\n--- Gradient checking del MLP ---")

def numerical_gradient_mlp(mlp, X, y, layer_idx, param_type, h=1e-5):
    """Gradiente numerico para verificar."""
    layer = mlp.layers[layer_idx]
    param = layer.W if param_type == 'W' else layer.b
    grad = np.zeros_like(param)
    
    it = np.nditer(param, flags=['multi_index'])
    while not it.finished:
        idx = it.multi_index
        old_val = param[idx]
        
        param[idx] = old_val + h
        mlp.forward(X)
        loss_plus = mlp.loss(y)
        
        param[idx] = old_val - h
        mlp.forward(X)
        loss_minus = mlp.loss(y)
        
        grad[idx] = (loss_plus - loss_minus) / (2 * h)
        param[idx] = old_val
        it.iternext()
    
    return grad

# Check gradientes de la primera capa (sobre subset)
X_small = X_train[:5]
y_small = y_train[:5]

mlp.forward(X_small)
mlp.backward(y_small)

grad_W0_ana = mlp.layers[0].dW
grad_W0_num = numerical_gradient_mlp(mlp, X_small, y_small, 0, 'W')

error = np.linalg.norm(grad_W0_ana - grad_W0_num) / (
    np.linalg.norm(grad_W0_ana) + np.linalg.norm(grad_W0_num) + 1e-15)

print(f"  Gradient check W0: error = {error:.2e} {'PASS' if error < 1e-4 else 'FAIL'}")


# =====================================================================
#   PARTE 9: LAYER NORMALIZATION BACKWARD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: LAYER NORMALIZATION ===")
print("=" * 80)

"""
LayerNorm: normaliza sobre features (no batch).
Usado en Transformers porque no depende del batch size.

y = gamma * (x - mean) / sqrt(var + eps) + beta
mean/var sobre la dimension de features.
"""

print("\n--- LayerNorm con backward ---")

class LayerNormLayer:
    def __init__(self, dim, eps=1e-5):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)
        self.eps = eps
    
    def forward(self, X):
        self.X = X
        self.mean = X.mean(axis=-1, keepdims=True)
        self.var = X.var(axis=-1, keepdims=True)
        self.std = np.sqrt(self.var + self.eps)
        self.X_norm = (X - self.mean) / self.std
        return self.gamma * self.X_norm + self.beta
    
    def backward(self, dout):
        n = self.X.shape[-1]
        
        self.dgamma = (dout * self.X_norm).sum(axis=0)
        self.dbeta = dout.sum(axis=0)
        
        dX_norm = dout * self.gamma
        dmean = -dX_norm.sum(axis=-1, keepdims=True) / self.std
        dvar = (-0.5 * dX_norm * (self.X - self.mean) / (self.std**3)).sum(axis=-1, keepdims=True)
        
        dX = dX_norm / self.std + dvar * 2 * (self.X - self.mean) / n + dmean / n
        return dX

# Test
np.random.seed(42)
X_ln = np.random.randn(4, 8)
ln = LayerNormLayer(8)

out = ln.forward(X_ln)
print(f"  Input mean per sample: {X_ln.mean(axis=1)}")
print(f"  Output mean per sample: {out.mean(axis=1)}")
print(f"  Output std per sample: {out.std(axis=1)}")

dout = np.random.randn(4, 8)
dX = ln.backward(dout)
print(f"  dX shape: {dX.shape}")


# =====================================================================
#   PARTE 10: ACTIVACIONES AVANZADAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: ACTIVACIONES AVANZADAS ===")
print("=" * 80)

"""
Activaciones modernas usadas en Transformers:
- GELU: Gaussian Error Linear Unit.
- SiLU/Swish: x * sigmoid(x).
- Leaky ReLU, ELU, Mish.
"""

print("\n--- GELU (Gaussian Error Linear Unit) ---")

def gelu(x):
    """GELU: x * Φ(x) donde Φ es CDF de la normal."""
    return x * 0.5 * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)))

def gelu_deriv(x, h=1e-5):
    """Derivada numerica de GELU."""
    return (gelu(x + h) - gelu(x - h)) / (2 * h)

def silu(x):
    """SiLU/Swish: x * sigmoid(x)."""
    s = 1 / (1 + np.exp(-x))
    return x * s

def silu_deriv(x):
    s = 1 / (1 + np.exp(-x))
    return s + x * s * (1 - s)

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def leaky_relu_deriv(x, alpha=0.01):
    return np.where(x > 0, 1.0, alpha)

x_vals = np.linspace(-3, 3, 7)
print(f"  {'x':>6s}  {'GELU':>8s}  {'GELU_d':>8s}  {'SiLU':>8s}  {'SiLU_d':>8s}  {'LeakyR':>8s}")
for x in x_vals:
    print(f"  {x:6.2f}  {gelu(x):8.4f}  {gelu_deriv(x):8.4f}  "
          f"{silu(x):8.4f}  {silu_deriv(x):8.4f}  {leaky_relu(x):8.4f}")


print("\n--- GELU vs ReLU ---")
print("""
  GELU:
    - Suave (diferenciable en todo punto).
    - Usado en GPT, BERT, ViT.
    - Permite gradientes pequeños para x < 0.
    
  ReLU:
    - No diferenciable en x=0.
    - Gradiente exactamente 0 para x < 0 (dead neurons).
    - Mas rapido de computar.
""")


# =====================================================================
#   PARTE 11: ATTENTION BACKWARD COMPLETO
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 11: ATTENTION BACKWARD ===")
print("=" * 80)

"""
Backward de scaled dot-product attention:
  attn = softmax(Q @ K^T / sqrt(d)) @ V

Necesitamos: dQ, dK, dV.
"""

print("\n--- Attention forward + backward ---")

def attention_forward(Q, K, V):
    """Scaled dot-product attention."""
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)
    
    # Softmax
    exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    attn_weights = exp_scores / exp_scores.sum(axis=-1, keepdims=True)
    
    output = attn_weights @ V
    
    return output, attn_weights, scores

def attention_backward(dout, Q, K, V, attn_weights):
    """Backward de attention."""
    d_k = Q.shape[-1]
    
    # dV = attn_weights^T @ dout
    dV = attn_weights.T @ dout
    
    # d(attn_weights) = dout @ V^T
    dattn = dout @ V.T
    
    # d(softmax): dscore_i = attn_i * (dattn_i - sum_j(attn_j * dattn_j))
    dscores = attn_weights * (dattn - (attn_weights * dattn).sum(axis=-1, keepdims=True))
    
    # Scale
    dscores /= np.sqrt(d_k)
    
    # dQ = dscores @ K
    dQ = dscores @ K
    
    # dK = dscores^T @ Q
    dK = dscores.T @ Q
    
    return dQ, dK, dV

# Test
np.random.seed(42)
seq_len, d_model = 5, 8
Q = np.random.randn(seq_len, d_model)
K = np.random.randn(seq_len, d_model)
V = np.random.randn(seq_len, d_model)

out, weights, scores = attention_forward(Q, K, V)
dout = np.random.randn(*out.shape)
dQ, dK, dV = attention_backward(dout, Q, K, V, weights)

print(f"  Q: {Q.shape}, K: {K.shape}, V: {V.shape}")
print(f"  Output: {out.shape}")
print(f"  dQ: {dQ.shape}, dK: {dK.shape}, dV: {dV.shape}")

# Gradient check para dQ
def attn_loss_Q(Q_flat):
    Q_r = Q_flat.reshape(Q.shape)
    o, _, _ = attention_forward(Q_r, K, V)
    return np.sum(o * dout)

from functools import partial
dQ_num = np.zeros_like(Q)
h = 1e-5
for i in range(Q.size):
    Q_flat = Q.flatten()
    Q_flat_p = Q_flat.copy(); Q_flat_p[i] += h
    Q_flat_m = Q_flat.copy(); Q_flat_m[i] -= h
    dQ_num.flat[i] = (attn_loss_Q(Q_flat_p) - attn_loss_Q(Q_flat_m)) / (2*h)

err_Q = np.linalg.norm(dQ - dQ_num) / (np.linalg.norm(dQ) + np.linalg.norm(dQ_num) + 1e-15)
print(f"  Gradient check dQ: error = {err_Q:.2e} {'PASS' if err_Q < 1e-4 else 'FAIL'}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE BACKPROPAGATION:

1. Grafo computacional: DAG de operaciones.

2. Autograd: registrar operaciones, propagar gradientes.

3. Value (micrograd): autograd para escalares.

4. Tensor autograd: matmul, add, relu con backward.

5. Capas: Linear, BatchNorm, LayerNorm, Dropout.

6. Vanishing gradients: sigmoid/tanh saturan. Usar ReLU/GELU.

7. Gradient clipping + inicializacion He/Xavier.

8. Residual connections: shortcut previene vanishing.

9. Attention backward: dQ, dK, dV completos.

10. GELU/SiLU: activaciones modernas para Transformers.

FIN DEL MODULO 08: CALCULO Y OPTIMIZACION.
"""

print("\n FIN DE ARCHIVO 03_backpropagation_y_autograd.")
print(" Backpropagation y autograd han sido dominados.")
print(" Siguiente modulo: PROBABILIDAD Y ESTADISTICA.")
