# ===========================================================================
# 02_peft_y_lora.py
# ===========================================================================
# MODULO 20: TRANSFER LEARNING Y FINE-TUNING
# ARCHIVO 02: PEFT, LoRA, QLoRA — Fine-tuning Eficiente
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar tecnicas de Parameter-Efficient Fine-Tuning:
# LoRA, QLoRA, adapters, prefix tuning, y cuando usar cada una.
# Implementacion desde cero y comparativa.
#
# CONTENIDO:
#   1. El problema del full fine-tuning.
#   2. PEFT: paradigma de fine-tuning eficiente.
#   3. LoRA: Low-Rank Adaptation.
#   4. LoRA desde cero (implementacion).
#   5. Aplicar LoRA a un modelo.
#   6. Rank selection y alpha.
#   7. QLoRA: LoRA + quantizacion.
#   8. Adapters: modulos insertados.
#   9. Prefix Tuning: prompts aprendidos.
#   10. Comparativa de metodos PEFT.
#   11. Best practices para fine-tuning.
#
# NIVEL: LLM ENGINEER / MLOPS.
# ===========================================================================

import numpy as np
import math
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset
    HAS_TORCH = True
    print(f"  PyTorch: {torch.__version__}")
except ImportError:
    HAS_TORCH = False
    print("  PyTorch not available.")


# =====================================================================
#   PARTE 1: EL PROBLEMA DEL FULL FINE-TUNING
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: FULL FINE-TUNING ===")
print("=" * 80)

"""
FULL FINE-TUNING: actualizar TODOS los parametros del modelo.

PROBLEMAS:
1. MEMORIA: LLaMA 7B necesita ~28GB solo para pesos (FP32).
   + optimizer states (Adam): ~56GB mas.
   + gradientes: ~28GB mas.
   Total: ~112GB para un modelo de 7B. No cabe en una GPU!

2. ALMACENAMIENTO: guardar una copia completa por tarea.
   10 tareas × 7B params × 4 bytes = 280GB de checkpoints.

3. CATASTROPHIC FORGETTING: al fine-tunear,
   el modelo olvida conocimiento general.

4. OVERFITTING: datasets de fine-tuning son pequeños.
   Muchos params + pocos datos = overfitting garantizado.

SOLUCION: PEFT — actualizar POCOS parametros.
  LoRA: 0.1-1% de los parametros originales.
  → Cabe en 1 GPU consumer (16-24GB).
  → Un "adapter" por tarea (~10-50MB).
  → Menos overfitting.
  → Sin forgetting (pesos originales intactos).
"""

if HAS_TORCH:
    # Demostrar el problema de memoria
    def estimate_memory(n_params, dtype_bytes=4):
        """Estima memoria para fine-tuning."""
        weights = n_params * dtype_bytes / 1e9  # GB
        optimizer = weights * 2  # Adam: m + v
        gradients = weights
        total = weights + optimizer + gradients
        return {'weights': weights, 'optimizer': optimizer,
                'gradients': gradients, 'total': total}

    print("\n--- Memoria para full fine-tuning ---")
    models = {
        'GPT-2 (124M)': 124e6,
        'LLaMA 7B': 7e9,
        'LLaMA 13B': 13e9,
        'LLaMA 70B': 70e9,
    }
    for name, params in models.items():
        mem = estimate_memory(params)
        print(f"  {name:<15}: {mem['total']:.1f} GB total "
              f"(weights={mem['weights']:.1f}, opt={mem['optimizer']:.1f})")


# =====================================================================
#   PARTE 2: PEFT PARADIGMA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: PEFT — PARAMETER-EFFICIENT FINE-TUNING ===")
print("=" * 80)

"""
PEFT: modificar un modelo ENORME cambiando MUY POCOS parametros.

METODOS PRINCIPALES:

1. LoRA: añadir matrices de bajo rango a las proyecciones.
   → 0.1-1% params. Standard de la industria.

2. QLoRA: LoRA + modelo base en 4-bit.
   → Fine-tune LLaMA 65B en 1 GPU de 48GB.

3. Adapters: modulos pequeños insertados entre capas.
   → 1-5% params. Mas expresivo que LoRA.

4. Prefix Tuning: aprender "prompts" como vectores.
   → ~0.01% params. Menos expresivo.

5. Prompt Tuning: version mas simple de prefix tuning.
   → Casi 0% params. Solo funciona en modelos grandes.

REGLA: LoRA/QLoRA es el default. Usa otros si no funciona.
"""

print("""
  FULL FINE-TUNING:
    Modelo (7B params) → todo trainable → 7B params actualizados

  LoRA:
    Modelo (7B params) → FROZEN
    + LoRA adapters (~10M params) → solo estos se actualizan
    → 0.14% de los params originales!
""")


# =====================================================================
#   PARTE 3: LoRA — LOW-RANK ADAPTATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: LoRA ===")
print("=" * 80)

"""
LoRA (Hu et al., 2021):

IDEA: los cambios necesarios para adaptar un modelo son de BAJO RANGO.

  En vez de actualizar W (d × d), aprende:
  ΔW = B @ A  donde A es (r × d) y B es (d × r)

  r << d (tipicamente r=4, 8, 16, 64)

  W_new = W_frozen + α/r * (B @ A)

  α (alpha): factor de escala. Tipicamente α = r o α = 2*r.

PARAMETROS:
  Original W: d × d params.
  LoRA: r × d + d × r = 2 × r × d params.
  Si d=4096, r=8: 65K vs 16M params (250x menos!).

DONDE APLICAR LoRA:
  - Q, V projections (standard minimo).
  - Q, K, V, O projections (mejor).
  - + FFN up/down (maximo quality).
"""

if HAS_TORCH:
    class LoRALinear(nn.Module):
        """Linear layer con LoRA adapter."""

        def __init__(self, original_linear: nn.Linear, rank: int = 8,
                     alpha: float = 16.0):
            super().__init__()
            self.original = original_linear
            self.rank = rank
            self.alpha = alpha
            self.scaling = alpha / rank

            in_features = original_linear.in_features
            out_features = original_linear.out_features

            # Congelar pesos originales
            self.original.weight.requires_grad = False
            if self.original.bias is not None:
                self.original.bias.requires_grad = False

            # LoRA matrices
            self.lora_A = nn.Parameter(torch.randn(rank, in_features) * 0.01)
            self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
            # B inicializado a 0: al inicio, ΔW = 0

        def forward(self, x):
            # Original + LoRA delta
            original_out = self.original(x)
            lora_out = (x @ self.lora_A.T) @ self.lora_B.T * self.scaling
            return original_out + lora_out

        def merge(self):
            """Fusiona LoRA en los pesos originales (para inference)."""
            with torch.no_grad():
                self.original.weight += self.scaling * (self.lora_B @ self.lora_A)

        @property
        def n_trainable(self):
            return self.lora_A.numel() + self.lora_B.numel()

    # Demo
    print("\n--- LoRA Linear ---")

    original = nn.Linear(512, 512)
    lora = LoRALinear(original, rank=8, alpha=16)

    x = torch.randn(2, 10, 512)
    out = lora(x)

    total_params = sum(p.numel() for p in original.parameters())
    lora_params = lora.n_trainable
    trainable = sum(p.numel() for p in lora.parameters() if p.requires_grad)

    print(f"  Original params: {total_params:,}")
    print(f"  LoRA params: {lora_params:,}")
    print(f"  Trainable: {trainable:,}")
    print(f"  Ratio: {lora_params/total_params*100:.2f}%")
    print(f"  Input: {x.shape} → Output: {out.shape}")


# =====================================================================
#   PARTE 4: APLICAR LoRA A UN MODELO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: LoRA EN UN TRANSFORMER ===")
print("=" * 80)

if HAS_TORCH:
    class SimpleTransformerBlock(nn.Module):
        """Transformer block simple para demo."""
        def __init__(self, d_model, n_heads):
            super().__init__()
            self.ln1 = nn.LayerNorm(d_model)
            self.q_proj = nn.Linear(d_model, d_model)
            self.k_proj = nn.Linear(d_model, d_model)
            self.v_proj = nn.Linear(d_model, d_model)
            self.o_proj = nn.Linear(d_model, d_model)
            self.ln2 = nn.LayerNorm(d_model)
            self.ffn_up = nn.Linear(d_model, 4 * d_model)
            self.ffn_down = nn.Linear(4 * d_model, d_model)

        def forward(self, x):
            h = self.ln1(x)
            q, k, v = self.q_proj(h), self.k_proj(h), self.v_proj(h)
            attn = F.scaled_dot_product_attention(q, k, v)
            x = x + self.o_proj(attn)
            h = self.ln2(x)
            x = x + self.ffn_down(F.gelu(self.ffn_up(h)))
            return x

    class SimpleModel(nn.Module):
        def __init__(self, vocab_size, d_model, n_layers, n_heads):
            super().__init__()
            self.emb = nn.Embedding(vocab_size, d_model)
            self.blocks = nn.ModuleList([
                SimpleTransformerBlock(d_model, n_heads)
                for _ in range(n_layers)
            ])
            self.head = nn.Linear(d_model, vocab_size)

        def forward(self, x):
            x = self.emb(x)
            for block in self.blocks:
                x = block(x)
            return self.head(x)

    def apply_lora(model, rank=8, alpha=16, target_modules=None):
        """Aplica LoRA a un modelo existente."""
        if target_modules is None:
            target_modules = ['q_proj', 'v_proj']

        lora_count = 0
        for name, module in model.named_modules():
            for target in target_modules:
                if hasattr(module, target):
                    original = getattr(module, target)
                    if isinstance(original, nn.Linear):
                        lora_layer = LoRALinear(original, rank, alpha)
                        setattr(module, target, lora_layer)
                        lora_count += 1

        # Congelar todo excepto LoRA
        for param in model.parameters():
            param.requires_grad = False
        for name, param in model.named_parameters():
            if 'lora_' in name:
                param.requires_grad = True

        return lora_count

    # Demo
    print("\n--- Aplicando LoRA ---")

    model = SimpleModel(vocab_size=1000, d_model=256, n_layers=4, n_heads=4)
    total_before = sum(p.numel() for p in model.parameters())

    n_lora = apply_lora(model, rank=8, alpha=16,
                        target_modules=['q_proj', 'v_proj'])

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_after = sum(p.numel() for p in model.parameters())

    print(f"  LoRA layers added: {n_lora}")
    print(f"  Total params: {total_after:,}")
    print(f"  Trainable: {trainable:,}")
    print(f"  Frozen: {total_after - trainable:,}")
    print(f"  Trainable ratio: {trainable/total_after*100:.2f}%")

    # Entrenar con LoRA
    print("\n--- Fine-tuning con LoRA ---")
    torch.manual_seed(42)

    X = torch.randint(0, 1000, (500, 20))
    y = torch.randint(0, 1000, (500, 20))
    ds = TensorDataset(X, y)
    ldr = DataLoader(ds, batch_size=32, shuffle=True)

    # Solo optimizar params con requires_grad=True
    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=1e-3
    )

    for epoch in range(5):
        model.train()
        total_loss = 0
        for xb, yb in ldr:
            optimizer.zero_grad()
            logits = model(xb)
            loss = F.cross_entropy(logits.view(-1, 1000), yb.view(-1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        if epoch % 2 == 0:
            print(f"  Epoch {epoch+1}: loss={total_loss/len(ldr):.4f}")


# =====================================================================
#   PARTE 5: RANK Y ALPHA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: RANK Y ALPHA ===")
print("=" * 80)

"""
RANK (r):
  r=1: minimo. Muy pocas params. Puede ser insuficiente.
  r=4-8: standard. Funciona bien para la mayoria de tareas.
  r=16-64: mas expresivo. Para tareas complejas o datasets grandes.
  r=256: casi full fine-tuning. Probablemente innecesario.

ALPHA (α):
  Escala el update de LoRA: ΔW = (α/r) * B @ A
  α = r: scaling = 1. Default de HuggingFace PEFT.
  α = 2r: scaling = 2. Mas agresivo.

  Si α es fijo y cambias r, el scaling cambia.
  Solucion: fijar α y solo variar r.

REGLA: r=8, α=16 es un buen default.
"""

if HAS_TORCH:
    print("\n--- Efecto del rank ---")

    for rank in [1, 4, 8, 16, 64]:
        lora_params = 2 * rank * 256  # Per layer
        total_lora = lora_params * 8   # 4 layers × 2 targets
        scaling = 16.0 / rank
        print(f"  rank={rank:3d}: {total_lora:>8,} lora params, "
              f"scaling={scaling:.2f}")


# =====================================================================
#   PARTE 6: ADAPTERS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: ADAPTERS ===")
print("=" * 80)

"""
ADAPTERS (Houlsby et al., 2019):
  Modulos INSERTADOS entre las capas del transformer.

  x → down_proj (d → d_bottleneck) → ReLU
  → up_proj (d_bottleneck → d) → + x (residual) → output

  Similar a LoRA pero:
  - Se inserta como modulo separado (no modifica pesos existentes).
  - Tiene no-linearidad (LoRA es puramente lineal).
  - Tipicamente mas params que LoRA para misma calidad.
"""

if HAS_TORCH:
    class Adapter(nn.Module):
        """Adapter module (Houlsby style)."""
        def __init__(self, d_model, bottleneck=64):
            super().__init__()
            self.down = nn.Linear(d_model, bottleneck)
            self.up = nn.Linear(bottleneck, d_model)
            nn.init.zeros_(self.up.weight)
            nn.init.zeros_(self.up.bias)

        def forward(self, x):
            return x + self.up(F.relu(self.down(x)))

    adapter = Adapter(256, bottleneck=32)
    x = torch.randn(2, 10, 256)
    out = adapter(x)
    n = sum(p.numel() for p in adapter.parameters())
    print(f"\n  Adapter(256→32→256): {n:,} params")
    print(f"  Output == Input al inicio (init zeros)")


# =====================================================================
#   PARTE 7: PREFIX TUNING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: PREFIX TUNING ===")
print("=" * 80)

"""
PREFIX TUNING (Li & Liang, 2021):
  Prepend vectores APRENDIDOS como "prefix" a K y V.

  K = [K_prefix; K_real]
  V = [V_prefix; V_real]

  El modelo atiende al prefix como si fueran tokens reales.
  Pero el prefix es APRENDIDO, no derivado de tokens.

  → Extremadamente pocas params (~0.01%).
  → Funciona bien en modelos grandes.
"""

if HAS_TORCH:
    class PrefixTuning(nn.Module):
        """Prefix tuning simple."""

        def __init__(self, d_model, prefix_length=10, n_layers=4):
            super().__init__()
            self.prefix_length = prefix_length
            # Un prefix por capa (K y V)
            self.prefixes = nn.ParameterList([
                nn.Parameter(torch.randn(2, prefix_length, d_model) * 0.01)
                for _ in range(n_layers)
            ])

        def get_prefix(self, layer_idx, batch_size):
            """Devuelve (K_prefix, V_prefix) para un batch."""
            prefix = self.prefixes[layer_idx]
            k_prefix = prefix[0].unsqueeze(0).expand(batch_size, -1, -1)
            v_prefix = prefix[1].unsqueeze(0).expand(batch_size, -1, -1)
            return k_prefix, v_prefix

    pt = PrefixTuning(d_model=256, prefix_length=10, n_layers=4)
    total_prefix = sum(p.numel() for p in pt.parameters())
    print(f"\n  Prefix Tuning: {total_prefix:,} params")
    print(f"  = 4 layers × 2(K,V) × 10 prefix × 256 d_model")
    print(f"  → Mucho menos que LoRA, pero menos expresivo")


# =====================================================================
#   PARTE 8: COMPARATIVA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: COMPARATIVA PEFT ===")
print("=" * 80)

"""
  | Metodo         | % Params  | Expresividad | Memoria  | Velocidad |
  |---------------|-----------|-------------|----------|-----------|
  | Full FT        | 100%      | Maxima       | Maxima   | Lenta     |
  | LoRA           | 0.1-1%    | Alta         | Baja     | Rapida    |
  | QLoRA          | 0.1-1%    | Alta         | Minima   | Media     |
  | Adapters       | 1-5%      | Alta         | Media    | Media     |
  | Prefix Tuning  | 0.01%     | Media        | Baja     | Rapida    |
  | Prompt Tuning  | ~0%       | Baja         | Minima   | Rapida    |
"""

if HAS_TORCH:
    d = 256
    n_layers = 4

    methods = {
        'Full FT': sum(p.numel() for p in SimpleModel(1000, d, n_layers, 4).parameters()),
        'LoRA (r=8)': 2 * 8 * d * 2 * n_layers,
        'LoRA (r=64)': 2 * 64 * d * 2 * n_layers,
        'Adapter (b=32)': (d*32 + 32*d + 32 + d) * n_layers,
        'Prefix (l=10)': 2 * 10 * d * n_layers,
    }

    total = methods['Full FT']
    print(f"\n  Modelo base: {total:,} params (d={d}, {n_layers} layers)")
    print()
    for name, params in methods.items():
        pct = params / total * 100
        print(f"  {name:<18}: {params:>10,} params ({pct:>6.2f}%)")


# =====================================================================
#   PARTE 9: QLoRA — QUANTIZACION + LoRA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: QLoRA ===")
print("=" * 80)

"""
QLoRA (Dettmers et al., 2023):

IDEA: cargar el modelo base en 4-bit y aplicar LoRA en FP16.

COMPONENTES:
1. NF4 (Normal Float 4-bit): quantizacion optima para pesos
   distribuidos normalmente. Mejor que INT4.

2. Double quantization: quantizar las constantes de quantizacion.
   Ahorra ~0.5 bits por parametro.

3. Paged optimizers: usar CPU memory como backup de GPU.
   Permite batch sizes variables sin OOM.

RESULTADO:
  LLaMA 65B: necesita ~130GB en FP16.
  Con QLoRA: necesita ~33GB (4-bit) + ~1GB (LoRA).
  → Cabe en 1 GPU A100 de 40GB!

SIMULACION DE QUANTIZACION:
"""

if HAS_TORCH:
    def quantize_nf4_simulated(tensor):
        """Simula quantizacion NF4 (4-bit)."""
        # NF4 usa 16 niveles optimos para distribucion normal
        nf4_levels = torch.tensor([
            -1.0, -0.6962, -0.5251, -0.3949, -0.2844, -0.1848,
            -0.0911, 0.0, 0.0796, 0.1609, 0.2461, 0.3379,
            0.4407, 0.5626, 0.7230, 1.0
        ])

        # Normalizar tensor
        absmax = tensor.abs().max()
        normalized = tensor / (absmax + 1e-10)

        # Quantizar: encontrar nivel mas cercano
        distances = (normalized.unsqueeze(-1) - nf4_levels).abs()
        indices = distances.argmin(dim=-1)
        quantized = nf4_levels[indices]

        # Dequantizar
        return quantized * absmax, indices

    # Demo quantizacion
    print("\n--- Simulacion NF4 ---")
    original_weights = torch.randn(256, 256)
    quantized, indices = quantize_nf4_simulated(original_weights)

    error = (original_weights - quantized).abs()
    print(f"  Original dtype: float32 ({original_weights.numel() * 4 / 1024:.0f} KB)")
    print(f"  Quantized: 4-bit ({original_weights.numel() * 0.5 / 1024:.0f} KB)")
    print(f"  Compression: {4 / 0.5:.0f}x")
    print(f"  Mean abs error: {error.mean():.6f}")
    print(f"  Max abs error: {error.max():.6f}")
    print(f"  → Muy poca perdida para 8x compresion!")

    # Memoria con QLoRA
    print("\n--- Memoria QLoRA ---")
    for name, n_params in models.items():
        fp16 = n_params * 2 / 1e9
        fp4 = n_params * 0.5 / 1e9
        lora_overhead = n_params * 0.01 * 2 / 1e9  # 1% params en FP16
        total_qlora = fp4 + lora_overhead
        print(f"  {name:<15}: FP16={fp16:.1f}GB, "
              f"QLoRA={total_qlora:.1f}GB ({fp16/total_qlora:.1f}x ahorro)")


# =====================================================================
#   PARTE 10: MERGE Y MULTI-TASK LoRA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: MERGE Y MULTI-TASK ===")
print("=" * 80)

"""
MERGE: fusionar LoRA en los pesos base para inference.
  W_merged = W_base + (α/r) * B @ A
  → Sin overhead en inference (mismo modelo, pesos diferentes).

MULTI-TASK LoRA: un adapter por tarea.
  Base model (compartido) + LoRA_chat + LoRA_code + LoRA_medical
  → Cambiar tarea = cargar adapter diferente (~10-50MB).
  → No necesitas N copias del modelo base!

LoRA STACKING: combinar multiples adapters.
  W = W_base + ΔW_chat + 0.5 * ΔW_code
  → Mezclar capacidades de diferentes fine-tunes.
"""

if HAS_TORCH:
    print("\n--- LoRA Merge demo ---")

    # Crear modelo con LoRA
    base = nn.Linear(128, 128)
    lora_layer = LoRALinear(base, rank=4, alpha=8)

    # Entrenar LoRA (simular)
    with torch.no_grad():
        lora_layer.lora_A.normal_(0, 0.1)
        lora_layer.lora_B.normal_(0, 0.1)

    # Verificar equivalencia pre/post merge
    x_test = torch.randn(1, 128)
    with torch.no_grad():
        out_before = lora_layer(x_test)

    # Merge
    lora_layer.merge()

    with torch.no_grad():
        out_after = base(x_test)  # Ahora base tiene los pesos merged

    diff = (out_before - out_after).abs().max().item()
    print(f"  Pre-merge output[0,:3]:  {out_before[0,:3].tolist()}")
    print(f"  Post-merge output[0,:3]: {out_after[0,:3].tolist()}")
    print(f"  Max difference: {diff:.8f}")
    print(f"  → Merge es exacto (diferencia = precision numerica)")

    # Multi-task
    print("\n--- Multi-task LoRA ---")
    tasks = {
        'chat': {'rank': 8, 'size_mb': 8 * 256 * 2 * 4 * 2 / 1e6},
        'code': {'rank': 16, 'size_mb': 16 * 256 * 2 * 4 * 2 / 1e6},
        'medical': {'rank': 8, 'size_mb': 8 * 256 * 2 * 4 * 2 / 1e6},
    }

    print(f"  Base model: {total:,} params")
    for task, info in tasks.items():
        print(f"  LoRA_{task}: rank={info['rank']}, "
              f"size={info['size_mb']:.2f} MB")
    print(f"  → Cambiar tarea = cargar adapter diferente!")


# =====================================================================
#   PARTE 11: LoRA DROPOUT Y REGULARIZACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: LoRA DROPOUT ===")
print("=" * 80)

"""
LoRA DROPOUT: aplicar dropout al output de LoRA.
  lora_out = dropout((x @ A^T) @ B^T) * scaling
  → Regulariza el adapter, evita overfitting.
  → Tipicamente dropout=0.05-0.1.

WEIGHT DECAY en LoRA:
  Aplicar weight decay solo a LoRA params, no al modelo base.
  Los pesos base estan frozen, no tiene sentido regularizarlos.

LEARNING RATE:
  LoRA tipicamente necesita lr MAS ALTO que full fine-tuning.
  Full FT: lr=1e-5 a 5e-5
  LoRA: lr=1e-4 a 3e-4 (10x mas alto!)
  → Porque hay menos params, necesita updates mas grandes.
"""

if HAS_TORCH:
    class LoRALinearWithDropout(nn.Module):
        """LoRA con dropout para regularizacion."""

        def __init__(self, original, rank=8, alpha=16, dropout=0.1):
            super().__init__()
            self.original = original
            self.scaling = alpha / rank

            original.weight.requires_grad = False
            if original.bias is not None:
                original.bias.requires_grad = False

            self.lora_A = nn.Parameter(
                torch.randn(rank, original.in_features) * 0.01
            )
            self.lora_B = nn.Parameter(
                torch.zeros(original.out_features, rank)
            )
            self.lora_dropout = nn.Dropout(dropout)

        def forward(self, x):
            base_out = self.original(x)
            lora_out = self.lora_dropout(
                (x @ self.lora_A.T) @ self.lora_B.T
            ) * self.scaling
            return base_out + lora_out

    # Demo
    print("\n--- LoRA con dropout ---")
    base_drop = nn.Linear(128, 128)
    lora_drop = LoRALinearWithDropout(base_drop, rank=8, dropout=0.1)

    lora_drop.train()
    x = torch.randn(2, 10, 128)
    out1 = lora_drop(x)
    out2 = lora_drop(x)
    diff = (out1 - out2).abs().mean().item()
    print(f"  Train mode: outputs differ by {diff:.6f} (dropout active)")

    lora_drop.eval()
    out3 = lora_drop(x)
    out4 = lora_drop(x)
    diff_eval = (out3 - out4).abs().mean().item()
    print(f"  Eval mode: outputs differ by {diff_eval:.6f} (deterministic)")


# =====================================================================
#   PARTE 12: BEST PRACTICES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: BEST PRACTICES ===")
print("=" * 80)

print("""
  CHECKLIST PARA FINE-TUNING CON LoRA:

  PREPARACION:
  [ ] Elegir modelo base (LLaMA, Mistral, Gemma...).
  [ ] Preparar dataset en formato instruccion/respuesta.
  [ ] Decidir target modules (Q,V minimo; all para maximo).

  HIPERPARAMETROS:
  [ ] rank: 8 (default), 16-64 si dataset grande.
  [ ] alpha: 2 * rank (o igual a rank).
  [ ] lr: 1e-4 a 3e-4 (10x mas que full FT).
  [ ] batch_size: 4-16 (con gradient accumulation).
  [ ] epochs: 1-3 (LLMs overfittean rapido).
  [ ] warmup: 3-10% de los steps totales.

  ENTRENAMIENTO:
  [ ] Gradient clipping = 1.0.
  [ ] Cosine LR schedule con warmup.
  [ ] Evaluar en val set cada N steps.
  [ ] Early stopping por val_loss.

  POST-ENTRENAMIENTO:
  [ ] Merge LoRA para deployment.
  [ ] Evaluar en benchmarks (MMLU, HumanEval...).
  [ ] Comparar con base model sin fine-tune.

  ERRORES COMUNES:
  ✗ lr muy bajo → no aprende.
  ✗ Muchos epochs → overfitting.
  ✗ rank muy alto → desperdicio de memoria.
  ✗ No congelar base → full FT accidental.
  ✗ Dataset mal formateado → aprende basura.
""")


# =====================================================================
#   PARTE 9: SELECCION DE HIPERPARAMETROS LoRA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: GUIA DE HIPERPARAMETROS ===")
print("=" * 80)

"""
COMO ELEGIR HIPERPARAMETROS DE LoRA:

┌──────────────┬─────────────────────────────────────────────┐
│ Parametro    │ Guia                                        │
├──────────────┼─────────────────────────────────────────────┤
│ rank (r)     │ 8: general, 16-32: tareas complejas,        │
│              │ 4: memoria limitada, 64: near full-FT       │
├──────────────┼─────────────────────────────────────────────┤
│ alpha (α)    │ Regla: α = 2*r (ej: r=8, α=16)             │
│              │ scaling = α/r. Mayor α → mas influencia.    │
├──────────────┼─────────────────────────────────────────────┤
│ target       │ Minimo: q_proj, v_proj                      │
│ modules      │ Recomendado: q,k,v,o_proj                   │
│              │ Maximo: + gate,up,down_proj (FFN)            │
├──────────────┼─────────────────────────────────────────────┤
│ lr           │ 1e-4 a 5e-4 para LoRA                       │
│              │ 2e-4 default (Unsloth/TRL)                   │
├──────────────┼─────────────────────────────────────────────┤
│ dropout      │ 0.0-0.1 para LoRA dropout                   │
│              │ 0.05 es bueno default                        │
├──────────────┼─────────────────────────────────────────────┤
│ epochs       │ 1-3 para datasets grandes (>10K)            │
│              │ 3-5 para datasets pequeños (<1K)             │
├──────────────┼─────────────────────────────────────────────┤
│ batch_size   │ Tan grande como quepa en memoria.            │
│              │ Usar gradient accumulation si es necesario.  │
└──────────────┴─────────────────────────────────────────────┘
"""

# ─── Simulacion de impacto de rank ───
print("\n--- Impacto del rank en parametros ---")

d_model = 4096  # Dimension de Llama-7B

for r in [4, 8, 16, 32, 64, 128]:
    params_lora = 2 * d_model * r  # A + B para una capa
    # 4 proyecciones de atencion (q, k, v, o) * 32 capas
    total_params = params_lora * 4 * 32
    total_base = d_model * d_model * 4 * 32  # params originales
    pct = total_params / total_base * 100
    
    print(f"  r={r:>3}: {total_params:>10,} LoRA params "
          f"({pct:.2f}% del base) "
          f"| ~{total_params * 2 / 1e6:.0f}MB FP16")


# =====================================================================
#   PARTE 10: MULTI-ADAPTER MANAGEMENT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: MULTI-ADAPTER ===")
print("=" * 80)

"""
MULTI-ADAPTER: Tener MULTIPLES LoRA adapters para diferentes tareas
cargados simultaneamente.

CASOS DE USO:
  - Modelo base + LoRA español + LoRA codigo + LoRA medico
  - Cambiar entre adapters segun el tipo de request
  - Servir multiples "modelos" con una sola copia base en GPU

VENTAJA: solo almacenas la base una vez en VRAM.
"""

class MultiAdapterManager:
    """
    Gestor de multiples LoRA adapters sobre un modelo base compartido.
    
    En produccion, esto es lo que hace HuggingFace PEFT internamente.
    """
    
    def __init__(self, base_dim: int):
        self.base_dim = base_dim
        self.adapters = {}
        self.active_adapter = None
    
    def add_adapter(self, name: str, rank: int, alpha: float = None):
        """Registrar un nuevo adapter."""
        if alpha is None:
            alpha = rank * 2
        
        # Simular matrices A y B
        A = np.random.randn(rank, self.base_dim) * 0.01
        B = np.zeros((self.base_dim, rank))
        
        self.adapters[name] = {
            "A": A, "B": B,
            "rank": rank, "alpha": alpha,
            "scaling": alpha / rank,
        }
        print(f"  Adapter '{name}' añadido (r={rank}, α={alpha})")
    
    def set_active(self, name: str):
        """Activar un adapter."""
        if name not in self.adapters:
            raise ValueError(f"Adapter '{name}' no encontrado")
        self.active_adapter = name
        print(f"  Adapter activo: '{name}'")
    
    def get_delta_w(self, name: str = None):
        """Obtener ΔW del adapter activo o especificado."""
        name = name or self.active_adapter
        if name is None:
            return np.zeros((self.base_dim, self.base_dim))
        
        adapter = self.adapters[name]
        delta_w = adapter["B"] @ adapter["A"] * adapter["scaling"]
        return delta_w
    
    def list_adapters(self):
        """Listar todos los adapters."""
        for name, adapter in self.adapters.items():
            active = " (ACTIVE)" if name == self.active_adapter else ""
            size_mb = (adapter["A"].nbytes + adapter["B"].nbytes) / 1e6
            print(f"  {name}: r={adapter['rank']}, "
                  f"α={adapter['alpha']}, "
                  f"size={size_mb:.2f}MB{active}")

# Demostrar multi-adapter
print("\n--- Demo Multi-Adapter ---")
manager = MultiAdapterManager(base_dim=512)
manager.add_adapter("spanish", rank=8)
manager.add_adapter("code", rank=16)
manager.add_adapter("medical", rank=32)

print("\nAdapters disponibles:")
manager.list_adapters()

manager.set_active("code")
delta = manager.get_delta_w()
print(f"\nΔW shape: {delta.shape}, norm: {np.linalg.norm(delta):.6f}")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: PEFT Y LoRA ===")
print("=" * 80)

print("""
  PEFT = fine-tuning eficiente cambiando POCOS parametros.

  LoRA (standard):
  - ΔW = B @ A (bajo rango r << d)
  - r=8, α=16 default
  - Aplicar a Q, V (minimo) o Q,K,V,O,FFN (maximo)
  - 0.1-1% params trainables
  - Merge para inference (sin overhead)

  QLoRA:
  - Modelo base en 4-bit (NF4)
  - LoRA adapters en FP16/BF16
  - Fine-tune 70B en 1 GPU de 48GB!

  HIPERPARAMETROS:
  - rank: 8 (general), 16-32 (complejo), 4 (limitado)
  - alpha: 2 * rank
  - lr: 2e-4
  - epochs: 1-3

  MULTI-ADAPTER:
  - Multiples LoRA sobre una base compartida.
  - Cambiar adapter segun el tipo de request.
  - Eficiente en memoria: solo la base en VRAM.

  RECETA:
  1. Cargar modelo pre-entrenado.
  2. Congelar todos los pesos.
  3. Añadir LoRA a las proyecciones de atencion.
  4. Entrenar solo LoRA params con AdamW.
  5. Merge LoRA para deployment.

  HERRAMIENTAS:
  - HuggingFace PEFT: libreria standard.
  - bitsandbytes: quantizacion para QLoRA.
  - Unsloth: 2x mas rapido que PEFT.
""")

print("=" * 80)
print("=== FIN MODULO 20, ARCHIVO 02 ===")
print("=" * 80)


