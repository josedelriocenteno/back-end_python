# ===========================================================================
# 01_transfer_learning.py - MODULO 20: TRANSFER LEARNING
# ===========================================================================
import numpy as np, warnings
warnings.filterwarnings('ignore')
try:
    import torch, torch.nn as nn, torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset
    HAS = True
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
except ImportError:
    HAS = False

# =====================================================================
#   PARTE 1: WHAT IS TRANSFER LEARNING
# =====================================================================
print("\n" + "="*80)
print("=== CAPITULO 1: TRANSFER LEARNING ===")
print("="*80)

"""
TRANSFER LEARNING: usar conocimiento de una tarea para mejorar otra.

Paradigma:
  1. Pre-train on large dataset (ImageNet, Wikipedia).
  2. Fine-tune on small target dataset.

Why it works:
  - Lower layers learn universal features (edges, textures, syntax).
  - Higher layers learn task-specific features.
  - Reusing lower layers saves compute and data.

Strategies:
  1. Feature extraction: freeze pretrained, train new head.
  2. Fine-tuning: unfreeze some/all layers, train with low LR.
  3. Full fine-tuning: train everything.
"""

print("  Transfer Learning strategies:")
strategies = [
    ("Feature Extraction", "Freeze backbone, train head only", "Small data"),
    ("Partial Fine-tune", "Unfreeze top layers + head", "Medium data"),
    ("Full Fine-tune", "Unfreeze all, low LR", "Large data"),
    ("Linear Probing", "Train linear layer on features", "Evaluation"),
]
for s, d, w in strategies:
    print(f"    {s:>20s}: {d:>35s} | {w}")

# =====================================================================
#   PARTE 2: PRETRAINED BACKBONE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 2: PRETRAINED BACKBONE ===")
print("="*80)

if HAS:
    class PretrainedCNN(nn.Module):
        """Simulates a pretrained CNN backbone."""
        def __init__(self):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(3, 64, 3, padding=1), nn.ReLU(), nn.BatchNorm2d(64),
                nn.MaxPool2d(2),
                nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.BatchNorm2d(128),
                nn.MaxPool2d(2),
                nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(), nn.BatchNorm2d(256),
                nn.AdaptiveAvgPool2d((1, 1)),
            )
            self.classifier = nn.Linear(256, 1000)  # ImageNet classes

        def forward(self, x):
            feat = self.features(x)
            feat = feat.flatten(1)
            return self.classifier(feat)

    backbone = PretrainedCNN()
    # Simulate pretrained weights
    torch.manual_seed(42)
    for p in backbone.parameters():
        nn.init.normal_(p, 0, 0.02)
    
    x = torch.randn(4, 3, 32, 32)
    print(f"  Backbone: {x.shape} -> {backbone(x).shape}")
    print(f"  Params: {sum(p.numel() for p in backbone.parameters()):,}")

# =====================================================================
#   PARTE 3: FEATURE EXTRACTION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 3: FEATURE EXTRACTION ===")
print("="*80)

if HAS:
    # Freeze all backbone params
    for param in backbone.features.parameters():
        param.requires_grad = False
    
    # Replace classifier
    backbone.classifier = nn.Sequential(
        nn.Linear(256, 64), nn.ReLU(), nn.Dropout(0.3),
        nn.Linear(64, 5),  # 5 target classes
    )
    
    trainable = sum(p.numel() for p in backbone.parameters() if p.requires_grad)
    total = sum(p.numel() for p in backbone.parameters())
    print(f"  Total params: {total:,}")
    print(f"  Trainable:    {trainable:,}")
    print(f"  Frozen:       {total - trainable:,}")
    print(f"  Ratio:        {trainable/total*100:.1f}% trainable")

# =====================================================================
#   PARTE 4: TRAINING FEATURE EXTRACTOR
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 4: TRAINING ===")
print("="*80)

if HAS:
    torch.manual_seed(42)
    X_img = torch.randn(200, 3, 32, 32)
    y_img = torch.randint(0, 5, (200,))
    
    train_dl = DataLoader(TensorDataset(X_img[:160], y_img[:160]), batch_size=16, shuffle=True)
    
    opt = torch.optim.Adam(filter(lambda p: p.requires_grad, backbone.parameters()), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    backbone.to(DEVICE)
    for epoch in range(10):
        backbone.train()
        total_loss = 0
        for xb, yb in train_dl:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            opt.zero_grad()
            loss = criterion(backbone(xb), yb)
            loss.backward()
            opt.step()
            total_loss += loss.item()
        if epoch % 3 == 0:
            print(f"    epoch {epoch}: loss={total_loss/len(train_dl):.4f}")

# =====================================================================
#   PARTE 5: FINE-TUNING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 5: FINE-TUNING ===")
print("="*80)

"""
Fine-tuning: unfreeze backbone, use LOWER learning rate.
  - Backbone LR: 1e-5 to 1e-4 (preserve pretrained features).
  - Head LR: 1e-3 to 1e-2 (learn new task fast).
  - Differential LR: different LR per layer group.
"""

if HAS:
    # Unfreeze backbone
    for param in backbone.features.parameters():
        param.requires_grad = True
    
    # Differential learning rates
    param_groups = [
        {'params': backbone.features.parameters(), 'lr': 1e-4},
        {'params': backbone.classifier.parameters(), 'lr': 1e-3},
    ]
    opt_ft = torch.optim.Adam(param_groups)
    
    print(f"  Differential LR:")
    print(f"    Backbone: lr=1e-4")
    print(f"    Head:     lr=1e-3")
    
    for epoch in range(5):
        backbone.train()
        total_loss = 0
        for xb, yb in train_dl:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            opt_ft.zero_grad()
            loss = criterion(backbone(xb), yb)
            loss.backward()
            opt_ft.step()
            total_loss += loss.item()
        print(f"    epoch {epoch}: loss={total_loss/len(train_dl):.4f}")

# =====================================================================
#   PARTE 6: GRADUAL UNFREEZING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 6: GRADUAL UNFREEZE ===")
print("="*80)

"""
Gradual unfreezing (ULMFiT):
  Epoch 1: train head only.
  Epoch 2: unfreeze last block + head.
  Epoch 3: unfreeze more layers.
  ...until all unfrozen.
"""

if HAS:
    def freeze_all(model):
        for p in model.parameters():
            p.requires_grad = False

    def unfreeze_from(model, layer_idx):
        """Unfreeze from layer_idx onwards."""
        layers = list(model.features.children())
        for i, layer in enumerate(layers):
            if i >= layer_idx:
                for p in layer.parameters():
                    p.requires_grad = True

    freeze_all(backbone)
    # Unfreeze classifier always
    for p in backbone.classifier.parameters():
        p.requires_grad = True
    
    schedule = [(0, 6), (2, 3), (4, 0)]  # (epoch, unfreeze_from)
    for epoch, unfreeze_idx in schedule:
        unfreeze_from(backbone, unfreeze_idx)
        trainable = sum(p.numel() for p in backbone.parameters() if p.requires_grad)
        print(f"  Epoch {epoch}: unfreeze from layer {unfreeze_idx}, trainable={trainable:,}")

# =====================================================================
#   PARTE 7: DOMAIN ADAPTATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 7: DOMAIN ADAPTATION ===")
print("="*80)

"""
When source and target domains differ:
  1. Same task, different domain (medical images).
  2. Different task, same domain.
  3. Different task, different domain (hardest).

Techniques:
  - Domain-specific augmentation.
  - Intermediate fine-tuning.
  - Few-shot learning.
  - Domain adversarial training.
"""

print("  Domain adaptation strategies:")
das = [
    ("Close domains", "Direct fine-tune", "ImageNet -> Dogs"),
    ("Far domains", "Intermediate task", "ImageNet -> Medical"),
    ("Few-shot", "Meta-learning", "5 examples per class"),
    ("Zero-shot", "CLIP-style", "No target examples"),
]
for d, s, e in das:
    print(f"    {d:>14s}: {s:>20s} | {e}")

# =====================================================================
#   PARTE 8: NLP TRANSFER LEARNING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 8: NLP TRANSFER ===")
print("="*80)

"""
NLP Transfer Learning evolution:
  Word2Vec/GloVe: pretrained embeddings only.
  ELMo: contextualized embeddings.
  BERT: full model pretraining + fine-tuning.
  GPT: generative pretraining.
  T5: text-to-text pretraining.
  
  Modern: prompt engineering, in-context learning, adapters.
"""

if HAS:
    class NLPTransferModel(nn.Module):
        def __init__(self, vocab, d_model, n_heads, n_layers, num_classes):
            super().__init__()
            self.emb = nn.Embedding(vocab, d_model)
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=d_model, nhead=n_heads, dim_feedforward=d_model*4,
                batch_first=True)
            self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
            self.classifier = nn.Linear(d_model, num_classes)
        
        def forward(self, x):
            h = self.emb(x)
            h = self.encoder(h)
            h = h.mean(dim=1)  # pool
            return self.classifier(h)
    
    nlp_model = NLPTransferModel(5000, 64, 4, 2, 3)
    tokens = torch.randint(0, 5000, (4, 30))
    print(f"  NLP model: {list(tokens.shape)} -> {list(nlp_model(tokens).shape)}")
    print(f"  Params: {sum(p.numel() for p in nlp_model.parameters()):,}")

# =====================================================================
#   PARTE 9: LORA (LOW-RANK ADAPTATION)
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 9: LoRA ===")
print("="*80)

"""
LoRA: Low-Rank Adaptation.
  Freeze pretrained weights W.
  Add low-rank decomposition: W + A @ B.
  A: (d, r), B: (r, d), r << d.
  
  Only train A and B (~0.1% of params).
  Inference: merge W + A@B (no extra latency).
"""

if HAS:
    class LoRALinear(nn.Module):
        def __init__(self, original_linear, rank=4, alpha=1.0):
            super().__init__()
            self.original = original_linear
            self.original.weight.requires_grad = False
            if self.original.bias is not None:
                self.original.bias.requires_grad = False
            
            in_f = original_linear.in_features
            out_f = original_linear.out_features
            self.lora_A = nn.Parameter(torch.randn(in_f, rank) * 0.01)
            self.lora_B = nn.Parameter(torch.zeros(rank, out_f))
            self.alpha = alpha / rank
        
        def forward(self, x):
            return self.original(x) + (x @ self.lora_A @ self.lora_B) * self.alpha
    
    orig = nn.Linear(256, 256)
    lora = LoRALinear(orig, rank=4)
    
    orig_params = sum(p.numel() for p in orig.parameters())
    lora_trainable = sum(p.numel() for p in lora.parameters() if p.requires_grad)
    
    print(f"  Original params: {orig_params:,}")
    print(f"  LoRA trainable:  {lora_trainable:,}")
    print(f"  Ratio: {lora_trainable/orig_params*100:.2f}%")
    
    x = torch.randn(4, 256)
    print(f"  Output: {list(lora(x).shape)}")

# =====================================================================
#   PARTE 10: QLORA
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 10: QLoRA ===")
print("="*80)

"""
QLoRA: Quantized LoRA.
  1. Quantize base model to 4-bit (NF4).
  2. Add LoRA adapters in fp16.
  3. Train only LoRA params.
  
  Fine-tune 65B model on single 48GB GPU.
  No quality loss compared to full fine-tuning.
"""

print("  QLoRA pipeline:")
steps = [
    "1. Load pretrained model in 4-bit (bitsandbytes)",
    "2. Add LoRA adapters (peft library)",
    "3. Train with fp16 gradients",
    "4. Merge adapters for inference",
    "5. Optionally quantize merged model",
]
for s in steps:
    print(f"    {s}")

# =====================================================================
#   PARTE 11: ADAPTER LAYERS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 11: ADAPTERS ===")
print("="*80)

if HAS:
    class Adapter(nn.Module):
        def __init__(self, d_model, bottleneck_dim=64):
            super().__init__()
            self.down = nn.Linear(d_model, bottleneck_dim)
            self.up = nn.Linear(bottleneck_dim, d_model)
        
        def forward(self, x):
            return x + self.up(F.relu(self.down(x)))
    
    adapter = Adapter(256, 32)
    x = torch.randn(4, 10, 256)
    print(f"  Adapter: {list(x.shape)} -> {list(adapter(x).shape)}")
    print(f"  Params: {sum(p.numel() for p in adapter.parameters()):,}")

# =====================================================================
#   PARTE 12: PREFIX TUNING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 12: PREFIX TUNING ===")
print("="*80)

"""
Prefix tuning: prepend learnable tokens to input.
  Freeze model, only train prefix embeddings.
  
  Input: [prefix_1, prefix_2, ..., prefix_k, token_1, token_2, ...]
  Only prefix tokens are trainable.
"""

if HAS:
    class PrefixTuning(nn.Module):
        def __init__(self, model, prefix_len=10, d_model=64):
            super().__init__()
            self.model = model
            for p in self.model.parameters():
                p.requires_grad = False
            self.prefix = nn.Parameter(torch.randn(1, prefix_len, d_model) * 0.01)
        
        def forward(self, x):
            B = x.size(0)
            prefix = self.prefix.expand(B, -1, -1)
            h = self.model.emb(x)
            h = torch.cat([prefix, h], dim=1)
            h = self.model.encoder(h)
            h = h[:, self.prefix.size(1):].mean(dim=1)
            return self.model.classifier(h)
    
    pt_model = PrefixTuning(nlp_model, prefix_len=10, d_model=64)
    trainable = sum(p.numel() for p in pt_model.parameters() if p.requires_grad)
    print(f"  Prefix tuning: {trainable:,} trainable params")

# =====================================================================
#   PARTE 13: KNOWLEDGE DISTILLATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 13: DISTILLATION ===")
print("="*80)

"""
Knowledge Distillation: large teacher -> small student.
  1. Teacher produces soft labels (with temperature).
  2. Student learns from soft labels + hard labels.
  
  Loss = alpha * KL(student, teacher/T) + (1-alpha) * CE(student, labels)
"""

if HAS:
    def distillation_loss(student_logits, teacher_logits, labels,
                           temperature=4.0, alpha=0.7):
        soft_loss = F.kl_div(
            F.log_softmax(student_logits / temperature, dim=-1),
            F.softmax(teacher_logits / temperature, dim=-1),
            reduction='batchmean') * (temperature ** 2)
        hard_loss = F.cross_entropy(student_logits, labels)
        return alpha * soft_loss + (1 - alpha) * hard_loss
    
    teacher_out = torch.randn(4, 10)
    student_out = torch.randn(4, 10)
    labels = torch.tensor([0, 3, 5, 7])
    
    d_loss = distillation_loss(student_out, teacher_out, labels)
    print(f"  Distillation loss: {d_loss.item():.4f}")
    print(f"  Temperature: 4.0, alpha: 0.7")

# =====================================================================
#   PARTE 14: CONTRASTIVE LEARNING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 14: CONTRASTIVE ===")
print("="*80)

"""
Contrastive learning: learn representations by comparing.
  Positive pairs: augmented views of same image.
  Negative pairs: different images.
  
  SimCLR, MoCo, CLIP, DINO.
  Loss: InfoNCE / NT-Xent.
"""

if HAS:
    def info_nce_loss(features, temperature=0.07):
        B = features.shape[0] // 2
        labels = torch.arange(B).repeat(2).to(features.device)
        features = F.normalize(features, dim=1)
        similarity = features @ features.T / temperature
        # Mask self-similarity
        mask = torch.eye(2*B, device=features.device).bool()
        similarity.masked_fill_(mask, -1e9)
        return F.cross_entropy(similarity, labels)
    
    feats = torch.randn(8, 128)  # 4 pairs
    loss = info_nce_loss(feats)
    print(f"  InfoNCE loss: {loss.item():.4f}")

# =====================================================================
#   PARTE 15: PEFT COMPARISON
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 15: PEFT COMPARISON ===")
print("="*80)

peft_methods = [
    ("Method", "Trainable %", "Memory", "Quality"),
    ("Full FT", "100%", "High", "Best"),
    ("LoRA", "0.1-1%", "Low", "Near-best"),
    ("QLoRA", "0.1-1%", "Very low", "Near-best"),
    ("Adapter", "1-5%", "Low", "Good"),
    ("Prefix", "0.1%", "Very low", "Good"),
    ("Prompt", "0.01%", "Minimal", "Variable"),
]

for row in peft_methods:
    print(f"  {row[0]:>10s} {row[1]:>12s} {row[2]:>10s} {row[3]:>10s}")

# =====================================================================
#   PARTE 16: PRACTICAL TIPS
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 16: TIPS ===")
print("="*80)

tips = [
    "1. Start with feature extraction, then fine-tune if needed",
    "2. Use lower LR for pretrained layers (10x-100x lower)",
    "3. Augmentation is critical for small datasets",
    "4. Monitor for catastrophic forgetting",
    "5. Use validation set to decide when to stop",
    "6. Larger pretrained model usually better",
    "7. Match preprocessing (resize, normalize) to pretrained",
    "8. LoRA for LLMs, full FT for vision (usually)",
    "9. Evaluate on OOD data to check generalization",
    "10. Document pretrained model version and config",
]

for tip in tips:
    print(f"    {tip}")

# =====================================================================
#   PARTE 17: MULTI-TASK LEARNING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 17: MULTI-TASK ===")
print("="*80)

if HAS:
    class MultiTaskModel(nn.Module):
        def __init__(self, d_model=64):
            super().__init__()
            self.shared = nn.Sequential(
                nn.Linear(20, d_model), nn.ReLU(),
                nn.Linear(d_model, d_model), nn.ReLU())
            self.head_clf = nn.Linear(d_model, 5)
            self.head_reg = nn.Linear(d_model, 1)
        
        def forward(self, x):
            shared = self.shared(x)
            return self.head_clf(shared), self.head_reg(shared)
    
    mtl = MultiTaskModel()
    x = torch.randn(4, 20)
    clf_out, reg_out = mtl(x)
    print(f"  Multi-task: {list(x.shape)} -> clf={list(clf_out.shape)}, reg={list(reg_out.shape)}")

# =====================================================================
#   PARTE 18: CURRICULUM
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 18: CURRICULUM ===")
print("="*80)

"""
Transfer Learning curriculum:
  Phase 1: Pre-train on large dataset.
  Phase 2: Intermediate task fine-tuning (optional).
  Phase 3: Target task fine-tuning.
  Phase 4: Task-specific adaptation (LoRA/Prompt).
"""

curriculum = [
    ("Phase 1", "Pre-train", "Large corpus, self-supervised"),
    ("Phase 2", "Intermediate", "Related task, supervised"),
    ("Phase 3", "Fine-tune", "Target task, full or partial"),
    ("Phase 4", "Adapt", "LoRA/Prompt for deployment"),
]

print(f"  {'Phase':>8s} {'Stage':>14s} {'Description':>30s}")
for p, s, d in curriculum:
    print(f"  {p:>8s} {s:>14s} {d:>30s}")

# =====================================================================
#   PARTE 19: EVALUATION
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 19: EVALUATION ===")
print("="*80)

"""
Evaluating transfer learning:
  1. Compare: TL vs training from scratch.
  2. Measure: accuracy, convergence speed, data efficiency.
  3. Ablation: which layers to freeze/unfreeze.
  4. Out-of-distribution: does TL generalize better?
"""

print("  Evaluation metrics for TL:")
metrics = [
    ("Accuracy gain", "TL acc - scratch acc"),
    ("Data efficiency", "Same acc with less data"),
    ("Convergence", "Epochs to reach target acc"),
    ("OOD robustness", "Performance on shifted data"),
    ("Forgetting", "Loss on source task after FT"),
]
for m, d in metrics:
    print(f"    {m:>18s}: {d}")

# =====================================================================
#   PARTE 20: SUMMARY
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 20: SUMMARY ===")
print("="*80)

"""
TRANSFER LEARNING COMPLETE:
1. Feature extraction: freeze backbone.
2. Fine-tuning: differential LR.
3. Gradual unfreezing: layer-by-layer.
4. LoRA/QLoRA: parameter-efficient.
5. Adapters/Prefix: lightweight alternatives.
6. Distillation: teacher-student.
7. Contrastive: representation learning.
8. Multi-task: shared backbone.

FIN FASE 4: DEEP LEARNING.
"""

summary = [
    ("Feature extract", "Freeze + new head"),
    ("Fine-tune", "Diff LR, gradual unfreeze"),
    ("LoRA", "Low-rank adaptation"),
    ("QLoRA", "4-bit + LoRA"),
    ("Distillation", "Teacher -> student"),
    ("Contrastive", "SimCLR, CLIP"),
    ("PEFT", "Efficient adaptation"),
]

print(f"\n  {'Method':>16s} {'Description':>25s}")
for m, d in summary:
    print(f"  {m:>16s} {d:>25s}")


# =====================================================================
#   PARTE 21: LORA MERGING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 21: LORA MERGE ===")
print("="*80)

"""
LoRA merging: combine adapter with base weights.
  W_merged = W_original + A @ B * (alpha/rank)
  No extra latency at inference.
  Can merge multiple LoRA adapters (task arithmetic).
"""

if HAS:
    def merge_lora(lora_module):
        merged = lora_module.original.weight.data.clone()
        merged += (lora_module.lora_A @ lora_module.lora_B).T * lora_module.alpha
        return merged

    merged_w = merge_lora(lora)
    print(f"  Original weight: {lora.original.weight.shape}")
    print(f"  Merged weight:   {merged_w.shape}")
    print(f"  Diff norm: {(merged_w - lora.original.weight.data).norm():.6f}")


# =====================================================================
#   PARTE 22: CLIP CONCEPT
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 22: CLIP ===")
print("="*80)

"""
CLIP (Contrastive Language-Image Pretraining):
  Image encoder + Text encoder trained jointly.
  Contrastive loss: match image-text pairs.
  
  Zero-shot classification:
    1. Encode image.
    2. Encode text prompts ("a photo of a cat", "a photo of a dog").
    3. Pick highest similarity.
"""

if HAS:
    class MiniCLIP(nn.Module):
        def __init__(self, img_dim, text_dim, embed_dim):
            super().__init__()
            self.img_proj = nn.Linear(img_dim, embed_dim)
            self.text_proj = nn.Linear(text_dim, embed_dim)
            self.temperature = nn.Parameter(torch.tensor(0.07))

        def forward(self, img_feat, text_feat):
            img_e = F.normalize(self.img_proj(img_feat), dim=-1)
            text_e = F.normalize(self.text_proj(text_feat), dim=-1)
            logits = img_e @ text_e.T / self.temperature
            return logits

    clip = MiniCLIP(256, 128, 64)
    img = torch.randn(4, 256)
    txt = torch.randn(4, 128)
    logits = clip(img, txt)
    print(f"  CLIP logits: {list(logits.shape)}")
    print(f"  Zero-shot: pick argmax of image-text similarity")


# =====================================================================
#   PARTE 23: RLHF OVERVIEW
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 23: RLHF ===")
print("="*80)

"""
RLHF (Reinforcement Learning from Human Feedback):
  1. Supervised fine-tuning (SFT) on demonstrations.
  2. Train reward model from human preferences.
  3. Optimize policy (LLM) with PPO against reward model.

Alternatives:
  DPO: Direct Preference Optimization (no reward model).
  ORPO: Odds Ratio Preference Optimization.
  Constitutional AI: self-improvement with principles.
"""

rlhf_steps = [
    ("Step 1", "SFT", "Fine-tune on demonstrations"),
    ("Step 2", "Reward Model", "Train on preference pairs"),
    ("Step 3", "PPO", "Optimize LLM with RM signal"),
    ("Alt", "DPO", "Direct optimization, no RM"),
]

print(f"  {'Step':>8s} {'Method':>14s} {'Description':>30s}")
for s, m, d in rlhf_steps:
    print(f"  {s:>8s} {m:>14s} {d:>30s}")


# =====================================================================
#   PARTE 24: MODEL HUB
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 24: MODEL HUB ===")
print("="*80)

"""
Model Hub patterns (HuggingFace):
  1. from_pretrained(): load pretrained model.
  2. AutoModel: auto-detect architecture.
  3. Pipeline: high-level inference API.
  4. Trainer: standardized training loop.
  5. push_to_hub(): share models.
"""

print("  HuggingFace ecosystem:")
hf = [
    ("transformers", "Models + tokenizers"),
    ("datasets", "Data loading + processing"),
    ("peft", "LoRA, adapters, prefix"),
    ("trl", "RLHF training"),
    ("accelerate", "Multi-GPU, mixed precision"),
    ("evaluate", "Metrics"),
]
for lib, desc in hf:
    print(f"    {lib:>14s}: {desc}")


# =====================================================================
#   PARTE 25: DATA EFFICIENCY
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 25: DATA EFFICIENCY ===")
print("="*80)

"""
Transfer learning enables data-efficient learning:
  - 100 examples: feature extraction sufficient.
  - 1K examples: partial fine-tuning.
  - 10K examples: full fine-tuning.
  - 100K+: train from scratch may compete.
"""

if HAS:
    data_sizes = [50, 100, 500, 1000, 5000]
    print(f"  {'N samples':>10s} {'Strategy':>25s} {'Expected acc':>14s}")
    for n in data_sizes:
        if n < 100:
            strat, acc = "Feature extraction", "Low-Medium"
        elif n < 1000:
            strat, acc = "Partial fine-tune", "Medium-High"
        else:
            strat, acc = "Full fine-tune", "High"
        print(f"  {n:10d} {strat:>25s} {acc:>14s}")


# =====================================================================
#   PARTE 26: CATASTROPHIC FORGETTING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 26: FORGETTING ===")
print("="*80)

"""
Catastrophic forgetting: model forgets source task after fine-tuning.

Mitigation:
  1. Lower LR for pretrained layers.
  2. Elastic Weight Consolidation (EWC).
  3. Progressive neural networks.
  4. Replay: mix source data during fine-tuning.
  5. LoRA: don't modify original weights.
"""

print("  Anti-forgetting strategies:")
anti = [
    ("Low LR", "Simple, effective"),
    ("EWC", "Penalize changing important weights"),
    ("Replay", "Mix old data in training"),
    ("LoRA", "Weights unchanged, adapters only"),
    ("Gradual unfreeze", "Layer-by-layer, gentle"),
]
for s, d in anti:
    print(f"    {s:>16s}: {d}")


# =====================================================================
#   PARTE 27: SELF-TRAINING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 27: SELF-TRAINING ===")
print("="*80)

"""
Self-training (pseudo-labeling):
  1. Train model on labeled data.
  2. Predict labels for unlabeled data.
  3. Add high-confidence predictions to training set.
  4. Retrain. Repeat.

Works well with pretrained models as initialization.
"""

print("  Self-training pipeline:")
print("    1. Train on labeled data (with pretrained init)")
print("    2. Predict on unlabeled (confidence threshold)")
print("    3. Add pseudo-labels to training set")
print("    4. Retrain and iterate")


# =====================================================================
#   PARTE 28: PROMPT TUNING
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 28: PROMPT TUNING ===")
print("="*80)

"""
Prompt tuning vs Prompt engineering:
  Engineering: craft text prompts manually.
  Tuning: learn continuous prompt embeddings.
  
  Only ~100-1000 parameters to train.
  Model weights completely frozen.
"""

if HAS:
    class PromptTuning(nn.Module):
        def __init__(self, model, n_prompts=5, d_model=64):
            super().__init__()
            self.model = model
            for p in self.model.parameters():
                p.requires_grad = False
            self.prompts = nn.Parameter(torch.randn(n_prompts, d_model) * 0.01)

        def forward(self, x):
            B = x.size(0)
            h = self.model.emb(x)
            prompts = self.prompts.unsqueeze(0).expand(B, -1, -1)
            h = torch.cat([prompts, h], dim=1)
            h = self.model.encoder(h)
            h = h.mean(dim=1)
            return self.model.classifier(h)

    prompt_model = PromptTuning(nlp_model)
    trainable = sum(p.numel() for p in prompt_model.parameters() if p.requires_grad)
    print(f"  Prompt tuning: {trainable} trainable params")


# =====================================================================
#   PARTE 29: DEPLOYMENT
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 29: DEPLOYMENT ===")
print("="*80)

deploy = [
    "1. Merge LoRA adapters into base model",
    "2. Quantize to int8/int4 (GPTQ, AWQ, bitsandbytes)",
    "3. Export to ONNX or TensorRT",
    "4. Benchmark latency and throughput",
    "5. Set up model serving (vLLM, TGI, Triton)",
    "6. Monitor quality metrics in production",
    "7. A/B test against baseline",
    "8. Version control model + config + data",
]

for step in deploy:
    print(f"    {step}")


# =====================================================================
#   PARTE 30: FASE 4 FINAL
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 30: FASE 4 COMPLETE ===")
print("="*80)

phase4 = [
    ("Mod 17", "PyTorch Fundamentos", "Tensors, autograd, training"),
    ("Mod 18", "CNN/RNN/Transformers", "Architectures, attention"),
    ("Mod 19", "Transformer Scratch", "Full implementation"),
    ("Mod 20", "Transfer Learning", "LoRA, PEFT, distillation"),
]

print(f"\n  {'Module':>8s} {'Topic':>22s} {'Coverage':>30s}")
for m, t, c in phase4:
    print(f"  {m:>8s} {t:>22s} {c:>30s}")

print("\n  FASE 4 DEEP LEARNING: COMPLETADA")


# =====================================================================
#   PARTE 31: FULL PROJECT ARCHITECTURE
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 31: PROJECT ARCH ===")
print("="*80)

"""
Production TL project structure:

project/
├── data/
│   ├── raw/              # Original data
│   ├── processed/        # Preprocessed
│   └── splits/           # Train/val/test
├── models/
│   ├── pretrained/       # Downloaded weights
│   ├── adapters/         # LoRA checkpoints
│   └── exported/         # ONNX/TensorRT
├── src/
│   ├── data.py           # Dataset, DataLoader
│   ├── model.py          # Architecture + LoRA
│   ├── train.py          # Training loop
│   ├── evaluate.py       # Metrics
│   └── inference.py      # Serve predictions
├── configs/
│   └── experiment.yaml   # Hyperparameters
├── notebooks/            # Exploration
└── requirements.txt
"""

print("  Production project structure:")
dirs = [
    ("data/", "Raw + processed + splits"),
    ("models/", "Pretrained + adapters + exported"),
    ("src/", "Data, model, train, eval, inference"),
    ("configs/", "Experiment hyperparameters"),
]
for d, desc in dirs:
    print(f"    {d:<16s} {desc}")


# =====================================================================
#   PARTE 32: CHEATSHEET
# =====================================================================
print("\n\n" + "="*80)
print("=== CAPITULO 32: CHEATSHEET ===")
print("="*80)

cheatsheet = [
    ("Small data, similar domain", "Feature extraction"),
    ("Small data, different domain", "Fine-tune + heavy augmentation"),
    ("Medium data", "Gradual unfreezing + diff LR"),
    ("Large data", "Full fine-tune or train from scratch"),
    ("LLM adaptation", "LoRA / QLoRA"),
    ("Multiple tasks", "Multi-task with shared backbone"),
    ("No labels", "Self-training + pseudo-labels"),
    ("Model too large", "Distillation to smaller model"),
    ("Zero-shot needed", "CLIP-style contrastive"),
    ("Deployment", "Merge LoRA + quantize + ONNX"),
]

print(f"\n  {'Scenario':>30s} {'Recommended':>25s}")
for scenario, rec in cheatsheet:
    print(f"  {scenario:>30s} {rec:>25s}")

print("\n" + "="*80)
print("=== CONCLUSION ===")
print("="*80)
print("\n FIN DE ARCHIVO 01_transfer_learning.")
print(" Transfer Learning dominado.")
print(" FIN MODULO 20 / FIN FASE 4: DEEP LEARNING.")
