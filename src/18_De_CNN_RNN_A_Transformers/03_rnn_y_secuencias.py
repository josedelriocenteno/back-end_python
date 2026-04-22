# ===========================================================================
# 03_rnn_y_secuencias.py
# ===========================================================================
# MODULO 18: DE CNN/RNN A TRANSFORMERS
# ARCHIVO 03: RNN, LSTM, GRU — Procesamiento de Secuencias
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar redes recurrentes: RNN vanilla, LSTM, GRU, bidireccionales,
# attention basico, y cuando usar RNNs vs Transformers. Incluye
# implementacion from scratch y con PyTorch.
#
# CONTENIDO:
#   1. Por que RNNs: datos secuenciales.
#   2. RNN vanilla: la recurrencia basica.
#   3. El problema del vanishing gradient en RNNs.
#   4. LSTM: Long Short-Term Memory.
#   5. GRU: Gated Recurrent Unit.
#   6. Bidirectional RNNs.
#   7. Stacked/Deep RNNs.
#   8. Sequence-to-one: clasificacion de secuencias.
#   9. Sequence-to-sequence: encoder-decoder.
#   10. Attention mecanismo basico.
#   11. RNN vs Transformer: cuando usar cada uno.
#   12. Ejercicio: clasificacion de series temporales.
#
# NIVEL: DEEP LEARNING ENGINEER.
# ===========================================================================

import numpy as np
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset
    from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
    HAS_TORCH = True
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"  PyTorch: {torch.__version__}, Device: {DEVICE}")
except ImportError:
    HAS_TORCH = False
    print("  PyTorch not available.")


# =====================================================================
#   PARTE 1: POR QUE RNNS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: DATOS SECUENCIALES ===")
print("=" * 80)

"""
DATOS SECUENCIALES: el ORDEN importa.

  "El perro mordio al gato" ≠ "El gato mordio al perro"

EJEMPLOS:
  - Texto: secuencia de palabras/tokens.
  - Audio: secuencia de muestras.
  - Series temporales: precios, sensores, logs.
  - Video: secuencia de frames.
  - DNA: secuencia de nucleotidos.

POR QUE NO USAR MLP/CNN:
  MLP: no entiende orden. "abc" = "cba".
  CNN: entiende orden LOCAL (receptive field limitado).
  RNN: procesa paso a paso, manteniendo MEMORIA.

POR QUE NO USAR SIEMPRE TRANSFORMERS:
  - Para secuencias cortas (< 100 tokens): RNN puede ser mas eficiente.
  - Para streaming (tiempo real): RNN procesa token a token.
  - Para resources limitados: RNN usa menos memoria.
  - PERO: para la mayoria de tareas modernas, Transformer gana.
"""

print("""
  MLP:  [x1, x2, x3] → proceso TODO junto → output
  CNN:  [x1, x2, x3] → ventana deslizante → output
  RNN:  x1 → h1 → x2 → h2 → x3 → h3 → output
                    ↑          ↑
               memoria     memoria acumulada
""")


# =====================================================================
#   PARTE 2: RNN VANILLA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: RNN VANILLA ===")
print("=" * 80)

"""
RNN: en cada paso t, combina el input actual con la memoria anterior.

  h_t = tanh(W_xh @ x_t + W_hh @ h_{t-1} + b)

  h_t: hidden state (memoria) en el paso t.
  x_t: input en el paso t.
  W_xh: pesos input → hidden.
  W_hh: pesos hidden → hidden (la RECURRENCIA).

UNROLLED (desenrollada):
  x1  x2  x3  x4
  ↓   ↓   ↓   ↓
  h1→ h2→ h3→ h4 → output
  ↑
  h0 (zero)

PROBLEMA CRITICO: VANISHING GRADIENT.
  Al hacer backprop through time, los gradientes se multiplican
  por W_hh en CADA paso. Si |W_hh| < 1, gradientes → 0.
  Si |W_hh| > 1, gradientes → ∞.
  → La RNN NO PUEDE aprender dependencias largas.
"""

print("\n--- RNN desde cero (numpy) ---")


class RNNFromScratch:
    """RNN vanilla implementada con numpy."""

    def __init__(self, input_size, hidden_size, output_size):
        scale = 0.01
        np.random.seed(42)
        self.W_xh = np.random.randn(hidden_size, input_size) * scale
        self.W_hh = np.random.randn(hidden_size, hidden_size) * scale
        self.b_h = np.zeros(hidden_size)
        self.W_hy = np.random.randn(output_size, hidden_size) * scale
        self.b_y = np.zeros(output_size)
        self.hidden_size = hidden_size

    def forward(self, x_seq):
        """Forward pass sobre secuencia completa.
        x_seq: (seq_len, input_size)
        """
        h = np.zeros(self.hidden_size)
        hidden_states = []

        for t in range(len(x_seq)):
            h = np.tanh(self.W_xh @ x_seq[t] + self.W_hh @ h + self.b_h)
            hidden_states.append(h.copy())

        # Output del ultimo paso
        y = self.W_hy @ h + self.b_y
        return y, hidden_states


# Demo
rnn_manual = RNNFromScratch(input_size=4, hidden_size=8, output_size=2)
x_seq = np.random.randn(10, 4)  # Secuencia de 10 pasos, 4 features

output, hidden_states = rnn_manual.forward(x_seq)
print(f"  Input: secuencia de {len(x_seq)} pasos, {x_seq.shape[1]} features")
print(f"  Hidden states: {len(hidden_states)} x {len(hidden_states[0])}")
print(f"  Output: {output.shape}")
print(f"\n  Hidden state evolution (norma):")
for t in [0, 3, 6, 9]:
    print(f"    t={t}: ||h||={np.linalg.norm(hidden_states[t]):.4f}")


# =====================================================================
#   PARTE 3: VANISHING GRADIENT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: VANISHING GRADIENT ===")
print("=" * 80)

"""
EL PROBLEMA CENTRAL DE RNN VANILLA:

Para secuencia de longitud T, el gradiente respecto a h_0 es:

  ∂L/∂h_0 = ∂L/∂h_T * ∏(t=1 to T) ∂h_t/∂h_{t-1}

Cada ∂h_t/∂h_{t-1} ≈ diag(1 - tanh²) * W_hh

Si los eigenvalues de W_hh < 1:
  El producto de T matrices → 0 exponencialmente.
  → Gradientes DESAPARECEN. No aprende del pasado.

Si los eigenvalues de W_hh > 1:
  El producto → ∞ exponencialmente.
  → Gradientes EXPLOTAN. Entrenamiento inestable.

DEMOSTRACION:
"""

if HAS_TORCH:
    print("\n--- Demo: gradientes en RNN vanilla ---")

    rnn_simple = nn.RNN(input_size=4, hidden_size=32, num_layers=1, batch_first=True)

    # Secuencias de diferente longitud
    for seq_len in [10, 50, 100, 200]:
        x = torch.randn(1, seq_len, 4, requires_grad=True)
        output, h_n = rnn_simple(x)

        # Gradiente respecto al primer paso
        loss = output[:, -1, :].sum()
        loss.backward()

        grad_norm_first = x.grad[:, 0, :].norm().item()
        grad_norm_last = x.grad[:, -1, :].norm().item()
        ratio = grad_norm_first / (grad_norm_last + 1e-10)

        print(f"  seq_len={seq_len:3d}: "
              f"grad_first={grad_norm_first:.6f}, "
              f"grad_last={grad_norm_last:.6f}, "
              f"ratio={ratio:.6f}")

        x.grad = None

    print(f"\n  → A medida que la secuencia crece, el gradiente")
    print(f"    del primer paso DESAPARECE.")
    print(f"  → LSTM y GRU resuelven esto con GATES.")


# =====================================================================
#   PARTE 4: LSTM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: LSTM — LONG SHORT-TERM MEMORY ===")
print("=" * 80)

"""
LSTM (Hochreiter & Schmidhuber, 1997):

SOLUCION al vanishing gradient: CELL STATE + GATES.

Cell state (c_t): "autopista" de informacion que fluye sin
multiplicaciones por matrices de pesos. Como un conveyor belt.

3 GATES (puertas):
  FORGET gate (f_t): que BORRAR de la memoria.
    f_t = σ(W_f @ [h_{t-1}, x_t] + b_f)
    f_t ∈ (0,1). 0 = olvidar todo, 1 = recordar todo.

  INPUT gate (i_t): que AGREGAR a la memoria.
    i_t = σ(W_i @ [h_{t-1}, x_t] + b_i)
    c_candidate = tanh(W_c @ [h_{t-1}, x_t] + b_c)

  OUTPUT gate (o_t): que EXPONER como hidden state.
    o_t = σ(W_o @ [h_{t-1}, x_t] + b_o)

ACTUALIZACION:
  c_t = f_t * c_{t-1} + i_t * c_candidate
  h_t = o_t * tanh(c_t)

POR QUE FUNCIONA:
  El cell state c_t se actualiza con SUMAS, no multiplicaciones.
  → Los gradientes fluyen a traves de c_t sin degradarse.
  → Puede recordar informacion de CIENTOS de pasos atras.
"""

if HAS_TORCH:
    print("\n--- LSTM en PyTorch ---")

    # LSTM vs RNN: comparacion de gradientes
    lstm = nn.LSTM(input_size=4, hidden_size=32, num_layers=1, batch_first=True)

    print(f"  Gradientes LSTM vs RNN (seq_len=100):")
    for model_type, model in [('RNN', rnn_simple), ('LSTM', lstm)]:
        x = torch.randn(1, 100, 4, requires_grad=True)
        if model_type == 'RNN':
            output, _ = model(x)
        else:
            output, (_, _) = model(x)

        loss = output[:, -1, :].sum()
        loss.backward()

        grad_first = x.grad[:, 0, :].norm().item()
        grad_last = x.grad[:, -1, :].norm().item()
        ratio = grad_first / (grad_last + 1e-10)

        print(f"  {model_type:4s}: first={grad_first:.6f}, "
              f"last={grad_last:.6f}, ratio={ratio:.4f}")

    print(f"  → LSTM mantiene gradientes MUCHO mejor que RNN!")

    # Anatomia de un LSTM
    print(f"\n--- Anatomia del LSTM ---")
    lstm_cell = nn.LSTMCell(input_size=4, hidden_size=32)
    n_params = sum(p.numel() for p in lstm_cell.parameters())
    print(f"  LSTMCell(4, 32): {n_params} params")
    print(f"  = 4 * (input*hidden + hidden*hidden + 2*hidden)")
    print(f"  = 4 * (4*32 + 32*32 + 2*32) = {4*(4*32+32*32+2*32)}")
    print(f"  → 4x mas params que RNN simple (4 gates)")


# =====================================================================
#   PARTE 5: GRU
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: GRU — GATED RECURRENT UNIT ===")
print("=" * 80)

"""
GRU (Cho et al., 2014):

VERSION SIMPLIFICADA de LSTM. Solo 2 gates en vez de 3.

  RESET gate (r_t): cuanto del pasado usar para el candidato.
    r_t = σ(W_r @ [h_{t-1}, x_t])

  UPDATE gate (z_t): cuanto del pasado mantener.
    z_t = σ(W_z @ [h_{t-1}, x_t])

  Candidato: h_candidate = tanh(W @ [r_t * h_{t-1}, x_t])
  Output: h_t = (1 - z_t) * h_{t-1} + z_t * h_candidate

COMPARACION:
  LSTM: 3 gates + cell state. Mas expresivo.
  GRU: 2 gates, sin cell state. Mas simple, menos params.

EN LA PRACTICA: rendimiento MUY similar.
  GRU es mas rapido. LSTM tiene ligera ventaja en secuencias largas.
  Usa GRU por defecto, LSTM si no funciona.
"""

if HAS_TORCH:
    # Comparar tamaños
    rnn_4 = nn.RNN(4, 32, batch_first=True)
    lstm_4 = nn.LSTM(4, 32, batch_first=True)
    gru_4 = nn.GRU(4, 32, batch_first=True)

    print(f"\n  Parametros (input=4, hidden=32):")
    for name, model in [('RNN', rnn_4), ('LSTM', lstm_4), ('GRU', gru_4)]:
        params = sum(p.numel() for p in model.parameters())
        print(f"    {name:5s}: {params:,} params")

    print(f"  → LSTM ~4x params de RNN, GRU ~3x params de RNN")


# =====================================================================
#   PARTE 6: BIDIRECTIONAL RNNs
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: BIDIRECTIONAL RNNs ===")
print("=" * 80)

"""
BIDIRECTIONAL: procesa la secuencia en AMBAS direcciones.

  Forward:  x1 → h1→ → h2→ → h3→ → h4→
  Backward: x1 ← h1← ← h2← ← h3← ← h4←

  Output: [h_forward; h_backward] (concatenados)

POR QUE: en muchas tareas, el FUTURO tambien es informativo.
  "The cat sat on the ___": el contexto posterior ayuda.

CUANDO USAR:
  - Clasificacion de texto (ves toda la oracion).
  - NER, POS tagging.
  - Audio transcription.

CUANDO NO USAR:
  - Generacion de texto (no ves el futuro).
  - Prediccion en tiempo real.
"""

if HAS_TORCH:
    print("\n--- Bidirectional LSTM ---")

    lstm_uni = nn.LSTM(4, 32, batch_first=True, bidirectional=False)
    lstm_bi = nn.LSTM(4, 32, batch_first=True, bidirectional=True)

    x = torch.randn(2, 10, 4)  # batch=2, seq=10, feat=4

    out_uni, (h_uni, _) = lstm_uni(x)
    out_bi, (h_bi, _) = lstm_bi(x)

    print(f"  Unidirectional output: {out_uni.shape}")
    print(f"  Bidirectional output:  {out_bi.shape}")
    print(f"  → Bi duplica la dimension de salida (2 * hidden)")
    print(f"  h_n uni: {h_uni.shape}, bi: {h_bi.shape}")


# =====================================================================
#   PARTE 7: CLASIFICACION DE SECUENCIAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: SEQUENCE CLASSIFICATION ===")
print("=" * 80)

"""
SEQ → ONE: clasificar toda la secuencia en una categoria.

ESTRATEGIAS:
1. Ultimo hidden state: h_T (simple, puede perder info).
2. Max pooling sobre todos los h_t (captura el maximo).
3. Attention: ponderacion aprendida de todos los h_t.
"""

if HAS_TORCH:
    class SequenceClassifier(nn.Module):
        """Clasificador de secuencias con LSTM."""

        def __init__(self, input_size, hidden_size, num_classes,
                     num_layers=2, dropout=0.3, bidirectional=True):
            super().__init__()
            self.lstm = nn.LSTM(
                input_size, hidden_size, num_layers,
                batch_first=True, dropout=dropout if num_layers > 1 else 0,
                bidirectional=bidirectional,
            )
            direction_factor = 2 if bidirectional else 1
            self.classifier = nn.Sequential(
                nn.Linear(hidden_size * direction_factor, hidden_size),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_size, num_classes),
            )

        def forward(self, x):
            output, (h_n, _) = self.lstm(x)
            # Usar ultimo hidden state de ambas direcciones
            if self.lstm.bidirectional:
                h = torch.cat([h_n[-2], h_n[-1]], dim=1)
            else:
                h = h_n[-1]
            return self.classifier(h)

    # Dataset sintetico: clasificar tipo de serie temporal
    torch.manual_seed(42)
    n = 1000
    seq_len = 30
    n_classes = 3

    X_seq = torch.randn(n, seq_len, 4)
    y_seq = torch.randint(0, n_classes, (n,))

    # Añadir patron por clase
    for i in range(n):
        c = y_seq[i].item()
        if c == 0:
            X_seq[i, :, 0] += torch.linspace(0, 2, seq_len)  # Tendencia up
        elif c == 1:
            X_seq[i, :, 0] += torch.linspace(2, 0, seq_len)  # Tendencia down
        else:
            X_seq[i, :, 0] += torch.sin(torch.linspace(0, 4*np.pi, seq_len))

    train_seq = TensorDataset(X_seq[:800], y_seq[:800])
    val_seq = TensorDataset(X_seq[800:], y_seq[800:])
    train_ldr = DataLoader(train_seq, batch_size=64, shuffle=True)
    val_ldr = DataLoader(val_seq, batch_size=200)

    # Entrenar
    print("\n--- Sequence Classifier ---")

    model_seq = SequenceClassifier(4, 64, n_classes, num_layers=2, bidirectional=True)
    n_params = sum(p.numel() for p in model_seq.parameters())
    print(f"  Model: {n_params:,} params")

    optimizer = torch.optim.Adam(model_seq.parameters(), lr=1e-3)

    for epoch in range(20):
        model_seq.train()
        for xb, yb in train_ldr:
            optimizer.zero_grad()
            loss = nn.CrossEntropyLoss()(model_seq(xb), yb)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model_seq.parameters(), 1.0)
            optimizer.step()

        if epoch % 5 == 0:
            model_seq.eval()
            with torch.no_grad():
                correct = sum(
                    (model_seq(xb).argmax(1) == yb).sum().item()
                    for xb, yb in val_ldr
                )
                val_acc = correct / len(val_seq)
            print(f"  Epoch {epoch+1:3d}: val_acc={val_acc:.4f}")


# =====================================================================
#   PARTE 8: ATTENTION BASICO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: ATTENTION MECANISMO ===")
print("=" * 80)

"""
ATTENTION: en vez de usar solo h_T (ultimo estado),
aprende a PONDERAR todos los hidden states.

  α_t = softmax(score(h_t, query))
  context = Σ α_t * h_t

La red aprende QUE pasos de la secuencia son mas importantes.

TIPOS:
1. Additive (Bahdanau): score = V^T @ tanh(W @ [h_t; query])
2. Dot-product: score = h_t^T @ query
3. Scaled dot-product: score = (h_t^T @ query) / √d

El scaled dot-product es el que usan los Transformers.
"""

if HAS_TORCH:
    class AttentionClassifier(nn.Module):
        """LSTM + Attention para clasificacion."""

        def __init__(self, input_size, hidden_size, num_classes):
            super().__init__()
            self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True,
                                bidirectional=True)
            self.attention = nn.Linear(hidden_size * 2, 1)
            self.classifier = nn.Linear(hidden_size * 2, num_classes)

        def forward(self, x):
            outputs, _ = self.lstm(x)  # (B, T, 2*H)

            # Attention weights
            scores = self.attention(outputs).squeeze(-1)  # (B, T)
            weights = F.softmax(scores, dim=1)  # (B, T)

            # Weighted sum
            context = (weights.unsqueeze(-1) * outputs).sum(dim=1)  # (B, 2*H)

            return self.classifier(context)

    model_attn = AttentionClassifier(4, 64, n_classes)
    optimizer_attn = torch.optim.Adam(model_attn.parameters(), lr=1e-3)

    print("\n--- LSTM + Attention ---")
    for epoch in range(20):
        model_attn.train()
        for xb, yb in train_ldr:
            optimizer_attn.zero_grad()
            loss = nn.CrossEntropyLoss()(model_attn(xb), yb)
            loss.backward()
            optimizer_attn.step()

        if epoch % 5 == 0:
            model_attn.eval()
            with torch.no_grad():
                correct = sum(
                    (model_attn(xb).argmax(1) == yb).sum().item()
                    for xb, yb in val_ldr
                )
                val_acc = correct / len(val_seq)
            print(f"  Epoch {epoch+1:3d}: val_acc={val_acc:.4f}")

    # Ver attention weights
    model_attn.eval()
    with torch.no_grad():
        x_demo = X_seq[0:1]
        outputs, _ = model_attn.lstm(x_demo)
        scores = model_attn.attention(outputs).squeeze(-1)
        weights = F.softmax(scores, dim=1)

    print(f"\n  Attention weights (first 10 steps):")
    w = weights[0].numpy()
    for t in range(min(10, len(w))):
        bar = "█" * int(w[t] * 100)
        print(f"    t={t:2d}: {w[t]:.4f} {bar}")


# =====================================================================
#   PARTE 9: RNN vs TRANSFORMER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: RNN vs TRANSFORMER ===")
print("=" * 80)

"""
  COMPARACION:

  | Aspecto              | RNN/LSTM        | Transformer           |
  |----------------------|-----------------|-----------------------|
  | Secuencial           | SI (paso a paso)| NO (paralelo)         |
  | Contexto largo       | Limitado        | Ilimitado (con cost)  |
  | Velocidad training   | Lento (serial)  | Rapido (paralelo)     |
  | Velocidad inference  | OK (streaming)  | Depende               |
  | Params               | Menos           | Mas                   |
  | Performance          | Buena           | Mejor (generalmente)  |

  USAR RNN CUANDO:
  - Secuencias cortas (< 50-100 tokens).
  - Streaming/real-time (procesar token a token).
  - Recursos muy limitados.
  - Datos secuenciales simples (series temporales).

  USAR TRANSFORMER CUANDO:
  - Secuencias largas.
  - Maxima calidad importa.
  - Hay suficientes datos y compute.
  - NLP, vision, audio (practicamente todo).
"""

print("""
  TIMELINE:
  2014: LSTM/GRU dominan NLP.
  2017: "Attention is All You Need" — Transformer.
  2018: BERT, GPT — Transformers conquistan NLP.
  2020: ViT — Transformers conquistan vision.
  2023: GPT-4, LLMs — Transformers dominan TODO.

  PERO: RNNs no estan muertos.
  - Mamba (2024): alternativa eficiente a Transformers.
  - xLSTM (2024): LSTM modernizado compite con Transformers.
  - State Space Models: hibrido RNN/Transformer.
""")


# =====================================================================
#   PARTE 10: LSTM DESDE CERO (PYTORCH)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: LSTM DESDE CERO ===")
print("=" * 80)

"""
Implementar LSTMCell manual para entender las gates internamente.
Misma matematica que PyTorch pero visible paso a paso.
"""

if HAS_TORCH:
    class LSTMCellManual(nn.Module):
        """LSTM Cell implementada manualmente."""

        def __init__(self, input_size, hidden_size):
            super().__init__()
            self.hidden_size = hidden_size

            # 4 gates en una sola matrix multiplication (eficiente)
            self.W_x = nn.Linear(input_size, 4 * hidden_size)
            self.W_h = nn.Linear(hidden_size, 4 * hidden_size, bias=False)

        def forward(self, x_t, state=None):
            """
            x_t: (batch, input_size)
            state: (h, c) cada uno (batch, hidden_size)
            """
            batch_size = x_t.size(0)
            if state is None:
                h = torch.zeros(batch_size, self.hidden_size)
                c = torch.zeros(batch_size, self.hidden_size)
            else:
                h, c = state

            # Calcular las 4 gates de una vez
            gates = self.W_x(x_t) + self.W_h(h)

            # Separar en forget, input, cell_candidate, output
            f_gate = torch.sigmoid(gates[:, :self.hidden_size])
            i_gate = torch.sigmoid(gates[:, self.hidden_size:2*self.hidden_size])
            c_cand = torch.tanh(gates[:, 2*self.hidden_size:3*self.hidden_size])
            o_gate = torch.sigmoid(gates[:, 3*self.hidden_size:])

            # Actualizar cell state y hidden state
            c_new = f_gate * c + i_gate * c_cand
            h_new = o_gate * torch.tanh(c_new)

            return h_new, c_new, {
                'forget': f_gate, 'input': i_gate,
                'output': o_gate, 'candidate': c_cand,
            }

    # Demo: ver gates en accion
    print("\n--- LSTM Cell Manual ---")
    cell = LSTMCellManual(4, 16)

    x_step = torch.randn(2, 4)
    h_new, c_new, gate_info = cell(x_step)

    print(f"  Input: {x_step.shape}")
    print(f"  h_new: {h_new.shape}")
    print(f"  c_new: {c_new.shape}")
    print(f"\n  Gate activations (mean):")
    for name, vals in gate_info.items():
        print(f"    {name:>10}: {vals.mean().item():.4f} "
              f"(min={vals.min().item():.3f}, max={vals.max().item():.3f})")

    # Procesar secuencia con cell manual
    print("\n--- Secuencia con LSTM manual ---")
    seq = torch.randn(1, 20, 4)  # 1 sample, 20 steps, 4 features
    h, c = None, None
    gate_history = {'forget': [], 'input': [], 'output': []}

    for t in range(20):
        x_t = seq[:, t, :]
        if h is None:
            h_new, c_new, gates = cell(x_t)
        else:
            h_new, c_new, gates = cell(x_t, (h, c))
        h, c = h_new, c_new
        for g in gate_history:
            gate_history[g].append(gates[g].mean().item())

    print(f"  Gate means over 20 steps:")
    for g, vals in gate_history.items():
        print(f"    {g:>8}: start={vals[0]:.3f}, "
              f"mid={vals[10]:.3f}, end={vals[-1]:.3f}")


# =====================================================================
#   PARTE 11: PACKED SEQUENCES (LONGITUD VARIABLE)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: PACKED SEQUENCES ===")
print("=" * 80)

"""
EN LA PRACTICA, las secuencias tienen LONGITUDES DIFERENTES.
  "Hola" (4 chars) vs "Buenos dias mundo" (17 chars)

SOLUCION NAIVE: pad con zeros hasta la longitud maxima.
  → Desperdicia compute procesando zeros.

SOLUCION CORRECTA: pack_padded_sequence / pad_packed_sequence.
  → PyTorch procesa SOLO los tokens reales.
  → Mas eficiente y correcto (el padding no afecta al output).
"""

if HAS_TORCH:
    print("\n--- Packed Sequences ---")

    # Simular batch de secuencias de longitud variable
    sequences = [
        torch.randn(15, 4),  # Secuencia de 15 pasos
        torch.randn(10, 4),  # Secuencia de 10 pasos
        torch.randn(7, 4),   # Secuencia de 7 pasos
    ]
    lengths = [15, 10, 7]

    # Pad: todas a longitud 15
    padded = torch.nn.utils.rnn.pad_sequence(sequences, batch_first=True)
    print(f"  Padded batch: {padded.shape}")  # (3, 15, 4)

    # Pack
    packed = pack_padded_sequence(padded, lengths, batch_first=True,
                                  enforce_sorted=True)
    print(f"  Packed data: {packed.data.shape}")
    print(f"  Packed batch_sizes: {packed.batch_sizes}")

    # Pasar por LSTM
    lstm_pack = nn.LSTM(4, 32, batch_first=True)
    output_packed, (h_n, c_n) = lstm_pack(packed)

    # Unpack
    output_padded, output_lengths = pad_packed_sequence(
        output_packed, batch_first=True
    )
    print(f"  Output unpacked: {output_padded.shape}")
    print(f"  Output lengths: {output_lengths.tolist()}")
    print(f"  → Cada secuencia procesada con su longitud real")


# =====================================================================
#   PARTE 12: ENCODER-DECODER (SEQ2SEQ)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: ENCODER-DECODER ===")
print("=" * 80)

"""
SEQ2SEQ: transformar una secuencia en OTRA secuencia.

  Encoder: input → hidden state (contexto)
  Decoder: hidden state → output secuencia

APLICACIONES:
  - Traduccion: "Hello" → "Hola"
  - Summarizacion: texto largo → resumen
  - Chatbots: pregunta → respuesta

ARQUITECTURA:
  Encoder LSTM procesa input → ultimo h,c = contexto
  Decoder LSTM genera output paso a paso usando el contexto
"""

if HAS_TORCH:
    class Seq2SeqEncoder(nn.Module):
        def __init__(self, input_size, hidden_size, num_layers=1):
            super().__init__()
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                                batch_first=True)

        def forward(self, x):
            _, (h_n, c_n) = self.lstm(x)
            return h_n, c_n

    class Seq2SeqDecoder(nn.Module):
        def __init__(self, output_size, hidden_size, num_layers=1):
            super().__init__()
            self.lstm = nn.LSTM(output_size, hidden_size, num_layers,
                                batch_first=True)
            self.fc = nn.Linear(hidden_size, output_size)

        def forward(self, x, hidden):
            output, hidden = self.lstm(x, hidden)
            prediction = self.fc(output)
            return prediction, hidden

    class Seq2Seq(nn.Module):
        def __init__(self, input_size, output_size, hidden_size):
            super().__init__()
            self.encoder = Seq2SeqEncoder(input_size, hidden_size)
            self.decoder = Seq2SeqDecoder(output_size, hidden_size)
            self.output_size = output_size

        def forward(self, src, tgt_len):
            # Encode
            h, c = self.encoder(src)

            # Decode (autoregressive)
            batch_size = src.size(0)
            decoder_input = torch.zeros(batch_size, 1, self.output_size)
            outputs = []

            for t in range(tgt_len):
                out, (h, c) = self.decoder(decoder_input, (h, c))
                outputs.append(out)
                decoder_input = out

            return torch.cat(outputs, dim=1)

    # Demo
    print("\n--- Seq2Seq ---")
    s2s = Seq2Seq(input_size=4, output_size=2, hidden_size=64)
    n_params = sum(p.numel() for p in s2s.parameters())

    src = torch.randn(3, 10, 4)  # batch=3, src_len=10, features=4
    out = s2s(src, tgt_len=5)

    print(f"  Model: {n_params:,} params")
    print(f"  Source: {src.shape}")
    print(f"  Output: {out.shape}")
    print(f"  → Transforma seq(10,4) → seq(5,2)")


# =====================================================================
#   PARTE 13: TIME SERIES FORECASTING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: TIME SERIES FORECASTING ===")
print("=" * 80)

"""
PREDICCION DE SERIES TEMPORALES con LSTM:
  Dado: x_1, x_2, ..., x_T
  Predecir: x_{T+1}, ..., x_{T+H}

TECNICAS:
  1. Direct: predecir H pasos directamente.
  2. Recursive: predecir 1 paso, alimentar como input, repetir.
  3. Seq2Seq: encoder-decoder para multi-step.
"""

if HAS_TORCH:
    print("\n--- Time Series Forecasting ---")

    # Generar serie temporal sinusoidal
    torch.manual_seed(42)
    t = torch.linspace(0, 20 * np.pi, 1000)
    series = torch.sin(t) + 0.5 * torch.sin(3 * t) + 0.1 * torch.randn(1000)

    # Crear ventanas: input=30 pasos, output=5 pasos
    window_in, window_out = 30, 5
    X_ts, y_ts = [], []
    for i in range(len(series) - window_in - window_out):
        X_ts.append(series[i:i+window_in])
        y_ts.append(series[i+window_in:i+window_in+window_out])

    X_ts = torch.stack(X_ts).unsqueeze(-1)  # (N, 30, 1)
    y_ts = torch.stack(y_ts)                # (N, 5)

    # Split
    n_train = int(0.8 * len(X_ts))
    train_ts = TensorDataset(X_ts[:n_train], y_ts[:n_train])
    val_ts = TensorDataset(X_ts[n_train:], y_ts[n_train:])
    train_ts_ldr = DataLoader(train_ts, batch_size=64, shuffle=True)
    val_ts_ldr = DataLoader(val_ts, batch_size=256)

    class TimeSeriesLSTM(nn.Module):
        def __init__(self, hidden=64, forecast=5):
            super().__init__()
            self.lstm = nn.LSTM(1, hidden, num_layers=2,
                                batch_first=True, dropout=0.2)
            self.head = nn.Linear(hidden, forecast)

        def forward(self, x):
            out, _ = self.lstm(x)
            return self.head(out[:, -1, :])

    model_ts = TimeSeriesLSTM(hidden=64, forecast=5)
    opt_ts = torch.optim.Adam(model_ts.parameters(), lr=1e-3)

    for epoch in range(30):
        model_ts.train()
        for xb, yb in train_ts_ldr:
            opt_ts.zero_grad()
            loss = nn.MSELoss()(model_ts(xb), yb)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model_ts.parameters(), 1.0)
            opt_ts.step()

        if epoch % 10 == 0:
            model_ts.eval()
            with torch.no_grad():
                val_loss = sum(
                    nn.MSELoss()(model_ts(xb), yb).item()
                    for xb, yb in val_ts_ldr
                ) / len(val_ts_ldr)
            print(f"  Epoch {epoch+1:3d}: val_MSE={val_loss:.4f}")

    # Prediccion de ejemplo
    model_ts.eval()
    with torch.no_grad():
        sample = X_ts[n_train:n_train+1]
        pred = model_ts(sample)
        actual = y_ts[n_train]
    print(f"\n  Prediccion 5 pasos:")
    print(f"    Real:    {actual.numpy().round(3)}")
    print(f"    Pred:    {pred[0].numpy().round(3)}")
    print(f"    Error:   {(pred[0] - actual).abs().numpy().round(3)}")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: RNN Y SECUENCIAS ===")
print("=" * 80)

print("""
  JERARQUIA DE REDES RECURRENTES:

  RNN Vanilla → problema vanishing gradient
      ↓
  LSTM → 3 gates + cell state → resuelve vanishing
  GRU  → 2 gates, mas simple, rendimiento similar
      ↓
  Bidirectional → ve pasado Y futuro
  Deep/Stacked → multiples capas para features mas abstractas
      ↓
  + Attention → aprende QUE pasos importan
      ↓
  Transformer → SOLO attention, sin recurrencia

  APLICACIONES:
  1. Seq→One: clasificacion de secuencias (BiLSTM + Attention).
  2. Seq→Seq: traduccion, summarization (Encoder-Decoder).
  3. Time Series: forecasting con LSTM multi-step.

  RECETA:
  1. Default: BiLSTM 2 capas + Attention.
  2. Gradient clipping = 1.0 (SIEMPRE con RNNs).
  3. Dropout entre capas LSTM (no dentro).
  4. Pack/pad sequences para batches de longitud variable.
  5. Si no funciona → usa Transformer.
""")

print("=" * 80)
print("=== FIN MODULO 18, ARCHIVO 03 ===")
print("=" * 80)

