# ===========================================================================
# 02_herencia_composicion_y_solid.py
# ===========================================================================
# MODULO 05: POO Y DISENO PROFESIONAL
# ARCHIVO 02: Herencia, Composicion, ABC, Protocols y Principios SOLID
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar herencia vs composicion, clases abstractas (ABC), protocols
# para duck typing tipado, y los principios SOLID aplicados a ML.
#
# CONTENIDO:
#   1. Herencia: simple, super(), MRO.
#   2. ABC: clases abstractas para interfaces.
#   3. Protocol: duck typing con type hints.
#   4. Composicion vs Herencia: cuando usar cada una.
#   5. Mixins: reutilizar funcionalidad sin herencia profunda.
#   6. SOLID: Single Responsibility, Open/Closed, Liskov, Interface
#      Segregation, Dependency Inversion.
#   7. Ejercicio: Pipeline ML con SOLID.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import time
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Any, Optional
from dataclasses import dataclass, field


# =====================================================================
#   PARTE 1: HERENCIA
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: HERENCIA SIMPLE ===")
print("=" * 80)

"""
Herencia: una clase (hija) hereda atributos y metodos de otra (padre).
La clase hija PUEDE sobrescribir metodos del padre.

super() llama al metodo del padre.
"""

print("\n--- Herencia basica ---")

class ModeloBase:
    """Clase base para todos los modelos ML."""
    
    def __init__(self, nombre: str, version: str = "1.0"):
        self.nombre = nombre
        self.version = version
        self._entrenado = False
    
    def entrenar(self, datos: list):
        print(f"  [{self.nombre}] Entrenando con {len(datos)} datos...")
        self._entrenado = True
    
    def predecir(self, x):
        if not self._entrenado:
            raise RuntimeError(f"{self.nombre} no esta entrenado")
        return None  # Subclases implementan esto
    
    def __repr__(self):
        estado = "entrenado" if self._entrenado else "sin entrenar"
        return f"{self.__class__.__name__}('{self.nombre}', v{self.version}, {estado})"


class ModeloLineal(ModeloBase):
    """Modelo lineal: hereda de ModeloBase."""
    
    def __init__(self, nombre: str, n_features: int):
        super().__init__(nombre)  # Llama __init__ del padre
        self.n_features = n_features
        self.pesos = [0.0] * n_features
    
    def entrenar(self, datos: list):
        super().entrenar(datos)  # Llama entrenar() del padre
        # Logica especifica
        import random
        self.pesos = [random.gauss(0, 0.1) for _ in range(self.n_features)]
        print(f"  [{self.nombre}] Pesos ajustados: {len(self.pesos)} features")
    
    def predecir(self, x: list) -> float:
        super().predecir(x)  # Verifica entrenado
        return sum(w * xi for w, xi in zip(self.pesos, x))


class ModeloEnsemble(ModeloBase):
    """Ensemble: combina varios modelos."""
    
    def __init__(self, nombre: str, modelos: list):
        super().__init__(nombre)
        self.modelos = modelos
    
    def entrenar(self, datos: list):
        for modelo in self.modelos:
            modelo.entrenar(datos)
        self._entrenado = True
    
    def predecir(self, x) -> float:
        super().predecir(x)
        preds = [m.predecir(x) for m in self.modelos]
        return sum(preds) / len(preds)

# Uso
lineal = ModeloLineal("LinearReg", 3)
lineal.entrenar([1, 2, 3, 4, 5])
pred = lineal.predecir([0.5, 1.0, -0.3])
print(f"\n  {lineal}")
print(f"  Prediccion: {pred:.4f}")

# isinstance verifica herencia
print(f"\n  isinstance(lineal, ModeloBase): {isinstance(lineal, ModeloBase)}")
print(f"  isinstance(lineal, ModeloLineal): {isinstance(lineal, ModeloLineal)}")


print("\n" + "=" * 80)
print("=== CAPITULO 2: MRO — METHOD RESOLUTION ORDER ===")
print("=" * 80)

"""
MRO: el orden en que Python busca metodos en la jerarquia de herencia.
Python usa el algoritmo C3 linearization.

Se puede ver con: Clase.__mro__ o Clase.mro()
"""

print("\n--- MRO con herencia multiple ---")

class A:
    def metodo(self):
        return "A"

class B(A):
    def metodo(self):
        return "B"

class C(A):
    def metodo(self):
        return "C"

class D(B, C):
    pass  # Hereda de B y C

d = D()
print(f"  D().metodo() = '{d.metodo()}'")
print(f"  MRO: {[cls.__name__ for cls in D.__mro__]}")


# =====================================================================
#   PARTE 2: CLASES ABSTRACTAS (ABC)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: ABC — CLASES ABSTRACTAS ===")
print("=" * 80)

"""
ABC (Abstract Base Class) define una INTERFAZ que las subclases
DEBEN implementar. No puedes instanciar una ABC directamente.

@abstractmethod marca metodos que DEBEN ser sobrescritos.

EN ML: definir interfaces para modelos, metricas, datasets, etc.
"""

print("\n--- ABC para modelos ML ---")

class ModeloABC(ABC):
    """Interfaz abstracta para modelos ML."""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
    
    @abstractmethod
    def fit(self, X: list, y: list) -> None:
        """Entrenar el modelo. DEBE ser implementado."""
        ...
    
    @abstractmethod
    def predict(self, X: list) -> list:
        """Predecir. DEBE ser implementado."""
        ...
    
    @abstractmethod
    def score(self, X: list, y: list) -> float:
        """Evaluar. DEBE ser implementado."""
        ...
    
    def resumen(self) -> str:
        """Metodo concreto: NO necesita ser sobrescrito."""
        return f"{self.__class__.__name__}('{self.nombre}')"

# No puedes instanciar una ABC
try:
    m = ModeloABC("test")
except TypeError as e:
    print(f"  No se puede instanciar ABC: {e}")


class RegresionLineal(ModeloABC):
    """Implementacion concreta de ModeloABC."""
    
    def __init__(self, nombre: str = "LinearReg"):
        super().__init__(nombre)
        self.coefs = []
    
    def fit(self, X: list, y: list) -> None:
        import random
        self.coefs = [random.gauss(0, 0.1) for _ in range(len(X[0]))]
        print(f"  [{self.nombre}] Entrenado con {len(X)} muestras")
    
    def predict(self, X: list) -> list:
        return [sum(c * xi for c, xi in zip(self.coefs, x)) for x in X]
    
    def score(self, X: list, y: list) -> float:
        preds = self.predict(X)
        errors = [(p - yi)**2 for p, yi in zip(preds, y)]
        return 1.0 - sum(errors) / len(errors)

reg = RegresionLineal()
X = [[1, 2], [3, 4], [5, 6]]
y = [3, 7, 11]
reg.fit(X, y)
print(f"  Predicciones: {[f'{p:.2f}' for p in reg.predict(X)]}")
print(f"  Resumen: {reg.resumen()}")


# =====================================================================
#   PARTE 3: PROTOCOLS (DUCK TYPING TIPADO)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: PROTOCOLS — DUCK TYPING CON TIPOS ===")
print("=" * 80)

"""
Protocol (Python 3.8+) define una interfaz SIN herencia.
Es duck typing con type hints: "si tiene estos metodos, es valido".

Diferencia con ABC:
- ABC: la clase DEBE heredar explicitamente.
- Protocol: la clase solo debe tener los metodos correctos.

Protocol es mas flexible y pythonic que ABC.
"""

print("\n--- Protocol para cualquier cosa predecible ---")

@runtime_checkable
class Predictable(Protocol):
    """Cualquier objeto con predict() es Predictable."""
    
    def predict(self, X: list) -> list:
        ...

@runtime_checkable
class Trainable(Protocol):
    """Cualquier objeto con fit() es Trainable."""
    
    def fit(self, X: list, y: list) -> None:
        ...

# Esta clase NO hereda de Predictable, pero cumple el protocolo
class RandomPredictor:
    def predict(self, X: list) -> list:
        import random
        return [random.random() for _ in X]

# isinstance funciona con @runtime_checkable
rp = RandomPredictor()
print(f"  RandomPredictor es Predictable: {isinstance(rp, Predictable)}")
print(f"  RandomPredictor es Trainable:   {isinstance(rp, Trainable)}")
print(f"  RegresionLineal es Predictable: {isinstance(reg, Predictable)}")
print(f"  RegresionLineal es Trainable:   {isinstance(reg, Trainable)}")

def evaluar_modelo(modelo: Predictable, X: list, y: list) -> float:
    """Acepta CUALQUIER objeto con predict(). Duck typing tipado."""
    preds = modelo.predict(X)
    error = sum((p - yi)**2 for p, yi in zip(preds, y)) / len(y)
    return error

print(f"\n  Error RandomPredictor: {evaluar_modelo(rp, X, y):.4f}")
print(f"  Error RegresionLineal: {evaluar_modelo(reg, X, y):.4f}")


# =====================================================================
#   PARTE 4: COMPOSICION VS HERENCIA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: COMPOSICION > HERENCIA ===")
print("=" * 80)

"""
REGLA DE ORO: "Favor composition over inheritance."

HERENCIA: "es un" (is-a). Perro ES UN Animal.
COMPOSICION: "tiene un" (has-a). Coche TIENE UN Motor.

Problemas de herencia profunda:
- Acoplamiento fuerte.
- Fragilidad: cambio en padre rompe hijos.
- Diamond problem con herencia multiple.

Composicion es MAS FLEXIBLE: cambias componentes sin tocar la clase.
"""

print("\n--- Composicion: Pipeline ML ---")

class Tokenizer:
    """Componente de tokenizacion."""
    def __init__(self, tipo: str = "word"):
        self.tipo = tipo
    def tokenize(self, texto: str) -> list:
        if self.tipo == "word":
            return texto.lower().split()
        elif self.tipo == "char":
            return list(texto.lower())
        return [texto]

class Vectorizer:
    """Componente de vectorizacion."""
    def __init__(self, dim: int = 100):
        self.dim = dim
    def vectorize(self, tokens: list) -> list:
        return [len(t) / 10.0 for t in tokens[:self.dim]]

class Classifier:
    """Componente de clasificacion."""
    def classify(self, vector: list) -> str:
        score = sum(vector) / max(len(vector), 1)
        return "positivo" if score > 0.4 else "negativo"

class TextPipeline:
    """Pipeline que COMPONE componentes (no hereda)."""
    
    def __init__(self, tokenizer: Tokenizer, vectorizer: Vectorizer,
                 classifier: Classifier):
        self.tokenizer = tokenizer
        self.vectorizer = vectorizer
        self.classifier = classifier
    
    def procesar(self, texto: str) -> dict:
        tokens = self.tokenizer.tokenize(texto)
        vector = self.vectorizer.vectorize(tokens)
        label = self.classifier.classify(vector)
        return {"texto": texto[:30], "n_tokens": len(tokens), "label": label}

# Cambiar componentes sin tocar TextPipeline
pipeline_word = TextPipeline(Tokenizer("word"), Vectorizer(50), Classifier())
pipeline_char = TextPipeline(Tokenizer("char"), Vectorizer(50), Classifier())

texto = "Machine learning es fantastico para NLP"
print(f"  Word pipeline: {pipeline_word.procesar(texto)}")
print(f"  Char pipeline: {pipeline_char.procesar(texto)}")


# =====================================================================
#   PARTE 5: MIXINS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: MIXINS — REUTILIZAR SIN HERENCIA PROFUNDA ===")
print("=" * 80)

"""
Un Mixin es una clase que proporciona funcionalidad adicional
SIN ser una clase base principal. Es herencia "horizontal".

Reglas de Mixins:
1. NO tienen __init__ (o llaman super().__init__).
2. Proporcionan metodos utilitarios.
3. Se nombran con sufijo Mixin.
"""

print("\n--- Mixins para modelos ML ---")

class SerializableMixin:
    """Mixin que agrega serializacion JSON."""
    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict(), default=str)

class LoggableMixin:
    """Mixin que agrega logging."""
    def log(self, mensaje: str, nivel: str = "INFO"):
        print(f"  [{nivel}] [{self.__class__.__name__}] {mensaje}")

class MetricsMixin:
    """Mixin que agrega tracking de metricas."""
    def __init_metrics(self):
        if not hasattr(self, '_metricas_historial'):
            self._metricas_historial = []
    
    def registrar_metrica(self, nombre: str, valor: float):
        self.__init_metrics()
        self._metricas_historial.append({"metrica": nombre, "valor": valor})
    
    def obtener_metricas(self) -> list:
        self.__init_metrics()
        return self._metricas_historial

class SmartModel(ModeloBase, SerializableMixin, LoggableMixin, MetricsMixin):
    """Modelo que usa TODOS los mixins."""
    
    def entrenar(self, datos):
        self.log("Iniciando entrenamiento")
        super().entrenar(datos)
        self.registrar_metrica("loss", 0.5)
        self.registrar_metrica("accuracy", 0.85)
        self.log(f"Metricas: {self.obtener_metricas()}")

smart = SmartModel("SmartBERT")
smart.entrenar([1, 2, 3, 4, 5])
print(f"  JSON: {smart.to_json()}")
print(f"  Metricas: {smart.obtener_metricas()}")


# =====================================================================
#   PARTE 6: PRINCIPIOS SOLID
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: SOLID — LOS 5 PRINCIPIOS ===")
print("=" * 80)

"""
S - Single Responsibility: una clase, una razon para cambiar.
O - Open/Closed: abierto a extension, cerrado a modificacion.
L - Liskov Substitution: subclases sustituibles por padre.
I - Interface Segregation: interfaces pequenas y especificas.
D - Dependency Inversion: depender de abstracciones, no implementaciones.
"""

print("\n--- S: Single Responsibility ---")

# MAL: una clase hace todo
class ModeloMonolito:
    def cargar_datos(self): pass
    def preprocesar(self): pass
    def entrenar(self): pass
    def evaluar(self): pass
    def guardar(self): pass
    def enviar_email(self): pass  # No es responsabilidad del modelo

# BIEN: cada clase tiene UNA responsabilidad
class DataLoader:
    def cargar(self, path: str) -> list:
        return [{"data": i} for i in range(100)]

class Preprocessor:
    def procesar(self, datos: list) -> list:
        return [d for d in datos if d]

class Trainer:
    def entrenar(self, modelo, datos):
        print(f"    Entrenando {modelo} con {len(datos)} datos")

class Evaluator:
    def evaluar(self, modelo, datos) -> float:
        return 0.92

print("  SRP: DataLoader, Preprocessor, Trainer, Evaluator separados")


print("\n--- O: Open/Closed ---")

# Abierto a extension: agregar nuevas metricas sin modificar Evaluator

class MetricaBase(ABC):
    @abstractmethod
    def calcular(self, y_true: list, y_pred: list) -> float: ...
    @abstractmethod
    def nombre(self) -> str: ...

class Accuracy(MetricaBase):
    def calcular(self, y_true, y_pred) -> float:
        return sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true)
    def nombre(self) -> str:
        return "accuracy"

class MSE(MetricaBase):
    def calcular(self, y_true, y_pred) -> float:
        return sum((a - b)**2 for a, b in zip(y_true, y_pred)) / len(y_true)
    def nombre(self) -> str:
        return "mse"

class EvaluadorOC:
    """Cerrado a modificacion: acepta CUALQUIER MetricaBase."""
    def evaluar(self, y_true, y_pred, metricas: list[MetricaBase]) -> dict:
        return {m.nombre(): m.calcular(y_true, y_pred) for m in metricas}

ev = EvaluadorOC()
y_true = [1, 0, 1, 1, 0]
y_pred = [1, 0, 0, 1, 0]
resultados = ev.evaluar(y_true, y_pred, [Accuracy(), MSE()])
print(f"  O/C: {resultados}")


print("\n--- L: Liskov Substitution ---")

# Si RegresionLineal hereda de ModeloABC, debe ser usable
# en CUALQUIER lugar donde se use ModeloABC
def pipeline_generico(modelo: ModeloABC, X, y):
    """Funciona con CUALQUIER subclase de ModeloABC."""
    modelo.fit(X, y)
    preds = modelo.predict(X)
    score = modelo.score(X, y)
    return score

s = pipeline_generico(RegresionLineal("test"), X, y)
print(f"  Liskov: score = {s:.4f}")


print("\n--- I: Interface Segregation ---")

# MAL: interfaz gorda
class ModeloGordo(ABC):
    @abstractmethod
    def fit(self): ...
    @abstractmethod
    def predict(self): ...
    @abstractmethod
    def plot(self): ...  # No todos los modelos plotean
    @abstractmethod
    def export_onnx(self): ...  # No todos exportan

# BIEN: interfaces pequenas
class Fittable(Protocol):
    def fit(self, X, y) -> None: ...

class Predictable2(Protocol):
    def predict(self, X) -> list: ...

class Exportable(Protocol):
    def export(self, formato: str) -> bytes: ...

print("  ISP: Fittable, Predictable, Exportable por separado")


print("\n--- D: Dependency Inversion ---")

# MAL: depender de implementacion concreta
class PipelineMal:
    def __init__(self):
        self.modelo = RegresionLineal()  # Acoplado a implementacion

# BIEN: depender de abstraccion
class PipelineBien:
    def __init__(self, modelo: ModeloABC):  # Depende de abstraccion
        self.modelo = modelo
    
    def ejecutar(self, X, y):
        self.modelo.fit(X, y)
        return self.modelo.predict(X)

# Puedo inyectar cualquier modelo
p = PipelineBien(RegresionLineal("DI_test"))
resultado = p.ejecutar(X, y)
print(f"  DI: {[f'{r:.2f}' for r in resultado]}")


# =====================================================================
#   PARTE 7: EJERCICIO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: EJERCICIO — PIPELINE ML CON SOLID ===")
print("=" * 80)

"""
Construir un pipeline ML que siga TODOS los principios SOLID.
"""

print("\n--- Pipeline SOLID ---")

@runtime_checkable
class Transformer(Protocol):
    def transform(self, datos: list) -> list: ...

@runtime_checkable
class FitTransformer(Protocol):
    def fit(self, datos: list) -> None: ...
    def transform(self, datos: list) -> list: ...

class NormalizadorMinMax:
    def __init__(self):
        self.min_val = None
        self.max_val = None
    
    def fit(self, datos: list):
        self.min_val = min(datos)
        self.max_val = max(datos)
    
    def transform(self, datos: list) -> list:
        rango = self.max_val - self.min_val
        if rango == 0:
            return [0.0] * len(datos)
        return [(x - self.min_val) / rango for x in datos]

class FiltroOutliers:
    def __init__(self, n_sigma: float = 2.0):
        self.n_sigma = n_sigma
        self.media = None
        self.std = None
    
    def fit(self, datos: list):
        self.media = sum(datos) / len(datos)
        var = sum((x - self.media)**2 for x in datos) / len(datos)
        self.std = var ** 0.5
    
    def transform(self, datos: list) -> list:
        return [x for x in datos if abs(x - self.media) <= self.n_sigma * self.std]

class SOLIDPipeline:
    """Pipeline que acepta cualquier FitTransformer via DI."""
    
    def __init__(self, pasos: list[tuple[str, Any]]):
        self.pasos = pasos
    
    def fit_transform(self, datos: list) -> list:
        resultado = datos
        for nombre, paso in self.pasos:
            if hasattr(paso, 'fit'):
                paso.fit(resultado)
            resultado = paso.transform(resultado)
            print(f"  [{nombre}] {len(datos)} -> {len(resultado)} items")
        return resultado

import random
random.seed(42)
datos_raw = [random.gauss(50, 15) for _ in range(100)]
datos_raw.extend([200, -100])  # outliers

pipeline = SOLIDPipeline([
    ("FiltroOutliers", FiltroOutliers(2.0)),
    ("Normalizar", NormalizadorMinMax()),
])

resultado = pipeline.fit_transform(datos_raw)
print(f"\n  Entrada: {len(datos_raw)} valores")
print(f"  Salida:  {len(resultado)} valores")
print(f"  Rango:   [{min(resultado):.2f}, {max(resultado):.2f}]")


print("\n" + "=" * 80)
print("=== CAPITULO 9: ABSTRACT PROPERTIES Y CLASSMETHODS ===")
print("=" * 80)

"""
Las ABCs pueden definir abstract properties y abstract classmethods.
Las subclases DEBEN implementarlos.
"""

print("\n--- Abstract properties ---")

class DatasetABC(ABC):
    """Interfaz abstracta para datasets."""
    
    @property
    @abstractmethod
    def size(self) -> int:
        """Numero de muestras. DEBE implementarse."""
        ...
    
    @property
    @abstractmethod
    def features_dim(self) -> int:
        """Dimension de features. DEBE implementarse."""
        ...
    
    @abstractmethod
    def __getitem__(self, idx: int) -> dict:
        ...
    
    @classmethod
    @abstractmethod
    def from_file(cls, path: str):
        """Factory method abstracto."""
        ...
    
    def info(self) -> str:
        return f"{self.__class__.__name__}(size={self.size}, dim={self.features_dim})"

class CSVDataset(DatasetABC):
    def __init__(self, datos: list[list], labels: list):
        self._datos = datos
        self._labels = labels
    
    @property
    def size(self) -> int:
        return len(self._datos)
    
    @property
    def features_dim(self) -> int:
        return len(self._datos[0]) if self._datos else 0
    
    def __getitem__(self, idx):
        return {"features": self._datos[idx], "label": self._labels[idx]}
    
    @classmethod
    def from_file(cls, path: str):
        # Simulacion
        datos = [[i * 0.1, i * 0.2] for i in range(50)]
        labels = [i % 2 for i in range(50)]
        return cls(datos, labels)

ds = CSVDataset.from_file("datos.csv")
print(f"  {ds.info()}")
print(f"  ds[0]: {ds[0]}")


print("\n" + "=" * 80)
print("=== CAPITULO 10: HERENCIA COOPERATIVA CON SUPER() ===")
print("=" * 80)

"""
En herencia multiple, super() sigue el MRO para llamar
a todos los padres en orden correcto. Cada clase solo
llama a la SIGUIENTE en el MRO, no directamente al padre.
"""

print("\n--- Cooperativa con super() ---")

class ComponenteBase:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inicializado = True

class ConLog(ComponenteBase):
    def __init__(self, log_level="INFO", **kwargs):
        super().__init__(**kwargs)
        self.log_level = log_level
        print(f"    ConLog init: log_level={log_level}")

class ConCache(ComponenteBase):
    def __init__(self, cache_size=100, **kwargs):
        super().__init__(**kwargs)
        self.cache_size = cache_size
        print(f"    ConCache init: cache_size={cache_size}")

class ConValidacion(ComponenteBase):
    def __init__(self, strict=True, **kwargs):
        super().__init__(**kwargs)
        self.strict = strict
        print(f"    ConValidacion init: strict={strict}")

class ServicioCompleto(ConLog, ConCache, ConValidacion):
    """Hereda de 3 mixins cooperativos."""
    def __init__(self, nombre, **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre
        print(f"    ServicioCompleto init: {nombre}")

print("  Creando ServicioCompleto:")
svc = ServicioCompleto("ml-api", log_level="DEBUG", cache_size=500, strict=False)
print(f"\n  MRO: {[c.__name__ for c in ServicioCompleto.__mro__]}")
print(f"  log_level: {svc.log_level}")
print(f"  cache_size: {svc.cache_size}")
print(f"  strict: {svc.strict}")


print("\n" + "=" * 80)
print("=== CAPITULO 11: ADAPTER PATTERN ===")
print("=" * 80)

"""
Adapter: hacer que una clase con interfaz incompatible
funcione donde se espera otra interfaz.
Util para integrar librerias externas.
"""

print("\n--- Adapter para modelos de diferentes frameworks ---")

class SklearnModel:
    """Modelo que usa la API de sklearn (fit/predict)."""
    def fit(self, X, y):
        self.media = sum(y) / len(y)
    def predict(self, X):
        return [self.media] * len(X)

class KerasModel:
    """Modelo que usa la API de Keras (compile/fit/evaluate)."""
    def compile(self, optimizer="adam"):
        self.optimizer = optimizer
    def fit_model(self, X, y, epochs=1):  # Diferente nombre!
        self.weights = [0.5]
    def predict_proba(self, X):  # Diferente nombre!
        return [0.5] * len(X)

class KerasAdapter(ModeloABC):
    """Adapter: convierte KerasModel a interfaz ModeloABC."""
    
    def __init__(self, keras_model: KerasModel, nombre: str = "keras_adapted"):
        super().__init__(nombre)
        self._model = keras_model
        self._model.compile()
    
    def fit(self, X, y):
        self._model.fit_model(X, y)
        print(f"  [{self.nombre}] Adaptado fit_model -> fit")
    
    def predict(self, X):
        preds = self._model.predict_proba(X)
        print(f"  [{self.nombre}] Adaptado predict_proba -> predict")
        return preds
    
    def score(self, X, y):
        preds = self.predict(X)
        return 1.0 - sum((p-yi)**2 for p, yi in zip(preds, y)) / len(y)

keras_m = KerasModel()
adapter = KerasAdapter(keras_m, "keras_bert")

# Ahora funciona con pipeline_generico que espera ModeloABC
score = pipeline_generico(adapter, X, y)
print(f"  Score via adapter: {score:.4f}")


print("\n" + "=" * 80)
print("=== CAPITULO 12: EJERCICIO — MODEL LIFECYCLE ===")
print("=" * 80)

"""
Implementar un lifecycle completo de modelo usando composicion,
ABC, protocols y SOLID.
"""

from enum import Enum, auto

class Phase(Enum):
    CREATED = auto()
    VALIDATED = auto()
    TRAINED = auto()
    EVALUATED = auto()
    DEPLOYED = auto()

@runtime_checkable
class Validatable(Protocol):
    def validate(self, datos: list) -> bool: ...

@runtime_checkable
class Deployable(Protocol):
    def deploy(self, target: str) -> dict: ...

class ModelLifecycle:
    """Gestiona el lifecycle de un modelo con transiciones validas."""
    
    TRANSITIONS = {
        Phase.CREATED: [Phase.VALIDATED],
        Phase.VALIDATED: [Phase.TRAINED],
        Phase.TRAINED: [Phase.EVALUATED],
        Phase.EVALUATED: [Phase.DEPLOYED, Phase.TRAINED],
        Phase.DEPLOYED: [Phase.TRAINED],
    }
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.phase = Phase.CREATED
        self.historial = []
    
    def transition_to(self, target: Phase):
        allowed = self.TRANSITIONS.get(self.phase, [])
        if target not in allowed:
            raise ValueError(
                f"No se puede ir de {self.phase.name} a {target.name}. "
                f"Permitido: {[p.name for p in allowed]}"
            )
        old = self.phase
        self.phase = target
        self.historial.append(f"{old.name} -> {target.name}")
        print(f"  [{self.nombre}] {old.name} -> {target.name}")
    
    def __repr__(self):
        return f"ModelLifecycle('{self.nombre}', phase={self.phase.name})"

print("\n--- Model Lifecycle ---")
lc = ModelLifecycle("bert_v2")
print(f"  {lc}")

lc.transition_to(Phase.VALIDATED)
lc.transition_to(Phase.TRAINED)
lc.transition_to(Phase.EVALUATED)
lc.transition_to(Phase.DEPLOYED)
print(f"  {lc}")
print(f"  Historial: {lc.historial}")

# Transicion invalida
try:
    lc2 = ModelLifecycle("test")
    lc2.transition_to(Phase.DEPLOYED)
except ValueError as e:
    print(f"  Error: {e}")


print("\n" + "=" * 80)
print("=== CAPITULO 13: PROXY PATTERN ===")
print("=" * 80)

"""
Proxy: controla el acceso a un objeto. Util para:
- Lazy loading (cargar solo cuando se necesita).
- Caching transparente.
- Control de acceso / permisos.
"""

print("\n--- Lazy Loading Proxy ---")

class HeavyModel:
    """Modelo que tarda en cargarse (simulado)."""
    def __init__(self, nombre: str):
        print(f"    [HeavyModel] Cargando '{nombre}' (lento)...")
        self.nombre = nombre
        self.weights = [0.1] * 1000  # Simula pesos grandes
    
    def predict(self, x):
        return sum(x) * 0.1

class LazyModelProxy:
    """Proxy que carga el modelo solo cuando se necesita."""
    
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._model = None
    
    def _load(self):
        if self._model is None:
            self._model = HeavyModel(self._nombre)
    
    def predict(self, x):
        self._load()
        return self._model.predict(x)
    
    def __repr__(self):
        loaded = "cargado" if self._model else "no cargado"
        return f"LazyProxy('{self._nombre}', {loaded})"

proxy = LazyModelProxy("BERT-large")
print(f"  Proxy creado: {proxy}")
print(f"  (Modelo NO se ha cargado aun)")

result = proxy.predict([1, 2, 3])
print(f"  Prediccion: {result}")
print(f"  Proxy ahora: {proxy}")


print("\n" + "=" * 80)
print("=== CAPITULO 14: DI CONTAINER ===")
print("=" * 80)

"""
Dependency Injection Container: registra y resuelve dependencias
automaticamente. Base de frameworks como FastAPI.
"""

print("\n--- DI Container simple ---")

class DIContainer:
    """Contenedor de inyeccion de dependencias."""
    
    def __init__(self):
        self._factories = {}
        self._singletons = {}
    
    def register(self, interface, factory, singleton=False):
        self._factories[interface] = (factory, singleton)
        return self
    
    def resolve(self, interface):
        if interface not in self._factories:
            raise ValueError(f"No registrado: {interface}")
        
        factory, is_singleton = self._factories[interface]
        
        if is_singleton:
            if interface not in self._singletons:
                self._singletons[interface] = factory()
            return self._singletons[interface]
        
        return factory()

container = DIContainer()
container.register("config", lambda: {"lr": 0.001, "device": "cuda"}, singleton=True)
container.register("tokenizer", lambda: Tokenizer("word"))
container.register("classifier", Classifier)

cfg1 = container.resolve("config")
cfg2 = container.resolve("config")
print(f"  Config singleton: {cfg1 is cfg2}")

tk1 = container.resolve("tokenizer")
tk2 = container.resolve("tokenizer")
print(f"  Tokenizer no-singleton: {tk1 is tk2}")

cl = container.resolve("classifier")
print(f"  Classifier: {cl}")


print("\n" + "=" * 80)
print("=== CAPITULO 15: ANTI-PATRONES DE HERENCIA ===")
print("=" * 80)

"""
Anti-patrones comunes que deben evitarse:
"""

print("""
+---------------------------+-----------------------------------+
| ANTI-PATRON               | SOLUCION                          |
+---------------------------+-----------------------------------+
| God class (hace todo)     | SRP: dividir en clases            |
| Deep inheritance (>3)     | Composicion + Mixins              |
| isinstance() excesivo     | Polimorfismo / Protocol           |
| Circular dependencies     | DI Container / interfaces         |
| Herencia por reutilizar   | Composicion (has-a > is-a)        |
| Mixin sin super()         | Herencia cooperativa              |
| ABC cuando no necesario   | Protocol (duck typing)            |
| Singleton mutable global  | DI + configuracion explicita      |
+---------------------------+-----------------------------------+
""")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE HERENCIA, COMPOSICION Y SOLID:

1. Herencia: "es un". super() para llamar al padre. MRO con C3.

2. ABC: interfaces abstractas. Abstract properties y classmethods.

3. Protocol: duck typing tipado. NO requiere herencia.

4. Composicion > Herencia: mas flexible, menos acoplamiento.

5. Mixins cooperativos: super() sigue el MRO correctamente.

6. SOLID: SRP, OCP, LSP, ISP, DIP.

7. Adapter: convertir interfaces incompatibles.

8. Proxy: lazy loading, caching transparente.

9. DI Container: registrar y resolver dependencias.

10. Model Lifecycle: state machine con transiciones validas.

Siguiente archivo: Patrones de diseno para ML.
"""

print("\n FIN DE ARCHIVO 02_herencia_composicion_y_solid.")
print(" SOLID y composicion han sido dominados.")
