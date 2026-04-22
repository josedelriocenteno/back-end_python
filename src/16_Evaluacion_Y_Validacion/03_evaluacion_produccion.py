# ===========================================================================
# 03_evaluacion_produccion.py
# ===========================================================================
# MODULO 16: EVALUACION Y VALIDACION
# ARCHIVO 03: Monitoreo de Modelos en Produccion, Drift, A/B Testing
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar la evaluacion de modelos DESPUES del deploy: monitoreo
# continuo, deteccion de degradacion, drift, A/B testing para
# modelos, dashboards de metricas, y cuando re-entrenar.
#
# CONTENIDO:
#   1. Por que monitorear modelos en produccion.
#   2. Metricas de produccion vs metricas offline.
#   3. Data drift detection (PSI, KS, Wasserstein).
#   4. Concept drift detection.
#   5. Prediction drift.
#   6. A/B testing para modelos ML.
#   7. Shadow mode / Champion-Challenger.
#   8. Alertas y thresholds.
#   9. Dashboards de metricas.
#   10. Cuando re-entrenar.
#   11. Canary deployments para ML.
#   12. Pipeline de monitoreo end-to-end.
#
# NIVEL: ARQUITECTO ML / MLOPS ENGINEER.
# ===========================================================================

import numpy as np
import time
from datetime import datetime, timedelta
from collections import deque
from typing import Any, Callable, Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (
        accuracy_score, f1_score, precision_score, recall_score,
        roc_auc_score, log_loss, confusion_matrix
    )
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from scipy import stats
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# =====================================================================
#   PARTE 1: POR QUE MONITOREAR MODELOS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: MONITOREO — EL MODELO NO ES ESTATICO ===")
print("=" * 80)

"""
UN MODELO EN PRODUCCION SE DEGRADA.

No es cuestion de SI se degradara, sino CUANDO.

POR QUE:
1. El mundo cambia:
   - Inflacion cambia patrones de gasto.
   - Nuevos competidores cambian comportamiento de usuarios.
   - COVID cambio TODO.

2. Los datos cambian:
   - Nuevas fuentes de datos con distribuciones diferentes.
   - Bugs en pipelines de datos (un campo empieza a llegar null).
   - Cambios en la definicion de features upstream.

3. El modelo envejece:
   - Features que eran predictivas dejan de serlo.
   - La relacion X→Y cambia (concept drift).
   - Nuevas categorias que el modelo nunca vio.

SIN MONITOREO:
  Tu modelo puede estar prediciendo BASURA durante meses
  y nadie lo nota hasta que un cliente se queja.

CON MONITOREO:
  Alertas automaticas cuando algo cambia.
  Sabes EXACTAMENTE cuando re-entrenar.
  Puedes comparar versiones con A/B testing.
"""

print("""
  Timeline tipica de un modelo en produccion:

  Deploy ──→ Performance OK ──→ Degradacion gradual ──→ Fallo silencioso
  │                                                         │
  │  Sin monitoreo: nadie nota ─────────────────────────────┘
  │
  │  Con monitoreo: ALERTA → re-entrenar → deploy v2
""")


# =====================================================================
#   PARTE 2: METRICAS OFFLINE VS PRODUCCION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: METRICAS OFFLINE vs PRODUCCION ===")
print("=" * 80)

"""
OFFLINE (antes del deploy):
  - Accuracy, F1, AUC en test set.
  - Cross-validation scores.
  - Son ESTATICAS: calculadas una vez.

PRODUCCION (despues del deploy):
  - Las mismas metricas, pero calculadas CONTINUAMENTE.
  - MAS metricas especificas:
    * Latencia de prediccion (p50, p95, p99).
    * Throughput (predicciones/segundo).
    * Error rate (excepciones, timeouts).
    * Feature freshness (antigüedad de las features).
    * Prediction distribution (cambios en output).
    * Business metrics (conversion, revenue impact).

REGLA: las metricas de negocio son las que IMPORTAN.
  Un modelo con AUC=0.99 pero que no mejora conversion = inutil.
"""


class ProductionMetricsTracker:
    """Trackea metricas de un modelo en produccion."""

    def __init__(self, model_name: str, window_size: int = 1000):
        self.model_name = model_name
        self.window_size = window_size

        # Metricas ML
        self._predictions = deque(maxlen=window_size)
        self._actuals = deque(maxlen=window_size)
        self._probabilities = deque(maxlen=window_size)

        # Metricas operacionales
        self._latencies_ms = deque(maxlen=window_size)
        self._errors = deque(maxlen=window_size)

        # Historial de metricas agregadas
        self._metric_history: List[Dict] = []

    def log_prediction(self, prediction: int, probability: float,
                       latency_ms: float, actual: Optional[int] = None,
                       error: bool = False):
        """Registra una prediccion con metadata."""
        self._predictions.append(prediction)
        self._probabilities.append(probability)
        self._latencies_ms.append(latency_ms)
        self._errors.append(error)
        if actual is not None:
            self._actuals.append(actual)

    def get_ml_metrics(self) -> Dict:
        """Calcula metricas ML sobre la ventana actual."""
        if len(self._actuals) < 10:
            return {'status': 'insufficient_data'}

        preds = list(self._predictions)[:len(self._actuals)]
        actuals = list(self._actuals)

        metrics = {
            'accuracy': accuracy_score(actuals, preds),
            'f1': f1_score(actuals, preds, zero_division=0),
            'precision': precision_score(actuals, preds, zero_division=0),
            'recall': recall_score(actuals, preds, zero_division=0),
            'positive_rate': np.mean(preds),
            'n_samples': len(actuals),
        }

        try:
            probs = list(self._probabilities)[:len(self._actuals)]
            metrics['auc'] = roc_auc_score(actuals, probs)
            metrics['log_loss'] = log_loss(actuals, probs)
        except Exception:
            pass

        return metrics

    def get_operational_metrics(self) -> Dict:
        """Metricas operacionales."""
        latencies = list(self._latencies_ms)
        errors = list(self._errors)

        if not latencies:
            return {'status': 'no_data'}

        return {
            'latency_p50': float(np.percentile(latencies, 50)),
            'latency_p95': float(np.percentile(latencies, 95)),
            'latency_p99': float(np.percentile(latencies, 99)),
            'latency_mean': float(np.mean(latencies)),
            'error_rate': float(np.mean(errors)),
            'throughput': len(latencies),
        }

    def get_prediction_distribution(self) -> Dict:
        """Distribucion de predicciones (detecta cambios en output)."""
        preds = list(self._predictions)
        probs = list(self._probabilities)

        if not preds:
            return {'status': 'no_data'}

        return {
            'prediction_mean': float(np.mean(preds)),
            'prediction_std': float(np.std(preds)),
            'probability_mean': float(np.mean(probs)),
            'probability_std': float(np.std(probs)),
            'pct_positive': float(np.mean(np.array(preds) == 1)),
            'pct_high_confidence': float(
                np.mean((np.array(probs) > 0.9) | (np.array(probs) < 0.1))
            ),
        }

    def snapshot(self) -> Dict:
        """Snapshot completo de todas las metricas."""
        snap = {
            'model': self.model_name,
            'timestamp': datetime.now(),
            'ml_metrics': self.get_ml_metrics(),
            'operational': self.get_operational_metrics(),
            'prediction_dist': self.get_prediction_distribution(),
        }
        self._metric_history.append(snap)
        return snap


# Demo
print("\n--- Production Metrics Tracker ---")

if HAS_SKLEARN:
    # Entrenar modelo
    X, y = make_classification(
        n_samples=2000, n_features=20, n_informative=10,
        random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=42
    )

    model = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(max_iter=1000, random_state=42))
    ])
    model.fit(X_train, y_train)

    # Simular produccion
    tracker = ProductionMetricsTracker("churn_model_v1")

    for i in range(len(X_test)):
        start = time.time()
        pred = model.predict(X_test[i:i+1])[0]
        prob = model.predict_proba(X_test[i:i+1])[0, 1]
        latency = (time.time() - start) * 1000

        tracker.log_prediction(
            prediction=pred, probability=prob,
            latency_ms=latency, actual=y_test[i]
        )

    snap = tracker.snapshot()

    print(f"\n  ML Metrics:")
    for k, v in snap['ml_metrics'].items():
        if isinstance(v, float):
            print(f"    {k}: {v:.4f}")

    print(f"\n  Operational Metrics:")
    for k, v in snap['operational'].items():
        if isinstance(v, float):
            print(f"    {k}: {v:.4f}")

    print(f"\n  Prediction Distribution:")
    for k, v in snap['prediction_dist'].items():
        if isinstance(v, float):
            print(f"    {k}: {v:.4f}")


# =====================================================================
#   PARTE 3: DATA DRIFT DETECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: DATA DRIFT DETECTION ===")
print("=" * 80)

"""
DATA DRIFT: la distribucion de las FEATURES cambia.

El modelo fue entrenado con datos de enero-junio.
En diciembre, los patrones de compra cambian (Navidad).
→ Las features tienen distribuciones diferentes.
→ El modelo puede degradarse.

METODOS DE DETECCION:

1. PSI (Population Stability Index):
   Compara histogramas. Simple y efectivo.
   PSI < 0.1: sin drift.
   PSI 0.1-0.25: drift moderado.
   PSI > 0.25: drift significativo.

2. KS Test (Kolmogorov-Smirnov):
   Test estadistico. p < 0.05 = drift.
   Mas sensible que PSI con datasets grandes.

3. Wasserstein Distance (Earth Mover's Distance):
   Distancia entre distribuciones.
   Interpretable: "cuanto trabajo para mover una distribucion a otra".
"""


class DataDriftDetector:
    """Detecta drift en features usando multiples metodos."""

    def __init__(self):
        self._reference: Dict[str, np.ndarray] = {}

    def set_reference(self, feature_name: str, values: np.ndarray):
        """Establece distribucion de referencia (training data)."""
        self._reference[feature_name] = np.array(values, dtype=float)

    def psi(self, reference: np.ndarray, current: np.ndarray,
            n_bins: int = 10) -> float:
        """Population Stability Index."""
        breakpoints = np.percentile(reference, np.linspace(0, 100, n_bins + 1))
        breakpoints[0], breakpoints[-1] = -np.inf, np.inf

        ref_pct = (np.histogram(reference, breakpoints)[0] + 1) / (len(reference) + n_bins)
        cur_pct = (np.histogram(current, breakpoints)[0] + 1) / (len(current) + n_bins)

        return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))

    def ks_test(self, reference: np.ndarray, current: np.ndarray) -> Dict:
        """Kolmogorov-Smirnov test."""
        stat, pvalue = stats.ks_2samp(reference, current)
        return {'statistic': float(stat), 'p_value': float(pvalue),
                'drift': pvalue < 0.05}

    def wasserstein(self, reference: np.ndarray,
                    current: np.ndarray) -> float:
        """Wasserstein (Earth Mover's) distance."""
        return float(stats.wasserstein_distance(reference, current))

    def check_feature(self, feature_name: str,
                      current: np.ndarray) -> Dict:
        """Ejecuta todos los tests para una feature."""
        if feature_name not in self._reference:
            return {'error': f'No reference for {feature_name}'}

        ref = self._reference[feature_name]
        cur = np.array(current, dtype=float)

        psi_val = self.psi(ref, cur)
        ks = self.ks_test(ref, cur)
        wass = self.wasserstein(ref, cur)

        # Verdict
        drift_signals = 0
        if psi_val > 0.1:
            drift_signals += 1
        if ks['drift']:
            drift_signals += 1
        if psi_val > 0.25:
            drift_signals += 1

        return {
            'feature': feature_name,
            'psi': psi_val,
            'ks_statistic': ks['statistic'],
            'ks_pvalue': ks['p_value'],
            'wasserstein': wass,
            'drift_signals': drift_signals,
            'verdict': 'DRIFT' if drift_signals >= 2 else
                       'WARNING' if drift_signals >= 1 else 'OK',
            'ref_mean': float(np.mean(ref)),
            'cur_mean': float(np.mean(cur)),
            'mean_shift_pct': float(
                abs(np.mean(cur) - np.mean(ref)) / (abs(np.mean(ref)) + 1e-10) * 100
            ),
        }

    def check_all(self, current_data: Dict[str, np.ndarray]) -> List[Dict]:
        """Verifica drift en todas las features."""
        results = []
        for name, values in current_data.items():
            if name in self._reference:
                results.append(self.check_feature(name, values))
        return sorted(results, key=lambda x: x.get('psi', 0), reverse=True)


# Demo
print("\n--- Multi-method Drift Detection ---")

if HAS_SKLEARN:
    detector = DataDriftDetector()

    # Features de referencia (training)
    np.random.seed(42)
    ref_features = {
        'income': np.random.lognormal(10, 0.8, 1000),
        'age': np.random.normal(40, 12, 1000),
        'score': np.random.beta(2, 5, 1000),
    }

    for name, values in ref_features.items():
        detector.set_reference(name, values)

    # Escenario 1: sin drift
    np.random.seed(123)
    current_no_drift = {
        'income': np.random.lognormal(10, 0.8, 800),
        'age': np.random.normal(40, 12, 800),
        'score': np.random.beta(2, 5, 800),
    }

    print(f"\n  Escenario 1: SIN drift")
    for result in detector.check_all(current_no_drift):
        print(f"    {result['feature']:>8}: PSI={result['psi']:.4f}, "
              f"KS_p={result['ks_pvalue']:.3f}, "
              f"Wass={result['wasserstein']:.4f} → {result['verdict']}")

    # Escenario 2: drift en income
    current_drift = {
        'income': np.random.lognormal(10.5, 1.0, 800),  # Shifted!
        'age': np.random.normal(40, 12, 800),
        'score': np.random.beta(2, 5, 800),
    }

    print(f"\n  Escenario 2: drift en income")
    for result in detector.check_all(current_drift):
        print(f"    {result['feature']:>8}: PSI={result['psi']:.4f}, "
              f"KS_p={result['ks_pvalue']:.3f}, "
              f"mean_shift={result['mean_shift_pct']:.1f}% → {result['verdict']}")


# =====================================================================
#   PARTE 4: CONCEPT DRIFT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: CONCEPT DRIFT ===")
print("=" * 80)

"""
CONCEPT DRIFT vs DATA DRIFT:

DATA DRIFT: P(X) cambia, pero P(Y|X) no cambia.
  Ejemplo: los clientes son mas jovenes, pero el modelo
  sigue prediciendo correctamente para cada edad.
  → Puede o no afectar performance.

CONCEPT DRIFT: P(Y|X) cambia.
  Ejemplo: antes, comprar > 5 veces/mes = no churn.
  Ahora, comprar > 5 veces/mes = puede ser churn
  (porque compran para stockear antes de irse).
  → SIEMPRE afecta performance.

DETECCION:
  - Monitorear metricas ML en ventana deslizante.
  - Si accuracy baja pero features no tienen drift → concept drift.
  - ADWIN, DDM, Page-Hinkley: algoritmos especificos.
"""


class ConceptDriftDetector:
    """Detecta concept drift monitoreando performance en ventanas."""

    def __init__(self, window_size: int = 200, threshold: float = 0.05):
        self.window_size = window_size
        self.threshold = threshold
        self._errors = deque(maxlen=window_size * 2)
        self._alerts: List[Dict] = []

    def update(self, actual: int, predicted: int):
        """Agrega una observacion."""
        self._errors.append(int(actual != predicted))

    def check(self) -> Dict:
        """Compara error rate de la primera y segunda mitad."""
        errors = list(self._errors)
        if len(errors) < self.window_size:
            return {'status': 'insufficient_data', 'drift': False}

        mid = len(errors) // 2
        old_error = np.mean(errors[:mid])
        new_error = np.mean(errors[mid:])
        change = new_error - old_error

        drift = change > self.threshold

        result = {
            'old_error_rate': float(old_error),
            'new_error_rate': float(new_error),
            'change': float(change),
            'drift': drift,
            'n_samples': len(errors),
        }

        if drift:
            self._alerts.append({**result, 'timestamp': datetime.now()})

        return result


# Demo
print("\n--- Concept Drift Detection ---")

if HAS_SKLEARN:
    cd_detector = ConceptDriftDetector(window_size=200, threshold=0.05)

    # Fase 1: modelo funciona bien
    for i in range(300):
        actual = np.random.binomial(1, 0.5)
        # Modelo acierta 85% del tiempo
        predicted = actual if np.random.random() < 0.85 else 1 - actual
        cd_detector.update(actual, predicted)

    result_ok = cd_detector.check()
    print(f"  Fase 1 (modelo OK):")
    print(f"    Error old: {result_ok['old_error_rate']:.3f}")
    print(f"    Error new: {result_ok['new_error_rate']:.3f}")
    print(f"    Drift: {result_ok['drift']}")

    # Fase 2: modelo se degrada (concept drift)
    for i in range(300):
        actual = np.random.binomial(1, 0.5)
        # Modelo acierta solo 65% (degradado)
        predicted = actual if np.random.random() < 0.65 else 1 - actual
        cd_detector.update(actual, predicted)

    result_drift = cd_detector.check()
    print(f"\n  Fase 2 (concept drift):")
    print(f"    Error old: {result_drift['old_error_rate']:.3f}")
    print(f"    Error new: {result_drift['new_error_rate']:.3f}")
    print(f"    Drift: {result_drift['drift']}")


# =====================================================================
#   PARTE 5: A/B TESTING PARA MODELOS ML
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: A/B TESTING PARA MODELOS ===")
print("=" * 80)

"""
A/B TESTING para modelos ML:

El mismo concepto que A/B testing en producto,
pero comparando MODELOS en vez de UIs.

SETUP:
  - Modelo A (champion/control): modelo actual en produccion.
  - Modelo B (challenger/treatment): nuevo modelo candidato.
  - Trafico se divide aleatoriamente (ej: 90% A, 10% B).
  - Se comparan metricas tras suficientes observaciones.
  - Si B es significativamente mejor → promover B.

METRICAS A COMPARAR:
  - ML metrics: accuracy, F1, AUC.
  - Business metrics: conversion, revenue, engagement.
  - Latencia y reliability.

TEST ESTADISTICO:
  - Z-test o chi-squared para proporciones.
  - t-test para metricas continuas.
  - Necesitas suficiente POWER (n muestras).
"""


class ABTestFramework:
    """Framework para A/B testing de modelos ML."""

    def __init__(self, model_a, model_b,
                 traffic_split: float = 0.5):
        self.model_a = model_a
        self.model_b = model_b
        self.traffic_split = traffic_split

        self._results_a: List[Dict] = []
        self._results_b: List[Dict] = []

    def route(self) -> str:
        """Decide que modelo usar para esta request."""
        return 'A' if np.random.random() < self.traffic_split else 'B'

    def predict_and_log(self, X: np.ndarray,
                        actual: Optional[int] = None) -> Dict:
        """Predice con el modelo asignado y loguea resultado."""
        variant = self.route()
        model = self.model_a if variant == 'A' else self.model_b

        start = time.time()
        pred = model.predict(X.reshape(1, -1))[0]
        prob = model.predict_proba(X.reshape(1, -1))[0, 1]
        latency = (time.time() - start) * 1000

        result = {
            'variant': variant,
            'prediction': int(pred),
            'probability': float(prob),
            'latency_ms': latency,
            'actual': actual,
            'correct': int(pred == actual) if actual is not None else None,
        }

        if variant == 'A':
            self._results_a.append(result)
        else:
            self._results_b.append(result)

        return result

    def analyze(self) -> Dict:
        """Analiza resultados del A/B test."""
        if not self._results_a or not self._results_b:
            return {'status': 'insufficient_data'}

        # Filtrar resultados con actuals
        a_correct = [r['correct'] for r in self._results_a if r['correct'] is not None]
        b_correct = [r['correct'] for r in self._results_b if r['correct'] is not None]

        if len(a_correct) < 30 or len(b_correct) < 30:
            return {'status': 'need_more_samples',
                    'n_a': len(a_correct), 'n_b': len(b_correct)}

        acc_a = np.mean(a_correct)
        acc_b = np.mean(b_correct)

        # Z-test para proporciones
        n_a, n_b = len(a_correct), len(b_correct)
        p_pool = (sum(a_correct) + sum(b_correct)) / (n_a + n_b)
        se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        z_stat = (acc_b - acc_a) / (se + 1e-10)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # Latencias
        lat_a = [r['latency_ms'] for r in self._results_a]
        lat_b = [r['latency_ms'] for r in self._results_b]

        return {
            'n_a': n_a, 'n_b': n_b,
            'accuracy_a': float(acc_a),
            'accuracy_b': float(acc_b),
            'difference': float(acc_b - acc_a),
            'z_statistic': float(z_stat),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'winner': 'B' if acc_b > acc_a and p_value < 0.05 else
                      'A' if acc_a > acc_b and p_value < 0.05 else 'TIE',
            'latency_a_p50': float(np.percentile(lat_a, 50)),
            'latency_b_p50': float(np.percentile(lat_b, 50)),
        }


# Demo
print("\n--- A/B Test ---")

if HAS_SKLEARN:
    # Modelo A: LogReg (actual)
    model_a = Pipeline([('s', StandardScaler()),
                        ('c', LogisticRegression(max_iter=1000, random_state=42))])
    model_a.fit(X_train, y_train)

    # Modelo B: RF (challenger)
    model_b = Pipeline([('s', StandardScaler()),
                        ('c', RandomForestClassifier(100, random_state=42))])
    model_b.fit(X_train, y_train)

    ab = ABTestFramework(model_a, model_b, traffic_split=0.5)

    # Simular trafico
    for i in range(len(X_test)):
        ab.predict_and_log(X_test[i], actual=y_test[i])

    results = ab.analyze()
    print(f"\n  A/B Test Results:")
    print(f"    Model A (LogReg): acc={results['accuracy_a']:.4f} (n={results['n_a']})")
    print(f"    Model B (RF):     acc={results['accuracy_b']:.4f} (n={results['n_b']})")
    print(f"    Difference: {results['difference']:.4f}")
    print(f"    p-value: {results['p_value']:.4f}")
    print(f"    Significant: {results['significant']}")
    print(f"    Winner: {results['winner']}")
    print(f"    Latency A: {results['latency_a_p50']:.3f}ms, "
          f"B: {results['latency_b_p50']:.3f}ms")


# =====================================================================
#   PARTE 6: SHADOW MODE / CHAMPION-CHALLENGER
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: SHADOW MODE ===")
print("=" * 80)

"""
SHADOW MODE: el challenger predice en PARALELO pero NO afecta al usuario.

  Request → Champion (produce respuesta real)
          → Challenger (shadow, solo loguea prediccion)

VENTAJAS:
  - Zero risk: el usuario siempre ve el champion.
  - Comparacion con datos reales de produccion.
  - Detecta problemas de latencia/errores antes del switch.

FLUJO:
  1. Deploy challenger en shadow mode.
  2. Correr 1-2 semanas recolectando predicciones.
  3. Comparar metricas champion vs challenger.
  4. Si challenger es mejor → promover a champion.
  5. El ex-champion se archiva o se pone en shadow.
"""


class ShadowDeployment:
    """Simula shadow mode: champion responde, challenger solo loguea."""

    def __init__(self, champion, challenger):
        self.champion = champion
        self.challenger = challenger
        self._log: List[Dict] = []

    def predict(self, X: np.ndarray) -> int:
        """Solo el champion responde al usuario."""
        # Champion prediction (esta se usa)
        champ_pred = self.champion.predict(X.reshape(1, -1))[0]
        champ_prob = self.champion.predict_proba(X.reshape(1, -1))[0, 1]

        # Challenger prediction (solo loguea)
        chall_pred = self.challenger.predict(X.reshape(1, -1))[0]
        chall_prob = self.challenger.predict_proba(X.reshape(1, -1))[0, 1]

        self._log.append({
            'champion_pred': int(champ_pred),
            'champion_prob': float(champ_prob),
            'challenger_pred': int(chall_pred),
            'challenger_prob': float(chall_prob),
            'agree': champ_pred == chall_pred,
        })

        return int(champ_pred)  # Solo champion responde

    def agreement_rate(self) -> float:
        """Porcentaje de acuerdo entre champion y challenger."""
        if not self._log:
            return 0.0
        return float(np.mean([r['agree'] for r in self._log]))

    def compare(self, actuals: List[int]) -> Dict:
        """Compara rendimiento con actuals."""
        n = min(len(actuals), len(self._log))
        champ_preds = [self._log[i]['champion_pred'] for i in range(n)]
        chall_preds = [self._log[i]['challenger_pred'] for i in range(n)]
        acts = actuals[:n]

        return {
            'champion_accuracy': float(accuracy_score(acts, champ_preds)),
            'challenger_accuracy': float(accuracy_score(acts, chall_preds)),
            'agreement_rate': self.agreement_rate(),
            'n_predictions': n,
        }


# Demo
print("\n--- Shadow Deployment ---")

if HAS_SKLEARN:
    shadow = ShadowDeployment(model_a, model_b)

    for i in range(len(X_test)):
        shadow.predict(X_test[i])

    comparison = shadow.compare(y_test.tolist())
    print(f"  Champion accuracy:   {comparison['champion_accuracy']:.4f}")
    print(f"  Challenger accuracy: {comparison['challenger_accuracy']:.4f}")
    print(f"  Agreement rate:      {comparison['agreement_rate']:.2%}")
    print(f"  N predictions:       {comparison['n_predictions']}")


# =====================================================================
#   PARTE 7: ALERTAS Y THRESHOLDS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: SISTEMA DE ALERTAS ===")
print("=" * 80)

"""
THRESHOLDS TIPICOS:

| Metrica          | Warning    | Critical   |
|------------------|------------|------------|
| Accuracy drop    | > 2%       | > 5%       |
| F1 drop          | > 3%       | > 8%       |
| PSI              | > 0.1      | > 0.25     |
| Latency p99      | > 200ms    | > 500ms    |
| Error rate       | > 1%       | > 5%       |
| Null rate        | > 5%       | > 20%      |
| Positive rate    | ±10%       | ±25%       |
"""


class AlertSystem:
    """Sistema de alertas con severidad configurable."""

    def __init__(self):
        self._rules: List[Dict] = []
        self._alerts: List[Dict] = []

    def add_rule(self, name: str, check_fn: Callable[[Dict], bool],
                 severity: str = "warning", action: str = "notify"):
        self._rules.append({
            'name': name, 'check_fn': check_fn,
            'severity': severity, 'action': action
        })

    def evaluate(self, metrics: Dict) -> List[Dict]:
        """Evalua todas las reglas contra las metricas."""
        triggered = []
        for rule in self._rules:
            try:
                if rule['check_fn'](metrics):
                    alert = {
                        'rule': rule['name'],
                        'severity': rule['severity'],
                        'action': rule['action'],
                        'timestamp': datetime.now(),
                    }
                    triggered.append(alert)
                    self._alerts.append(alert)
            except Exception:
                pass
        return triggered


# Demo
print("\n--- Alert System ---")

alerts = AlertSystem()

alerts.add_rule(
    "accuracy_drop",
    lambda m: m.get('accuracy', 1.0) < 0.80,
    severity="critical", action="retrain"
)
alerts.add_rule(
    "high_latency",
    lambda m: m.get('latency_p99', 0) > 200,
    severity="warning", action="investigate"
)
alerts.add_rule(
    "drift_detected",
    lambda m: m.get('max_psi', 0) > 0.25,
    severity="critical", action="retrain"
)

# Test con metricas buenas
good_metrics = {'accuracy': 0.88, 'latency_p99': 50, 'max_psi': 0.05}
triggered = alerts.evaluate(good_metrics)
print(f"  Good metrics: {len(triggered)} alerts")

# Test con metricas malas
bad_metrics = {'accuracy': 0.72, 'latency_p99': 350, 'max_psi': 0.30}
triggered = alerts.evaluate(bad_metrics)
print(f"  Bad metrics: {len(triggered)} alerts")
for a in triggered:
    print(f"    [{a['severity'].upper()}] {a['rule']} → {a['action']}")


# =====================================================================
#   PARTE 8: CUANDO RE-ENTRENAR
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: CUANDO RE-ENTRENAR ===")
print("=" * 80)

"""
ESTRATEGIAS DE RE-ENTRENAMIENTO:

1. SCHEDULED: re-entrenar cada X tiempo (semanal, mensual).
   + Simple, predecible.
   - Puede re-entrenar sin necesidad o esperar demasiado.

2. TRIGGERED: re-entrenar cuando drift o degradacion detectada.
   + Eficiente, solo cuando necesario.
   - Requiere monitoreo robusto.

3. CONTINUO: re-entrenar con cada batch de datos nuevos.
   + Siempre actualizado.
   - Costoso, riesgo de inestabilidad.

4. HIBRIDO: scheduled + triggered.
   + Lo mejor de ambos.
   - Mas complejo de implementar.

DECISION:
  - Datos cambian rapido (fraude, ads) → triggered o continuo.
  - Datos estables (medicos, manufactura) → scheduled mensual.
  - Siempre: monitorear y alertar independientemente.
"""


class RetrainTrigger:
    """Decide cuando re-entrenar basado en metricas."""

    def __init__(self, accuracy_threshold: float = 0.80,
                 psi_threshold: float = 0.25,
                 max_days: int = 30):
        self.accuracy_threshold = accuracy_threshold
        self.psi_threshold = psi_threshold
        self.max_days = max_days
        self.last_train_date = datetime.now()
        self._decisions: List[Dict] = []

    def should_retrain(self, current_accuracy: float,
                       max_psi: float) -> Dict:
        """Decide si es necesario re-entrenar."""
        days_since = (datetime.now() - self.last_train_date).days
        reasons = []

        if current_accuracy < self.accuracy_threshold:
            reasons.append(f"accuracy={current_accuracy:.3f} < {self.accuracy_threshold}")
        if max_psi > self.psi_threshold:
            reasons.append(f"PSI={max_psi:.3f} > {self.psi_threshold}")
        if days_since > self.max_days:
            reasons.append(f"days={days_since} > {self.max_days}")

        decision = {
            'should_retrain': len(reasons) > 0,
            'reasons': reasons,
            'current_accuracy': current_accuracy,
            'max_psi': max_psi,
            'days_since_last_train': days_since,
            'timestamp': datetime.now(),
        }
        self._decisions.append(decision)
        return decision


# Demo
print("\n--- Retrain Trigger ---")

trigger = RetrainTrigger(accuracy_threshold=0.82, psi_threshold=0.20)

scenarios = [
    (0.88, 0.05, "Modelo funciona bien"),
    (0.79, 0.08, "Accuracy baja"),
    (0.85, 0.30, "Drift detectado"),
    (0.75, 0.35, "Ambos problemas"),
]

for acc, psi, desc in scenarios:
    decision = trigger.should_retrain(acc, psi)
    print(f"\n  {desc}:")
    print(f"    Retrain: {decision['should_retrain']}")
    if decision['reasons']:
        for reason in decision['reasons']:
            print(f"    → {reason}")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: EVALUACION EN PRODUCCION ===")
print("=" * 80)

print("""
  PIPELINE DE MONITOREO:

  Deploy → Metricas ML → Drift Detection → Alertas → Re-train?
              ↓                ↓               ↓
         Dashboard        Data Drift     Concept Drift
                          PSI, KS        Error Rate

  PATRONES:
  1. A/B Testing: comparar modelos con trafico real.
  2. Shadow Mode: zero-risk testing del challenger.
  3. Champion-Challenger: flujo de promocion controlado.
  4. Canary: deploy gradual (1% → 10% → 50% → 100%).

  METRICAS CLAVE:
  - ML: accuracy, F1, AUC (en ventana deslizante).
  - Drift: PSI, KS, Wasserstein (por feature).
  - Ops: latencia p50/p95/p99, error rate.
  - Business: conversion, revenue, engagement.

  REGLA DE ORO:
  Si no monitorizas tu modelo, no sabes si funciona.
  Si no sabes si funciona, no deberia estar en produccion.
""")

print("=" * 80)
print("=== FIN MODULO 16, ARCHIVO 03 ===")
print("=" * 80)
