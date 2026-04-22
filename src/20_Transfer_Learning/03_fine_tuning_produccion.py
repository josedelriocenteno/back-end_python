# ===========================================================================
# 03_fine_tuning_produccion.py
# ===========================================================================
# MODULO 20: TRANSFER LEARNING Y FINE-TUNING
# ARCHIVO 03: Fine-Tuning para Produccion
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Pipeline completo de fine-tuning: preparacion de datos,
# entrenamiento con LoRA, evaluacion, deployment, y monitoreo.
# Cubre SFT, RLHF/DPO, quantizacion, y serving.
#
# CONTENIDO:
#   1. Pipeline de fine-tuning end-to-end.
#   2. Preparacion de datos: formatos de instruccion.
#   3. Supervised Fine-Tuning (SFT).
#   4. DPO: Direct Preference Optimization.
#   5. Quantizacion para deployment (GPTQ, AWQ, GGUF).
#   6. Model merging: combinar modelos.
#   7. Evaluacion de LLMs.
#   8. Serving: vLLM, TGI, Ollama.
#   9. MLOps para LLMs.
#   10. Costos y optimizacion.
#
# NIVEL: LLM ENGINEER / MLOPS SENIOR.
# ===========================================================================

import numpy as np
import math
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset, Dataset
    HAS_TORCH = True
    print(f"  PyTorch: {torch.__version__}")
except ImportError:
    HAS_TORCH = False
    print("  PyTorch not available.")


# =====================================================================
#   PARTE 1: PIPELINE DE FINE-TUNING
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: PIPELINE END-TO-END ===")
print("=" * 80)

"""
PIPELINE COMPLETO DE FINE-TUNING:

  1. DATOS:
     Recopilar → Limpiar → Formatear → Split

  2. MODELO BASE:
     Seleccionar → Cargar (quantizado) → Aplicar LoRA

  3. ENTRENAMIENTO:
     SFT (Supervised Fine-Tuning) → opcional DPO/RLHF

  4. EVALUACION:
     Benchmarks → Human eval → A/B testing

  5. DEPLOYMENT:
     Merge LoRA → Quantizar → Servir (vLLM/TGI)

  6. MONITOREO:
     Latencia → Calidad → Costos → Drift
"""

print("""
  FLUJO:

  Datos (JSONL) → Tokenizar → SFT con LoRA
       ↓
  Modelo fine-tuned → Merge → GGUF/GPTQ
       ↓
  vLLM / Ollama → API → Usuarios
       ↓
  Monitoring → ¿Degradacion? → Re-train
""")


# =====================================================================
#   PARTE 2: PREPARACION DE DATOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: PREPARACION DE DATOS ===")
print("=" * 80)

"""
FORMATOS DE DATOS PARA FINE-TUNING:

1. INSTRUCTION FORMAT (Alpaca style):
   {"instruction": "Traduce al ingles",
    "input": "Hola mundo",
    "output": "Hello world"}

2. CHAT FORMAT (ChatML/Llama):
   {"messages": [
     {"role": "system", "content": "Eres un asistente."},
     {"role": "user", "content": "Hola"},
     {"role": "assistant", "content": "Hola! Como puedo ayudarte?"}
   ]}

3. COMPLETION FORMAT:
   {"text": "### Pregunta: ...\n### Respuesta: ..."}

REGLAS DE CALIDAD:
  - Minimo 1K-10K ejemplos para SFT.
  - Diversidad > cantidad.
  - Calidad > cantidad (100 buenos > 10K malos).
  - Formato CONSISTENTE.
"""

# Simular dataset de instrucciones
print("\n--- Dataset de instrucciones ---")


class InstructionDataset(Dataset):
    """Dataset para Supervised Fine-Tuning."""

    def __init__(self, instructions, max_len=64, vocab_size=1000):
        self.instructions = instructions
        self.max_len = max_len
        self.vocab_size = vocab_size

    def __len__(self):
        return len(self.instructions)

    def __getitem__(self, idx):
        item = self.instructions[idx]
        # Simular tokenizacion: hash de strings a IDs
        tokens = []
        full_text = f"### Instruction: {item['instruction']}\n"
        if item.get('input'):
            full_text += f"### Input: {item['input']}\n"
        full_text += f"### Response: {item['output']}"

        for char in full_text:
            tokens.append(ord(char) % self.vocab_size)

        # Pad/truncate
        if len(tokens) > self.max_len:
            tokens = tokens[:self.max_len]
        else:
            tokens = tokens + [0] * (self.max_len - len(tokens))

        tokens = torch.tensor(tokens, dtype=torch.long)
        # Labels: shift right (next token prediction)
        input_ids = tokens[:-1]
        labels = tokens[1:]
        return input_ids, labels


# Crear dataset sintetico
instructions = [
    {"instruction": "Suma dos numeros", "input": "3 + 5", "output": "8"},
    {"instruction": "Traduce al ingles", "input": "Hola", "output": "Hello"},
    {"instruction": "Capitaliza", "input": "hello world", "output": "Hello World"},
    {"instruction": "Invierte", "input": "abc", "output": "cba"},
    {"instruction": "Cuenta letras", "input": "python", "output": "6"},
] * 200  # 1000 ejemplos

dataset = InstructionDataset(instructions)
print(f"  Dataset: {len(dataset)} ejemplos")
print(f"  Sample input shape: {dataset[0][0].shape}")
print(f"  Sample label shape: {dataset[0][1].shape}")


# =====================================================================
#   PARTE 3: SUPERVISED FINE-TUNING (SFT)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: SFT — SUPERVISED FINE-TUNING ===")
print("=" * 80)

"""
SFT: entrenar el modelo para seguir instrucciones.

  Input:  "### Instruction: Traduce\n### Input: Hola\n### Response:"
  Output: "Hello"

El modelo aprende a:
  1. Entender la instruccion.
  2. Procesar el input.
  3. Generar la respuesta correcta.

LOSS: solo sobre los tokens de RESPUESTA (no instruccion).
  → Masked loss: ignorar tokens de prompt.
"""

if HAS_TORCH:
    class MiniLM(nn.Module):
        """Language Model minimo para demo de SFT."""

        def __init__(self, vocab_size, d_model=128, n_layers=3, n_heads=4):
            super().__init__()
            self.emb = nn.Embedding(vocab_size, d_model)
            self.pos = nn.Embedding(256, d_model)
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=d_model, nhead=n_heads, dim_feedforward=4*d_model,
                dropout=0.1, batch_first=True, norm_first=True,
            )
            self.transformer = nn.TransformerEncoder(encoder_layer, n_layers)
            self.head = nn.Linear(d_model, vocab_size)
            self.d_model = d_model

        def forward(self, x):
            B, T = x.shape
            positions = torch.arange(T, device=x.device)
            x = self.emb(x) + self.pos(positions)

            # Causal mask
            mask = nn.Transformer.generate_square_subsequent_mask(T, device=x.device)
            x = self.transformer(x, mask=mask, is_causal=True)
            return self.head(x)

    # SFT Training
    print("\n--- SFT Training ---")

    vocab_size = 1000
    model_sft = MiniLM(vocab_size, d_model=128, n_layers=3)
    n_params = sum(p.numel() for p in model_sft.parameters())
    print(f"  Model: {n_params:,} params")

    train_ldr = DataLoader(dataset, batch_size=32, shuffle=True)
    optimizer = torch.optim.AdamW(model_sft.parameters(), lr=3e-4,
                                   weight_decay=0.01)

    # LR schedule con warmup
    total_steps = len(train_ldr) * 5  # 5 epochs
    warmup_steps = int(0.1 * total_steps)

    def get_lr(step):
        if step < warmup_steps:
            return step / warmup_steps
        progress = (step - warmup_steps) / (total_steps - warmup_steps)
        return 0.5 * (1 + math.cos(math.pi * progress))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, get_lr)

    for epoch in range(5):
        model_sft.train()
        total_loss = 0
        for step, (xb, yb) in enumerate(train_ldr):
            optimizer.zero_grad()
            logits = model_sft(xb)
            loss = F.cross_entropy(logits.view(-1, vocab_size), yb.view(-1),
                                    ignore_index=0)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model_sft.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_ldr)
        lr = optimizer.param_groups[0]['lr'] * get_lr(epoch * len(train_ldr))
        print(f"  Epoch {epoch+1}: loss={avg_loss:.4f}")


# =====================================================================
#   PARTE 4: DPO — DIRECT PREFERENCE OPTIMIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: DPO ===")
print("=" * 80)

"""
DESPUES DE SFT: alinear el modelo con preferencias humanas.

RLHF (clasico, ChatGPT):
  1. Entrenar reward model con preferencias humanas.
  2. Optimizar LLM con PPO para maximizar reward.
  → Complejo, inestable, caro.

DPO (Rafailov et al., 2023):
  SIMPLIFICA RLHF eliminando el reward model.
  Directamente optimiza: "prefiere respuesta A sobre B".

  Loss_DPO = -log σ(β * (log π(y_w|x)/π_ref(y_w|x)
                       - log π(y_l|x)/π_ref(y_l|x)))

  y_w: respuesta preferida (winner).
  y_l: respuesta no preferida (loser).
  π_ref: modelo de referencia (pre-DPO).
  β: temperatura (tipicamente 0.1-0.5).

DATOS PARA DPO:
  {"prompt": "Explica X",
   "chosen": "Respuesta buena detallada...",
   "rejected": "Respuesta mala vaga..."}
"""

if HAS_TORCH:
    def dpo_loss(policy_chosen_logps, policy_rejected_logps,
                 ref_chosen_logps, ref_rejected_logps, beta=0.1):
        """Calcula DPO loss."""
        chosen_rewards = beta * (policy_chosen_logps - ref_chosen_logps)
        rejected_rewards = beta * (policy_rejected_logps - ref_rejected_logps)

        loss = -F.logsigmoid(chosen_rewards - rejected_rewards).mean()

        # Metricas
        reward_margin = (chosen_rewards - rejected_rewards).mean().item()
        accuracy = (chosen_rewards > rejected_rewards).float().mean().item()

        return loss, {'reward_margin': reward_margin, 'accuracy': accuracy}

    # Demo
    print("\n--- DPO Loss ---")
    batch = 16
    policy_chosen = torch.randn(batch) * 0.5  # Log probs chosen
    policy_rejected = torch.randn(batch) * 0.5 - 0.3  # Lower
    ref_chosen = torch.randn(batch) * 0.5
    ref_rejected = torch.randn(batch) * 0.5

    loss, metrics = dpo_loss(policy_chosen, policy_rejected,
                              ref_chosen, ref_rejected, beta=0.1)

    print(f"  DPO loss: {loss.item():.4f}")
    print(f"  Reward margin: {metrics['reward_margin']:.4f}")
    print(f"  Accuracy: {metrics['accuracy']:.2%}")
    print(f"  → El modelo aprende a preferir 'chosen' sobre 'rejected'")


# =====================================================================
#   PARTE 5: QUANTIZACION PARA DEPLOYMENT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: QUANTIZACION ===")
print("=" * 80)

"""
QUANTIZACION POST-TRAINING: reducir precision para inference.

FORMATOS:
1. GPTQ (GPU): quantiza a 4-bit con calibracion.
   → Rapido en GPU. Usado con vLLM/TGI.

2. AWQ (GPU): quantiza preservando canales "importantes".
   → Mejor calidad que GPTQ. Mas lento de crear.

3. GGUF (CPU/GPU): formato de llama.cpp.
   → Corre en CPU! Usado con Ollama.
   → Variantes: Q4_K_M (recomendado), Q5_K_M, Q8_0.

REGLA DE CALIDAD:
  FP16 (baseline) > Q8 (casi igual) > Q5 (bueno) > Q4 (aceptable) > Q3 (limite)
"""

if HAS_TORCH:
    # Simular quantizacion y medir degradacion
    print("\n--- Efecto de quantizacion ---")

    def simulate_quantization(tensor, bits):
        """Simula quantizacion uniforme."""
        qmin = -(2 ** (bits - 1))
        qmax = 2 ** (bits - 1) - 1
        scale = tensor.abs().max() / qmax
        quantized = torch.clamp(torch.round(tensor / scale), qmin, qmax)
        return quantized * scale

    weights = torch.randn(512, 512)

    for bits in [16, 8, 5, 4, 3, 2]:
        if bits == 16:
            quant = weights.half().float()
        else:
            quant = simulate_quantization(weights, bits)

        error = (weights - quant).abs().mean().item()
        relative = error / weights.abs().mean().item() * 100
        size_mb = weights.numel() * bits / 8 / 1024 / 1024

        print(f"  {bits:2d}-bit: error={error:.6f} "
              f"({relative:.2f}%), size={size_mb:.2f} MB")

    print(f"\n  → Q4 tiene <5% error relativo: excelente trade-off")


# =====================================================================
#   PARTE 6: MODEL MERGING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: MODEL MERGING ===")
print("=" * 80)

"""
MODEL MERGING: combinar multiples modelos sin re-entrenar.

METODOS:
1. Linear merge: W = α*W_A + (1-α)*W_B
   Simple. Funciona si los modelos son similares.

2. SLERP: interpolacion esferica.
   Mejor que linear para modelos en espacios curvos.

3. TIES: elimina params redundantes antes de merge.
   Mejor calidad. Usado en mergekit.

4. DARE: dropout aleatorio antes de merge.
   Sorprendentemente efectivo.

CASO DE USO:
  Modelo_chat (bueno conversando) + Modelo_code (bueno en codigo)
  → Merge → Modelo que conviersa Y codifica.
"""

if HAS_TORCH:
    print("\n--- Linear Merge ---")

    model_a = torch.randn(256, 256)
    model_b = torch.randn(256, 256)

    for alpha in [0.0, 0.3, 0.5, 0.7, 1.0]:
        merged = alpha * model_a + (1 - alpha) * model_b
        dist_a = (merged - model_a).norm().item()
        dist_b = (merged - model_b).norm().item()
        print(f"  α={alpha:.1f}: dist_A={dist_a:.1f}, dist_B={dist_b:.1f}")

    # SLERP
    print("\n--- SLERP Merge ---")

    def slerp(t, v0, v1, eps=1e-8):
        """Spherical Linear Interpolation."""
        v0_flat = v0.flatten().float()
        v1_flat = v1.flatten().float()

        v0_norm = v0_flat / (v0_flat.norm() + eps)
        v1_norm = v1_flat / (v1_flat.norm() + eps)

        omega = torch.acos(torch.clamp(
            torch.dot(v0_norm, v1_norm), -1.0, 1.0
        ))

        if omega.abs() < eps:
            return (1 - t) * v0 + t * v1

        sin_omega = torch.sin(omega)
        result_flat = (torch.sin((1-t)*omega)/sin_omega * v0_flat +
                       torch.sin(t*omega)/sin_omega * v1_flat)
        return result_flat.view(v0.shape)

    slerp_merged = slerp(0.5, model_a, model_b)
    print(f"  SLERP(0.5) norm: {slerp_merged.norm():.1f}")
    print(f"  Linear(0.5) norm: {((model_a + model_b)/2).norm():.1f}")
    print(f"  → SLERP preserva la norma mejor")


# =====================================================================
#   PARTE 7: EVALUACION DE LLMs
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: EVALUACION ===")
print("=" * 80)

"""
BENCHMARKS STANDARD:

1. MMLU: conocimiento general (57 materias).
2. HumanEval: generacion de codigo.
3. GSM8K: razonamiento matematico.
4. TruthfulQA: veracidad.
5. HellaSwag: sentido comun.
6. MT-Bench: calidad de conversacion (scored by GPT-4).
7. AlpacaEval: preferencia humana simulada.

METRICAS:
  - Perplexity: calidad del language model.
  - BLEU/ROUGE: para traduccion/summarizacion.
  - Pass@k: para codigo (k intentos, al menos 1 correcto).
  - Win rate: preferencia A vs B.

EVALUACION PRACTICA:
  1. Benchmarks automaticos (rapido, reproducible).
  2. Human evaluation (caro, subjetivo, gold standard).
  3. LLM-as-judge (GPT-4 evalua, buen proxy).
  4. A/B testing en produccion (definitivo).
"""

if HAS_TORCH:
    # Simular evaluacion
    print("\n--- Evaluacion automatica ---")

    model_sft.eval()
    test_ds = InstructionDataset(instructions[:100])
    test_ldr = DataLoader(test_ds, batch_size=100)

    with torch.no_grad():
        for xb, yb in test_ldr:
            logits = model_sft(xb)
            loss = F.cross_entropy(logits.view(-1, vocab_size), yb.view(-1),
                                    ignore_index=0)
            preds = logits.argmax(-1)
            mask = yb != 0
            accuracy = ((preds == yb) & mask).float().sum() / mask.sum()

            ppl = math.exp(loss.item())
            print(f"  Perplexity: {ppl:.2f}")
            print(f"  Token accuracy: {accuracy:.4f}")
            break


# =====================================================================
#   PARTE 8: SERVING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: SERVING ===")
print("=" * 80)

"""
OPCIONES DE SERVING:

1. vLLM (GPU):
   - PagedAttention: gestiona KV-cache eficientemente.
   - Continuous batching: procesa multiples requests.
   - Throughput: 10-30x mas que naive inference.
   pip install vllm
   python -m vllm.entrypoints.openai.api_server --model meta-llama/...

2. TGI - Text Generation Inference (GPU):
   - De HuggingFace. Docker-based.
   - Tensor parallelism para multi-GPU.
   docker run ghcr.io/huggingface/text-generation-inference --model-id ...

3. Ollama (CPU/GPU):
   - Para uso local. Formato GGUF.
   - Facil: ollama run llama3
   - API compatible con OpenAI.

4. llama.cpp (CPU):
   - Inference en CPU puro. C++.
   - Quantizacion GGUF nativa.

METRICAS DE SERVING:
  - TTFT: Time To First Token (latencia percibida).
  - TPS: Tokens Per Second (throughput).
  - Concurrent users: cuantos a la vez.
"""

print("""
  EJEMPLO vLLM:

  from vllm import LLM, SamplingParams

  llm = LLM(model="meta-llama/Llama-3-8B-Instruct",
            quantization="awq",
            max_model_len=4096)

  params = SamplingParams(temperature=0.7, top_p=0.9,
                          max_tokens=256)

  outputs = llm.generate(["Explain quantum computing"], params)
""")


# =====================================================================
#   PARTE 9: COSTOS Y OPTIMIZACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: COSTOS ===")
print("=" * 80)

"""
COSTOS DE FINE-TUNING (2024-2025):

GPU CLOUD (por hora):
  A100 40GB: ~$1.50/hr
  A100 80GB: ~$2.50/hr
  H100 80GB: ~$4.00/hr
  RTX 4090 (consumer): ~$0.50/hr

FINE-TUNING TIPICO (LLaMA 7B, QLoRA):
  GPU: A100 40GB x 1
  Tiempo: 2-8 horas
  Costo: $3-20

FINE-TUNING FULL (LLaMA 70B):
  GPU: A100 80GB x 8
  Tiempo: 24-72 horas
  Costo: $500-2000

OPTIMIZACIONES:
  1. QLoRA: reduce GPU de 80GB a 24GB.
  2. Gradient checkpointing: reduce memoria 2-3x.
  3. Flash Attention: 2x mas rapido.
  4. Gradient accumulation: simula batch sizes grandes.
  5. Mixed precision (BF16): 2x mas rapido que FP32.
"""

if HAS_TORCH:
    print("\n--- Estimacion de costos ---")

    configs = [
        ("7B QLoRA (1 A100)", 1, 2.50, 4),
        ("7B Full FT (4 A100)", 4, 2.50, 12),
        ("13B QLoRA (1 A100)", 1, 2.50, 8),
        ("70B QLoRA (1 A100-80)", 1, 2.50, 24),
        ("70B Full FT (8 H100)", 8, 4.00, 48),
    ]

    print(f"  {'Config':<25} {'GPUs':>4} {'Hours':>6} {'Cost':>8}")
    print(f"  {'-'*25} {'-'*4} {'-'*6} {'-'*8}")
    for name, gpus, rate, hours in configs:
        cost = gpus * rate * hours
        print(f"  {name:<25} {gpus:>4} {hours:>6} ${cost:>7.0f}")


# =====================================================================
#   PARTE 10: EVALUACION DE LLMs — METRICAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: EVALUACION DE LLMs ===")
print("=" * 80)

"""
METRICAS PARA EVALUAR LLMs FINE-TUNED:

METRICAS AUTOMATICAS:
  1. Perplexity: mide que tan "sorprendido" esta el modelo.
     - Menor = mejor.
     - PPL = exp(avg_loss).
     - Un modelo perfecto tiene PPL = 1.

  2. BLEU: compara n-gramas entre generacion y referencia.
     - Usado en traduccion.
     - 0-100 (100 = identico).

  3. ROUGE: overlap de n-gramas orientado a recall.
     - ROUGE-1: unigramas.
     - ROUGE-2: bigramas.
     - ROUGE-L: subsecuencia comun mas larga.
     - Usado en resumen.

  4. Exact Match (EM): ¿la respuesta es exactamente correcta?
     - Usado en QA.

  5. F1 Token: overlap de tokens entre prediccion y referencia.

METRICAS HUMANAS (MAS IMPORTANTES):
  1. Helpfulness: ¿la respuesta es util?
  2. Harmlessness: ¿la respuesta es segura?
  3. Honesty: ¿la respuesta es verdadera?
  4. Formatting: ¿el formato es correcto?

LLM-AS-JUDGE:
  - Usar un LLM fuerte (GPT-4, Claude) para evaluar outputs.
  - Mas rapido que evaluacion humana.
  - Correlaciona ~80-90% con juicio humano.
"""


# ─── Implementacion de metricas basicas ───

def calcular_bleu_simple(referencia, candidato, max_n=4):
    """
    BLEU score simplificado (sin brevity penalty).
    
    BLEU = prod(precision_n)^(1/max_n)
    
    Donde precision_n = n-gramas_comunes / n-gramas_totales_candidato
    
    Ejemplo:
      ref  = "el gato esta en la casa"
      cand = "el gato esta en la casa"
      → BLEU = 1.0 (identico)
    """
    ref_tokens = referencia.lower().split()
    cand_tokens = candidato.lower().split()
    
    if len(cand_tokens) == 0:
        return 0.0
    
    precisions = []
    for n in range(1, max_n + 1):
        ref_ngrams = {}
        for i in range(len(ref_tokens) - n + 1):
            ng = tuple(ref_tokens[i:i+n])
            ref_ngrams[ng] = ref_ngrams.get(ng, 0) + 1
        
        cand_ngrams = {}
        for i in range(len(cand_tokens) - n + 1):
            ng = tuple(cand_tokens[i:i+n])
            cand_ngrams[ng] = cand_ngrams.get(ng, 0) + 1
        
        matches = 0
        total = 0
        for ng, count in cand_ngrams.items():
            matches += min(count, ref_ngrams.get(ng, 0))
            total += count
        
        if total == 0:
            precisions.append(0.0)
        else:
            precisions.append(matches / total)
    
    # Media geometrica
    if 0.0 in precisions:
        return 0.0
    
    log_avg = sum(math.log(p) for p in precisions) / len(precisions)
    bleu = math.exp(log_avg)
    
    # Brevity penalty
    bp = min(1.0, math.exp(1 - len(ref_tokens) / max(len(cand_tokens), 1)))
    
    return bleu * bp


def calcular_rouge_l(referencia, candidato):
    """
    ROUGE-L: usa la Longest Common Subsequence (LCS).
    
    F1 = 2 * P * R / (P + R)
    donde P = LCS/len(cand), R = LCS/len(ref)
    """
    ref_tokens = referencia.lower().split()
    cand_tokens = candidato.lower().split()
    
    m, n = len(ref_tokens), len(cand_tokens)
    if m == 0 or n == 0:
        return 0.0
    
    # Tabla DP para LCS
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref_tokens[i-1] == cand_tokens[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    lcs_len = dp[m][n]
    precision = lcs_len / n
    recall = lcs_len / m
    
    if precision + recall == 0:
        return 0.0
    
    f1 = 2 * precision * recall / (precision + recall)
    return f1


# Demostrar metricas
print("\n--- Metricas de evaluacion ---")

referencia = "el modelo de lenguaje genera texto coherente y util"
candidatos = [
    "el modelo de lenguaje genera texto coherente y util",
    "el modelo genera texto coherente",
    "los perros son animales domesticos",
]

for cand in candidatos:
    bleu = calcular_bleu_simple(referencia, cand)
    rouge = calcular_rouge_l(referencia, cand)
    print(f"  BLEU={bleu:.3f} ROUGE-L={rouge:.3f} | '{cand[:50]}'")


# =====================================================================
#   PARTE 11: COSTOS Y PLANIFICACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: COSTOS ===")
print("=" * 80)

"""
COSTOS DE FINE-TUNING Y SERVING:

FINE-TUNING (precios estimados 2024-2026):
  ┌─────────────┬──────────┬──────────┬──────────┐
  │ Modelo      │ GPU      │ Metodo   │ Costo    │
  ├─────────────┼──────────┼──────────┼──────────┤
  │ 7B (Llama)  │ 1x A100  │ QLoRA    │ $5-15    │
  │ 13B         │ 1x A100  │ QLoRA    │ $15-40   │
  │ 70B         │ 4x A100  │ QLoRA    │ $100-300 │
  │ 7B          │ RTX 4090 │ QLoRA    │ ~gratis* │
  └─────────────┴──────────┴──────────┴──────────┘
  * Solo electricidad si tienes el hardware.

SERVING (costo por 1M tokens):
  ┌──────────────┬────────────┬────────────┐
  │ Metodo       │ Input      │ Output     │
  ├──────────────┼────────────┼────────────┤
  │ GPT-4o       │ $2.50      │ $10.00     │
  │ Claude 3.5   │ $3.00      │ $15.00     │
  │ Self-hosted  │ $0.10-0.50 │ $0.10-0.50 │
  │ Ollama local │ ~gratis    │ ~gratis    │
  └──────────────┴────────────┴────────────┘
"""


def estimar_costos_finetuning(
    modelo_params_b: float,
    dataset_size: int,
    epochs: int = 3,
    metodo: str = "qlora",
    gpu: str = "A100",
):
    """
    Estima costos de fine-tuning.
    
    Args:
        modelo_params_b: parametros en billones (7, 13, 70)
        dataset_size: numero de ejemplos
        epochs: epochs de entrenamiento
        metodo: "full", "lora", "qlora"
        gpu: "A100", "H100", "RTX4090"
    """
    # Tokens por ejemplo (promedio)
    tokens_per_example = 512
    total_tokens = dataset_size * tokens_per_example * epochs
    
    # Throughput (tokens/segundo segun GPU y metodo)
    throughputs = {
        ("A100", "qlora"): {7: 3000, 13: 1500, 70: 400},
        ("A100", "lora"):  {7: 2000, 13: 1000, 70: 300},
        ("H100", "qlora"): {7: 5000, 13: 2500, 70: 700},
        ("RTX4090", "qlora"): {7: 2000, 13: 800, 70: 0},
    }
    
    key = (gpu, metodo)
    param_key = min([7, 13, 70], key=lambda x: abs(x - modelo_params_b))
    tps = throughputs.get(key, {}).get(param_key, 1000)
    
    if tps == 0:
        return {"error": f"{gpu} no soporta {param_key}B con {metodo}"}
    
    # Tiempo en horas
    tiempo_s = total_tokens / tps
    tiempo_h = tiempo_s / 3600
    
    # Costo por hora segun GPU
    costo_hora = {"A100": 2.0, "H100": 3.5, "RTX4090": 0.0}
    num_gpus = 1 if param_key <= 13 else 4
    
    costo_total = tiempo_h * costo_hora.get(gpu, 2.0) * num_gpus
    
    return {
        "modelo": f"{modelo_params_b}B",
        "dataset": f"{dataset_size:,} examples",
        "total_tokens": f"{total_tokens:,}",
        "tiempo_horas": round(tiempo_h, 1),
        "gpus": f"{num_gpus}x {gpu}",
        "costo_usd": round(costo_total, 2),
    }

# Ejemplos de estimacion
print("\n--- Estimacion de costos ---")
configs = [
    (7, 5000, 3, "qlora", "A100"),
    (7, 50000, 3, "qlora", "A100"),
    (13, 10000, 3, "qlora", "A100"),
    (70, 10000, 2, "qlora", "A100"),
    (7, 5000, 3, "qlora", "RTX4090"),
]

for params, ds, ep, met, gpu in configs:
    est = estimar_costos_finetuning(params, ds, ep, met, gpu)
    if "error" in est:
        print(f"  {est}")
    else:
        print(f"  {est['modelo']:>4} | {est['dataset']:>15} | "
              f"{est['tiempo_horas']:>5}h | {est['gpus']:>10} | "
              f"${est['costo_usd']:.2f}")


# =====================================================================
#   PARTE 12: MLOPS PARA LLMs
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: MLOPS ===")
print("=" * 80)

"""
MLOPS PARA LLMs — checklist de produccion:

VERSIONADO:
  - Modelo base: HuggingFace model ID + commit hash.
  - Adapter: versionado con git (son pequeños).
  - Dataset: hash del dataset usado.
  - Config: todos los hiperparametros.

MONITOREO:
  - Latencia P50/P95/P99.
  - Tokens por segundo.
  - Tasa de errores.
  - Uso de GPU/memoria.
  - Calidad (sampling + LLM-as-judge).

SEGURIDAD:
  - Guardrails: filtrar inputs/outputs peligrosos.
  - Rate limiting.
  - Input sanitization (prompt injection).
  - Output validation.

CI/CD:
  - Tests automaticos de regresion.
  - Benchmark suite antes de deploy.
  - Canary deployment (10% trafico primero).
  - Rollback automatico si calidad baja.
"""

print("""
  STACK RECOMENDADO:

  Fine-tuning:  Unsloth / HF TRL + PEFT
  Datos:        HuggingFace Datasets
  Tracking:     Weights & Biases / MLflow
  Serving:      vLLM (GPU) / Ollama (local)
  Monitoring:   Prometheus + Grafana
  Guardrails:   NeMo Guardrails / Guardrails AI
""")


# ─── Production Checklist Implementacion ───

class ProductionChecklist:
    """
    Checklist automatizado para validar que un modelo
    esta listo para produccion.
    """
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.checks = {}
    
    def check_model_size(self, size_gb: float, max_gb: float = 20.0):
        """Verificar que el modelo cabe en la GPU objetivo."""
        passed = size_gb <= max_gb
        self.checks["model_size"] = {
            "passed": passed,
            "detail": f"{size_gb:.1f}GB / {max_gb}GB max",
        }
        return passed
    
    def check_latency(self, p50_ms: float, p99_ms: float,
                      max_p50: float = 500, max_p99: float = 2000):
        """Verificar latencia aceptable."""
        passed = p50_ms <= max_p50 and p99_ms <= max_p99
        self.checks["latency"] = {
            "passed": passed,
            "detail": f"P50={p50_ms}ms P99={p99_ms}ms",
        }
        return passed
    
    def check_quality(self, score: float, threshold: float = 0.8):
        """Verificar calidad minima."""
        passed = score >= threshold
        self.checks["quality"] = {
            "passed": passed,
            "detail": f"{score:.2%} (min: {threshold:.2%})",
        }
        return passed
    
    def check_safety(self, toxic_rate: float, max_rate: float = 0.01):
        """Verificar tasa de respuestas toxicas."""
        passed = toxic_rate <= max_rate
        self.checks["safety"] = {
            "passed": passed,
            "detail": f"{toxic_rate:.3%} toxic (max: {max_rate:.2%})",
        }
        return passed
    
    def report(self):
        """Generar reporte de checklist."""
        all_passed = all(c["passed"] for c in self.checks.values())
        status = "READY" if all_passed else "NOT READY"
        
        print(f"\n  === Production Checklist: {self.model_name} ===")
        print(f"  Status: {'✅' if all_passed else '❌'} {status}")
        
        for name, check in self.checks.items():
            icon = "✅" if check["passed"] else "❌"
            print(f"    {icon} {name}: {check['detail']}")
        
        return all_passed


# Demostrar checklist
checklist = ProductionChecklist("my-llama-7b-ft")
checklist.check_model_size(4.5, max_gb=16.0)
checklist.check_latency(p50_ms=120, p99_ms=850)
checklist.check_quality(score=0.87)
checklist.check_safety(toxic_rate=0.002)
checklist.report()

# Modelo que NO pasa
checklist_bad = ProductionChecklist("untested-model")
checklist_bad.check_model_size(25.0, max_gb=16.0)
checklist_bad.check_latency(p50_ms=2000, p99_ms=8000)
checklist_bad.check_quality(score=0.65)
checklist_bad.check_safety(toxic_rate=0.05)
checklist_bad.report()


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: FINE-TUNING PRODUCCION ===")
print("=" * 80)

print("""
  PIPELINE COMPLETO:

  1. DATOS: JSONL instrucciones/chat, 1K-100K ejemplos.
  2. SFT: fine-tune con LoRA/QLoRA, lr=2e-4, 1-3 epochs.
  3. DPO: alinear con preferencias (opcional pero recomendado).
  4. EVALUACION: BLEU, ROUGE-L, perplexity + human eval.
  5. MERGE: fusionar LoRA en modelo base.
  6. QUANTIZE: GPTQ/AWQ (GPU) o GGUF (CPU).
  7. SERVE: vLLM (produccion) o Ollama (local).
  8. CHECKLIST: size, latency, quality, safety.
  9. MONITOR: latencia, calidad, costos.

  COSTOS TIPICOS:
  - Fine-tune 7B QLoRA: $5-15 (unas horas en A100).
  - Serving self-hosted: $0.10-0.50 por 1M tokens.
  - 10-100x mas barato que APIs comerciales a escala.

  METRICAS CLAVE:
  - BLEU/ROUGE-L para tareas generativas.
  - Exact Match para QA.
  - LLM-as-judge para calidad general.
  - Perplexity para sanity check.

  EL FUTURO:
  - Modelos mas pequeños y eficientes (Phi-3, Gemma).
  - Fine-tuning en consumer GPUs (RTX 4090).
  - Agentes autonomos basados en LLMs fine-tuned.
  - Multimodal: texto + imagen + audio + video.
""")

print("=" * 80)
print("=== FIN MODULO 20: TRANSFER LEARNING Y FINE-TUNING ===")
print("=" * 80)

