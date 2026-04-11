# ===========================================================================
# 02_logging_debugging_y_codigo_defensivo.py
# ===========================================================================
# MODULO 06: ERRORES, TESTING Y ROBUSTEZ
# ARCHIVO 02: Logging Profesional, Debugging y Codigo Defensivo
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar logging estructurado, tecnicas de debugging, assertions,
# type checking en runtime, y patrones de codigo defensivo para
# pipelines de ML en produccion.
#
# CONTENIDO:
#   1. Modulo logging: niveles, handlers, formatters.
#   2. Logging estructurado (JSON) para produccion.
#   3. Assertions y invariantes.
#   4. Debugging: breakpoint(), pdb, tecnicas.
#   5. Codigo defensivo: validacion, guardrails.
#   6. Type checking en runtime.
#   7. Linters: conceptos de mypy, ruff.
#   8. Ejercicio: pipeline con logging completo.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import logging
import json
import time
import sys
import os
from typing import Any, Optional, Union
from dataclasses import dataclass, field
from functools import wraps
from contextlib import contextmanager


# =====================================================================
#   PARTE 1: MODULO LOGGING
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: LOGGING — NIVELES Y CONFIGURACION ===")
print("=" * 80)

"""
logging es SUPERIOR a print() para produccion:
- Niveles: DEBUG < INFO < WARNING < ERROR < CRITICAL
- Handlers: archivo, consola, red, etc.
- Formatters: timestamp, nombre, nivel, etc.
- Filtros: controlar que se loggea.

NUNCA usar print() en codigo de produccion. SIEMPRE logging.
"""

print("\n--- Niveles de logging ---")

# Crear logger especifico (no usar root logger)
logger = logging.getLogger("ml_pipeline")
logger.setLevel(logging.DEBUG)

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "  %(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
console_handler.setFormatter(formatter)

# Evitar handlers duplicados
if not logger.handlers:
    logger.addHandler(console_handler)

logger.debug("Mensaje DEBUG (no se ve con INFO level en consola)")
logger.info("Pipeline iniciado")
logger.warning("Dataset tiene valores NaN")
logger.error("Modelo fallo en epoch 5")
logger.critical("OOM: sin memoria GPU")


print("\n" + "=" * 80)
print("=== CAPITULO 2: LOGGING ESTRUCTURADO (JSON) ===")
print("=" * 80)

"""
En produccion, los logs deben ser PARSEABLES por herramientas
como ELK, Datadog, Splunk. JSON es el formato estandar.
"""

print("\n--- JSON Formatter custom ---")

class JSONFormatter(logging.Formatter):
    """Formatter que produce JSON para cada log entry."""
    
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Agregar extras si existen
        if hasattr(record, 'extra_data'):
            log_entry["data"] = record.extra_data
        
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }
        
        return json.dumps(log_entry, default=str)

# Crear logger con JSON
json_logger = logging.getLogger("ml_json")
json_logger.setLevel(logging.DEBUG)

json_handler = logging.StreamHandler()
json_handler.setFormatter(JSONFormatter())

if not json_logger.handlers:
    json_logger.addHandler(json_handler)

json_logger.info("Entrenamiento iniciado")

# Log con datos extra
extra_record = json_logger.makeRecord(
    "ml_json", logging.INFO, "training", 0,
    "Epoch completada", (), None
)
extra_record.extra_data = {"epoch": 5, "loss": 0.23, "accuracy": 0.91}
json_logger.handle(extra_record)


print("\n--- Logger con contexto ---")

class ContextLogger:
    """Logger que automaticamente incluye contexto."""
    
    def __init__(self, nombre: str, contexto: dict = None):
        self._logger = logging.getLogger(nombre)
        self._contexto = contexto or {}
    
    def with_context(self, **kwargs):
        """Retorna nuevo logger con contexto adicional."""
        nuevo_ctx = {**self._contexto, **kwargs}
        return ContextLogger(self._logger.name, nuevo_ctx)
    
    def _log(self, level, msg, **extra):
        data = {**self._contexto, **extra}
        self._logger.log(level, f"{msg} | ctx={data}")
    
    def info(self, msg, **extra):
        self._log(logging.INFO, msg, **extra)
    
    def error(self, msg, **extra):
        self._log(logging.ERROR, msg, **extra)
    
    def warning(self, msg, **extra):
        self._log(logging.WARNING, msg, **extra)

ctx_logger = ContextLogger("ml_ctx")
pipeline_logger = ctx_logger.with_context(pipeline="sentiment", version="2.0")
step_logger = pipeline_logger.with_context(step="preprocessing")

step_logger.info("Procesando datos", n_rows=1000)
step_logger.warning("Valores NaN detectados", n_nan=42)


# =====================================================================
#   PARTE 2: LOGGING DECORATORS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: DECORADORES PARA LOGGING ===")
print("=" * 80)

"""
Decoradores que automatizan el logging de funciones:
entradas, salidas, tiempo, errores.
"""

print("\n--- @log_call: logear llamadas automaticamente ---")

def log_call(func=None, *, level=logging.INFO):
    """Decorador que logea cada llamada a la funcion."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            fname = fn.__name__
            logger.log(level, f"Llamando {fname}(args={args[:2]}, kwargs={kwargs})")
            
            start = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
                elapsed = time.perf_counter() - start
                logger.log(level, f"{fname} completado en {elapsed*1000:.1f}ms")
                return result
            except Exception as e:
                elapsed = time.perf_counter() - start
                logger.error(f"{fname} FALLO en {elapsed*1000:.1f}ms: {e}")
                raise
        return wrapper
    
    if func is not None:
        return decorator(func)
    return decorator

@log_call
def entrenar_modelo_v2(datos: list, epochs: int = 5):
    time.sleep(0.01)
    return {"modelo": "trained", "epochs": epochs}

@log_call(level=logging.DEBUG)
def predecir_v2(x):
    return [0.5] * len(x)

resultado = entrenar_modelo_v2([1, 2, 3], epochs=10)


print("\n--- @validate_inputs: validar automaticamente ---")

def validate_inputs(**validators):
    """Decorador que valida inputs de una funcion."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(fn)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            for param_name, validator_fn in validators.items():
                if param_name in bound.arguments:
                    val = bound.arguments[param_name]
                    if not validator_fn(val):
                        raise ValueError(
                            f"Validacion fallida para '{param_name}': {val}"
                        )
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@validate_inputs(
    lr=lambda x: isinstance(x, float) and 0 < x < 1,
    epochs=lambda x: isinstance(x, int) and x > 0,
    modelo=lambda x: isinstance(x, str) and len(x) > 0,
)
def configurar_training(modelo: str, lr: float, epochs: int):
    return {"modelo": modelo, "lr": lr, "epochs": epochs}

print("\n  Validacion correcta:")
print(f"  {configurar_training('BERT', 0.001, 10)}")

print("  Validacion incorrecta:")
try:
    configurar_training('BERT', 5.0, 10)
except ValueError as e:
    print(f"  ERROR: {e}")


# =====================================================================
#   PARTE 3: ASSERTIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: ASSERTIONS E INVARIANTES ===")
print("=" * 80)

"""
assert condicion, "mensaje"

CUANDO USAR assert:
- Verificar invariantes internos (cosas que NUNCA deberian pasar).
- Pre/post condiciones durante desarrollo.
- NO para validar input del usuario (se puede desactivar con -O).

assert se puede DESACTIVAR con python -O. NO usar para validacion.
"""

print("\n--- Assertions correctas ---")

def normalizar_vector(v: list) -> list:
    """Normaliza un vector a norma unitaria."""
    assert len(v) > 0, "Vector no puede estar vacio"
    
    norma = sum(x**2 for x in v) ** 0.5
    assert norma > 0, f"Vector nulo no se puede normalizar: {v}"
    
    resultado = [x / norma for x in v]
    
    # Post-condicion: verificar que la norma es ~1
    norma_resultado = sum(x**2 for x in resultado) ** 0.5
    assert abs(norma_resultado - 1.0) < 1e-10, \
        f"Normalizacion fallo: norma={norma_resultado}"
    
    return resultado

v = normalizar_vector([3, 4])
print(f"  normalizar([3, 4]) = {[f'{x:.4f}' for x in v]}")
print(f"  norma = {sum(x**2 for x in v)**0.5:.10f}")

try:
    normalizar_vector([])
except AssertionError as e:
    print(f"  AssertionError: {e}")

try:
    normalizar_vector([0, 0, 0])
except AssertionError as e:
    print(f"  AssertionError: {e}")


print("\n--- Design by Contract ---")

class SortedList:
    """Lista que mantiene invariante de orden."""
    
    def __init__(self, items=None):
        self._items = sorted(items or [])
        self._check_invariant()
    
    def _check_invariant(self):
        """Verificar que la lista esta ordenada."""
        for i in range(1, len(self._items)):
            assert self._items[i] >= self._items[i-1], \
                f"Invariante roto: {self._items[i-1]} > {self._items[i]}"
    
    def insert(self, value):
        """Insertar manteniendo orden."""
        import bisect
        bisect.insort(self._items, value)
        self._check_invariant()
    
    def __repr__(self):
        return f"SortedList({self._items})"

sl = SortedList([5, 2, 8, 1])
print(f"\n  {sl}")
sl.insert(4)
print(f"  Tras insert(4): {sl}")


# =====================================================================
#   PARTE 4: DEBUGGING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: TECNICAS DE DEBUGGING ===")
print("=" * 80)

"""
Tecnicas de debugging en Python:
1. print() / logging (basico)
2. breakpoint() / pdb (interactivo)
3. traceback (analizar stack)
4. vars() / dir() / inspect (introspeccion)
"""

print("\n--- Introspeccion para debugging ---")

import inspect

class ModeloDebug:
    """Modelo con metodos de introspeccion para debug."""
    
    def __init__(self, nombre: str, config: dict):
        self.nombre = nombre
        self.config = config
        self._history = []
    
    def entrenar(self, datos: list):
        self._history.append({"accion": "train", "n": len(datos)})
    
    def debug_info(self) -> dict:
        """Informacion de debugging completa."""
        return {
            "class": self.__class__.__name__,
            "id": id(self),
            "attrs": {k: type(v).__name__ for k, v in self.__dict__.items()},
            "methods": [m for m in dir(self) if not m.startswith('_') 
                       and callable(getattr(self, m))],
            "size_bytes": sys.getsizeof(self),
            "history": self._history,
        }

md = ModeloDebug("test", {"lr": 0.001})
md.entrenar([1, 2, 3])
info = md.debug_info()
for k, v in info.items():
    print(f"  {k}: {v}")


print("\n--- Traceback helpers ---")

import traceback

def debug_traceback():
    """Captura y formatea traceback para logging."""
    try:
        # Simular error anidado
        datos = {"a": [1, 2, 3]}
        _ = datos["b"][10]
    except (KeyError, IndexError):
        tb_str = traceback.format_exc()
        lines = tb_str.strip().split("\n")
        print("  Traceback (ultimas 3 lineas):")
        for line in lines[-3:]:
            print(f"    {line}")

debug_traceback()


# =====================================================================
#   PARTE 5: CODIGO DEFENSIVO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: CODIGO DEFENSIVO ===")
print("=" * 80)

"""
Codigo defensivo: anticipar y manejar TODOS los inputs posibles.
No confiar en que el usuario (o otra funcion) pase datos correctos.
"""

print("\n--- Validacion de datos de entrada ---")

@dataclass
class TrainingConfig:
    """Configuracion con validacion defensiva."""
    modelo: str
    lr: float
    epochs: int
    batch_size: int = 32
    device: str = "cpu"
    
    def __post_init__(self):
        """Validar TODOS los campos en construccion."""
        if not isinstance(self.modelo, str) or not self.modelo:
            raise ValueError(f"modelo debe ser str no vacio, got: {self.modelo!r}")
        
        if not isinstance(self.lr, (int, float)) or self.lr <= 0 or self.lr >= 1:
            raise ValueError(f"lr debe estar en (0, 1), got: {self.lr}")
        
        if not isinstance(self.epochs, int) or self.epochs < 1:
            raise ValueError(f"epochs debe ser int >= 1, got: {self.epochs}")
        
        if not isinstance(self.batch_size, int) or self.batch_size < 1:
            raise ValueError(f"batch_size debe ser int >= 1, got: {self.batch_size}")
        
        if self.device not in ("cpu", "cuda", "mps"):
            raise ValueError(f"device debe ser cpu/cuda/mps, got: {self.device!r}")
        
        # Normalizar
        self.lr = float(self.lr)
        self.modelo = self.modelo.strip()

cfg = TrainingConfig("BERT", 0.001, 10)
print(f"  Config valida: {cfg}")

for bad_args in [
    ("", 0.001, 10),
    ("BERT", -0.1, 10),
    ("BERT", 0.001, 0),
    ("BERT", 0.001, 10, 32, "tpu"),
]:
    try:
        TrainingConfig(*bad_args)
    except ValueError as e:
        print(f"  Rechazado: {e}")


print("\n--- Guardrails para inferencia ---")

def inferencia_segura(modelo_nombre: str, input_data: Any) -> dict:
    """Inferencia con todas las validaciones necesarias."""
    
    # 1. Validar tipo de input
    if input_data is None:
        return {"error": "Input es None", "status": "rejected"}
    
    # 2. Validar que es iterable
    if not hasattr(input_data, '__len__'):
        return {"error": f"Input no tiene longitud: {type(input_data)}", 
                "status": "rejected"}
    
    # 3. Validar longitud
    MAX_INPUT = 10_000
    if len(input_data) > MAX_INPUT:
        return {"error": f"Input demasiado largo: {len(input_data)} > {MAX_INPUT}",
                "status": "rejected"}
    
    if len(input_data) == 0:
        return {"error": "Input vacio", "status": "rejected"}
    
    # 4. Inferencia (simulada)
    try:
        resultado = sum(hash(str(x)) % 100 for x in input_data) / len(input_data) / 100
        return {"prediction": resultado, "status": "ok", "input_size": len(input_data)}
    except Exception as e:
        return {"error": str(e), "status": "error"}

tests = [
    ("normal", [1, 2, 3]),
    ("none", None),
    ("vacio", []),
    ("largo", list(range(20_000))),
    ("string", "hola mundo"),
]

for nombre, data in tests:
    r = inferencia_segura("bert", data)
    print(f"  {nombre}: {r['status']} {'- ' + r.get('error', '') if r['status'] != 'ok' else ''}")


# =====================================================================
#   PARTE 6: TYPE CHECKING EN RUNTIME
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: TYPE CHECKING EN RUNTIME ===")
print("=" * 80)

"""
Python es dinamicamente tipado, pero en produccion necesitas
validar tipos. Formas:
1. isinstance() checks
2. Decoradores de validacion
3. Runtime type checkers (beartype, typeguard)
4. Pydantic (validacion + parsing)
"""

print("\n--- Simulacion de Pydantic-style validation ---")

class Validated:
    """Descriptor que valida tipo y rango."""
    
    def __init__(self, tipo, min_val=None, max_val=None, choices=None):
        self.tipo = tipo
        self.min_val = min_val
        self.max_val = max_val
        self.choices = choices
    
    def __set_name__(self, owner, name):
        self.name = name
        self.attr = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.attr, None)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.tipo):
            raise TypeError(f"{self.name}: esperaba {self.tipo.__name__}, "
                          f"got {type(value).__name__}")
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name}: {value} < min({self.min_val})")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name}: {value} > max({self.max_val})")
        if self.choices and value not in self.choices:
            raise ValueError(f"{self.name}: {value} no en {self.choices}")
        setattr(obj, self.attr, value)

class ModelConfig:
    lr = Validated(float, min_val=0.0, max_val=1.0)
    epochs = Validated(int, min_val=1, max_val=10000)
    optimizer = Validated(str, choices=["adam", "sgd", "rmsprop"])
    
    def __init__(self, lr, epochs, optimizer):
        self.lr = lr
        self.epochs = epochs
        self.optimizer = optimizer
    
    def __repr__(self):
        return f"ModelConfig(lr={self.lr}, epochs={self.epochs}, opt='{self.optimizer}')"

mc = ModelConfig(0.001, 10, "adam")
print(f"  {mc}")

for args, label in [
    ((5.0, 10, "adam"), "lr fuera de rango"),
    ((0.001, -1, "adam"), "epochs negativo"),
    ((0.001, 10, "napoleon"), "optimizer invalido"),
    (("string", 10, "adam"), "lr tipo incorrecto"),
]:
    try:
        ModelConfig(*args)
    except (TypeError, ValueError) as e:
        print(f"  {label}: {e}")


# =====================================================================
#   PARTE 7: EJERCICIO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: EJERCICIO — PIPELINE CON LOGGING COMPLETO ===")
print("=" * 80)

print("\n--- Pipeline ML con logging profesional ---")

class MLLogger:
    """Logger especializado para ML con metricas."""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.metricas = []
        self.eventos = []
    
    def log_metrica(self, nombre: str, valor: float, step: int = 0):
        entry = {"metrica": nombre, "valor": valor, "step": step}
        self.metricas.append(entry)
        print(f"  [{self.nombre}] METRIC {nombre}={valor:.4f} (step={step})")
    
    def log_evento(self, evento: str, **datos):
        entry = {"evento": evento, **datos}
        self.eventos.append(entry)
        datos_str = ", ".join(f"{k}={v}" for k, v in datos.items())
        print(f"  [{self.nombre}] EVENT {evento} ({datos_str})")
    
    def resumen(self):
        print(f"\n  [{self.nombre}] Resumen:")
        print(f"    {len(self.metricas)} metricas registradas")
        print(f"    {len(self.eventos)} eventos registrados")
        if self.metricas:
            for m in self.metricas[-3:]:
                print(f"    Ultima: {m['metrica']}={m['valor']:.4f}")

ml_log = MLLogger("experiment_001")
ml_log.log_evento("training_start", modelo="BERT", lr=0.001)

import random
random.seed(42)
for epoch in range(1, 6):
    loss = 1.0 / epoch + random.gauss(0, 0.05)
    acc = 1.0 - loss + random.gauss(0, 0.02)
    ml_log.log_metrica("loss", loss, step=epoch)
    ml_log.log_metrica("accuracy", acc, step=epoch)

ml_log.log_evento("training_end", epochs=5, status="completed")
ml_log.resumen()


print("\n" + "=" * 80)
print("=== CAPITULO 9: LOG ROTATION Y MULTIPLES HANDLERS ===")
print("=" * 80)

"""
En produccion necesitas:
- Archivo rotativo (no llenar disco).
- Consola para desarrollo.
- Diferentes niveles por handler.
"""

print("\n--- Configuracion multi-handler (conceptual) ---")

print("""
EJEMPLO DE CONFIGURACION PARA PRODUCCION:

import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# Handler 1: Consola (solo WARNING+)
console = logging.StreamHandler()
console.setLevel(logging.WARNING)

# Handler 2: Archivo rotativo (todo, max 10MB, 5 backups)
file_handler = RotatingFileHandler(
    "ml_pipeline.log",
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)

# Handler 3: Archivo diario para errores
error_handler = TimedRotatingFileHandler(
    "ml_errors.log",
    when="midnight",
    backupCount=30
)
error_handler.setLevel(logging.ERROR)

logger.addHandler(console)
logger.addHandler(file_handler)
logger.addHandler(error_handler)
""")


print("\n--- Filtros custom ---")

class MLFilter(logging.Filter):
    """Solo deja pasar logs relacionados con ML."""
    
    def __init__(self, keywords=None):
        super().__init__()
        self.keywords = keywords or ["model", "train", "predict", "loss"]
    
    def filter(self, record):
        msg = record.getMessage().lower()
        return any(kw in msg for kw in self.keywords)

# Demostrar filtro
ml_filter = MLFilter(["model", "train", "epoch"])

test_messages = [
    "Model BERT loaded",
    "Training started",
    "Database connected",
    "Epoch 5 completed",
    "Config updated",
]

print("  Mensajes filtrados por MLFilter:")
for msg in test_messages:
    record = logging.LogRecord("test", logging.INFO, "", 0, msg, (), None)
    passed = ml_filter.filter(record)
    print(f"    {'PASS' if passed else 'SKIP'}: {msg}")


print("\n" + "=" * 80)
print("=== CAPITULO 10: PERFORMANCE PROFILING ===")
print("=" * 80)

"""
Profiling: medir donde pasa tiempo tu codigo.
Herramientas: cProfile, line_profiler, memory_profiler.
"""

print("\n--- Profiler simple con decorador ---")

import cProfile
from io import StringIO

def profile_function(func):
    """Decorador que hace profile de una funcion."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        # Extraer stats
        import pstats
        stream = StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(5)
        
        lines = stream.getvalue().strip().split("\n")
        for line in lines[:8]:
            print(f"    {line}")
        
        return result
    return wrapper

@profile_function
def operacion_pesada():
    datos = [i ** 2 for i in range(100_000)]
    ordenados = sorted(datos, reverse=True)
    return sum(ordenados[:100])

print("  Profiling operacion_pesada():")
r = operacion_pesada()
print(f"  Resultado: {r}")


print("\n--- Timer context manager reutilizable ---")

class DetailedTimer:
    """Timer con acumulacion de mediciones."""
    
    def __init__(self):
        self.mediciones = {}
    
    @contextmanager
    def measure(self, nombre: str):
        start = time.perf_counter()
        yield
        elapsed = time.perf_counter() - start
        if nombre not in self.mediciones:
            self.mediciones[nombre] = []
        self.mediciones[nombre].append(elapsed)
    
    def report(self):
        for nombre, tiempos in self.mediciones.items():
            avg = sum(tiempos) / len(tiempos)
            total = sum(tiempos)
            print(f"    {nombre}: {len(tiempos)} calls, "
                  f"avg={avg*1000:.2f}ms, total={total*1000:.2f}ms")

timer = DetailedTimer()

for _ in range(5):
    with timer.measure("tokenize"):
        "hola mundo machine learning".split()
    
    with timer.measure("sort"):
        sorted(range(10000), reverse=True)

timer.report()


print("\n" + "=" * 80)
print("=== CAPITULO 11: SANITIZACION DE INPUTS ===")
print("=" * 80)

"""
Sanitizar inputs antes de procesar: evitar inyecciones,
caracteres peligrosos, datos malformados.
"""

print("\n--- Sanitizador de texto ---")

class TextSanitizer:
    """Sanitiza texto para procesamiento seguro."""
    
    @staticmethod
    def sanitize(texto: str, max_length: int = 10000) -> str:
        if not isinstance(texto, str):
            raise TypeError(f"Se espera str, got {type(texto).__name__}")
        
        # 1. Truncar
        texto = texto[:max_length]
        
        # 2. Remover caracteres de control (excepto newline, tab)
        texto = "".join(c for c in texto if c.isprintable() or c in "\n\t")
        
        # 3. Normalizar espacios
        texto = " ".join(texto.split())
        
        # 4. Strip
        texto = texto.strip()
        
        return texto
    
    @staticmethod
    def sanitize_for_sql(texto: str) -> str:
        """Sanitizar para prevenir SQL injection basica."""
        dangerous = ["'", '"', ";", "--", "/*", "*/", "DROP", "DELETE"]
        for d in dangerous:
            texto = texto.replace(d, "")
        return texto

sanitizer = TextSanitizer()
tests_sanitize = [
    "  Hola   Mundo  ",
    "texto\x00con\x01control\x02chars",
    "normal text",
    "x" * 20000,
    "'; DROP TABLE models; --",
]

for t in tests_sanitize:
    clean = sanitizer.sanitize(t)
    print(f"  '{t[:30]}...' -> '{clean[:30]}'")


print("\n" + "=" * 80)
print("=== CAPITULO 12: LINTERS Y HERRAMIENTAS ===")
print("=" * 80)

"""
Herramientas de calidad de codigo:
"""

print("""
+------------------+-----------------------------------+--------------------+
| HERRAMIENTA      | QUE HACE                          | COMANDO            |
+------------------+-----------------------------------+--------------------+
| mypy             | Type checking estatico            | mypy src/          |
| ruff             | Linter + formatter (muy rapido)   | ruff check src/    |
| black            | Formatter de codigo               | black src/         |
| isort            | Ordenar imports                   | isort src/         |
| pylint           | Linter completo                   | pylint src/        |
| bandit           | Seguridad                         | bandit -r src/     |
| pytest           | Testing                           | pytest tests/      |
| coverage         | Coverage de tests                 | coverage run -m ...|
+------------------+-----------------------------------+--------------------+

CONFIGURACION EN pyproject.toml:

[tool.mypy]
strict = true
warn_return_any = true

[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I"]

[tool.black]
line-length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"
""")


print("\n" + "=" * 80)
print("=== CAPITULO 13: RATE LIMITING ===")
print("=" * 80)

"""
Rate limiting: proteger servicios de abuso limitando
llamadas por segundo/minuto.
"""

print("\n--- Rate limiter con decorador ---")

class RateLimiter:
    """Limita llamadas por periodo de tiempo."""
    
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Limpiar llamadas antiguas
            self.calls = [t for t in self.calls if now - t < self.period]
            
            if len(self.calls) >= self.max_calls:
                wait = self.period - (now - self.calls[0])
                raise RuntimeError(
                    f"Rate limit: {self.max_calls}/{self.period}s. "
                    f"Espera {wait:.1f}s"
                )
            
            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper

@RateLimiter(max_calls=3, period=1.0)
def api_call_limited(query: str) -> dict:
    return {"query": query, "status": "ok"}

print("  Llamadas con rate limit (3/segundo):")
for i in range(5):
    try:
        r = api_call_limited(f"query_{i}")
        print(f"    Call {i}: {r['status']}")
    except RuntimeError as e:
        print(f"    Call {i}: BLOQUEADO - {e}")


print("\n" + "=" * 80)
print("=== CAPITULO 14: CONFIGURACION POR ENTORNO ===")
print("=" * 80)

"""
Patron para cargar configuracion segun entorno:
desarrollo, staging, produccion.
"""

print("\n--- Config por entorno ---")

class EnvConfig:
    """Carga config segun variable de entorno."""
    
    DEFAULTS = {
        "development": {
            "debug": True,
            "log_level": "DEBUG",
            "db_url": "sqlite:///dev.db",
            "cache_ttl": 0,
        },
        "staging": {
            "debug": False,
            "log_level": "INFO",
            "db_url": "postgresql://staging:5432/ml",
            "cache_ttl": 300,
        },
        "production": {
            "debug": False,
            "log_level": "WARNING",
            "db_url": "postgresql://prod:5432/ml",
            "cache_ttl": 3600,
        },
    }
    
    def __init__(self, env: str = None):
        self.env = env or os.getenv("APP_ENV", "development")
        if self.env not in self.DEFAULTS:
            raise ValueError(f"Entorno no valido: {self.env}")
        self._config = dict(self.DEFAULTS[self.env])
    
    def get(self, key: str, default=None):
        # Primero env var, luego config, luego default
        env_key = f"APP_{key.upper()}"
        return os.getenv(env_key, self._config.get(key, default))
    
    def __repr__(self):
        return f"EnvConfig(env='{self.env}', keys={list(self._config.keys())})"

for env in ["development", "staging", "production"]:
    cfg = EnvConfig(env)
    print(f"  {env}: debug={cfg.get('debug')}, log={cfg.get('log_level')}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE LOGGING, DEBUGGING Y CODIGO DEFENSIVO:

1. logging > print(): niveles, handlers, formatters.

2. JSON logging: parseable por herramientas de produccion.

3. ContextLogger: agregar contexto automaticamente.

4. Decoradores: @log_call, @validate_inputs.

5. Assertions: invariantes internos (NO para validacion).

6. Debugging: breakpoint(), traceback, introspeccion.

7. Codigo defensivo: validar TODO en la frontera.

8. Type checking runtime: descriptores, Pydantic-style.

9. Profiling: cProfile, timers, medir rendimiento.

10. Sanitizacion: limpiar inputs antes de procesar.

11. Rate limiting: proteger servicios de abuso.

12. Config por entorno: dev/staging/production.

Siguiente archivo: Testing con pytest.
"""

print("\n FIN DE ARCHIVO 02_logging_debugging_y_codigo_defensivo.")
print(" El logging y codigo defensivo han sido dominados.")
