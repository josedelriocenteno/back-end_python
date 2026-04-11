# ===========================================================================
# 01_notacion_big_o_y_analisis_memoria.py
# ===========================================================================
# MÓDULO 03: ALGORITMIA Y COMPLEJIDAD COMPUTACIONAL
# ARCHIVO 01: Notación Big-O, Análisis Asintótico y Perfilado de Memoria
# ===========================================================================
#
# OBJETIVO ABSOLUTO (1000+ LÍNEAS):
# Dominar la notación Big-O no como una tabla que memorizar, sino como
# una herramienta de INGENIERÍA para predecir el rendimiento de tu código
# ANTES de ejecutarlo. Cuando un ingeniero de IA dice "esto es O(N²)",
# no está haciendo poesía: está calculando si su pipeline aguantará 
# 10 millones de registros o si la GPU se quedará sin memoria.
#
# CONTENIDO:
#   1. Qué es Big-O realmente (Upper Bound Asintótico).
#   2. Las 7 complejidades fundamentales con código Y benchmarks.
#   3. Reglas para calcular Big-O de cualquier función.
#   4. Complejidad espacial (memoria) además de temporal.
#   5. Análisis amortizado (por qué list.append es O(1) "amortizado").
#   6. Perfilado real con time, tracemalloc y cProfile.
#   7. Big-O de todas las estructuras de Python (tabla definitiva).
#   8. Ejercicios: detectar la complejidad de funciones reales de ML.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import time
import sys
import random
import tracemalloc
from functools import lru_cache


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 1: ¿QUÉ ES BIG-O REALMENTE?                                  ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: BIG-O — LA MATEMÁTICA DEL RENDIMIENTO ===")
print("=" * 80)

"""
Big-O NO mide el TIEMPO de ejecución. Mide cómo ESCALA el tiempo (o la 
memoria) cuando el INPUT CRECE.

Si tu función procesa N documentos:
- O(1): Tarda lo MISMO con 10 documentos que con 10 millones.
- O(N): Si duplicas los documentos, tardas el doble.
- O(N²): Si duplicas los documentos, tardas 4 veces más.
- O(2^N): Cada documento extra DUPLICA el tiempo total.

DEFINICIÓN FORMAL (para entrevistas):
f(n) es O(g(n)) si existen constantes c > 0 y n₀ tal que:
    f(n) ≤ c · g(n)  para todo n ≥ n₀

En lenguaje humano: "a partir de cierto punto, f(n) nunca crece más 
rápido que g(n) multiplicado por una constante".

REGLA CRÍTICA: Big-O describe el PEOR CASO (upper bound).
Si buscas un elemento en una lista:
- Mejor caso: el primero (O(1)) 
- Peor caso: el último o no existe (O(N))
- Big-O dice: O(N), porque nos preparamos para lo peor.

EN IA, ESTO IMPORTA PORQUE:
- Un tokenizador que es O(N²) con 1000 tokens funciona.
  Con 100,000 tokens en un documento largo, tu servidor muere.
- Un grid search con 5 hiperparámetros × 10 valores = 10⁵ combinaciones.
  Con 10 × 20 valores = 20¹⁰ = 10 BILLONES. Imposible.
"""

print("\n--- Las 7 complejidades fundamentales ---")
print("""
╔══════════════════╦═══════════════════╦════════════════════════════════╗
║ COMPLEJIDAD      ║ NOMBRE            ║ EJEMPLO EN IA                 ║
╠══════════════════╬═══════════════════╬════════════════════════════════╣
║ O(1)             ║ Constante         ║ dict[key], len(list)          ║
║ O(log N)         ║ Logarítmica       ║ Búsqueda binaria, bisect     ║
║ O(N)             ║ Lineal            ║ Recorrer un dataset           ║
║ O(N log N)       ║ Linearítmica      ║ sorted(), Timsort, Merge Sort ║
║ O(N²)            ║ Cuadrática        ║ Atención naive (sin Flash)    ║
║ O(2^N)           ║ Exponencial       ║ Subconjuntos, fuerza bruta   ║
║ O(N!)            ║ Factorial         ║ Permutaciones, TSP bruto     ║
╚══════════════════╩═══════════════════╩════════════════════════════════╝
""")


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: O(1) — TIEMPO CONSTANTE ===")
print("=" * 80)

"""
O(1) significa que la operación tarda lo MISMO sin importar el tamaño
del input. No importa si tienes 10 o 10 millones de elementos.

En Python, las operaciones O(1) más importantes son:
- dict[key]: acceso por clave (hash table lookup).
- list[index]: acceso por índice (array de punteros).
- len(anything): almacenado como campo, no se recalcula.
- set.add(x): inserción en hash table.
- deque.appendleft(x): inserción por la izquierda.
"""

print("\n--- Benchmark: dict lookup O(1) — NO crece con N ---")

def benchmark_dict_lookup(n: int) -> float:
    """Mide el tiempo de un lookup en un dict de N elementos."""
    d = {f"key_{i}": i for i in range(n)}
    clave_buscar = f"key_{n - 1}"  # La última clave (peor caso en lista)
    
    inicio = time.perf_counter()
    for _ in range(100_000):
        _ = d[clave_buscar]
    return time.perf_counter() - inicio

for n in [100, 10_000, 1_000_000]:
    t = benchmark_dict_lookup(n)
    print(f"  dict[key] con N={n:>10,}: {t*1000:.2f} ms (100K lookups)")

print("  -> El tiempo es CONSTANTE, no crece con N. Eso es O(1).")


print("\n" + "=" * 80)
print("=== CAPÍTULO 3: O(log N) — TIEMPO LOGARÍTMICO ===")
print("=" * 80)

"""
O(log N) significa que cada paso DIVIDE el problema a la mitad.
Si tienes 1,000,000 de elementos, solo necesitas ~20 pasos (log₂(10⁶) ≈ 20).

El algoritmo estrella es la BÚSQUEDA BINARIA:
- Requiere datos ORDENADOS.
- Mira el elemento del MEDIO.
- Si es menor, descarta la mitad inferior.
- Si es mayor, descarta la mitad superior.
- Repite hasta encontrar o agotar.

En Python: el módulo `bisect` implementa búsqueda binaria a nivel C.
"""

import bisect

print("\n--- Búsqueda binaria manual vs lineal ---")

def busqueda_lineal(lista: list, objetivo) -> int:
    """O(N): recorre toda la lista."""
    for i, x in enumerate(lista):
        if x == objetivo:
            return i
    return -1

def busqueda_binaria(lista: list, objetivo) -> int:
    """O(log N): divide a la mitad en cada paso."""
    izq, der = 0, len(lista) - 1
    while izq <= der:
        mid = (izq + der) // 2
        if lista[mid] == objetivo:
            return mid
        elif lista[mid] < objetivo:
            izq = mid + 1
        else:
            der = mid - 1
    return -1

# Benchmark
datos_ordenados = list(range(1_000_000))
objetivo = 999_999  # Peor caso para búsqueda lineal

inicio = time.perf_counter()
busqueda_lineal(datos_ordenados, objetivo)
t_lineal = time.perf_counter() - inicio

inicio = time.perf_counter()
for _ in range(10_000):  # Repetimos más porque es muy rápida
    busqueda_binaria(datos_ordenados, objetivo)
t_binaria = (time.perf_counter() - inicio) / 10_000

inicio = time.perf_counter()
for _ in range(10_000):
    bisect.bisect_left(datos_ordenados, objetivo)
t_bisect = (time.perf_counter() - inicio) / 10_000

print(f"  Lineal O(N) en 1M items:     {t_lineal*1000:.2f} ms")
print(f"  Binaria O(log N) manual:     {t_binaria*1000:.4f} ms")
print(f"  bisect (C-level) O(log N):   {t_bisect*1000:.4f} ms")
print(f"  Ratio lineal vs binaria: ~{t_lineal/t_binaria:.0f}x más lenta")


print("\n" + "=" * 80)
print("=== CAPÍTULO 4: O(N) — TIEMPO LINEAL ===")
print("=" * 80)

"""
O(N) significa que el tiempo crece PROPORCIONALMENTE al input.
Si duplicas los datos, tardas el doble. Es la complejidad "justa".

En ML, O(N) es el MÍNIMO necesario para:
- Leer un dataset (tienes que ver cada registro al menos una vez).
- Calcular la media, la desviación estándar, el min/max.
- Tokenizar un corpus (cada token se visita una vez).
- Normalizar un vector de features.

Si tu operación es O(N), tienes un algoritmo EFICIENTE.
"""

print("\n--- Benchmark: crecimiento lineal ---")

def suma_manual(lista: list) -> int:
    """O(N): visita cada elemento una vez."""
    total = 0
    for x in lista:
        total += x
    return total

for n in [100_000, 500_000, 1_000_000, 5_000_000]:
    datos = list(range(n))
    inicio = time.perf_counter()
    suma_manual(datos)
    t = time.perf_counter() - inicio
    print(f"  suma_manual(N={n:>10,}): {t*1000:.2f} ms")

print("  -> Si N se multiplica x5, el tiempo también se multiplica ~x5. Eso es O(N).")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: O(N log N) — TIEMPO LINEARÍTMICO ===")
print("=" * 80)

"""
O(N log N) es la complejidad de los mejores algoritmos de ordenación
basados en comparaciones: Timsort (Python), Merge Sort, Quick Sort.

¿Por qué no se puede ordenar más rápido que O(N log N)?
El "Decision Tree Lower Bound" demuestra matemáticamente que cualquier
algoritmo que compare elementos necesita al menos N log₂ N comparaciones
para distinguir entre las N! posibles permutaciones.

En IA, O(N log N) aparece en:
- Ordenar predicciones por confidence score (ranking).
- Construir árboles de decisión (en cada split, ordenas por feature).
- K-Nearest Neighbors con KD-Trees.
"""

print("\n--- Benchmark: sorted() es O(N log N) ---")

for n in [100_000, 500_000, 1_000_000, 2_000_000]:
    datos = [random.random() for _ in range(n)]
    inicio = time.perf_counter()
    sorted(datos)
    t = time.perf_counter() - inicio
    print(f"  sorted(N={n:>10,}): {t*1000:.2f} ms")

print("  -> Crece más rápido que lineal pero mucho menos que cuadrático.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 6: O(N²) — TIEMPO CUADRÁTICO ===")
print("=" * 80)

"""
O(N²) significa que el tiempo crece con el CUADRADO del input.
Si duplicas N, el tiempo se CUADRUPLICA. Con 10x más datos, 100x más tiempo.

O(N²) es la señal de alarma #1 en IA. Aparece cuando:
- Tienes un loop dentro de otro loop sobre los mismos datos.
- Usas list.insert(0, x) en un bucle (cada insert es O(N)).
- Comparas todos los pares de elementos (distancia entre embeddings naive).
- Self-attention en Transformers: cada token atiende a TODOS los demás.
  Con secuencia de 4096 tokens: 4096² = 16.7 millones de operaciones.
  Flash Attention de Tri Dao existe para resolver exactamente esto.
"""

print("\n--- Ejemplo: detectar duplicados O(N²) vs O(N) ---")

def tiene_duplicados_cuadratico(lista: list) -> bool:
    """O(N²): compara cada par de elementos."""
    n = len(lista)
    for i in range(n):
        for j in range(i + 1, n):
            if lista[i] == lista[j]:
                return True
    return False

def tiene_duplicados_lineal(lista: list) -> bool:
    """O(N): usa un set para tracking O(1) por consulta."""
    vistos = set()
    for x in lista:
        if x in vistos:  # O(1) lookup en set
            return True
        vistos.add(x)  # O(1) inserción en set
    return False

n_test = 10_000
datos_sin_dup = list(range(n_test))

inicio = time.perf_counter()
tiene_duplicados_cuadratico(datos_sin_dup)
t_cuadratico = time.perf_counter() - inicio

inicio = time.perf_counter()
tiene_duplicados_lineal(datos_sin_dup)
t_lineal = time.perf_counter() - inicio

print(f"  O(N²) con N={n_test}: {t_cuadratico*1000:.2f} ms")
print(f"  O(N) con N={n_test}:  {t_lineal*1000:.2f} ms")
print(f"  Ratio: O(N²) es ~{t_cuadratico/t_lineal:.0f}x más lento")
print(f"  Con N=1M, O(N²) tardaría ~{(t_cuadratico * (1_000_000/n_test)**2)/3600:.0f} HORAS.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 7: O(2^N) Y O(N!) — LO INTRATABLE ===")
print("=" * 80)

"""
Estas complejidades son INTRATABLES para todo N > 30.
No importa cuántas GPUs tengas: si el algoritmo es O(2^N), estás acabado.

O(2^N) aparece cuando:
- Generas TODOS los subconjuntos de un conjunto (power set).
- Fibonacci recursivo sin memoización.
- Fuerza bruta en problemas de optimización combinatoria.

O(N!) aparece cuando:
- Generas TODAS las permutaciones.
- Travelling Salesman Problem (TSP) por fuerza bruta.
"""

print("\n--- O(2^N): Fibonacci sin memoización ---")

def fibonacci_recursivo(n: int) -> int:
    """O(2^N): cada llamada genera DOS llamadas más."""
    if n <= 1:
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)

# Solo hasta n=35 porque más allá es intratable
for n in [10, 20, 25, 30]:
    inicio = time.perf_counter()
    resultado = fibonacci_recursivo(n)
    t = time.perf_counter() - inicio
    print(f"  fib({n:>2}) = {resultado:>15,}  Tiempo: {t*1000:.2f} ms")

print("  -> Cada incremento de 5 multiplica el tiempo por ~30x. INTRATABLE.")


print("\n--- O(2^N) salvado con memoización -> O(N) ---")

@lru_cache(maxsize=None)
def fibonacci_memo(n: int) -> int:
    """O(N) con memoización: cada subproblema se calcula UNA SOLA VEZ."""
    if n <= 1:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)

for n in [10, 20, 50, 100, 500]:
    inicio = time.perf_counter()
    resultado = fibonacci_memo(n)
    t = time.perf_counter() - inicio
    print(f"  fib_memo({n:>3}) = {str(resultado)[:20]:>20}...  Tiempo: {t*1000:.4f} ms")

print("  -> lru_cache convierte O(2^N) en O(N). Magia de programación dinámica.")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 2: REGLAS PARA CALCULAR BIG-O                                 ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 8: LAS 5 REGLAS DE ORO PARA CALCULAR BIG-O ===")
print("=" * 80)

"""
REGLA 1: IGNORA LAS CONSTANTES
    O(2N) = O(N).  O(100N) = O(N).  O(0.5N²) = O(N²).
    Las constantes no importan cuando N tiende a infinito.

REGLA 2: QUÉDATE CON EL TÉRMINO DOMINANTE
    O(N² + N) = O(N²).  O(N³ + N² + N) = O(N³).
    Cuando N es grande, el término menor es despreciable.

REGLA 3: LOOPS ANIDADOS MULTIPLICAN
    for i in range(N):       # O(N)
        for j in range(N):   # × O(N)
            ...              # = O(N²)

REGLA 4: LOOPS SECUENCIALES SUMAN
    for i in range(N):   # O(N)
        ...
    for j in range(M):   # O(M)
        ...
    # Total: O(N + M). Si M = N, entonces O(2N) = O(N).

REGLA 5: RECURSIÓN — CUENTA EL ÁRBOL DE LLAMADAS
    Si cada llamada genera K llamadas y hay D niveles de profundidad:
    O(K^D).
    Fibonacci: K=2, D=N → O(2^N).
    Merge Sort: K=2, D=log N → O(N log N) (cada nivel procesa N elementos).
"""

print("\n--- Ejercicio: ¿Cuál es la complejidad? ---")

def ejemplo_1(lista: list) -> int:
    """¿Complejidad?"""
    total = 0                           # O(1)
    for x in lista:                     # O(N)
        total += x                      # O(1)
    return total                        # O(1)
# RESPUESTA: O(N). Un solo loop sobre N elementos.

def ejemplo_2(lista: list) -> list:
    """¿Complejidad?"""
    resultado = []                      # O(1)
    for x in lista:                     # O(N)
        if x not in resultado:          # O(N) buscar en lista NO es O(1)
            resultado.append(x)         # O(1) amortizado
    return resultado
# RESPUESTA: O(N²). "x not in resultado" es O(N) dentro de un O(N) loop.
# SOLUCIÓN: usar set() para el tracking -> O(N) total.

def ejemplo_3(lista_a: list, lista_b: list) -> list:
    """¿Complejidad si len(a) = N, len(b) = M?"""
    resultado = []
    for a in lista_a:                   # O(N)
        resultado.append(a * 2)         # O(1)
    for b in lista_b:                   # O(M)
        resultado.append(b + 1)         # O(1)
    return resultado
# RESPUESTA: O(N + M). Dos loops secuenciales sobre inputs DIFERENTES.

def ejemplo_4(n: int) -> list:
    """¿Complejidad?"""
    resultado = []
    i = n
    while i > 0:                        # ¿Cuántas veces?
        resultado.append(i)
        i = i // 2                      # Se divide a la mitad cada vez
    return resultado
# RESPUESTA: O(log N). El loop ejecuta log₂(N) veces.

print(f"  ejemplo_1([1..N]):  O(N)    -> {ejemplo_1([1,2,3,4,5])}")
print(f"  ejemplo_2([1,2,1,3]): O(N²) -> {ejemplo_2([1,2,1,3,2])}")
print(f"  ejemplo_3(a,b):    O(N+M)   -> {ejemplo_3([1,2],[3,4])}")
print(f"  ejemplo_4(16):     O(log N) -> {ejemplo_4(16)}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 3: COMPLEJIDAD ESPACIAL (MEMORIA)                             ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 9: COMPLEJIDAD ESPACIAL — CUÁNTA RAM CONSUME ===")
print("=" * 80)

"""
Big-O no solo mide TIEMPO. También mide ESPACIO (memoria RAM).

La complejidad espacial cuenta cuánta MEMORIA EXTRA necesita tu algoritmo
(sin contar el input original).

Ejemplos:
- sum(lista): O(1) espacio. Solo una variable acumuladora.
- sorted(lista): O(N) espacio. Crea una NUEVA lista ordenada.
- lista.sort(): O(1) espacio*. Ordena IN-PLACE (*Timsort usa O(N) temporal).
- Fibonacci memo: O(N) espacio. Cachea todos los subproblemas.
- Matriz N×N: O(N²) espacio.

EN IA, la memoria es a menudo MÁS LIMITANTE que el tiempo:
- Un modelo BERT-large tiene 340M parámetros × 4 bytes (float32) = 1.3 GB.
- Self-attention: O(N²) MEMORIA. Con N=4096 tokens y batch=32:
  32 × 4096 × 4096 × 4 bytes = 2 GB solo para la matriz de atención.
- Esto es por lo que Flash Attention fue revolucionario: reduce 
  ESPACIO de O(N²) a O(N) calculando la atención por bloques.
"""

print("\n--- Midiendo complejidad espacial con tracemalloc ---")

def crear_lista_nueva(n: int) -> list:
    """O(N) espacio: crea N elementos nuevos."""
    return [i * 2 for i in range(n)]

def sumar_in_place(lista: list) -> int:
    """O(1) espacio: solo una variable extra."""
    total = 0
    for x in lista:
        total += x
    return total

for n in [10_000, 100_000, 1_000_000]:
    tracemalloc.start()
    resultado = crear_lista_nueva(n)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"  crear_lista(N={n:>10,}): Memoria pico = {peak / 1024:.1f} KB")

print()
for n in [10_000, 100_000, 1_000_000]:
    datos = list(range(n))
    tracemalloc.start()
    sumar_in_place(datos)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"  sumar_in_place(N={n:>10,}): Memoria pico = {peak / 1024:.1f} KB")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 4: ANÁLISIS AMORTIZADO                                        ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 10: ANÁLISIS AMORTIZADO — POR QUÉ APPEND ES O(1) ===")
print("=" * 80)

"""
list.append() se dice O(1) AMORTIZADO. ¿Qué significa "amortizado"?

La mayoría de las veces, append es O(1): simplemente escribe en el 
slot libre del array interno. PERO de vez en cuando, el array se llena
y Python debe:
1. Pedir un bloque de memoria MÁS GRANDE al SO (malloc).
2. COPIAR todos los N punteros existentes al nuevo bloque.
3. Liberar el bloque viejo.

Este coste de copia es O(N). Pero ocurre cada vez MENOS frecuente:
- El array empieza con capacidad 4.
- Se expande a ~5 (factor ~1.125x + offset).
- Luego a ~9, ~16, ~25, ~35...

Si haces N appends, el coste TOTAL de todas las copias es ~3N.
Dividido entre N operaciones: 3N/N = O(1) amortizado.

Es como hipoteca de una casa: un solo pago sería intratable,
pero repartido en 30 años es manejable.
"""

print("\n--- Visualización del amortizado: appends con resize ---")

lista = []
tamanio_anterior = sys.getsizeof(lista)
resizes = 0

for i in range(100_000):
    lista.append(i)
    tamanio_actual = sys.getsizeof(lista)
    if tamanio_actual > tamanio_anterior:
        if resizes < 10:
            print(f"  Resize #{resizes}: al insertar [{i}], "
                  f"memoria {tamanio_anterior} -> {tamanio_actual} bytes "
                  f"(+{tamanio_actual - tamanio_anterior} bytes)")
        resizes += 1
        tamanio_anterior = tamanio_actual

print(f"  ... Total resizes para 100K appends: {resizes}")
print(f"  -> Solo {resizes} eventos O(N), el resto fueron O(1). Amortizado = O(1).")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 5: PERFILADO REAL DE CÓDIGO                                   ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 11: PERFILADO CON TIMEIT Y PERF_COUNTER ===")
print("=" * 80)

"""
El análisis teórico Big-O te dice la CLASE de complejidad.
Pero en producción necesitas MEDICIONES REALES.

Herramientas de perfilado de Python:
1. time.perf_counter(): reloj de alta resolución, ideal para benchmarks.
2. timeit: módulo de benchmarking que ejecuta N repeticiones.
3. tracemalloc: perfilado de memoria (ya visto).
4. cProfile: perfilado de CPU function-by-function.
5. memory_profiler: decorador @profile para línea por línea (pip install).
"""

print("\n--- perf_counter: la herramienta diaria del ingeniero ---")

def benchmark(func, *args, n_repeticiones: int = 5):
    """Ejecuta func n veces y reporta min/max/media."""
    tiempos = []
    for _ in range(n_repeticiones):
        inicio = time.perf_counter()
        func(*args)
        tiempos.append(time.perf_counter() - inicio)
    
    media = sum(tiempos) / len(tiempos)
    minimo = min(tiempos)
    maximo = max(tiempos)
    
    print(f"  {func.__name__:<30} media={media*1000:.2f}ms "
          f"min={minimo*1000:.2f}ms max={maximo*1000:.2f}ms")

# Comparar diferentes formas de sumar
datos_bench = list(range(500_000))

def sum_builtin(d): return sum(d)
def sum_loop(d):
    t = 0
    for x in d:
        t += x
    return t
def sum_comprehension(d): return sum(x for x in d)

benchmark(sum_builtin, datos_bench)
benchmark(sum_loop, datos_bench)
benchmark(sum_comprehension, datos_bench)
print("  -> sum() builtin es C puro. El loop Python es ~10x más lento.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: PERFILADO DE MEMORIA CON TRACEMALLOC ===")
print("=" * 80)

"""
tracemalloc ya lo usamos en módulos anteriores, pero aquí lo formalizamos
como herramienta de análisis de complejidad espacial.
"""

print("\n--- Comparando uso de RAM: lista vs generador ---")

# Lista: O(N) espacio
tracemalloc.start()
lista_grande = [x**2 for x in range(1_000_000)]
total_lista = sum(lista_grande)
mem_lista = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()
del lista_grande

# Generador: O(1) espacio
tracemalloc.start()
total_gen = sum(x**2 for x in range(1_000_000))
mem_gen = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()

print(f"  Lista (sum de list comprehension): pico = {mem_lista / 1024 / 1024:.1f} MB")
print(f"  Generador (sum de gen expr):       pico = {mem_gen / 1024:.1f} KB")
print(f"  Ahorro: {mem_lista / mem_gen:.0f}x menos memoria con generador")
print(f"  Resultados iguales: {total_lista == total_gen}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 6: BIG-O DE TODAS LAS ESTRUCTURAS DE PYTHON                  ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 13: TABLA DEFINITIVA BIG-O DE PYTHON ===")
print("=" * 80)

"""
╔═══════════════════════════════════════════════════════════════════════╗
║                           LIST                                       ║
╠═══════════════════════════════╦═══════════╦═══════════════════════════╣
║ list[i]                       ║ O(1)      ║ Acceso directo a array   ║
║ list.append(x)                ║ O(1)*     ║ *Amortizado              ║
║ list.pop()                    ║ O(1)      ║ Último elemento          ║
║ list.pop(i) / insert(i)      ║ O(N)      ║ Desplaza punteros        ║
║ x in list                     ║ O(N)      ║ Búsqueda lineal          ║
║ list.sort()                   ║ O(N log N)║ Timsort                  ║
║ list + list2                  ║ O(N+M)    ║ Crea nueva lista         ║
╠═══════════════════════════════╩═══════════╩═══════════════════════════╣
║                           DICT                                       ║
╠═══════════════════════════════╦═══════════╦═══════════════════════════╣
║ dict[key]                     ║ O(1)      ║ Hash table lookup        ║
║ dict[key] = value             ║ O(1)      ║ Hash table insert        ║
║ key in dict                   ║ O(1)      ║ Hash table lookup        ║
║ del dict[key]                 ║ O(1)      ║ Hash table delete        ║
║ dict.keys() / .values()       ║ O(1)      ║ Vista, no copia          ║
║ for k in dict                 ║ O(N)      ║ Recorre entries          ║
╠═══════════════════════════════╩═══════════╩═══════════════════════════╣
║                           SET                                        ║
╠═══════════════════════════════╦═══════════╦═══════════════════════════╣
║ x in set                      ║ O(1)      ║ Hash table lookup        ║
║ set.add(x)                    ║ O(1)      ║ Hash table insert        ║
║ set & set2 (intersección)     ║ O(min)    ║ Itera el menor           ║
║ set | set2 (unión)            ║ O(N+M)    ║ Copia ambos              ║
╠═══════════════════════════════╩═══════════╩═══════════════════════════╣
║                          DEQUE                                       ║
╠═══════════════════════════════╦═══════════╦═══════════════════════════╣
║ deque.append(x)               ║ O(1)      ║ Cola derecha             ║
║ deque.appendleft(x)           ║ O(1)      ║ Cola izquierda           ║
║ deque.popleft()               ║ O(1)      ║ Extrae izquierda         ║
║ deque[i]                      ║ O(N)      ║ Hay que recorrer bloques ║
╠═══════════════════════════════╩═══════════╩═══════════════════════════╣
║                         TUPLE                                        ║
╠═══════════════════════════════╦═══════════╦═══════════════════════════╣
║ tuple[i]                      ║ O(1)      ║ Acceso directo           ║
║ x in tuple                    ║ O(N)      ║ Búsqueda lineal          ║
║ hash(tuple)                   ║ O(N)      ║ Recorre elementos        ║
╚═══════════════════════════════╩═══════════╩═══════════════════════════╝
"""


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: EJERCICIO FINAL — OPTIMIZAR UN PIPELINE ML ===")
print("=" * 80)

"""
Ejercicio: Dado un pipeline de procesamiento de datos ineficiente, 
identifica los cuellos de botella y optimízalo.
"""

print("\n--- Pipeline ANTES de optimizar (O(N²)) ---")

def pipeline_ineficiente(corpus: list[str]) -> dict:
    """
    Cuenta la frecuencia de palabras en un corpus.
    TIENE UN BUG DE RENDIMIENTO OCULTO.
    """
    todas_las_palabras = []
    for documento in corpus:
        palabras = documento.lower().split()
        for palabra in palabras:
            todas_las_palabras.append(palabra)
    
    # BUG: esto es O(N²) porque "if p not in frecuencias" es O(N) en LISTA
    frecuencias = {}
    for palabra in todas_las_palabras:
        if palabra not in frecuencias:  # O(1) en dict, pero...
            frecuencias[palabra] = 0
        frecuencias[palabra] += 1
    
    # BUG 2: ordenar la salida como lista de tuplas, luego filtrar
    ordenadas = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    
    # BUG 3: reconstruir dict desde lista (innecesario)
    resultado = {}
    for palabra, conteo in ordenadas:
        resultado[palabra] = conteo
    
    return resultado


print("\n--- Pipeline OPTIMIZADO (O(N log N) por el sort final) ---")

from collections import Counter

def pipeline_optimizado(corpus: list[str]) -> dict:
    """
    Misma funcionalidad, rendimiento óptimo.
    """
    # Counter hace el conteo en una sola pasada O(N)
    frecuencias = Counter()
    for documento in corpus:
        frecuencias.update(documento.lower().split())
    
    # most_common() usa heapq internamente: O(N log K)
    return dict(frecuencias.most_common())


# Benchmark
corpus_test = [
    f"el modelo de inteligencia artificial número {i} procesa datos con python" 
    for i in range(50_000)
]

inicio = time.perf_counter()
r1 = pipeline_ineficiente(corpus_test)
t_inef = time.perf_counter() - inicio

inicio = time.perf_counter()
r2 = pipeline_optimizado(corpus_test)
t_opt = time.perf_counter() - inicio

print(f"  Ineficiente: {t_inef*1000:.2f} ms")
print(f"  Optimizado:  {t_opt*1000:.2f} ms")
print(f"  Speedup:     {t_inef/t_opt:.1f}x más rápido")
print(f"  Resultados iguales: {r1 == r2}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: BIG-Ω, BIG-Θ — LAS OTRAS NOTACIONES ===")
print("=" * 80)

"""
Big-O NO es la única notación asintótica. Hay tres:

1. Big-O (O): UPPER BOUND — "como máximo crece así".
   -> f(n) = O(g(n)) si f(n) ≤ c·g(n) para n grande.
   -> Es lo que usamos el 99% del tiempo.

2. Big-Ω (Omega): LOWER BOUND — "como mínimo crece así".
   -> f(n) = Ω(g(n)) si f(n) ≥ c·g(n) para n grande.
   -> Ejemplo: cualquier sort basado en comparaciones es Ω(N log N).
              No se puede hacer MEJOR que eso.

3. Big-Θ (Theta): TIGHT BOUND — "crece exactamente así".
   -> f(n) = Θ(g(n)) si f(n) = O(g(n)) Y f(n) = Ω(g(n)).
   -> Ejemplo: Merge Sort es Θ(N log N). Siempre. Ni mejor ni peor.

¿POR QUÉ ESTO IMPORTA EN IA?
Cuando un paper dice que su algoritmo de atención es O(N√N), 
te dice que EN EL PEOR CASO crece así. Pero podría ser más rápido
en la práctica (mejor caso). Si dice Θ(N√N), SIEMPRE crece así.

En entrevistas, la mayoría dice "Big-O" cuando realmente quiere decir
"Tight Bound". Si dices "Timsort es O(N log N)" estás siendo correcto
pero impreciso: su MEJOR caso es O(N), su PEOR caso es O(N log N),
y su tight bound (Θ) depende del caso.
"""

print("\n--- Mejor, Promedio y Peor caso: importa cuál analizas ---")

print("""
╔═══════════════════════╦══════════════╦══════════════╦═══════════════╗
║ ALGORITMO             ║ MEJOR CASO   ║ PROMEDIO     ║ PEOR CASO     ║
╠═══════════════════════╬══════════════╬══════════════╬═══════════════╣
║ Búsqueda lineal       ║ O(1)         ║ O(N)         ║ O(N)          ║
║ Búsqueda binaria      ║ O(1)         ║ O(log N)     ║ O(log N)      ║
║ Timsort               ║ O(N)         ║ O(N log N)   ║ O(N log N)    ║
║ Quick Sort             ║ O(N log N)   ║ O(N log N)   ║ O(N²)         ║
║ dict[key]              ║ O(1)         ║ O(1)         ║ O(N)*         ║
║ Inserción en BST       ║ O(log N)     ║ O(log N)     ║ O(N)          ║
╚═══════════════════════╩══════════════╩══════════════╩═══════════════╝

* O(N) en dict solo si TODAS las claves colisionan. Prácticamente imposible.
""")

print("""  NOTA SOBRE QUICK SORT VS TIMSORT:
  Python usa Timsort, NO Quick Sort. ¿Por qué?
  - Quick Sort tiene O(N²) en el peor caso (pivot malo, datos ya ordenados).
  - Timsort tiene O(N log N) en el peor caso SIEMPRE.
  - Timsort es O(N) en datos ya semi-ordenados (detecta "runs").
  - Timsort es ESTABLE (Quick Sort no).
  Por eso Python eligió Timsort: predecibilidad > velocidad teórica.""")


print("\n" + "=" * 80)
print("=== CAPÍTULO 16: CPROFILE — ENCONTRAR CUELLOS DE BOTELLA REALES ===")
print("=" * 80)

"""
cProfile es el profiler de CPU nativo de Python.
Mide cuántas veces se llama cada función y cuánto tiempo consume.
Es LA herramienta para encontrar el 20% de código que causa el 80%
del tiempo de ejecución (principio de Pareto).
"""

import cProfile
import io
import pstats

print("\n--- Perfilando un pipeline con cProfile ---")

def paso_tokenizar(textos):
    return [texto.lower().split() for texto in textos]

def paso_contar(tokens_lista):
    conteo = {}
    for tokens in tokens_lista:
        for token in tokens:
            conteo[token] = conteo.get(token, 0) + 1
    return conteo

def paso_filtrar(conteo, min_freq=2):
    return {k: v for k, v in conteo.items() if v >= min_freq}

def pipeline_completo(textos):
    tokens = paso_tokenizar(textos)
    conteo = paso_contar(tokens)
    filtrado = paso_filtrar(conteo)
    return filtrado

textos_test = [f"el modelo {i} es un modelo de inteligencia artificial {i}" for i in range(10_000)]

# Ejecutar con profiler
profiler = cProfile.Profile()
profiler.enable()
resultado_pipeline = pipeline_completo(textos_test)
profiler.disable()

# Formatear resultados
stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream).sort_stats('cumulative')
stats.print_stats(8)  # Top 8 funciones
print(stream.getvalue())


print("\n" + "=" * 80)
print("=== CAPÍTULO 17: ANTIPATRONES DE COMPLEJIDAD EN CÓDIGO ML ===")
print("=" * 80)

"""
Los 5 antipatrones de complejidad más comunes en código de IA:
"""

print("\n--- ANTIPATRÓN 1: 'x in list' dentro de un loop ---")
print("""
  # MAL: O(N²)
  for item in dataset:
      if item not in seen_list:  # O(N) por cada iteración
          seen_list.append(item)

  # BIEN: O(N)
  seen_set = set()
  for item in dataset:
      if item not in seen_set:  # O(1)
          seen_set.add(item)
""")

print("--- ANTIPATRÓN 2: list.insert(0, x) en un loop ---")
print("""
  # MAL: O(N²) — cada insert desplaza TODOS los elementos
  for i in range(n):
      lista.insert(0, i)

  # BIEN: O(N) — usar deque
  from collections import deque
  d = deque()
  for i in range(n):
      d.appendleft(i)  # O(1) cada uno
""")

print("--- ANTIPATRÓN 3: concatenar strings en loop ---")
print("""
  # MAL: O(N²) — cada += crea un string NUEVO
  resultado = ""
  for palabra in palabras:
      resultado += palabra + " "

  # BIEN: O(N) — join une todo de una vez
  resultado = " ".join(palabras)
""")

print("--- ANTIPATRÓN 4: nested loops para intersección ---")
print("""
  # MAL: O(N*M_) 
  comunes = []
  for a in lista_a:
      for b in lista_b:
          if a == b:
              comunes.append(a)

  # BIEN: O(N + M) — sets
  comunes = list(set(lista_a) & set(lista_b))
""")

print("--- ANTIPATRÓN 5: recalcular lo que puedes cachear ---")
print("""
  # MAL: O(2^N) — Fibonacci sin caché
  def fib(n):
      if n <= 1: return n
      return fib(n-1) + fib(n-2)

  # BIEN: O(N) — con lru_cache
  @lru_cache(maxsize=None)
  def fib(n):
      if n <= 1: return n
      return fib(n-1) + fib(n-2)
""")


print("\n" + "=" * 80)
print("=== CAPÍTULO 18: PREDICCIÓN DE ESCALABILIDAD ===")
print("=" * 80)

"""
Con Big-O puedes PREDECIR cuánto tardará tu código con datos reales
antes de ejecutarlo. Esto es lo que hace un ingeniero senior en 
la fase de diseño de un pipeline.
"""

print("\n--- Calculadora de escalabilidad ---")

import math

def predecir_tiempo(t_medido_ms: float, n_medido: int, n_objetivo: int, 
                    complejidad: str) -> float:
    """Predice el tiempo para n_objetivo basándose en una medición."""
    if complejidad == "O(1)":
        return t_medido_ms
    elif complejidad == "O(log N)":
        return t_medido_ms * math.log2(n_objetivo) / math.log2(n_medido)
    elif complejidad == "O(N)":
        return t_medido_ms * n_objetivo / n_medido
    elif complejidad == "O(N log N)":
        return t_medido_ms * (n_objetivo * math.log2(n_objetivo)) / (n_medido * math.log2(n_medido))
    elif complejidad == "O(N²)":
        return t_medido_ms * (n_objetivo / n_medido) ** 2
    else:
        return float('inf')

# Ejemplo: medimos 50ms para 10K items. ¿Cuánto tardará con 10M?
print(f"  Si un O(N) tarda 50ms con 10K items:")
print(f"    Con 1M items:  {predecir_tiempo(50, 10_000, 1_000_000, 'O(N)'):.0f} ms = {predecir_tiempo(50, 10_000, 1_000_000, 'O(N)')/1000:.1f} s")
print(f"    Con 10M items: {predecir_tiempo(50, 10_000, 10_000_000, 'O(N)'):.0f} ms = {predecir_tiempo(50, 10_000, 10_000_000, 'O(N)')/1000:.0f} s")

print(f"\n  Si un O(N²) tarda 50ms con 10K items:")
t_1m = predecir_tiempo(50, 10_000, 1_000_000, "O(N²)")
t_10m = predecir_tiempo(50, 10_000, 10_000_000, "O(N²)")
print(f"    Con 1M items:  {t_1m:.0f} ms = {t_1m/1000/3600:.0f} HORAS")
print(f"    Con 10M items: {t_10m:.0f} ms = {t_10m/1000/3600/24:.0f} DÍAS")
print(f"  -> Un O(N²) que 'funciona bien' en desarrollo MATA en producción.")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN ARQUITECTÓNICA ===")
print("=" * 80)

"""
RESUMEN DEFINITIVO DE BIG-O PARA INGENIERÍA IA:

1. Big-O mide ESCALABILIDAD, no velocidad absoluta.
   Un O(N) lento puede ser mejor que un O(N²) rápido si N crece.

2. Las 7 complejidades: O(1) < O(log N) < O(N) < O(N log N) < O(N²) < O(2^N) < O(N!).

3. Reglas: constantes se ignoran, término dominante gana, loops anidados multiplican.

4. Complejidad ESPACIAL importa tanto como temporal en IA:
   la RAM es finita y los tensores son enormes.

5. Amortizado: list.append es O(1) amortizado gracias a la sobre-asignación.

6. La optimización #1: cambiar una estructura de datos.
   "x in list" (O(N)) -> "x in set" (O(1)). Eso cambiado salva pipelines.

7. Perfilar antes de optimizar: perf_counter para tiempo, tracemalloc para memoria.

8. Los generadores (O(1) espacio) eliminan la necesidad de materializar 
   listas intermedias, ahorrando GB de RAM en pipelines de datos.

9. Big-Omega, Big-Theta: la notación completa para mejor/peor/tight bound.

10. cProfile: identifica el 20% de código que causa el 80% del tiempo.

11. Predicción de escalabilidad: con Big-O predices el comportamiento 
    en producción ANTES de desplegar.

Siguiente archivo: Búsquedas y el módulo bisect.
"""

print("\n FIN DE ARCHIVO 01_notacion_big_o_y_analisis_memoria.")
print(" La base algorítmica está construida. Siguiente: búsquedas y bisect.")

