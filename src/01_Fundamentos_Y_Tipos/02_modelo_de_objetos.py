# ===========================================================================
# 02_modelo_de_objetos.py
# ===========================================================================
# MÓDULO 01: FUNDAMENTOS SÓLIDOS
# ARCHIVO 02: El Modelo de Objetos de Python — Cómo funciona la memoria
# ===========================================================================
#
# OBJETIVO DE ESTE ARCHIVO:
# Entender CÓMO Python gestiona variables, memoria y objetos internamente.
# Este es el conocimiento que separa a alguien que "usa Python" de alguien
# que "domina Python". Todo lo que hagas en IA (tensores, modelos, datos)
# se rige por estas reglas.
#
# NIVEL: Desde cero, pero yendo MUY profundo.
# ===========================================================================


# ===========================================================================
# CAPÍTULO 1: TODO EN PYTHON ES UN OBJETO
# ===========================================================================

"""
Esta frase la oirás mil veces: "En Python, todo es un objeto".
Pero nadie explica qué significa realmente. Vamos a hacerlo.

¿QUÉ ES UN OBJETO EN PYTHON?
==============================
Un objeto es una ESTRUCTURA DE DATOS en la memoria del ordenador que tiene:

  1. IDENTIDAD (id): dirección de memoria donde vive
  2. TIPO (type): qué tipo de dato es (int, str, list, etc.)
  3. VALOR: el contenido del objeto
  4. CONTADOR DE REFERENCIAS: cuántas variables apuntan a él

Cuando digo "todo es un objeto", quiero decir LITERALMENTE TODO:

  - Los números son objetos:         42 es un objeto de tipo int
  - Los strings son objetos:         "hola" es un objeto de tipo str
  - Las listas son objetos:          [1, 2, 3] es un objeto de tipo list
  - Las funciones son objetos:       def f(): ... crea un objeto de tipo function
  - Las clases son objetos:          class Foo: ... crea un objeto de tipo type
  - Los módulos son objetos:         import os crea un objeto de tipo module
  - type es un objeto:               type misma es un objeto
  - None es un objeto:               None es un singleton de tipo NoneType
  - True y False son objetos:        Son instancias de bool (que hereda de int)

Esto es diferente a lenguajes como Java o C++, donde los tipos primitivos
(int, float, bool) NO son objetos — son valores "de primera clase" que
viven directamente en la pila (stack), no en el heap.

En Python, HASTA un simple número 42 es un objeto en el heap con:
  - Su id (dirección de memoria)
  - Su tipo (int)
  - Su valor (42)
  - Su refcount (cuántas variables apuntan a él)
"""

# Demostración: todo tiene identidad y tipo
print("=== TODO ES UN OBJETO ===")

x = 42
print(f"x = {x}")
print(f"  id(x)   = {id(x)}")          # Dirección en memoria
print(f"  type(x) = {type(x)}")        # <class 'int'>
print(f"  x es un objeto: {isinstance(x, object)}")  # True

s = "hola"
print(f"\ns = '{s}'")
print(f"  id(s)   = {id(s)}")
print(f"  type(s) = {type(s)}")
print(f"  s es un objeto: {isinstance(s, object)}")

import sys
print(f"\nsys es un objeto:")
print(f"  id(sys)   = {id(sys)}")
print(f"  type(sys) = {type(sys)}")     # <class 'module'>

def mi_funcion():
    pass

print(f"\nmi_funcion es un objeto:")
print(f"  id(mi_funcion)   = {id(mi_funcion)}")
print(f"  type(mi_funcion) = {type(mi_funcion)}")  # <class 'function'>

print(f"\nNone es un objeto: {isinstance(None, object)}")
print(f"  type(None) = {type(None)}")   # <class 'NoneType'>

print(f"\nTrue es un objeto: {isinstance(True, object)}")
print(f"  type(True) = {type(True)}")   # <class 'bool'>
print(f"  True es un int: {isinstance(True, int)}")  # True!
print(f"  True + True = {True + True}")  # 2! Porque bool hereda de int

print(f"\ntype es un objeto:")
print(f"  type(type) = {type(type)}")   # <class 'type'> — ¡se apunta a sí mismo!


# ===========================================================================
# CAPÍTULO 2: VARIABLES NO SON CAJAS — SON ETIQUETAS
# ===========================================================================

"""
EL ERROR MENTAL MÁS COMÚN
===========================
La mayoría de la gente piensa que una variable es una "caja" que
contiene un valor:

    x = 42
    ┌─────┐
    │ x   │ ← caja llamada "x" que contiene 42
    │ 42  │
    └─────┘

ESTO ES INCORRECTO EN PYTHON.

LA REALIDAD: VARIABLES SON ETIQUETAS (REFERENCIAS)
====================================================
En Python, los OBJETOS existen en memoria independientemente.
Las variables son NOMBRES (etiquetas) que APUNTAN a esos objetos.

    x = 42

    Lo que realmente pasa:

    1. Python crea un objeto int con valor 42 en memoria (heap)
    2. Python crea un nombre "x" en el espacio de nombres actual
    3. "x" APUNTA al objeto 42

    x ──────────► ┌───────────────────┐
                  │ Objeto int        │
                  │ id: 140234567890  │
                  │ type: int         │
                  │ value: 42         │
                  │ refcount: 1       │
                  └───────────────────┘

    y = x   # NO copia el valor. Crea otra etiqueta al MISMO objeto.

    x ──────────► ┌───────────────────┐
                  │ Objeto int        │
    y ──────────► │ id: 140234567890  │
                  │ type: int         │
                  │ value: 42         │
                  │ refcount: 2       │ ← ahora 2 referencias
                  └───────────────────┘

¿POR QUÉ IMPORTA ESTO?
========================
Porque si el objeto es MUTABLE (como una lista), modificarlo desde
cualquier referencia afecta a TODAS las referencias:
"""

print("\n=== VARIABLES SON REFERENCIAS ===")

# Con tipos inmutables (int), no se nota tanto el efecto:
a = 42
b = a
print(f"a = {a}, b = {b}")
print(f"id(a) = {id(a)}, id(b) = {id(b)}")
print(f"a is b: {a is b}")   # True — apuntan al MISMO objeto

b = 100  # b ahora apunta a un NUEVO objeto (100)
print(f"\nDespués de b = 100:")
print(f"a = {a}, b = {b}")   # a sigue siendo 42
print(f"id(a) = {id(a)}, id(b) = {id(b)}")
print(f"a is b: {a is b}")   # False — ya apuntan a objetos distintos

# Con tipos MUTABLES (list), la cosa cambia:
print("\n--- PELIGRO CON MUTABLES ---")
lista_a = [1, 2, 3]
lista_b = lista_a  # lista_b apunta al MISMO objeto
print(f"lista_a = {lista_a}")
print(f"lista_b = {lista_b}")
print(f"id(lista_a) = {id(lista_a)}")
print(f"id(lista_b) = {id(lista_b)}")
print(f"lista_a is lista_b: {lista_a is lista_b}")  # True

# Modificamos a través de lista_b
lista_b.append(4)  # modificamos el OBJETO, no la referencia
print(f"\nDespués de lista_b.append(4):")
print(f"lista_a = {lista_a}")  # [1, 2, 3, 4] ← ¡lista_a TAMBIÉN cambió!
print(f"lista_b = {lista_b}")  # [1, 2, 3, 4]

"""
ESTO ES LA FUENTE DEL 50% DE LOS BUGS EN PYTHON.

Cuando haces lista_b = lista_a, NO copias la lista.
Creas OTRA REFERENCIA al MISMO objeto.
Cualquier modificación a través de cualquier referencia afecta al
mismo objeto.

Para copiar de verdad:
  lista_b = lista_a.copy()       # copia superficial
  lista_b = lista_a[:]           # copia superficial (slicing)
  lista_b = list(lista_a)        # copia superficial

  import copy
  lista_b = copy.deepcopy(lista_a)  # copia profunda (recursiva)

La diferencia entre copy y deepcopy la explicamos más adelante.
"""


# ===========================================================================
# CAPÍTULO 3: id(), type(), isinstance() — LAS 3 FUNCIONES CLAVE
# ===========================================================================

"""
Tres funciones que necesitas dominar para entender Python:

id(objeto)
==========
Devuelve la IDENTIDAD del objeto: un número único que lo identifica
mientras viva en memoria. En CPython, es la dirección de memoria.

type(objeto)
============
Devuelve el TIPO del objeto: la clase a la que pertenece.

isinstance(objeto, tipo)
========================
Comprueba si un objeto es de un tipo (o de una subclase de ese tipo).
MÁS SEGURO que type() porque respeta la herencia.
"""

print("\n=== id(), type(), isinstance() ===")

# id() — identidad
x = [1, 2, 3]
y = [1, 2, 3]
z = x

print(f"x = {x}, id(x) = {id(x)}")
print(f"y = {y}, id(y) = {id(y)}")
print(f"z = {z}, id(z) = {id(z)}")
print(f"x is z: {x is z}")     # True — mismo objeto
print(f"x is y: {x is y}")     # False — objetos distintos con mismo valor
print(f"x == y: {x == y}")     # True — mismo VALOR

"""
CLAVE: is vs ==

  x == y   → ¿tienen el mismo VALOR?       (compara contenido)
  x is y   → ¿son el MISMO OBJETO?         (compara id)

  Regla de oro:
  - Usa == para comparar valores (99% de los casos)
  - Usa is SOLO para comparar contra None:
      if resultado is None:     # ← CORRECTO
      if resultado == None:     # ← INCORRECTO (puede fallar con __eq__)

  ¿Por qué is None y no == None?
  Porque una clase puede sobreescribir __eq__ y hacer que x == None
  devuelva True cuando no debería. Pero x is None siempre es seguro
  porque compara identidad, no un método sobreescribible.
"""

# type() — tipo
print(f"\ntype(42) = {type(42)}")
print(f"type(3.14) = {type(3.14)}")
print(f"type('hola') = {type('hola')}")
print(f"type([1,2]) = {type([1,2])}")
print(f"type({{}}) = {type({})}")       # {} es dict, no set!
print(f"type(set()) = {type(set())}")   # set vacío se crea así
print(f"type(True) = {type(True)}")
print(f"type(None) = {type(None)}")

# isinstance() — comprobación con herencia
print(f"\nisinstance(True, bool) = {isinstance(True, bool)}")
print(f"isinstance(True, int)  = {isinstance(True, int)}")   # True! bool hereda de int
print(f"type(True) == int: {type(True) == int}")             # False! type() es exacto
print(f"type(True) == bool: {type(True) == bool}")           # True

"""
Por eso en código profesional se prefiere isinstance() sobre type():

  # ❌ MAL: no respeta herencia
  if type(x) == int:
      ...

  # ✅ BIEN: respeta herencia
  if isinstance(x, int):
      ...

  # ✅ TAMBIÉN: comprobar múltiples tipos
  if isinstance(x, (int, float)):
      ...
"""


# ===========================================================================
# CAPÍTULO 4: MUTABILIDAD vs INMUTABILIDAD
# ===========================================================================

"""
Este concepto es TAN importante que un capítulo entero no es suficiente.
Pero vamos a cubrirlo en profundidad.

DEFINICIÓN:
- INMUTABLE: no se puede modificar después de creado
- MUTABLE: se puede modificar después de creado

TIPOS INMUTABLES EN PYTHON:
  int         →  42 no se puede modificar. Si haces x + 1, se crea un NUEVO int.
  float       →  3.14 inmutable
  str         →  "hola" inmutable. No puedes cambiar una letra.
  tuple       →  (1, 2, 3) inmutable
  frozenset   →  frozenset({1, 2, 3}) inmutable
  bool        →  True/False inmutables
  None        →  None es inmutable (singleton)
  bytes       →  b"hola" inmutable

TIPOS MUTABLES EN PYTHON:
  list        →  [1, 2, 3] puedes añadir, quitar, cambiar elementos
  dict        →  {"a": 1} puedes añadir, quitar, cambiar pares
  set         →  {1, 2, 3} puedes añadir, quitar elementos
  bytearray   →  bytearray(b"hola") mutable
  objetos custom → las instancias de tus clases (por defecto)

¿POR QUÉ IMPORTA LA MUTABILIDAD?
==================================

1. SEGURIDAD: si pasas un objeto inmutable a una función, sabes que
   no lo va a modificar. Con mutables, no tienes esa garantía.

2. HASHABILIDAD: solo los objetos inmutables pueden ser claves de
   diccionario o elementos de set. Porque su hash no puede cambiar.
   (Un dict es un hash map, y si la clave cambia, el hash map se rompe)

3. THREADING: los objetos inmutables son thread-safe de forma natural.
   No necesitas locks ni sincronización.

4. RENDIMIENTO: Python puede optimizar objetos inmutables (caching,
   interning) porque sabe que nunca cambiarán.

5. EN IA: los tensores de PyTorch son mutables (modificas pesos
   durante el entrenamiento). Los datos de entrada deberían ser
   inmutables (no quieres modificar el dataset por accidente).
"""

print("\n=== MUTABILIDAD vs INMUTABILIDAD ===")

# ─── Inmutables: operaciones crean NUEVOS objetos ───
print("\n--- Inmutables ---")
x = 42
print(f"x = {x}, id = {id(x)}")
x = x + 1   # NO modifica 42. Crea un NUEVO objeto 43 y x apunta a él
print(f"x = {x}, id = {id(x)}")  # id DIFERENTE: es un objeto nuevo

s = "hola"
print(f"\ns = '{s}', id = {id(s)}")
s = s + " mundo"  # NO modifica "hola". Crea un NUEVO string "hola mundo"
print(f"s = '{s}', id = {id(s)}")  # id DIFERENTE

# Los strings son inmutables — no puedes cambiar un carácter
try:
    s[0] = "H"  # ERROR: 'str' object does not support item assignment
except TypeError as e:
    print(f"\nError al intentar s[0] = 'H': {e}")

# ─── Mutables: operaciones MODIFICAN el mismo objeto ───
print("\n--- Mutables ---")
lista = [1, 2, 3]
print(f"lista = {lista}, id = {id(lista)}")
lista.append(4)  # MODIFICA el mismo objeto en su lugar (in-place)
print(f"lista = {lista}, id = {id(lista)}")  # MISMO id!

d = {"nombre": "Juan"}
print(f"\nd = {d}, id = {id(d)}")
d["edad"] = 25  # MODIFICA el mismo dict
print(f"d = {d}, id = {id(d)}")  # MISMO id!


# ===========================================================================
# CAPÍTULO 5: INTERNING Y CACHING — OPTIMIZACIONES DE CPython
# ===========================================================================

"""
CPython hace optimizaciones internas con objetos inmutables que
debes conocer para no confundirte:

INTEGER CACHING (Small Integer Pool)
=====================================
CPython pre-crea y cachea los enteros del -5 al 256.
Cuando usas un número en ese rango, Python reutiliza el mismo objeto.
"""

print("\n=== INTERNING Y CACHING ===")

# Integers -5 a 256 están cacheados
a = 256
b = 256
print(f"a = 256, b = 256")
print(f"a is b: {a is b}")   # True! Mismo objeto (cacheado)

a = 257
b = 257
print(f"\na = 257, b = 257")
print(f"a is b: {a is b}")   # Puede ser False! (fuera del cache)
# NOTA: en el REPL puede dar True por optimización del compilador.
# En scripts, generalmente es False para números > 256.

"""
STRING INTERNING
================
Python también cachea ciertos strings:
- Strings que parecen identificadores (letras, números, underscores)
- Strings cortos
- Strings usados como nombres de variables/funciones

Esto es una OPTIMIZACIÓN INTERNA. NUNCA debes depender de esto.
Usa == para comparar strings, NUNCA is.
"""

s1 = "hola"
s2 = "hola"
print(f"\ns1 = 'hola', s2 = 'hola'")
print(f"s1 is s2: {s1 is s2}")   # True (Python cachea "hola")
print(f"s1 == s2: {s1 == s2}")   # True

s3 = "hola mundo"
s4 = "hola mundo"
print(f"\ns3 = 'hola mundo', s4 = 'hola mundo'")
print(f"s3 is s4: {s3 is s4}")   # Puede variar (tiene espacio)
print(f"s3 == s4: {s3 == s4}")   # True siempre

"""
REGLA: NUNCA uses 'is' para comparar valores.
Solo para: x is None, x is True, x is False (y estos últimos son raros).

En el contexto de IA:
Cuando trabajas con tensores en PyTorch, cada tensor es un objeto mutable
con su propio id. Dos tensores con los mismos valores NO son el mismo
objeto:
  t1 = torch.tensor([1, 2, 3])
  t2 = torch.tensor([1, 2, 3])
  t1 is t2  → False
  torch.equal(t1, t2) → True
"""


# ===========================================================================
# CAPÍTULO 6: REFERENCE COUNTING — CÓMO PYTHON GESTIONA MEMORIA
# ===========================================================================

"""
Python usa un sistema llamado REFERENCE COUNTING para saber cuándo
un objeto puede ser eliminado de la memoria.

CÓMO FUNCIONA:
  1. Cada objeto tiene un contador: refcount
  2. Cuando una variable apunta al objeto: refcount += 1
  3. Cuando una variable deja de apuntar: refcount -= 1
  4. Cuando refcount llega a 0: el objeto se destruye inmediatamente
"""

print("\n=== REFERENCE COUNTING ===")

# sys.getrefcount() muestra el refcount de un objeto
# NOTA: la propia llamada a getrefcount() crea una referencia temporal,
# así que el número será 1 más de lo esperado.

a = [1, 2, 3]
print(f"Refcount de a: {sys.getrefcount(a)}")  # 2 (a + argumento de getrefcount)

b = a  # nueva referencia al mismo objeto
print(f"Refcount después de b = a: {sys.getrefcount(a)}")  # 3

c = a  # otra referencia
print(f"Refcount después de c = a: {sys.getrefcount(a)}")  # 4

del b  # elimina la referencia b (no el objeto)
print(f"Refcount después de del b: {sys.getrefcount(a)}")  # 3

c = "otra cosa"  # c ahora apunta a otro objeto
print(f"Refcount después de c = 'otra cosa': {sys.getrefcount(a)}")  # 2

"""
¿QUÉ PASA CUANDO REFCOUNT LLEGA A 0?
======================================
El objeto se destruye INMEDIATAMENTE y su memoria se libera.

Puedes observar esto con __del__:
"""

class ObjetoRastreable:
    def __init__(self, nombre):
        self.nombre = nombre
        print(f"  {self.nombre}: CREADO (id={id(self)})")

    def __del__(self):
        print(f"  {self.nombre}: DESTRUIDO")

print("\n--- Lifecycle de objetos ---")
obj1 = ObjetoRastreable("obj1")
print(f"  obj1 existe, refcount: {sys.getrefcount(obj1)}")

obj1 = None  # obj1 deja de apuntar → refcount = 0 → se destruye
print("  obj1 fue asignado a None")

"""
EL PROBLEMA: CICLOS DE REFERENCIA
===================================
¿Qué pasa si A apunta a B y B apunta a A?

  a.ref = b
  b.ref = a

  Si eliminamos a y b, los objetos siguen apuntándose mutuamente.
  Refcount nunca llega a 0. ¡Memory leak!

  Para esto, Python tiene un segundo mecanismo: el Garbage Collector
  generacional (gc module), que detecta y rompe estos ciclos.
"""

print("\n--- Ciclos de referencia ---")
import gc

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.referencia = None

    def __repr__(self):
        ref_nombre = self.referencia.nombre if self.referencia else "None"
        return f"Nodo({self.nombre} → {ref_nombre})"

# Creamos un ciclo
nodo_a = Nodo("A")
nodo_b = Nodo("B")
nodo_a.referencia = nodo_b
nodo_b.referencia = nodo_a

print(f"  {nodo_a}")
print(f"  {nodo_b}")
print(f"  id(nodo_a) = {id(nodo_a)}")
print(f"  id(nodo_b) = {id(nodo_b)}")

# Aunque hagamos del, el ciclo impide la destrucción inmediata
del nodo_a
del nodo_b
# Los objetos siguen en memoria hasta que el GC los detecte

# Forzamos el GC para limpiar ciclos
recolectados = gc.collect()
print(f"  Objetos recolectados por GC: {recolectados}")

"""
EN IA:
Los modelos de deep learning (PyTorch) crean grafos computacionales
que pueden tener ciclos. PyTorch usa sus propios mecanismos de
gestión de memoria, pero entender cómo funciona la memoria en Python
te ayuda a depurar memory leaks en pipelines de entrenamiento.

Situaciones comunes de memory leak en IA:
  - Guardar el historial de losses sin convertir a .item()
    → el grafo computacional entero se mantiene en memoria
  - No usar torch.no_grad() durante inferencia
  - Acumular tensores en listas sin desconectarlos del grafo
"""


# ===========================================================================
# CAPÍTULO 7: COPIAS — SHALLOW vs DEEP
# ===========================================================================

"""
Dado que las variables son referencias, copiar objetos mutables
requiere cuidado especial.

3 NIVELES DE "COPIA":

1. ASIGNACIÓN (=): No copia nada. Crea otra referencia al mismo objeto.
2. SHALLOW COPY: Copia el contenedor, pero NO los elementos internos.
3. DEEP COPY: Copia TODO recursivamente.
"""

print("\n=== COPIAS: SHALLOW vs DEEP ===")

import copy

# ─── ASIGNACIÓN: NO copia ───
original = [[1, 2], [3, 4], [5, 6]]
asignacion = original

print("--- Asignación ---")
print(f"original = {original}")
print(f"asignacion is original: {asignacion is original}")  # True
asignacion[0][0] = 999
print(f"Tras asignacion[0][0] = 999:")
print(f"original = {original}")    # [[999, 2], [3, 4], [5, 6]] ← AFECTADO
original[0][0] = 1  # restaurar

# ─── SHALLOW COPY: copia el contenedor ───
print("\n--- Shallow Copy ---")
shallow = copy.copy(original)
# También: shallow = original.copy()
# También: shallow = original[:]
# También: shallow = list(original)

print(f"shallow is original: {shallow is original}")  # False! Otro contenedor
print(f"shallow[0] is original[0]: {shallow[0] is original[0]}")  # True! MISMAS sublistas

shallow[0][0] = 777
print(f"Tras shallow[0][0] = 777:")
print(f"original = {original}")    # [[777, 2], [3, 4], [5, 6]] ← ¡AFECTADO!
print(f"shallow = {shallow}")

"""
¿Por qué? Porque shallow copy copia el contenedor exterior (la lista
principal), pero los elementos INTERNOS (las sublistas) siguen siendo
las mismas referencias.

Visualmente:

  original ──► [ ● , ● , ● ]     shallow ──► [ ● , ● , ● ]
                 │    │    │                     │    │    │
                 ▼    ▼    ▼                     ▼    ▼    ▼
               [1,2] [3,4] [5,6]   ← MISMO objeto! Se comparten
"""

original[0][0] = 1  # restaurar

# ─── DEEP COPY: copia TODO ───
print("\n--- Deep Copy ---")
deep = copy.deepcopy(original)

print(f"deep is original: {deep is original}")  # False
print(f"deep[0] is original[0]: {deep[0] is original[0]}")  # False! ¡DISTINTO!

deep[0][0] = 555
print(f"Tras deep[0][0] = 555:")
print(f"original = {original}")    # [[1, 2], [3, 4], [5, 6]] ← NO afectado
print(f"deep = {deep}")           # [[555, 2], [3, 4], [5, 6]]

"""
CUÁNDO USAR CADA UNA:

  Asignación (=):
    - Cuando QUIERES que dos nombres apunten al mismo objeto
    - Cuando el objeto es inmutable (no importa compartir)

  Shallow copy:
    - Cuando quieres una copia del contenedor principal
    - Y los elementos internos son inmutables (int, str, tuple)
    - Ejemplo: lista de números, lista de strings

  Deep copy:
    - Cuando tienes estructuras anidadas con mutables
    - Ejemplo: lista de listas, dict de dicts
    - MÁS LENTO, usa más memoria

EN IA:
  - Los tensores de PyTorch se copian con tensor.clone()
  - .clone() es una "deep copy" del tensor (incluyendo datos y gradientes)
  - tensor.detach() crea un tensor que comparte datos pero sin gradientes
  - Esto es crítico durante entrenamiento vs inferencia
"""


# ===========================================================================
# CAPÍTULO 8: PASO POR REFERENCIA vs PASO POR VALOR
# ===========================================================================

"""
En Python, cuando pasas un argumento a una función, ¿qué se pasa?
¿El valor? ¿La referencia? ¿Una copia?

La respuesta correcta es: NINGUNA de las anteriores.
Python usa "PASS BY ASSIGNMENT" (paso por asignación).

Cuando llamas a f(x), Python hace lo equivalente a:
  parametro = x   ← asignación

Es decir, el parámetro de la función es una NUEVA REFERENCIA al
MISMO OBJETO. No es una copia. No es "la variable original".
Es otra etiqueta apuntando al mismo objeto.
"""

print("\n=== PASO POR ASIGNACIÓN ===")

# ─── Con inmutables: parece "paso por valor" ───
def duplicar(n):
    print(f"  Dentro, id(n) = {id(n)}")
    n = n * 2  # n ahora apunta a un NUEVO objeto
    print(f"  Después de n * 2, id(n) = {id(n)}")
    return n

x = 10
print(f"Antes: x = {x}, id = {id(x)}")
resultado = duplicar(x)
print(f"Después: x = {x}")  # x NO cambió (inmutable)
print(f"Resultado: {resultado}")

# ─── Con mutables: parece "paso por referencia" ───
def agregar_elemento(lista, elemento):
    print(f"  Dentro, id(lista) = {id(lista)}")
    lista.append(elemento)  # modifica el OBJETO original

mi_lista = [1, 2, 3]
print(f"\nAntes: mi_lista = {mi_lista}, id = {id(mi_lista)}")
agregar_elemento(mi_lista, 4)
print(f"Después: mi_lista = {mi_lista}")  # ¡MODIFICADA! [1, 2, 3, 4]

"""
PERO CUIDADO: si REASIGNAS el parámetro, pierdes la referencia:
"""

def intentar_reemplazar(lista):
    print(f"  Dentro antes, id = {id(lista)}")
    lista = [99, 99, 99]  # reasignación: lista apunta a un NUEVO objeto
    print(f"  Dentro después, id = {id(lista)}")
    # La variable local 'lista' ahora apunta a otro objeto
    # Pero la variable externa sigue apuntando al original

mi_lista2 = [1, 2, 3]
print(f"\nAntes: mi_lista2 = {mi_lista2}, id = {id(mi_lista2)}")
intentar_reemplazar(mi_lista2)
print(f"Después: mi_lista2 = {mi_lista2}")  # NO cambió! [1, 2, 3]

"""
RESUMEN:
  - Si MODIFICAS el objeto (append, pop, clear, []=): afecta al original
  - Si REASIGNAS (=): solo cambias la referencia LOCAL
  - Si quieres proteger el original: pasa una copia

  def funcion_segura(lista):
      lista = lista.copy()  # trabajamos con una copia
      lista.append(42)      # no afecta al original
      return lista

EN IA:
Muchas funciones de PyTorch modifican tensores IN-PLACE:
  - tensor.add_(5)       ← in-place (modifica el tensor original)
  - tensor.add(5)        ← out-of-place (crea un nuevo tensor)

La convención de PyTorch: las funciones con _ al final son in-place.
Esto viene directamente de cómo funciona el paso de objetos en Python.
"""


# ===========================================================================
# CAPÍTULO 9: NAMESPACES Y SCOPES — DONDE VIVEN LOS NOMBRES
# ===========================================================================

"""
Ya sabes que las variables son "nombres que apuntan a objetos".
Pero, ¿dónde se guardan esos nombres?

En NAMESPACES (espacios de nombres).

Un namespace es un DICCIONARIO que mapea nombres → objetos.

TIPOS DE NAMESPACES:
  1. Built-in:  nombres pre-definidos (print, len, int, etc.)
  2. Global:    nombres definidos a nivel del módulo
  3. Enclosing: nombres de funciones externas (closures)
  4. Local:     nombres dentro de la función actual

Python busca un nombre en este orden (regla LEGB):
  L → Local
  E → Enclosing
  G → Global
  B → Built-in
"""

print("\n=== NAMESPACES ===")

# Ver el namespace global
print(f"Namespace global (parcial): {list(globals().keys())[:10]}...")
# globals() devuelve el dict de nombres globales

def mi_func():
    variable_local = 42
    print(f"  Namespace local: {locals()}")  # dict de nombres locales

mi_func()

# La cadena LEGB en acción:
variable_global = "soy global"

def exterior():
    variable_enclosing = "soy enclosing"

    def interior():
        variable_local = "soy local"
        print(f"  local: {variable_local}")
        print(f"  enclosing: {variable_enclosing}")
        print(f"  global: {variable_global}")
        print(f"  built-in: {len}")  # < built-in function len >

    interior()

exterior()


# ===========================================================================
# CAPÍTULO 10: RESUMEN Y CONEXIÓN CON IA
# ===========================================================================

"""
RESUMEN DE LO APRENDIDO EN ESTE ARCHIVO:

1. TODO en Python es un objeto con id, type y value
2. Las variables son ETIQUETAS (referencias), no cajas
3. Asignación (=) crea una nueva referencia, NO una copia
4. Los tipos inmutables (int, str, tuple) son seguros de compartir
5. Los tipos mutables (list, dict, set) son peligrosos de compartir
6. is compara identidad (mismo objeto), == compara valor
7. Usa is SOLO con None: if x is None
8. Python usa reference counting + GC para gestionar memoria
9. Shallow copy copia el contenedor, deep copy copia todo
10. Las funciones reciben referencias, no copias
11. Los nombres viven en namespaces, y se buscan con la regla LEGB

CONEXIÓN DIRECTA CON IA:

1. TENSORES: Los tensores de PyTorch son objetos mutables. Entender
   referencias es CRÍTICO para no crear bugs con gradientes.

2. DATASETS: Un dataset es una estructura de datos (lista de dicts,
   DataFrame de Pandas). Entender mutabilidad te evita bugs.

3. PARÁMETROS DE MODELO: Los pesos de una red neuronal son tensores
   mutables que se modifican in-place durante el entrenamiento.
   El optimizer modifica directamente estos objetos.

4. MEMORY LEAKS: Si no entiendes reference counting, no puedes
   depurar por qué tu training loop consume cada vez más RAM.

5. BATCH PROCESSING: Cuando procesas datos en batches, entender
   copias vs referencias determina si puedes paralelizar o no.

ARCHIVO SIGUIENTE: 03_tipos_numericos.py
→ int, float, complex en profundidad
→ Precisión de punto flotante (IEEE 754)
→ Decimal para precisión exacta
→ Operadores aritméticos completo
→ Conexión con tensores y cálculo numérico
"""
