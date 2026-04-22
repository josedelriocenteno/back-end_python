# ===========================================================================
# 01_tensores_y_autograd.py - MODULO 17: PYTORCH FUNDAMENTOS
# ===========================================================================
# Tensores, Autograd, GPU, y operaciones fundamentales de PyTorch.
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
    print(f"  CUDA available: {torch.cuda.is_available()}")
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
except ImportError:
    HAS_TORCH = False
    print("  PyTorch not installed. Conceptual mode.")

# =====================================================================
#   PARTE 1: TENSORES BASICOS
# =====================================================================
print("\n" + "="*80)
print("=== CAPITULO 1: TENSORES ===")
print("="*80)

"""
TENSOR: estructura de datos fundamental de PyTorch.
  - Similar a numpy ndarray pero con soporte GPU y autograd.
  - 0D: scalar, 1D: vector, 2D: matrix, 3D+: tensor.

Creacion:
  torch.tensor([1,2,3])       # from list
  torch.zeros(3, 4)           # zeros
  torch.ones(3, 4)            # ones
  torch.randn(3, 4)           # normal distribution
  torch.rand(3, 4)            # uniform [0, 1)
  torch.arange(0, 10)         # range
  torch.linspace(0, 1, 10)    # evenly spaced
  torch.eye(3)                # identity matrix
  torch.empty(3, 4)           # uninitialized
"""

if HAS_TORCH:
    # Scalar
    t0 = torch.tensor(42.0)
    print(f"  Scalar: {t0}, shape={t0.shape}, ndim={t0.ndim}")
    
    # Vector
    t1 = torch.tensor([1.0, 2.0, 3.0])
    print(f"  Vector: {t1}, shape={t1.shape}")
    
    # Matrix
    t2 = torch.randn(3, 4)
    print(f"  Matrix: shape={t2.shape}, dtype={t2.dtype}")
    
    # 3D tensor (batch of matrices)
    t3 = torch.randn(2, 3, 4)
    print(f"  3D: shape={t3.shape}")
    
    # Creation functions
    print(f"\n  zeros: {torch.zeros(2, 3).shape}")
    print(f"  ones:  {torch.ones(2, 3).shape}")
    print(f"  eye:   {torch.eye(3).shape}")
    print(f"  arange: {torch.arange(0, 5)}")
    print(f"  linspace: {torch.linspace(0, 1, 5)}")

# =====================================================================
#   PARTE 2: DTYPES Y CASTING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 2: DTYPES ===")
print("="*80)

"""
PyTorch dtypes:
  torch.float32 (default), torch.float64, torch.float16
  torch.int32, torch.int64, torch.int16, torch.int8
  torch.bool
  torch.complex64

REGLA: neural networks usan float32.
  float16: para mixed precision training (mas rapido, menos memoria).
"""

if HAS_TORCH:
    t_f32 = torch.tensor([1.0, 2.0])
    t_f64 = torch.tensor([1.0, 2.0], dtype=torch.float64)
    t_int = torch.tensor([1, 2, 3])
    t_bool = torch.tensor([True, False])
    
    print(f"  float32: {t_f32.dtype}")
    print(f"  float64: {t_f64.dtype}")
    print(f"  int64:   {t_int.dtype}")
    print(f"  bool:    {t_bool.dtype}")
    
    # Casting
    t_casted = t_int.float()
    print(f"  int->float: {t_casted.dtype}")
    t_half = t_f32.half()
    print(f"  float->half: {t_half.dtype}")

# =====================================================================
#   PARTE 3: OPERACIONES TENSORIALES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 3: OPERACIONES ===")
print("="*80)

if HAS_TORCH:
    a = torch.tensor([1.0, 2.0, 3.0])
    b = torch.tensor([4.0, 5.0, 6.0])
    
    # Element-wise
    print(f"  a + b = {a + b}")
    print(f"  a * b = {a * b}")
    print(f"  a ** 2 = {a ** 2}")
    
    # Reduction
    print(f"  sum:  {a.sum()}")
    print(f"  mean: {a.mean()}")
    print(f"  max:  {a.max()}")
    print(f"  argmax: {a.argmax()}")
    
    # Matrix operations
    M = torch.randn(3, 4)
    N = torch.randn(4, 2)
    print(f"\n  matmul: {M.shape} @ {N.shape} = {(M @ N).shape}")
    print(f"  transpose: {M.shape} -> {M.T.shape}")
    
    # In-place operations (end with _)
    c = torch.zeros(3)
    c.add_(a)
    print(f"  in-place add: {c}")

# =====================================================================
#   PARTE 4: INDEXING Y SLICING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 4: INDEXING ===")
print("="*80)

if HAS_TORCH:
    t = torch.arange(12).reshape(3, 4).float()
    print(f"  tensor:\n{t}")
    print(f"  t[0]:    {t[0]}")
    print(f"  t[:, 1]: {t[:, 1]}")
    print(f"  t[1, 2]: {t[1, 2]}")
    print(f"  t[t > 5]: {t[t > 5]}")
    
    # Fancy indexing
    idx = torch.tensor([0, 2])
    print(f"  t[idx]:  {t[idx]}")

# =====================================================================
#   PARTE 5: RESHAPE Y VIEW
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 5: RESHAPE ===")
print("="*80)

"""
view: returns a view (shares memory). Requires contiguous memory.
reshape: returns view if possible, else copies.
contiguous: ensures contiguous memory layout.
unsqueeze: add dimension.
squeeze: remove size-1 dimensions.
flatten: collapse all dims to 1D.
"""

if HAS_TORCH:
    t = torch.arange(24).float()
    print(f"  original: {t.shape}")
    print(f"  view(4,6): {t.view(4, 6).shape}")
    print(f"  reshape(2,3,4): {t.reshape(2, 3, 4).shape}")
    print(f"  unsqueeze(0): {t.unsqueeze(0).shape}")
    
    t2 = torch.randn(1, 3, 1, 4)
    print(f"  squeeze: {t2.shape} -> {t2.squeeze().shape}")
    
    t3 = torch.randn(2, 3, 4)
    print(f"  flatten: {t3.shape} -> {t3.flatten().shape}")
    print(f"  flatten(1): {t3.shape} -> {t3.flatten(1).shape}")

# =====================================================================
#   PARTE 6: NUMPY INTEROP
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 6: NUMPY ===")
print("="*80)

if HAS_TORCH:
    # Torch -> Numpy (shares memory on CPU)
    t = torch.tensor([1.0, 2.0, 3.0])
    n = t.numpy()
    print(f"  torch->numpy: {type(n)}, {n}")
    
    # Numpy -> Torch
    n2 = np.array([4.0, 5.0, 6.0])
    t2 = torch.from_numpy(n2)
    print(f"  numpy->torch: {type(t2)}, {t2}")
    
    # WARNING: they share memory!
    t[0] = 99
    print(f"  Shared memory: torch={t[0]}, numpy={n[0]}")

# =====================================================================
#   PARTE 7: AUTOGRAD
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 7: AUTOGRAD ===")
print("="*80)

"""
AUTOGRAD: automatic differentiation.
  - Track operations on tensors with requires_grad=True.
  - Call .backward() to compute gradients.
  - Access gradients via .grad attribute.

CHAIN RULE: dy/dx = dy/dz * dz/dx
PyTorch builds a computational graph and applies chain rule.
"""

if HAS_TORCH:
    # Simple gradient
    x = torch.tensor(3.0, requires_grad=True)
    y = x ** 2 + 2 * x + 1   # y = x² + 2x + 1
    y.backward()               # dy/dx = 2x + 2 = 8
    print(f"  x = {x.item()}")
    print(f"  y = x² + 2x + 1 = {y.item()}")
    print(f"  dy/dx = 2x + 2 = {x.grad.item()}")
    
    # Multi-variable
    w = torch.tensor([1.0, 2.0], requires_grad=True)
    b = torch.tensor(0.5, requires_grad=True)
    x_in = torch.tensor([3.0, 4.0])
    
    output = (w * x_in).sum() + b  # w·x + b = 11.5
    output.backward()
    
    print(f"\n  w·x + b = {output.item()}")
    print(f"  d/dw = x = {w.grad}")
    print(f"  d/db = 1 = {b.grad}")

# =====================================================================
#   PARTE 8: GRADIENT DESCENT MANUAL
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 8: GD MANUAL ===")
print("="*80)

if HAS_TORCH:
    # Linear regression: y = 2x + 1 + noise
    torch.manual_seed(42)
    X_data = torch.linspace(0, 5, 100).unsqueeze(1)
    y_data = 2 * X_data + 1 + torch.randn_like(X_data) * 0.3
    
    # Parameters
    w = torch.randn(1, requires_grad=True)
    b = torch.zeros(1, requires_grad=True)
    lr = 0.01
    
    print(f"  Training linear regression manually:")
    for epoch in range(100):
        # Forward
        y_pred = X_data * w + b
        loss = ((y_pred - y_data) ** 2).mean()
        
        # Backward
        loss.backward()
        
        # Update (no_grad to prevent tracking)
        with torch.no_grad():
            w -= lr * w.grad
            b -= lr * b.grad
        
        # Zero gradients
        w.grad.zero_()
        b.grad.zero_()
        
        if epoch % 25 == 0:
            print(f"    epoch {epoch:3d}: loss={loss.item():.4f}, w={w.item():.3f}, b={b.item():.3f}")
    
    print(f"  Final: w={w.item():.3f} (true=2), b={b.item():.3f} (true=1)")

# =====================================================================
#   PARTE 9: NN.MODULE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 9: NN.MODULE ===")
print("="*80)

"""
nn.Module: base class for all neural network models.
  - Define layers in __init__.
  - Define forward pass in forward().
  - Parameters automatically tracked.

Key layers:
  nn.Linear(in, out): fully connected layer.
  nn.Conv2d: convolution.
  nn.ReLU, nn.Sigmoid, nn.Tanh: activations.
  nn.BatchNorm1d: batch normalization.
  nn.Dropout: regularization.
"""

if HAS_TORCH:
    class SimpleNet(nn.Module):
        def __init__(self, input_dim, hidden_dim, output_dim):
            super().__init__()
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(hidden_dim, output_dim)
        
        def forward(self, x):
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x
    
    model = SimpleNet(10, 32, 2)
    print(f"  Model: {model}")
    print(f"\n  Parameters:")
    total = 0
    for name, param in model.named_parameters():
        print(f"    {name}: {param.shape}")
        total += param.numel()
    print(f"  Total params: {total}")

# =====================================================================
#   PARTE 10: TRAINING LOOP
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 10: TRAINING LOOP ===")
print("="*80)

"""
Standard training loop:
1. Forward pass: y_pred = model(x).
2. Loss: loss = criterion(y_pred, y_true).
3. Backward: loss.backward().
4. Update: optimizer.step().
5. Zero grads: optimizer.zero_grad().
"""

if HAS_TORCH:
    torch.manual_seed(42)
    X_clf = torch.randn(500, 10)
    y_clf = (X_clf[:, 0] + X_clf[:, 1] > 0).long()
    
    dataset = TensorDataset(X_clf, y_clf)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    model = SimpleNet(10, 32, 2)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    print(f"  Training loop:")
    for epoch in range(20):
        total_loss = 0
        correct = 0
        total = 0
        
        for X_batch, y_batch in loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += (predicted == y_batch).sum().item()
            total += y_batch.size(0)
        
        if epoch % 5 == 0:
            acc = correct / total
            print(f"    epoch {epoch:2d}: loss={total_loss/len(loader):.4f}, acc={acc:.4f}")

# =====================================================================
#   PARTE 11: LOSS FUNCTIONS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 11: LOSS FUNCTIONS ===")
print("="*80)

"""
Classification:
  nn.CrossEntropyLoss: multiclass (includes softmax).
  nn.BCEWithLogitsLoss: binary (includes sigmoid).
  nn.NLLLoss: negative log likelihood.

Regression:
  nn.MSELoss: mean squared error.
  nn.L1Loss: mean absolute error.
  nn.SmoothL1Loss: Huber loss.
"""

if HAS_TORCH:
    # CrossEntropy
    logits = torch.randn(4, 3)
    targets = torch.tensor([0, 1, 2, 1])
    ce_loss = nn.CrossEntropyLoss()(logits, targets)
    print(f"  CrossEntropy: {ce_loss.item():.4f}")
    
    # BCE
    pred_binary = torch.randn(4)
    target_binary = torch.tensor([1.0, 0.0, 1.0, 0.0])
    bce_loss = nn.BCEWithLogitsLoss()(pred_binary, target_binary)
    print(f"  BCEWithLogits: {bce_loss.item():.4f}")
    
    # MSE
    pred_reg = torch.randn(4)
    target_reg = torch.randn(4)
    mse_loss = nn.MSELoss()(pred_reg, target_reg)
    print(f"  MSE: {mse_loss.item():.4f}")

# =====================================================================
#   PARTE 12: OPTIMIZERS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 12: OPTIMIZERS ===")
print("="*80)

"""
SGD: simple, needs LR tuning, momentum helps.
Adam: adaptive LR, default choice.
AdamW: Adam with weight decay (better regularization).
RMSprop: adaptive, good for RNNs.
"""

if HAS_TORCH:
    dummy = nn.Linear(10, 2)
    
    optims = {
        'SGD': torch.optim.SGD(dummy.parameters(), lr=0.01),
        'SGD+mom': torch.optim.SGD(dummy.parameters(), lr=0.01, momentum=0.9),
        'Adam': torch.optim.Adam(dummy.parameters(), lr=0.001),
        'AdamW': torch.optim.AdamW(dummy.parameters(), lr=0.001, weight_decay=0.01),
    }
    
    for name in optims:
        print(f"  {name}")

# =====================================================================
#   PARTE 13: DATASET & DATALOADER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 13: DATASET ===")
print("="*80)

if HAS_TORCH:
    class CustomDataset(Dataset):
        def __init__(self, n_samples=1000, n_features=10):
            self.X = torch.randn(n_samples, n_features)
            self.y = (self.X[:, 0] > 0).long()
        
        def __len__(self):
            return len(self.X)
        
        def __getitem__(self, idx):
            return self.X[idx], self.y[idx]
    
    ds = CustomDataset(500, 10)
    dl = DataLoader(ds, batch_size=64, shuffle=True, num_workers=0)
    
    print(f"  Dataset: {len(ds)} samples")
    print(f"  Batches: {len(dl)}")
    
    for X_b, y_b in dl:
        print(f"  First batch: X={X_b.shape}, y={y_b.shape}")
        break

# =====================================================================
#   PARTE 14: ACTIVATION FUNCTIONS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 14: ACTIVATIONS ===")
print("="*80)

if HAS_TORCH:
    x = torch.linspace(-3, 3, 7)
    print(f"  x = {x.tolist()}")
    print(f"  ReLU:    {F.relu(x).tolist()}")
    print(f"  Sigmoid: {torch.sigmoid(x).tolist()}")
    print(f"  Tanh:    {torch.tanh(x).tolist()}")
    print(f"  LeakyReLU: {F.leaky_relu(x, 0.1).tolist()}")
    print(f"  GELU:    {F.gelu(x).tolist()}")
    
    # Softmax
    logits = torch.tensor([2.0, 1.0, 0.1])
    probs = F.softmax(logits, dim=0)
    print(f"\n  Softmax: {logits.tolist()} -> {probs.tolist()}")
    print(f"  Sum = {probs.sum().item()}")

# =====================================================================
#   PARTE 15: REGULARIZATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 15: REGULARIZATION ===")
print("="*80)

"""
1. Dropout: randomly zero elements during training.
2. Weight decay: L2 regularization (in optimizer).
3. BatchNorm: normalize activations.
4. Early stopping: stop when val loss stops improving.
"""

if HAS_TORCH:
    class RegularizedNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(10, 64)
            self.bn1 = nn.BatchNorm1d(64)
            self.drop1 = nn.Dropout(0.3)
            self.fc2 = nn.Linear(64, 32)
            self.bn2 = nn.BatchNorm1d(32)
            self.drop2 = nn.Dropout(0.2)
            self.fc3 = nn.Linear(32, 2)
        
        def forward(self, x):
            x = F.relu(self.bn1(self.fc1(x)))
            x = self.drop1(x)
            x = F.relu(self.bn2(self.fc2(x)))
            x = self.drop2(x)
            return self.fc3(x)
    
    reg_model = RegularizedNet()
    
    # Train vs eval mode
    reg_model.train()
    out_train = reg_model(torch.randn(5, 10))
    reg_model.eval()
    out_eval = reg_model(torch.randn(5, 10))
    
    print(f"  RegularizedNet params: {sum(p.numel() for p in reg_model.parameters())}")
    print(f"  Train mode: dropout/bn active")
    print(f"  Eval mode:  dropout off, bn uses running stats")

# =====================================================================
#   PARTE 16: LR SCHEDULER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 16: LR SCHEDULER ===")
print("="*80)

if HAS_TORCH:
    model_sched = nn.Linear(10, 2)
    opt = torch.optim.Adam(model_sched.parameters(), lr=0.01)
    
    schedulers = {
        'StepLR': torch.optim.lr_scheduler.StepLR(opt, step_size=10, gamma=0.5),
        'CosineAnnealing': torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=50),
    }
    
    for name in schedulers:
        print(f"  {name}")

# =====================================================================
#   PARTE 17: SAVE & LOAD
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 17: SAVE/LOAD ===")
print("="*80)

"""
Save model:
  torch.save(model.state_dict(), 'model.pth')  # recommended
  torch.save(model, 'model_full.pth')           # entire model

Load model:
  model.load_state_dict(torch.load('model.pth'))
"""

if HAS_TORCH:
    print("  Save: torch.save(model.state_dict(), 'model.pth')")
    print("  Load: model.load_state_dict(torch.load('model.pth'))")
    print("  Checkpoint: save model + optimizer + epoch + loss")

# =====================================================================
#   PARTE 18: GPU OPERATIONS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 18: GPU ===")
print("="*80)

if HAS_TORCH:
    print(f"  Device: {DEVICE}")
    t_cpu = torch.randn(3, 3)
    t_dev = t_cpu.to(DEVICE)
    print(f"  CPU tensor: {t_cpu.device}")
    print(f"  Device tensor: {t_dev.device}")

# =====================================================================
#   PARTE 19: FULL PIPELINE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 19: FULL PIPELINE ===")
print("="*80)

if HAS_TORCH:
    torch.manual_seed(42)
    
    # Data
    X_full = torch.randn(1000, 20)
    y_full = ((X_full[:, :3].sum(1)) > 0).long()
    
    n_train = 800
    X_train_t, X_test_t = X_full[:n_train], X_full[n_train:]
    y_train_t, y_test_t = y_full[:n_train], y_full[n_train:]
    
    train_ds = TensorDataset(X_train_t, y_train_t)
    train_dl = DataLoader(train_ds, batch_size=64, shuffle=True)
    
    # Model
    class FullNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(20, 64), nn.ReLU(), nn.BatchNorm1d(64), nn.Dropout(0.2),
                nn.Linear(64, 32), nn.ReLU(), nn.Dropout(0.1),
                nn.Linear(32, 2),
            )
        def forward(self, x):
            return self.net(x)
    
    net = FullNet().to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
    
    # Train
    print(f"  Full pipeline training:")
    for epoch in range(30):
        net.train()
        for xb, yb in train_dl:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            optimizer.zero_grad()
            loss = criterion(net(xb), yb)
            loss.backward()
            optimizer.step()
        
        if epoch % 10 == 0:
            net.eval()
            with torch.no_grad():
                preds = net(X_test_t.to(DEVICE)).argmax(1).cpu()
                acc = (preds == y_test_t).float().mean()
            print(f"    epoch {epoch:2d}: acc={acc:.4f}")
    
    # Final eval
    net.eval()
    with torch.no_grad():
        final_preds = net(X_test_t.to(DEVICE)).argmax(1).cpu()
        final_acc = (final_preds == y_test_t).float().mean()
    print(f"  Final accuracy: {final_acc:.4f}")

# =====================================================================
#   PARTE 20: BEST PRACTICES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 20: BEST PRACTICES ===")
print("="*80)

practices = [
    ("torch.manual_seed", "Reproducibility"),
    ("model.train/eval", "Dropout/BN behavior"),
    ("torch.no_grad()", "Inference speedup"),
    ("state_dict", "Save only weights"),
    (".to(device)", "GPU/CPU portability"),
    ("DataLoader", "Batching + shuffling"),
    ("gradient clipping", "Prevent exploding grads"),
    ("mixed precision", "fp16 for speed"),
]

print(f"\n  {'Practice':>20s} {'Purpose':>25s}")
for p, r in practices:
    print(f"  {p:>20s} {r:>25s}")


# =====================================================================
#   PARTE 21: GRADIENT CLIPPING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 21: GRADIENT CLIPPING ===")
print("="*80)

"""
Gradient clipping: limitar magnitud de gradientes.
Previene exploding gradients (comun en RNNs).

clip_grad_norm_: escala gradientes si norma > max_norm.
clip_grad_value_: clamp individual gradient values.
"""

if HAS_TORCH:
    model_gc = nn.Linear(10, 2)
    opt_gc = torch.optim.SGD(model_gc.parameters(), lr=0.1)
    
    x_gc = torch.randn(5, 10)
    y_gc = torch.tensor([0, 1, 0, 1, 0])
    
    loss_gc = nn.CrossEntropyLoss()(model_gc(x_gc), y_gc)
    loss_gc.backward()
    
    # Check gradient norm before clipping
    total_norm_before = 0
    for p in model_gc.parameters():
        if p.grad is not None:
            total_norm_before += p.grad.data.norm(2).item() ** 2
    total_norm_before = total_norm_before ** 0.5
    
    # Clip
    torch.nn.utils.clip_grad_norm_(model_gc.parameters(), max_norm=1.0)
    
    total_norm_after = 0
    for p in model_gc.parameters():
        if p.grad is not None:
            total_norm_after += p.grad.data.norm(2).item() ** 2
    total_norm_after = total_norm_after ** 0.5
    
    print(f"  Grad norm before clip: {total_norm_before:.4f}")
    print(f"  Grad norm after clip:  {total_norm_after:.4f}")


# =====================================================================
#   PARTE 22: WEIGHT INITIALIZATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 22: INIT ===")
print("="*80)

"""
Weight initialization matters:
  - Xavier/Glorot: for sigmoid/tanh. Var = 2/(fan_in + fan_out).
  - Kaiming/He: for ReLU. Var = 2/fan_in.
  - Orthogonal: for RNNs.
  - Normal/Uniform: simple.
"""

if HAS_TORCH:
    def init_weights(m):
        if isinstance(m, nn.Linear):
            nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
            if m.bias is not None:
                nn.init.zeros_(m.bias)
    
    init_model = nn.Sequential(nn.Linear(10, 32), nn.ReLU(), nn.Linear(32, 2))
    init_model.apply(init_weights)
    
    for name, param in init_model.named_parameters():
        if 'weight' in name:
            print(f"  {name}: mean={param.data.mean():.4f}, std={param.data.std():.4f}")


# =====================================================================
#   PARTE 23: NN.SEQUENTIAL
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 23: SEQUENTIAL ===")
print("="*80)

if HAS_TORCH:
    seq_model = nn.Sequential(
        nn.Linear(20, 128),
        nn.ReLU(),
        nn.BatchNorm1d(128),
        nn.Dropout(0.3),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 10),
    )
    
    print(f"  Sequential model:")
    for i, layer in enumerate(seq_model):
        print(f"    [{i}] {layer}")
    
    out = seq_model(torch.randn(5, 20))
    print(f"  Output: {out.shape}")


# =====================================================================
#   PARTE 24: EARLY STOPPING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 24: EARLY STOPPING ===")
print("="*80)

class EarlyStopping:
    """Stop training when validation loss stops improving."""
    
    def __init__(self, patience=5, min_delta=0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.should_stop = False
    
    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0
        return self.should_stop

es = EarlyStopping(patience=3)
losses = [1.0, 0.8, 0.7, 0.72, 0.73, 0.74, 0.75]
for i, loss in enumerate(losses):
    stop = es(loss)
    print(f"  epoch {i}: loss={loss:.2f}, counter={es.counter}, stop={stop}")


# =====================================================================
#   PARTE 25: BROADCASTING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 25: BROADCASTING ===")
print("="*80)

if HAS_TORCH:
    # Broadcasting rules (same as numpy)
    a = torch.randn(3, 4)
    b = torch.randn(4)
    c = a + b  # b broadcasts along dim 0
    print(f"  {a.shape} + {b.shape} = {c.shape}")
    
    d = torch.randn(3, 1)
    e = a + d  # d broadcasts along dim 1
    print(f"  {a.shape} + {d.shape} = {e.shape}")


# =====================================================================
#   PARTE 26: EINSUM
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 26: EINSUM ===")
print("="*80)

"""
torch.einsum: Einstein notation for tensor operations.
Powerful and concise for complex tensor operations.
"""

if HAS_TORCH:
    A = torch.randn(3, 4)
    B = torch.randn(4, 5)
    
    # Matrix multiply
    C = torch.einsum('ij,jk->ik', A, B)
    print(f"  matmul: {C.shape}")
    
    # Batch matmul
    batch_A = torch.randn(8, 3, 4)
    batch_B = torch.randn(8, 4, 5)
    batch_C = torch.einsum('bij,bjk->bik', batch_A, batch_B)
    print(f"  batch matmul: {batch_C.shape}")
    
    # Trace
    sq = torch.randn(4, 4)
    trace = torch.einsum('ii->', sq)
    print(f"  trace: {trace.item():.4f}")
    
    # Dot product
    v1 = torch.randn(5)
    v2 = torch.randn(5)
    dot = torch.einsum('i,i->', v1, v2)
    print(f"  dot: {dot.item():.4f}")


# =====================================================================
#   PARTE 27: CHECKPOINT PATTERN
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 27: CHECKPOINT ===")
print("="*80)

"""
Checkpoint: save model + optimizer + epoch for resuming training.

checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
    'best_val_loss': best_val_loss,
}
torch.save(checkpoint, 'checkpoint.pth')

# Resume:
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
"""

print("  Checkpoint pattern:")
print("    Save: model + optimizer + epoch + loss")
print("    Resume: load all, continue training")
print("    Best model: save when val_loss improves")


# =====================================================================
#   PARTE 28: MODEL SUMMARY
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 28: MODEL SUMMARY ===")
print("="*80)

if HAS_TORCH:
    def model_summary(model):
        """Print model summary like Keras."""
        total_params = 0
        trainable_params = 0
        
        print(f"  {'Layer':>30s} {'Shape':>15s} {'Params':>10s}")
        print(f"  " + "-"*58)
        for name, param in model.named_parameters():
            n = param.numel()
            total_params += n
            if param.requires_grad:
                trainable_params += n
            print(f"  {name:>30s} {str(list(param.shape)):>15s} {n:>10,}")
        
        print(f"  " + "-"*58)
        print(f"  Total params: {total_params:,}")
        print(f"  Trainable:    {trainable_params:,}")
        return total_params
    
    model_summary(seq_model)


# =====================================================================
#   PARTE 29: TRAINING UTILITIES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 29: UTILITIES ===")
print("="*80)

if HAS_TORCH:
    class Trainer:
        """Reusable training class."""
        
        def __init__(self, model, criterion, optimizer, device='cpu'):
            self.model = model.to(device)
            self.criterion = criterion
            self.optimizer = optimizer
            self.device = device
            self.history = {'train_loss': [], 'val_loss': []}
        
        def train_epoch(self, loader):
            self.model.train()
            total_loss = 0
            for xb, yb in loader:
                xb, yb = xb.to(self.device), yb.to(self.device)
                self.optimizer.zero_grad()
                loss = self.criterion(self.model(xb), yb)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            return total_loss / len(loader)
        
        def evaluate(self, loader):
            self.model.eval()
            total_loss = 0
            correct = 0
            total = 0
            with torch.no_grad():
                for xb, yb in loader:
                    xb, yb = xb.to(self.device), yb.to(self.device)
                    out = self.model(xb)
                    total_loss += self.criterion(out, yb).item()
                    correct += (out.argmax(1) == yb).sum().item()
                    total += yb.size(0)
            return total_loss / len(loader), correct / total
    
    print("  Trainer class: encapsulates train/eval logic")
    print("  Usage: trainer = Trainer(model, criterion, optimizer)")


# =====================================================================
#   PARTE 30: TENSOR MEMORY
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 30: MEMORY ===")
print("="*80)

if HAS_TORCH:
    t_f32 = torch.randn(1000, 1000)
    t_f16 = t_f32.half()
    
    print(f"  float32: {t_f32.element_size() * t_f32.nelement() / 1e6:.1f} MB")
    print(f"  float16: {t_f16.element_size() * t_f16.nelement() / 1e6:.1f} MB")
    print(f"  Savings: {(1 - t_f16.element_size()/t_f32.element_size())*100:.0f}%")
    
    # Detach from graph
    x_detach = torch.randn(3, requires_grad=True)
    y_detach = x_detach * 2
    z_detach = y_detach.detach()  # no gradient tracking
    print(f"\n  detach: requires_grad={z_detach.requires_grad}")

print("\n" + "="*80)
print("=== CONCLUSION ===")
print("="*80)

"""
RESUMEN PYTORCH FUNDAMENTOS:
1. Tensores: creacion, dtypes, operaciones, indexing.
2. Autograd: gradientes automaticos, computational graph.
3. nn.Module: definir modelos, forward pass.
4. Training loop: forward, loss, backward, step.
5. Dataset/DataLoader: batch processing.
6. Regularization: dropout, batchnorm, weight decay.
7. Save/Load: state_dict pattern.
8. GPU: .to(device) para portabilidad.
"""

print("\n FIN DE ARCHIVO 01_tensores_y_autograd.")
print(" PyTorch fundamentos dominados.")
