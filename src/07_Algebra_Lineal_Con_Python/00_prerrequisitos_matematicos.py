# ===========================================================================
# 00_prerrequisitos_matematicos.py
# ===========================================================================
# MODULO 07: ALGEBRA LINEAL CON PYTHON
# ARCHIVO 00: Prerrequisitos Matematicos — La Base de Todo
# ===========================================================================
#
# POR QUE ESTE ARCHIVO EXISTE:
#   Antes de tocar vectores con NumPy, necesitas entender 3 cosas:
#   1. Que ES un vector geometricamente (no solo una lista de numeros).
#   2. Que es una derivada parcial y un gradiente.
#   3. Que significa que una funcion sea "lineal".
#
#   Sin esto, cuando llegues a gradient descent o PCA, estaras
#   memorizando formulas sin entender QUE hacen ni POR QUE funcionan.
#
# COMO LEER ESTE ARCHIVO:
#   - Ejecuta cada seccion por separado.
#   - Lee los comentarios ANTES de mirar el codigo.
#   - Si algo no tiene sentido, PARA y relee. No avances sin entender.
#
# NIVEL: Desde cero absoluto hasta la base que necesita un ingeniero IA.
# ===========================================================================

import numpy as np


# =====================================================================
#   PARTE 1: INTUICION GEOMETRICA DE VECTORES
# =====================================================================
#
# La mayoria de cursos empiezan con "un vector es una lista de numeros".
# Eso es CORRECTO pero INCOMPLETO. Un vector es una FLECHA en el espacio.
# Tiene dos propiedades:
#   - DIRECCION: hacia donde apunta.
#   - MAGNITUD: que tan largo es (que tan "fuerte" es).
#
# Piensa en un vector como una instruccion de movimiento:
#   [3, 2] significa "camina 3 pasos a la derecha y 2 pasos arriba".
#
# EN ML:
#   - Un embedding de palabra es un vector: su DIRECCION codifica
#     el significado de la palabra. Palabras similares apuntan
#     en direcciones similares.
#   - Un gradiente es un vector: su DIRECCION te dice hacia donde
#     subir mas rapido, y su MAGNITUD te dice que tan empinado es.
#
# =====================================================================

print("\n" + "=" * 80)
print("=== PARTE 1: INTUICION GEOMETRICA DE VECTORES ===")
print("=" * 80)


# --- 1.1: Un vector es una flecha ---

print("\n--- 1.1: Un vector es una flecha ---")

# Creamos un vector 2D. Piensa en el como una flecha desde el origen (0,0)
# hasta el punto (3, 2).
v = np.array([3.0, 2.0])

# La MAGNITUD es la longitud de la flecha.
# Se calcula con el teorema de Pitagoras: sqrt(3^2 + 2^2)
magnitud = np.sqrt(v[0]**2 + v[1]**2)
magnitud_np = np.linalg.norm(v)  # Lo mismo pero con NumPy

print(f"  Vector v = {v}")
print(f"  Magnitud manual = sqrt({v[0]}^2 + {v[1]}^2) = sqrt({v[0]**2 + v[1]**2}) = {magnitud:.4f}")
print(f"  Magnitud NumPy  = {magnitud_np:.4f}")

# La DIRECCION se puede expresar como un vector unitario
# (un vector de magnitud 1 que apunta en la misma direccion).
v_unitario = v / magnitud
print(f"\n  Vector unitario = v / ||v|| = {v_unitario}")
print(f"  Magnitud del unitario = {np.linalg.norm(v_unitario):.10f} (siempre 1)")
print(f"  Misma direccion, pero 'normalizado' a longitud 1")


# --- 1.2: Suma de vectores = composicion de movimientos ---

print("\n\n--- 1.2: Suma de vectores ---")

# Si v1 = "camina 3 derecha, 2 arriba"
# y v2 = "camina 1 izquierda, 4 arriba"
# Entonces v1 + v2 = "camina 2 derecha, 6 arriba"
# Es como hacer los dos movimientos uno tras otro.

v1 = np.array([3.0, 2.0])
v2 = np.array([-1.0, 4.0])
suma = v1 + v2

print(f"  v1 = {v1}  (3 derecha, 2 arriba)")
print(f"  v2 = {v2} (1 izquierda, 4 arriba)")
print(f"  v1 + v2 = {suma}  (2 derecha, 6 arriba)")
print(f"  Es como encadenar dos movimientos.")


# --- 1.3: Escalar un vector = estirar/encoger la flecha ---

print("\n\n--- 1.3: Escalado de vectores ---")

# Multiplicar por un escalar cambia la MAGNITUD pero no la DIRECCION.
# - escalar > 1: estira (la flecha se alarga)
# - 0 < escalar < 1: encoge (la flecha se acorta)
# - escalar < 0: invierte Y escala (la flecha apunta al reves)
# - escalar = 0: colapsa al origen (sin direccion)

v = np.array([2.0, 1.0])

for c in [2.0, 0.5, -1.0, 0.0]:
    resultado = c * v
    print(f"  {c:4.1f} * {v} = {resultado}")

print(f"\n  EN ML: el learning rate ES un escalar que escala el gradiente.")
print(f"  w = w - lr * gradiente")
print(f"  Si lr = 0.01, estas 'encogiendo' el gradiente 100x antes de aplicarlo.")


# --- 1.4: Combinacion lineal --- 

print("\n\n--- 1.4: Combinacion lineal ---")

# Una combinacion lineal es: a*v1 + b*v2
# Donde a y b son escalares, y v1, v2 son vectores.
# Es la operacion MAS FUNDAMENTAL del algebra lineal.

# EJEMPLO: con v1 = [1, 0] y v2 = [0, 1], puedo llegar a CUALQUIER
# punto en 2D eligiendo los escalares correctos.

e1 = np.array([1.0, 0.0])  # Vector base: "1 paso a la derecha"
e2 = np.array([0.0, 1.0])  # Vector base: "1 paso arriba"

# Para llegar a [5, 3]:
a, b = 5.0, 3.0
destino = a * e1 + b * e2
print(f"  e1 = {e1} (base horizontal)")
print(f"  e2 = {e2} (base vertical)")
print(f"  {a}*e1 + {b}*e2 = {destino}")
print(f"  Puedo llegar a CUALQUIER punto en R² con estas dos bases.")

# OTRO ejemplo: bases NO estandar
u1 = np.array([1.0, 1.0])
u2 = np.array([1.0, -1.0])
# Para llegar a [5, 3] con estas bases:
# a*u1 + b*u2 = [5, 3]
# a + b = 5, a - b = 3  ->  a = 4, b = 1
destino2 = 4 * u1 + 1 * u2
print(f"\n  Con bases diferentes: u1={u1}, u2={u2}")
print(f"  4*u1 + 1*u2 = {destino2} (mismo punto, diferente camino)")
print(f"\n  EN ML: un embedding ES una combinacion lineal de features latentes.")


# --- 1.5: Span y base ---

print("\n\n--- 1.5: Span (espacio generado) y base ---")

# El SPAN de un conjunto de vectores es todos los puntos a los que
# puedes llegar con combinaciones lineales de esos vectores.
#
# Si tienes 2 vectores que NO son paralelos en R², su span es TODO R².
# Si tienes 2 vectores paralelos, su span es solo UNA linea.
#
# Una BASE es el minimo conjunto de vectores cuyo span cubre todo
# el espacio. En R² necesitas exactamente 2 vectores no paralelos.

# Estos DOS cubren todo R²:
v1 = np.array([1.0, 0.0])
v2 = np.array([0.0, 1.0])

# Estos DOS son paralelos — solo cubren una linea:
v3 = np.array([1.0, 2.0])
v4 = np.array([2.0, 4.0])  # = 2 * v3, misma direccion!

# Para verificar si son paralelos, comprobamos si uno es multiplo del otro
ratio = v4 / v3  # Si todos los elementos son iguales, son paralelos
print(f"  v3 = {v3}, v4 = {v4}")
print(f"  v4 / v3 = {ratio}")
print(f"  Son paralelos (v4 = {ratio[0]}*v3): {np.allclose(ratio, ratio[0])}")
print(f"  -> Solo cubren UNA linea, no todo R²")

print(f"\n  EN ML: si dos features son proporcionales (redundantes),")
print(f"  no aportan informacion nueva. PCA detecta esto.")


# =====================================================================
#   PARTE 2: DERIVADAS PARCIALES
# =====================================================================
#
# Una derivada te dice: "si muevo x un poquito, cuanto cambia f(x)?"
#
# Con UNA variable es simple:
#   f(x) = x²  ->  f'(x) = 2x
#   En x=3: f'(3) = 6, o sea "si aumento x un poquito, f sube ~6 veces mas"
#
# Con VARIAS variables necesitas derivadas PARCIALES:
#   f(x, y) = x² + 3y
#   ∂f/∂x = 2x  (derivar respecto a x, tratando y como constante)
#   ∂f/∂y = 3    (derivar respecto a y, tratando x como constante)
#
# EN ML: la loss function depende de MILES de parametros (pesos).
# Necesitas la derivada parcial respecto a CADA peso para saber
# en que direccion ajustarlo.
#
# =====================================================================

print("\n\n" + "=" * 80)
print("=== PARTE 2: DERIVADAS PARCIALES ===")
print("=" * 80)


# --- 2.1: Derivada con una variable (repaso) ---

print("\n--- 2.1: Derivada con una variable ---")

def f_simple(x):
    """f(x) = x² — ejemplo basico."""
    return x ** 2

# La derivada en un punto se aproxima numericamente:
# f'(x) ≈ (f(x + h) - f(x - h)) / (2h)
# Esto se llama "diferencias centrales" y es mas preciso que (f(x+h) - f(x))/h

def derivada_numerica(f, x, h=1e-7):
    """Aproximar f'(x) con diferencias centrales."""
    return (f(x + h) - f(x - h)) / (2 * h)

x = 3.0
deriv = derivada_numerica(f_simple, x)
print(f"  f(x) = x²")
print(f"  f'(x) = 2x (analitica)")
print(f"  f'({x}) analitica  = {2 * x}")
print(f"  f'({x}) numerica   = {deriv:.6f}")
print(f"  Significado: en x={x}, si subes x un poquito, f sube ~{2*x}x mas rapido")


# --- 2.2: Derivada parcial ---

print("\n\n--- 2.2: Derivada parcial ---")

def f_2vars(x, y):
    """f(x, y) = x² + 3xy + y²"""
    return x**2 + 3*x*y + y**2

# Derivada parcial respecto a x: tratar y como constante
# ∂f/∂x = 2x + 3y
def df_dx_analitica(x, y):
    return 2*x + 3*y

# Derivada parcial respecto a y: tratar x como constante
# ∂f/∂y = 3x + 2y
def df_dy_analitica(x, y):
    return 3*x + 2*y

# Numericamente: mover SOLO x (o SOLO y) un poquito
def parcial_x_numerica(f, x, y, h=1e-7):
    return (f(x + h, y) - f(x - h, y)) / (2 * h)

def parcial_y_numerica(f, x, y, h=1e-7):
    return (f(x, y + h) - f(x, y - h)) / (2 * h)

x0, y0 = 2.0, 1.0
print(f"  f(x, y) = x² + 3xy + y²")
print(f"  Punto: ({x0}, {y0})")
print(f"")
print(f"  ∂f/∂x analitica = 2x + 3y = {df_dx_analitica(x0, y0)}")
print(f"  ∂f/∂x numerica  = {parcial_x_numerica(f_2vars, x0, y0):.6f}")
print(f"  Significado: si SOLO mueves x un poquito (y fijo), f cambia ~{df_dx_analitica(x0, y0)}")
print(f"")
print(f"  ∂f/∂y analitica = 3x + 2y = {df_dy_analitica(x0, y0)}")
print(f"  ∂f/∂y numerica  = {parcial_y_numerica(f_2vars, x0, y0):.6f}")
print(f"  Significado: si SOLO mueves y un poquito (x fijo), f cambia ~{df_dy_analitica(x0, y0)}")


# =====================================================================
#   PARTE 3: EL GRADIENTE
# =====================================================================
#
# El gradiente es simplemente TODAS las derivadas parciales juntas
# en un vector:
#
#   ∇f = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]
#
# Es un VECTOR que:
#   - APUNTA en la direccion de maximo crecimiento de f.
#   - Su MAGNITUD indica que tan empinada es la subida.
#
# Si quieres BAJAR (minimizar la loss), vas en la direccion OPUESTA:
#   -∇f  (gradiente negativo)
#
# ESTO ES DESCENSO DE GRADIENTE:
#   w_nuevo = w_viejo - lr * ∇L(w)
#
# =====================================================================

print("\n\n" + "=" * 80)
print("=== PARTE 3: EL GRADIENTE ===")
print("=" * 80)


# --- 3.1: Gradiente como vector de derivadas parciales ---

print("\n--- 3.1: Gradiente como vector ---")

def f_grad(params):
    """f(x, y) = x² + 3xy + y². Recibe array [x, y]."""
    x, y = params
    return x**2 + 3*x*y + y**2

def gradiente_numerico(f, params, h=1e-7):
    """Calcular gradiente numericamente para f: R^n -> R."""
    grad = np.zeros_like(params)
    for i in range(len(params)):
        params_plus = params.copy()
        params_minus = params.copy()
        params_plus[i] += h
        params_minus[i] -= h
        grad[i] = (f(params_plus) - f(params_minus)) / (2 * h)
    return grad

punto = np.array([2.0, 1.0])
grad = gradiente_numerico(f_grad, punto)
grad_analitico = np.array([2*punto[0] + 3*punto[1], 3*punto[0] + 2*punto[1]])

print(f"  f(x,y) = x² + 3xy + y²")
print(f"  Punto: {punto}")
print(f"  ∇f analitico = [2x+3y, 3x+2y] = {grad_analitico}")
print(f"  ∇f numerico  = {grad}")
print(f"  Direccion: {grad / np.linalg.norm(grad)} (normalizado)")
print(f"  Magnitud (pendiente): {np.linalg.norm(grad):.4f}")


# --- 3.2: El gradiente apunta hacia ARRIBA ---

print("\n\n--- 3.2: El gradiente apunta hacia la subida mas empinada ---")

# Si estamos en un punto y queremos MINIMIZAR f,
# debemos ir en la direccion OPUESTA al gradiente.

punto = np.array([2.0, 1.0])
valor_actual = f_grad(punto)
grad = gradiente_numerico(f_grad, punto)

# Movernos un paso pequeno en la direccion del gradiente (SUBIR)
lr = 0.01
punto_subir = punto + lr * grad
valor_subir = f_grad(punto_subir)

# Movernos un paso pequeno en la direccion OPUESTA (BAJAR)
punto_bajar = punto - lr * grad
valor_bajar = f_grad(punto_bajar)

print(f"  Punto actual: {punto}, f = {valor_actual}")
print(f"  Gradiente: {grad}")
print(f"")
print(f"  Mover EN direccion del gradiente (subir):")
print(f"    Nuevo punto: {punto_subir}, f = {valor_subir:.4f} (SUBE)")
print(f"")
print(f"  Mover CONTRA el gradiente (bajar):")
print(f"    Nuevo punto: {punto_bajar}, f = {valor_bajar:.4f} (BAJA)")
print(f"")
print(f"  CONCLUSION: -∇f siempre te lleva cuesta abajo.")
print(f"  ESTO es descenso de gradiente: w -= lr * grad")


# --- 3.3: Mini gradient descent completo ---

print("\n\n--- 3.3: Descenso de gradiente en accion ---")

# Minimizar f(x, y) = x² + y² (minimo en [0, 0])
def f_cuadratica(params):
    return params[0]**2 + params[1]**2

punto = np.array([5.0, 3.0])  # Empezamos lejos del minimo
lr = 0.1
historia = [punto.copy()]

print(f"  Minimizar f(x,y) = x² + y²")
print(f"  Minimo real: [0, 0]")
print(f"  Punto inicial: {punto}")

for i in range(20):
    grad = gradiente_numerico(f_cuadratica, punto)
    punto = punto - lr * grad  # La unica linea que importa
    historia.append(punto.copy())
    if i < 5 or i == 19:
        print(f"  Paso {i+1:2d}: punto={punto}, f={f_cuadratica(punto):.6f}")

print(f"\n  En 20 pasos, de {historia[0]} llegamos a {punto}")
print(f"  Cerca de [0, 0]: {np.allclose(punto, [0, 0], atol=0.01)}")


# =====================================================================
#   PARTE 4: FUNCIONES LINEALES Y SUS PROPIEDADES
# =====================================================================
#
# Una funcion es LINEAL si cumple DOS propiedades:
#
#   1. ADITIVIDAD:    T(a + b) = T(a) + T(b)
#      "Transformar la suma = suma de las transformaciones"
#
#   2. HOMOGENEIDAD:  T(c * a) = c * T(a)
#      "Transformar el escalado = escalar la transformacion"
#
# Ambas se resumen en UNA:
#   T(c1*a + c2*b) = c1*T(a) + c2*T(b)
#
# POR QUE IMPORTA:
#   - Si una funcion es lineal, se puede representar como una MATRIZ.
#   - Las capas lineales de redes neuronales (nn.Linear) SON funciones
#     lineales: y = W @ x.
#   - ReLU, sigmoid, softmax NO son lineales. Por eso las ponemos
#     ENTRE capas lineales: para que la red pueda aprender patrones
#     no lineales.
#
# =====================================================================

print("\n\n" + "=" * 80)
print("=== PARTE 4: FUNCIONES LINEALES ===")
print("=" * 80)


# --- 4.1: Probar si una funcion es lineal ---

print("\n--- 4.1: Que es una funcion lineal ---")

# EJEMPLO 1: f(x) = 2x  (lineal)
def f_lineal(x):
    """Multiplicar por 2 — es lineal."""
    return 2 * x

# Comprobar aditividad: f(a + b) == f(a) + f(b)?
a = np.array([1.0, 3.0])
b = np.array([2.0, -1.0])

print(f"  f(x) = 2x")
print(f"  a = {a}, b = {b}")
print(f"  f(a + b) = {f_lineal(a + b)}")
print(f"  f(a) + f(b) = {f_lineal(a) + f_lineal(b)}")
print(f"  Aditividad: {np.allclose(f_lineal(a + b), f_lineal(a) + f_lineal(b))}")

# Comprobar homogeneidad: f(c * a) == c * f(a)?
c = 3.0
print(f"\n  f({c} * a) = {f_lineal(c * a)}")
print(f"  {c} * f(a) = {c * f_lineal(a)}")
print(f"  Homogeneidad: {np.allclose(f_lineal(c * a), c * f_lineal(a))}")
print(f"  -> f(x) = 2x ES lineal ✓")


# --- 4.2: Funciones NO lineales ---

print("\n\n--- 4.2: Funciones NO lineales ---")

# EJEMPLO 2: f(x) = x² (NO lineal)
def f_cuadrado(x):
    return x ** 2

print(f"  f(x) = x²")
a_val, b_val = 2.0, 3.0
print(f"  f(a + b) = f({a_val + b_val}) = {f_cuadrado(a_val + b_val)}")
print(f"  f(a) + f(b) = {f_cuadrado(a_val)} + {f_cuadrado(b_val)} = {f_cuadrado(a_val) + f_cuadrado(b_val)}")
print(f"  {f_cuadrado(a_val + b_val)} != {f_cuadrado(a_val) + f_cuadrado(b_val)}")
print(f"  -> f(x) = x² NO es lineal ✗")

# EJEMPLO 3: ReLU (NO lineal)
def relu(x):
    return np.maximum(x, 0)

a_relu = np.array([-1.0, 2.0])
b_relu = np.array([3.0, -4.0])
print(f"\n  ReLU(x) = max(x, 0)")
print(f"  ReLU(a + b) = ReLU({a_relu + b_relu}) = {relu(a_relu + b_relu)}")
print(f"  ReLU(a) + ReLU(b) = {relu(a_relu)} + {relu(b_relu)} = {relu(a_relu) + relu(b_relu)}")
print(f"  -> ReLU NO es lineal ✗")

# EJEMPLO 4: f(x) = x + 1 (AFIN, no lineal)
def f_afin(x):
    return x + 1

print(f"\n  f(x) = x + 1")
print(f"  f(0) = {f_afin(0.0)} (deberia ser 0 si fuera lineal)")
print(f"  -> f(x) = x + 1 es AFIN (lineal + constante), NO puramente lineal")
print(f"  OJO: nn.Linear calcula y = W@x + b. Es AFIN, no lineal.")
print(f"  Pero por convencion se llama 'capa lineal'.")


# --- 4.3: Toda funcion lineal = multiplicacion por matriz ---

print("\n\n--- 4.3: Funcion lineal = multiplicacion por matriz ---")

# TEOREMA CLAVE:
# Si T: R^n -> R^m es lineal, SIEMPRE existe una matriz A (m x n)
# tal que T(x) = A @ x.
#
# Esto es revolucionario: significa que cualquier transformacion lineal
# se puede representar con una tabla de numeros (la matriz).

# Ejemplo: rotar 90 grados
def rotar_90(v):
    """Rotar un vector 2D 90 grados (lineal)."""
    return np.array([-v[1], v[0]])

# La misma operacion como matriz:
R90 = np.array([[0, -1],
                [1,  0]])

v_test = np.array([3.0, 1.0])
print(f"  Rotar 90° como funcion: {rotar_90(v_test)}")
print(f"  Rotar 90° como matriz:  {R90 @ v_test}")
print(f"  Son iguales: {np.allclose(rotar_90(v_test), R90 @ v_test)}")

# Verificar que es lineal
a = np.array([1.0, 2.0])
b = np.array([3.0, -1.0])
print(f"\n  T(a+b) = {rotar_90(a + b)}")
print(f"  T(a)+T(b) = {rotar_90(a) + rotar_90(b)}")
print(f"  Lineal: {np.allclose(rotar_90(a + b), rotar_90(a) + rotar_90(b))}")

print(f"\n  CONCLUSION:")
print(f"  - Funcion lineal <-> Matriz. Son lo mismo.")
print(f"  - nn.Linear(768, 128) crea una matriz W de 128x768.")
print(f"  - Cuando haces y = W @ x, estas aplicando una transformacion lineal.")
print(f"  - Los PESOS de la red son las ENTRADAS de esa matriz.")


# --- 4.4: Por que necesitamos funciones NO lineales ---

print("\n\n--- 4.4: Por que las redes necesitan no-linealidad ---")

# Si apilas capas lineales SIN activacion:
#   y = W2 @ (W1 @ x) = (W2 @ W1) @ x = W3 @ x
# Resultado: sigue siendo UNA transformacion lineal.
# No importa cuantas capas pongas, el resultado es equivalente a UNA.

W1 = np.random.randn(4, 3) * 0.1
W2 = np.random.randn(2, 4) * 0.1
x = np.random.randn(3)

# Dos capas lineales sin activacion
y_2capas = W2 @ (W1 @ x)

# Equivalente a una sola capa
W_combinada = W2 @ W1  # (2, 3)
y_1capa = W_combinada @ x

print(f"  W1: {W1.shape}, W2: {W2.shape}")
print(f"  W2 @ W1 @ x = {y_2capas}")
print(f"  (W2@W1) @ x = {y_1capa}")
print(f"  Son iguales: {np.allclose(y_2capas, y_1capa)}")
print(f"\n  SIN activacion no-lineal, 100 capas = 1 capa.")
print(f"  Por eso ReLU/GELU van entre capas: rompen la linealidad")
print(f"  y permiten aprender patrones complejos.")


# =====================================================================
#   PARTE 5: RESUMEN Y PUENTE A ARCHIVO 01
# =====================================================================

print("\n\n" + "=" * 80)
print("=== PARTE 5: RESUMEN — PUENTE A ALGEBRA LINEAL ===")
print("=" * 80)

print("""
  RESUMEN DE PRERREQUISITOS:

  1. VECTOR = flecha con direccion y magnitud.
     -> En ML: embeddings, gradientes, features.

  2. DERIVADA PARCIAL = cuanto cambia f si mueves UNA variable.
     -> En ML: cuanto cambia la loss si ajustas UN peso.

  3. GRADIENTE = vector de todas las derivadas parciales.
     -> Apunta hacia la subida mas empinada.
     -> Gradient descent: w -= lr * gradiente (ir cuesta abajo).

  4. FUNCION LINEAL = T(a+b) = T(a) + T(b).
     -> Toda funcion lineal ES una multiplicacion por matriz.
     -> nn.Linear(in, out) = matriz de pesos W.
     -> Sin no-linealidad (ReLU), apilar capas no sirve de nada.

  AHORA ESTAS LISTO para el archivo 01_vectores_y_matrices.py,
  donde trabajaras con NumPy para hacer todo esto eficientemente.
""")

print(" FIN DE ARCHIVO 00_prerrequisitos_matematicos.")
print(" La base matematica ha sido establecida.")
