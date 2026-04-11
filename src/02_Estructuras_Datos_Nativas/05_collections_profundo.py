# ===========================================================================
# 05_collections_profundo.py
# ===========================================================================
# MÓDULO 02: ESTRUCTURAS DE DATOS NATIVAS (AISLADAS)
# ARCHIVO 05: El Módulo collections — Contenedores Especializados de CPython
# ===========================================================================
#
# OBJETIVO ABSOLUTO (1000+ LÍNEAS):
# El módulo `collections` de la Standard Library de Python proporciona 
# contenedores de datos especializados que EXTIENDEN y OPTIMIZAN los tipos
# básicos (list, dict, set, tuple) para casos de uso concretos.
#
# En este archivo aprenderemos cada contenedor de forma AISLADA:
#   1. deque    — Cola de doble extremo O(1). Reemplaza a list para FIFO/LIFO.
#   2. Counter  — Diccionario de frecuencias. La base de Bag-of-Words en NLP.
#   3. defaultdict — Diccionario con fábrica de valores por defecto.
#   4. OrderedDict — Diccionario con orden garantizado (pre-3.7 legacy + LRU).
#   5. ChainMap — Cadena de diccionarios para gestión de configs multi-nivel.
#
# CADA CONTENEDOR se explica desde:
#   - Su estructura interna en C (Objects/*.c de CPython).
#   - Su complejidad asintótica Big-O.
#   - Su caso de uso REAL en pipelines de IA, NLP o MLOps.
#   - Errores comunes y antipatrones.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR. CERO SUPOSICIONES PREVIAS.
# ===========================================================================

import sys
import time
import random
from collections import deque, Counter, defaultdict, OrderedDict, ChainMap


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 1: collections.deque — LA COLA DE DOBLE EXTREMO O(1)          ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: POR QUÉ EXISTE deque (EL FRACASO DE list COMO COLA) ===")
print("=" * 80)

"""
En el archivo 01_listas aprendimos que list.insert(0, x) y list.pop(0) 
tienen complejidad O(N) porque desplazan TODOS los punteros del array interno.

En IA esto es catastrófico cuando necesitas una COLA FIFO (First-In, First-Out):
- Buffer de streaming de tokens de un LLM (los nuevos entran, los viejos salen).
- Ventana deslizante (sliding window) para procesamiento de secuencias temporales.
- BFS (Breadth-First Search) en grafos de conocimiento.
- Rate limiter: guarda los últimos N timestamps de peticiones API.

Para todas estas tareas, necesitas insertar y extraer de AMBOS extremos en O(1).
La list de Python NO puede hacer esto. El deque SÍ.

ESTRUCTURA INTERNA EN C (Modules/_collectionsmodule.c):
Un deque en CPython NO es un array dinámico como la list. Es una LISTA 
DOBLEMENTE ENLAZADA DE BLOQUES (doubly-linked list of fixed-size blocks).

Cada bloque (block) contiene un array fijo de 64 punteros a PyObject.
Los bloques están conectados entre sí por punteros prev/next.

typedef struct BLOCK {
    struct BLOCK *leftlink;   // Puntero al bloque anterior
    struct BLOCK *rightlink;  // Puntero al bloque siguiente
    PyObject *data[BLOCKLEN]; // Array de 64 punteros a objetos
} block;

Esto significa:
- Añadir/quitar por la IZQUIERDA: O(1). Solo mueves un puntero dentro del bloque.
- Añadir/quitar por la DERECHA: O(1). Igual.
- Acceder por ÍNDICE (deque[i]): O(N). Tiene que saltar entre bloques.
  ¡ESTE ES EL TRADE-OFF! Si necesitas acceso aleatorio rápido, usa list.
  Si necesitas inserción/extracción por ambos lados, usa deque.
"""

print("\n--- Benchmark: list.pop(0) vs deque.popleft() ---")

# Creamos estructuras con 100,000 elementos
n = 100_000
lista_cola = list(range(n))
deque_cola = deque(range(n))

# Medir list.pop(0) - Debería ser LENTO (O(N) por cada pop)
inicio = time.perf_counter()
while lista_cola:
    lista_cola.pop(0)
tiempo_lista = time.perf_counter() - inicio

# Medir deque.popleft() - Debería ser RÁPIDO (O(1) por cada pop)
inicio = time.perf_counter()
while deque_cola:
    deque_cola.popleft()
tiempo_deque = time.perf_counter() - inicio

print(f"  list.pop(0)     x {n}: {tiempo_lista*1000:.2f} ms")
print(f"  deque.popleft() x {n}: {tiempo_deque*1000:.2f} ms")
print(f"  Ratio: deque fue ~{tiempo_lista/tiempo_deque:.0f}x más rápido")


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: OPERACIONES FUNDAMENTALES DEL DEQUE ===")
print("=" * 80)

"""
El deque tiene métodos simétricos: todo lo que puedes hacer por la derecha,
lo puedes hacer por la izquierda. Ambos en O(1).
"""

print("\n--- Adición y extracción bidireccional ---")

buffer_tokens = deque()
print(f"Deque vacío: {buffer_tokens}")

# Añadir por la DERECHA (como list.append)
buffer_tokens.append("token_1")
buffer_tokens.append("token_2")
buffer_tokens.append("token_3")
print(f"Tras 3x append (derecha): {buffer_tokens}")

# Añadir por la IZQUIERDA (lo que list NO puede hacer en O(1))
buffer_tokens.appendleft("token_0")
buffer_tokens.appendleft("token_-1")
print(f"Tras 2x appendleft: {buffer_tokens}")

# Extraer por la DERECHA (como list.pop())
ultimo = buffer_tokens.pop()
print(f"pop() extrajo: '{ultimo}' -> {buffer_tokens}")

# Extraer por la IZQUIERDA (lo que list.pop(0) hace en O(N))
primero = buffer_tokens.popleft()
print(f"popleft() extrajo: '{primero}' -> {buffer_tokens}")


print("\n--- extend y extendleft ---")

# extend: añade múltiples elementos por la derecha
buffer_tokens.extend(["A", "B", "C"])
print(f"Tras extend(['A','B','C']): {buffer_tokens}")

# extendleft: añade múltiples por la izquierda, pero OJO: INVIERTE EL ORDEN
# Porque los va añadiendo uno a uno por la izquierda
buffer_tokens.extendleft(["X", "Y", "Z"])
print(f"Tras extendleft(['X','Y','Z']): {buffer_tokens}")
print(f"  -> 'Z' quedó primero porque fue el último en entrar por la izquierda")


print("\n--- rotate: giro circular del deque ---")

rueda = deque([1, 2, 3, 4, 5])
print(f"\nAntes de rotar: {rueda}")

rueda.rotate(2)  # Gira 2 posiciones a la DERECHA
print(f"Tras rotate(2) [derecha]: {rueda}")  # [4, 5, 1, 2, 3]

rueda.rotate(-2)  # Gira 2 posiciones a la IZQUIERDA (deshace)
print(f"Tras rotate(-2) [izquierda]: {rueda}")  # [1, 2, 3, 4, 5]

# Uso en IA: rotar embeddings posicionales (Rotary Position Embedding - RoPE)
# en modelos como LLaMA donde las posiciones se "giran" matemáticamente.


print("\n" + "=" * 80)
print("=== CAPÍTULO 3: DEQUE CON MAXLEN (VENTANA DESLIZANTE AUTOMÁTICA) ===")
print("=" * 80)

"""
El parámetro maxlen es el SUPERPODER del deque para IA.
Cuando creas un deque con maxlen=N, el deque NUNCA supera N elementos.
Si añades un elemento nuevo cuando está lleno, el del extremo OPUESTO
se descarta automáticamente. Sin código extra. Sin if-else.

Esto es EXACTAMENTE lo que necesitas para:
- Sliding window de los últimos N tokens en NLP.
- Buffer circular de los últimos N losses para early stopping.
- Rate limiter: guardar los timestamps de las últimas N peticiones API.
- Media móvil (moving average) de las últimas N métricas.
"""

print("\n--- Ventana deslizante de métricas de entrenamiento ---")

# Queremos monitorizar la media de los últimos 5 losses para early stopping
ventana_loss = deque(maxlen=5)

# Simulamos 10 epochs de entrenamiento
losses_simulados = [2.5, 2.1, 1.8, 1.5, 1.3, 1.2, 1.15, 1.1, 1.08, 1.05]

print(f"{'Epoch':<8} {'Loss':<8} {'Ventana':<30} {'Media Ventana':<15}")
print("-" * 65)

for epoch, loss in enumerate(losses_simulados, 1):
    ventana_loss.append(loss)
    media = sum(ventana_loss) / len(ventana_loss)
    print(f"{epoch:<8} {loss:<8.2f} {str(list(ventana_loss)):<30} {media:<15.4f}")

print(f"\n  -> La ventana NUNCA supera {ventana_loss.maxlen} elementos.")
print(f"  -> Los más antiguos se descartan automáticamente.")
print(f"  -> Tamaño final del deque: {len(ventana_loss)}")


print("\n--- Rate Limiter para APIs de LLMs ---")

from time import perf_counter

class RateLimiter:
    """
    Limita a max_requests peticiones por ventana de window_seconds.
    Implementado con deque(maxlen) para eficiencia O(1).
    """
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = deque(maxlen=max_requests)
    
    def permitir(self) -> bool:
        ahora = perf_counter()
        # Si no hemos llegado al máximo, siempre permitir
        if len(self.timestamps) < self.max_requests:
            self.timestamps.append(ahora)
            return True
        # Si el timestamp más antiguo está fuera de la ventana, permitir
        if ahora - self.timestamps[0] > self.window_seconds:
            self.timestamps.append(ahora)  # El más antiguo se descarta automáticamente
            return True
        return False

limiter = RateLimiter(max_requests=3, window_seconds=1.0)
print(f"\nRate Limiter: max 3 peticiones por segundo")
for i in range(5):
    resultado = limiter.permitir()
    print(f"  Petición {i+1}: {'✓ Permitida' if resultado else '✗ BLOQUEADA'}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 2: collections.Counter — FRECUENCIA Y BAG-OF-WORDS            ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 4: COUNTER — EL DICCIONARIO DE FRECUENCIAS ===")
print("=" * 80)

"""
Counter es una SUBCLASE de dict. Hereda TODO lo que aprendimos en el archivo
02_diccionarios (hash table, O(1) lookup, probing cuadrático, etc.).
La diferencia: los VALUES son siempre conteos (int) y tiene métodos extra
para aritmética de frecuencias.

En NLP, Counter implementa directamente el modelo BAG-OF-WORDS (BoW):
el modelo más básico que representa un documento como un vector de frecuencias 
de palabras, ignorando el orden. Era el estándar antes de que los embeddings
neuronales (Word2Vec, BERT) lo superaran. Pero sigue siendo útil para:
- Análisis exploratorio de corpus.
- Feature extraction rápida en scikit-learn (CountVectorizer usa Counter internamente).
- Detección de anomalías en logs.
- Conteo de tokens para estimación de costes de APIs de LLMs.
"""

print("\n--- Creación desde diferentes fuentes ---")

# Desde una lista (caso más común: tokens de NLP)
tokens_corpus = ["el", "gato", "come", "el", "pez", "y", "el", "gato", "duerme"]
frecuencias = Counter(tokens_corpus)
print(f"Counter desde lista: {frecuencias}")

# Desde un string (cuenta CARACTERES, no palabras)
conteo_chars = Counter("inteligencia artificial")
print(f"Counter desde string: {conteo_chars}")

# Desde kwargs (inicialización directa)
inventario = Counter(gpu_a100=4, gpu_h100=2, cpu_epyc=8)
print(f"Counter desde kwargs: {inventario}")

# Desde un diccionario existente
freq_dict = {"python": 100, "javascript": 80, "rust": 30}
frecuencias_lenguajes = Counter(freq_dict)
print(f"Counter desde dict: {frecuencias_lenguajes}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: MÉTODOS CRÍTICOS DE COUNTER ===")
print("=" * 80)

print("\n--- .most_common(n) — Los N elementos más frecuentes ---")

corpus_grande = Counter(
    ["transformer"] * 150 + ["attention"] * 120 + ["embedding"] * 90 +
    ["layer"] * 80 + ["gradient"] * 60 + ["loss"] * 50 + ["epoch"] * 30 +
    ["batch"] * 20 + ["stride"] * 10 + ["padding"] * 5
)

# Top 5 términos más frecuentes (implementado con heapq internamente -> O(N log K))
top_5 = corpus_grande.most_common(5)
print(f"Top 5 términos del corpus IA:")
for palabra, conteo in top_5:
    barra = "█" * (conteo // 5)
    print(f"  {palabra:<15} {conteo:>4}  {barra}")

# Sin argumento: devuelve TODOS ordenados de mayor a menor
todos_ordenados = corpus_grande.most_common()
print(f"\nTodos ordenados: {todos_ordenados}")

# Los MENOS frecuentes (útil para detectar typos o tokens raros)
menos_frecuentes = corpus_grande.most_common()[:-4:-1]  # Últimos 3
print(f"3 menos frecuentes (posibles typos): {menos_frecuentes}")


print("\n--- .elements() — Expande el Counter a iterable repetido ---")

mini_counter = Counter(a=3, b=1, c=2)
expansion = list(mini_counter.elements())
print(f"Counter {mini_counter} expandido: {expansion}")
# -> ['a', 'a', 'a', 'b', 'c', 'c']
# Útil para reconstruir la lista original o para sampling con pesos.


print("\n--- .subtract() — Resta de frecuencias (NO elimina negativos) ---")

inventario_inicial = Counter(gpu_a100=10, gpu_h100=5, tpu_v4=3)
uso_este_mes = Counter(gpu_a100=7, gpu_h100=6, tpu_v4=1)

inventario_inicial.subtract(uso_este_mes)
print(f"\nInventario tras subtract: {inventario_inicial}")
print(f"  gpu_h100 = {inventario_inicial['gpu_h100']}  (¡NEGATIVO! Usamos más de las que teníamos)")
# Los valores negativos NO se eliminan. Esto es útil para detectar sobreuso.

# .update() hace la operación INVERSA: SUMA frecuencias
reposicion = Counter(gpu_h100=10)
inventario_inicial.update(reposicion)
print(f"Tras reposición: {inventario_inicial}")


print("\n--- Aritmética directa entre Counters ---")

doc_a = Counter("machine learning is amazing".split())
doc_b = Counter("machine learning is powerful".split())

# Suma: combina frecuencias
union_freq = doc_a + doc_b
print(f"\nSuma (combinar corpus): {union_freq}")

# Resta: elimina, descarta negativos y ceros
diferencia = doc_a - doc_b
print(f"Resta (palabras exclusivas de A): {diferencia}")

# Intersección (&): MÍNIMO de cada frecuencia
interseccion = doc_a & doc_b
print(f"Intersección (palabras compartidas, freq mínima): {interseccion}")

# Unión (|): MÁXIMO de cada frecuencia
union_max = doc_a | doc_b
print(f"Unión (todas, freq máxima): {union_max}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 6: COUNTER PARA ESTIMACIÓN DE COSTES DE APIs LLM ===")
print("=" * 80)

"""
Caso de uso REAL en producción 2026:
Las APIs de OpenAI, Anthropic y Google cobran por TOKEN.
Antes de enviar un prompt a la API, necesitas ESTIMAR cuántos tokens tiene
para calcular el coste. Un Counter sobre los tokens te da la distribución
de frecuencias que necesitas.
"""

print("\n--- Estimador de costes de prompt ---")

def estimar_coste_prompt(texto: str, precio_por_1k_tokens: float = 0.003) -> dict:
    """
    Estimador simplificado. En producción usarías tiktoken de OpenAI.
    Aquí usamos split() como tokenizador básico.
    """
    tokens = texto.lower().split()
    frecuencias = Counter(tokens)
    
    total_tokens = sum(frecuencias.values())
    tokens_unicos = len(frecuencias)
    coste_estimado = (total_tokens / 1000) * precio_por_1k_tokens
    
    return {
        "total_tokens": total_tokens,
        "tokens_unicos": tokens_unicos,
        "ratio_repeticion": 1 - (tokens_unicos / total_tokens) if total_tokens else 0,
        "top_5_tokens": frecuencias.most_common(5),
        "coste_usd": coste_estimado,
    }

prompt_ejemplo = """
Eres un asistente de inteligencia artificial especializado en machine learning.
Tu tarea es analizar el siguiente dataset de machine learning y proporcionar
recomendaciones de machine learning para mejorar el rendimiento del modelo
de machine learning que estamos entrenando.
"""

analisis = estimar_coste_prompt(prompt_ejemplo)
print(f"  Total tokens: {analisis['total_tokens']}")
print(f"  Tokens únicos: {analisis['tokens_unicos']}")
print(f"  Ratio repetición: {analisis['ratio_repeticion']:.2%}")
print(f"  Top 5: {analisis['top_5_tokens']}")
print(f"  Coste estimado: ${analisis['coste_usd']:.6f}")
print(f"  -> Un ratio de repetición alto indica que el prompt se puede optimizar.")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 3: collections.defaultdict — VALORES POR DEFECTO AUTOMÁTICOS  ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 7: DEFAULTDICT — EL DICT QUE NUNCA LANZA KeyError ===")
print("=" * 80)

"""
El problema que resuelve defaultdict es simple pero devastador en código ML:

Con un dict normal, acceder a una clave que no existe lanza KeyError:
    frecuencias = {}
    frecuencias["gato"] += 1  # KeyError: 'gato'

Soluciones antes de defaultdict:
    1. if "gato" not in freq: freq["gato"] = 0   # 2 lookups, feo
    2. freq["gato"] = freq.get("gato", 0) + 1    # Funcional pero verboso
    3. freq.setdefault("gato", 0)                 # Correcto pero poco legible

defaultdict elimina todo esto: le pasas una FÁBRICA (factory function) que
genera el valor por defecto cuando accedes a una clave inexistente.
La fábrica se ejecuta SOLO cuando la clave no existe. Es lazy.
"""

print("\n--- Fábricas comunes ---")

# int() como fábrica -> devuelve 0 (perfecto para contadores)
contadores = defaultdict(int)
for palabra in ["gato", "perro", "gato", "gato", "perro"]:
    contadores[palabra] += 1  # Nunca falla. Si no existe, crea con 0 y suma 1.
print(f"defaultdict(int): {dict(contadores)}")

# list() como fábrica -> devuelve [] (perfecto para agrupar)
grupos = defaultdict(list)
datos = [("train", "img_001"), ("val", "img_002"), ("train", "img_003"), 
         ("test", "img_004"), ("val", "img_005"), ("train", "img_006")]

for split, imagen in datos:
    grupos[split].append(imagen)  # Si el split no existe, crea lista vacía y appendea
print(f"\ndefaultdict(list) - Agrupación: {dict(grupos)}")

# set() como fábrica -> devuelve set() (perfecto para relaciones únicas)
grafo_conocimiento = defaultdict(set)
relaciones = [("Python", "usa", "CPython"), ("Python", "usa", "PyPy"),
              ("PyTorch", "depende", "Python"), ("TensorFlow", "depende", "Python"),
              ("Python", "usa", "CPython")]  # Duplicado -> set lo ignora

for sujeto, _, objeto in relaciones:
    grafo_conocimiento[sujeto].add(objeto)
print(f"\ndefaultdict(set) - Grafo: {dict(grafo_conocimiento)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: DEFAULTDICT CON FÁBRICAS LAMBDA Y ANIDADAS ===")
print("=" * 80)

"""
La fábrica puede ser CUALQUIER callable sin argumentos:
- lambda: -> valor personalizado
- Funciones custom
- Incluso otro defaultdict (para crear estructuras multi-nivel automáticas)
"""

print("\n--- Fábrica lambda con valor personalizado ---")

# Configuración de hiperparámetros con defaults inteligentes
# Si alguien accede a un hiperparámetro no configurado, recibe "auto"
config_flexible = defaultdict(lambda: "auto")
config_flexible["learning_rate"] = 0.001
config_flexible["optimizer"] = "adamw"

print(f"LR configurado: {config_flexible['learning_rate']}")
print(f"Optimizer configurado: {config_flexible['optimizer']}")
print(f"Scheduler (no configurado -> auto): {config_flexible['scheduler']}")
print(f"Dropout (no configurado -> auto): {config_flexible['dropout']}")


print("\n--- Matrices de confusión con defaultdict anidado ---")

# defaultdict de defaultdict(int) -> Matriz 2D sparse automática
# Perfecta para matrices de confusión donde la mayoría de celdas son 0

matriz_confusion = defaultdict(lambda: defaultdict(int))

# Simulamos predicciones vs realidad
predicciones = [
    ("gato", "gato"), ("gato", "perro"), ("perro", "perro"),
    ("gato", "gato"), ("pajaro", "pajaro"), ("perro", "gato"),
    ("gato", "gato"), ("perro", "perro"), ("pajaro", "gato"),
]

for real, predicho in predicciones:
    matriz_confusion[real][predicho] += 1

print("\nMatriz de Confusión (generada automáticamente):")
todas_clases = sorted(set(r for r, _ in predicciones) | set(p for _, p in predicciones))
print(f"{'':>10}", end="")
for clase in todas_clases:
    print(f"{clase:>10}", end="")
print()
for clase_real in todas_clases:
    print(f"{clase_real:>10}", end="")
    for clase_pred in todas_clases:
        print(f"{matriz_confusion[clase_real][clase_pred]:>10}", end="")
    print()


print("\n" + "=" * 80)
print("=== CAPÍTULO 9: DEFAULTDICT — PELIGROS Y EFECTOS SECUNDARIOS ===")
print("=" * 80)

"""
PELIGRO CRÍTICO: Acceder a una clave crea la entrada.
Esto puede contaminar tu diccionario con claves fantasma.
"""

print("\n--- El efecto secundario de la lectura ---")

dd_peligroso = defaultdict(int)
dd_peligroso["existe"] = 42

# "Solo estoy MIRANDO si hay algo"... pero el defaultdict CREA la clave
valor = dd_peligroso["no_existe"]  # Ahora "no_existe" EXISTE con valor 0
print(f"Claves tras 'mirar': {list(dd_peligroso.keys())}")
print(f"  -> '¡no_existe' fue CREADA solo por leerla!")

# SOLUCIÓN: Usa `in` o `.get()` para consultar sin crear
dd_seguro = defaultdict(int)
dd_seguro["real"] = 42

# Esto NO crea la clave:
if "fantasma" in dd_seguro:
    print("Existe")
valor_seguro = dd_seguro.get("fantasma", 0)  # Tampoco crea

print(f"Claves seguras (sin fantasmas): {list(dd_seguro.keys())}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 4: collections.OrderedDict — ORDEN EXPLÍCITO + LRU CACHE      ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 10: ORDEREDDICT — ¿SIGUE SIENDO ÚTIL DESPUÉS DE PYTHON 3.7? ===")
print("=" * 80)

"""
Desde Python 3.7, los dict REGULARES preservan el orden de inserción.
Entonces, ¿para qué sirve OrderedDict todavía?

Respuesta: OrderedDict tiene FUNCIONALIDADES EXTRA que dict no tiene:

1. .move_to_end(key, last=True/False) — Puede mover una clave al principio 
   o al final en O(1). Imposible con dict regular.

2. Comparación sensible al orden — Dos OrderedDicts son iguales SOLO si 
   tienen las mismas claves en el MISMO ORDEN. Dos dicts regulares son 
   iguales si tienen las mismas claves sin importar el orden.

3. Implementación de LRU Cache — El método move_to_end + popitem 
   permite construir un cache LRU (Least Recently Used) en pocas líneas.

EN IA: Los LRU Caches son críticos para:
- Cachear embeddings de tokens frecuentes.
- Cachear resultados de inferencia para prompts repetidos.
- Semantic caching en aplicaciones RAG.
"""

print("\n--- move_to_end: reorganización O(1) ---")

od = OrderedDict()
od["c"] = 3
od["a"] = 1
od["b"] = 2
print(f"Orden original: {list(od.keys())}")

od.move_to_end("c")  # Mover "c" al final
print(f"Tras move_to_end('c'): {list(od.keys())}")

od.move_to_end("b", last=False)  # Mover "b" al PRINCIPIO
print(f"Tras move_to_end('b', last=False): {list(od.keys())}")


print("\n--- Comparación sensible al orden ---")

dict_a = {"x": 1, "y": 2}
dict_b = {"y": 2, "x": 1}
print(f"\ndict regular: {{x:1, y:2}} == {{y:2, x:1}}? {dict_a == dict_b}")  # True

od_a = OrderedDict([("x", 1), ("y", 2)])
od_b = OrderedDict([("y", 2), ("x", 1)])
print(f"OrderedDict: [x,y] == [y,x]? {od_a == od_b}")  # False


print("\n--- LRU Cache implementado con OrderedDict ---")

class LRUCache:
    """
    Cache Least Recently Used con capacidad fija.
    Cuando se llena, expulsa la entrada MENOS recientemente usada.
    """
    def __init__(self, capacidad: int):
        self.capacidad = capacidad
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        if key in self.cache:
            # Mover al final (marcarlo como "recientemente usado")
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacidad:
            # Expulsar el PRIMERO (el menos recientemente usado)
            expulsado = self.cache.popitem(last=False)
            # print(f"  [LRU] Expulsado: {expulsado}")
    
    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

# Simular cache de embeddings de tokens
cache_embeddings = LRUCache(capacidad=5)

# Cargamos algunos embeddings
tokens_frecuentes = ["the", "is", "a", "of", "to", "and", "in"]
for i, tok in enumerate(tokens_frecuentes):
    cache_embeddings.put(tok, [0.1 * i] * 4)  # Embedding simulado

# Simulamos lecturas (los más frecuentes se piden más)
lecturas_simuladas = ["the"] * 20 + ["is"] * 15 + ["rare_token"] * 5 + ["a"] * 10
random.shuffle(lecturas_simuladas)

for tok in lecturas_simuladas:
    resultado = cache_embeddings.get(tok)

print(f"\nLRU Cache de Embeddings (cap={cache_embeddings.capacidad}):")
print(f"  Hits: {cache_embeddings.hits}, Misses: {cache_embeddings.misses}")
print(f"  Hit Rate: {cache_embeddings.hit_rate:.2%}")
print(f"  Cache actual: {list(cache_embeddings.cache.keys())}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 5: collections.ChainMap — CAPAS DE CONFIGURACIÓN              ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 11: CHAINMAP — BÚSQUEDA EN CADENA DE DICCIONARIOS ===")
print("=" * 80)

"""
ChainMap agrupa MÚLTIPLES diccionarios en una sola vista LÓGICA.
Cuando buscas una clave, busca en orden: primero en el primer dict,
luego en el segundo, etc. El primero que tenga la clave, gana.

Esto es EXACTAMENTE el patrón que usan los frameworks de ML para configuración:
1. Argumentos de línea de comandos (máxima prioridad)
2. Variables de entorno
3. Archivo de configuración (config.yaml)
4. Valores por defecto del framework

Con ChainMap, no necesitas fusionar todos los dicts en uno.
Cada capa mantiene su identidad y se puede modificar independientemente.
"""

print("\n--- Sistema de configuración multi-nivel para MLOps ---")

# Capa 4: Defaults del framework (menor prioridad)
defaults = {
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 100,
    "optimizer": "adam",
    "device": "cpu",
    "seed": 42,
}

# Capa 3: Archivo config.yaml del proyecto
config_yaml = {
    "learning_rate": 0.0005,
    "batch_size": 64,
    "device": "cuda",
}

# Capa 2: Variables de entorno
env_vars = {
    "device": "cuda:1",  # El admin de infra forzó la GPU 1
}

# Capa 1: Argumentos CLI del usuario (máxima prioridad)
args_cli = {
    "epochs": 10,  # "Solo quiero un test rápido"
}

# Crear ChainMap con prioridad decreciente
config = ChainMap(args_cli, env_vars, config_yaml, defaults)

print("Configuración resuelta (ChainMap):")
for key in ["learning_rate", "batch_size", "epochs", "optimizer", "device", "seed"]:
    print(f"  {key:<20} = {config[key]}")

print(f"\n  'epochs' viene de: args_cli (= {args_cli.get('epochs', 'N/A')})")
print(f"  'device' viene de: env_vars (= {env_vars.get('device', 'N/A')})")
print(f"  'optimizer' viene de: defaults (= {defaults.get('optimizer', 'N/A')})")


print("\n--- Propiedades útiles de ChainMap ---")

# .maps -> Lista de los dicts internos (modificable)
print(f"\nNúmero de capas: {len(config.maps)}")

# .new_child() -> Crea una nueva capa con máxima prioridad
config_experimento = config.new_child({"learning_rate": 0.01, "experiment_id": "exp_007"})
print(f"Config con capa experimental: LR = {config_experimento['learning_rate']}")
print(f"Config original sin afectar: LR = {config['learning_rate']}")

# .parents -> ChainMap sin la primera capa
print(f"Parents (sin CLI): epochs = {config.parents['epochs']}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: COMPARACIÓN FINAL — CUÁNDO USAR CADA CONTENEDOR ===")
print("=" * 80)

"""
GUÍA DEFINITIVA DE SELECCIÓN PARA INGENIERÍA IA:

╔═══════════════════╦═══════════════════════════════════════════════════════╗
║ CONTENEDOR        ║ CUÁNDO USARLO                                       ║
╠═══════════════════╬═══════════════════════════════════════════════════════╣
║ deque             ║ Cola FIFO/LIFO, ventana deslizante, buffer circular.║
║                   ║ Inserción/extracción por ambos extremos en O(1).    ║
║                   ║ NO para acceso por índice aleatorio (usar list).    ║
╠═══════════════════╬═══════════════════════════════════════════════════════╣
║ Counter           ║ Contar frecuencias. Bag-of-Words NLP.               ║
║                   ║ Top-K elementos. Estimación de costes por tokens.   ║
║                   ║ Aritmética de multiconjuntos (suma, resta, &, |).   ║
╠═══════════════════╬═══════════════════════════════════════════════════════╣
║ defaultdict       ║ Agrupar datos por clave (defaultdict(list)).        ║
║                   ║ Contadores (defaultdict(int)). Grafos (set).        ║
║                   ║ CUIDADO: la lectura crea claves fantasma.           ║
╠═══════════════════╬═══════════════════════════════════════════════════════╣
║ OrderedDict       ║ Cuando necesitas move_to_end() o comparación de    ║
║                   ║ orden. LRU Caches personalizados. En PyTorch,       ║
║                   ║ nn.Module usa OrderedDict para model.state_dict(). ║
╠═══════════════════╬═══════════════════════════════════════════════════════╣
║ ChainMap          ║ Configuración multi-nivel (CLI > env > yaml > def). ║
║                   ║ Scoping de variables (como el LEGB de Python).      ║
║                   ║ Cuando NO quieres fusionar dicts permanentemente.   ║
╚═══════════════════╩═══════════════════════════════════════════════════════╝
"""

# Verificación de tamaños en memoria
print("\n--- Comparación de overhead en memoria ---")

data_base = list(range(1000))

tam_list = sys.getsizeof(data_base)
tam_deque = sys.getsizeof(deque(data_base))
tam_counter = sys.getsizeof(Counter(data_base))
tam_set = sys.getsizeof(set(data_base))

print(f"  list({len(data_base)} items):    {tam_list:>8} bytes")
print(f"  deque({len(data_base)} items):   {tam_deque:>8} bytes")
print(f"  Counter({len(data_base)} items): {tam_counter:>8} bytes")
print(f"  set({len(data_base)} items):     {tam_set:>8} bytes")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 6: EJERCICIOS AVANZADOS INTEGRADORES                          ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 13: BFS EN GRAFOS DE CONOCIMIENTO CON DEQUE ===")
print("=" * 80)

"""
BFS (Breadth-First Search / Búsqueda en anchura) es el algoritmo fundamental
para recorrer grafos. En IA se usa para:
- Explorar grafos de conocimiento (Knowledge Graphs).
- Encontrar la ruta más corta entre dos entidades (ej: en Wikidata).
- Recorrer árboles de decisión o árboles de estrategia de agentes.

BFS requiere una COLA FIFO: el primer nodo descubierto es el primero en 
procesarse. Usar list.pop(0) sería O(N). Con deque.popleft() es O(1).
"""

print("\n--- Grafo de dependencias de frameworks ML ---")

grafo_deps = {
    "PyTorch": ["NumPy", "CUDA", "cuDNN"],
    "TensorFlow": ["NumPy", "CUDA", "Protobuf"],
    "Scikit-Learn": ["NumPy", "SciPy", "Joblib"],
    "HuggingFace": ["PyTorch", "Tokenizers", "SafeTensors"],
    "LangChain": ["HuggingFace", "OpenAI-SDK", "Pydantic"],
    "NumPy": ["BLAS", "LAPACK"],
    "SciPy": ["NumPy", "BLAS"],
    "CUDA": [],
    "cuDNN": ["CUDA"],
    "BLAS": [],
    "LAPACK": ["BLAS"],
    "Protobuf": [],
    "Joblib": [],
    "Tokenizers": [],
    "SafeTensors": [],
    "OpenAI-SDK": [],
    "Pydantic": [],
}

def bfs_dependencias(grafo: dict, inicio: str) -> list:
    """
    Recorre en anchura todas las dependencias transitivas de un paquete.
    Retorna la lista de dependencias en orden de descubrimiento (nivel por nivel).
    """
    visitados = set()
    cola = deque([inicio])  # <-- deque como cola FIFO O(1)
    orden_descubrimiento = []
    
    while cola:
        nodo = cola.popleft()  # O(1) en vez de list.pop(0) O(N)
        
        if nodo in visitados:
            continue
        
        visitados.add(nodo)
        orden_descubrimiento.append(nodo)
        
        # Añadir dependencias hijas a la cola
        for dependencia in grafo.get(nodo, []):
            if dependencia not in visitados:
                cola.append(dependencia)
    
    return orden_descubrimiento

# ¿Qué necesita LangChain transitivamente?
deps_langchain = bfs_dependencias(grafo_deps, "LangChain")
print(f"Dependencias transitivas de LangChain (BFS):")
for i, dep in enumerate(deps_langchain):
    nivel = " " * (i * 2)
    print(f"  {i}: {dep}")

print(f"  Total: {len(deps_langchain)} paquetes necesarios")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: TF-IDF MANUAL CON COUNTER (RANKING DE RELEVANCIA) ===")
print("=" * 80)

"""
TF-IDF (Term Frequency - Inverse Document Frequency) es la métrica 
clásica de relevancia de palabras en un corpus. Antes de los embeddings 
neuronales, era EL estándar para búsqueda y ranking de textos.

TF(t, d) = (frecuencia del término t en el documento d) / (total de términos en d)
IDF(t, D) = log(total de documentos / documentos que contienen t)
TF-IDF(t, d, D) = TF(t, d) × IDF(t, D)

Un Counter por documento nos da el TF. Un Counter global nos da el DF (Document Frequency).
"""

import math

corpus_tfidf = {
    "d1": "el aprendizaje profundo usa redes neuronales profundas",
    "d2": "el procesamiento de lenguaje natural es una rama de la inteligencia artificial",
    "d3": "las redes neuronales convolucionales procesan imágenes con aprendizaje profundo",
    "d4": "los modelos de lenguaje son redes neuronales entrenadas con texto masivo",
}

# Paso 1: Counter por documento (TF)
tf_por_documento = {}
for doc_id, texto in corpus_tfidf.items():
    tokens = texto.lower().split()
    conteo = Counter(tokens)
    total = sum(conteo.values())
    tf_por_documento[doc_id] = {token: freq / total for token, freq in conteo.items()}

# Paso 2: Document Frequency (DF) usando Counter
df = Counter()
for doc_id, texto in corpus_tfidf.items():
    tokens_unicos = set(texto.lower().split())
    df.update(tokens_unicos)

N = len(corpus_tfidf)

# Paso 3: IDF
idf = {token: math.log(N / df_count) for token, df_count in df.items()}

# Paso 4: TF-IDF
print("\nTF-IDF para el documento 'd1':")
tfidf_d1 = {}
for token, tf_val in tf_por_documento["d1"].items():
    tfidf_d1[token] = tf_val * idf[token]

# Ordenar por relevancia
tfidf_ordenado = sorted(tfidf_d1.items(), key=lambda x: x[1], reverse=True)
for token, score in tfidf_ordenado:
    print(f"  {token:<20} TF-IDF: {score:.4f}")

# Buscar término más relevante globalmente
print(f"\nPalabra con mayor IDF (más discriminativa): {max(idf.items(), key=lambda x: x[1])}")
print(f"Palabra con menor IDF (más común): {min(idf.items(), key=lambda x: x[1])}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: PIPELINE INTEGRADOR — TODOS LOS CONTENEDORES JUNTOS ===")
print("=" * 80)

"""
Ejercicio final: construimos un mini sistema de procesamiento de logs de
entrenamiento de un modelo IA que usa TODOS los contenedores de collections.
"""

print("\n--- Sistema de monitorización de entrenamiento ---")

# Simulamos logs de entrenamiento
random.seed(42)
logs_entrenamiento = []
for epoch in range(1, 21):
    for batch in range(1, 51):
        loss = max(0.01, 3.0 - (epoch * 0.15) + random.uniform(-0.1, 0.1))
        gpu = random.choice(["gpu_0", "gpu_1", "gpu_2"])
        status = random.choice(["ok"] * 95 + ["warning"] * 4 + ["error"] * 1)
        logs_entrenamiento.append({
            "epoch": epoch, "batch": batch, "loss": round(loss, 4),
            "gpu": gpu, "status": status
        })

print(f"Total de logs generados: {len(logs_entrenamiento)}")

# 1. deque(maxlen=10): Últimos 10 losses para media móvil
ultimos_losses = deque(maxlen=10)

# 2. Counter: Conteo de estados y uso de GPUs
conteo_estados = Counter()
conteo_gpus = Counter()

# 3. defaultdict(list): Agrupar losses por GPU
losses_por_gpu = defaultdict(list)

# 4. OrderedDict: Cache de los últimos losses por epoch (solo el más reciente por epoch)
cache_epoch = OrderedDict()

# Procesar todos los logs
for log in logs_entrenamiento:
    ultimos_losses.append(log["loss"])
    conteo_estados[log["status"]] += 1
    conteo_gpus[log["gpu"]] += 1
    losses_por_gpu[log["gpu"]].append(log["loss"])
    cache_epoch[log["epoch"]] = log["loss"]  # Se sobreescribe, queda el último batch

# 5. ChainMap: Configuración del sistema de monitorización
config_monitor_defaults = {"alerta_loss_threshold": 2.5, "ventana_media": 10, "formato": "json"}
config_monitor_usuario = {"alerta_loss_threshold": 1.5}
config_monitor = ChainMap(config_monitor_usuario, config_monitor_defaults)

# Reportar resultados
print(f"\n--- Reporte de Monitorización ---")
print(f"  Media móvil (últimos {len(ultimos_losses)} batches): {sum(ultimos_losses)/len(ultimos_losses):.4f}")
print(f"  Estados: {dict(conteo_estados)}")
print(f"  Uso GPUs: {dict(conteo_gpus)}")
print(f"  GPU más usada: {conteo_gpus.most_common(1)[0]}")

print(f"\n  Loss medio por GPU:")
for gpu, losses in sorted(losses_por_gpu.items()):
    media_gpu = sum(losses) / len(losses)
    print(f"    {gpu}: {media_gpu:.4f} ({len(losses)} batches)")

print(f"\n  Últimos 5 epochs en cache: {list(cache_epoch.items())[-5:]}")
print(f"  Threshold de alerta (ChainMap): {config_monitor['alerta_loss_threshold']}")
print(f"  Formato (default): {config_monitor['formato']}")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN ARQUITECTÓNICA ===")
print("=" * 80)

"""
RESUMEN DEFINITIVO DEL MÓDULO COLLECTIONS PARA INGENIERÍA IA:

1. deque(maxlen=N) es la estructura #1 para ventanas deslizantes, rate limiters, 
   y cualquier buffer que necesite O(1) en ambos extremos. Jamás uses list.pop(0).
   BFS en grafos de conocimiento requiere deque como cola FIFO.

2. Counter es Bag-of-Words nativo. most_common() usa heapq internamente (O(N log K)).
   La aritmética de Counters (+, -, &, |) permite operaciones de corpus sin loops.
   TF-IDF se implementa naturalmente combinando Counter + math.log.

3. defaultdict elimina la verificación "if key not in dict" a cambio de un riesgo:
   la LECTURA crea claves. Usa .get() o `in` para consultas seguras.

4. OrderedDict sigue vivo en 2026 por move_to_end() y popitem(last=False),
   que permiten implementar LRU Caches en pocas líneas. PyTorch state_dict()
   lo usa internamente.

5. ChainMap implementa búsqueda en cascada sobre múltiples dicts sin fusionarlos.
   Es el patrón estándar para sistemas de configuración multi-nivel en MLOps.

Con este archivo cerramos el Módulo 02: Estructuras de Datos Nativas.
Has dominado las 5 estructuras fundamentales y sus 5 extensiones especializadas.
Siguiente: Módulo 03 — Algoritmia y Complejidad Computacional.
"""

print("\n FIN DE ARCHIVO 05_collections_profundo.")
print(" El módulo collections ha sido conquistado. Siguiente: Algoritmia y Big-O.")

