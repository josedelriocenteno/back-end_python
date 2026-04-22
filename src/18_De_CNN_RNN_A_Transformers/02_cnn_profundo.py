# ===========================================================================
# 02_cnn_profundo.py
# ===========================================================================
# MODULO 18: DE CNN/RNN A TRANSFORMERS
# ARCHIVO 02: CNN en Profundidad — Convoluciones, Pooling, Arquitecturas
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar CNNs desde los fundamentos: convolucion como operacion,
# tipos de padding y stride, pooling, arquitecturas clasicas
# (LeNet, VGG, ResNet), residual connections, y patrones modernos.
#
# CONTENIDO:
#   1. Convolucion: la operacion matematica.
#   2. Convolucion en PyTorch: nn.Conv2d.
#   3. Padding, stride, dilation.
#   4. Pooling: MaxPool, AvgPool, AdaptivePool.
#   5. Arquitectura LeNet-5 (clasica).
#   6. VGG: profundidad con bloques repetidos.
#   7. ResNet: residual connections (la innovacion clave).
#   8. Bottleneck blocks.
#   9. Batch Norm en CNNs.
#   10. Modern CNN patterns: SE blocks, depthwise separable.
#   11. CNN para clasificacion completa.
#   12. Feature extraction y visualizacion.
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
    HAS_TORCH = True
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"  PyTorch: {torch.__version__}, Device: {DEVICE}")
except ImportError:
    HAS_TORCH = False
    print("  PyTorch not available.")


# =====================================================================
#   PARTE 1: CONVOLUCION — LA OPERACION MATEMATICA
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: CONVOLUCION ===")
print("=" * 80)

"""
CONVOLUCION: deslizar un FILTRO (kernel) sobre la imagen,
multiplicar elemento a elemento, y sumar.

  Input (5x5)     Kernel (3x3)     Output (3x3)
  1 0 1 0 1       1  0  1          ?  ?  ?
  0 1 0 1 0       0  1  0          ?  ?  ?
  1 0 1 0 1       1  0  1          ?  ?  ?
  0 1 0 1 0
  1 0 1 0 1

  Output[0,0] = sum(Input[0:3, 0:3] * Kernel) = 1+0+1+0+1+0+1+0+1 = 5

POR QUE CONVOLUCION EN VEZ DE FULLY CONNECTED:
1. PARAMETER SHARING: el mismo filtro se aplica a toda la imagen.
   FC con imagen 224x224x3: 150K params por neurona.
   Conv 3x3: 27 params por filtro. ENORME ahorro.

2. TRANSLATION EQUIVARIANCE: si el gato se mueve,
   la activacion se mueve con el. No necesita re-aprender.

3. LOCALITY: cada neurona solo ve un area local (receptive field).
   Features locales (bordes, texturas) son lo que importa.
"""

# Convolucion manual con numpy
print("\n--- Convolucion manual (numpy) ---")

def conv2d_manual(image, kernel):
    """Convolucion 2D sin padding."""
    h, w = image.shape
    kh, kw = kernel.shape
    oh, ow = h - kh + 1, w - kw + 1
    output = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            patch = image[i:i+kh, j:j+kw]
            output[i, j] = np.sum(patch * kernel)
    return output

# Imagen 5x5
image = np.array([
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
], dtype=float)

# Filtro detector de bordes horizontales
edge_h = np.array([
    [-1, -1, -1],
    [ 0,  0,  0],
    [ 1,  1,  1],
], dtype=float)

# Filtro detector de bordes verticales
edge_v = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1],
], dtype=float)

result_h = conv2d_manual(image, edge_h)
result_v = conv2d_manual(image, edge_v)

print(f"  Input (5x5):\n{image}")
print(f"\n  Edge horizontal (3x3):\n{result_h}")
print(f"\n  Edge vertical (3x3):\n{result_v}")
print(f"\n  → Cada filtro detecta un PATRON especifico")


# =====================================================================
#   PARTE 2: CONVOLUCION EN PYTORCH
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: nn.Conv2d ===")
print("=" * 80)

"""
nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)

PARAMETROS CLAVE:
  in_channels: canales de entrada (3 para RGB, 1 para grayscale).
  out_channels: numero de filtros (= numero de feature maps de salida).
  kernel_size: tamaño del filtro (3, 5, 7...).
  stride: paso del deslizamiento (1 = pixel a pixel, 2 = saltar 1).
  padding: pixeles de borde añadidos.

FORMULA DE TAMAÑO DE SALIDA:
  H_out = (H_in + 2*padding - kernel_size) / stride + 1

EJEMPLO:
  Input: 32x32, kernel=3, padding=1, stride=1
  H_out = (32 + 2 - 3) / 1 + 1 = 32  (mismo tamaño!)

  Input: 32x32, kernel=3, padding=0, stride=2
  H_out = (32 + 0 - 3) / 2 + 1 = 15  (reduce tamaño!)
"""

if HAS_TORCH:
    print("\n--- Conv2d en PyTorch ---")

    # Formato: (batch, channels, height, width)
    x = torch.randn(1, 3, 32, 32)  # 1 imagen RGB 32x32
    print(f"  Input: {x.shape}")

    # Diferentes configuraciones
    configs = [
        ("3x3, pad=0, stride=1", nn.Conv2d(3, 16, 3, stride=1, padding=0)),
        ("3x3, pad=1, stride=1", nn.Conv2d(3, 16, 3, stride=1, padding=1)),
        ("3x3, pad=1, stride=2", nn.Conv2d(3, 16, 3, stride=1, padding=1)),
        ("5x5, pad=2, stride=1", nn.Conv2d(3, 16, 5, stride=1, padding=2)),
        ("1x1, pad=0, stride=1", nn.Conv2d(3, 16, 1, stride=1, padding=0)),
    ]

    for name, conv in configs:
        out = conv(x)
        n_params = sum(p.numel() for p in conv.parameters())
        print(f"  {name:<22} → {str(out.shape):<25} params={n_params}")

    # 1x1 convolution: cambia canales sin cambiar tamaño
    print(f"\n  1x1 conv: 'red de canales'. Muy usada en ResNet/Inception.")
    print(f"  Reduce dimensionalidad de canales (ej: 256 → 64).")


# =====================================================================
#   PARTE 3: PADDING, STRIDE, DILATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: PADDING, STRIDE, DILATION ===")
print("=" * 80)

"""
PADDING:
  'valid' (padding=0): output es mas pequeno que input.
  'same' (padding=k//2): output MISMO tamaño que input (con stride=1).

STRIDE:
  stride=1: output casi del mismo tamaño.
  stride=2: output la MITAD del tamaño. Reemplaza MaxPool en redes modernas.

DILATION:
  Expande el kernel insertando huecos.
  dilation=2 con kernel 3x3: receptive field de 5x5 con 9 params.
  Util en segmentacion (captura contexto amplio sin perder resolucion).
"""

if HAS_TORCH:
    x = torch.randn(1, 1, 16, 16)

    configs_pad = {
        "No padding": nn.Conv2d(1, 1, 3, padding=0),
        "Same padding": nn.Conv2d(1, 1, 3, padding=1),
        "Stride=2": nn.Conv2d(1, 1, 3, padding=1, stride=2),
        "Dilation=2": nn.Conv2d(1, 1, 3, padding=2, dilation=2),
    }

    print(f"\n  Input: {x.shape[2]}x{x.shape[3]}")
    for name, conv in configs_pad.items():
        out = conv(x)
        print(f"  {name:<16} → {out.shape[2]}x{out.shape[3]}")


# =====================================================================
#   PARTE 4: POOLING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: POOLING ===")
print("=" * 80)

"""
POOLING: reduce tamaño espacial, mantiene features importantes.

TIPOS:
1. MaxPool: toma el MAXIMO de cada ventana.
   → Detecta si la feature EXISTE (invarianza a posicion exacta).

2. AvgPool: toma la MEDIA de cada ventana.
   → Suaviza features. Menos agresivo que MaxPool.

3. AdaptiveAvgPool: output de tamaño FIJO independiente del input.
   → Permite que la red acepte imagenes de CUALQUIER tamaño.

4. Global Average Pooling (GAP): AdaptiveAvgPool(1,1).
   → Reemplaza las capas FC finales. Menos params, menos overfitting.
"""

if HAS_TORCH:
    x = torch.randn(1, 16, 32, 32)
    print(f"\n  Input: {x.shape}")

    pools = {
        "MaxPool2d(2)": nn.MaxPool2d(2),
        "AvgPool2d(2)": nn.AvgPool2d(2),
        "AdaptiveAvg(8,8)": nn.AdaptiveAvgPool2d((8, 8)),
        "AdaptiveAvg(1,1)": nn.AdaptiveAvgPool2d((1, 1)),  # GAP
    }

    for name, pool in pools.items():
        out = pool(x)
        print(f"  {name:<22} → {out.shape}")

    print(f"\n  GAP (1x1): de (B, C, H, W) → (B, C, 1, 1)")
    print(f"  → Elimina dimension espacial, deja solo canales")
    print(f"  → Cada canal = respuesta de un filtro")


# =====================================================================
#   PARTE 5: LeNet-5
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: LeNet-5 (1998) ===")
print("=" * 80)

"""
LeNet-5 (Yann LeCun, 1998):
  La PRIMERA CNN exitosa. Usada para leer digitos postales.

  Input (1x32x32) → Conv(6, 5x5) → Pool → Conv(16, 5x5) → Pool
  → Flatten → FC(120) → FC(84) → FC(10)

  Solo ~60K parametros. Hoy es un juguete,
  pero establecio la ARQUITECTURA base de todas las CNNs.
"""

if HAS_TORCH:
    class LeNet5(nn.Module):
        def __init__(self, num_classes=10):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(1, 6, 5, padding=2),   # 32→32
                nn.Tanh(),
                nn.AvgPool2d(2),                   # 32→16
                nn.Conv2d(6, 16, 5),               # 16→12
                nn.Tanh(),
                nn.AvgPool2d(2),                   # 12→6
            )
            self.classifier = nn.Sequential(
                nn.Linear(16 * 6 * 6, 120),
                nn.Tanh(),
                nn.Linear(120, 84),
                nn.Tanh(),
                nn.Linear(84, num_classes),
            )

        def forward(self, x):
            x = self.features(x)
            x = x.flatten(1)
            return self.classifier(x)

    lenet = LeNet5()
    x = torch.randn(1, 1, 32, 32)
    out = lenet(x)
    n_params = sum(p.numel() for p in lenet.parameters())
    print(f"\n  LeNet-5: {n_params:,} params")
    print(f"  Input: {x.shape} → Output: {out.shape}")


# =====================================================================
#   PARTE 6: VGG — PROFUNDIDAD CON BLOQUES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: VGG (2014) ===")
print("=" * 80)

"""
VGG (Simonyan & Zisserman, 2014):
  IDEA: usa SOLO 3x3 convolutions, pero MUCHAS capas.
  Dos 3x3 convs = receptive field de 5x5 con MENOS params.
  Tres 3x3 convs = receptive field de 7x7.

  PATRON: [Conv3x3]*N → MaxPool → [Conv3x3]*N → MaxPool → ...

  VGG-16: 16 capas. ~138M params. MUY grande pero simple.
"""

if HAS_TORCH:
    def make_vgg_block(in_ch, out_ch, n_convs):
        layers = []
        for i in range(n_convs):
            layers.append(nn.Conv2d(in_ch if i == 0 else out_ch, out_ch, 3, padding=1))
            layers.append(nn.BatchNorm2d(out_ch))
            layers.append(nn.ReLU(inplace=True))
        layers.append(nn.MaxPool2d(2))
        return nn.Sequential(*layers)

    class MiniVGG(nn.Module):
        """VGG simplificado para demostracion."""
        def __init__(self, num_classes=10):
            super().__init__()
            self.features = nn.Sequential(
                make_vgg_block(1, 32, 2),    # 32→16
                make_vgg_block(32, 64, 2),   # 16→8
                make_vgg_block(64, 128, 3),  # 8→4
            )
            self.classifier = nn.Sequential(
                nn.AdaptiveAvgPool2d(1),
                nn.Flatten(),
                nn.Linear(128, num_classes),
            )

        def forward(self, x):
            return self.classifier(self.features(x))

    vgg = MiniVGG()
    x = torch.randn(1, 1, 32, 32)
    out = vgg(x)
    n_params = sum(p.numel() for p in vgg.parameters())
    print(f"\n  MiniVGG: {n_params:,} params")
    print(f"  Input: {x.shape} → Output: {out.shape}")


# =====================================================================
#   PARTE 7: RESNET — RESIDUAL CONNECTIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: ResNet — LA INNOVACION CLAVE ===")
print("=" * 80)

"""
RESNET (He et al., 2015):

PROBLEMA: redes mas profundas deberian ser MEJORES,
pero en la practica, redes de 50+ capas eran PEORES que de 20.
¿Por que? Degradation problem (no es overfitting).

SOLUCION: RESIDUAL CONNECTION (skip connection).

  En vez de aprender: y = F(x)
  Aprende: y = F(x) + x   (el residuo)

  Si F(x) = 0, entonces y = x → la identidad.
  → La red SIEMPRE puede aprender la identidad.
  → Nunca es PEOR que una red mas shallow.

INTUICION: es mas facil aprender "cuanto cambiar" (residuo)
que aprender "que valor producir" desde cero.

IMPACTO: hizo posible redes de 100, 1000+ capas.
Todas las redes modernas usan skip connections
(Transformers, U-Net, DenseNet...).
"""

if HAS_TORCH:
    class ResidualBlock(nn.Module):
        """Bloque residual basico de ResNet."""

        def __init__(self, in_channels, out_channels, stride=1):
            super().__init__()
            self.conv1 = nn.Conv2d(in_channels, out_channels, 3,
                                   stride=stride, padding=1, bias=False)
            self.bn1 = nn.BatchNorm2d(out_channels)
            self.conv2 = nn.Conv2d(out_channels, out_channels, 3,
                                   stride=1, padding=1, bias=False)
            self.bn2 = nn.BatchNorm2d(out_channels)

            # Shortcut: si cambian dimensiones, necesitamos 1x1 conv
            self.shortcut = nn.Sequential()
            if stride != 1 or in_channels != out_channels:
                self.shortcut = nn.Sequential(
                    nn.Conv2d(in_channels, out_channels, 1,
                              stride=stride, bias=False),
                    nn.BatchNorm2d(out_channels),
                )

        def forward(self, x):
            residual = self.shortcut(x)    # Skip connection
            out = F.relu(self.bn1(self.conv1(x)))
            out = self.bn2(self.conv2(out))
            out = F.relu(out + residual)    # F(x) + x
            return out

    class MiniResNet(nn.Module):
        """ResNet simplificado."""

        def __init__(self, num_classes=10):
            super().__init__()
            self.stem = nn.Sequential(
                nn.Conv2d(1, 32, 3, padding=1, bias=False),
                nn.BatchNorm2d(32),
                nn.ReLU(inplace=True),
            )
            self.layer1 = self._make_layer(32, 32, 2, stride=1)
            self.layer2 = self._make_layer(32, 64, 2, stride=2)
            self.layer3 = self._make_layer(64, 128, 2, stride=2)

            self.head = nn.Sequential(
                nn.AdaptiveAvgPool2d(1),
                nn.Flatten(),
                nn.Linear(128, num_classes),
            )

        def _make_layer(self, in_ch, out_ch, n_blocks, stride):
            layers = [ResidualBlock(in_ch, out_ch, stride)]
            for _ in range(1, n_blocks):
                layers.append(ResidualBlock(out_ch, out_ch, 1))
            return nn.Sequential(*layers)

        def forward(self, x):
            x = self.stem(x)
            x = self.layer1(x)
            x = self.layer2(x)
            x = self.layer3(x)
            return self.head(x)

    resnet = MiniResNet()
    x = torch.randn(1, 1, 32, 32)
    out = resnet(x)
    n_params = sum(p.numel() for p in resnet.parameters())
    print(f"\n  MiniResNet: {n_params:,} params")
    print(f"  Input: {x.shape} → Output: {out.shape}")

    # Verificar que gradientes fluyen
    loss = out.sum()
    loss.backward()
    grad_norms = []
    for name, p in resnet.named_parameters():
        if p.grad is not None:
            grad_norms.append((name, p.grad.norm().item()))
    print(f"\n  Gradient flow (primeras y ultimas capas):")
    for name, norm in grad_norms[:3] + grad_norms[-3:]:
        print(f"    {name:<35} grad_norm={norm:.6f}")
    print(f"  → Gradientes fluyen bien gracias a skip connections!")


# =====================================================================
#   PARTE 8: BOTTLENECK BLOCKS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: BOTTLENECK BLOCKS ===")
print("=" * 80)

"""
BOTTLENECK: reducir dimensionalidad antes de la conv costosa.

BLOQUE BASICO (ResNet-18/34):
  Conv3x3 → BN → ReLU → Conv3x3 → BN → (+skip) → ReLU

BLOQUE BOTTLENECK (ResNet-50/101/152):
  Conv1x1 (reduce canales) → BN → ReLU
  Conv3x3 (procesa) → BN → ReLU
  Conv1x1 (expande canales) → BN → (+skip) → ReLU

  1x1 conv de 256 → 64: reduce 4x los canales.
  3x3 conv de 64 → 64: convolucion real (barata ahora).
  1x1 conv de 64 → 256: restaura canales.

  → MUCHOS menos parametros que 3x3 directo en 256 canales.
"""

if HAS_TORCH:
    class BottleneckBlock(nn.Module):
        """Bottleneck residual block (ResNet-50+)."""

        EXPANSION = 4

        def __init__(self, in_channels, bottleneck_channels, stride=1):
            super().__init__()
            out_channels = bottleneck_channels * self.EXPANSION

            self.conv1 = nn.Conv2d(in_channels, bottleneck_channels, 1, bias=False)
            self.bn1 = nn.BatchNorm2d(bottleneck_channels)
            self.conv2 = nn.Conv2d(bottleneck_channels, bottleneck_channels, 3,
                                   stride=stride, padding=1, bias=False)
            self.bn2 = nn.BatchNorm2d(bottleneck_channels)
            self.conv3 = nn.Conv2d(bottleneck_channels, out_channels, 1, bias=False)
            self.bn3 = nn.BatchNorm2d(out_channels)

            self.shortcut = nn.Sequential()
            if stride != 1 or in_channels != out_channels:
                self.shortcut = nn.Sequential(
                    nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
                    nn.BatchNorm2d(out_channels),
                )

        def forward(self, x):
            residual = self.shortcut(x)
            out = F.relu(self.bn1(self.conv1(x)))
            out = F.relu(self.bn2(self.conv2(out)))
            out = self.bn3(self.conv3(out))
            return F.relu(out + residual)

    # Comparar params
    basic = ResidualBlock(256, 256)
    bottleneck = BottleneckBlock(256, 64)

    basic_params = sum(p.numel() for p in basic.parameters())
    bottleneck_params = sum(p.numel() for p in bottleneck.parameters())

    print(f"\n  Basic block (256→256):      {basic_params:,} params")
    print(f"  Bottleneck (256→64→256):    {bottleneck_params:,} params")
    print(f"  Ahorro: {(1 - bottleneck_params/basic_params)*100:.0f}%")
    print(f"  → Bottleneck es mas eficiente con muchos canales")


# =====================================================================
#   PARTE 9: SE (SQUEEZE-AND-EXCITATION) BLOCKS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: SQUEEZE-AND-EXCITATION ===")
print("=" * 80)

"""
SE BLOCK (Hu et al., 2017): atencion POR CANAL.

IDEA: no todos los canales son igualmente importantes.
SE aprende un peso de importancia para cada canal.

  Input (B, C, H, W)
  → Squeeze: GAP → (B, C, 1, 1) → (B, C)
  → Excitation: FC → ReLU → FC → Sigmoid → (B, C)
  → Scale: multiply input por pesos → (B, C, H, W)

Costo computacional: insignificante (dos FC pequenas).
Beneficio: +1-2% accuracy. GRATIS.
"""

if HAS_TORCH:
    class SEBlock(nn.Module):
        """Squeeze-and-Excitation block."""

        def __init__(self, channels, reduction=16):
            super().__init__()
            self.squeeze = nn.AdaptiveAvgPool2d(1)
            self.excitation = nn.Sequential(
                nn.Linear(channels, channels // reduction, bias=False),
                nn.ReLU(inplace=True),
                nn.Linear(channels // reduction, channels, bias=False),
                nn.Sigmoid(),
            )

        def forward(self, x):
            b, c, _, _ = x.shape
            # Squeeze: (B, C, H, W) → (B, C)
            y = self.squeeze(x).view(b, c)
            # Excitation: (B, C) → (B, C) pesos
            y = self.excitation(y).view(b, c, 1, 1)
            # Scale: reponderar canales
            return x * y

    se = SEBlock(64, reduction=16)
    x = torch.randn(2, 64, 16, 16)
    out = se(x)
    se_params = sum(p.numel() for p in se.parameters())
    print(f"\n  SE block: {se_params} params extra para {64} canales")
    print(f"  Input: {x.shape} → Output: {out.shape} (mismo tamaño)")
    print(f"  → Aprende que canales son mas importantes")


# =====================================================================
#   PARTE 10: DEPTHWISE SEPARABLE CONVOLUTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: DEPTHWISE SEPARABLE CONV ===")
print("=" * 80)

"""
DEPTHWISE SEPARABLE (MobileNet, 2017):

Conv normal 3x3 de C_in → C_out:
  Params = C_in * C_out * 3 * 3

Depthwise separable = 2 pasos:
  1. DEPTHWISE: conv 3x3 SEPARADA por canal (groups=C_in).
     Params = C_in * 3 * 3
  2. POINTWISE: conv 1x1 para mezclar canales.
     Params = C_in * C_out

Total: C_in*9 + C_in*C_out vs C_in*C_out*9
  → ~9x menos parametros!

USO: redes para moviles (MobileNet, EfficientNet).
"""

if HAS_TORCH:
    class DepthwiseSeparableConv(nn.Module):
        """Depthwise separable convolution."""

        def __init__(self, in_ch, out_ch, kernel_size=3, stride=1, padding=1):
            super().__init__()
            self.depthwise = nn.Conv2d(
                in_ch, in_ch, kernel_size, stride=stride,
                padding=padding, groups=in_ch, bias=False
            )
            self.pointwise = nn.Conv2d(in_ch, out_ch, 1, bias=False)
            self.bn = nn.BatchNorm2d(out_ch)

        def forward(self, x):
            x = self.depthwise(x)
            x = self.pointwise(x)
            return F.relu(self.bn(x))

    # Comparar
    normal_conv = nn.Conv2d(64, 128, 3, padding=1)
    dw_conv = DepthwiseSeparableConv(64, 128)

    normal_params = sum(p.numel() for p in normal_conv.parameters())
    dw_params = sum(p.numel() for p in dw_conv.parameters())

    print(f"\n  Conv normal (64→128, 3x3):   {normal_params:,} params")
    print(f"  Depthwise separable:          {dw_params:,} params")
    print(f"  Reduccion: {normal_params/dw_params:.1f}x menos params")


# =====================================================================
#   PARTE 11: CNN COMPLETA — ENTRENAMIENTO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: CNN COMPLETA ===")
print("=" * 80)

"""
CNN moderna para clasificacion con todas las best practices:
- ResNet-style con residual blocks.
- BatchNorm + ReLU.
- Global Average Pooling (sin FC grandes).
- Data: generamos imagenes sinteticas para demo.
"""

if HAS_TORCH:
    class ModernCNN(nn.Module):
        """CNN moderna con residuals, BN, GAP."""

        def __init__(self, in_channels=1, num_classes=10):
            super().__init__()
            self.stem = nn.Sequential(
                nn.Conv2d(in_channels, 32, 3, padding=1, bias=False),
                nn.BatchNorm2d(32),
                nn.ReLU(inplace=True),
            )

            self.stage1 = nn.Sequential(
                ResidualBlock(32, 64, stride=2),
                ResidualBlock(64, 64),
            )
            self.stage2 = nn.Sequential(
                ResidualBlock(64, 128, stride=2),
                ResidualBlock(128, 128),
            )

            self.head = nn.Sequential(
                nn.AdaptiveAvgPool2d(1),
                nn.Flatten(),
                nn.Dropout(0.2),
                nn.Linear(128, num_classes),
            )

        def forward(self, x):
            x = self.stem(x)
            x = self.stage1(x)
            x = self.stage2(x)
            return self.head(x)

    # Datos sinteticos (imagenes 16x16 con patrones)
    torch.manual_seed(42)
    n_samples = 2000
    n_classes = 5

    # Crear imagenes con patrones distinguibles
    X_img = torch.randn(n_samples, 1, 16, 16)
    y_img = torch.randint(0, n_classes, (n_samples,))

    # Añadir patron de clase
    for i in range(n_samples):
        c = y_img[i].item()
        X_img[i, 0, c*3:(c+1)*3, :] += 2.0  # Banda horizontal por clase

    # Split
    train_imgs = TensorDataset(X_img[:1600], y_img[:1600])
    val_imgs = TensorDataset(X_img[1600:], y_img[1600:])
    train_ldr = DataLoader(train_imgs, batch_size=64, shuffle=True)
    val_ldr = DataLoader(val_imgs, batch_size=256)

    # Entrenar
    print("\n--- Entrenando ModernCNN ---")

    model_cnn = ModernCNN(in_channels=1, num_classes=n_classes)
    n_params = sum(p.numel() for p in model_cnn.parameters())
    print(f"  Modelo: {n_params:,} params")

    optimizer = torch.optim.AdamW(model_cnn.parameters(), lr=1e-3, weight_decay=0.01)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(20):
        model_cnn.train()
        total_loss = 0
        for xb, yb in train_ldr:
            optimizer.zero_grad()
            loss = criterion(model_cnn(xb), yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        if epoch % 5 == 0:
            model_cnn.eval()
            with torch.no_grad():
                correct = sum(
                    (model_cnn(xb).argmax(1) == yb).sum().item()
                    for xb, yb in val_ldr
                )
                val_acc = correct / len(val_imgs)
            print(f"  Epoch {epoch+1:3d}: loss={total_loss/len(train_ldr):.4f}, "
                  f"val_acc={val_acc:.4f}")


# =====================================================================
#   PARTE 12: FEATURE VISUALIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: FEATURE MAPS Y VISUALIZACION ===")
print("=" * 80)

"""
FEATURE MAPS: que "ve" cada capa de la CNN.

Capas tempranas: bordes, texturas, colores.
Capas medias: partes de objetos (ojos, ruedas).
Capas profundas: objetos completos, conceptos abstractos.

TECNICAS DE VISUALIZACION:
1. Activaciones intermedias: que se activa para una imagen.
2. Filtros aprendidos: que patron busca cada filtro.
3. Grad-CAM: que regiones de la imagen son importantes.
"""

if HAS_TORCH:
    print("\n--- Feature maps intermedias ---")

    model_cnn.eval()
    x_sample = X_img[0:1]

    # Hook para capturar activaciones intermedias
    activations = {}

    def get_activation(name):
        def hook(model, input, output):
            activations[name] = output.detach()
        return hook

    # Registrar hooks
    model_cnn.stem.register_forward_hook(get_activation('stem'))
    model_cnn.stage1.register_forward_hook(get_activation('stage1'))
    model_cnn.stage2.register_forward_hook(get_activation('stage2'))

    with torch.no_grad():
        _ = model_cnn(x_sample)

    for name, act in activations.items():
        print(f"  {name}: shape={act.shape}, "
              f"mean={act.mean():.4f}, std={act.std():.4f}, "
              f"active={( act > 0).float().mean():.2%}")

    # Filtros aprendidos
    print("\n--- Filtros del primer conv ---")
    first_conv = model_cnn.stem[0]
    filters = first_conv.weight.data
    print(f"  Shape: {filters.shape} (out_ch, in_ch, H, W)")
    print(f"  Filter 0:\n{filters[0, 0].numpy().round(2)}")
    print(f"  Filter 1:\n{filters[1, 0].numpy().round(2)}")
    print(f"  → Cada filtro busca un patron diferente")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: CNN EN PROFUNDIDAD ===")
print("=" * 80)

print("""
  EVOLUCION DE CNNs:

  LeNet (1998) → simple, 60K params
  VGG (2014) → profundidad, 138M params
  ResNet (2015) → skip connections, 25M params
  MobileNet (2017) → depthwise separable, 3M params
  EfficientNet (2019) → compound scaling, 5-66M params

  COMPONENTES CLAVE:
  1. Convolucion: extrae features locales (parameter sharing).
  2. Pooling/Stride: reduce dimension espacial.
  3. Residual connections: gradientes fluyen (profundidad).
  4. BatchNorm: estabilidad.
  5. GAP: reemplaza FC (menos overfitting).
  6. SE blocks: atencion por canal (+1-2% gratis).
  7. Depthwise separable: 9x menos params.

  REGLAS:
  - Empezar con ResNet pre-entrenado (transfer learning).
  - 3x3 kernels siempre (excpto 1x1 para bottleneck).
  - BatchNorm despues de conv, antes de ReLU.
  - GAP en vez de flatten + FC grande.
  - Data augmentation es critica para CNNs.
""")

print("=" * 80)
print("=== FIN MODULO 18, ARCHIVO 02 ===")
print("=" * 80)
