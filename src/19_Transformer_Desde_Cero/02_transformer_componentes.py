# ===========================================================================
# 02_transformer_componentes.py
# ===========================================================================
# MODULO 19: TRANSFORMER DESDE CERO
# ARCHIVO 02: Componentes del Transformer en Detalle
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Implementar y entender cada componente del Transformer:
# Multi-Head Attention, positional encoding, layer norm,
# feed-forward network, encoder, decoder, y masking.
#
# CONTENIDO:
#   1. Scaled Dot-Product Attention (detalle).
#   2. Multi-Head Attention: por que multiples cabezas.
#   3. Positional Encoding: sin/cos y aprendido.
#   4. Layer Normalization vs Batch Normalization.
#   5. Feed-Forward Network (FFN).
#   6. Encoder Block completo.
#   7. Decoder Block completo.
#   8. Masking: padding mask y causal mask.
#   9. Transformer completo.
#   10. Tokenizacion basica.
#   11. Transformer para clasificacion.
#
# NIVEL: DEEP LEARNING ARCHITECT.
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
#   PARTE 1: SCALED DOT-PRODUCT ATTENTION
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: SCALED DOT-PRODUCT ATTENTION ===")
print("=" * 80)

"""
LA OPERACION CENTRAL DEL TRANSFORMER.

  Attention(Q, K, V) = softmax(Q @ K^T / √d_k) @ V

INTUICION:
  Q (Query): "que estoy buscando"
  K (Key): "que informacion tengo"
  V (Value): "que valor devuelvo"

  Q @ K^T: similitud entre cada query y cada key.
  / √d_k: normalizar para evitar gradientes muy pequenos.
  softmax: convertir similitudes en probabilidades.
  @ V: ponderar los values por las probabilidades.

EJEMPLO (lenguaje):
  "The cat sat on the mat"
  Query para "sat": ¿con que palabras me relaciono?
  Keys: todas las palabras.
  Resultado: alta atencion a "cat" (sujeto) y "mat" (objeto).
"""

if HAS_TORCH:
    def scaled_dot_product_attention(Q, K, V, mask=None):
        """
        Q: (batch, n_heads, seq_len, d_k)
        K: (batch, n_heads, seq_len, d_k)
        V: (batch, n_heads, seq_len, d_v)
        mask: (batch, 1, 1, seq_len) o (1, 1, seq_len, seq_len)
        """
        d_k = Q.size(-1)

        # 1. Calcular scores: Q @ K^T
        scores = torch.matmul(Q, K.transpose(-2, -1))  # (B, H, T, T)

        # 2. Escalar por √d_k
        scores = scores / math.sqrt(d_k)

        # 3. Aplicar mask (si hay)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))

        # 4. Softmax → probabilidades
        attention_weights = F.softmax(scores, dim=-1)

        # 5. Ponderar values
        output = torch.matmul(attention_weights, V)  # (B, H, T, d_v)

        return output, attention_weights

    # Demo
    print("\n--- Scaled Dot-Product Attention ---")

    batch, heads, seq_len, d_k = 1, 1, 4, 8
    Q = torch.randn(batch, heads, seq_len, d_k)
    K = torch.randn(batch, heads, seq_len, d_k)
    V = torch.randn(batch, heads, seq_len, d_k)

    output, weights = scaled_dot_product_attention(Q, K, V)

    print(f"  Q, K, V: {Q.shape}")
    print(f"  Output: {output.shape}")
    print(f"  Attention weights (token 0 atiende a):")
    w = weights[0, 0, 0].numpy()
    for i, val in enumerate(w):
        bar = "█" * int(val * 40)
        print(f"    → token {i}: {val:.3f} {bar}")
    print(f"  Sum: {w.sum():.4f} (debe ser 1.0)")


# =====================================================================
#   PARTE 2: MULTI-HEAD ATTENTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: MULTI-HEAD ATTENTION ===")
print("=" * 80)

"""
POR QUE MULTIPLES CABEZAS:

Una sola cabeza de atencion solo puede capturar UN tipo de relacion.
Multiples cabezas capturan DIFERENTES relaciones simultaneamente:

  Cabeza 1: atencion sintatica (sujeto-verbo).
  Cabeza 2: atencion posicional (token anterior).
  Cabeza 3: atencion semantica (sinonimos).
  Cabeza 4: atencion de correferencia (pronombres).

IMPLEMENTACION:
  1. Proyectar Q, K, V con matrices aprendidas (una por cabeza).
  2. Calcular atencion en paralelo para cada cabeza.
  3. Concatenar outputs de todas las cabezas.
  4. Proyectar con W_O final.

  MultiHead(Q,K,V) = Concat(head_1, ..., head_h) @ W_O
  donde head_i = Attention(Q@W_Q_i, K@W_K_i, V@W_V_i)
"""

if HAS_TORCH:
    class MultiHeadAttention(nn.Module):
        """Multi-Head Attention implementado desde cero."""

        def __init__(self, d_model, n_heads, dropout=0.1):
            super().__init__()
            assert d_model % n_heads == 0
            self.d_model = d_model
            self.n_heads = n_heads
            self.d_k = d_model // n_heads

            # Proyecciones lineales
            self.W_Q = nn.Linear(d_model, d_model)
            self.W_K = nn.Linear(d_model, d_model)
            self.W_V = nn.Linear(d_model, d_model)
            self.W_O = nn.Linear(d_model, d_model)
            self.dropout = nn.Dropout(dropout)

        def forward(self, Q, K, V, mask=None):
            batch_size = Q.size(0)

            # 1. Proyectar Q, K, V
            Q = self.W_Q(Q)  # (B, T, d_model)
            K = self.W_K(K)
            V = self.W_V(V)

            # 2. Reshape para multiples cabezas
            # (B, T, d_model) → (B, T, n_heads, d_k) → (B, n_heads, T, d_k)
            Q = Q.view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
            K = K.view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
            V = V.view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)

            # 3. Atencion escalada
            output, weights = scaled_dot_product_attention(Q, K, V, mask)

            # 4. Concatenar cabezas
            # (B, n_heads, T, d_k) → (B, T, d_model)
            output = output.transpose(1, 2).contiguous().view(
                batch_size, -1, self.d_model
            )

            # 5. Proyeccion final
            return self.W_O(output), weights

    # Demo
    print("\n--- Multi-Head Attention ---")

    mha = MultiHeadAttention(d_model=64, n_heads=8)
    x = torch.randn(2, 10, 64)  # batch=2, seq=10, d_model=64

    out, weights = mha(x, x, x)  # Self-attention
    n_params = sum(p.numel() for p in mha.parameters())

    print(f"  d_model=64, n_heads=8, d_k={64//8}")
    print(f"  Input: {x.shape}")
    print(f"  Output: {out.shape}")
    print(f"  Attention weights: {weights.shape} (B, H, T, T)")
    print(f"  Params: {n_params:,}")


# =====================================================================
#   PARTE 3: POSITIONAL ENCODING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: POSITIONAL ENCODING ===")
print("=" * 80)

"""
PROBLEMA: el Transformer NO tiene nocion de ORDEN.
  Sin PE: "the cat sat" = "sat the cat" (misma atencion).

SOLUCION: sumar un vector de posicion a cada embedding.

SINUSOIDAL (original, Vaswani 2017):
  PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
  PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

  Ventaja: funciona para cualquier longitud (no aprende nada).
  Cada dimension captura frecuencias diferentes.

APRENDIDO (BERT, GPT):
  PE = nn.Embedding(max_len, d_model)
  Ventaja: la red aprende las posiciones optimas.
  Desventaja: limitado a max_len posiciones.

ROTARY (RoPE, LLaMA, Mistral):
  Codifica posicion RELATIVA rotando Q y K.
  Estado del arte para LLMs.
"""

if HAS_TORCH:
    class SinusoidalPositionalEncoding(nn.Module):
        """Positional Encoding sinusoidal (Vaswani et al.)."""

        def __init__(self, d_model, max_len=5000, dropout=0.1):
            super().__init__()
            self.dropout = nn.Dropout(dropout)

            pe = torch.zeros(max_len, d_model)
            position = torch.arange(0, max_len).unsqueeze(1).float()
            div_term = torch.exp(
                torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
            )

            pe[:, 0::2] = torch.sin(position * div_term)
            pe[:, 1::2] = torch.cos(position * div_term)
            pe = pe.unsqueeze(0)  # (1, max_len, d_model)

            self.register_buffer('pe', pe)

        def forward(self, x):
            # x: (batch, seq_len, d_model)
            x = x + self.pe[:, :x.size(1), :]
            return self.dropout(x)

    # Demo
    print("\n--- Positional Encoding ---")
    pe = SinusoidalPositionalEncoding(d_model=64)
    x = torch.zeros(1, 20, 64)  # 20 posiciones
    out = pe(x)

    # Mostrar patrones
    pe_vals = pe.pe[0, :10, :8].numpy()
    print(f"  PE values (pos 0-9, dims 0-7):")
    print(f"  {'Pos':<5}", end="")
    for d in range(8):
        print(f" dim{d:>3}", end="")
    print()
    for pos in range(10):
        print(f"  {pos:<5}", end="")
        for d in range(8):
            print(f" {pe_vals[pos, d]:6.3f}", end="")
        print()


# =====================================================================
#   PARTE 4: LAYER NORMALIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: LAYER NORM vs BATCH NORM ===")
print("=" * 80)

"""
BATCH NORM: normaliza sobre el BATCH (para cada feature).
  Problemas en secuencias: batch sizes variables, inference.

LAYER NORM: normaliza sobre las FEATURES (para cada muestra).
  No depende del batch → funciona igual en train e inference.
  STANDARD en Transformers.

  LayerNorm(x) = γ * (x - μ) / (σ + ε) + β
  donde μ y σ se calculan sobre la ultima dimension.
"""

if HAS_TORCH:
    x = torch.randn(2, 5, 64)  # batch=2, seq=5, features=64

    bn = nn.BatchNorm1d(64)
    ln = nn.LayerNorm(64)

    # LayerNorm normaliza por muestra
    out_ln = ln(x)
    print(f"\n  Input: {x.shape}")
    print(f"  LayerNorm output mean: {out_ln[0, 0].mean().item():.6f}")
    print(f"  LayerNorm output std:  {out_ln[0, 0].std().item():.4f}")
    print(f"  → Normaliza sobre features, no sobre batch")


# =====================================================================
#   PARTE 5: FEED-FORWARD NETWORK
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: FEED-FORWARD NETWORK ===")
print("=" * 80)

"""
FFN: dos capas lineales con activacion.

  FFN(x) = W2 @ GELU(W1 @ x + b1) + b2

Dimension interna tipicamente 4x d_model:
  d_model=512 → d_ff=2048

Cada posicion se procesa INDEPENDIENTEMENTE.
La FFN es donde el modelo "piensa" y transforma representaciones.

VARIANTES MODERNAS:
  - SwiGLU (LLaMA): mejor que GELU para LLMs.
  - Mixture of Experts (MoE): solo activa un subconjunto de FFNs.
"""

if HAS_TORCH:
    class FeedForward(nn.Module):
        """FFN del Transformer."""
        def __init__(self, d_model, d_ff=None, dropout=0.1):
            super().__init__()
            d_ff = d_ff or 4 * d_model
            self.net = nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(d_ff, d_model),
                nn.Dropout(dropout),
            )

        def forward(self, x):
            return self.net(x)

    ffn = FeedForward(64, 256)
    x = torch.randn(2, 10, 64)
    out = ffn(x)
    n_params = sum(p.numel() for p in ffn.parameters())
    print(f"\n  FFN(64→256→64): {n_params:,} params")
    print(f"  Input: {x.shape} → Output: {out.shape}")


# =====================================================================
#   PARTE 6: ENCODER BLOCK
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: ENCODER BLOCK ===")
print("=" * 80)

"""
ENCODER BLOCK = MHA + FFN + residuals + LayerNorm.

  x → LayerNorm → MHA → + x (residual) →
  → LayerNorm → FFN → + (residual) → output

NOTA: Pre-LN (LayerNorm antes) vs Post-LN (LayerNorm despues).
  Pre-LN es mas estable en entrenamiento. Usado en GPT-2+.
"""

if HAS_TORCH:
    class TransformerEncoderBlock(nn.Module):
        """Un bloque del encoder (Pre-LN)."""

        def __init__(self, d_model, n_heads, d_ff=None, dropout=0.1):
            super().__init__()
            self.ln1 = nn.LayerNorm(d_model)
            self.mha = MultiHeadAttention(d_model, n_heads, dropout)
            self.ln2 = nn.LayerNorm(d_model)
            self.ffn = FeedForward(d_model, d_ff, dropout)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x, mask=None):
            # Pre-LN: norm → attention → residual
            normed = self.ln1(x)
            attn_out, _ = self.mha(normed, normed, normed, mask)
            x = x + self.dropout(attn_out)

            # Pre-LN: norm → ffn → residual
            normed = self.ln2(x)
            ffn_out = self.ffn(normed)
            x = x + self.dropout(ffn_out)

            return x

    enc_block = TransformerEncoderBlock(d_model=64, n_heads=8)
    x = torch.randn(2, 10, 64)
    out = enc_block(x)
    n_params = sum(p.numel() for p in enc_block.parameters())
    print(f"\n  Encoder block: {n_params:,} params")
    print(f"  Input: {x.shape} → Output: {out.shape}")


# =====================================================================
#   PARTE 7: MASKING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: MASKING ===")
print("=" * 80)

"""
DOS TIPOS DE MASKS:

1. PADDING MASK: ignora tokens de padding.
   [hello, world, PAD, PAD] → mask = [1, 1, 0, 0]
   Atencion: no atender a posiciones PAD.

2. CAUSAL MASK (look-ahead mask): impide ver el futuro.
   Para generacion autoregresiva (GPT).
   Token t solo puede atender a tokens 0..t.

   1 0 0 0
   1 1 0 0
   1 1 1 0
   1 1 1 1
"""

if HAS_TORCH:
    def create_causal_mask(seq_len):
        """Mask triangular inferior (para decoder/GPT)."""
        return torch.tril(torch.ones(seq_len, seq_len)).unsqueeze(0).unsqueeze(0)

    def create_padding_mask(lengths, max_len):
        """Mask de padding basado en longitudes reales."""
        mask = torch.arange(max_len).expand(len(lengths), max_len)
        mask = mask < torch.tensor(lengths).unsqueeze(1)
        return mask.unsqueeze(1).unsqueeze(2)  # (B, 1, 1, T)

    # Causal mask
    causal = create_causal_mask(5)
    print(f"\n  Causal mask (5x5):")
    print(causal[0, 0].int().numpy())

    # Padding mask
    pad_mask = create_padding_mask([4, 3, 5], 5)
    print(f"\n  Padding mask (lengths=[4,3,5]):")
    for i in range(3):
        print(f"    Seq {i}: {pad_mask[i, 0, 0].int().tolist()}")

    # Atencion con causal mask
    Q = K = V = torch.randn(1, 1, 5, 8)
    out_masked, w_masked = scaled_dot_product_attention(Q, K, V, causal)
    print(f"\n  Attention con causal mask (token 2):")
    print(f"    weights: {w_masked[0, 0, 2].numpy().round(3)}")
    print(f"    → Solo atiende a tokens 0, 1, 2 (no ve 3, 4)")


# =====================================================================
#   PARTE 8: TRANSFORMER COMPLETO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: TRANSFORMER ENCODER COMPLETO ===")
print("=" * 80)

if HAS_TORCH:
    class TransformerEncoder(nn.Module):
        """Stack de encoder blocks con embeddings."""

        def __init__(self, vocab_size, d_model, n_heads, n_layers,
                     d_ff=None, max_len=512, dropout=0.1):
            super().__init__()
            self.embedding = nn.Embedding(vocab_size, d_model)
            self.pos_enc = SinusoidalPositionalEncoding(d_model, max_len, dropout)
            self.layers = nn.ModuleList([
                TransformerEncoderBlock(d_model, n_heads, d_ff, dropout)
                for _ in range(n_layers)
            ])
            self.final_norm = nn.LayerNorm(d_model)
            self.d_model = d_model

        def forward(self, x, mask=None):
            # Embedding + positional encoding
            x = self.embedding(x) * math.sqrt(self.d_model)
            x = self.pos_enc(x)

            # N encoder blocks
            for layer in self.layers:
                x = layer(x, mask)

            return self.final_norm(x)

    # Demo: mini BERT
    print("\n--- Mini Transformer Encoder ---")

    encoder = TransformerEncoder(
        vocab_size=1000, d_model=64, n_heads=4,
        n_layers=4, d_ff=256, max_len=128
    )
    n_params = sum(p.numel() for p in encoder.parameters())

    tokens = torch.randint(0, 1000, (2, 20))  # batch=2, seq=20
    out = encoder(tokens)

    print(f"  Config: vocab=1000, d=64, heads=4, layers=4")
    print(f"  Params: {n_params:,}")
    print(f"  Input tokens: {tokens.shape}")
    print(f"  Output: {out.shape}")


# =====================================================================
#   PARTE 9: TRANSFORMER PARA CLASIFICACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: CLASIFICACION CON TRANSFORMER ===")
print("=" * 80)

if HAS_TORCH:
    class TransformerClassifier(nn.Module):
        """Transformer para clasificacion de secuencias."""

        def __init__(self, vocab_size, d_model, n_heads, n_layers,
                     num_classes, d_ff=None, max_len=128, dropout=0.1):
            super().__init__()
            self.encoder = TransformerEncoder(
                vocab_size, d_model, n_heads, n_layers, d_ff, max_len, dropout
            )
            self.classifier = nn.Sequential(
                nn.Linear(d_model, d_model),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(d_model, num_classes),
            )

        def forward(self, x):
            encoded = self.encoder(x)
            # Usar media de todos los tokens (como pooling)
            pooled = encoded.mean(dim=1)
            return self.classifier(pooled)

    # Dataset sintetico
    torch.manual_seed(42)
    n_samples = 1000
    seq_length = 15
    vocab = 100
    n_cls = 3

    X_tok = torch.randint(1, vocab, (n_samples, seq_length))
    y_tok = torch.randint(0, n_cls, (n_samples,))
    # Señal: clase determina el primer token
    for i in range(n_samples):
        X_tok[i, 0] = y_tok[i].item() + 1

    train_tok = TensorDataset(X_tok[:800], y_tok[:800])
    val_tok = TensorDataset(X_tok[800:], y_tok[800:])
    train_ldr = DataLoader(train_tok, batch_size=64, shuffle=True)
    val_ldr = DataLoader(val_tok, batch_size=200)

    model_clf = TransformerClassifier(
        vocab_size=vocab, d_model=32, n_heads=4, n_layers=2,
        num_classes=n_cls, d_ff=128
    )
    n_params = sum(p.numel() for p in model_clf.parameters())
    print(f"\n  Classifier: {n_params:,} params")

    opt = torch.optim.Adam(model_clf.parameters(), lr=1e-3)

    for epoch in range(15):
        model_clf.train()
        for xb, yb in train_ldr:
            opt.zero_grad()
            loss = nn.CrossEntropyLoss()(model_clf(xb), yb)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model_clf.parameters(), 1.0)
            opt.step()

        if epoch % 3 == 0:
            model_clf.eval()
            with torch.no_grad():
                correct = sum(
                    (model_clf(xb).argmax(1) == yb).sum().item()
                    for xb, yb in val_ldr
                )
            print(f"  Epoch {epoch+1:3d}: val_acc={correct/len(val_tok):.4f}")


# =====================================================================
#   PARTE 10: DECODER BLOCK CON CROSS-ATTENTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: DECODER BLOCK ===")
print("=" * 80)

"""
DECODER BLOCK: 3 sub-capas (en vez de 2 del encoder):

  1. Masked Self-Attention: atiende solo a tokens anteriores.
  2. Cross-Attention: atiende al output del encoder.
  3. Feed-Forward Network.

  x → LN → Masked MHA(x, x, x) → +residual
  → LN → Cross MHA(x, enc_out, enc_out) → +residual
  → LN → FFN → +residual → output

CROSS-ATTENTION:
  Q viene del decoder (que estoy buscando).
  K, V vienen del encoder (la informacion fuente).
  → El decoder "consulta" al encoder.
"""

if HAS_TORCH:
    class TransformerDecoderBlock(nn.Module):
        """Bloque del decoder con masked self-attn + cross-attn."""

        def __init__(self, d_model, n_heads, d_ff=None, dropout=0.1):
            super().__init__()
            # Masked self-attention
            self.ln1 = nn.LayerNorm(d_model)
            self.self_attn = MultiHeadAttention(d_model, n_heads, dropout)

            # Cross-attention
            self.ln2 = nn.LayerNorm(d_model)
            self.cross_attn = MultiHeadAttention(d_model, n_heads, dropout)

            # FFN
            self.ln3 = nn.LayerNorm(d_model)
            self.ffn = FeedForward(d_model, d_ff, dropout)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x, enc_output, self_mask=None, cross_mask=None):
            # 1. Masked self-attention
            normed = self.ln1(x)
            attn_out, _ = self.self_attn(normed, normed, normed, self_mask)
            x = x + self.dropout(attn_out)

            # 2. Cross-attention (Q=decoder, K,V=encoder)
            normed = self.ln2(x)
            cross_out, cross_weights = self.cross_attn(
                normed, enc_output, enc_output, cross_mask
            )
            x = x + self.dropout(cross_out)

            # 3. FFN
            x = x + self.dropout(self.ffn(self.ln3(x)))
            return x, cross_weights

    dec_block = TransformerDecoderBlock(d_model=64, n_heads=8)
    x_dec = torch.randn(2, 8, 64)    # Decoder input
    x_enc = torch.randn(2, 12, 64)   # Encoder output
    causal_m = create_causal_mask(8)

    out_dec, cross_w = dec_block(x_dec, x_enc, self_mask=causal_m)
    n_params = sum(p.numel() for p in dec_block.parameters())

    print(f"\n  Decoder block: {n_params:,} params")
    print(f"  Decoder input: {x_dec.shape}")
    print(f"  Encoder output: {x_enc.shape}")
    print(f"  Decoder output: {out_dec.shape}")
    print(f"  Cross-attn weights: {cross_w.shape}")
    print(f"  → Decoder (8 tokens) atiende a encoder (12 tokens)")


# =====================================================================
#   PARTE 11: ENCODER-DECODER TRANSFORMER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: FULL ENCODER-DECODER ===")
print("=" * 80)

"""
TRANSFORMER COMPLETO (Vaswani et al., 2017):
  Encoder: procesa la secuencia fuente.
  Decoder: genera la secuencia objetivo, consultando al encoder.

  Usado en: traduccion (T5, mBART), summarizacion, STT.
"""

if HAS_TORCH:
    class FullTransformer(nn.Module):
        """Transformer Encoder-Decoder completo."""

        def __init__(self, src_vocab, tgt_vocab, d_model=64,
                     n_heads=4, n_layers=2, d_ff=256, max_len=128):
            super().__init__()
            # Encoder
            self.src_emb = nn.Embedding(src_vocab, d_model)
            self.src_pe = SinusoidalPositionalEncoding(d_model, max_len)
            self.enc_layers = nn.ModuleList([
                TransformerEncoderBlock(d_model, n_heads, d_ff)
                for _ in range(n_layers)
            ])
            self.enc_norm = nn.LayerNorm(d_model)

            # Decoder
            self.tgt_emb = nn.Embedding(tgt_vocab, d_model)
            self.tgt_pe = SinusoidalPositionalEncoding(d_model, max_len)
            self.dec_layers = nn.ModuleList([
                TransformerDecoderBlock(d_model, n_heads, d_ff)
                for _ in range(n_layers)
            ])
            self.dec_norm = nn.LayerNorm(d_model)

            # Output
            self.output_proj = nn.Linear(d_model, tgt_vocab)
            self.d_model = d_model

        def encode(self, src):
            x = self.src_emb(src) * math.sqrt(self.d_model)
            x = self.src_pe(x)
            for layer in self.enc_layers:
                x = layer(x)
            return self.enc_norm(x)

        def decode(self, tgt, enc_output):
            T = tgt.size(1)
            causal = create_causal_mask(T).to(tgt.device)

            x = self.tgt_emb(tgt) * math.sqrt(self.d_model)
            x = self.tgt_pe(x)

            for layer in self.dec_layers:
                x, _ = layer(x, enc_output, self_mask=causal)

            return self.dec_norm(x)

        def forward(self, src, tgt):
            enc_out = self.encode(src)
            dec_out = self.decode(tgt, enc_out)
            return self.output_proj(dec_out)

    # Demo
    print("\n--- Full Encoder-Decoder ---")

    transformer = FullTransformer(
        src_vocab=500, tgt_vocab=500, d_model=64,
        n_heads=4, n_layers=2, d_ff=256
    )
    n_params = sum(p.numel() for p in transformer.parameters())

    src = torch.randint(0, 500, (2, 10))
    tgt = torch.randint(0, 500, (2, 8))
    out = transformer(src, tgt)

    print(f"  Params: {n_params:,}")
    print(f"  Source: {src.shape} → Encoder")
    print(f"  Target: {tgt.shape} → Decoder")
    print(f"  Output: {out.shape} (B, tgt_len, tgt_vocab)")


# =====================================================================
#   PARTE 12: ATTENTION VISUALIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: VISUALIZACION DE ATENCION ===")
print("=" * 80)

"""
VISUALIZAR ATENCION: entender QUE aprende cada cabeza.

En la practica:
  - Cabezas tempranas: patrones posicionales (atiende a vecinos).
  - Cabezas intermedias: patrones sintacticos.
  - Cabezas profundas: patrones semanticos/abstractos.
"""

if HAS_TORCH:
    print("\n--- Patrones de atencion ---")

    # Capturar pesos de atencion por cabeza
    model_clf.eval()
    x_sample = X_tok[:1]

    # Hook para capturar atencion
    attn_weights_all = []

    def capture_attention(module, input, output):
        if isinstance(output, tuple) and len(output) == 2:
            _, weights = output
            attn_weights_all.append(weights.detach())

    hooks = []
    for layer in model_clf.encoder.layers:
        h = layer.mha.register_forward_hook(capture_attention)
        hooks.append(h)

    with torch.no_grad():
        _ = model_clf(x_sample)

    for h in hooks:
        h.remove()

    # Analizar patrones
    for i, w in enumerate(attn_weights_all):
        # w: (1, n_heads, T, T)
        print(f"\n  Layer {i+1} attention patterns:")
        for head in range(min(4, w.shape[1])):
            diagonal = torch.diagonal(w[0, head]).mean().item()
            neighbor = 0
            if w.shape[-1] > 1:
                neighbor = torch.diagonal(w[0, head], offset=-1).mean().item()
            entropy = -(w[0, head] * (w[0, head] + 1e-10).log()).sum(-1).mean().item()
            print(f"    Head {head}: self={diagonal:.3f}, "
                  f"prev={neighbor:.3f}, entropy={entropy:.2f}")


# =====================================================================
#   PARTE 13: COMPLEJIDAD COMPUTACIONAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: COMPLEJIDAD ===")
print("=" * 80)

"""
COMPLEJIDAD DEL TRANSFORMER:

Self-Attention: O(n² · d) donde n=seq_len, d=d_model
  → CUADRATICA en la longitud de secuencia!
  → seq_len=1K: 1M operaciones
  → seq_len=100K: 10B operaciones

FFN: O(n · d²)
  → Lineal en n, cuadratica en d.

TOTAL: O(n² · d + n · d²)
  Para n < d: dominado por FFN.
  Para n > d: dominado por atencion.

SOLUCIONES PARA CONTEXTOS LARGOS:
  1. Sparse Attention (BigBird): O(n · √n)
  2. Linear Attention: O(n · d)
  3. Flash Attention: mismo O() pero 2-4x mas rapido en GPU
  4. Sliding Window (Mistral): O(n · w) donde w << n
"""

if HAS_TORCH:
    import time

    print("\n--- Benchmark: atencion vs longitud ---")

    d_model = 64
    n_heads = 4
    mha_bench = MultiHeadAttention(d_model, n_heads)
    mha_bench.eval()

    for seq_len in [32, 64, 128, 256, 512]:
        x = torch.randn(1, seq_len, d_model)
        # Warmup
        with torch.no_grad():
            _ = mha_bench(x, x, x)

        # Time
        start = time.time()
        with torch.no_grad():
            for _ in range(10):
                _ = mha_bench(x, x, x)
        elapsed = (time.time() - start) / 10 * 1000

        print(f"  seq_len={seq_len:4d}: {elapsed:.2f} ms "
              f"(n²={seq_len**2:>8,})")

    print(f"\n  → Tiempo crece ~cuadraticamente con seq_len")
    print(f"  → Por eso contextos largos son caros!")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: COMPONENTES DEL TRANSFORMER ===")
print("=" * 80)

print("""
  COMPONENTES:

  1. EMBEDDING: tokens → vectores (nn.Embedding).
  2. POSITIONAL ENCODING: orden de los tokens (sin/cos o aprendido).
  3. MULTI-HEAD ATTENTION: relaciones entre tokens.
     Q @ K^T / √d → softmax → @ V (por cabeza, luego concat).
  4. LAYER NORM: normaliza features (no batch).
  5. FEED-FORWARD: MLP por posicion (d→4d→d).
  6. RESIDUAL CONNECTIONS: x + sublayer(x).
  7. MASKING: padding mask + causal mask.

  ENCODER BLOCK: LN → MHA → residual → LN → FFN → residual
  DECODER BLOCK: + masked self-attention + cross-attention

  COMPLEJIDAD: O(n² · d) para atencion → problema con contextos largos

  ESCALAMIENTO:
    GPT-2: 12 layers, 768 d_model, 12 heads = 117M params
    GPT-3: 96 layers, 12288 d_model, 96 heads = 175B params
    → Solo escalar estos numeros!
""")

print("=" * 80)
print("=== FIN MODULO 19, ARCHIVO 02 ===")
print("=" * 80)
