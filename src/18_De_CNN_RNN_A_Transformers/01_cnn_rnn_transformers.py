# ===========================================================================
# 01_cnn_rnn_transformers.py - MODULO 18: CNN, RNN, TRANSFORMERS
# ===========================================================================
import numpy as np, warnings
warnings.filterwarnings('ignore')
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset
    HAS = True
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
except ImportError:
    HAS = False

# =====================================================================
#   PARTE 1: CONVOLUTION FUNDAMENTALS
# =====================================================================
print("\n" + "="*80)
print("=== CAPITULO 1: CONVOLUTION ===")
print("="*80)

"""
CONVOLUTION: operacion que aplica un KERNEL (filtro) sobre datos.
  - Detecta patrones locales (edges, textures, shapes).
  - Translation invariant: mismo patron en cualquier posicion.
  - Parameter sharing: mismo kernel en toda la imagen.

Conv2d(in_channels, out_channels, kernel_size, stride, padding):
  - in_channels: RGB=3, grayscale=1.
  - out_channels: num filtros (feature maps).
  - kernel_size: tamaño del filtro (3x3, 5x5).
  - stride: salto del filtro.
  - padding: bordes.

Output size: (W - K + 2P) / S + 1
"""

if HAS:
    # 1D convolution (for sequences/time series)
    conv1d = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
    x_1d = torch.randn(4, 1, 100)  # batch=4, channels=1, length=100
    out_1d = conv1d(x_1d)
    print(f"  Conv1d: {x_1d.shape} -> {out_1d.shape}")
    
    # 2D convolution (for images)
    conv2d = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1)
    x_2d = torch.randn(4, 3, 28, 28)  # batch=4, RGB, 28x28
    out_2d = conv2d(x_2d)
    print(f"  Conv2d: {x_2d.shape} -> {out_2d.shape}")
    
    print(f"  Conv2d params: {sum(p.numel() for p in conv2d.parameters())}")

# =====================================================================
#   PARTE 2: POOLING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 2: POOLING ===")
print("="*80)

"""
Pooling: reduce spatial dimensions.
  MaxPool2d: max value in window (preserves strong features).
  AvgPool2d: average value (smoother).
  AdaptiveAvgPool2d: output fixed size regardless of input.
"""

if HAS:
    x = torch.randn(1, 1, 8, 8)
    
    maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
    avgpool = nn.AvgPool2d(kernel_size=2, stride=2)
    adaptive = nn.AdaptiveAvgPool2d((1, 1))
    
    print(f"  Input: {x.shape}")
    print(f"  MaxPool2d(2): {maxpool(x).shape}")
    print(f"  AvgPool2d(2): {avgpool(x).shape}")
    print(f"  AdaptiveAvg(1,1): {adaptive(x).shape}")

# =====================================================================
#   PARTE 3: CNN ARCHITECTURE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 3: CNN ARCHITECTURE ===")
print("="*80)

if HAS:
    class CNN(nn.Module):
        def __init__(self, num_classes=10):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.BatchNorm2d(32),
                nn.MaxPool2d(2),
                nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.BatchNorm2d(64),
                nn.MaxPool2d(2),
                nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.BatchNorm2d(128),
                nn.AdaptiveAvgPool2d((1, 1)),
            )
            self.classifier = nn.Sequential(
                nn.Flatten(),
                nn.Linear(128, 64), nn.ReLU(), nn.Dropout(0.3),
                nn.Linear(64, num_classes),
            )
        
        def forward(self, x):
            x = self.features(x)
            return self.classifier(x)
    
    cnn = CNN(10)
    x_img = torch.randn(4, 1, 28, 28)
    out = cnn(x_img)
    print(f"  CNN: {x_img.shape} -> {out.shape}")
    print(f"  Params: {sum(p.numel() for p in cnn.parameters()):,}")

# =====================================================================
#   PARTE 4: CNN TRAINING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 4: CNN TRAINING ===")
print("="*80)

if HAS:
    torch.manual_seed(42)
    X_fake = torch.randn(500, 1, 28, 28)
    y_fake = torch.randint(0, 10, (500,))
    
    train_dl = DataLoader(TensorDataset(X_fake[:400], y_fake[:400]), batch_size=32, shuffle=True)
    test_dl = DataLoader(TensorDataset(X_fake[400:], y_fake[400:]), batch_size=32)
    
    cnn = CNN(10).to(DEVICE)
    opt = torch.optim.Adam(cnn.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(10):
        cnn.train()
        total_loss = 0
        for xb, yb in train_dl:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            opt.zero_grad()
            loss = criterion(cnn(xb), yb)
            loss.backward()
            opt.step()
            total_loss += loss.item()
        if epoch % 3 == 0:
            print(f"    epoch {epoch}: loss={total_loss/len(train_dl):.4f}")

# =====================================================================
#   PARTE 5: FAMOUS CNN ARCHITECTURES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 5: ARCHITECTURES ===")
print("="*80)

"""
FAMOUS CNNs:
  LeNet (1998): 5 layers. First practical CNN.
  AlexNet (2012): 8 layers. GPU training. ImageNet winner.
  VGG (2014): 16-19 layers. 3x3 convs only. Simple but deep.
  GoogLeNet (2014): Inception modules. 22 layers. 1x1 convs.
  ResNet (2015): Skip connections. 50-152 layers. REVOLUTIONARY.
  EfficientNet (2019): NAS-optimized. Compound scaling.
  ConvNeXt (2022): Modernized ResNet. Competes with ViT.
"""

if HAS:
    # ResNet block concept
    class ResBlock(nn.Module):
        def __init__(self, channels):
            super().__init__()
            self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
            self.bn1 = nn.BatchNorm2d(channels)
            self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
            self.bn2 = nn.BatchNorm2d(channels)
        
        def forward(self, x):
            residual = x
            out = F.relu(self.bn1(self.conv1(x)))
            out = self.bn2(self.conv2(out))
            out += residual  # SKIP CONNECTION
            return F.relu(out)
    
    rb = ResBlock(32)
    x_rb = torch.randn(2, 32, 8, 8)
    print(f"  ResBlock: {x_rb.shape} -> {rb(x_rb).shape}")
    print(f"  Skip connection: output = F(x) + x")

# =====================================================================
#   PARTE 6: RNN FUNDAMENTALS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 6: RNN ===")
print("="*80)

"""
RNN: Recurrent Neural Network.
  - Procesa SECUENCIAS (texto, audio, time series).
  - Hidden state: memoria del pasado.
  
  h_t = tanh(W_hh * h_{t-1} + W_xh * x_t + b)
  
  Problemas:
  - Vanishing gradients: no aprende dependencias largas.
  - Exploding gradients: gradient clipping ayuda.
"""

if HAS:
    rnn = nn.RNN(input_size=10, hidden_size=32, num_layers=2, batch_first=True)
    x_seq = torch.randn(4, 20, 10)  # batch=4, seq_len=20, features=10
    output, h_n = rnn(x_seq)
    
    print(f"  RNN input: {x_seq.shape}")
    print(f"  RNN output: {output.shape}")
    print(f"  RNN h_n: {h_n.shape}")
    print(f"  Params: {sum(p.numel() for p in rnn.parameters()):,}")

# =====================================================================
#   PARTE 7: LSTM
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 7: LSTM ===")
print("="*80)

"""
LSTM: Long Short-Term Memory.
  Gates control information flow:
  - Forget gate: what to discard from cell state.
  - Input gate: what new info to store.
  - Output gate: what to output.
  - Cell state: long-term memory highway.
  
  Solves vanishing gradient problem.
"""

if HAS:
    lstm = nn.LSTM(input_size=10, hidden_size=64, num_layers=2,
                    batch_first=True, dropout=0.2, bidirectional=False)
    x_seq = torch.randn(4, 30, 10)
    output, (h_n, c_n) = lstm(x_seq)
    
    print(f"  LSTM input: {x_seq.shape}")
    print(f"  LSTM output: {output.shape}")
    print(f"  h_n: {h_n.shape}, c_n: {c_n.shape}")
    
    # Bidirectional
    bilstm = nn.LSTM(10, 64, 2, batch_first=True, bidirectional=True)
    bi_out, _ = bilstm(x_seq)
    print(f"  BiLSTM output: {bi_out.shape}  (2x hidden)")

# =====================================================================
#   PARTE 8: GRU
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 8: GRU ===")
print("="*80)

"""
GRU: Gated Recurrent Unit.
  Simplified LSTM: 2 gates instead of 3.
  - Reset gate: how much past to forget.
  - Update gate: how much to update.
  
  Faster than LSTM, similar performance.
"""

if HAS:
    gru = nn.GRU(input_size=10, hidden_size=64, num_layers=2, batch_first=True)
    x_seq = torch.randn(4, 30, 10)
    output, h_n = gru(x_seq)
    print(f"  GRU output: {output.shape}, h_n: {h_n.shape}")

# =====================================================================
#   PARTE 9: SEQUENCE CLASSIFICATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 9: SEQ CLASSIFICATION ===")
print("="*80)

if HAS:
    class LSTMClassifier(nn.Module):
        def __init__(self, input_dim, hidden_dim, num_classes, num_layers=2):
            super().__init__()
            self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers,
                                batch_first=True, dropout=0.2)
            self.fc = nn.Linear(hidden_dim, num_classes)
        
        def forward(self, x):
            _, (h_n, _) = self.lstm(x)
            return self.fc(h_n[-1])  # Last layer hidden state
    
    clf = LSTMClassifier(10, 64, 5)
    x = torch.randn(8, 50, 10)
    print(f"  LSTM clf: {x.shape} -> {clf(x).shape}")

# =====================================================================
#   PARTE 10: ATTENTION MECHANISM
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 10: ATTENTION ===")
print("="*80)

"""
ATTENTION: "which parts of input to focus on?"

Scaled Dot-Product Attention:
  Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V

  Q: Query (what am I looking for?)
  K: Key (what do I contain?)
  V: Value (what do I return?)

This is THE fundamental building block of Transformers.
"""

if HAS:
    def scaled_dot_product_attention(Q, K, V, mask=None):
        d_k = Q.size(-1)
        scores = Q @ K.transpose(-2, -1) / (d_k ** 0.5)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        weights = F.softmax(scores, dim=-1)
        return weights @ V, weights
    
    Q = torch.randn(2, 8, 10, 64)  # batch, heads, seq, dim
    K = torch.randn(2, 8, 10, 64)
    V = torch.randn(2, 8, 10, 64)
    
    out, weights = scaled_dot_product_attention(Q, K, V)
    print(f"  Attention: Q={Q.shape} -> out={out.shape}")
    print(f"  Weights: {weights.shape} (sum={weights.sum(-1)[0,0,0]:.4f})")

# =====================================================================
#   PARTE 11: MULTI-HEAD ATTENTION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 11: MULTI-HEAD ===")
print("="*80)

"""
Multi-Head Attention:
  Multiple attention heads learn different relationships.
  
  MultiHead(Q, K, V) = Concat(head_1, ..., head_h) @ W_O
  head_i = Attention(Q @ W_Q_i, K @ W_K_i, V @ W_V_i)
"""

if HAS:
    mha = nn.MultiheadAttention(embed_dim=64, num_heads=8, batch_first=True)
    x = torch.randn(4, 20, 64)  # batch=4, seq=20, dim=64
    attn_out, attn_weights = mha(x, x, x)  # self-attention
    print(f"  MHA: {x.shape} -> {attn_out.shape}")
    print(f"  Params: {sum(p.numel() for p in mha.parameters()):,}")

# =====================================================================
#   PARTE 12: TRANSFORMER ENCODER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 12: TRANSFORMER ===")
print("="*80)

"""
Transformer Encoder Layer:
  1. Multi-Head Self-Attention
  2. Add & LayerNorm (residual connection)
  3. Feed-Forward Network (2 linear layers + ReLU)
  4. Add & LayerNorm
"""

if HAS:
    encoder_layer = nn.TransformerEncoderLayer(
        d_model=64, nhead=8, dim_feedforward=256,
        dropout=0.1, batch_first=True
    )
    encoder = nn.TransformerEncoder(encoder_layer, num_layers=6)
    
    x = torch.randn(4, 20, 64)
    out = encoder(x)
    print(f"  TransformerEncoder: {x.shape} -> {out.shape}")
    print(f"  Params: {sum(p.numel() for p in encoder.parameters()):,}")

# =====================================================================
#   PARTE 13: POSITIONAL ENCODING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 13: POSITIONAL ===")
print("="*80)

"""
Transformer has NO notion of position.
Positional Encoding adds position info.

PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
"""

if HAS:
    class PositionalEncoding(nn.Module):
        def __init__(self, d_model, max_len=5000):
            super().__init__()
            pe = torch.zeros(max_len, d_model)
            pos = torch.arange(0, max_len).unsqueeze(1).float()
            div = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))
            pe[:, 0::2] = torch.sin(pos * div)
            pe[:, 1::2] = torch.cos(pos * div)
            self.register_buffer('pe', pe.unsqueeze(0))
        
        def forward(self, x):
            return x + self.pe[:, :x.size(1)]
    
    pe = PositionalEncoding(64)
    x = torch.randn(2, 20, 64)
    print(f"  PE: {x.shape} -> {pe(x).shape}")

# =====================================================================
#   PARTE 14: FULL TRANSFORMER CLASSIFIER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 14: TRANSFORMER CLF ===")
print("="*80)

if HAS:
    class TransformerClassifier(nn.Module):
        def __init__(self, input_dim, d_model, nhead, num_layers, num_classes):
            super().__init__()
            self.embedding = nn.Linear(input_dim, d_model)
            self.pos_enc = PositionalEncoding(d_model)
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=d_model, nhead=nhead, dim_feedforward=d_model*4,
                dropout=0.1, batch_first=True
            )
            self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
            self.classifier = nn.Linear(d_model, num_classes)
        
        def forward(self, x):
            x = self.embedding(x)
            x = self.pos_enc(x)
            x = self.encoder(x)
            x = x.mean(dim=1)  # Global average pooling
            return self.classifier(x)
    
    tcf = TransformerClassifier(10, 64, 8, 4, 5)
    x = torch.randn(4, 30, 10)
    print(f"  Transformer clf: {x.shape} -> {tcf(x).shape}")
    print(f"  Params: {sum(p.numel() for p in tcf.parameters()):,}")

# =====================================================================
#   PARTE 15: CNN vs RNN vs TRANSFORMER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 15: COMPARISON ===")
print("="*80)

comparison = [
    ("", "CNN", "RNN/LSTM", "Transformer"),
    ("Input", "Grid (image)", "Sequence", "Sequence/Set"),
    ("Locality", "Local patterns", "Sequential", "Global"),
    ("Parallelizable", "Yes", "No (sequential)", "Yes"),
    ("Long-range", "Limited", "LSTM helps", "Excellent"),
    ("Memory", "O(1) per layer", "O(n)", "O(n²)"),
    ("Best for", "Images", "Short seq", "Long seq/NLP"),
]

for row in comparison:
    print(f"  {row[0]:>14s} {row[1]:>14s} {row[2]:>14s} {row[3]:>14s}")

# =====================================================================
#   PARTE 16: TRAINING COMPARISON
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 16: TRAINING COMPARE ===")
print("="*80)

if HAS:
    torch.manual_seed(42)
    X_seq = torch.randn(300, 20, 10)
    y_seq = (X_seq[:, :, 0].mean(1) > 0).long()
    
    train_dl = DataLoader(TensorDataset(X_seq[:240], y_seq[:240]), batch_size=32, shuffle=True)
    
    models_cmp = {
        'LSTM': LSTMClassifier(10, 32, 2, 1),
        'Transformer': TransformerClassifier(10, 32, 4, 2, 2),
    }
    
    for name, m in models_cmp.items():
        m.to(DEVICE)
        opt = torch.optim.Adam(m.parameters(), lr=0.001)
        for epoch in range(15):
            m.train()
            for xb, yb in train_dl:
                xb, yb = xb.to(DEVICE), yb.to(DEVICE)
                opt.zero_grad()
                nn.CrossEntropyLoss()(m(xb), yb).backward()
                opt.step()
        
        m.eval()
        with torch.no_grad():
            preds = m(X_seq[240:].to(DEVICE)).argmax(1).cpu()
            acc = (preds == y_seq[240:]).float().mean()
        n_params = sum(p.numel() for p in m.parameters())
        print(f"  {name:>12s}: acc={acc:.4f}, params={n_params:,}")

# =====================================================================
#   PARTE 17: DATA AUGMENTATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 17: AUGMENTATION ===")
print("="*80)

"""
Image augmentation (torchvision.transforms):
  RandomHorizontalFlip, RandomRotation, RandomCrop,
  ColorJitter, RandomErasing, Normalize.

Sequence augmentation:
  Random masking, noise injection, time warping.
"""

print("  Image augmentation techniques:")
augs = [
    ("RandomHorizontalFlip", "50% chance flip"),
    ("RandomRotation(10)", "±10 degrees"),
    ("ColorJitter", "brightness/contrast/saturation"),
    ("RandomCrop", "crop and resize"),
    ("RandomErasing", "erase random patch"),
    ("Normalize", "mean/std normalization"),
]
for name, desc in augs:
    print(f"    {name:>25s}: {desc}")

# =====================================================================
#   PARTE 18: VISION TRANSFORMER (ViT)
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 18: ViT ===")
print("="*80)

"""
Vision Transformer (ViT):
1. Split image into patches (e.g., 16x16).
2. Flatten each patch to a vector.
3. Linear projection + positional encoding.
4. Feed through Transformer encoder.
5. [CLS] token for classification.
"""

if HAS:
    class PatchEmbedding(nn.Module):
        def __init__(self, img_size=28, patch_size=7, in_channels=1, embed_dim=64):
            super().__init__()
            self.n_patches = (img_size // patch_size) ** 2
            self.proj = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)
        
        def forward(self, x):
            x = self.proj(x)  # (B, embed_dim, n_h, n_w)
            x = x.flatten(2)  # (B, embed_dim, n_patches)
            return x.transpose(1, 2)  # (B, n_patches, embed_dim)
    
    pe_vit = PatchEmbedding(28, 7, 1, 64)
    x_img = torch.randn(2, 1, 28, 28)
    patches = pe_vit(x_img)
    print(f"  ViT patches: {x_img.shape} -> {patches.shape}")
    print(f"  {(28//7)**2} patches of dim 64")

# =====================================================================
#   PARTE 19: BEST PRACTICES
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 19: BEST PRACTICES ===")
print("="*80)

practices = [
    ("CNN", "Use BatchNorm + residual connections"),
    ("CNN", "Start with pretrained (transfer learning)"),
    ("RNN", "Use LSTM/GRU over vanilla RNN"),
    ("RNN", "Bidirectional for non-causal tasks"),
    ("RNN", "Gradient clipping essential"),
    ("Transformer", "Use LayerNorm + residual"),
    ("Transformer", "Warmup LR scheduler"),
    ("Transformer", "Label smoothing"),
    ("General", "Data augmentation always helps"),
    ("General", "Start small, scale up"),
]

print(f"\n  {'Domain':>12s} {'Practice':>40s}")
for domain, practice in practices:
    print(f"  {domain:>12s} {practice:>40s}")

# =====================================================================
#   PARTE 20: ARCHITECTURE CHEATSHEET
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 20: CHEATSHEET ===")
print("="*80)

guide = [
    ("Image classification", "ResNet / EfficientNet / ViT"),
    ("Object detection", "YOLO / Faster R-CNN"),
    ("Segmentation", "U-Net / DeepLab"),
    ("Text classification", "BERT / RoBERTa"),
    ("Translation", "Transformer / mBART"),
    ("Generation", "GPT / T5"),
    ("Time series", "LSTM / Temporal Fusion Transformer"),
    ("Audio", "Wav2Vec2 / Whisper"),
    ("Tabular", "XGBoost > DL (usually)"),
]

print(f"\n  {'Task':>22s} {'Architecture':>30s}")
for task, arch in guide:
    print(f"  {task:>22s} {arch:>30s}")


# =====================================================================
#   PARTE 21: INCEPTION MODULE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 21: INCEPTION ===")
print("="*80)

"""
Inception: apply multiple filter sizes in parallel.
  Branch 1: 1x1 conv
  Branch 2: 1x1 -> 3x3 conv
  Branch 3: 1x1 -> 5x5 conv
  Branch 4: MaxPool -> 1x1 conv
  Concatenate all branches.
"""

if HAS:
    class InceptionBlock(nn.Module):
        def __init__(self, in_ch, ch_1x1, ch_3x3, ch_5x5, ch_pool):
            super().__init__()
            self.branch1 = nn.Conv2d(in_ch, ch_1x1, 1)
            self.branch2 = nn.Sequential(
                nn.Conv2d(in_ch, ch_3x3, 1),
                nn.Conv2d(ch_3x3, ch_3x3, 3, padding=1))
            self.branch3 = nn.Sequential(
                nn.Conv2d(in_ch, ch_5x5, 1),
                nn.Conv2d(ch_5x5, ch_5x5, 5, padding=2))
            self.branch4 = nn.Sequential(
                nn.MaxPool2d(3, stride=1, padding=1),
                nn.Conv2d(in_ch, ch_pool, 1))
        
        def forward(self, x):
            return torch.cat([self.branch1(x), self.branch2(x),
                              self.branch3(x), self.branch4(x)], dim=1)
    
    inc = InceptionBlock(32, 16, 16, 8, 8)
    x_inc = torch.randn(2, 32, 8, 8)
    print(f"  Inception: {x_inc.shape} -> {inc(x_inc).shape}")
    print(f"  Output channels: 16+16+8+8 = 48")


# =====================================================================
#   PARTE 22: DEPTHWISE SEPARABLE CONV
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 22: DEPTHWISE ===")
print("="*80)

"""
Depthwise Separable Conv (MobileNet):
  1. Depthwise: one filter per input channel.
  2. Pointwise: 1x1 conv to mix channels.
  
  Params: K²*C + C*C' vs K²*C*C' (standard).
  ~8-9x fewer parameters.
"""

if HAS:
    class DepthwiseSeparable(nn.Module):
        def __init__(self, in_ch, out_ch, kernel_size=3):
            super().__init__()
            self.depthwise = nn.Conv2d(in_ch, in_ch, kernel_size,
                                        padding=kernel_size//2, groups=in_ch)
            self.pointwise = nn.Conv2d(in_ch, out_ch, 1)
        
        def forward(self, x):
            return self.pointwise(self.depthwise(x))
    
    standard = nn.Conv2d(32, 64, 3, padding=1)
    dws = DepthwiseSeparable(32, 64, 3)
    
    std_params = sum(p.numel() for p in standard.parameters())
    dws_params = sum(p.numel() for p in dws.parameters())
    print(f"  Standard Conv: {std_params:,} params")
    print(f"  Depthwise Sep: {dws_params:,} params")
    print(f"  Ratio: {std_params/dws_params:.1f}x fewer")


# =====================================================================
#   PARTE 23: 1x1 CONVOLUTIONS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 23: 1x1 CONV ===")
print("="*80)

"""
1x1 conv: "Network in Network".
Uses:
  1. Channel reduction (bottleneck).
  2. Channel expansion.
  3. Cross-channel interaction.
  4. Add nonlinearity without changing spatial size.
"""

if HAS:
    # Bottleneck: reduce channels
    bottleneck = nn.Conv2d(256, 64, 1)
    x_bn = torch.randn(1, 256, 16, 16)
    print(f"  Bottleneck: {x_bn.shape} -> {bottleneck(x_bn).shape}")
    print(f"  Params: {sum(p.numel() for p in bottleneck.parameters()):,}")


# =====================================================================
#   PARTE 24: SEQ2SEQ
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 24: SEQ2SEQ ===")
print("="*80)

"""
Sequence-to-Sequence: encoder-decoder architecture.
  Encoder: input sequence -> context vector.
  Decoder: context vector -> output sequence.
  
  Applications: translation, summarization, chatbots.
"""

if HAS:
    class Seq2SeqEncoder(nn.Module):
        def __init__(self, input_dim, hidden_dim, num_layers=1):
            super().__init__()
            self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        
        def forward(self, x):
            _, (h, c) = self.lstm(x)
            return h, c
    
    class Seq2SeqDecoder(nn.Module):
        def __init__(self, input_dim, hidden_dim, output_dim, num_layers=1):
            super().__init__()
            self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
            self.fc = nn.Linear(hidden_dim, output_dim)
        
        def forward(self, x, hidden):
            out, hidden = self.lstm(x, hidden)
            return self.fc(out), hidden
    
    enc = Seq2SeqEncoder(10, 64)
    dec = Seq2SeqDecoder(10, 64, 10)
    
    src = torch.randn(4, 20, 10)
    h, c = enc(src)
    tgt = torch.randn(4, 15, 10)
    out, _ = dec(tgt, (h, c))
    print(f"  Encoder: {src.shape} -> h={h.shape}")
    print(f"  Decoder: {tgt.shape} -> {out.shape}")


# =====================================================================
#   PARTE 25: TEACHER FORCING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 25: TEACHER FORCING ===")
print("="*80)

"""
Teacher forcing: feed ground truth as decoder input.
  - Training: use true previous token (fast convergence).
  - Inference: use predicted previous token (autoregressive).
  - Scheduled sampling: mix both (gradually reduce teacher forcing).

Without TF: error accumulates (exposure bias).
"""

print("  Teacher forcing modes:")
print("    Training: decoder_input = ground_truth[t-1]")
print("    Inference: decoder_input = model_prediction[t-1]")
print("    Scheduled: P(teacher) decreases over epochs")


# =====================================================================
#   PARTE 26: ATTENTION VARIANTS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 26: ATTENTION TYPES ===")
print("="*80)

"""
Attention variants:
1. Dot-product: Q @ K^T
2. Scaled dot-product: Q @ K^T / sqrt(d)
3. Additive (Bahdanau): v^T @ tanh(W_q@Q + W_k@K)
4. Multi-head: parallel attention heads
5. Cross-attention: Q from decoder, K/V from encoder
6. Self-attention: Q=K=V from same input
7. Causal/masked: prevent attending to future
8. Linear attention: O(n) approximation
9. Flash attention: IO-aware exact attention
"""

attn_types = [
    ("Self-attention", "Q=K=V same input", "Transformer encoder"),
    ("Cross-attention", "Q from dec, K/V from enc", "Transformer decoder"),
    ("Causal", "Mask future tokens", "GPT, generation"),
    ("Multi-head", "Parallel heads", "All transformers"),
    ("Flash", "IO-optimized", "Production training"),
]

print(f"  {'Type':>16s} {'Description':>25s} {'Use':>20s}")
for t, d, u in attn_types:
    print(f"  {t:>16s} {d:>25s} {u:>20s}")


# =====================================================================
#   PARTE 27: CAUSAL MASKING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 27: CAUSAL MASK ===")
print("="*80)

if HAS:
    def create_causal_mask(seq_len):
        """Create upper triangular mask for causal attention."""
        mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
        return mask  # True = masked
    
    mask = create_causal_mask(5)
    print(f"  Causal mask (5x5):")
    for row in mask:
        print(f"    {['.' if not x else 'X' for x in row]}")
    
    # Apply in transformer
    x = torch.randn(2, 10, 64)
    mask_10 = create_causal_mask(10).to(DEVICE)
    
    dec_layer = nn.TransformerEncoderLayer(d_model=64, nhead=8, batch_first=True)
    out = dec_layer(x, src_mask=mask_10.float().masked_fill(mask_10, float('-inf')))
    print(f"\n  Causal output: {out.shape}")


# =====================================================================
#   PARTE 28: TRANSFORMER DECODER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 28: DECODER ===")
print("="*80)

if HAS:
    decoder_layer = nn.TransformerDecoderLayer(
        d_model=64, nhead=8, dim_feedforward=256,
        dropout=0.1, batch_first=True
    )
    decoder = nn.TransformerDecoder(decoder_layer, num_layers=4)
    
    memory = torch.randn(2, 20, 64)  # encoder output
    tgt = torch.randn(2, 15, 64)     # decoder input
    
    out = decoder(tgt, memory)
    print(f"  Decoder: tgt={tgt.shape}, memory={memory.shape} -> {out.shape}")


# =====================================================================
#   PARTE 29: ENCODER-DECODER
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 29: ENC-DEC ===")
print("="*80)

if HAS:
    full_transformer = nn.Transformer(
        d_model=64, nhead=8, num_encoder_layers=4,
        num_decoder_layers=4, dim_feedforward=256,
        dropout=0.1, batch_first=True
    )
    
    src = torch.randn(2, 20, 64)
    tgt = torch.randn(2, 15, 64)
    out = full_transformer(src, tgt)
    print(f"  Full Transformer: src={src.shape}, tgt={tgt.shape} -> {out.shape}")
    print(f"  Params: {sum(p.numel() for p in full_transformer.parameters()):,}")


# =====================================================================
#   PARTE 30: DEEP LEARNING TIMELINE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 30: TIMELINE ===")
print("="*80)

timeline = [
    (1989, "LeNet", "First practical CNN"),
    (2012, "AlexNet", "Deep learning revolution"),
    (2014, "GAN", "Generative Adversarial Networks"),
    (2014, "Seq2Seq+Attn", "Attention mechanism born"),
    (2015, "ResNet", "Skip connections, 152 layers"),
    (2017, "Transformer", "Attention Is All You Need"),
    (2018, "BERT", "Pretrained NLP revolution"),
    (2018, "GPT-1", "Generative pretraining"),
    (2020, "ViT", "Vision Transformer"),
    (2020, "GPT-3", "Few-shot learning, 175B params"),
    (2022, "ChatGPT", "LLMs go mainstream"),
    (2023, "GPT-4", "Multimodal, SOTA"),
    (2024, "Mixture of Experts", "Efficient scaling"),
]

print(f"  {'Year':>6s} {'Model':>12s} {'Impact':>35s}")
for year, model, impact in timeline:
    print(f"  {year:6d} {model:>12s} {impact:>35s}")


# =====================================================================
#   PARTE 31: U-NET
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 31: U-NET ===")
print("="*80)

"""
U-Net: encoder-decoder for segmentation.
  Encoder: downsample (extract features).
  Decoder: upsample (recover resolution).
  Skip connections: concatenate encoder features to decoder.
  
  Used in: medical imaging, diffusion models (Stable Diffusion).
"""

if HAS:
    class UNetBlock(nn.Module):
        def __init__(self, in_ch, out_ch):
            super().__init__()
            self.conv = nn.Sequential(
                nn.Conv2d(in_ch, out_ch, 3, padding=1), nn.ReLU(), nn.BatchNorm2d(out_ch),
                nn.Conv2d(out_ch, out_ch, 3, padding=1), nn.ReLU(), nn.BatchNorm2d(out_ch))
        def forward(self, x):
            return self.conv(x)
    
    class MiniUNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.enc1 = UNetBlock(1, 32)
            self.enc2 = UNetBlock(32, 64)
            self.pool = nn.MaxPool2d(2)
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
            self.dec1 = UNetBlock(96, 32)  # 64 + 32 skip
            self.final = nn.Conv2d(32, 1, 1)
        
        def forward(self, x):
            e1 = self.enc1(x)
            e2 = self.enc2(self.pool(e1))
            d1 = self.dec1(torch.cat([self.up(e2), e1], dim=1))
            return self.final(d1)
    
    unet = MiniUNet()
    x = torch.randn(2, 1, 32, 32)
    print(f"  U-Net: {x.shape} -> {unet(x).shape}")
    print(f"  Params: {sum(p.numel() for p in unet.parameters()):,}")


# =====================================================================
#   PARTE 32: GAN CONCEPT
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 32: GAN ===")
print("="*80)

"""
GAN: Generator vs Discriminator.
  Generator: random noise -> fake data.
  Discriminator: real vs fake classifier.
  
  Training: minimax game.
    D tries to distinguish real from fake.
    G tries to fool D.
    
  Variants: DCGAN, WGAN, StyleGAN, CycleGAN.
"""

if HAS:
    class Generator(nn.Module):
        def __init__(self, latent_dim=100, img_dim=784):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(latent_dim, 256), nn.ReLU(),
                nn.Linear(256, 512), nn.ReLU(),
                nn.Linear(512, img_dim), nn.Tanh())
        def forward(self, z):
            return self.net(z)
    
    class Discriminator(nn.Module):
        def __init__(self, img_dim=784):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(img_dim, 512), nn.LeakyReLU(0.2),
                nn.Linear(512, 256), nn.LeakyReLU(0.2),
                nn.Linear(256, 1), nn.Sigmoid())
        def forward(self, x):
            return self.net(x)
    
    G = Generator(100, 784)
    D = Discriminator(784)
    z = torch.randn(4, 100)
    fake = G(z)
    score = D(fake)
    print(f"  Generator: z={z.shape} -> fake={fake.shape}")
    print(f"  Discriminator: fake={fake.shape} -> score={score.shape}")


# =====================================================================
#   PARTE 33: MODEL SCALING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 33: SCALING ===")
print("="*80)

"""
Scaling laws (Kaplan et al., Chinchilla):
  Performance improves with:
  1. More parameters (width, depth).
  2. More data.
  3. More compute.
  
  Optimal allocation: balance params and data.
  Chinchilla: tokens ≈ 20 × parameters.
  
  Efficient scaling:
  - Mixture of Experts (MoE): sparse activation.
  - Distillation: large -> small model.
  - Quantization: fp32 -> int8/int4.
  - Pruning: remove redundant weights.
"""

scaling = [
    ("Width", "More neurons per layer", "Linear param increase"),
    ("Depth", "More layers", "Better representations"),
    ("Data", "More training data", "Less overfitting"),
    ("Compute", "More GPU hours", "Better optimization"),
    ("MoE", "Sparse experts", "Efficient scaling"),
    ("Distillation", "Teacher->student", "Smaller model"),
    ("Quantization", "Lower precision", "Faster inference"),
]

print(f"  {'Method':>14s} {'Description':>22s} {'Effect':>22s}")
for m, d, e in scaling:
    print(f"  {m:>14s} {d:>22s} {e:>22s}")

print("\n" + "="*80)
print("=== CONCLUSION ===")
print("="*80)
print("\n FIN DE ARCHIVO 01_cnn_rnn_transformers.")
print(" CNN, RNN, y Transformers dominados.")
