# ===========================================================================
# 03_gpt_y_llm_architecture.py
# ===========================================================================
# MODULO 19: TRANSFORMER DESDE CERO
# ARCHIVO 03: GPT y Arquitecturas de LLMs
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Implementar un mini-GPT desde cero: decoder-only transformer,
# generacion autoregresiva, tokenizacion, temperature, top-k/top-p,
# y entender como escalan los LLMs modernos.
#
# CONTENIDO:
#   1. Decoder-only vs Encoder-only vs Encoder-Decoder.
#   2. GPT architecture: Decoder-only Transformer.
#   3. Causal Language Modeling: predecir el siguiente token.
#   4. Mini-GPT desde cero.
#   5. Generacion autoregresiva.
#   6. Temperature, top-k, top-p sampling.
#   7. KV-Cache: inference eficiente.
#   8. Tokenizacion: BPE y SentencePiece.
#   9. Scaling laws: como escalan los LLMs.
#   10. Arquitecturas modernas: LLaMA, Mistral.
#
# NIVEL: LLM ENGINEER / AI ARCHITECT.
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
#   PARTE 1: DECODER-ONLY vs ENCODER-ONLY
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: TRES SABORES DE TRANSFORMER ===")
print("=" * 80)

"""
ENCODER-ONLY (BERT):
  - Ve TODA la secuencia (bidireccional).
  - Ideal para: clasificacion, NER, QA extractivo.
  - No puede GENERAR texto.

DECODER-ONLY (GPT):
  - Ve solo tokens ANTERIORES (causal/autoregresivo).
  - Ideal para: generacion de texto, completion.
  - Es el que usan TODOS los LLMs modernos.

ENCODER-DECODER (T5, BART):
  - Encoder: ve toda la entrada.
  - Decoder: genera output autoregressivamente.
  - Ideal para: traduccion, summarizacion.

POR QUE DECODER-ONLY GANO:
  1. Mas simple (una sola stack).
  2. Escala mejor con mas datos y params.
  3. Un solo modelo para MUCHAS tareas (in-context learning).
  4. GPT-3 demostro que scale = intelligence.
"""

print("""
  BERT (encoder):     [CLS] The cat sat [SEP]  → clasificacion
                       ↕    ↕   ↕   ↕            (ve todo)

  GPT (decoder):      The → cat → sat → on → ?  → generacion
                       →    →    →    →           (solo ve pasado)

  T5 (enc-dec):       "translate: hello" → encoder → decoder → "hola"
""")


# =====================================================================
#   PARTE 2: GPT ARCHITECTURE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: GPT ARCHITECTURE ===")
print("=" * 80)

"""
GPT = stack de DECODER blocks con CAUSAL MASK.

Componentes:
  1. Token embedding + Positional embedding.
  2. N decoder blocks (cada uno = Masked MHA + FFN).
  3. LM Head: proyeccion final a vocabulario.

Entrenamiento:
  Input:  [The, cat, sat, on]
  Target: [cat, sat, on, the]  (shifted right)
  Loss: CrossEntropy en cada posicion.

El modelo aprende: P(next_token | previous_tokens).

TODOS los LLMs son variaciones de esta arquitectura:
  GPT-2, GPT-3, GPT-4, LLaMA, Mistral, Claude.
"""

if HAS_TORCH:
    # Reusar componentes del archivo anterior
    def scaled_dot_product_attention(Q, K, V, mask=None):
        d_k = Q.size(-1)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        weights = F.softmax(scores, dim=-1)
        return torch.matmul(weights, V), weights

    class MultiHeadAttention(nn.Module):
        def __init__(self, d_model, n_heads, dropout=0.1):
            super().__init__()
            assert d_model % n_heads == 0
            self.d_model = d_model
            self.n_heads = n_heads
            self.d_k = d_model // n_heads
            self.W_Q = nn.Linear(d_model, d_model)
            self.W_K = nn.Linear(d_model, d_model)
            self.W_V = nn.Linear(d_model, d_model)
            self.W_O = nn.Linear(d_model, d_model)
            self.dropout = nn.Dropout(dropout)

        def forward(self, Q, K, V, mask=None):
            B = Q.size(0)
            Q = self.W_Q(Q).view(B, -1, self.n_heads, self.d_k).transpose(1, 2)
            K = self.W_K(K).view(B, -1, self.n_heads, self.d_k).transpose(1, 2)
            V = self.W_V(V).view(B, -1, self.n_heads, self.d_k).transpose(1, 2)
            output, weights = scaled_dot_product_attention(Q, K, V, mask)
            output = output.transpose(1, 2).contiguous().view(B, -1, self.d_model)
            return self.W_O(output), weights

    class FeedForward(nn.Module):
        def __init__(self, d_model, d_ff=None, dropout=0.1):
            super().__init__()
            d_ff = d_ff or 4 * d_model
            self.net = nn.Sequential(
                nn.Linear(d_model, d_ff), nn.GELU(),
                nn.Dropout(dropout), nn.Linear(d_ff, d_model),
                nn.Dropout(dropout),
            )
        def forward(self, x):
            return self.net(x)

    class GPTBlock(nn.Module):
        """Decoder block para GPT (Pre-LN)."""
        def __init__(self, d_model, n_heads, d_ff=None, dropout=0.1):
            super().__init__()
            self.ln1 = nn.LayerNorm(d_model)
            self.attn = MultiHeadAttention(d_model, n_heads, dropout)
            self.ln2 = nn.LayerNorm(d_model)
            self.ffn = FeedForward(d_model, d_ff, dropout)

        def forward(self, x, mask=None):
            # Masked self-attention + residual
            normed = self.ln1(x)
            attn_out, _ = self.attn(normed, normed, normed, mask)
            x = x + attn_out
            # FFN + residual
            x = x + self.ffn(self.ln2(x))
            return x


# =====================================================================
#   PARTE 3: MINI-GPT COMPLETO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: MINI-GPT DESDE CERO ===")
print("=" * 80)

if HAS_TORCH:
    class MiniGPT(nn.Module):
        """GPT minimalista pero completo."""

        def __init__(self, vocab_size, d_model, n_heads, n_layers,
                     max_len=256, d_ff=None, dropout=0.1):
            super().__init__()
            self.d_model = d_model
            self.token_emb = nn.Embedding(vocab_size, d_model)
            self.pos_emb = nn.Embedding(max_len, d_model)

            self.blocks = nn.ModuleList([
                GPTBlock(d_model, n_heads, d_ff, dropout)
                for _ in range(n_layers)
            ])

            self.ln_final = nn.LayerNorm(d_model)
            self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

            # Weight tying: compartir pesos entre embedding y lm_head
            self.lm_head.weight = self.token_emb.weight

            self._init_weights()

        def _init_weights(self):
            for module in self.modules():
                if isinstance(module, nn.Linear):
                    nn.init.normal_(module.weight, mean=0.0, std=0.02)
                    if module.bias is not None:
                        nn.init.zeros_(module.bias)
                elif isinstance(module, nn.Embedding):
                    nn.init.normal_(module.weight, mean=0.0, std=0.02)

        def forward(self, idx, targets=None):
            B, T = idx.shape

            # Embeddings
            tok_emb = self.token_emb(idx)
            pos_emb = self.pos_emb(torch.arange(T, device=idx.device))
            x = tok_emb + pos_emb

            # Causal mask
            mask = torch.tril(torch.ones(T, T, device=idx.device))
            mask = mask.unsqueeze(0).unsqueeze(0)

            # Transformer blocks
            for block in self.blocks:
                x = block(x, mask)

            x = self.ln_final(x)
            logits = self.lm_head(x)  # (B, T, vocab_size)

            # Loss si hay targets
            loss = None
            if targets is not None:
                loss = F.cross_entropy(
                    logits.view(-1, logits.size(-1)),
                    targets.view(-1)
                )

            return logits, loss

        @torch.no_grad()
        def generate(self, idx, max_new_tokens, temperature=1.0,
                     top_k=None, top_p=None):
            """Generacion autoregresiva."""
            for _ in range(max_new_tokens):
                # Crop a max_len
                idx_cond = idx[:, -256:]

                # Forward
                logits, _ = self(idx_cond)
                logits = logits[:, -1, :]  # Solo ultimo paso

                # Temperature
                logits = logits / temperature

                # Top-k filtering
                if top_k is not None:
                    v, _ = torch.topk(logits, top_k)
                    logits[logits < v[:, [-1]]] = float('-inf')

                # Top-p (nucleus) filtering
                if top_p is not None:
                    sorted_logits, sorted_idx = torch.sort(logits, descending=True)
                    cumulative_probs = torch.cumsum(
                        F.softmax(sorted_logits, dim=-1), dim=-1
                    )
                    mask = cumulative_probs - F.softmax(sorted_logits, dim=-1) >= top_p
                    sorted_logits[mask] = float('-inf')
                    logits = sorted_logits.scatter(1, sorted_idx, sorted_logits)

                # Sample
                probs = F.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, 1)
                idx = torch.cat([idx, next_token], dim=1)

            return idx

    # Crear modelo
    print("\n--- Mini-GPT ---")

    vocab_size = 256  # Byte-level
    model_gpt = MiniGPT(
        vocab_size=vocab_size, d_model=64, n_heads=4,
        n_layers=4, max_len=128, d_ff=256
    )
    n_params = sum(p.numel() for p in model_gpt.parameters())
    print(f"  Params: {n_params:,}")
    print(f"  Config: vocab={vocab_size}, d=64, heads=4, layers=4")

    # Entrenar en datos sinteticos
    print("\n--- Entrenando Mini-GPT ---")

    # Generar secuencias con patron: numeros crecientes
    torch.manual_seed(42)
    data = []
    for _ in range(500):
        start = torch.randint(1, 50, (1,)).item()
        seq = torch.arange(start, start + 20) % vocab_size
        data.append(seq)

    train_data = torch.stack(data)
    train_ds = TensorDataset(train_data[:, :-1], train_data[:, 1:])
    train_ldr = DataLoader(train_ds, batch_size=32, shuffle=True)

    optimizer = torch.optim.AdamW(model_gpt.parameters(), lr=3e-4)

    for epoch in range(15):
        model_gpt.train()
        total_loss = 0
        for xb, yb in train_ldr:
            _, loss = model_gpt(xb, yb)
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model_gpt.parameters(), 1.0)
            optimizer.step()
            total_loss += loss.item()

        if epoch % 3 == 0:
            avg = total_loss / len(train_ldr)
            print(f"  Epoch {epoch+1:3d}: loss={avg:.4f}")


# =====================================================================
#   PARTE 4: GENERACION Y SAMPLING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: GENERACION Y SAMPLING ===")
print("=" * 80)

"""
ESTRATEGIAS DE GENERACION:

1. GREEDY: siempre elegir el token mas probable.
   → Deterministico, repetitivo, aburrido.

2. TEMPERATURE: escalar logits antes de softmax.
   T < 1: mas seguro (como greedy).
   T > 1: mas aleatorio (mas creativo/loco).
   T = 1: sampling normal.

3. TOP-K: solo considerar los K tokens mas probables.
   K=1: greedy. K=50: balanceado.
   Elimina tokens improbables de la cola.

4. TOP-P (NUCLEUS): considerar tokens hasta acumular prob P.
   P=0.9: toma los tokens que suman 90% de probabilidad.
   Adaptativo: si hay un token dominante, solo toma ese.

COMBINACION: temperature + top-p es lo standard en LLMs.
"""

if HAS_TORCH:
    print("\n--- Generacion con diferentes configs ---")

    model_gpt.eval()
    prompt = torch.tensor([[5, 6, 7, 8]])  # Numeros crecientes

    configs = [
        ("Greedy (T=0.01)", dict(temperature=0.01, top_k=None, top_p=None)),
        ("Creative (T=1.5)", dict(temperature=1.5, top_k=None, top_p=None)),
        ("Top-k=5", dict(temperature=1.0, top_k=5, top_p=None)),
        ("Top-p=0.9", dict(temperature=1.0, top_k=None, top_p=0.9)),
    ]

    for name, kwargs in configs:
        generated = model_gpt.generate(prompt.clone(), max_new_tokens=10, **kwargs)
        tokens = generated[0].tolist()
        print(f"  {name:<20}: {tokens}")

    print(f"\n  → Greedy produce la secuencia mas predecible")
    print(f"  → Temperature alta introduce mas variabilidad")


# =====================================================================
#   PARTE 5: SCALING LAWS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: SCALING LAWS ===")
print("=" * 80)

"""
SCALING LAWS (Kaplan et al., 2020):

  Loss ∝ 1 / N^α  donde N = numero de parametros

  MAS PARAMETROS → MENOS LOSS (predeciblemente).

CHINCHILLA (Hoffmann et al., 2022):
  Tokens_optimos ≈ 20 * Parameters
  GPT-3 (175B params) deberia ver 3.5T tokens.
  Pero solo vio 300B → sub-entrenado!

  LLaMA (7B): entrenado con 1T tokens → mejor que GPT-3 en muchos tasks.

TENDENCIA 2024-2025:
  - Modelos mas pequeños pero mejor entrenados.
  - Mixture of Experts (MoE): 8x7B params pero solo 7B activos.
  - Distilacion: modelo grande → modelo pequeño.
"""

print("""
  ESCALA DE LLMs:

  | Modelo       | Params  | Tokens   | Año  |
  |-------------|---------|----------|------|
  | GPT-2        | 1.5B    | 40B      | 2019 |
  | GPT-3        | 175B    | 300B     | 2020 |
  | LLaMA        | 7-65B   | 1-1.4T   | 2023 |
  | Mistral 7B   | 7B      | ~2T      | 2023 |
  | LLaMA 3      | 8-70B   | 15T+     | 2024 |
  | GPT-4        | ~1.8T?  | ~13T?    | 2023 |
""")


# =====================================================================
#   PARTE 6: ARQUITECTURAS MODERNAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: ARQUITECTURAS MODERNAS ===")
print("=" * 80)

"""
DIFERENCIAS CLAVE entre GPT-2 y LLMs modernos:

1. RoPE (Rotary Position Embedding):
   Codifica posicion RELATIVA rotando Q y K.
   Mejor que sinusoidal/aprendido para contextos largos.

2. RMSNorm en vez de LayerNorm:
   RMSNorm(x) = x / RMS(x) * γ
   Mas rapido (sin calcular media). Misma calidad.

3. SwiGLU en vez de GELU en FFN:
   SwiGLU(x) = Swish(xW) ⊙ (xV)
   Mejor loss empiricamente. Usado en LLaMA.

4. Grouped Query Attention (GQA):
   En vez de n_heads queries Y keys, comparte keys/values
   entre grupos de queries. Reduce KV-cache.
   Mistral: 8 KV heads para 32 Q heads.

5. Sliding Window Attention:
   Cada token atiende solo a W tokens vecinos.
   Reduce complejidad de O(n²) a O(n*W).
   Mistral: window=4096.

6. Flash Attention:
   Optimizacion de HARDWARE (no de algoritmo).
   Calcula atencion en bloques para usar cache de GPU.
   2-4x mas rapido, sin cambiar el output.
"""

if HAS_TORCH:
    class RMSNorm(nn.Module):
        """Root Mean Square Layer Normalization (LLaMA style)."""
        def __init__(self, d_model, eps=1e-6):
            super().__init__()
            self.weight = nn.Parameter(torch.ones(d_model))
            self.eps = eps

        def forward(self, x):
            rms = torch.sqrt(torch.mean(x ** 2, dim=-1, keepdim=True) + self.eps)
            return x / rms * self.weight

    # Comparar RMSNorm vs LayerNorm
    x = torch.randn(2, 10, 64)
    ln = nn.LayerNorm(64)
    rmsn = RMSNorm(64)

    out_ln = ln(x)
    out_rms = rmsn(x)

    print(f"\n  LayerNorm output std:  {out_ln.std().item():.4f}")
    print(f"  RMSNorm output std:    {out_rms.std().item():.4f}")
    print(f"  → RMSNorm es mas simple (sin restar media)")


# =====================================================================
#   PARTE 7: SwiGLU FFN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: SwiGLU FFN ===")
print("=" * 80)

"""
SwiGLU (Shazeer, 2020): la FFN de los LLMs modernos.

FFN clasica:  y = W2 @ GELU(W1 @ x)
SwiGLU:       y = W2 @ (Swish(W_gate @ x) ⊙ (W_up @ x))

  Swish(x) = x * sigmoid(x)
  ⊙ = multiplicacion elemento a elemento

Tiene 3 matrices (W_gate, W_up, W2) en vez de 2 (W1, W2).
Para mantener el mismo # params, d_ff se reduce a 2/3.

RESULTADO: mejor loss que GELU con mismos params.
Usado en: LLaMA, Mistral, Gemma, PaLM.
"""

if HAS_TORCH:
    class SwiGLUFFN(nn.Module):
        """SwiGLU Feed-Forward (LLaMA style)."""
        def __init__(self, d_model, d_ff=None, dropout=0.1):
            super().__init__()
            d_ff = d_ff or int(4 * d_model * 2 / 3)
            self.w_gate = nn.Linear(d_model, d_ff, bias=False)
            self.w_up = nn.Linear(d_model, d_ff, bias=False)
            self.w_down = nn.Linear(d_ff, d_model, bias=False)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x):
            gate = F.silu(self.w_gate(x))  # Swish = SiLU
            up = self.w_up(x)
            return self.dropout(self.w_down(gate * up))

    # Comparar
    ffn_gelu = FeedForward(64, 256)
    ffn_swiglu = SwiGLUFFN(64, 170)

    gelu_params = sum(p.numel() for p in ffn_gelu.parameters())
    swiglu_params = sum(p.numel() for p in ffn_swiglu.parameters())

    print(f"\n  GELU FFN (64→256→64):    {gelu_params:,} params")
    print(f"  SwiGLU FFN (64→170→64):  {swiglu_params:,} params")
    print(f"  → Similar params, mejor performance empirica")


# =====================================================================
#   PARTE 8: KV-CACHE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: KV-CACHE ===")
print("=" * 80)

"""
KV-CACHE: optimizacion CRITICA para inference.

PROBLEMA: en generacion autoregresiva, cada token nuevo
requiere recalcular la atencion con TODOS los tokens previos.
  Token 100: calcula K,V para tokens 0-99 (de nuevo!)
  Token 101: calcula K,V para tokens 0-100 (de nuevo!)
  → O(n² · d) total para generar n tokens.

SOLUCION: CACHEAR K y V de tokens ya procesados.
  Token 100: solo calcula K,V para token 100. Usa cache para 0-99.
  → O(n · d) total. MUCHO mas rapido.

PERO: el KV-cache consume MEMORIA.
  GPT-3: 96 layers × 96 heads × 12288 d_model × 2 (K+V) × seq_len
  Para context=2K: ~3GB solo de KV-cache.
  Para context=100K: ~150GB!

SOLUCIONES:
  - GQA: compartir K,V entre grupos de queries.
  - Sliding Window: solo cachear ultimos W tokens.
  - Quantizacion: KV-cache en FP8/INT8.
"""

if HAS_TORCH:
    class GPTBlockWithKVCache(nn.Module):
        """GPT block con soporte de KV-cache."""

        def __init__(self, d_model, n_heads, d_ff=None):
            super().__init__()
            self.d_model = d_model
            self.n_heads = n_heads
            self.d_k = d_model // n_heads

            self.ln1 = nn.LayerNorm(d_model)
            self.W_Q = nn.Linear(d_model, d_model)
            self.W_K = nn.Linear(d_model, d_model)
            self.W_V = nn.Linear(d_model, d_model)
            self.W_O = nn.Linear(d_model, d_model)

            self.ln2 = nn.LayerNorm(d_model)
            self.ffn = FeedForward(d_model, d_ff)

        def forward(self, x, kv_cache=None):
            B, T, _ = x.shape
            normed = self.ln1(x)

            Q = self.W_Q(normed).view(B, T, self.n_heads, self.d_k).transpose(1, 2)
            K = self.W_K(normed).view(B, T, self.n_heads, self.d_k).transpose(1, 2)
            V = self.W_V(normed).view(B, T, self.n_heads, self.d_k).transpose(1, 2)

            # Concatenar con cache
            if kv_cache is not None:
                K_cache, V_cache = kv_cache
                K = torch.cat([K_cache, K], dim=2)
                V = torch.cat([V_cache, V], dim=2)

            new_cache = (K, V)

            # Atencion (causal)
            full_len = K.size(2)
            mask = torch.tril(torch.ones(T, full_len))
            # Ajustar: solo las ultimas T filas del triangular
            if kv_cache is not None:
                mask = torch.ones(T, full_len)
                for i in range(T):
                    pos = full_len - T + i
                    mask[i, pos+1:] = 0
            mask = mask.unsqueeze(0).unsqueeze(0)

            attn_out, _ = scaled_dot_product_attention(Q, K, V, mask)
            attn_out = attn_out.transpose(1, 2).contiguous().view(B, T, self.d_model)
            x = x + self.W_O(attn_out)
            x = x + self.ffn(self.ln2(x))
            return x, new_cache

    # Demo KV-cache
    print("\n--- KV-Cache demo ---")
    import time

    block_kv = GPTBlockWithKVCache(64, 4, 256)
    block_kv.eval()

    # Sin cache: procesar toda la secuencia
    x_full = torch.randn(1, 50, 64)
    start = time.time()
    with torch.no_grad():
        for _ in range(10):
            out_full, _ = block_kv(x_full)
    time_no_cache = (time.time() - start) / 10

    # Con cache: procesar token a token
    start = time.time()
    with torch.no_grad():
        for _ in range(10):
            cache = None
            for t in range(50):
                x_t = torch.randn(1, 1, 64)
                _, cache = block_kv(x_t, kv_cache=cache)
    time_with_cache = (time.time() - start) / 10

    print(f"  Full forward (50 tokens):  {time_no_cache*1000:.2f} ms")
    print(f"  Token-by-token (cached):   {time_with_cache*1000:.2f} ms")
    print(f"  → KV-cache evita recalcular K,V de tokens previos")


# =====================================================================
#   PARTE 9: TOKENIZACION BPE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: TOKENIZACION ===")
print("=" * 80)

"""
TOKENIZACION: convertir texto en numeros.

METODOS:
1. Character-level: cada caracter es un token.
   Vocab pequeño (~100) pero secuencias MUY largas.

2. Word-level: cada palabra es un token.
   Vocab enorme (~500K). No maneja palabras nuevas.

3. BPE (Byte-Pair Encoding): el standard.
   Empieza con caracteres, fusiona pares frecuentes.
   "lowest" → ["low", "est"]
   Vocab: 30K-100K. Balance perfecto.

4. SentencePiece: BPE a nivel de bytes.
   Funciona para cualquier idioma sin preproceso.
   Usado por LLaMA, Mistral.
"""

# Implementacion simple de BPE
print("\n--- BPE simplificado ---")


class SimpleBPE:
    """Tokenizador BPE minimalista."""

    def __init__(self, vocab_size=300):
        self.vocab_size = vocab_size
        self.merges = {}
        self.vocab = {}

    def train(self, text):
        """Entrena BPE en un texto."""
        # Inicializar con bytes
        tokens = list(text.encode('utf-8'))

        # Iterar: encontrar y fusionar par mas frecuente
        next_id = 256  # Bytes van de 0-255
        while next_id < self.vocab_size:
            # Contar pares
            pairs = {}
            for i in range(len(tokens) - 1):
                pair = (tokens[i], tokens[i+1])
                pairs[pair] = pairs.get(pair, 0) + 1

            if not pairs:
                break

            # Par mas frecuente
            best_pair = max(pairs, key=pairs.get)
            if pairs[best_pair] < 2:
                break

            # Fusionar
            self.merges[best_pair] = next_id
            new_tokens = []
            i = 0
            while i < len(tokens):
                if (i < len(tokens) - 1 and
                    (tokens[i], tokens[i+1]) == best_pair):
                    new_tokens.append(next_id)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
            next_id += 1

        print(f"  Merges aprendidos: {len(self.merges)}")
        return tokens

    def encode(self, text):
        """Tokeniza texto con merges aprendidos."""
        tokens = list(text.encode('utf-8'))
        for pair, new_id in self.merges.items():
            new_tokens = []
            i = 0
            while i < len(tokens):
                if (i < len(tokens) - 1 and
                    (tokens[i], tokens[i+1]) == pair):
                    new_tokens.append(new_id)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
        return tokens


# Demo
text = "the cat sat on the mat. the cat ate the rat."
bpe = SimpleBPE(vocab_size=280)
trained = bpe.train(text * 10)

encoded = bpe.encode("the cat")
print(f"  'the cat' → {encoded}")
print(f"  Bytes: {list('the cat'.encode('utf-8'))}")
print(f"  → BPE comprime tokens frecuentes")


# =====================================================================
#   PARTE 10: PERPLEXITY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: PERPLEXITY ===")
print("=" * 80)

"""
PERPLEXITY: metrica standard para evaluar language models.

  PPL = exp(-(1/N) * Σ log P(x_i | x_{<i}))

INTUICION:
  PPL = 1: el modelo predice perfectamente.
  PPL = V: tan malo como adivinar al azar (V = vocab size).

BENCHMARKS:
  GPT-2 en WikiText-103: PPL ≈ 29
  GPT-3: PPL ≈ 20
  LLaMA 7B: PPL ≈ 12
  → Menor PPL = mejor modelo.
"""

if HAS_TORCH:
    @torch.no_grad()
    def compute_perplexity(model, data_loader):
        """Calcula perplexity del modelo."""
        model.eval()
        total_loss = 0
        total_tokens = 0

        for xb, yb in data_loader:
            _, loss = model(xb, yb)
            n_tokens = yb.numel()
            total_loss += loss.item() * n_tokens
            total_tokens += n_tokens

        avg_loss = total_loss / total_tokens
        return math.exp(avg_loss)

    ppl = compute_perplexity(model_gpt, train_ldr)
    print(f"\n  Mini-GPT perplexity (train): {ppl:.2f}")
    print(f"  Random baseline: {vocab_size:.0f}")
    print(f"  → {ppl:.0f} << {vocab_size} = el modelo aprendio algo!")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: GPT Y LLMs ===")
print("=" * 80)

print("""
  GPT = Decoder-only Transformer + Causal Mask

  COMPONENTES:
  1. Token + Position Embedding
  2. N x (Masked MHA → FFN) blocks
  3. LM Head (logits → vocabulario)

  ENTRENAMIENTO:
  Next token prediction: P(x_t | x_1, ..., x_{t-1})

  GENERACION:
  Autoregresiva: genera 1 token → alimenta → genera siguiente
  Sampling: temperature + top-p (nucleus)

  INNOVACIONES MODERNAS:
  - RoPE > sinusoidal (posiciones relativas)
  - RMSNorm > LayerNorm (mas rapido)
  - SwiGLU > GELU (mejor FFN)
  - GQA > MHA (menos KV-cache)
  - KV-Cache: evita recalcular K,V previos
  - Flash Attention (optimizacion GPU)
  - Weight tying (embedding = lm_head)

  TOKENIZACION: BPE / SentencePiece (30K-100K vocab)
  EVALUACION: Perplexity (menor = mejor)

  SCALING: mas params + mas datos = mejor modelo
  CHINCHILLA: tokens_optimos ≈ 20 * params
""")

print("=" * 80)
print("=== FIN MODULO 19, ARCHIVO 03 ===")
print("=" * 80)
