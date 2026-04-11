# ===========================================================================
# 01_clases_y_objetos_desde_cero.py
# ===========================================================================
# MODULO 05: POO Y DISENO PROFESIONAL
# ARCHIVO 01: Clases, Objetos, Atributos, Metodos y el Modelo de Datos
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar la POO de Python desde los cimientos: como Python implementa
# objetos internamente, el protocolo de datos (dunder methods),
# descriptores, slots, y patrones de inicializacion profesional.
#
# CONTENIDO:
#   1. Clases como plantillas de objetos.
#   2. __init__, __repr__, __str__, __eq__, __hash__.
#   3. Atributos de instancia vs clase. MRO.
#   4. Encapsulacion: convenciones _, __ y properties.
#   5. __slots__: optimizacion de memoria.
#   6. Dataclasses: POO moderna sin boilerplate.
#   7. Dunder methods: __len__, __getitem__, __contains__, __call__.
#   8. Ejercicio: Dataset class con protocolo de datos completo.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import sys
import time
from typing import Any, Optional
from dataclasses import dataclass, field, asdict, astuple


# =====================================================================
#   PARTE 1: CLASES COMO PLANTILLAS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: CLASES Y OBJETOS DESDE CERO ===")
print("=" * 80)

"""
En Python, TODO es un objeto: ints, strings, funciones, modulos.
Una clase es una PLANTILLA para crear objetos.

class MiClase:
    ...

obj = MiClase()  # Instanciacion: crea un objeto a partir de la plantilla.

Internamente, Python:
1. Llama MiClase.__new__(MiClase) para crear la instancia.
2. Llama MiClase.__init__(instancia) para inicializarla.
3. Retorna la instancia.
"""

print("\n--- Clase minima ---")

class Punto:
    """Representa un punto en 2D."""
    
    def __init__(self, x: float, y: float):
        self.x = x  # Atributo de instancia
        self.y = y
    
    def distancia_al_origen(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5
    
    def __repr__(self) -> str:
        return f"Punto({self.x}, {self.y})"
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

p1 = Punto(3, 4)
p2 = Punto(0, 0)

print(f"  repr(p1): {repr(p1)}")
print(f"  str(p1):  {str(p1)}")
print(f"  Distancia al origen: {p1.distancia_al_origen()}")
print(f"  type(p1): {type(p1)}")
print(f"  isinstance: {isinstance(p1, Punto)}")


print("\n" + "=" * 80)
print("=== CAPITULO 2: ATRIBUTOS DE INSTANCIA VS CLASE ===")
print("=" * 80)

"""
ATRIBUTO DE CLASE: compartido por TODAS las instancias.
ATRIBUTO DE INSTANCIA: unico para cada objeto.

Cuando accedes a obj.attr, Python busca:
1. En obj.__dict__ (atributos de instancia).
2. En type(obj).__dict__ (atributos de clase).
3. En las clases padre (MRO).
"""

print("\n--- Atributos de clase vs instancia ---")

class Modelo:
    """Modelo ML con atributos de clase e instancia."""
    
    # Atributo de clase: compartido
    framework = "PyTorch"
    total_creados = 0
    
    def __init__(self, nombre: str, version: str = "1.0"):
        # Atributos de instancia: unicos por objeto
        self.nombre = nombre
        self.version = version
        self.entrenado = False
        Modelo.total_creados += 1
    
    def __repr__(self):
        return f"Modelo('{self.nombre}', v{self.version})"

m1 = Modelo("BERT")
m2 = Modelo("GPT", "3.5")

print(f"  m1.framework: {m1.framework} (de clase)")
print(f"  m2.framework: {m2.framework} (de clase)")
print(f"  Total creados: {Modelo.total_creados}")

# Modificar atributo de clase vs instancia
m1.framework = "TensorFlow"  # Crea atributo de INSTANCIA en m1
print(f"\n  Tras m1.framework = 'TensorFlow':")
print(f"  m1.framework: {m1.framework} (instancia)")
print(f"  m2.framework: {m2.framework} (sigue siendo clase)")
print(f"  Modelo.framework: {Modelo.framework}")

# __dict__ muestra atributos de instancia
print(f"\n  m1.__dict__: {m1.__dict__}")
print(f"  m2.__dict__: {m2.__dict__}")


print("\n" + "=" * 80)
print("=== CAPITULO 3: __repr__ vs __str__ ===")
print("=" * 80)

"""
__repr__: representacion para DESARROLLADORES. Deberia ser inequivoca.
          Idealmente: eval(repr(obj)) == obj
__str__:  representacion para USUARIOS. Puede ser mas legible.

Si solo implementas uno, implementa __repr__. 
Python usa __repr__ como fallback si __str__ no existe.
"""

print("\n--- repr vs str ---")

class Embedding:
    def __init__(self, nombre: str, dim: int, valores: list):
        self.nombre = nombre
        self.dim = dim
        self.valores = valores
    
    def __repr__(self):
        return f"Embedding('{self.nombre}', dim={self.dim})"
    
    def __str__(self):
        preview = self.valores[:3]
        return f"[{self.nombre}] dim={self.dim}, preview={preview}..."

emb = Embedding("word2vec", 300, [0.1] * 300)
print(f"  repr: {repr(emb)}")
print(f"  str:  {str(emb)}")
print(f"  f-string: {emb}")  # Usa __str__
print(f"  En lista: {[emb]}")  # Usa __repr__


# =====================================================================
#   PARTE 2: DUNDER METHODS (PROTOCOLO DE DATOS)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: DUNDER METHODS — EL PROTOCOLO DE DATOS ===")
print("=" * 80)

"""
Los dunder methods (double underscore) permiten que tus objetos
se comporten como tipos nativos de Python:

COMPARACION: __eq__, __lt__, __le__, __gt__, __ge__, __ne__
HASH:        __hash__ (necesario para usar como key de dict/set)
LONGITUD:    __len__
INDEXACION:  __getitem__, __setitem__, __delitem__
ITERACION:   __iter__, __next__
CONTENCION:  __contains__ (para 'in')
LLAMADA:     __call__ (hacer que el objeto sea callable)
ARITMETICA:  __add__, __mul__, __sub__, etc.
CONTEXTO:    __enter__, __exit__ (para 'with')
"""

print("\n--- __eq__ y __hash__: igualdad y uso en dicts/sets ---")

class TokenInfo:
    """Informacion de un token con igualdad por contenido."""
    
    def __init__(self, texto: str, pos: str, frecuencia: int = 0):
        self.texto = texto
        self.pos = pos
        self.frecuencia = frecuencia
    
    def __eq__(self, other):
        if not isinstance(other, TokenInfo):
            return NotImplemented
        return self.texto == other.texto and self.pos == other.pos
    
    def __hash__(self):
        return hash((self.texto, self.pos))
    
    def __repr__(self):
        return f"Token('{self.texto}', {self.pos}, freq={self.frecuencia})"

t1 = TokenInfo("gato", "NOUN", 100)
t2 = TokenInfo("gato", "NOUN", 200)  # Mismo token, diferente freq
t3 = TokenInfo("gato", "VERB", 50)

print(f"  t1 == t2: {t1 == t2} (mismo texto+pos)")
print(f"  t1 == t3: {t1 == t3} (diferente pos)")
print(f"  En set: {len({t1, t2, t3})} tokens unicos")


print("\n--- __len__, __getitem__, __contains__: protocolo secuencia ---")

class Vocabulario:
    """Vocabulario con protocolo de secuencia completo."""
    
    def __init__(self, palabras: list[str]):
        self._palabras = sorted(set(palabras))
        self._index = {p: i for i, p in enumerate(self._palabras)}
    
    def __len__(self) -> int:
        return len(self._palabras)
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._palabras[key]
        elif isinstance(key, str):
            return self._index.get(key, -1)
        elif isinstance(key, slice):
            return self._palabras[key]
        raise TypeError(f"Indice no soportado: {type(key)}")
    
    def __contains__(self, item: str) -> bool:
        return item in self._index
    
    def __iter__(self):
        return iter(self._palabras)
    
    def __repr__(self):
        return f"Vocabulario(size={len(self)})"

vocab = Vocabulario(["hola", "mundo", "python", "ml", "deep", "learning", "hola"])

print(f"\n  vocab: {vocab}")
print(f"  len(vocab): {len(vocab)}")
print(f"  vocab[0]: '{vocab[0]}'")
print(f"  vocab['python']: {vocab['python']}")
print(f"  'ml' in vocab: {'ml' in vocab}")
print(f"  'java' in vocab: {'java' in vocab}")
print(f"  vocab[1:3]: {vocab[1:3]}")
print(f"  for: {[p for p in vocab]}")


print("\n--- __call__: objetos callable ---")

class Activacion:
    """Funcion de activacion como objeto callable."""
    
    def __init__(self, tipo: str = "relu"):
        self.tipo = tipo
        self.call_count = 0
    
    def __call__(self, x: float) -> float:
        self.call_count += 1
        if self.tipo == "relu":
            return max(0, x)
        elif self.tipo == "sigmoid":
            import math
            return 1 / (1 + math.exp(-x))
        elif self.tipo == "tanh":
            import math
            return math.tanh(x)
        return x
    
    def __repr__(self):
        return f"Activacion('{self.tipo}')"

relu = Activacion("relu")
sigmoid = Activacion("sigmoid")

print(f"\n  relu(-3) = {relu(-3)}")
print(f"  relu(5) = {relu(5)}")
print(f"  sigmoid(0) = {sigmoid(0):.4f}")
print(f"  sigmoid(2) = {sigmoid(2):.4f}")
print(f"  relu fue llamado {relu.call_count} veces")
print(f"  callable(relu): {callable(relu)}")


print("\n--- __add__, __mul__: aritmetica de objetos ---")

class Vector:
    """Vector N-dimensional con operaciones aritmeticas."""
    
    def __init__(self, *componentes):
        self.componentes = list(componentes)
    
    def __add__(self, other):
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError("Dimensiones diferentes")
            return Vector(*[a + b for a, b in zip(self.componentes, other.componentes)])
        return NotImplemented
    
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector(*[c * scalar for c in self.componentes])
        return NotImplemented
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __len__(self):
        return len(self.componentes)
    
    def __getitem__(self, idx):
        return self.componentes[idx]
    
    def __repr__(self):
        return f"Vector({', '.join(f'{c:.2f}' for c in self.componentes)})"
    
    def dot(self, other):
        return sum(a * b for a, b in zip(self.componentes, other.componentes))
    
    def norma(self):
        return sum(c**2 for c in self.componentes) ** 0.5

v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)

print(f"\n  v1 = {v1}")
print(f"  v2 = {v2}")
print(f"  v1 + v2 = {v1 + v2}")
print(f"  v1 * 3 = {v1 * 3}")
print(f"  2 * v2 = {2 * v2}")
print(f"  v1.dot(v2) = {v1.dot(v2)}")
print(f"  v1.norma() = {v1.norma():.4f}")


# =====================================================================
#   PARTE 3: ENCAPSULACION Y PROPERTIES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: ENCAPSULACION EN PYTHON ===")
print("=" * 80)

"""
Python NO tiene private/public como Java/C++.
Usa CONVENCIONES:
- _atributo: "protegido" (convencion, no enforcement)
- __atributo: name mangling (_Clase__atributo)
- propiedad: @property para getters/setters controlados

REGLA: usar _ para atributos internos + @property si necesitas
validacion o calculo.
"""

print("\n--- Convenciones de encapsulacion ---")

class RedNeuronal:
    """Red neuronal con encapsulacion profesional."""
    
    def __init__(self, nombre: str, capas: list[int]):
        self.nombre = nombre          # Publico
        self._capas = list(capas)     # "Protegido" (uso interno)
        self.__secreto = "clave123"   # Name mangling
        self._entrenada = False
        self._metricas = {}
    
    @property
    def capas(self) -> list:
        """Getter: retorna copia para evitar modificacion externa."""
        return self._capas.copy()
    
    @property
    def n_params(self) -> int:
        """Propiedad calculada: numero total de parametros."""
        total = 0
        for i in range(1, len(self._capas)):
            total += self._capas[i-1] * self._capas[i] + self._capas[i]
        return total
    
    @property
    def entrenada(self) -> bool:
        return self._entrenada
    
    @entrenada.setter
    def entrenada(self, valor: bool):
        if not isinstance(valor, bool):
            raise TypeError("entrenada debe ser bool")
        self._entrenada = valor
    
    def __repr__(self):
        return f"RedNeuronal('{self.nombre}', capas={self._capas})"

red = RedNeuronal("MLP", [768, 256, 64, 2])

print(f"  Red: {red}")
print(f"  Capas: {red.capas}")
print(f"  Parametros: {red.n_params:,}")
print(f"  Entrenada: {red.entrenada}")

red.entrenada = True
print(f"  Tras entrenar: {red.entrenada}")

try:
    red.entrenada = "si"  # Error de tipo
except TypeError as e:
    print(f"  Validacion: {e}")

# Name mangling
print(f"\n  __secreto via mangling: {red._RedNeuronal__secreto}")


# =====================================================================
#   PARTE 4: __SLOTS__ Y OPTIMIZACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: __SLOTS__ — OPTIMIZACION DE MEMORIA ===")
print("=" * 80)

"""
Por defecto, Python usa __dict__ para guardar atributos de instancia.
__dict__ es un diccionario -> flexible pero consume memoria.

__slots__ reemplaza __dict__ con una estructura fija:
- Menor uso de memoria (~40% menos).
- Acceso mas rapido a atributos.
- NO puedes agregar atributos dinamicamente.

CUANDO USAR __slots__:
- Cuando creas MUCHAS instancias (> 10,000).
- Cuando los atributos son fijos y conocidos.
- En data classes de alto rendimiento.
"""

print("\n--- Comparacion: con y sin __slots__ ---")

class TokenSlot:
    __slots__ = ('texto', 'idx', 'embedding')
    
    def __init__(self, texto: str, idx: int, embedding: float = 0.0):
        self.texto = texto
        self.idx = idx
        self.embedding = embedding

class TokenDict:
    def __init__(self, texto: str, idx: int, embedding: float = 0.0):
        self.texto = texto
        self.idx = idx
        self.embedding = embedding

# Comparar memoria
import sys

t_slot = TokenSlot("hola", 0, 0.5)
t_dict = TokenDict("hola", 0, 0.5)

print(f"  Con __slots__: {sys.getsizeof(t_slot)} bytes (sin __dict__)")
print(f"  Sin __slots__: {sys.getsizeof(t_dict)} + {sys.getsizeof(t_dict.__dict__)} bytes (__dict__)")

# Probar que no se pueden agregar atributos
try:
    t_slot.nuevo = "error"
except AttributeError as e:
    print(f"  Slots bloquea: {e}")


# =====================================================================
#   PARTE 5: DATACLASSES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: DATACLASSES — POO MODERNA ===")
print("=" * 80)

"""
@dataclass auto-genera: __init__, __repr__, __eq__, y opcionalmente
__hash__, __lt__, etc.

ES LA FORMA MODERNA de crear clases que son principalmente "contenedores
de datos" (records, DTOs, configuraciones).

Parametros de @dataclass:
- frozen=True: inmutable (genera __hash__ automaticamente).
- order=True: genera __lt__, __le__, __gt__, __ge__.
- slots=True: usa __slots__ (Python 3.10+).
- kw_only=True: todos los params son keyword-only (Python 3.10+).
"""

print("\n--- Dataclass basica ---")

@dataclass
class Experimento:
    nombre: str
    modelo: str
    dataset: str
    epochs: int = 10
    lr: float = 0.001
    metricas: dict = field(default_factory=dict)
    
    @property
    def config_key(self) -> str:
        return f"{self.modelo}_{self.dataset}_e{self.epochs}_lr{self.lr}"

exp1 = Experimento("exp_001", "BERT", "IMDB", epochs=20, lr=0.0005)
exp2 = Experimento("exp_001", "BERT", "IMDB", epochs=20, lr=0.0005)
exp3 = Experimento("exp_002", "GPT", "Wiki")

print(f"  exp1: {exp1}")
print(f"  exp1 == exp2: {exp1 == exp2}")
print(f"  exp1 == exp3: {exp1 == exp3}")
print(f"  config_key: {exp1.config_key}")
print(f"  asdict: {asdict(exp3)}")


print("\n--- Dataclass frozen (inmutable) ---")

@dataclass(frozen=True)
class Config:
    modelo: str
    lr: float
    epochs: int
    batch_size: int = 32

config = Config("BERT", 0.001, 10)
print(f"\n  Config: {config}")
print(f"  hash(config): {hash(config)}")

# Inmutable: no se puede modificar
try:
    config.lr = 0.01
except AttributeError as e:
    print(f"  Frozen bloquea: {type(e).__name__}")

# Como es hashable, se puede usar como key de dict
cache = {config: {"accuracy": 0.92}}
print(f"  Cache[config]: {cache[config]}")


print("\n--- Dataclass con order=True ---")

@dataclass(order=True)
class ModelScore:
    score: float
    nombre: str = field(compare=False)  # No participa en comparacion
    
scores = [
    ModelScore(0.92, "BERT"),
    ModelScore(0.95, "GPT-4"),
    ModelScore(0.88, "T5"),
    ModelScore(0.91, "RoBERTa"),
]

print(f"\n  Ordenados por score:")
for s in sorted(scores, reverse=True):
    print(f"    {s.nombre}: {s.score}")


print("\n--- Dataclass con __post_init__ ---")

@dataclass
class TrainingRun:
    modelo: str
    dataset: str
    epochs: int
    lr: float
    # Campos calculados
    nombre_run: str = field(init=False)
    timestamp: str = field(init=False)
    
    def __post_init__(self):
        """Se ejecuta DESPUES de __init__ auto-generado."""
        self.nombre_run = f"{self.modelo}_{self.dataset}_e{self.epochs}"
        import datetime
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

run = TrainingRun("BERT", "IMDB", 10, 0.001)
print(f"\n  Run: {run}")
print(f"  Nombre auto: {run.nombre_run}")


# =====================================================================
#   PARTE 6: EJERCICIO COMPLETO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: EJERCICIO — DATASET CLASS PROFESIONAL ===")
print("=" * 80)

"""
Construir una clase Dataset que implemente el protocolo de datos
completo: indexacion, iteracion, longitud, slicing, representacion.
"""

print("\n--- MLDataset profesional ---")

@dataclass
class Muestra:
    """Una muestra del dataset."""
    features: list
    label: int
    id: int = 0

class MLDataset:
    """Dataset con protocolo de datos completo."""
    
    def __init__(self, nombre: str, muestras: list[Muestra] = None):
        self.nombre = nombre
        self._muestras = muestras or []
    
    def agregar(self, muestra: Muestra):
        muestra.id = len(self._muestras)
        self._muestras.append(muestra)
    
    def __len__(self) -> int:
        return len(self._muestras)
    
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            nuevas = self._muestras[idx]
            return MLDataset(f"{self.nombre}_slice", nuevas)
        return self._muestras[idx]
    
    def __contains__(self, label: int) -> bool:
        return any(m.label == label for m in self._muestras)
    
    def __iter__(self):
        return iter(self._muestras)
    
    def __repr__(self):
        return f"MLDataset('{self.nombre}', n={len(self)})"
    
    def __add__(self, other):
        if not isinstance(other, MLDataset):
            return NotImplemented
        combinado = MLDataset(
            f"{self.nombre}+{other.nombre}",
            self._muestras + other._muestras
        )
        return combinado
    
    @property
    def distribucion_labels(self) -> dict:
        dist = {}
        for m in self._muestras:
            dist[m.label] = dist.get(m.label, 0) + 1
        return dist
    
    def split(self, ratio: float = 0.8) -> tuple:
        """Split train/test."""
        n = int(len(self) * ratio)
        train = MLDataset(f"{self.nombre}_train", self._muestras[:n])
        test = MLDataset(f"{self.nombre}_test", self._muestras[n:])
        return train, test

# Construir dataset
import random
random.seed(42)

ds = MLDataset("sentiment")
for i in range(100):
    features = [random.gauss(0, 1) for _ in range(5)]
    label = random.choice([0, 1])
    ds.agregar(Muestra(features, label))

print(f"  Dataset: {ds}")
print(f"  len(ds): {len(ds)}")
print(f"  ds[0]: {ds[0]}")
print(f"  ds[95:]: {ds[95:]}")
print(f"  1 in ds: {1 in ds}")
print(f"  Distribucion: {ds.distribucion_labels}")

train, test = ds.split(0.8)
print(f"\n  Train: {train}")
print(f"  Test:  {test}")

# Combinar datasets
ds2 = MLDataset("extra")
for i in range(20):
    ds2.agregar(Muestra([random.gauss(0, 1) for _ in range(5)], random.choice([0, 1])))

combinado = train + ds2
print(f"  Combinado: {combinado}")


print("\n" + "=" * 80)
print("=== CAPITULO 9: COMPARACION DE PATRONES ===")
print("=" * 80)

"""
Cuando usar cada patron:
"""

print("""
+--------------------+-------------------------------+--------------------+
| PATRON             | CUANDO USAR                   | EJEMPLO            |
+--------------------+-------------------------------+--------------------+
| Clase normal       | Logica compleja + estado      | MLModel, Pipeline  |
| @dataclass         | Contenedor de datos           | Config, Resultado  |
| @dataclass(frozen) | Datos inmutables / hashables  | CacheKey, Config   |
| __slots__          | Muchas instancias, memoria    | Token, Feature     |
| NamedTuple         | Tupla con nombres, inmutable  | Coordenada, Punto  |
| dict               | Esquema desconocido/variable  | JSON response      |
+--------------------+-------------------------------+--------------------+
""")


print("\n" + "=" * 80)
print("=== CAPITULO 10: CONTEXT MANAGER PROTOCOL ===")
print("=" * 80)

"""
__enter__ y __exit__ permiten que un objeto se use con 'with'.
with obj as valor:
    ...       # __enter__ retorna valor
              # __exit__ se llama al salir (incluso con excepcion)
"""

print("\n--- Context manager para conexion a DB simulada ---")

class DBConnection:
    """Simula una conexion a base de datos."""
    
    def __init__(self, host: str, db: str):
        self.host = host
        self.db = db
        self.connected = False
        self.queries = 0
    
    def __enter__(self):
        print(f"  Conectando a {self.host}/{self.db}...")
        self.connected = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  Cerrando conexion ({self.queries} queries ejecutadas)")
        self.connected = False
        if exc_type is not None:
            print(f"  Error capturado: {exc_val}")
        return False  # No suprime excepciones
    
    def query(self, sql: str) -> list:
        if not self.connected:
            raise RuntimeError("No conectado")
        self.queries += 1
        return [{"resultado": f"datos_{self.queries}"}]

with DBConnection("localhost", "ml_experiments") as db:
    r1 = db.query("SELECT * FROM experiments")
    r2 = db.query("SELECT * FROM metrics")
    print(f"  Query 1: {r1}")
    print(f"  Query 2: {r2}")

print(f"  Fuera del with: connected={db.connected}")


print("\n--- Context manager para modelo en modo evaluacion ---")

class ModelContext:
    """Context manager que pone un modelo en modo eval/train."""
    
    def __init__(self, modelo_nombre: str):
        self.nombre = modelo_nombre
        self.modo = "train"
    
    def __enter__(self):
        self.modo_anterior = self.modo
        self.modo = "eval"
        print(f"  [{self.nombre}] Modo: {self.modo}")
        return self
    
    def __exit__(self, *args):
        self.modo = self.modo_anterior
        print(f"  [{self.nombre}] Restaurado a modo: {self.modo}")
        return False

modelo_ctx = ModelContext("BERT")
print(f"  Antes: modo={modelo_ctx.modo}")
with modelo_ctx as m:
    print(f"  Dentro: modo={m.modo}")
print(f"  Despues: modo={modelo_ctx.modo}")


print("\n" + "=" * 80)
print("=== CAPITULO 11: DESCRIPTORES ===")
print("=" * 80)

"""
Un descriptor es un objeto que define __get__, __set__, o __delete__.
Controla el acceso a atributos de OTRA clase.

@property internamente usa descriptores.
"""

print("\n--- Descriptor para validacion de tipos ---")

class TypedAttribute:
    """Descriptor que valida el tipo de un atributo."""
    
    def __init__(self, nombre: str, tipo: type):
        self.nombre = nombre
        self.tipo = tipo
    
    def __set_name__(self, owner, name):
        self.attr_name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.attr_name, None)
    
    def __set__(self, obj, valor):
        if not isinstance(valor, self.tipo):
            raise TypeError(
                f"'{self.nombre}' debe ser {self.tipo.__name__}, "
                f"recibio {type(valor).__name__}"
            )
        setattr(obj, self.attr_name, valor)

class HyperParams:
    """Configuracion con validacion automatica via descriptores."""
    lr = TypedAttribute("lr", float)
    epochs = TypedAttribute("epochs", int)
    modelo = TypedAttribute("modelo", str)
    
    def __init__(self, lr: float, epochs: int, modelo: str):
        self.lr = lr
        self.epochs = epochs
        self.modelo = modelo
    
    def __repr__(self):
        return f"HyperParams(lr={self.lr}, epochs={self.epochs}, modelo='{self.modelo}')"

hp = HyperParams(0.001, 10, "BERT")
print(f"  {hp}")

try:
    hp.lr = "invalid"
except TypeError as e:
    print(f"  Validacion descriptor: {e}")

hp.lr = 0.0005
print(f"  Tras cambio: {hp}")


print("\n" + "=" * 80)
print("=== CAPITULO 12: NAMEDTUPLE VS DATACLASS ===")
print("=" * 80)

"""
NamedTuple: tupla inmutable con nombres. Mas ligera que dataclass.
Dataclass: mas flexible (mutable, metodos, herencia).
"""

from collections import namedtuple
from typing import NamedTuple

print("\n--- NamedTuple clasico ---")

PuntoNT = namedtuple("PuntoNT", ["x", "y"])
p = PuntoNT(3, 4)
print(f"  PuntoNT: {p}")
print(f"  x={p.x}, y={p.y}")
print(f"  Es tupla: {isinstance(p, tuple)}")
print(f"  Desempaquetar: x, y = {p[0]}, {p[1]}")

print("\n--- NamedTuple con typing ---")

class Resultado(NamedTuple):
    modelo: str
    accuracy: float
    loss: float
    epoch: int = 0

r = Resultado("BERT", 0.92, 0.15, epoch=10)
print(f"  {r}")
print(f"  accuracy: {r.accuracy}")

# Inmutable
try:
    r.accuracy = 0.95
except AttributeError as e:
    print(f"  Inmutable: {type(e).__name__}")

# Comparacion de memoria
import sys

@dataclass
class ResultadoDC:
    modelo: str
    accuracy: float
    loss: float
    epoch: int = 0

nt = Resultado("A", 0.9, 0.1)
dc = ResultadoDC("A", 0.9, 0.1)
print(f"\n  NamedTuple: {sys.getsizeof(nt)} bytes")
print(f"  Dataclass:  {sys.getsizeof(dc)} + {sys.getsizeof(dc.__dict__)} bytes")


print("\n" + "=" * 80)
print("=== CAPITULO 13: __NEW__ VS __INIT__ ===")
print("=" * 80)

"""
__new__: CREA la instancia (antes de __init__).
__init__: INICIALIZA la instancia (despues de __new__).

__new__ es necesario para:
- Inmutables (str, int, tuple): no puedes modificar en __init__.
- Singleton pattern.
- Metaclasses.
"""

print("\n--- __new__ para tipos inmutables ---")

class UpperStr(str):
    """String que siempre es uppercase."""
    
    def __new__(cls, valor):
        instance = super().__new__(cls, valor.upper())
        return instance

s = UpperStr("hola mundo")
print(f"  UpperStr('hola mundo') = '{s}'")
print(f"  Es str: {isinstance(s, str)}")


class PositiveInt(int):
    """Entero que siempre es positivo."""
    
    def __new__(cls, valor):
        if valor < 0:
            valor = abs(valor)
        return super().__new__(cls, valor)

n = PositiveInt(-42)
print(f"  PositiveInt(-42) = {n}")
print(f"  Es int: {isinstance(n, int)}")


print("\n" + "=" * 80)
print("=== CAPITULO 14: BENCHMARK SLOTS VS DICT VS NAMEDTUPLE ===")
print("=" * 80)

"""
Benchmark de memoria para diferentes enfoques de almacenamiento.
"""

print("\n--- Benchmark de memoria con 100K instancias ---")

import tracemalloc

class FeatureDict:
    def __init__(self, name, value, dtype):
        self.name = name
        self.value = value
        self.dtype = dtype

class FeatureSlots:
    __slots__ = ('name', 'value', 'dtype')
    def __init__(self, name, value, dtype):
        self.name = name
        self.value = value
        self.dtype = dtype

FeatureNT = namedtuple("FeatureNT", ["name", "value", "dtype"])

N = 50_000

# Dict
tracemalloc.start()
lista_dict = [FeatureDict(f"f{i}", i * 0.1, "float") for i in range(N)]
_, peak_dict = tracemalloc.get_traced_memory()
tracemalloc.stop()
del lista_dict

# Slots
tracemalloc.start()
lista_slots = [FeatureSlots(f"f{i}", i * 0.1, "float") for i in range(N)]
_, peak_slots = tracemalloc.get_traced_memory()
tracemalloc.stop()
del lista_slots

# NamedTuple
tracemalloc.start()
lista_nt = [FeatureNT(f"f{i}", i * 0.1, "float") for i in range(N)]
_, peak_nt = tracemalloc.get_traced_memory()
tracemalloc.stop()
del lista_nt

print(f"  {N:,} instancias:")
print(f"    __dict__:    {peak_dict/1024/1024:.1f} MB")
print(f"    __slots__:   {peak_slots/1024/1024:.1f} MB")
print(f"    NamedTuple:  {peak_nt/1024/1024:.1f} MB")
if peak_slots > 0:
    print(f"    Ratio dict/slots: {peak_dict/peak_slots:.1f}x")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE CLASES Y OBJETOS PARA INGENIERIA IA:

1. Todo en Python es un objeto. Clases son plantillas.

2. __init__ inicializa. __repr__ para devs, __str__ para users.

3. Dunder methods: __eq__, __hash__, __len__, __getitem__, __call__
   permiten que tus objetos se comporten como tipos nativos.

4. Encapsulacion: _ convencion, __ name mangling, @property.

5. __slots__: ~40% menos memoria, sin atributos dinamicos.

6. @dataclass: auto-genera __init__, __repr__, __eq__.

7. Context managers: __enter__/__exit__ para setup/teardown.

8. Descriptores: __get__/__set__ para validacion automatica.

9. NamedTuple: inmutable, ligero, ideal para records simples.

10. __new__ vs __init__: crear vs inicializar.

Siguiente archivo: Herencia, composicion y SOLID.
"""

print("\n FIN DE ARCHIVO 01_clases_y_objetos_desde_cero.")
print(" Las bases de POO en Python han sido dominadas.")
