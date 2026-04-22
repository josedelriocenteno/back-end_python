# ===========================================================================
# 05_booleanos_logica_y_control.py
# ===========================================================================
# MÓDULO 01: FUNDAMENTOS Y TIPOS
# ARCHIVO 05: Booleanos, Lógica y Control de Flujo
# ===========================================================================
#
# OBJETIVO DE ESTE ARCHIVO:
# Dominar booleanos, operadores lógicos (con cortocircuito), condicionales,
# bucles, match/case, y todas las herramientas de control de flujo de Python.
# Todo desde cero con contexto completo para IA.
#
# NIVEL: Desde cero absoluto con profundidad extrema.
# ===========================================================================


# ===========================================================================
# CAPÍTULO 1: BOOLEANOS — MÁS DE LO QUE PARECE
# ===========================================================================

"""
Los booleanos representan verdad (True) o falsedad (False).
En Python, bool es una SUBCLASE de int:
  True == 1
  False == 0

Esto no es un detalle trivial. Es clave para muchas operaciones en IA.
"""

print("=== BOOLEANOS ===")

# bool hereda de int
print(f"isinstance(True, int): {isinstance(True, int)}")   # True
print(f"isinstance(True, bool): {isinstance(True, bool)}") # True
print(f"True + True:  {True + True}")    # 2
print(f"True * 10:    {True * 10}")      # 10
print(f"False + 5:    {False + 5}")      # 5

# Esto es ÚTIL para contar:
resultados = [True, False, True, True, False, True]
aciertos = sum(resultados)  # 4 — porque True=1
total = len(resultados)
precision = aciertos / total
print(f"\nResultados: {resultados}")
print(f"Aciertos: {aciertos}/{total} = {precision:.2%}")

"""
EN IA USAS ESTO CONSTANTEMENTE:

  # Calcular accuracy de un modelo:
  predicciones = [1, 0, 1, 1, 0]
  reales       = [1, 0, 0, 1, 0]
  correctos = [p == r for p, r in zip(predicciones, reales)]
  accuracy = sum(correctos) / len(correctos)
  # correctos = [True, True, False, True, True] → sum = 4 → accuracy = 0.8

  # Contar valores nulos:
  nulos = sum(1 for x in datos if x is None)
  # O más pythónico:
  nulos = sum(x is None for x in datos)
"""


# ===========================================================================
# CAPÍTULO 2: OPERADORES DE COMPARACIÓN
# ===========================================================================

print("\n=== OPERADORES DE COMPARACIÓN ===")

a, b = 10, 3

print(f"a = {a}, b = {b}")
print(f"a == b: {a == b}")    # igualdad de VALOR
print(f"a != b: {a != b}")    # desigualdad
print(f"a > b:  {a > b}")     # mayor que
print(f"a < b:  {a < b}")     # menor que
print(f"a >= b: {a >= b}")    # mayor o igual
print(f"a <= b: {a <= b}")    # menor o igual

# Encadenamiento de comparaciones (EXCLUSIVO de Python)
x = 5
print(f"\n1 < x < 10:  {1 < x < 10}")        # True (equivale a 1<x and x<10)
print(f"1 < x > 3:   {1 < x > 3}")           # True
print(f"0 <= x <= 5 <= 100: {0 <= x <= 5 <= 100}")  # True

"""
Encadenar comparaciones es elegante y MUY legible:

  # Validar que una probabilidad está en rango:
  if 0 <= prob <= 1:
      print("Probabilidad válida")

  # Validar que un learning rate es razonable:
  if 1e-6 <= lr <= 1e-1:
      print("Learning rate en rango aceptable")

  # Verificar que los datos están normalizados:
  if 0 <= min_val <= max_val <= 1:
      print("Datos normalizados correctamente")
"""

# Comparación de strings (lexicográfica)
print(f"\n'abc' < 'abd': {'abc' < 'abd'}")     # True (c < d)
print(f"'abc' < 'abcd': {'abc' < 'abcd'}")    # True (más corto)
print(f"'ABC' < 'abc': {'ABC' < 'abc'}")      # True (A=65 < a=97)

# Comparación de listas (element-wise)
print(f"\n[1,2,3] < [1,2,4]: {[1,2,3] < [1,2,4]}")   # True (3 < 4)
print(f"[1,2] < [1,2,3]: {[1,2] < [1,2,3]}")          # True (más corta)


# ===========================================================================
# CAPÍTULO 3: OPERADORES LÓGICOS — and, or, not
# ===========================================================================

"""
Python tiene tres operadores lógicos: and, or, not

PERO (y esto es clave) NO devuelven siempre True/False.
Devuelven UNO DE LOS OPERANDOS. Esto se llama "cortocircuito" y
es una herramienta MUY potente.
"""

print("\n=== OPERADORES LÓGICOS ===")

# ─── not: invierte el valor booleano ───
print("--- not ---")
print(f"not True:  {not True}")      # False
print(f"not False: {not False}")     # True
print(f"not 0:     {not 0}")         # True (0 es falsy)
print(f"not 'hola': {not 'hola'}")   # False ('hola' es truthy)
print(f"not []:    {not []}")        # True (lista vacía es falsy)
print(f"not None:  {not None}")      # True


# ─── and: evaluación en cortocircuito ───
print("\n--- and (cortocircuito) ---")

"""
REGLA DE and:
  a and b

  1. Evalúa a
  2. Si a es FALSY → devuelve a (NO evalúa b)
  3. Si a es TRUTHY → devuelve b

  Devuelve el PRIMER valor falsy, o el ÚLTIMO valor si todos son truthy.
"""

print(f"True and True:    {True and True}")         # True
print(f"True and False:   {True and False}")        # False
print(f"False and True:   {False and True}")        # False
print(f"0 and 'hola':     {0 and 'hola'}")          # 0 (0 es falsy, devuelve 0)
print(f"'hola' and 42:    {'hola' and 42}")         # 42 (hola es truthy, devuelve 42)
print(f"'' and 42:        {'' and 42}")             # '' (vacío es falsy)
print(f"[1] and [2]:      {[1] and [2]}")           # [2]
print(f"None and 'algo':  {None and 'algo'}")       # None

# ─── or: evaluación en cortocircuito ───
print("\n--- or (cortocircuito) ---")

"""
REGLA DE or:
  a or b

  1. Evalúa a
  2. Si a es TRUTHY → devuelve a (NO evalúa b)
  3. Si a es FALSY → devuelve b

  Devuelve el PRIMER valor truthy, o el ÚLTIMO valor si todos son falsy.
"""

print(f"True or False:    {True or False}")          # True
print(f"False or True:    {False or True}")          # True
print(f"False or False:   {False or False}")         # False
print(f"'hola' or 'mundo': {'hola' or 'mundo'}")    # 'hola'
print(f"'' or 'default':  {'' or 'default'}")        # 'default'
print(f"None or 42:       {None or 42}")             # 42
print(f"0 or '' or []:    {0 or '' or []}")          # [] (todos falsy, devuelve último)
print(f"0 or '' or 'ok':  {0 or '' or 'ok'}")       # 'ok'

"""
PATRONES PRÁCTICOS CON CORTOCIRCUITO:

  1. Valor por defecto:
     nombre = input_nombre or "Anónimo"
     # Si input_nombre es vacío/None → usa "Anónimo"

  2. Acceso seguro:
     resultado = datos and datos.get("clave")
     # Si datos es None → no evalúa .get() → evita AttributeError

  3. Validación:
     if usuario and usuario.activo and usuario.tiene_permiso("admin"):
         # Solo evalúa cada parte si la anterior es True
         # Si usuario es None, no llega a .activo

EN IA:
  # Valor por defecto de hiperparámetro:
  lr = config.get("learning_rate") or 1e-3

  # Logging condicional:
  debug and print(f"Loss: {loss:.4f}")  # Solo imprime si debug es True

  # Primer modelo disponible:
  modelo = modelo_gpu or modelo_cpu or modelo_dummy
"""


# ===========================================================================
# CAPÍTULO 4: CONDICIONALES — if / elif / else
# ===========================================================================

print("\n=== CONDICIONALES ===")

"""
La estructura de decisión más fundamental en cualquier lenguaje.
"""

# ─── if básico ───
temperatura = 35

if temperatura > 30:
    print(f"{temperatura}°C: Hace mucho calor")

# ─── if / else ───
edad = 17

if edad >= 18:
    print("Es adulto")
else:
    print(f"Es menor (tiene {edad} años)")

# ─── if / elif / else ───
puntuacion = 85

if puntuacion >= 90:
    grade = "A"
elif puntuacion >= 80:
    grade = "B" 
elif puntuacion >= 70:
    grade = "C"
elif puntuacion >= 60:
    grade = "D"
else:
    grade = "F"

print(f"\nPuntuación {puntuacion}: Grade {grade}")

"""
REGLAS IMPORTANTES:
1. Solo se ejecuta UNA rama (la primera que sea True)
2. else es OPCIONAL
3. Puedes tener tantos elif como quieras
4. La indentación es OBLIGATORIA (4 espacios por convención)
"""

# ─── Operador ternario (expresión condicional) ───
print("\n--- Operador ternario ---")

# Sintaxis: valor_si_true IF condición ELSE valor_si_false
x = 42
resultado = "par" if x % 2 == 0 else "impar"
print(f"{x} es {resultado}")

# Anidado (evitar si es complejo)
valor = 0
signo = "positivo" if valor > 0 else "negativo" if valor < 0 else "cero"
print(f"{valor} es {signo}")

"""
Cuándo usar ternario:
  ✅ Asignaciones simples: x = a if condicion else b
  ❌ Lógica compleja: usa if/elif/else normal
  ❌ Efectos secundarios: no pongas print() dentro
  
EN IA:
  # Activación condicional:
  activation = "relu" if use_relu else "gelu"
  
  # Device selection:
  device = "cuda" if torch.cuda.is_available() else "cpu"
"""


# ===========================================================================
# CAPÍTULO 5: MATCH / CASE — PATTERN MATCHING (Python 3.10+)
# ===========================================================================

"""
Python 3.10 introdujo match/case, que es MUCHO más potente que
un simple switch/case de otros lenguajes.

Es STRUCTURAL PATTERN MATCHING: puede hacer matching por estructura,
tipo, valores, y más.
"""

print("\n=== MATCH / CASE ===")

# ─── Matching simple (como switch) ───
def clasificar_status(status_code):
    match status_code:
        case 200:
            return "OK"
        case 301:
            return "Redirect"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:    # _ es el wildcard (como default en switch)
            return f"Unknown ({status_code})"

for code in [200, 404, 500, 418]:
    print(f"  HTTP {code}: {clasificar_status(code)}")

# ─── Matching por estructura (lo potente) ───
print("\n--- Matching por estructura ---")

def procesar_comando(comando):
    match comando.split():
        case ["entrenar", modelo]:
            print(f"  Entrenando modelo: {modelo}")
        case ["evaluar", modelo, dataset]:
            print(f"  Evaluando {modelo} con {dataset}")
        case ["predecir", modelo, *datos]:
            print(f"  Prediciendo con {modelo}, datos: {datos}")
        case ["salir" | "exit" | "quit"]:
            print("  Cerrando...")
        case _:
            print(f"  Comando no reconocido: {comando}")

procesar_comando("entrenar bert")
procesar_comando("evaluar gpt datos_test")
procesar_comando("predecir resnet img1 img2 img3")
procesar_comando("salir")

# ─── Matching por tipo ───
print("\n--- Matching por tipo ---")

def procesar_dato(dato):
    match dato:
        case int(n) if n > 0:
            print(f"  Entero positivo: {n}")
        case int(n):
            print(f"  Entero no positivo: {n}")
        case float(f):
            print(f"  Float: {f}")
        case str(s) if len(s) > 0:
            print(f"  String no vacío: '{s}'")
        case list() as l if len(l) > 0:
            print(f"  Lista con {len(l)} elementos")
        case None:
            print("  None recibido")
        case _:
            print(f"  Tipo desconocido: {type(dato)}")

for dato in [42, -5, 3.14, "hola", [1,2,3], None, ""]:
    procesar_dato(dato)

# ─── Matching con diccionarios ───
print("\n--- Matching con dicts ---")

def procesar_config(config):
    match config:
        case {"model": modelo, "epochs": int(epochs), "lr": float(lr)}:
            print(f"  Config completa: {modelo}, {epochs} epochs, lr={lr}")
        case {"model": modelo, "epochs": int(epochs)}:
            print(f"  Sin lr: {modelo}, {epochs} epochs (lr default)")
        case {"model": modelo}:
            print(f"  Solo modelo: {modelo} (defaults)")
        case _:
            print(f"  Config inválida: {config}")

procesar_config({"model": "bert", "epochs": 10, "lr": 0.001})
procesar_config({"model": "gpt", "epochs": 5})
procesar_config({"model": "llama"})
procesar_config({})

"""
PATTERN MATCHING EN IA:
  - Procesar respuestas de APIs con diferentes formatos
  - Parsear configuraciones de entrenamiento
  - Routing de comandos en agentes IA
  - Validar inputs de diferente estructura
  - Procesar outputs de LLMs con diferentes formatos
"""


# ===========================================================================
# CAPÍTULO 6: BUCLES — for y while
# ===========================================================================

print("\n=== BUCLES ===")

# ─── for: iterar sobre secuencias ───
print("--- for ---")

# Sobre una lista
modelos = ["bert", "gpt", "llama", "mistral"]
for modelo in modelos:
    print(f"  Modelo: {modelo}")

# Sobre un string
for char in "PYTHON":
    print(f"  {char}", end=" ")
print()

# Sobre un range
print("\n  Números del 0 al 4:")
for i in range(5):
    print(f"    {i}")

# range(inicio, fin, paso)
print("  Pares del 0 al 10:")
for i in range(0, 11, 2):
    print(f"    {i}", end=" ")
print()

# ─── enumerate: cuando necesitas el índice ───
print("\n--- enumerate ---")

for i, modelo in enumerate(modelos):
    print(f"  [{i}] {modelo}")

# Con índice inicial diferente
for i, modelo in enumerate(modelos, start=1):
    print(f"  {i}. {modelo}")

# ─── zip: iterar sobre múltiples secuencias en paralelo ───
print("\n--- zip ---")

nombres = ["GPT-4", "Claude", "Gemini"]
empresas = ["OpenAI", "Anthropic", "Google"]
fechas = [2023, 2024, 2024]

for nombre, empresa, fecha in zip(nombres, empresas, fechas):
    print(f"  {nombre} ({empresa}, {fecha})")

"""
zip() se detiene en la secuencia MÁS CORTA.
Para usar la más larga: itertools.zip_longest()
"""

# ─── Iterar sobre diccionarios ───
print("\n--- Iterar dicts ---")

hiperparams = {"lr": 0.001, "epochs": 50, "batch_size": 32, "dropout": 0.1}

# Solo claves (default)
print("  Claves:", list(hiperparams.keys()))

# Solo valores
print("  Valores:", list(hiperparams.values()))

# Pares clave-valor
for key, value in hiperparams.items():
    print(f"  {key}: {value}")


# ─── while: bucle condicional ───
print("\n--- while ---")

# Básico
contador = 5
while contador > 0:
    print(f"  Cuenta atrás: {contador}")
    contador -= 1
print("  ¡Despegue!")

# while con condición de salida
# (simulando un training loop básico)
import random

loss = 10.0
epoch = 0
print("\n  Simulación de training:")
while loss > 0.5:
    epoch += 1
    loss *= random.uniform(0.7, 0.95)  # simular descenso
    if epoch % 5 == 0 or loss <= 0.5:
        print(f"  Epoch {epoch:3d}: loss = {loss:.4f}")

print(f"  Convergió en {epoch} epochs")


# ─── break, continue, else en bucles ───
print("\n--- break, continue, else ---")

# break: sale del bucle INMEDIATAMENTE
print("  break:")
for i in range(100):
    if i == 5:
        print(f"    Encontrado en posición {i}")
        break
else:
    # else en for: se ejecuta SOLO si NO hubo break
    print("    No encontrado")

# continue: salta a la siguiente iteración
print("\n  continue (solo pares):")
for i in range(10):
    if i % 2 != 0:
        continue  # salta impares
    print(f"    {i}", end=" ")
print()

# else en for (poco conocido pero útil)
print("\n  else en for:")

def buscar_en_lista(lista, objetivo):
    for item in lista:
        if item == objetivo:
            return f"Encontrado: {objetivo}"
    else:
        return f"No encontrado: {objetivo}"

print(f"  {buscar_en_lista([1,2,3,4,5], 3)}")
print(f"  {buscar_en_lista([1,2,3,4,5], 9)}")

"""
PATRÓN ÚTIL EN IA — for/else para búsqueda:

  # Buscar el primer checkpoint válido:
  for checkpoint_path in checkpoint_paths:
      if os.path.exists(checkpoint_path):
          model.load(checkpoint_path)
          break
  else:
      # Si ningún checkpoint existe → entrenar desde cero
      print("No se encontró checkpoint, entrenando desde cero")
"""


# ===========================================================================
# CAPÍTULO 7: COMPREHENSIONS — PYTHON POWER
# ===========================================================================

"""
Las comprehensions son la forma PYTHÓNICA de crear listas, dicts y sets
a partir de iterables. Son más concisas Y más rápidas que bucles for.
"""

print("\n=== COMPREHENSIONS ===")

# ─── List comprehension ───
print("--- List comprehension ---")

# Without comprehension:
cuadrados_loop = []
for i in range(10):
    cuadrados_loop.append(i ** 2)

# With comprehension:
cuadrados = [i ** 2 for i in range(10)]
print(f"  Cuadrados: {cuadrados}")

# Con filtro (if)
pares = [i for i in range(20) if i % 2 == 0]
print(f"  Pares: {pares}")

# Con transformación + filtro
palabras = ["hola", "machine", "a", "learning", "de", "python"]
largas = [p.upper() for p in palabras if len(p) > 3]
print(f"  Palabras largas: {largas}")

# ─── Dict comprehension ───
print("\n--- Dict comprehension ---")

cuadrados_dict = {i: i**2 for i in range(6)}
print(f"  Cuadrados dict: {cuadrados_dict}")

# Invertir un diccionario
original = {"a": 1, "b": 2, "c": 3}
invertido = {v: k for k, v in original.items()}
print(f"  Original: {original}")
print(f"  Invertido: {invertido}")

# Desde dos listas
modelos = ["bert", "gpt", "llama"]
scores = [0.92, 0.95, 0.89]
ranking = {m: s for m, s in zip(modelos, scores)}
print(f"  Ranking: {ranking}")

# ─── Set comprehension ───
print("\n--- Set comprehension ---")

texto = "abracadabra"
caracteres_unicos = {c for c in texto}
print(f"  Caracteres únicos de '{texto}': {caracteres_unicos}")

# ─── Generator expression (lazy) ───
print("\n--- Generator expression ---")

# Usa () en vez de [] → NO crea toda la lista en memoria
suma_cuadrados = sum(i**2 for i in range(1_000_000))
print(f"  Suma de cuadrados 0..999999: {suma_cuadrados}")

"""
GENERATORS vs LIST COMPREHENSION:

  [x**2 for x in range(1_000_000)]   # → Crea una lista de 1M ítems en RAM
  (x**2 for x in range(1_000_000))   # → Genera uno a uno, sin almacenar todo

Para IA, los generators son CRUCIALES para procesar datasets grandes:
  - No cargas todo el dataset en memoria
  - Generas y procesas batch a batch
  - PyTorch DataLoader funciona con este principio
"""

# ─── Comprehensions anidadas ───
print("\n--- Comprehensions anidadas ---")

# Aplanar una lista de listas
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
plano = [num for fila in matriz for num in fila]
print(f"  Aplanado: {plano}")

# Equivalente con bucles:
# for fila in matriz:
#     for num in fila:
#         plano.append(num)

"""
REGLA DE LEGIBILIDAD:
  - 1 nivel de comprehension → ✅ úsalo siempre
  - 2 niveles → ⚠️ solo si es claro
  - 3+ niveles → ❌ usa bucles normales, nadie entiende eso
"""


# ===========================================================================
# CAPÍTULO 8: WALRUS OPERATOR (:=) — Python 3.8+
# ===========================================================================

"""
El operador walrus (:=) permite asignar Y usar un valor en la misma
expresión. El nombre viene de la cara del morse: :=)
"""

print("\n=== WALRUS OPERATOR (:=) ===")

# Sin walrus: calculas dos veces
datos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
if len(datos) > 5:
    print(f"  Lista larga: {len(datos)} elementos")  # len() calculado 2 veces

# Con walrus: calculas una vez
if (n := len(datos)) > 5:
    print(f"  Lista larga: {n} elementos")  # n ya tiene el valor

# Útil en comprehensions con filtro y transformación
import math
numeros = [2, -1, 4, -3, 16, -5, 9]
raices = [raiz for x in numeros if x >= 0 and (raiz := math.sqrt(x)) > 2]
print(f"  Raíces > 2: {raices}")

# Útil en while con lectura
print("\n  Simulando lectura de datos:")
import io
buffer = io.StringIO("línea1\nlínea2\nlínea3\n")
while (linea := buffer.readline()):
    print(f"    Leído: {linea.strip()}")

"""
EN IA:
  # Procesar batches hasta que se acaben:
  while (batch := next(data_iter, None)) is not None:
      loss = model.train_step(batch)

  # Filtrar y transformar en una pasada:
  features = [f for col in columns if (f := extract_feature(col)) is not None]
"""


# ===========================================================================
# CAPÍTULO 9: ITERACIÓN AVANZADA — enumerate, zip, reversed, sorted
# ===========================================================================

print("\n=== ITERACIÓN AVANZADA ===")

# ─── reversed() ───
print("--- reversed ---")
for i in reversed(range(5)):
    print(f"  {i}", end=" ")
print()

# ─── sorted() ───
print("\n--- sorted ---")
losses = [0.45, 0.23, 0.67, 0.12, 0.89, 0.34]
print(f"  Original: {losses}")
print(f"  Sorted:   {sorted(losses)}")
print(f"  Reversed: {sorted(losses, reverse=True)}")

# sorted con key
modelos = [("bert", 0.92), ("gpt", 0.95), ("llama", 0.89)]
por_score = sorted(modelos, key=lambda x: x[1], reverse=True)
print(f"  Por score: {por_score}")

# ─── any() y all() — evaluación lógica de iterables ───
print("\n--- any() y all() ---")

predicciones = [True, True, False, True, True]
print(f"  any({predicciones}): {any(predicciones)}")  # True si ALGUNO es True
print(f"  all({predicciones}): {all(predicciones)}")  # True si TODOS son True

# Uso práctico:
datos = [3.14, 2.71, None, 1.41]
hay_nulos = any(x is None for x in datos)
todos_positivos = all(x > 0 for x in datos if x is not None)
print(f"\n  ¿Hay nulos? {hay_nulos}")
print(f"  ¿Todos positivos? {todos_positivos}")

"""
any() y all() SON ESENCIALES EN IA:

  # ¿Algún gradiente es NaN?
  if any(torch.isnan(p.grad).any() for p in model.parameters()):
      print("¡Gradiente NaN detectado!")

  # ¿Todos los tests pasan?
  if all(test() for test in validation_tests):
      model.save()

  # ¿Algún feature tiene valores faltantes?
  if any(df[col].isna().any() for col in df.columns):
      print("Datos con valores faltantes")
"""


# ===========================================================================
# CAPÍTULO 10: TRUTHINESS Y FALSINESS — DEEP DIVE
# ===========================================================================

"""
Esto es TAN fundamental que merece su propia sección detallada.

En Python, CUALQUIER objeto puede evaluarse como booleano.
No solo True/False, sino CUALQUIER valor.

VALORES FALSY (se evalúan como False):
  - None
  - False
  - 0, 0.0, 0j (cero numérico)
  - '' (string vacío)
  - [] (lista vacía)
  - () (tupla vacía)
  - {} (dict vacío)
  - set() (set vacío)
  - range(0) (range vacío)
  - Objetos cuyo __bool__() o __len__() devuelven False/0

TODO LO DEMÁS ES TRUTHY.
"""

print("\n=== TRUTHINESS / FALSINESS ===")

print("--- Valores falsy ---")
falsys = [None, False, 0, 0.0, 0j, '', [], (), {}, set(), range(0)]
for val in falsys:
    print(f"  bool({str(val):>10}) = {bool(val)}  (tipo: {type(val).__name__})")

print("\n--- Valores truthy ---")
truthys = [True, 1, -1, 0.001, 'x', [0], (0,), {0: 0}, {0}, ' ']
for val in truthys:
    print(f"  bool({str(val):>10}) = {bool(val)}  (tipo: {type(val).__name__})")

"""
TRAMPA COMÚN: [0] es TRUTHY (lista con un elemento, aunque sea 0).
  bool([])  → False (lista vacía)
  bool([0]) → True  (lista con UN elemento)

Otro error común:
  if x == True:    # ❌ MAL — compara valor
  if x is True:    # ⚠️ Demasiado estricto
  if x:            # ✅ CORRECTO — pythónico

Python SIEMPRE usa truthiness en condicionales:
  if lista:        # ← equivale a: if len(lista) > 0
  if nombre:       # ← equivale a: if nombre != ''
  if resultado:    # ← equivale a: if resultado is not None and resultado != 0
"""

# ─── Definir truthiness personalizada ───
print("\n--- __bool__ y __len__ personalizados ---")

class Dataset:
    """Ejemplo: un dataset que es truthy si tiene datos."""
    def __init__(self, datos):
        self.datos = datos

    def __len__(self):
        return len(self.datos)

    def __bool__(self):
        return len(self.datos) > 0

    def __repr__(self):
        return f"Dataset({len(self.datos)} items)"

ds_lleno = Dataset([1, 2, 3])
ds_vacio = Dataset([])

print(f"  {ds_lleno}: bool = {bool(ds_lleno)}")
print(f"  {ds_vacio}: bool = {bool(ds_vacio)}")

# Uso natural en condicionales:
if ds_lleno:
    print(f"  Dataset listo para entrenar ({len(ds_lleno)} items)")
if not ds_vacio:
    print(f"  Dataset vacío, necesita datos")


# ===========================================================================
# CAPÍTULO 11: is vs == — IDENTIDAD vs IGUALDAD
# ===========================================================================

"""
Esta distinción es CRÍTICA y fuente de bugs sutiles.

  ==  : compara VALORES (¿contienen lo mismo?)
  is  : compara IDENTIDAD (¿son el MISMO objeto en memoria?)

REGLA: usa == para comparar valores, usa 'is' SOLO para None.
"""

print("\n=== is vs == ===")

# Con enteros pequeños: Python los cachea (-5 a 256)
a = 256
b = 256
print(f"  a=256, b=256: a == b → {a == b}, a is b → {a is b}")

# Con enteros grandes: son objetos diferentes
a = 1000
b = 1000
print(f"  a=1000, b=1000: a == b → {a == b}, a is b → {a is b}")

"""
Python hace "integer interning" de -5 a 256.
  Esos enteros son singletons: siempre el MISMO objeto.
  Fuera de ese rango, cada asignación crea un objeto nuevo.

NUNCA uses 'is' para comparar números o strings.
El resultado depende de optimizaciones internas de CPython
que pueden cambiar entre versiones.
"""

# Caso correcto: comparar con None
x = None
print(f"\n  x is None: {x is None}")       # ✅ CORRECTO
print(f"  x == None: {x == None}")          # ⚠️ funciona pero no pythónico

# Caso correcto: comparar con True/False (raro pero válido)
val = True
print(f"  val is True: {val is True}")      # ✅ pero mejor usar: if val:

"""
REGLA DE ORO:
  if x is None:        # ✅ comparar con None
  if x is not None:    # ✅ negar None
  if x == 42:          # ✅ comparar valores
  if x is 42:          # ❌ NUNCA — puede fallar
  if x:                # ✅ verificar truthiness
"""

# Listas y mutabilidad
lista1 = [1, 2, 3]
lista2 = [1, 2, 3]
lista3 = lista1

print(f"\n  lista1 == lista2: {lista1 == lista2}")  # True (mismo contenido)
print(f"  lista1 is lista2: {lista1 is lista2}")    # False (objetos diferentes)
print(f"  lista1 is lista3: {lista1 is lista3}")    # True (misma referencia)

# Modificar lista3 MODIFICA lista1 (son el mismo objeto):
lista3.append(4)
print(f"  Tras lista3.append(4): lista1 = {lista1}")  # [1, 2, 3, 4] !!


# ===========================================================================
# CAPÍTULO 12: pass, Ellipsis, y PLACEHOLDERS
# ===========================================================================

"""
pass y Ellipsis (...) son herramientas para código incompleto.
"""

print("\n=== pass y Ellipsis ===")

# ─── pass: no hacer nada ───
# Necesario porque Python no permite bloques vacíos

# Clase vacía (placeholder):
class FuturoModelo:
    pass

# Función vacía (TODO):
def entrenar():
    pass  # TODO: implementar

# Condicional vacío:
x = 5
if x > 0:
    pass  # De momento no hacemos nada con positivos
else:
    print("Negativo")

# ─── Ellipsis (...): placeholder moderno ───
# Es un valor real de Python: type(Ellipsis) → <class 'ellipsis'>

def cargar_datos():
    ...  # Más moderno que pass para indicar "por implementar"

# En type hints (visto en módulos posteriores):
# def procesar(datos: list[...]) → ...:  # placeholder

print(f"  type(Ellipsis): {type(Ellipsis)}")
print(f"  ... is Ellipsis: {... is Ellipsis}")


# ===========================================================================
# CAPÍTULO 13: PATRONES AVANZADOS DE CONTROL DE FLUJO
# ===========================================================================

print("\n=== PATRONES AVANZADOS ===")

# ─── Diccionario como switch ───
"""
Antes de match/case (Python < 3.10), se usaba dict como switch.
Aún es útil cuando las acciones son funciones.
"""

print("--- Dict dispatch ---")

def relu(x):
    return max(0, x)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def tanh(x):
    return math.tanh(x)

activaciones = {
    "relu": relu,
    "sigmoid": sigmoid,
    "tanh": tanh,
}

for nombre, fn in activaciones.items():
    resultado = fn(0.5)
    print(f"  {nombre}(0.5) = {resultado:.4f}")

# ─── Guard clauses (early return) ───
print("\n--- Guard clauses ---")

def procesar_batch(batch):
    """Procesa un batch de datos con early returns."""
    # Guards: verificar condiciones de fallo PRIMERO
    if batch is None:
        return "Error: batch es None"

    if len(batch) == 0:
        return "Error: batch vacío"

    if any(x < 0 for x in batch):
        return "Error: valores negativos"

    # Solo llegamos aquí si todo está bien
    return f"Batch procesado: {len(batch)} items, media={sum(batch)/len(batch):.2f}"

# Tests
print(f"  {procesar_batch(None)}")
print(f"  {procesar_batch([])}")
print(f"  {procesar_batch([1, -2, 3])}")
print(f"  {procesar_batch([1, 2, 3, 4, 5])}")

"""
GUARD CLAUSES es un patrón FUNDAMENTAL en código profesional.
En vez de anidar if dentro de if dentro de if:

  ❌ MAL:
  def procesar(x):
      if x is not None:
          if len(x) > 0:
              if all(v >= 0 for v in x):
                  # ... código real ...
                  
  ✅ BIEN (guards):
  def procesar(x):
      if x is None: return error
      if len(x) == 0: return error
      if any(v < 0 for v in x): return error
      # ... código real (sin anidación) ...
"""

# ─── for/else para búsqueda con fallback ───
print("\n--- for/else patrón de búsqueda ---")

checkpoints = ["model_v3.pt", "model_v2.pt", "model_v1.pt"]
existentes = {"model_v2.pt"}  # simular archivos que existen

for cp in checkpoints:
    if cp in existentes:
        print(f"  Cargando checkpoint: {cp}")
        break
else:
    print("  No se encontró checkpoint, entrenando desde cero")


# ===========================================================================
# CAPÍTULO 14: ITERACIÓN FUNCIONAL — map, filter, reduce
# ===========================================================================

print("\n=== map, filter, reduce ===")

"""
Estos son los pilares de la programación funcional.
Los vemos aquí porque se usan en combinación con bucles y comprehensions.
"""

# ─── map: aplicar función a cada elemento ───
print("--- map ---")
numeros = [1, 4, 9, 16, 25]
raices = list(map(math.sqrt, numeros))
print(f"  map(sqrt, {numeros}) = {raices}")

# Equivalente con comprehension:
raices_comp = [math.sqrt(n) for n in numeros]
print(f"  Comprehension: {raices_comp}")

# ─── filter: filtrar elementos ───
print("\n--- filter ---")
numeros = list(range(-5, 6))
positivos = list(filter(lambda x: x > 0, numeros))
print(f"  filter(>0, {numeros})")
print(f"  = {positivos}")

# ─── reduce: acumular valor ───
print("\n--- reduce ---")
from functools import reduce

numeros = [1, 2, 3, 4, 5]
producto = reduce(lambda a, b: a * b, numeros)
print(f"  reduce(*, {numeros}) = {producto}")  # 1*2*3*4*5 = 120

# Equivalente imperativo:
producto_loop = 1
for n in numeros:
    producto_loop *= n
print(f"  Loop equivalente: {producto_loop}")

"""
RECOMENDACIÓN:
  - map/filter → usa comprehensions (más legible en Python)
  - reduce → usa funciones built-in (sum, max, min, math.prod)
  - Solo usa map/filter cuando ya tienes una función nombrada:
    list(map(str.upper, palabras))  # ← esto es legible
    [p.upper() for p in palabras]   # ← esto también
"""


# ===========================================================================
# CAPÍTULO 15: RESUMEN Y SIGUIENTE ARCHIVO
# ===========================================================================

"""
LO QUE HAS APRENDIDO:

1. BOOLEANOS:
   - bool hereda de int (True=1, False=0)
   - sum() de booleanos para contar True
   - Truthiness: falsy (0, None, vacío) vs truthy (todo lo demás)
   - __bool__ y __len__ para definir truthiness personalizada

2. COMPARACIONES:
   - ==, !=, <, >, <=, >=
   - Encadenamiento: 0 <= x <= 1
   - is vs == (identidad vs valor)
   - Integer interning: Python cachea -5 a 256

3. OPERADORES LÓGICOS:
   - and devuelve el primer falsy o el último valor
   - or devuelve el primer truthy o el último valor
   - Cortocircuito para valores por defecto: x = valor or default
   - not invierte la truthiness

4. CONDICIONALES:
   - if / elif / else
   - Operador ternario: a if cond else b
   - match/case: pattern matching potente (Python 3.10+)
   - Guard clauses: early return para evitar anidación

5. BUCLES:
   - for sobre iterables (listas, range, dicts, strings)
   - while para condiciones
   - break, continue, else en bucles
   - enumerate, zip, reversed, sorted

6. COMPREHENSIONS:
   - List: [expr for x in iterable if cond]
   - Dict: {k: v for ...}
   - Set: {expr for ...}
   - Generator: (expr for ...) — lazy, ahorra memoria

7. WALRUS: (n := expr) para asignar y usar en una expresión

8. FUNCIONAL: map, filter, reduce (prefer comprehensions)

9. UTILIDADES: any(), all(), pass, Ellipsis, dict dispatch

SIGUIENTE ARCHIVO: Módulo 02 → Estructuras de Datos
→ Listas como la estructura de datos fundamental
→ Todos los métodos
→ Slicing avanzado
→ Listas anidadas (matrices)
→ Complejidad de operaciones (Big O)
→ Listas en el contexto de datasets y batches de IA
"""

