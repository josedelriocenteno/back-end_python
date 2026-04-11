# ===========================================================================
# 02_busquedas_y_bisect.py
# ===========================================================================
# MÓDULO 03: ALGORITMIA Y COMPLEJIDAD COMPUTACIONAL
# ARCHIVO 02: Búsquedas Binarias, Módulo bisect y Aplicaciones en ML
# ===========================================================================
#
# OBJETIVO (1000+ LÍNEAS):
# Dominar las búsquedas como herramienta diaria de ingeniería.
# No solo "buscar un elemento" — sino insertar en orden, clasificar
# por umbral, encontrar el K-ésimo elemento, y construir estructuras
# fundamentales de ML como árboles de decisión simplificados.
#
# CONTENIDO:
#   1. Búsqueda lineal: cuándo es suficiente y cuándo no.
#   2. Búsqueda binaria: implementación desde cero + análisis.
#   3. Módulo bisect: bisect_left, bisect_right, insort.
#   4. Aplicaciones en ML: umbrales de clasificación, bucketing.
#   5. Two-pointer technique para problemas de pares.
#   6. Búsqueda ternaria y golden-section (optimización de hiperparámetros).
#   7. Búsqueda en matrices 2D ordenadas.
#   8. Ejercicio integrador: sistema de ranking de confianza.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import time
import bisect
import random
import sys
from typing import Optional, Any
from collections import defaultdict


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 1: BÚSQUEDA LINEAL — LA BASE                                  ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: BÚSQUEDA LINEAL — CUÁNDO ES SUFICIENTE ===")
print("=" * 80)

"""
La búsqueda lineal recorre CADA elemento hasta encontrar el objetivo.
Complejidad: O(N) en el peor caso.

¿Cuándo es SUFICIENTE?
- Datos NO ordenados (no puedes usar binaria).
- N < ~1000 (la diferencia es despreciable).
- Buscas por un criterio complejo (no solo igualdad).
- Solo necesitas buscar una vez (no vale la pena ordenar).

¿Cuándo NO es suficiente?
- Búsquedas repetidas sobre los mismos datos.
- N > 10,000 (empieza a doler).
- Tiempo real / baja latencia (APIs de inferencia).
"""

print("\n--- Implementaciones de búsqueda lineal ---")

def busqueda_lineal_simple(lista: list, objetivo) -> int:
    """Retorna el índice del objetivo o -1 si no existe."""
    for i, x in enumerate(lista):
        if x == objetivo:
            return i
    return -1

def busqueda_lineal_con_predicado(lista: list, predicado) -> Optional[Any]:
    """Retorna el PRIMER elemento que cumple el predicado."""
    for x in lista:
        if predicado(x):
            return x
    return None

# Ejemplo ML: encontrar la primera predicción con score > 0.9
predicciones = [
    {"id": 0, "label": "perro", "score": 0.72},
    {"id": 1, "label": "gato", "score": 0.85},
    {"id": 2, "label": "ave", "score": 0.93},
    {"id": 3, "label": "pez", "score": 0.95},
]

alta_confianza = busqueda_lineal_con_predicado(
    predicciones, 
    lambda p: p["score"] > 0.9
)
print(f"Primera predicción con score > 0.9: {alta_confianza}")


print("\n--- Búsqueda lineal: encontrar TODOS los matches ---")

def buscar_todos(lista: list, predicado) -> list:
    """Retorna TODOS los elementos que cumplen el predicado."""
    return [x for x in lista if predicado(x)]

altas = buscar_todos(predicciones, lambda p: p["score"] > 0.85)
print(f"Todas las predicciones con score > 0.85: {altas}")


print("\n--- Búsqueda del mínimo/máximo con criterio ---")

def argmin(lista: list, key=None):
    """Retorna el elemento con el menor valor de key(x)."""
    if key is None:
        key = lambda x: x
    mejor = None
    mejor_val = float('inf')
    for x in lista:
        val = key(x)
        if val < mejor_val:
            mejor_val = val
            mejor = x
    return mejor

def argmax(lista: list, key=None):
    """Retorna el elemento con el mayor valor de key(x)."""
    if key is None:
        key = lambda x: x
    mejor = None
    mejor_val = float('-inf')
    for x in lista:
        val = key(x)
        if val > mejor_val:
            mejor_val = val
            mejor = x
    return mejor

# Ejemplo: mejor y peor predicción
mejor_pred = argmax(predicciones, key=lambda p: p["score"])
peor_pred = argmin(predicciones, key=lambda p: p["score"])
print(f"Mejor predicción: {mejor_pred}")
print(f"Peor predicción: {peor_pred}")

# En Python, max() y min() ya aceptan key=
print(f"Lo mismo con max(): {max(predicciones, key=lambda p: p['score'])}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 2: BÚSQUEDA BINARIA DESDE CERO                                ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 2: BÚSQUEDA BINARIA — IMPLEMENTACIÓN DESDE CERO ===")
print("=" * 80)

"""
REQUISITO ABSOLUTO: los datos deben estar ORDENADOS.
Si no están ordenados, primero ordenas O(N log N) y luego buscas O(log N).
Si solo buscas una vez, O(N) lineal es mejor (N < N log N + log N).
Si buscas M veces, ordenar + M búsquedas = O(N log N + M log N).
Con M > N, la búsqueda binaria amortiza con creces el coste del sort.

ALGORITMO:
1. Mira el elemento del MEDIO de la sublista.
2. Si es el objetivo, lo encontraste.
3. Si el objetivo es MENOR, busca en la mitad IZQUIERDA.
4. Si el objetivo es MAYOR, busca en la mitad DERECHA.
5. Repite hasta encontrar o agotar (izq > der).

Cada paso elimina la MITAD del espacio de búsqueda.
Con 1,000,000 de elementos: log₂(1,000,000) ≈ 20 pasos. NADA.
"""

print("\n--- Búsqueda binaria iterativa ---")

def busqueda_binaria(lista: list, objetivo) -> int:
    """
    Retorna el índice del objetivo o -1 si no existe.
    REQUIERE: lista ordenada ascendentemente.
    Complejidad: O(log N) tiempo, O(1) espacio.
    """
    izq, der = 0, len(lista) - 1
    
    while izq <= der:
        # Evitar overflow en otros lenguajes: mid = izq + (der - izq) // 2
        mid = (izq + der) // 2
        
        if lista[mid] == objetivo:
            return mid
        elif lista[mid] < objetivo:
            izq = mid + 1  # Descartar mitad izquierda
        else:
            der = mid - 1  # Descartar mitad derecha
    
    return -1  # No encontrado

datos = list(range(0, 100, 2))  # [0, 2, 4, 6, ..., 98]
print(f"Datos: {datos[:10]}... ({len(datos)} elementos)")
print(f"Buscar 42: índice = {busqueda_binaria(datos, 42)}")
print(f"Buscar 43: índice = {busqueda_binaria(datos, 43)} (no existe)")


print("\n--- Búsqueda binaria recursiva ---")

def busqueda_binaria_rec(lista: list, objetivo, izq: int = 0, der: int = None) -> int:
    """
    Versión recursiva. Misma lógica, diferente estilo.
    O(log N) tiempo, O(log N) espacio (stack de recursión).
    """
    if der is None:
        der = len(lista) - 1
    
    if izq > der:
        return -1
    
    mid = (izq + der) // 2
    
    if lista[mid] == objetivo:
        return mid
    elif lista[mid] < objetivo:
        return busqueda_binaria_rec(lista, objetivo, mid + 1, der)
    else:
        return busqueda_binaria_rec(lista, objetivo, izq, mid - 1)

print(f"Recursiva buscar 42: {busqueda_binaria_rec(datos, 42)}")
print(f"Recursiva buscar 43: {busqueda_binaria_rec(datos, 43)}")


print("\n--- Contar pasos de búsqueda binaria ---")

def busqueda_binaria_verbose(lista: list, objetivo) -> tuple:
    """Retorna (índice, número_de_pasos)."""
    izq, der = 0, len(lista) - 1
    pasos = 0
    
    while izq <= der:
        pasos += 1
        mid = (izq + der) // 2
        
        if lista[mid] == objetivo:
            return mid, pasos
        elif lista[mid] < objetivo:
            izq = mid + 1
        else:
            der = mid - 1
    
    return -1, pasos

import math
for n in [100, 1_000, 10_000, 100_000, 1_000_000]:
    datos_n = list(range(n))
    objetivo_n = n - 1  # Peor caso: último elemento
    idx, pasos = busqueda_binaria_verbose(datos_n, objetivo_n)
    print(f"  N={n:>10,}: encontrado en {pasos:>3} pasos (log₂N = {math.log2(n):.1f})")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 3: MÓDULO BISECT — BÚSQUEDA BINARIA A NIVEL C                ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 3: BISECT — LA NAVAJA SUIZA DE LA BÚSQUEDA ORDENADA ===")
print("=" * 80)

"""
El módulo `bisect` de Python implementa búsqueda binaria en C puro.
Es ~10x más rápido que una implementación Python pura.

FUNCIONES CLAVE:
- bisect_left(a, x):  Punto de inserción a la IZQUIERDA de x existente.
- bisect_right(a, x): Punto de inserción a la DERECHA de x existente.
- insort_left(a, x):  Inserta x manteniendo el orden (izquierda).
- insort_right(a, x): Inserta x manteniendo el orden (derecha).

bisect_left vs bisect_right:
Si x ya existe en la lista:
- bisect_left retorna el índice ANTES del primer x.
- bisect_right retorna el índice DESPUÉS del último x.

NOTA: bisect.bisect() es alias de bisect_right().
"""

print("\n--- bisect_left vs bisect_right ---")

datos_con_dup = [1, 3, 5, 5, 5, 7, 9]
print(f"Datos: {datos_con_dup}")

pos_left = bisect.bisect_left(datos_con_dup, 5)
pos_right = bisect.bisect_right(datos_con_dup, 5)

print(f"bisect_left(5):  {pos_left}  -> insertaría ANTES de los 5s")
print(f"bisect_right(5): {pos_right} -> insertaría DESPUÉS de los 5s")
print(f"Cantidad de 5s en la lista: {pos_right - pos_left}")


print("\n--- Usar bisect para buscar si un elemento existe ---")

def buscar_con_bisect(lista_ordenada: list, objetivo) -> int:
    """
    Busca un elemento usando bisect_left. O(log N).
    Retorna el índice del elemento o -1 si no existe.
    """
    idx = bisect.bisect_left(lista_ordenada, objetivo)
    if idx < len(lista_ordenada) and lista_ordenada[idx] == objetivo:
        return idx
    return -1

datos_ord = [10, 20, 30, 40, 50, 60, 70]
print(f"\nBuscar 30: {buscar_con_bisect(datos_ord, 30)}")
print(f"Buscar 35: {buscar_con_bisect(datos_ord, 35)}")


print("\n--- insort: inserción manteniendo el orden ---")

lista_ordenada = [10, 20, 30, 50, 60]
print(f"Antes: {lista_ordenada}")

bisect.insort(lista_ordenada, 40)
print(f"Tras insort(40): {lista_ordenada}")

bisect.insort(lista_ordenada, 25)
print(f"Tras insort(25): {lista_ordenada}")

# CUIDADO: insort es O(log N) para BUSCAR la posición + O(N) para INSERTAR.
# El insert desplaza elementos. Total: O(N), no O(log N).
# Para inserción masiva, usa un heap o un árbol balanceado.


print("\n" + "=" * 80)
print("=== CAPÍTULO 4: APLICACIONES ML — CLASIFICACIÓN POR UMBRALES ===")
print("=" * 80)

"""
En ML, un clasificador binario produce un SCORE continuo (ej: 0.0 - 1.0).
Para convertirlo en una predicción (positivo/negativo), aplicas un UMBRAL.

Si el score > umbral -> Positivo
Si el score <= umbral -> Negativo

¿Cómo eliges el umbral óptimo? Pruebas MUCHOS umbrales y calculas 
métricas (precision, recall, F1) para cada uno. Bisect hace esto eficiente.
"""

print("\n--- Clasificación por umbral con bisect ---")

# Scores de un modelo, ya ordenados
random.seed(42)
scores_modelo = sorted([random.random() for _ in range(10_000)])
labels_reales = [1 if s > 0.5 + random.gauss(0, 0.15) else 0 for s in scores_modelo]

def contar_positivos_sobre_umbral(scores_ord: list, umbral: float) -> int:
    """
    Cuenta cuántos scores son > umbral usando bisect.
    O(log N) en vez de O(N).
    """
    idx = bisect.bisect_right(scores_ord, umbral)
    return len(scores_ord) - idx

for umbral in [0.3, 0.5, 0.7, 0.9]:
    n_positivos = contar_positivos_sobre_umbral(scores_modelo, umbral)
    print(f"  Umbral {umbral}: {n_positivos} predichos positivos "
          f"({n_positivos/len(scores_modelo):.1%} del total)")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: BUCKETING — ASIGNAR CATEGORÍAS CON BISECT ===")
print("=" * 80)

"""
Bucketing (o binning) es la técnica de asignar valores continuos 
a categorías discretas. Muy usado en feature engineering:
- Agrupar edades: joven, adulto, senior.
- Agrupar scores: bajo, medio, alto, muy alto.
- Discretizar features continuas para árboles de decisión.

bisect.bisect() es PERFECTO para esto.
"""

print("\n--- Asignar grados de confianza ---")

def asignar_confianza(score: float) -> str:
    """
    Clasifica un score en categorías de confianza.
    Usa bisect para O(log K) donde K = número de umbrales.
    """
    umbrales = [0.3, 0.5, 0.7, 0.9]
    categorias = ["Muy Baja", "Baja", "Media", "Alta", "Muy Alta"]
    
    idx = bisect.bisect(umbrales, score)
    return categorias[idx]

scores_test = [0.15, 0.35, 0.55, 0.75, 0.95]
for s in scores_test:
    print(f"  Score {s:.2f} -> {asignar_confianza(s)}")


print("\n--- Asignar letras de calificación (estilo universitario) ---")

def calificacion(nota: float) -> str:
    """Asigna letra basada en umbrales."""
    umbrales = [60, 70, 80, 90]
    letras = ["F", "D", "C", "B", "A"]
    return letras[bisect.bisect(umbrales, nota)]

for nota in [45, 65, 75, 85, 95]:
    print(f"  Nota {nota} -> {calificacion(nota)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 6: TWO-POINTER TECHNIQUE ===")
print("=" * 80)

"""
La técnica de dos punteros es un patrón algorítmico que usa dos 
índices que se mueven por la lista (generalmente uno desde cada extremo).

Puede transformar problemas O(N²) en O(N).

Requiere: datos ORDENADOS.

Usos en ML:
- Encontrar pares de features cuya suma = target.
- Validar rangos de hiperparámetros.
- Merge de dos listas ordenadas (base de Merge Sort).
"""

print("\n--- Problema: encontrar dos numbers que sumen target ---")

def dos_suma_cuadratico(lista: list, target: int) -> tuple:
    """O(N²): prueba todas las parejas."""
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] + lista[j] == target:
                return (i, j)
    return None

def dos_suma_two_pointer(lista_ordenada: list, target: int) -> tuple:
    """
    O(N): dos punteros desde los extremos.
    REQUIERE: lista ordenada.
    """
    izq, der = 0, len(lista_ordenada) - 1
    
    while izq < der:
        suma = lista_ordenada[izq] + lista_ordenada[der]
        if suma == target:
            return (izq, der)
        elif suma < target:
            izq += 1  # Necesitamos un número más grande
        else:
            der -= 1  # Necesitamos un número más pequeño
    
    return None

datos_ord = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
target = 20
resultado = dos_suma_two_pointer(datos_ord, target)
if resultado:
    i, j = resultado
    print(f"Par que suma {target}: datos[{i}]={datos_ord[i]} + datos[{j}]={datos_ord[j]}")


print("\n--- Benchmark: O(N²) vs O(N) ---")

n_bench = 5_000
datos_bench = list(range(1, n_bench + 1))
target_bench = n_bench + n_bench - 1  # Los dos mayores

inicio = time.perf_counter()
dos_suma_cuadratico(datos_bench, target_bench)
t_cuad = time.perf_counter() - inicio

inicio = time.perf_counter()
dos_suma_two_pointer(datos_bench, target_bench)
t_tp = time.perf_counter() - inicio

print(f"  O(N²): {t_cuad*1000:.2f} ms")
print(f"  O(N):  {t_tp*1000:.4f} ms")
print(f"  Ratio: {t_cuad/t_tp:.0f}x más rápido con two-pointer")


print("\n" + "=" * 80)
print("=== CAPÍTULO 7: MERGE DE LISTAS ORDENADAS ===")
print("=" * 80)

"""
Fusionar dos listas ya ordenadas en una sola ordenada es la operación 
central de Merge Sort. Es O(N + M) donde N y M son las longitudes.

En ML se usa para:
- Combinar resultados de dos shards de datos.
- Merge de inverted indexes.
- Unir dos streams de predicciones ordenados por timestamp.
"""

print("\n--- Merge de dos listas ordenadas O(N + M) ---")

def merge_ordenado(a: list, b: list) -> list:
    """Fusiona dos listas ordenadas en una nueva lista ordenada."""
    resultado = []
    i, j = 0, 0
    
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            resultado.append(a[i])
            i += 1
        else:
            resultado.append(b[j])
            j += 1
    
    # Añadir el resto
    resultado.extend(a[i:])
    resultado.extend(b[j:])
    
    return resultado

lista_a = [1, 3, 5, 7, 9]
lista_b = [2, 4, 6, 8, 10]
merged = merge_ordenado(lista_a, lista_b)
print(f"Lista A: {lista_a}")
print(f"Lista B: {lista_b}")
print(f"Merged:  {merged}")

# Verificar
assert merged == sorted(lista_a + lista_b)
print(f"Verificado: merge == sorted(a + b)")


print("\n--- Merge de K listas con heapq.merge ---")

import heapq

listas_k = [
    [1, 5, 9, 13],
    [2, 6, 10, 14],
    [3, 7, 11, 15],
    [4, 8, 12, 16],
]

# heapq.merge() hace merge de K listas ordenadas.
# Complejidad: O(N log K) donde N = total de elementos, K = número de listas.
resultado_k = list(heapq.merge(*listas_k))
print(f"\nMerge de {len(listas_k)} listas: {resultado_k}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: BÚSQUEDA EN MATRICES 2D ORDENADAS ===")
print("=" * 80)

"""
En ML, a menudo trabajas con matrices donde:
- Cada fila está ordenada de izquierda a derecha.
- Cada columna está ordenada de arriba a abajo.

Ejemplo: matriz de distancias entre embeddings (parcialmente ordenada).

Algoritmo: "Staircase Search" (empezar por esquina superior-derecha).
Complejidad: O(N + M) donde N = filas, M = columnas.
"""

print("\n--- Staircase Search en matriz 2D ---")

def buscar_matriz_2d(matriz: list[list[int]], objetivo: int) -> tuple:
    """
    Busca objetivo en una matriz donde filas y columnas están ordenadas.
    Empieza por la esquina superior-derecha.
    O(N + M) donde N = filas, M = columnas.
    """
    if not matriz or not matriz[0]:
        return None
    
    filas = len(matriz)
    cols = len(matriz[0])
    
    # Empezar en esquina superior-derecha
    fila, col = 0, cols - 1
    
    while fila < filas and col >= 0:
        valor = matriz[fila][col]
        if valor == objetivo:
            return (fila, col)
        elif valor < objetivo:
            fila += 1   # Necesitamos algo más grande -> bajar
        else:
            col -= 1    # Necesitamos algo más pequeño -> izquierda
    
    return None

matriz = [
    [ 1,  4,  7, 11],
    [ 2,  5,  8, 12],
    [ 3,  6,  9, 16],
    [10, 13, 14, 17],
]

print("Matriz:")
for fila in matriz:
    print(f"  {fila}")

for obj in [5, 9, 15, 17]:
    pos = buscar_matriz_2d(matriz, obj)
    print(f"  Buscar {obj:>2}: {'encontrado en ' + str(pos) if pos else 'no encontrado'}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 9: LOWER/UPPER BOUND — RANGOS CON BISECT ===")
print("=" * 80)

"""
bisect_left y bisect_right definen los LÍMITES de un rango de valores.
Esto permite contar elementos en un rango [lo, hi] en O(log N).
"""

print("\n--- Contar elementos en un rango ---")

def contar_en_rango(lista_ord: list, lo: float, hi: float) -> int:
    """
    Cuenta cuántos elementos están en [lo, hi] (inclusive).
    O(log N) con bisect.
    """
    izq = bisect.bisect_left(lista_ord, lo)
    der = bisect.bisect_right(lista_ord, hi)
    return der - izq

random.seed(42)
scores = sorted([random.random() for _ in range(100_000)])

for lo, hi in [(0.0, 0.5), (0.3, 0.7), (0.9, 1.0)]:
    conteo = contar_en_rango(scores, lo, hi)
    print(f"  Scores en [{lo}, {hi}]: {conteo} ({conteo/len(scores):.1%})")


print("\n--- Percentil con bisect ---")

def percentil(lista_ord: list, valor: float) -> float:
    """
    Calcula en qué percentil cae un valor.
    O(log N).
    """
    pos = bisect.bisect_left(lista_ord, valor)
    return pos / len(lista_ord) * 100

print(f"\n  Score 0.5 está en el percentil {percentil(scores, 0.5):.1f}")
print(f"  Score 0.95 está en el percentil {percentil(scores, 0.95):.1f}")
print(f"  Score 0.1 está en el percentil {percentil(scores, 0.1):.1f}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: SORTED CONTAINERS — MANTENIENDO EL ORDEN DINÁMICO ===")
print("=" * 80)

"""
insort mantiene una lista ordenada tras cada inserción, pero el insert
subyacente es O(N). Para datos que cambian constantemente, hay alternativas:

1. heapq: O(log N) insert y O(1) para ver el mínimo (pero no para buscar).
2. sortedcontainers (pip): SortedList con O(log N) insert Y búsqueda.
3. Reconstruir el sort periódicamente (batch inserts).

Aquí simulamos un stream de scores donde mantenemos el ranking actualizado.
"""

print("\n--- Simulando un stream de predicciones con ranking en vivo ---")

class RankingEnVivo:
    """
    Mantiene un ranking ordenado de scores con insort.
    Para datasets pequeños (~10K) es suficiente.
    """
    def __init__(self):
        self.scores = []
        self.datos = []
    
    def agregar(self, score: float, dato: str):
        """Inserta manteniendo el orden. O(N) por el desplazamiento."""
        idx = bisect.bisect_left(self.scores, score)
        self.scores.insert(idx, score)
        self.datos.insert(idx, dato)
    
    def top_k(self, k: int) -> list:
        """Retorna los K mejores (mayores scores). O(K)."""
        return list(zip(self.scores[-k:], self.datos[-k:]))[::-1]
    
    def percentil_de(self, score: float) -> float:
        """En qué percentil está este score. O(log N)."""
        pos = bisect.bisect_left(self.scores, score)
        return pos / len(self.scores) * 100

ranking = RankingEnVivo()
random.seed(123)
for i in range(1000):
    score = random.random()
    ranking.agregar(score, f"pred_{i}")

print(f"  Total predicciones: {len(ranking.scores)}")
print(f"  Top 3:")
for score, dato in ranking.top_k(3):
    print(f"    {dato}: {score:.4f}")

print(f"\n  Score 0.5 está en el percentil {ranking.percentil_de(0.5):.1f}")
print(f"  Score 0.95 está en el percentil {ranking.percentil_de(0.95):.1f}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 11: TABLA DE COMPLEJIDAD DE BÚSQUEDAS ===")
print("=" * 80)

"""
╔═══════════════════════════════════╦══════════════╦═══════════════════╗
║ ALGORITMO                         ║ TIEMPO       ║ ESPACIO           ║
╠═══════════════════════════════════╬══════════════╬═══════════════════╣
║ Búsqueda lineal                   ║ O(N)         ║ O(1)              ║
║ Búsqueda binaria (manual)         ║ O(log N)     ║ O(1)              ║
║ bisect_left / bisect_right        ║ O(log N)     ║ O(1)              ║
║ insort                            ║ O(N)         ║ O(1)*             ║
║ Two-pointer                       ║ O(N)         ║ O(1)              ║
║ Merge de 2 listas                 ║ O(N + M)     ║ O(N + M)          ║
║ Merge de K listas (heapq)         ║ O(N log K)   ║ O(K)              ║
║ Staircase search (matriz 2D)      ║ O(N + M)     ║ O(1)              ║
║ Hash lookup (dict/set)            ║ O(1)         ║ O(N)              ║
╚═══════════════════════════════════╩══════════════╩═══════════════════╝

* insort es O(log N) para BUSCAR la posición + O(N) para el insert.
  El cuello de botella es el desplazamiento de elementos en la lista.
"""


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: BINARY SEARCH ON ANSWER (BÚSQUEDA PARAMÉTRICA) ===")
print("=" * 80)

"""
La búsqueda binaria no solo sirve para "encontrar un elemento".
Puede buscar el VALOR ÓPTIMO de un parámetro cuando:
- La función objetivo es MONÓTONA (crece o decrece).
- Puedes verificar si un valor es "suficiente" en O(N) o menos.

En ML esto se usa para:
- Encontrar el umbral óptimo de un clasificador.
- Calibrar la temperatura de softmax.
- Encontrar el learning rate máximo antes de divergir.
"""

print("\n--- Encontrar umbral óptimo que maximice F1 ---")

def calcular_precision_recall(scores_ord: list, labels: list, umbral: float):
    """Calcula precision y recall para un umbral dado."""
    tp = fp = fn = 0
    for score, label in zip(scores_ord, labels):
        pred = 1 if score > umbral else 0
        if pred == 1 and label == 1:
            tp += 1
        elif pred == 1 and label == 0:
            fp += 1
        elif pred == 0 and label == 1:
            fn += 1
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

# Generar datos simulados
random.seed(42)
n_samples = 5_000
scores_sim = sorted([random.random() for _ in range(n_samples)])
# Labels con algo de ruido
labels_sim = [1 if s > 0.45 + random.gauss(0, 0.1) else 0 for s in scores_sim]

# Búsqueda del mejor umbral probando múltiples valores
mejor_umbral = 0
mejor_f1 = 0

for umbral_candidato in [i / 100 for i in range(10, 91)]:
    _, _, f1 = calcular_precision_recall(scores_sim, labels_sim, umbral_candidato)
    if f1 > mejor_f1:
        mejor_f1 = f1
        mejor_umbral = umbral_candidato

prec, rec, f1 = calcular_precision_recall(scores_sim, labels_sim, mejor_umbral)
print(f"  Mejor umbral: {mejor_umbral:.2f}")
print(f"  Precision: {prec:.3f}, Recall: {rec:.3f}, F1: {f1:.3f}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: EXPONENTIAL SEARCH ===")
print("=" * 80)

"""
Exponential Search combina búsqueda exponencial + binaria.
Útil cuando NO SABES el tamaño de la lista (streams infinitos)
o cuando el elemento está CERCA del inicio.

Algoritmo:
1. Empieza con rango [0, 1].
2. Si lista[rango_derecho] < objetivo, duplica el rango: [0, 2], [0, 4], [0, 8]...
3. Cuando encuentres un rango que contenga el objetivo, aplica binaria.

Complejidad: O(log i) donde i es la POSICIÓN del elemento.
Si el elemento está en posición 8, solo necesitas ~3+3 = 6 pasos.
Regular binary search haría log(N) pasos sobre TODA la lista.
"""

print("\n--- Implementación de Exponential Search ---")

def exponential_search(lista: list, objetivo) -> int:
    """
    O(log i) donde i es la posición del elemento.
    Ideal cuando el elemento está cerca del inicio.
    """
    n = len(lista)
    if n == 0:
        return -1
    
    if lista[0] == objetivo:
        return 0
    
    # Fase 1: encontrar el rango duplicando
    bound = 1
    while bound < n and lista[bound] < objetivo:
        bound *= 2
    
    # Fase 2: búsqueda binaria en el rango [bound//2, min(bound, n-1)]
    izq = bound // 2
    der = min(bound, n - 1)
    
    while izq <= der:
        mid = (izq + der) // 2
        if lista[mid] == objetivo:
            return mid
        elif lista[mid] < objetivo:
            izq = mid + 1
        else:
            der = mid - 1
    
    return -1

datos_exp = list(range(1_000_000))

# Elemento cerca del inicio
inicio = time.perf_counter()
exponential_search(datos_exp, 7)
t_exp_cerca = time.perf_counter() - inicio

# Elemento al final
inicio = time.perf_counter()
exponential_search(datos_exp, 999_990)
t_exp_lejos = time.perf_counter() - inicio

# Comparar con bisect
inicio = time.perf_counter()
bisect.bisect_left(datos_exp, 7)
t_bisect_cerca = time.perf_counter() - inicio

print(f"  Exponential (cerca del inicio):  {t_exp_cerca*1e6:.1f} µs")
print(f"  Exponential (cerca del final):   {t_exp_lejos*1e6:.1f} µs")
print(f"  bisect (siempre log N):          {t_bisect_cerca*1e6:.1f} µs")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: NEAREST NEIGHBOR SEARCH CON BISECT ===")
print("=" * 80)

"""
Encontrar el valor MÁS CERCANO a un target en una lista ordenada.
Esto es la base del K-Nearest Neighbors en 1D.

Con bisect: O(log N) para encontrar el punto de inserción,
luego O(1) para comparar los dos vecinos.
"""

print("\n--- Encontrar el valor más cercano ---")

def valor_mas_cercano(lista_ord: list, target: float) -> float:
    """
    Encuentra el valor más cercano a target en una lista ordenada.
    O(log N).
    """
    if not lista_ord:
        return None
    
    idx = bisect.bisect_left(lista_ord, target)
    
    # Comprobar los dos candidatos: izquierda y derecha del punto de inserción
    candidatos = []
    if idx < len(lista_ord):
        candidatos.append(lista_ord[idx])
    if idx > 0:
        candidatos.append(lista_ord[idx - 1])
    
    return min(candidatos, key=lambda x: abs(x - target))

def k_mas_cercanos(lista_ord: list, target: float, k: int) -> list:
    """
    Encuentra los K valores más cercanos a target.
    O(log N + K).
    """
    idx = bisect.bisect_left(lista_ord, target)
    
    # Expandir desde el punto de inserción hacia ambos lados
    izq, der = idx - 1, idx
    resultado = []
    
    while len(resultado) < k and (izq >= 0 or der < len(lista_ord)):
        dist_izq = abs(lista_ord[izq] - target) if izq >= 0 else float('inf')
        dist_der = abs(lista_ord[der] - target) if der < len(lista_ord) else float('inf')
        
        if dist_izq <= dist_der:
            resultado.append(lista_ord[izq])
            izq -= 1
        else:
            resultado.append(lista_ord[der])
            der += 1
    
    return resultado

# Embedding scores de un modelo
embeddings_1d = sorted([random.gauss(0, 1) for _ in range(10_000)])
query = 0.75

cercano = valor_mas_cercano(embeddings_1d, query)
print(f"Valor más cercano a {query}: {cercano:.4f} (diff: {abs(cercano - query):.6f})")

k_cercanos = k_mas_cercanos(embeddings_1d, query, 5)
print(f"5 más cercanos: {[f'{x:.4f}' for x in k_cercanos]}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: EJERCICIO INTEGRADOR — ROUTER DE CONFIANZA ===")
print("=" * 80)

"""
Ejercicio final: construir un sistema de routing que clasifique
predicciones de ML en diferentes pipelines según su confianza.

- Score < 0.3: Rechazar (alto riesgo de error).
- Score 0.3-0.6: Enviar a revisión humana.
- Score 0.6-0.85: Aceptar con logging.
- Score > 0.85: Aceptar fast-path (alta confianza).
"""

print("\n--- Sistema de routing basado en confianza ---")

class ConfidenceRouter:
    """
    Enruta predicciones a diferentes pipelines según su score.
    Usa bisect para clasificar en O(log K) donde K = número de umbrales.
    Mantiene estadísticas de cada pipeline.
    """
    
    def __init__(self):
        self.umbrales = [0.3, 0.6, 0.85]
        self.rutas = ["RECHAZAR", "REVISIÓN_HUMANA", "ACEPTAR_LOG", "FAST_PATH"]
        self.estadisticas = defaultdict(int)
        self.scores_por_ruta = defaultdict(list)
    
    def clasificar(self, score: float) -> str:
        """Clasifica un score en una ruta. O(log K)."""
        idx = bisect.bisect(self.umbrales, score)
        ruta = self.rutas[idx]
        self.estadisticas[ruta] += 1
        self.scores_por_ruta[ruta].append(score)
        return ruta
    
    def procesar_batch(self, scores: list[float]) -> dict:
        """Procesa un batch completo de scores."""
        resultado = {}
        for i, score in enumerate(scores):
            resultado[i] = {
                "score": score,
                "ruta": self.clasificar(score)
            }
        return resultado
    
    def resumen(self) -> str:
        """Genera resumen de routing."""
        total = sum(self.estadisticas.values())
        lineas = [f"  Total procesados: {total}"]
        for ruta in self.rutas:
            n = self.estadisticas[ruta]
            pct = n / total * 100 if total > 0 else 0
            scores_ruta = self.scores_por_ruta[ruta]
            media = sum(scores_ruta) / len(scores_ruta) if scores_ruta else 0
            lineas.append(f"  {ruta:<20}: {n:>6} ({pct:>5.1f}%) | score medio: {media:.3f}")
        return "\n".join(lineas)

# Simular un stream de predicciones
random.seed(42)
router = ConfidenceRouter()

scores_stream = [random.betavariate(2, 3) for _ in range(10_000)]
router.procesar_batch(scores_stream)

print(router.resumen())

# Stats adicionales
for ruta in router.rutas:
    scores_r = router.scores_por_ruta[ruta]
    if scores_r:
        p50 = sorted(scores_r)[len(scores_r) // 2]
        print(f"  {ruta}: mediana = {p50:.3f}, min = {min(scores_r):.3f}, max = {max(scores_r):.3f}")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN ARQUITECTÓNICA ===")
print("=" * 80)

"""
RESUMEN DE BÚSQUEDAS PARA INGENIERÍA IA:

1. Búsqueda lineal O(N): suficiente para N < 1000 o datos sin orden.

2. Búsqueda binaria O(log N): para datos ordenados y búsquedas repetidas.
   20 pasos para 1 millón de elementos.

3. bisect: la implementación en C. Siempre úsala en vez de tu propia versión.
   bisect_left para la primera ocurrencia, bisect_right para después de la última.

4. Bucketing con bisect: convierte scores continuos en categorías.
   Feature engineering esencial para modelos ML.

5. Two-pointer: transforma O(N²) en O(N) para problemas de pares.

6. Merge: O(N + M) para fusionar datos ordenados de múltiples fuentes.
   heapq.merge para K fuentes en O(N log K).

7. Staircase search: O(N + M) en matrices 2D parcialmente ordenadas.

8. Rangos con bisect: contar en [lo, hi] en O(log N), no O(N).

9. Binary search on answer: buscar el valor óptimo de un parámetro.

10. Exponential search: O(log i) cuando el target está cerca del inicio.

11. K-nearest con bisect+expand: O(log N + K) para vecinos en 1D.

Siguiente archivo: Sorting y Timsort bajo el capó.
"""

print("\n FIN DE ARCHIVO 02_busquedas_y_bisect.")
print(" Dominio de búsquedas eficientes completado.")

