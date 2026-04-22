# ===========================================================================
# 01_transformer_scratch.py - MODULO 19: TRANSFORMER DESDE CERO
# ===========================================================================
import numpy as np, math, warnings
warnings.filterwarnings('ignore')
try:
    import torch, torch.nn as nn, torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset
    HAS = True
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
except ImportError:
    HAS = False

# =====================================================================
#   PARTE 1: SCALED DOT-PRODUCT ATTENTION
# =====================================================================
print("\n" + "="*80)
print("=== CAPITULO 1: ATTENTION ===")
print("="*80)

"""
Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V

Q: (batch, seq_q, d_k)
K: (batch, seq_k, d_k)
V: (batch, seq_k, d_v)
Output: (batch, seq_q, d_v)
"""

if HAS:
    def attention(Q, K, V, mask=None):
        d_k = Q.size(-1)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn_weights = F.softmax(scores, dim=-1)
        return torch.matmul(attn_weights, V), attn_weights

    Q = torch.randn(2, 5, 64)
    K = torch.randn(2, 5, 64)
    V = torch.randn(2, 5, 64)
    out, w = attention(Q, K, V)
    print(f"  Attention: Q{list(Q.shape)} -> out{list(out.shape)}")
    print(f"  Weights sum: {w.sum(-1)[0,0]:.4f}")

# =====================================================================
#   PARTE 2: MULTI-HEAD ATTENTION FROM SCRATCH
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 2: MULTI-HEAD ===")
print("="*80)

if HAS:
    class MultiHeadAttention(nn.Module):
        def __init__(self, d_model, n_heads):
            super().__init__()
            assert d_model % n_heads == 0
            self.d_model = d_model
            self.n_heads = n_heads
            self.d_k = d_model // n_heads
            self.W_q = nn.Linear(d_model, d_model)
            self.W_k = nn.Linear(d_model, d_model)
            self.W_v = nn.Linear(d_model, d_model)
            self.W_o = nn.Linear(d_model, d_model)

        def forward(self, q, k, v, mask=None):
            B = q.size(0)
            Q = self.W_q(q).view(B, -1, self.n_heads, self.d_k).transpose(1, 2)
            K = self.W_k(k).view(B, -1, self.n_heads, self.d_k).transpose(1, 2)
            V = self.W_v(v).view(B, -1, self.n_heads, self.d_k).transpose(1, 2)
            if mask is not None:
                mask = mask.unsqueeze(1)
            out, _ = attention(Q, K, V, mask)
            out = out.transpose(1, 2).contiguous().view(B, -1, self.d_model)
            return self.W_o(out)

    mha = MultiHeadAttention(64, 8)
    x = torch.randn(2, 10, 64)
    print(f"  MHA: {list(x.shape)} -> {list(mha(x, x, x).shape)}")
    print(f"  Params: {sum(p.numel() for p in mha.parameters()):,}")

# =====================================================================
#   PARTE 3: POSITIONAL ENCODING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 3: POSITIONAL ENCODING ===")
print("="*80)

if HAS:
    class PositionalEncoding(nn.Module):
        def __init__(self, d_model, max_len=5000, dropout=0.1):
            super().__init__()
            self.dropout = nn.Dropout(dropout)
            pe = torch.zeros(max_len, d_model)
            pos = torch.arange(0, max_len).unsqueeze(1).float()
            div = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
            pe[:, 0::2] = torch.sin(pos * div)
            pe[:, 1::2] = torch.cos(pos * div)
            self.register_buffer('pe', pe.unsqueeze(0))

        def forward(self, x):
            return self.dropout(x + self.pe[:, :x.size(1)])

    pe = PositionalEncoding(64)
    x = torch.randn(2, 20, 64)
    print(f"  PE: {list(x.shape)} -> {list(pe(x).shape)}")

# =====================================================================
#   PARTE 4: FEED-FORWARD NETWORK
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 4: FFN ===")
print("="*80)

"""
FFN(x) = ReLU(x @ W1 + b1) @ W2 + b2
Typically d_ff = 4 * d_model.
"""

if HAS:
    class FeedForward(nn.Module):
        def __init__(self, d_model, d_ff, dropout=0.1):
            super().__init__()
            self.linear1 = nn.Linear(d_model, d_ff)
            self.linear2 = nn.Linear(d_ff, d_model)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x):
            return self.linear2(self.dropout(F.gelu(self.linear1(x))))

    ffn = FeedForward(64, 256)
    print(f"  FFN: {list(x.shape)} -> {list(ffn(x).shape)}")

# =====================================================================
#   PARTE 5: ENCODER LAYER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 5: ENCODER LAYER ===")
print("="*80)

if HAS:
    class EncoderLayer(nn.Module):
        def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
            super().__init__()
            self.self_attn = MultiHeadAttention(d_model, n_heads)
            self.ffn = FeedForward(d_model, d_ff, dropout)
            self.norm1 = nn.LayerNorm(d_model)
            self.norm2 = nn.LayerNorm(d_model)
            self.drop1 = nn.Dropout(dropout)
            self.drop2 = nn.Dropout(dropout)

        def forward(self, x, mask=None):
            attn = self.self_attn(x, x, x, mask)
            x = self.norm1(x + self.drop1(attn))
            ff = self.ffn(x)
            x = self.norm2(x + self.drop2(ff))
            return x

    enc_layer = EncoderLayer(64, 8, 256)
    print(f"  EncoderLayer: {list(x.shape)} -> {list(enc_layer(x).shape)}")

# =====================================================================
#   PARTE 6: DECODER LAYER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 6: DECODER LAYER ===")
print("="*80)

if HAS:
    class DecoderLayer(nn.Module):
        def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
            super().__init__()
            self.self_attn = MultiHeadAttention(d_model, n_heads)
            self.cross_attn = MultiHeadAttention(d_model, n_heads)
            self.ffn = FeedForward(d_model, d_ff, dropout)
            self.norm1 = nn.LayerNorm(d_model)
            self.norm2 = nn.LayerNorm(d_model)
            self.norm3 = nn.LayerNorm(d_model)
            self.drop1 = nn.Dropout(dropout)
            self.drop2 = nn.Dropout(dropout)
            self.drop3 = nn.Dropout(dropout)

        def forward(self, x, memory, src_mask=None, tgt_mask=None):
            attn1 = self.self_attn(x, x, x, tgt_mask)
            x = self.norm1(x + self.drop1(attn1))
            attn2 = self.cross_attn(x, memory, memory, src_mask)
            x = self.norm2(x + self.drop2(attn2))
            ff = self.ffn(x)
            x = self.norm3(x + self.drop3(ff))
            return x

    dec_layer = DecoderLayer(64, 8, 256)
    mem = torch.randn(2, 20, 64)
    tgt = torch.randn(2, 15, 64)
    print(f"  DecoderLayer: tgt{list(tgt.shape)}, mem{list(mem.shape)} -> {list(dec_layer(tgt, mem).shape)}")

# =====================================================================
#   PARTE 7: FULL ENCODER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 7: ENCODER ===")
print("="*80)

if HAS:
    class Encoder(nn.Module):
        def __init__(self, d_model, n_heads, d_ff, n_layers, dropout=0.1):
            super().__init__()
            self.layers = nn.ModuleList([
                EncoderLayer(d_model, n_heads, d_ff, dropout)
                for _ in range(n_layers)])
            self.norm = nn.LayerNorm(d_model)

        def forward(self, x, mask=None):
            for layer in self.layers:
                x = layer(x, mask)
            return self.norm(x)

    encoder = Encoder(64, 8, 256, 6)
    out = encoder(torch.randn(2, 20, 64))
    print(f"  Encoder(6 layers): -> {list(out.shape)}")
    print(f"  Params: {sum(p.numel() for p in encoder.parameters()):,}")

# =====================================================================
#   PARTE 8: FULL DECODER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 8: DECODER ===")
print("="*80)

if HAS:
    class Decoder(nn.Module):
        def __init__(self, d_model, n_heads, d_ff, n_layers, dropout=0.1):
            super().__init__()
            self.layers = nn.ModuleList([
                DecoderLayer(d_model, n_heads, d_ff, dropout)
                for _ in range(n_layers)])
            self.norm = nn.LayerNorm(d_model)

        def forward(self, x, memory, src_mask=None, tgt_mask=None):
            for layer in self.layers:
                x = layer(x, memory, src_mask, tgt_mask)
            return self.norm(x)

    decoder = Decoder(64, 8, 256, 6)
    mem = torch.randn(2, 20, 64)
    tgt = torch.randn(2, 15, 64)
    out = decoder(tgt, mem)
    print(f"  Decoder(6 layers): -> {list(out.shape)}")

# =====================================================================
#   PARTE 9: CAUSAL MASK
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 9: CAUSAL MASK ===")
print("="*80)

if HAS:
    def causal_mask(size):
        mask = torch.triu(torch.ones(size, size), diagonal=1) == 0
        return mask

    m = causal_mask(5)
    print(f"  Causal mask 5x5:")
    for row in m.int():
        print(f"    {row.tolist()}")

# =====================================================================
#   PARTE 10: FULL TRANSFORMER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 10: FULL TRANSFORMER ===")
print("="*80)

if HAS:
    class Transformer(nn.Module):
        def __init__(self, src_vocab, tgt_vocab, d_model=64, n_heads=8,
                     d_ff=256, n_layers=4, dropout=0.1, max_len=200):
            super().__init__()
            self.src_emb = nn.Embedding(src_vocab, d_model)
            self.tgt_emb = nn.Embedding(tgt_vocab, d_model)
            self.pos_enc = PositionalEncoding(d_model, max_len, dropout)
            self.encoder = Encoder(d_model, n_heads, d_ff, n_layers, dropout)
            self.decoder = Decoder(d_model, n_heads, d_ff, n_layers, dropout)
            self.output_proj = nn.Linear(d_model, tgt_vocab)
            self.d_model = d_model

        def forward(self, src, tgt, src_mask=None, tgt_mask=None):
            src_e = self.pos_enc(self.src_emb(src) * math.sqrt(self.d_model))
            tgt_e = self.pos_enc(self.tgt_emb(tgt) * math.sqrt(self.d_model))
            memory = self.encoder(src_e, src_mask)
            dec_out = self.decoder(tgt_e, memory, src_mask, tgt_mask)
            return self.output_proj(dec_out)

    model = Transformer(src_vocab=1000, tgt_vocab=1000, d_model=64,
                         n_heads=8, d_ff=256, n_layers=4)
    src = torch.randint(0, 1000, (2, 20))
    tgt = torch.randint(0, 1000, (2, 15))
    tgt_mask = causal_mask(15)
    out = model(src, tgt, tgt_mask=tgt_mask)
    print(f"  Transformer: src{list(src.shape)}, tgt{list(tgt.shape)} -> {list(out.shape)}")
    total = sum(p.numel() for p in model.parameters())
    print(f"  Total params: {total:,}")

# =====================================================================
#   PARTE 11: TRAINING THE TRANSFORMER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 11: TRAINING ===")
print("="*80)

if HAS:
    torch.manual_seed(42)
    # Toy task: copy sequence (shifted by 1)
    vocab_size = 50
    seq_len = 10
    n_samples = 500

    src_data = torch.randint(2, vocab_size, (n_samples, seq_len))
    tgt_input = torch.cat([torch.ones(n_samples, 1).long(), src_data[:, :-1]], dim=1)
    tgt_output = src_data

    train_dl = DataLoader(TensorDataset(src_data[:400], tgt_input[:400], tgt_output[:400]),
                           batch_size=32, shuffle=True)

    model = Transformer(vocab_size, vocab_size, d_model=32, n_heads=4, d_ff=128, n_layers=2)
    model.to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(20):
        model.train()
        total_loss = 0
        for s, ti, to in train_dl:
            s, ti, to = s.to(DEVICE), ti.to(DEVICE), to.to(DEVICE)
            mask = causal_mask(ti.size(1)).to(DEVICE)
            opt.zero_grad()
            out = model(s, ti, tgt_mask=mask)
            loss = criterion(out.view(-1, vocab_size), to.view(-1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            total_loss += loss.item()
        if epoch % 5 == 0:
            print(f"    epoch {epoch:2d}: loss={total_loss/len(train_dl):.4f}")

# =====================================================================
#   PARTE 12: INFERENCE (AUTOREGRESSIVE)
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 12: INFERENCE ===")
print("="*80)

if HAS:
    def greedy_decode(model, src, max_len, start_token=1):
        model.eval()
        src = src.to(DEVICE)
        with torch.no_grad():
            memory = model.encoder(model.pos_enc(
                model.src_emb(src) * math.sqrt(model.d_model)))
        
        ys = torch.tensor([[start_token]]).to(DEVICE)
        for _ in range(max_len - 1):
            mask = causal_mask(ys.size(1)).to(DEVICE)
            with torch.no_grad():
                tgt_e = model.pos_enc(model.tgt_emb(ys) * math.sqrt(model.d_model))
                dec_out = model.decoder(tgt_e, memory, tgt_mask=mask)
                logits = model.output_proj(dec_out[:, -1])
                next_token = logits.argmax(-1, keepdim=True)
            ys = torch.cat([ys, next_token], dim=1)
        return ys

    test_src = src_data[450:451]
    decoded = greedy_decode(model, test_src, seq_len)
    print(f"  Source:  {test_src[0].tolist()}")
    print(f"  Decoded: {decoded[0].tolist()}")

# =====================================================================
#   PARTE 13: LABEL SMOOTHING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 13: LABEL SMOOTHING ===")
print("="*80)

"""
Label smoothing: soft targets instead of hard.
  Hard: [0, 0, 1, 0]
  Smooth(eps=0.1): [0.033, 0.033, 0.9, 0.033]
Prevents overconfidence, improves generalization.
"""

if HAS:
    class LabelSmoothingLoss(nn.Module):
        def __init__(self, n_classes, smoothing=0.1):
            super().__init__()
            self.smoothing = smoothing
            self.n_classes = n_classes
            self.confidence = 1.0 - smoothing

        def forward(self, pred, target):
            pred = pred.log_softmax(dim=-1)
            true_dist = torch.zeros_like(pred)
            true_dist.fill_(self.smoothing / (self.n_classes - 1))
            true_dist.scatter_(1, target.unsqueeze(1), self.confidence)
            return torch.mean(torch.sum(-true_dist * pred, dim=-1))

    ls = LabelSmoothingLoss(10, 0.1)
    pred = torch.randn(4, 10)
    target = torch.tensor([0, 3, 5, 7])
    print(f"  CE loss: {nn.CrossEntropyLoss()(pred, target):.4f}")
    print(f"  LS loss: {ls(pred, target):.4f}")

# =====================================================================
#   PARTE 14: WARMUP SCHEDULER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 14: WARMUP ===")
print("="*80)

"""
Warmup: gradually increase LR then decay.
  lr = d_model^(-0.5) * min(step^(-0.5), step * warmup^(-1.5))
"""

if HAS:
    class WarmupScheduler:
        def __init__(self, optimizer, d_model, warmup_steps=4000):
            self.opt = optimizer
            self.d_model = d_model
            self.warmup = warmup_steps
            self.step_num = 0

        def step(self):
            self.step_num += 1
            lr = self.d_model**(-0.5) * min(
                self.step_num**(-0.5), self.step_num * self.warmup**(-1.5))
            for p in self.opt.param_groups:
                p['lr'] = lr
            return lr

    dummy_opt = torch.optim.Adam(model.parameters(), lr=0)
    ws = WarmupScheduler(dummy_opt, 64, 400)
    lrs = [ws.step() for _ in range(1000)]
    print(f"  LR at step 1:    {lrs[0]:.6f}")
    print(f"  LR at step 400:  {lrs[399]:.6f} (peak)")
    print(f"  LR at step 1000: {lrs[999]:.6f}")

# =====================================================================
#   PARTE 15: PRE-NORM vs POST-NORM
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 15: PRE vs POST NORM ===")
print("="*80)

"""
POST-NORM (original): x + Sublayer(LayerNorm(x))  -- harder to train deep
PRE-NORM (modern):     LayerNorm(x + Sublayer(x))  -- more stable training

GPT-2, LLaMA use Pre-Norm. Original paper uses Post-Norm.
"""

if HAS:
    class PreNormEncoderLayer(nn.Module):
        def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
            super().__init__()
            self.attn = MultiHeadAttention(d_model, n_heads)
            self.ffn = FeedForward(d_model, d_ff, dropout)
            self.norm1 = nn.LayerNorm(d_model)
            self.norm2 = nn.LayerNorm(d_model)

        def forward(self, x, mask=None):
            x = x + self.attn(self.norm1(x), self.norm1(x), self.norm1(x), mask)
            x = x + self.ffn(self.norm2(x))
            return x

    pn = PreNormEncoderLayer(64, 8, 256)
    print(f"  Pre-Norm: {list(pn(torch.randn(2,10,64)).shape)}")

# =====================================================================
#   PARTE 16: BEAM SEARCH
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 16: BEAM SEARCH ===")
print("="*80)

"""
Beam search: keep top-k candidates at each step.
  beam_width=1: greedy decoding.
  beam_width=5: explore 5 paths, pick best.
  
  Better quality than greedy, but slower.
"""

print("  Decoding strategies:")
strategies = [
    ("Greedy", "Pick argmax", "Fast, suboptimal"),
    ("Beam(k=5)", "Top-5 candidates", "Better, k× slower"),
    ("Sampling", "Sample from dist", "Diverse outputs"),
    ("Top-k", "Sample from top-k", "Controlled diversity"),
    ("Top-p", "Sample from nucleus", "Dynamic threshold"),
    ("Temperature", "Scale logits", "Controls randomness"),
]
for s, d, n in strategies:
    print(f"    {s:>12s}: {d:>20s} | {n}")

# =====================================================================
#   PARTE 17: KV-CACHE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 17: KV-CACHE ===")
print("="*80)

"""
KV-Cache: cache Key/Value for past tokens during autoregressive generation.
Without: recompute K,V for ALL tokens at each step -> O(n²) per token.
With: only compute K,V for new token, concat with cache -> O(n) per token.
Critical for fast LLM inference.
"""

print("  KV-Cache speedup:")
print("    Without: step t computes attention over all t tokens")
print("    With: step t only computes new K,V, reuses cached")
print("    Speedup: O(n) vs O(n²) per generation step")

# =====================================================================
#   PARTE 18: ROTARY POSITIONAL EMBEDDING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 18: RoPE ===")
print("="*80)

"""
RoPE (Rotary Position Embedding):
  Encode position by rotating Q,K vectors.
  Relative position info via inner product.
  Used in: LLaMA, GPT-NeoX, PaLM.
  Advantage: extrapolates to longer sequences.
"""

if HAS:
    def rotary_embedding(x, seq_len):
        d = x.shape[-1]
        theta = 1.0 / (10000 ** (torch.arange(0, d, 2).float() / d))
        pos = torch.arange(seq_len).float()
        angles = torch.einsum('i,j->ij', pos, theta)
        cos_a = angles.cos().unsqueeze(0).unsqueeze(0)
        sin_a = angles.sin().unsqueeze(0).unsqueeze(0)
        x1, x2 = x[..., ::2], x[..., 1::2]
        rotated = torch.cat([x1*cos_a - x2*sin_a, x1*sin_a + x2*cos_a], dim=-1)
        return rotated

    x = torch.randn(1, 1, 10, 64)
    print(f"  RoPE: {list(x.shape)} -> {list(rotary_embedding(x, 10).shape)}")

# =====================================================================
#   PARTE 19: GROUPED QUERY ATTENTION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 19: GQA ===")
print("="*80)

"""
GQA (Grouped Query Attention):
  MHA: each head has own Q, K, V projections.
  MQA: all heads share K, V (saves memory).
  GQA: groups of heads share K, V (middle ground).
  
  LLaMA 2 uses GQA. Reduces KV-cache memory.
"""

print("  Attention variants:")
print("    MHA: n_heads Q, n_heads K, n_heads V")
print("    MQA: n_heads Q, 1 K, 1 V")
print("    GQA: n_heads Q, n_groups K, n_groups V")

# =====================================================================
#   PARTE 20: SUMMARY
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 20: SUMMARY ===")
print("="*80)

"""
TRANSFORMER FROM SCRATCH:
1. Scaled dot-product attention: Q@K^T/sqrt(d) -> softmax -> @V
2. Multi-head: parallel heads, concat, project
3. Positional encoding: sin/cos or learned or RoPE
4. Encoder: self-attn + FFN + residual + LayerNorm
5. Decoder: masked self-attn + cross-attn + FFN
6. Full model: Embedding + PE + Encoder + Decoder + Output
7. Training: label smoothing, warmup, gradient clipping
8. Inference: greedy, beam search, sampling
9. Modern: Pre-Norm, KV-cache, RoPE, GQA, Flash Attention
"""

components = [
    ("Attention", "Core mechanism"),
    ("Multi-Head", "Parallel attention"),
    ("Positional", "Position info"),
    ("Encoder", "Self-attn + FFN"),
    ("Decoder", "Masked + cross-attn"),
    ("Full Model", "End-to-end"),
    ("Training", "Smoothing + warmup"),
    ("Inference", "Autoregressive"),
    ("Modern", "RoPE + GQA + KV-cache"),
]

print(f"\n  {'Component':>14s} {'Role':>20s}")
for c, r in components:
    print(f"  {c:>14s} {r:>20s}")


# =====================================================================
#   PARTE 21: SwiGLU FFN
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 21: SwiGLU ===")
print("="*80)

"""
SwiGLU: modern FFN used in LLaMA, PaLM.
  SwiGLU(x) = (x @ W1 * SiLU(x @ W_gate)) @ W2
  Better than ReLU FFN at same param count.
"""

if HAS:
    class SwiGLU(nn.Module):
        def __init__(self, d_model, d_ff):
            super().__init__()
            self.w1 = nn.Linear(d_model, d_ff, bias=False)
            self.w2 = nn.Linear(d_ff, d_model, bias=False)
            self.w_gate = nn.Linear(d_model, d_ff, bias=False)

        def forward(self, x):
            return self.w2(F.silu(self.w_gate(x)) * self.w1(x))

    swiglu = SwiGLU(64, 256)
    x = torch.randn(2, 10, 64)
    print(f"  SwiGLU: {list(x.shape)} -> {list(swiglu(x).shape)}")
    print(f"  Params: {sum(p.numel() for p in swiglu.parameters()):,}")


# =====================================================================
#   PARTE 22: RMSNORM
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 22: RMSNORM ===")
print("="*80)

"""
RMSNorm: simpler than LayerNorm.
  No mean subtraction, just scale by RMS.
  Used in LLaMA, GPT-NeoX. Slightly faster.
"""

if HAS:
    class RMSNorm(nn.Module):
        def __init__(self, d_model, eps=1e-6):
            super().__init__()
            self.weight = nn.Parameter(torch.ones(d_model))
            self.eps = eps

        def forward(self, x):
            rms = torch.sqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
            return x / rms * self.weight

    rn = RMSNorm(64)
    x = torch.randn(2, 10, 64)
    print(f"  RMSNorm: {list(rn(x).shape)}")


# =====================================================================
#   PARTE 23: SAMPLING STRATEGIES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 23: SAMPLING ===")
print("="*80)

if HAS:
    def sample_with_temperature(logits, temperature=1.0):
        scaled = logits / temperature
        probs = F.softmax(scaled, dim=-1)
        return torch.multinomial(probs, 1)

    def top_k_sampling(logits, k=10):
        vals, idx = logits.topk(k)
        probs = F.softmax(vals, dim=-1)
        sampled = torch.multinomial(probs, 1)
        return idx.gather(-1, sampled)

    def top_p_sampling(logits, p=0.9):
        sorted_logits, sorted_idx = logits.sort(descending=True)
        probs = F.softmax(sorted_logits, dim=-1)
        cumsum = probs.cumsum(dim=-1)
        mask = cumsum - probs > p
        sorted_logits[mask] = -float('inf')
        probs = F.softmax(sorted_logits, dim=-1)
        sampled = torch.multinomial(probs, 1)
        return sorted_idx.gather(-1, sampled)

    logits = torch.randn(1, 50)
    print(f"  Temperature=0.5: {sample_with_temperature(logits, 0.5).item()}")
    print(f"  Temperature=1.0: {sample_with_temperature(logits, 1.0).item()}")
    print(f"  Top-k=10: {top_k_sampling(logits, 10).item()}")
    print(f"  Top-p=0.9: {top_p_sampling(logits, 0.9).item()}")


# =====================================================================
#   PARTE 24: GPT-STYLE (DECODER-ONLY)
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 24: GPT-STYLE ===")
print("="*80)

"""
GPT: decoder-only transformer.
  No encoder, no cross-attention.
  Causal self-attention only.
  Used for: text generation, code, reasoning.
"""

if HAS:
    class GPTBlock(nn.Module):
        def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
            super().__init__()
            self.norm1 = nn.LayerNorm(d_model)
            self.attn = MultiHeadAttention(d_model, n_heads)
            self.norm2 = nn.LayerNorm(d_model)
            self.ffn = FeedForward(d_model, d_ff, dropout)

        def forward(self, x, mask=None):
            x = x + self.attn(self.norm1(x), self.norm1(x), self.norm1(x), mask)
            x = x + self.ffn(self.norm2(x))
            return x

    class MiniGPT(nn.Module):
        def __init__(self, vocab, d_model, n_heads, d_ff, n_layers, max_len=512):
            super().__init__()
            self.emb = nn.Embedding(vocab, d_model)
            self.pos = nn.Embedding(max_len, d_model)
            self.blocks = nn.ModuleList([
                GPTBlock(d_model, n_heads, d_ff) for _ in range(n_layers)])
            self.norm = nn.LayerNorm(d_model)
            self.head = nn.Linear(d_model, vocab, bias=False)

        def forward(self, x):
            B, T = x.shape
            pos_ids = torch.arange(T, device=x.device).unsqueeze(0)
            h = self.emb(x) + self.pos(pos_ids)
            mask = causal_mask(T).to(x.device)
            for block in self.blocks:
                h = block(h, mask)
            return self.head(self.norm(h))

    gpt = MiniGPT(1000, 64, 8, 256, 4)
    tokens = torch.randint(0, 1000, (2, 20))
    print(f"  MiniGPT: {list(tokens.shape)} -> {list(gpt(tokens).shape)}")
    print(f"  Params: {sum(p.numel() for p in gpt.parameters()):,}")


# =====================================================================
#   PARTE 25: BERT-STYLE (ENCODER-ONLY)
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 25: BERT-STYLE ===")
print("="*80)

"""
BERT: encoder-only, bidirectional.
  No causal mask -> sees full context.
  Pre-training: MLM (masked language model) + NSP.
  Fine-tuning: classification, NER, QA.
"""

if HAS:
    class MiniBERT(nn.Module):
        def __init__(self, vocab, d_model, n_heads, d_ff, n_layers, max_len=512):
            super().__init__()
            self.emb = nn.Embedding(vocab, d_model)
            self.pos = nn.Embedding(max_len, d_model)
            self.encoder = Encoder(d_model, n_heads, d_ff, n_layers)
            self.mlm_head = nn.Linear(d_model, vocab)

        def forward(self, x):
            B, T = x.shape
            pos_ids = torch.arange(T, device=x.device).unsqueeze(0)
            h = self.emb(x) + self.pos(pos_ids)
            h = self.encoder(h)
            return self.mlm_head(h)

    bert = MiniBERT(1000, 64, 8, 256, 4)
    tokens = torch.randint(0, 1000, (2, 20))
    print(f"  MiniBERT: {list(tokens.shape)} -> {list(bert(tokens).shape)}")


# =====================================================================
#   PARTE 26: ARCHITECTURE COMPARISON
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 26: ARCHITECTURES ===")
print("="*80)

archs = [
    ("", "Encoder-only", "Decoder-only", "Enc-Dec"),
    ("Model", "BERT", "GPT", "T5/BART"),
    ("Masking", "None (bidir)", "Causal", "Mixed"),
    ("Pre-train", "MLM", "Next token", "Span corrupt"),
    ("Best for", "Understanding", "Generation", "Seq2Seq"),
]

for row in archs:
    print(f"  {row[0]:>10s} {row[1]:>14s} {row[2]:>14s} {row[3]:>14s}")


# =====================================================================
#   PARTE 27: TOKENIZATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 27: TOKENIZATION ===")
print("="*80)

"""
Tokenization converts text to token IDs.
  Word-level: simple but huge vocab, OOV problem.
  Character-level: small vocab but long sequences.
  Subword (BPE/WordPiece/SentencePiece): best balance.

BPE: iteratively merge most frequent byte pairs.
  "lowest" -> ["low", "est"] or ["l", "ow", "est"]
"""

print("  Tokenization methods:")
methods = [
    ("Word-level", "Simple, OOV issues", "50k+ vocab"),
    ("Char-level", "No OOV, long seq", "~256 vocab"),
    ("BPE", "Balanced, standard", "30k-50k vocab"),
    ("WordPiece", "BERT's tokenizer", "30k vocab"),
    ("SentencePiece", "Language agnostic", "Configurable"),
]
for m, d, v in methods:
    print(f"    {m:>14s}: {d:>22s} | {v}")


# =====================================================================
#   PARTE 28: MIXED PRECISION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 28: MIXED PRECISION ===")
print("="*80)

"""
Mixed precision: use fp16/bf16 for most ops, fp32 for critical.
  torch.cuda.amp.autocast: auto mixed precision.
  GradScaler: prevent underflow in fp16 gradients.
  ~2x speedup, ~50% less memory.
"""

print("  Mixed precision training:")
print("    autocast: forward pass in fp16")
print("    GradScaler: scale loss to prevent underflow")
print("    Master weights: keep fp32 copy for updates")


# =====================================================================
#   PARTE 29: PRODUCTION CHECKLIST
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 29: PRODUCTION ===")
print("="*80)

checklist = [
    "1. Tokenizer consistency (train/inference)",
    "2. KV-cache for fast generation",
    "3. Batch inference with padding/masking",
    "4. Quantization (int8/int4) for deployment",
    "5. ONNX export for cross-platform",
    "6. Streaming output (token by token)",
    "7. Max length handling (truncation)",
    "8. Temperature/top-p for quality control",
    "9. Monitoring: latency, throughput, memory",
    "10. Safety: input validation, output filtering",
]

for item in checklist:
    print(f"    {item}")


# =====================================================================
#   PARTE 30: TRANSFORMER EVOLUTION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 30: EVOLUTION ===")
print("="*80)

"""
2017: Transformer (Vaswani) - Attention Is All You Need
2018: BERT (Google) - Bidirectional encoder
2018: GPT-1 (OpenAI) - Generative decoder
2019: GPT-2 - Scaled up, Pre-Norm
2020: GPT-3 - 175B, in-context learning
2021: Codex - Code generation
2022: InstructGPT/ChatGPT - RLHF alignment
2023: LLaMA - Open weights, RoPE+GQA+SwiGLU+RMSNorm
2023: GPT-4 - Multimodal, MoE
2024: Gemini, Claude, Llama 3 - Competition era
"""

print("  Key innovations per generation:")
innovations = [
    ("Original", "Self-attention, PE, Enc-Dec"),
    ("BERT era", "Pre-training + fine-tuning"),
    ("GPT era", "Scale + emergent abilities"),
    ("Modern", "RoPE, GQA, SwiGLU, RMSNorm"),
    ("Alignment", "RLHF, DPO, Constitutional AI"),
]

for era, innov in innovations:
    print(f"    {era:>10s}: {innov}")


# =====================================================================
#   PARTE 31: ATTENTION COMPLEXITY
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 31: COMPLEXITY ===")
print("="*80)

"""
Standard attention: O(n² * d) time, O(n²) memory.
For n=4096, d=128: ~2 billion FLOPs per layer.

Efficient variants:
  Flash Attention: O(n²*d) but IO-aware -> 2-4x faster.
  Linear attention: O(n*d²) -> good for very long sequences.
  Sparse attention: O(n*sqrt(n)) -> Longformer, BigBird.
  Ring attention: distributed across devices.
"""

if HAS:
    seq_lengths = [128, 512, 2048, 8192, 32768]
    d = 128
    print(f"  {'Seq Len':>8s} {'Self-Attn FLOPs':>16s} {'Memory (MB)':>12s}")
    for n in seq_lengths:
        flops = 2 * n * n * d  # Q@K^T + Attn@V
        mem_mb = n * n * 4 / 1e6  # float32 attention matrix
        print(f"  {n:8d} {flops:16,} {mem_mb:12.1f}")


# =====================================================================
#   PARTE 32: LLAMA RECIPE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 32: LLAMA RECIPE ===")
print("="*80)

"""
LLaMA architecture (Meta, 2023):
  1. Pre-Norm with RMSNorm (not LayerNorm).
  2. SwiGLU activation (not ReLU/GELU).
  3. RoPE (Rotary Position Embedding).
  4. GQA (Grouped Query Attention) in LLaMA 2.
  5. No bias in linear layers.
  6. Decoder-only (causal).

Sizes:
  LLaMA 7B:  d=4096, layers=32, heads=32
  LLaMA 13B: d=5120, layers=40, heads=40
  LLaMA 70B: d=8192, layers=80, heads=64, GQA groups=8
"""

if HAS:
    class LLaMABlock(nn.Module):
        def __init__(self, d_model, n_heads, d_ff):
            super().__init__()
            self.norm1 = RMSNorm(d_model)
            self.attn = MultiHeadAttention(d_model, n_heads)
            self.norm2 = RMSNorm(d_model)
            self.ffn = SwiGLU(d_model, d_ff)

        def forward(self, x, mask=None):
            h = self.norm1(x)
            x = x + self.attn(h, h, h, mask)
            x = x + self.ffn(self.norm2(x))
            return x

    llama_block = LLaMABlock(64, 8, 256)
    x = torch.randn(2, 10, 64)
    out = llama_block(x)
    print(f"  LLaMA block: {list(x.shape)} -> {list(out.shape)}")
    print(f"  Components: RMSNorm + MHA + SwiGLU")
    print(f"  Params: {sum(p.numel() for p in llama_block.parameters()):,}")

    llama_sizes = [
        ("7B", 4096, 32, 32, "11008"),
        ("13B", 5120, 40, 40, "13824"),
        ("70B", 8192, 80, 64, "28672"),
    ]
    print(f"\n  {'Size':>5s} {'d_model':>8s} {'layers':>7s} {'heads':>6s} {'d_ff':>7s}")
    for name, d, l, h, ff in llama_sizes:
        print(f"  {name:>5s} {d:8d} {l:7d} {h:6d} {ff:>7s}")

print("\n" + "="*80)
print("=== CONCLUSION ===")
print("="*80)
print("\n FIN DE ARCHIVO 01_transformer_scratch.")
print(" Transformer implementado desde cero.")
