# ===========================================================================
# 03_tuplas_e_inmutabilidad_estricta.py
# ===========================================================================
# MÓDULO 02: ESTRUCTURAS DE DATOS NATIVAS (AISLADAS)
# ARCHIVO 03: Tuplas, Inmutabilidades Falsas y Arquitectura de Tipado
# ===========================================================================
#
# OBJETIVO DE INGENIERÍA PURA:
# Destruiremos el falso concepto de que una Tupla es una Lista Inmutable y 
# le otorgaremos su estatus real: El Registro de Datos de CPython (Struct C).
#
# Entenderemos por qué el Intérprete (AST) optimiza y regala memoria en su 
# instanciación (`Constant Folding`). Diseccionaremos la inmutabilidad interna 
# híbrida (Listas dentros de tuplas que colapsan los Hashmaps). Finalizaremos
# con las `typing.NamedTuple`, la estructura de datos obligatoria para
# retornar outputs empaquetados en HuggingFace Transformers, PyTorch, Jax, etc.
# 
# NIVEL: EXPERTO / ARQUITECTURA DE CÓDIGO FUENTE
# ===========================================================================

import sys
import time
import dis
import gc
from collections import namedtuple
from typing import NamedTuple, Any

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: SINTAXIS CRÍTICA Y LA TRAMPA DE LA COMA ===")
print("=" * 80)

"""
A diferencia de las Listas u Diccionarios, la Tupla no nace del paréntesis `()`.
Los paréntesis en Python existen primordialmente para establecer Prioridad Jerárquica 
Matemática de Operadores (Ej: `(2 + 5) * 8`).
Lo que construye la Tupla de forma inherente en CPython es LA COMA `,`.
"""

print("\n--- Instanciaciones Correctas e Incorrectas ---")

# Tuplas Multi-dimensionales básicas
coordenada_pixel_pantalla = 1920, 1080  # -> Ojo! No lleva paréntesis. ES UNA TUPLA IGUAL.
coordenadas_con_paren = (1920, 1080)

print(f"Tipo Sin Paréntsis: {type(coordenada_pixel_pantalla)}")
print(f"¿Los valores Ram de C evalúan IDénticos matemáticamente?: {coordenada_pixel_pantalla == coordenadas_con_paren}")

# TRAMPA 1: La Tupla Unitaria (Singleton Tuple)
peligro_un_elemento = (5)   
seguro_un_elemento = (5,)   

print(f"La trampa ' (5) ' evaluó a Int!: {type(peligro_un_elemento)}")
print(f"El Comma Extra ' (5,) ' evaluó a Tupla!: {type(seguro_un_elemento)}")

# TRAMPA 2: Retornos accidentales en configuraciones MLOPS.
# Supongamos que escribes una configuración yaml / Diccionario Python. 
# Y accidentalmente pones una coma al final de una linea limpia.
config_batch = {
    "size": 32, # Ok.
    "learning_rate": 0.001, # CPython parsea que es Dictionary Key. Pero...
    "activation_flag": True, # Error comun: el dev deja esto escrito así accidentalmente al copiar/pegar un texto.
}
# La coma a fin de lista dentro de un diccionario está mitigada por defecto por PyObject Dictonarys Sintax.
# PERO si lo haces asignando una simple variable:
lr_del_modelo = 0.001,  

print(f"Asignación descuidada con trailing comma [lr = 0.001,] Evaluó a: {type(lr_del_modelo)}")
# Si ese hiperparámetro entra a un backend compilador Tensorflow C-level, estallará exigiendo Floats.


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: ARQUITECTURA C-LAYER DEL 'CONSTANT FOLDING' (ACELERACIÓN EXTREMA) ===")
print("=" * 80)

"""
El Intérprete CPython (CPython ByteCode Evaluator) tiene un optimizador interno ("Peephole 
Optimizer" en CPY 3.9 o en el Compiler de AST).
Sabe detectar estructuras inmutables. "Si los datos nunca van a cambiar, ni mutar, ¿Para 
qué rayos voy a calcular e inferir Punteros de Lista CADA VEZ que paso el CPU por ese bucle For?".
El Compilador "Plièga" las Constantes (Constant Folding) y las guarda EN EL CAJA FUERTE 
DE MEMORIA DE LA FUNCIÓN pre-cálculada de inmediato.
"""

print("\n--- Demostración Exhaustiva de Compilador: Desamblado ByteCode `Dis` ---")

# Funcionalidad que construye Listas Dinámicas
def funcion_devuelve_lista():
    return [1, 2, 3, 4]  # <-- La lista es Alterable. El compilador DEBE generarla Virgenes CADA ITERACIÓN.

# Funcionalidad que construye Tuplas Inmutables Estáticas.
def funcion_devuelve_tupla():
    return (1, 2, 3, 4)  # <-- Tupla base.

print("BYTECODE Opcodes para 'funcion_lista():'")
dis.dis(funcion_devuelve_lista)
"""
Observa:
  LOAD_CONST  (carga 1)
  LOAD_CONST  (carga 2,3,4)
  BUILD_LIST  <-- INTRUCCIÓN PESADA Y TRABAJOSA DE RAM. LENTO. Pide MALLOC AL OS.
  RETURN_VALUE
"""

print("\nBYTECODE Opcodes para 'funcion_tupla():'")
dis.dis(funcion_devuelve_tupla)
"""
Observa La Magia Absoluta!:
  LOAD_CONST  (carga el Bloque Entero! (1,2,3,4) de golpe desde un rincón almacenado C estático).
  RETURN_VALUE
-> NUNCA SE CONSTRUYE NADA DURANTE EL BUCLE! Cero Trabajo de Cpu. Operacion Instántanea Inmortal!
"""

print("\n--- Perfilación Real Micro-Segundos MLOps Train-Loop Simulation ---")
# ¿Importa esto cuando el loop procesa 5 millones de tensores?
start_t = time.perf_counter()
for _ in range(5_000_000):
    a = [1, 2, 3, 4, 5, 6, 7]
print(f"Tiempo CPU construyendo Lista 5M VECES: {(time.perf_counter() - start_t)*1000:.2f} ms")

start_t = time.perf_counter()
for _ in range(5_000_000):
    b = (1, 2, 3, 4, 5, 6, 7)
print(f"Tiempo CPU recupernado Tupla Constante 5M VECES: {(time.perf_counter() - start_t)*1000:.2f} ms")


print("\n" + "=" * 80)
print("=== CAPÍTULO 3: MEMORY OVERHEAD Y FREE-LISTS DE CPYTHON ===")
print("=" * 80)

"""
¿Qué ocurre cuándo borras a Cuchillo con el Garbage Collector millones de datos?
CPython no devuelve tan rápidamente esa escasa Memoria Tupla al Sistema Operativo RAM 
físico Windows/MacOsLInux. 
Python utiliza un Sistema de Reciclaje interno ultra-rápido: Free-Lists caching object.

(Si CPython compila Tuplas que tienen Longitud Menor a los 20 índices), al destruirlas, 
las cachea temporalmente en una Piscina (Pool Array C). Y si la proxima linea de codigo
pide una Tupla 20.. le entrega EL MISMO PUNTERO Físico vacío para evadir llamar al Malloc
de Sistema de Reserva Lento.
"""
print("\n--- Análisis Sys.getsizeof() Base ---")

tam_lista = sys.getsizeof([1, 2, 3, 4, 5])
tam_tupla = sys.getsizeof((1, 2, 3, 4, 5))

# La Tupla SIEMPRE será más ligera que la lista porque carece de "Allocated Buffers" en C struct.
print(f"Estructura Memoria Lista C-Punteros: {tam_lista} Bytes (Contiene Sobreasignación y Control).")
print(f"Estructura Memoria Tupla Estricta:   {tam_tupla} Bytes (Ajustada al 100% Sin Phats Base).")


print("\n" + "=" * 80)
print("=== CAPÍTULO 4: LA ESTAFA DE LA INMUTABILIDAD (SHALLOW TUPLE MUTATION) ===")
print("=" * 80)

"""
Pregunta Fija de Entrevista a Arquitecto Senior: "Si la tupla es Inmutable..
¿Puedo mutarla de algún modo?"

RESPUESTA CIENTÍFICA: La Tupla ES Absolutamente inmutable... !EN SUS REFERENCIAS! (Punteros).
Si una Tupla apunta al Puntero 'A', 'B' y 'C', NUNCA APUNTARÁ A NADA MÁS!!
Pero si resulta que el Puntero 'C' está apuntando a un Objeto Mutable (Una Lista), ese
objeto C ESTÁ FUERA DE LA JURISDICCIÓN DE LA TUPLA.

¡Y puedes mutar al Objeto Externo a través del Cordon Umbelicar inmutable de la Tupla!
"""

print("\n--- Demostración del Caos Lógico (Mutando Dentro de la Inmutabilidad) ---")

# Una tupla que contiene un INT y una LISTA.
tupla_trampa = (404, [100, 200, 300])

print(f"Estado Inmaculado Inicial: {tupla_trampa}")

# Ataque Directo al Puntero de la Tupla: ¡RECHAZADO CPython INMUTABLE!
try:
    tupla_trampa[0] = 505
except TypeError as t_error:
    print(f"Violación de Inmutabilidad Directa Bloqueada: {t_error}")

# Ataque In-Directo Vía Puntero Resguardado C: !CONCEDIDO!
# Estamos operando .append(99) en el array físico 0xFFFF de la externa Memoria local Lista!.
tupla_trampa[1].append(400) 
tupla_trampa[1][0] = 101 # Y mutamos in-place!.

print(f"Hacking Interno Aceptado!. Estado Post-Mutación del Array Interno: {tupla_trampa}")

"""
CONSECUENCIA MATEMÁTICA: LA PÉRDIDA ABSOLUTA DEL HASHMAP DICT-KEY.
En el módulo de Tics anteriores dejamos claro un axioma Absoluto de Python Deep.
Si tratamos de encajar esta tupla `(404, [lists])` en un Diccionario Key Object o SET...
¿Qué sucederá?
"""

try:
    dict_falla_miserable = {
        tupla_trampa: "Valor Mapeado del Tensor"
    }
except TypeError as err:
    print(f"\n!Excepción TypeError!: {err}")
    print(" -> EL CONCEPTO ESTÁ EXPLICITADO: ¡No basta con poner 'parentesis'!")
    print(" -> Una tupla SOLO ES HASHABLE Si TODAAAAAAAAAAS y ABSOLUTAMENTE TODAS")
    print(" -> SUS CONEXIONES HIJAS INFINITAS Son HASHABLES E INMUTABLES TAMBIÉN!")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: DOMINIO DE EMPAQUETADO / UNPACKING O(*) EXTREMO  ===")
print("=" * 80)

"""
¿Cómo extrae un IA sus Tensor-Shapes o sus Resultados Lógicos Ocultos Multiples?
El Unpacking Túpular en Python es la Herramienta Lógica Visual más pura.
"""

print("\n--- Desensablaje Lineal Posicional ---")
tensor_shape = (32, 128, 512, 1024)

# Ignoramos la dimensión Batch y Profundidad Extra (Usaremos 'Dummy variable `_` Mágicas Dunder').
# En linters y Pylint el Single Underscore '_', es la forma legal internacional para decirle  
# al Garbage Collector: "Sé que esto te lo tragaste, pero miénalo a Basurero que no lo requiero RAM-Trackear".

b_trash, primera_dim_real, _, ultima_dim_ancla = tensor_shape

print(f"Dimensiones extraidas localmente O(1): Dim Base: {primera_dim_real} | Extremo: {ultima_dim_ancla}")


print("\n--- Empaquetado en Tupla Colectora con Operadores Asteriscos C (Pep 3132) ---")
# Una funcion ML nos devuelve un Batch inmenso de resultados donde el Inicio Es El Loss.
gran_output_inference = (0.015, "Perro", 0.98, "Gato", 0.85, "Pájaro", 0.33)

# Queremos sacar el Perfil Predictivo. 
loss_num_incalculable , *lista_preds_mutables_generada = gran_output_inference

print(f"Extraído Singular Mago 1: {loss_num_incalculable}")
# Y Magia de Asterísco!
# Python absorbió 'TODO EL CONTENIDO RESTANTE DEL UNIVERSO' Y LO EMPACÓ AUTOMÁTICAMENTE a Array List.
print(f"Agrupación Asterísquial Compresa (Muto Inmutable A Generada array dinámico): {lista_preds_mutables_generada}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 6: COLLECTIONS.NAMEDTUPLE — TRANSICIÓN A ORIENTADA OBJETOS ===")
print("=" * 80)

"""
Si los tensores de IA y los Parámetros viajan empaquetados en Tuplas Ciegamente Constantes...
`(_, 128, _, 1024)`. 
Tu código CPython en MLOps acabará lleno de sentencias matemáticas horribles de Índice Directo:
`if data_batch[2] < data_batch_val[1]: print("Error en Shape")`.
Nadie entiende nada del código así (Magic Numbers Coding Horror).

Ahí es donde `collections.namedtuple` rescata a la Humanidad.
Eficaz, de Velocidad C-level IDÉNTICA a la tupla Base inmutable, PERO ACCESO DIRECTO DE 
ATRIBUTO (.Atribute_Name). Pura Legibilidad Object-Oriented (OO).
"""

print("\n--- Construyendo SubClases Mágicas de Memory C inmaculado ---")

# (Se declara en el Module-Level, Nombre del Clase y Array String con Atributos a Asentar).
# Creamos C-Layer Clase:
CofiguraMOP_RedNeruonal = namedtuple("ConfiguracionRedGen", ["capas_base", "dims_ocultas", "optimizador"])

# La instanciamos Dinámicamente pasándole los parámetros empaquetados obligatorios en la orden posicional.
config_c_experimento = CofiguraMOP_RedNeruonal(12, 1024, "AdamWW")

print(f"Tuple Estética de Debuggeo C: {config_c_experimento}")
print(f"Acceso directo y legible IA: Optimizador Seleccionado = '{config_c_experimento.optimizador}'")

# Y como era de esperar, Siendo Clase Basada en Tuple Core. ES IMBORRABLE E INMUTABLE.
try:
    config_c_experimento.optimizador = "SGD"
except AttributeError as c_err_named:
    print(f" -> Operador bloqueado exitosamente protegiendo hiperdatos!: {c_err_named}")

# "Y Sí es Inmutable, ¿Cómo modifico UNA COSA para correr otro experimento clone IA?"
# Usando la función Privada expuesta ._replace, que Genera Clonación Copia en Memoria y Regresa Nuevo ID:
nueva_exp_rama_alternativa = config_c_experimento._replace(optimizador="SGD")
print(f"La Copia Desligada RAM Exponencial y Mutada Legalmente: {nueva_exp_rama_alternativa}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 7: TYPING.NAMEDTUPLE — EL ESTÁNDAR ORO INDUSTRIAL EN 2026 MLOPS ===")
print("=" * 80)

"""
El método anterior de String Lists `["dims_ocultas"]` era útil en Python 2.5++.
Actualmente el paradigma Absoluto C-Layer Type-Hinted de Mypi Pylint usa 
MÓDULOS DEL TIPADO (Dataclasses o Typing_namedptuples).

La Diferencia es Brutal:
1. Permite Sintaxis Pura de Clases POO y Herencia Base (En lugar de un Factory string).
2. Permite Documentacion Interna (Docstrings de la Clase generada).
3. Permite VALORES POR DEFECTO BASE (El named tuple clásico fallaba estrepitosamente aqui sin magias de fields raras).
4. El IDE Y Copilot de IAs detectaran los errores lógicos estáticos al segundo de picar tecla (Linters Mypy / Pylance).
"""
print("\n--- Extrayendo Clase IA Predictora mediante Tipados Complejos ---")

class InferenciaBatchTransaccional(NamedTuple):
    """
    Subclase inmaculada de Type-Hints NamedTuples C.
    Ideal para agrupar Returns Múltiples de Funciones Forward Passes CPython o NLP Pipelines.
    """
    logits_salida: list[float]  # Forzamos List Array Python Hints!
    indice_ganador_predictivo: int
    scores_normalizadas: bool = True     # ¡VALORES POR DEFECTO BASE LEGALIZADOS!
    observaciones_opcionales: Any = None # Modulo Tipado ANY Hibrido


# Instanciar el Registro IA:
salida_predicional_ciclo_2 = InferenciaBatchTransaccional(   
    logits_salida=[0.02, 0.05, -2.10, 0.99], 
    indice_ganador_predictivo=3,
)

print(f"Clase Final Inmutáble Tipada: {salida_predicional_ciclo_2}")
print(f"Valores por defecto Absorvidos Magistralmente in C-Level: bool={salida_predicional_ciclo_2.scores_normalizadas}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: EL CUELLO DE BOTELLA DEL RENDIMIENTO 'ZIP' && METODOS MULTIVERSALES ===")
print("=" * 80)

"""
Existen métodos que conviven con las tuplas en el espacio infinito del Big Data IA (ETL processings).
Ej: Cargar Datasets Ziped.
La función Universal O(N) Nativa C de `zip` Mapea infinitos arrays lineales... ¿En qué los Convierte?
EN UNA EXTRACCIÓN DE TUPLAS SIMULTÁNEAS EN TIEMPO REAL LAZY AL INTÉRPRETE.
"""

labels_entrenamiento = [1,   0,   1]
datos_crudos_texto   = ["T", "F", "D"]

print("\n--- Zip de Listas. Mapeo a Array Tublar C-layer Lazy Loader ---")
# zip no hace array nuevo!, Hace Lazy Generators Engine, se lo obligas al For u list() caster!
combinacion_multiversal_empaquetada_como_listado_tupla = list(zip(labels_entrenamiento, datos_crudos_texto))
print(f"La extraccion genera Tuplas Internas Constantes Protectoramente: {combinacion_multiversal_empaquetada_como_listado_tupla}")


print("\n--- Transposición Vectorial Compleja (Matriz Rotatoria) ---")
# Exámen ML Senior: Tienes Matrix y la Quieres Rotar 90 Gados.
matriz_2d = [
    (1,  2, 3),
    (10,20,30)
]
# Usa el Asterísco de Unpacking de Python sobre C-Zip Method. Absurdametne Limpio.
# Pasa Dos Argumentos Aislados Desempaquetados al motor Zip (List 0, y List 1 posicional).
matriz_rotada_90_grads = list(zip(*matriz_2d)) 
print(f"Magica Transpuesta de List-Tuplas en C-Level: \n {matriz_rotada_90_grads}")



print("\n" + "=" * 80)
print("=== CAPÍTULO 9: TUPLAS COMO RETORNO MÚLTIPLE DE FUNCIONES ===")
print("=" * 80)

"""
En Python, una función puede retornar MÚLTIPLES valores separados por comas.
CPython internamente empaqueta esos valores en una TUPLA automática.
Esto es el patrón #1 de toda función de ML:
- train() retorna (model, history, metrics)
- evaluate() retorna (loss, accuracy, confusion_matrix)
- preprocess() retorna (X_train, X_test, y_train, y_test)
"""

print("\n--- Return múltiple: tupla implícita ---")

def evaluar_modelo_simulado(predicciones: list, reales: list) -> tuple:
    """
    Calcula métricas de un modelo.
    Retorna MÚLTIPLES valores empaquetados automáticamente en tupla.
    """
    assert len(predicciones) == len(reales), "Longitudes deben coincidir"
    
    correctas = sum(1 for p, r in zip(predicciones, reales) if p == r)
    total = len(predicciones)
    accuracy = correctas / total
    
    errores = [i for i, (p, r) in enumerate(zip(predicciones, reales)) if p != r]
    
    # Python empaqueta esto como tupla (accuracy, correctas, total, errores)
    return accuracy, correctas, total, errores

preds = [1, 0, 1, 1, 0, 1, 0, 1]
reals = [1, 0, 0, 1, 0, 1, 1, 1]

# Desempaquetado directo
acc, ok, tot, errs = evaluar_modelo_simulado(preds, reals)
print(f"Accuracy: {acc:.2%} ({ok}/{tot})")
print(f"Índices erróneos: {errs}")

# También puedes capturar la tupla entera
resultado_empaquetado = evaluar_modelo_simulado(preds, reals)
print(f"Tipo del retorno: {type(resultado_empaquetado)}")
print(f"Acceso por índice: accuracy = {resultado_empaquetado[0]:.2%}")


print("\n--- Patrón: return typing.NamedTuple para claridad ---")

class MetricasModelo(NamedTuple):
    """Resultado tipado de evaluación de un modelo."""
    accuracy: float
    precision: float
    recall: float
    f1_score: float

def evaluar_con_namedtuple(preds: list, reals: list) -> MetricasModelo:
    """Retorna métricas empaquetadas con nombres legibles."""
    tp = sum(1 for p, r in zip(preds, reals) if p == 1 and r == 1)
    fp = sum(1 for p, r in zip(preds, reals) if p == 1 and r == 0)
    fn = sum(1 for p, r in zip(preds, reals) if p == 0 and r == 1)
    tn = sum(1 for p, r in zip(preds, reals) if p == 0 and r == 0)
    
    accuracy = (tp + tn) / len(preds)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return MetricasModelo(accuracy=accuracy, precision=precision, recall=recall, f1_score=f1)

metricas = evaluar_con_namedtuple(preds, reals)
print(f"\nAccuracy: {metricas.accuracy:.2%}")
print(f"Precision: {metricas.precision:.2%}")
print(f"Recall: {metricas.recall:.2%}")
print(f"F1-Score: {metricas.f1_score:.2%}")
# Acceso posicional TAMBIÉN funciona (es una tupla):
print(f"Por índice [0]: {metricas[0]:.2%}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: TUPLAS COMO CLAVES COMPUESTAS DE DICCIONARIOS ===")
print("=" * 80)

"""
Las tuplas (si son puras, sin mutables) son HASHABLES.
Esto las convierte en la ÚNICA estructura nativa de Python que puede
servir como clave COMPUESTA de un diccionario.

Caso de uso real en ML:
- Cache de resultados indexado por (modelo, dataset, hiperparámetro).
- Matrices sparse indexadas por (fila, columna).
- Grafos: aristas indexadas por (nodo_origen, nodo_destino).
"""

print("\n--- Cache de experimentos con claves compuestas ---")

cache_experimentos = {}

# La clave es una tupla (modelo, dataset, learning_rate)
cache_experimentos[("BERT", "IMDB", 0.001)] = {"accuracy": 0.92, "epochs": 5}
cache_experimentos[("BERT", "IMDB", 0.01)] = {"accuracy": 0.89, "epochs": 3}
cache_experimentos[("GPT-2", "IMDB", 0.001)] = {"accuracy": 0.94, "epochs": 8}
cache_experimentos[("BERT", "SST-2", 0.001)] = {"accuracy": 0.91, "epochs": 4}

print("Cache de experimentos:")
for (modelo, dataset, lr), resultado in cache_experimentos.items():
    print(f"  {modelo:<8} {dataset:<8} lr={lr}  -> acc={resultado['accuracy']}")

# Búsqueda O(1)
consulta = ("BERT", "IMDB", 0.001)
print(f"\nBúsqueda de {consulta}: {cache_experimentos.get(consulta)}")


print("\n--- Matriz sparse con tuplas como coordenadas ---")

# En ML, muchas matrices son SPARSE (la mayoría de celdas son 0).
# Un dict con tuplas (fila, col) como claves es más eficiente que una matriz densa.
matriz_sparse = {}
matriz_sparse[(0, 5)] = 3.14
matriz_sparse[(2, 8)] = 2.71
matriz_sparse[(100, 200)] = 1.0  # En una matriz densa, esto ocuparía 100x200 celdas.

def get_sparse(matriz: dict, fila: int, col: int, default: float = 0.0) -> float:
    return matriz.get((fila, col), default)

print(f"Sparse[0,5] = {get_sparse(matriz_sparse, 0, 5)}")
print(f"Sparse[0,0] = {get_sparse(matriz_sparse, 0, 0)} (default)")
print(f"Total celdas almacenadas: {len(matriz_sparse)} (vs 20,000 en densa)")


print("\n" + "=" * 80)
print("=== CAPÍTULO 11: COMPARACIÓN Y SORTING DE TUPLAS (LEXICOGRÁFICO) ===")
print("=" * 80)

"""
Las tuplas se comparan LEXICOGRÁFICAMENTE (elemento por elemento, de izquierda
a derecha). El primer par de elementos que difiera decide el resultado.

Esto es BRUTALMENTE ÚTIL para sorting multi-criterio en ML:
- Ordenar modelos por (accuracy DESC, latency ASC).
- Priority queues: (prioridad, timestamp, tarea).
- Sorting estable con múltiples claves.
"""

print("\n--- Comparación lexicográfica elemento a elemento ---")

# Primer elemento decide
print(f"(1, 100) < (2, 0)    = {(1, 100) < (2, 0)}")  # True: 1 < 2

# Si el primero es igual, se mira el segundo
print(f"(2, 1)   < (2, 5)    = {(2, 1) < (2, 5)}")     # True: 2==2, 1 < 5

# Si ambos iguales, se mira el tercero
print(f"(1, 2, 3) < (1, 2, 4) = {(1, 2, 3) < (1, 2, 4)}")  # True

# La más corta es "menor" si todos los elementos coinciden
print(f"(1, 2)   < (1, 2, 0) = {(1, 2) < (1, 2, 0)}")  # True


print("\n--- Sorting multi-criterio de resultados de modelos ---")

resultados_modelos = [
    ("BERT-base",  0.91, 45.2),   # (nombre, accuracy, latencia_ms)
    ("DistilBERT", 0.88, 22.1),
    ("BERT-large", 0.93, 120.5),
    ("TinyBERT",   0.85, 8.3),
    ("RoBERTa",    0.93, 89.0),
]

# Ordenar por accuracy DESC, luego por latencia ASC
# Truco: negar accuracy para invertir el orden
ordenados = sorted(resultados_modelos, key=lambda x: (-x[1], x[2]))

print(f"\nModelos ordenados por accuracy DESC, latencia ASC:")
for nombre, acc, lat in ordenados:
    print(f"  {nombre:<15} Accuracy: {acc:.2%}  Latencia: {lat:.1f}ms")


print("\n--- Priority Queue manual con tuplas ---")

# Las tuplas permiten implementar colas de prioridad sin heapq
# (heapq se verá en el módulo de Algoritmia)
import heapq

cola_tareas = []
heapq.heappush(cola_tareas, (3, "entrenar_modelo"))
heapq.heappush(cola_tareas, (1, "preprocesar_datos"))
heapq.heappush(cola_tareas, (2, "validar_features"))
heapq.heappush(cola_tareas, (1, "limpiar_nulos"))

print(f"\nEjecutando tareas por prioridad (menor = más urgente):")
while cola_tareas:
    prioridad, tarea = heapq.heappop(cola_tareas)
    print(f"  Prioridad {prioridad}: {tarea}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: NAMEDTUPLE VS DATACLASS — CUÁNDO USAR CADA UNA ===")
print("=" * 80)

"""
Desde Python 3.7, las dataclasses compiten con las NamedTuples.
¿Cuál usar? Depende de la INMUTABILIDAD Y IDENTIDAD.

╔══════════════════════╦═══════════════════╦════════════════════╗
║ CARACTERÍSTICA        ║ NamedTuple        ║ dataclass          ║
╠══════════════════════╬═══════════════════╬════════════════════╣
║ Mutable              ║ NO (inmutable)    ║ SÍ (por defecto)   ║
║ Hashable             ║ SÍ (si pura)      ║ NO (por defecto)   ║
║ Herencia             ║ De tuple          ║ De object           ║
║ Clave de dict        ║ SÍ               ║ NO (salvo frozen)   ║
║ Desempaquetado       ║ SÍ (a, b = nt)   ║ NO                  ║
║ Iteración            ║ SÍ (for x in nt) ║ NO                  ║
║ Indexación           ║ SÍ (nt[0])       ║ NO                  ║
║ Métodos custom       ║ Sí (herencia)     ║ Sí (directo)        ║
║ __slots__            ║ Automático        ║ Manual              ║
║ Memoria              ║ Muy eficiente     ║ Normal              ║
║ Uso ideal            ║ Registros de solo ║ Objetos con estado  ║
║                      ║ lectura, retornos ║ mutable, configs    ║
╚══════════════════════╩═══════════════════╩════════════════════╝

REGLA DE ORO:
- ¿Los datos NO deben cambiar después de crearse? -> NamedTuple.
- ¿Los datos SÍ necesitan modificarse? -> dataclass.
- ¿Necesitas usarlo como clave de dict? -> NamedTuple o dataclass(frozen=True).
"""

from dataclasses import dataclass

print("\n--- Comparación directa ---")

class PuntoNT(NamedTuple):
    x: float
    y: float

@dataclass
class PuntoDC:
    x: float
    y: float

nt = PuntoNT(1.0, 2.0)
dc = PuntoDC(1.0, 2.0)

print(f"NamedTuple: {nt}, tipo: {type(nt).__bases__}")
print(f"Dataclass:  {dc}, tipo: {type(dc).__bases__}")

# Inmutabilidad
try:
    nt.x = 5.0
except AttributeError as e:
    print(f"NamedTuple inmutable: {e}")

dc.x = 5.0  # Funciona sin problemas
print(f"Dataclass mutada: {dc}")

# Desempaquetado
a, b = nt  # NamedTuple sí soporta
print(f"Desempaquetado NamedTuple: a={a}, b={b}")
# a, b = dc  # ¡ERROR! Dataclass no soporta desempaquetado.

# Hashabilidad
print(f"NamedTuple como clave dict: {{{nt}: 'valor'}}")
try:
    {dc: "valor"}
except TypeError as e:
    print(f"Dataclass como clave dict: {e}")

# Tamaño en memoria
print(f"\nMemoria NamedTuple: {sys.getsizeof(nt)} bytes")
print(f"Memoria Dataclass:  {sys.getsizeof(dc)} bytes")


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: MÉTODOS INTERNOS DE NAMEDTUPLE (_asdict, _fields, _make) ===")
print("=" * 80)

"""
Las NamedTuples (tanto collections como typing) exponen métodos "privados"
(con underscore) que son fundamentales para serialización y transformación:
- ._asdict()  -> Convierte a OrderedDict (útil para JSON serialization).
- ._fields    -> Tupla con los nombres de los campos.
- ._make(iter) -> Constructor alternativo desde un iterable.
- ._replace() -> Crea copia con campos modificados (ya visto en Cap 6).
"""

print("\n--- _asdict(): serialización a diccionario ---")

class ExperimentoML(NamedTuple):
    modelo: str
    dataset: str
    accuracy: float
    epochs: int
    learning_rate: float = 0.001

exp = ExperimentoML("BERT", "IMDB", 0.92, 5)
print(f"NamedTuple: {exp}")
print(f"._asdict(): {exp._asdict()}")

# Muy útil para logging en JSON
import json
log_json = json.dumps(exp._asdict(), indent=2)
print(f"JSON serializado:\n{log_json}")


print("\n--- _fields: introspección de campos ---")
print(f"Campos: {ExperimentoML._fields}")
# Útil para generar headers de CSV automáticamente
header_csv = ",".join(ExperimentoML._fields)
print(f"Header CSV: {header_csv}")


print("\n--- _make(): constructor desde iterable (ej: fila CSV) ---")
fila_csv = ["GPT-2", "SST-2", 0.94, 10, 0.0005]
exp_desde_csv = ExperimentoML._make(fila_csv)
print(f"Desde CSV: {exp_desde_csv}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: MEMORY PROFILING EXHAUSTIVO — TUPLA vs LISTA vs DICT ===")
print("=" * 80)

"""
¿Cuánto ahorra REALMENTE una tupla frente a una lista o dict cuando 
tienes MILLONES de registros (ej: predicciones de un modelo)?
"""

print("\n--- Comparación de overhead por registro ---")

# Un registro con 5 campos
registro_tupla = (42, "BERT", 0.92, True, "IMDB")
registro_lista = [42, "BERT", 0.92, True, "IMDB"]
registro_dict  = {"id": 42, "modelo": "BERT", "acc": 0.92, "ok": True, "ds": "IMDB"}

print(f"Tupla (5 campos): {sys.getsizeof(registro_tupla):>6} bytes")
print(f"Lista (5 campos): {sys.getsizeof(registro_lista):>6} bytes")
print(f"Dict  (5 campos): {sys.getsizeof(registro_dict):>6} bytes")

# Calcular el ahorro por 1M de registros
n_registros = 1_000_000
ahorro_vs_lista = (sys.getsizeof(registro_lista) - sys.getsizeof(registro_tupla)) * n_registros
ahorro_vs_dict = (sys.getsizeof(registro_dict) - sys.getsizeof(registro_tupla)) * n_registros

print(f"\nPara {n_registros:,} registros:")
print(f"  Ahorro Tupla vs Lista: {ahorro_vs_lista / 1024 / 1024:.1f} MB")
print(f"  Ahorro Tupla vs Dict:  {ahorro_vs_dict / 1024 / 1024:.1f} MB")
print(f"  (Solo el overhead del contenedor, sin contar contenido)")


print("\n--- Benchmark de creación masiva ---")

import time

n_bench = 500_000

inicio = time.perf_counter()
lista_tuplas = [(i, f"token_{i}", i * 0.01) for i in range(n_bench)]
t_tupla = time.perf_counter() - inicio

inicio = time.perf_counter()
lista_listas = [[i, f"token_{i}", i * 0.01] for i in range(n_bench)]
t_lista = time.perf_counter() - inicio

inicio = time.perf_counter()
lista_dicts = [{"id": i, "token": f"token_{i}", "score": i * 0.01} for i in range(n_bench)]
t_dict = time.perf_counter() - inicio

print(f"\n  Crear {n_bench} tuplas:  {t_tupla*1000:.2f} ms")
print(f"  Crear {n_bench} listas:  {t_lista*1000:.2f} ms")
print(f"  Crear {n_bench} dicts:   {t_dict*1000:.2f} ms")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: PATRONES AVANZADOS EN PRODUCCIÓN IA ===")
print("=" * 80)

print("\n--- Patrón: Configuraciones inmutables con NamedTuple ---")

class ModelConfig(NamedTuple):
    """Configuración inmutable de un modelo. Una vez creada, no se puede alterar."""
    model_name: str
    hidden_size: int
    num_layers: int
    dropout: float = 0.1
    activation: str = "gelu"

# Config base
config_base = ModelConfig("transformer", 768, 12)
print(f"Config base: {config_base}")

# Variante para experimento (sin mutar la original)
config_grande = config_base._replace(hidden_size=1024, num_layers=24)
print(f"Config grande: {config_grande}")
print(f"Config base intacta: {config_base}")


print("\n--- Patrón: Múltiples retornos tipados en pipelines NLP ---")

class TokenizacionResult(NamedTuple):
    """Resultado de tokenización para un batch de textos."""
    input_ids: list[list[int]]
    attention_mask: list[list[int]]
    token_count: int

def tokenizar_batch(textos: list[str], vocab_size: int = 30000) -> TokenizacionResult:
    """Simula tokenización de un batch de textos."""
    input_ids = []
    attention_mask = []
    total_tokens = 0
    
    for texto in textos:
        # Simulación: cada palabra = 1 token con ID basado en hash
        tokens = [hash(palabra) % vocab_size for palabra in texto.split()]
        mask = [1] * len(tokens)
        input_ids.append(tokens)
        attention_mask.append(mask)
        total_tokens += len(tokens)
    
    return TokenizacionResult(
        input_ids=input_ids,
        attention_mask=attention_mask,
        token_count=total_tokens
    )

textos_ejemplo = ["el gato come pescado", "la IA domina el mundo"]
resultado_tok = tokenizar_batch(textos_ejemplo)
print(f"\nTokens totales: {resultado_tok.token_count}")
print(f"Input IDs (2 textos): {[len(ids) for ids in resultado_tok.input_ids]} tokens cada uno")
print(f"Tipo retorno: {type(resultado_tok)}")
# Sigue siendo desempaquetable:
ids, masks, count = resultado_tok
print(f"Desempaquetado: {count} tokens totales")


print("\n" + "=" * 80)
print("=== CAPÍTULO 16: TABLA DE COMPLEJIDAD Y MÉTODOS COMPLETOS ===")
print("=" * 80)

"""
╔═══════════════════════════════╦═══════════════════╗
║ OPERACIÓN                     ║ COMPLEJIDAD       ║
╠═══════════════════════════════╬═══════════════════╣
║ tuple[i]                      ║ O(1)              ║
║ len(tuple)                    ║ O(1)              ║
║ x in tuple                    ║ O(N)              ║
║ tuple.count(x)                ║ O(N)              ║
║ tuple.index(x)                ║ O(N)              ║
║ tuple + tuple2                ║ O(N + M)          ║
║ tuple * k                     ║ O(N * k)          ║
║ hash(tuple)                   ║ O(N)              ║
║ tuple[a:b]                    ║ O(b - a)          ║
║ min(tuple) / max(tuple)       ║ O(N)              ║
║ sorted(tuple)                 ║ O(N log N)        ║
╚═══════════════════════════════╩═══════════════════╝

NOTA: Las tuplas NO tienen .append(), .extend(), .insert(), .remove(),
.pop(), .sort(), .reverse(), ni .clear(). Son INMUTABLES.
Los únicos métodos son .count() y .index().
"""


print("\n" + "=" * 80)
print("=== CAPÍTULO 17: TUPLE() VS GENERADOR — NO EXISTE TUPLE COMPREHENSION ===")
print("=" * 80)

"""
Error CLÁSICO de principiante y pregunta de entrevista:
"¿Cómo hago una tuple comprehension?"

La respuesta es: NO EXISTE.

(x for x in range(5))  -> Esto es un GENERATOR, no una tupla.
tuple(x for x in range(5))  -> Esto crea una tupla desde un generator.

La diferencia es FUNDAMENTAL para memoria:
- Un generator produce valores LAZY (uno a uno, sin almacenarlos todos).
- Una tupla almacena TODOS los valores de golpe en memoria.

En ML, los generators son la base de los DataLoaders eficientes.
"""

print("\n--- La trampa: paréntesis NO crean tuple comprehension ---")

# Esto NO es una tupla — es un generador
generador = (x**2 for x in range(5))
print(f"Tipo con paréntesis: {type(generador)}")
print(f"  -> Es un generator, NO una tupla!")

# Para crear una tupla desde una expresión, necesitas tuple()
tupla_real = tuple(x**2 for x in range(5))
print(f"tuple() explícito: {tupla_real}, tipo: {type(tupla_real)}")

# Diferencia en memoria
import sys
gen = (x for x in range(1_000_000))
tup = tuple(range(10))  # Solo 10 para no consumir RAM
print(f"\nMemoria generator (1M items): {sys.getsizeof(gen)} bytes (constante!)")
print(f"Memoria tupla (10 items): {sys.getsizeof(tup)} bytes")
print(f"  -> El generator NO almacena los datos, los produce bajo demanda.")


print("\n--- Generator como DataLoader lazy ---")

def generar_batches_lazy(dataset: list, batch_size: int):
    """
    Generator que produce batches bajo demanda.
    A diferencia de crear una lista de batches, esto NO consume
    memoria extra — produce cada batch solo cuando se necesita.
    """
    for i in range(0, len(dataset), batch_size):
        yield tuple(dataset[i : i + batch_size])  # Cada batch como tupla inmutable

dataset = list(range(100))
loader = generar_batches_lazy(dataset, batch_size=30)

print(f"Tipo del loader: {type(loader)}")
for i, batch in enumerate(loader):
    print(f"  Batch {i}: {len(batch)} elementos, tipo: {type(batch)}")
    # Cada batch es una TUPLA inmutable — no se puede alterar accidentalmente


print("\n" + "=" * 80)
print("=== CAPÍTULO 18: HASHING INTERNO DE TUPLAS EN CPYTHON ===")
print("=" * 80)

"""
¿Cómo calcula Python el hash de una tupla?
No es simplemente sumar los hashes de los elementos.

CPython (desde 3.8) usa el algoritmo SipHash-based xxHash:
1. Toma el hash de CADA elemento individualmente.
2. Los combina con operaciones XOR, multiplicación y rotación de bits.
3. El resultado final es un entero de 64 bits único y determinístico.

Esto garantiza que:
- Tuplas con los mismos elementos en DIFERENTE ORDEN tienen hashes DISTINTOS.
- La distribución de hashes es uniforme (minimiza colisiones en dicts).
- El cómputo es O(N) donde N es el número de elementos.
"""

print("\n--- Hashes de tuplas: orden importa ---")

t1 = (1, 2, 3)
t2 = (3, 2, 1)
t3 = (1, 2, 3)

print(f"hash((1, 2, 3)) = {hash(t1)}")
print(f"hash((3, 2, 1)) = {hash(t2)}")
print(f"hash((1, 2, 3)) = {hash(t3)}  (idéntico al primero)")

print(f"\n¿(1,2,3) == (3,2,1)?: {t1 == t2}")
print(f"¿(1,2,3) == (1,2,3)?: {t1 == t3}")
print(f"¿hash iguales t1,t3?: {hash(t1) == hash(t3)}")

# Tuplas vacías y unitarias
print(f"\nhash(())  = {hash(())}")
print(f"hash((42,)) = {hash((42,))}")

# La tupla vacía es hashable y su hash es constante (siempre el mismo)
print(f"hash(()) == hash(()): {hash(()) == hash(())}")


print("\n--- Caché de hash en tuplas vs cálculo en cada acceso ---")

"""
A diferencia de los strings (que cachean su hash tras el primer cálculo),
las tuplas NO cachean su hash. Cada vez que llamas hash(tupla), CPython
recalcula recorriendo todos los elementos.

Esto significa que para tuplas muy grandes como clave de dict, el primer
lookup es más lento. Pero en la práctica, las tuplas usadas como clave
suelen ser pequeñas (2-5 elementos).
"""

import time

tupla_grande = tuple(range(10_000))
tupla_peque = (1, 2, 3)

# Benchmark: hash de tupla grande vs pequeña
n_iter = 100_000

inicio = time.perf_counter()
for _ in range(n_iter):
    hash(tupla_peque)
t_peque = time.perf_counter() - inicio

inicio = time.perf_counter()
for _ in range(n_iter):
    hash(tupla_grande)
t_grande = time.perf_counter() - inicio

print(f"\n  hash(tupla_3_items) x {n_iter}: {t_peque*1000:.2f} ms")
print(f"  hash(tupla_10K_items) x {n_iter}: {t_grande*1000:.2f} ms")
print(f"  Ratio: la grande es ~{t_grande/t_peque:.0f}x más lenta")
print(f"  -> Por eso las claves de dict deben ser tuplas CORTAS.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 19: EJERCICIO INTEGRADOR — PIPELINE ML COMPLETO CON TUPLAS ===")
print("=" * 80)

"""
Ejercicio final que combina todos los patrones de tuplas aprendidos
para construir un mini sistema de tracking de experimentos ML.
"""

print("\n--- Sistema de Experiment Tracking con NamedTuples ---")

import random
random.seed(42)

class HyperParams(NamedTuple):
    model: str
    lr: float
    batch_size: int
    optimizer: str = "adam"

class ExperimentResult(NamedTuple):
    params: HyperParams
    accuracy: float
    loss: float
    epochs_trained: int

# Generar experimentos
experimentos = []
for modelo in ["BERT", "GPT-2", "T5"]:
    for lr in [0.001, 0.0005, 0.0001]:
        for bs in [16, 32]:
            hp = HyperParams(model=modelo, lr=lr, batch_size=bs)
            # Simular resultado (más lr bajo = mejor accuracy, más o menos)
            acc = min(0.99, 0.80 + random.uniform(0, 0.15) + (0.001 / lr) * 0.001)
            loss = max(0.01, 1.0 - acc + random.uniform(-0.05, 0.05))
            result = ExperimentResult(
                params=hp,
                accuracy=round(acc, 4),
                loss=round(loss, 4),
                epochs_trained=random.randint(3, 15)
            )
            experimentos.append(result)

print(f"Total experimentos: {len(experimentos)}")

# Top 5 por accuracy (sorting lexicográfico con tuplas)
top_5 = sorted(experimentos, key=lambda e: -e.accuracy)[:5]
print(f"\nTop 5 experimentos:")
for i, exp in enumerate(top_5, 1):
    print(f"  #{i}: {exp.params.model:<6} lr={exp.params.lr:>6} bs={exp.params.batch_size:>2} "
          f"-> acc={exp.accuracy:.4f} loss={exp.loss:.4f}")

# Cache de resultados indexado por hiperparámetros (tupla como clave)
cache = {}
for exp in experimentos:
    # HyperParams ES una NamedTuple -> hashable -> clave de dict
    cache[exp.params] = {"accuracy": exp.accuracy, "loss": exp.loss}

# Búsqueda O(1) por hiperparámetros exactos
consulta = HyperParams("BERT", 0.0001, 32)
resultado = cache.get(consulta)
print(f"\nBúsqueda por HP exacto {consulta}: {resultado}")

# Agrupar resultados por modelo usando desempaquetado
from collections import defaultdict
por_modelo = defaultdict(list)
for exp in experimentos:
    por_modelo[exp.params.model].append(exp.accuracy)

print(f"\nMedia de accuracy por modelo:")
for modelo, accs in sorted(por_modelo.items()):
    media = sum(accs) / len(accs)
    print(f"  {modelo:<6}: {media:.4f} ({len(accs)} experimentos)")

# Serialización a JSON via _asdict()
mejor = top_5[0]
log_entry = {
    "best_experiment": mejor._asdict(),
    "params": mejor.params._asdict(),
}
import json
print(f"\nLog JSON del mejor experimento:")
print(json.dumps(log_entry, indent=2, default=str))


print("\n" + "=" * 80)
print("=== CONCLUSIONES Y SÍNTESIS ARQUITECTÓNICAS DE IA ===")
print("=" * 80)

"""
Resumen Final del Conocimiento Estático Tuplar CPython:

1. La COMA crea la tupla, no los paréntesis. Cuidado con (5) vs (5,).

2. Constant Folding: el compilador pre-calcula tuplas de constantes,
   eliminando el coste de construcción en loops de millones de iteraciones.

3. Free-Lists: CPython cachea tuplas pequeñas destruidas para reutilizar
   sus punteros, evitando llamadas al malloc del SO.

4. Inmutabilidad PARCIAL: los punteros son fijos, pero si apuntan a un
   mutable (lista, dict), ESE MUTABLE sí puede cambiar. Esto destruye
   la hashabilidad y la elegibilidad como clave de dict/set.

5. Unpacking (*args, _, *rest) es la herramienta #1 para extraer datos
   de retornos de funciones ML de forma legible.

6. collections.namedtuple vs typing.NamedTuple: la segunda es el estándar
   moderno por soportar type hints, defaults y docstrings.

7. NamedTuple vs dataclass: NamedTuple para registros inmutables y retornos;
   dataclass para objetos con estado mutable y lógica compleja.

8. Tuplas como claves compuestas de dict: (modelo, dataset, lr) -> resultado.
   La única forma nativa de tener claves multi-campo en Python.

9. Comparación lexicográfica: sorting multi-criterio nativo sin key= complejo.

10. Overhead mínimo: una tupla de 5 campos ahorra ~16-200 bytes por registro
    frente a lista/dict. Con millones de registros, son GB de diferencia.

11. NO existe tuple comprehension. (x for x in ...) es un GENERATOR.
    Usa tuple() para materializar si necesitas inmutabilidad.

12. El hash de tuplas es O(N) y NO se cachea. Usa tuplas cortas como claves.
"""
print(" FIN DE ARQUIVO 03_tuplas_estrictas_inmutables. El paradigma inmutable ha sido conquistado!")


