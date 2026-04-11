# ===========================================================================
# 03_tipos_numericos.py
# ===========================================================================
# MÓDULO 01: FUNDAMENTOS SÓLIDOS
# ARCHIVO 03: Tipos Numéricos — int, float, complex, Decimal, Fractions
# ===========================================================================
#
# OBJETIVO DE ESTE ARCHIVO:
# Dominar TODOS los tipos numéricos de Python desde cero, incluyendo
# las trampas de punto flotante, precisión, IEEE 754, y la conexión
# directa con tensores y cálculo numérico para IA.
#
# NIVEL: Desde cero absoluto, con profundidad extrema.
# ===========================================================================


# ===========================================================================
# CAPÍTULO 1: ENTEROS (int) — MÁS PROFUNDO DE LO QUE PARECE
# ===========================================================================

"""
LO BÁSICO
==========
Un entero es un número sin decimales: ..., -2, -1, 0, 1, 2, ...

En Python, los enteros son objetos de tipo 'int'.
"""

x = 42
print(f"x = {x}, type = {type(x)}")

# Operaciones básicas con enteros:
a = 10
b = 3

print(f"\n=== OPERACIONES CON ENTEROS ===")
print(f"a = {a}, b = {b}")
print(f"a + b  = {a + b}")      # Suma: 13
print(f"a - b  = {a - b}")      # Resta: 7
print(f"a * b  = {a * b}")      # Multiplicación: 30
print(f"a / b  = {a / b}")      # División REAL: 3.3333... → ¡DEVUELVE FLOAT!
print(f"a // b = {a // b}")     # División ENTERA: 3 → descarta decimales
print(f"a % b  = {a % b}")      # Módulo (resto): 1
print(f"a ** b = {a ** b}")     # Potencia: 1000
print(f"-a     = {-a}")         # Negación: -10
print(f"abs(-a)= {abs(-a)}")    # Valor absoluto: 10
print(f"divmod(a, b) = {divmod(a, b)}")  # (cociente, resto): (3, 1)

"""
ATENCIÓN — TRAMPA FRECUENTE:

  a / b   → SIEMPRE devuelve float (incluso si el resultado es exacto)
  a // b  → SIEMPRE devuelve int (descarta la parte decimal)

  10 / 2   → 5.0 (float, no int!)
  10 // 2  → 5   (int)

  Esto es un error MUY común en principiantes.
"""

print(f"\n10 / 2  = {10 / 2}, type = {type(10 / 2)}")    # 5.0, float
print(f"10 // 2 = {10 // 2}, type = {type(10 // 2)}")    # 5, int

"""
LO QUE LA MAYORÍA NO SABE: ENTEROS DE PRECISIÓN ARBITRARIA
============================================================
En la mayoría de lenguajes (C, Java, Go), los enteros tienen un
tamaño FIJO:

  C int      → 32 bits → rango: -2,147,483,648 a 2,147,483,647
  C long     → 64 bits → rango: -9.2 * 10^18   a 9.2 * 10^18
  Java int   → 32 bits
  Java long  → 64 bits

Si intentas almacenar un número más grande → OVERFLOW (se desborda
y da un resultado incorrecto).

En Python NO EXISTE OVERFLOW para enteros.

Los enteros en Python pueden ser TAN GRANDES COMO QUIERAS.
Python usa internamente una representación de "longitud variable":
almacena el número como un array de dígitos, y simplemente usa
más memoria si el número es más grande.
"""

print("\n=== ENTEROS DE PRECISIÓN ARBITRARIA ===")

# Esto es perfectamente válido en Python:
grande = 2 ** 1000
print(f"2^1000 tiene {len(str(grande))} dígitos")
print(f"2^1000 = {grande}")

# Factorial de 100 (un número ENORME):
import math
fact_100 = math.factorial(100)
print(f"\n100! tiene {len(str(fact_100))} dígitos")
print(f"100! = {fact_100}")

# En C, esto causaría overflow. En Python, funciona perfectamente.

"""
¿POR QUÉ IMPORTA PARA IA?

1. En deep learning, los ÍNDICES de datasets grandes pueden ser
   enteros muy grandes (billones de registros).

2. Los hashes de objetos son enteros grandes.

3. Cuando implementas criptografía o tokenización, trabajas con
   números enormes.

4. PERO: en computación numérica (NumPy, PyTorch), los enteros
   SÍ tienen tamaño fijo (int32, int64) porque necesitan
   eficiencia de memoria y compatibilidad con hardware.

   import numpy as np
   x = np.int32(2147483647)  # máximo int32
   x + 1  # → OVERFLOW! Da -2147483648

   Esto es una fuente MUY común de bugs en IA cuando los índices
   o contadores exceden int32. PyTorch usa int64 por defecto para
   evitar esto, pero NumPy usa int64 en Linux y int32 en Windows.
"""


# ─── Bases numéricas ───
print("\n=== BASES NUMÉRICAS ===")

decimal = 255           # base 10 (normal)
binario = 0b11111111    # base 2 (prefijo 0b)
octal = 0o377           # base 8 (prefijo 0o)
hexadecimal = 0xFF      # base 16 (prefijo 0x)

print(f"Decimal:     {decimal}")
print(f"Binario:     0b{bin(binario)} = {binario}")
print(f"Octal:       0o{oct(octal)} = {octal}")
print(f"Hexadecimal: 0x{hex(hexadecimal)} = {hexadecimal}")
print(f"Todos son iguales: {decimal == binario == octal == hexadecimal}")

# Conversiones
print(f"\nbin(42) = {bin(42)}")    # '0b101010'
print(f"oct(42) = {oct(42)}")    # '0o52'
print(f"hex(42) = {hex(42)}")    # '0x2a'
print(f"int('ff', 16) = {int('ff', 16)}")  # 255 — parsear hex a int

"""
Para IA:
- Hexadecimal se usa en colores (RGB: #FF5733), hashes, y direcciones
  de memoria.
- Binario se usa en operaciones de bits, máscaras, y entender cómo
  los datos se almacenan en memoria.
- Los tensores de PyTorch almacenan datos en formatos binarios
  (float32, float16, bfloat16). Entender bits ayuda a entender
  la precisión numérica.
"""


# ─── Separadores de miles con underscore ───
print("\n=== SEPARADORES ===")
poblacion = 47_450_795      # más legible que 47450795
velocidad_luz = 299_792_458  # m/s
pixeles = 1_920 * 1_080     # resolución Full HD

print(f"Población España: {poblacion:,}")     # formato con comas
print(f"Velocidad luz: {velocidad_luz:,} m/s")
print(f"Píxeles Full HD: {pixeles:,}")


# ─── Operaciones a nivel de bits (bitwise) ───
print("\n=== OPERACIONES BITWISE ===")

a = 0b1010  # 10
b = 0b1100  # 12

print(f"a = {a} ({bin(a)})")
print(f"b = {b} ({bin(b)})")
print(f"a & b  = {a & b}  ({bin(a & b)})")   # AND: 1000 = 8
print(f"a | b  = {a | b}  ({bin(a | b)})")   # OR:  1110 = 14
print(f"a ^ b  = {a ^ b}  ({bin(a ^ b)})")   # XOR: 0110 = 6
print(f"~a     = {~a}  ({bin(~a)})")         # NOT: -11 (complemento a 2)
print(f"a << 2 = {a << 2}  ({bin(a << 2)})") # Shift izq: 101000 = 40
print(f"a >> 1 = {a >> 1}  ({bin(a >> 1)})") # Shift der: 101 = 5

"""
Las operaciones bitwise son raras en Python normal, pero aparecen en:
- Máscaras de atención en Transformers (attention masks)
- Operaciones sobre imágenes (cada píxel son bits)
- Hashing (funciones hash usan XOR internamente)
- Flags y permisos
"""


# ===========================================================================
# CAPÍTULO 2: PUNTO FLOTANTE (float) — LA FUENTE DE TODOS LOS MALES
# ===========================================================================

"""
LO BÁSICO
==========
Un float es un número con decimales: 3.14, -0.001, 1e10

En Python, los floats siguen el estándar IEEE 754 de doble precisión
(64 bits / 8 bytes), igual que Java double o C double.
"""

print("\n\n========================================")
print("=== PUNTO FLOTANTE (float) ===")
print("========================================")

pi = 3.14159265358979323846
e = 2.71828182845904523536

print(f"pi = {pi}")
print(f"e  = {e}")
print(f"type(pi) = {type(pi)}")

# ─── Notación científica ───
print("\n=== NOTACIÓN CIENTÍFICA ===")
avogadro = 6.022e23        # 6.022 × 10^23
planck = 6.626e-34          # 6.626 × 10^-34
print(f"Número de Avogadro: {avogadro}")
print(f"Constante de Planck: {planck}")
print(f"También: {1e3} = {float('1e3')}")  # 1000.0

"""
IEEE 754 — CÓMO SE ALMACENAN LOS FLOATS
=========================================
Esto es CRUCIAL entenderlo para IA, porque los modelos de deep learning
se entrenan con floats y la precisión importa MUCHO.

Un float de 64 bits (double) se divide en:
  ┌─────┬───────────────┬──────────────────────────────────────────┐
  │ S   │ Exponente     │ Mantisa (Significando)                   │
  │ 1b  │ 11 bits       │ 52 bits                                  │
  └─────┴───────────────┴──────────────────────────────────────────┘

  S = signo (0 = positivo, 1 = negativo)
  Exponente = controla la magnitud (lo grande o pequeño que es)
  Mantisa = controla la precisión (los dígitos significativos)

  Valor = (-1)^S × 2^(E-1023) × 1.M

  Con 52 bits de mantisa, tienes aproximadamente 15-17 dígitos
  decimales de precisión.

FORMATOS EN DEEP LEARNING:
  float64 (double)    → 64 bits → 15-17 dígitos → para ciencia
  float32 (single)    → 32 bits → 6-9 dígitos   → estándar en DL
  float16 (half)      → 16 bits → 3-4 dígitos   → entrenamiento rápido
  bfloat16            → 16 bits → 3-4 dígitos   → rango como float32!, mantisa reducida
  float8              →  8 bits → 2-3 dígitos   → inferencia ultra-rápida

  En PyTorch:
    tensor_32 = torch.tensor([1.0], dtype=torch.float32)  # estándar
    tensor_16 = torch.tensor([1.0], dtype=torch.float16)  # rápido, menos preciso
    tensor_bf = torch.tensor([1.0], dtype=torch.bfloat16) # Google TPU

  Usar float16 o bfloat16 es MUY común para:
  - Entrenar más rápido (Mixed Precision Training)
  - Usar menos memoria GPU (entrenar modelos más grandes)
  - Inferencia más rápida

  PERO: menor precisión → posibles problemas numéricos (NaN, overflow)
"""


# ─── EL PROBLEMA DE LA PRECISIÓN ───
print("\n=== EL PROBLEMA DE PRECISIÓN ===")

print(f"0.1 + 0.2 = {0.1 + 0.2}")  # 0.30000000000000004 ← ¡NO ES 0.3!

"""
¿POR QUÉ 0.1 + 0.2 NO ES 0.3?

Porque 0.1 NO SE PUEDE REPRESENTAR EXACTAMENTE en binario.

En base 10: 1/3 = 0.33333... (infinitos decimales)
En base 2:  1/10 = 0.00011001100110011... (infinitos bits)

Como solo tenemos 52 bits de mantisa, se TRUNCA.
El 0.1 almacenado NO es exactamente 0.1.
El 0.2 almacenado NO es exactamente 0.2.
Su suma NO es exactamente 0.3.

Esto NO es un bug de Python. Es una limitación FUNDAMENTAL de IEEE 754.
Todos los lenguajes tienen este problema (C, Java, JavaScript, etc.)
"""

# Cómo manejar comparaciones con floats:
a = 0.1 + 0.2
b = 0.3

# ❌ MAL: comparación directa
print(f"\na == b: {a == b}")  # False — ¡INCORRECTO!

# ✅ BIEN: comparación con tolerancia
EPSILON = 1e-9
print(f"abs(a - b) < epsilon: {abs(a - b) < EPSILON}")  # True

# ✅ MEJOR: usar math.isclose()
print(f"math.isclose(a, b): {math.isclose(a, b)}")  # True

# math.isclose usa por defecto rel_tol=1e-9 (tolerancia relativa)
# y abs_tol=0.0 (tolerancia absoluta)
print(f"math.isclose(a, b, rel_tol=1e-15): {math.isclose(a, b, rel_tol=1e-15)}")

"""
EN IA — POR QUÉ LA PRECISIÓN IMPORTA:

1. LOSS FUNCTION: La función de pérdida de una red neuronal calcula
   diferencias muy pequeñas. Si el float no tiene suficiente precisión,
   el gradiente puede ser 0 cuando no debería (vanishing gradient).

2. ACUMULACIÓN DE ERRORES: Si sumas millones de floats pequeños
   (muy común al calcular el loss promedio de un dataset), los errores
   de redondeo se acumulan. Solución: usar Kahan summation o float64.

3. OVERFLOW/UNDERFLOW:
   - Si un float es DEMASIADO GRANDE → float('inf')
   - Si un float es DEMASIADO PEQUEÑO (cercano a 0) → 0.0 (underflow)
   - Esto puede pasar con softmax si los logits son muy grandes
   - Solución: log-softmax, numerical stability tricks

4. MIXED PRECISION: Entrenar con float16 es 2x más rápido en GPU,
   pero puede causar problemas numéricos. Se usa "loss scaling" para
   evitarlos.
"""


# ─── Valores especiales de float ───
print("\n=== VALORES ESPECIALES ===")

# Infinito
inf_pos = float('inf')
inf_neg = float('-inf')
print(f"float('inf')  = {inf_pos}")
print(f"float('-inf') = {inf_neg}")
print(f"inf + 1       = {inf_pos + 1}")          # inf
print(f"inf * -1      = {inf_pos * -1}")          # -inf
print(f"1 / inf       = {1 / inf_pos}")           # 0.0
print(f"inf > 999999  = {inf_pos > 999999}")      # True

# NaN (Not a Number)
nan = float('nan')
print(f"\nfloat('nan')  = {nan}")
print(f"nan == nan     = {nan == nan}")            # False! NaN NO es igual a sí mismo
print(f"nan != nan     = {nan != nan}")            # True!
print(f"math.isnan(nan)= {math.isnan(nan)}")      # True — forma correcta de comprobar

# NaN es contagioso: cualquier operación con NaN da NaN
print(f"nan + 1        = {nan + 1}")               # nan
print(f"nan * 0        = {nan * 0}")               # nan
print(f"nan > 0        = {nan > 0}")               # False
print(f"nan < 0        = {nan < 0}")               # False

"""
NaN en IA:
  - Si ves NaN en tu loss durante entrenamiento → algo está MUY MAL
  - Causas comunes:
    → Learning rate demasiado alto
    → División por cero en el forward pass
    → Log de un número negativo o cero
    → Gradientes que explotan (exploding gradients)
  - PyTorch tiene torch.isnan() y torch.isinf()
  - Es CRUCIAL verificar NaN durante entrenamiento

  # Ejemplo de detección de NaN en training loop:
  # loss = criterion(output, target)
  # if torch.isnan(loss):
  #     print("NaN detectado! Abortando...")
  #     break
"""


# ===========================================================================
# CAPÍTULO 3: EL MÓDULO decimal — PRECISIÓN EXACTA
# ===========================================================================

"""
Cuando necesitas precisión EXACTA (dinero, finanzas, contabilidad),
no uses float. Usa el módulo decimal.
"""

from decimal import Decimal, getcontext

print("\n=== MÓDULO DECIMAL ===")

# Float impreciso:
print(f"float: 0.1 + 0.2 = {0.1 + 0.2}")

# Decimal preciso:
d1 = Decimal('0.1')
d2 = Decimal('0.2')
print(f"Decimal: 0.1 + 0.2 = {d1 + d2}")  # 0.3 exacto

# CUIDADO: crear Decimal desde float hereda la imprecisión:
d_malo = Decimal(0.1)  # ← NO hagas esto
d_bueno = Decimal('0.1')  # ← SÍ, desde string
print(f"\nDecimal(0.1) = {d_malo}")     # 0.10000000000000000555...
print(f"Decimal('0.1') = {d_bueno}")   # 0.1

# Configurar precisión:
getcontext().prec = 50  # 50 dígitos significativos
print(f"\nPi con 50 dígitos: {Decimal(1) / Decimal(3)}")

"""
¿Usar Decimal en IA?
NO. Decimal es para finanzas.
En IA usamos float32/float16 porque:
1. Las GPUs operan con floats, no con Decimal
2. PyTorch/NumPy no soportan Decimal
3. La precisión de float32 es más que suficiente para gradientes
4. Decimal es MUCHO más lento que float

Solo mencionamos Decimal para que tengas el conocimiento completo.
"""


# ===========================================================================
# CAPÍTULO 4: EL MÓDULO fractions — FRACCIONES EXACTAS
# ===========================================================================

from fractions import Fraction

print("\n=== MÓDULO FRACTIONS ===")

f1 = Fraction(1, 3)    # 1/3
f2 = Fraction(1, 6)    # 1/6
print(f"1/3 + 1/6 = {f1 + f2}")  # 1/2 exacto
print(f"Tipo: {type(f1 + f2)}")

# Convertir float a fracción (muestra la imprecisión):
f_from_float = Fraction(0.1)
print(f"\nFraction(0.1) = {f_from_float}")
# 3602879701896397/36028797018963968 ← la representación binaria de 0.1

# Desde string es exacto:
f_exacto = Fraction('0.1')
print(f"Fraction('0.1') = {f_exacto}")  # 1/10

"""
Misma historia que Decimal: no se usa en IA, pero es importante
conocerlo para tener el panorama completo de tipos numéricos.
"""


# ===========================================================================
# CAPÍTULO 5: NÚMEROS COMPLEJOS (complex) — SÍ, EXISTEN EN PYTHON
# ===========================================================================

"""
Python soporta números complejos de forma nativa.
Un número complejo tiene parte real y parte imaginaria:
  z = a + bj   (donde j es la unidad imaginaria, √(-1))

NOTA: Python usa 'j' (convención de ingeniería), no 'i' (matemáticas).
"""

print("\n=== NÚMEROS COMPLEJOS ===")

z1 = 3 + 4j
z2 = complex(2, -1)  # 2 - 1j

print(f"z1 = {z1}")
print(f"z2 = {z2}")
print(f"type(z1) = {type(z1)}")

# Acceder a partes
print(f"\nz1.real = {z1.real}")    # 3.0
print(f"z1.imag = {z1.imag}")    # 4.0
print(f"z1.conjugate() = {z1.conjugate()}")  # 3 - 4j

# Operaciones
print(f"\nz1 + z2 = {z1 + z2}")    # (5+3j)
print(f"z1 * z2 = {z1 * z2}")    # (10+5j)
print(f"abs(z1) = {abs(z1)}")    # 5.0 (módulo: √(3²+4²))

"""
¿COMPLEJOS EN IA?
Sí, más de lo que piensas:

1. TRANSFORMADA DE FOURIER: FFT trabaja con números complejos.
   Se usa para procesamiento de audio, señales, y recientemente
   en architecturas como FNet (reemplaza atención con FFT).

2. QUANTUM COMPUTING: Los estados cuánticos son vectores de
   números complejos. Si te interesa QML (Quantum ML), los
   necesitarás.

3. REDES NEURONALES COMPLEJAS: Existen architecturas que
   trabajan en el dominio complejo (Complex-valued Neural Networks).

4. ANÁLISIS ESPECTRAL: En procesamiento de imágenes y audio.

PyTorch soporta tensores complejos:
  # torch.tensor([1+2j, 3+4j], dtype=torch.complex64)
"""


# ===========================================================================
# CAPÍTULO 6: CONVERSIONES ENTRE TIPOS (CASTING)
# ===========================================================================

print("\n=== CONVERSIONES (CASTING) ===")

# Python NUNCA convierte tipos implícitamente (excepto int → float en operaciones)
# Siempre debes ser EXPLÍCITO

# int → float
print(f"float(42) = {float(42)}")    # 42.0

# float → int (TRUNCA, no redondea)
print(f"int(3.7) = {int(3.7)}")      # 3 (pierde .7)
print(f"int(3.2) = {int(3.2)}")      # 3
print(f"int(-3.7) = {int(-3.7)}")    # -3 (trunca hacia cero)

# Para redondear:
print(f"\nround(3.7) = {round(3.7)}")      # 4
print(f"round(3.5) = {round(3.5)}")      # 4 (Banker's rounding!)
print(f"round(4.5) = {round(4.5)}")      # 4 ← ¿¡4?! Sí.
print(f"round(5.5) = {round(5.5)}")      # 6

"""
BANKER'S ROUNDING (Redondeo bancario)
======================================
Python usa "round half to even": cuando el valor está exactamente
en el medio (x.5), redondea al número PAR más cercano.

  round(0.5) = 0   (0 es par)
  round(1.5) = 2   (2 es par)
  round(2.5) = 2   (2 es par)
  round(3.5) = 4   (4 es par)
  round(4.5) = 4   (4 es par)

¿Por qué? Para evitar sesgo estadístico al redondear muchos datos.
Si siempre redondeas .5 hacia arriba, la media se desplaza.

Para IA esto importa cuando:
- Calculas métricas redondeadas
- Cuantizas modelos (conviertes float32 a int8)
- Haces binning de datos
"""

# str → int/float
print(f"\nint('42') = {int('42')}")
print(f"float('3.14') = {float('3.14')}")
print(f"int('ff', 16) = {int('ff', 16)}")  # 255 — base 16

# Booleanos son ints
print(f"\nint(True) = {int(True)}")    # 1
print(f"int(False) = {int(False)}")    # 0
print(f"True + True = {True + True}")  # 2
print(f"sum([True, False, True, True]) = {sum([True, False, True, True])}")  # 3

"""
El hecho de que True == 1 y False == 0 es MUY útil en IA:

  # Contar valores positivos:
  predicciones = [True, False, True, True, False]
  verdaderos = sum(predicciones)  # 3

  # Calcular accuracy:
  correctos = [pred == real for pred, real in zip(predictions, labels)]
  accuracy = sum(correctos) / len(correctos)

  Esto funciona DIRECTAMENTE porque bool es subclase de int.
"""


# ===========================================================================
# CAPÍTULO 7: FUNCIONES MATEMÁTICAS — EL MÓDULO math
# ===========================================================================

print("\n=== MÓDULO MATH ===")

# Constantes
print(f"math.pi    = {math.pi}")
print(f"math.e     = {math.e}")
print(f"math.tau   = {math.tau}")      # 2π (añadido en Python 3.6)
print(f"math.inf   = {math.inf}")      # Infinito
print(f"math.nan   = {math.nan}")      # NaN

# Redondeo
print(f"\nmath.floor(3.7) = {math.floor(3.7)}")  # 3 (redondea abajo)
print(f"math.ceil(3.2)  = {math.ceil(3.2)}")    # 4 (redondea arriba)
print(f"math.trunc(3.7) = {math.trunc(3.7)}")  # 3 (trunca)

# Potencias y raíces
print(f"\nmath.sqrt(16)   = {math.sqrt(16)}")      # 4.0
print(f"math.pow(2, 10) = {math.pow(2, 10)}")    # 1024.0
print(f"16 ** 0.5       = {16 ** 0.5}")           # 4.0 — alternativa

# Exponenciales y logaritmos (CRUCIALES para IA)
print(f"\nmath.exp(1)     = {math.exp(1)}")          # e^1 = 2.718...
print(f"math.log(e)     = {math.log(e)}")          # ln(e) = 1.0
print(f"math.log(100)   = {math.log(100)}")        # ln(100) = 4.605...
print(f"math.log10(100) = {math.log10(100)}")      # log₁₀(100) = 2.0
print(f"math.log2(8)    = {math.log2(8)}")         # log₂(8) = 3.0

"""
LOGARITMOS EN IA — POR QUÉ SON FUNDAMENTALES:

1. CROSS-ENTROPY LOSS (la función de pérdida más usada en clasificación)
   usa logaritmos: L = -Σ y_i * log(p_i)

2. LOG-SOFTMAX: Para estabilidad numérica, se calcula log(softmax(x))
   en vez de log(softmax(x)) por separado.

3. INFORMACIÓN y ENTROPÍA: La teoría de información (Shannon) se basa
   en logaritmos. H(X) = -Σ p(x) * log(p(x))

4. LEARNING RATE DECAY: Se usa decaimiento logarítmico.

5. ESCALAS LOGARÍTMICAS: Los hiperparámetros como learning rate se
   buscan en escala logarítmica (1e-5, 1e-4, 1e-3, ...).

Si no entiendes logaritmos, no puedes entender las funciones de pérdida.
Los veremos en profundidad en el módulo 09 (Cálculo y Optimización).
"""

# Trigonometría (menos usada en IA básico, pero aparece en embeddings)
print(f"\nmath.sin(0)       = {math.sin(0)}")
print(f"math.cos(0)       = {math.cos(0)}")
print(f"math.sin(math.pi) = {math.sin(math.pi)}")  # debería ser 0, es ~1e-16

"""
TRIGONOMETRÍA EN IA:
Las funciones seno y coseno se usan en:
  - POSITIONAL ENCODING de Transformers (señales sinusoidales)
  - ROTARY POSITIONAL EMBEDDINGS (RoPE) — usado en LLaMA
  - Procesamiento de señales y audio
  - Geometría en visión por computador
"""

# Combinatoria e IA
print(f"\nmath.factorial(10) = {math.factorial(10)}")  # 3628800
print(f"math.comb(10, 3)   = {math.comb(10, 3)}")    # 120 (combinaciones)
print(f"math.perm(10, 3)   = {math.perm(10, 3)}")    # 720 (permutaciones)


# ===========================================================================
# CAPÍTULO 8: OPERADORES DE COMPARACIÓN Y ASIGNACIÓN
# ===========================================================================

print("\n=== OPERADORES DE COMPARACIÓN ===")

print(f"5 == 5:  {5 == 5}")      # True (igualdad de valor)
print(f"5 != 3:  {5 != 3}")      # True (desigualdad)
print(f"5 > 3:   {5 > 3}")       # True (mayor que)
print(f"5 < 3:   {5 < 3}")       # False (menor que)
print(f"5 >= 5:  {5 >= 5}")      # True (mayor o igual)
print(f"5 <= 3:  {5 <= 3}")      # False (menor o igual)

# Python permite encadenar comparaciones (otros lenguajes no):
x = 5
print(f"\n1 < x < 10: {1 < x < 10}")    # True (equivale a 1 < x and x < 10)
print(f"1 < x > 3:  {1 < x > 3}")       # True
print(f"0 <= x <= 5 <= 10: {0 <= x <= 5 <= 10}")  # True

"""
Encadenar comparaciones es MUY pythónico y legible.
Úsalo para validar rangos:

  if 0 <= probability <= 1:
      print("Probabilidad válida")

  if min_val <= user_input <= max_val:
      print("Input en rango")
"""

# ─── Operadores de asignación aumentada ───
print("\n=== ASIGNACIÓN AUMENTADA ===")

x = 10
x += 5    # x = x + 5
print(f"x += 5:  x = {x}")   # 15
x -= 3    # x = x - 3
print(f"x -= 3:  x = {x}")   # 12
x *= 2    # x = x * 2
print(f"x *= 2:  x = {x}")   # 24
x //= 5   # x = x // 5
print(f"x //= 5: x = {x}")   # 4
x **= 3   # x = x ** 3
print(f"x **= 3: x = {x}")   # 64

"""
NOTA IMPORTANTE:
Para inmutables (int, str, tuple), += crea un NUEVO objeto.
Para mutables (list), += modifica IN-PLACE (es como .extend()).

  # Con int (inmutable):
  x = 42
  id_antes = id(x)
  x += 1     # crea NUEVO objeto 43, x apunta a él
  id_despues = id(x)
  # id_antes != id_despues

  # Con list (mutable):
  lista = [1, 2]
  id_antes = id(lista)
  lista += [3, 4]  # modifica IN-PLACE (equivale a lista.extend([3,4]))
  id_despues = id(lista)
  # id_antes == id_despues  ← MISMO objeto!
"""

# Demostración:
n = 42
print(f"\nint: id antes de += {id(n)}")
n += 1
print(f"int: id después de += {id(n)}")  # DIFERENTE

lista = [1, 2]
print(f"\nlist: id antes de += {id(lista)}")
lista += [3, 4]
print(f"list: id después de += {id(lista)}")  # MISMO


# ===========================================================================
# CAPÍTULO 9: CONVERSIÓN DE TIPOS — bool() Y LA VERDAD EN PYTHON
# ===========================================================================

"""
En Python, CUALQUIER objeto puede evaluarse como True o False.
Esto se llama "truthiness" (veracidad) y es fundamental para
condicionales y bucles.

REGLA: un valor es False ("falsy") si es "vacío" o "cero".
       Todo lo demás es True ("truthy").

VALORES FALSY en Python (la lista COMPLETA):
  False         (el booleano)
  None          (la ausencia de valor)
  0             (cero entero)
  0.0           (cero float)
  0j            (cero complejo)
  ''            (string vacío)
  []            (lista vacía)
  ()            (tupla vacía)
  {}            (dict vacío)
  set()         (set vacío)
  frozenset()   (frozenset vacío)
  range(0)      (rango vacío)
  b''           (bytes vacío)
  bytearray()   (bytearray vacío)

TODO lo demás es TRUTHY.
"""

print("\n=== TRUTHINESS ===")

valores_falsy = [False, None, 0, 0.0, 0j, '', [], (), {}, set(), frozenset(), range(0)]
valores_truthy = [True, 1, -1, 0.001, "hola", [0], (0,), {"": 0}, {0}, "False"]

print("FALSY:")
for v in valores_falsy:
    print(f"  bool({v!r:15}) = {bool(v)}")

print("\nTRUTHY:")
for v in valores_truthy:
    print(f"  bool({v!r:15}) = {bool(v)}")

"""
USO PRÁCTICO EN CÓDIGO:

  # ✅ Pythónico:
  if lista:           # True si la lista tiene elementos
      ...
  if not lista:       # True si la lista está vacía
      ...

  # ❌ No pythónico (pero funciona):
  if len(lista) > 0:
      ...
  if len(lista) == 0:
      ...

  # ✅ Con strings:
  nombre = input("Tu nombre: ")
  if nombre:          # True si el usuario escribió algo
      print(f"Hola, {nombre}")
  else:
      print("No escribiste nada")

EN IA:
  # Verificar si un dataset tiene datos:
  if dataset:
      train(dataset)
  else:
      print("Dataset vacío!")

  # Verificar si un resultado es None:
  resultado = modelo.predict(datos)
  if resultado is not None:  # ← más explícito que 'if resultado'
      procesar(resultado)
"""


# ===========================================================================
# CAPÍTULO 10: RESUMEN Y MAPA DEL MÓDULO
# ===========================================================================

"""
LO QUE HAS APRENDIDO EN ESTE ARCHIVO:

1. ENTEROS (int):
   - Precisión arbitraria (sin overflow)
   - Bases: decimal, binario (0b), octal (0o), hexadecimal (0x)
   - Operaciones bitwise (AND, OR, XOR, shifts)
   - En NumPy/PyTorch SÍ hay overflow (int32, int64)

2. PUNTO FLOTANTE (float):
   - IEEE 754 doble precisión (64 bits)
   - ¡0.1 + 0.2 ≠ 0.3! Usar math.isclose() para comparar
   - Valores especiales: inf, -inf, nan
   - NaN no es igual a sí mismo → usar math.isnan()
   - Formatos en DL: float32, float16, bfloat16, float8

3. DECIMAL: Precisión exacta para finanzas (no para IA)

4. FRACTIONS: Fracciones exactas (no para IA)

5. COMPLEX: Números complejos (FFT, quantum, señales)

6. CONVERSIONES:
   - Siempre explícitas: int(), float(), str()
   - int(float) TRUNCA, no redondea
   - round() usa Banker's rounding
   - bool es subclase de int (True=1, False=0)

7. MATH: Funciones matemáticas esenciales
   - exp, log: fundamentales para funciones de pérdida
   - sin, cos: usadas en positional encoding
   - sqrt, pow: operaciones básicas

8. TRUTHINESS: Todo valor puede ser True/False
   - Falsy: 0, None, vacío
   - Truthy: todo lo demás

ARCHIVO SIGUIENTE: 04_strings_completo.py
→ Strings como objetos inmutables
→ Métodos de string exhaustivos
→ F-strings profesionales
→ Encoding (UTF-8, ASCII, Unicode)
→ Expresiones regulares (preview)
→ Strings en procesamiento de texto para NLP
"""
