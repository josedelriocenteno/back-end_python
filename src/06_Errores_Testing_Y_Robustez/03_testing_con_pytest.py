# ===========================================================================
# 03_testing_con_pytest.py
# ===========================================================================
# MODULO 06: ERRORES, TESTING Y ROBUSTEZ
# ARCHIVO 03: Testing Profesional con pytest
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar testing en Python: pytest, fixtures, parametrize, mocking,
# testing de ML code, property-based testing, y CI/CD integration.
#
# NOTA: Este archivo es un MONOLITO EDUCATIVO. Los tests se definen
# como funciones que se LLAMAN directamente para demostrar los conceptos.
# En produccion, estarian en archivos test_*.py separados.
#
# CONTENIDO:
#   1. Fundamentos de pytest: assert, fixtures, markers.
#   2. Parametrize: multiples inputs en un test.
#   3. Fixtures: setup/teardown reutilizable.
#   4. Mocking: simular dependencias.
#   5. Testing de ML: modelos, datos, pipelines.
#   6. Property-based testing: hypothesis concepts.
#   7. Coverage y CI/CD: conceptos.
#   8. Ejercicio: test suite completa para ML.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import time
import math
import random
import os
from typing import Any, Optional
from dataclasses import dataclass, field
from unittest.mock import Mock, patch, MagicMock
from contextlib import contextmanager


# =====================================================================
#   PARTE 1: FUNDAMENTOS DE TESTING
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: POR QUE TESTING ES CRITICO EN ML ===")
print("=" * 80)

"""
En ML, los bugs son SILENCIOSOS:
- Un modelo puede entrenar sin errores pero dar resultados basura.
- Data leakage no produce exceptions, solo metricas infladas.
- Un cambio en preprocessing puede degradar 10% de accuracy sin aviso.

TIPOS DE TESTS EN ML:
1. Unit tests: funciones individuales.
2. Integration tests: componentes juntos.
3. Data tests: validar datos de entrada/salida.
4. Model tests: verificar comportamiento del modelo.
5. Regression tests: detectar degradacion.
"""

print("""
+------------------+-----------------------------------+------------------+
| TIPO             | QUE TESTEA                        | EJEMPLO          |
+------------------+-----------------------------------+------------------+
| Unit             | Funcion individual                | tokenize()       |
| Integration      | Componentes juntos                | Pipeline end2end |
| Data             | Calidad de datos                  | No NaN, schema   |
| Model            | Comportamiento del modelo         | Accuracy > 0.8   |
| Regression       | No degradacion con cambios        | Score no baja    |
| Performance      | Tiempo/memoria                    | Latencia < 100ms |
+------------------+-----------------------------------+------------------+
""")


# =====================================================================
#   PARTE 2: TESTING CON ASSERT (SIN PYTEST)
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 2: TESTING CON ASSERT NATIVO ===")
print("=" * 80)

"""
pytest usa assert nativo de Python (con introspection magics).
Nosotros lo simulamos con un mini framework de test.
"""

print("\n--- Mini test framework ---")

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name):
        self.passed += 1
        print(f"  PASS: {name}")
    
    def add_fail(self, name, error):
        self.failed += 1
        self.errors.append((name, error))
        print(f"  FAIL: {name} -> {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n  {total} tests: {self.passed} passed, {self.failed} failed")

results = TestResult()

def run_test(func):
    """Ejecuta una funcion de test y captura errores."""
    try:
        func()
        results.add_pass(func.__name__)
    except AssertionError as e:
        results.add_fail(func.__name__, str(e))
    except Exception as e:
        results.add_fail(func.__name__, f"{type(e).__name__}: {e}")


# =====================================================================
#   PARTE 3: CODE UNDER TEST
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 3: CODIGO A TESTEAR ===")
print("=" * 80)

"""
Definimos las funciones y clases que vamos a testear.
"""

def tokenize(texto: str) -> list[str]:
    """Tokeniza texto en palabras."""
    if not isinstance(texto, str):
        raise TypeError(f"Se espera str, got {type(texto).__name__}")
    return texto.lower().strip().split()

def normalizar(valores: list[float]) -> list[float]:
    """Normaliza valores a rango [0, 1]."""
    if not valores:
        return []
    min_v = min(valores)
    max_v = max(valores)
    rango = max_v - min_v
    if rango == 0:
        return [0.5] * len(valores)
    return [(v - min_v) / rango for v in valores]

def accuracy(y_true: list, y_pred: list) -> float:
    """Calcula accuracy."""
    if len(y_true) != len(y_pred):
        raise ValueError("Longitudes diferentes")
    if not y_true:
        raise ValueError("Listas vacias")
    return sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true)

@dataclass
class SimpleModel:
    nombre: str
    threshold: float = 0.5
    entrenado: bool = False
    
    def fit(self, X: list, y: list):
        if not X or not y:
            raise ValueError("Datos vacios")
        self.entrenado = True
        self._media = sum(y) / len(y)
    
    def predict(self, X: list) -> list:
        if not self.entrenado:
            raise RuntimeError("Modelo no entrenado")
        return [1 if x > self.threshold else 0 for x in X]
    
    def predict_proba(self, X: list) -> list:
        if not self.entrenado:
            raise RuntimeError("Modelo no entrenado")
        return [min(1.0, max(0.0, x * self._media)) for x in X]


# =====================================================================
#   PARTE 4: UNIT TESTS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 4: UNIT TESTS ===")
print("=" * 80)

print("\n--- Tests de tokenize() ---")

def test_tokenize_basico():
    assert tokenize("Hola Mundo") == ["hola", "mundo"]

def test_tokenize_con_espacios():
    assert tokenize("  hola   mundo  ") == ["hola", "mundo"]

def test_tokenize_vacio():
    assert tokenize("") == []
    assert tokenize("   ") == []

def test_tokenize_tipo_incorrecto():
    try:
        tokenize(123)
        assert False, "Debio lanzar TypeError"
    except TypeError:
        pass  # Esperado

def test_tokenize_una_palabra():
    assert tokenize("Python") == ["python"]

for test in [test_tokenize_basico, test_tokenize_con_espacios,
             test_tokenize_vacio, test_tokenize_tipo_incorrecto,
             test_tokenize_una_palabra]:
    run_test(test)


print("\n--- Tests de normalizar() ---")

def test_normalizar_basico():
    result = normalizar([0, 50, 100])
    assert result == [0.0, 0.5, 1.0]

def test_normalizar_ya_normalizado():
    result = normalizar([0, 0.5, 1.0])
    assert result[0] == 0.0
    assert result[-1] == 1.0

def test_normalizar_negativos():
    result = normalizar([-10, 0, 10])
    assert result == [0.0, 0.5, 1.0]

def test_normalizar_todos_iguales():
    result = normalizar([5, 5, 5])
    assert result == [0.5, 0.5, 0.5]

def test_normalizar_vacio():
    assert normalizar([]) == []

def test_normalizar_un_elemento():
    assert normalizar([42]) == [0.5]

for test in [test_normalizar_basico, test_normalizar_ya_normalizado,
             test_normalizar_negativos, test_normalizar_todos_iguales,
             test_normalizar_vacio, test_normalizar_un_elemento]:
    run_test(test)


print("\n--- Tests de accuracy() ---")

def test_accuracy_perfecto():
    assert accuracy([1, 0, 1], [1, 0, 1]) == 1.0

def test_accuracy_cero():
    assert accuracy([1, 1, 1], [0, 0, 0]) == 0.0

def test_accuracy_parcial():
    assert accuracy([1, 0, 1, 0], [1, 0, 0, 1]) == 0.5

def test_accuracy_longitudes_diferentes():
    try:
        accuracy([1, 2], [1])
        assert False, "Debio lanzar ValueError"
    except ValueError:
        pass

def test_accuracy_vacio():
    try:
        accuracy([], [])
        assert False, "Debio lanzar ValueError"
    except ValueError:
        pass

for test in [test_accuracy_perfecto, test_accuracy_cero,
             test_accuracy_parcial, test_accuracy_longitudes_diferentes,
             test_accuracy_vacio]:
    run_test(test)


# =====================================================================
#   PARTE 5: PARAMETRIZE (SIMULATED)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: PARAMETRIZE — MULTIPLES INPUTS ===")
print("=" * 80)

"""
En pytest: @pytest.mark.parametrize("input,expected", [...])
Nosotros lo simulamos con un loop.
"""

print("\n--- Parametrized tests ---")

def parametrize_test(nombre, cases, test_fn):
    """Simula @pytest.mark.parametrize."""
    for i, case in enumerate(cases):
        test_name = f"{nombre}[case_{i}]"
        try:
            test_fn(*case)
            results.add_pass(test_name)
        except AssertionError as e:
            results.add_fail(test_name, str(e))

# Test parametrizado de tokenize
tokenize_cases = [
    ("hola mundo", ["hola", "mundo"]),
    ("Python ML", ["python", "ml"]),
    ("", []),
    ("UNA", ["una"]),
    ("a b c d e", ["a", "b", "c", "d", "e"]),
]

def check_tokenize(texto, expected):
    assert tokenize(texto) == expected, f"tokenize('{texto}') != {expected}"

parametrize_test("test_tokenize_param", tokenize_cases, check_tokenize)


# Test parametrizado de accuracy
accuracy_cases = [
    ([1, 0, 1], [1, 0, 1], 1.0),
    ([1, 0, 1], [0, 1, 0], 0.0),
    ([1, 0, 1, 0], [1, 0, 0, 1], 0.5),
    ([1, 1, 0, 0, 1], [1, 1, 0, 0, 1], 1.0),
]

def check_accuracy(y_true, y_pred, expected):
    result = accuracy(y_true, y_pred)
    assert abs(result - expected) < 1e-10, f"accuracy={result}, expected={expected}"

parametrize_test("test_accuracy_param", accuracy_cases, check_accuracy)


# =====================================================================
#   PARTE 6: FIXTURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: FIXTURES — SETUP/TEARDOWN ===")
print("=" * 80)

"""
En pytest:
@pytest.fixture
def trained_model():
    model = SimpleModel("test")
    model.fit([0.1, 0.5, 0.9], [0, 0, 1])
    return model

Nosotros lo simulamos con context managers.
"""

print("\n--- Fixtures simuladas ---")

@contextmanager
def fixture_modelo_entrenado():
    """Fixture: modelo ya entrenado."""
    modelo = SimpleModel("test_model", threshold=0.5)
    modelo.fit([0.1, 0.5, 0.9, 0.2, 0.8], [0, 0, 1, 0, 1])
    yield modelo
    # Teardown (si fuera necesario)

@contextmanager
def fixture_dataset():
    """Fixture: dataset de prueba."""
    random.seed(42)
    X = [random.gauss(0.5, 0.2) for _ in range(100)]
    y = [1 if x > 0.5 else 0 for x in X]
    yield X, y

def test_modelo_predict():
    with fixture_modelo_entrenado() as modelo:
        preds = modelo.predict([0.1, 0.9])
        assert isinstance(preds, list)
        assert len(preds) == 2
        assert all(p in (0, 1) for p in preds)

def test_modelo_predict_proba():
    with fixture_modelo_entrenado() as modelo:
        probs = modelo.predict_proba([0.5])
        assert isinstance(probs, list)
        assert 0 <= probs[0] <= 1

def test_modelo_no_entrenado():
    modelo = SimpleModel("untrained")
    try:
        modelo.predict([1, 2])
        assert False, "Debio lanzar RuntimeError"
    except RuntimeError:
        pass

for test in [test_modelo_predict, test_modelo_predict_proba,
             test_modelo_no_entrenado]:
    run_test(test)


# =====================================================================
#   PARTE 7: MOCKING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: MOCKING — SIMULAR DEPENDENCIAS ===")
print("=" * 80)

"""
Mock: simular objetos/funciones que:
- Son lentas (API externa)
- Son impredecibles (random)
- No estan disponibles en test (GPU, DB)

unittest.mock: Mock, MagicMock, patch
"""

print("\n--- Mock basico ---")

# Simular una API externa
api_mock = Mock()
api_mock.predict.return_value = [0.9, 0.1, 0.8]
api_mock.model_name = "bert-base"

def test_mock_basico():
    result = api_mock.predict([1, 2, 3])
    assert result == [0.9, 0.1, 0.8]
    api_mock.predict.assert_called_once_with([1, 2, 3])

run_test(test_mock_basico)


print("\n--- Mock con side_effect ---")

call_count = 0

def api_flaky():
    """API que falla las primeras 2 veces."""
    global call_count
    call_count += 1
    if call_count <= 2:
        raise ConnectionError("timeout")
    return {"status": "ok"}

def test_side_effect():
    mock_api = Mock(side_effect=[
        ConnectionError("timeout"),
        ConnectionError("timeout"),
        {"status": "ok"},
    ])
    
    # Primeras 2 fallan
    for _ in range(2):
        try:
            mock_api()
        except ConnectionError:
            pass
    
    # Tercera funciona
    result = mock_api()
    assert result == {"status": "ok"}
    assert mock_api.call_count == 3

run_test(test_side_effect)


print("\n--- MagicMock para objetos complejos ---")

def test_magic_mock():
    db = MagicMock()
    db.query.return_value = [{"id": 1, "score": 0.9}]
    db.__len__.return_value = 100
    
    results_db = db.query("SELECT * FROM models")
    assert len(results_db) == 1
    assert results_db[0]["score"] == 0.9
    assert len(db) == 100

run_test(test_magic_mock)


# =====================================================================
#   PARTE 8: TESTING DE ML
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: TESTING ESPECIFICO DE ML ===")
print("=" * 80)

"""
Tests especificos para codigo de ML:
1. Data tests: schema, distribuciones, NaN.
2. Model tests: forma de output, rangos, determinismo.
3. Training tests: loss decrece, no NaN.
4. Invariance tests: comportamiento ante transformaciones.
"""

print("\n--- Data tests ---")

def test_data_no_nan():
    """Verificar que no hay NaN en el dataset."""
    datos = [1.0, 2.0, 3.0, 4.0, 5.0]
    assert not any(math.isnan(x) for x in datos), "Dataset contiene NaN"

def test_data_schema():
    """Verificar schema del dataset."""
    sample = {"features": [1, 2, 3], "label": 1, "id": "abc"}
    
    assert "features" in sample, "Falta feature"
    assert "label" in sample, "Falta label"
    assert isinstance(sample["features"], list), "Features debe ser list"
    assert sample["label"] in (0, 1), "Label debe ser binario"

def test_data_balance():
    """Verificar que las clases no estan muy desbalanceadas."""
    labels = [1, 0, 1, 0, 1, 0, 1, 1, 0, 0]
    ratio = labels.count(1) / len(labels)
    assert 0.3 <= ratio <= 0.7, f"Clases desbalanceadas: {ratio:.2f}"

for test in [test_data_no_nan, test_data_schema, test_data_balance]:
    run_test(test)


print("\n--- Model tests ---")

def test_output_shape():
    """Output debe tener misma longitud que input."""
    with fixture_modelo_entrenado() as modelo:
        for n in [1, 5, 10, 100]:
            X = [0.5] * n
            preds = modelo.predict(X)
            assert len(preds) == n, f"Output shape {len(preds)} != input {n}"

def test_output_range():
    """Probabilidades deben estar en [0, 1]."""
    with fixture_modelo_entrenado() as modelo:
        X = [random.random() for _ in range(50)]
        probs = modelo.predict_proba(X)
        for p in probs:
            assert 0 <= p <= 1, f"Probabilidad fuera de rango: {p}"

def test_determinism():
    """Mismo input debe dar mismo output."""
    with fixture_modelo_entrenado() as modelo:
        X = [0.3, 0.5, 0.7]
        pred1 = modelo.predict(X)
        pred2 = modelo.predict(X)
        assert pred1 == pred2, "Modelo no es determinista"

for test in [test_output_shape, test_output_range, test_determinism]:
    run_test(test)


print("\n--- Training tests ---")

def test_training_loss_decreases():
    """Loss debe decrecer durante training (simulado)."""
    losses = [1.0, 0.8, 0.6, 0.4, 0.3]
    for i in range(1, len(losses)):
        assert losses[i] < losses[i-1], \
            f"Loss no decrece en step {i}: {losses[i]} >= {losses[i-1]}"

def test_training_no_nan_loss():
    """Loss no debe ser NaN."""
    losses = [0.5, 0.3, 0.2, 0.15, 0.1]
    for loss in losses:
        assert not math.isnan(loss), f"Loss es NaN"
        assert not math.isinf(loss), f"Loss es Inf"

for test in [test_training_loss_decreases, test_training_no_nan_loss]:
    run_test(test)


print("\n--- Invariance tests ---")

def test_invariance_padding():
    """Tokenizer debe ser invariante a padding (espacios)."""
    assert tokenize("hola mundo") == tokenize("  hola  mundo  ")

def test_invariance_case():
    """Tokenizer debe ser case-insensitive."""
    assert tokenize("Hola") == tokenize("hola")
    assert tokenize("PYTHON ML") == tokenize("python ml")

for test in [test_invariance_padding, test_invariance_case]:
    run_test(test)


# =====================================================================
#   PARTE 9: PROPERTY-BASED TESTING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: PROPERTY-BASED TESTING ===")
print("=" * 80)

"""
En vez de testear con inputs especificos, defines PROPIEDADES
que deben cumplirse para TODOS los inputs posibles.

hypothesis genera inputs aleatorios automaticamente.
Nosotros lo simulamos con random.
"""

print("\n--- Property: normalizar siempre produce [0, 1] ---")

def test_property_normalizar_rango():
    """Para CUALQUIER input, normalizar produce valores en [0, 1]."""
    random.seed(42)
    for _ in range(100):
        n = random.randint(2, 20)
        valores = [random.gauss(0, 100) for _ in range(n)]
        resultado = normalizar(valores)
        
        for v in resultado:
            assert 0 <= v <= 1, f"Valor {v} fuera de [0, 1] para input {valores}"

run_test(test_property_normalizar_rango)


def test_property_normalizar_min_max():
    """El min siempre es 0 y el max siempre es 1 (si hay varianza)."""
    random.seed(42)
    for _ in range(50):
        valores = [random.gauss(0, 10) for _ in range(5)]
        if max(valores) != min(valores):
            resultado = normalizar(valores)
            assert abs(min(resultado) - 0.0) < 1e-10
            assert abs(max(resultado) - 1.0) < 1e-10

run_test(test_property_normalizar_min_max)


def test_property_tokenize_longitud():
    """tokenize nunca produce tokens mas largos que el input."""
    random.seed(42)
    for _ in range(50):
        words = ["".join(chr(random.randint(97, 122)) for _ in range(random.randint(1, 10)))
                 for _ in range(random.randint(1, 10))]
        texto = " ".join(words)
        tokens = tokenize(texto)
        assert len(tokens) <= len(texto)

run_test(test_property_tokenize_longitud)


# =====================================================================
#   PARTE 10: INTEGRATION TESTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: INTEGRATION TESTS ===")
print("=" * 80)

"""
Integration tests: verificar que componentes funcionan JUNTOS.
En ML: pipeline completo desde datos hasta prediccion.
"""

print("\n--- Integration test de pipeline completo ---")

class MiniPipeline:
    """Pipeline simple para testing."""
    
    def __init__(self):
        self.preprocessed = False
        self.trained = False
    
    def preprocess(self, textos: list) -> list:
        self.preprocessed = True
        return [t.lower().split() for t in textos]
    
    def train(self, datos: list, labels: list):
        if not self.preprocessed:
            raise RuntimeError("Debe preprocesar primero")
        self.trained = True
        self._avg_len = sum(len(d) for d in datos) / len(datos)
    
    def predict(self, textos: list) -> list:
        if not self.trained:
            raise RuntimeError("Debe entrenar primero")
        datos = self.preprocess(textos)
        return [1 if len(d) > self._avg_len else 0 for d in datos]

def test_pipeline_end_to_end():
    """Test de integracion: todo el pipeline."""
    pipeline = MiniPipeline()
    
    textos_train = ["hola mundo", "machine learning es genial", "python"]
    labels = [0, 1, 0]
    
    datos = pipeline.preprocess(textos_train)
    assert pipeline.preprocessed
    assert len(datos) == 3
    
    pipeline.train(datos, labels)
    assert pipeline.trained
    
    preds = pipeline.predict(["hola", "deep learning con transformers avanzados"])
    assert isinstance(preds, list)
    assert len(preds) == 2
    assert all(p in (0, 1) for p in preds)

def test_pipeline_sin_preprocess():
    """Pipeline debe fallar si no se preprocesa."""
    pipeline = MiniPipeline()
    try:
        pipeline.train([[1]], [1])
        assert False, "Debio fallar sin preprocess"
    except RuntimeError:
        pass

def test_pipeline_sin_train():
    """Pipeline debe fallar si no se entrena."""
    pipeline = MiniPipeline()
    try:
        pipeline.predict(["hola"])
        assert False, "Debio fallar sin train"
    except RuntimeError:
        pass

for test in [test_pipeline_end_to_end, test_pipeline_sin_preprocess,
             test_pipeline_sin_train]:
    run_test(test)


# =====================================================================
#   PARTE 11: PERFORMANCE TESTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: PERFORMANCE TESTS ===")
print("=" * 80)

"""
Verificar que funciones cumplen requisitos de performance:
- Latencia maxima.
- Throughput minimo.
- Uso de memoria.
"""

print("\n--- Latency tests ---")

def test_tokenize_latency():
    """Tokenize debe completar en < 1ms para textos normales."""
    texto = "Machine learning con Python es fantastico para NLP"
    
    start = time.perf_counter()
    for _ in range(1000):
        tokenize(texto)
    elapsed = (time.perf_counter() - start) / 1000
    
    assert elapsed < 0.001, f"Latencia {elapsed*1000:.3f}ms > 1ms"

def test_normalizar_latency():
    """Normalizar 10K valores debe completar en < 10ms."""
    valores = list(range(10_000))
    
    start = time.perf_counter()
    normalizar(valores)
    elapsed = time.perf_counter() - start
    
    assert elapsed < 0.01, f"Latencia {elapsed*1000:.1f}ms > 10ms"

def test_throughput():
    """Pipeline debe procesar al menos 1000 items/sec."""
    pipeline = MiniPipeline()
    textos = ["hola mundo python ml"] * 100
    labels = [0] * 100
    
    datos = pipeline.preprocess(textos)
    pipeline.train(datos, labels)
    
    start = time.perf_counter()
    n_items = 0
    for _ in range(10):
        preds = pipeline.predict(textos)
        n_items += len(preds)
    elapsed = time.perf_counter() - start
    
    throughput = n_items / elapsed
    assert throughput > 1000, f"Throughput {throughput:.0f} < 1000 items/sec"

for test in [test_tokenize_latency, test_normalizar_latency, test_throughput]:
    run_test(test)


# =====================================================================
#   PARTE 12: REGRESSION TESTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: REGRESSION TESTS ===")
print("=" * 80)

"""
Regression tests: asegurar que cambios no rompen funcionalidad existente.
En ML: guardar predicciones esperadas y comparar tras cambios.
"""

print("\n--- Snapshot testing (simulado) ---")

SNAPSHOTS = {
    "tokenize_basic": {
        "input": "Hello World ML",
        "expected": ["hello", "world", "ml"]
    },
    "normalizar_basic": {
        "input": [0, 50, 100],
        "expected": [0.0, 0.5, 1.0]
    },
    "accuracy_perfect": {
        "input": {"y_true": [1, 0, 1], "y_pred": [1, 0, 1]},
        "expected": 1.0
    },
}

def test_regression_tokenize():
    snap = SNAPSHOTS["tokenize_basic"]
    result = tokenize(snap["input"])
    assert result == snap["expected"], \
        f"Regression: tokenize cambio de {snap['expected']} a {result}"

def test_regression_normalizar():
    snap = SNAPSHOTS["normalizar_basic"]
    result = normalizar(snap["input"])
    assert result == snap["expected"], \
        f"Regression: normalizar cambio"

def test_regression_accuracy():
    snap = SNAPSHOTS["accuracy_perfect"]
    result = accuracy(snap["input"]["y_true"], snap["input"]["y_pred"])
    assert abs(result - snap["expected"]) < 1e-10, \
        f"Regression: accuracy cambio de {snap['expected']} a {result}"

for test in [test_regression_tokenize, test_regression_normalizar,
             test_regression_accuracy]:
    run_test(test)


# =====================================================================
#   PARTE 13: TEST HELPERS Y ASSERTIONS CUSTOM
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: ASSERTIONS CUSTOM PARA ML ===")
print("=" * 80)

"""
Crear assertions especializadas para ML que dan mensajes claros.
"""

print("\n--- ML Assertions ---")

def assert_array_close(a: list, b: list, rtol: float = 1e-5, msg: str = ""):
    """Assert que dos listas son aproximadamente iguales."""
    assert len(a) == len(b), f"Longitudes diferentes: {len(a)} vs {len(b)}"
    for i, (x, y) in enumerate(zip(a, b)):
        if abs(x - y) > rtol * max(abs(x), abs(y), 1):
            raise AssertionError(
                f"Elemento {i}: {x} != {y} (rtol={rtol}) {msg}"
            )

def assert_probabilities(probs: list, msg: str = ""):
    """Assert que una lista son probabilidades validas."""
    for i, p in enumerate(probs):
        assert 0 <= p <= 1, f"Prob[{i}]={p} fuera de [0,1] {msg}"

def assert_labels_valid(labels: list, valid_labels: set, msg: str = ""):
    """Assert que todos los labels son validos."""
    invalid = [l for l in labels if l not in valid_labels]
    assert not invalid, f"Labels invalidos: {invalid} {msg}"

def test_custom_assertions():
    assert_array_close([1.0, 2.0, 3.0], [1.00001, 2.00001, 3.00001])
    assert_probabilities([0.1, 0.5, 0.9, 0.0, 1.0])
    assert_labels_valid([0, 1, 0, 1, 1], {0, 1})

run_test(test_custom_assertions)


# =====================================================================
#   PARTE 14: PYTEST REAL Y CI/CD
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: PYTEST EN LA PRACTICA ===")
print("=" * 80)

"""
En un proyecto real, los tests van en archivos separados:

proyecto/
├── src/
│   └── ml_pipeline/
│       ├── tokenizer.py
│       ├── model.py
│       └── metrics.py
├── tests/
│   ├── conftest.py          # Fixtures compartidas
│   ├── test_tokenizer.py
│   ├── test_model.py
│   └── test_metrics.py
├── pyproject.toml
└── pytest.ini

COMANDOS CLAVE:
  pytest                    # Ejecutar todos los tests
  pytest tests/test_model.py  # Un archivo
  pytest -v                 # Verbose
  pytest -x                 # Parar en primer fallo
  pytest -k "tokenize"      # Solo tests con "tokenize" en nombre
  pytest --cov=src          # Con coverage
  pytest -n auto            # Paralelo (pytest-xdist)
"""

print("""
EJEMPLO DE ARCHIVO test_model.py:

    import pytest
    from ml_pipeline.model import SimpleModel

    @pytest.fixture
    def trained_model():
        model = SimpleModel("test")
        model.fit([0.1, 0.5, 0.9], [0, 0, 1])
        return model

    def test_predict_shape(trained_model):
        preds = trained_model.predict([0.1, 0.9])
        assert len(preds) == 2

    @pytest.mark.parametrize("input,expected_len", [
        ([0.5], 1),
        ([0.1, 0.9], 2),
        ([0.1]*100, 100),
    ])
    def test_predict_parametrized(trained_model, input, expected_len):
        assert len(trained_model.predict(input)) == expected_len

    def test_predict_raises_untrained():
        model = SimpleModel("untrained")
        with pytest.raises(RuntimeError, match="no entrenado"):
            model.predict([1])
""")


print("\n--- CI/CD Pipeline para ML ---")

print("""
EJEMPLO DE .github/workflows/test.yml:

name: ML Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=src --cov-report=xml
      - run: mypy src/ --strict
      - run: ruff check src/

REGLA: NO merges sin tests verdes.
""")


# =====================================================================
#   RESULTADO FINAL
# =====================================================================

print("\n" + "=" * 80)
print("=== RESULTADO DE TODOS LOS TESTS ===")
print("=" * 80)

results.summary()


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE TESTING PARA ML:

1. Testing es CRITICO en ML: bugs silenciosos, data leakage.

2. pytest: assert nativo, fixtures, parametrize, markers.

3. Fixtures: setup reutilizable. conftest.py para compartir.

4. Parametrize: un test, multiples inputs.

5. Mocking: simular APIs, DBs, GPUs. Mock, patch, MagicMock.

6. Data tests: schema, NaN, balance, distribucion.

7. Model tests: output shape, rango [0,1], determinismo.

8. Training tests: loss decrece, no NaN, convergencia.

9. Invariance tests: padding, case, orden.

10. Property-based: propiedades para TODO input.

11. Integration tests: pipeline end-to-end.

12. Performance tests: latencia, throughput.

13. Regression tests: snapshots para detectar cambios.

14. CI/CD: automatizar tests en cada push.

FIN DEL MODULO 06: ERRORES, TESTING Y ROBUSTEZ.
FIN DE LA FASE 1: PYTHON — DOMINIO PROFUNDO.
"""

print("\n FIN DE ARCHIVO 03_testing_con_pytest.")
print(" Testing profesional para ML ha sido dominado.")
print(" Siguiente fase: FASE 2 — MATEMATICAS Y DATOS.")
