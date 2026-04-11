# ===========================================================================
# 01_listas_y_arrays_dinamicos_profundo.py
# ===========================================================================
# MÓDULO 02: ESTRUCTURAS DE DATOS NATIVAS (AISLADAS)
# ARCHIVO 01: Listas y Arrays Dinámicos a Nivel CPython y Sistemas IA
# ===========================================================================
#
# OBJETIVO DE INGENIERÍA Y DOMINIO ABSOLUTO (1000+ LÍNEAS):
# Dominar absoluta y categóricamente la estructura de datos madre de Python:
# LA LISTA. Romperemos los mitos de "lista enlazada", exploraremos su memoria
# en el lenguaje C subyacente (C-Python PyListObject) e implementaremos todo
# el abanico de operaciones posibles. Analizaremos por qué su ineficiencia en
# operaciones matemáticas puras empujó a la creación de NumPy para el Machine Learning.
#
# Este documento no resume nada. Examina:
# 1. Punteros `ob_item` y Memory Fragmentations.
# 2. Análisis del Bytecode mediante `dis` para descubrir los opcodes.
# 3. Reference Cycles (Ciclos de referencias destructivos para el Garbage Collector).
# 4. Implementaciones puras de ML desde Cero construyendo Datasets con Slicing Extremo.
# 5. La diferencia arquitectónica entre Subclasificar The Built-in `list` y `UserList`.
#
# NIVEL: EXPERTO EN INFRAESTRUCTURA M.L. / CORE PYTHON DEV.
# ===========================================================================

import sys
import copy
import time
import dis
import random
import tracemalloc
import gc
from collections import UserList


print("\n" + "=" * 80)
print("=== CAPÍTULO 1: LA REALIDAD FÍSICA Y EL C-STRUCT DE UNA LISTA ===")
print("=" * 80)

"""
En muchos lenguajes clásicos (LISP, C++ std::list), una "Lista" suele referirse a 
una "Linked List" (Lista Enlazada).
En una LinkedList, cada objeto de memoria tiene dos cosas: El Dato físico y un Puntero
diciendo en qué sector remoto de la placa RAM está el "Siguiente Objeto". Esto hace que 
el coste computacional de buscar el objeto número 10,000 en la RAM sea O(N), porque 
te obliga a "saltar" uno a uno siguiendo el mapa para encontrarlo.

EN PYTHON, LA LISTA (list) NO ES UNA LISTA ENLAZADA.

En los cimientos de CPython (el intérprete de C base de tu sistema), el código fuente 
`Include/listobject.h` define que una lista es esto:

typedef struct {
    PyObject_VAR_HEAD
    PyObject **ob_item;
    Py_ssize_t allocated;
} PyListObject;

La estructura física real tiene tres cosas críticas que un Ingeniero IA debe memorizar:
1. `PyObject_VAR_HEAD`: Una cabecera (Header) genérica que TODA variable de Python tiene.
    Aquí se guarda el famoso "Reference Count" para el Garbage Collector, y el TAMAÑO actual
    legible (El `len()` O(1)).
2. `**ob_item`: DOBLE ASTERISCO. En el Lenguaje C esto es un puntero a un Array de Punteros.
    Significa que la Lista no guarda los datos. Repito. LA LISTA NO GUARDA LOS STRINGS 
    NI LOS INTS. Guarda referencias puras de 8 Bytes que apuntan a otras direcciones de RAM.
    ¡Por eso puedes meter un Objeto TensorFlow, seguido de un String, seguido de un Int!
3. `allocated`: Memoria en exceso guardada pero no reportada por `len()`. Si la lista
    tiene 3 elementos, el Allocated de C a lo mejor es 8. Esto salva a la CPU de tener 
    que pedir permisos a tu Sistema Operativo al agregar los siguientes cinco items.

LIMITACIONES MATEMÁTICAS EN M.L. (Y por qué existe NumPy):
La CPU de tu ordenador moderno tiene L1, L2 y L3 Caches super eficientes. 
Si los dígitos matemáticos de los pesos neurales están en fila pegados en la placa de silicio,
la CPU los procesa literalmente de a 4 en 4 (Instrucciones SIMD Vectorizadas).
Al usar las Listas de Python, la CPU pide el segundo item, extrae el Puntero, va al otro extremo
de la Ciudad de la Memoria RAM a buscarlo, lo opera, pide el tercero, y salta de nuevo.
Este terrible fenómeno se llama "CACHE MISS" (Fallo de caché local). Destroza el rendimiento.
"""

print("\n--- Analizando la Pesa Genérica Mínima ---")

# Una Lista con un solo dígito simple
mi_lista_basica = [1]

print(f"Lista Base: {mi_lista_basica}")
print(f"Tipo Base: {type(mi_lista_basica)}")
# En Arquitecturas de 64 bits, una Lista Vacia ronda los 56 bytes reales. 
# Añadirle "1" elemento le inyecta +8 Bytes (Total ~64 bytes de Objeto de Infraestructura).
peso_lista_bytes = sys.getsizeof(mi_lista_basica)
print(f"Tamaño Estructural (Excluye a los elementos meta) -> {peso_lista_bytes} bytes")

print("\n--- Demostración de Punteros Heterogéneos ---")

# Construiremos Strings que ocupan KILOBYTES reales de RAM
texto_gigante_a = "P" * 100_000   # String de ~100 KB
texto_gigante_b = "X" * 100_000   # String de ~100 KB

print(f"Peso del string Texto A: {sys.getsizeof(texto_gigante_a)} Bytes reales")

lista_gigantesca = [texto_gigante_a, texto_gigante_b]
# ¡ALERTA! El peso a continuación no debe ser 200 KB!.
peso_lista_gigantesca = sys.getsizeof(lista_gigantesca)
print(f"Peso Estructural de la Lista Alojadadora: {peso_lista_gigantesca} Bytes")

if peso_lista_gigantesca < 200_000:
    print(" -> EL CONCEPTO ESTÁ DEMOSTRADO: La Lista jamás retuvo a los Strings Gigantes.")
    print(" -> Solo retuvo DOS PUNTEROS de 8-bytes (*ob_item) atados a los Strings de alcance Global.")
    print(" -> ESTE ES EL SECRETO DE PYTHON DE BAJO NIVEL.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: CREACIÓN, CASTEO Y OPERACIONES DE INGESTA MASIVAS ===")
print("=" * 80)

"""
¿Cómo debe un Ingeniero MLOps cargar los logs de validación o inicializar colecciones?
La inicialización debe estar guiada por el AST (Abstract Syntax Tree) hacia el compilador puro.
"""

print("\n--- El Bytecode de Crear Listas (Corchetes vs List Class) ---")

def creador_lista_literal():
    return []

def creador_lista_funcion():
    return list()

print("Desamblando `[]` -> Literal:")
dis.dis(creador_lista_literal)
# Instrucción limpia: BUILD_LIST (Orden directa a C). Rápido, furioso.

print("\nDesamblando `list()` -> Función:")
dis.dis(creador_lista_funcion)
# Instrucciones Complejas: LOAD_GLOBAL (Ir al entorno y buscar 'list'), 
# y luego CALL_FUNCTION (Lanzar un wrapper de ejecución C). LENTO.

"""
Regla #1: Siempre que inicialices un buffer, hiperparametro, loop_state vacio,
USA LOS CORCHETES `[]`.
"""

# Casting y Transformaciones directas C-Level (Ingesta de iterables)
# Cuando tienes un conjunto matemático estricto y quieres convertirlo, `list()`
# lee en C-Layer el tamaño del objeto Set/Range y pide memoria "Allocated" DE GOLPE.
# Esto es O(N) infinitamente más rápido que hacer list.append() N veces.

rango_millonario = range(1_000_000)
# list() sabrá la respuesta y pedirá "MALLOC" de 8 MB exactos al OS instantáneamente.
lista_casting_puro = list(rango_puro := range(5))
print(f"\nDesde clase C (Rápido): {lista_casting_puro}")

# Tipado Fuerte para Listas en Arquitecturas (Python 3.9+)
# Ideal para linters Mypy en proyectos OpenSource
def entrenar_modelo_vision(layers: list[int], activations: list[str]) -> list[float]:
    # El type-hint indica la intención explícita al programador, pero en ejecución
    # Python lo ignorará, manteniendo la arquitectura dinámica y flexible.
    return [0.99, 0.98, 0.94]

print(f"Return Tipado: {entrenar_modelo_vision(layers=[64, 128], activations=['relu'])}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 3: MATEMÁTICA ASINTÓTICA (O(N)) EN MÉTODOS NATIVOS ===")
print("=" * 80)

"""
Manejar el C-"Dynamic Array" conlleva Regalos y Penalizaciones críticas absolutas.
La penalización principal viene de "desplazar" Punteros de Array en RAM C.
Si tengo un tren de 1 Millón de vagones y trato de inyectar AL PRINCIPIO un nuevo
vagón con `.insert(0, X)`. Python está OBLIGADO a desplazar físicamente cada uno
de los 1,000,000 Punteros (A uno contiguo +1 del Array Ob_item). 
Esto fusilará la CPU. Totalmente prohibido.
"""

# Inicializamos buffer
memoria_lote = [10, 20, 30, 40, 50]
print(f"\nBuffer Base: {memoria_lote}")

# ─── 3.1 OPERACIONES GRATUITAS: CONSTANTES O(1) ───

# 1. Agregado al fondo libre de punteros (Amortizado)
memoria_lote.append(60)       
print(f" Tras APPPEND(60) [O(1) Garantizado]: {memoria_lote}")

# 2. Extirpación Final Ciega (Amortizada)
# Guarda el return si es necesario. No toca el resto del array lógico.
ultimo_dato = memoria_lote.pop()   
print(f" Tras POP() Final Extrajo '{ultimo_dato}' [O(1)]: {memoria_lote}")

# 3. Sustituciones por índice directo
memoria_lote[2] = 999          
print(f" Tras SET [2] = 999 [O(1) Memoria Contigua de Puntero]: {memoria_lote}")

# 4. Chequeo de Identidad y Longitud CPython
# `len()` NO cueta elementos!!. No va de 0 a final del tren evaluando si exsten.
# Va a la "PylistObject -> ob_size" que es un Int físico almacenado!.
tamanio_inst = len(memoria_lote) 
print(f" Extracción de `len` pura. [O(1)] Tamaño estático: {tamanio_inst}")


# ─── 3.2 TRABAJO ARDUO (PELIGRO CPU): LINEALES O(N) ───

print("\n(Simulando la Catástrofe Local de Memoria en Cuellos De Botella IA):")

buffer_secundario = [1, 2, 3, 4]

# 1. INSERCION PELIGROSA -> `insert(indice, valor)`
buffer_secundario.insert(0, 100) 
print(f" Insert in posición 0 [O(N)]: {buffer_secundario} (Toda la fila se recorrió)")
# SOLUCIÓN en Ingeniería:
# Si necesitas empujar cosas tanto por detrás como por DElANTE CONSTANTEMENTE, no usas list.
# USAS >> collections.deque  (Que es la implementación purísima y real en C de Linked List).

# 2. EVALUACIÓN Y PURGA CIEGA -> `remove(valor)`
# Realiza Internamente una Fase Búsqueda O(N) y luego una Fase Desplazamiento O(N).
try:
    buffer_secundario.remove(3) 
    print(f" Remove Valor 3 [O(N) * 2]: {buffer_secundario}")
except ValueError:
    pass
# Dato Avanzado: `.remove(obj)` solo borra la PRIMERA coincidencia izquierda-derecha. No borra Duelos.

# 3. VERIFICACIONES DE PRESENCIA NATIVA (A.K.A BUSQUEDAS EN BUCLE)
# `if objetivo in lista:`  -> Escáner de Secuencia Linear 
es_valido = 99 in buffer_secundario  # O(N)
indice_presencia = buffer_secundario.index(4) if 4 in buffer_secundario else -1  # O(N) + O(N) = O(2N) MAL.
print(f" Está 99?: {es_valido} | Índice de 4: {indice_presencia}")

# ─── 3.3 CONCATENACIONES (ADD VS EXTEND) ───

arr_A = [1, 2]
arr_B = [3, 4]

# Operación A: `+` Suma Aritmética
# Crea una TERCERA lista en RAM libre de CPython, Pide un OS Malloc Total, clona A y B.
# O(Len(A) + Len(B)). Memorié Exhaustiva y dolorosísima si se hace en bucles FOR de 1 Millon iters.
arr_C = arr_A + arr_B 

# Operación B: `+=` ó `.extend` MODO IN-PLACE (En Sitio)
# Analiza Arr_A. Ve que le caben 2 items extra. Empuja punteros al fondo sin Malloc Extra y retorna.
# O(Len(B)) pura. Consumo Minimo de Garbage.
arr_A.extend(arr_B) 
# Identico en bytecode: arr_A += arr_B


print("\n" + "=" * 80)
print("=== CAPÍTULO 4: LA FÓRMULA DE OVER-ALLOCATION AL MILLÍMETRO ===")
print("=" * 80)

"""
Revisita teórica de C-Language Core Python.
Mencioné el Allocated, pero ¿por qué importa esto? Porque cuando cargas datasets
con un bucle For Loop mediante list.append(features), tu ordenador va dar unos 
pequeños tropiezos (Stutters). 

Fórmula Interna Oficial CPython 3.10+ (List Resize Algo):
```c
size_t new_allocated = (size_t)newsize + (newsize >> 3) + (newsize < 9 ? 3 : 6);
```
Cuando "newsize" (Tú exiges meter 1 elemento más) supere el "Allocated" anterior, 
el Cpython te dará de forma gratuita `(TAMAÑO // 8)` (El Bitwise shift >> 3) mas unos +3/+6 libres.

Demostremos esto haciendo un Log Histórico de memoria.
"""

print("\n--- Demostración de Saltos Malloc Internos en tu RAM ---")

lista_crecimiento_vivo = []
bytes_historicos = sys.getsizeof(lista_crecimiento_vivo)

print(f"0 items: Buffer inicial de la Lista vacía: {bytes_historicos} Bytes")

# Si inyectamos un millón de datos... ¿Cuántas veces interrumpe al Sistema Operativo?
cuantas_veces_pidio_memoria = 0
for iterador_elemento in range(1, 20_000):
    lista_crecimiento_vivo.append("Datos")
    bytes_actuales = sys.getsizeof(lista_crecimiento_vivo)
    
    # Si la lista creción, hubo OverAllocation.
    if bytes_actuales > bytes_historicos:
        if cuantas_veces_pidio_memoria < 8: # Print solo de los 8 primeros estallidos visuales.
            print(f" + Salto de Puntero! Al inyectar elemento [{iterador_elemento}], la Memoria Virtual saltó de {bytes_historicos} -> a {bytes_actuales} Bytes")
        cuantas_veces_pidio_memoria += 1
        bytes_historicos = bytes_actuales

print(f"... (Interrupciones silenciadas) ...")
print(f"Para insertar {len(lista_crecimiento_vivo)} elementos en secuencia pura, laLista pidió C-Mallocs extra SOLO {cuantas_veces_pidio_memoria} veces reales!")
print(" -> !Por Eso O(1) Amortizado es Incontestable y brutalmente rápido!")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: LA REFERENCIA SUPERFICIAL (TRAMPAS M.L EN MATRICES) ===")
print("=" * 80)

"""
EXAMEN CLÁSICO DE MACHINE LEARNING ENGINEER. (Bugs Destructores de Redes).
Estás armando una matriz bidimensional (Tablero, Pixeles Padding, Matriz Confusión),
y te dejas llevar por los Operadores Matemáticos directos sobre String-Lists de Python.
"""

print("\n--- EL ANTIPATRÓN DEL JUNIOR (*) ---")

# Inocente: Quiero una Matriz 3x3 rellena de Ceros. Cogeré una Fila `[0]*3` y la multilicaré
tablero_venenoso = [[0] * 3] * 3

print("Matriz inicial construida:")
for renglon in tablero_venenoso: print(f"  {renglon}")
    
# De repente, tu modelo IA procesa y actualiza la prediccion 0 en la fila 0 de las Confusions.
tablero_venenoso[0][0] = 999  # Literalmente dice: Edita la Posicion 0 de la Fila 0.

print("Matriz Mutada tras una injección en Pos [0,0]:")
for renglon in tablero_venenoso: print(f"  {renglon}")

"""
[999, 0, 0]
[999, 0, 0]
[999, 0, 0]

¡¿CÓMO ES POSIBLE QUE MUTE LA FILA 2 Y 3 SI SOLO TOQUÉ LA CERO?!
Respuesta: Python y el Asterísco `*`.
Python NO clona un objeto Mutalbe (El `[0] * 3` del paréntesis de arriba). CPython
creó UNA SOLA list interna de memoria ID 0xFFFF. Y luego copió ESE PUNTERO 0xFFFF tres veces
para meterlo al array madre.
Las Cuatro variables son un Espejo! Comparten Fysis-Memoria. Un Shallow Trap en toda regla.
"""

print("\n--- LA CONSTRUCCIÓN EXPERTA (LIST COMPREHENSION DESLIGADO) ---")

# Obligamos a la CPU a Instanciar una Lista NUEVA (`[0,0,0]`) en CADA CICLO 
# del iterador For Oculto C. Generando ID RAMS Unicas que jamás conectaran entre sí.

tablero_sanado = [[0] * 3 for ciclo_vacio in range(3)] 

tablero_sanado[0][0] = 999 # Operamos sobre el array único puro de Fila 0.
print("Tablero Sano operado en [0][0]:")
for reg in tablero_sanado: print(f"  {reg}")

print("\nCorroboración con Sistema de Identificaciones Hash Subyacente (C-id()):")
print(f" -> ID Rama 0 Tablero FALSO: {id(tablero_venenoso[0])}  |  ID Rama 1 Tablero FALSO: {id(tablero_venenoso[1])} (Iguales! Espejos!)")
print(f" -> ID Rama 0 Tablero SANO:  {id(tablero_sanado[0])}  |  ID Rama 1 Tablero SANO:  {id(tablero_sanado[1])} (Distinct Memory!)")


print("\n" + "=" * 80)
print("=== CAPÍTULO 6: CLONACIÓN MASIVA EN PROFUNDIDAD (SHALLOW COPY VS DEEPCOPY) ===")
print("=" * 80)

"""
Avanzando en la clonación, a veces te descargas configuraciones Base desde APIs, 
tienes Datasets que purgar para Data-Traning por un parte, y Data-Validation por otra.
Pero debes CORTAR el cordon que los ata al original.
"""

configuracion_llm_json_simulado = ["GPT-4", [1024, 512, "ReLU"], {"temp": 0.7, "top_p": 0.9}]

print("\n--- COPY SUPERFICIAL (SHALLOW COPY) ---")
# Todos estos métodos clonan la Raíz, pero los Hijos Adentro siguen atados por Shallow Ref:
# 1. lista.copy()
# 2. list(lista)
# 3. lista[:]

config_shallow_copia = configuracion_llm_json_simulado.copy()

# Alteramos el diccionario profundo interno de la Clónica "Modificando la Temperatura a 1.0"
config_shallow_copia[2]["temp"] = 1.0

print(f"Originaria Config(Afectada en Origen Peligro!): {configuracion_llm_json_simulado[2]}")
print(f"Copia Config   (Alterada legalmente!): {config_shallow_copia[2]}")
# Ambás arrojarán 'temp'=1.0, rompiendo los records históricos o las consts originales.

print("\n--- COPY PROFUNDO RECURSIVO (DEEPCOPY MODULE) ---")
# Debemos Importar la Librería `copy` estándar del core que maneja HashMaps internos y 
# recursiones complejas para purgar y regenerar todas las capas inferiores.

configuracion_llm_json_simulado_2 = ["LLaMA", [4096, 4096, "GeLU"], {"temp": 0.7, "top_p": 0.9}]
configuracion_DEEP_CLONE = copy.deepcopy(configuracion_llm_json_simulado_2)

configuracion_DEEP_CLONE[2]["temp"] = 100.0 # Hack extremo

print(f"Originaría V2 Profundizada (SE SALVÓ! Sigue): {configuracion_llm_json_simulado_2[2]}")
print(f"Copia Devastada (Solo sufrió lo clónico local): {configuracion_DEEP_CLONE[2]}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 7: LA COMPRESSION MATRIX E IMPLEMENTACIONES PURAS DE M.L ===")
print("=" * 80)

"""
Los "List Comprehension" empujan la lógica a nivel C pre-ejecutando.
Eliminan el retardo del Opcode CALL_FUNCTION y LOAD_LOCAL en bucles For estándar.
Pero podemos anidarlos y crear magia.
"""

print("\n--- Normalizando Características de Dataset (Map / Filter 1D) ---")
sensores_temperaturas_float = [ 23.4, -400.1, 22.1, 45.9, -270.0, 18.0 ] 

# Lógica IA: Ignorar el sensor si reporta menores que Cero (errores absolutos). Multiplicar validas por *100 de escalado.
# A NIVEL C-SPEED: [ EXPRESION   FOR-LOOP   IF-FILTER ]
sensores_normalizados = [ (temp * 100.0) for temp in sensores_temperaturas_float if temp > 0.0 ] 
print(f"Pipeline Funcional limpio (Normalizados Positivos): {sensores_normalizados}")


print("\n--- List Comprehension 2D (Aplastamiento de Tensores [Flatten]) ---")
un_tensor_3D_matrices_rgb = [
    [255, 128, 64],  # Fila Pixeles Top
    [100, 200, 0 ],  # Fila Pixeles MID
    [10 , 20 , 30]   # Fila Pixeles BOT
]

# Las redes Fully Connected (Dense Layers) requieren la imagen "Aplastada" a Un vector lineal puro 1D.
# COMPREHENSION ANIDADO: DE IZQUIERDA A DERECHA EN CASCADA COMO FOR-LOOPS DE ABAJO A ARRIBA MATEMÁTICAMENTE:
vector_aplanado_input = [ 
    pixel_unitario 
    for fila_pixelada in un_tensor_3D_matrices_rgb 
    for pixel_unitario in fila_pixelada 
]
print(f"Imagen (3x3) Transformada a Matriz Densa 1D (Para red MLP Base): {vector_aplanado_input}")


print("\n--- Ejercicio Pro Extremo: Múltiplicación de Matrices Matemáticas puras ---")
# Una IA cruza Pesos X Entradas. Matriz A * Matriz B (Dot Product).
# A = 2x3,  B = 3x2  => Resultado C = 2x2.
Mat_A = [[1, 2, 3], 
         [4, 5, 6]]

Mat_B = [[7, 8], 
         [9, 1], 
         [2, 3]]

# ¡MÚLTIPLICACIÓN USANDO *ZIP* COMPREHENSION PARA COLUMNAS Y FILAS C-LEVEL!
# 1. Hacemos Transposición mágica de Mat_B usando Zip(*Matrix)
# 2. Hacemos Producto Escalar
# 3. Empaquetamos todo.

# La Matriz B "Transpuesta" intercambia filas a columnas: B_T = [(7,9,2), (8,1,3)]
Matriz_Resultado = [
    [
        sum(item_a * item_b_t for item_a, item_b_t in zip(fila_a, columna_b)) 
        for columna_b in zip(*Mat_B) # Magia ZIP* Transpone en C la Matrïz derecha entera!.
    ]
    for fila_a in Mat_A
]
print(f"\nResultado MatMath 2x2 Creado Artesanalmente con Lists Comprehensions: \n {Matriz_Resultado[0]} \n {Matriz_Resultado[1]}")
# Deberá ser: [1*7 + 2*9 + 3*2 = 31... ] [31, 19] / [85, 55].


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: SLICING Y EL DESTRUCTOR IN-PLACE DEL PUNTERO C ===")
print("=" * 80)

"""
El "Slice" (`secuencia[inicio : fin_exclusivo : paso]`) es la tecnología con la que se 
manejan los Batch_loaders en PyTorch antes de ceder al C++.
"""
correa_de_datos = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# --- SLICING PREDOMINANTE ---
print("\n--- Cortes Vectorizados BATCHING ---")

b_size = 4
primer_gran_lote = correa_de_datos[:b_size]           # Hasta indice 3 (Cuatro primeros elementos)
ultimo_gran_lote = correa_de_datos[-b_size:]          # El guion pide Indices Negativos a fondo del Train Array. [70, 80]
lote_intermedio  = correa_de_datos[b_size: b_size*2]  # Lote intermedio 2

print(f"Batch Forward: {primer_gran_lote} | Inter: {lote_intermedio} | Tail: {ultimo_gran_lote}")

# --- STRIDES (SALTOS) Y SEPARACIÓN DATASET / SUBSAMPLING ---
print("\n--- Strides Alternos y Tunning ---")
los_datos_pares_frecuencias = correa_de_datos[::2]  # Coge toda la tabla, saltndo de a 2.
print(f"Separación Frecuencias Senoidales / Impar / Data: {los_datos_pares_frecuencias}")

girar_sentido_series_temporales = correa_de_datos[::-1]
print(f"Flip Completo Bidireccional Time-Series Model: {girar_sentido_series_temporales}")


# --- DESTRUCTOR DE MEMORIA IN-PLACE HACKING ---
# Las listas permiten REEMPLAZAR secuencias por iterables COMPLETAMENTE DESIGUALE EN TAMAÑO!
base_estatica_c = [1, 1, 1, 1, 1]
pointer_memoria_estatica = id(base_estatica_c)

# Destruimos los tres unos internos (indice 1 al 4 exclusivo).
# Inyectamos CINCO NUEVES donde antes cabian TRES UNOS. Pliégalos como Malloc Mágico.
base_estatica_c[1:4] = [999, 999, 999, 999, 999]

print(f"\nHack In-Place Replacement: {base_estatica_c}")
print(f" Punteros Inalterables?: {id(base_estatica_c) == pointer_memoria_estatica} (Sí, conservan las dependencias del OS).")


print("\n" + "=" * 80)
print("=== CAPÍTULO 9: DEL `DEL` AL GARBAGE COLLECTOR & REFERENCE CYCLES ===")
print("=" * 80)

"""
Para borrar objetos tienes tres caminos.
`A.pop(x)` -> Extrae el return O(N)
`A.remove(val)` -> Busca y extrae el primero coincidente O(N)
`del A[slice]` -> Instrucción directa a nivel C (No es una función, es Operador Core). Coge Cuchillo e interrumpe punteros O(N).
"""

print("\n--- La instrucción `del` Nativa del SO ---")
array_carnicero = [0, 1, 2, 3, 4, 5, 6, 7]
del array_carnicero[::2]  # Acuchillamos posiciones pares usando Slacing Strided. Instantáneo CPython Block Release!
print(f"Restos Purificados por Borrado Ciego: {array_carnicero}")

print("\n--- LA DEMENCIA DEL GARBAGE COLLECTOR CPYTHON (REFERENCE CYCLES) ---")

# En Cpython, la liberación de memoria (RAM Free) se logra cuando 'Reference Count == 0'.
# Es decir, NINGUNA VARiABLE de tu scope General apunta a un Byte específico. Entonces se destruye.
# ¡Bugs en Modelos IA!: Memory Leaks al cargar Batches inmensos de Datasets en Loops interminables.

gc.collect() # Limpiamos basura del sistema anterior.

var_nodo_A = ["NodoA", "Data: Inf"]
var_nodo_B = ["NodoB", "Data: Base"]

# ATAMOS CIRCULARMENTE LOS OBJETOS A SI MISMOS. (Reference Cycle)
var_nodo_A.append(var_nodo_B) # A -> B
var_nodo_B.append(var_nodo_A) # B -> A

# Ahora están entrelazados en la memoria profunda C.
# Procedemos a "Eliminarlos" Localmente del Sistema Padre.
del var_nodo_A
del var_nodo_B

# PREGUNTA CRUZADA. ¿Se eliminó la Memoria RAM de los Textos Bases "Data Inf"?
# ¡NO! El Recuento de Referencia para A es de 1 (El B interno aún le apunta a él adentro)!
# El Recuento para B es de 1 (El A interno aún le apùnta). 
# MEMORY LEAK MORTAL CREADO SATISFACTORIAMENTE PARA DESTRUIR TUS GPU Y RAMS.

bytes_basuras_rescatados = gc.collect()  # El Módulo de Garbage Collection oficial Cyclic Isolation Algorithm interviene.
print(f"El Recolector Python Garbage Localizó Nodos Circulares Aislados Basuras e intervino:")
print(f" ¡{bytes_depositos_rescatados := bytes_basuras_rescatados} bytes muertos rescatados forzosamente del Ciclo Circular de Arrays Python!")


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: USERLIST VS SUBCLASSING (EL GRAN PRECEPT CORE) ===")
print("=" * 80)

"""
Muchas veces en Infraestructura o MLOps necesitas heredar una lista para dotarla
de funciones especiales y crear DataLoaders robustos que notifiquen, sumen operaciones
o emitan Trazas Observables hacia el servidor.

¿Heredas la propia función integrada  `class MiLista(list)` ?
En Python 3, heredar de la clase genérica interna C (los built-ins en C directos `list`, `dict`) 
tiene graves problemas: Algunos de sus métodos internos matemáticos (ej: Listas y operaciones inplace c) 
No usan tus propias funciones sobreescritas en clases hijas que mutan __getitem__ ó append y saltan
a C Base inalterable!.

SOLUCIÓN CORE: `collections.UserList`.
UserList se implementó 100% en Python de Alto Nivel para actuar de molde inmaculado (Wrapper) para clases derivadas que sí respetarán
magicamente los Override Functions (Polymorfismo de Opcion) que un Arquitecto haga.
"""

print("\n--- Subclasificando con Colecciones Integradas Abstractas ---")

class DataLoaderListaPersonalizada(UserList):
    """
    Subclase Experta que emitira Logs Internos cuando mutemos Datasets 
    sin chocar con el Intérprete CPython subyacente.
    `UserList` almacena el Array Real en el atributo interno: `self.data` -> Un list puro de python.
    """
    def append(self, item):
        print(f"[Logging Remoto] -> Agregando '{item:5s}' al Lote de Memoria.")
        # Super invocará la función real. (De hecho podemos tocar self.data directamente).
        super().append(item) 
        
    def purgar_nulos_data(self):
        # Accedemos a ".data", el atributo puro Wrapper. Modificaciones sin colisiones abstractas.
        self.data = [d for d in self.data if d is not None]
        print(f"[Core Remoto] Pipeline Purgó la Data!")

mi_wrapper_ia = DataLoaderListaPersonalizada()
mi_wrapper_ia.extend(["TensorA", "TensorB"]) # Acciones Base Herredadeas Normal (Extend). No imprime log de mi append.
mi_wrapper_ia.append("TensorC")              # Usa el mio Polimórfico! Saluda al servidor.
mi_wrapper_ia.append(None)
mi_wrapper_ia.purgar_nulos_data()            # Accede y destripa el `.data` coreano.

print(f"Clase Final Intelectualizada IA: {mi_wrapper_ia.data}")



print("\n" + "=" * 80)
print("=== CAPÍTULO 11: SORTING INTERNALS — TIMSORT BAJO EL CAPÓ ===")
print("=" * 80)

"""
Python usa TIMSORT (inventado por Tim Peters para CPython en 2002).
Es un algoritmo HÍBRIDO que combina:
- Merge Sort (para secuencias grandes).
- Insertion Sort (para secuencias pequeñas, ≤64 elementos).

Complejidad:
- Mejor caso: O(N) — cuando los datos ya están casi ordenados.
- Caso promedio: O(N log N).
- Peor caso: O(N log N).
- Espacio: O(N) (necesita memoria auxiliar para el merge).

Timsort es ESTABLE: dos elementos con la misma clave mantienen su orden
relativo original. Esto es CRUCIAL en ML cuando ordenas predicciones
que tienen el mismo score — necesitas que el desempate sea determinístico.

HAY DOS FORMAS DE ORDENAR EN PYTHON:
1. list.sort()  -> Ordena IN-PLACE. Modifica la lista original. Retorna None.
2. sorted(iter) -> Crea una NUEVA lista ordenada. No modifica el original.
"""

print("\n--- list.sort() vs sorted(): in-place vs copia ---")

scores_modelo = [0.92, 0.87, 0.95, 0.88, 0.91, 0.93]
print(f"Original: {scores_modelo}")

# sorted() crea copia nueva
scores_ordenados = sorted(scores_modelo)
print(f"sorted() (nueva lista): {scores_ordenados}")
print(f"Original sin tocar: {scores_modelo}")

# list.sort() muta in-place
retorno = scores_modelo.sort()
print(f"Tras .sort() in-place: {scores_modelo}")
print(f"Retorno de .sort(): {retorno}")
# -> None. TRAMPA CLÁSICA: no hagas x = lista.sort() porque x será None.


print("\n--- Ordenación con key= (Criterio personalizado) ---")

# Ordenar predicciones por score descendente
predicciones = [
    {"clase": "gato", "score": 0.92},
    {"clase": "perro", "score": 0.87},
    {"clase": "pájaro", "score": 0.95},
    {"clase": "pez", "score": 0.88},
]

# key= recibe una función que extrae el valor de comparación
por_score_desc = sorted(predicciones, key=lambda p: p["score"], reverse=True)
print(f"\nPredicciones ordenadas por score (desc):")
for p in por_score_desc:
    print(f"  {p['clase']:<10} -> {p['score']}")

# Ordenación ESTABLE: si dos tienen el mismo score, mantienen su orden original
datos_empate = [("A", 3), ("B", 1), ("C", 3), ("D", 1)]
ordenados_estable = sorted(datos_empate, key=lambda x: x[1])
print(f"\nOrdenación estable (empates preservan orden): {ordenados_estable}")
# B y D tienen score 1, pero B estaba antes -> B sigue antes.


print("\n--- Benchmark: sort() sobre datos ya ordenados (Timsort O(N)) ---")

# Timsort detecta runs (secuencias ya ordenadas) y las fusiona.
# Por eso, ordenar datos YA ORDENADOS es O(N), no O(N log N).
n_bench = 500_000

datos_aleatorios = [random.random() for _ in range(n_bench)]
datos_ya_ordenados = sorted(datos_aleatorios)

# Medir sort de datos aleatorios
copia_aleatorios = datos_aleatorios.copy()
inicio = time.perf_counter()
copia_aleatorios.sort()
t_aleatorio = time.perf_counter() - inicio

# Medir sort de datos YA ordenados
inicio = time.perf_counter()
datos_ya_ordenados.sort()
t_ya_ordenado = time.perf_counter() - inicio

print(f"\n  Sort de {n_bench} aleatorios:     {t_aleatorio*1000:.2f} ms")
print(f"  Sort de {n_bench} ya ordenados:   {t_ya_ordenado*1000:.2f} ms")
print(f"  Ratio: datos ordenados fue ~{t_aleatorio/t_ya_ordenado:.0f}x más rápido (Timsort runs)")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: TRACEMALLOC — PERFILADO REAL DE RAM EN PIPELINES ML ===")
print("=" * 80)

"""
sys.getsizeof() solo mide el contenedor, no su contenido.
Para medir el impacto REAL en RAM de un pipeline ML, usamos tracemalloc
(módulo de la Standard Library de CPython).

tracemalloc captura snapshots del heap de memoria y te dice:
- Cuántos bytes TOTALES consume tu código (incluyendo objetos hijos).
- En qué LÍNEA de código se asignó cada bloque de memoria.
- La diferencia entre dos snapshots (para detectar leaks).
"""

print("\n--- Midiendo el coste REAL de crear un dataset grande ---")

tracemalloc.start()
snapshot_antes = tracemalloc.take_snapshot()

# Simulamos la carga de un dataset: 100K registros con features
dataset_simulado = [
    {"id": i, "features": [random.random() for _ in range(10)], "label": random.randint(0, 1)}
    for i in range(100_000)
]

snapshot_despues = tracemalloc.take_snapshot()
tracemalloc.stop()

# Calcular diferencia
estadisticas = snapshot_despues.compare_to(snapshot_antes, 'lineno')

print(f"  Top 3 consumidores de memoria:")
for stat in estadisticas[:3]:
    print(f"    {stat}")

print(f"\n  Elementos en dataset: {len(dataset_simulado)}")
print(f"  Tamaño contenedor lista: {sys.getsizeof(dataset_simulado) / 1024:.1f} KB")
print(f"  (El contenido real consume MUCHO más — los dicts y listas internas)")


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: DATALOADER MANUAL — BATCHING DESDE CERO ===")
print("=" * 80)

"""
En PyTorch, el DataLoader toma un dataset y lo divide en batches.
Aquí implementamos esa lógica DESDE CERO usando solo listas y slicing.
Esto es exactamente lo que ocurre por debajo del DataLoader antes de 
pasarlo a los tensores C++ de PyTorch.
"""

print("\n--- Implementación de batching con listas ---")

def crear_batches(dataset: list, batch_size: int, shuffle: bool = False) -> list:
    """
    Divide un dataset en batches de tamaño fijo.
    Si shuffle=True, mezcla antes de dividir (como en entrenamiento).
    El último batch puede tener menos elementos (drop_last=False).
    """
    if shuffle:
        # Copiamos para no mutar el original y luego mezclamos
        dataset = dataset.copy()
        random.shuffle(dataset)
    
    batches = []
    for i in range(0, len(dataset), batch_size):
        batch = dataset[i : i + batch_size]  # Slicing puro O(batch_size)
        batches.append(batch)
    
    return batches

# Dataset de ejemplo
dataset_ids = list(range(23))  # 23 muestras
batch_size = 8

batches = crear_batches(dataset_ids, batch_size, shuffle=False)
print(f"Dataset: {len(dataset_ids)} muestras, batch_size={batch_size}")
print(f"Total batches generados: {len(batches)}")
for i, batch in enumerate(batches):
    print(f"  Batch {i}: {batch} (size={len(batch)})")


print("\n--- Train / Validation / Test Split manual ---")

def train_val_test_split(dataset: list, train_pct: float = 0.7, 
                         val_pct: float = 0.15, seed: int = 42) -> tuple:
    """
    Divide un dataset en train/val/test usando solo listas y slicing.
    """
    datos = dataset.copy()
    random.seed(seed)
    random.shuffle(datos)
    
    n = len(datos)
    n_train = int(n * train_pct)
    n_val = int(n * val_pct)
    
    train = datos[:n_train]
    val = datos[n_train : n_train + n_val]
    test = datos[n_train + n_val:]
    
    return train, val, test

dataset_completo = list(range(100))
train, val, test = train_val_test_split(dataset_completo)

print(f"\nSplit de {len(dataset_completo)} muestras:")
print(f"  Train: {len(train)} ({len(train)/len(dataset_completo):.0%})")
print(f"  Val:   {len(val)} ({len(val)/len(dataset_completo):.0%})")
print(f"  Test:  {len(test)} ({len(test)/len(dataset_completo):.0%})")

# Verificar no solapamiento (DATA LEAKAGE check)
solapamiento = set(train) & set(val) | set(train) & set(test) | set(val) & set(test)
print(f"  Solapamiento: {len(solapamiento)} (debe ser 0)")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: ENUMERATE, ZIP Y PATRONES DE ITERACIÓN AVANZADOS ===")
print("=" * 80)

"""
Un ingeniero de IA itera sobre listas CONSTANTEMENTE.
Hacerlo mal (con índices manuales) genera código frágil y lento.
Hacerlo bien (con enumerate, zip, reversed) genera código Pythonic y eficiente.
"""

print("\n--- enumerate(): índice + valor sin variables manuales ---")

capas_modelo = ["embedding", "attention", "feedforward", "layernorm", "output"]

# ANTIPATRÓN:
# for i in range(len(capas_modelo)):
#     print(f"Capa {i}: {capas_modelo[i]}")

# PATRÓN CORRECTO:
print("Capas del modelo:")
for idx, nombre_capa in enumerate(capas_modelo):
    print(f"  Layer {idx}: {nombre_capa}")

# Con start= para numerar desde 1
print("\nNumeración humana (start=1):")
for num, capa in enumerate(capas_modelo, start=1):
    print(f"  {num}. {capa}")


print("\n--- zip(): iteración paralela de múltiples listas ---")

nombres_modelos = ["BERT", "GPT-4", "LLaMA", "Gemini"]
parametros = ["340M", "1.7T", "70B", "Ultra"]
licencias = ["Apache", "Propietaria", "Meta", "Propietaria"]

print("\nComparación de modelos:")
for nombre, params, licencia in zip(nombres_modelos, parametros, licencias):
    print(f"  {nombre:<10} {params:<8} {licencia}")

# zip() se detiene en el iterable MÁS CORTO.
# Para incluir todos, usa itertools.zip_longest (módulo 04).

# zip + enumerate juntos:
print("\nCon índice:")
for i, (nombre, params) in enumerate(zip(nombres_modelos, parametros)):
    print(f"  #{i}: {nombre} ({params})")


print("\n--- reversed(): iteración inversa sin copiar ---")

# reversed() devuelve un ITERADOR, no crea una lista nueva.
# Nunca hagas lista[::-1] si solo necesitas iterar en reversa sin materializarlo.
epochs_losses = [2.5, 2.1, 1.8, 1.5, 1.2]
print("\nLosses en orden inverso (sin crear lista):")
for loss in reversed(epochs_losses):
    print(f"  {loss}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: TABLA DE COMPLEJIDAD COMPLETA DE LIST ===")
print("=" * 80)

"""
╔════════════════════════════════╦═══════════════════╗
║ OPERACIÓN                      ║ COMPLEJIDAD       ║
╠════════════════════════════════╬═══════════════════╣
║ list[i]                        ║ O(1)              ║
║ list[i] = x                   ║ O(1)              ║
║ len(list)                      ║ O(1)              ║
║ list.append(x)                 ║ O(1) amortizado   ║
║ list.pop()                     ║ O(1)              ║
║ list.pop(i)                    ║ O(N)              ║
║ list.insert(i, x)             ║ O(N)              ║
║ list.remove(x)                 ║ O(N)              ║
║ x in list                      ║ O(N)              ║
║ list.index(x)                  ║ O(N)              ║
║ list.count(x)                  ║ O(N)              ║
║ list.sort()                    ║ O(N log N)        ║
║ list.reverse()                 ║ O(N)              ║
║ list + list2                   ║ O(N + M)          ║
║ list.extend(iter)              ║ O(K)              ║
║ list[a:b]                      ║ O(b - a)          ║
║ del list[i]                    ║ O(N)              ║
║ list.copy()                    ║ O(N)              ║
╚════════════════════════════════╩═══════════════════╝

REGLAS DE ORO PARA IA:
1. Usa APPEND para construir, nunca INSERT(0).
2. Si necesitas "x in list" frecuente, convierte a SET.
3. Si necesitas pop(0), usa collections.deque.
4. sorted() crea copia, .sort() muta in-place (y retorna None).
"""


print("\n" + "=" * 80)
print("=== CAPÍTULO 16: MAP, FILTER Y REDUCE — PROGRAMACIÓN FUNCIONAL CON LISTAS ===")
print("=" * 80)

"""
Python soporta tres funciones de programación funcional que operan sobre listas:
- map(func, iterable): aplica func a cada elemento. Retorna iterador.
- filter(func, iterable): filtra elementos donde func retorna True.
- reduce(func, iterable): acumula resultado aplicando func secuencialmente.

En IA estas funciones permiten transformar datos sin loops explícitos.
Sin embargo, las List Comprehensions suelen ser más legibles y rápidas.
"""

print("\n--- map(): transformación sin loop ---")

scores_raw = [0.92, 0.87, 0.95, 0.88, 0.91]

# map + lambda para convertir a porcentaje string
scores_formateados = list(map(lambda s: f"{s:.0%}", scores_raw))
print(f"Scores formateados con map: {scores_formateados}")

# map con función nativa (más rápido que lambda)
strings_numeros = ["10", "20", "30", "40"]
numeros = list(map(int, strings_numeros))
print(f"Strings a ints con map(int, ...): {numeros}")


print("\n--- filter(): selección condicional ---")

losses = [2.5, 0.8, 1.2, 0.05, 3.1, 0.001]
buenas_losses = list(filter(lambda l: l < 1.0, losses))
print(f"Losses < 1.0 (filter): {buenas_losses}")


print("\n--- reduce(): acumulación (importar de functools) ---")

from functools import reduce

numeros = [1, 2, 3, 4, 5]
producto = reduce(lambda a, b: a * b, numeros)
print(f"Producto de {numeros} con reduce: {producto}")  # 120

# Flatten con reduce + concatenación
listas_anidadas = [[1, 2], [3, 4], [5, 6]]
aplanado = reduce(lambda a, b: a + b, listas_anidadas)
print(f"Flatten con reduce: {aplanado}")


print("\n--- Comprehension vs map/filter (benchmark y legibilidad) ---")

datos = list(range(100_000))

# Map + filter
inicio = time.perf_counter()
r1 = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, datos)))
t_map = time.perf_counter() - inicio

# List comprehension equivalente
inicio = time.perf_counter()
r2 = [x * 2 for x in datos if x % 2 == 0]
t_comp = time.perf_counter() - inicio

print(f"\n  map+filter: {t_map*1000:.2f} ms")
print(f"  Comprehension: {t_comp*1000:.2f} ms")
print(f"  Resultados iguales: {r1 == r2}")
print(f"  -> La comprehension suele ser MÁS RÁPIDA porque evita lambdas.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 17: STAR UNPACKING (*) EN LLAMADAS Y ASIGNACIONES ===")
print("=" * 80)

"""
El operador * (single star / splat) tiene dos usos fundamentales con listas:
1. En ASIGNACIONES: captura "el resto" de elementos.
2. En LLAMADAS: expande una lista como argumentos posicionales.
"""

print("\n--- * en asignaciones: captura del resto ---")

metrics = [0.95, 0.92, 0.88, 0.85, 0.80, 0.75]

mejor, *intermedios, peor = metrics
print(f"Mejor: {mejor}, Peor: {peor}")
print(f"Intermedios: {intermedios}")

# Extraer cabecera y cola de un dataset
header, *filas = [
    ["nombre", "score", "label"],
    ["img_01", 0.95, 1],
    ["img_02", 0.72, 0],
    ["img_03", 0.88, 1],
]
print(f"\nHeader: {header}")
print(f"Filas: {filas}")


print("\n--- * en llamadas: expansión de argumentos ---")

def crear_rango(inicio: int, fin: int, paso: int = 1) -> list:
    return list(range(inicio, fin, paso))

params = [0, 20, 3]
resultado = crear_rango(*params)  # Equivale a crear_rango(0, 20, 3)
print(f"crear_rango(*{params}) = {resultado}")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN DE INGENIERÍA PARA CIERRE DE ARQUITECTURA DE ESTRUCTURAS === ")
print("=" * 80)

"""
Hemos recorrido e implementado a nivel C todos los entresijos de una PyListObject.
1. Conocimos el `ob_item` Array of Pointers de 8-Bytes base y el Cache Miss del Hardware.
2. Comprobamos la Fórmula de PreAllocated Limits en saltos estáticos limitando SysCalls extra.
3. Repartimos y Desempaquetamos Arrays vía iteraciones destructivas `*args`.
4. Construimos Tensores Simulados con List Comprehensions evadiendo bucles O(N*N) Lentos.
5. Creamos Operaciones Matrices Transpuestas zip(*Matriz) y Productos Escalares Invocados.
6. Demostramos el Slicing Hacker con submuestreo Stepped Indexs, Muting in-place O(N).
7. Entablamos Garbage Collection Reference Cycles evadiendo catástrofes de Memory Leak.
8. Cerramos Subclasificando Mocks con UserList envolviendo clases DataLoadings.
9. Timsort: O(N) en datos casi ordenados, O(N log N) general. ESTABLE.
10. tracemalloc para medir impacto REAL en RAM de pipelines.
11. DataLoader manual con batching y train/val/test split desde cero.
12. enumerate + zip + reversed: la tríada de iteración Pythonic.
13. map/filter/reduce: paradigma funcional vs comprehension (velocidad y legibilidad).
14. Star unpacking: captura del resto y expansión de argumentos.
"""
print(" FIN DE ARQUIVO 01_listas_y_arrays. Python MLOps Framework Cerrado.")


