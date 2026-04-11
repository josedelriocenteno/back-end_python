# ===========================================================================
# 01_que_es_python.py
# ===========================================================================
# MÓDULO 01: FUNDAMENTOS SÓLIDOS
# ARCHIVO 01: ¿Qué es Python? — Todo lo que necesitas saber desde cero
# ===========================================================================
#
# OBJETIVO DE ESTE ARCHIVO:
# Que entiendas QUÉ es Python, CÓMO funciona por dentro, POR QUÉ es el
# lenguaje dominante en IA/ML, y cuál es la mentalidad correcta para
# aprenderlo si tu objetivo es ser Ingeniero de IA.
#
# NIVEL: Desde cero absoluto. No se asume que sepas nada.
# ESTILO: Explicación exhaustiva. Cada concepto con contexto completo.
# ===========================================================================


# ===========================================================================
# CAPÍTULO 1: ¿QUÉ ES UN LENGUAJE DE PROGRAMACIÓN?
# ===========================================================================

"""
Antes de hablar de Python, necesitas entender qué es un lenguaje de
programación y por qué existen.

UN ORDENADOR SOLO ENTIENDE NÚMEROS
===================================
Un procesador (CPU) es un chip que ejecuta instrucciones. Pero esas
instrucciones son secuencias de 0s y 1s llamadas "código máquina":

    10110000 01100001    → mueve el valor 97 al registro AL
    11001101 00010000    → interrupción del sistema

Esto es ilegible para humanos. Trabajar así es posible, pero es como
construir un rascacielos moviendo átomos uno a uno.

LA JERARQUÍA DE ABSTRACCIÓN
============================
Los lenguajes de programación son CAPAS DE ABSTRACCIÓN que nos permiten
comunicarnos con la máquina de forma humana:

    Nivel más bajo (cercano a la máquina):
    ──────────────────────────────────────
    1. Código máquina    → 10110000 01100001 (binario puro)
    2. Ensamblador (ASM) → MOV AL, 97        (nombres legibles para instrucciones)
    3. C / C++           → int x = 97;       (sintaxis parecida al inglés)
    4. Java / C#         → int x = 97;       (con máquina virtual, más portable)
    5. Python            → x = 97            (máxima simplicidad)
    ──────────────────────────────────────
    Nivel más alto (cercano al humano)

Cada nivel hacia arriba SACRIFICA algo de control/velocidad a cambio de
GANAR productividad y legibilidad.

Python está en el nivel más alto de esta jerarquía. Eso significa:
  - Es MUY fácil de leer y escribir
  - Es MÁS LENTO que C/C++ ejecutando (10x-100x más lento)
  - Pero permite DESARROLLAR mucho más rápido

¿Por qué ese trade-off importa para IA?
Porque en IA, el cuello de botella NO es la velocidad de Python.
Las operaciones pesadas (multiplicación de matrices, entrenamiento de redes)
las ejecutan librerías escritas en C/C++/CUDA (NumPy, PyTorch, TensorFlow).
Python solo es el "director de orquesta" que dice QUÉ hacer, no el que
hace el trabajo pesado.

Esto es FUNDAMENTAL entenderlo desde el día 1:
→ Python es LENTO ejecutando Python puro
→ Pero las librerías de IA en Python ejecutan código C/CUDA ultra-rápido
→ Tú escribes Python cómodo, y por debajo se ejecuta C a velocidad brutal
"""


# ===========================================================================
# CAPÍTULO 2: ¿QUÉ ES PYTHON EXACTAMENTE?
# ===========================================================================

"""
DEFINICIÓN TÉCNICA
==================
Python es un lenguaje de programación:

  1. DE ALTO NIVEL
     No necesitas gestionar memoria manualmente (como en C con malloc/free).
     Python lo hace por ti con un "recolector de basura" (garbage collector).

  2. INTERPRETADO (no compilado directamente)
     - En C: escribes código → compilas a ejecutable → ejecutas el binario
     - En Python: escribes código → el intérprete lo lee y ejecuta línea a línea

     Pero OJO, esto es una simplificación. En realidad, Python hace esto:
       a) Lee tu archivo .py
       b) Lo COMPILA a "bytecode" (una representación intermedia)
       c) Ejecuta ese bytecode en la "Python Virtual Machine" (PVM)

     Ese bytecode se guarda en archivos .pyc (dentro de __pycache__/).
     La próxima vez que ejecutes el mismo script, si no cambió, Python
     reutiliza el .pyc compilado → arranque más rápido.

  3. DINÁMICAMENTE TIPADO
     No declaras el tipo de una variable. Python lo infiere:

       x = 42        # Python sabe que x es int
       x = "hola"    # Ahora x es str. Sin error. Sin declaración.

     Esto es lo OPUESTO a lenguajes "estáticamente tipados" como Java:
       int x = 42;        // Java: debes declarar el tipo
       x = "hola";        // ERROR en Java: no puedes cambiar el tipo

     Ventaja del tipado dinámico: flexibilidad, rapidez de desarrollo
     Desventaja: errores que en Java se pillan al compilar, en Python
     solo se pillan AL EJECUTAR (en runtime).

     Por eso en Python profesional se usan TYPE HINTS (anotaciones de tipo):
       x: int = 42
       def sumar(a: int, b: int) -> int:
           return a + b

     Los type hints NO cambian el comportamiento. Python los ignora.
     Pero herramientas como mypy los leen y te avisan de errores.
     Esto lo veremos en profundidad más adelante.

  4. MULTIPARADIGMA
     Python soporta varios estilos de programación:

     - Programación IMPERATIVA (hacer cosas paso a paso):
         total = 0
         for numero in [1, 2, 3]:
             total += numero

     - Programación ORIENTADA A OBJETOS (organizar en clases):
         class Perro:
             def __init__(self, nombre):
                 self.nombre = nombre
             def ladrar(self):
                 return f"{self.nombre} dice: ¡Guau!"

     - Programación FUNCIONAL (funciones puras, sin estado):
         numeros = [1, 2, 3, 4, 5]
         pares = list(filter(lambda x: x % 2 == 0, numeros))

     Para IA, usarás los tres estilos constantemente:
     - Imperativo para scripts rápidos y experimentación
     - OOP para diseñar sistemas (APIs, pipelines)
     - Funcional para transformaciones de datos (map, filter, reduce)

  5. CON GESTIÓN AUTOMÁTICA DE MEMORIA
     En C, si pides memoria y olvidas liberarla → memory leak (tu programa
     consume más y más RAM hasta crashear).

     En Python, cuando un objeto ya no se usa, el garbage collector lo
     detecta y libera la memoria automáticamente.

     Python usa DOS mecanismos:
     a) Reference Counting: cada objeto tiene un contador de cuántas
        variables lo referencian. Cuando llega a 0 → se borra.
     b) Generational GC: detecta "ciclos" (A apunta a B, B apunta a A)
        que el reference counting no puede resolver.

     Esto lo profundizaremos en el archivo de modelo de objetos.


HISTORIA RELEVANTE
==================
- Creado por Guido van Rossum en 1991 (Países Bajos)
- Nombrado por Monty Python (el grupo de comedia), no la serpiente
- Python 2 vs Python 3: en 2008 salió Python 3, incompatible con Python 2.
  Python 2 murió oficialmente el 1 de enero de 2020.
  SIEMPRE usa Python 3. Si ves código con "print" sin paréntesis
  (print "hola"), es Python 2. Ignóralo.
- Versión actual estable: Python 3.12+ (abril 2026)
- El desarrollo lo gestiona la Python Software Foundation (PSF)
- El proceso de mejora se hace mediante PEPs (Python Enhancement Proposals)
  Las PEPs más famosas que debes conocer:
    PEP 8   → Guía de estilo de código
    PEP 20  → El Zen de Python (import this)
    PEP 484 → Type Hints
    PEP 572 → Walrus operator (:=)
    PEP 3107 → Function annotations
"""


# ===========================================================================
# CAPÍTULO 3: ¿POR QUÉ PYTHON DOMINA LA IA?
# ===========================================================================

"""
Esta es la pregunta más importante si tu objetivo es ser Ingeniero de IA.

RAZÓN 1: EL ECOSISTEMA DE LIBRERÍAS
====================================
Python tiene el ecosistema de librerías de IA/ML/Data más grande del mundo.
No es que Python sea "bueno para IA". Es que TODAS las herramientas de IA
están escritas para Python:

  Capa 1 — Computación numérica:
    NumPy       → Arrays multidimensionales, álgebra lineal
    SciPy       → Algoritmos científicos avanzados

  Capa 2 — Manipulación de datos:
    Pandas      → DataFrames (tablas de datos)
    Polars      → Alternativa moderna a Pandas (más rápido)

  Capa 3 — Machine Learning clásico:
    Scikit-learn → Algoritmos ML (regresión, clasificación, clustering)
    XGBoost      → Gradient boosting (ganador de Kaggle)
    LightGBM     → Alternativa a XGBoost de Microsoft

  Capa 4 — Deep Learning:
    PyTorch      → Framework #1 en investigación y cada vez más en producción
    TensorFlow   → Framework de Google, dominante en producción
    JAX          → Framework de Google para investigación avanzada

  Capa 5 — NLP y LLMs:
    Hugging Face Transformers → Modelos pre-entrenados (BERT, GPT, LLaMA)
    LangChain    → Framework para aplicaciones con LLMs
    LlamaIndex   → Framework para RAG

  Capa 6 — Visión por computador:
    OpenCV       → Procesamiento de imágenes
    Pillow/PIL   → Manipulación de imágenes
    torchvision  → Modelos de visión pre-entrenados

  Capa 7 — MLOps y producción:
    MLflow       → Tracking de experimentos
    FastAPI      → APIs de alto rendimiento para servir modelos
    Docker SDK   → Contenedores desde Python
    Ray          → Computación distribuida

  Capa 8 — Agentes e IA Generativa:
    OpenAI SDK   → API de GPT-4, DALL-E
    Anthropic SDK → API de Claude
    Google GenAI → API de Gemini
    CrewAI       → Multi-agentes
    AutoGen      → Agentes conversacionales

NO existe un ecosistema comparable en otro lenguaje.
Si intentas hacer lo mismo en Java, Go o Rust, te faltan el 80% de las
herramientas. Python ganó por efecto de red: todos publican para Python
→ más gente usa Python → más herramientas en Python → ciclo infinito.


RAZÓN 2: PYTHON ES EL "PEGAMENTO"
===================================
En IA, un proyecto típico combina muchas piezas:
  - Leer datos de una base de datos (SQL)
  - Limpiar y transformar datos (Pandas)
  - Entrenar un modelo (PyTorch)
  - Servir el modelo como API (FastAPI)
  - Monitorizar el rendimiento (MLflow)

Python es el PEGAMENTO que conecta todas estas piezas.
No necesitas aprender 5 lenguajes diferentes. Con Python haces todo.

Las partes que necesitan velocidad (multiplicación de matrices, inferencia
de redes neuronales) las ejecutan librerías en C/C++/CUDA.
Tú solo escribes Python.


RAZÓN 3: LA COMUNIDAD Y LA DOCUMENTACIÓN
==========================================
- Stack Overflow: Python es el lenguaje con más preguntas respondidas
- GitHub: más repositorios de IA/ML en Python que en todos los demás
  lenguajes combinados
- Papers con código: el 90%+ de los papers de ML publican código en Python
- Tutoriales: Andrej Karpathy, Fast.ai, DeepLearning.ai → todo en Python

Cuando un investigador de Google, OpenAI o Meta publica un paper nuevo,
el código de referencia es en Python. Si no sabes Python, no puedes
reproducir ni entender los avances.


RAZÓN 4: VELOCIDAD DE PROTOTIPADO
===================================
En IA, la velocidad de ITERACIÓN es más importante que la velocidad de
EJECUCIÓN. Un Ingeniero de IA necesita:
  - Probar 50 configuraciones de hiperparámetros
  - Experimentar con 10 arquitecturas de red diferentes
  - Iterar sobre el preprocessing de datos
  - Visualizar resultados rápidamente

Python permite hacer todo esto más rápido que cualquier otro lenguaje.
Lo que en C++ lleva 200 líneas, en Python son 20.

Cuando ya tienes el modelo que funciona y necesitas optimizar para
producción, puedes:
  a) Usar TorchScript/ONNX para compilar el modelo
  b) Servir con TensorRT (NVIDIA) para máxima velocidad
  c) Convertir las partes críticas a C/Cython
  d) Usar Rust para los servicios de backend

Pero la EXPERIMENTACIÓN y el DESARROLLO siempre son en Python.
"""


# ===========================================================================
# CAPÍTULO 4: CÓMO SE EJECUTA PYTHON POR DENTRO
# ===========================================================================

"""
Esto es algo que el 95% de los tutoriales no explican, pero que tú
necesitas entender para dominar Python a nivel extremo.

EL PROCESO COMPLETO DE EJECUCIÓN
==================================

Cuando ejecutas: python mi_script.py

Ocurre todo esto:

  PASO 1: LECTURA
  ─────────────────
  Python lee el archivo mi_script.py como texto plano (bytes UTF-8).

  PASO 2: LEXING (Análisis léxico)
  ─────────────────────────────────
  El "lexer" convierte el texto en "tokens" (unidades mínimas de significado):

    x = 42 + 3

    Se convierte en tokens:
    [NAME:'x'] [EQUAL:'='] [NUMBER:'42'] [PLUS:'+'] [NUMBER:'3'] [NEWLINE]

  PASO 3: PARSING (Análisis sintáctico)
  ──────────────────────────────────────
  El "parser" organiza los tokens en un AST (Abstract Syntax Tree):

    Assign
    ├── target: Name('x')
    └── value: BinOp
              ├── left: Constant(42)
              ├── op: Add
              └── right: Constant(3)

  El AST es la representación estructurada de tu código.
  Puedes verlo tú mismo con el módulo ast de Python:

    import ast
    tree = ast.parse("x = 42 + 3")
    print(ast.dump(tree, indent=2))

  PASO 4: COMPILACIÓN A BYTECODE
  ──────────────────────────────
  El compilador de CPython transforma el AST en "bytecode":
  instrucciones de bajo nivel para la Python Virtual Machine (PVM).

    x = 42 + 3

    Se compila a (simplificado):
      LOAD_CONST  42
      LOAD_CONST  3
      BINARY_ADD
      STORE_NAME  x

  Puedes ver el bytecode real con el módulo dis:

    import dis
    dis.dis("x = 42 + 3")

  Este bytecode se guarda en __pycache__/mi_script.cpython-312.pyc
  Es un formato binario que la PVM puede leer más rápido que el .py.

  PASO 5: EJECUCIÓN EN LA PVM
  ────────────────────────────
  La Python Virtual Machine (PVM) es un bucle en C que:
    1. Lee la siguiente instrucción de bytecode
    2. La ejecuta
    3. Vuelve al paso 1

  Es un bucle infinito (llamado "eval loop") dentro del archivo
  ceval.c del código fuente de CPython.

  Cada instrucción de bytecode manipula una "pila" (stack):
    LOAD_CONST 42    → pila: [42]
    LOAD_CONST 3     → pila: [42, 3]
    BINARY_ADD       → saca 42 y 3, suma, mete 45 → pila: [45]
    STORE_NAME x     → saca 45, lo asigna a 'x' → pila: []


¿POR QUÉ ESTO IMPORTA PARA IA?
================================
1. Entender que Python compila a bytecode te ayuda a entender:
   - Por qué import es "lento" la primera vez (compila)
   - Por qué la segunda vez es rápido (__pycache__)
   - Por qué Python no es "interpretado" en el sentido puro

2. Cuando hagas profiling de código lento, necesitas saber dónde está
   el cuello de botella: ¿en tu Python? ¿en la librería C?

3. El GIL (Global Interpreter Lock) opera a nivel de bytecode.
   Esto es CRÍTICO para entender concurrencia en Python.
   Lo veremos en detalle en el módulo 07.
"""


# ===========================================================================
# CAPÍTULO 5: CPython, PyPy, Cython — LAS IMPLEMENTACIONES
# ===========================================================================

"""
"Python" es una ESPECIFICACIÓN (un documento que dice cómo debe funcionar).
Pero hay varias IMPLEMENTACIONES (programas que ejecutan esa especificación):

CPython (la que usas tú)
========================
- Implementación de referencia, escrita en C
- Cuando instalas Python de python.org, instalas CPython
- Es la más usada (99%+ de usuarios)
- Todas las librerías de IA están testeadas contra CPython
- USA ESTA. No uses otra salvo que tengas una razón muy específica.

PyPy
====
- Implementación alternativa con JIT (Just-In-Time compilation)
- Puede ser 4x-10x más rápida que CPython para código Python puro
- PERO: muchas librerías de IA NO son compatibles (NumPy parcialmente,
  PyTorch NO funciona con PyPy)
- Conclusión: interesante de conocer, NO la uses para IA

Cython
======
- No es una implementación de Python. Es un LENGUAJE separado.
- Permite escribir código "casi Python" que se compila a C
- Se usa para escribir extensiones rápidas
- NumPy, Pandas, scikit-learn usan Cython internamente
- Tú probablemente no escribirás Cython, pero es bueno saber que existe

Jython (Python en Java)
========================
- Python corriendo sobre la JVM (Java Virtual Machine)
- Irrelevante para IA. Solo mencionado para completitud.

IronPython (Python en .NET)
============================
- Python corriendo sobre .NET
- Irrelevante para IA.

MicroPython
===========
- Python para microcontroladores (Arduino, Raspberry Pi Pico)
- Irrelevante para IA en la nube, pero interesante para IoT + IA edge.


CONCLUSIÓN:
→ Usa CPython. Siempre. Para IA no hay alternativa real.
→ Cuando diga "Python" en estos apuntes, me refiero a CPython.
"""


# ===========================================================================
# CAPÍTULO 6: VERSIONES DE PYTHON — CUÁL USAR
# ===========================================================================

"""
A abril de 2026, las versiones activas de Python son:

  Python 3.11 → Soporte de seguridad hasta oct 2027
  Python 3.12 → Soporte activo hasta oct 2028
  Python 3.13 → Soporte activo hasta oct 2029 (RECOMENDADA)
  Python 3.14 → Beta/RC (no usar en producción todavía)

¿CUÁL USAR?
→ Para aprender: Python 3.13 (la más estable moderna)
→ Para producción: la que tu empresa/proyecto requiera (normalmente 3.11+)

CAMBIOS IMPORTANTES POR VERSIÓN:

Python 3.8 (2019) — histórico:
  - Walrus operator (:=)    → asignar y evaluar en una expresión
  - f-strings con =         → f"{x=}" imprime "x=42"
  - Positional-only params  → def f(x, /, y): ...

Python 3.9 (2020):
  - Type hints nativos       → list[int] en vez de List[int]
  - Dict merge operator      → d1 | d2

Python 3.10 (2021):
  - Pattern matching          → match/case (como switch potenciado)
  - Better error messages     → Python ahora te dice EXACTAMENTE qué falta
  - Parenthesized context managers

Python 3.11 (2022):
  - 10-60% más rápido que 3.10 (Faster CPython project)
  - Exception groups          → ExceptionGroup, except*
  - Tomllib                   → Leer archivos TOML nativamente

Python 3.12 (2023):
  - F-strings anidados        → f"{'hola' if True else 'adiós'}"
  - Per-interpreter GIL       → Primer paso hacia eliminar el GIL
  - Type parameter syntax     → def f[T](x: T) -> T: ...

Python 3.13 (2024):
  - Free-threaded mode (experimental) → Python sin GIL (--disable-gil)
  - Improved REPL              → REPL interactivo mejorado
  - Mejor mensajes de error    → Aún más claros

PARA IA:
La mayoría de librerías (PyTorch, TensorFlow, etc.) soportan 3.10-3.12.
Usa 3.12 o 3.13 salvo que una librería específica no lo soporte.
Siempre verifica la compatibilidad antes de instalar.
"""


# ===========================================================================
# CAPÍTULO 7: INSTALACIÓN Y PRIMER PROGRAMA
# ===========================================================================

# Verificar qué Python tienes instalado:
# En terminal:
#   python --version
#   python3 --version
#
# Si no tienes Python 3.12+:
#   Linux (Ubuntu/Debian):
#     sudo apt update
#     sudo apt install python3.13 python3.13-venv python3.13-dev
#
#   macOS:
#     brew install python@3.13
#
#   Windows:
#     Descarga de https://www.python.org/downloads/
#     MARCA "Add Python to PATH" durante la instalación

# ───────────────────────────────────────────────────────────────
# Tu primer programa en Python:
# ───────────────────────────────────────────────────────────────

print("Hola, mundo")

# Eso es todo. Una línea. Sin punto y coma. Sin llaves. Sin main().
# En Java sería:
#   public class Main {
#       public static void main(String[] args) {
#           System.out.println("Hola, mundo");
#       }
#   }
#
# En C sería:
#   #include <stdio.h>
#   int main() {
#       printf("Hola, mundo\n");
#       return 0;
#   }
#
# Python elimina toda la ceremonia. Escribes lo que quieres hacer.
# Esta filosofía se llama "batteries included" y "there should be one
# obvious way to do it".


# ───────────────────────────────────────────────────────────────
# Ejecutar el programa:
# ───────────────────────────────────────────────────────────────
# En terminal:
#   python 01_que_es_python.py
#
# O si tienes Python 2 y 3 instalados:
#   python3 01_que_es_python.py
#
# También puedes usar el REPL (Read-Eval-Print-Loop):
#   python3
#   >>> print("Hola, mundo")
#   Hola, mundo
#   >>> exit()
#
# El REPL es perfecto para experimentar rápidamente.
# En Python 3.13+, el REPL tiene colores y autocompletado mejorado.


# ===========================================================================
# CAPÍTULO 8: EL ZEN DE PYTHON
# ===========================================================================

# Ejecuta esto en el REPL:
import this

# Esto imprime los principios filosóficos de Python.
# Los más importantes para un Ingeniero de IA:
#
# "Beautiful is better than ugly."
#   → Tu código debe ser legible. Si parece un jeroglífico, está mal.
#
# "Explicit is better than implicit."
#   → Mejor ser claro que inteligente. No uses trucos crípticos.
#
# "Simple is better than complex."
#   → La solución más simple que funcione es la mejor.
#
# "Readability counts."
#   → El código se lee 10 veces más de lo que se escribe.
#     Escribe para el futuro tú, no para el tú de hoy.
#
# "Errors should never pass silently."
#   → No ocultes errores con try/except vacíos. Nunca.
#
# "In the face of ambiguity, refuse the temptation to guess."
#   → Si algo no está claro, pregunta/investiga. No asumas.
#
# "There should be one-- and preferably only one --obvious way to do it."
#   → Python intenta que haya UNA forma clara de hacer cada cosa.
#     (Aunque no siempre lo consigue)


# ===========================================================================
# CAPÍTULO 9: PYTHON EN EL CONTEXTO DE IA — TU MAPA MENTAL
# ===========================================================================

"""
Como futuro Ingeniero de IA, necesitas un mapa mental de DÓNDE encaja
cada cosa. Aquí va:

NIVEL 1: LENGUAJE (estos apuntes, módulos 01-07)
─────────────────────────────────────────────────
Python como lenguaje: sintaxis, tipos, funciones, clases, módulos,
errores, memoria, generadores, metaclases, rendimiento.

Sin esto, todo lo demás se construye sobre arena.


NIVEL 2: HERRAMIENTAS MATEMÁTICAS (módulos 08-12)
──────────────────────────────────────────────────
NumPy, Pandas, álgebra lineal, cálculo, probabilidad.

Esto es el "vocabulario" de la IA. Los modelos de ML/DL son
esencialmente FUNCIONES MATEMÁTICAS. Si no dominas las matemáticas
implementadas en Python, no puedes entender qué hace un modelo
ni depurarlo cuando falla.


NIVEL 3: MACHINE LEARNING CLÁSICO (módulos 14-17)
──────────────────────────────────────────────────
Scikit-learn, features, evaluación, validación.

Antes de Deep Learning, necesitas entender ML clásico.
Muchos problemas reales se resuelven con un XGBoost, no con un
Transformer de 7 billones de parámetros.


NIVEL 4: DEEP LEARNING (módulos 18-21)
──────────────────────────────────────
PyTorch, CNNs, RNNs, Transformers, transfer learning.

Aquí empiezas a construir redes neuronales desde cero.
Implementar un Transformer tú mismo es la prueba de que
realmente entiendes cómo funciona la IA moderna.


NIVEL 5: NLP Y LLMs (módulos 22-27)
────────────────────────────────────
Tokenización, HuggingFace, APIs de LLMs, RAG, Agentes, Fine-tuning.

Esta es la capa "aplicada" de IA. Donde construyes productos reales:
chatbots, asistentes, sistemas de búsqueda semántica, agentes autónomos.


NIVEL 6: PRODUCCIÓN (módulos 28-32)
────────────────────────────────────
Backend, async, MLOps, Docker, Testing.

De nada sirve un modelo que funciona en un Jupyter notebook pero no
en producción. Un Ingeniero de IA DEBE saber desplegar modelos.


NIVEL 7: PROYECTO REAL (módulo 33)
──────────────────────────────────
Un proyecto end-to-end que demuestre todo lo anterior.
Esto es lo que pones en tu CV y muestras en entrevistas.


CONSEJO CLAVE:
No saltes niveles. Cada nivel se construye sobre el anterior.
Si no dominas NumPy, no puedes entender PyTorch.
Si no dominas funciones y clases, no puedes entender scikit-learn.
Si no dominas Python, no puedes hacer nada.

ESTOS APUNTES SON EL NIVEL 1.
El más importante de todos.
"""


# ===========================================================================
# CAPÍTULO 10: ENTORNOS VIRTUALES — POR QUÉ Y CÓMO (ESENCIAL)
# ===========================================================================

"""
Antes de escribir una sola línea más de Python, necesitas entender
los entornos virtuales. Es lo PRIMERO que hace un profesional.

EL PROBLEMA
============
Python tiene un sistema de paquetes global. Si instalas una librería:
    pip install numpy

Se instala en tu Python del sistema. Todos tus proyectos comparten
las mismas librerías y las mismas versiones.

¿Qué pasa si:
  - Proyecto A necesita NumPy 1.24
  - Proyecto B necesita NumPy 2.0
  - Son incompatibles

Respuesta: TODO SE ROMPE.

LA SOLUCIÓN: ENTORNOS VIRTUALES
================================
Un entorno virtual es una COPIA AISLADA de Python para cada proyecto.

Cada proyecto tiene SU propio Python, SUS propias librerías, SUS
propias versiones. Sin conflictos.

CÓMO CREAR UNO (usando venv, que viene con Python):
─────────────────────────────────────────────────────
  # 1. Crear el entorno virtual (una sola vez por proyecto)
  python3 -m venv .venv

  # Esto crea una carpeta .venv/ con:
  #   .venv/bin/python    → copia del intérprete Python
  #   .venv/lib/          → librerías aisladas
  #   .venv/bin/pip       → pip aislado

  # 2. Activar el entorno virtual (cada vez que abras terminal)
  source .venv/bin/activate          # Linux/macOS
  .venv\Scripts\activate             # Windows

  # Tu prompt cambiará a: (.venv) usuario@máquina:~$
  # Ahora pip instala SOLO dentro de .venv/

  # 3. Instalar dependencias
  pip install numpy pandas

  # 4. Congelar dependencias (para que otros reproduzcan tu entorno)
  pip freeze > requirements.txt

  # 5. Desactivar cuando termines
  deactivate

REGLAS DE ORO:
  1. NUNCA instales librerías en el Python del sistema
  2. SIEMPRE crea un .venv para cada proyecto
  3. SIEMPRE añade .venv/ al .gitignore
  4. SIEMPRE genera requirements.txt
  5. NUNCA subas .venv/ a Git (pesa demasiado)

ALTERNATIVAS A VENV:
  - Poetry: gestión moderna de dependencias + packaging
  - uv: alternativa ultra-rápida escrita en Rust (muy nueva)
  - conda: popular en ciencia de datos, gestiona también paquetes C
  - pipenv: otra alternativa (menos popular hoy)

Para empezar, usa venv. Es simple y viene con Python.
Cuando avances, te enseñaré Poetry y uv.
"""


# ===========================================================================
# CAPÍTULO 11: ESTRUCTURA DE UN PROYECTO PYTHON PROFESIONAL
# ===========================================================================

"""
Desde el día 1, tus proyectos deben tener estructura profesional.
No es un archivo suelto en el escritorio.

ESTRUCTURA MÍNIMA PARA APRENDER:
=================================

mi_proyecto/
├── .venv/                  ← entorno virtual (NO se sube a Git)
├── .gitignore              ← archivos que Git debe ignorar
├── requirements.txt        ← dependencias del proyecto
├── README.md               ← documentación del proyecto
└── src/                    ← tu código
    ├── __init__.py         ← convierte src/ en un paquete Python
    └── main.py             ← punto de entrada


ESTRUCTURA PROFESIONAL (para proyectos reales):
================================================

mi_proyecto/
├── .venv/
├── .gitignore
├── .env                    ← variables de entorno (secretos, NO subir a Git)
├── .env.example            ← plantilla de .env (SÍ se sube)
├── pyproject.toml          ← configuración moderna de Python (reemplaza setup.py)
├── requirements.txt
├── requirements-dev.txt    ← dependencias de desarrollo (pytest, mypy, etc.)
├── README.md
├── Makefile                ← comandos útiles automatizados
├── Dockerfile              ← para containerizar (módulo 31)
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py           ← configuración centralizada
│   ├── models/             ← clases de dominio
│   ├── services/           ← lógica de negocio
│   ├── repositories/       ← acceso a datos
│   └── utils/              ← funciones auxiliares
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── conftest.py         ← configuración de pytest
├── notebooks/              ← Jupyter notebooks para experimentación
├── data/                   ← datos locales (NO subir a Git si son grandes)
├── models/                 ← modelos entrenados guardados
└── docs/                   ← documentación adicional


QUÉ PONER EN .gitignore:
=========================
"""

gitignore_ejemplo = """
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# Entorno virtual
.venv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Variables de entorno
.env

# Datos y modelos (si son grandes)
data/
models/*.pkl
models/*.pt
*.h5

# Jupyter
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db
"""

print(gitignore_ejemplo)


# ===========================================================================
# CAPÍTULO 12: TU PRIMER PROGRAMA REAL
# ===========================================================================

"""
Ahora que entiendes el contexto, vamos a escribir algo real.
No un "hola mundo", sino un programa mínimo que demuestre varios
conceptos fundamentales.
"""

# ─── Un programa que procesa datos ─────────────────────────────

# 1. Definimos datos (los hardcodeamos por ahora)
temperaturas_semana = [22.5, 25.0, 19.3, 28.1, 24.7, 21.0, 26.8]
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# 2. Calculamos estadísticas básicas
total = sum(temperaturas_semana)                    # sum() es built-in
cantidad = len(temperaturas_semana)                 # len() es built-in
media = total / cantidad
maxima = max(temperaturas_semana)                   # max() es built-in
minima = min(temperaturas_semana)                   # min() es built-in

# 3. Encontramos el día más caluroso
indice_max = temperaturas_semana.index(maxima)      # .index() busca posición
dia_mas_caluroso = dias[indice_max]

# 4. Mostramos resultados con f-strings (formatted string literals)
print("=" * 50)                                     # Multiplica string
print("📊 INFORME SEMANAL DE TEMPERATURAS")
print("=" * 50)

for i, (dia, temp) in enumerate(zip(dias, temperaturas_semana)):
    # enumerate() da el índice
    # zip() combina dos listas en pares
    indicador = "🔥" if temp == maxima else "❄️" if temp == minima else "  "
    print(f"  {indicador} {dia:<12} {temp:>5.1f}°C")
    #        {dia:<12}  → alinea a la izquierda, 12 caracteres
    #        {temp:>5.1f} → alinea a la derecha, 5 chars, 1 decimal

print("-" * 50)
print(f"  Media:   {media:.1f}°C")
print(f"  Máxima:  {maxima:.1f}°C ({dia_mas_caluroso})")
print(f"  Mínima:  {minima:.1f}°C")
print("=" * 50)

# 5. Clasificación simple (preludio a ML)
if media > 25:
    clasificacion = "Semana calurosa"
elif media > 20:
    clasificacion = "Semana templada"
else:
    clasificacion = "Semana fría"

print(f"\n  Clasificación: {clasificacion}")

"""
NOTA SOBRE ESTE PROGRAMA:
- Usa listas, strings, números, booleanos
- Usa funciones built-in (sum, len, max, min, print, enumerate, zip)
- Usa f-strings con formateo
- Usa condicionales (if/elif/else)
- Usa bucles (for)
- Usa desempaquetado (dia, temp)

Cada uno de estos conceptos se explicará EN PROFUNDIDAD en los archivos
siguientes. Este programa es solo un preview de lo que viene.

En el próximo archivo veremos el MODELO DE OBJETOS de Python:
cómo funciona la memoria, qué son las referencias, por qué Python
es "todo objetos", y cómo entender id(), type(), y la diferencia
entre identidad e igualdad.
"""


# ===========================================================================
# RESUMEN DE ESTE ARCHIVO
# ===========================================================================

"""
LO QUE HAS APRENDIDO:

1. Python es un lenguaje interpretado de alto nivel con tipado dinámico
2. CPython compila tu .py → bytecode (.pyc) → lo ejecuta en la PVM
3. Python domina IA por su ecosistema de librerías, no por su velocidad
4. Las librerías de IA (NumPy, PyTorch) ejecutan C/CUDA por debajo
5. Siempre usar Python 3.12+ y CPython
6. Siempre crear entornos virtuales (.venv)
7. Siempre tener estructura profesional de proyecto
8. El Zen de Python: legibilidad, simplicidad, explicitud

ARCHIVO SIGUIENTE: 02_modelo_de_objetos.py
→ Cómo Python gestiona la memoria
→ Variables como REFERENCIAS a objetos
→ id(), type(), is vs ==
→ Mutabilidad vs inmutabilidad
→ El corazón de cómo funciona Python
"""
