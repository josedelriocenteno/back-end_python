# ===========================================================================
# 02_redes_neuronales_basicas.py
# ===========================================================================
# MODULO 17: PYTORCH FUNDAMENTOS
# ARCHIVO 02: Redes Neuronales Basicas — Del Perceptron al MLP
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Construir redes neuronales desde los fundamentos: perceptron,
# redes multicapa, funciones de activacion en profundidad,
# backpropagation manual vs autograd, y arquitecturas practicas.
#
# CONTENIDO:
#   1. Perceptron desde cero (sin PyTorch).
#   2. Perceptron con PyTorch.
#   3. Funciones de activacion: matematicas y cuando usar cada una.
#   4. MLP (Multi-Layer Perceptron) paso a paso.
#   5. Backpropagation manual: la matematica.
#   6. Backpropagation con autograd: la magia.
#   7. Inicializacion de pesos: por que importa.
#   8. Batch Normalization: que hace y por que funciona.
#   9. Dropout: regularizacion estocástica.
#   10. Arquitecturas MLP para clasificacion y regresion.
#   11. Debugging de redes neuronales.
#   12. Ejercicio: MLP para dataset real.
#
# NIVEL: ARQUITECTO ML / DEEP LEARNING ENGINEER.
# ===========================================================================

import numpy as np
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import Dataset, DataLoader, TensorDataset
    HAS_TORCH = True
    print(f"  PyTorch version: {torch.__version__}")
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
except ImportError:
    HAS_TORCH = False
    print("  PyTorch not installed. Conceptual mode.")


# =====================================================================
#   PARTE 1: PERCEPTRON DESDE CERO (SIN PYTORCH)
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: PERCEPTRON — EL ATOMO DE DEEP LEARNING ===")
print("=" * 80)

"""
EL PERCEPTRON (Rosenblatt, 1958):

La unidad MAS SIMPLE de una red neuronal.

MATEMATICA:
  z = w₁x₁ + w₂x₂ + ... + wₙxₙ + b = w·x + b
  y = σ(z)   donde σ es una funcion de activacion

Para clasificacion binaria:
  y = 1 si z > 0
  y = 0 si z <= 0

LIMITACION FUNDAMENTAL:
  Un perceptron solo puede separar clases LINEALMENTE.
  No puede aprender XOR (Minsky & Papert, 1969).
  → Necesitas MULTIPLES capas (MLP) para problemas no-lineales.

PERO: entender el perceptron es entender TODA red neuronal,
porque cada neurona de un transformer ES un perceptron con activacion.
"""

print("\n--- Perceptron desde cero (numpy) ---")


class PerceptronNumpy:
    """Perceptron implementado solo con numpy."""

    def __init__(self, n_features: int, lr: float = 0.01):
        # Inicializar pesos pequenos aleatorios
        np.random.seed(42)
        self.weights = np.random.randn(n_features) * 0.01
        self.bias = 0.0
        self.lr = lr
        self.losses = []

    def sigmoid(self, z):
        """σ(z) = 1 / (1 + e^(-z))"""
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

    def forward(self, X):
        """z = Xw + b, y = σ(z)"""
        z = X @ self.weights + self.bias
        return self.sigmoid(z)

    def predict(self, X):
        """Clase predicha: 1 si prob > 0.5"""
        return (self.forward(X) > 0.5).astype(int)

    def fit(self, X, y, epochs=100, verbose=True):
        """
        Gradient Descent:
          dL/dw = (1/N) * X^T @ (y_pred - y)
          dL/db = (1/N) * sum(y_pred - y)
        """
        for epoch in range(epochs):
            # Forward
            y_pred = self.forward(X)

            # Loss (binary cross-entropy)
            eps = 1e-15
            loss = -np.mean(y * np.log(y_pred + eps) +
                           (1 - y) * np.log(1 - y_pred + eps))
            self.losses.append(loss)

            # Backward (gradientes manuales)
            error = y_pred - y  # dL/dz
            grad_w = (X.T @ error) / len(y)  # dL/dw
            grad_b = np.mean(error)  # dL/db

            # Update
            self.weights -= self.lr * grad_w
            self.bias -= self.lr * grad_b

            if verbose and epoch % 20 == 0:
                acc = np.mean(self.predict(X) == y)
                print(f"    epoch {epoch:3d}: loss={loss:.4f}, acc={acc:.4f}")

        return self


# Demo: clasificacion lineal
np.random.seed(42)
N = 200
X_linear = np.random.randn(N, 2)
y_linear = (X_linear[:, 0] + X_linear[:, 1] > 0).astype(int)

perceptron = PerceptronNumpy(n_features=2, lr=0.1)
perceptron.fit(X_linear, y_linear, epochs=100)

acc = np.mean(perceptron.predict(X_linear) == y_linear)
print(f"\n  Perceptron accuracy (linear data): {acc:.4f}")
print(f"  Pesos aprendidos: w={perceptron.weights.round(3)}, b={perceptron.bias:.3f}")


# Demo: XOR (falla!)
print("\n--- XOR: el limite del perceptron ---")
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y_xor = np.array([0, 1, 1, 0])

perceptron_xor = PerceptronNumpy(n_features=2, lr=0.5)
perceptron_xor.fit(X_xor, y_xor, epochs=200, verbose=False)

preds_xor = perceptron_xor.predict(X_xor)
print(f"  XOR predictions: {preds_xor} (expected: [0, 1, 1, 0])")
print(f"  XOR accuracy: {np.mean(preds_xor == y_xor):.2f}")
print(f"  → FALLA: XOR no es linealmente separable")
print(f"  → Necesitamos capas ocultas (MLP)")


# =====================================================================
#   PARTE 2: PERCEPTRON CON PYTORCH
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: PERCEPTRON CON PYTORCH ===")
print("=" * 80)

"""
El mismo perceptron, pero con PyTorch:
  - nn.Linear: capa lineal (w·x + b).
  - autograd: calcula gradientes automaticamente.
  - optimizer: actualiza pesos.

COMPARACION:
  NumPy: calculas gradientes a mano (grad_w = X.T @ error / N).
  PyTorch: loss.backward() → gradientes automaticos para TODO.
"""

if HAS_TORCH:
    print("\n--- Perceptron PyTorch ---")

    # Datos
    X_t = torch.tensor(X_linear, dtype=torch.float32)
    y_t = torch.tensor(y_linear, dtype=torch.float32)

    # Modelo: una sola capa lineal + sigmoid
    class PerceptronTorch(nn.Module):
        def __init__(self, n_features):
            super().__init__()
            self.linear = nn.Linear(n_features, 1)

        def forward(self, x):
            return torch.sigmoid(self.linear(x)).squeeze()

    model = PerceptronTorch(2)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    criterion = nn.BCELoss()

    for epoch in range(100):
        optimizer.zero_grad()
        y_pred = model(X_t)
        loss = criterion(y_pred, y_t)
        loss.backward()
        optimizer.step()

        if epoch % 25 == 0:
            acc = ((y_pred > 0.5).float() == y_t).float().mean()
            print(f"    epoch {epoch:3d}: loss={loss.item():.4f}, acc={acc.item():.4f}")

    # XOR con PyTorch (tambien falla)
    X_xor_t = torch.tensor(X_xor, dtype=torch.float32)
    y_xor_t = torch.tensor(y_xor, dtype=torch.float32)

    model_xor = PerceptronTorch(2)
    opt_xor = torch.optim.SGD(model_xor.parameters(), lr=0.5)

    for epoch in range(500):
        opt_xor.zero_grad()
        loss = nn.BCELoss()(model_xor(X_xor_t), y_xor_t)
        loss.backward()
        opt_xor.step()

    preds = (model_xor(X_xor_t) > 0.5).int()
    print(f"\n  XOR con perceptron PyTorch: {preds.flatten().tolist()}")
    print(f"  → Sigue fallando. Necesitamos capas ocultas.")


# =====================================================================
#   PARTE 3: FUNCIONES DE ACTIVACION EN PROFUNDIDAD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: FUNCIONES DE ACTIVACION ===")
print("=" * 80)

"""
SIN activacion, una red de N capas es equivalente a UNA capa lineal:
  f(x) = W3 @ W2 @ W1 @ x = W_total @ x
  → No importa cuantas capas pongas, sigue siendo LINEAL.

La activacion introduce NO-LINEALIDAD → la red puede aproximar
CUALQUIER funcion (Universal Approximation Theorem).

FUNCIONES PRINCIPALES:

1. SIGMOID: σ(z) = 1/(1+e^(-z))
   Rango: (0, 1). Util para probabilidades.
   PROBLEMA: vanishing gradient en valores extremos.
   USO: capa de salida para clasificacion binaria.

2. TANH: tanh(z) = (e^z - e^(-z)) / (e^z + e^(-z))
   Rango: (-1, 1). Centrado en 0 (mejor que sigmoid).
   PROBLEMA: tambien vanishing gradient.
   USO: RNNs (historicamente).

3. RELU: max(0, z)
   Rango: [0, ∞). Simple y efectivo.
   PROBLEMA: "dying ReLU" — neuronas que siempre dan 0.
   USO: DEFAULT para capas ocultas de redes profundas.

4. LEAKY RELU: max(αz, z) donde α=0.01
   Rango: (-∞, ∞). Evita dying ReLU.
   USO: alternativa a ReLU cuando hay dying neurons.

5. GELU: z * Φ(z) donde Φ es la CDF de la normal.
   Rango: (-0.17, ∞). Suave, diferenciable.
   USO: Transformers (BERT, GPT). Estado del arte.

6. SWISH/SiLU: z * σ(z)
   Similar a GELU. Usada en EfficientNet, LLMs modernos.

7. SOFTMAX: e^zi / Σe^zj
   Rango: (0, 1), suma = 1. Distribucion de probabilidad.
   USO: capa de salida para clasificacion multiclase.
"""

if HAS_TORCH:
    z = torch.linspace(-5, 5, 100)

    activations = {
        'Sigmoid': torch.sigmoid(z),
        'Tanh': torch.tanh(z),
        'ReLU': F.relu(z),
        'LeakyReLU': F.leaky_relu(z, 0.1),
        'GELU': F.gelu(z),
        'SiLU/Swish': F.silu(z),
    }

    print(f"\n  {'Activation':<15} {'Min':>8} {'Max':>8} {'Mean':>8} {'Non-zero%':>10}")
    for name, values in activations.items():
        nz = (values.abs() > 1e-6).float().mean() * 100
        print(f"  {name:<15} {values.min().item():8.3f} {values.max().item():8.3f} "
              f"{values.mean().item():8.3f} {nz.item():10.1f}%")

    # Gradientes de activaciones
    print(f"\n  Gradientes en z=0 y z=3:")
    for name, act_fn in [('Sigmoid', torch.sigmoid), ('Tanh', torch.tanh),
                          ('ReLU', F.relu), ('GELU', F.gelu)]:
        for z_val in [0.0, 3.0]:
            z_t = torch.tensor(z_val, requires_grad=True)
            out = act_fn(z_t)
            out.backward()
            print(f"    {name}({z_val}): grad={z_t.grad.item():.4f}")


# =====================================================================
#   PARTE 4: MLP — MULTI-LAYER PERCEPTRON
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: MLP — RESUELVE XOR Y MUCHO MAS ===")
print("=" * 80)

"""
MLP: stack de capas lineales con activaciones no-lineales entre ellas.

Arquitectura:
  Input → Linear(in, hidden) → ReLU → Linear(hidden, out) → Output

Con UNA capa oculta y suficientes neuronas, un MLP puede aproximar
CUALQUIER funcion continua (Universal Approximation Theorem).

PERO: "puede aproximar" no significa "puede aprender eficientemente".
Las redes profundas (muchas capas) son mas eficientes en la practica.
"""

if HAS_TORCH:
    print("\n--- MLP resuelve XOR ---")

    class MLPxor(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(2, 8),
                nn.ReLU(),
                nn.Linear(8, 1),
                nn.Sigmoid(),
            )

        def forward(self, x):
            return self.net(x).squeeze()

    torch.manual_seed(42)
    mlp_xor = MLPxor()
    optimizer = torch.optim.Adam(mlp_xor.parameters(), lr=0.01)
    criterion = nn.BCELoss()

    for epoch in range(1000):
        optimizer.zero_grad()
        pred = mlp_xor(X_xor_t)
        loss = criterion(pred, y_xor_t)
        loss.backward()
        optimizer.step()

    preds_mlp = (mlp_xor(X_xor_t) > 0.5).int()
    print(f"  XOR con MLP: {preds_mlp.flatten().tolist()}")
    print(f"  Expected:    [0, 1, 1, 0]")
    print(f"  → MLP RESUELVE XOR con una capa oculta!")

    # Veamos que aprendio la capa oculta
    with torch.no_grad():
        hidden_out = torch.relu(mlp_xor.net[0](X_xor_t))
        print(f"\n  Representacion oculta (8 neuronas):")
        for i, (x, h) in enumerate(zip(X_xor, hidden_out)):
            print(f"    x={x} → hidden={h.numpy().round(2)}")
        print(f"  → La capa oculta TRANSFORMA el espacio para que sea separable")


# =====================================================================
#   PARTE 5: BACKPROPAGATION MANUAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: BACKPROPAGATION — LA MATEMATICA ===")
print("=" * 80)

"""
BACKPROP: algoritmo para calcular gradientes eficientemente.

Para una red de 2 capas:
  z1 = W1 @ x + b1          (pre-activacion capa 1)
  a1 = ReLU(z1)              (post-activacion capa 1)
  z2 = W2 @ a1 + b2          (pre-activacion capa 2)
  y_pred = sigmoid(z2)       (output)
  L = BCE(y_pred, y_true)    (loss)

FORWARD: calcula output de izquierda a derecha.
BACKWARD: calcula gradientes de derecha a izquierda (chain rule).

  dL/dz2 = y_pred - y_true
  dL/dW2 = dL/dz2 @ a1.T
  dL/db2 = dL/dz2
  dL/da1 = W2.T @ dL/dz2
  dL/dz1 = dL/da1 * (z1 > 0)  [derivada de ReLU]
  dL/dW1 = dL/dz1 @ x.T
  dL/db1 = dL/dz1
"""

print("\n--- Backprop manual (numpy) ---")

np.random.seed(42)
# Red de 2 capas: 2 → 4 → 1
W1 = np.random.randn(4, 2) * 0.5
b1 = np.zeros(4)
W2 = np.random.randn(1, 4) * 0.5
b2 = np.zeros(1)

lr_manual = 0.1

def sigmoid_np(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

# Entrenar en XOR
X_bp = X_xor.copy()
y_bp = y_xor.copy().reshape(-1, 1)

for epoch in range(2000):
    # === FORWARD ===
    z1 = X_bp @ W1.T + b1              # (4, 4)
    a1 = np.maximum(0, z1)             # ReLU
    z2 = a1 @ W2.T + b2               # (4, 1)
    y_pred = sigmoid_np(z2)            # (4, 1)

    # Loss (BCE)
    eps = 1e-15
    loss = -np.mean(y_bp * np.log(y_pred + eps) +
                    (1 - y_bp) * np.log(1 - y_pred + eps))

    # === BACKWARD ===
    dz2 = y_pred - y_bp                # (4, 1)
    dW2 = dz2.T @ a1 / len(X_bp)      # (1, 4)
    db2 = np.mean(dz2, axis=0)         # (1,)
    da1 = dz2 @ W2                     # (4, 4)
    dz1 = da1 * (z1 > 0)              # ReLU derivative
    dW1 = dz1.T @ X_bp / len(X_bp)    # (4, 2)
    db1 = np.mean(dz1, axis=0)         # (4,)

    # === UPDATE ===
    W2 -= lr_manual * dW2
    b2 -= lr_manual * db2
    W1 -= lr_manual * dW1
    b1 -= lr_manual * db1

    if epoch % 500 == 0:
        print(f"    epoch {epoch:4d}: loss={loss:.4f}")

preds_manual = (sigmoid_np(np.maximum(0, X_bp @ W1.T + b1) @ W2.T + b2) > 0.5).astype(int)
print(f"\n  XOR manual backprop: {preds_manual.flatten().tolist()}")
print(f"  → Backprop manual funciona, pero es TEDIOSO")
print(f"  → Autograd lo hace automaticamente para CUALQUIER red")


# =====================================================================
#   PARTE 6: AUTOGRAD vs MANUAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: AUTOGRAD — NUNCA MAS GRADIENTES MANUALES ===")
print("=" * 80)

"""
AUTOGRAD construye un grafo computacional y aplica chain rule
automaticamente. Cada operacion de tensor se registra.

VENTAJAS:
1. No necesitas calcular derivadas a mano.
2. Funciona para CUALQUIER arquitectura (CNN, RNN, Transformer).
3. Soporta grafos dinamicos (a diferencia de TF 1.x).
4. Eficiente: gradientes se calculan en un solo backward pass.
"""

if HAS_TORCH:
    print("\n--- Comparacion: gradiente manual vs autograd ---")

    # Funcion: f(x) = x³ + 2x² - 5x + 3
    # Derivada: f'(x) = 3x² + 4x - 5

    x_val = 2.0

    # Manual
    manual_grad = 3 * x_val**2 + 4 * x_val - 5
    print(f"  f'({x_val}) manual: {manual_grad}")

    # Autograd
    x_auto = torch.tensor(x_val, requires_grad=True)
    f = x_auto**3 + 2 * x_auto**2 - 5 * x_auto + 3
    f.backward()
    print(f"  f'({x_val}) autograd: {x_auto.grad.item()}")
    print(f"  Match: {abs(manual_grad - x_auto.grad.item()) < 1e-6}")

    # Autograd con operaciones complejas
    print("\n--- Autograd con red completa ---")

    torch.manual_seed(42)
    net = nn.Sequential(
        nn.Linear(2, 8), nn.ReLU(),
        nn.Linear(8, 4), nn.ReLU(),
        nn.Linear(4, 1), nn.Sigmoid(),
    )

    x_in = torch.randn(1, 2)
    target = torch.tensor([[1.0]])

    out = net(x_in)
    loss = nn.BCELoss()(out, target)
    loss.backward()

    print(f"  Red de 3 capas:")
    for name, param in net.named_parameters():
        if param.grad is not None:
            print(f"    {name}: shape={param.shape}, "
                  f"grad_norm={param.grad.norm().item():.6f}")
    print(f"  → Autograd calculo gradientes para {sum(p.numel() for p in net.parameters())} parametros")


# =====================================================================
#   PARTE 7: INICIALIZACION DE PESOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: INICIALIZACION — DONDE EMPIEZA TODO ===")
print("=" * 80)

"""
PROBLEMA: si inicializas MAL los pesos, la red no aprende.

1. ZEROS: todos los pesos = 0.
   → Todas las neuronas aprenden lo MISMO (simetria).
   → La red se comporta como una sola neurona. DESASTRE.

2. RANDOM GRANDE: pesos ~ N(0, 10).
   → Activaciones saturan (sigmoid → 0 o 1).
   → Gradientes → 0 (vanishing gradient).

3. RANDOM PEQUENO: pesos ~ N(0, 0.001).
   → Activaciones colapsan a 0.
   → Gradientes → 0. Otra vez no aprende.

SOLUCIONES:

XAVIER/GLOROT (2010): W ~ N(0, 2/(fan_in + fan_out))
  Diseñada para sigmoid/tanh.
  Mantiene varianza de activaciones entre capas.

KAIMING/HE (2015): W ~ N(0, 2/fan_in)
  Diseñada para ReLU.
  Compensa que ReLU elimina la mitad de las activaciones.

REGLA:
  ReLU → Kaiming (He).
  Sigmoid/Tanh → Xavier (Glorot).
  PyTorch usa Kaiming por defecto en nn.Linear.
"""

if HAS_TORCH:
    print("\n--- Efecto de inicializacion ---")

    # Red profunda (10 capas) para ver el efecto
    def check_activations(init_fn, name):
        torch.manual_seed(42)
        layers = []
        for i in range(10):
            l = nn.Linear(64, 64)
            init_fn(l.weight)
            nn.init.zeros_(l.bias)
            layers.append(l)

        # Forward pass con input aleatorio
        x = torch.randn(32, 64)
        act_stats = []
        for layer in layers:
            x = torch.relu(layer(x))
            act_stats.append((x.mean().item(), x.std().item()))

        print(f"\n  {name}:")
        print(f"    {'Layer':<8} {'Mean':>8} {'Std':>8}")
        for i, (mean, std) in enumerate(act_stats):
            marker = " ← dead!" if std < 1e-6 else ""
            print(f"    {i+1:<8} {mean:8.4f} {std:8.4f}{marker}")

    check_activations(lambda w: nn.init.normal_(w, 0, 0.001), "Small init (0.001)")
    check_activations(lambda w: nn.init.normal_(w, 0, 1.0), "Large init (1.0)")
    check_activations(lambda w: nn.init.kaiming_normal_(w, mode='fan_in'), "Kaiming (correcto)")
    check_activations(lambda w: nn.init.xavier_normal_(w), "Xavier")


# =====================================================================
#   PARTE 8: BATCH NORMALIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: BATCH NORMALIZATION ===")
print("=" * 80)

"""
BATCH NORMALIZATION (Ioffe & Szegedy, 2015):

IDEA: normalizar las activaciones de cada capa para que tengan
mean=0 y std=1, luego escalar con parametros aprendidos.

FORMULA:
  x_norm = (x - μ_batch) / (σ_batch + ε)
  y = γ * x_norm + β   (γ y β son aprendidos)

POR QUE FUNCIONA:
  1. Reduce "internal covariate shift".
  2. Permite learning rates mas altos.
  3. Actua como regularizador (ruido del batch).
  4. Hace el entrenamiento MUCHO mas estable.

DONDE PONERLO:
  Linear → BatchNorm → ReLU (mas comun)
  o
  Linear → ReLU → BatchNorm (tambien funciona)

IMPORTANTE:
  En inference, usa la MEDIA MOVIL (no el batch).
  model.eval() activa este modo.
"""

if HAS_TORCH:
    print("\n--- BatchNorm: con vs sin ---")

    class MLPNoBN(nn.Module):
        def __init__(self, input_dim=20, hidden=128):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, hidden), nn.ReLU(),
                nn.Linear(hidden, hidden), nn.ReLU(),
                nn.Linear(hidden, hidden), nn.ReLU(),
                nn.Linear(hidden, 2),
            )
        def forward(self, x):
            return self.net(x)

    class MLPWithBN(nn.Module):
        def __init__(self, input_dim=20, hidden=128):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, hidden), nn.BatchNorm1d(hidden), nn.ReLU(),
                nn.Linear(hidden, hidden), nn.BatchNorm1d(hidden), nn.ReLU(),
                nn.Linear(hidden, hidden), nn.BatchNorm1d(hidden), nn.ReLU(),
                nn.Linear(hidden, 2),
            )
        def forward(self, x):
            return self.net(x)

    # Datos de clasificacion
    from sklearn.datasets import make_classification
    X_cls, y_cls = make_classification(1000, 20, n_informative=10, random_state=42)
    X_t = torch.tensor(X_cls, dtype=torch.float32)
    y_t = torch.tensor(y_cls, dtype=torch.long)
    dataset = TensorDataset(X_t, y_t)
    loader = DataLoader(dataset, batch_size=64, shuffle=True)

    def train_model(model, loader, epochs=20, lr=0.01):
        optimizer = torch.optim.SGD(model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        losses = []
        for epoch in range(epochs):
            epoch_loss = 0
            for xb, yb in loader:
                optimizer.zero_grad()
                out = model(xb)
                loss = criterion(out, yb)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()
            losses.append(epoch_loss / len(loader))
        return losses

    torch.manual_seed(42)
    model_no_bn = MLPNoBN()
    losses_no_bn = train_model(model_no_bn, loader, epochs=20, lr=0.01)

    torch.manual_seed(42)
    model_bn = MLPWithBN()
    losses_bn = train_model(model_bn, loader, epochs=20, lr=0.01)

    print(f"  {'Epoch':<8} {'Sin BN':>10} {'Con BN':>10}")
    for i in [0, 4, 9, 14, 19]:
        print(f"  {i+1:<8} {losses_no_bn[i]:10.4f} {losses_bn[i]:10.4f}")

    print(f"\n  → BatchNorm converge mas rapido y es mas estable")


# =====================================================================
#   PARTE 9: DROPOUT — REGULARIZACION ESTOCASTICA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: DROPOUT ===")
print("=" * 80)

"""
DROPOUT (Srivastava et al., 2014):

IDEA: durante training, APAGAR neuronas aleatoriamente con prob p.
  Cada mini-batch ve una RED DIFERENTE.
  → Previene co-adaptacion de neuronas.
  → Equivalente aproximado a un ENSEMBLE de sub-redes.

REGLA:
  p=0.5 para capas ocultas (clasico).
  p=0.1-0.3 para redes modernas (transformers).
  NUNCA dropout en la capa de salida.

IMPORTANTE:
  En training: dropout activo (apaga neuronas).
  En inference: dropout OFF + escalar por (1-p).
  PyTorch maneja esto con model.train() / model.eval().
"""

if HAS_TORCH:
    print("\n--- Dropout: overfitting control ---")

    class MLPDropout(nn.Module):
        def __init__(self, input_dim=20, hidden=128, dropout=0.5):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, hidden), nn.ReLU(), nn.Dropout(dropout),
                nn.Linear(hidden, hidden), nn.ReLU(), nn.Dropout(dropout),
                nn.Linear(hidden, 2),
            )
        def forward(self, x):
            return self.net(x)

    # Comparar train vs eval mode
    torch.manual_seed(42)
    model_drop = MLPDropout(dropout=0.5)
    x_test = torch.randn(1, 20)

    model_drop.train()
    outputs_train = [model_drop(x_test).detach() for _ in range(5)]
    print(f"  Train mode (dropout ON):")
    for i, out in enumerate(outputs_train):
        print(f"    Run {i+1}: {out.numpy().round(4)}")
    print(f"  → Diferentes cada vez (estocastico)")

    model_drop.eval()
    outputs_eval = [model_drop(x_test).detach() for _ in range(3)]
    print(f"\n  Eval mode (dropout OFF):")
    for i, out in enumerate(outputs_eval):
        print(f"    Run {i+1}: {out.numpy().round(4)}")
    print(f"  → Siempre igual (determinista)")


# =====================================================================
#   PARTE 10: MLP COMPLETO PARA CLASIFICACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: MLP PROFESIONAL COMPLETO ===")
print("=" * 80)

"""
MLP de produccion incluye:
  - BatchNorm para estabilidad.
  - Dropout para regularizacion.
  - Inicializacion correcta.
  - Learning rate scheduling.
  - Early stopping.
  - Logging de metricas.
"""

if HAS_TORCH:
    class ProfessionalMLP(nn.Module):
        """MLP con todas las best practices."""

        def __init__(self, input_dim, hidden_dims, output_dim,
                     dropout=0.3, use_batchnorm=True):
            super().__init__()

            layers = []
            prev_dim = input_dim
            for h_dim in hidden_dims:
                layers.append(nn.Linear(prev_dim, h_dim))
                if use_batchnorm:
                    layers.append(nn.BatchNorm1d(h_dim))
                layers.append(nn.GELU())  # Activacion moderna
                layers.append(nn.Dropout(dropout))
                prev_dim = h_dim

            layers.append(nn.Linear(prev_dim, output_dim))
            self.network = nn.Sequential(*layers)

            # Inicializacion Kaiming
            self._init_weights()

        def _init_weights(self):
            for m in self.modules():
                if isinstance(m, nn.Linear):
                    nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
                    if m.bias is not None:
                        nn.init.zeros_(m.bias)

        def forward(self, x):
            return self.network(x)

    # Entrenamiento completo
    print("\n--- Entrenamiento profesional ---")

    torch.manual_seed(42)
    model_pro = ProfessionalMLP(
        input_dim=20, hidden_dims=[128, 64, 32], output_dim=2,
        dropout=0.3, use_batchnorm=True
    )

    n_params = sum(p.numel() for p in model_pro.parameters())
    print(f"  Modelo: {n_params:,} parametros")
    print(f"  Arquitectura: 20 → 128 → 64 → 32 → 2")

    # Split
    X_train, X_val = X_t[:800], X_t[800:]
    y_train, y_val = y_t[:800], y_t[800:]

    train_ds = TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)

    optimizer = torch.optim.AdamW(model_pro.parameters(), lr=0.001, weight_decay=0.01)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=30)
    criterion = nn.CrossEntropyLoss()

    best_val_acc = 0
    patience = 5
    patience_counter = 0

    print(f"\n  {'Epoch':<8} {'TrainLoss':>10} {'ValAcc':>8} {'LR':>10}")

    for epoch in range(30):
        # Train
        model_pro.train()
        total_loss = 0
        for xb, yb in train_loader:
            optimizer.zero_grad()
            out = model_pro(xb)
            loss = criterion(out, yb)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model_pro.parameters(), 1.0)
            optimizer.step()
            total_loss += loss.item()

        # Validate
        model_pro.eval()
        with torch.no_grad():
            val_out = model_pro(X_val)
            val_acc = (val_out.argmax(1) == y_val).float().mean().item()

        avg_loss = total_loss / len(train_loader)
        lr = scheduler.get_last_lr()[0]
        scheduler.step()

        if epoch % 5 == 0:
            print(f"  {epoch+1:<8} {avg_loss:10.4f} {val_acc:8.4f} {lr:10.6f}")

        # Early stopping
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"  Early stopping at epoch {epoch+1}")
                break

    print(f"\n  Best val accuracy: {best_val_acc:.4f}")


# =====================================================================
#   PARTE 11: DEBUGGING DE REDES NEURONALES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: DEBUGGING — CUANDO NO APRENDE ===")
print("=" * 80)

"""
CHECKLIST DE DEBUGGING:

1. OVERFITTING A 1 BATCH:
   El modelo DEBE poder memorizar un solo batch.
   Si no puede → bug en la arquitectura o loss.

2. GRADIENTES:
   - Todos cero → dying ReLU, learning rate demasiado bajo.
   - Explotan → learning rate demasiado alto.
   - NaN → division por cero, log de 0.

3. LOSS:
   - No baja → lr muy bajo, arquitectura inadecuada.
   - Explota → lr muy alto, datos no normalizados.
   - Oscila mucho → batch size muy pequeno.

4. ACTIVACIONES:
   - Todas cero → dying ReLU, mala inicializacion.
   - Todas saturadas → datos no normalizados.

5. DATOS:
   - Labels mezclados.
   - Features sin normalizar.
   - Leakage.
"""

if HAS_TORCH:
    print("\n--- Test: Overfit 1 batch (sanity check) ---")

    torch.manual_seed(42)
    model_debug = ProfessionalMLP(20, [64, 32], 2, dropout=0.0)
    opt_debug = torch.optim.Adam(model_debug.parameters(), lr=0.01)

    # Un solo batch de 16 muestras
    x_batch = X_t[:16]
    y_batch = y_t[:16]

    model_debug.train()
    for step in range(100):
        opt_debug.zero_grad()
        out = model_debug(x_batch)
        loss = nn.CrossEntropyLoss()(out, y_batch)
        loss.backward()
        opt_debug.step()

    acc_overfit = (model_debug(x_batch).argmax(1) == y_batch).float().mean()
    print(f"  Overfit 1 batch: acc={acc_overfit:.4f}")
    print(f"  {'✓ PASS' if acc_overfit > 0.95 else '✗ FAIL'}: "
          f"{'modelo puede memorizar' if acc_overfit > 0.95 else 'BUG!'}")

    # Gradient check
    print("\n--- Gradient health check ---")
    model_debug.zero_grad()
    out = model_debug(x_batch)
    loss = nn.CrossEntropyLoss()(out, y_batch)
    loss.backward()

    for name, param in model_debug.named_parameters():
        if param.grad is not None:
            grad = param.grad
            status = "OK"
            if grad.abs().max() < 1e-7:
                status = "DEAD (vanishing)"
            elif grad.abs().max() > 1e3:
                status = "EXPLODING"
            elif torch.isnan(grad).any():
                status = "NaN!"
            print(f"    {name:<30} grad_norm={grad.norm():.6f}  [{status}]")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: REDES NEURONALES BASICAS ===")
print("=" * 80)

print("""
  DE PERCEPTRON A MLP PROFESIONAL:

  1. PERCEPTRON: w·x + b → activacion.
     Solo problemas lineales. No resuelve XOR.

  2. MLP: capas + activaciones no-lineales.
     Universal approximator. Resuelve XOR y mas.

  3. ACTIVACIONES: ReLU (default), GELU (transformers).
     Sin activacion = red lineal inutil.

  4. BACKPROP: chain rule automatica con autograd.
     Nunca calcules gradientes a mano.

  5. INICIALIZACION: Kaiming para ReLU, Xavier para sigmoid/tanh.
     Mala init = red que no aprende.

  6. BATCH NORM: normaliza activaciones entre capas.
     Mas estable, converge mas rapido.

  7. DROPOUT: apaga neuronas aleatoriamente.
     Regularizacion efectiva contra overfitting.

  8. DEBUGGING: overfit 1 batch, check gradientes, check loss.

  RECETA MLP PROFESIONAL:
    Linear → BatchNorm → GELU → Dropout → repeat → Linear output
    + AdamW optimizer
    + Cosine annealing LR
    + Gradient clipping
    + Early stopping
""")

print("=" * 80)
print("=== FIN MODULO 17, ARCHIVO 02 ===")
print("=" * 80)
