# ===========================================================================
# 01_excepciones_y_manejo_errores.py
# ===========================================================================
# MODULO 06: ERRORES, TESTING Y ROBUSTEZ
# ARCHIVO 01: Excepciones, Manejo de Errores y Context Managers
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar el sistema de excepciones de Python: jerarquia, excepciones
# custom, patrones de manejo, context managers, y codigo robusto para
# pipelines de ML en produccion.
#
# CONTENIDO:
#   1. Jerarquia de excepciones de Python.
#   2. try/except/else/finally — flujo completo.
#   3. Excepciones custom para ML.
#   4. Patrones: EAFP vs LBYL.
#   5. Context managers: __enter__/__exit__ y contextlib.
#   6. Exception chaining y __cause__.
#   7. Warnings: alertar sin romper.
#   8. Ejercicio: pipeline robusto con error handling.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import sys
import os
import time
import traceback
import warnings
from contextlib import contextmanager, suppress
from dataclasses import dataclass, field
from typing import Optional, Any


# =====================================================================
#   PARTE 1: JERARQUIA DE EXCEPCIONES
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: JERARQUIA DE EXCEPCIONES DE PYTHON ===")
print("=" * 80)

"""
BaseException
├── SystemExit          # sys.exit()
├── KeyboardInterrupt   # Ctrl+C
├── GeneratorExit       # generator.close()
└── Exception           # TODAS las excepciones normales
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── OSError (IOError)
    │   └── FileNotFoundError
    ├── ValueError
    ├── TypeError
    ├── AttributeError
    ├── RuntimeError
    │   └── RecursionError
    ├── StopIteration
    └── ...

REGLA: NUNCA capturar BaseException. Capturar Exception o mas especifico.
"""

print("\n--- Explorando la jerarquia ---")

excepciones_comunes = [
    ValueError, TypeError, KeyError, IndexError,
    FileNotFoundError, AttributeError, RuntimeError,
    ZeroDivisionError, StopIteration, OverflowError,
]

for exc in excepciones_comunes:
    mro = [c.__name__ for c in exc.__mro__]
    print(f"  {exc.__name__}: {' -> '.join(mro)}")


print("\n" + "=" * 80)
print("=== CAPITULO 2: TRY/EXCEPT/ELSE/FINALLY ===")
print("=" * 80)

"""
try:
    # Codigo que puede fallar
except TipoError as e:
    # Manejar el error
else:
    # Se ejecuta SOLO si NO hubo excepcion
finally:
    # Se ejecuta SIEMPRE (con o sin excepcion)

REGLA: el bloque 'else' es para codigo que depende del exito de 'try'
pero que NO quieres proteger con except.
"""

print("\n--- Flujo completo ---")

def dividir_seguro(a, b):
    """Ejemplo de try/except/else/finally."""
    try:
        resultado = a / b
    except ZeroDivisionError:
        print(f"    except: Division por cero ({a}/{b})")
        return None
    except TypeError as e:
        print(f"    except: Tipo incorrecto: {e}")
        return None
    else:
        print(f"    else: {a}/{b} = {resultado:.4f}")
        return resultado
    finally:
        print(f"    finally: siempre se ejecuta")

dividir_seguro(10, 3)
dividir_seguro(10, 0)
dividir_seguro("a", 3)


print("\n--- Multiples except ---")

def procesar_dato(dato):
    """Manejar diferentes tipos de error."""
    try:
        valor = int(dato)
        resultado = 100 / valor
        return resultado
    except ValueError:
        print(f"    '{dato}' no es un numero valido")
    except ZeroDivisionError:
        print(f"    '{dato}' produce division por cero")
    except (TypeError, AttributeError) as e:
        print(f"    Error de tipo: {e}")
    return None

procesar_dato("42")
procesar_dato("abc")
procesar_dato("0")
procesar_dato(None)


print("\n--- Capturar y re-lanzar ---")

def cargar_modelo(path: str):
    """Captura, agrega contexto y re-lanza."""
    try:
        # Simula lectura de archivo
        if not path.endswith(".pt"):
            raise ValueError(f"Formato no soportado: {path}")
        if "corrupto" in path:
            raise RuntimeError("Archivo corrupto")
        return {"modelo": "loaded", "path": path}
    except ValueError:
        raise  # Re-lanza sin modificar
    except RuntimeError as e:
        # Agrega contexto y re-lanza
        raise RuntimeError(f"Error cargando modelo '{path}': {e}") from e

try:
    cargar_modelo("modelo.onnx")
except ValueError as e:
    print(f"  Capturado ValueError: {e}")

try:
    cargar_modelo("corrupto.pt")
except RuntimeError as e:
    print(f"  Capturado RuntimeError: {e}")


# =====================================================================
#   PARTE 2: EXCEPCIONES CUSTOM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: EXCEPCIONES CUSTOM PARA ML ===")
print("=" * 80)

"""
Crear excepciones propias para dominios especificos.
REGLAS:
1. SIEMPRE heredar de Exception (o subclase).
2. Nombrar con sufijo Error o Exception.
3. Incluir informacion util como atributos.
4. Organizar en jerarquia si hay muchas.
"""

print("\n--- Jerarquia de excepciones ML ---")

class MLError(Exception):
    """Base para todas las excepciones de ML."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.details = details or {}

class DataError(MLError):
    """Errores relacionados con datos."""
    pass

class DataValidationError(DataError):
    """Los datos no pasan validacion."""
    def __init__(self, message: str, invalid_rows: list = None):
        super().__init__(message, {"invalid_rows": invalid_rows or []})
        self.invalid_rows = invalid_rows or []

class DataNotFoundError(DataError):
    """Dataset no encontrado."""
    def __init__(self, dataset_name: str):
        super().__init__(f"Dataset '{dataset_name}' no encontrado")
        self.dataset_name = dataset_name

class ModelError(MLError):
    """Errores relacionados con modelos."""
    pass

class ModelNotTrainedError(ModelError):
    """Modelo no entrenado."""
    def __init__(self, model_name: str):
        super().__init__(f"Modelo '{model_name}' no esta entrenado")
        self.model_name = model_name

class InferenceError(ModelError):
    """Error durante inferencia."""
    def __init__(self, message: str, input_data: Any = None):
        super().__init__(message, {"input_data": str(input_data)[:100]})
        self.input_data = input_data

class PipelineError(MLError):
    """Errores en el pipeline."""
    def __init__(self, step: str, message: str, cause: Exception = None):
        super().__init__(f"[{step}] {message}")
        self.step = step
        self.cause = cause

# Uso
print("  Jerarquia:")
for exc in [MLError, DataError, DataValidationError, ModelError, 
            ModelNotTrainedError, InferenceError, PipelineError]:
    depth = len(exc.__mro__) - len(Exception.__mro__)
    indent = "  " * depth
    print(f"    {indent}{exc.__name__}")

# Probar excepciones custom
try:
    raise DataValidationError(
        "5 filas con NaN en columna 'price'",
        invalid_rows=[10, 23, 45, 67, 89]
    )
except DataError as e:
    print(f"\n  Capturado DataError: {e}")
    print(f"  Filas invalidas: {e.invalid_rows}")
    print(f"  Es MLError: {isinstance(e, MLError)}")


print("\n--- Excepciones como control de flujo ---")

class RetryableError(MLError):
    """Error que se puede reintentar."""
    def __init__(self, message: str, max_retries: int = 3):
        super().__init__(message)
        self.max_retries = max_retries

class NonRetryableError(MLError):
    """Error fatal, no reintentar."""
    pass

def llamar_api_ml(query: str, intento: int = 0):
    """Simula una llamada a API que puede fallar."""
    import random
    random.seed(intento)
    r = random.random()
    
    if r < 0.3:
        raise RetryableError("API timeout", max_retries=3)
    elif r < 0.4:
        raise NonRetryableError("API key invalida")
    return {"resultado": f"respuesta_{intento}"}

def llamar_con_retry(query: str, max_retries: int = 3):
    """Patron retry con excepciones custom."""
    for intento in range(max_retries):
        try:
            return llamar_api_ml(query, intento)
        except RetryableError as e:
            print(f"    Intento {intento+1}/{max_retries}: {e}")
            if intento == max_retries - 1:
                raise
            time.sleep(0.01)  # Backoff simulado
        except NonRetryableError:
            raise  # No reintentar

try:
    resultado = llamar_con_retry("test query")
    print(f"  Resultado: {resultado}")
except RetryableError:
    print("  Todos los reintentos fallaron")
except NonRetryableError as e:
    print(f"  Error fatal: {e}")


# =====================================================================
#   PARTE 3: EAFP VS LBYL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: EAFP VS LBYL ===")
print("=" * 80)

"""
LBYL: Look Before You Leap (Java style)
  if key in dict:
      value = dict[key]

EAFP: Easier to Ask Forgiveness than Permission (Python style)
  try:
      value = dict[key]
  except KeyError:
      ...

Python PREFIERE EAFP. Es mas rapido cuando el caso comun es exitoso.
EAFP es thread-safe; LBYL puede tener race conditions.
"""

print("\n--- LBYL vs EAFP ---")

config = {"lr": 0.001, "epochs": 10, "batch_size": 32}

# LBYL
if "modelo" in config:
    modelo = config["modelo"]
else:
    modelo = "default"
print(f"  LBYL: modelo = '{modelo}'")

# EAFP (Pythonic)
try:
    modelo = config["modelo"]
except KeyError:
    modelo = "default"
print(f"  EAFP: modelo = '{modelo}'")

# Aun mejor: usar .get()
modelo = config.get("modelo", "default")
print(f"  .get(): modelo = '{modelo}'")


print("\n--- EAFP para atributos ---")

class ModeloSimple:
    pass

ms = ModeloSimple()

# LBYL
if hasattr(ms, 'predict'):
    ms.predict([1, 2, 3])
else:
    print("  LBYL: No tiene predict")

# EAFP
try:
    ms.predict([1, 2, 3])
except AttributeError:
    print("  EAFP: No tiene predict")


# =====================================================================
#   PARTE 4: CONTEXT MANAGERS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: CONTEXT MANAGERS PROFESIONALES ===")
print("=" * 80)

"""
Context managers garantizan cleanup (liberacion de recursos)
incluso si hay excepciones.

Dos formas de crear:
1. Clase con __enter__/__exit__
2. Generador con @contextmanager
"""

print("\n--- Context manager clase ---")

class Timer:
    """Mide el tiempo de un bloque."""
    
    def __init__(self, nombre: str = "bloque"):
        self.nombre = nombre
        self.elapsed = 0
    
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"  [{self.nombre}] {self.elapsed*1000:.2f} ms")
        return False  # No suprime excepciones

with Timer("suma") as t:
    total = sum(range(1_000_000))
print(f"  Resultado: {total}, tiempo guardado: {t.elapsed*1000:.2f} ms")


print("\n--- Context manager generador ---")

@contextmanager
def gpu_context(device: str = "cuda:0"):
    """Simula asignar/liberar GPU."""
    print(f"  Asignando GPU {device}...")
    memoria_usada = 0
    try:
        yield device
        memoria_usada = 4096  # MB simulados
    except Exception as e:
        print(f"  Error en GPU: {e}")
        raise
    finally:
        print(f"  Liberando GPU {device} ({memoria_usada} MB)")

with gpu_context("cuda:0") as gpu:
    print(f"  Usando {gpu} para inferencia")


print("\n--- Context manager que suprime excepciones ---")

# suppress() de contextlib
with suppress(FileNotFoundError):
    # Si el archivo no existe, no pasa nada
    with open("/tmp/no_existe_abc123.txt") as f:
        data = f.read()
    print("  Esto no se imprime si el archivo no existe")

print("  Ejecucion continua despues de suppress()")


print("\n--- Multiples context managers ---")

@contextmanager
def db_connection(nombre: str):
    print(f"    Conectando a DB '{nombre}'...")
    yield {"db": nombre, "connected": True}
    print(f"    Desconectando de DB '{nombre}'")

@contextmanager
def transaction():
    print(f"    Iniciando transaccion...")
    try:
        yield
        print(f"    COMMIT")
    except Exception:
        print(f"    ROLLBACK")
        raise

# Anidar context managers
with db_connection("experiments") as db:
    with transaction():
        print(f"    Insertando en {db['db']}...")


print("\n--- Context manager reentrant ---")

class ModelPool:
    """Pool de modelos con context manager."""
    
    def __init__(self, modelos: list):
        self._modelos = modelos
        self._disponibles = list(modelos)
        self._en_uso = []
    
    @contextmanager
    def acquire(self):
        if not self._disponibles:
            raise RuntimeError("No hay modelos disponibles")
        modelo = self._disponibles.pop()
        self._en_uso.append(modelo)
        try:
            yield modelo
        finally:
            self._en_uso.remove(modelo)
            self._disponibles.append(modelo)
    
    def __repr__(self):
        return f"Pool(disp={len(self._disponibles)}, uso={len(self._en_uso)})"

pool = ModelPool(["bert-1", "bert-2", "bert-3"])
print(f"\n  {pool}")

with pool.acquire() as m1:
    print(f"  Usando: {m1}, {pool}")
    with pool.acquire() as m2:
        print(f"  Usando: {m1}, {m2}, {pool}")

print(f"  Tras liberar: {pool}")


# =====================================================================
#   PARTE 5: EXCEPTION CHAINING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: EXCEPTION CHAINING ===")
print("=" * 80)

"""
Python soporta exception chaining:
- raise X from Y: explicito (Y es __cause__)
- raise X dentro de except: implicito (__context__)

Permite rastrear la cadena completa de errores.
"""

print("\n--- raise from (chaining explicito) ---")

def cargar_config(path: str) -> dict:
    try:
        # Simula error de lectura
        raise FileNotFoundError(f"No existe: {path}")
    except FileNotFoundError as e:
        raise PipelineError("config", "No se pudo cargar configuracion") from e

try:
    cargar_config("/etc/ml/config.yaml")
except PipelineError as e:
    print(f"  Error: {e}")
    print(f"  Causa: {e.__cause__}")
    print(f"  Cadena: {type(e).__name__} <- {type(e.__cause__).__name__}")


print("\n--- Formatear traceback ---")

def funcion_c():
    raise ValueError("dato corrupto")

def funcion_b():
    try:
        funcion_c()
    except ValueError as e:
        raise RuntimeError("pipeline fallo") from e

def funcion_a():
    try:
        funcion_b()
    except RuntimeError:
        # Obtener traceback como string
        tb = traceback.format_exc()
        print("  Traceback capturado:")
        for line in tb.strip().split("\n")[-4:]:
            print(f"    {line}")

funcion_a()


# =====================================================================
#   PARTE 6: WARNINGS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: WARNINGS — ALERTAR SIN ROMPER ===")
print("=" * 80)

"""
warnings.warn() emite advertencias SIN detener la ejecucion.
Categorias: DeprecationWarning, FutureWarning, UserWarning, etc.

EN ML: avisar de APIs deprecadas, configuraciones suboptimas, etc.
"""

print("\n--- Warnings basicos ---")

def entrenar_modelo(lr: float, epochs: int):
    if lr > 0.1:
        warnings.warn(
            f"lr={lr} es muy alto, puede causar divergencia",
            UserWarning,
            stacklevel=2
        )
    if epochs < 3:
        warnings.warn(
            f"epochs={epochs} es muy bajo para convergencia",
            UserWarning,
            stacklevel=2
        )
    return {"lr": lr, "epochs": epochs, "status": "ok"}

# Capturar warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    entrenar_modelo(0.5, 2)
    
    print(f"  Warnings capturados: {len(w)}")
    for warning in w:
        print(f"    {warning.category.__name__}: {warning.message}")


print("\n--- DeprecationWarning ---")

def api_antigua(datos):
    """API deprecada."""
    warnings.warn(
        "api_antigua() sera removida en v3.0. Usar api_nueva() en su lugar.",
        DeprecationWarning,
        stacklevel=2
    )
    return api_nueva(datos)

def api_nueva(datos):
    return {"procesado": True, "n": len(datos)}

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    resultado = api_antigua([1, 2, 3])
    if w:
        print(f"  {w[0].category.__name__}: {w[0].message}")
    print(f"  Resultado: {resultado}")


# =====================================================================
#   PARTE 7: PATRONES DE ERROR HANDLING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: PATRONES DE ERROR HANDLING ===")
print("=" * 80)

"""
Patrones profesionales para manejar errores en produccion.
"""

print("\n--- Patron: Result type (evitar excepciones) ---")

@dataclass
class Result:
    """Tipo Result: exito o error sin excepciones."""
    success: bool
    value: Any = None
    error: str = None
    
    @classmethod
    def ok(cls, value):
        return cls(success=True, value=value)
    
    @classmethod
    def fail(cls, error: str):
        return cls(success=False, error=error)
    
    def unwrap(self):
        if self.success:
            return self.value
        raise RuntimeError(f"Unwrap en error: {self.error}")

def procesar_input(texto: str) -> Result:
    if not texto:
        return Result.fail("Texto vacio")
    if len(texto) > 1000:
        return Result.fail(f"Texto muy largo: {len(texto)} chars")
    tokens = texto.split()
    return Result.ok({"tokens": tokens, "n": len(tokens)})

for texto in ["Hola mundo", "", "x" * 2000]:
    r = procesar_input(texto)
    if r.success:
        print(f"  OK: {r.value}")
    else:
        print(f"  ERROR: {r.error}")


print("\n--- Patron: Error accumulator ---")

class ErrorAccumulator:
    """Acumula errores sin detener la ejecucion."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def add_error(self, msg: str, field: str = None):
        self.errors.append({"msg": msg, "field": field})
    
    def add_warning(self, msg: str):
        self.warnings.append(msg)
    
    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0
    
    def raise_if_errors(self):
        if self.has_errors:
            msgs = [e["msg"] for e in self.errors]
            raise DataValidationError(
                f"{len(self.errors)} errores de validacion",
                invalid_rows=msgs
            )
    
    def summary(self) -> str:
        return f"Errors: {len(self.errors)}, Warnings: {len(self.warnings)}"

def validar_dataset(datos: list[dict]) -> ErrorAccumulator:
    acc = ErrorAccumulator()
    
    for i, row in enumerate(datos):
        if "features" not in row:
            acc.add_error(f"Fila {i}: falta 'features'", field="features")
        if "label" not in row:
            acc.add_error(f"Fila {i}: falta 'label'", field="label")
        elif row["label"] not in (0, 1):
            acc.add_warning(f"Fila {i}: label={row['label']} no es binario")
    
    return acc

datos_test = [
    {"features": [1, 2], "label": 1},
    {"features": [3, 4]},
    {"label": 0},
    {"features": [5, 6], "label": 3},
]

acc = validar_dataset(datos_test)
print(f"\n  {acc.summary()}")
for e in acc.errors:
    print(f"    ERROR: {e['msg']}")
for w in acc.warnings:
    print(f"    WARNING: {w}")


print("\n--- Patron: Graceful degradation ---")

def obtener_embedding(texto: str) -> list:
    """Intenta multiples fuentes con fallback."""
    
    # Intento 1: API externa (puede fallar)
    try:
        if len(texto) > 50:
            raise ConnectionError("API timeout")
        return [0.1 * len(texto)] * 5  # Simulado
    except ConnectionError:
        pass
    
    # Intento 2: Cache local
    try:
        cache = {"hola": [0.1, 0.2, 0.3, 0.4, 0.5]}
        if texto in cache:
            return cache[texto]
        raise KeyError(texto)
    except KeyError:
        pass
    
    # Fallback: embedding por defecto
    warnings.warn(f"Usando embedding default para '{texto[:20]}'")
    return [0.0] * 5

print(f"  Normal: {obtener_embedding('hola')}")
print(f"  Cache: {obtener_embedding('hola')}")

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    result = obtener_embedding("x" * 100)
    print(f"  Fallback: {result}")


# =====================================================================
#   PARTE 8: EJERCICIO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: EJERCICIO — PIPELINE ROBUSTO ===")
print("=" * 80)

"""
Pipeline ML completo con error handling profesional.
"""

print("\n--- Pipeline con error handling completo ---")

@contextmanager
def pipeline_context(nombre: str):
    """Context manager para pipeline con timing y error handling."""
    inicio = time.perf_counter()
    errores = []
    print(f"  [{nombre}] Iniciando pipeline...")
    
    try:
        yield errores
    except Exception as e:
        errores.append(str(e))
        print(f"  [{nombre}] ERROR FATAL: {e}")
    finally:
        elapsed = time.perf_counter() - inicio
        status = "FAIL" if errores else "OK"
        print(f"  [{nombre}] Finalizado ({status}) en {elapsed*1000:.1f}ms")
        if errores:
            print(f"  [{nombre}] Errores: {errores}")

class RobustPipeline:
    """Pipeline que no se detiene con errores en pasos individuales."""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.resultados = {}
        self.errores = {}
    
    def ejecutar_paso(self, nombre_paso: str, funcion, *args, **kwargs):
        """Ejecuta un paso capturando errores."""
        try:
            resultado = funcion(*args, **kwargs)
            self.resultados[nombre_paso] = resultado
            print(f"    [{nombre_paso}] OK")
            return resultado
        except Exception as e:
            self.errores[nombre_paso] = str(e)
            print(f"    [{nombre_paso}] ERROR: {e}")
            return None
    
    def resumen(self):
        print(f"\n  Pipeline '{self.nombre}':")
        print(f"    Pasos exitosos: {len(self.resultados)}")
        print(f"    Pasos fallidos: {len(self.errores)}")
        if self.errores:
            for paso, err in self.errores.items():
                print(f"    - {paso}: {err}")

# Funciones del pipeline
def cargar_datos(n: int) -> list:
    if n <= 0:
        raise DataValidationError("n debe ser positivo")
    import random
    return [{"x": random.gauss(0, 1), "y": random.choice([0, 1])} for _ in range(n)]

def preprocesar(datos: list) -> list:
    return [d for d in datos if abs(d["x"]) < 3]

def entrenar(datos: list) -> dict:
    if len(datos) < 10:
        raise ModelError("Insuficientes datos para entrenar")
    return {"modelo": "trained", "n_datos": len(datos)}

def evaluar(modelo: dict, datos: list) -> dict:
    return {"accuracy": 0.92, "f1": 0.89}

# Ejecutar pipeline
with pipeline_context("ML_v1") as errors:
    pipeline = RobustPipeline("sentiment_analysis")
    
    datos = pipeline.ejecutar_paso("cargar", cargar_datos, 100)
    
    if datos:
        datos_limpios = pipeline.ejecutar_paso("preprocesar", preprocesar, datos)
    
    if datos and datos_limpios:
        modelo = pipeline.ejecutar_paso("entrenar", entrenar, datos_limpios)
    
    if modelo and datos_limpios:
        metricas = pipeline.ejecutar_paso("evaluar", evaluar, modelo, datos_limpios)
    
    pipeline.resumen()


print("\n" + "=" * 80)
print("=== CAPITULO 10: EXPONENTIAL BACKOFF ===")
print("=" * 80)

"""
Patron profesional para reintentos con backoff exponencial.
Evita saturar servicios caidos.
"""

print("\n--- Backoff exponencial ---")

def retry_with_backoff(func, max_retries=5, base_delay=0.01, max_delay=1.0):
    """Reintenta con backoff exponencial y jitter."""
    import random
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)
            total_delay = delay + jitter
            print(f"    Intento {attempt+1} fallo: {e}. Retry en {total_delay*1000:.0f}ms")
            time.sleep(total_delay)

counter = {"n": 0}

def api_inestable():
    counter["n"] += 1
    if counter["n"] < 4:
        raise ConnectionError(f"timeout (intento {counter['n']})")
    return {"status": "ok", "intentos": counter["n"]}

counter["n"] = 0
resultado = retry_with_backoff(api_inestable, max_retries=5)
print(f"  Resultado tras {resultado['intentos']} intentos: {resultado['status']}")


print("\n" + "=" * 80)
print("=== CAPITULO 11: CIRCUIT BREAKER PATTERN ===")
print("=" * 80)

"""
Circuit Breaker: si un servicio falla muchas veces, deja de intentar
por un periodo. Evita cascada de errores.

Estados: CLOSED (normal) -> OPEN (bloqueado) -> HALF_OPEN (probando)
"""

print("\n--- Circuit Breaker ---")

class CircuitBreaker:
    """Implementacion basica de circuit breaker."""
    
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"
    
    def __init__(self, failure_threshold: int = 3, reset_timeout: float = 5.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = self.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
        self.success_count = 0
    
    def call(self, func, *args, **kwargs):
        if self.state == self.OPEN:
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = self.HALF_OPEN
                print(f"    [CB] HALF_OPEN: probando...")
            else:
                raise RuntimeError(f"Circuit breaker OPEN (fallos: {self.failure_count})")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        self.state = self.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = self.OPEN
            print(f"    [CB] OPEN: demasiados fallos ({self.failure_count})")
    
    def __repr__(self):
        return f"CB(state={self.state}, fails={self.failure_count})"

cb = CircuitBreaker(failure_threshold=3, reset_timeout=0.1)

fail_counter = {"n": 0}

def servicio_fragil():
    fail_counter["n"] += 1
    if fail_counter["n"] <= 4:
        raise ConnectionError("servicio caido")
    return "ok"

# Provocar apertura del circuit breaker
for i in range(5):
    try:
        resultado = cb.call(servicio_fragil)
        print(f"  Llamada {i+1}: {resultado} | {cb}")
    except (ConnectionError, RuntimeError) as e:
        print(f"  Llamada {i+1}: {e} | {cb}")

# Esperar reset
time.sleep(0.15)
fail_counter["n"] = 10  # Ya no falla
try:
    resultado = cb.call(servicio_fragil)
    print(f"  Tras reset: {resultado} | {cb}")
except Exception as e:
    print(f"  Tras reset: {e} | {cb}")


print("\n" + "=" * 80)
print("=== CAPITULO 12: TABLA DE DECISIONES ===")
print("=" * 80)

print("""
+----------------------------+-----------------------------------+
| SITUACION                  | ACCION                            |
+----------------------------+-----------------------------------+
| Error recuperable          | try/except + fallback             |
| Error fatal                | raise + log                       |
| API externa inestable      | retry + backoff exponencial       |
| Servicio con fallos frecuentes | Circuit breaker               |
| Validacion de inputs       | ErrorAccumulator                  |
| Recurso que cleanup        | Context manager                   |
| API deprecada              | warnings.warn(DeprecationWarning) |
| Flujo sin excepciones      | Result type (ok/fail)             |
| Error en paso de pipeline  | capturar + continuar              |
| Multiples fuentes          | graceful degradation              |
+----------------------------+-----------------------------------+
""")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE EXCEPCIONES Y ERROR HANDLING:

1. Jerarquia: Exception > (ValueError, TypeError, KeyError...)
   NUNCA capturar BaseException.

2. try/except/else/finally: else para exito, finally para cleanup.

3. Excepciones custom: jerarquia propia (MLError, DataError...).

4. EAFP > LBYL: mas pythonic y thread-safe.

5. Context managers: garantizan cleanup. @contextmanager.

6. Exception chaining: raise X from Y para rastrear causas.

7. Warnings: alertar sin detener.

8. Result type: alternativa a excepciones.

9. Retry + Backoff exponencial: para APIs inestables.

10. Circuit Breaker: proteger contra servicios caidos.

Siguiente archivo: Logging, debugging y codigo defensivo.
"""

print("\n FIN DE ARCHIVO 01_excepciones_y_manejo_errores.")
print(" El error handling profesional ha sido dominado.")
