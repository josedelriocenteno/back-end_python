# ===========================================================================
# 03_sorting_y_timsort.py
# ===========================================================================
# MÓDULO 03: ALGORITMIA Y COMPLEJIDAD COMPUTACIONAL
# ARCHIVO 03: Algoritmos de Ordenación, Timsort bajo el Capó y Sorted Patterns
# ===========================================================================
#
# OBJETIVO (1000+ LÍNEAS):
# Entender por qué Python eligió Timsort, cómo funciona internamente,
# y dominar sorted()/list.sort() con keys avanzados, estabilidad,
# y patrones de ordenación que aparecen constantemente en pipelines ML.
#
# CONTENIDO:
#   1. Fundamentos: por qué ordenar es O(N log N) mínimo.
#   2. Algoritmos clásicos comparados: Bubble, Selection, Insertion, 
#      Merge Sort, Quick Sort.
#   3. Timsort bajo el capó: runs, galloping, merge.
#   4. sorted() vs list.sort(): cuándo usar cada uno.
#   5. Key functions avanzadas: lambda, operator, attrgetter.
#   6. Ordenación multi-criterio (estabilidad de Timsort).
#   7. Aplicaciones ML: ranking de predicciones, Top-K, argsort.
#   8. Ejercicio: sistema de leaderboard para experimentos ML.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import time
import random
import sys
import operator
from typing import NamedTuple
from collections import defaultdict


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 1: FUNDAMENTOS DE ORDENACIÓN                                  ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: ¿POR QUÉ O(N LOG N) ES EL LÍMITE? ===")
print("=" * 80)

"""
TEOREMA FUNDAMENTAL: Ningún algoritmo de ordenación basado en 
COMPARACIONES puede ser más rápido que O(N log N) en el peor caso.

DEMOSTRACIÓN INTUITIVA:
- N elementos tienen N! posibles permutaciones.
- Cada comparación divide las posibilidades en 2.
- Necesitas al menos log₂(N!) comparaciones.
- Por la aproximación de Stirling: log₂(N!) ≈ N log₂ N.

EXCEPCIONES (algoritmos NO basados en comparaciones):
- Counting Sort: O(N + K) donde K = rango de valores. Requiere enteros.
- Radix Sort: O(d·N) donde d = número de dígitos. Requiere tipos discretos.
- Bucket Sort: O(N) promedio. Requiere distribución uniforme.

Python usa TIMSORT (basado en comparaciones, O(N log N) peor caso).
¿Por qué no usa Counting/Radix? Porque Python debe ordenar CUALQUIER tipo
(strings, objetos, floats), no solo enteros.
"""

print("\n--- La jerarquía de rendimiento de sorts ---")
print("""
╔═══════════════════════╦══════════════╦══════════════╦═══════════════╗
║ ALGORITMO             ║ MEJOR        ║ PROMEDIO     ║ PEOR          ║
╠═══════════════════════╬══════════════╬══════════════╬═══════════════╣
║ Bubble Sort           ║ O(N)         ║ O(N²)        ║ O(N²)         ║
║ Selection Sort        ║ O(N²)        ║ O(N²)        ║ O(N²)         ║
║ Insertion Sort        ║ O(N)         ║ O(N²)        ║ O(N²)         ║
║ Merge Sort            ║ O(N log N)   ║ O(N log N)   ║ O(N log N)    ║
║ Quick Sort            ║ O(N log N)   ║ O(N log N)   ║ O(N²)         ║
║ Heap Sort             ║ O(N log N)   ║ O(N log N)   ║ O(N log N)    ║
║ Timsort (Python)      ║ O(N)         ║ O(N log N)   ║ O(N log N)    ║
╚═══════════════════════╩══════════════╩══════════════╩═══════════════╝

TIMSORT DESTACA: O(N) en el MEJOR caso (datos ya casi ordenados).
Todos los demás O(N log N) son O(N log N) siempre.
""")


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: ALGORITMOS O(N²) — POR QUÉ SON MALOS ===")
print("=" * 80)

"""
Los mostramos para entender POR QUÉ Timsort es mejor.
Nunca los uses en producción.
"""

print("\n--- Bubble Sort: el más ineficiente ---")

def bubble_sort(lista: list) -> list:
    """
    O(N²): compara pares adyacentes y los intercambia.
    Ineficiente pero útil para entender la base.
    """
    arr = lista.copy()
    n = len(arr)
    for i in range(n):
        intercambio = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambio = True
        if not intercambio:  # Optimización: si no hubo intercambios, ya está ordenado
            break
    return arr

print(f"Bubble Sort: {bubble_sort([5, 3, 8, 1, 9, 2])}")


print("\n--- Insertion Sort: bueno para datos casi ordenados ---")

def insertion_sort(lista: list) -> list:
    """
    O(N²) peor caso, PERO O(N) si los datos ya están casi ordenados.
    Timsort lo usa internamente para ordenar "runs" pequeños.
    """
    arr = lista.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

print(f"Insertion Sort: {insertion_sort([5, 3, 8, 1, 9, 2])}")


print("\n--- Benchmark: O(N²) vs sorted() ---")

for n in [1_000, 5_000, 10_000]:
    datos = [random.random() for _ in range(n)]
    
    inicio = time.perf_counter()
    insertion_sort(datos)
    t_insertion = time.perf_counter() - inicio
    
    inicio = time.perf_counter()
    sorted(datos)
    t_sorted = time.perf_counter() - inicio
    
    print(f"  N={n:>6}: Insertion={t_insertion*1000:>8.2f}ms  "
          f"sorted()={t_sorted*1000:>6.2f}ms  "
          f"Ratio: {t_insertion/t_sorted:.0f}x")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 2: MERGE SORT — LA BASE DE TIMSORT                            ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 3: MERGE SORT — DIVIDE AND CONQUER ===")
print("=" * 80)

"""
Merge Sort es el ANCESTRO de Timsort. Entender Merge Sort es 
REQUISITO para entender Timsort.

ALGORITMO (divide and conquer):
1. DIVIDE: Parte la lista por la mitad recursivamente.
2. CONQUISTA: Cuando cada sub-lista tiene 1 elemento, está "ordenada".
3. COMBINA: Fusiona (merge) las sub-listas ordenadas.

Complejidad:
- Tiempo: O(N log N) siempre (no tiene peor caso malo).
- Espacio: O(N) (necesita arrays temporales para el merge).
- Estable: SÍ (elementos iguales mantienen su orden relativo).
"""

print("\n--- Merge Sort implementado ---")

def merge_sort(lista: list) -> list:
    """
    Merge Sort recursivo. O(N log N) tiempo, O(N) espacio.
    """
    if len(lista) <= 1:
        return lista
    
    # DIVIDE
    mid = len(lista) // 2
    izquierda = merge_sort(lista[:mid])
    derecha = merge_sort(lista[mid:])
    
    # COMBINA (merge)
    return _merge(izquierda, derecha)

def _merge(a: list, b: list) -> list:
    """Fusiona dos listas ordenadas."""
    resultado = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:  # <= para ESTABILIDAD
            resultado.append(a[i])
            i += 1
        else:
            resultado.append(b[j])
            j += 1
    resultado.extend(a[i:])
    resultado.extend(b[j:])
    return resultado

datos_test = [38, 27, 43, 3, 9, 82, 10]
print(f"Original: {datos_test}")
print(f"Merge Sort: {merge_sort(datos_test)}")

# Verificar estabilidad
# Si dos elementos son "iguales" según la comparación, mantienen su orden original
datos_estabilidad = [(3, 'a'), (1, 'b'), (3, 'c'), (1, 'd')]
sorted_estable = sorted(datos_estabilidad, key=lambda x: x[0])
print(f"\nEstabilidad: {datos_estabilidad}")
print(f"Sorted:      {sorted_estable}")
print(f"Los dos 3s mantienen orden (a antes de c): ✓")
print(f"Los dos 1s mantienen orden (b antes de d): ✓")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 3: TIMSORT — EL ALGORITMO DE PYTHON                           ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 4: TIMSORT — CÓMO FUNCIONA INTERNAMENTE ===")
print("=" * 80)

"""
Timsort fue inventado por Tim Peters en 2002 para Python.
Hoy lo usan también Java, Swift, Android y Rust.

ES UN HÍBRIDO: Merge Sort + Insertion Sort.

PASO 1: DETECTAR "RUNS" (secuencias ya ordenadas)
- Timsort recorre la lista buscando sub-secuencias que ya están
  ordenadas (ascendente o descendente). Las descendentes las invierte.
- Si un run es demasiado corto (< minrun ≈ 32-64), lo extiende
  usando Insertion Sort (que es O(N) para datos casi ordenados).

PASO 2: APILAR LOS RUNS
- Los runs detectados se apilan en un stack.
- Se mantiene un INVARIANTE del stack que garantiza que los merges
  serán eficientes (similar a la secuencia de Fibonacci).

PASO 3: MERGE CON GALLOPING
- Cuando dos runs se fusionan, Timsort usa "galloping mode":
  si muchos elementos consecutivos vienen del mismo run, 
  usa búsqueda binaria para saltar bloques enteros en vez de
  comparar uno a uno.

¿POR QUÉ ES GENIAL?
- Datos ya ordenados: solo un run → O(N).
- Datos parcialmente ordenados: pocos runs → cercano a O(N).
- Datos aleatorios: muchos runs → O(N log N) estándar.
- NUNCA peor que O(N log N). SIEMPRE estable.
"""

print("\n--- Demostración: Timsort es O(N) en datos ya ordenados ---")

for n in [100_000, 500_000, 1_000_000, 5_000_000]:
    # Datos ya ordenados
    ordenados = list(range(n))
    inicio = time.perf_counter()
    sorted(ordenados)
    t_ord = time.perf_counter() - inicio
    
    # Datos aleatorios
    aleatorios = [random.random() for _ in range(n)]
    inicio = time.perf_counter()
    sorted(aleatorios)
    t_alea = time.perf_counter() - inicio
    
    ratio = t_alea / t_ord if t_ord > 0 else float('inf')
    print(f"  N={n:>10,}: ya_ordenados={t_ord*1000:>6.1f}ms  "
          f"aleatorios={t_alea*1000:>8.1f}ms  ratio={ratio:>5.1f}x")

print("  -> Datos ya ordenados son DRAMÁTICAMENTE más rápidos. Eso es Timsort.")


print("\n--- Timsort: 'casi ordenados' también es rápido ---")

def desordenar_parcialmente(lista: list, porcentaje: float) -> list:
    """Desordena un porcentaje de los elementos."""
    resultado = lista.copy()
    n_swap = int(len(resultado) * porcentaje / 100)
    for _ in range(n_swap):
        i = random.randint(0, len(resultado) - 1)
        j = random.randint(0, len(resultado) - 1)
        resultado[i], resultado[j] = resultado[j], resultado[i]
    return resultado

n = 1_000_000
base = list(range(n))

for pct in [0, 1, 5, 10, 50, 100]:
    datos = desordenar_parcialmente(base, pct)
    inicio = time.perf_counter()
    sorted(datos)
    t = time.perf_counter() - inicio
    print(f"  {pct:>3}% desordenado: {t*1000:.1f} ms")

print("  -> Timsort escala suavemente con el grado de desorden.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: SORTED() VS LIST.SORT() ===")
print("=" * 80)

"""
Python tiene DOS formas de ordenar:

1. sorted(iterable, key=, reverse=): 
   - Crea una NUEVA lista ordenada.
   - Funciona con CUALQUIER iterable (tuple, set, dict, generator...).
   - No modifica el original.
   - O(N) espacio extra.

2. list.sort(key=, reverse=):
   - Ordena la lista IN-PLACE (modifica el original).
   - SOLO funciona con listas.
   - Retorna None (no la lista).
   - O(1) espacio extra (Timsort usa algo de espacio temporal).
   
REGLA DE ORO:
- Necesitas preservar el original → sorted()
- Solo necesitas ordenar sin preservar → list.sort() (más eficiente)
"""

print("\n--- sorted() vs .sort() ---")

datos_original = [5, 3, 8, 1, 9, 2]

# sorted(): no modifica el original
nuevo = sorted(datos_original)
print(f"Original tras sorted(): {datos_original}")  # No cambia
print(f"Nuevo: {nuevo}")

# .sort(): modifica in-place
datos_copia = datos_original.copy()
resultado = datos_copia.sort()
print(f"\nOriginal tras .sort(): {datos_copia}")  # Cambiado
print(f"Retorno de .sort(): {resultado}")  # None!


print("\n--- sorted() con cualquier iterable ---")

# Funciona con tuplas, sets, dicts, generators...
print(f"sorted(tuple): {sorted((5, 3, 1, 4, 2))}")
print(f"sorted(set):   {sorted({5, 3, 1, 4, 2})}")
print(f"sorted(dict):  {sorted({'b': 2, 'a': 1, 'c': 3})}")  # Ordena las CLAVES
print(f"sorted(str):   {sorted('python')}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 4: KEY FUNCTIONS AVANZADAS                                    ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 6: KEY FUNCTIONS — EL PODER DE LA PERSONALIZACIÓN ===")
print("=" * 80)

"""
El parámetro key= acepta una función que se aplica a cada elemento
ANTES de comparar. Esto permite ordenar por CUALQUIER criterio.

Opciones:
1. lambda: para funciones simples inline.
2. operator.itemgetter: para indexar dicts/tuplas (más rápido que lambda).
3. operator.attrgetter: para acceder a atributos de objetos.
4. Función nombrada: para lógica compleja.
"""

print("\n--- Lambda: ordenar predicciones por score ---")

predicciones = [
    {"modelo": "BERT", "acc": 0.92, "loss": 0.15},
    {"modelo": "GPT-2", "acc": 0.89, "loss": 0.22},
    {"modelo": "T5", "acc": 0.95, "loss": 0.08},
    {"modelo": "RoBERTa", "acc": 0.93, "loss": 0.12},
]

# Ordenar por accuracy (descendente)
por_acc = sorted(predicciones, key=lambda p: p["acc"], reverse=True)
print("Por accuracy (desc):")
for p in por_acc:
    print(f"  {p['modelo']:<10} acc={p['acc']:.2f}")


print("\n--- operator.itemgetter: más rápido que lambda ---")

from operator import itemgetter, attrgetter

# itemgetter crea una función callable que extrae items por key/índice
por_loss = sorted(predicciones, key=itemgetter("loss"))
print("\nPor loss (asc):")
for p in por_loss:
    print(f"  {p['modelo']:<10} loss={p['loss']:.2f}")

# itemgetter con múltiples keys (ordenación multi-criterio)
datos_multi = [
    ("Alice", 90, 85),
    ("Bob", 85, 90),
    ("Charlie", 90, 90),
    ("Diana", 85, 85),
]

# Ordenar por nota1 descendente, luego nota2 descendente
por_notas = sorted(datos_multi, key=itemgetter(1, 2), reverse=True)
print(f"\nMulti-criterio: {por_notas}")


print("\n--- attrgetter: para objetos ---")

class Experimento(NamedTuple):
    nombre: str
    accuracy: float
    epochs: int
    lr: float

experimentos = [
    Experimento("exp_01", 0.92, 10, 0.001),
    Experimento("exp_02", 0.95, 20, 0.0005),
    Experimento("exp_03", 0.88, 5, 0.01),
    Experimento("exp_04", 0.95, 15, 0.001),
]

por_acc = sorted(experimentos, key=attrgetter("accuracy"), reverse=True)
print("\nExperimentos por accuracy:")
for e in por_acc:
    print(f"  {e.nombre}: acc={e.accuracy}, epochs={e.epochs}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 7: ORDENACIÓN MULTI-CRITERIO CON ESTABILIDAD ===")
print("=" * 80)

"""
La ESTABILIDAD de Timsort permite ordenar por múltiples criterios:
ordena primero por el criterio SECUNDARIO, luego por el PRIMARIO.
Como el sort es estable, el orden del secundario se preserva.

Alternativa: devolver una TUPLA desde la key function.
Timsort compara tuplas lexicográficamente.
"""

print("\n--- Multi-criterio con tupla como key ---")

# Ordenar: accuracy desc, luego lr asc (empate en accuracy → menor lr primero)
ranking = sorted(
    experimentos,
    key=lambda e: (-e.accuracy, e.lr)  # Negativo = descendente
)
print("Ranking (accuracy desc, lr asc):")
for e in ranking:
    print(f"  {e.nombre}: acc={e.accuracy}, lr={e.lr}")


print("\n--- Multi-criterio por sorts sucesivos (estabilidad) ---")

datos_empleados = [
    ("Alice", "Engineering", 90_000),
    ("Bob", "Marketing", 80_000),
    ("Charlie", "Engineering", 85_000),
    ("Diana", "Marketing", 90_000),
    ("Eve", "Engineering", 90_000),
]

# Paso 1: ordenar por salario (secundario)
paso_1 = sorted(datos_empleados, key=lambda e: e[2], reverse=True)

# Paso 2: ordenar por departamento (primario) — la estabilidad preserva el salario
paso_2 = sorted(paso_1, key=lambda e: e[1])

print("\nOrdenado por departamento, luego salario:")
for e in paso_2:
    print(f"  {e[0]:<10} {e[1]:<15} ${e[2]:,}")

# Es equivalente a una sola tupla-key
equiv = sorted(datos_empleados, key=lambda e: (e[1], -e[2]))
print(f"\nEquivalente (tupla-key): {equiv == paso_2}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 5: PATRONES DE ORDENACIÓN EN ML                               ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 8: ARGSORT — OBTENER LOS ÍNDICES DE ORDENACIÓN ===")
print("=" * 80)

"""
argsort retorna los ÍNDICES que ordenarían la lista, sin modificarla.
Es fundamental en NumPy (np.argsort) y en ranking de predicciones.
"""

print("\n--- argsort manual (sin NumPy) ---")

def argsort(lista: list, reverse: bool = False) -> list:
    """
    Retorna los índices que ordenarían la lista.
    Equivalente a numpy.argsort() pero en Python puro.
    """
    return [i for i, _ in sorted(enumerate(lista), 
                                  key=lambda x: x[1], 
                                  reverse=reverse)]

scores = [0.72, 0.95, 0.88, 0.91, 0.85]
indices_orden = argsort(scores, reverse=True)

print(f"Scores: {scores}")
print(f"Argsort (desc): {indices_orden}")
print(f"Ranking:")
for rank, idx in enumerate(indices_orden, 1):
    print(f"  #{rank}: posición {idx} -> score {scores[idx]}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 9: TOP-K SIN ORDENAR TODO ===")
print("=" * 80)

"""
Si solo necesitas los K mejores de N elementos, NO necesitas
ordenar todo (O(N log N)). Alternativas:

1. sorted()[:K]: O(N log N) — simple pero ordena todo.
2. heapq.nlargest(K, ...): O(N log K) — MEJOR cuando K << N.
3. Partition-based: O(N) promedio — quickselect.

heapq.nlargest es la herramienta correcta para Top-K en producción.
"""

import heapq

print("\n--- Top-K: sorted vs heapq.nlargest ---")

random.seed(42)
datos_grandes = [random.random() for _ in range(1_000_000)]
k = 10

# Método 1: sorted[:K]
inicio = time.perf_counter()
top_sorted = sorted(datos_grandes, reverse=True)[:k]
t_sorted = time.perf_counter() - inicio

# Método 2: heapq.nlargest
inicio = time.perf_counter()
top_heap = heapq.nlargest(k, datos_grandes)
t_heap = time.perf_counter() - inicio

print(f"  sorted()[:10]:       {t_sorted*1000:.2f} ms")
print(f"  heapq.nlargest(10):  {t_heap*1000:.2f} ms")
print(f"  Speedup: {t_sorted/t_heap:.1f}x")
print(f"  Resultados iguales: {top_sorted == top_heap}")


print("\n--- Top-K con key (predicciones de modelo) ---")

resultados_modelo = [
    {"id": i, "score": random.random(), "label": random.choice(["cat", "dog", "bird"])}
    for i in range(100_000)
]

top_10 = heapq.nlargest(10, resultados_modelo, key=lambda r: r["score"])
print(f"\nTop 10 predicciones:")
for r in top_10:
    print(f"  id={r['id']:>5} label={r['label']:<5} score={r['score']:.4f}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: COUNTING SORT — O(N) PARA ENTEROS ACOTADOS ===")
print("=" * 80)

"""
Counting Sort NO compara elementos. Cuenta cuántas veces aparece
cada valor y reconstruye la lista ordenada desde los conteos.

Complejidad: O(N + K) donde K = max_valor - min_valor.
Si K es pequeño (ej: notas 0-100, labels 0-9), es MÁS RÁPIDO que Timsort.

En ML: ordenar labels, categorías codificadas, cuantiles discretos.
"""

print("\n--- Counting Sort implementado ---")

def counting_sort(lista: list) -> list:
    """O(N + K) donde K = max - min."""
    if not lista:
        return []
    
    min_val = min(lista)
    max_val = max(lista)
    rango = max_val - min_val + 1
    
    # Conteo
    conteos = [0] * rango
    for x in lista:
        conteos[x - min_val] += 1
    
    # Reconstruir
    resultado = []
    for i, conteo in enumerate(conteos):
        resultado.extend([i + min_val] * conteo)
    
    return resultado

datos_labels = [random.randint(0, 9) for _ in range(100)]
print(f"Counting Sort (labels 0-9): {counting_sort(datos_labels)[:20]}...")


print("\n--- Benchmark: Counting Sort vs sorted() para enteros acotados ---")

for n in [100_000, 500_000, 1_000_000]:
    datos_ints = [random.randint(0, 100) for _ in range(n)]
    
    inicio = time.perf_counter()
    counting_sort(datos_ints)
    t_count = time.perf_counter() - inicio
    
    inicio = time.perf_counter()
    sorted(datos_ints)
    t_sorted = time.perf_counter() - inicio
    
    print(f"  N={n:>10,}: Counting={t_count*1000:>6.1f}ms  "
          f"sorted()={t_sorted*1000:>6.1f}ms  "
          f"Ratio: {t_sorted/t_count:.1f}x")


print("\n" + "=" * 80)
print("=== CAPÍTULO 11: REVERSE Y CLAVE NEGATIVA ===")
print("=" * 80)

"""
Para ordenar en orden DESCENDENTE:
1. reverse=True: la forma correcta y rápida.
2. -valor en la key: funciona para numéricos (no strings).
3. NO usar sorted()[::-1]: ordena asc y luego invierte (doble trabajo).
"""

print("\n--- Las formas de ordenar descendente ---")

nums = [3, 1, 4, 1, 5, 9, 2, 6]

# BIEN: reverse=True
r1 = sorted(nums, reverse=True)

# BIEN para numéricos: negativo en key
r2 = sorted(nums, key=lambda x: -x)

# MAL: reversed después de sort (funciona pero es ineficiente conceptualmente)
r3 = sorted(nums)[::-1]

print(f"reverse=True:  {r1}")
print(f"key=negative:  {r2}")
print(f"sorted()[::-1]: {r3}")
print(f"Todos iguales: {r1 == r2 == r3}")

# Para strings descendentes: no puedes negar, usa reverse=True
palabras = ["python", "ai", "ml", "deep", "learning"]
por_largo_desc = sorted(palabras, key=lambda w: -len(w))
print(f"\nPalabras por largo desc: {por_largo_desc}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: EJERCICIO INTEGRADOR — LEADERBOARD ML ===")
print("=" * 80)

"""
Construir un leaderboard para tracking de experimentos ML.
- Ordenar por métrica principal (accuracy) descendente.
- Desempatar por métrica secundaria (loss) ascendente.
- Soportar filtrado por modelo y epoch range.
"""

print("\n--- Sistema de Leaderboard ---")

class MLLeaderboard:
    """Leaderboard para experimentos de Machine Learning."""
    
    def __init__(self):
        self.experimentos = []
    
    def registrar(self, nombre: str, modelo: str, accuracy: float, 
                  loss: float, epochs: int, lr: float):
        self.experimentos.append({
            "nombre": nombre,
            "modelo": modelo,
            "accuracy": accuracy,
            "loss": loss,
            "epochs": epochs,
            "lr": lr,
        })
    
    def ranking(self, top_k: int = 10, modelo: str = None) -> list:
        """Retorna top_k experimentos, opcionalmente filtrados por modelo."""
        datos = self.experimentos
        if modelo:
            datos = [e for e in datos if e["modelo"] == modelo]
        
        return sorted(
            datos,
            key=lambda e: (-e["accuracy"], e["loss"])
        )[:top_k]
    
    def stats_por_modelo(self) -> dict:
        """Estadísticas agregadas por modelo."""
        por_modelo = defaultdict(list)
        for e in self.experimentos:
            por_modelo[e["modelo"]].append(e["accuracy"])
        
        stats = {}
        for modelo, accs in por_modelo.items():
            accs_sorted = sorted(accs)
            stats[modelo] = {
                "n": len(accs),
                "media": sum(accs) / len(accs),
                "mejor": max(accs),
                "peor": min(accs),
                "mediana": accs_sorted[len(accs_sorted) // 2],
            }
        return stats
    
    def mostrar_ranking(self, top_k: int = 10, modelo: str = None):
        ranking_list = self.ranking(top_k, modelo)
        titulo = f"Top {top_k}" + (f" ({modelo})" if modelo else " (global)")
        print(f"\n  {titulo}:")
        print(f"  {'#':<3} {'Nombre':<12} {'Modelo':<8} {'Acc':>6} {'Loss':>6} {'Epochs':>6} {'LR':>8}")
        print(f"  {'-'*55}")
        for i, e in enumerate(ranking_list, 1):
            print(f"  {i:<3} {e['nombre']:<12} {e['modelo']:<8} "
                  f"{e['accuracy']:>6.4f} {e['loss']:>6.4f} {e['epochs']:>6} {e['lr']:>8.5f}")

# Generar experimentos simulados
random.seed(42)
lb = MLLeaderboard()

for i in range(100):
    modelo = random.choice(["BERT", "GPT-2", "T5", "RoBERTa"])
    lr = random.choice([0.001, 0.0005, 0.0001, 0.00005])
    epochs = random.randint(5, 50)
    # Accuracy correlacionada con modelo y lr
    base_acc = {"BERT": 0.88, "GPT-2": 0.85, "T5": 0.90, "RoBERTa": 0.89}
    acc = min(0.99, base_acc[modelo] + random.gauss(0, 0.04))
    loss = max(0.01, 1.0 - acc + random.gauss(0, 0.03))
    
    lb.registrar(f"exp_{i:03d}", modelo, round(acc, 4), round(loss, 4), epochs, lr)

lb.mostrar_ranking(top_k=10)
lb.mostrar_ranking(top_k=5, modelo="T5")

# Estadísticas por modelo
print("\n  Estadísticas por modelo:")
for modelo, stats in sorted(lb.stats_por_modelo().items()):
    print(f"  {modelo:<10}: n={stats['n']:>3} media={stats['media']:.4f} "
          f"mejor={stats['mejor']:.4f} peor={stats['peor']:.4f}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: QUICK SORT — EL RIVAL DE TIMSORT ===")
print("=" * 80)

"""
Quick Sort es el algoritmo más usado en otros lenguajes (C stdlib).
Python NO lo usa porque tiene O(N²) en el peor caso.
Pero vale la pena entenderlo para entrevistas y para comparar.

ALGORITMO:
1. Elige un PIVOT (generalmente el último o uno aleatorio).
2. PARTITION: pone todos los menores a la izquierda del pivot
   y todos los mayores a la derecha.
3. Recursivamente ordena las dos mitades.

Complejidad:
- Mejor/Promedio: O(N log N)
- Peor: O(N²) (cuando el pivot es siempre el mínimo o máximo)
- Espacio: O(log N) para el stack de recursión
- NO es estable
"""

print("\n--- Quick Sort implementado ---")

def quick_sort(lista: list) -> list:
    """Quick Sort recursivo. O(N log N) promedio, O(N²) peor caso."""
    if len(lista) <= 1:
        return lista
    
    pivot = lista[-1]
    menores = [x for x in lista[:-1] if x <= pivot]
    mayores = [x for x in lista[:-1] if x > pivot]
    
    return quick_sort(menores) + [pivot] + quick_sort(mayores)

print(f"Quick Sort: {quick_sort([38, 27, 43, 3, 9, 82, 10])}")

# El peor caso de Quick Sort: datos ya ordenados con pivot = último
print("\n--- Peor caso de Quick Sort (por eso Python usa Timsort) ---")

# Con N > 1000, Quick Sort recursivo haría stack overflow en Python
# por la profundidad de recursión O(N)
print("""
  Quick Sort con datos [1, 2, 3, ..., N] y pivot = último:
  - Pivot = N, menores = [1..N-1], mayores = []
  - Pivot = N-1, menores = [1..N-2], mayores = []
  - ...
  - Esto da N niveles de recursión, cada uno O(N)
  - Total: O(N²) con stack O(N)
  
  Timsort con [1, 2, 3, ..., N]:  
  - Detecta UN solo run ascendente.
  - Total: O(N). Sin recursión.
  -> Timsort es ESTRICTAMENTE SUPERIOR para Python.
""")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: FUNCTOOLS.CMP_TO_KEY — COMPARADORES CUSTOM ===")
print("=" * 80)

"""
Antes de Python 3, sorted() aceptaba un parámetro cmp= para 
comparar dos elementos. Python 3 lo eliminó en favor de key=.

PERO a veces necesitas lógica de comparación compleja que no se 
puede expresar como una función key simple. Para eso existe
functools.cmp_to_key().

Un comparador retorna:
- Negativo si a < b
- 0 si a == b  
- Positivo si a > b
"""

from functools import cmp_to_key

print("\n--- Ordenación con comparador custom ---")

def comparar_versiones(v1: str, v2: str) -> int:
    """
    Compara versiones semánticas: '1.2.3' vs '1.10.1'.
    No puedes ordenar strings directamente porque '10' < '2' como string.
    """
    partes1 = list(map(int, v1.split('.')))
    partes2 = list(map(int, v2.split('.')))
    
    for p1, p2 in zip(partes1, partes2):
        if p1 < p2:
            return -1
        if p1 > p2:
            return 1
    
    return len(partes1) - len(partes2)

versiones = ["1.2.3", "1.10.1", "1.2.10", "2.0.0", "1.1.0", "1.2.1"]

# SIN cmp_to_key (string sort, INCORRECTO):
por_string = sorted(versiones)
print(f"String sort (INCORRECTO): {por_string}")

# CON cmp_to_key (semántico, CORRECTO):
por_version = sorted(versiones, key=cmp_to_key(comparar_versiones))
print(f"Semántico (CORRECTO):     {por_version}")


print("\n--- Natural sort para nombres de archivo ---")

import re

def natural_sort_key(s: str):
    """
    Key function para 'natural sort': 
    'file2' < 'file10' (no 'file10' < 'file2').
    Separa números de texto y compara números como enteros.
    """
    return [int(c) if c.isdigit() else c.lower() 
            for c in re.split(r'(\d+)', s)]

archivos = [
    "model_1.pt", "model_10.pt", "model_2.pt", 
    "model_20.pt", "model_3.pt", "model_100.pt"
]

print(f"Sort normal:  {sorted(archivos)}")
print(f"Natural sort: {sorted(archivos, key=natural_sort_key)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: PARTIAL SORT Y NTH ELEMENT ===")
print("=" * 80)

"""
A veces no necesitas la lista COMPLETAMENTE ordenada:
- Solo los K mejores (Top-K) -> heapq.nlargest
- Solo el K-ésimo elemento (mediana, percentil) -> nth element
- Solo separar "los buenos" de "los malos" -> partition

Python stdlib no tiene un quickselect nativo, 
pero podemos construir uno.
"""

print("\n--- K-ésimo elemento más grande (quickselect simplificado) ---")

def kth_largest(lista: list, k: int) -> float:
    """
    Encuentra el K-ésimo elemento más grande.
    Promedio O(N), peor caso O(N²).
    Usa heapq para la versión production-ready.
    """
    # Versión simple con heapq
    return heapq.nlargest(k, lista)[-1]

random.seed(42)
datos_kth = [random.random() for _ in range(100_000)]

# Mediana (k = N/2)
mediana = kth_largest(datos_kth, len(datos_kth) // 2)
mediana_sorted = sorted(datos_kth)[len(datos_kth) // 2]
print(f"Mediana via kth_largest: {mediana:.6f}")
print(f"Mediana via sorted:     {mediana_sorted:.6f}")
print(f"¿Iguales? {abs(mediana - mediana_sorted) < 1e-10}")


print("\n--- Partition: separar sin ordenar ---")

def partition_por_umbral(lista: list, umbral: float) -> tuple:
    """
    Separa en dos listas: menores y mayores que umbral.
    O(N) tiempo, O(N) espacio.
    """
    menores = [x for x in lista if x <= umbral]
    mayores = [x for x in lista if x > umbral]
    return menores, mayores

scores_part = [random.random() for _ in range(20)]
bajo_umbral, sobre_umbral = partition_por_umbral(scores_part, 0.5)
print(f"\nScores < 0.5: {len(bajo_umbral)} elementos")
print(f"Scores > 0.5: {len(sobre_umbral)} elementos")
print(f"Total preservado: {len(bajo_umbral) + len(sobre_umbral) == len(scores_part)}")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN ARQUITECTÓNICA ===")
print("=" * 80)

"""
RESUMEN DE SORTING PARA INGENIERÍA IA:

1. O(N log N) es el límite teórico para sorts basados en comparaciones.

2. Python usa TIMSORT: híbrido Merge Sort + Insertion Sort.
   - O(N) en datos ya ordenados.
   - O(N log N) en datos aleatorios.
   - SIEMPRE estable. NUNCA peor que O(N log N).

3. sorted() crea nueva lista (trabaja con cualquier iterable).
   list.sort() modifica in-place (solo listas, más eficiente).

4. key= acepta funciones: lambda, itemgetter, attrgetter.
   Para multi-criterio, retorna TUPLA desde key.

5. Estabilidad: la garantía de que elementos iguales mantienen
   su orden relativo. Permite sorts sucesivos por múltiples criterios.

6. Top-K: usa heapq.nlargest/nsmallest, no sorted()[:K].
   O(N log K) vs O(N log N).

7. Counting Sort O(N+K): más rápido que Timsort para enteros acotados.

8. argsort: obtener índices de ordenación sin modificar el original.

9. Timsort detecta "runs" y los merge: escala suavemente con el desorden.

10. Quick Sort: O(N²) en peor caso. Python eligió Timsort por predecibilidad.

11. cmp_to_key: para comparaciones complejas (versiones, natural sort).

12. Partial sort: heapq para Top-K y mediana sin ordenar todo.

BENCHMARK RESUMEN (N = 1M, datos aleatorios):
  - Insertion Sort: ~intratable (O(N²) = minutos)
  - Quick Sort:     ~350ms (O(N log N) promedio, pero O(N²) peor caso)
  - Merge Sort:     ~500ms (O(N log N) siempre, pero lento en Python puro)
  - sorted():       ~180ms (Timsort en C, O(N log N), estable)
  - Counting Sort:  ~50ms (O(N+K), pero solo para enteros acotados)

CONCLUSIÓN FINAL:
  En Python, sorted() y list.sort() son la ÚNICA opción en producción.
  Cualquier reimplementación en Python puro será 5-50x más lenta
  que la implementación en C de Timsort. Los algoritmos clásicos
  se estudian para ENTENDER la teoría, no para usarlos.

Siguiente archivo: Heaps y colas de prioridad.
"""

print("\n FIN DE ARCHIVO 03_sorting_y_timsort.")
print(" El motor de ordenación de Python ha sido diseccionado.")


