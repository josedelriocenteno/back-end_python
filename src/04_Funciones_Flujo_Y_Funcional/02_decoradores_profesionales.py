# ===========================================================================
# 02_decoradores_profesionales.py
# ===========================================================================
# MÓDULO 04: FUNCIONES, FLUJO Y PROGRAMACIÓN FUNCIONAL
# ARCHIVO 02: Decoradores desde Cero hasta Producción
# ===========================================================================
#
# OBJETIVO (1000+ LÍNEAS):
# Los decoradores son EL PATRÓN MÁS IMPORTANTE de Python para 
# código de producción. Entenderlos desde el mecanismo interno (closures +
# higher-order functions) hasta patrones avanzados: decoradores con 
# argumentos, decoradores de clase, stacking, functools.wraps,
# y aplicaciones reales en API ML/FastAPI.
#
# CONTENIDO:
#   1. Qué es un decorador (syntactic sugar para wrapper).
#   2. functools.wraps: preservar metadatos.
#   3. Decoradores con argumentos.
#   4. Decoradores de clase (__call__).
#   5. Stacking (composición de decoradores).
#   6. Decoradores para métodos de clase.
#   7. Aplicaciones: timing, retry, logging, caching, validation.
#   8. Ejercicio: decorador de rate limiting para APIs ML.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import time
import functools
import logging
from typing import Callable, Any, Optional
from collections import defaultdict


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 1: DECORADORES DESDE CERO                                     ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n" + "=" * 80)
print("=== CAPÍTULO 1: ¿QUÉ ES UN DECORADOR? ===")
print("=" * 80)

"""
Un decorador es syntactic sugar para:
    func = decorator(func)

Es decir, @decorator encima de una función es EXACTAMENTE lo mismo que:
    def func():
        ...
    func = decorator(func)

Un decorador es simplemente una FUNCIÓN que:
1. Recibe una función como argumento.
2. Define una función wrapper interna.
3. Retorna el wrapper.

El wrapper REEMPLAZA a la función original.
"""

print("\n--- Decorador sin @ (la forma explícita) ---")

def mi_decorador(func):
    """El decorador más simple: imprime antes y después."""
    def wrapper(*args, **kwargs):
        print(f"  ANTES de llamar a {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"  DESPUÉS de llamar a {func.__name__}")
        return resultado
    return wrapper

def saludar(nombre):
    print(f"  Hola, {nombre}!")
    return nombre

# Sin syntactic sugar:
saludar_decorada = mi_decorador(saludar)
saludar_decorada("Python")


print("\n--- El mismo decorador con @ ---")

@mi_decorador
def despedir(nombre):
    print(f"  Adiós, {nombre}!")
    return nombre

despedir("Python")


print("\n" + "=" * 80)
print("=== CAPÍTULO 2: FUNCTOOLS.WRAPS — PRESERVAR LA IDENTIDAD ===")
print("=" * 80)

"""
SIN @wraps, el wrapper REEMPLAZA los metadatos de la función:
- __name__ se pierde (es "wrapper" en vez del nombre original).
- __doc__ se pierde.
- __module__ se pierde.

@functools.wraps(func) copia estos metadatos del original al wrapper.
SIEMPRE usa @wraps en decoradores de producción.
"""

print("\n--- Sin @wraps: metadatos perdidos ---")

def decorador_sin_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorador_sin_wraps
def mi_func_a():
    """Docstring original de mi_func_a."""
    pass

print(f"  __name__: '{mi_func_a.__name__}'")  # 'wrapper' ¡mal!
print(f"  __doc__:  '{mi_func_a.__doc__}'")   # None ¡mal!


print("\n--- Con @wraps: metadatos preservados ---")

def decorador_con_wraps(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorador_con_wraps
def mi_func_b():
    """Docstring original de mi_func_b."""
    pass

print(f"  __name__: '{mi_func_b.__name__}'")  # 'mi_func_b' ✓
print(f"  __doc__:  '{mi_func_b.__doc__}'")   # Docstring original ✓
print(f"  __wrapped__: {mi_func_b.__wrapped__}")  # Referencia al original


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 2: DECORADORES PRÁCTICOS                                      ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 3: DECORADOR DE TIMING ===")
print("=" * 80)

"""
El decorador más útil en ML: medir cuánto tarda una función.
"""

def timer(func):
    """Mide y reporta el tiempo de ejecución."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        elapsed = time.perf_counter() - inicio
        print(f"  ⏱️  {func.__name__}() tardó {elapsed*1000:.2f} ms")
        return resultado
    return wrapper

@timer
def procesar_datos(n):
    """Simula procesamiento."""
    return sum(i**2 for i in range(n))

procesar_datos(100_000)
procesar_datos(1_000_000)


print("\n" + "=" * 80)
print("=== CAPÍTULO 4: DECORADOR DE RETRY ===")
print("=" * 80)

"""
Reintentar una función que puede fallar (ej: llamada a API, DB connection).
Este es un decorador CON ARGUMENTOS:
@retry(max_attempts=3, delay=1.0)
"""

print("\n--- Decorador con argumentos (3 niveles de funciones) ---")

def retry(max_attempts: int = 3, delay: float = 0.1, 
          exceptions: tuple = (Exception,)):
    """
    Decorador que reintenta la función si lanza una excepción.
    
    ESTRUCTURA (3 niveles):
    retry(args)           -> retorna decorador
      decorador(func)     -> retorna wrapper
        wrapper(*args)    -> ejecuta func con retries
    """
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"  ⚠️  {func.__name__} falló (intento {attempt}/"
                              f"{max_attempts}): {e}. Reintentando...")
                        time.sleep(delay)
                    else:
                        print(f"  ❌ {func.__name__} falló después de "
                              f"{max_attempts} intentos.")
                        raise last_exception
        return wrapper
    return decorador

import random

@retry(max_attempts=5, delay=0.01)
def llamar_api_inestable():
    """Simula una API que falla el 60% de las veces."""
    if random.random() < 0.6:
        raise ConnectionError("API timeout")
    return {"status": "ok", "data": [1, 2, 3]}

random.seed(42)
try:
    resultado = llamar_api_inestable()
    print(f"  ✅ Resultado: {resultado}")
except ConnectionError:
    print(f"  La API no respondió.")


print("\n" + "=" * 80)
print("=== CAPÍTULO 5: DECORADOR DE LOGGING ===")
print("=" * 80)

def log_calls(nivel: str = "INFO"):
    """Decorador que loguea cada llamada a la función."""
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args[:3]]  # Limitar
            kwargs_repr = [f"{k}={v!r}" for k, v in list(kwargs.items())[:3]]
            signature = ", ".join(args_repr + kwargs_repr)
            print(f"  [{nivel}] Llamando {func.__name__}({signature})")
            
            inicio = time.perf_counter()
            resultado = func(*args, **kwargs)
            elapsed = time.perf_counter() - inicio
            
            print(f"  [{nivel}] {func.__name__} retornó en {elapsed*1000:.1f}ms")
            return resultado
        return wrapper
    return decorador

@log_calls(nivel="DEBUG")
def procesar_batch(datos: list, batch_size: int = 32):
    return len(datos) // batch_size

procesar_batch(list(range(1000)), batch_size=64)


print("\n" + "=" * 80)
print("=== CAPÍTULO 6: DECORADOR DE VALIDACIÓN DE TIPOS ===")
print("=" * 80)

"""
Validar argumentos en runtime. Útil para APIs que reciben datos externos.
"""

def validar_tipos(**tipos_esperados):
    """Decorador que valida tipos de argumentos en runtime."""
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Mapear args posicionales a nombres de parámetros
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            for param_name, expected_type in tipos_esperados.items():
                if param_name in bound.arguments:
                    valor = bound.arguments[param_name]
                    if not isinstance(valor, expected_type):
                        raise TypeError(
                            f"'{param_name}' esperaba {expected_type.__name__}, "
                            f"recibió {type(valor).__name__}: {valor!r}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorador

@validar_tipos(lr=float, epochs=int)
def configurar_training(modelo: str, lr: float, epochs: int):
    return f"Config: {modelo}, lr={lr}, epochs={epochs}"

print(f"\n  {configurar_training('BERT', lr=0.001, epochs=10)}")

try:
    configurar_training("BERT", lr="not_a_float", epochs=10)
except TypeError as e:
    print(f"  ✅ Validación: {e}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                                                                        ║
# ║   PARTE 3: PATRONES AVANZADOS                                         ║
# ║                                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

print("\n\n" + "=" * 80)
print("=== CAPÍTULO 7: STACKING DE DECORADORES ===")
print("=" * 80)

"""
Puedes apilar múltiples decoradores. Se aplican de ABAJO hacia ARRIBA:

@decorador_a
@decorador_b
def func():
    ...

Equivale a: func = decorador_a(decorador_b(func))
El de abajo se aplica primero.
"""

print("\n--- Stacking: timer + log_calls ---")

@timer
@log_calls(nivel="INFO")
def entrenar_modelo_v2(datos, epochs=5):
    total = sum(d**2 for d in datos for _ in range(epochs))
    return total

entrenar_modelo_v2(list(range(100)), epochs=3)


print("\n" + "=" * 80)
print("=== CAPÍTULO 8: DECORADORES DE CLASE ===")
print("=" * 80)

"""
Un decorador puede ser una CLASE con __call__ en lugar de una función.
Ventaja: la clase tiene estado persistente entre llamadas.
"""

print("\n--- Decorador como clase: contador de llamadas ---")

class ContadorLlamadas:
    """Decorador que cuenta cuántas veces se llama una función."""
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        resultado = self.func(*args, **kwargs)
        return resultado
    
    def reset(self):
        self.count = 0

@ContadorLlamadas
def inferencia(texto):
    return f"Procesado: {texto[:20]}..."

for t in ["Hola mundo", "Machine learning", "Deep learning", "NLP avanzado"]:
    inferencia(t)

print(f"  inferencia fue llamada {inferencia.count} veces")
inferencia.reset()
print(f"  Tras reset: {inferencia.count} veces")


print("\n" + "=" * 80)
print("=== CAPÍTULO 9: DECORADOR CON CACHÉ Y TTL ===")
print("=" * 80)

"""
lru_cache no tiene TTL (Time To Live). A veces necesitas que 
los resultados cacheados EXPIREN después de un tiempo.
"""

def cache_con_ttl(ttl_seconds: float = 60.0, maxsize: int = 128):
    """Cache que expira entries después de ttl_seconds."""
    def decorador(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            ahora = time.time()
            
            if key in cache:
                resultado, timestamp = cache[key]
                if ahora - timestamp < ttl_seconds:
                    return resultado
                else:
                    del cache[key]
            
            # Evitar que la caché crezca sin límite
            if len(cache) >= maxsize:
                # Eliminar la entrada más antigua
                oldest_key = min(cache, key=lambda k: cache[k][1])
                del cache[oldest_key]
            
            resultado = func(*args, **kwargs)
            cache[key] = (resultado, ahora)
            return resultado
        
        wrapper.cache = cache
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorador

@cache_con_ttl(ttl_seconds=0.1)  # TTL de 100ms
def embedding_costoso(texto: str) -> list:
    """Simula un cómputo costoso de embedding."""
    time.sleep(0.01)
    return [hash(texto) % 100 / 100]

# Primera llamada: computa
t1 = time.perf_counter()
embedding_costoso("hola mundo")
print(f"  1ª llamada: {(time.perf_counter()-t1)*1000:.1f}ms")

# Segunda llamada: cache hit
t1 = time.perf_counter()
embedding_costoso("hola mundo")
print(f"  2ª llamada: {(time.perf_counter()-t1)*1000:.1f}ms (cache hit)")

# Esperar a que expire
time.sleep(0.11)
t1 = time.perf_counter()
embedding_costoso("hola mundo")
print(f"  3ª llamada: {(time.perf_counter()-t1)*1000:.1f}ms (cache expiró)")


print("\n" + "=" * 80)
print("=== CAPÍTULO 10: DECORADOR SINGLEDISPATCH ===")
print("=" * 80)

"""
@functools.singledispatch permite crear funciones que se comportan
diferente según el TIPO del primer argumento. Polimorfismo funcional.
"""

from functools import singledispatch

@singledispatch
def procesar(dato):
    """Procesa un dato según su tipo."""
    raise TypeError(f"Tipo no soportado: {type(dato)}")

@procesar.register(str)
def _(dato):
    return f"Texto procesado: '{dato.upper()}'"

@procesar.register(list)
def _(dato):
    return f"Lista de {len(dato)} elementos"

@procesar.register(int)
def _(dato):
    return f"Entero: {dato * 2}"

@procesar.register(float)
def _(dato):
    return f"Float: {dato:.4f}"

for d in ["hola", [1, 2, 3], 42, 3.14]:
    print(f"  procesar({d!r}) -> {procesar(d)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 11: EJERCICIO — RATE LIMITER PARA API ML ===")
print("=" * 80)

"""
Construir un decorador que limita la tasa de llamadas a una función.
Útil para: llamadas a APIs de OpenAI, Anthropic, etc.
"""

print("\n--- Rate Limiter decorador ---")

def rate_limit(max_calls: int, period: float = 1.0):
    """
    Limita a max_calls llamadas por periodo (en segundos).
    Si se excede, espera hasta que se libere un slot.
    """
    def decorador(func):
        timestamps = []
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ahora = time.time()
            
            # Limpiar timestamps fuera del periodo
            while timestamps and ahora - timestamps[0] > period:
                timestamps.pop(0)
            
            if len(timestamps) >= max_calls:
                # Esperar hasta que se libere un slot
                wait_time = period - (ahora - timestamps[0])
                if wait_time > 0:
                    print(f"  ⏳ Rate limit alcanzado. Esperando {wait_time:.2f}s...")
                    time.sleep(wait_time)
                timestamps.pop(0)
            
            timestamps.append(time.time())
            return func(*args, **kwargs)
        
        wrapper.reset = lambda: timestamps.clear()
        return wrapper
    return decorador

@rate_limit(max_calls=3, period=0.5)
def llamar_openai(prompt: str) -> str:
    return f"Respuesta a: '{prompt[:30]}...'"

print("Llamadas con rate limiting (3 por 0.5s):")
for i in range(5):
    inicio = time.perf_counter()
    resp = llamar_openai(f"Pregunta {i+1}: ¿Qué es machine learning?")
    elapsed = time.perf_counter() - inicio
    print(f"  [{i+1}] {resp} ({elapsed*1000:.0f}ms)")


print("\n" + "=" * 80)
print("=== CAPÍTULO 12: DECORADORES PARA MÉTODOS DE CLASE ===")
print("=" * 80)

"""
Tres decoradores built-in para métodos:
- @staticmethod: no recibe self ni cls. Es como una función normal en la clase.
- @classmethod: recibe cls (la clase) en lugar de self.
- @property: convierte un método en un atributo calculado.
"""

print("\n--- staticmethod, classmethod, property ---")

class MLModel:
    """Ejemplo de uso de decoradores de método."""
    
    _instancias = 0
    
    def __init__(self, nombre: str, version: str = "1.0"):
        self.nombre = nombre
        self.version = version
        self._params = {}
        MLModel._instancias += 1
    
    @staticmethod
    def validar_nombre(nombre: str) -> bool:
        """No necesita self ni cls. Función utilitaria."""
        return bool(nombre) and nombre.isidentifier()
    
    @classmethod
    def desde_config(cls, config: dict):
        """Crea una instancia desde un diccionario de configuración."""
        return cls(nombre=config["nombre"], version=config.get("version", "1.0"))
    
    @classmethod
    def total_instancias(cls):
        return cls._instancias
    
    @property
    def nombre_completo(self):
        """Atributo calculado: parece un atributo, es un método."""
        return f"{self.nombre}_v{self.version}"
    
    @property
    def num_params(self):
        return len(self._params)

# Uso
print(f"  Nombre válido: {MLModel.validar_nombre('bert_base')}")
print(f"  Nombre inválido: {MLModel.validar_nombre('123-bad')}")

modelo = MLModel.desde_config({"nombre": "gpt", "version": "3.5"})
print(f"  Desde config: {modelo.nombre_completo}")
print(f"  Total instancias: {MLModel.total_instancias()}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 13: DECORADOR DE DEPRECACIÓN ===")
print("=" * 80)

"""
Marcar funciones como deprecated para que emitan warnings.
Patrón muy usado en librerías que evolucionan (scikit-learn, pandas).
"""

import warnings

def deprecated(razon: str = "", version: str = ""):
    """Decorador que marca una función como deprecated."""
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            msg = f"'{func.__name__}' está deprecated"
            if version:
                msg += f" desde v{version}"
            if razon:
                msg += f". {razon}"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        wrapper._deprecated = True
        wrapper._deprecated_msg = razon
        return wrapper
    return decorador

@deprecated(razon="Usa 'entrenar_v2' en su lugar", version="2.0")
def entrenar_v1(datos, epochs=5):
    return f"Entrenado con {len(datos)} datos"

# Capturar el warning en vez de mostrarlo
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    entrenar_v1([1, 2, 3])
    if w:
        print(f"  Warning: {w[0].message}")
        print(f"  Categoría: {w[0].category.__name__}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 14: DECORADOR FLEXIBLE (CON O SIN ARGUMENTOS) ===")
print("=" * 80)

"""
A veces necesitas un decorador que funcione TANTO con como sin args:
@mi_deco         -> sin argumentos
@mi_deco(arg=1)  -> con argumentos

Truco: si el primer argumento es callable, es sin paréntesis.
"""

def flexible_decorator(_func=None, *, nivel="INFO"):
    """
    Funciona con y sin argumentos:
    @flexible_decorator
    @flexible_decorator(nivel="DEBUG")
    """
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  [{nivel}] -> {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    
    if _func is not None:
        # Llamado sin argumentos: @flexible_decorator
        return decorador(_func)
    # Llamado con argumentos: @flexible_decorator(nivel="DEBUG")
    return decorador

@flexible_decorator
def func_a():
    return "A"

@flexible_decorator(nivel="DEBUG")
def func_b():
    return "B"

print(f"  func_a: {func_a()}")
print(f"  func_b: {func_b()}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 15: DECORADOR DE PROFILING (MEMORIA + TIEMPO) ===")
print("=" * 80)

"""
Combinar timing con medición de memoria para profiling completo.
"""

import tracemalloc

def profile(func):
    """Decorador que mide tiempo y memoria de una función."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        inicio = time.perf_counter()
        
        resultado = func(*args, **kwargs)
        
        elapsed = time.perf_counter() - inicio
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"  📊 {func.__name__}():")
        print(f"     Tiempo: {elapsed*1000:.2f} ms")
        print(f"     Memoria actual: {current/1024:.1f} KB")
        print(f"     Memoria pico:   {peak/1024:.1f} KB")
        
        return resultado
    return wrapper

@profile
def crear_lista_grande(n):
    return [i**2 for i in range(n)]

crear_lista_grande(100_000)


print("\n" + "=" * 80)
print("=== CAPÍTULO 16: DECORADOR CONDICIONAL ===")
print("=" * 80)

"""
Aplicar un decorador solo si se cumple una condición.
Útil para: desactivar logging en producción, desactivar profiling, etc.
"""

def condicional(condicion: bool, decorador):
    """
    Aplica el decorador solo si la condición es True.
    Uso: @condicional(DEBUG, timer)
    """
    def wrapper(func):
        if condicion:
            return decorador(func)
        return func
    return wrapper

DEBUG = True

@condicional(DEBUG, timer)
def proceso_debug(n):
    return sum(range(n))

@condicional(not DEBUG, timer)  # NO se aplica porque DEBUG=True
def proceso_prod(n):
    return sum(range(n))

print(f"\n  Con timer: {proceso_debug(100_000)}")
print(f"  Sin timer: {proceso_prod(100_000)}")


print("\n" + "=" * 80)
print("=== CAPÍTULO 17: EJERCICIO — MIDDLEWARE CHAIN PARA PIPELINE ML ===")
print("=" * 80)

"""
Construir un sistema de middleware donde cada decorador es un paso
del pipeline de inferencia: validar input, preprocesar, inferir,
postprocesar, cachear.
"""

print("\n--- Middleware chain ---")

def middleware_validar(func):
    """Middleware: valida que el input sea no vacío."""
    @functools.wraps(func)
    def wrapper(texto, **kwargs):
        if not texto or not texto.strip():
            return {"error": "Input vacío", "resultado": None}
        return func(texto.strip(), **kwargs)
    return wrapper

def middleware_preprocesar(func):
    """Middleware: preprocesa el texto (lowercase, strip)."""
    @functools.wraps(func)
    def wrapper(texto, **kwargs):
        texto_limpio = texto.lower().strip()
        kwargs["texto_original"] = texto
        return func(texto_limpio, **kwargs)
    return wrapper

def middleware_log(func):
    """Middleware: loguea la inferencia."""
    @functools.wraps(func)
    def wrapper(texto, **kwargs):
        print(f"    [LOG] Infiriendo sobre: '{texto[:50]}'")
        resultado = func(texto, **kwargs)
        print(f"    [LOG] Resultado: {resultado.get('label', 'N/A')}")
        return resultado
    return wrapper

@middleware_validar
@middleware_preprocesar
@middleware_log
def clasificar_sentimiento(texto, **kwargs):
    """Simula clasificación de sentimiento."""
    palabras_positivas = {"bueno", "excelente", "genial", "bien", "mejor"}
    palabras_negativas = {"malo", "terrible", "peor", "horrible", "error"}
    
    tokens = set(texto.split())
    pos = len(tokens & palabras_positivas)
    neg = len(tokens & palabras_negativas)
    
    if pos > neg:
        label, score = "positivo", 0.7 + pos * 0.1
    elif neg > pos:
        label, score = "negativo", 0.7 + neg * 0.1
    else:
        label, score = "neutro", 0.5
    
    return {"label": label, "score": min(score, 1.0), 
            "original": kwargs.get("texto_original", texto)}

# Probar el pipeline
textos_test = [
    "  Este producto es EXCELENTE y genial  ",
    " Terrible experiencia, horrible ",
    "  ",  # Vacío -> validación lo captura
    " Un producto normal ",
]

print("Pipeline de inferencia con middlewares:")
for texto in textos_test:
    resultado = clasificar_sentimiento(texto)
    print(f"  Input: '{texto.strip()[:30]}' -> {resultado}")
    print()


print("\n" + "=" * 80)
print("=== CAPITULO 18: DECORADOR DE SCHEMA VALIDATION ===")
print("=" * 80)

"""
Validar que los inputs y outputs de una funcion cumplan un schema.
Patron comun en APIs ML donde los datos deben tener forma especifica.
"""

def validate_schema(input_schema: dict = None, output_schema: dict = None):
    """
    Decorador que valida schema de input/output.
    input_schema: {nombre_param: tipo_esperado}
    output_schema: tipo esperado del return
    """
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Validar inputs
            if input_schema:
                import inspect
                sig = inspect.signature(func)
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()

                for param, expected in input_schema.items():
                    if param in bound.arguments:
                        val = bound.arguments[param]
                        if not isinstance(val, expected):
                            raise ValueError(
                                f"Input '{param}': esperaba {expected.__name__}, "
                                f"recibio {type(val).__name__}"
                            )

            resultado = func(*args, **kwargs)

            # Validar output
            if output_schema and not isinstance(resultado, output_schema):
                raise ValueError(
                    f"Output: esperaba {output_schema.__name__}, "
                    f"recibio {type(resultado).__name__}"
                )

            return resultado
        return wrapper
    return decorador

@validate_schema(
    input_schema={"texto": str, "max_length": int},
    output_schema=dict
)
def analizar_texto(texto: str, max_length: int = 512) -> dict:
    tokens = texto.split()[:max_length]
    return {"n_tokens": len(tokens), "preview": " ".join(tokens[:5])}

print("\n--- Schema validation ---")
result = analizar_texto("Hola mundo esto es una prueba de validacion", max_length=10)
print(f"  Resultado valido: {result}")

try:
    analizar_texto(12345)  # No es string
except ValueError as e:
    print(f"  Error capturado: {e}")


print("\n" + "=" * 80)
print("=== CAPITULO 19: COMPOSE DECORATORS HELPER ===")
print("=" * 80)

"""
Funcion helper para componer multiples decoradores en uno solo.
En vez de apilar 5 @decoradores, creas uno compuesto.
"""

def compose_decorators(*decorators):
    """
    Compone multiples decoradores en uno solo.
    compose_decorators(a, b, c) equivale a @a @b @c
    """
    def composed(func):
        for deco in reversed(decorators):
            func = deco(func)
        return func
    return composed

# Crear un decorador compuesto para funciones de produccion
production_ready = compose_decorators(
    timer,
    ContadorLlamadas,
)

@production_ready
def predecir_produccion(datos):
    """Prediccion lista para produccion."""
    return [d * 2 for d in datos]

print("\n--- Decorador compuesto ---")
predecir_produccion([1, 2, 3])
predecir_produccion([4, 5, 6])
print(f"  Llamadas totales: {predecir_produccion.count}")


print("\n" + "=" * 80)
print("=== CAPITULO 20: SIMULACION DE ROUTE DECORATOR (FASTAPI-STYLE) ===")
print("=" * 80)

"""
FastAPI usa decoradores masivamente para definir endpoints:
@app.get("/predict")
async def predict(data: Input) -> Output: ...

Vamos a simular este patron para entender como funciona internamente.
"""

print("\n--- Mini framework de routing con decoradores ---")

class MiniAPI:
    """Simulacion simplificada de un framework web con decoradores."""

    def __init__(self, nombre: str = "api"):
        self.nombre = nombre
        self.routes = {}
        self.middleware_stack = []

    def route(self, path: str, method: str = "GET"):
        """Decorador que registra un endpoint."""
        def decorador(func):
            key = f"{method} {path}"
            self.routes[key] = {
                "handler": func,
                "path": path,
                "method": method,
                "name": func.__name__,
                "doc": func.__doc__ or "",
            }
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorador

    def get(self, path: str):
        """Shorthand para @route(path, "GET")."""
        return self.route(path, "GET")

    def post(self, path: str):
        """Shorthand para @route(path, "POST")."""
        return self.route(path, "POST")

    def handle_request(self, method: str, path: str, **kwargs):
        """Simula el manejo de una request."""
        key = f"{method} {path}"
        if key not in self.routes:
            return {"status": 404, "error": f"Ruta no encontrada: {key}"}

        handler = self.routes[key]["handler"]
        try:
            result = handler(**kwargs)
            return {"status": 200, "data": result}
        except Exception as e:
            return {"status": 500, "error": str(e)}

    def listar_rutas(self):
        """Lista todas las rutas registradas."""
        for key, info in self.routes.items():
            print(f"  {key} -> {info['name']}(): {info['doc'][:50]}")

# Crear la API
app = MiniAPI("ml-api")

@app.get("/health")
def health_check():
    """Verifica que la API esta activa."""
    return {"status": "healthy", "version": "1.0"}

@app.post("/predict")
def predict(texto: str = "", modelo: str = "bert"):
    """Endpoint de prediccion de sentimiento."""
    # Simulacion
    score = len(texto) % 10 / 10
    label = "positivo" if score > 0.5 else "negativo"
    return {"modelo": modelo, "label": label, "score": score}

@app.get("/models")
def list_models():
    """Lista modelos disponibles."""
    return ["bert-base", "gpt-2", "t5-small", "roberta-large"]

# Probar la API
print("Rutas registradas:")
app.listar_rutas()

print("\nSimulando requests:")
r1 = app.handle_request("GET", "/health")
print(f"  GET /health -> {r1}")

r2 = app.handle_request("POST", "/predict", texto="Excelente producto", modelo="bert")
print(f"  POST /predict -> {r2}")

r3 = app.handle_request("GET", "/models")
print(f"  GET /models -> {r3}")

r4 = app.handle_request("GET", "/no-existe")
print(f"  GET /no-existe -> {r4}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE DECORADORES PARA INGENIERIA IA:

1. Un decorador es syntactic sugar: @deco sobre func = func = deco(func).

2. SIEMPRE usar @functools.wraps(func) en el wrapper.

3. Decorador con argumentos = 3 niveles de funciones:
   exterior(args) -> decorador(func) -> wrapper(*args)

4. Decoradores practicos de produccion:
   - @timer: medir latencia de inferencia.
   - @retry: reintentar llamadas a APIs/DBs.
   - @log_calls: trazabilidad de pipelines.
   - @validar_tipos: validar inputs en runtime.
   - @cache_con_ttl: cache con expiracion.
   - @rate_limit: limitar calls a APIs externas.
   - @deprecated: marcar funciones obsoletas.
   - @profile: medir tiempo + memoria.
   - @validate_schema: validar inputs/outputs.

5. Decoradores de clase: __call__, con estado persistente.

6. Decorador flexible: funciona con y sin argumentos (_func=None).

7. Decorador condicional: aplicar solo si condicion es True.

8. singledispatch: polimorfismo basado en tipo del primer arg.

9. Stacking y compose_decorators: componer multiples decoradores.

10. Route decorators: base de FastAPI, Flask, Django REST.

11. Middleware chain: decoradores como pasos de un pipeline.

Siguiente archivo: Generadores e Itertools.
"""

print("\n FIN DE ARCHIVO 02_decoradores_profesionales.")
print(" Los decoradores han sido dominados de cero a produccion.")
