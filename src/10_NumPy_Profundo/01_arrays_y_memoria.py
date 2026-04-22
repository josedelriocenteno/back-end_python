# ===========================================================================
# 01_arrays_y_memoria.py
# ===========================================================================
# MODULO 10: NUMPY PROFUNDO
# ARCHIVO 01: Arrays, Memoria y Representacion Interna
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar la estructura interna de ndarray: dtypes, strides,
# memory layout, views vs copies, structured arrays, mmap.
#
# CONTENIDO:
#   1. ndarray internals: data, dtype, shape, strides.
#   2. Dtypes: precision, casting, custom dtypes.
#   3. Memory layout: C-order vs Fortran-order.
#   4. Views vs Copies: cuando se comparte memoria.
#   5. Strides y stride tricks.
#   6. Structured arrays y record arrays.
#   7. Memory-mapped files (np.memmap).
#   8. Alineacion y cache efficiency.
#   9. Ejercicio: implementar operaciones con strides.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import sys
import time


# =====================================================================
#   PARTE 1: NDARRAY INTERNALS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: NDARRAY INTERNALS ===")
print("=" * 80)

"""
ndarray es un BLOQUE CONTIGUO de memoria con metadata:
- data: puntero al buffer de memoria.
- dtype: tipo de cada elemento.
- shape: dimensiones del array.
- strides: bytes a saltar por dimension.
- flags: C_CONTIGUOUS, F_CONTIGUOUS, OWNDATA, WRITEABLE.

A diferencia de listas Python, todos los elementos son del MISMO tipo
y estan contiguos en memoria -> operaciones vectorizadas rapidas.
"""

print("\n--- Anatomia de un ndarray ---")

a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)

print(f"  Array:\n{a}")
print(f"  dtype: {a.dtype}")
print(f"  shape: {a.shape}")
print(f"  strides: {a.strides}  (bytes por fila, bytes por columna)")
print(f"  ndim: {a.ndim}")
print(f"  size: {a.size}  (total elementos)")
print(f"  itemsize: {a.itemsize}  (bytes por elemento)")
print(f"  nbytes: {a.nbytes}  (total bytes = size * itemsize)")
print(f"  flags:\n{a.flags}")

# Comparar con lista Python
list_equiv = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
print(f"\n  Memoria ndarray: {a.nbytes} bytes")
print(f"  Memoria lista:   {sys.getsizeof(list_equiv) + sum(sys.getsizeof(row) for row in list_equiv)} bytes (aprox)")


print("\n--- Data pointer y base ---")

b = a[0]  # View de la primera fila
print(f"  a.data: {a.ctypes.data}")
print(f"  b.data: {b.ctypes.data}")
print(f"  b es view de a: {b.base is a}")
print(f"  b.flags.owndata: {b.flags.owndata}")

c = a.copy()
print(f"\n  c es copia: {c.base is None}")
print(f"  c.flags.owndata: {c.flags.owndata}")


# =====================================================================
#   PARTE 2: DTYPES EN PROFUNDIDAD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: DTYPES EN PROFUNDIDAD ===")
print("=" * 80)

"""
dtype define:
- Tipo de dato (int, float, complex, bool, string).
- Tamaño en bytes (8, 16, 32, 64 bits).
- Byte order (big-endian, little-endian).

EN ML:
- float32: entrenamiento en GPU (mas rapido, menos memoria).
- float64: precision numerica (gradientes, eigenvalues).
- float16/bfloat16: inferencia, mixed precision.
- int8/uint8: cuantizacion de modelos.
"""

print("\n--- Tipos numericos ---")

dtypes_info = [
    ('bool', np.bool_),
    ('int8', np.int8),
    ('int16', np.int16),
    ('int32', np.int32),
    ('int64', np.int64),
    ('uint8', np.uint8),
    ('float16', np.float16),
    ('float32', np.float32),
    ('float64', np.float64),
    ('complex64', np.complex64),
    ('complex128', np.complex128),
]

print(f"  {'Tipo':<12s}  {'Bytes':>5s}  {'Min':>20s}  {'Max':>20s}")
for name, dt in dtypes_info:
    info = np.iinfo(dt) if np.issubdtype(dt, np.integer) else None
    finfo = np.finfo(dt) if np.issubdtype(dt, np.floating) else None
    if info:
        print(f"  {name:<12s}  {np.dtype(dt).itemsize:5d}  {info.min:>20d}  {info.max:>20d}")
    elif finfo:
        print(f"  {name:<12s}  {np.dtype(dt).itemsize:5d}  {finfo.min:>20.4e}  {finfo.max:>20.4e}")
    else:
        print(f"  {name:<12s}  {np.dtype(dt).itemsize:5d}")


print("\n--- Precision y errores ---")

# float32 vs float64
x32 = np.float32(1.0)
x64 = np.float64(1.0)
eps32 = np.finfo(np.float32).eps
eps64 = np.finfo(np.float64).eps

print(f"  float32 epsilon: {eps32}")
print(f"  float64 epsilon: {eps64}")
print(f"  1.0 + eps32 == 1.0 (float32): {np.float32(1.0 + eps32/2) == np.float32(1.0)}")
print(f"  1.0 + eps64 == 1.0 (float64): {np.float64(1.0 + eps64/2) == np.float64(1.0)}")

# Overflow
print(f"\n  int8 max + 1: {np.int8(127) + np.int8(1)} (overflow!)")
print(f"  float32 de 1e38 * 10: {np.float32(1e38) * np.float32(10)} (inf!)")


print("\n--- Casting y promocion ---")

"""
Reglas de casting:
- safe: no pierde informacion (int32 -> int64).
- same_kind: mismo tipo (int32 -> int64, float32 -> float64).
- unsafe: puede perder (float64 -> int32).
"""

a_int = np.array([1, 2, 3], dtype=np.int32)
a_float = np.array([1.5, 2.5, 3.5], dtype=np.float64)

result = a_int + a_float
print(f"  int32 + float64 -> {result.dtype}")

# Casting explicito
big = np.array([1000], dtype=np.int32)
small = big.astype(np.int8)
print(f"  1000 as int8: {small[0]} (overflow!)")

# Safe casting check
print(f"  int32 -> float64 safe: {np.can_cast(np.int32, np.float64, casting='safe')}")
print(f"  float64 -> int32 safe: {np.can_cast(np.float64, np.int32, casting='safe')}")


# =====================================================================
#   PARTE 3: MEMORY LAYOUT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: MEMORY LAYOUT ===")
print("=" * 80)

"""
C-order (row-major): filas contiguas en memoria.
  [[1, 2, 3],
   [4, 5, 6]]  ->  [1, 2, 3, 4, 5, 6]

Fortran-order (column-major): columnas contiguas.
  [[1, 2, 3],
   [4, 5, 6]]  ->  [1, 4, 2, 5, 3, 6]

EN ML: C-order es el default. Fortran es mas rapido para
operaciones por columna (LAPACK usa Fortran).
"""

print("\n--- C vs Fortran order ---")

c_arr = np.array([[1, 2, 3], [4, 5, 6]], order='C')
f_arr = np.array([[1, 2, 3], [4, 5, 6]], order='F')

print(f"  C-order strides: {c_arr.strides}")
print(f"  F-order strides: {f_arr.strides}")
print(f"  C contiguous: {c_arr.flags['C_CONTIGUOUS']}")
print(f"  F contiguous: {f_arr.flags['F_CONTIGUOUS']}")
print(f"  F-arr C contiguous: {f_arr.flags['C_CONTIGUOUS']}")
print(f"  F-arr F contiguous: {f_arr.flags['F_CONTIGUOUS']}")

# Flat view muestra el layout real
print(f"\n  C-order flat: {c_arr.ravel(order='K')}")
print(f"  F-order flat: {f_arr.ravel(order='K')}")


print("\n--- Performance: row vs column access ---")

big = np.random.rand(5000, 5000)

# Row access (C-contiguous = fast)
start = time.perf_counter()
for i in range(5000):
    _ = big[i, :].sum()
row_time = time.perf_counter() - start

# Column access (not contiguous = slower)
start = time.perf_counter()
for i in range(5000):
    _ = big[:, i].sum()
col_time = time.perf_counter() - start

print(f"  Row access:    {row_time:.4f}s")
print(f"  Column access: {col_time:.4f}s")
print(f"  Ratio: {col_time/row_time:.2f}x")


# =====================================================================
#   PARTE 4: VIEWS VS COPIES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: VIEWS VS COPIES ===")
print("=" * 80)

"""
VIEW: comparte memoria con el original. Cambiar uno cambia el otro.
COPY: memoria independiente.

VIEWS se crean con: slicing, reshape, transpose, ravel(order='K').
COPIES se crean con: fancy indexing, boolean indexing, .copy().

CRITICO en ML: si modificas un view sin querer, corrompes datos.
"""

print("\n--- Operaciones que crean views ---")

original = np.arange(12).reshape(3, 4)
print(f"  Original:\n{original}")

# Slicing = VIEW
view1 = original[0:2, 1:3]
print(f"\n  Slice [0:2, 1:3] es view: {view1.base is original}")
view1[0, 0] = 99
print(f"  Despues de modificar slice, original:\n{original}")
original[0, 1] = 1  # Restaurar

# Reshape = VIEW (si posible)
view2 = original.reshape(4, 3)
print(f"\n  Reshape es view: {view2.base is original}")

# Transpose = VIEW
view3 = original.T
print(f"  Transpose es view: {view3.base is original}")


print("\n--- Operaciones que crean copies ---")

# Fancy indexing = COPY
idx = np.array([0, 2])
copy1 = original[idx]
print(f"  Fancy indexing es copy: {copy1.base is None}")

# Boolean indexing = COPY
mask = original > 5
copy2 = original[mask]
print(f"  Boolean indexing es copy: {copy2.base is None}")

# Explicit copy
copy3 = original.copy()
print(f"  .copy() es copy: {copy3.base is None}")


print("\n--- Peligros de views ---")

def process_data_WRONG(X):
    """PELIGRO: modifica el input sin querer."""
    X_processed = X[:, :2]  # View!
    X_processed *= 2  # Modifica X tambien!
    return X_processed

def process_data_SAFE(X):
    """SEGURO: trabaja con copia."""
    X_processed = X[:, :2].copy()
    X_processed *= 2
    return X_processed

X = np.ones((3, 4))
_ = process_data_WRONG(X)
print(f"  Despues de WRONG: X[0,0] = {X[0,0]} (modificado!)")

X = np.ones((3, 4))
_ = process_data_SAFE(X)
print(f"  Despues de SAFE:  X[0,0] = {X[0,0]} (intacto)")


# =====================================================================
#   PARTE 5: STRIDES EN PROFUNDIDAD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: STRIDES EN PROFUNDIDAD ===")
print("=" * 80)

"""
Strides: bytes a saltar para moverse al siguiente elemento en cada dimension.

Para array (3, 4) de float64 (8 bytes):
- stride[0] = 4 * 8 = 32 (saltar una fila = 4 elementos)
- stride[1] = 8 (saltar una columna = 1 elemento)

Los strides permiten crear views sin copiar datos.
"""

print("\n--- Entender strides ---")

a = np.arange(12, dtype=np.float64).reshape(3, 4)
print(f"  Shape: {a.shape}")
print(f"  Strides: {a.strides}")
print(f"  itemsize: {a.itemsize}")
print(f"  stride[0] = {a.shape[1]} * {a.itemsize} = {a.strides[0]}")
print(f"  stride[1] = 1 * {a.itemsize} = {a.strides[1]}")

# Transpose cambia strides
print(f"\n  Transpose strides: {a.T.strides}")
print(f"  (filas y columnas intercambiadas)")


print("\n--- Stride tricks: sliding window ---")

from numpy.lib.stride_tricks import as_strided

def sliding_window_1d(arr, window_size):
    """Crear ventana deslizante sin copiar datos."""
    n = len(arr)
    new_shape = (n - window_size + 1, window_size)
    new_strides = (arr.strides[0], arr.strides[0])
    return as_strided(arr, shape=new_shape, strides=new_strides)

data = np.arange(10)
windows = sliding_window_1d(data, 3)
print(f"  Data: {data}")
print(f"  Windows (size=3):\n{windows}")
print(f"  Shape: {windows.shape} (sin copia!)")
print(f"  Strides: {windows.strides}")


print("\n--- Stride tricks: im2col (CNN) ---")

"""
im2col: transformar patches de imagen en columnas.
Usado en convoluciones eficientes.
"""

def im2col_2d(image, kernel_h, kernel_w):
    """Extraer patches para convolucion."""
    h, w = image.shape
    out_h = h - kernel_h + 1
    out_w = w - kernel_w + 1
    
    strides = image.strides
    new_shape = (out_h, out_w, kernel_h, kernel_w)
    new_strides = (strides[0], strides[1], strides[0], strides[1])
    
    return as_strided(image, shape=new_shape, strides=new_strides)

img = np.arange(25).reshape(5, 5)
patches = im2col_2d(img, 3, 3)
print(f"\n  Image (5x5):\n{img}")
print(f"  Patches shape: {patches.shape}")
print(f"  Patch [0,0]:\n{patches[0, 0]}")
print(f"  Patch [1,1]:\n{patches[1, 1]}")


# =====================================================================
#   PARTE 6: STRUCTURED ARRAYS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: STRUCTURED ARRAYS ===")
print("=" * 80)

"""
Structured arrays: arrays con columnas de diferentes tipos.
Como un DataFrame pero a nivel NumPy.
"""

print("\n--- Definir structured dtype ---")

dt = np.dtype([
    ('name', 'U20'),
    ('age', np.int32),
    ('height', np.float64),
    ('is_student', np.bool_),
])

people = np.array([
    ('Alice', 30, 1.65, False),
    ('Bob', 25, 1.80, True),
    ('Charlie', 35, 1.75, False),
    ('Diana', 22, 1.60, True),
], dtype=dt)

print(f"  dtype: {people.dtype}")
print(f"  Nombres: {people['name']}")
print(f"  Edades: {people['age']}")
print(f"  Estudiantes: {people[people['is_student']]['name']}")
print(f"  Edad promedio: {people['age'].mean():.1f}")


print("\n--- Record arrays ---")

rec = people.view(np.recarray)
print(f"  rec.name: {rec.name}")
print(f"  rec.age: {rec.age}")
print(f"  rec[0]: {rec[0]}")


# =====================================================================
#   PARTE 7: MEMORY-MAPPED FILES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: MEMORY-MAPPED FILES ===")
print("=" * 80)

"""
np.memmap: acceder a datos en disco como si fueran un array.
No carga todo en RAM. Util para datasets enormes.

EN ML: cargar embeddings grandes, datasets que no caben en RAM.
"""

print("\n--- Crear y usar memmap ---")

import tempfile
import os

# Crear archivo temporal
tmpdir = tempfile.mkdtemp()
filepath = os.path.join(tmpdir, 'big_array.dat')

# Escribir
mm_write = np.memmap(filepath, dtype=np.float32, mode='w+', shape=(1000, 100))
mm_write[:] = np.random.randn(1000, 100).astype(np.float32)
mm_write.flush()

# Leer (sin cargar todo en RAM)
mm_read = np.memmap(filepath, dtype=np.float32, mode='r', shape=(1000, 100))
print(f"  Shape: {mm_read.shape}")
print(f"  First row mean: {mm_read[0].mean():.4f}")
print(f"  File size: {os.path.getsize(filepath):,} bytes")
print(f"  Array nbytes: {mm_read.nbytes:,} bytes")

# Cleanup
del mm_write, mm_read
os.remove(filepath)
os.rmdir(tmpdir)


# =====================================================================
#   PARTE 8: CACHE EFFICIENCY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: CACHE EFFICIENCY ===")
print("=" * 80)

"""
CPU cache lines son ~64 bytes. Acceso secuencial es rapido.
Acceso aleatorio causa cache misses.

Reglas:
1. Iterar en C-order (filas) es rapido.
2. Mantener datos contiguos.
3. Evitar arrays transpuestos para operaciones intensivas.
"""

print("\n--- Contiguity y performance ---")

n = 2000
a_c = np.ascontiguousarray(np.random.rand(n, n))
a_f = np.asfortranarray(np.random.rand(n, n))

# Sum por filas (C-order win)
start = time.perf_counter()
_ = a_c.sum(axis=1)
t_c_row = time.perf_counter() - start

start = time.perf_counter()
_ = a_f.sum(axis=1)
t_f_row = time.perf_counter() - start

# Sum por columnas (F-order win)
start = time.perf_counter()
_ = a_c.sum(axis=0)
t_c_col = time.perf_counter() - start

start = time.perf_counter()
_ = a_f.sum(axis=0)
t_f_col = time.perf_counter() - start

print(f"  Sum por FILAS:    C={t_c_row:.4f}s, F={t_f_row:.4f}s")
print(f"  Sum por COLUMNAS: C={t_c_col:.4f}s, F={t_f_col:.4f}s")


print("\n--- np.ascontiguousarray ---")

# Transpose NO es contigua
a = np.random.rand(1000, 1000)
a_t = a.T
print(f"  a C_CONTIGUOUS: {a.flags['C_CONTIGUOUS']}")
print(f"  a.T C_CONTIGUOUS: {a_t.flags['C_CONTIGUOUS']}")

a_t_contig = np.ascontiguousarray(a_t)
print(f"  ascontiguousarray C_CONTIGUOUS: {a_t_contig.flags['C_CONTIGUOUS']}")


# =====================================================================
#   PARTE 9: CUANTIZACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: CUANTIZACION DE MODELOS ===")
print("=" * 80)

"""
Cuantizacion: reducir precision para ahorrar memoria y computo.
float32 -> float16: 2x menos memoria.
float32 -> int8: 4x menos memoria.

EN ML: inferencia mas rapida, modelos en dispositivos edge.
"""

print("\n--- Precision vs memoria ---")

original = np.random.randn(1000000).astype(np.float32)

for dtype in [np.float64, np.float32, np.float16]:
    converted = original.astype(dtype)
    error = np.mean(np.abs(original.astype(np.float64) - converted.astype(np.float64)))
    print(f"  {str(np.dtype(dtype)):>10s}: {converted.nbytes/1e6:6.2f} MB, "
          f"mean_error = {error:.2e}")


print("\n--- Simular int8 quantization ---")

def quantize_int8(arr):
    """Cuantizar a int8 (rango [-128, 127])."""
    scale = (arr.max() - arr.min()) / 255
    zero_point = int(-128 - arr.min() / scale)
    quantized = np.clip(np.round(arr / scale) + zero_point, -128, 127).astype(np.int8)
    return quantized, scale, zero_point

def dequantize_int8(quantized, scale, zero_point):
    """Reconstruir desde int8."""
    return (quantized.astype(np.float32) - zero_point) * scale

weights = np.random.randn(1000).astype(np.float32)
q_weights, scale, zp = quantize_int8(weights)
reconstructed = dequantize_int8(q_weights, scale, zp)

quant_error = np.mean(np.abs(weights - reconstructed))
print(f"\n  Original: {weights.nbytes} bytes ({weights.dtype})")
print(f"  Quantized: {q_weights.nbytes} bytes ({q_weights.dtype})")
print(f"  Compression: {weights.nbytes / q_weights.nbytes:.1f}x")
print(f"  Mean error: {quant_error:.6f}")


# =====================================================================
#   PARTE 10: ARRAY CREATION PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: PATRONES DE CREACION ===")
print("=" * 80)

print("\n--- Funciones de creacion ---")

# zeros, ones, empty, full
print(f"  zeros(3):    {np.zeros(3)}")
print(f"  ones(3):     {np.ones(3)}")
print(f"  full(3, 7):  {np.full(3, 7.0)}")
print(f"  eye(3):\n{np.eye(3)}")

# arange vs linspace
print(f"\n  arange(0, 1, 0.3):    {np.arange(0, 1, 0.3)}")
print(f"  linspace(0, 1, 4):    {np.linspace(0, 1, 4)}")
print(f"  logspace(0, 3, 4):    {np.logspace(0, 3, 4)}")
print(f"  geomspace(1, 1000, 4):{np.geomspace(1, 1000, 4)}")

# Random
np.random.seed(42)
print(f"\n  random.rand(3):       {np.random.rand(3)}")
print(f"  random.randn(3):      {np.random.randn(3)}")
print(f"  random.randint(0,10,3):{np.random.randint(0, 10, 3)}")

# From existing
print(f"\n  zeros_like(a):  shape={np.zeros_like(np.ones((2,3))).shape}")
print(f"  empty_like(a):  shape={np.empty_like(np.ones((2,3))).shape}")


print("\n--- Performance de creacion ---")

n = 1000000
for name, fn in [
    ("zeros", lambda: np.zeros(n)),
    ("empty", lambda: np.empty(n)),
    ("ones", lambda: np.ones(n)),
    ("full", lambda: np.full(n, 0.0)),
    ("arange", lambda: np.arange(n, dtype=np.float64)),
]:
    start = time.perf_counter()
    for _ in range(100):
        _ = fn()
    t = time.perf_counter() - start
    print(f"  {name:8s}: {t:.4f}s (100 iters)")


# =====================================================================
#   PARTE 11: NP.SHARES_MEMORY Y DEBUGGING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: DEBUGGING DE MEMORIA ===")
print("=" * 80)

print("\n--- np.shares_memory ---")

a = np.arange(10)
b = a[2:5]
c = a.copy()
d = a[[0, 1, 2]]

print(f"  shares_memory(a, b): {np.shares_memory(a, b)}")
print(f"  shares_memory(a, c): {np.shares_memory(a, c)}")
print(f"  shares_memory(a, d): {np.shares_memory(a, d)}")


print("\n--- Tracking allocations ---")

"""
Para debugging de memoria en ML:
- np.shares_memory: ver si hay aliasing.
- array.flags: ver contiguidad y ownership.
- sys.getsizeof: tamaño del objeto Python.
- array.nbytes: tamaño del buffer numpy.
"""

large = np.random.rand(10000, 100)
view_of_large = large[:1000]
copy_of_large = large[:1000].copy()

print(f"  large nbytes:         {large.nbytes:>12,} bytes")
print(f"  view nbytes (virtual):{view_of_large.nbytes:>12,} bytes")
print(f"  copy nbytes (real):   {copy_of_large.nbytes:>12,} bytes")
print(f"  view owns data: {view_of_large.flags.owndata}")
print(f"  copy owns data: {copy_of_large.flags.owndata}")


# =====================================================================
#   PARTE 12: SAVE Y LOAD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: SAVE Y LOAD ===")
print("=" * 80)

"""
Formatos de persistencia:
- np.save/load: un array, formato .npy.
- np.savez/load: multiples arrays, formato .npz.
- np.savetxt/loadtxt: texto CSV.
"""

print("\n--- np.save / np.load ---")

import tempfile, os
tmpdir = tempfile.mkdtemp()

weights = np.random.randn(100, 50).astype(np.float32)
biases = np.random.randn(50).astype(np.float32)

# Single array
path_single = os.path.join(tmpdir, 'weights.npy')
np.save(path_single, weights)
loaded = np.load(path_single)
print(f"  Saved weights: {weights.shape}, {weights.dtype}")
print(f"  Loaded match: {np.array_equal(weights, loaded)}")
print(f"  File size: {os.path.getsize(path_single):,} bytes")

# Multiple arrays
path_multi = os.path.join(tmpdir, 'model.npz')
np.savez(path_multi, weights=weights, biases=biases)
data = np.load(path_multi)
print(f"\n  npz keys: {list(data.keys())}")
print(f"  Weights match: {np.array_equal(weights, data['weights'])}")

# Compressed
path_compressed = os.path.join(tmpdir, 'model_compressed.npz')
np.savez_compressed(path_compressed, weights=weights, biases=biases)
print(f"  Uncompressed: {os.path.getsize(path_multi):,} bytes")
print(f"  Compressed:   {os.path.getsize(path_compressed):,} bytes")

# Cleanup
for f in [path_single, path_multi, path_compressed]:
    os.remove(f)
os.rmdir(tmpdir)


# =====================================================================
#   PARTE 13: BYTE ORDER Y ENDIANNESS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: BYTE ORDER ===")
print("=" * 80)

"""
Byte order (endianness):
- Little-endian (<): LSB primero (x86, ARM).
- Big-endian (>): MSB primero (network, some file formats).

Importa cuando: lees archivos binarios, interoperas con C/Fortran.
"""

print("\n--- Byte order ---")

a_le = np.array([1, 256, 65536], dtype='<i4')  # Little-endian int32
a_be = np.array([1, 256, 65536], dtype='>i4')  # Big-endian int32
a_native = np.array([1, 256, 65536], dtype=np.int32)

print(f"  Native byte order: {a_native.dtype.byteorder}")
print(f"  Little-endian bytes: {a_le.tobytes()[:8].hex()}")
print(f"  Big-endian bytes:    {a_be.tobytes()[:8].hex()}")

# Swap byte order
swapped = a_native.byteswap().newbyteorder()
print(f"  Byte-swapped dtype: {swapped.dtype}")


# =====================================================================
#   PARTE 14: MIXED PRECISION SIMULATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: MIXED PRECISION ===")
print("=" * 80)

"""
Mixed precision: usar float16 para forward/backward, float32 para master weights.
Reduce memoria 2x, acelera computo en GPU.

Loss scaling: multiplicar loss por factor grande antes de backward
para evitar underflow en float16 gradients.
"""

print("\n--- Mixed precision simulation ---")

np.random.seed(42)

# Master weights (float32)
W_master = np.random.randn(256, 128).astype(np.float32) * 0.01

# Forward en float16
W_half = W_master.astype(np.float16)
X = np.random.randn(32, 256).astype(np.float16)
Y_half = X @ W_half

# Gradiente en float16
grad_half = np.random.randn(*W_master.shape).astype(np.float16) * 0.001

# Loss scaling
loss_scale = 1024.0
grad_scaled = grad_half * np.float16(loss_scale)

# Update en float32
grad_fp32 = grad_scaled.astype(np.float32) / loss_scale
lr = 0.01
W_master -= lr * grad_fp32

print(f"  Master weights dtype: {W_master.dtype}")
print(f"  Compute dtype: {W_half.dtype}")
print(f"  Memory saving: {W_master.nbytes / W_half.nbytes:.1f}x")
print(f"  Grad range (fp16): [{np.min(np.abs(grad_half[grad_half != 0])):.2e}, {np.max(np.abs(grad_half)):.2e}]")
print(f"  Loss scale: {loss_scale}")


# =====================================================================
#   PARTE 15: ADVANCED MEMORY PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: ADVANCED MEMORY PATTERNS ===")
print("=" * 80)

print("\n--- Memory pool pattern ---")

class ArrayPool:
    """Pre-allocar arrays para evitar allocations repetidas."""
    
    def __init__(self, shape, dtype=np.float32, pool_size=10):
        self.pool = [np.empty(shape, dtype=dtype) for _ in range(pool_size)]
        self.available = list(range(pool_size))
        self.shape = shape
    
    def acquire(self):
        if not self.available:
            raise RuntimeError("Pool exhausted")
        idx = self.available.pop()
        return self.pool[idx], idx
    
    def release(self, idx):
        self.pool[idx][:] = 0  # Reset
        self.available.append(idx)

pool = ArrayPool((1000, 100), pool_size=5)

# Simular uso
arr, idx = pool.acquire()
arr[:] = np.random.randn(1000, 100)
print(f"  Acquired array {idx}: shape={arr.shape}")
pool.release(idx)
print(f"  Released. Available: {len(pool.available)}")


print("\n--- Zero-copy interop ---")

"""
NumPy arrays pueden compartirse sin copia con:
- PyTorch: torch.from_numpy(arr)
- TensorFlow: tf.constant(arr)
- Pandas: pd.DataFrame(arr)
- C extensions: arr.ctypes
"""

arr = np.random.randn(100).astype(np.float32)
print(f"  Data pointer: {arr.ctypes.data}")
print(f"  Can pass to C via ctypes.data")
print(f"  Buffer protocol: {memoryview(arr).nbytes} bytes")


print("\n--- np.frombuffer ---")

# Crear array desde bytes sin copia
raw_bytes = b'\x00\x00\x80\x3f\x00\x00\x00\x40\x00\x00\x40\x40'  # 1.0, 2.0, 3.0 in float32
arr_from_buf = np.frombuffer(raw_bytes, dtype=np.float32)
print(f"  From bytes: {arr_from_buf}")


# =====================================================================
#   PARTE 16: STRIDE TRICKS AVANZADO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: STRIDE TRICKS AVANZADO ===")
print("=" * 80)

print("\n--- Sliding window 2D (batch) ---")

def sliding_window_2d(arr, window_h, window_w):
    """Ventanas 2D sobre una imagen."""
    h, w = arr.shape
    out_h = h - window_h + 1
    out_w = w - window_w + 1
    
    s = arr.strides
    shape = (out_h, out_w, window_h, window_w)
    strides = (s[0], s[1], s[0], s[1])
    
    return as_strided(arr, shape=shape, strides=strides)

img = np.arange(16).reshape(4, 4)
windows = sliding_window_2d(img, 2, 2)
print(f"  Image (4x4):\n{img}")
print(f"  Windows shape: {windows.shape}")
print(f"  Window [0,0]:\n{windows[0,0]}")
print(f"  Window [2,2]:\n{windows[2,2]}")

# Aplicar operacion (max pooling!)
max_pool = windows.max(axis=(2, 3))
print(f"  Max pooling 2x2:\n{max_pool}")

# Average pooling
avg_pool = windows.mean(axis=(2, 3))
print(f"  Avg pooling 2x2:\n{avg_pool}")


# =====================================================================
#   PARTE 17: NP.PACKBITS Y BITWISE OPS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: PACKBITS Y BITWISE ===")
print("=" * 80)

"""
np.packbits: comprimir arrays booleanos (8 bools -> 1 byte).
Util para masks de attention, sparse features.
"""

print("\n--- np.packbits ---")

mask = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1], dtype=np.uint8)
packed = np.packbits(mask)
unpacked = np.unpackbits(packed)[:len(mask)]

print(f"  Original: {mask} ({mask.nbytes} bytes)")
print(f"  Packed:   {packed} ({packed.nbytes} bytes)")
print(f"  Unpacked: {unpacked}")
print(f"  Compression: {mask.nbytes / packed.nbytes:.0f}x")

# Bitwise ops
a = np.array([0b1010, 0b1100], dtype=np.uint8)
b = np.array([0b1100, 0b1010], dtype=np.uint8)
print(f"\n  a & b: {np.bitwise_and(a, b)}")
print(f"  a | b: {np.bitwise_or(a, b)}")
print(f"  a ^ b: {np.bitwise_xor(a, b)}")


# =====================================================================
#   PARTE 18: TILE, REPEAT, BROADCAST_TO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: TILE, REPEAT, BROADCAST_TO ===")
print("=" * 80)

"""
tile: repetir array en cada dimension.
repeat: repetir cada elemento.
broadcast_to: crear view sin copiar (preferido).
"""

print("\n--- tile vs repeat vs broadcast_to ---")

v = np.array([1, 2, 3])

print(f"  tile(v, 3):     {np.tile(v, 3)}")
print(f"  tile(v, (2,3)): shape={np.tile(v, (2, 3)).shape}")
print(f"  repeat(v, 2):   {np.repeat(v, 2)}")

# broadcast_to (NO copia!)
expanded = np.broadcast_to(v, (4, 3))
print(f"  broadcast_to(v, (4,3)):\n{expanded}")
print(f"  Owns data: {expanded.flags.owndata}")
print(f"  Strides: {expanded.strides} (stride 0 en dim 0 = no copy)")

# Performance
n = 10000
v_big = np.random.randn(100)

start = time.perf_counter()
tiled = np.tile(v_big, (n, 1))
t_tile = time.perf_counter() - start

start = time.perf_counter()
broadcasted = np.broadcast_to(v_big, (n, 100))
t_broadcast = time.perf_counter() - start

print(f"\n  tile:         {t_tile:.6f}s ({tiled.nbytes:,} bytes)")
print(f"  broadcast_to: {t_broadcast:.6f}s (0 bytes extra!)")


# =====================================================================
#   PARTE 19: MEMORY ALIGNMENT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: MEMORY ALIGNMENT ===")
print("=" * 80)

"""
SIMD (AVX/SSE) requiere datos alineados a 16/32/64 bytes.
NumPy alinea por defecto, pero slices pueden desalinear.
"""

print("\n--- Alignment check ---")

a = np.random.randn(100)
print(f"  a aligned: {a.ctypes.data % 64 == 0}")
print(f"  a[1:] aligned: {a[1:].ctypes.data % 64 == 0}")

# np.require para forzar alignment
a_aligned = np.require(a, requirements=['C_CONTIGUOUS', 'ALIGNED'])
print(f"  require aligned: {a_aligned.flags['ALIGNED']}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE ARRAYS Y MEMORIA:

1. ndarray = buffer + dtype + shape + strides.

2. dtypes: float32 para GPU, float64 para precision.

3. C-order vs F-order: C es default, F para LAPACK.

4. Views = memoria compartida. Copies = independiente.

5. Strides: sliding windows, im2col sin copias.

6. Structured arrays: columnas heterogeneas.

7. memmap: datos mayores que RAM.

8. Cache efficiency: acceso secuencial > aleatorio.

9. Cuantizacion: float32->int8 para inferencia.

10. np.shares_memory: debugging de aliasing.

Siguiente archivo: Broadcasting y operaciones vectorizadas.
"""

print("\n FIN DE ARCHIVO 01_arrays_y_memoria.")
print(" Arrays y memoria han sido dominados.")
