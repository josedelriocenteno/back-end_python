# ===========================================================================
# 01_funciones_scope_y_closures.py
# ===========================================================================
# MÓDULO 04: FUNCIONES, FLUJO Y PROGRAMACIÓN FUNCIONAL
# ARCHIVO 01: Funciones, Scope LEGB, Closures y First-Class Functions
# ===========================================================================
#
# OBJETIVO (1000+ LÍNEAS):
# Dominar las funciones de Python como ciudadanos de primera clase.
# Entender el modelo de scope LEGB que gobierna la visibilidad de variables,
# closures para factories de funciones, y el patrón de higher-order functions
# que es la base de decoradores, callbacks, y programación funcional.
#
# CONTENIDO:
#   1. Funciones como objetos de primera clase.
#   2. Parámetros: *args, **kwargs, keyword-only, positional-only.
#   3. Scope LEGB: Local, Enclosing, Global, Built-in.
#   4. global y nonlocal: cuándo y por qué (casi nunca).
#   5. Closures: funciones que capturan su entorno.
#   6. Factory functions: crear funciones dinámicamente.
#   7. Higher-order functions: funciones que reciben/retornan funciones.
#   8. Aplicaciones ML: callbacks, schedulers, function registries.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import time
import sys
from typing import Callable, Any
from functools import partial


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 1: FUNCIONES COMO OBJETOS DE PRIMERA CLASE                    ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: FUNCIONES SON OBJETOS ===")
print("=" * 80)

"""
En Python, las funciones son OBJETOS de primera clase (first-class objects).
Esto significa que una función:
1. Se puede asignar a una variable.
2. Se puede pasar como argumento a otra función.
3. Se puede retornar desde otra función.
4. Se puede almacenar en estructuras de datos (listas, dicts).
5. Tiene atributos: __name__, __doc__, __defaults__, __code__.

Esto es la BASE de:
- Decoradores.
- Callbacks en training loops.
- Function registries (mapeo nombre -> función).
- Programación funcional (map, filter, reduce).
"""

print("\n--- Funciones como objetos ---")

def saludar(nombre: str) -> str:
    """Retorna un saludo formal."""
    return f"Hola, {nombre}!"

# 1. Asignar a variable
mi_funcion = saludar
print(f"Llamada directa: {saludar('Python')}")
print(f"Via variable:     {mi_funcion('Python')}")
print(f"¿Son la misma?    {saludar is mi_funcion}")

# 2. Inspeccionar atributos
print(f"\n__name__: {saludar.__name__}")
print(f"__doc__:  {saludar.__doc__}")
print(f"type():   {type(saludar)}")
print(f"id():     {id(saludar)}")

# 3. Almacenar en estructuras de datos
operaciones = {
    "sumar": lambda a, b: a + b,
    "restar": lambda a, b: a - b,
    "multiplicar": lambda a, b: a * b,
}

for nombre_op, func in operaciones.items():
    print(f"  {nombre_op}(10, 3) = {func(10, 3)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: PARÁMETROS EN PROFUNDIDAD ===")
print("=" * 80)

"""
Python tiene 5 tipos de parámetros:
1. Posicionales regulares.
2. *args: captura posicionales extra como TUPLA.
3. **kwargs: captura keyword extras como DICCIONARIO.
4. Keyword-only (después de *): DEBEN pasarse por nombre.
5. Positional-only (antes de /): NO se pueden pasar por nombre (Python 3.8+).

ORDEN OBLIGATORIO:
def func(pos_only, /, regular, *, keyword_only, **kwargs)
"""

print("\n--- *args y **kwargs ---")

def log_flexible(*args, **kwargs):
    """Acepta cualquier cantidad de argumentos posicionales y keyword."""
    print(f"  args ({type(args).__name__}): {args}")
    print(f"  kwargs ({type(kwargs).__name__}): {kwargs}")

log_flexible(1, 2, 3, nivel="INFO", modelo="BERT")


print("\n--- Keyword-only arguments (después de *) ---")

def entrenar_modelo(datos, *, epochs: int = 10, lr: float = 0.001, 
                    verbose: bool = True):
    """epochs, lr y verbose SOLO se pueden pasar por nombre."""
    if verbose:
        print(f"  Entrenando con {len(datos)} datos, epochs={epochs}, lr={lr}")

# entrenar_modelo([1,2,3], 20)  # TypeError! epochs es keyword-only
entrenar_modelo([1, 2, 3], epochs=20, lr=0.0001)


print("\n--- Positional-only arguments (antes de /) (Python 3.8+) ---")

def distancia_euclidiana(x1, y1, x2, y2, /):
    """x1, y1, x2, y2 SOLO se pueden pasar por posición."""
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

print(f"  Distancia (0,0) a (3,4): {distancia_euclidiana(0, 0, 3, 4)}")
# distancia_euclidiana(x1=0, y1=0, x2=3, y2=4)  # TypeError!


print("\n--- Patrón completo: positional-only + regular + keyword-only ---")

def configurar_pipeline(
    nombre, /,                  # Solo posicional
    modelo, dataset,            # Regular (posicional o keyword)
    *, lr=0.001, epochs=10      # Solo keyword
):
    print(f"  Pipeline: {nombre} | modelo={modelo} | dataset={dataset} "
          f"| lr={lr} | epochs={epochs}")

configurar_pipeline("v1", "BERT", "IMDB", lr=0.0005, epochs=20)
configurar_pipeline("v2", modelo="GPT", dataset="Wiki")


print("\n--- Desempaquetado con * y ** ---")

params = [1, 2, 3, 4]
print(f"  Distancia: {distancia_euclidiana(*params)}")

config = {"modelo": "T5", "dataset": "CommonCrawl", "lr": 0.0001}
configurar_pipeline("v3", **config)


print("\n--- Valores por defecto mutables: LA TRAMPA ---")

def agregar_item_MAL(item, lista=[]):
    """BUG: la lista por defecto se comparte entre TODAS las llamadas."""
    lista.append(item)
    return lista

print(f"\n  Llamada 1: {agregar_item_MAL('a')}")
print(f"  Llamada 2: {agregar_item_MAL('b')}")
print(f"  ¡La lista se acumula entre llamadas!")

def agregar_item_BIEN(item, lista=None):
    """CORRECTO: usar None y crear una nueva lista en cada llamada."""
    if lista is None:
        lista = []
    lista.append(item)
    return lista

print(f"\n  Llamada 1: {agregar_item_BIEN('a')}")
print(f"  Llamada 2: {agregar_item_BIEN('b')}")
print(f"  Cada llamada tiene su propia lista.")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 2: SCOPE LEGB                                                 ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 3: SCOPE LEGB — LA REGLA DE VISIBILIDAD ===")
print("=" * 80)

"""
Cuando Python busca una variable, la busca en este orden:
L - Local: dentro de la función actual.
E - Enclosing: en la función que contiene a la actual (closures).
G - Global: a nivel de módulo.
B - Built-in: nombres predefinidos de Python (len, print, int...).

Si no la encuentra en ninguno, lanza NameError.

REGLA DE ORO:
- Python PUEDE LEER variables de cualquier scope.
- Python SOLO PUEDE MODIFICAR variables del scope LOCAL por defecto.
- Para modificar global: declarar `global nombre`.
- Para modificar enclosing: declarar `nonlocal nombre`.
"""

print("\n--- Demostración LEGB ---")

x_global = "SOY GLOBAL"

def funcion_externa():
    x_enclosing = "SOY ENCLOSING"
    
    def funcion_interna():
        x_local = "SOY LOCAL"
        
        # Python busca en orden: L -> E -> G -> B
        print(f"  Local:     {x_local}")
        print(f"  Enclosing: {x_enclosing}")
        print(f"  Global:    {x_global}")
        print(f"  Built-in:  {len}")  # len es built-in
    
    funcion_interna()

funcion_externa()


print("\n--- Shadowing: cuando un scope oculta otro ---")

valor = "GLOBAL"

def shadow_demo():
    valor = "LOCAL"  # Sombrea la variable global
    print(f"  Dentro de la función: {valor}")

shadow_demo()
print(f"  Fuera de la función: {valor}")  # Global no cambia


print("\n--- global: NO LA USES (pero entiéndela) ---")

contador_global = 0

def incrementar_mal():
    global contador_global  # Permite MODIFICAR la variable global
    contador_global += 1

incrementar_mal()
incrementar_mal()
print(f"\n  contador_global = {contador_global}")
print(f"  EVITA 'global'. Crea estado compartido invisible -> bugs.")


print("\n--- nonlocal: modificar variable del enclosing scope ---")

def crear_contador():
    """Factory que crea contadores independientes usando nonlocal."""
    count = 0
    
    def incrementar():
        nonlocal count  # Modifica count del enclosing scope
        count += 1
        return count
    
    return incrementar

counter_a = crear_contador()
counter_b = crear_contador()

print(f"\n  Counter A: {counter_a()}, {counter_a()}, {counter_a()}")
print(f"  Counter B: {counter_b()}, {counter_b()}")
print(f"  Son independientes: cada closure tiene su propia 'count'")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 3: CLOSURES                                                   ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 4: CLOSURES — FUNCIONES CON MEMORIA ===")
print("=" * 80)

"""
Una CLOSURE es una función que recuerda las variables del entorno
donde fue creada, incluso después de que ese entorno haya terminado.

TÉCNICAMENTE: una closure es una función interna que:
1. Referencia variables libres (del enclosing scope).
2. Se retorna desde la función externa.
3. Las variables capturadas sobreviven en __closure__.

EN ML, las closures son FUNDAMENTALES para:
- Learning rate schedulers: generan lr en función del step.
- Loss functions parametrizadas: crear cross_entropy con class_weights.
- Callbacks que capturan el estado del entrenamiento.
"""

print("\n--- Anatomía de una closure ---")

def crear_multiplicador(factor: float):
    """Factory: retorna una función que multiplica por 'factor'."""
    
    def multiplicar(x: float) -> float:
        return x * factor  # 'factor' es variable LIBRE (del enclosing)
    
    return multiplicar

doble = crear_multiplicador(2)
triple = crear_multiplicador(3)

print(f"doble(5) = {doble(5)}")
print(f"triple(5) = {triple(5)}")

# Inspeccionar la closure
print(f"\ndoble.__closure__: {doble.__closure__}")
print(f"doble.__closure__[0].cell_contents: {doble.__closure__[0].cell_contents}")
print(f"triple.__closure__[0].cell_contents: {triple.__closure__[0].cell_contents}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: FACTORY FUNCTIONS PARA ML ===")
print("=" * 80)

"""
Las factory functions crean funciones personalizadas en runtime.
Son MÁS POTENTES QUE LAMBDAS: pueden tener estado, docstrings,
y lógica arbitrariamente compleja.
"""

print("\n--- Learning Rate Scheduler como closure ---")

def crear_lr_scheduler(lr_inicial: float, decay: float = 0.95):
    """Crea un scheduler que reduce el lr exponencialmente."""
    step = [0]  # Lista para esquivar nonlocal (mutable)
    
    def get_lr() -> float:
        lr = lr_inicial * (decay ** step[0])
        step[0] += 1
        return lr
    
    return get_lr

scheduler = crear_lr_scheduler(0.01, decay=0.9)
for i in range(10):
    lr = scheduler()
    print(f"  Step {i}: lr = {lr:.6f}")


print("\n--- Loss function parametrizada ---")

def crear_weighted_loss(pesos_clase: dict):
    """Crea una función de loss con pesos personalizados por clase."""
    
    def loss(predicciones: list, labels: list) -> float:
        total_loss = 0
        for pred, label in zip(predicciones, labels):
            error = (pred - 1.0) ** 2 if label == 1 else pred ** 2
            peso = pesos_clase.get(label, 1.0)
            total_loss += error * peso
        return total_loss / len(predicciones)
    
    return loss

# Clases desbalanceadas: clase 1 es rara -> peso alto
loss_fn = crear_weighted_loss({0: 1.0, 1: 5.0})
preds = [0.1, 0.8, 0.3, 0.9]
labels = [0, 1, 0, 1]
print(f"\n  Loss ponderada: {loss_fn(preds, labels):.4f}")

# Loss sin pesos
loss_simple = crear_weighted_loss({0: 1.0, 1: 1.0})
print(f"  Loss simple:    {loss_simple(preds, labels):.4f}")


print("\n--- Function Registry: mapeo nombre -> función ---")

class ModelRegistry:
    """Registro de funciones de creación de modelos."""
    
    def __init__(self):
        self._registry = {}
    
    def register(self, nombre: str):
        """Decorador para registrar una función de creación de modelo."""
        def decorator(func):
            self._registry[nombre] = func
            return func
        return decorator
    
    def create(self, nombre: str, **kwargs):
        if nombre not in self._registry:
            raise KeyError(f"Modelo '{nombre}' no registrado. "
                         f"Disponibles: {list(self._registry.keys())}")
        return self._registry[nombre](**kwargs)
    
    def listar(self):
        return list(self._registry.keys())

registry = ModelRegistry()

@registry.register("linear")
def crear_linear(input_dim=768, output_dim=2):
    return {"tipo": "linear", "params": input_dim * output_dim}

@registry.register("mlp")
def crear_mlp(input_dim=768, hidden_dim=256, output_dim=2):
    return {"tipo": "mlp", "params": input_dim * hidden_dim + hidden_dim * output_dim}

print(f"\n  Modelos registrados: {registry.listar()}")
print(f"  Crear linear: {registry.create('linear')}")
print(f"  Crear mlp:    {registry.create('mlp', hidden_dim=512)}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 4: HIGHER-ORDER FUNCTIONS                                     ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 6: HIGHER-ORDER FUNCTIONS ===")
print("=" * 80)

"""
Una función de orden superior (higher-order function) es una función que:
- Recibe una función como argumento, O
- Retorna una función como resultado.

map(), filter(), sorted() son higher-order functions built-in.
Los decoradores son higher-order functions que wrappean otras funciones.
"""

print("\n--- map(): aplicar función a cada elemento ---")

# map es lazy (retorna un iterador)
nums = [1, 2, 3, 4, 5]
cuadrados = list(map(lambda x: x**2, nums))
print(f"map(x², {nums}) = {cuadrados}")

# Equivalente a list comprehension (preferido en Python moderno)
cuadrados_lc = [x**2 for x in nums]
print(f"List comp: {cuadrados_lc}")


print("\n--- filter(): filtrar elementos ---")

pares = list(filter(lambda x: x % 2 == 0, range(20)))
print(f"filter(par, 0-19) = {pares}")


print("\n--- reduce(): acumular un resultado ---")

from functools import reduce

producto = reduce(lambda a, b: a * b, [1, 2, 3, 4, 5])
print(f"reduce(*, [1,2,3,4,5]) = {producto}")


print("\n--- Funciones como callbacks en training ---")

def entrenar_con_callbacks(datos, epochs, callbacks=None):
    """Simula un training loop con callbacks."""
    if callbacks is None:
        callbacks = []
    
    for epoch in range(1, epochs + 1):
        # Simular métricas
        loss = 1.0 / epoch
        acc = 1.0 - loss
        metricas = {"epoch": epoch, "loss": loss, "acc": acc}
        
        for callback in callbacks:
            callback(metricas)

def log_metricas(metricas):
    print(f"  [LOG] Epoch {metricas['epoch']}: loss={metricas['loss']:.4f}")

def early_stop_factory(patience=3, min_loss=0.2):
    mejores = {"loss": float('inf'), "wait": 0}
    
    def check(metricas):
        if metricas["loss"] < mejores["loss"]:
            mejores["loss"] = metricas["loss"]
            mejores["wait"] = 0
        else:
            mejores["wait"] += 1
        
        if mejores["wait"] >= patience:
            print(f"  [EARLY STOP] Patience agotada en epoch {metricas['epoch']}")
    
    return check

print("\nTraining con callbacks:")
entrenar_con_callbacks(
    datos=[1, 2, 3],
    epochs=5,
    callbacks=[log_metricas, early_stop_factory(patience=2)]
)


print("\n" + "=" * 80)
print("=== CAPÍTULO 7: FUNCTOOLS.PARTIAL — FUNCIONES PARCIALMENTE APLICADAS ===")
print("=" * 80)

"""
functools.partial(func, *args, **kwargs) crea una NUEVA función
con algunos argumentos pre-rellenados. Es como una closure simplificada.
"""

print("\n--- partial: pre-rellenar argumentos ---")

def potencia(base, exponente):
    return base ** exponente

cuadrado = partial(potencia, exponente=2)
cubo = partial(potencia, exponente=3)

print(f"cuadrado(5) = {cuadrado(5)}")
print(f"cubo(5) = {cubo(5)}")

# Ejemplo ML: crear variantes de optimizadores
def optimizar(params, lr, momentum=0.9, weight_decay=0.0):
    return f"SGD(lr={lr}, mom={momentum}, wd={weight_decay})"

sgd_fast = partial(optimizar, lr=0.01)
sgd_slow = partial(optimizar, lr=0.0001, weight_decay=0.01)

print(f"\n  SGD rápido: {sgd_fast(params='model')}")
print(f"  SGD lento:  {sgd_slow(params='model')}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: LAMBDA — FUNCIONES ANÓNIMAS ===")
print("=" * 80)

"""
lambda crea funciones anónimas de UNA sola expresión.
Son útiles como argumentos de sorted(), map(), filter() cuando
la función es trivial y no merece un nombre.

REGLA: si el lambda ocupa más de una línea o es difícil de leer,
usa una función nombrada (def).
"""

print("\n--- Lambda vs def ---")

# Equivalentes:
f1 = lambda x: x ** 2
def f2(x): return x ** 2

print(f"lambda(5) = {f1(5)}")
print(f"def(5)    = {f2(5)}")
print(f"lambda.__name__ = '{f1.__name__}'")  # <lambda>
print(f"def.__name__    = '{f2.__name__}'")  # f2

# Lambda en sorted
datos_ml = [
    {"name": "BERT", "params": 110_000_000},
    {"name": "GPT-2", "params": 1_500_000_000},
    {"name": "T5-small", "params": 60_000_000},
]

por_params = sorted(datos_ml, key=lambda m: m["params"])
print(f"\nModelos por tamaño:")
for m in por_params:
    print(f"  {m['name']}: {m['params']:,} params")


print("\n" + "=" * 80)
print("=== CAPÍTULO 9: TYPE HINTS PARA FUNCIONES ===")
print("=" * 80)

"""
Los type hints son DOCUMENTACIÓN VIVA. No afectan al runtime de Python
pero ayudan a los IDEs, mypy, y al equipo a entender el código.

Para funciones:
- Callable[[arg_types], return_type]: tipo de una función.
- Callable[..., return_type]: función con args cualquiera.
"""

print("\n--- Type hints con Callable ---")

def aplicar_transformacion(
    datos: list[float],
    transformacion: Callable[[float], float]
) -> list[float]:
    """Aplica una transformación a cada elemento."""
    return [transformacion(x) for x in datos]

resultado = aplicar_transformacion(
    [1.0, 2.0, 3.0, 4.0],
    lambda x: x ** 0.5
)
print(f"  sqrt([1,2,3,4]) = {[f'{x:.2f}' for x in resultado]}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: EJERCICIO — PIPELINE DE TRANSFORMACIONES ML ===")
print("=" * 80)

"""
Construir un pipeline que encadene múltiples transformaciones sobre datos,
usando closures y higher-order functions.
"""

print("\n--- Pipeline funcional ---")

class FunctionalPipeline:
    """Pipeline de transformaciones composables."""
    
    def __init__(self):
        self.steps: list[tuple[str, Callable]] = []
    
    def add(self, nombre: str, func: Callable):
        self.steps.append((nombre, func))
        return self  # Permite chaining
    
    def ejecutar(self, datos, verbose=True):
        resultado = datos
        for nombre, func in self.steps:
            resultado = func(resultado)
            if verbose:
                muestra = str(resultado)[:60]
                print(f"  [{nombre}] -> {muestra}...")
        return resultado

# Crear transformaciones como funciones puras
def normalizar(datos: list[float]) -> list[float]:
    min_val, max_val = min(datos), max(datos)
    rango = max_val - min_val
    return [(x - min_val) / rango if rango > 0 else 0 for x in datos]

def filtrar_outliers_factory(n_sigma: float = 2.0):
    """Factory que crea un filtro de outliers parametrizado."""
    def filtrar(datos: list[float]) -> list[float]:
        media = sum(datos) / len(datos)
        varianza = sum((x - media)**2 for x in datos) / len(datos)
        std = varianza ** 0.5
        return [x for x in datos if abs(x - media) <= n_sigma * std]
    return filtrar

def aplicar_log(datos: list[float]) -> list[float]:
    import math
    return [math.log1p(max(0, x)) for x in datos]

# Montar pipeline
import random
random.seed(42)
datos_raw = [random.gauss(100, 20) for _ in range(50)]
datos_raw.extend([300, -50])  # Outliers

pipeline = (FunctionalPipeline()
    .add("Filtrar outliers", filtrar_outliers_factory(2.0))
    .add("Normalizar 0-1", normalizar)
)

print("Pipeline de transformaciones:")
resultado_final = pipeline.ejecutar(datos_raw)
print(f"\n  Entrada: {len(datos_raw)} valores")
print(f"  Salida:  {len(resultado_final)} valores")
print(f"  Rango:   [{min(resultado_final):.2f}, {max(resultado_final):.2f}]")


print("\n" + "=" * 80)
print("=== CAPÍTULO 11: INTROSPECCIÓN DE FUNCIONES CON inspect ===")
print("=" * 80)

"""
El módulo inspect permite inspeccionar funciones en runtime:
- Obtener la firma (parámetros, defaults, annotations).
- Obtener el código fuente.
- Saber si algo es función, generador, clase, etc.

Esto es fundamental para:
- Frameworks que auto-generan documentación.
- Dependency injection (FastAPI lo usa masivamente).
- Validación dinámica de argumentos.
"""

import inspect

print("\n--- inspect.signature: obtener la firma ---")

def entrenar(modelo: str, epochs: int = 10, lr: float = 0.001,
             *, verbose: bool = True) -> dict:
    """Entrena un modelo con los parámetros dados."""
    return {"modelo": modelo, "epochs": epochs, "lr": lr}

sig = inspect.signature(entrenar)
print(f"  Firma: {sig}")
print(f"  Parámetros:")
for name, param in sig.parameters.items():
    print(f"    {name}: kind={param.kind.name}, default={param.default}, "
          f"annotation={param.annotation}")

print(f"\n  Return annotation: {sig.return_annotation}")


print("\n--- inspect: obtener código fuente ---")

source = inspect.getsource(normalizar)
print(f"  Código de normalizar():")
for line in source.strip().split("\n")[:5]:
    print(f"    {line}")


print("\n--- inspect: verificar tipos de callable ---")

class MiClase:
    def metodo(self): pass
    @staticmethod
    def estatico(): pass
    @classmethod
    def de_clase(cls): pass

print(f"  normalizar es función: {inspect.isfunction(normalizar)}")
print(f"  MiClase es clase: {inspect.isclass(MiClase)}")
print(f"  metodo es método: {inspect.ismethod(MiClase().metodo)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: COMPOSICIÓN DE FUNCIONES (COMPOSE) ===")
print("=" * 80)

"""
Compose: f(g(h(x))) = compose(f, g, h)(x).
Patrón fundamental en programación funcional.
Python no lo tiene built-in, pero se construye fácil.
"""

print("\n--- compose: encadenar funciones ---")

def compose(*funciones):
    """Compone funciones de derecha a izquierda: compose(f, g)(x) = f(g(x))."""
    from functools import reduce
    
    def compuesta(x):
        return reduce(lambda acc, f: f(acc), reversed(funciones), x)
    
    return compuesta

# Pipeline de limpieza de texto
limpiar = compose(
    str.strip,
    str.lower,
    lambda s: " ".join(s.split()),  # Colapsar espacios
)

textos = ["  HOLA   MUNDO  ", "  Machine   Learning  "]
for t in textos:
    print(f"  '{t}' -> '{limpiar(t)}'")


print("\n--- pipe: composición de izquierda a derecha ---")

def pipe(*funciones):
    """pipe(f, g)(x) = g(f(x)). Más natural para pipelines de datos."""
    from functools import reduce
    def piped(x):
        return reduce(lambda acc, f: f(acc), funciones, x)
    return piped

# Pipeline numérico
import math

procesar_score = pipe(
    lambda x: max(0.0, x),       # Clamp a 0+
    lambda x: math.log1p(x),    # Log transform
    lambda x: round(x, 4),      # Redondear
)

scores = [-0.5, 0.0, 1.0, 10.0, 100.0]
for s in scores:
    print(f"  score={s:>6.1f} -> {procesar_score(s)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: CLOSURE PITFALL — EL ERROR DEL LOOP ===")
print("=" * 80)

"""
El error MÁS COMÚN con closures: crear funciones en un loop.
La variable del loop se captura POR REFERENCIA, no por valor.
Todas las closures ven el ÚLTIMO valor del loop.
"""

print("\n--- El bug ---")

# MAL: todas las funciones imprimen 4 (el último valor de i)
funciones_mal = []
for i in range(5):
    funciones_mal.append(lambda: i)

print(f"  Bug: {[f() for f in funciones_mal]}")
print(f"  Esperado: [0, 1, 2, 3, 4]")
print(f"  Real:     {[f() for f in funciones_mal]}")

# SOLUCIÓN 1: default argument (captura por valor)
funciones_bien = []
for i in range(5):
    funciones_bien.append(lambda i=i: i)  # i=i fuerza copia

print(f"\n  Solución (default arg): {[f() for f in funciones_bien]}")

# SOLUCIÓN 2: factory function
def crear_func(valor):
    return lambda: valor

funciones_bien2 = [crear_func(i) for i in range(5)]
print(f"  Solución (factory):    {[f() for f in funciones_bien2]}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: EJERCICIO — METRICS TRACKER CON CLOSURES ===")
print("=" * 80)

"""
Construir un tracker de métricas de entrenamiento que usa closures
para mantener estado y factories para crear métricas personalizadas.
"""

print("\n--- MetricsTracker ---")

def crear_metrics_tracker():
    """Factory que crea un tracker de métricas con closures."""
    historial = {}
    
    def registrar(nombre: str, valor: float, step: int):
        if nombre not in historial:
            historial[nombre] = []
        historial[nombre].append({"step": step, "valor": valor})
    
    def obtener(nombre: str) -> list:
        return historial.get(nombre, [])
    
    def resumen(nombre: str) -> dict:
        datos = historial.get(nombre, [])
        if not datos:
            return {}
        valores = [d["valor"] for d in datos]
        return {
            "nombre": nombre,
            "n": len(valores),
            "min": min(valores),
            "max": max(valores),
            "media": sum(valores) / len(valores),
            "ultimo": valores[-1],
        }
    
    def todos_los_nombres() -> list:
        return list(historial.keys())
    
    # Retornar un namespace de funciones (patrón módulo)
    return type("MetricsTracker", (), {
        "registrar": staticmethod(registrar),
        "obtener": staticmethod(obtener),
        "resumen": staticmethod(resumen),
        "nombres": staticmethod(todos_los_nombres),
    })()

tracker = crear_metrics_tracker()

# Simular entrenamiento
import random
random.seed(42)
for step in range(1, 21):
    loss = 1.0 / step + random.gauss(0, 0.05)
    acc = 1.0 - loss + random.gauss(0, 0.02)
    tracker.registrar("loss", loss, step)
    tracker.registrar("accuracy", acc, step)

print(f"Métricas registradas: {tracker.nombres()}")
for nombre in tracker.nombres():
    r = tracker.resumen(nombre)
    print(f"  {r['nombre']}: n={r['n']}, min={r['min']:.4f}, "
          f"max={r['max']:.4f}, media={r['media']:.4f}, ultimo={r['ultimo']:.4f}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: CURRYING — APLICACIÓN PARCIAL PROGRESIVA ===")
print("=" * 80)

"""
Currying: transformar f(a, b, c) en f(a)(b)(c).
Cada llamada retorna una nueva función que espera el siguiente argumento.
Es la base teórica de partial() pero más estricto.
"""

print("\n--- Curry manual ---")

def curry_suma(a):
    def paso2(b):
        def paso3(c):
            return a + b + c
        return paso3
    return paso2

print(f"  curry_suma(1)(2)(3) = {curry_suma(1)(2)(3)}")

# Crear variantes
sumar_10 = curry_suma(10)
sumar_10_20 = sumar_10(20)
print(f"  sumar_10(20)(30) = {sumar_10_20(30)}")


print("\n--- Auto-curry genérico ---")

def auto_curry(func):
    """Convierte cualquier función en su versión curried."""
    n_params = len(inspect.signature(func).parameters)
    
    def curried(*args):
        if len(args) >= n_params:
            return func(*args[:n_params])
        return lambda *more: curried(*args, *more)
    
    return curried

@auto_curry
def distancia(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2) ** 0.5

# Todas estas formas son válidas:
print(f"\n  distancia(0, 0, 3, 4) = {distancia(0, 0, 3, 4)}")
print(f"  distancia(0)(0)(3)(4) = {distancia(0)(0)(3)(4)}")
print(f"  distancia(0, 0)(3, 4) = {distancia(0, 0)(3, 4)}")

# Fijar origen
desde_origen = distancia(0, 0)
print(f"  desde_origen(3, 4) = {desde_origen(3, 4)}")
print(f"  desde_origen(1, 1) = {desde_origen(1, 1):.4f}")


print("\n--- Currying para ML: crear evaluadores parciales ---")

@auto_curry
def evaluar_modelo(metrica, threshold, modelo, datos):
    """Evalua un modelo contra un threshold con una metrica."""
    score = hash((modelo, str(datos))) % 100 / 100
    ok = "PASS" if score >= threshold else "FAIL"
    return f"{metrica}({modelo}): {score:.2f} [{ok}]"

# Fijar metrica y threshold
eval_accuracy_80 = evaluar_modelo("accuracy", 0.8)
eval_f1_70 = evaluar_modelo("f1_score", 0.7)

print(f"  {eval_accuracy_80('BERT', [1,2,3])}")
print(f"  {eval_accuracy_80('GPT', [1,2,3])}")
print(f"  {eval_f1_70('T5', [4,5,6])}")

# Fijar tambien el modelo
eval_bert_acc = eval_accuracy_80("BERT")
print(f"  BERT con datos [7,8]: {eval_bert_acc([7,8])}")
print(f"  BERT con datos [9,0]: {eval_bert_acc([9,0])}")


print("\n" + "=" * 80)
print("=== CONCLUSIÓN ARQUITECTÓNICA ===")
print("=" * 80)

"""
RESUMEN DE FUNCIONES Y SCOPE PARA INGENIERÍA IA:

1. Las funciones son OBJETOS: se asignan, pasan y retornan libremente.

2. Parámetros: *args/**kwargs, keyword-only (*), positional-only (/).

3. LEGB: L(ocal) -> E(nclosing) -> G(lobal) -> B(uilt-in).

4. Closures: funciones que capturan su entorno. __closure__ las guarda.

5. Factory functions: crean funciones parametrizadas en runtime.

6. Higher-order functions: map, filter, sorted(key=), callbacks.

7. partial: variantes pre-rellenadas. compose/pipe: encadenar funciones.

8. inspect: introspección de firmas, código fuente, tipos de callable.

9. Closure pitfall: en loops, capturan referencia. Usar i=i o factory.

10. Currying: f(a, b, c) -> f(a)(b)(c). Base teórica de partial.

11. NUNCA usar defaults mutables (lista=[]).  Usar lista=None.

TABLA DE PATRONES DE FUNCIONES:
╔═══════════════════════╦═══════════════════════════════════════╗
║ PATRÓN                ║ CASO DE USO                           ║
╠═══════════════════════╬═══════════════════════════════════════╣
║ Factory function      ║ Crear LR schedulers, loss functions   ║
║ Closure con estado    ║ Contadores, acumuladores, trackers    ║
║ partial()             ║ Variantes de optimizadores            ║
║ compose/pipe          ║ Pipelines de transformación           ║
║ Function registry     ║ Plugin systems, model registries      ║
║ Callback              ║ Training hooks, event handlers        ║
║ Currying              ║ Configuración progresiva              ║
║ Higher-order          ║ map, filter, sorted(key=)             ║
╚═══════════════════════╩═══════════════════════════════════════╝

Siguiente archivo: Decoradores profesionales.
"""

print("\n FIN DE ARCHIVO 01_funciones_scope_y_closures.")
print(" Las funciones como ciudadanos de primera clase han sido dominadas.")
