# ===========================================================================
# 04_sets_y_teoria_de_conjuntos.py
# ===========================================================================
# MÓDULO 02: ESTRUCTURAS DE DATOS NATIVAS (AISLADAS)
# ARCHIVO 04: Sets, Frozensets y Teoría de Conjuntos Aplicada a IA
# ===========================================================================
#
# OBJETIVO ABSOLUTO (1000+ LÍNEAS):
# Dominar la estructura Set de Python como una TABLA HASH SIN VALORES.
# En el capítulo de Diccionarios aprendimos que la Key se hashea a un Slot
# mediante la función hash() y la fórmula de probing cuadrático. 
# Un Set es EXACTAMENTE esa mecánica, pero extirpando el Value del par Key:Value.
# Solo quedan las Keys. Esto produce una estructura con:
#   - Búsqueda O(1) (frente al O(N) devastador de las Listas).
#   - Inserción O(1).
#   - Eliminación O(1).
#   - Unión, Intersección, Diferencia, Diferencia Simétrica: O(min(N,M)).
#   - Deduplicación automática (no admite duplicados por definición hash).
#
# EN IA/NLP ESTO ES MORTALMENTE IMPORTANTE:
# - Deduplicar tokens de un corpus de 10 millones de palabras.
# - Calcular la similitud Jaccard entre dos documentos.
# - Verificar si un token pertenece a un vocabulario de 50,000 entradas en O(1).
# - Crear conjuntos de stop-words inmutables con Frozenset.
# - Diferencias simétricas para detectar drift en datasets de producción.
#
# NIVEL: ARQUITECTO ML / NLP ENGINEER. CERO SUPOSICIONES PREVIAS.
# ===========================================================================

import sys
import time
import random
import hashlib
from typing import FrozenSet

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: QUÉ ES UN SET EN CPYTHON (HASH TABLE SIN VALORES) ===")
print("=" * 80)

"""
En el archivo anterior (02_diccionarios) aprendimos:
- Un dict en CPython es un Hash Table con dos arrays internos:
  dk_indices (tabla de slots) y dk_entries (pares hash+key+value).
- La clave se hashea, se mapea a un slot, y se almacena junto a su valor.

Un SET es IDÉNTICO en su motor interno, con UNA diferencia demoledora:
NO EXISTE EL VALUE. Solo existe la KEY.

El código fuente C de CPython (Objects/setobject.c) define:
typedef struct {
    Py_hash_t hash;      // El hash computado de la Key
    PyObject *key;        // Puntero a la Key
} setentry;

Compara esto con la entrada de un diccionario:
typedef struct {
    Py_hash_t me_hash;
    PyObject *me_key;
    PyObject *me_value;   // <-- ESTA LÍNEA NO EXISTE EN SETS
} PyDictKeyEntry;

CONSECUENCIA DIRECTA: 
- Un set consume MENOS MEMORIA que un dict equivalente (falta el puntero de 8 bytes del value).
- La mecánica de colisiones, probing y resize es IDÉNTICA.
- La restricción de hashabilidad es IDÉNTICA: solo puedes meter objetos inmutables.
"""

print("\n--- Anatomía base de un Set vacío ---")

set_vacio_llaves = set()
set_vacio_literal = set()  # NO se puede usar {} porque eso crea un DICT vacío

# TRAMPA CLÁSICA DE ENTREVISTA:
supuesto_set = {}
print(f"¿Qué tipo es '{{}}'? -> {type(supuesto_set)}")  # dict, NO set
print(f"¿Qué tipo es 'set()'? -> {type(set_vacio_llaves)}")  # set

# Para crear un set con contenido, sí puedes usar llaves:
set_con_datos = {1, 2, 3}
print(f"Set con datos {{1,2,3}}: {type(set_con_datos)} -> {set_con_datos}")

print(f"\nMemoria de un Set vacío: {sys.getsizeof(set_vacio_llaves)} bytes")
print(f"Memoria de un Dict vacío: {sys.getsizeof({})} bytes")


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: POR QUÉ UN SET BUSCA EN O(1) Y UNA LISTA EN O(N) ===")
print("=" * 80)

"""
Este concepto es el más importante de todo este archivo para un Ingeniero de IA.

Imagina que tienes un vocabulario de 50,000 palabras (típico en un tokenizer BPE
como el de GPT-2). Tu pipeline NLP recibe un texto y necesita verificar:
"¿Esta palabra está en mi vocabulario?"

OPCIÓN A (Lista - O(N)):
    vocabulario = ["the", "a", "is", ...]  # 50,000 palabras
    if "inteligencia" in vocabulario:       # Python recorre UNA POR UNA las 50,000
        ...
    PEOR CASO: 50,000 comparaciones de strings. Multiplicado por cada palabra del 
    texto de entrada. Si el texto tiene 10,000 palabras:
    50,000 * 10,000 = 500,000,000 operaciones. TU SERVIDOR SE MUERE.

OPCIÓN B (Set - O(1)):
    vocabulario = {"the", "a", "is", ...}  # 50,000 palabras hasheadas
    if "inteligencia" in vocabulario:       # Python hashea "inteligencia", va al slot, DONE.
        ...
    PEOR CASO: 1 operación de hash + 1-2 probes. Multiplicado por 10,000 palabras:
    ~10,000 operaciones. Instantáneo.
"""

print("\n--- Benchmark Real: Lista vs Set en búsqueda masiva ---")

# Construimos un vocabulario de 100,000 palabras aleatorias
random.seed(42)
palabras_aleatorias = [f"token_{i}" for i in range(100_000)]

vocabulario_lista = palabras_aleatorias.copy()
vocabulario_set = set(palabras_aleatorias)

# Generamos 10,000 consultas (mitad existentes, mitad inventadas)
consultas = random.sample(palabras_aleatorias, 5_000) + [f"inexistente_{i}" for i in range(5_000)]
random.shuffle(consultas)

# BENCHMARK LISTA
inicio_lista = time.perf_counter()
encontrados_lista = 0
for palabra in consultas:
    if palabra in vocabulario_lista:
        encontrados_lista += 1
tiempo_lista = time.perf_counter() - inicio_lista

# BENCHMARK SET
inicio_set = time.perf_counter()
encontrados_set = 0
for palabra in consultas:
    if palabra in vocabulario_set:
        encontrados_set += 1
tiempo_set = time.perf_counter() - inicio_set

print(f"  LISTA -> {encontrados_lista} encontrados en {tiempo_lista*1000:.2f} ms")
print(f"  SET   -> {encontrados_set} encontrados en {tiempo_set*1000:.2f} ms")
print(f"  RATIO DE VELOCIDAD: El Set fue ~{tiempo_lista/tiempo_set:.0f}x más rápido")
print(f"  (La diferencia crece EXPONENCIALMENTE con el tamaño del vocabulario)")


print("\n" + "=" * 80)
print("=== CAPÍTULO 3: RESTRICCIÓN DE HASHABILIDAD Y TIPOS PERMITIDOS ===")
print("=" * 80)

"""
Regla idéntica a la de las claves de diccionario (porque el motor interno es el mismo):
SOLO PUEDES METER OBJETOS HASHABLES (INMUTABLES) EN UN SET.

¿Qué es hashable?
Un objeto es hashable si tiene un método __hash__() que devuelve un entero 
constante durante toda su vida, y un método __eq__() para compararse con otros.

HASHABLES (se pueden meter en sets):
- int, float, bool, str, bytes          -> Todos inmutables
- tuple (SOLO si todos sus elementos son hashables también)
- frozenset                              -> Set inmutable (lo veremos después)
- None                                   -> Singleton inmutable

NO HASHABLES (PROHIBIDOS en sets):
- list                                   -> Mutable
- dict                                   -> Mutable
- set                                    -> Mutable (¡un set no puede contener otro set!)
"""

print("\n--- Demostración de restricciones ---")

# Tipos válidos dentro de un set
set_valido_heterogeneo = {42, 3.14, True, "Python", None, (1, 2, 3), b"bytes"}
print(f"Set heterogéneo válido ({len(set_valido_heterogeneo)} items): {set_valido_heterogeneo}")

# CURIOSIDAD AVANZADA: True == 1 y False == 0 en Python (herencia de int).
# El set lo detecta y los trata como duplicados:
set_bool_int = {1, True, 0, False}
print(f"Set con {{1, True, 0, False}}: {set_bool_int}")
# Solo queda {0, 1} porque True==1 y False==0 son el MISMO hash.

# Intentar meter una lista -> EXPLOTA
try:
    set_falla = {[1, 2, 3]}
except TypeError as e:
    print(f"\nIntento de meter lista en set -> TypeError: {e}")

# Intentar meter un dict -> EXPLOTA
try:
    set_falla_dict = { {"key": "value"} }
except TypeError as e:
    print(f"Intento de meter dict en set -> TypeError: {e}")

# Intentar meter un set DENTRO de otro set -> EXPLOTA
try:
    set_interno = {1, 2}
    set_externo = {set_interno}
except TypeError as e:
    print(f"Intento de meter set dentro de set -> TypeError: {e}")

# Tupla con lista interna -> TAMBIÉN EXPLOTA (la lista envenena la hashabilidad)
try:
    tupla_envenenada = (1, 2, [3, 4])
    set_tupla_envenenada = {tupla_envenenada}
except TypeError as e:
    print(f"Tupla con lista interior -> TypeError: {e}")

# Tupla PURA (sin mutables internos) -> FUNCIONA
tupla_pura = (1, 2, (3, 4))
set_tupla_pura = {tupla_pura}
print(f"\nTupla pura anidada dentro de set: {set_tupla_pura}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 4: CREACIÓN, CASTING Y DEDUPLICACIÓN AUTOMÁTICA ===")
print("=" * 80)

"""
La deduplicación automática es el primer superpoder que un Data Engineer de ML usa.
¿Tienes un corpus con 10 millones de tokens donde "the" aparece 500,000 veces?
Convertir esa lista a set() instantáneamente te da el vocabulario único.
"""

print("\n--- Deduplicación instantánea ---")

# Simulación de tokens extraídos de un corpus NLP
corpus_tokens_repetidos = ["el", "gato", "come", "el", "pez", "y", "el", "gato", "duerme",
                           "el", "perro", "come", "el", "pez", "gato", "gato", "gato"]
print(f"Corpus bruto:  {len(corpus_tokens_repetidos)} tokens")

vocabulario_unico = set(corpus_tokens_repetidos)
print(f"Vocabulario único: {vocabulario_unico}")
print(f"Tamaño vocabulario: {len(vocabulario_unico)} palabras únicas")

# ADVERTENCIA CRÍTICA: Los sets NO preservan orden de inserción.
# A diferencia de los dicts (que desde Python 3.7 sí lo preservan),
# los sets son DESORDENADOS por diseño. El orden de iteración depende del hash.
# Si necesitas deduplicar PRESERVANDO ORDEN, usa dict.fromkeys():
vocabulario_ordenado = list(dict.fromkeys(corpus_tokens_repetidos))
print(f"Deduplicado CON orden de inserción preservado: {vocabulario_ordenado}")


print("\n--- Las 5 formas de crear un Set ---")

# 1. Literal con llaves (solo para sets NO vacíos)
set_literal = {10, 20, 30}

# 2. Constructor set() desde cualquier iterable
set_desde_lista = set([1, 2, 3, 2, 1])
set_desde_string = set("inteligencia artificial")  # Cada CARÁCTER se convierte en elemento
set_desde_range = set(range(0, 100, 10))
set_desde_tupla = set((7, 8, 9))

print(f"\nDesde string 'inteligencia artificial': {set_desde_string}")
print(f"  -> Cada carácter es un elemento. Espacios incluidos. Duplicados eliminados.")
print(f"  -> Total caracteres únicos: {len(set_desde_string)}")

# 3. Set Comprehension (equivalente a List Comprehension pero con {})
# Extremadamente útil para filtrado + deduplicación simultánea
numeros_brutos = [1, -3, 5, -7, 2, 5, -3, 8, 1]
set_positivos_unicos = {abs(n) for n in numeros_brutos if n != 0}
print(f"\nSet Comprehension (absolutos, sin cero, únicos): {set_positivos_unicos}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: OPERACIONES MUTADORAS (AÑADIR/ELIMINAR ELEMENTOS) ===")
print("=" * 80)

"""
A diferencia de los diccionarios y listas, los sets NO tienen índices.
No existe set[0] ni set["key"]. Los elementos se localizan por HASH, no por posición.
Esto elimina el concepto de "ordenar" o "acceder por posición".
"""

print("\n--- Adición: .add() y .update() ---")

modelo_tags = {"transformer", "nlp"}
print(f"Inicial: {modelo_tags}")

# .add(elemento) - Añade UN solo elemento. O(1).
# Si ya existe, NO hace nada (idempotente). No lanza error.
modelo_tags.add("generativo")
modelo_tags.add("nlp")  # Ya existe -> ignorado silenciosamente
print(f"Tras .add('generativo') y .add('nlp' duplicado): {modelo_tags}")

# .update(iterable) - Añade MÚLTIPLES elementos desde cualquier iterable. O(len(iterable)).
modelo_tags.update(["bert", "gpt", "nlp"])  # Lista
modelo_tags.update({"attention", "encoder"})  # Otro set
modelo_tags.update("abc")  # String -> añade 'a', 'b', 'c' como caracteres individuales
print(f"Tras .update() masivo: {modelo_tags}")


print("\n--- Eliminación: .remove(), .discard(), .pop(), .clear() ---")

kit_herramientas = {"pytorch", "tensorflow", "jax", "keras", "onnx", "mlflow"}
print(f"\nKit inicial: {kit_herramientas}")

# .remove(elem) - Elimina el elemento. Si NO EXISTE, lanza KeyError.
# PELIGROSO en producción si no estás seguro de que existe.
kit_herramientas.remove("tensorflow")
print(f"Tras .remove('tensorflow'): {kit_herramientas}")

try:
    kit_herramientas.remove("caffe")  # No existe
except KeyError as e:
    print(f"¡EXPLOSIÓN! .remove() de elemento inexistente: KeyError {e}")

# .discard(elem) - Elimina el elemento. Si NO EXISTE, NO hace nada. Silencioso.
# SIEMPRE PREFERIBLE en pipelines de producción ML.
kit_herramientas.discard("caffe")  # No existe -> silencio total
kit_herramientas.discard("keras")  # Existe -> eliminado
print(f"Tras .discard('caffe' inexistente + 'keras'): {kit_herramientas}")

# .pop() - Extrae y devuelve un elemento ARBITRARIO. 
# NO es el último, NO es el primero, NO hay garantía de orden.
# Útil para consumir sets iterativamente (ej: tareas pendientes).
elemento_extraido = kit_herramientas.pop()
print(f"Elemento extraído aleatoriamente con .pop(): '{elemento_extraido}'")
print(f"Set restante: {kit_herramientas}")

# .clear() - Vacía el set completamente. Lo deja en set() vacío.
copia_kit = kit_herramientas.copy()
copia_kit.clear()
print(f"Tras .clear(): {copia_kit} (len={len(copia_kit)})")


print("\n" + "=" * 80)
print("=== CAPÍTULO 6: ÁLGEBRA DE CONJUNTOS (UNIÓN, INTERSECCIÓN, DIFERENCIA) ===")
print("=" * 80)

"""
Aquí es donde los Sets se convierten en la HERRAMIENTA MATEMÁTICA más poderosa
de todo Python para un Ingeniero de IA. Las operaciones de conjuntos del Álgebra
están implementadas NATIVAMENTE en C dentro de CPython.

Contexto IA Real:
- UNIÓN:       "¿Cuál es el vocabulario TOTAL si combino corpus A y corpus B?"
- INTERSECCIÓN: "¿Qué palabras comparten ambos documentos?" (base de Jaccard Similarity)
- DIFERENCIA:  "¿Qué tokens tiene el dataset de producción que NO estaban en training?"
- SIMÉTRICA:   "¿Qué tokens son EXCLUSIVOS de cada dataset?" (drift detection)
"""

# Corpus de dos documentos NLP
doc_a_tokens = {"machine", "learning", "is", "the", "future", "of", "ai"}
doc_b_tokens = {"deep", "learning", "is", "a", "subset", "of", "machine", "ai"}

print(f"\nDoc A tokens: {doc_a_tokens}")
print(f"Doc B tokens: {doc_b_tokens}")

# ─── 6.1 UNIÓN (A ∪ B): Todos los tokens de ambos, sin duplicados ───
union_metodo = doc_a_tokens.union(doc_b_tokens)
union_operador = doc_a_tokens | doc_b_tokens  # Operador pipe equivalente

print(f"\nUNIÓN (vocabulario total combinado): {union_operador}")
print(f"  Total tokens únicos combinados: {len(union_operador)}")

# ─── 6.2 INTERSECCIÓN (A ∩ B): Solo los tokens que AMBOS comparten ───
interseccion_metodo = doc_a_tokens.intersection(doc_b_tokens)
interseccion_operador = doc_a_tokens & doc_b_tokens  # Operador ampersand

print(f"\nINTERSECCIÓN (tokens compartidos): {interseccion_operador}")
print(f"  Tokens en común: {len(interseccion_operador)}")

# ─── 6.3 DIFERENCIA (A - B): Tokens que están en A pero NO en B ───
diferencia_a_menos_b = doc_a_tokens - doc_b_tokens
diferencia_b_menos_a = doc_b_tokens - doc_a_tokens

print(f"\nDIFERENCIA A-B (exclusivos de A): {diferencia_a_menos_b}")
print(f"DIFERENCIA B-A (exclusivos de B): {diferencia_b_menos_a}")

# ─── 6.4 DIFERENCIA SIMÉTRICA (A △ B): Los que NO comparten ninguno ───
# Equivale a (A - B) ∪ (B - A). Los elementos que están en uno u otro, pero NO en ambos.
simetrica_operador = doc_a_tokens ^ doc_b_tokens
simetrica_metodo = doc_a_tokens.symmetric_difference(doc_b_tokens)

print(f"\nDIFERENCIA SIMÉTRICA (exclusivos de cada uno): {simetrica_operador}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 7: MÉTRICAS DE SIMILITUD NLP CON SETS (JACCARD INDEX) ===")
print("=" * 80)

"""
La SIMILITUD DE JACCARD (Jaccard Index / Jaccard Similarity) es una de las métricas
más antiguas y robustas del NLP y del Information Retrieval. Se usa para:
- Medir la similitud entre dos textos/documentos.
- Detección de duplicados (near-duplicate detection).
- Clustering de documentos.
- Evaluación de la calidad de un sistema RAG.

FÓRMULA MATEMÁTICA:
    J(A, B) = |A ∩ B| / |A ∪ B|

Si J = 1.0 -> Los documentos tienen exactamente el mismo vocabulario.
Si J = 0.0 -> No comparten ni una sola palabra.

Toda esta fórmula se implementa en 1 línea de Python usando Sets.
"""

print("\n--- Implementación Jaccard de Producción con Sets ---")

def jaccard_similarity(texto_a: str, texto_b: str) -> float:
    """
    Calcula la similitud Jaccard entre dos textos.
    Tokenización básica por espacios (en producción usarías un tokenizer BPE).
    """
    set_a = set(texto_a.lower().split())
    set_b = set(texto_b.lower().split())
    
    interseccion = len(set_a & set_b)
    union = len(set_a | set_b)
    
    if union == 0:
        return 0.0
    
    return interseccion / union

# Ejemplo con documentos de prueba
doc_1 = "el gato negro duerme sobre la alfombra roja"
doc_2 = "el perro negro duerme sobre la cama azul"
doc_3 = "python es un lenguaje de programación potente"

sim_1_2 = jaccard_similarity(doc_1, doc_2)
sim_1_3 = jaccard_similarity(doc_1, doc_3)
sim_2_3 = jaccard_similarity(doc_2, doc_3)

print(f"Jaccard(doc1, doc2) = {sim_1_2:.4f}  [Esperado: alto, comparten estructura]")
print(f"Jaccard(doc1, doc3) = {sim_1_3:.4f}  [Esperado: bajo/cero, temas distintos]")
print(f"Jaccard(doc2, doc3) = {sim_2_3:.4f}  [Esperado: bajo/cero, temas distintos]")


print("\n--- Detección de Drift en Datasets (Producción MLOps) ---")

vocabulario_training = {"gato", "perro", "casa", "coche", "mesa", "silla", "agua", "pan"}
vocabulario_produccion = {"gato", "perro", "drone", "criptomoneda", "blockchain", "agua", "pan"}

tokens_nuevos_no_vistos = vocabulario_produccion - vocabulario_training
tokens_desaparecidos = vocabulario_training - vocabulario_produccion
drift_simetrico = vocabulario_training ^ vocabulario_produccion

jaccard_drift = jaccard_similarity(
    " ".join(vocabulario_training), 
    " ".join(vocabulario_produccion)
)

print(f"\nTokens NUEVOS en producción (no vistos en training): {tokens_nuevos_no_vistos}")
print(f"Tokens DESAPARECIDOS de producción: {tokens_desaparecidos}")
print(f"Drift total simétrico: {drift_simetrico}")
print(f"Jaccard (vocabulario train vs prod): {jaccard_drift:.4f}")
print(f"  -> Si Jaccard < 0.5, tu modelo probablemente necesita re-entrenamiento urgente.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: PREDICADOS DE SUBCONJUNTOS (ISSUBSET, ISSUPERSET, ISDISJOINT) ===")
print("=" * 80)

"""
Los predicados booleanos de subconjuntos son vitales para validar:
- ¿Mi vocabulario de test está CONTENIDO en el de training? (Si no, hay data leakage inverso).
- ¿Dos categorías de clasificación son COMPLETAMENTE DISJUNTAS? (Si no, hay solapamiento de clases).
"""

print("\n--- Relaciones de inclusión ---")

set_padre = {"a", "b", "c", "d", "e"}
set_hijo = {"a", "c", "e"}
set_ajeno = {"x", "y", "z"}

# .issubset(otro) o <=  ->  "¿Todos mis elementos están en el otro?"
print(f"¿{set_hijo} es subconjunto de {set_padre}? {set_hijo.issubset(set_padre)}")  # True
print(f"¿{set_hijo} es subconjunto de {set_padre}? {set_hijo <= set_padre}")          # True (operador)

# .issuperset(otro) o >=  ->  "¿Contiene todos los elementos del otro?"
print(f"¿{set_padre} es superconjunto de {set_hijo}? {set_padre.issuperset(set_hijo)}")  # True
print(f"¿{set_padre} es superconjunto de {set_hijo}? {set_padre >= set_hijo}")            # True

# Subconjunto ESTRICTO (< y >): Todos los elementos están incluidos Y hay elementos extra
print(f"¿Subconjunto estricto (hijo < padre)? {set_hijo < set_padre}")   # True
print(f"¿Subconjunto estricto (padre < padre)? {set_padre < set_padre}") # False (son iguales)

# .isdisjoint(otro)  ->  "¿NO comparten absolutamente NINGÚN elemento?"
print(f"\n¿{set_hijo} y {set_ajeno} son disjuntos? {set_hijo.isdisjoint(set_ajeno)}")  # True
print(f"¿{set_hijo} y {set_padre} son disjuntos? {set_hijo.isdisjoint(set_padre)}")    # False


print("\n--- Caso MLOps: Validar integridad de splits Train/Val/Test ---")

ids_train = {1, 2, 3, 4, 5, 6, 7, 8}
ids_val   = {9, 10, 11}
ids_test  = {12, 13, 14}

# REGLA DE ORO: Los splits DEBEN ser disjuntos. Si no, hay DATA LEAKAGE.
train_val_disjoint = ids_train.isdisjoint(ids_val)
train_test_disjoint = ids_train.isdisjoint(ids_test)
val_test_disjoint = ids_val.isdisjoint(ids_test)

print(f"Train ∩ Val  = ∅? {train_val_disjoint}")
print(f"Train ∩ Test = ∅? {train_test_disjoint}")
print(f"Val   ∩ Test = ∅? {val_test_disjoint}")

if all([train_val_disjoint, train_test_disjoint, val_test_disjoint]):
    print("✓ Validación PASADA: Cero data leakage entre splits.")
else:
    print("✗ ALERTA CRÍTICA: Data leakage detectado. Modelo comprometido.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 9: ACTUALIZACIÓN IN-PLACE CON OPERADORES DE ASIGNACIÓN ===")
print("=" * 80)

"""
Igual que los dicts tienen |= (PEP 584), los sets tienen versiones in-place
de todas las operaciones de álgebra de conjuntos. Esto es critical para 
pipelines de streaming donde vas acumulando tokens en un vocabulario vivo.
"""

vocab_acumulado = {"the", "is", "a"}
print(f"\nVocabulario inicial: {vocab_acumulado}")

# |= (Update/Union in-place)
vocab_acumulado |= {"learning", "deep", "the"}  # "the" ya existe, ignorado
print(f"Tras |= union batch 1: {vocab_acumulado}")

# &= (Intersection update in-place) - SOLO RETIENE los que están en ambos
filtro_permitidos = {"the", "deep", "learning", "model"}
vocab_filtrado = vocab_acumulado.copy()
vocab_filtrado &= filtro_permitidos
print(f"Tras &= intersection con filtro: {vocab_filtrado}")

# -= (Difference update in-place) - ELIMINA los del segundo set
stopwords = {"the", "is", "a"}
vocab_limpio = vocab_acumulado.copy()
vocab_limpio -= stopwords
print(f"Tras -= eliminación de stopwords: {vocab_limpio}")

# ^= (Symmetric difference update in-place) - RETIENE solo los exclusivos de cada uno
set_x = {1, 2, 3, 4}
set_y = {3, 4, 5, 6}
set_x ^= set_y
print(f"Tras ^= simétrica: {set_x}")  # {1, 2, 5, 6}


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: FROZENSET (EL SET INMUTABLE PARA CLAVES DE DICT Y CACHING) ===")
print("=" * 80)

"""
Problema desbloqueado:
En el Capítulo 3 vimos que un set normal NO SE PUEDE meter dentro de otro set,
ni usarse como clave de un diccionario, porque es MUTABLE (y por tanto no hashable).

¿Y si necesitas un CONJUNTO como clave de un dict?
Ejemplo real: Tienes un sistema de caché donde la clave es un conjunto de features
seleccionadas, y el valor es el accuracy del modelo entrenado con esas features.
{"altura", "peso", "edad"} -> 0.95
{"altura", "peso"} -> 0.88

Para esto existe FROZENSET: un set CONGELADO, INMUTABLE, HASHABLE.
Tiene TODAS las operaciones de lectura del set (unión, intersección, etc.)
pero NINGUNA operación de escritura (.add, .remove, .discard -> NO EXISTEN).
"""

print("\n--- Frozenset como clave de diccionario ---")

# Caché de resultados de Feature Selection en AutoML
cache_feature_selection = {}

features_v1 = frozenset({"altura", "peso", "edad"})
features_v2 = frozenset({"altura", "peso"})
features_v3 = frozenset({"edad", "ingresos", "zona"})

cache_feature_selection[features_v1] = {"accuracy": 0.95, "f1": 0.93}
cache_feature_selection[features_v2] = {"accuracy": 0.88, "f1": 0.85}
cache_feature_selection[features_v3] = {"accuracy": 0.72, "f1": 0.69}

print("Cache de Feature Selection:")
for features, metricas in cache_feature_selection.items():
    print(f"  {set(features)} -> Accuracy: {metricas['accuracy']}")

# Búsqueda O(1) en la caché
consulta = frozenset({"peso", "altura", "edad"})  # MISMO contenido que v1, distinto orden
print(f"\nBúsqueda de {set(consulta)}: {cache_feature_selection.get(consulta)}")
print("  -> ¡Funciona! El orden NO importa. El hash del frozenset depende del CONTENIDO, no del orden.")


print("\n--- Frozenset dentro de otro Set ---")

# Necesitas un conjunto de CONJUNTOS (ej: todas las combinaciones de features probadas)
combinaciones_probadas = set()
combinaciones_probadas.add(frozenset({"a", "b"}))
combinaciones_probadas.add(frozenset({"b", "c"}))
combinaciones_probadas.add(frozenset({"a", "b"}))  # Duplicado -> ignorado

print(f"\nConjunto de conjuntos: {combinaciones_probadas}")
print(f"  Total combinaciones únicas: {len(combinaciones_probadas)}")


print("\n--- Frozenset: operaciones de lectura permitidas ---")

fs_a = frozenset({1, 2, 3, 4})
fs_b = frozenset({3, 4, 5, 6})

print(f"\nUnión:               {fs_a | fs_b}")
print(f"Intersección:        {fs_a & fs_b}")
print(f"Diferencia:          {fs_a - fs_b}")
print(f"Simétrica:           {fs_a ^ fs_b}")
print(f"Es subconjunto:      {frozenset({1,2}).issubset(fs_a)}")

# Operaciones de ESCRITURA -> PROHIBIDAS
try:
    fs_a.add(99)
except AttributeError as e:
    print(f"\n.add() en frozenset -> AttributeError: {e}")
    print("  -> Frozenset NO tiene .add(), .remove(), .discard(), .update(), .pop(), .clear()")


print("\n" + "=" * 80)
print("=== CAPÍTULO 11: SET COMPREHENSIONS Y PATRONES AVANZADOS DE FILTRADO ===")
print("=" * 80)

"""
Las Set Comprehensions son idénticas en sintaxis a las List Comprehensions,
pero usan llaves {} en vez de corchetes []. Son la forma más Pythonica de
construir vocabularios filtrados, conjuntos de IDs válidos, etc.
"""

print("\n--- Extracción de vocabulario con filtrado ---")

corpus_crudo = """
El aprendizaje profundo es una rama del machine learning que utiliza 
redes neuronales artificiales con múltiples capas para aprender 
representaciones de datos. El deep learning ha revolucionado campos 
como el procesamiento del lenguaje natural y la visión por computadora.
"""

# Extraemos vocabulario único en minúsculas, filtrando palabras cortas (< 3 chars)
# y eliminando puntuación básica
import string

vocabulario_filtrado = {
    palabra.strip(string.punctuation).lower()
    for palabra in corpus_crudo.split()
    if len(palabra.strip(string.punctuation)) >= 3
}

print(f"Vocabulario filtrado (≥3 chars, lowercase, sin puntuación):")
print(f"  {vocabulario_filtrado}")
print(f"  Total: {len(vocabulario_filtrado)} palabras únicas")


print("\n--- Generación de N-gramas únicos con Sets ---")

def extraer_ngramas_unicos(texto: str, n: int) -> set:
    """Extrae todos los n-gramas de caracteres únicos de un texto."""
    texto_limpio = texto.lower().replace(" ", "_")
    return {texto_limpio[i:i+n] for i in range(len(texto_limpio) - n + 1)}

bigramas = extraer_ngramas_unicos("deep learning", 2)
trigramas = extraer_ngramas_unicos("deep learning", 3)

print(f"\nBigramas únicos de 'deep learning': {bigramas}")
print(f"Trigramas únicos de 'deep learning': {trigramas}")

# Comparar n-gramas entre dos textos (fingerprinting de similitud)
ng_a = extraer_ngramas_unicos("machine learning", 3)
ng_b = extraer_ngramas_unicos("machine translation", 3)
similitud_ngramas = len(ng_a & ng_b) / len(ng_a | ng_b) if ng_a | ng_b else 0

print(f"\nSimilitud por trigramas entre 'machine learning' y 'machine translation': {similitud_ngramas:.4f}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: RESIZE INTERNO Y PERFILADO DE MEMORIA ===")
print("=" * 80)

"""
Al igual que los diccionarios, los sets tienen un factor de carga (load factor)
del ~66% (~2/3). Cuando el set supera ese umbral, CPython dispara un RESIZE
que duplica la tabla hash interna y RE-HASHEA todos los elementos.

Esto es importante para Data Engineers que acumulan IDs de documentos procesados
en un set en streaming: el resize causa picos de memoria y latencia.
"""

print("\n--- Perfilado de Resizes internos ---")

set_creciente = set()
peso_previo = sys.getsizeof(set_creciente)
resizes = 0

for i in range(50_000):
    set_creciente.add(f"token_{i}")
    peso_actual = sys.getsizeof(set_creciente)
    
    if peso_actual > peso_previo:
        if resizes < 6:
            print(f"  [Set Resize] al insertar token_{i}: {peso_previo} -> {peso_actual} bytes "
                  f"(+{peso_actual - peso_previo} bytes)")
        resizes += 1
        peso_previo = peso_actual

print(f"  ... Total resizes para 50,000 inserciones: {resizes}")
print(f"  Tamaño final del set en memoria: {sys.getsizeof(set_creciente) / 1024:.1f} KB")

# Pre-sizing tip: si sabes cuántos elementos vas a meter, no hay forma nativa de 
# pre-reservar como en C++ (unordered_set::reserve). Pero puedes minimizar el impacto
# construyendo el set DE GOLPE desde un generador en vez de .add() iterativo.


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: ERRORES COMUNES Y ANTIPATRONES EN PRODUCCIÓN ===")
print("=" * 80)

"""
Recopilación de los bugs más devastadores que he visto en código ML real
relacionados con sets.
"""

print("\n--- ANTIPATRÓN 1: Iterar y modificar simultáneamente ---")

numeros = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
# ESTO EXPLOTA (igual que con dicts):
# for n in numeros:
#     if n % 2 == 0:
#         numeros.remove(n)  # RuntimeError: Set changed size during iteration

# SOLUCIÓN: Crear copia congelada para iterar
numeros_copia = numeros.copy()
for n in numeros_copia:
    if n % 2 == 0:
        numeros.remove(n)
print(f"Set tras eliminar pares (iterando sobre copia): {numeros}")


print("\n--- ANTIPATRÓN 2: Confiar en el orden de iteración ---")

# Los sets NO garantizan orden. Si tu pipeline depende de procesar 
# elementos en un orden específico, NO uses un set.
# En su lugar: sorted(mi_set) para obtener una lista ordenada.
desordenado = {"z", "a", "m", "b"}
print(f"Iteración directa (orden impredecible): {list(desordenado)}")
print(f"Iteración ordenada: {sorted(desordenado)}")


print("\n--- ANTIPATRÓN 3: Usar set() para deduplicar datos con contexto ---")

# Si tienes registros con más información que la clave de deduplicación,
# set() te pierde todo el contexto. Usa un dict para deduplicar preservando datos.
registros = [
    {"id": 1, "texto": "hola", "score": 0.9},
    {"id": 1, "texto": "hola", "score": 0.95},  # Duplicado con mejor score
    {"id": 2, "texto": "adiós", "score": 0.8},
]

# MAL: set() no funciona con dicts (no son hashables)
# BIEN: dict keyed por ID, quedándote con el mejor score
deduplicado = {}
for reg in registros:
    if reg["id"] not in deduplicado or reg["score"] > deduplicado[reg["id"]]["score"]:
        deduplicado[reg["id"]] = reg

print(f"Deduplicado inteligente (mejor score por ID): {list(deduplicado.values())}")



print("\n" + "=" * 80)
print("=== CAPÍTULO 14: MINHASH — SIMILITUD A ESCALA MASIVA (LOCALITY-SENSITIVE HASHING) ===")
print("=" * 80)

"""
Jaccard Similarity funciona perfecto con sets pequeños. ¿Pero qué pasa cuando 
tienes 10 MILLONES de documentos y necesitas encontrar los duplicados cercanos?
Calcular Jaccard entre cada par es O(N²) -> 10M² = 100 TRILLONES de comparaciones.
Imposible.

La solución industrial se llama MINHASH (Min-wise Independent Permutations).
Es un algoritmo de Locality-Sensitive Hashing (LSH) que APROXIMA la similitud
Jaccard sin calcularla exactamente. La idea:

1. Defines K funciones hash diferentes (ej: K=100).
2. Para cada documento, aplicas cada hash a todos sus elementos.
3. Para cada función hash, guardas SOLO el valor MÍNIMO (de ahí "MinHash").
4. La firma (signature) del documento es un vector de K valores mínimos.
5. La probabilidad de que dos documentos tengan el mismo mínimo para una 
   función hash dada es EXACTAMENTE su Jaccard Similarity.

Esto reduce cada documento de un set de tamaño variable a un vector fijo de K ints.
Comparar dos vectores de 100 ints es instantáneo.
"""

print("\n--- Implementación didáctica de MinHash con Sets ---")

def crear_funciones_hash(num_funciones: int, primo: int = 2147483647):
    """
    Genera num_funciones hash de la familia universal:
    h(x) = (a*x + b) % primo
    donde a y b son aleatorios.
    """
    funciones = []
    random.seed(12345)  # Reproducibilidad
    for _ in range(num_funciones):
        a = random.randint(1, primo - 1)
        b = random.randint(0, primo - 1)
        funciones.append((a, b, primo))
    return funciones

def calcular_minhash_signature(conjunto: set, funciones_hash: list) -> list:
    """
    Calcula la firma MinHash de un conjunto.
    Para cada función hash, encuentra el mínimo hash de todos los elementos.
    """
    signature = []
    for a, b, p in funciones_hash:
        min_hash = float('inf')
        for elem in conjunto:
            # Hasheamos el hash del elemento (que es un int)
            h = (a * hash(elem) + b) % p
            if h < min_hash:
                min_hash = h
        signature.append(min_hash)
    return signature

def jaccard_minhash_aproximado(sig_a: list, sig_b: list) -> float:
    """Estima Jaccard comparando las K posiciones de las firmas."""
    coincidencias = sum(1 for a, b in zip(sig_a, sig_b) if a == b)
    return coincidencias / len(sig_a)

# Creamos dos documentos con solapamiento conocido
doc_x = {"machine", "learning", "is", "amazing", "and", "powerful", "technology"}
doc_y = {"machine", "learning", "is", "incredible", "and", "transformative", "technology"}

# Jaccard exacto para comparar
jaccard_real = len(doc_x & doc_y) / len(doc_x | doc_y)

# MinHash con K=200 funciones hash
K = 200
funciones = crear_funciones_hash(K)
sig_x = calcular_minhash_signature(doc_x, funciones)
sig_y = calcular_minhash_signature(doc_y, funciones)

jaccard_estimado = jaccard_minhash_aproximado(sig_x, sig_y)

print(f"  Jaccard EXACTO (sets):     {jaccard_real:.4f}")
print(f"  Jaccard ESTIMADO (MinHash): {jaccard_estimado:.4f}")
print(f"  Error absoluto:            {abs(jaccard_real - jaccard_estimado):.4f}")
print(f"  (Con K={K} hashes, el error típico es < {1/K**0.5:.3f})")
print(f"  En producción: Spotify, Google, Pinterest usan MinHash+LSH para deduplicar contenido.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: PATRONES MULTISET (FRECUENCIA vs PERTENENCIA) ===")
print("=" * 80)

"""
Un set puro solo responde SÍ/NO a la pregunta "¿existe este elemento?".
No cuenta cuántas veces aparece. Esto es un problema en NLP donde la 
FRECUENCIA de un token es tan importante como su existencia.

Para esto existe collections.Counter (que veremos en profundidad en el 
siguiente archivo 05_collections_profundo.py). Pero aquí establecemos 
el puente conceptual entre Set (existencia) y Counter (frecuencia).
"""

print("\n--- El problema de la frecuencia ignorada ---")

texto_analizar = "el gato el perro el gato el gato"
tokens = texto_analizar.split()

# Set: pierde la frecuencia
set_tokens = set(tokens)
print(f"Set (solo existencia): {set_tokens}")  # {'el', 'gato', 'perro'}

# Para conservar frecuencia, usamos un dict manualmente (antes de conocer Counter):
frecuencias = {}
for token in tokens:
    frecuencias[token] = frecuencias.get(token, 0) + 1

print(f"Frecuencias manuales (dict): {frecuencias}")

# Ahora podemos combinar AMBOS: Set para existencia rápida + Dict para frecuencia
vocabulario_rapido = set(frecuencias.keys())  # O(1) lookup
print(f"¿'gato' existe? {('gato' in vocabulario_rapido)}  ¿Cuántas veces? {frecuencias.get('gato', 0)}")
print(f"¿'avión' existe? {('avión' in vocabulario_rapido)}  ¿Cuántas veces? {frecuencias.get('avión', 0)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 16: EJERCICIO COMPLETO — PIPELINE NLP DE COMPARACIÓN DE DOCUMENTOS ===")
print("=" * 80)

"""
Ejercicio integrador que combina TODO lo aprendido en este archivo.
Construimos un mini motor de búsqueda que:
1. Tokeniza documentos.
2. Elimina stopwords usando un FROZENSET.
3. Calcula Jaccard entre el query y cada documento.
4. Devuelve los documentos más relevantes.
"""

print("\n--- Motor de búsqueda por similitud de conjuntos ---")

# Stopwords como FROZENSET (inmutable, hashable, eficiente)
STOPWORDS_ES = frozenset({
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "al", "a", "en", "con", "por", "para",
    "y", "o", "que", "es", "son", "se", "su", "como",
    "más", "pero", "no", "si", "ya", "ha", "fue", "ser",
    "está", "están", "este", "esta", "estos", "estas",
    "muy", "también", "sobre", "entre", "desde", "hasta",
})

def tokenizar_y_limpiar(texto: str, stopwords: FrozenSet[str] = STOPWORDS_ES) -> set:
    """
    Tokeniza un texto, convierte a minúsculas, elimina puntuación y stopwords.
    Retorna un SET de tokens únicos limpios.
    """
    tokens_brutos = texto.lower().split()
    tokens_limpios = set()
    for token in tokens_brutos:
        # Eliminar puntuación de los extremos
        token_limpio = token.strip(string.punctuation)
        # Filtrar: no vacío, no stopword, longitud mínima 2
        if token_limpio and token_limpio not in stopwords and len(token_limpio) >= 2:
            tokens_limpios.add(token_limpio)
    return tokens_limpios

def buscar_documentos(query: str, corpus: dict, top_n: int = 3) -> list:
    """
    Busca los documentos más similares al query usando Jaccard Similarity.
    corpus: dict {id_doc: texto_completo}
    Retorna lista de tuplas (id_doc, score) ordenada por relevancia.
    """
    tokens_query = tokenizar_y_limpiar(query)
    
    if not tokens_query:
        return []
    
    resultados = []
    for doc_id, texto_doc in corpus.items():
        tokens_doc = tokenizar_y_limpiar(texto_doc)
        
        if not tokens_doc:
            continue
        
        # Jaccard puro con sets
        interseccion = len(tokens_query & tokens_doc)
        union = len(tokens_query | tokens_doc)
        score = interseccion / union if union > 0 else 0.0
        
        # Información adicional para debug
        palabras_comunes = tokens_query & tokens_doc
        
        resultados.append({
            "doc_id": doc_id,
            "score": score,
            "palabras_comunes": palabras_comunes,
            "tokens_doc": len(tokens_doc),
        })
    
    # Ordenar por score descendente
    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados[:top_n]

# Corpus de prueba
corpus_documentos = {
    "D001": "El aprendizaje profundo utiliza redes neuronales para reconocer patrones en datos masivos",
    "D002": "Python es un lenguaje de programación muy popular para la inteligencia artificial",
    "D003": "Las redes neuronales convolucionales son excelentes para el reconocimiento de imágenes",
    "D004": "El procesamiento del lenguaje natural permite a las máquinas entender texto humano",
    "D005": "Los transformers han revolucionado el campo del procesamiento de lenguaje natural",
    "D006": "La cocina mediterránea es famosa por el uso de aceite de oliva y tomates frescos",
    "D007": "El entrenamiento de modelos grandes requiere GPUs potentes y muchos datos de texto",
}

# Búsqueda
query_usuario = "redes neuronales para reconocimiento de patrones"
print(f"\nQuery: '{query_usuario}'")
print(f"Tokens del query (limpios): {tokenizar_y_limpiar(query_usuario)}")
print(f"\nResultados:")

resultados = buscar_documentos(query_usuario, corpus_documentos)
for i, r in enumerate(resultados, 1):
    print(f"  #{i} [{r['doc_id']}] Score: {r['score']:.4f}")
    print(f"      Palabras en común: {r['palabras_comunes']}")
    print(f"      Texto: '{corpus_documentos[r['doc_id']][:80]}...'")

# Segunda búsqueda para verificar
query_2 = "procesamiento de lenguaje natural y transformers"
print(f"\nQuery 2: '{query_2}'")
resultados_2 = buscar_documentos(query_2, corpus_documentos)
for i, r in enumerate(resultados_2, 1):
    print(f"  #{i} [{r['doc_id']}] Score: {r['score']:.4f} | Común: {r['palabras_comunes']}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 17: REFERENCIA RÁPIDA DE COMPLEJIDAD TEMPORAL ===")
print("=" * 80)

"""
TABLA DE COMPLEJIDAD DE TODAS LAS OPERACIONES DE SET EN CPYTHON:

╔═══════════════════════════════════╦═══════════════╗
║ OPERACIÓN                         ║ COMPLEJIDAD   ║
╠═══════════════════════════════════╬═══════════════╣
║ x in s                            ║ O(1) promedio ║
║ s.add(x)                          ║ O(1) promedio ║
║ s.remove(x)                       ║ O(1) promedio ║
║ s.discard(x)                      ║ O(1) promedio ║
║ s.pop()                           ║ O(1)          ║
║ len(s)                            ║ O(1)          ║
║ s.clear()                         ║ O(N)          ║
║ s.copy()                          ║ O(N)          ║
║ s | t  (unión)                    ║ O(len(s)+len(t))║
║ s & t  (intersección)             ║ O(min(s,t))   ║
║ s - t  (diferencia)               ║ O(len(s))     ║
║ s ^ t  (simétrica)                ║ O(len(s)+len(t))║
║ s <= t (subconjunto)              ║ O(len(s))     ║
║ s >= t (superconjunto)            ║ O(len(t))     ║
║ s.isdisjoint(t)                   ║ O(min(s,t))   ║
║ set(iterable) [construcción]      ║ O(N)          ║
╚═══════════════════════════════════╩═══════════════╝

NOTA: "O(1) promedio" significa O(1) amortizado. En el peor caso teórico
(todas las claves colisionan al mismo slot), degrada a O(N). Pero la 
función hash de CPython está diseñada para que esto sea estadísticamente
imposible en la práctica.
"""

# Demostración de que O(1) se mantiene incluso con sets enormes
print("\n--- Verificación O(1) en sets de 1M de elementos ---")

set_millon = set(range(1_000_000))

# Búsqueda de algo que existe (peor caso de recorrido si fuera lista)
inicio = time.perf_counter()
for _ in range(100_000):
    _ = 999_999 in set_millon  # Último elemento
fin = time.perf_counter()
print(f"  100K búsquedas del elemento #999,999 en set de 1M: {(fin-inicio)*1000:.2f} ms")

# Búsqueda de algo que NO existe
inicio = time.perf_counter()
for _ in range(100_000):
    _ = -1 in set_millon  # No existe
fin = time.perf_counter()
print(f"  100K búsquedas de elemento inexistente en set de 1M: {(fin-inicio)*1000:.2f} ms")
print(f"  -> Ambas son O(1). No importa si el set tiene 100 o 10M de elementos.")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN ARQUITECTÓNICA DEFINITIVA ===")
print("=" * 80)

"""
RESUMEN DEFINITIVO DE SETS PARA INGENIERÍA IA:

1. Un Set es un HASH TABLE SIN VALORES. Motor C idéntico al dict.
   Búsqueda, inserción, eliminación: TODO O(1).

2. SIEMPRE que necesites verificar "¿existe X en mi colección?", convierte 
   tu lista a set. La diferencia entre O(N) y O(1) es la diferencia entre 
   un servidor que aguanta y uno que se cae.

3. Las operaciones de ÁLGEBRA DE CONJUNTOS (unión, intersección, diferencia)
   son la base de métricas NLP como Jaccard Similarity, detección de drift
   en vocabularios, y validación de integridad de splits train/val/test.

4. FROZENSET es la versión inmutable. Úsalo como clave de diccionario cuando
   necesites cachear resultados indexados por conjuntos de features.

5. Los sets NO preservan orden. Si necesitas orden, usa dict.fromkeys() para
   deduplicar o sorted() para iterar.

6. NUNCA modifiques un set mientras iteras sobre él. Crea una copia primero.

7. El factor de carga es ~66%. Resizes internos son inevitables pero se 
   minimizan construyendo el set de golpe (set(generador)) en vez de .add()
   iterativo.

8. MINHASH permite escalar la similitud Jaccard a millones de documentos
   reduciendo cada set a un vector fijo de K hashes mínimos.

9. Los sets son para EXISTENCIA. Si necesitas FRECUENCIA, combiná set (lookup
   rápido) con dict (conteo) o directamente usa collections.Counter (siguiente archivo).
"""

print("\n FIN DE ARCHIVO 04_sets_y_teoria_de_conjuntos.")
print(" La estructura Hash sin valores ha sido conquistada. Siguiente: Collections Profundo.")

