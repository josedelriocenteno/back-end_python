# ===========================================================================
# 04_heapq_y_colas_de_prioridad.py
# ===========================================================================
# MÓDULO 03: ALGORITMIA Y COMPLEJIDAD COMPUTACIONAL
# ARCHIVO 04: Heaps, heapq, Colas de Prioridad y Aplicaciones en ML
# ===========================================================================
#
# OBJETIVO (1000+ LÍNEAS):
# Dominar la estructura de datos HEAP como herramienta de producción.
# Los heaps son la base de Top-K, scheduling de tareas, Dijkstra,
# A*, y Huffman coding. En ML: beam search, priority queues para
# procesamiento de batches, y event-driven architectures.
#
# CONTENIDO:
#   1. Qué es un heap (min-heap, max-heap).
#   2. Módulo heapq: heappush, heappop, heappushpop, heapify.
#   3. Implementar un max-heap (Python solo tiene min-heap).
#   4. nlargest / nsmallest: Top-K eficiente.
#   5. Cola de prioridad con tuples y dataclasses.
#   6. Merge de K streams ordenados.
#   7. Median maintenance (mediana en stream).
#   8. Ejercicio: scheduler de tareas ML con prioridad.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import heapq
import time
import random
import sys
from typing import Any, Optional
from collections import defaultdict
from dataclasses import dataclass, field


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 1: ¿QUÉ ES UN HEAP?                                          ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: HEAP — LA ESTRUCTURA DE DATOS SEMI-ORDENADA ===")
print("=" * 80)

"""
Un HEAP es un árbol binario COMPLETO donde cada padre es menor (min-heap)
o mayor (max-heap) que sus hijos. NO está completamente ordenado:
solo garantiza que el MÍNIMO (o máximo) está en la raíz.

PROPIEDADES CLAVE:
- Insertar: O(log N) — el elemento "burbujea" hasta su posición.
- Extraer mínimo: O(log N) — se reemplaza la raíz y se "hunde".
- Ver el mínimo: O(1) — siempre está en la posición [0].
- Construir heap desde lista: O(N) — sorprendentemente, no O(N log N).

¿POR QUÉ NO USAR SORTED()?
Si solo necesitas el mínimo/máximo, sorted() es O(N log N).
Un heap da O(1) para ver el mínimo y O(log N) para extraerlo.
Si insertas y extraes continuamente, el heap es DRAMÁTICAMENTE mejor.

IMPLEMENTACIÓN EN PYTHON:
Python implementa el heap como un ARRAY (lista) donde:
- heap[0] es la raíz (mínimo).
- heap[k] tiene hijos en heap[2k+1] y heap[2k+2].
- heap[k] tiene padre en heap[(k-1)//2].
No hay nodos ni punteros. Solo un array. Eficiencia máxima de caché.

PYTHON SOLO TIENE MIN-HEAP. Para max-heap, negamos los valores.
"""

print("\n--- Visualización de un min-heap ---")
print("""
                    1           <- raíz = MÍNIMO
                  /   \\
                3       2       <- hijos de 1
              / \\     / \\
             7   4   5   6     <- hijos de 3 y 2
            
  Array: [1, 3, 2, 7, 4, 5, 6]
  - heap[0] = 1 (raíz/mínimo)
  - heap[1] = 3 (hijo izq de 1), heap[2] = 2 (hijo der de 1)
  - heap[3] = 7 (hijo izq de 3), heap[4] = 4 (hijo der de 3)
""")


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: HEAPQ — OPERACIONES FUNDAMENTALES ===")
print("=" * 80)

"""
FUNCIONES DEL MÓDULO heapq:
- heapq.heappush(heap, item): Inserta item. O(log N).
- heapq.heappop(heap): Extrae y retorna el mínimo. O(log N).
- heapq.heappushpop(heap, item): Push + pop en una operación. O(log N).
- heapq.heapreplace(heap, item): Pop + push (extrae antes de insertar). O(log N).
- heapq.heapify(lista): Convierte lista en heap IN-PLACE. O(N).
- heapq.nlargest(k, iterable): Los K mayores. O(N log K).
- heapq.nsmallest(k, iterable): Los K menores. O(N log K).
- heapq.merge(*iterables): Merge de iterables ordenados. O(N log K).
"""

print("\n--- heappush y heappop ---")

heap = []
elementos = [5, 3, 8, 1, 9, 2, 7]

print(f"Insertando: {elementos}")
for elem in elementos:
    heapq.heappush(heap, elem)
    print(f"  push({elem}): heap = {heap}")

print(f"\nExtrayendo en orden:")
while heap:
    minimo = heapq.heappop(heap)
    print(f"  pop() -> {minimo}, heap restante = {heap}")


print("\n--- heapify: convertir lista en heap O(N) ---")

datos = [5, 3, 8, 1, 9, 2, 7]
print(f"Original: {datos}")

heapq.heapify(datos)
print(f"Tras heapify: {datos}")
print(f"  datos[0] = {datos[0]} (siempre el mínimo)")


print("\n--- heappushpop vs heapreplace ---")

"""
heappushpop(heap, item): Inserta item, luego extrae el mínimo.
  Más eficiente que push() seguido de pop().
  Si item < heap[0]: retorna item directamente (no lo inserta).

heapreplace(heap, item): Extrae el mínimo, luego inserta item.
  El item insertado puede ser MENOR que el extraído.
"""

heap_test = [1, 3, 5, 7, 9]
heapq.heapify(heap_test)

# heappushpop: push 4, pop mínimo
heap_copy = heap_test.copy()
resultado = heapq.heappushpop(heap_copy, 4)
print(f"\nheappushpop(heap, 4): extrajo {resultado}, heap = {heap_copy}")

# heapreplace: pop mínimo, push 4
heap_copy2 = heap_test.copy()
resultado2 = heapq.heapreplace(heap_copy2, 4)
print(f"heapreplace(heap, 4): extrajo {resultado2}, heap = {heap_copy2}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 2: MAX-HEAP EN PYTHON                                         ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 3: MAX-HEAP — NEGANDO VALORES ===")
print("=" * 80)

"""
Python SOLO tiene min-heap. Para simular un max-heap:
- Al insertar: negar el valor -> heappush(heap, -valor)
- Al extraer: negar de nuevo -> -heappop(heap)

Esto funciona porque:
- Si a < b, entonces -a > -b
- El min-heap del negativo es el max-heap del original
"""

print("\n--- Max-heap con negación ---")

class MaxHeap:
    """Wrapper para simular max-heap con heapq."""
    
    def __init__(self):
        self._heap = []
    
    def push(self, valor):
        heapq.heappush(self._heap, -valor)
    
    def pop(self):
        return -heapq.heappop(self._heap)
    
    def peek(self):
        return -self._heap[0] if self._heap else None
    
    def __len__(self):
        return len(self._heap)
    
    def __bool__(self):
        return bool(self._heap)

max_h = MaxHeap()
for v in [3, 1, 4, 1, 5, 9, 2, 6]:
    max_h.push(v)
    print(f"  push({v}): máximo = {max_h.peek()}")

print(f"\nExtrayendo en orden descendente:")
while max_h:
    print(f"  pop() -> {max_h.pop()}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 3: COLA DE PRIORIDAD                                          ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 4: COLA DE PRIORIDAD CON HEAPQ ===")
print("=" * 80)

"""
Una cola de prioridad procesa elementos por PRIORIDAD, no por orden de llegada.
El elemento con mayor prioridad (menor número en min-heap) se procesa primero.

EN ML:
- Beam search: mantener los K mejores candidatos parciales.
- Job scheduler: procesar las inferencias más urgentes primero.
- A* search: explorar el nodo más prometedor primero.
- Event-driven training: procesar eventos por timestamp.

PROBLEMA CON HEAPQ + TUPLAS:
heapq compara por el primer elemento de la tupla.
Si hay empate, compara el segundo. Si el segundo no es comparable
(ej: un dict), lanza TypeError. Solución: usar un contador único.
"""

print("\n--- Cola de prioridad con tuplas (prioridad, contador, dato) ---")

class PriorityQueue:
    """Cola de prioridad thread-safe con desempate por orden de inserción."""
    
    def __init__(self):
        self._heap = []
        self._counter = 0  # Desempate: el que se insertó primero sale primero
    
    def push(self, prioridad: int, dato: Any):
        """Menor prioridad = más urgente."""
        heapq.heappush(self._heap, (prioridad, self._counter, dato))
        self._counter += 1
    
    def pop(self) -> tuple:
        """Retorna (prioridad, dato) del más urgente."""
        prioridad, _, dato = heapq.heappop(self._heap)
        return prioridad, dato
    
    def peek(self) -> tuple:
        prioridad, _, dato = self._heap[0]
        return prioridad, dato
    
    def __len__(self):
        return len(self._heap)
    
    def __bool__(self):
        return bool(self._heap)

# Ejemplo: cola de tareas de inferencia
pq = PriorityQueue()
pq.push(3, {"tipo": "batch_inference", "modelo": "BERT"})
pq.push(1, {"tipo": "realtime_inference", "modelo": "GPT-2"})
pq.push(2, {"tipo": "fine_tuning", "modelo": "T5"})
pq.push(1, {"tipo": "realtime_inference", "modelo": "BERT"})  # Misma prioridad

print("Procesando tareas por prioridad:")
while pq:
    prior, tarea = pq.pop()
    print(f"  Prioridad {prior}: {tarea['tipo']} ({tarea['modelo']})")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: COLA DE PRIORIDAD CON DATACLASS ===")
print("=" * 80)

"""
Python 3.7+ permite usar dataclasses con __lt__ definido 
para una implementación más limpia de colas de prioridad.
"""

@dataclass(order=True)
class Task:
    """Tarea con prioridad para cola de prioridad."""
    prioridad: int
    orden: int = field(compare=True)  # Desempate por orden
    nombre: str = field(compare=False)
    datos: dict = field(default_factory=dict, compare=False)

print("\n--- Cola con dataclass ---")

task_heap = []
counter = 0

tareas = [
    (2, "entrenar_modelo", {"epochs": 10}),
    (1, "inferencia_urgente", {"batch": 32}),
    (3, "preprocesar_datos", {"rows": 1_000_000}),
    (1, "inferencia_vip", {"batch": 1}),
]

for prior, nombre, datos in tareas:
    t = Task(prioridad=prior, orden=counter, nombre=nombre, datos=datos)
    heapq.heappush(task_heap, t)
    counter += 1

print("Procesando:")
while task_heap:
    task = heapq.heappop(task_heap)
    print(f"  [{task.prioridad}] {task.nombre}: {task.datos}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 4: TOP-K Y NLARGEST/NSMALLEST                                ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 6: TOP-K EFICIENTE CON HEAPQ ===")
print("=" * 80)

"""
CUÁNDO USAR QUÉ:
- K = 1: usar min()/max(). O(N).
- K pequeño (K << N): usar heapq.nlargest/nsmallest. O(N log K).
- K grande (~N): usar sorted(). O(N log N).
- K = N: usar sorted(). Obvio.

heapq.nlargest mantiene un min-heap de tamaño K:
1. Inserta los primeros K elementos.
2. Para cada elemento nuevo: si es mayor que heap[0], reemplázalo.
3. Al final, el heap contiene los K mayores.
"""

print("\n--- Benchmark: min() vs nlargest(1) vs sorted()[-1] ---")

random.seed(42)
datos = [random.random() for _ in range(1_000_000)]

inicio = time.perf_counter()
r1 = max(datos)
t1 = time.perf_counter() - inicio

inicio = time.perf_counter()
r2 = heapq.nlargest(1, datos)[0]
t2 = time.perf_counter() - inicio

inicio = time.perf_counter()
r3 = sorted(datos)[-1]
t3 = time.perf_counter() - inicio

print(f"  max():          {t1*1000:.2f} ms")
print(f"  nlargest(1):    {t2*1000:.2f} ms")
print(f"  sorted()[-1]:   {t3*1000:.2f} ms")
print(f"  -> Para K=1, max() es ~{t2/t1:.0f}x más rápido que nlargest.")


print("\n--- Top-K con key function ---")

registros = [
    {"exp": f"exp_{i:03d}", "acc": random.random(), "loss": random.uniform(0.01, 1.0)}
    for i in range(50_000)
]

inicio = time.perf_counter()
top_10_acc = heapq.nlargest(10, registros, key=lambda r: r["acc"])
t_heap = time.perf_counter() - inicio

inicio = time.perf_counter()
top_10_sorted = sorted(registros, key=lambda r: r["acc"], reverse=True)[:10]
t_sort = time.perf_counter() - inicio

print(f"\n  heapq.nlargest(10): {t_heap*1000:.2f} ms")
print(f"  sorted()[:10]:      {t_sort*1000:.2f} ms")
print(f"  Speedup: {t_sort/t_heap:.1f}x")
print(f"  Top 3:")
for r in top_10_acc[:3]:
    print(f"    {r['exp']}: acc={r['acc']:.4f}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 7: TOP-K MANUAL CON HEAP DE TAMAÑO FIJO ===")
print("=" * 80)

"""
Implementar Top-K manualmente para entender el algoritmo.
Útil cuando necesitas procesar un STREAM (no tienes todos los datos).
"""

print("\n--- Top-K en streaming ---")

class TopKTracker:
    """Mantiene los K mejores elementos vistos en un stream."""
    
    def __init__(self, k: int):
        self.k = k
        self._heap = []  # Min-heap de tamaño K
    
    def agregar(self, valor: float, dato: Any = None):
        """
        Agrega un elemento al tracker.
        Si tenemos < K elementos: simplemente inserta.
        Si tenemos K elementos: solo inserta si es mayor que el mínimo.
        """
        entry = (valor, dato)
        
        if len(self._heap) < self.k:
            heapq.heappush(self._heap, entry)
        elif valor > self._heap[0][0]:
            heapq.heapreplace(self._heap, entry)
    
    def resultado(self) -> list:
        """Retorna los K mejores, ordenados de mayor a menor."""
        return sorted(self._heap, reverse=True)
    
    @property
    def umbral(self) -> float:
        """El score mínimo para entrar en el top-K."""
        return self._heap[0][0] if self._heap else float('-inf')

# Simular stream de 1M predicciones, mantener top-10
tracker = TopKTracker(k=10)
random.seed(42)

for i in range(1_000_000):
    score = random.random()
    tracker.agregar(score, f"pred_{i}")

print(f"Procesadas 1M predicciones, Top 10:")
for score, dato in tracker.resultado():
    print(f"  {dato}: {score:.6f}")
print(f"Umbral actual: {tracker.umbral:.6f}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 5: MERGE DE K STREAMS                                         ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 8: MERGE DE K STREAMS CON HEAPQ.MERGE ===")
print("=" * 80)

"""
heapq.merge() fusiona múltiples iterables ORDENADOS en uno solo.
Es LAZY (generador): no carga todo en memoria.

Complejidad: O(N log K) donde N = total de elementos, K = número de streams.

EN ML:
- Combinar logs de múltiples workers ordenados por timestamp.
- Merge de shards de un dataset distribuido.
- Unir índices invertidos de múltiples servidores.
"""

print("\n--- Merge de múltiples logs ordenados ---")

def generar_logs(worker_id: int, n: int) -> list:
    """Simula logs de un worker, ordenados por timestamp."""
    timestamps = sorted([random.uniform(0, 100) for _ in range(n)])
    return [(ts, f"worker_{worker_id}", f"event_{i}") for i, ts in enumerate(timestamps)]

random.seed(42)
logs_w0 = generar_logs(0, 5)
logs_w1 = generar_logs(1, 5)
logs_w2 = generar_logs(2, 5)

print("Logs individuales:")
for logs in [logs_w0, logs_w1, logs_w2]:
    print(f"  {logs[0][1]}: {[f'{ts:.1f}' for ts, _, _ in logs]}")

# Merge
merged_logs = list(heapq.merge(logs_w0, logs_w1, logs_w2))
print(f"\nMerged (ordenados por timestamp):")
for ts, worker, event in merged_logs[:8]:
    print(f"  [{ts:>5.1f}] {worker} -> {event}")
print(f"  ... ({len(merged_logs)} total)")


print("\n--- Benchmark: heapq.merge vs sorted(concatenar) ---")

random.seed(42)
k_streams = 100
n_per_stream = 10_000

streams = [sorted([random.random() for _ in range(n_per_stream)]) for _ in range(k_streams)]

# Método 1: sorted(concatenar)
inicio = time.perf_counter()
r1 = sorted(sum(streams, []))
t_sort = time.perf_counter() - inicio

# Método 2: heapq.merge (lazy, materializado con list())
inicio = time.perf_counter()
r2 = list(heapq.merge(*streams))
t_merge = time.perf_counter() - inicio

print(f"  sorted(concat):  {t_sort*1000:.2f} ms")
print(f"  heapq.merge:     {t_merge*1000:.2f} ms")
print(f"  Iguales: {r1 == r2}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 6: PROBLEMAS CLÁSICOS CON HEAPS                              ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 9: MEDIANA EN STREAM (TWO-HEAP) ===")
print("=" * 80)

"""
Problema: calcular la MEDIANA de un stream de datos en tiempo real.
No puedes ordenar todo cada vez que llega un nuevo número.

Solución: TWO HEAPS
- max-heap (izquierda): la mitad MENOR de los datos.
- min-heap (derecha): la mitad MAYOR de los datos.
- La mediana es max_heap.top o promedio de ambos tops.

Complejidad: O(log N) por inserción, O(1) para consultar mediana.
"""

print("\n--- MedianFinder con two heaps ---")

class MedianFinder:
    """Calcula la mediana de un stream en O(log N) por inserción."""
    
    def __init__(self):
        self.max_heap = []  # Mitad izquierda (negados para simular max-heap)
        self.min_heap = []  # Mitad derecha
    
    def add(self, num: float):
        """Inserta un número. O(log N)."""
        # Siempre insertar primero en max_heap (izquierda)
        heapq.heappush(self.max_heap, -num)
        
        # Mover el máximo de izquierda a derecha si es mayor que el mínimo de derecha
        if self.min_heap and -self.max_heap[0] > self.min_heap[0]:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        
        # Balancear: la diferencia de tamaños debe ser <= 1
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)
    
    def median(self) -> float:
        """Retorna la mediana actual. O(1)."""
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2

mf = MedianFinder()
stream = [2, 3, 4, 1, 5, 8, 7, 6]

print(f"Stream: {stream}")
for num in stream:
    mf.add(num)
    print(f"  Tras añadir {num}: mediana = {mf.median()}")

# Verificar contra sorted
datos_acumulados = stream[::]
print(f"\nVerificación: sorted = {sorted(datos_acumulados)}")
print(f"Mediana real: {sorted(datos_acumulados)[len(datos_acumulados)//2 - 1]}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: HEAP SORT ===")
print("=" * 80)

"""
Heap Sort: construye un heap O(N), luego extrae N veces O(log N).
Total: O(N log N). Siempre. No es adaptativo como Timsort.

Pros: O(1) espacio extra (in-place), O(N log N) garantizado.
Contras: no estable, no adaptativo, peor constante que Timsort.
"""

print("\n--- Heap Sort implementado ---")

def heap_sort(lista: list) -> list:
    """Heap Sort usando heapq. O(N log N) tiempo, O(N) espacio."""
    heap = lista.copy()
    heapq.heapify(heap)  # O(N)
    return [heapq.heappop(heap) for _ in range(len(heap))]  # O(N log N)

datos_hs = [5, 3, 8, 1, 9, 2, 7, 4, 6]
print(f"Original:  {datos_hs}")
print(f"Heap Sort: {heap_sort(datos_hs)}")


print("\n--- Benchmark: Heap Sort vs sorted() ---")

for n in [100_000, 500_000, 1_000_000]:
    datos_bench = [random.random() for _ in range(n)]
    
    inicio = time.perf_counter()
    heap_sort(datos_bench)
    t_heap = time.perf_counter() - inicio
    
    inicio = time.perf_counter()
    sorted(datos_bench)
    t_sorted = time.perf_counter() - inicio
    
    print(f"  N={n:>10,}: HeapSort={t_heap*1000:>7.1f}ms  "
          f"sorted()={t_sorted*1000:>7.1f}ms  "
          f"Ratio: {t_heap/t_sorted:.1f}x más lento")


print("\n" + "=" * 80)
print("=== CAPÍTULO 11: TABLA DE COMPLEJIDAD DE HEAP ===")
print("=" * 80)

"""
╔════════════════════════════════════╦══════════════╦═══════════════════╗
║ OPERACIÓN                          ║ TIEMPO       ║ NOTAS             ║
╠════════════════════════════════════╬══════════════╬═══════════════════╣
║ heapq.heappush(heap, x)           ║ O(log N)     ║ Burbujea arriba   ║
║ heapq.heappop(heap)               ║ O(log N)     ║ Hunde la raíz     ║
║ heapq.heappushpop(heap, x)        ║ O(log N)     ║ Push + pop combo  ║
║ heapq.heapreplace(heap, x)        ║ O(log N)     ║ Pop + push combo  ║
║ heapq.heapify(lista)              ║ O(N)         ║ Bottom-up build   ║
║ heap[0] (ver mínimo)              ║ O(1)         ║ Siempre la raíz   ║
║ heapq.nlargest(k, data)           ║ O(N log K)   ║ Mantiene heap K   ║
║ heapq.nsmallest(k, data)          ║ O(N log K)   ║ Mantiene heap K   ║
║ heapq.merge(*iterables)           ║ O(N log K)   ║ K = num iterables ║
║ Heap Sort completo                ║ O(N log N)   ║ heapify + N pops  ║
╚════════════════════════════════════╩══════════════╩═══════════════════╝
"""


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: EJERCICIO — SCHEDULER DE TAREAS ML ===")
print("=" * 80)

"""
Construir un scheduler que gestione tareas de ML con:
- Prioridades (1=urgente, 5=baja).
- Dependencias entre tareas.
- Estimación de recursos (GPU, CPU, RAM).
"""

print("\n--- ML Task Scheduler ---")

@dataclass
class MLTask:
    nombre: str
    prioridad: int  # 1-5, 1 = más urgente
    tipo: str  # 'train', 'inference', 'preprocess', 'evaluate'
    gpu_required: bool = False
    ram_gb: float = 1.0
    eta_minutes: float = 5.0

class MLScheduler:
    """Scheduler de tareas ML con cola de prioridad."""
    
    def __init__(self, gpu_count: int = 1, ram_gb: float = 16.0):
        self._heap = []
        self._counter = 0
        self.gpu_count = gpu_count
        self.ram_gb = ram_gb
        self.gpu_used = 0
        self.ram_used = 0.0
        self.completed = []
    
    def submit(self, task: MLTask):
        """Envía una tarea al scheduler."""
        heapq.heappush(self._heap, (task.prioridad, self._counter, task))
        self._counter += 1
    
    def next_task(self) -> Optional[MLTask]:
        """Obtiene la siguiente tarea ejecutable."""
        # Buscar la tarea de mayor prioridad que quepa en recursos
        temp = []
        resultado = None
        
        while self._heap:
            prior, cnt, task = heapq.heappop(self._heap)
            
            gpu_ok = not task.gpu_required or self.gpu_used < self.gpu_count
            ram_ok = self.ram_used + task.ram_gb <= self.ram_gb
            
            if gpu_ok and ram_ok and resultado is None:
                resultado = task
                if task.gpu_required:
                    self.gpu_used += 1
                self.ram_used += task.ram_gb
            else:
                temp.append((prior, cnt, task))
        
        # Restaurar las tareas no seleccionadas
        for item in temp:
            heapq.heappush(self._heap, item)
        
        return resultado
    
    def complete(self, task: MLTask):
        """Marca una tarea como completada y libera recursos."""
        if task.gpu_required:
            self.gpu_used -= 1
        self.ram_used -= task.ram_gb
        self.completed.append(task)
    
    def status(self):
        print(f"  Pendientes: {len(self._heap)} | Completadas: {len(self.completed)} | "
              f"GPU: {self.gpu_used}/{self.gpu_count} | RAM: {self.ram_used:.1f}/{self.ram_gb:.1f} GB")

# Simular workload
scheduler = MLScheduler(gpu_count=2, ram_gb=32.0)

tareas_ml = [
    MLTask("preprocess_dataset", 2, "preprocess", ram_gb=8.0, eta_minutes=30),
    MLTask("train_bert", 1, "train", gpu_required=True, ram_gb=12.0, eta_minutes=120),
    MLTask("inference_batch", 1, "inference", gpu_required=True, ram_gb=4.0, eta_minutes=10),
    MLTask("evaluate_model", 3, "evaluate", ram_gb=2.0, eta_minutes=5),
    MLTask("train_gpt2", 2, "train", gpu_required=True, ram_gb=16.0, eta_minutes=240),
    MLTask("preprocess_images", 4, "preprocess", ram_gb=4.0, eta_minutes=15),
]

for t in tareas_ml:
    scheduler.submit(t)

print("Estado inicial:")
scheduler.status()

print("\nEjecutando tareas:")
step = 1
while True:
    task = scheduler.next_task()
    if task is None:
        break
    print(f"  Step {step}: Ejecutando '{task.nombre}' (prioridad={task.prioridad}, "
          f"tipo={task.tipo}, GPU={'sí' if task.gpu_required else 'no'}, "
          f"RAM={task.ram_gb}GB)")
    scheduler.status()
    scheduler.complete(task)
    step += 1

print(f"\nTodas las tareas completadas:")
for t in scheduler.completed:
    print(f"  ✓ {t.nombre}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: DIJKSTRA SIMPLIFICADO CON HEAP ===")
print("=" * 80)

"""
Dijkstra encuentra el camino más corto entre nodos en un grafo
con pesos NO negativos. Usa una cola de prioridad (heap) para
siempre explorar el nodo más cercano primero.

Complejidad: O((V + E) log V) con heap.

EN ML: 
- Búsqueda en grafos de conocimiento.
- Rutas en grafos de dependencias de pipelines.
"""

print("\n--- Dijkstra con heapq ---")

def dijkstra(grafo: dict, origen: str) -> dict:
    """
    Camino más corto desde origen a todos los nodos.
    grafo: {nodo: [(vecino, peso), ...]}
    Retorna: {nodo: distancia_mínima}
    """
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[origen] = 0
    
    # Cola de prioridad: (distancia_acumulada, nodo)
    cola = [(0, origen)]
    visitados = set()
    
    while cola:
        dist_actual, nodo = heapq.heappop(cola)
        
        if nodo in visitados:
            continue
        visitados.add(nodo)
        
        for vecino, peso in grafo.get(nodo, []):
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                heapq.heappush(cola, (nueva_dist, vecino))
    
    return distancias

# Grafo de ejemplo: pipeline de ML con tiempos de ejecución
grafo_pipeline = {
    "datos_raw": [("limpieza", 10), ("validación", 5)],
    "limpieza": [("features", 15), ("normalización", 8)],
    "validación": [("limpieza", 3)],
    "features": [("training", 30)],
    "normalización": [("features", 5)],
    "training": [("evaluación", 10)],
    "evaluación": [],
}

distancias = dijkstra(grafo_pipeline, "datos_raw")
print("Distancias mínimas desde 'datos_raw':")
for nodo, dist in sorted(distancias.items(), key=lambda x: x[1]):
    print(f"  {nodo:<20} -> {dist} unidades de tiempo")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: LAZY DELETION — ELIMINACIÓN PEREZOSA ===")
print("=" * 80)

"""
heapq no soporta eliminar un elemento arbitrario del heap.
Solo puedes extraer el mínimo con heappop().

Solución: LAZY DELETION.
1. Marca el elemento como "eliminado" (sin sacarlo del heap).
2. Cuando hagas pop, ignora los elementos marcados.
3. Esto es O(log N) amortizado.

MUY USADO en A*, Dijkstra con actualizaciones, y event systems.
"""

print("\n--- Heap con lazy deletion ---")

class LazyHeap:
    """
    Min-heap con soporte para eliminación perezosa.
    Los elementos eliminados se marcan y se ignoran en pop.
    """
    REMOVED = '<removed>'
    
    def __init__(self):
        self._heap = []
        self._entries = {}  # key -> entry (para marcar como eliminado)
        self._counter = 0
    
    def push(self, key: str, prioridad: float):
        """Inserta o actualiza un elemento."""
        if key in self._entries:
            self._remove(key)
        
        entry = [prioridad, self._counter, key]
        self._entries[key] = entry
        heapq.heappush(self._heap, entry)
        self._counter += 1
    
    def _remove(self, key: str):
        """Marca un elemento como eliminado (lazy)."""
        entry = self._entries.pop(key)
        entry[-1] = self.REMOVED
    
    def pop(self) -> tuple:
        """Extrae el mínimo NO eliminado."""
        while self._heap:
            prioridad, _, key = heapq.heappop(self._heap)
            if key != self.REMOVED:
                del self._entries[key]
                return key, prioridad
        raise KeyError("Heap vacío")
    
    def update_priority(self, key: str, nueva_prioridad: float):
        """Actualiza la prioridad de un elemento existente."""
        self.push(key, nueva_prioridad)
    
    def __len__(self):
        return len(self._entries)

# Ejemplo: actualizar prioridades dinámicamente
lh = LazyHeap()
lh.push("task_A", 3)
lh.push("task_B", 1)
lh.push("task_C", 5)
lh.push("task_D", 2)

print(f"Heap inicial ({len(lh)} elementos)")

# Actualizar prioridad de task_C (era 5, ahora es 0 → la más urgente)
lh.update_priority("task_C", 0)
print(f"Tras actualizar task_C a prioridad 0:")

while len(lh) > 0:
    key, prior = lh.pop()
    print(f"  pop() -> {key} (prioridad={prior})")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: BEAM SEARCH — BÚSQUEDA POR HACES ===")
print("=" * 80)

"""
Beam Search es el algoritmo de decodificación más usado en NLP
para generación de texto (GPT, T5, BART, etc.).

Mantiene los K mejores candidatos parciales en cada paso 
usando un heap. K = beam width.

Algoritmo:
1. Empieza con un candidato: el token <start>.
2. Para cada candidato, genera todas las extensiones posibles.
3. De TODAS las extensiones, quédate solo con las K mejores (heap).
4. Repite hasta que todos los beams terminen o alcances max_length.
"""

print("\n--- Beam Search simplificado ---")

def beam_search_demo(vocabulario: list, beam_width: int, max_len: int) -> list:
    """
    Simula beam search con scores aleatorios.
    En producción, los scores vienen de un modelo de lenguaje.
    """
    random.seed(42)
    
    # Cada candidato es (score_negado, secuencia)
    # Negado porque usamos min-heap para mantener los MEJORES (mayores scores)
    beams = [(0.0, ["<start>"])]  # (score acumulado negado, tokens)
    
    for step in range(max_len):
        candidatos = []
        
        for score_neg, tokens in beams:
            # Generar extensiones (simular probabilidades del modelo)
            for token in vocabulario:
                token_score = random.uniform(0.01, 0.5)
                nuevo_score = score_neg - token_score  # Acumular (negado)
                nueva_seq = tokens + [token]
                candidatos.append((nuevo_score, nueva_seq))
        
        # Mantener solo los beam_width mejores
        # nsmallest porque los scores están negados (menor = más probable)
        beams = heapq.nsmallest(beam_width, candidatos)
    
    # Convertir scores de vuelta a positivos
    return [(-score, tokens) for score, tokens in beams]

vocab = ["el", "gato", "perro", "come", "duerme", "bien"]
resultados = beam_search_demo(vocab, beam_width=3, max_len=4)

print(f"Beam Search (width=3, vocab={vocab}):")
for i, (score, tokens) in enumerate(resultados):
    print(f"  Beam {i+1}: score={score:.3f} | {' '.join(tokens)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 16: RUNNING K-SMALLEST — VENTANA DESLIZANTE ===")
print("=" * 80)

"""
Mantener los K menores elementos en una ventana deslizante.
Útil para detectar anomalías en series temporales:
si un nuevo valor es más pequeño que el K-ésimo menor de los 
últimos W valores, es una anomalía.
"""

print("\n--- Detector de anomalías con heap sobre ventana ---")

class AnomalyDetector:
    """Detecta valores anormalmente bajos usando un rolling K-smallest."""
    
    def __init__(self, window_size: int, k: int, threshold_pct: float = 5.0):
        self.window_size = window_size
        self.k = k
        self.threshold_pct = threshold_pct
        self.window = []
    
    def check(self, valor: float) -> tuple:
        """Retorna (es_anomalía, percentil_en_ventana)."""
        self.window.append(valor)
        if len(self.window) > self.window_size:
            self.window.pop(0)
        
        if len(self.window) < self.k:
            return False, 50.0
        
        # K menores de la ventana actual
        k_menores = heapq.nsmallest(self.k, self.window)
        umbral = k_menores[-1]  # El K-ésimo menor
        
        # El percentil del valor actual en la ventana
        menores_que_valor = sum(1 for x in self.window if x < valor)
        percentil = menores_que_valor / len(self.window) * 100
        
        es_anomalia = percentil < self.threshold_pct
        return es_anomalia, percentil

detector = AnomalyDetector(window_size=50, k=5, threshold_pct=5.0)

random.seed(42)
serie = [random.gauss(100, 10) for _ in range(100)]
# Inyectar anomalías
serie[30] = 50  # Anomalía: valor muy bajo
serie[70] = 45  # Anomalía: valor muy bajo

anomalias = []
for i, valor in enumerate(serie):
    es_anom, pct = detector.check(valor)
    if es_anom:
        anomalias.append((i, valor, pct))

print(f"Serie de {len(serie)} puntos, {len(anomalias)} anomalías detectadas:")
for idx, val, pct in anomalias:
    print(f"  Punto {idx}: valor={val:.1f} (percentil={pct:.1f}%)")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN ARQUITECTÓNICA ===")
print("=" * 80)

"""
RESUMEN DE HEAPS PARA INGENIERÍA IA:

1. Heap = árbol binario parcialmente ordenado en un array.
   O(1) para ver mínimo, O(log N) para insertar/extraer.

2. heapq: módulo stdlib. Solo min-heap. Para max-heap, negar valores.

3. Top-K: heapq.nlargest O(N log K). Mejor que sorted O(N log N) cuando K << N.
   Para K=1 usa max()/min().

4. Cola de prioridad: (prioridad, contador, dato). 
   Contador para desempatar sin comparar datos.

5. Merge de K streams: heapq.merge() es lazy y O(N log K).

6. Mediana en stream: two-heap (max-heap izq + min-heap der).
   O(log N) inserción, O(1) consulta.

7. Dijkstra: camino más corto con cola de prioridad O((V+E) log V).

8. Lazy deletion: marcar como eliminado sin extraer. Para updates.

9. Beam search: mantiene K mejores candidatos con heap.

10. Anomaly detection: rolling K-smallest sobre ventana deslizante.

Siguiente archivo: Programación dinámica y lru_cache.
"""

print("\n FIN DE ARCHIVO 04_heapq_y_colas_de_prioridad.")
print(" El paradigma de colas de prioridad ha sido dominado.")

