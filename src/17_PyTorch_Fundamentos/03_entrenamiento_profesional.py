# ===========================================================================
# 03_entrenamiento_profesional.py
# ===========================================================================
# MODULO 17: PYTORCH FUNDAMENTOS
# ARCHIVO 03: Training Loop Profesional, Optimizadores, Schedulers
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar el entrenamiento de redes neuronales en produccion:
# training loop robusto, optimizadores avanzados, learning rate
# scheduling, gradient accumulation, mixed precision, checkpointing,
# y patrones de entrenamiento distribuido.
#
# CONTENIDO:
#   1. Training loop basico vs profesional.
#   2. Optimizadores: SGD, Adam, AdamW, LAMB.
#   3. Learning rate scheduling: step, cosine, warmup.
#   4. Gradient clipping y accumulation.
#   5. Mixed precision training (AMP).
#   6. Checkpointing y resume.
#   7. Early stopping robusto.
#   8. Logging y experiment tracking.
#   9. Reproducibilidad: seeds y determinismo.
#   10. Training utilities: EMA, label smoothing.
#   11. Pipeline de entrenamiento completo.
#
# NIVEL: DEEP LEARNING ENGINEER / MLOPS.
# ===========================================================================

import numpy as np
import time
import os
import json
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import Dataset, DataLoader, TensorDataset, random_split
    HAS_TORCH = True
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"  PyTorch: {torch.__version__}, Device: {DEVICE}")
except ImportError:
    HAS_TORCH = False
    print("  PyTorch not available.")


# =====================================================================
#   PARTE 1: TRAINING LOOP BASICO vs PROFESIONAL
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: TRAINING LOOP — DE BASICO A PROFESIONAL ===")
print("=" * 80)

"""
TRAINING LOOP BASICO (tutorial de PyTorch):
  for epoch in range(n_epochs):
      for batch in loader:
          optimizer.zero_grad()
          output = model(batch)
          loss = criterion(output, target)
          loss.backward()
          optimizer.step()

PROBLEMAS:
  - No valida.
  - No guarda checkpoints.
  - No hace gradient clipping.
  - No loguea metricas.
  - No soporta mixed precision.
  - No tiene early stopping.
  - No es reproducible.

TRAINING LOOP PROFESIONAL necesita TODO lo anterior.
Vamos a construirlo pieza por pieza.
"""


# =====================================================================
#   PARTE 2: OPTIMIZADORES EN PROFUNDIDAD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: OPTIMIZADORES ===")
print("=" * 80)

"""
TODOS los optimizadores hacen: θ_new = θ_old - update

La diferencia es COMO calculan 'update'.

1. SGD: update = lr * gradient
   Simple. Puede ser lento. Oscila en valles estrechos.
   + Con momentum: acumula velocidad en la direccion consistente.

2. ADAM (Adaptive Moment Estimation):
   Mantiene media movil del gradiente (m) y del cuadrado (v).
   update = lr * m / (√v + ε)
   → Adapta lr POR PARAMETRO.
   → Funciona bien casi siempre.

3. ADAMW (Adam + Weight Decay desacoplado):
   Adam regular aplica weight decay DENTRO del update adaptivo.
   AdamW lo aplica SEPARADO → regularizacion correcta.
   → STANDARD en deep learning moderno.

4. LAMB (Layer-wise Adaptive):
   Escala el update por la norma de los pesos de cada capa.
   → Permite batch sizes ENORMES (BERT usaba LAMB).

REGLA PRACTICA:
  - Empieza con AdamW (lr=1e-3 a 3e-4).
  - Si overfitting: sube weight_decay.
  - Para fine-tuning: lr mas bajo (1e-5 a 5e-5).
  - SGD + momentum: a veces generaliza mejor, pero requiere mas tuning.
"""

if HAS_TORCH:
    from sklearn.datasets import make_classification

    # Crear dataset comun
    X_np, y_np = make_classification(
        n_samples=2000, n_features=20, n_informative=12,
        n_classes=2, random_state=42
    )
    X_all = torch.tensor(X_np, dtype=torch.float32)
    y_all = torch.tensor(y_np, dtype=torch.long)

    # Split
    train_ds = TensorDataset(X_all[:1600], y_all[:1600])
    val_ds = TensorDataset(X_all[1600:], y_all[1600:])
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=256)

    # Modelo simple para comparar optimizadores
    def make_model():
        torch.manual_seed(42)
        return nn.Sequential(
            nn.Linear(20, 64), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(64, 32), nn.BatchNorm1d(32), nn.ReLU(),
            nn.Linear(32, 2),
        )

    def train_with_optimizer(opt_class, opt_kwargs, n_epochs=20):
        model = make_model()
        optimizer = opt_class(model.parameters(), **opt_kwargs)
        criterion = nn.CrossEntropyLoss()
        history = []

        for epoch in range(n_epochs):
            model.train()
            total_loss = 0
            for xb, yb in train_loader:
                optimizer.zero_grad()
                loss = criterion(model(xb), yb)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()

            model.eval()
            with torch.no_grad():
                val_correct = sum(
                    (model(xb).argmax(1) == yb).sum().item()
                    for xb, yb in val_loader
                )
                val_acc = val_correct / len(val_ds)

            history.append({
                'loss': total_loss / len(train_loader),
                'val_acc': val_acc,
            })

        return history

    print("\n--- Comparando optimizadores ---")

    optimizers = {
        'SGD (lr=0.01)': (torch.optim.SGD, {'lr': 0.01}),
        'SGD+Mom (0.9)': (torch.optim.SGD, {'lr': 0.01, 'momentum': 0.9}),
        'Adam (1e-3)': (torch.optim.Adam, {'lr': 1e-3}),
        'AdamW (1e-3)': (torch.optim.AdamW, {'lr': 1e-3, 'weight_decay': 0.01}),
    }

    results = {}
    for name, (opt_cls, opt_kw) in optimizers.items():
        hist = train_with_optimizer(opt_cls, opt_kw, n_epochs=20)
        results[name] = hist
        final = hist[-1]
        print(f"  {name:<18} loss={final['loss']:.4f}  val_acc={final['val_acc']:.4f}")

    print(f"\n  → AdamW es el standard. SGD+momentum puede generalizar mejor con tuning.")


# =====================================================================
#   PARTE 3: LEARNING RATE SCHEDULING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: LEARNING RATE SCHEDULING ===")
print("=" * 80)

"""
EL learning rate es EL hiperparametro mas importante.

Demasiado alto → diverge.
Demasiado bajo → converge MUY lento.
Constante → sub-optimo.

SCHEDULERS:

1. STEP DECAY: reduce lr cada N epochs por factor gamma.
   lr = lr_0 * gamma^(epoch // step_size)
   Simple pero brusco.

2. COSINE ANNEALING: lr sigue un coseno de lr_max a lr_min.
   Suave, sin cambios bruscos. MUY popular.

3. WARMUP + COSINE: empieza con lr=0, sube linealmente, luego cosine.
   STANDARD en transformers. Evita inestabilidad al inicio.

4. ONE CYCLE: sube a lr_max y luego baja. Super-convergencia.
   Permite lr MUY altos → entrena rapido.

5. REDUCE ON PLATEAU: reduce lr cuando la metrica se estanca.
   Reactivo, bueno cuando no sabes cuanto entrenar.
"""

if HAS_TORCH:
    print("\n--- Visualizando schedulers ---")

    def simulate_scheduler(scheduler_cls, scheduler_kwargs,
                           optimizer_lr=0.1, n_epochs=50):
        """Simula un scheduler sin entrenar."""
        model_dummy = nn.Linear(1, 1)
        opt = torch.optim.SGD(model_dummy.parameters(), lr=optimizer_lr)
        sched = scheduler_cls(opt, **scheduler_kwargs)
        lrs = []
        for _ in range(n_epochs):
            lrs.append(opt.param_groups[0]['lr'])
            # Simular step
            opt.step()
            sched.step()
        return lrs

    schedulers = {
        'StepLR': (torch.optim.lr_scheduler.StepLR,
                   {'step_size': 10, 'gamma': 0.5}),
        'CosineAnnealing': (torch.optim.lr_scheduler.CosineAnnealingLR,
                            {'T_max': 50, 'eta_min': 1e-4}),
        'ExponentialLR': (torch.optim.lr_scheduler.ExponentialLR,
                          {'gamma': 0.95}),
    }

    print(f"  {'Epoch':<8}", end="")
    for name in schedulers:
        print(f" {name:>18}", end="")
    print()

    all_lrs = {}
    for name, (cls, kwargs) in schedulers.items():
        all_lrs[name] = simulate_scheduler(cls, kwargs, optimizer_lr=0.1)

    for epoch in [0, 10, 20, 30, 40, 49]:
        print(f"  {epoch:<8}", end="")
        for name in schedulers:
            print(f" {all_lrs[name][epoch]:18.6f}", end="")
        print()

    # Warmup + Cosine (manual)
    print("\n--- Warmup + Cosine Decay (patron de transformers) ---")

    def warmup_cosine_lr(epoch, warmup_epochs=5, total_epochs=50,
                         lr_max=0.001, lr_min=1e-6):
        if epoch < warmup_epochs:
            return lr_max * (epoch + 1) / warmup_epochs
        progress = (epoch - warmup_epochs) / (total_epochs - warmup_epochs)
        return lr_min + 0.5 * (lr_max - lr_min) * (1 + np.cos(np.pi * progress))

    print(f"  {'Epoch':<8} {'LR':>12}")
    for e in [0, 2, 5, 10, 25, 49]:
        lr = warmup_cosine_lr(e)
        print(f"  {e:<8} {lr:12.8f}")


# =====================================================================
#   PARTE 4: GRADIENT CLIPPING Y ACCUMULATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: GRADIENT CLIPPING & ACCUMULATION ===")
print("=" * 80)

"""
GRADIENT CLIPPING:
  Limita la norma de los gradientes para evitar explosion.
  Esencial en RNNs y transformers.

  torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

GRADIENT ACCUMULATION:
  Simula batch sizes mas grandes sin mas memoria GPU.

  Quieres batch_size=256 pero solo caben 32 en GPU:
  → Acumula gradientes de 8 mini-batches de 32.
  → Solo haces optimizer.step() cada 8 batches.

  accumulation_steps = effective_batch_size / actual_batch_size
"""

if HAS_TORCH:
    print("\n--- Gradient Clipping ---")

    model_clip = make_model()
    opt_clip = torch.optim.Adam(model_clip.parameters(), lr=0.001)

    # Sin clipping
    xb, yb = next(iter(train_loader))
    opt_clip.zero_grad()
    loss = nn.CrossEntropyLoss()(model_clip(xb), yb)
    loss.backward()

    grad_norm_before = torch.nn.utils.clip_grad_norm_(
        model_clip.parameters(), float('inf')
    )
    print(f"  Grad norm (sin clip): {grad_norm_before:.4f}")

    # Con clipping
    opt_clip.zero_grad()
    loss = nn.CrossEntropyLoss()(model_clip(xb), yb)
    loss.backward()

    grad_norm_after = torch.nn.utils.clip_grad_norm_(
        model_clip.parameters(), max_norm=1.0
    )
    print(f"  Grad norm (clip=1.0): {grad_norm_after:.4f}")

    # Gradient Accumulation
    print("\n--- Gradient Accumulation ---")

    accumulation_steps = 4
    effective_batch = 64 * accumulation_steps

    model_acc = make_model()
    opt_acc = torch.optim.Adam(model_acc.parameters(), lr=0.001)

    model_acc.train()
    opt_acc.zero_grad()
    total_loss = 0

    for step, (xb, yb) in enumerate(train_loader):
        loss = nn.CrossEntropyLoss()(model_acc(xb), yb)
        loss = loss / accumulation_steps  # Normalizar
        loss.backward()
        total_loss += loss.item()

        if (step + 1) % accumulation_steps == 0:
            torch.nn.utils.clip_grad_norm_(model_acc.parameters(), 1.0)
            opt_acc.step()
            opt_acc.zero_grad()

        if step >= 7:
            break

    print(f"  Effective batch size: {effective_batch}")
    print(f"  Actual batch size: 64")
    print(f"  Accumulation steps: {accumulation_steps}")
    print(f"  → Misma calidad, menos memoria GPU")


# =====================================================================
#   PARTE 5: CHECKPOINTING Y RESUME
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: CHECKPOINTING ===")
print("=" * 80)

"""
CHECKPOINTING: guardar el estado del entrenamiento para:
1. Reanudar si se cae la maquina.
2. Seleccionar el mejor modelo (por val_loss).
3. Compartir modelos.

QUE GUARDAR:
  - model.state_dict(): pesos del modelo.
  - optimizer.state_dict(): estado del optimizador (momentum, etc).
  - epoch: en que epoch estabamos.
  - best_val_loss: para saber si mejorar.
  - scheduler.state_dict(): estado del LR scheduler.
"""

if HAS_TORCH:
    class CheckpointManager:
        """Maneja guardado y carga de checkpoints."""

        def __init__(self, save_dir: str, max_keep: int = 3):
            self.save_dir = save_dir
            self.max_keep = max_keep
            self._checkpoints: List[str] = []
            os.makedirs(save_dir, exist_ok=True)

        def save(self, model, optimizer, epoch, val_loss,
                 scheduler=None, extra=None):
            """Guarda checkpoint."""
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_loss,
            }
            if scheduler:
                checkpoint['scheduler_state_dict'] = scheduler.state_dict()
            if extra:
                checkpoint.update(extra)

            path = os.path.join(self.save_dir, f'checkpoint_epoch{epoch}.pt')
            torch.save(checkpoint, path)
            self._checkpoints.append(path)

            # Limpiar checkpoints viejos
            while len(self._checkpoints) > self.max_keep:
                old = self._checkpoints.pop(0)
                if os.path.exists(old):
                    os.remove(old)

            return path

        def load_latest(self, model, optimizer, scheduler=None):
            """Carga el ultimo checkpoint."""
            if not self._checkpoints:
                return None

            path = self._checkpoints[-1]
            checkpoint = torch.load(path, weights_only=False)

            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            if scheduler and 'scheduler_state_dict' in checkpoint:
                scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

            return checkpoint

    # Demo
    print("\n--- Checkpoint Manager ---")
    ckpt_dir = '/tmp/pytorch_checkpoints'
    ckpt_mgr = CheckpointManager(ckpt_dir, max_keep=2)

    model_ckpt = make_model()
    opt_ckpt = torch.optim.Adam(model_ckpt.parameters())

    # Guardar checkpoints
    for epoch in range(5):
        path = ckpt_mgr.save(model_ckpt, opt_ckpt, epoch, val_loss=0.5-epoch*0.1)
        print(f"  Saved epoch {epoch}: {os.path.basename(path)}")

    print(f"  Checkpoints guardados: {len(ckpt_mgr._checkpoints)}")
    print(f"  → max_keep=2: solo los 2 mas recientes")


# =====================================================================
#   PARTE 6: EARLY STOPPING ROBUSTO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: EARLY STOPPING ===")
print("=" * 80)

"""
EARLY STOPPING: detener entrenamiento cuando val_loss deja de mejorar.

PARAMETROS:
  patience: cuantos epochs esperar sin mejora.
  min_delta: mejora minima para contar como mejora.
  mode: 'min' (loss) o 'max' (accuracy).

BEST PRACTICE:
  patience = 5-10 epochs.
  Guardar el mejor modelo, no el ultimo.
"""

if HAS_TORCH:
    class EarlyStopping:
        """Early stopping con restore del mejor modelo."""

        def __init__(self, patience: int = 5, min_delta: float = 1e-4,
                     mode: str = 'min'):
            self.patience = patience
            self.min_delta = min_delta
            self.mode = mode
            self.counter = 0
            self.best_value = float('inf') if mode == 'min' else -float('inf')
            self.best_state = None
            self.should_stop = False

        def __call__(self, value, model) -> bool:
            improved = False
            if self.mode == 'min':
                improved = value < self.best_value - self.min_delta
            else:
                improved = value > self.best_value + self.min_delta

            if improved:
                self.best_value = value
                self.best_state = {k: v.clone() for k, v in model.state_dict().items()}
                self.counter = 0
            else:
                self.counter += 1
                if self.counter >= self.patience:
                    self.should_stop = True

            return self.should_stop

        def restore_best(self, model):
            """Restaura los pesos del mejor epoch."""
            if self.best_state:
                model.load_state_dict(self.best_state)

    # Demo
    print("\n--- Early Stopping ---")
    es = EarlyStopping(patience=3, mode='min')
    simulated_losses = [0.8, 0.6, 0.5, 0.5, 0.51, 0.52, 0.53]

    model_es = make_model()
    for epoch, loss in enumerate(simulated_losses):
        stop = es(loss, model_es)
        print(f"  Epoch {epoch}: loss={loss:.2f}, "
              f"counter={es.counter}, stop={stop}")
        if stop:
            print(f"  → Stopped! Best loss: {es.best_value:.2f}")
            break


# =====================================================================
#   PARTE 7: EXPERIMENT TRACKING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: EXPERIMENT TRACKING ===")
print("=" * 80)

"""
SIN tracking, despues de 50 experimentos no recuerdas:
  - Que hiperparametros uso el mejor modelo.
  - Que datos uso.
  - Si ya probaste esa configuracion.

HERRAMIENTAS: MLflow, Weights & Biases, TensorBoard.
Nosotros hacemos uno simple pero funcional.
"""

if HAS_TORCH:
    class ExperimentTracker:
        """Tracking simple de experimentos."""

        def __init__(self, experiment_name: str):
            self.name = experiment_name
            self._runs: List[Dict] = []
            self._current_run: Optional[Dict] = None

        def start_run(self, config: Dict):
            self._current_run = {
                'config': config,
                'metrics': [],
                'start_time': time.time(),
            }

        def log_metrics(self, epoch: int, **kwargs):
            if self._current_run:
                self._current_run['metrics'].append({'epoch': epoch, **kwargs})

        def end_run(self, final_metrics: Dict = None):
            if self._current_run:
                self._current_run['duration'] = time.time() - self._current_run['start_time']
                if final_metrics:
                    self._current_run['final'] = final_metrics
                self._runs.append(self._current_run)
                self._current_run = None

        def best_run(self, metric: str = 'val_acc', mode: str = 'max') -> Dict:
            if not self._runs:
                return {}
            key_fn = lambda r: r.get('final', {}).get(metric, -float('inf') if mode == 'max' else float('inf'))
            return max(self._runs, key=key_fn) if mode == 'max' else min(self._runs, key=key_fn)

        def summary(self):
            print(f"\n  Experiment: {self.name}, {len(self._runs)} runs")
            for i, run in enumerate(self._runs):
                final = run.get('final', {})
                config = run['config']
                print(f"    Run {i+1}: lr={config.get('lr')}, "
                      f"val_acc={final.get('val_acc', '?'):.4f}, "
                      f"duration={run['duration']:.1f}s")

    # Demo
    print("\n--- Experiment Tracking ---")
    tracker = ExperimentTracker("optimizer_search")

    for lr in [0.01, 0.001, 0.0001]:
        tracker.start_run({'lr': lr, 'optimizer': 'AdamW'})

        model_exp = make_model()
        opt_exp = torch.optim.AdamW(model_exp.parameters(), lr=lr)

        for epoch in range(10):
            model_exp.train()
            for xb, yb in train_loader:
                opt_exp.zero_grad()
                loss = nn.CrossEntropyLoss()(model_exp(xb), yb)
                loss.backward()
                opt_exp.step()

            model_exp.eval()
            with torch.no_grad():
                val_acc = sum(
                    (model_exp(xb).argmax(1) == yb).sum().item()
                    for xb, yb in val_loader
                ) / len(val_ds)

            tracker.log_metrics(epoch, val_acc=val_acc, loss=loss.item())

        tracker.end_run({'val_acc': val_acc})

    tracker.summary()
    best = tracker.best_run('val_acc', 'max')
          f"val_acc={best['final']['val_acc']:.4f}")


# =====================================================================
#   PARTE 8: REPRODUCIBILIDAD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: REPRODUCIBILIDAD ===")
print("=" * 80)

"""
REPRODUCIBILIDAD: ejecutar el mismo codigo → mismo resultado.

FUENTES DE NO-DETERMINISMO:
1. Random seeds (numpy, python, torch).
2. CUDA operations (algunos kernels son no-deterministas).
3. DataLoader workers (orden de datos).
4. Floating point operations (orden de suma).

SOLUCION:
  Fijar TODAS las semillas + flags de determinismo.
"""

if HAS_TORCH:
    def set_seed(seed: int = 42):
        """Fija TODAS las semillas para reproducibilidad."""
        import random
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
        # Determinismo (puede ser mas lento)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    # Verificar reproducibilidad
    print("\n--- Test de reproducibilidad ---")
    results_repro = []
    for run in range(3):
        set_seed(42)
        model_r = make_model()
        opt_r = torch.optim.Adam(model_r.parameters(), lr=0.001)

        model_r.train()
        for xb, yb in train_loader:
            opt_r.zero_grad()
            loss = nn.CrossEntropyLoss()(model_r(xb), yb)
            loss.backward()
            opt_r.step()
            break  # Solo 1 batch

        # Verificar que los pesos son iguales
        first_param = list(model_r.parameters())[0].data[0, :3].tolist()
        results_repro.append(first_param)
        print(f"  Run {run+1}: pesos[0,:3] = {[f'{v:.6f}' for v in first_param]}")

    match = all(r == results_repro[0] for r in results_repro)
    print(f"  Reproducible: {match} ✓" if match else "  NOT reproducible ✗")


# =====================================================================
#   PARTE 9: EMA (EXPONENTIAL MOVING AVERAGE)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: EMA — PESOS SUAVIZADOS ===")
print("=" * 80)

"""
EMA: mantener una copia "suavizada" de los pesos del modelo.

  ema_weights = decay * ema_weights + (1 - decay) * model_weights

BENEFICIOS:
  - Los pesos EMA son mas estables que los ultimos pesos.
  - Generalizan mejor (menos ruido de SGD).
  - STANDARD en modelos de produccion (GPT, difusion models).

DECAY tipico: 0.999 o 0.9999.

USO:
  - Entrenar con pesos normales.
  - Evaluar/servir con pesos EMA.
"""

if HAS_TORCH:
    class EMAModel:
        """Exponential Moving Average de pesos."""

        def __init__(self, model: nn.Module, decay: float = 0.999):
            self.decay = decay
            self.shadow = {}
            self.backup = {}

            for name, param in model.named_parameters():
                if param.requires_grad:
                    self.shadow[name] = param.data.clone()

        def update(self, model: nn.Module):
            """Actualiza pesos EMA."""
            for name, param in model.named_parameters():
                if param.requires_grad and name in self.shadow:
                    self.shadow[name] = (
                        self.decay * self.shadow[name] +
                        (1 - self.decay) * param.data
                    )

        def apply(self, model: nn.Module):
            """Reemplaza pesos del modelo con EMA (para eval)."""
            for name, param in model.named_parameters():
                if param.requires_grad and name in self.shadow:
                    self.backup[name] = param.data.clone()
                    param.data = self.shadow[name]

        def restore(self, model: nn.Module):
            """Restaura pesos originales (para seguir entrenando)."""
            for name, param in model.named_parameters():
                if name in self.backup:
                    param.data = self.backup[name]
            self.backup = {}

    # Demo
    print("\n--- EMA ---")
    set_seed(42)
    model_ema_demo = make_model()
    ema = EMAModel(model_ema_demo, decay=0.99)
    opt_ema = torch.optim.Adam(model_ema_demo.parameters(), lr=0.001)

    model_ema_demo.train()
    for epoch in range(10):
        for xb, yb in train_loader:
            opt_ema.zero_grad()
            loss = nn.CrossEntropyLoss()(model_ema_demo(xb), yb)
            loss.backward()
            opt_ema.step()
            ema.update(model_ema_demo)

    # Evaluar con pesos normales
    model_ema_demo.eval()
    with torch.no_grad():
        val_acc_normal = sum(
            (model_ema_demo(xb).argmax(1) == yb).sum().item()
            for xb, yb in val_loader
        ) / len(val_ds)

    # Evaluar con pesos EMA
    ema.apply(model_ema_demo)
    with torch.no_grad():
        val_acc_ema = sum(
            (model_ema_demo(xb).argmax(1) == yb).sum().item()
            for xb, yb in val_loader
        ) / len(val_ds)
    ema.restore(model_ema_demo)

    print(f"  Val accuracy (normal):  {val_acc_normal:.4f}")
    print(f"  Val accuracy (EMA):     {val_acc_ema:.4f}")
    print(f"  → EMA suele generalizar mejor o igual")


# =====================================================================
#   PARTE 10: LABEL SMOOTHING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: LABEL SMOOTHING ===")
print("=" * 80)

"""
LABEL SMOOTHING (Szegedy et al., 2016):

En vez de targets "duros" [0, 1], usa targets "suaves":
  y_smooth = (1 - ε) * y_hard + ε / K

Ejemplo con K=3 clases y ε=0.1:
  Hard:  [0, 1, 0]
  Smooth: [0.033, 0.933, 0.033]

BENEFICIOS:
  - Previene sobreconfianza del modelo.
  - Mejor calibracion de probabilidades.
  - Actua como regularizador.

PyTorch: nn.CrossEntropyLoss(label_smoothing=0.1)
"""

if HAS_TORCH:
    print("\n--- Label Smoothing ---")

    set_seed(42)

    # Sin label smoothing
    model_no_ls = make_model()
    opt1 = torch.optim.Adam(model_no_ls.parameters(), lr=0.001)
    criterion_hard = nn.CrossEntropyLoss(label_smoothing=0.0)

    # Con label smoothing
    model_ls = make_model()
    opt2 = torch.optim.Adam(model_ls.parameters(), lr=0.001)
    criterion_smooth = nn.CrossEntropyLoss(label_smoothing=0.1)

    for epoch in range(15):
        for (xb, yb) in train_loader:
            opt1.zero_grad()
            loss1 = criterion_hard(model_no_ls(xb), yb)
            loss1.backward()
            opt1.step()

            opt2.zero_grad()
            loss2 = criterion_smooth(model_ls(xb), yb)
            loss2.backward()
            opt2.step()

    # Evaluar confianza
    model_no_ls.eval()
    model_ls.eval()

    with torch.no_grad():
        probs_hard = F.softmax(model_no_ls(X_all[1600:]), dim=1)
        probs_smooth = F.softmax(model_ls(X_all[1600:]), dim=1)

    max_conf_hard = probs_hard.max(1).values.mean().item()
    max_conf_smooth = probs_smooth.max(1).values.mean().item()

    print(f"  Confianza promedio (sin smoothing): {max_conf_hard:.4f}")
    print(f"  Confianza promedio (con smoothing): {max_conf_smooth:.4f}")
    print(f"  → Label smoothing reduce sobreconfianza")


# =====================================================================
#   PARTE 11: PIPELINE DE ENTRENAMIENTO COMPLETO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: PIPELINE PROFESIONAL COMPLETO ===")
print("=" * 80)

"""
Juntamos TODAS las piezas en un Trainer reutilizable:
  - Optimizador (AdamW)
  - LR scheduler (cosine con warmup)
  - Gradient clipping
  - Early stopping
  - Checkpointing
  - EMA
  - Label smoothing
  - Experiment tracking
  - Reproducibilidad
"""

if HAS_TORCH:
    class ProfessionalTrainer:
        """Trainer profesional que combina todas las best practices."""

        def __init__(self, model, train_loader, val_loader,
                     lr=1e-3, weight_decay=0.01, max_epochs=50,
                     patience=7, grad_clip=1.0, label_smoothing=0.1,
                     ema_decay=0.999, seed=42):
            self.model = model
            self.train_loader = train_loader
            self.val_loader = val_loader
            self.max_epochs = max_epochs
            self.grad_clip = grad_clip

            # Seed
            set_seed(seed)

            # Optimizer + Scheduler
            self.optimizer = torch.optim.AdamW(
                model.parameters(), lr=lr, weight_decay=weight_decay
            )
            self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=max_epochs
            )

            # Loss con label smoothing
            self.criterion = nn.CrossEntropyLoss(label_smoothing=label_smoothing)

            # Early stopping
            self.early_stopping = EarlyStopping(patience=patience, mode='max')

            # EMA
            self.ema = EMAModel(model, decay=ema_decay)

            # History
            self.history: List[Dict] = []

        def train_epoch(self) -> float:
            self.model.train()
            total_loss = 0
            n_batches = 0
            for xb, yb in self.train_loader:
                self.optimizer.zero_grad()
                out = self.model(xb)
                loss = self.criterion(out, yb)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(), self.grad_clip
                )
                self.optimizer.step()
                self.ema.update(self.model)
                total_loss += loss.item()
                n_batches += 1
            return total_loss / n_batches

        @torch.no_grad()
        def validate(self, use_ema=True) -> Dict:
            if use_ema:
                self.ema.apply(self.model)

            self.model.eval()
            correct = 0
            total = 0
            total_loss = 0

            for xb, yb in self.val_loader:
                out = self.model(xb)
                loss = self.criterion(out, yb)
                total_loss += loss.item()
                correct += (out.argmax(1) == yb).sum().item()
                total += len(yb)

            if use_ema:
                self.ema.restore(self.model)

            return {
                'val_loss': total_loss / len(self.val_loader),
                'val_acc': correct / total,
            }

        def fit(self) -> List[Dict]:
            print(f"\n  {'Epoch':<7} {'Loss':>8} {'ValAcc':>8} "
                  f"{'ValLoss':>8} {'LR':>10} {'ES':>4}")

            for epoch in range(self.max_epochs):
                train_loss = self.train_epoch()
                val_metrics = self.validate(use_ema=True)
                self.scheduler.step()

                lr = self.optimizer.param_groups[0]['lr']
                stop = self.early_stopping(val_metrics['val_acc'], self.model)

                record = {
                    'epoch': epoch,
                    'train_loss': train_loss,
                    **val_metrics,
                    'lr': lr,
                }
                self.history.append(record)

                if epoch % 5 == 0 or stop:
                    es_counter = self.early_stopping.counter
                    print(f"  {epoch+1:<7} {train_loss:8.4f} "
                          f"{val_metrics['val_acc']:8.4f} "
                          f"{val_metrics['val_loss']:8.4f} "
                          f"{lr:10.6f} {es_counter:4d}")

                if stop:
                    print(f"  → Early stopping at epoch {epoch+1}")
                    self.early_stopping.restore_best(self.model)
                    break

            return self.history

    # Entrenar con el pipeline completo
    print("\n--- Pipeline Profesional ---")

    set_seed(42)
    model_final = nn.Sequential(
        nn.Linear(20, 128), nn.BatchNorm1d(128), nn.GELU(), nn.Dropout(0.3),
        nn.Linear(128, 64), nn.BatchNorm1d(64), nn.GELU(), nn.Dropout(0.2),
        nn.Linear(64, 32), nn.BatchNorm1d(32), nn.GELU(),
        nn.Linear(32, 2),
    )

    trainer = ProfessionalTrainer(
        model=model_final,
        train_loader=train_loader,
        val_loader=val_loader,
        lr=1e-3,
        weight_decay=0.01,
        max_epochs=40,
        patience=7,
        grad_clip=1.0,
        label_smoothing=0.1,
        ema_decay=0.999,
    )

    history = trainer.fit()

    # Resultado final
    best_epoch = max(history, key=lambda x: x['val_acc'])
    print(f"\n  Mejor epoch: {best_epoch['epoch']+1}")
    print(f"  Val accuracy: {best_epoch['val_acc']:.4f}")
    print(f"  Val loss: {best_epoch['val_loss']:.4f}")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: ENTRENAMIENTO PROFESIONAL ===")
print("=" * 80)

print("""
  RECETA DE ENTRENAMIENTO PROFESIONAL:

  1. OPTIMIZER: AdamW (lr=1e-3, weight_decay=0.01).
  2. SCHEDULER: Cosine Annealing (o warmup + cosine).
  3. GRADIENT CLIPPING: max_norm=1.0.
  4. GRADIENT ACCUMULATION: si batch no cabe en GPU.
  5. EARLY STOPPING: patience=5-10, restore best.
  6. CHECKPOINTING: guardar top-K modelos.
  7. EMA: decay=0.999, evaluar con pesos EMA.
  8. LABEL SMOOTHING: ε=0.1 para mejor calibracion.
  9. REPRODUCIBILIDAD: fijar TODAS las semillas.
  10. TRACKING: loguear todo para poder comparar.

  DEBUGGING:
    - Overfit 1 batch primero.
    - Verificar gradientes (no NaN, no zero).
    - Loss debe bajar monotonicamente en train.
    - Val loss sube = overfitting → mas regularizacion.

  HERRAMIENTAS REALES:
    - PyTorch Lightning: abstrae el training loop.
    - HuggingFace Trainer: para NLP/LLMs.
    - Weights & Biases: experiment tracking.
    - MLflow: lifecycle management.
""")

print("=" * 80)
print("=== FIN MODULO 17, ARCHIVO 03 ===")
print("=" * 80)
