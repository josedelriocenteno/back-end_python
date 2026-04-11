# ===========================================================================
# 02_optimizacion_y_gradient_descent.py
# ===========================================================================
# MODULO 08: CALCULO Y OPTIMIZACION
# ARCHIVO 02: Optimizacion y Variantes de Gradient Descent
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar gradient descent y todas sus variantes usadas en ML:
# SGD, momentum, RMSprop, Adam, learning rate schedules.
#
# CONTENIDO:
#   1. Gradient descent vanilla.
#   2. Stochastic gradient descent (SGD).
#   3. Mini-batch SGD.
#   4. Momentum.
#   5. RMSprop.
#   6. Adam (y AdamW).
#   7. Learning rate schedules.
#   8. Convexidad y puntos criticos.
#   9. Ejercicio: optimizadores sobre funciones de test.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time


# =====================================================================
#   PARTE 1: GRADIENT DESCENT VANILLA
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: GRADIENT DESCENT VANILLA ===")
print("=" * 80)

"""
Algoritmo basico:
  w = w - lr * ∇L(w)

Problema: usa TODOS los datos para cada paso.
Para N=1M datos, cada paso es MUY caro.
"""

print("\n--- GD Vanilla ---")

def gradient_descent(f, grad_f, x0, lr=0.01, epochs=100):
    """Gradient descent basico."""
    x = x0.copy()
    history = [x.copy()]
    loss_history = [f(x)]
    
    for _ in range(epochs):
        g = grad_f(x)
        x = x - lr * g
        history.append(x.copy())
        loss_history.append(f(x))
    
    return x, history, loss_history

# Funcion cuadratica: f(x,y) = x^2 + 10*y^2
def quadratic(x):
    return x[0]**2 + 10 * x[1]**2

def grad_quadratic(x):
    return np.array([2*x[0], 20*x[1]])

x0 = np.array([5.0, 5.0])
x_opt, hist, losses = gradient_descent(quadratic, grad_quadratic, x0, lr=0.05, epochs=50)

print(f"  f(x,y) = x² + 10y²")
print(f"  Inicio: {x0}, loss={quadratic(x0):.2f}")
print(f"  Final:  [{x_opt[0]:.6f}, {x_opt[1]:.6f}], loss={quadratic(x_opt):.8f}")
print(f"  Pasos: {len(hist)}")


# =====================================================================
#   PARTE 2: SGD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: STOCHASTIC GRADIENT DESCENT ===")
print("=" * 80)

"""
En vez de usar TODOS los datos, usa un solo ejemplo por paso.
Ventajas: mucho mas rapido, efecto de regularizacion.
Desventajas: ruidoso, puede no converger exactamente.

VARIANTES:
- SGD puro: 1 ejemplo por paso.
- Mini-batch SGD: B ejemplos por paso (tipico B=32-256).
- GD completo: todos los datos (batch GD).
"""

print("\n--- Comparacion Batch vs Mini-batch vs SGD ---")

class LinearModel:
    def __init__(self, d):
        self.w = np.zeros(d)
    
    def predict(self, X):
        return X @ self.w
    
    def loss(self, X, y):
        return np.mean((self.predict(X) - y) ** 2)
    
    def gradient(self, X, y):
        n = X.shape[0]
        return (2/n) * X.T @ (self.predict(X) - y)

# Datos
np.random.seed(42)
N = 1000
d = 5
X_data = np.random.randn(N, d)
w_true = np.array([1.0, -2.0, 0.5, 3.0, -1.0])
y_data = X_data @ w_true + np.random.randn(N) * 0.1

def train_batch(X, y, lr, epochs):
    model = LinearModel(X.shape[1])
    losses = []
    for _ in range(epochs):
        losses.append(model.loss(X, y))
        grad = model.gradient(X, y)
        model.w -= lr * grad
    return model, losses

def train_sgd(X, y, lr, epochs):
    model = LinearModel(X.shape[1])
    losses = []
    n = X.shape[0]
    for epoch in range(epochs):
        losses.append(model.loss(X, y))
        for i in np.random.permutation(n):
            Xi = X[i:i+1]
            yi = y[i:i+1]
            grad = model.gradient(Xi, yi)
            model.w -= lr * grad
    return model, losses

def train_minibatch(X, y, lr, epochs, batch_size=32):
    model = LinearModel(X.shape[1])
    losses = []
    n = X.shape[0]
    for epoch in range(epochs):
        losses.append(model.loss(X, y))
        indices = np.random.permutation(n)
        for start in range(0, n, batch_size):
            batch = indices[start:start+batch_size]
            grad = model.gradient(X[batch], y[batch])
            model.w -= lr * grad
    return model, losses

# Entrenar
model_batch, losses_batch = train_batch(X_data, y_data, lr=0.01, epochs=50)
model_mini, losses_mini = train_minibatch(X_data, y_data, lr=0.01, epochs=5, batch_size=32)
model_sgd, losses_sgd = train_sgd(X_data, y_data, lr=0.001, epochs=2)

print(f"  Batch GD   (50 epochs): loss={losses_batch[-1]:.6f}, w_error={np.linalg.norm(model_batch.w - w_true):.6f}")
print(f"  Mini-batch  (5 epochs): loss={losses_mini[-1]:.6f}, w_error={np.linalg.norm(model_mini.w - w_true):.6f}")
print(f"  SGD         (2 epochs): loss={losses_sgd[-1]:.6f}, w_error={np.linalg.norm(model_sgd.w - w_true):.6f}")


# =====================================================================
#   PARTE 3: MOMENTUM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: MOMENTUM ===")
print("=" * 80)

"""
Problema: SGD oscila en direcciones de alta curvatura.
Solucion: acumular velocidad (como una bola rodando).

v_t = β * v_{t-1} + ∇L(w_t)
w_t = w_t - lr * v_t

β tipico: 0.9
"""

print("\n--- Momentum optimizer ---")

class MomentumOptimizer:
    def __init__(self, lr=0.01, beta=0.9):
        self.lr = lr
        self.beta = beta
        self.v = None
    
    def step(self, params, grads):
        if self.v is None:
            self.v = np.zeros_like(params)
        
        self.v = self.beta * self.v + grads
        params -= self.lr * self.v
        return params

def train_with_optimizer(f, grad_f, x0, optimizer, epochs=100):
    x = x0.copy()
    losses = [f(x)]
    for _ in range(epochs):
        g = grad_f(x)
        x = optimizer.step(x, g)
        losses.append(f(x))
    return x, losses

# Comparar vanilla vs momentum
x0 = np.array([5.0, 5.0])

_, losses_vanilla = train_with_optimizer(
    quadratic, grad_quadratic, x0,
    MomentumOptimizer(lr=0.01, beta=0.0), epochs=100
)

_, losses_momentum = train_with_optimizer(
    quadratic, grad_quadratic, x0,
    MomentumOptimizer(lr=0.01, beta=0.9), epochs=100
)

print(f"  Vanilla (100 epochs): loss = {losses_vanilla[-1]:.8f}")
print(f"  Momentum(100 epochs): loss = {losses_momentum[-1]:.8f}")
print(f"  Momentum es {losses_vanilla[-1]/max(losses_momentum[-1],1e-20):.0f}x mejor")


# =====================================================================
#   PARTE 4: NESTEROV MOMENTUM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: NESTEROV ACCELERATED GRADIENT ===")
print("=" * 80)

"""
Nesterov: evaluar el gradiente en la posicion ANTICIPADA.
"Mira adelante antes de saltar."

v_t = β * v_{t-1} + ∇L(w_t - β * v_{t-1})
w_t = w_t - lr * v_t
"""

print("\n--- Nesterov momentum ---")

class NesterovOptimizer:
    def __init__(self, lr=0.01, beta=0.9):
        self.lr = lr
        self.beta = beta
        self.v = None
    
    def step(self, params, grad_fn):
        if self.v is None:
            self.v = np.zeros_like(params)
        
        # Look-ahead
        lookahead = params - self.lr * self.beta * self.v
        grad = grad_fn(lookahead)
        
        self.v = self.beta * self.v + grad
        params -= self.lr * self.v
        return params

x0 = np.array([5.0, 5.0])
x_nag = x0.copy()
v = np.zeros(2)
losses_nag = [quadratic(x_nag)]

for _ in range(100):
    lookahead = x_nag - 0.01 * 0.9 * v
    g = grad_quadratic(lookahead)
    v = 0.9 * v + g
    x_nag = x_nag - 0.01 * v
    losses_nag.append(quadratic(x_nag))

print(f"  Nesterov (100 epochs): loss = {losses_nag[-1]:.8f}")


# =====================================================================
#   PARTE 5: RMSPROP
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: RMSPROP ===")
print("=" * 80)

"""
RMSprop: adaptar learning rate POR PARAMETRO.
Divide por la raiz de la media movil de gradientes^2.

s_t = β * s_{t-1} + (1-β) * g_t²
w_t = w_t - lr * g_t / (√s_t + ε)

Resultado: parametros con gradientes grandes -> lr efectivo pequeño
           parametros con gradientes pequeños -> lr efectivo grande
"""

print("\n--- RMSprop optimizer ---")

class RMSpropOptimizer:
    def __init__(self, lr=0.01, beta=0.99, eps=1e-8):
        self.lr = lr
        self.beta = beta
        self.eps = eps
        self.s = None
    
    def step(self, params, grads):
        if self.s is None:
            self.s = np.zeros_like(params)
        
        self.s = self.beta * self.s + (1 - self.beta) * grads**2
        params -= self.lr * grads / (np.sqrt(self.s) + self.eps)
        return params

x0 = np.array([5.0, 5.0])

_, losses_rmsprop = train_with_optimizer(
    quadratic, grad_quadratic, x0,
    RMSpropOptimizer(lr=0.1), epochs=100
)

print(f"  RMSprop (100 epochs): loss = {losses_rmsprop[-1]:.8f}")


# =====================================================================
#   PARTE 6: ADAM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: ADAM ===")
print("=" * 80)

"""
Adam: combina Momentum + RMSprop + bias correction.
EL OPTIMIZADOR POR DEFECTO EN DEEP LEARNING.

m_t = β₁ * m_{t-1} + (1-β₁) * g_t        (1er momento: media)
v_t = β₂ * v_{t-1} + (1-β₂) * g_t²       (2do momento: varianza)
m̂_t = m_t / (1 - β₁^t)                   (bias correction)
v̂_t = v_t / (1 - β₂^t)                   (bias correction)
w_t = w_t - lr * m̂_t / (√v̂_t + ε)

Hyperparams tipicos: lr=0.001, β₁=0.9, β₂=0.999, ε=1e-8
"""

print("\n--- Adam optimizer ---")

class AdamOptimizer:
    """Adam optimizer completo."""
    
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = None  # Primer momento
        self.v = None  # Segundo momento
        self.t = 0     # Timestep
    
    def step(self, params, grads):
        if self.m is None:
            self.m = np.zeros_like(params)
            self.v = np.zeros_like(params)
        
        self.t += 1
        
        # Actualizar momentos
        self.m = self.beta1 * self.m + (1 - self.beta1) * grads
        self.v = self.beta2 * self.v + (1 - self.beta2) * grads**2
        
        # Bias correction
        m_hat = self.m / (1 - self.beta1**self.t)
        v_hat = self.v / (1 - self.beta2**self.t)
        
        # Update
        params -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
        return params

x0 = np.array([5.0, 5.0])

_, losses_adam = train_with_optimizer(
    quadratic, grad_quadratic, x0,
    AdamOptimizer(lr=0.1), epochs=100
)

print(f"  Adam (100 epochs): loss = {losses_adam[-1]:.8f}")


print("\n--- AdamW (Adam con weight decay desacoplado) ---")

"""
AdamW: weight decay NO va dentro de Adam, se aplica APARTE.
w_t = w_t - lr * (m̂_t / (√v̂_t + ε) + λ * w_t)

Es el optimizador preferido para Transformers.
"""

class AdamWOptimizer:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8, weight_decay=0.01):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.wd = weight_decay
        self.m = None
        self.v = None
        self.t = 0
    
    def step(self, params, grads):
        if self.m is None:
            self.m = np.zeros_like(params)
            self.v = np.zeros_like(params)
        
        self.t += 1
        self.m = self.beta1 * self.m + (1 - self.beta1) * grads
        self.v = self.beta2 * self.v + (1 - self.beta2) * grads**2
        
        m_hat = self.m / (1 - self.beta1**self.t)
        v_hat = self.v / (1 - self.beta2**self.t)
        
        # Weight decay desacoplado
        params -= self.lr * (m_hat / (np.sqrt(v_hat) + self.eps) + self.wd * params)
        return params

_, losses_adamw = train_with_optimizer(
    quadratic, grad_quadratic, x0,
    AdamWOptimizer(lr=0.1, weight_decay=0.01), epochs=100
)
print(f"  AdamW (100 epochs): loss = {losses_adamw[-1]:.8f}")


# =====================================================================
#   PARTE 7: COMPARACION DE OPTIMIZADORES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: COMPARACION DE OPTIMIZADORES ===")
print("=" * 80)

print("\n--- Benchmark en Rosenbrock ---")

def rosenbrock(x):
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

def grad_rosenbrock(x):
    dx = -2 * (1 - x[0]) + 200 * (x[1] - x[0]**2) * (-2 * x[0])
    dy = 200 * (x[1] - x[0]**2)
    return np.array([dx, dy])

x0 = np.array([-1.0, 1.0])
optimizers = {
    "SGD(0.001)": MomentumOptimizer(lr=0.001, beta=0.0),
    "Momentum":   MomentumOptimizer(lr=0.001, beta=0.9),
    "RMSprop":    RMSpropOptimizer(lr=0.001),
    "Adam":       AdamOptimizer(lr=0.01),
    "AdamW":      AdamWOptimizer(lr=0.01, weight_decay=0.001),
}

print(f"  Rosenbrock: minimo en (1, 1)")
print(f"  Inicio: {x0}\n")

for name, opt in optimizers.items():
    x_final, losses = train_with_optimizer(
        rosenbrock, grad_rosenbrock, x0, opt, epochs=500
    )
    dist = np.linalg.norm(x_final - np.array([1.0, 1.0]))
    print(f"  {name:12s}: loss={losses[-1]:12.6f}, dist_optimo={dist:.6f}")


# =====================================================================
#   PARTE 8: LEARNING RATE SCHEDULES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: LEARNING RATE SCHEDULES ===")
print("=" * 80)

"""
El learning rate no tiene que ser constante.
Schedulers comunes:
1. Step decay: reducir por factor cada N epochs.
2. Exponential decay: lr = lr0 * gamma^t.
3. Cosine annealing: lr sigue coseno.
4. Warmup + decay: subir linealmente, luego bajar.
5. One-cycle: subir y bajar una vez.
"""

print("\n--- Implementacion de schedulers ---")

class StepDecayScheduler:
    def __init__(self, lr0, step_size, gamma=0.1):
        self.lr0 = lr0
        self.step_size = step_size
        self.gamma = gamma
    
    def get_lr(self, epoch):
        return self.lr0 * (self.gamma ** (epoch // self.step_size))

class ExponentialDecayScheduler:
    def __init__(self, lr0, gamma=0.99):
        self.lr0 = lr0
        self.gamma = gamma
    
    def get_lr(self, epoch):
        return self.lr0 * (self.gamma ** epoch)

class CosineAnnealingScheduler:
    def __init__(self, lr0, T_max, lr_min=0):
        self.lr0 = lr0
        self.T_max = T_max
        self.lr_min = lr_min
    
    def get_lr(self, epoch):
        return self.lr_min + 0.5 * (self.lr0 - self.lr_min) * (
            1 + np.cos(np.pi * epoch / self.T_max))

class WarmupCosineScheduler:
    def __init__(self, lr0, warmup_epochs, total_epochs):
        self.lr0 = lr0
        self.warmup = warmup_epochs
        self.total = total_epochs
    
    def get_lr(self, epoch):
        if epoch < self.warmup:
            return self.lr0 * epoch / self.warmup
        progress = (epoch - self.warmup) / (self.total - self.warmup)
        return self.lr0 * 0.5 * (1 + np.cos(np.pi * progress))

# Visualizar schedulers
schedulers = {
    "Step(30)":      StepDecayScheduler(0.1, 30, 0.1),
    "Exponential":   ExponentialDecayScheduler(0.1, 0.97),
    "Cosine":        CosineAnnealingScheduler(0.1, 100),
    "Warmup+Cosine": WarmupCosineScheduler(0.1, 10, 100),
}

print(f"\n  {'Epoch':>6s}", end="")
for name in schedulers:
    print(f"  {name:>14s}", end="")
print()

for epoch in [0, 5, 10, 20, 30, 50, 70, 90, 99]:
    print(f"  {epoch:6d}", end="")
    for name, sched in schedulers.items():
        lr = sched.get_lr(epoch)
        print(f"  {lr:14.6f}", end="")
    print()


print("\n--- Entrenar con warmup+cosine ---")

def train_with_schedule(f, grad_f, x0, scheduler, epochs=100):
    x = x0.copy()
    losses = [f(x)]
    m = np.zeros_like(x0)
    v_sq = np.zeros_like(x0)
    
    for t in range(1, epochs + 1):
        g = grad_f(x)
        lr = scheduler.get_lr(t)
        
        # Adam con lr variable
        m = 0.9 * m + 0.1 * g
        v_sq = 0.999 * v_sq + 0.001 * g**2
        m_hat = m / (1 - 0.9**t)
        v_hat = v_sq / (1 - 0.999**t)
        
        x -= lr * m_hat / (np.sqrt(v_hat) + 1e-8)
        losses.append(f(x))
    
    return x, losses

sched = WarmupCosineScheduler(0.1, warmup_epochs=10, total_epochs=200)
x_sched, losses_sched = train_with_schedule(
    rosenbrock, grad_rosenbrock, np.array([-1.0, 1.0]), sched, epochs=200
)
print(f"  Warmup+Cosine + Adam on Rosenbrock: loss={losses_sched[-1]:.6f}")


# =====================================================================
#   PARTE 9: CONVEXIDAD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: CONVEXIDAD Y PUNTOS CRITICOS ===")
print("=" * 80)

"""
Convexa: solo un minimo global. GD siempre converge.
No convexa: multiples minimos locales, saddle points.

EN ML:
- Regresion lineal: CONVEXA. Minimo global garantizado.
- Redes neuronales: NO CONVEXA. Saddle points dominan.

Tipos de puntos criticos (∇f = 0):
- Minimo: Hessiana positiva definida.
- Maximo: Hessiana negativa definida.
- Saddle: Hessiana indefinida.
"""

print("\n--- Detectar tipo de punto critico ---")

def classify_critical_point(f, x, h=1e-5):
    """Clasificar punto critico usando la Hessiana."""
    n = len(x)
    H = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            x_pp = x.copy(); x_pp[i] += h; x_pp[j] += h
            x_pm = x.copy(); x_pm[i] += h; x_pm[j] -= h
            x_mp = x.copy(); x_mp[i] -= h; x_mp[j] += h
            x_mm = x.copy(); x_mm[i] -= h; x_mm[j] -= h
            H[i,j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4*h*h)
    
    eigenvals = np.linalg.eigvalsh(H)
    
    if all(eigenvals > 0):
        return "MINIMO", eigenvals
    elif all(eigenvals < 0):
        return "MAXIMO", eigenvals
    else:
        return "SADDLE POINT", eigenvals

# Puntos criticos de f(x,y) = x^3 - 3xy^2
def monkey_saddle(x):
    return x[0]**3 - 3 * x[0] * x[1]**2

# Cuadratica (minimo en origen)
tipo, vals = classify_critical_point(quadratic, np.array([0.0, 0.0]))
print(f"  x²+10y² en (0,0): {tipo}, eigenvalues={vals}")

# Saddle point
def saddle(x):
    return x[0]**2 - x[1]**2

tipo, vals = classify_critical_point(saddle, np.array([0.0, 0.0]))
print(f"  x²-y² en (0,0): {tipo}, eigenvalues={vals}")


print("\n" + "=" * 80)
print("=== CAPITULO 10: EJERCICIO — OPTIMIZER BENCHMARK ===")
print("=" * 80)

"""
Comparar todos los optimizadores en regresion lineal con datos reales.
"""

print("\n--- Benchmark completo ---")

np.random.seed(42)
N = 500
d = 10
X_bench = np.random.randn(N, d)
w_bench = np.random.randn(d)
y_bench = X_bench @ w_bench + np.random.randn(N) * 0.5

def linear_loss(w):
    return np.mean((X_bench @ w - y_bench)**2)

def linear_grad(w):
    return (2/N) * X_bench.T @ (X_bench @ w - y_bench)

w0 = np.zeros(d)

results = {}
configs = [
    ("SGD(0.01)",     MomentumOptimizer(lr=0.01, beta=0.0)),
    ("SGD(0.1)",      MomentumOptimizer(lr=0.1, beta=0.0)),
    ("Momentum(0.9)", MomentumOptimizer(lr=0.01, beta=0.9)),
    ("RMSprop",       RMSpropOptimizer(lr=0.01)),
    ("Adam(0.001)",   AdamOptimizer(lr=0.001)),
    ("Adam(0.01)",    AdamOptimizer(lr=0.01)),
    ("AdamW",         AdamWOptimizer(lr=0.01, weight_decay=0.01)),
]

for name, opt in configs:
    w_final, losses = train_with_optimizer(
        linear_loss, linear_grad, w0, opt, epochs=200
    )
    results[name] = losses[-1]
    w_err = np.linalg.norm(w_final - w_bench)
    print(f"  {name:16s}: loss={losses[-1]:.8f}, w_error={w_err:.6f}")


print("\n" + "=" * 80)
print("=== CAPITULO 11: GRADIENT NOISE Y REGULARIZACION ===")
print("=" * 80)

"""
El ruido en SGD tiene un efecto REGULARIZADOR.
- Batch size grande: menos ruido, optimizacion mas precisa.
- Batch size pequeño: mas ruido, mejor generalizacion.

La relacion lr/batch_size debe mantenerse constante al escalar.
"""

print("\n--- Efecto del batch size ---")

for bs in [1, 8, 32, 128, 512]:
    model_bs = LinearModel(X_data.shape[1])
    n = X_data.shape[0]
    
    for epoch in range(3):
        indices = np.random.permutation(n)
        for start in range(0, n, bs):
            batch = indices[start:start+bs]
            grad = model_bs.gradient(X_data[batch], y_data[batch])
            model_bs.w -= 0.01 * grad
    
    loss = model_bs.loss(X_data, y_data)
    print(f"  batch_size={bs:4d}: loss={loss:.6f}")


print("\n--- Gradient noise scale ---")

"""
Gradient noise = Var(stochastic_grad - true_grad)
A menor batch size, mayor ruido.

Smith et al. (2018): batch_size ~ lr / noise_scale
"""

np.random.seed(42)
true_grad = LinearModel(d).gradient(X_data, y_data)

for bs in [1, 8, 32, 128]:
    noises = []
    for _ in range(100):
        batch = np.random.choice(N, bs, replace=False)
        stoch_grad = LinearModel(d).gradient(X_data[batch], y_data[batch])
        noises.append(np.linalg.norm(stoch_grad - true_grad))
    print(f"  bs={bs:4d}: noise_mean={np.mean(noises):.4f}, noise_std={np.std(noises):.4f}")


print("\n" + "=" * 80)
print("=== CAPITULO 12: EARLY STOPPING ===")
print("=" * 80)

"""
Detener el entrenamiento cuando el validation loss sube.
Es una forma de REGULARIZACION.
"""

print("\n--- Early stopping ---")

class EarlyStopping:
    """Monitor de early stopping."""
    
    def __init__(self, patience=5, min_delta=1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = float('inf')
        self.counter = 0
        self.best_epoch = 0
    
    def step(self, val_loss, epoch):
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
            self.best_epoch = epoch
        else:
            self.counter += 1
        
        return self.counter >= self.patience

# Simular overfitting
np.random.seed(42)
n_train, n_val = 30, 100
X_es = np.random.randn(n_train + n_val, 1)
y_es = np.sin(X_es[:, 0]) + np.random.randn(n_train + n_val) * 0.1

X_tr, X_va = X_es[:n_train], X_es[n_train:]
y_tr, y_va = y_es[:n_train], y_es[n_train:]

# "Features" polinomiales (overfitting con grado alto)
degree = 15
X_tr_poly = np.column_stack([X_tr**i for i in range(degree + 1)])
X_va_poly = np.column_stack([X_va**i for i in range(degree + 1)])

w = np.zeros(degree + 1)
es = EarlyStopping(patience=10)
lr = 0.001

for epoch in range(500):
    # Train
    y_pred_tr = X_tr_poly @ w
    train_loss = np.mean((y_pred_tr - y_tr) ** 2)
    grad = (2 / n_train) * X_tr_poly.T @ (y_pred_tr - y_tr)
    w -= lr * grad
    
    # Val
    y_pred_va = X_va_poly @ w
    val_loss = np.mean((y_pred_va - y_va) ** 2)
    
    if es.step(val_loss, epoch):
        print(f"  Early stopping en epoch {epoch}")
        print(f"  Mejor epoch: {es.best_epoch}, val_loss: {es.best_loss:.4f}")
        break


print("\n" + "=" * 80)
print("=== CAPITULO 13: HYPERPARAMETER SEARCH ===")
print("=" * 80)

"""
Encontrar los mejores hyperparams:
1. Grid search: probar todas las combinaciones.
2. Random search: muestrear aleatoriamente (mejor que grid!).
3. Bayesian optimization: usar resultados previos.
"""

print("\n--- Random search para lr y regularizacion ---")

np.random.seed(42)
best_loss = float('inf')
best_config = {}

for trial in range(20):
    lr = 10 ** np.random.uniform(-4, -1)      # log-uniform en [1e-4, 0.1]
    reg = 10 ** np.random.uniform(-5, -1)      # log-uniform en [1e-5, 0.1]
    
    w = np.zeros(d)
    for _ in range(50):
        grad = (2/N) * X_bench.T @ (X_bench @ w - y_bench) + 2 * reg * w
        w -= lr * grad
    
    loss = np.mean((X_bench @ w - y_bench)**2)
    
    if loss < best_loss:
        best_loss = loss
        best_config = {'lr': lr, 'reg': reg}
        print(f"  Trial {trial:2d}: lr={lr:.6f}, reg={reg:.6f}, loss={loss:.6f} *BEST*")

print(f"\n  Mejor: lr={best_config['lr']:.6f}, reg={best_config['reg']:.6f}")


print("\n" + "=" * 80)
print("=== CAPITULO 14: L-BFGS ===")
print("=" * 80)

"""
L-BFGS: cuasi-Newton. Aproxima la Hessiana sin calcularla.
Usa ultimas m actualizaciones para aproximar H^{-1}.

Ventajas: convergencia rapida, pocos hyperparams.
Desventajas: no funciona con mini-batch, mucha memoria.
"""

print("\n--- L-BFGS simplificado ---")

def lbfgs_step(f, grad_f, x, memory, m=10):
    """Un paso de L-BFGS."""
    g = grad_f(x)
    
    if len(memory) == 0:
        return -g
    
    q = g.copy()
    alphas = []
    
    # Backward loop
    for s, y_m, rho in reversed(memory[-m:]):
        alpha = rho * np.dot(s, q)
        alphas.append(alpha)
        q -= alpha * y_m
    
    # Initial Hessian approximation
    s_last, y_last, _ = memory[-1]
    gamma = np.dot(s_last, y_last) / np.dot(y_last, y_last)
    r = gamma * q
    
    # Forward loop
    for (s, y_m, rho), alpha in zip(memory[-m:], reversed(alphas)):
        beta = rho * np.dot(y_m, r)
        r += (alpha - beta) * s
    
    return -r

# Entrenar con L-BFGS
x = np.array([5.0, 5.0])
memory = []
losses_lbfgs = [quadratic(x)]

for i in range(50):
    g_old = grad_quadratic(x)
    direction = lbfgs_step(quadratic, grad_quadratic, x, memory)
    
    # Line search simple
    lr = 0.1
    x_new = x + lr * direction
    
    g_new = grad_quadratic(x_new)
    s = x_new - x
    y = g_new - g_old
    rho = 1.0 / (np.dot(y, s) + 1e-10)
    memory.append((s, y, rho))
    
    x = x_new
    losses_lbfgs.append(quadratic(x))

print(f"  L-BFGS (50 pasos): loss = {losses_lbfgs[-1]:.8f}")


print("\n" + "=" * 80)
print("=== CAPITULO 15: GRADIENT ACCUMULATION ===")
print("=" * 80)

"""
Gradient accumulation: simular batch sizes grandes sin memoria.
En vez de batch_size=256, hacer 8 pasos de batch_size=32.
Acumular gradientes y actualizar cada N pasos.

CRITICO para entrenar modelos grandes (LLMs) en GPUs limitadas.
"""

print("\n--- Gradient accumulation ---")

def train_with_accumulation(X, y, lr, epochs, batch_size, accumulation_steps):
    """Entrenar con gradient accumulation."""
    model = LinearModel(X.shape[1])
    n = X.shape[0]
    effective_batch = batch_size * accumulation_steps
    losses = []
    
    for epoch in range(epochs):
        losses.append(model.loss(X, y))
        indices = np.random.permutation(n)
        step = 0
        accumulated_grad = np.zeros_like(model.w)
        
        for start in range(0, n, batch_size):
            batch = indices[start:start+batch_size]
            grad = model.gradient(X[batch], y[batch])
            accumulated_grad += grad
            step += 1
            
            if step % accumulation_steps == 0:
                model.w -= lr * accumulated_grad / accumulation_steps
                accumulated_grad = np.zeros_like(model.w)
    
    return model, losses

# Comparar batch real vs acumulado
model_real, losses_real = train_minibatch(X_data, y_data, lr=0.01, epochs=3, batch_size=128)
model_accum, losses_accum = train_with_accumulation(
    X_data, y_data, lr=0.01, epochs=3, batch_size=32, accumulation_steps=4
)

print(f"  Batch real (128):        loss = {model_real.loss(X_data, y_data):.6f}")
print(f"  Accum (32x4=128):        loss = {model_accum.loss(X_data, y_data):.6f}")
print(f"  Diferencia: {abs(model_real.loss(X_data, y_data) - model_accum.loss(X_data, y_data)):.6f}")


print("\n" + "=" * 80)
print("=== CAPITULO 16: LINE SEARCH ===")
print("=" * 80)

"""
Line search: encontrar el lr optimo en cada paso.
- Backtracking: empezar con lr grande, reducir hasta Armijo condition.
- Wolfe conditions: criterio mas estricto.
"""

print("\n--- Backtracking line search ---")

def backtracking_line_search(f, grad_f, x, direction, alpha=1.0, rho=0.5, c=1e-4):
    """Armijo backtracking line search."""
    fx = f(x)
    gx = grad_f(x)
    dot = np.dot(gx, direction)
    
    while f(x + alpha * direction) > fx + c * alpha * dot:
        alpha *= rho
        if alpha < 1e-10:
            break
    
    return alpha

x_ls = np.array([5.0, 5.0])
direction = -grad_quadratic(x_ls)

alpha_opt = backtracking_line_search(quadratic, grad_quadratic, x_ls, direction)
print(f"  Punto: {x_ls}")
print(f"  Direccion: {direction}")
print(f"  Step size optimo: {alpha_opt:.4f}")
print(f"  f(x): {quadratic(x_ls):.4f}")
print(f"  f(x + α*d): {quadratic(x_ls + alpha_opt * direction):.4f}")



print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE OPTIMIZACION:

1. GD Vanilla: simple pero lento (usa todos los datos).

2. SGD/Mini-batch: rapido, ruido = regularizacion.

3. Momentum + Nesterov: acumula velocidad.

4. RMSprop: learning rate adaptativo por parametro.

5. Adam/AdamW: el estandar en deep learning.

6. LR Schedules: warmup + cosine es el estandar actual.

7. Convexidad: ML es no-convexo, saddle points dominan.

8. Early stopping: regularizacion via parada temprana.

9. Hyperparameter search: random > grid.

10. L-BFGS: cuasi-Newton para problemas no-stochastic.

Siguiente archivo: Backpropagation y grafo computacional.
"""

print("\n FIN DE ARCHIVO 02_optimizacion_y_gradient_descent.")
print(" Optimizacion ha sido dominada.")
