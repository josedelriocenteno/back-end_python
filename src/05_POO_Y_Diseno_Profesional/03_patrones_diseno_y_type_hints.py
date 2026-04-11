# ===========================================================================
# 03_patrones_diseno_y_type_hints.py
# ===========================================================================
# MODULO 05: POO Y DISENO PROFESIONAL
# ARCHIVO 03: Patrones de Diseno para ML y Type Hints Avanzados
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Patrones de diseno GOF aplicados a ML: Factory, Strategy, Observer,
# Singleton, Builder, Registry. Type hints avanzados: TypeVar, Generic,
# Literal, TypeAlias, overload.
#
# CONTENIDO:
#   1. Factory Pattern: crear modelos/datasets dinamicamente.
#   2. Strategy Pattern: intercambiar algoritmos en runtime.
#   3. Observer Pattern: callbacks y eventos de training.
#   4. Singleton: configuracion global unica.
#   5. Builder: construir pipelines paso a paso.
#   6. Registry: registro de componentes por nombre.
#   7. Type hints avanzados: TypeVar, Generic, Protocol.
#   8. Ejercicio: framework ML completo con patrones.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import time
from abc import ABC, abstractmethod
from typing import (TypeVar, Generic, Optional, Any, Callable,
                    Protocol, runtime_checkable)
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import defaultdict


# =====================================================================
#   PARTE 1: FACTORY PATTERN
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: FACTORY PATTERN ===")
print("=" * 80)

"""
Factory Pattern: crear objetos sin especificar la clase concreta.
El cliente pide "quiero un modelo de tipo X" y la factory lo crea.

EN ML: crear modelos, optimizadores, datasets por nombre.
"""

print("\n--- Simple Factory ---")

class OptimizerBase(ABC):
    @abstractmethod
    def step(self, params: list, grads: list) -> list: ...
    @abstractmethod
    def nombre(self) -> str: ...

class SGD(OptimizerBase):
    def __init__(self, lr: float = 0.01):
        self.lr = lr
    def step(self, params, grads):
        return [p - self.lr * g for p, g in zip(params, grads)]
    def nombre(self): return f"SGD(lr={self.lr})"

class Adam(OptimizerBase):
    def __init__(self, lr: float = 0.001, beta1: float = 0.9):
        self.lr = lr
        self.beta1 = beta1
    def step(self, params, grads):
        return [p - self.lr * g * (1 - self.beta1) for p, g in zip(params, grads)]
    def nombre(self): return f"Adam(lr={self.lr})"

class RMSProp(OptimizerBase):
    def __init__(self, lr: float = 0.001, decay: float = 0.9):
        self.lr = lr
        self.decay = decay
    def step(self, params, grads):
        return [p - self.lr * g for p, g in zip(params, grads)]
    def nombre(self): return f"RMSProp(lr={self.lr})"

class OptimizerFactory:
    """Factory que crea optimizadores por nombre."""
    
    _registry = {
        "sgd": SGD,
        "adam": Adam,
        "rmsprop": RMSProp,
    }
    
    @classmethod
    def crear(cls, nombre: str, **kwargs) -> OptimizerBase:
        nombre_lower = nombre.lower()
        if nombre_lower not in cls._registry:
            disponibles = list(cls._registry.keys())
            raise ValueError(f"'{nombre}' no disponible. Opciones: {disponibles}")
        return cls._registry[nombre_lower](**kwargs)
    
    @classmethod
    def registrar(cls, nombre: str, clase):
        cls._registry[nombre.lower()] = clase
    
    @classmethod
    def listar(cls) -> list:
        return list(cls._registry.keys())

# Uso
opt1 = OptimizerFactory.crear("adam", lr=0.0001)
opt2 = OptimizerFactory.crear("sgd", lr=0.01)
print(f"  opt1: {opt1.nombre()}")
print(f"  opt2: {opt2.nombre()}")
print(f"  Disponibles: {OptimizerFactory.listar()}")

# Registrar nuevo optimizador
class AdaGrad(OptimizerBase):
    def __init__(self, lr=0.01):
        self.lr = lr
    def step(self, params, grads):
        return [p - self.lr * g for p, g in zip(params, grads)]
    def nombre(self): return f"AdaGrad(lr={self.lr})"

OptimizerFactory.registrar("adagrad", AdaGrad)
opt3 = OptimizerFactory.crear("adagrad")
print(f"  Nuevo: {opt3.nombre()}")


# =====================================================================
#   PARTE 2: STRATEGY PATTERN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: STRATEGY PATTERN ===")
print("=" * 80)

"""
Strategy: encapsular un algoritmo en una clase y hacerlo intercambiable.
El contexto NO sabe que algoritmo usa internamente.

EN ML: diferentes estrategias de tokenizacion, loss, scheduling.
"""

print("\n--- Strategy para tokenizacion ---")

class TokenizationStrategy(ABC):
    @abstractmethod
    def tokenize(self, texto: str) -> list[str]: ...

class WordTokenizer(TokenizationStrategy):
    def tokenize(self, texto: str) -> list[str]:
        return texto.lower().split()

class CharTokenizer(TokenizationStrategy):
    def tokenize(self, texto: str) -> list[str]:
        return list(texto.lower())

class SubwordTokenizer(TokenizationStrategy):
    """Simula BPE tokenization."""
    def tokenize(self, texto: str) -> list[str]:
        palabras = texto.lower().split()
        tokens = []
        for p in palabras:
            if len(p) <= 3:
                tokens.append(p)
            else:
                tokens.append(p[:3])
                tokens.append("##" + p[3:])
        return tokens

class TextProcessor:
    """Contexto que usa una estrategia de tokenizacion."""
    
    def __init__(self, strategy: TokenizationStrategy):
        self._strategy = strategy
    
    @property
    def strategy(self) -> TokenizationStrategy:
        return self._strategy
    
    @strategy.setter
    def strategy(self, new_strategy: TokenizationStrategy):
        self._strategy = new_strategy
    
    def procesar(self, texto: str) -> dict:
        tokens = self._strategy.tokenize(texto)
        return {
            "strategy": self._strategy.__class__.__name__,
            "n_tokens": len(tokens),
            "tokens": tokens[:10],
        }

texto = "Machine learning con transformers"

proc = TextProcessor(WordTokenizer())
print(f"  Word: {proc.procesar(texto)}")

proc.strategy = SubwordTokenizer()
print(f"  Subword: {proc.procesar(texto)}")

proc.strategy = CharTokenizer()
r = proc.procesar(texto)
print(f"  Char: n={r['n_tokens']}, tokens={r['tokens']}")


# =====================================================================
#   PARTE 3: OBSERVER PATTERN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: OBSERVER PATTERN — CALLBACKS ===")
print("=" * 80)

"""
Observer: cuando un objeto cambia de estado, notifica a todos
los observadores registrados.

EN ML: callbacks de training (EarlyStopping, ModelCheckpoint, Logger).
"""

print("\n--- Observer para training callbacks ---")

class TrainingEvent(Enum):
    EPOCH_START = auto()
    EPOCH_END = auto()
    TRAIN_START = auto()
    TRAIN_END = auto()
    BATCH_END = auto()

@dataclass
class TrainingState:
    epoch: int = 0
    batch: int = 0
    loss: float = 0.0
    accuracy: float = 0.0
    mejores_metricas: dict = field(default_factory=dict)

class Callback(ABC):
    """Interfaz para callbacks de training."""
    @abstractmethod
    def on_event(self, evento: TrainingEvent, state: TrainingState): ...

class EarlyStopping(Callback):
    def __init__(self, patience: int = 3, min_delta: float = 0.01):
        self.patience = patience
        self.min_delta = min_delta
        self.wait = 0
        self.mejor_loss = float('inf')
        self.debe_parar = False
    
    def on_event(self, evento: TrainingEvent, state: TrainingState):
        if evento == TrainingEvent.EPOCH_END:
            if state.loss < self.mejor_loss - self.min_delta:
                self.mejor_loss = state.loss
                self.wait = 0
            else:
                self.wait += 1
                if self.wait >= self.patience:
                    self.debe_parar = True
                    print(f"    [EarlyStopping] Parando en epoch {state.epoch}")

class MetricsLogger(Callback):
    def __init__(self):
        self.historial = []
    
    def on_event(self, evento: TrainingEvent, state: TrainingState):
        if evento == TrainingEvent.EPOCH_END:
            self.historial.append({"epoch": state.epoch, "loss": state.loss,
                                   "acc": state.accuracy})
            print(f"    [Logger] Epoch {state.epoch}: loss={state.loss:.4f}, "
                  f"acc={state.accuracy:.4f}")

class TrainerWithCallbacks:
    """Trainer que notifica callbacks en cada evento."""
    
    def __init__(self, callbacks: list[Callback] = None):
        self.callbacks = callbacks or []
        self.state = TrainingState()
    
    def _notify(self, evento: TrainingEvent):
        for cb in self.callbacks:
            cb.on_event(evento, self.state)
    
    def fit(self, datos, epochs: int = 10):
        self._notify(TrainingEvent.TRAIN_START)
        
        for epoch in range(1, epochs + 1):
            self.state.epoch = epoch
            self._notify(TrainingEvent.EPOCH_START)
            
            # Simular metricas
            self.state.loss = 1.0 / epoch + 0.1
            self.state.accuracy = 1.0 - self.state.loss
            
            self._notify(TrainingEvent.EPOCH_END)
            
            # Verificar early stopping
            for cb in self.callbacks:
                if isinstance(cb, EarlyStopping) and cb.debe_parar:
                    self._notify(TrainingEvent.TRAIN_END)
                    return
        
        self._notify(TrainingEvent.TRAIN_END)

early_stop = EarlyStopping(patience=2)
logger = MetricsLogger()

trainer = TrainerWithCallbacks([logger, early_stop])
trainer.fit(datos=[1, 2, 3], epochs=10)
print(f"\n  Historial: {len(logger.historial)} epochs registrados")


# =====================================================================
#   PARTE 4: SINGLETON Y BUILDER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: SINGLETON — CONFIGURACION GLOBAL ===")
print("=" * 80)

"""
Singleton: garantiza que solo exista UNA instancia de una clase.
EN ML: configuracion global, model registry, conexion a DB.
"""

class AppConfig:
    """Singleton para configuracion de la aplicacion."""
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not AppConfig._initialized:
            self.debug = False
            self.device = "cpu"
            self.seed = 42
            self.log_level = "INFO"
            AppConfig._initialized = True
    
    def __repr__(self):
        return f"AppConfig(debug={self.debug}, device='{self.device}')"

c1 = AppConfig()
c2 = AppConfig()
print(f"  c1 is c2: {c1 is c2}")
c1.device = "cuda"
print(f"  c2.device: '{c2.device}' (misma instancia)")


print("\n" + "=" * 80)
print("=== CAPITULO 5: BUILDER PATTERN ===")
print("=" * 80)

"""
Builder: construir objetos complejos paso a paso.
EN ML: construir pipelines, configuraciones, architecturas.
"""

print("\n--- Builder para pipeline ML ---")

@dataclass
class PipelineConfig:
    nombre: str = "default"
    tokenizer: str = "word"
    vectorizer_dim: int = 100
    modelo: str = "linear"
    metricas: list = field(default_factory=list)
    batch_size: int = 32
    epochs: int = 10

class PipelineBuilder:
    """Builder fluido para construir pipelines."""
    
    def __init__(self):
        self._config = PipelineConfig()
    
    def nombre(self, n: str):
        self._config.nombre = n
        return self
    
    def tokenizer(self, t: str):
        self._config.tokenizer = t
        return self
    
    def vectorizer(self, dim: int):
        self._config.vectorizer_dim = dim
        return self
    
    def modelo(self, m: str):
        self._config.modelo = m
        return self
    
    def metricas(self, *ms: str):
        self._config.metricas = list(ms)
        return self
    
    def training(self, batch_size: int = 32, epochs: int = 10):
        self._config.batch_size = batch_size
        self._config.epochs = epochs
        return self
    
    def build(self) -> PipelineConfig:
        return self._config

config = (PipelineBuilder()
    .nombre("sentiment_v2")
    .tokenizer("subword")
    .vectorizer(256)
    .modelo("transformer")
    .metricas("accuracy", "f1", "precision")
    .training(batch_size=64, epochs=20)
    .build()
)

print(f"  Pipeline: {config}")


# =====================================================================
#   PARTE 5: TYPE HINTS AVANZADOS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: TYPE HINTS AVANZADOS ===")
print("=" * 80)

"""
Type hints avanzados para codigo de produccion:
- TypeVar: variables de tipo para generics.
- Generic: clases parametrizadas por tipo.
- Union, Optional, Literal.
- TypeAlias (Python 3.10+).
"""

print("\n--- TypeVar y Generic ---")

T = TypeVar('T')
V = TypeVar('V')

class Cache(Generic[T, V]):
    """Cache generico tipado."""
    
    def __init__(self, maxsize: int = 100):
        self._store: dict[T, V] = {}
        self._maxsize = maxsize
    
    def get(self, key: T) -> Optional[V]:
        return self._store.get(key)
    
    def set(self, key: T, value: V) -> None:
        if len(self._store) >= self._maxsize:
            oldest = next(iter(self._store))
            del self._store[oldest]
        self._store[key] = value
    
    def __len__(self) -> int:
        return len(self._store)
    
    def __repr__(self) -> str:
        return f"Cache(size={len(self)}/{self._maxsize})"

# Cache tipado: str -> list[float]
embedding_cache: Cache[str, list[float]] = Cache(maxsize=1000)
embedding_cache.set("hola", [0.1, 0.2, 0.3])
embedding_cache.set("mundo", [0.4, 0.5, 0.6])

print(f"  Cache: {embedding_cache}")
print(f"  get('hola'): {embedding_cache.get('hola')}")


print("\n--- TypeVar con restricciones ---")

Numeric = TypeVar('Numeric', int, float)

def promedio(valores: list[Numeric]) -> float:
    return sum(valores) / len(valores)

print(f"  promedio([1, 2, 3]): {promedio([1, 2, 3])}")
print(f"  promedio([1.5, 2.5]): {promedio([1.5, 2.5])}")


print("\n--- Enum para estados tipados ---")

class ModelState(Enum):
    CREATED = "created"
    TRAINING = "training"
    TRAINED = "trained"
    DEPLOYED = "deployed"
    FAILED = "failed"

class StatefulModel:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._state = ModelState.CREATED
    
    @property
    def state(self) -> ModelState:
        return self._state
    
    def train(self):
        if self._state != ModelState.CREATED:
            raise RuntimeError(f"No se puede entrenar desde estado {self._state}")
        self._state = ModelState.TRAINING
        self._state = ModelState.TRAINED
    
    def deploy(self):
        if self._state != ModelState.TRAINED:
            raise RuntimeError(f"No se puede deploy desde {self._state}")
        self._state = ModelState.DEPLOYED
    
    def __repr__(self):
        return f"StatefulModel('{self.nombre}', state={self._state.value})"

sm = StatefulModel("BERT")
print(f"\n  {sm}")
sm.train()
print(f"  Tras train: {sm}")
sm.deploy()
print(f"  Tras deploy: {sm}")


# =====================================================================
#   PARTE 6: EJERCICIO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: EJERCICIO — MINI FRAMEWORK ML ===")
print("=" * 80)

"""
Combinar TODOS los patrones en un mini framework ML:
- Registry para modelos (Factory).
- Strategy para metricas.
- Observer para callbacks.
- Builder para configuracion.
"""

print("\n--- Mini Framework ---")

class ModelRegistry2:
    """Registry global de modelos (Singleton + Factory)."""
    _models = {}
    
    @classmethod
    def register(cls, nombre: str):
        def decorator(model_cls):
            cls._models[nombre] = model_cls
            return model_cls
        return decorator
    
    @classmethod
    def create(cls, nombre: str, **kwargs):
        if nombre not in cls._models:
            raise ValueError(f"Modelo '{nombre}' no registrado")
        return cls._models[nombre](**kwargs)
    
    @classmethod
    def listar(cls):
        return list(cls._models.keys())

@ModelRegistry2.register("dummy")
class DummyModel:
    def __init__(self, output=0.5):
        self.output = output
    def predict(self, x):
        return [self.output] * len(x)

@ModelRegistry2.register("random")
class RandomModel:
    def __init__(self, seed=42):
        import random
        self.rng = random.Random(seed)
    def predict(self, x):
        return [self.rng.random() for _ in x]

print(f"  Modelos registrados: {ModelRegistry2.listar()}")

dummy = ModelRegistry2.create("dummy", output=0.9)
rand = ModelRegistry2.create("random")

datos_test = [1, 2, 3, 4, 5]
print(f"  Dummy preds: {dummy.predict(datos_test)}")
print(f"  Random preds: {[f'{p:.2f}' for p in rand.predict(datos_test)]}")


print("\n" + "=" * 80)
print("=== CAPITULO 8: CHAIN OF RESPONSIBILITY ===")
print("=" * 80)

"""
Chain of Responsibility: pasar una request a traves de una cadena
de handlers. Cada handler decide si procesa o pasa al siguiente.

EN ML: pipeline de validacion, middleware de preprocessing.
"""

print("\n--- Chain of Responsibility para validacion ---")

class ValidationHandler(ABC):
    def __init__(self):
        self._next = None
    
    def set_next(self, handler):
        self._next = handler
        return handler
    
    def handle(self, data: dict) -> dict:
        result = self.validate(data)
        if not result["valid"]:
            return result
        if self._next:
            return self._next.handle(data)
        return result
    
    @abstractmethod
    def validate(self, data: dict) -> dict: ...

class NotNullValidator(ValidationHandler):
    def __init__(self, required_fields: list):
        super().__init__()
        self.required = required_fields
    
    def validate(self, data):
        missing = [f for f in self.required if f not in data or data[f] is None]
        if missing:
            return {"valid": False, "error": f"Campos faltantes: {missing}"}
        return {"valid": True}

class TypeValidator(ValidationHandler):
    def __init__(self, schema: dict):
        super().__init__()
        self.schema = schema
    
    def validate(self, data):
        for field_name, expected_type in self.schema.items():
            if field_name in data and not isinstance(data[field_name], expected_type):
                return {"valid": False,
                        "error": f"'{field_name}' debe ser {expected_type.__name__}"}
        return {"valid": True}

class RangeValidator(ValidationHandler):
    def __init__(self, ranges: dict):
        super().__init__()
        self.ranges = ranges  # {campo: (min, max)}
    
    def validate(self, data):
        for field_name, (min_val, max_val) in self.ranges.items():
            if field_name in data:
                val = data[field_name]
                if not (min_val <= val <= max_val):
                    return {"valid": False,
                            "error": f"'{field_name}'={val} fuera de [{min_val},{max_val}]"}
        return {"valid": True}

# Construir cadena
not_null = NotNullValidator(["lr", "epochs", "modelo"])
type_check = TypeValidator({"lr": float, "epochs": int, "modelo": str})
range_check = RangeValidator({"lr": (0.0, 1.0), "epochs": (1, 1000)})

not_null.set_next(type_check).set_next(range_check)

# Probar
configs_test = [
    {"lr": 0.001, "epochs": 10, "modelo": "BERT"},
    {"lr": 0.001, "modelo": "BERT"},  # Falta epochs
    {"lr": "invalid", "epochs": 10, "modelo": "BERT"},  # Tipo mal
    {"lr": 5.0, "epochs": 10, "modelo": "BERT"},  # Fuera de rango
]

for cfg in configs_test:
    result = not_null.handle(cfg)
    status = "OK" if result["valid"] else result["error"]
    print(f"  {cfg} -> {status}")


print("\n" + "=" * 80)
print("=== CAPITULO 9: REPOSITORY PATTERN ===")
print("=" * 80)

"""
Repository: abstrae el acceso a datos.
El codigo de negocio no sabe si los datos vienen de DB, archivo, API.
"""

print("\n--- Repository para experimentos ML ---")

@dataclass
class ExperimentRecord:
    id: str
    modelo: str
    accuracy: float
    loss: float
    config: dict = field(default_factory=dict)

class ExperimentRepository(ABC):
    @abstractmethod
    def save(self, exp: ExperimentRecord) -> None: ...
    @abstractmethod
    def get(self, id: str) -> Optional[ExperimentRecord]: ...
    @abstractmethod
    def list_all(self) -> list[ExperimentRecord]: ...
    @abstractmethod
    def find_best(self, metric: str = "accuracy") -> Optional[ExperimentRecord]: ...

class InMemoryRepository(ExperimentRepository):
    """Repositorio en memoria (para testing y desarrollo)."""
    
    def __init__(self):
        self._store: dict[str, ExperimentRecord] = {}
    
    def save(self, exp):
        self._store[exp.id] = exp
    
    def get(self, id):
        return self._store.get(id)
    
    def list_all(self):
        return list(self._store.values())
    
    def find_best(self, metric="accuracy"):
        if not self._store:
            return None
        return max(self._store.values(), key=lambda e: getattr(e, metric, 0))

repo = InMemoryRepository()

import random
random.seed(42)
for i in range(10):
    exp = ExperimentRecord(
        id=f"exp_{i:03d}",
        modelo=random.choice(["BERT", "GPT", "T5"]),
        accuracy=random.uniform(0.7, 0.95),
        loss=random.uniform(0.1, 0.5),
        config={"lr": random.choice([0.001, 0.01]), "epochs": random.randint(5, 20)}
    )
    repo.save(exp)

print(f"  Total experiments: {len(repo.list_all())}")
best = repo.find_best("accuracy")
print(f"  Best: {best}")
print(f"  Get exp_003: {repo.get('exp_003')}")


print("\n" + "=" * 80)
print("=== CAPITULO 10: EVENT BUS PATTERN ===")
print("=" * 80)

"""
Event Bus: desacoplar emisores de receptores de eventos.
Los handlers se suscriben a tipos de evento, no a emisores concretos.
"""

print("\n--- Event Bus ---")

class EventBus:
    """Bus de eventos generico."""
    
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
    
    def subscribe(self, event_type: str, handler: Callable):
        self._handlers[event_type].append(handler)
        return self
    
    def publish(self, event_type: str, data: Any = None):
        for handler in self._handlers.get(event_type, []):
            handler(event_type, data)
    
    def on(self, event_type: str):
        """Decorador para suscribir handlers."""
        def decorator(func):
            self.subscribe(event_type, func)
            return func
        return decorator

bus = EventBus()

@bus.on("model.trained")
def log_training(event, data):
    print(f"    [LOG] {event}: {data}")

@bus.on("model.trained")
def save_metrics(event, data):
    print(f"    [SAVE] Guardando metricas: {data.get('accuracy', 'N/A')}")

@bus.on("model.deployed")
def notify_team(event, data):
    print(f"    [NOTIFY] Modelo deployado: {data}")

print("Publicando eventos:")
bus.publish("model.trained", {"modelo": "BERT", "accuracy": 0.95})
bus.publish("model.deployed", {"endpoint": "/predict", "version": "2.0"})
bus.publish("model.error", {"error": "OOM"})  # Nadie escucha esto


print("\n" + "=" * 80)
print("=== CAPITULO 11: EJERCICIO — EXPERIMENT TRACKER COMPLETO ===")
print("=" * 80)

"""
Combinar Repository + Event Bus + Builder + Factory
en un tracker de experimentos completo.
"""

print("\n--- Experiment Tracker ---")

class ExperimentTracker:
    """Tracker que combina todos los patrones."""
    
    def __init__(self, repo: ExperimentRepository):
        self.repo = repo
        self.bus = EventBus()
        self._run_counter = 0
    
    def on(self, event_type: str):
        return self.bus.on(event_type)
    
    def log_run(self, modelo: str, accuracy: float, loss: float,
                config: dict = None) -> ExperimentRecord:
        self._run_counter += 1
        exp = ExperimentRecord(
            id=f"run_{self._run_counter:04d}",
            modelo=modelo,
            accuracy=accuracy,
            loss=loss,
            config=config or {}
        )
        self.repo.save(exp)
        self.bus.publish("run.logged", {"id": exp.id, "modelo": modelo,
                                        "accuracy": accuracy})
        return exp
    
    def best_run(self) -> Optional[ExperimentRecord]:
        return self.repo.find_best("accuracy")
    
    def summary(self) -> dict:
        runs = self.repo.list_all()
        if not runs:
            return {}
        accs = [r.accuracy for r in runs]
        return {
            "total_runs": len(runs),
            "best_accuracy": max(accs),
            "mean_accuracy": sum(accs) / len(accs),
            "models_used": list(set(r.modelo for r in runs)),
        }

tracker = ExperimentTracker(InMemoryRepository())

@tracker.on("run.logged")
def on_run(event, data):
    print(f"    [TRACKER] Run {data['id']}: {data['modelo']} acc={data['accuracy']:.3f}")

# Simular experimentos
for modelo in ["BERT", "GPT", "T5", "BERT", "GPT"]:
    acc = random.uniform(0.75, 0.98)
    loss = random.uniform(0.05, 0.4)
    tracker.log_run(modelo, acc, loss, {"lr": 0.001})

print(f"\n  Summary: {tracker.summary()}")
print(f"  Best: {tracker.best_run()}")


print("\n" + "=" * 80)
print("=== CAPITULO 12: ITERATOR PATTERN AVANZADO ===")
print("=" * 80)

"""
El patron Iterator en Python se implementa con __iter__ y __next__.
Permite recorrer colecciones complejas de forma uniforme.
"""

print("\n--- Iterator para batching de datos ---")

class BatchIterator:
    """Itera sobre datos en batches de tamano fijo."""
    
    def __init__(self, datos: list, batch_size: int = 32):
        self._datos = datos
        self._batch_size = batch_size
        self._index = 0
    
    def __iter__(self):
        self._index = 0
        return self
    
    def __next__(self) -> list:
        if self._index >= len(self._datos):
            raise StopIteration
        batch = self._datos[self._index:self._index + self._batch_size]
        self._index += self._batch_size
        return batch
    
    def __len__(self) -> int:
        import math
        return math.ceil(len(self._datos) / self._batch_size)

datos_training = list(range(107))
batches = BatchIterator(datos_training, batch_size=32)

print(f"  Total items: {len(datos_training)}")
print(f"  Total batches: {len(batches)}")
for i, batch in enumerate(batches):
    print(f"  Batch {i}: {len(batch)} items [{batch[0]}..{batch[-1]}]")


print("\n--- Iterator infinito para data augmentation ---")

class InfiniteAugmenter:
    """Itera infinitamente sobre datos con augmentation."""
    
    def __init__(self, datos: list, seed: int = 42):
        self._datos = datos
        self._rng = random.Random(seed)
        self._epoch = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self._datos:
            raise StopIteration
        self._epoch += 1
        item = self._rng.choice(self._datos)
        noise = self._rng.gauss(0, 0.01)
        return item + noise

aug = InfiniteAugmenter([1.0, 2.0, 3.0])
samples = [next(aug) for _ in range(8)]
print(f"  8 muestras augmentadas: {[f'{s:.3f}' for s in samples]}")


print("\n" + "=" * 80)
print("=== CAPITULO 13: CALLABLE PROTOCOL Y STRATEGY CON FUNCIONES ===")
print("=" * 80)

"""
En Python, Strategy no requiere clases: funciones son first-class.
Callable Protocol tipifica funciones que siguen un contrato.
"""

print("\n--- Strategy con funciones simples ---")

@runtime_checkable
class LossFunction(Protocol):
    def __call__(self, y_true: list, y_pred: list) -> float: ...

def mse_loss(y_true: list, y_pred: list) -> float:
    return sum((a - b)**2 for a, b in zip(y_true, y_pred)) / len(y_true)

def mae_loss(y_true: list, y_pred: list) -> float:
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)

def huber_loss(y_true: list, y_pred: list, delta: float = 1.0) -> float:
    total = 0
    for a, b in zip(y_true, y_pred):
        error = abs(a - b)
        if error <= delta:
            total += 0.5 * error**2
        else:
            total += delta * (error - 0.5 * delta)
    return total / len(y_true)

def evaluar_con_loss(loss_fn: LossFunction, y_true: list, y_pred: list) -> dict:
    """Acepta cualquier callable que cumpla LossFunction."""
    valor = loss_fn(y_true, y_pred)
    return {"loss": loss_fn.__name__, "valor": valor}

y_true_test = [1.0, 2.0, 3.0, 4.0]
y_pred_test = [1.1, 2.3, 2.8, 4.2]

for fn in [mse_loss, mae_loss, huber_loss]:
    r = evaluar_con_loss(fn, y_true_test, y_pred_test)
    print(f"  {r['loss']}: {r['valor']:.4f}")


print("\n--- Registry de funciones con decorador ---")

LOSS_REGISTRY: dict[str, LossFunction] = {}

def register_loss(name: str):
    def decorator(fn):
        LOSS_REGISTRY[name] = fn
        return fn
    return decorator

@register_loss("cross_entropy")
def cross_entropy_loss(y_true, y_pred):
    import math
    eps = 1e-7
    total = 0
    for t, p in zip(y_true, y_pred):
        p = max(eps, min(1 - eps, p))
        total -= t * math.log(p) + (1 - t) * math.log(1 - p)
    return total / len(y_true)

@register_loss("hinge")
def hinge_loss(y_true, y_pred):
    return sum(max(0, 1 - t * p) for t, p in zip(y_true, y_pred)) / len(y_true)

print(f"\n  Loss functions registradas: {list(LOSS_REGISTRY.keys())}")
for name, fn in LOSS_REGISTRY.items():
    val = fn([1, 0, 1, 0], [0.9, 0.2, 0.8, 0.3])
    print(f"  {name}: {val:.4f}")


print("\n" + "=" * 80)
print("=== CAPITULO 14: GUIA DE SELECCION DE PATRONES ===")
print("=" * 80)

print("""
+---------------------+------------------------------------+---------------------+
| NECESIDAD           | PATRON                             | EJEMPLO ML          |
+---------------------+------------------------------------+---------------------+
| Crear objetos       | Factory + Registry                 | ModelFactory         |
| Algoritmo variable  | Strategy (clase o funcion)         | LossFunction         |
| Notificar cambios   | Observer / Event Bus               | Training callbacks   |
| Instancia unica     | Singleton                          | AppConfig            |
| Objeto complejo     | Builder                            | PipelineBuilder      |
| Validar en cadena   | Chain of Responsibility            | InputValidator       |
| Abstraer datos      | Repository                         | ExperimentRepo       |
| Acceso controlado   | Proxy                              | LazyModelProxy       |
| Interfaz diferente  | Adapter                            | KerasAdapter         |
| Desacoplar eventos  | Event Bus                          | ExperimentTracker    |
| Iterar colecciones  | Iterator                           | BatchIterator        |
| Tipado generico     | TypeVar + Generic                  | Cache[K, V]          |
+---------------------+------------------------------------+---------------------+
""")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE PATRONES DE DISENO PARA ML:

1. Factory + Registry: crear objetos por nombre con decoradores.

2. Strategy: intercambiar algoritmos (clases O funciones).

3. Observer: callbacks de training. EarlyStopping, Logger.

4. Singleton: configuracion global unica.

5. Builder: construir objetos complejos paso a paso.

6. Chain of Responsibility: validacion en cadena.

7. Repository: abstraer acceso a datos.

8. Event Bus: desacoplar emisores de receptores.

9. Iterator: batching, augmentation infinita.

10. Callable Protocol: tipificar funciones como strategies.

11. Composicion de patrones = frameworks profesionales.

FIN DEL MODULO 05: POO Y DISENO PROFESIONAL.
"""

print("\n FIN DE ARCHIVO 03_patrones_diseno_y_type_hints.")
print(" Los patrones para ML profesional han sido dominados.")
print(" Siguiente modulo: 06_Errores_Testing_Y_Robustez.")
