# ===========================================================================
# 03_generadores_itertools_y_yield.py
# ===========================================================================
# MÓDULO 04: FUNCIONES, FLUJO Y PROGRAMACIÓN FUNCIONAL
# ARCHIVO 03: Generadores, Itertools, yield from y Programación Lazy
# ===========================================================================
#
# OBJETIVO (1000+ LÍNEAS):
# Los generadores son el ARMA SECRETA de Python para procesar datos
# que no caben en memoria. Son la base de: data pipelines, streaming
# de tokens en LLMs, lectura de datasets masivos, y lazy evaluation.
#
# CONTENIDO:
#   1. Protocolo iterador: __iter__ y __next__.
#   2. Generadores con yield: lazy evaluation.
#   3. Generator expressions vs list comprehensions.
#   4. yield from: delegación de generadores.
#   5. send(), throw(), close(): generadores como coroutines.
#   6. itertools: product, chain, islice, groupby, tee, starmap.
#   7. Pipelines de generadores: procesamiento en streaming.
#   8. Ejercicio: streaming de tokens tipo LLM.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import itertools
import time
import sys
import os
from typing import Iterator, Generator, Iterable, Any
from collections import defaultdict


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 1: PROTOCOLO ITERADOR                                         ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: PROTOCOLO ITERADOR — __iter__ y __next__ ===")
print("=" * 80)

"""
En Python, todo lo que puedes recorrer con 'for' implementa el 
PROTOCOLO ITERADOR:

1. __iter__(): retorna el objeto iterador (generalmente self).
2. __next__(): retorna el siguiente elemento o lanza StopIteration.

Un ITERABLE es algo que tiene __iter__() (listas, strings, dicts...).
Un ITERADOR es algo que tiene __next__() (el objeto que recorre).

for item in coleccion:
    ...
    
Es equivalente a:
    iterador = iter(coleccion)    # llama coleccion.__iter__()
    while True:
        try:
            item = next(iterador)  # llama iterador.__next__()
        except StopIteration:
            break
"""

print("\n--- Iterador manual ---")

class ContadorIterador:
    """Iterador que cuenta de inicio a fin."""
    
    def __init__(self, inicio: int, fin: int):
        self.actual = inicio
        self.fin = fin
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.actual >= self.fin:
            raise StopIteration
        valor = self.actual
        self.actual += 1
        return valor

contador = ContadorIterador(1, 6)
print(f"  Manual: {list(contador)}")

# Un iterador se AGOTA: una sola pasada
contador2 = ContadorIterador(1, 4)
print(f"  1ª pasada: {list(contador2)}")
print(f"  2ª pasada: {list(contador2)}")  # Vacío


print("\n--- Diferencia: iterable vs iterador ---")

lista = [1, 2, 3]
print(f"  lista es iterable: {hasattr(lista, '__iter__')}")
print(f"  lista es iterador: {hasattr(lista, '__next__')}")

iterador = iter(lista)
print(f"  iter(lista) es iterador: {hasattr(iterador, '__next__')}")
print(f"  next(iterador) = {next(iterador)}")
print(f"  next(iterador) = {next(iterador)}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 2: GENERADORES CON YIELD                                      ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 2: GENERADORES — LAZY EVALUATION CON YIELD ===")
print("=" * 80)

"""
Un GENERADOR es una función que usa 'yield' en lugar de 'return'.
Cuando la llamas, NO ejecuta el código: retorna un objeto generador.
Cada vez que llamas next(), ejecuta hasta el siguiente yield.

VENTAJAS SOBRE LISTAS:
- Memoria O(1): solo mantiene UN elemento en memoria.
- Lazy: solo calcula cuando se necesita.
- Composables: se pueden encadenar como pipes Unix.

¿CUÁNDO USAR GENERADORES?
- Datos que no caben en memoria.
- Procesamiento en streaming (tokens, logs, datos de sensores).
- Cuando NO necesitas acceso aleatorio (solo recorrido secuencial).
- Pipelines de transformación de datos.
"""

print("\n--- Generador básico ---")

def contar_hasta(n: int):
    """Generador que cuenta de 1 a n."""
    i = 1
    while i <= n:
        yield i  # Pausa aquí, retorna i, y espera next()
        i += 1

gen = contar_hasta(5)
print(f"  Tipo: {type(gen)}")
print(f"  next: {next(gen)}, {next(gen)}, {next(gen)}")
print(f"  Rest: {list(gen)}")  # Consume el resto


print("\n--- Generador vs Lista: MEMORIA ---")

def rango_lista(n: int) -> list:
    """Crea toda la lista en memoria."""
    return [i for i in range(n)]

def rango_generador(n: int):
    """Genera uno a uno, O(1) memoria."""
    for i in range(n):
        yield i

# Comparar memoria
n = 1_000_000

lista_grande = rango_lista(n)
gen_grande = rango_generador(n)

print(f"  Lista de {n:,}: {sys.getsizeof(lista_grande):,} bytes")
print(f"  Generador:     {sys.getsizeof(gen_grande):,} bytes")
print(f"  Ratio: {sys.getsizeof(lista_grande) / sys.getsizeof(gen_grande):.0f}x más memoria")

del lista_grande


print("\n" + "=" * 80)
print("=== CAPÍTULO 3: GENERATOR EXPRESSIONS ===")
print("=" * 80)

"""
Generator expression = list comprehension CON PARÉNTESIS en vez de [].
- [x**2 for x in range(10)] -> lista (toda en memoria)
- (x**2 for x in range(10)) -> generador (lazy, O(1) memoria)
"""

print("\n--- List comp vs Gen exp ---")

# List comprehension: crea toda la lista
lc = [x**2 for x in range(10)]
print(f"  List comp: {lc}")

# Generator expression: lazy
ge = (x**2 for x in range(10))
print(f"  Gen exp tipo: {type(ge)}")
print(f"  Gen exp list: {list(ge)}")

# Uso directo en funciones (no necesitas paréntesis extra)
total = sum(x**2 for x in range(1_000_000))
print(f"  sum(x² para 1M): {total:,}")

# Esto NUNCA creó una lista de 1M elementos


print("\n" + "=" * 80)
print("=== CAPÍTULO 4: YIELD FROM — DELEGACIÓN DE GENERADORES ===")
print("=" * 80)

"""
'yield from' delega la generación a OTRO iterable/generador.
Es más eficiente y limpio que un for + yield manual.

yield from iterable  ==  for item in iterable: yield item

Pero yield from también PROPAGA send(), throw(), close().
"""

print("\n--- yield from básico ---")

def generar_numeros():
    yield from range(1, 4)

def generar_letras():
    yield from "abc"

def generar_todo():
    yield from generar_numeros()
    yield from generar_letras()

print(f"  yield from: {list(generar_todo())}")


print("\n--- yield from para aplanar listas anidadas ---")

def aplanar(estructura):
    """Aplana recursivamente cualquier estructura anidada."""
    for item in estructura:
        if isinstance(item, (list, tuple)):
            yield from aplanar(item)  # Recursión con yield from
        else:
            yield item

anidada = [1, [2, 3], [4, [5, 6]], [[7, 8], 9]]
print(f"  Anidada:  {anidada}")
print(f"  Aplanada: {list(aplanar(anidada))}")


print("\n--- yield from para datasets multi-shard ---")

def leer_shard(shard_id: int, n_items: int = 5):
    """Simula leer un shard de un dataset distribuido."""
    for i in range(n_items):
        yield {"shard": shard_id, "item": i, "data": f"dato_{shard_id}_{i}"}

def leer_dataset_completo(n_shards: int):
    """Lee todos los shards secuencialmente con yield from."""
    for shard_id in range(n_shards):
        yield from leer_shard(shard_id, n_items=3)

print("\nDataset multi-shard:")
for item in leer_dataset_completo(3):
    print(f"  {item}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 3: GENERADORES AVANZADOS                                      ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 5: SEND(), THROW(), CLOSE() ===")
print("=" * 80)

"""
Los generadores no son solo "productores de datos".
Pueden RECIBIR datos con .send() y MANEJAR excepciones con .throw().

gen.send(valor): envía un valor AL generador.
  El valor se asigna a la variable del yield: valor = yield producido

gen.throw(ExcepcionTipo): inyecta una excepción en el generador.
gen.close(): cierra el generador (lanza GeneratorExit internamente).
"""

print("\n--- send(): generador que recibe datos ---")

def acumulador():
    """Generador que acumula valores enviados con send()."""
    total = 0
    while True:
        valor = yield total  # Produce total, recibe valor via send()
        if valor is None:
            break
        total += valor

acc = acumulador()
next(acc)  # Primer next() para inicializar (llega al primer yield)
print(f"  send(10): {acc.send(10)}")
print(f"  send(20): {acc.send(20)}")
print(f"  send(5):  {acc.send(5)}")


print("\n--- Media móvil con send() ---")

def media_movil(window_size: int):
    """Calcula media móvil de los últimos N valores."""
    ventana = []
    media = 0.0
    
    while True:
        valor = yield media
        if valor is None:
            break
        ventana.append(valor)
        if len(ventana) > window_size:
            ventana.pop(0)
        media = sum(ventana) / len(ventana)

mm = media_movil(3)
next(mm)  # Inicializar

import random
random.seed(42)
for _ in range(8):
    val = random.randint(1, 20)
    media = mm.send(val)
    print(f"  valor={val:>3}, media_movil={media:.1f}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 4: ITERTOOLS — LA CAJA DE HERRAMIENTAS                       ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 6: ITERTOOLS — COMBINATORIA Y STREAMING ===")
print("=" * 80)

"""
itertools es el módulo stdlib para operaciones LAZY sobre iteradores.
TODOS retornan iteradores (no listas). Nunca consumen toda la fuente.
"""

print("\n--- itertools.chain: concatenar iterables ---")

cadena = list(itertools.chain([1, 2, 3], "abc", range(10, 13)))
print(f"  chain: {cadena}")

# chain.from_iterable: cuando los iterables vienen en una lista
listas = [[1, 2], [3, 4], [5, 6]]
plano = list(itertools.chain.from_iterable(listas))
print(f"  chain.from_iterable: {plano}")


print("\n--- itertools.islice: rebanar iteradores ---")

# No puedes hacer gen[5:10] en un generador. islice lo permite.
gen_infinito = itertools.count(0)  # 0, 1, 2, 3, ...
primeros_10 = list(itertools.islice(gen_infinito, 10))
print(f"  islice(count(), 10): {primeros_10}")

# Saltar los primeros 5, tomar los siguientes 5
gen_infinito2 = itertools.count(0)
slice_5_10 = list(itertools.islice(gen_infinito2, 5, 10))
print(f"  islice(count(), 5, 10): {slice_5_10}")


print("\n--- itertools.product: producto cartesiano ---")

# Equivale a for loops anidados
lrs = [0.001, 0.01, 0.1]
batch_sizes = [16, 32, 64]

configs = list(itertools.product(lrs, batch_sizes))
print(f"\n  Grid de hiperparámetros ({len(configs)} combinaciones):")
for lr, bs in configs[:5]:
    print(f"    lr={lr}, batch_size={bs}")
print(f"    ... ({len(configs)} total)")


print("\n--- itertools.combinations y permutations ---")

features = ["emb", "tfidf", "pos", "ner"]

# Combinaciones de 2 features
combos = list(itertools.combinations(features, 2))
print(f"\n  Combinaciones de 2 features ({len(combos)}):")
for c in combos:
    print(f"    {c}")

# Permutaciones (orden importa)
perms = list(itertools.permutations(features, 2))
print(f"  Permutaciones de 2: {len(perms)}")


print("\n--- itertools.groupby: agrupar datos consecutivos ---")

# groupby requiere datos ORDENADOS por la clave de agrupación
resultados = [
    {"modelo": "BERT", "score": 0.91},
    {"modelo": "BERT", "score": 0.89},
    {"modelo": "GPT", "score": 0.95},
    {"modelo": "GPT", "score": 0.93},
    {"modelo": "T5", "score": 0.88},
]

print(f"\n  Agrupado por modelo:")
for modelo, grupo in itertools.groupby(resultados, key=lambda x: x["modelo"]):
    items = list(grupo)
    media = sum(r["score"] for r in items) / len(items)
    print(f"    {modelo}: {len(items)} runs, media={media:.3f}")


print("\n--- itertools.tee: duplicar un iterador ---")

# Un iterador solo se puede recorrer UNA vez.
# tee() crea N copias independientes.
original = iter(range(5))
copia1, copia2 = itertools.tee(original, 2)

print(f"\n  Copia 1: {list(copia1)}")
print(f"  Copia 2: {list(copia2)}")


print("\n--- itertools.starmap: map con múltiples argumentos ---")

from operator import mul, add

pares = [(2, 5), (3, 4), (10, 3)]
productos = list(itertools.starmap(mul, pares))
print(f"\n  starmap(mul, pares): {productos}")


print("\n--- itertools.takewhile / dropwhile ---")

datos_loss = [0.9, 0.7, 0.5, 0.3, 0.4, 0.5, 0.6]

# takewhile: tomar mientras la condición sea True
descendente = list(itertools.takewhile(lambda x: x > 0.3, datos_loss))
print(f"\n  takewhile(>0.3): {descendente}")

# dropwhile: saltar mientras la condición sea True
despues = list(itertools.dropwhile(lambda x: x > 0.4, datos_loss))
print(f"  dropwhile(>0.4): {despues}")


print("\n--- itertools.accumulate: sumas acumuladas ---")

import operator

datos_epoch = [0.9, 0.7, 0.5, 0.3, 0.2, 0.15]
acumulado = list(itertools.accumulate(datos_epoch))
print(f"\n  Loss por epoch: {datos_epoch}")
print(f"  Acumulado:      {[f'{x:.2f}' for x in acumulado]}")

# Producto acumulado
prod_acum = list(itertools.accumulate([2, 3, 4, 5], operator.mul))
print(f"  Producto acum:  {prod_acum}")


print("\n--- itertools.count, cycle, repeat ---")

# count: contador infinito
primeros_5 = list(itertools.islice(itertools.count(10, 0.5), 5))
print(f"\n  count(10, 0.5): {primeros_5}")

# cycle: repite un iterable infinitamente
ciclo = list(itertools.islice(itertools.cycle(["train", "val"]), 6))
print(f"  cycle(['train','val']): {ciclo}")

# repeat: repite un valor N veces
rep = list(itertools.repeat("pad_token", 4))
print(f"  repeat('pad_token', 4): {rep}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 5: PIPELINES DE GENERADORES                                   ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 7: PIPELINE DE GENERADORES — PROCESAMIENTO STREAMING ===")
print("=" * 80)

"""
El patrón MÁS PODEROSO con generadores: encadenarlos como pipes Unix.
Cada generador procesa un elemento a la vez y lo pasa al siguiente.

datos_crudos | limpiar | tokenizar | filtrar | batch

Ventajas:
- Memoria O(1): solo un elemento en memoria a la vez.
- Composable: añadir/quitar pasos es trivial.
- Lazy: no procesa datos que no se necesitan.
"""

print("\n--- Pipeline de procesamiento de texto ---")

def leer_textos(textos: list[str]):
    """Fuente: genera textos uno a uno."""
    for texto in textos:
        yield texto

def limpiar_texto(textos):
    """Paso 1: limpieza básica."""
    for texto in textos:
        yield texto.strip().lower()

def tokenizar(textos):
    """Paso 2: tokenización simple (split por espacios)."""
    for texto in textos:
        yield texto.split()

def filtrar_cortos(token_lists, min_tokens: int = 3):
    """Paso 3: filtrar textos con menos de min_tokens."""
    for tokens in token_lists:
        if len(tokens) >= min_tokens:
            yield tokens

def agrupar_en_batches(items, batch_size: int = 2):
    """Paso 4: agrupar en batches."""
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

# Datos de ejemplo
corpus = [
    "  El transformer es un modelo revolucionario  ",
    "NLP avanzado",
    "  Machine Learning con PYTHON para IA ",
    "OK",
    "  Los embeddings capturan semántica del lenguaje  ",
    "  Deep learning con PyTorch  ",
]

# Montar pipeline (todo lazy, nada se ejecuta aún)
pipeline = agrupar_en_batches(
    filtrar_cortos(
        tokenizar(
            limpiar_texto(
                leer_textos(corpus)
            )
        ), min_tokens=3
    ), batch_size=2
)

print("Procesando corpus en streaming:")
for i, batch in enumerate(pipeline):
    print(f"  Batch {i}: {batch}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: INFINITE GENERATORS — STREAMS INFINITOS ===")
print("=" * 80)

"""
Los generadores pueden producir datos INFINITAMENTE.
Solo se consumen lo que se necesita (lazy evaluation).
"""

print("\n--- Generador de datos de entrenamiento infinito ---")

def data_augmentation_stream(datos_base: list, seed: int = 42):
    """Genera datos aumentados infinitamente con variaciones."""
    import random
    rng = random.Random(seed)
    
    while True:
        dato = rng.choice(datos_base)
        # Simular augmentation
        ruido = rng.gauss(0, 0.01)
        yield [x + ruido for x in dato]

datos = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
stream = data_augmentation_stream(datos)

# Tomar solo 5 muestras del stream infinito
print("5 muestras de stream infinito:")
for muestra in itertools.islice(stream, 5):
    print(f"  {[f'{x:.3f}' for x in muestra]}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 9: EJERCICIO — STREAMING DE TOKENS TIPO LLM ===")
print("=" * 80)

"""
Implementar un simulador de streaming de tokens como lo hacen
las APIs de LLMs (OpenAI, Anthropic).
"""

print("\n--- Token Streamer ---")

def token_streamer(texto: str, delay: float = 0.02):
    """
    Simula streaming token a token como un LLM.
    Cada yield produce un token con metadata.
    """
    tokens = texto.split()
    for i, token in enumerate(tokens):
        time.sleep(delay)  # Simular latencia de inferencia
        yield {
            "token": token,
            "index": i,
            "is_last": i == len(tokens) - 1,
            "logprob": -0.5 * (i + 1) / len(tokens)  # Simulado
        }

def formatear_stream(token_stream):
    """Formatea el stream para display progresivo."""
    buffer = []
    for chunk in token_stream:
        buffer.append(chunk["token"])
        yield " ".join(buffer)

# Simular streaming
respuesta = "El modelo transformer revolucionó el procesamiento del lenguaje natural"
print("Streaming de respuesta:")
for texto_parcial in formatear_stream(token_streamer(respuesta, delay=0.01)):
    print(f"\r  > {texto_parcial}", end="", flush=True)
print(" ✓")


print("\n--- Batch Iterator para datasets ---")

def batch_iterator(dataset: list, batch_size: int, shuffle: bool = False):
    """
    Iterador de batches para training loops.
    Genera (batch_data, batch_indices) por epoch.
    """
    import random
    indices = list(range(len(dataset)))
    
    if shuffle:
        random.shuffle(indices)
    
    for start in range(0, len(dataset), batch_size):
        batch_idx = indices[start:start + batch_size]
        batch_data = [dataset[i] for i in batch_idx]
        yield batch_data, batch_idx

dataset = list(range(10))
print(f"\nDataset: {dataset}")
print("Batches (size=3, shuffle=False):")
for batch, idx in batch_iterator(dataset, batch_size=3):
    print(f"  Batch {idx}: {batch}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: TABLA DE ITERTOOLS COMPLETA ===")
print("=" * 80)

print("""
╔══════════════════════════════════════════════════════════════════════╗
║ FUNCIÓN           ║ DESCRIPCIÓN                      ║ EJEMPLO     ║
╠══════════════════════════════════════════════════════════════════════╣
║ chain(a, b)       ║ Concatena iterables              ║ [1,2,3,4]   ║
║ chain.from_iter() ║ Concatena lista de iterables     ║ [1,2,3,4]   ║
║ islice(it, n)     ║ Rebana un iterador               ║ it[:n]      ║
║ count(n, step)    ║ Contador infinito                ║ n, n+1, ... ║
║ cycle(it)         ║ Repite infinitamente             ║ a,b,a,b,... ║
║ repeat(x, n)      ║ Repite x n veces                ║ x, x, x     ║
║ product(a, b)     ║ Producto cartesiano              ║ (a1,b1)...  ║
║ combinations(n,r) ║ Combinaciones sin repetición     ║ C(n,r)      ║
║ permutations(n,r) ║ Permutaciones                    ║ P(n,r)      ║
║ groupby(it, key)  ║ Agrupa consecutivos              ║ {k: [v]}    ║
║ tee(it, n)        ║ Duplica un iterador              ║ it → n its  ║
║ starmap(f, it)    ║ map con múltiples args            ║ f(*args)    ║
║ takewhile(p, it)  ║ Tomar mientras predicate=True    ║ [..break]   ║
║ dropwhile(p, it)  ║ Saltar mientras predicate=True   ║ [skip..]    ║
║ accumulate(it)    ║ Sumas acumuladas                 ║ [1,3,6,10]  ║
║ zip_longest(a, b) ║ zip con relleno                  ║ fillvalue   ║
║ compress(d, s)    ║ Filtrar con máscara              ║ d[s==True]  ║
║ filterfalse(p,it) ║ filter invertido                 ║ not pred    ║
╚══════════════════════════════════════════════════════════════════════╝
""")


print("\n" + "=" * 80)
print("=== CAPITULO 11: GENERADORES COMO CONTEXT MANAGERS ===")
print("=" * 80)

"""
contextlib.contextmanager transforma un generador en un context manager
(with statement). El yield divide el setup del teardown.

Antes del yield: __enter__ (setup)
Despues del yield: __exit__ (teardown)
"""

from contextlib import contextmanager

@contextmanager
def timer_context(nombre: str = "bloque"):
    """Context manager que mide tiempo de un bloque de codigo."""
    inicio = time.perf_counter()
    yield  # Aqui se ejecuta el bloque 'with'
    elapsed = time.perf_counter() - inicio
    print(f"  Timer {nombre}: {elapsed*1000:.2f} ms")

print("\n--- Timer como context manager ---")
with timer_context("procesamiento"):
    total = sum(i**2 for i in range(500_000))
    print(f"  Total: {total}")


@contextmanager
def abrir_dataset(nombre: str):
    """Simula apertura/cierre de un dataset con cleanup."""
    print(f"  Abriendo dataset '{nombre}'...")
    datos = [i * 0.1 for i in range(100)]  # Mock
    try:
        yield datos
    finally:
        print(f"  Cerrando dataset '{nombre}'. Recursos liberados.")

print("\n--- Dataset context manager ---")
with abrir_dataset("train.csv") as datos:
    print(f"  Procesando {len(datos)} registros")
    media = sum(datos) / len(datos)
    print(f"  Media: {media:.2f}")


@contextmanager
def capturar_metricas():
    """Context manager que captura metricas de un bloque."""
    import tracemalloc
    tracemalloc.start()
    inicio = time.perf_counter()
    metricas = {}

    yield metricas  # El bloque puede escribir en metricas

    elapsed = time.perf_counter() - inicio
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    metricas["tiempo_ms"] = elapsed * 1000
    metricas["memoria_kb"] = peak / 1024
    print(f"  Tiempo: {metricas['tiempo_ms']:.1f}ms, "
          f"Memoria pico: {metricas['memoria_kb']:.1f}KB")

print("\n--- Capturar metricas ---")
with capturar_metricas() as m:
    resultado = [x**2 for x in range(100_000)]
    m["n_items"] = len(resultado)

print(f"  Metricas completas: {m}")


print("\n" + "=" * 80)
print("=== CAPITULO 12: PATRONES AVANZADOS CON ITERTOOLS ===")
print("=" * 80)

"""
Patrones comunes que combinan multiples funciones de itertools.
"""

print("\n--- Sliding window (ventana deslizante) ---")

def sliding_window(iterable, n):
    """Ventana deslizante de tamano n sobre un iterable."""
    it = iter(iterable)
    window = []
    for _ in range(n):
        window.append(next(it))
    yield tuple(window)

    for item in it:
        window.pop(0)
        window.append(item)
        yield tuple(window)

datos_sw = [10, 20, 30, 40, 50, 60, 70]
print(f"  Datos: {datos_sw}")
print(f"  Ventanas de 3: {list(sliding_window(datos_sw, 3))}")


print("\n--- Chunking: dividir en bloques ---")

def chunked(iterable, size):
    """Divide un iterable en chunks de tamano fijo."""
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk

datos_ch = list(range(17))
for chunk in chunked(datos_ch, 5):
    print(f"  Chunk: {chunk}")


print("\n--- Roundrobin: distribuir entre workers ---")

def roundrobin(*iterables):
    """Distribuye elementos round-robin entre iterables."""
    iterators = [iter(it) for it in iterables]
    while iterators:
        for it in iterators[:]:
            try:
                yield next(it)
            except StopIteration:
                iterators.remove(it)

r = list(roundrobin("ABC", "D", "EF"))
print(f"\n  roundrobin('ABC', 'D', 'EF') = {r}")


print("\n--- Pairwise: pares consecutivos ---")

def pairwise_custom(iterable):
    """Genera pares consecutivos: (a,b), (b,c), (c,d), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

datos_pw = [10, 20, 15, 30, 25]
print(f"  Datos: {datos_pw}")
print(f"  Diferencias: {[b - a for a, b in pairwise_custom(datos_pw)]}")


print("\n--- Unique: eliminar duplicados manteniendo orden ---")

def unique(iterable, key=None):
    """Elimina duplicados manteniendo el orden de primera aparicion."""
    seen = set()
    for item in iterable:
        k = key(item) if key else item
        if k not in seen:
            seen.add(k)
            yield item

datos_dup = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(f"\n  Original: {datos_dup}")
print(f"  Unicos:   {list(unique(datos_dup))}")


print("\n" + "=" * 80)
print("=== CAPITULO 13: BENCHMARK GENERADOR VS LISTA ===")
print("=" * 80)

"""
Demostracion practica del ahorro de memoria con generadores.
"""

print("\n--- Memoria: procesamiento de 2M de registros ---")

def procesar_como_lista(n):
    """Crea TODA la lista, luego filtra, luego suma."""
    datos = [i * 0.5 for i in range(n)]
    filtrados = [x for x in datos if x > n * 0.25]
    return sum(filtrados)

def procesar_como_generador(n):
    """Genera, filtra y suma en streaming. O(1) memoria."""
    datos = (i * 0.5 for i in range(n))
    filtrados = (x for x in datos if x > n * 0.25)
    return sum(filtrados)

n_bench = 2_000_000

import tracemalloc

tracemalloc.start()
r1 = procesar_como_lista(n_bench)
_, peak_lista = tracemalloc.get_traced_memory()
tracemalloc.stop()

tracemalloc.start()
r2 = procesar_como_generador(n_bench)
_, peak_gen = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"  Lista:     pico = {peak_lista/1024/1024:.1f} MB, resultado = {r1:.0f}")
print(f"  Generador: pico = {peak_gen/1024/1024:.1f} MB, resultado = {r2:.0f}")
if peak_gen > 0:
    print(f"  Ahorro: {peak_lista/peak_gen:.0f}x menos memoria")


print("\n" + "=" * 80)
print("=== CAPITULO 14: ETL PIPELINE COMPLETO ===")
print("=" * 80)

"""
Pipeline ETL (Extract, Transform, Load) completamente lazy
usando generadores encadenados.
"""

print("\n--- ETL Pipeline ---")

import json

def extract_registros(n: int, seed: int = 42):
    """EXTRACT: genera registros simulados de un dataset."""
    rng = random.Random(seed)
    categorias = ["NLP", "Vision", "Audio", "Tabular"]

    for i in range(n):
        yield {
            "id": i,
            "score": rng.gauss(0.7, 0.15),
            "categoria": rng.choice(categorias),
            "procesado": rng.random() > 0.1,
            "timestamp": f"2024-01-{rng.randint(1,31):02d}",
        }

def transform_filtrar(registros, min_score=0.5):
    """TRANSFORM: filtrar registros con score bajo."""
    for r in registros:
        if r["score"] >= min_score and r["procesado"]:
            yield r

def transform_enriquecer(registros):
    """TRANSFORM: anadir campos calculados."""
    for r in registros:
        r["score_normalizado"] = min(1.0, max(0.0, r["score"]))
        if r["score"] > 0.85:
            r["tier"] = "gold"
        elif r["score"] > 0.7:
            r["tier"] = "silver"
        else:
            r["tier"] = "bronze"
        yield r

def transform_agrupar_stats(registros):
    """TRANSFORM: acumular stats por categoria en streaming."""
    stats = defaultdict(lambda: {"count": 0, "total_score": 0})

    for r in registros:
        cat = r["categoria"]
        stats[cat]["count"] += 1
        stats[cat]["total_score"] += r["score"]
        yield r

    # Al final, imprimir resumen
    print("\n  Estadisticas por categoria:")
    for cat, s in sorted(stats.items()):
        media = s["total_score"] / s["count"] if s["count"] else 0
        print(f"    {cat}: {s['count']} registros, score medio = {media:.3f}")

def load_contar(registros):
    """LOAD: contar y mostrar resumen."""
    total = 0
    por_tier = defaultdict(int)

    for r in registros:
        total += 1
        por_tier[r.get("tier", "unknown")] += 1

    return total, dict(por_tier)

# Montar pipeline ETL completo (todo lazy)
etl_pipeline = transform_agrupar_stats(
    transform_enriquecer(
        transform_filtrar(
            extract_registros(10_000),
            min_score=0.5
        )
    )
)

total, tiers = load_contar(etl_pipeline)
print(f"\n  Total procesados: {total}")
print(f"  Por tier: {tiers}")
print(f"  Todo procesado en streaming (O(1) memoria)")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE GENERADORES E ITERTOOLS PARA INGENIERIA IA:

1. Protocolo iterador: __iter__() y __next__(). Todo 'for' lo usa.

2. Generadores (yield): funciones lazy, O(1) memoria.

3. Generator expressions: (expr for x in it) -- lazy alternativo.

4. yield from: delega a otro generador. Limpio para recursion.

5. send(): generadores bidireccionales. Media movil, acumuladores.

6. itertools: chain, islice, product, groupby, tee, accumulate...

7. Pipelines de generadores: datos | limpiar | tokenizar | batch.

8. Context managers con @contextmanager: setup/teardown con yield.

9. Patrones: sliding window, chunking, roundrobin, pairwise, unique.

10. Memoria: generadores usan ~100x menos memoria que listas.

11. ETL streaming: extract | transform | load, todo lazy.

FIN DEL MODULO 04: FUNCIONES, FLUJO Y PROGRAMACION FUNCIONAL.
"""

print("\n FIN DE ARCHIVO 03_generadores_itertools_y_yield.")
print(" El paradigma lazy de Python ha sido dominado.")
print(" Siguiente modulo: 05_POO_Y_Diseno_Profesional.")

