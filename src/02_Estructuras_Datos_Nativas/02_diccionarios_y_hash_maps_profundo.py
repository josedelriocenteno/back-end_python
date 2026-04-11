# ===========================================================================
# 02_diccionarios_y_hash_maps_profundo.py
# ===========================================================================
# MÓDULO 02: ESTRUCTURAS DE DATOS NATIVAS (AISLADAS)
# ARCHIVO 02: Diccionarios, Hash Maps Iterativos y Dispatching en IA
# ===========================================================================
#
# OBJETIVO ESTRUCTURAL Y PROFUNDIDAD DEFINITIVA (MIL LÍNEAS+):
# Este documento aborda la estructura de datos madre absoluta de toda la 
# programación y de todo el estado de Machine Learning moderno: El Diccionario.
# PyTorch State_Dicts, Archivos JSON, Configuración YAML, Pesos de Layers,
# Vocabularios de NLP. Todo en la IA recae en los HashMap O(1) de Python.
#
# DESGLOSE HIPER-TÉCNICO:
# 1. Teoría Subyacente en CPython: dk_indices y dk_entries (Compact Dicts).
# 2. Resolución de Colisiones (Quadratic Probing vs Open Addressing).
# 3. Regla absoluta de Inmutabilidad de la Clave e Interning de Strings.
# 4. Vistas dinámicas, `dict.items()`, y el Runtime Error de Modificación iterativa.
# 5. Operadores de Fusión PEP 584 (`|` y `|=`) frente a `.update()`.
# 6. Técnicas MLOps: Tablas de Dispatch Funcional (Evitando If/Else).
# 7. Indexación Invertida O(1) para motores de Búsqueda RAG manuales.
# 8. Unpacking profundo (`**kwargs`).
# 9. JSON Serialization Hooks & Datasets estrucurados multinivel.
# 10. Benchmarks exhaustivos de RAM con Tracemalloc.
#
# NIVEL: EXPERTO / ARQUITECTO SOFTWARE ML. (0 suposiciones pre-existentes).
# ===========================================================================

import sys
import time
import math
import dis
import json
import random
import tracemalloc
import pickle
import hashlib
from typing import Dict, Any, Hashable, Union

# Un perfilador para evidenciar los saltos matemáticos de RAM O(1).
def perfilador_ram(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start = time.perf_counter()
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"[RAM Profile] {func.__name__} | Tim: {(fin-start)*1000:.4f}ms | Variación RAM: {current / 1024:.2f} KB | Pico Expansión: {peak / 1024:.2f} KB")
        return resultado
    return wrapper


print("\n" + "=" * 80)
print("=== CAPÍTULO 1: ANATOMÍA INTERNA DEL HASHTABLE (COMPACT DICTS 3.6+) ===")
print("=" * 80)

"""
Mucha gente cree que un Dicc en Python es como un Array de Tuplas gigantesco
que hay que buscar secuencialmente. 
Falso. El diccionario es un HASH TABLE (Tabla Hash).

El Hash Table de Python dicta que la búsqueda de una clave tiene un tiempo 
matemático Constante O(1). ¿Cómo se logra eso si hay 1 Millón de claves?

Paso 1: Se le envía la "Key" a la super-función `hash()`.
Paso 2: Esta función encripta esa key a un entero C Gigantesco (Ej: -49830843102).
Paso 3: Se hace la operación módulo `% Tamaño_del_Array_Memoria`. Esto nos
        da un número fijo, por ejemplo, en la posición #5.
Paso 4: Python va directamente al Slot 5 de la Placa de RAM y lo saca de inmediato.
        No recorre la 1, 2, 3 ni 4. Aterriza en la 5. Cero iteraciones.

LA EVOLUCIÓN EN PYTHON 3.6 (Compact Dicts de Raymond Hettinger)
Antes de 3.6, el Diccionario Python usaba ALBEDRÍO PURO (Sparse Array), 
con bloques en RAM vacíos y fragmentados. Desordenando la inserción.
Hoy en día internamente está separado en dos matrices en C:
A) `dk_indices`: Un mini-array liviano O(1) de busqueda lleno de Integers que 
    apunta a la Posición en el Entrie.
B) `dk_entries`: Una matriz de inserción estrictamente Secuencial O(N) que guarda
    el Hash de C, La Referencia a la Palabra Clave (Key Pointer) y la Referencia
    al Valor (Value Pointer).
ESTE ALGORITMO AHORRÓ UN 25% DE MEMORIA RAM EN TODO EL MUNDO. Y HIZO QUE AHORA LOS 
DICCIONARIOS MANTENGAN EL ORDEN DE INSERCIÓN AUTOMÁTICAMENTE (Adiós OrderedDict!).
"""

print("\n--- Demostrando la Complejidad Estructural Base ---")

diccionario_vacio = {}
tamanio_base_dict = sys.getsizeof(diccionario_vacio)

print(f"Diccionario Vacío de '{}' inicializa pre-reservando memoria: {tamanio_base_dict} Bytes")
# Aproximadamente ~64 Bytes en Linux x86_64. 
# Esto incluye el header de CPython, refcounts, el array de índices base(8) pre-alocado.

diccionario_elemental = {"LR": 0.001, "Epochs": 50, "Batch": 32}
print(f"Diccionario con 3 campos Hiperparámetros pesa: {sys.getsizeof(diccionario_elemental)} Bytes")

"""
PRECAUCIÓN DE RENDIMIENTO Y REDIMENSIONAMIENTO (DICT RESIZE CACHES):
Igual que las Listas sufrían Over-Allocation para no asediar tu Sistema Operativo.
A los diccionarios CPython les gusta que la Tabla `dk_indices` se mantenga SOLO al 2/3 de
su capacidad (66%). 
Cuando excedes 5 inserciones en un Diccionario Vacio (size_base 8 items * 0.66 = ~5 items),
CPython dispara el `dictresize()` en C. 
Duplicando de Golpe y pidiendo una mole de RAM para reconstruir (Re-Hash) todas las claves.

Mala Praxis: Iterar y llenar paso a paso un diccionario Inmenso con 1 billon de items con bucles vacios 
si podíamos haberlo importado de Gople (Donde Python evalua el Array Global de carga y le asigna la reserva Final de 1 vez).
"""

print("\n--- Efecto Cascada del Resize Malloc Oculto ---")

mi_dicc_dinamico = {}
peso_historico = sys.getsizeof(mi_dicc_dinamico)
colisiones_de_malloc = 0

for i in range(100_000):
    mi_dicc_dinamico[f"Clave_Dinamica_{i}"] = i
    peso_actual = sys.getsizeof(mi_dicc_dinamico)
    
    if peso_actual > peso_historico:
        # Imprimimos de las primeras 5 mudanzas para no polular logs.
        if colisiones_de_malloc < 5:
            print(f"  [CPython Resize!] en Turno {i}. RAM saltó de {peso_historico/1024:.2f}KB -> {peso_actual/1024:.2f}KB.")
        colisiones_de_malloc +=1
        peso_historico = peso_actual
        
print(f"  ... (Log Cortado) ... \n  Total de Recalculados y Resizes de Memoria: {colisiones_de_malloc} veces.")
print("  Moraleja MLOps: Construye Diccionarios por Comprensión Glogal si puedes en vez de Inyectar Punteros Unitarios en bucles Millonarios.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: LA MATEMÁTICA DE LA COLISIÓN (PROBING CUADRÁTICO) ===")
print("=" * 80)

"""
Como dijimos, `hash("perro")` y `hash("gato")` escupen un ID de 64 bits y ambos son mapeados
a un Slot limitando al número del índice (`% tamaño_matrix`).
¿Qué pasa si "perro" mapea al Slot 3, e insertamos "gato" y POR AZAR DEL DESTINO acaba 
también el el Slot 3? (Hash Collision Parcial O Indicial).

Si no hubiera solución, el Diccionario te sobreescribiría y perderías datos vitales del IA.
Los lenguajes primitivos (C estandar) usan Linear Probing: Miran el Cajón 3 (Lleno), Miran el 4 (Vacio), meto aquí.
Python NO USA "LINEAR PROBING".
"""

# Implementación de Simulación de la Fómula de CPython Interna de Colisión:
# pseudocodigo del Engine CPython oficial en Object/dictobject.c:
# j = (5*j) + 1 + perturb;
# perturb >>= 5;

def simulacion_pseudo_aleatoria_reparto_cpython(hash_colision_obj, tam_tabla=8):
    """
    Función educacional para denotar cómo Python aleja la basura de colisiones 
    espaciando cuadráticamente para evitar clusters trampa continuos (El fallo del Linear Probing).
    """
    j = hash_colision_obj % tam_tabla 
    perturb = hash_colision_obj
    print(f"  [Simulacro Probe] -> Slot Incial Buscado HASH-CLASH: {j} (Asumiremos que está LLENO)")
    
    for iterador_resolutivo in range(1, 6): # Probe Depth Search Fallback
        # Formula Mágica de CPython perturb shift
        j = ((5 * j) + 1 + perturb) 
        perturb >>= 5 # Bitwise Shift R. (División logica // 32 de C).
        j_modulo = j % tam_tabla
        print(f"   |-- Rebote Colisión {iterador_resolutivo}: Python Intenta escribir/encontrar en Slot [{j_modulo}]")

simulacion_pseudo_aleatoria_reparto_cpython(hash("NLP_Colision_Token"), 32)

print("\n(Este motor garantiza estadísticamente que nunca el Dictionary degradará tu Big-O a O(N) catastrófico).")


print("\n" + "=" * 80)
print("=== CAPÍTULO 3: HASHABILIDAD, INMUTABILIDAD E STRING INTERNING ===")
print("=" * 80)

"""
Regla de ORO Indestructible de Python:
- LOS VALUES (Valores) de un Diccionario pueden ser Absolutamente Todo: Modulos, Numeros, Otras Redes Neuronales, Tensores, None, Funciones.
- LAS KEYS (Claves) SOLO pueden ser objetos "HASHABLES" (Que tengan funcion mágica __hash__).

Hablamos de Inmutabilidad.
Una Lista `[1, 2, 3]` es Mutable. Si se meteria una Lista hoy, le calculamos el Hash "9800", se encaja en el 
Slot 5. Mañana le haces .append(4) a tu lista, Su Hash Muta. Si buscamos el Slot 5 nos dara un Hash disinto y
hemos roto la Integridad Hash de C. Cpython prohibe mutables.
"""

print("\n--- Fallo Catastrófico de Diseño Tensor Array como Keys ---")
# En Deep Learning, podrías intentar asociar una matriz 1D a un estado de Score...
try:
    arr_mutante_tensor = [0, 0, 0, 1] 
    dict_falla = {
        arr_mutante_tensor: "Score_Perfecto"
    }
except TypeError as error_grave:
    print(error_grave) # "unhashable type: 'list'"

# LA SOLUCIÓN EXPERTA IA (Tuplas de Cast Limpio):
arr_mutante_tensor_tuplificado = tuple([0, 0, 0, 1])
dict_funciona_excelente = {
    arr_mutante_tensor_tuplificado: "Score Perfecto! [0,0,0,1]"
}
print(f"\nConversión a Inmutable Hashable Correcta: {dict_funciona_excelente}")


print("\n--- El Fenómeno STRING INTERNING de Dict Keys ---")
"""
Otra maravilla de Python para IA NLP. (Donde los corpus procesan 10 Mllones de Keys string repetidas).
Si un String parece un identificador simple (sin caracteres raros o espacios, solo Ascii simple), 
CPYTHON INVOCARÁ "String Interning". 
Esto significa que si hay 1,000,000 variables y dicts usando la key `"learning_rate"`, 
tu ordenador NUNCA clonará ese String. Lo guardará en una Bóveda Única de C (Interned String Table),
y mandará 1 Millón de punteros diminutos.
"""

# Vamos a generar dinámicamente dos cadenas que son matemáticamente iguales.
a_key_str = "generative_ai"
b_key_str = "".join(['g','e','n','e','r','a','t','i','v','e','_','a','i'])

print(f"Los dos objetos strings son iguales en Contenedor (a == b) ?: {a_key_str == b_key_str}")

# Usamos sys.intern() para forzarlo manualmente si fuera muy complejo, pero 
# para chars ascii directos ocurren maravillas, pero al ser Creados via Join Dinámico,
# B_key_str ES UN OBJETO C DISTINTO RAM (A is B -> False).
print(f"Los dos objetos son misma memoria RAM por defecto de unión dinámica? : {a_key_str is b_key_str}")

import sys
b_key_str_internado_via_sys = sys.intern(b_key_str)
a_key_str_internado_via_sys = sys.intern(a_key_str)
print(f"Interned Malloc A equals Inerned Malloc B (Unificación Hash Absoluta)? : {a_key_str_internado_via_sys is b_key_str_internado_via_sys}")

# ESTO HACE QUE UN DICCIONARIO BUSQUE EN NS UN STRING. PORQUE NUNCA LEE CARACTER POR CARACTER, COMPARA 
# LA ID RAM EXCLUSIVA HASH INTERNED (Pointer O(1) Eq).


print("\n" + "=" * 80)
print("=== CAPÍTULO 4: TÉCNICAS NATIVAS DE CASTEADO Y CONSTRUCCIÓN AVANZADA ===")
print("=" * 80)

"""
Hay 5 (CINCO!) maneras de Instanciar un Diccionario de Memoria C en Python.
Las diseccionaremos para ver su consumo de Tiempo y por qué la gente abusa de KWARGS.
"""

lista_tup_dataset = [("batch_size", 32), ("epochs", 100), ("optimizer", "adam"), ("lr", 0.001)]

print("\n--- Las 5 Facciones CPythoniales ---")

# 1. Dict Literal (Directo). Mas veloz. Compile-Time Parsed.
metodo_1_literal = {"batch_size": 32, "epochs": 100, "optimizer": "adam", "lr": 0.001}

# 2. Kwargs Casting constructor (Funcional, Limpio). Penalizacion Callable function.
metodo_2_kwargs = dict(batch_size=32, epochs=100, optimizer="adam", lr=0.001)

# 3. List of Tuples Mapping (Usado al convertir DataLoads de Databases)
metodo_3_iterable = dict(lista_tup_dataset)

# 4. ZIP Inserction Zipeada Itertools paralela (Mapeo Rápido de Lists Paralelas MLOPS)
list_claves = ["batch_size", "epochs", "optimizer", "lr"]
list_values = [32, 100, "adam", 0.001]
metodo_4_zippeado = dict(zip(list_claves, list_values))

# 5. Dict Comprehension (Filtros C-level Aplicables Inline, Super Herramienta IA).
metodo_5_comprehensado = { clave: valor for clave, valor in zip(list_claves, list_values) if clave != "lr" }

print(f"Métrico Dict Comprehension (Expulsó LR condicionalmente): {metodo_5_comprehensado}")

# Mención Honorable 1: Múltiples Inicios .fromkeys(). Rápido llenado None O(N) Array.
claves_necesarias_api = ["api_key", "secret_hash", "token_lifespan_ms", "user_access"]
generacion_plantilla = dict.fromkeys(claves_necesarias_api, "Vacio")
print(f"Plantillado Rápido y Clonico con fromkeys: \n {generacion_plantilla}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: METODOS GET() Y SETDEFAULT() (BYPASSING ERROR BREAKS) ===")
print("=" * 80)

"""
El Anti-Patrón clásico de todo Desarrollador intermedio:
Extraer de un diccionario `if k in dict: do_this()` o Peor `try: x = dict[k] except KeyError`.
Los diccionarios exiten .get() implementado en código C que busca de un golpe sin lanzar 
excepciones trampa que rompan pipelines enteros de validacion en Modelos de Tensorflow/PyTorch.
"""
print("\n--- Patrones Robustos de Extracción (Evadir KeyErrors MLOps) ---")

config_aws_s3_download = {"bucket": "ia-dataset-3", "key": "train.csv", "timeout": 500}

# EXTRACCIÓN PELIGROSA: config_aws_s3_download["max_retries"] -> KeyError Fatal Error System Stop MLException.

# MÉTODO GET. (Clave, Valor_Por_Defecto_De_Fallback).
# ValorFallback = None si no lo especificas. Si no encuentra la key, no revienta, devuelve el backup Fallback.
intentos_redireccion = config_aws_s3_download.get("max_retries", 3)  
print(f"Get Extracción Bypass Return-Safe: Intentos definidos por Paracaidas Local: {intentos_redireccion}")

print("\n--- Patrón SetDefault (La inyección y Extracción Simultánea C) ---")
# Cuando inicializamos Contadores de Vocabulario Textos NLP. Un pipeline cuenta palabras.
# Requieres chekear si existe la palabra. Si NO EXISTE, la metemos con Count 0. Y al final Sume.

vocabularios_frecuencia_dict = {"el": 5003, "en": 300, "python": 40}

# ESTILO LENTO PYTHONICO (2 Hits de Búsqueda de Memoria O(1) * 2 = O(2)):
if "artificial" not in vocabularios_frecuencia_dict: # PRIMERA BUSQUEDA EN RAM
    vocabularios_frecuencia_dict["artificial"] = 0   # PRIMERA INYECCION, SEGUNDO GOLPE DE RAM.
vocabularios_frecuencia_dict["artificial"] += 1      # TERCER GOLPE RAM (EXTRAER) Y CUARTO RAM INYECTR 1.

# ESTILO SENIOR (C-LEVEL SETDEFAULT y Operaciones Compuestas)
# SetDefault -> Golpea una sola vez a nivel C. ¿No está artificial_2? Metemelo en C a 0 e Inmediatamente devuelvelo!
valor_retornado_seguro = vocabularios_frecuencia_dict.setdefault("artificial_2", 0)
vocabularios_frecuencia_dict["artificial_2"] += 1  

print(f"Técnnica SetDefault Instanciatura Rápida: {vocabularios_frecuencia_dict['artificial_2']}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 6: LAS "VISTAS" DINÁMICAS (VIEW OBJECTS DEL DICCIONARIO) ===")
print("=" * 80)

"""
En Python 2, ejecutar `dict.keys()` clonaba cada String de toda la Base a una Nueva 
Lista `[]` gigante independiente. (Memory Duplicate O(N) Ram overhead).
Si iterabas `dicc.items()` de una base de datos Giga-byte, tu ordenador colapsaba 
generando una Tupla Gigante temporal RAM en el backend.

En Python 3, ESTO DESAPARECIÓ. Y es uno de los mayores beneficios del Lenguaje Moderno.
Ahora, `keys`, `values` y `items` retornan ViewObjects (Objetos Vista).
No son listas ni tuplas de RAM.
Son ventanas transparentes interactivas Creadas O(1) PURE. Apuntan y miran (Peek) 
directamente al interior del Dictionary Memory Object en C-Time.
"""

print("\n--- Las 3 Ventanas Trastlucidas O(1) Memory Views ---")

dict_dataset_splits_tamaños = {"train": 1_000_000, "val": 200_000, "test": 50_000}

ventanas_claves = dict_dataset_splits_tamaños.keys()
ventanas_valores = dict_dataset_splits_tamaños.values()
ventanas_pares_items = dict_dataset_splits_tamaños.items()

print(f"Ventana Lógica (No copia RAM): {type(ventanas_claves)} = {ventanas_claves}")
print(f"Peso del Dictionary Matrix (Padre): {sys.getsizeof(dict_dataset_splits_tamaños)} bytes")
print(f"Peso de la ViewKeys Array (Ventana Hija): {sys.getsizeof(ventanas_claves)} bytes (Es bajísimo e irrisorio porque es inmaterial!)")

print("\n--- El Fenónomeno Mágico: Actualizaciones En Tiempo Real (Live View) ---")
# Una lista clonada se quedaría Atada al pasado si el Origen Muta. 
# La VISTA muta a la par que el objeto base en Milisegundos Cero Delay.

dict_dataset_splits_tamaños["dev"] = 15_000

print(f"Nuevas Claves Vistas Mágicamente Actualizadas tras Inyección Externa Ciega!! : {ventanas_claves}")

"""
PELIGRO EXTREMO: RuntimeError Exception - Dictionary Size Changed During Iteration.
Debido a que estas "Vistas" Iteran mirando Ciegamente en Tiempo Real la Ram Madre Interna DK_ENTRIES,
Si tu bucle for `for k in dict.keys()` decide por arte de mágia eliminar Items con `del dict[k]`...
La Tabla C de Python se destrozará porque el índice Puntero sobrecargará o caerá (Resize Exception Out Of Bounds).
Alerta! CPython intercepta este Error Cataclísmico Lógico lanzdo una Excpeción que rompre Inmediatamente tu APP.
"""

print("\n--- ¿Cómo elimino Items Dinámicos de un Dict iterativamente para purgarlo en IA? ---")

purga_target = {"perro": 19, "gato": 5, "lapiz": 1}

# ERROR ESTUARDO (RuntimeError garantizado en tu consola que rompe el entrenamiento LLM):
# for clave in purga_target.keys():
#   if purga_target[clave] < 10: 
#        del purga_target[clave] 

# FORMA SEGURA CIENTÍFICA: Materializamos temporalmente La Vista a una LISTA de RAM Independiente,
# y esa lista se reitera libre y pacíficamnente purgada.

# El `list()` forza a Python a Congelar los Items Actuales En una Pila de Datos Ram Independiente!
for clave_segura in list(purga_target.keys()): 
    if purga_target[clave_segura] < 10:
        del purga_target[clave_segura] # Destripamos sin miedo el Origen!

print(f"Diccionario Correctamente Purgado y Vacunado O(N Copy): {purga_target}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 7: EL FENÓMENO PEP-584 FUSIÓN DE CONFIGS DE MODELOS (PIPELINING) ===")
print("=" * 80)

"""
Durante años los diccionarios sufrieron un mal en lectura Pythónica al intentar
"FUSIONAR" dos sets o dos listas de parametros o JSONs.
Teníamos `.update(dict_b)` Modificando Destructivamente In-Place.
O desempacotamiento absurdo de diccer `z = {**x, **y}` para hacer Merges seguros puristas.

A partir de Python 3.9, se aprobó la Ley PEP-584 del Kernel Integral C.
Se instanció el OPERADOR DE MERGE ( `|` ) y UPDATE MERGE MÁS RÁPIDO Y SINTÁCTICAMENTE LIMPIO ( `|=` ).
Usarlo es mandatorio en ML Ops.
"""
print("\n--- Pipeline Config Merging Moderno Pythonic (Pipe Operators) ---")

hiperparametros_base = {"modelo": "ResNet18", "epocas": 50, "lr": 0.01, "optimizador": "sgd"}
hiperparametros_custom = {"lr": 0.0005, "optimizador": "adamw_8bit", "scheduller": "cosine"}

# Queremos Combinar Base y Custom. Dando Pioridad Máestra a los Customs Sobre los Bases!
# Si colisionan los parametros, ¿Quien gana? El que esté a la derecha domina CPython y sobrescribe con Blood-Prio.

# Creación Inmaculada Aislada y Devuelta (Tercera Memoria Limpia Creada. Sin alterar ni la uno ni la dos)
configuracion_final_mergeada = hiperparametros_base | hiperparametros_custom

print(f"Fusión Perfecta Generativa 3.9+: \n {configuracion_final_mergeada}")
# Output Fiel: {'modelo': 'ResNet18', 'epocas': 50, 'lr': 0.0005, 'optimizador': 'adamw_8bit', 'scheduller': 'cosine'}
# Notese (LR fue reescrita por la Segunda, el Custom). SGD Destruida por Adam!

print("\n--- Destrucción Controlada Update In-Place (Operadores Asignadores) ---")
# ¿Y si no quiero fundar una Config_3 Inmacualada Extra que Malloc consuma mis Mbytes RAMS extras?
# Acuchillo In-Place Base. 

hiperparametros_base |= hiperparametros_custom
print(f"El Operador de asignacion (`|=`) es idéntico C-Layer a `hiper_b.update(hiper_c)` \n Resaltado Origen Updateado In Place O(N): \n {hiperparametros_base}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: MATRIZ DE DECSION IF-ELIF EXTINCTION (DISPATCH MAPS PATTERN) ===")
print("=" * 80)

"""
¿Cómo es el interior de un "Game Engine" para IA o los Agents LLM?
Usualmente el Junior escribe:
if act_ia == "mover": 
    agente.mover()
elif act_ia == "hablar":
    agente.hablar()
... 50 elifs.

Un asco ineficiente que obliga al intérprete Python a resolver las casillas lógicas C Branch Predictors,
provocando Branch Predictor Misses horribles cada Check False en el Pipeline C.
LA SOLUCIÓN SÉNIOR IA AL CÓDIGO CAOS ES EL PATRÓN "DISPATCH TABLE".
Diccionarios mapeados a funciones (First-Class Objects Referenciados O(1)).
"""

print("\n--- The Elegant Strategy O(1) Calling Flow ---")

def engine_hablar():   return "(Agente Hablando Pipeline Tensor NLP Output...)"
def engine_matar():    return "(Invocando Tool-Call Gun System Agentic...)"
def engine_observar(): return "(Activando Computer Vision CV2 YoloV9 ObjDetect...)"
def engine_default():  return "(Error IA Logica Interna Fallida del LLM. Herramienta Not Found.)"

# Un Diccionaro puede apuntar (Values Pointer) a Funciones Mismas de Python Core en lugar de Numeros!
ACCIONES_DEL_AGENTE_TABLA_IA = {
    "speakTool": engine_hablar,
    "killTool": engine_matar,
    "observeTool": engine_observar
}

comando_enviado_por_LLM = "observeTool"

# RESOLUCIÓN MILISEGUNDO DE INTELIGENCIA Y DISPARO SIN "IF" ALGUNO O(1).
resultado_del_engine_directo = ACCIONES_DEL_AGENTE_TABLA_IA.get(comando_enviado_por_LLM, engine_default)()
# Paréntesis Extras Mágicos Finales Invocan Pushing Local C-Call () El Callback Escupido ! O(1) Extracción y Execution!
print(f"Logica Neural Engine Exito Directo: {resultado_del_engine_directo}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 9: INDEXACIÓN INVERTIDA A BASE DICCIONARIOS PARA BUSQUEDAS EN RAG (O(1)) ===")
print("=" * 80)

"""
En NLP para Retrieval-Augmented Generation (RAG) necesitamos "encontrar el documento
que dice una cosa".
Si tengo 10,000 PDFS Textuales largos convertidos a Cadenas. Y busco la palabra 
"Inteligencia". NO ITERAS Y GREPPEAS 10,000 PDFS MIENTRAS ESPERA EL USUARIO A(O(N)).
Generas en pre-calculo (Indexación Invertida Diccionarial Coreana Base Algoritmic NLP).

Inverted Index es un Diccionario Gigante donde CLAVE = Palabra ÚNICA Universal! 
VALOR = {SET de IDS DE LOS DOCUMENTOS DEL CORPUS QUE LA TIENEN}. 
Extracción Cero Latence.
"""

doc_db_simulacional = {
    "Doc1": "el gato duerme",
    "Doc2": "la IA es peligrosa a veces",
    "Doc3": "el gato IA despierta super poderoso de repente inteligente"
}

indexado_invertido_nlp = {} # Mapeo Lexical

for id_del_doc, texto_del_doc_completo in doc_db_simulacional.items():
    las_palabras_tokenizadas_crudamente = set(texto_del_doc_completo.split()) # Purificamos duplicados internos locales O(1).
    for la_palabra in las_palabras_tokenizadas_crudamente:
        # Usa SET DEFAULT para setear con LISTA u SET limpio en la base para ir Sumando IDs de Docs!!
        if la_palabra not in indexado_invertido_nlp:
            indexado_invertido_nlp[la_palabra] = set()
        indexado_invertido_nlp[la_palabra].add(id_del_doc)

print("\n--- Búsqueda Inversa Indexada SuperVeloz NLP Algoritmic Core ---")
print(f"Extraccion de Vocablo Inverso C ['IA'] -> Documentos Encontrados Instantaneamente: {indexado_invertido_nlp.get('IA', set())} ")
print(f"Extraccion Lexical C ['gato'] -> Multi-Documentos Matching Sets O(1): {indexado_invertido_nlp.get('gato', set())} ")
# Nota: Obviamente en 2026 usamos Postgres_Vector / PG_vector / ChromaDB o Elasticsearch, pero su core matemático es exactamente ESTE (Suma Index Trie / Dictonarys).


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: SERIALIZACIÓN COMPLEJA JSON Y PERSISTENCIA (PICKLE) ===")
print("=" * 80)

"""
Estructura final vital. Un Diccione en Ram está condenado a Volatilidad (Se borrará si mueres Localmente CPytyhon Process).
En la IA guardamos, transferimos Datasets al Cloud Amazon AWS bucket u lo mandamos al Cache Redis.

Hay dos estándares Oficiales.
1. JSON -> Estandar Human-Readble cross-languages universal. Convierte el Dict (Si es unicamente cadenas y numeros) en Cadena De Texto JSON.
2. PICKLE -> CSerializer Nativo puro Object Dump (Binario). Persiste cosas Raras Híbridas Pythonicas que no existen en otros lenguajes.

AVISO MORTAL M.L CYBER-SECURTY: Nunca, JAMÁS cargues una IA guardada (`torch.load`) O Datset `pickle.load` o Pytorch Checkpoint .pt (que recogen Pickle Coreano) de internet desconocido!!.
El Modulo Pickle (Serializador Binario Oficial dict) permíte cargar EXPORTACIONES que contienen CÓDIGO EJECUTABLE (Payloads remotos virus).
PyTorch.load usa en el Back-end el módulo Pickle y miles de repositoriso open source se hackearon en 2023 por esto. Siempre SafeTensors moderno.
"""

print("\n--- La Serializacion JSON Estándar Nativa Rápida (C-Level Dump Hooks) ---")

config_ml_cloud_dict = {"learning": None, "boolsive": True, "epochs_runs": 55, "stringt_metadata": "Config_11A"}
json_payload = json.dumps(config_ml_cloud_dict, indent=2)

print(" -> Jsonificado de Dict:")
print(json_payload)

print("\n--- Archivo Pickle (Binario Obj Dumping Persistent Bytes) ---")

serializado_byte__picklesiano_bruto = pickle.dumps(config_ml_cloud_dict)
print(f"Pura Serialización Binara C Dump Pickled Dict State : \n{serializado_byte__picklesiano_bruto[:45]} [...]")
print("!Esta basura indescifrable Bytecode puede cargar Clases/Funciones Peligrosas! CUIDADO IA Hackers.")

# DeSerializacion:
reconstruyido = pickle.loads(serializado_byte__picklesiano_bruto)
print(f"Deserializando Obj Python... Comprobando Valor Extraído: {reconstruyido['boolsive']}")



print("\n" + "=" * 80)
print("=== CAPÍTULO 11: DICT COMPREHENSION AVANZADO PARA ML ===")
print("=" * 80)

"""
Así como las listas tienen List Comprehension, los diccionarios tienen 
Dict Comprehension. Se ejecuta a velocidad C y permite transformar,
filtrar y construir dicts de forma funcional sin loops explícitos.

Sintaxis: {key_expr: value_expr for item in iterable if condition}
"""

print("\n--- Transformación de features con Dict Comprehension ---")

# Normalización min-max de un vector de features
features_raw = {"altura": 175, "peso": 82, "edad": 35, "salario": 45000}

min_val = min(features_raw.values())
max_val = max(features_raw.values())

features_normalizadas = {
    k: (v - min_val) / (max_val - min_val) 
    for k, v in features_raw.items()
}
print(f"Features raw: {features_raw}")
print(f"Normalizadas: {features_normalizadas}")


print("\n--- Filtrado de hiperparámetros activos ---")

config_completa = {
    "learning_rate": 0.001,
    "dropout": 0.0,       # Desactivado (0.0)
    "weight_decay": 0.01,
    "momentum": 0.0,      # Desactivado (0.0)
    "epochs": 100,
    "patience": 0,        # Desactivado (0)
}

# Solo parámetros con valores activos (no cero)
config_activa = {k: v for k, v in config_completa.items() if v != 0}
print(f"Config activa (sin ceros): {config_activa}")


print("\n--- Inversión de diccionarios (swap keys/values) ---")

# Útil para mapeos bidireccionales en NLP (id->token, token->id)
vocab_token_a_id = {"[PAD]": 0, "[UNK]": 1, "[CLS]": 2, "[SEP]": 3, "gato": 4, "perro": 5}

# Invertir: id -> token
vocab_id_a_token = {v: k for k, v in vocab_token_a_id.items()}
print(f"Token->ID: {vocab_token_a_id}")
print(f"ID->Token: {vocab_id_a_token}")
print(f"  Token del ID 4: '{vocab_id_a_token[4]}'")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: APLANAMIENTO (FLATTENING) DE DICTS ANIDADOS ===")
print("=" * 80)

"""
En ML, las configuraciones reales son dicts ANIDADOS en múltiples niveles.
YAML, JSON de HuggingFace, model configs de PyTorch... todos requieren 
aplanar o navegar dicts profundos.
"""

print("\n--- Flatten recursivo de dict multinivel ---")

config_profunda = {
    "model": {
        "name": "transformer",
        "layers": {
            "encoder": 12,
            "decoder": 12,
            "hidden_size": 768
        },
        "attention": {
            "heads": 12,
            "dropout": 0.1
        }
    },
    "training": {
        "batch_size": 32,
        "optimizer": "adamw"
    }
}

def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """
    Aplana un diccionario anidado usando notación de puntos.
    Ej: {"model": {"name": "bert"}} -> {"model.name": "bert"}
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep))
        else:
            items[new_key] = v
    return items

config_plana = flatten_dict(config_profunda)
print(f"Config anidada aplanada:")
for clave, valor in config_plana.items():
    print(f"  {clave:<35} = {valor}")


print("\n--- Reconstrucción (unflatten) desde claves con puntos ---")

def unflatten_dict(d: dict, sep: str = ".") -> dict:
    """Reconstruye un dict anidado desde claves con notación de puntos."""
    resultado = {}
    for clave_plana, valor in d.items():
        partes = clave_plana.split(sep)
        objetivo = resultado
        for parte in partes[:-1]:
            if parte not in objetivo:
                objetivo[parte] = {}
            objetivo = objetivo[parte]
        objetivo[partes[-1]] = valor
    return resultado

reconstruida = unflatten_dict(config_plana)
print(f"\nReconstruida iguala a la original: {reconstruida == config_profunda}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: SIMULACIÓN DE STATE_DICT DE PYTORCH ===")
print("=" * 80)

"""
En PyTorch, model.state_dict() retorna un OrderedDict que mapea 
cada nombre de capa a su tensor de pesos. Es LA forma estándar
de guardar y cargar modelos.

Aquí simulamos cómo funciona para entender la estructura.
"""

print("\n--- Simulación de state_dict de una red neuronal ---")

# Simulamos pesos como listas (en realidad serían tensores NumPy/PyTorch)
import random
random.seed(42)

state_dict_simulado = {
    "embedding.weight": [random.random() for _ in range(10)],
    "encoder.layer_0.attention.weight": [random.random() for _ in range(5)],
    "encoder.layer_0.attention.bias": [random.random() for _ in range(5)],
    "encoder.layer_0.feedforward.weight": [random.random() for _ in range(8)],
    "encoder.layer_1.attention.weight": [random.random() for _ in range(5)],
    "encoder.layer_1.attention.bias": [random.random() for _ in range(5)],
    "classifier.weight": [random.random() for _ in range(3)],
    "classifier.bias": [random.random() for _ in range(3)],
}

print(f"Estado del modelo ({len(state_dict_simulado)} parámetros):")
total_params = 0
for nombre_capa, pesos in state_dict_simulado.items():
    n_params = len(pesos)
    total_params += n_params
    print(f"  {nombre_capa:<45} shape: [{n_params}]")

print(f"  Total parámetros: {total_params}")

# Filtrar solo los pesos de atención
pesos_atencion = {k: v for k, v in state_dict_simulado.items() if "attention" in k}
print(f"\nSolo capas de atención ({len(pesos_atencion)}):")
for k in pesos_atencion:
    print(f"  {k}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: **KWARGS Y UNPACKING PROFUNDO ===")
print("=" * 80)

"""
El operador ** (double splat) desempaqueta un diccionario en argumentos
con nombre. Es el pilar de las APIs flexibles en Python y en frameworks ML.

Tres usos principales:
1. **kwargs en funciones: captura argumentos con nombre arbitrarios.
2. **dict en llamadas: expande un dict como argumentos de función.
3. {**dict1, **dict2}: fusión pre-3.9 (antes de PEP-584 | operator).
"""

print("\n--- **kwargs: captura de argumentos arbitrarios ---")

def entrenar_modelo(modelo: str, epochs: int, **kwargs):
    """
    Función flexible que acepta cualquier hiperparámetro adicional.
    kwargs captura todos los argumentos con nombre que no están en la firma.
    """
    print(f"  Modelo: {modelo}, Epochs: {epochs}")
    print(f"  Hiperparámetros extra: {kwargs}")
    
    # Acceder a kwargs como un dict normal
    lr = kwargs.get("learning_rate", 0.001)
    optimizer = kwargs.get("optimizer", "adam")
    print(f"  LR resuelto: {lr}, Optimizer: {optimizer}")

entrenar_modelo("BERT", 10, learning_rate=0.0005, optimizer="adamw", warmup_steps=1000)


print("\n--- ** en llamadas: expandir dict como argumentos ---")

config_entrenamiento = {
    "modelo": "GPT-2",
    "epochs": 5,
    "learning_rate": 0.0001,
    "optimizer": "adam",
}

# El ** expande el dict en argumentos con nombre
entrenar_modelo(**config_entrenamiento)


print("\n--- Fusión con ** (pre-Python 3.9) ---")

defaults = {"lr": 0.001, "bs": 32, "opt": "sgd"}
customs = {"lr": 0.01, "bs": 64}

# Forma clásica (funciona en 3.5+)
merged = {**defaults, **customs}  # customs sobreescribe defaults
print(f"\n  Merged con **: {merged}")

# Forma moderna (3.9+)
merged_moderna = defaults | customs
print(f"  Merged con |:  {merged_moderna}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: dict.pop() Y PATRONES DE EXTRACCIÓN SEGURA ===")
print("=" * 80)

"""
dict.pop(key, default) extrae Y ELIMINA una clave del diccionario.
Retorna el valor extraído (o el default si no existe).
Es el bisturí quirúrgico para separar campos de un dict sin KeyError.
"""

print("\n--- Separación de metadata de un payload API ---")

payload_api = {
    "model": "gpt-4",
    "prompt": "Explica quantum computing",
    "temperature": 0.7,
    "max_tokens": 500,
    "api_key": "sk-SECRET-KEY-012345",
    "user_id": "usr_789",
}

# Extraer y ELIMINAR campos sensibles del payload antes de loggear
api_key = payload_api.pop("api_key")  # Extrae y elimina
user_id = payload_api.pop("user_id")  # Extrae y elimina
debug_mode = payload_api.pop("debug", False)  # No existe -> False

print(f"API Key (extraída): {api_key[:8]}...")
print(f"User ID (extraído): {user_id}")
print(f"Debug (default): {debug_mode}")
print(f"Payload limpio para log: {payload_api}")
# -> El payload ya no contiene datos sensibles


print("\n" + "=" * 80)
print("=== CAPÍTULO 16: TABLA DE COMPLEJIDAD COMPLETA DE DICT ===")
print("=" * 80)

"""
╔═══════════════════════════════════╦═══════════════════╗
║ OPERACIÓN                         ║ COMPLEJIDAD       ║
╠═══════════════════════════════════╬═══════════════════╣
║ dict[key]                         ║ O(1) promedio     ║
║ dict[key] = value                 ║ O(1) promedio     ║
║ del dict[key]                     ║ O(1) promedio     ║
║ key in dict                       ║ O(1) promedio     ║
║ dict.get(key, default)            ║ O(1) promedio     ║
║ dict.setdefault(key, default)     ║ O(1) promedio     ║
║ dict.pop(key)                     ║ O(1) promedio     ║
║ dict.update(other)                ║ O(M) donde M=other║
║ dict.keys() / .values() / .items()║ O(1) (vista)      ║
║ len(dict)                         ║ O(1)              ║
║ dict.copy()                       ║ O(N)              ║
║ dict | dict2  (merge PEP-584)     ║ O(N + M)          ║
║ for k in dict                     ║ O(N)              ║
║ dict comprehension                ║ O(N)              ║
╚═══════════════════════════════════╩═══════════════════╝

NOTA: "O(1) promedio" significa O(1) amortizado. En el PEOR caso
(todas las claves colisionan), sería O(N), pero esto es 
estadísticamente imposible con el probing de CPython.

REGLAS DE ORO:
1. Siempre usa .get(key, default) en vez de dict[key] en producción.
2. Usa | para merge en vez de crear dicts temporales con {**a, **b}.
3. NUNCA modifiques un dict mientras iteras sus vistas -> list() primero.
4. Para configs inmutables, usa types.MappingProxyType (read-only view).
"""


print("\n" + "=" * 80)
print("=== CAPÍTULO 17: MAPPINGPROXYTYPE — DICCIONARIOS INMUTABLES ===")
print("=" * 80)

"""
Python no tiene un dict inmutable nativo (equivalente a frozenset vs set).
Pero el módulo `types` ofrece MappingProxyType: una VISTA DE SOLO LECTURA
sobre un diccionario existente. Cualquier intento de modificación lanza TypeError.

En MLOps esto es fundamental para:
- Proteger configuraciones de producción contra modificaciones accidentales.
- Pasar configs a funciones garantizando que NO las alterarán.
- Crear registros de hiperparámetros que NO se puedan mutar post-experimentación.
"""

from types import MappingProxyType

print("\n--- Creación de config inmutable ---")

config_interna_mutable = {
    "model": "BERT-base",
    "hidden_size": 768,
    "num_layers": 12,
    "learning_rate": 0.0001,
}

# Crear vista inmutable
config_publica = MappingProxyType(config_interna_mutable)

print(f"Lectura OK: {config_publica['model']}")
print(f"Tipo: {type(config_publica)}")

# Intento de modificación -> BLOQUEADO
try:
    config_publica["learning_rate"] = 0.01
except TypeError as e:
    print(f"Modificación bloqueada: {e}")

# Pero el dict ORIGINAL sigue siendo mutable (la proxy refleja cambios)
config_interna_mutable["epochs"] = 100
print(f"Reflejado desde el original: {config_publica.get('epochs')}")
print(f"  -> MappingProxyType es una VISTA, no una copia.")

# Patrón de producción: exponer la proxy, mantener el original privado
class ModelRegistry:
    """Registro de modelos con configuraciones protegidas."""
    def __init__(self):
        self._configs = {}
    
    def register(self, name: str, config: dict):
        self._configs[name] = config.copy()
    
    def get_config(self, name: str):
        """Retorna config como solo lectura."""
        return MappingProxyType(self._configs[name])

registry = ModelRegistry()
registry.register("bert", {"lr": 0.001, "layers": 12})
safe_config = registry.get_config("bert")
print(f"\nConfig protegida: {dict(safe_config)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 18: OPERACIONES DE CONJUNTO SOBRE DICT VIEWS ===")
print("=" * 80)

"""
Los dict_keys y dict_items se comportan como SETS.
Puedes hacer intersección, unión y diferencia entre las claves
de dos diccionarios. Esto es extremadamente útil para comparar
configuraciones o detectar diferencias entre modelos.
"""

print("\n--- Comparación de configs de dos experimentos ---")

exp_a = {"lr": 0.001, "batch_size": 32, "epochs": 50, "optimizer": "adam"}
exp_b = {"lr": 0.01,  "batch_size": 64, "epochs": 50, "scheduler": "cosine"}

# Claves comunes (intersección)
claves_comunes = exp_a.keys() & exp_b.keys()
print(f"Claves comunes: {claves_comunes}")

# Claves solo en A (diferencia)
solo_en_a = exp_a.keys() - exp_b.keys()
print(f"Solo en exp_a: {solo_en_a}")

# Claves solo en B
solo_en_b = exp_b.keys() - exp_a.keys()
print(f"Solo en exp_b: {solo_en_b}")

# Todas las claves (unión)
todas = exp_a.keys() | exp_b.keys()
print(f"Todas las claves: {todas}")

# Detectar qué valores CAMBIARON entre los dos experimentos
cambios = {k: (exp_a[k], exp_b[k]) for k in claves_comunes if exp_a[k] != exp_b[k]}
print(f"\nParámetros que cambiaron: {cambios}")
sin_cambio = {k: exp_a[k] for k in claves_comunes if exp_a[k] == exp_b[k]}
print(f"Parámetros sin cambio:    {sin_cambio}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 19: WALRUS OPERATOR EN PATRONES DE DICT ===")
print("=" * 80)

"""
El walrus operator (:=) de Python 3.8+ permite asignar y usar un valor
en la misma expresión. Es muy útil con diccionarios para evitar
dobles búsquedas (primero comprobar si existe, luego obtener el valor).
"""

print("\n--- Patrón: evitar doble lookup con := ---")

cache_resultados = {"exp_001": 0.92, "exp_002": 0.87}

# SIN walrus: doble búsqueda
exp_id = "exp_001"
if exp_id in cache_resultados:
    resultado = cache_resultados[exp_id]
    print(f"Sin walrus - Encontrado {exp_id}: {resultado}")

# CON walrus: una sola búsqueda
if (resultado := cache_resultados.get("exp_002")) is not None:
    print(f"Con walrus - Encontrado exp_002: {resultado}")

if (resultado := cache_resultados.get("exp_999")) is not None:
    print("No debería llegar aquí")
else:
    print(f"Con walrus - exp_999 no encontrado, resultado = {resultado}")


print("\n--- Walrus en procesamiento de datos ---")

# Patrón real: procesar datos solo si cumplen condición
registros = [
    {"tipo": "metric", "valor": 0.95},
    {"tipo": "log", "mensaje": "Epoch 5 completado"},
    {"tipo": "metric", "valor": 0.97},
    {"tipo": "error", "mensaje": "GPU memory overflow"},
]

metricas_encontradas = [
    v 
    for reg in registros 
    if (v := reg.get("valor")) is not None
]
print(f"Métricas extraídas con walrus: {metricas_encontradas}")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN DE INGENIERÍA: ARQUITECTURA HASH-MAP DE DICCIONARIOS PURE ===")
print("=" * 80)

"""
Resumen Definitivo MLOps Core Hash Maps:

1. Son inmensamente potentes bajo el Algoritmo O(1) de Hashings y Resolution 
   Cuadratic Probe Python Base C-Layer Arrays DkIndices / Entries (3.6+).

2. Tienen una regla de Hierro Imperturbable: KEY DEBE SER INMUTABLE / HASHABLE.
   Las Listas nunca. Las Tuplas siempre ok.

3. Se protegen contra Loops If Else tontos utilizando métodos .GET() con 
   parámetros Fallback y .SETDEFAULT() C-Core Pushers.

4. Redoblan el rendimiento de Loops Ciegos mediante ViewObjects O(1) 
   `.items()` Views Pointer Extractor Live.

5. Se funden Elegantemente bajo la norma PEP-584 de Pipelining configs 
   Operators (`| ` y ` |=`).

6. Sirven de Matrices Punteros Algoritmicas Dispatch para IAs Game Engines 
   y RAGs Local Inverted Indexes en Texto NLP.

7. Dict Comprehension para transformar, filtrar e invertir dicts a velocidad C.

8. Flatten/Unflatten para navegar configs multinivel (YAML, JSON, HuggingFace).

9. state_dict() de PyTorch es un OrderedDict: dominar dicts es dominar 
   la persistencia de modelos.

10. **kwargs para APIs flexibles; dict.pop() para extracción quirúrgica.

11. MappingProxyType para configs inmutables en producción.

12. dict.keys() soporta operaciones de SET (&, |, -) para comparar configs.

Con esto, has destruido y conquistado la estructura de Diccionarios.
"""
print(" FIN DE ARQUIVO 02_diccionarios_hashmaps. Python MLOps Framework Cerrado Exhaustivo.")
