# ===========================================================================
# 05_programacion_dinamica_y_lru_cache.py
# ===========================================================================
# MÓDULO 03: ALGORITMIA Y COMPLEJIDAD COMPUTACIONAL
# ARCHIVO 05: Programación Dinámica, Memoización y lru_cache
# ===========================================================================
#
# OBJETIVO (1000+ LÍNEAS):
# Entender la programación dinámica NO como un truco académico sino como 
# una TÉCNICA DE INGENIERÍA que aparece constantemente en ML:
# - Algoritmo de Viterbi (HMM, CRF).
# - Beam search (generación de texto).
# - Edit distance (NLP).
# - Dynamic Time Warping (series temporales).
# - Knapsack (selección de features).
#
# CONTENIDO:
#   1. Qué es programación dinámica (overlapping subproblems + optimal substructure).
#   2. Top-down (memoización con lru_cache) vs Bottom-up (tabulación).
#   3. Fibonacci: el Hello World de DP.
#   4. Climbing stairs, coin change, longest common subsequence.
#   5. Edit distance (Levenshtein): distancia entre strings para NLP.
#   6. Knapsack: selección óptima con restricciones.
#   7. functools.lru_cache y cache: la memoización nativa de Python.
#   8. Ejercicio: spell checker con edit distance.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import time
import sys
from functools import lru_cache, cache
from typing import Optional


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 1: ¿QUÉ ES PROGRAMACIÓN DINÁMICA?                            ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: PROGRAMACIÓN DINÁMICA — LA TÉCNICA MÁS PODEROSA ===")
print("=" * 80)

"""
La Programación Dinámica (DP) es una técnica para resolver problemas que:
1. Tienen SUBPROBLEMAS SOLAPADOS: el mismo cálculo se repite muchas veces.
2. Tienen SUBESTRUCTURA ÓPTIMA: la solución óptima se construye a partir 
   de soluciones óptimas de subproblemas.

Si un problema tiene ambas propiedades, DP puede reducir la complejidad
de EXPONENCIAL a POLINÓMICA.

DOS ENFOQUES:
1. TOP-DOWN (Memoización):
   - Recursión normal + caché de resultados.
   - Empiezas por el problema grande y bajas.
   - En Python: @lru_cache o @cache.
   - Más natural de implementar.
   - Riesgo de stack overflow con N muy grande.

2. BOTTOM-UP (Tabulación):
   - Iterativo con tabla (array/dict).
   - Empiezas por los casos base y subes.
   - Sin recursión, sin riesgo de stack overflow.
   - A veces se puede optimizar el espacio.

REGLA DE ORO:
"¿Puedo descomponer este problema en subproblemas más pequeños 
que se repiten?" Si sí -> DP.
"""


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: FIBONACCI — EL EJEMPLO CANÓNICO ===")
print("=" * 80)

"""
fib(N) = fib(N-1) + fib(N-2)
Base: fib(0) = 0, fib(1) = 1

SIN DP: O(2^N) — se recalculan los mismos subproblemas exponencialmente.
CON DP: O(N) — cada subproblema se calcula UNA sola vez.
"""

print("\n--- Fibonacci RECURSIVO (O(2^N)) ---")

def fib_recursivo(n: int) -> int:
    if n <= 1:
        return n
    return fib_recursivo(n - 1) + fib_recursivo(n - 2)

# Contar llamadas
call_count = 0
def fib_recursivo_count(n: int) -> int:
    global call_count
    call_count += 1
    if n <= 1:
        return n
    return fib_recursivo_count(n - 1) + fib_recursivo_count(n - 2)

for n in [10, 20, 25, 30]:
    call_count = 0
    inicio = time.perf_counter()
    result = fib_recursivo_count(n)
    t = time.perf_counter() - inicio
    print(f"  fib({n:>2}) = {result:>10,}  llamadas: {call_count:>12,}  tiempo: {t*1000:.2f} ms")


print("\n--- Fibonacci TOP-DOWN con @lru_cache (O(N)) ---")

@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

for n in [10, 50, 100, 500, 1000]:
    fib_memo.cache_clear()
    inicio = time.perf_counter()
    result = fib_memo(n)
    t = time.perf_counter() - inicio
    cache_info = fib_memo.cache_info()
    print(f"  fib({n:>4}) = {str(result)[:15]:>15}...  "
          f"hits={cache_info.hits:>6}  misses={cache_info.misses:>6}  "
          f"tiempo: {t*1000:.4f} ms")


print("\n--- Fibonacci BOTTOM-UP con tabulación (O(N)) ---")

def fib_tabla(n: int) -> int:
    """Bottom-up: sin recursión, sin riesgo de stack overflow."""
    if n <= 1:
        return n
    
    tabla = [0] * (n + 1)
    tabla[1] = 1
    
    for i in range(2, n + 1):
        tabla[i] = tabla[i - 1] + tabla[i - 2]
    
    return tabla[n]

# Con N muy grande, bottom-up no tiene límite de recursión
for n in [10, 100, 1000, 10000]:
    inicio = time.perf_counter()
    result = fib_tabla(n)
    t = time.perf_counter() - inicio
    print(f"  fib_tabla({n:>5}) = {str(result)[:15]:>15}...  tiempo: {t*1000:.4f} ms")


print("\n--- Fibonacci ESPACIO OPTIMIZADO O(1) ---")

def fib_optimo(n: int) -> int:
    """O(N) tiempo, O(1) espacio: solo necesitamos los 2 últimos valores."""
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    
    return prev1

print(f"\n  fib_optimo(1000): {str(fib_optimo(1000))[:20]}... (O(1) espacio)")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 2: PROBLEMAS CLÁSICOS DE DP                                   ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 3: CLIMBING STAIRS (ESCALERAS) ===")
print("=" * 80)

"""
Tienes N escalones. Puedes subir 1 o 2 escalones a la vez.
¿De cuántas formas puedes llegar al escalón N?

Es IDÉNTICO a Fibonacci: stairs(N) = stairs(N-1) + stairs(N-2).
Pero la INTERPRETACIÓN es diferente:
- stairs(N-1): las formas de llegar a N-1 (luego subes 1).
- stairs(N-2): las formas de llegar a N-2 (luego subes 2).
"""

@cache
def climbing_stairs(n: int) -> int:
    if n <= 2:
        return n
    return climbing_stairs(n - 1) + climbing_stairs(n - 2)

for n in [5, 10, 20, 50]:
    print(f"  Formas de subir {n:>2} escalones: {climbing_stairs(n):>15,}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 4: COIN CHANGE (CAMBIO DE MONEDAS) ===")
print("=" * 80)

"""
Dado un conjunto de monedas y un monto objetivo,
¿cuál es el MÍNIMO número de monedas para llegar al monto?

Ejemplo: monedas = [1, 5, 10, 25], monto = 36
Solución: 25 + 10 + 1 = 3 monedas.

Subproblema: para cada moneda c, si la uso, necesito
cambio_minimo(monto - c) + 1 monedas. Tomo el mínimo.

Complejidad: O(monto × len(monedas)).
"""

print("\n--- Coin Change: top-down con memoización ---")

def coin_change_memo(monedas: list, monto: int) -> int:
    """Mínimo número de monedas para llegar a monto."""
    
    @cache
    def dp(restante: int) -> int:
        if restante == 0:
            return 0
        if restante < 0:
            return float('inf')
        
        minimo = float('inf')
        for moneda in monedas:
            resultado = dp(restante - moneda)
            if resultado != float('inf'):
                minimo = min(minimo, resultado + 1)
        
        return minimo
    
    resultado = dp(monto)
    return resultado if resultado != float('inf') else -1

print(f"  Monedas [1,5,10,25], monto=36: {coin_change_memo([1,5,10,25], 36)} monedas")
print(f"  Monedas [1,5,10,25], monto=30: {coin_change_memo([1,5,10,25], 30)} monedas")
print(f"  Monedas [2], monto=3: {coin_change_memo([2], 3)} (imposible)")


print("\n--- Coin Change: bottom-up ---")

def coin_change_tabla(monedas: list, monto: int) -> int:
    """Bottom-up. O(monto × len(monedas)) tiempo, O(monto) espacio."""
    dp = [float('inf')] * (monto + 1)
    dp[0] = 0
    
    for i in range(1, monto + 1):
        for moneda in monedas:
            if moneda <= i and dp[i - moneda] != float('inf'):
                dp[i] = min(dp[i], dp[i - moneda] + 1)
    
    return dp[monto] if dp[monto] != float('inf') else -1

print(f"\n  Bottom-up [1,5,10,25], monto=36: {coin_change_tabla([1,5,10,25], 36)}")

# Benchmark
inicio = time.perf_counter()
coin_change_tabla([1, 5, 10, 25, 50], 9999)
t = time.perf_counter() - inicio
print(f"  [1,5,10,25,50], monto=9999: tiempo = {t*1000:.2f} ms")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: EDIT DISTANCE (LEVENSHTEIN) — CLAVE EN NLP ===")
print("=" * 80)

"""
La DISTANCIA DE EDICIÓN entre dos strings es el mínimo número de 
operaciones para transformar un string en otro:
- Insertar un carácter.
- Eliminar un carácter.
- Reemplazar un carácter.

EN NLP, ESTO ES FUNDAMENTAL:
- Spell checking: ¿cuál es la palabra más cercana a un typo?
- Fuzzy matching: unir registros con nombres similares.
- Evaluación de modelos de traducción (BLEU usa conceptos similares).
- Tokenización: alinear tokens con texto original.

Complejidad: O(N × M) donde N, M = longitudes de los strings.
"""

print("\n--- Edit Distance implementado ---")

def edit_distance(s1: str, s2: str) -> int:
    """
    Calcula la distancia de Levenshtein entre s1 y s2.
    Bottom-up DP. O(N × M) tiempo, O(N × M) espacio.
    """
    n, m = len(s1), len(s2)
    
    # Tabla de (n+1) × (m+1)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Casos base
    for i in range(n + 1):
        dp[i][0] = i  # Eliminar todos los caracteres de s1
    for j in range(m + 1):
        dp[0][j] = j  # Insertar todos los caracteres de s2
    
    # Llenar tabla
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Caracteres iguales, sin coste
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],     # Eliminar
                    dp[i][j - 1],     # Insertar
                    dp[i - 1][j - 1]  # Reemplazar
                )
    
    return dp[n][m]

# Ejemplos
pares = [
    ("kitten", "sitting"),
    ("python", "pyhton"),
    ("machine", "learning"),
    ("BERT", "bert"),
    ("transformers", "transformer"),
]

for s1, s2 in pares:
    d = edit_distance(s1, s2)
    print(f"  dist('{s1}', '{s2}') = {d}")


print("\n--- Edit Distance optimizado en espacio O(M) ---")

def edit_distance_optimizado(s1: str, s2: str) -> int:
    """O(N × M) tiempo, O(M) espacio: solo necesitamos la fila anterior."""
    n, m = len(s1), len(s2)
    
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    
    for i in range(1, n + 1):
        curr[0] = i
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev, curr = curr, prev
    
    return prev[m]

# Benchmark
s1_bench = "inteligencia artificial para machine learning con python"
s2_bench = "inteligencia artificiel para machne learning en python"

inicio = time.perf_counter()
d1 = edit_distance(s1_bench, s2_bench)
t1 = time.perf_counter() - inicio

inicio = time.perf_counter()
d2 = edit_distance_optimizado(s1_bench, s2_bench)
t2 = time.perf_counter() - inicio

print(f"\n  Distancia: {d1} (ambos métodos: {d1 == d2})")
print(f"  O(N×M) espacio: {t1*1000:.2f} ms")
print(f"  O(M) espacio:   {t2*1000:.2f} ms")


print("\n" + "=" * 80)
print("=== CAPÍTULO 6: LONGEST COMMON SUBSEQUENCE (LCS) ===")
print("=" * 80)

"""
LCS: la subsecuencia más larga que aparece en AMBOS strings
(no necesariamente contigua).

Ejemplo: LCS("ABCBDAB", "BDCABA") = "BCBA" (longitud 4).

EN NLP:
- Comparar dos textos para detectar plagio.
- Diff de código (git diff usa variantes de LCS).
- Evaluación de resúmenes (ROUGE-L usa LCS).
"""

print("\n--- LCS implementado ---")

def lcs(s1: str, s2: str) -> str:
    """Retorna la LCS de dos strings. O(N × M)."""
    n, m = len(s1), len(s2)
    
    # Tabla de longitudes
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Reconstruir la LCS
    result = []
    i, j = n, m
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(result))

print(f"  LCS('ABCBDAB', 'BDCABA') = '{lcs('ABCBDAB', 'BDCABA')}'")
print(f"  LCS('python', 'pytorch') = '{lcs('python', 'pytorch')}'")
print(f"  LCS('machine', 'learning') = '{lcs('machine', 'learning')}'")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 3: LRU_CACHE EN PROFUNDIDAD                                   ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 7: FUNCTOOLS.LRU_CACHE — MEMOIZACIÓN NATIVA ===")
print("=" * 80)

"""
@lru_cache es un DECORADOR que cachea los resultados de una función.
LRU = Least Recently Used: cuando la caché se llena, elimina el 
elemento usado menos recientemente.

PARÁMETROS:
- maxsize=128: tamaño máximo de la caché (por defecto 128).
  - maxsize=None: caché ilimitada (crece sin límite).
  - maxsize=0: sin caché (desactiva la memoización).
- typed=False: si True, distingue entre int y float (1 ≠ 1.0).

MÉTODOS DEL DECORADOR:
- func.cache_info(): estadísticas de hits/misses/tamaño.
- func.cache_clear(): limpia la caché.

RESTRICCIONES:
- Los argumentos deben ser HASHABLES (no puedes pasar listas/dicts).
- Funciona con tuplas, strings, ints, floats.

PYTHON 3.9+: @cache es equivalente a @lru_cache(maxsize=None).
"""

print("\n--- lru_cache con maxsize limitado ---")

@lru_cache(maxsize=4)
def consulta_costosa(query: str) -> str:
    """Simula una función costosa (ej: llamada a API, DB query)."""
    time.sleep(0.01)  # Simular latencia
    return f"resultado_para_{query}"

# Primera ronda: todo son misses
for q in ["BERT", "GPT", "T5", "RoBERTa"]:
    inicio = time.perf_counter()
    consulta_costosa(q)
    t = time.perf_counter() - inicio
    print(f"  '{q}': {t*1000:.1f} ms", end="")
    print(f" (MISS)" if t > 5 else f" (HIT)")

# Segunda ronda: todo son hits
for q in ["BERT", "GPT", "T5", "RoBERTa"]:
    inicio = time.perf_counter()
    consulta_costosa(q)
    t = time.perf_counter() - inicio
    print(f"  '{q}': {t*1000:.1f} ms (HIT)")

# Insertar uno nuevo: expulsa al LRU
consulta_costosa("LLaMA")
print(f"\n  Tras insertar 'LLaMA': {consulta_costosa.cache_info()}")

# BERT fue el LRU, se expulsó
inicio = time.perf_counter()
consulta_costosa("BERT")
t = time.perf_counter() - inicio
print(f"  'BERT' de nuevo: {t*1000:.1f} ms (fue EXPULSADO, es MISS)")

consulta_costosa.cache_clear()


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: PATRONES AVANZADOS CON LRU_CACHE ===")
print("=" * 80)

"""
Patrones comunes en producción con lru_cache.
"""

print("\n--- Patrón 1: Cachear cómputos de features ---")

@lru_cache(maxsize=1024)
def extraer_features(texto: str) -> tuple:
    """
    Simula la extracción de features de un texto.
    En producción, esto podría ser un embedding de BERT.
    Cacheamos porque el mismo texto produce las mismas features.
    
    NOTA: retornamos TUPLA porque las listas no son hashables.
    """
    # Simulación simple
    palabras = texto.lower().split()
    return tuple(len(p) for p in palabras)

textos = ["el gato negro", "el perro blanco", "el gato negro", "la casa azul"]
for t in textos:
    features = extraer_features(t)
    print(f"  '{t}' -> {features}")

print(f"  Cache: {extraer_features.cache_info()}")
print(f"  'el gato negro' se calculó UNA vez, la segunda fue hit.")

extraer_features.cache_clear()


print("\n--- Patrón 2: lru_cache con argumentos complejos ---")

"""
lru_cache requiere argumentos hashables. ¿Qué hacer con listas/dicts?
Solución: convertir a TUPLA o FROZENSET antes de llamar.
"""

@lru_cache(maxsize=128)
def procesar_config(config_tuple: tuple) -> dict:
    """Procesa una configuración (recibida como tupla de pares key-value)."""
    config = dict(config_tuple)
    return {"procesado": True, "n_params": len(config), **config}

# Convertir dict a tupla de items para hacerlo hashable
config = {"lr": 0.001, "epochs": 10, "batch_size": 32}
config_hashable = tuple(sorted(config.items()))

resultado = procesar_config(config_hashable)
print(f"\n  Config: {config}")
print(f"  Hashable: {config_hashable}")
print(f"  Resultado: {resultado}")

procesar_config.cache_clear()


print("\n--- Patrón 3: Invalidación selectiva (wrapper) ---")

class CachedComputer:
    """
    Wrapper que permite invalidar entradas específicas del caché.
    lru_cache nativo solo permite cache_clear() (todo o nada).
    """
    
    def __init__(self, maxsize=128):
        self._cache = {}
        self._maxsize = maxsize
    
    def compute(self, key: str) -> float:
        if key in self._cache:
            return self._cache[key]
        
        # Cómputo costoso simulado
        result = hash(key) % 1000 / 1000
        
        if len(self._cache) >= self._maxsize:
            # Eliminar la entrada más antigua (FIFO simple)
            oldest = next(iter(self._cache))
            del self._cache[oldest]
        
        self._cache[key] = result
        return result
    
    def invalidate(self, key: str):
        """Invalida una entrada específica."""
        self._cache.pop(key, None)
    
    def stats(self):
        return f"Cache size: {len(self._cache)}/{self._maxsize}"

cc = CachedComputer(maxsize=5)
for k in ["a", "b", "c", "a", "d", "e", "f"]:
    cc.compute(k)
print(f"\n  {cc.stats()}")
cc.invalidate("b")
print(f"  Tras invalidar 'b': {cc.stats()}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 4: PROBLEMAS DP APLICADOS A ML                                ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 9: KNAPSACK — SELECCIÓN ÓPTIMA CON RESTRICCIONES ===")
print("=" * 80)

"""
Problema de la mochila (0/1 Knapsack):
Tienes N items, cada uno con peso y valor.
Tienes una mochila con capacidad máxima W.
Maximiza el valor total sin exceder W.

EN ML (Feature Selection como Knapsack):
- Items = features candidatas.
- Valor = importancia/información de la feature.
- Peso = coste computacional de calcular la feature.
- Capacidad = presupuesto de latencia/cómputo.
"""

print("\n--- 0/1 Knapsack bottom-up ---")

def knapsack(pesos: list, valores: list, capacidad: int) -> tuple:
    """
    0/1 Knapsack. O(N × W) tiempo y espacio.
    Retorna (valor_máximo, items_seleccionados).
    """
    n = len(pesos)
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacidad + 1):
            # No incluir item i
            dp[i][w] = dp[i - 1][w]
            # Incluir item i (si cabe)
            if pesos[i - 1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i - 1][w - pesos[i - 1]] + valores[i - 1])
    
    # Reconstruir la solución
    items = []
    w = capacidad
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            items.append(i - 1)
            w -= pesos[i - 1]
    
    return dp[n][capacidad], items[::-1]

# Feature selection como Knapsack
features = [
    ("embedding_dim_768", 50, 85),   # (nombre, coste_ms, importancia)
    ("word_count", 1, 30),
    ("sentiment_score", 20, 60),
    ("tfidf_vector", 30, 75),
    ("pos_tags", 15, 45),
    ("ner_tags", 25, 55),
    ("bigram_freq", 5, 40),
]

nombres = [f[0] for f in features]
costes = [f[1] for f in features]
importancias = [f[2] for f in features]
presupuesto_ms = 80  # Máximo 80ms de latencia

valor_max, seleccionados = knapsack(costes, importancias, presupuesto_ms)

print(f"Presupuesto: {presupuesto_ms}ms")
print(f"Valor máximo alcanzable: {valor_max}")
print(f"Features seleccionadas:")
coste_total = 0
for idx in seleccionados:
    print(f"  {nombres[idx]:<20} coste={costes[idx]:>3}ms  importancia={importancias[idx]}")
    coste_total += costes[idx]
print(f"Coste total: {coste_total}ms / {presupuesto_ms}ms")


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: EJERCICIO — SPELL CHECKER CON EDIT DISTANCE ===")
print("=" * 80)

"""
Construir un corrector ortográfico simple que:
1. Recibe una palabra con posible error.
2. Busca las palabras más cercanas en un diccionario.
3. Sugiere correcciones ordenadas por distancia.

Esto es una aplicación directa de Edit Distance + DP.
"""

print("\n--- Spell Checker ---")

class SpellChecker:
    """Corrector ortográfico basado en Edit Distance."""
    
    def __init__(self, diccionario: list[str]):
        self.diccionario = diccionario
    
    def corregir(self, palabra: str, max_distancia: int = 3, 
                 top_k: int = 5) -> list[tuple[str, int]]:
        """
        Retorna las top_k palabras más cercanas con distancia <= max_distancia.
        """
        candidatos = []
        for palabra_dict in self.diccionario:
            d = edit_distance_optimizado(palabra.lower(), palabra_dict.lower())
            if d <= max_distancia:
                candidatos.append((palabra_dict, d))
        
        # Ordenar por distancia, luego alfabéticamente
        candidatos.sort(key=lambda x: (x[1], x[0]))
        return candidatos[:top_k]

# Diccionario de términos ML
diccionario_ml = [
    "python", "pytorch", "tensorflow", "transformer", "attention",
    "embedding", "tokenizer", "encoder", "decoder", "gradient",
    "backpropagation", "optimization", "regularization", "dropout",
    "convolution", "recurrent", "generative", "discriminative",
    "classification", "regression", "clustering", "dimensionality",
    "overfitting", "underfitting", "hyperparameter", "validation",
    "inference", "training", "evaluation", "deployment",
    "pipeline", "preprocessing", "feature", "dataset",
    "batch", "epoch", "learning", "neural", "network",
    "model", "weight", "bias", "activation", "softmax",
]

checker = SpellChecker(diccionario_ml)

palabras_con_error = ["pyton", "tensrflow", "tranformer", "gradiint", "embeding"]

for palabra in palabras_con_error:
    sugerencias = checker.corregir(palabra)
    print(f"\n  '{palabra}' -> ", end="")
    if sugerencias:
        mejor = sugerencias[0]
        print(f"¿Quisiste decir '{mejor[0]}'? (distancia={mejor[1]})")
        if len(sugerencias) > 1:
            otras = ", ".join(f"'{s[0]}'({s[1]})" for s in sugerencias[1:3])
            print(f"           Otras: {otras}")
    else:
        print("Sin sugerencias")


print("\n" + "=" * 80)
print("=== CAPÍTULO 11: MAXIMUM SUBARRAY (KADANE'S ALGORITHM) ===")
print("=" * 80)

"""
Encontrar el subarray contiguo con la suma máxima.
Es DP porque: max_ending_here[i] = max(arr[i], max_ending_here[i-1] + arr[i])

Complejidad: O(N) tiempo, O(1) espacio.

EN ML: encontrar la ventana temporal con mayor retorno acumulado,
o la subsecuencia de features que maximiza la correlación.
"""

print("\n--- Kadane's Algorithm ---")

def max_subarray(arr: list) -> tuple:
    """
    Retorna (suma_máxima, inicio, fin) del subarray con mayor suma.
    O(N) tiempo, O(1) espacio.
    """
    max_sum = arr[0]
    current_sum = arr[0]
    start = end = 0
    temp_start = 0
    
    for i in range(1, len(arr)):
        if current_sum + arr[i] < arr[i]:
            current_sum = arr[i]
            temp_start = i
        else:
            current_sum += arr[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, start, end

datos_kadane = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
suma, ini, fin = max_subarray(datos_kadane)
print(f"Array: {datos_kadane}")
print(f"Max subarray: {datos_kadane[ini:fin+1]}, suma = {suma}")

# Caso ML: retornos de un modelo a lo largo del tiempo
import random
random.seed(42)
retornos = [random.gauss(0.01, 0.1) for _ in range(100)]
suma_max, ini, fin = max_subarray(retornos)
print(f"\nMejor racha de retornos: posiciones [{ini}, {fin}], "
      f"ganancia acum = {suma_max:.4f}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: LONGEST INCREASING SUBSEQUENCE (LIS) ===")
print("=" * 80)

"""
Encontrar la subsecuencia creciente más larga (no contigua).
Ejemplo: [10, 9, 2, 5, 3, 7, 101, 18] -> [2, 3, 7, 101] (longitud 4).

Solución DP: O(N²).
Solución óptima con búsqueda binaria: O(N log N).

EN ML: encontrar la tendencia creciente más larga en métricas de training.
"""

print("\n--- LIS con DP O(N²) ---")

def lis_dp(arr: list) -> tuple:
    """
    Longest Increasing Subsequence.
    Retorna (longitud, subsecuencia).
    O(N²) tiempo, O(N) espacio.
    """
    n = len(arr)
    dp = [1] * n
    parent = [-1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    
    # Encontrar el final de la LIS
    max_len = max(dp)
    end_idx = dp.index(max_len)
    
    # Reconstruir
    lis = []
    idx = end_idx
    while idx != -1:
        lis.append(arr[idx])
        idx = parent[idx]
    lis.reverse()
    
    return max_len, lis

datos_lis = [10, 9, 2, 5, 3, 7, 101, 18]
longitud, subsec = lis_dp(datos_lis)
print(f"Array: {datos_lis}")
print(f"LIS: {subsec} (longitud {longitud})")


print("\n--- LIS con búsqueda binaria O(N log N) ---")

import bisect

def lis_binario(arr: list) -> int:
    """
    LIS usando patience sorting + bisect.
    O(N log N) tiempo, O(N) espacio.
    Retorna solo la longitud (reconstruir requiere más trabajo).
    """
    tails = []  # tails[i] = menor valor final de LIS de longitud i+1
    
    for x in arr:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    
    return len(tails)

print(f"\nLIS binario: longitud = {lis_binario(datos_lis)}")

# Benchmark
import time
random.seed(42)
datos_grandes = [random.randint(1, 10000) for _ in range(5000)]

inicio = time.perf_counter()
lis_dp(datos_grandes)
t_dp = time.perf_counter() - inicio

inicio = time.perf_counter()
lis_binario(datos_grandes)
t_bin = time.perf_counter() - inicio

print(f"N=5000: DP O(N²)={t_dp*1000:.1f}ms  Binario O(N log N)={t_bin*1000:.2f}ms")


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: ROUGE-L CON LCS — EVALUACIÓN DE RESÚMENES ===")
print("=" * 80)

"""
ROUGE-L es una métrica estándar para evaluar resúmenes de texto.
Usa LCS (Longest Common Subsequence) para calcular la similitud
entre un resumen generado y un resumen de referencia.

ROUGE-L:
- Precision = LCS(ref, gen) / len(gen)
- Recall = LCS(ref, gen) / len(ref)
- F1 = 2 * P * R / (P + R)
"""

print("\n--- Implementación de ROUGE-L ---")

def rouge_l(referencia: str, generado: str) -> dict:
    """
    Calcula ROUGE-L entre una referencia y un texto generado.
    Opera a nivel de palabra.
    """
    ref_tokens = referencia.lower().split()
    gen_tokens = generado.lower().split()
    
    # Calcular longitud de LCS
    n, m = len(ref_tokens), len(gen_tokens)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref_tokens[i-1] == gen_tokens[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    lcs_len = dp[n][m]
    
    precision = lcs_len / m if m > 0 else 0
    recall = lcs_len / n if n > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {"precision": precision, "recall": recall, "f1": f1, "lcs_length": lcs_len}

ref = "el modelo transformer utiliza atención para procesar secuencias"
gen1 = "el transformer usa atención para procesar datos en secuencias"
gen2 = "las redes neuronales convolucionales procesan imágenes"

for gen in [gen1, gen2]:
    scores = rouge_l(ref, gen)
    print(f"\n  Ref: '{ref}'")
    print(f"  Gen: '{gen}'")
    print(f"  ROUGE-L: P={scores['precision']:.3f}  R={scores['recall']:.3f}  "
          f"F1={scores['f1']:.3f}  (LCS={scores['lcs_length']})")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: GUÍA DE RECONOCIMIENTO DE PROBLEMAS DP ===")
print("=" * 80)

"""
¿CÓMO SABER SI UN PROBLEMA ES DP?

SEÑALES CLARAS:
1. "Cuántas formas hay de..." -> contar caminos = DP.
2. "Cuál es el mínimo/máximo..." -> optimización = posible DP.
3. "Puedes o no seleccionar cada item..." -> knapsack variant = DP.
4. "Secuencia/string" + "matching/similarity" -> edit distance/LCS = DP.
5. La solución recursiva recalcula los mismos subproblemas.

PATRÓN DE IMPLEMENTACIÓN:
1. Define el ESTADO: ¿qué parámetros describen un subproblema?
2. Define la TRANSICIÓN: ¿cómo se conectan subproblemas?
3. Define el CASO BASE: ¿cuándo es trivial?
4. Elige TOP-DOWN o BOTTOM-UP.
5. Optimiza ESPACIO si es posible.
"""

print("""
╔═══════════════════════════════════════════════════════════════════╗
║ TIPO DE PROBLEMA              ║ SOLUCIÓN DP                     ║
╠═══════════════════════════════╬═════════════════════════════════╣
║ Fibonacci / Escaleras         ║ dp[i] = dp[i-1] + dp[i-2]      ║
║ Coin Change                   ║ dp[i] = min(dp[i-c] + 1)       ║
║ Edit Distance                 ║ dp[i][j] tabla 2D               ║
║ LCS / ROUGE-L                 ║ dp[i][j] tabla 2D               ║
║ Knapsack                      ║ dp[i][w] incluir o no           ║
║ Max Subarray (Kadane)         ║ dp[i] = max(arr[i], dp[i-1]+a)  ║
║ LIS                           ║ dp[i] = max(dp[j]+1) para j<i   ║
║ Matrix Chain                  ║ dp[i][j] = min partitions       ║
║ Word Break                    ║ dp[i] = any(dp[j] and s[j:i])   ║
╚═══════════════════════════════╩═════════════════════════════════╝
""")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN ARQUITECTÓNICA ===")
print("=" * 80)

"""
RESUMEN DE PROGRAMACIÓN DINÁMICA PARA INGENIERÍA IA:

1. DP = subproblemas solapados + subestructura óptima.
   Si se repiten cálculos -> DP los elimina.

2. Top-down (memoización): @lru_cache/@cache. Natural, pero recursivo.
   Bottom-up (tabulación): iterativo, sin riesgo de stack overflow.

3. Fibonacci: el ejemplo canónico. 2^N -> N. lru_cache lo hace trivial.

4. Edit Distance (Levenshtein): O(N×M). Fundamental en NLP.

5. LCS: base de ROUGE-L. Knapsack: feature selection con budget.

6. @lru_cache: maxsize=None para caché ilimitada. Argumentos hashables.

7. Kadane: max subarray en O(N). LIS: subsecuencia creciente O(N log N).

8. ROUGE-L: evaluación de resúmenes basada en LCS.

9. Reconocimiento: "cuántas formas", "mínimo/máximo de", "matching" = DP.

FIN DEL MÓDULO 03: ALGORITMIA Y COMPLEJIDAD COMPUTACIONAL.
"""

print("\n FIN DE ARCHIVO 05_programacion_dinamica_y_lru_cache.")
print(" El módulo de algoritmia está COMPLETO.")
print(" Siguiente módulo: 04_Funciones_Flujo_Y_Funcional.")

