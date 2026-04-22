# ===========================================================================
# 03_feature_stores_y_produccion.py
# ===========================================================================
# MODULO 15: FEATURE ENGINEERING
# ARCHIVO 03: Feature Stores, Versionado, Pipelines de Produccion
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar la gestion de features en produccion: feature stores,
# versionado, validacion de calidad, pipelines end-to-end,
# y patrones que separan a un notebook de un sistema real.
#
# CONTENIDO:
#   1. Feature Store: que es y por que lo necesitas.
#   2. Implementacion de Feature Store en memoria.
#   3. Feature Registry con metadata y lineage.
#   4. Versionado de features.
#   5. Feature pipelines batch vs streaming.
#   6. Validacion de calidad de features.
#   7. Feature drift detection.
#   8. Point-in-time correctness.
#   9. Feature serving: online vs offline.
#   10. Monitoreo de features en produccion.
#   11. Feature store con Feast (conceptual).
#   12. Pipeline end-to-end completo.
#   13. Patrones anti-fraude: train-serve skew.
#   14. Testing de feature pipelines.
#   15. Best practices y checklist de produccion.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time
import json
import hashlib
from datetime import datetime, timedelta
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn.pipeline import Pipeline
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# =====================================================================
#   PARTE 1: QUE ES UN FEATURE STORE Y POR QUE LO NECESITAS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: FEATURE STORE — EL PROBLEMA ===")
print("=" * 80)

"""
PROBLEMA EN PRODUCCION:

Imagina este escenario (que pasa en TODAS las empresas):

1. Data Scientist A crea feature "avg_purchase_30d" en un notebook.
   - La calcula con pandas groupby.
   - La usa para entrenar un modelo que predice churn.

2. Data Scientist B necesita la misma feature para fraud detection.
   - La recalcula desde cero. Pero usa un JOIN diferente.
   - Resultado: DOS versiones de "avg_purchase_30d" que NO coinciden.

3. El modelo de churn va a produccion.
   - El ingeniero de ML reimplementa la feature en SQL.
   - Pero la logica de edge cases (nulls, outliers) difiere.
   - Resultado: TRAIN-SERVE SKEW — el modelo ve datos diferentes
     en produccion vs entrenamiento.

4. Pasan 3 meses. Nadie sabe:
   - Que features usa cada modelo.
   - Quien creo cada feature.
   - Si la feature sigue siendo valida.

SOLUCION: FEATURE STORE
  Un repositorio CENTRALIZADO donde:
  - Las features se DEFINEN una vez.
  - Se COMPUTAN de forma consistente.
  - Se SIRVEN tanto para training como inference.
  - Se VERSIONAN y se documentan.
  - Se VALIDAN automaticamente.

Herramientas reales: Feast, Tecton, Hopsworks, Vertex AI Feature Store.
Nosotros vamos a construir los CONCEPTOS desde cero.
"""

print("""
  Sin Feature Store:
    Notebook A ──→ feature_v1 ──→ Model A
    Notebook B ──→ feature_v2 ──→ Model B  (¡inconsistente!)
    SQL prod   ──→ feature_v3 ──→ Serving  (¡train-serve skew!)

  Con Feature Store:
    Feature Store ──→ feature (unica fuente de verdad)
       ├──→ Training (offline)
       └──→ Serving  (online)
""")


# =====================================================================
#   PARTE 2: FEATURE STORE EN MEMORIA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: FEATURE STORE DESDE CERO ===")
print("=" * 80)

"""
Vamos a construir un Feature Store conceptual con:
- Registro de features (nombre, descripcion, tipo, funcion de calculo).
- Metadata (quien la creo, cuando, version).
- Compute (batch).
- Validacion basica.

NO es un Feature Store de produccion (para eso usa Feast).
PERO te ensena los conceptos que Feast implementa.
"""


class FeatureDefinition:
    """Define UNA feature: su nombre, tipo, como calcularla, y metadata."""

    def __init__(self, name: str, dtype: str, compute_fn: Callable,
                 description: str = "", owner: str = "unknown",
                 tags: Optional[List[str]] = None):
        self.name = name
        self.dtype = dtype
        self.compute_fn = compute_fn
        self.description = description
        self.owner = owner
        self.tags = tags or []
        self.created_at = datetime.now()
        self.version = 1
        self._history: List[Dict] = []

    def compute(self, data: Any) -> Any:
        """Ejecuta la funcion de calculo sobre los datos."""
        result = self.compute_fn(data)
        self._history.append({
            'timestamp': datetime.now(),
            'n_records': len(result) if hasattr(result, '__len__') else 1,
            'version': self.version,
        })
        return result

    def update(self, new_compute_fn: Callable, reason: str = ""):
        """Actualiza la funcion de calculo, incrementa version."""
        self.version += 1
        self.compute_fn = new_compute_fn
        self._history.append({
            'timestamp': datetime.now(),
            'action': 'version_update',
            'version': self.version,
            'reason': reason,
        })

    def get_metadata(self) -> Dict:
        return {
            'name': self.name,
            'dtype': self.dtype,
            'description': self.description,
            'owner': self.owner,
            'tags': self.tags,
            'version': self.version,
            'created_at': str(self.created_at),
            'n_computations': len([h for h in self._history
                                   if h.get('action') != 'version_update']),
        }

    def __repr__(self):
        return f"Feature({self.name}, v{self.version}, {self.dtype})"


class FeatureStore:
    """
    Feature Store en memoria.

    Responsabilidades:
    1. Registrar features con metadata.
    2. Computar features de forma consistente.
    3. Cachear resultados.
    4. Validar calidad.
    5. Proveer lineage (quien uso que).
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self._features: Dict[str, FeatureDefinition] = {}
        self._cache: Dict[str, Any] = {}
        self._access_log: List[Dict] = []
        self._validators: Dict[str, List[Callable]] = {}

    def register(self, feature_def: FeatureDefinition) -> None:
        """Registra una feature en el store."""
        if feature_def.name in self._features:
            print(f"  [WARN] Feature '{feature_def.name}' ya existe. "
                  f"Usa update() para modificar.")
            return
        self._features[feature_def.name] = feature_def
        print(f"  [OK] Registrada: {feature_def}")

    def register_quick(self, name: str, compute_fn: Callable,
                       dtype: str = "float64", description: str = "",
                       owner: str = "unknown") -> FeatureDefinition:
        """Atajo para registrar features rapidamente."""
        feat = FeatureDefinition(name, dtype, compute_fn, description, owner)
        self.register(feat)
        return feat

    def compute(self, feature_name: str, data: Any,
                use_cache: bool = True) -> Any:
        """Computa una feature, opcionalmente usando cache."""
        if feature_name not in self._features:
            raise KeyError(f"Feature '{feature_name}' no registrada. "
                           f"Disponibles: {self.list_features()}")

        cache_key = f"{feature_name}_v{self._features[feature_name].version}"

        if use_cache and cache_key in self._cache:
            self._log_access(feature_name, "cache_hit")
            return self._cache[cache_key]

        feat = self._features[feature_name]
        result = feat.compute(data)

        # Validar si hay validators registrados
        if feature_name in self._validators:
            for validator in self._validators[feature_name]:
                validator(result, feature_name)

        if use_cache:
            self._cache[cache_key] = result

        self._log_access(feature_name, "computed")
        return result

    def compute_batch(self, feature_names: List[str], data: Any,
                      use_cache: bool = True) -> Dict[str, Any]:
        """Computa multiples features de una vez."""
        results = {}
        for name in feature_names:
            results[name] = self.compute(name, data, use_cache)
        return results

    def add_validator(self, feature_name: str, validator_fn: Callable):
        """Agrega un validador a una feature."""
        if feature_name not in self._validators:
            self._validators[feature_name] = []
        self._validators[feature_name].append(validator_fn)

    def list_features(self) -> List[str]:
        return list(self._features.keys())

    def get_metadata(self, feature_name: str = None) -> Dict:
        if feature_name:
            return self._features[feature_name].get_metadata()
        return {n: f.get_metadata() for n, f in self._features.items()}

    def get_lineage(self, feature_name: str) -> List[Dict]:
        """Retorna el historial de accesos a una feature."""
        return [log for log in self._access_log
                if log['feature'] == feature_name]

    def _log_access(self, feature_name: str, action: str):
        self._access_log.append({
            'feature': feature_name,
            'action': action,
            'timestamp': datetime.now(),
        })

    def invalidate_cache(self, feature_name: str = None):
        """Invalida cache de una feature o todas."""
        if feature_name:
            keys = [k for k in self._cache if k.startswith(feature_name)]
            for k in keys:
                del self._cache[k]
        else:
            self._cache.clear()

    def summary(self):
        """Imprime resumen del feature store."""
        print(f"\n  Feature Store: '{self.name}'")
        print(f"  Features registradas: {len(self._features)}")
        print(f"  Cache entries: {len(self._cache)}")
        print(f"  Total accesos: {len(self._access_log)}")
        for name, feat in self._features.items():
            meta = feat.get_metadata()
            print(f"    - {name} (v{meta['version']}, {meta['dtype']}, "
                  f"computed {meta['n_computations']}x) [{meta['owner']}]")


# --- Demo del Feature Store ---

print("\n--- Construyendo Feature Store ---")

store = FeatureStore("ecommerce_features")

if HAS_PANDAS:
    # Datos de ejemplo
    np.random.seed(42)
    n_customers = 1000
    df_customers = pd.DataFrame({
        'customer_id': range(n_customers),
        'age': np.random.randint(18, 75, n_customers),
        'income': np.random.lognormal(10, 0.8, n_customers),
        'n_purchases': np.random.poisson(10, n_customers),
        'total_spent': np.random.lognormal(6, 1.5, n_customers),
        'days_since_last': np.random.exponential(30, n_customers).astype(int),
        'is_premium': np.random.binomial(1, 0.2, n_customers),
    })

    # Registrar features
    store.register_quick(
        name="avg_order_value",
        compute_fn=lambda df: df['total_spent'] / (df['n_purchases'] + 1),
        dtype="float64",
        description="Valor medio por pedido (total_spent / n_purchases)",
        owner="data_team"
    )

    store.register_quick(
        name="purchase_frequency",
        compute_fn=lambda df: df['n_purchases'] / (df['days_since_last'] + 1),
        dtype="float64",
        description="Frecuencia de compra normalizada",
        owner="data_team"
    )

    store.register_quick(
        name="income_log",
        compute_fn=lambda df: np.log1p(df['income']),
        dtype="float64",
        description="Log-transform de income para reducir skewness",
        owner="ml_team"
    )

    store.register_quick(
        name="customer_segment",
        compute_fn=lambda df: pd.cut(
            df['total_spent'],
            bins=[0, 100, 500, 2000, float('inf')],
            labels=[0, 1, 2, 3]
        ).astype(int),
        dtype="int64",
        description="Segmento de cliente por gasto total",
        owner="business_team"
    )

    # Computar
    print("\n--- Computando features ---")
    features = store.compute_batch(
        ['avg_order_value', 'purchase_frequency', 'income_log'],
        df_customers
    )

    for name, values in features.items():
        print(f"  {name}: mean={values.mean():.4f}, std={values.std():.4f}")

    # Cache hit
    print("\n--- Cache ---")
    features_cached = store.compute('avg_order_value', df_customers)
    print(f"  Segunda llamada usa cache (sin recomputar)")

    store.summary()


# =====================================================================
#   PARTE 3: FEATURE REGISTRY Y METADATA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: REGISTRY, METADATA Y LINEAGE ===")
print("=" * 80)

"""
Un Feature Registry es el CATALOGO de todas las features:
- Que features existen.
- Quien las creo y cuando.
- Que modelos las usan.
- Su historial de cambios.
- Dependencias entre features.

Sin registry, a los 6 meses nadie sabe que features hay,
cuales son redundantes, o cuales se pueden borrar.
"""


class FeatureRegistry:
    """Catalogo centralizado de features con busqueda y dependencias."""

    def __init__(self):
        self._registry: Dict[str, Dict] = {}
        self._dependencies: Dict[str, List[str]] = {}
        self._model_usage: Dict[str, List[str]] = {}

    def register(self, name: str, metadata: Dict):
        """Registra una feature con su metadata."""
        self._registry[name] = {
            **metadata,
            'registered_at': datetime.now(),
        }

    def add_dependency(self, feature: str, depends_on: List[str]):
        """Declara que 'feature' depende de otras features."""
        self._dependencies[feature] = depends_on

    def register_model_usage(self, model_name: str, features: List[str]):
        """Registra que features usa un modelo."""
        self._model_usage[model_name] = features

    def search(self, query: str = "", tag: str = "",
               owner: str = "") -> List[str]:
        """Busca features por nombre, tag, o owner."""
        results = []
        for name, meta in self._registry.items():
            if query and query.lower() not in name.lower():
                continue
            if tag and tag not in meta.get('tags', []):
                continue
            if owner and owner != meta.get('owner', ''):
                continue
            results.append(name)
        return results

    def get_impact_analysis(self, feature: str) -> Dict:
        """Que modelos se ven afectados si cambio esta feature?"""
        affected_models = [
            model for model, feats in self._model_usage.items()
            if feature in feats
        ]
        # Features que dependen de esta
        downstream = [
            f for f, deps in self._dependencies.items()
            if feature in deps
        ]
        return {
            'feature': feature,
            'affected_models': affected_models,
            'downstream_features': downstream,
            'impact_level': 'HIGH' if affected_models else 'LOW',
        }

    def get_unused_features(self) -> List[str]:
        """Features que ningun modelo usa."""
        used = set()
        for feats in self._model_usage.values():
            used.update(feats)
        return [f for f in self._registry if f not in used]

    def summary(self):
        print(f"\n  Registry: {len(self._registry)} features, "
              f"{len(self._model_usage)} models")
        for name in self._registry:
            impact = self.get_impact_analysis(name)
            print(f"    {name}: {len(impact['affected_models'])} models, "
                  f"impact={impact['impact_level']}")


# Demo
print("\n--- Feature Registry ---")

registry = FeatureRegistry()

features_meta = {
    'avg_order_value': {'owner': 'data_team', 'tags': ['ecommerce', 'monetary']},
    'purchase_frequency': {'owner': 'data_team', 'tags': ['ecommerce', 'behavioral']},
    'income_log': {'owner': 'ml_team', 'tags': ['demographic', 'transform']},
    'customer_segment': {'owner': 'business_team', 'tags': ['ecommerce', 'derived']},
    'clv_score': {'owner': 'ml_team', 'tags': ['ecommerce', 'derived']},
}

for name, meta in features_meta.items():
    registry.register(name, meta)

registry.add_dependency('clv_score', ['avg_order_value', 'purchase_frequency'])
registry.add_dependency('customer_segment', ['avg_order_value'])

registry.register_model_usage('churn_model', ['avg_order_value', 'purchase_frequency', 'income_log'])
registry.register_model_usage('fraud_model', ['purchase_frequency', 'income_log'])

# Busqueda
print(f"  Search 'order': {registry.search(query='order')}")
print(f"  Search tag 'ecommerce': {registry.search(tag='ecommerce')}")
print(f"  Search owner 'ml_team': {registry.search(owner='ml_team')}")

# Impact analysis
impact = registry.get_impact_analysis('purchase_frequency')
print(f"\n  Impact de cambiar 'purchase_frequency':")
print(f"    Modelos afectados: {impact['affected_models']}")
print(f"    Features downstream: {impact['downstream_features']}")
print(f"    Nivel: {impact['impact_level']}")

print(f"\n  Features sin usar: {registry.get_unused_features()}")

registry.summary()


# =====================================================================
#   PARTE 4: VERSIONADO DE FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: VERSIONADO DE FEATURES ===")
print("=" * 80)

"""
PROBLEMA: cambias la logica de una feature y rompes un modelo en produccion.

SOLUCION: versionar features como versionas codigo.

Cada version de una feature:
- Tiene un hash unico basado en su logica.
- Se puede reproducir exactamente.
- Convive con versiones anteriores durante la transicion.

Patron: Blue-Green features.
  - v1 sigue sirviendo produccion.
  - v2 se prueba en shadow mode.
  - Si v2 es mejor, se promueve y v1 se depreca.
"""


class VersionedFeature:
    """Feature con historial de versiones completo."""

    def __init__(self, name: str, compute_fn: Callable,
                 description: str = ""):
        self.name = name
        self.description = description
        self._versions: OrderedDict[int, Dict] = OrderedDict()
        self._active_version = 1
        self._add_version(compute_fn, "initial version")

    def _add_version(self, compute_fn: Callable, reason: str):
        """Anade una nueva version."""
        version = len(self._versions) + 1
        # Hash de la funcion para detectar cambios
        fn_hash = hashlib.md5(
            compute_fn.__code__.co_code
        ).hexdigest()[:8]

        self._versions[version] = {
            'compute_fn': compute_fn,
            'created_at': datetime.now(),
            'reason': reason,
            'fn_hash': fn_hash,
            'status': 'active' if version == 1 else 'staging',
        }

    def update(self, new_compute_fn: Callable, reason: str = "update"):
        """Crea nueva version sin afectar la activa."""
        self._add_version(new_compute_fn, reason)
        latest = max(self._versions.keys())
        print(f"  [VERSION] {self.name}: v{latest} creada (staging). "
              f"Activa: v{self._active_version}")

    def promote(self, version: int):
        """Promueve una version a activa."""
        if version not in self._versions:
            raise ValueError(f"Version {version} no existe")
        # Deprecar la activa anterior
        if self._active_version in self._versions:
            self._versions[self._active_version]['status'] = 'deprecated'
        self._versions[version]['status'] = 'active'
        self._active_version = version
        print(f"  [PROMOTE] {self.name}: v{version} es ahora activa")

    def compute(self, data: Any, version: int = None) -> Any:
        """Computa usando la version activa o una especifica."""
        v = version or self._active_version
        return self._versions[v]['compute_fn'](data)

    def compare_versions(self, data: Any, v1: int, v2: int) -> Dict:
        """Compara output de dos versiones."""
        result_v1 = self.compute(data, v1)
        result_v2 = self.compute(data, v2)

        if hasattr(result_v1, '__len__'):
            diff = np.abs(np.array(result_v1) - np.array(result_v2))
            return {
                'mean_diff': float(np.mean(diff)),
                'max_diff': float(np.max(diff)),
                'pct_changed': float(np.mean(diff > 1e-10)),
                'correlation': float(np.corrcoef(
                    np.array(result_v1).flatten(),
                    np.array(result_v2).flatten()
                )[0, 1]),
            }
        return {'v1': result_v1, 'v2': result_v2}

    def history(self):
        print(f"\n  Version history: {self.name}")
        for v, info in self._versions.items():
            marker = " ◄ ACTIVE" if v == self._active_version else ""
            print(f"    v{v}: hash={info['fn_hash']}, "
                  f"status={info['status']}, "
                  f"reason='{info['reason']}'{marker}")


# Demo
print("\n--- Versionado de features ---")

if HAS_PANDAS:
    # v1: media simple
    feat_aov = VersionedFeature(
        "avg_order_value",
        compute_fn=lambda df: df['total_spent'] / (df['n_purchases'] + 1),
        description="Average order value"
    )

    # v2: con cap de outliers
    feat_aov.update(
        lambda df: np.clip(
            df['total_spent'] / (df['n_purchases'] + 1),
            0, df['total_spent'].quantile(0.99) / (df['n_purchases'].quantile(0.01) + 1)
        ),
        reason="Cap outliers at p99"
    )

    # Comparar
    comparison = feat_aov.compare_versions(df_customers, 1, 2)
    print(f"\n  Comparacion v1 vs v2:")
    for k, v in comparison.items():
        print(f"    {k}: {v:.6f}")

    # Promover v2
    feat_aov.promote(2)
    feat_aov.history()


# =====================================================================
#   PARTE 5: VALIDACION DE CALIDAD DE FEATURES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: VALIDACION DE CALIDAD ===")
print("=" * 80)

"""
Una feature puede ser TECNICAMENT CORRECTA pero CUALITATIVAMENTE MALA.

Validaciones esenciales:
1. Nulls: % de valores nulos.
2. Rango: valores fuera de rango esperado.
3. Distribucion: skewness, curtosis.
4. Unicidad: % de valores unicos (cardinalidad).
5. Correlacion: con el target (debe ser significativa).
6. Estabilidad: la distribucion no deberia cambiar drasticamente.
"""


class FeatureValidator:
    """Valida calidad de features con reglas configurables."""

    def __init__(self):
        self.rules: List[Dict] = []
        self.results: List[Dict] = []

    def add_rule(self, name: str, check_fn: Callable[[Any], bool],
                 severity: str = "warning"):
        """Agrega una regla de validacion."""
        self.rules.append({
            'name': name,
            'check_fn': check_fn,
            'severity': severity,
        })

    def validate(self, feature_name: str, values: Any) -> Dict:
        """Ejecuta todas las reglas sobre los valores."""
        results = {'feature': feature_name, 'checks': [], 'passed': True}

        for rule in self.rules:
            try:
                passed = rule['check_fn'](values)
            except Exception as e:
                passed = False

            result = {
                'rule': rule['name'],
                'passed': passed,
                'severity': rule['severity'],
            }
            results['checks'].append(result)

            if not passed and rule['severity'] == 'error':
                results['passed'] = False

        self.results.append(results)
        return results

    def report(self, results: Dict):
        """Imprime reporte de validacion."""
        status = "✓ PASSED" if results['passed'] else "✗ FAILED"
        print(f"\n  Validacion '{results['feature']}': {status}")
        for check in results['checks']:
            icon = "✓" if check['passed'] else "✗"
            print(f"    {icon} {check['rule']} [{check['severity']}]")


# Crear validador con reglas estandar
validator = FeatureValidator()

# Reglas genericas
validator.add_rule(
    "no_nulls",
    lambda v: not np.any(pd.isna(v)) if HAS_PANDAS else not np.any(np.isnan(v)),
    severity="error"
)

validator.add_rule(
    "no_infinites",
    lambda v: not np.any(np.isinf(np.array(v, dtype=float))),
    severity="error"
)

validator.add_rule(
    "variance_gt_zero",
    lambda v: float(np.std(np.array(v, dtype=float))) > 1e-10,
    severity="warning"
)

validator.add_rule(
    "no_extreme_outliers",
    lambda v: float(np.max(np.abs(np.array(v, dtype=float)))) < 1e10,
    severity="warning"
)

validator.add_rule(
    "reasonable_cardinality",
    lambda v: len(np.unique(np.array(v))) > 1,
    severity="warning"
)

# Validar features
if HAS_PANDAS:
    print("\n--- Validando features ---")

    test_features = {
        'avg_order_value': df_customers['total_spent'] / (df_customers['n_purchases'] + 1),
        'income_log': np.log1p(df_customers['income']),
        'bad_constant': np.zeros(len(df_customers)),
    }

    for name, values in test_features.items():
        results = validator.validate(name, values)
        validator.report(results)


# =====================================================================
#   PARTE 6: FEATURE DRIFT DETECTION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: FEATURE DRIFT DETECTION ===")
print("=" * 80)

"""
DRIFT: la distribucion de una feature CAMBIA entre entrenamiento y produccion.

Tipos:
1. DATA DRIFT: la distribucion de X cambia (ej: inflacion sube ingresos).
2. CONCEPT DRIFT: la relacion X->Y cambia (ej: el COVID cambia patrones).
3. FEATURE DRIFT: una feature especifica se desvia de su baseline.

Deteccion:
- PSI (Population Stability Index): compara distribuciones.
    PSI < 0.1: estable.
    PSI 0.1-0.25: cambio moderado.
    PSI > 0.25: cambio significativo → investigar.

- KS test: test estadistico de 2 muestras.
- Wasserstein distance: distancia entre distribuciones.
"""


def calculate_psi(expected: np.ndarray, actual: np.ndarray,
                  n_bins: int = 10) -> float:
    """
    Population Stability Index.

    Compara la distribucion 'expected' (training) con 'actual' (produccion).
    PSI = sum((actual_pct - expected_pct) * ln(actual_pct / expected_pct))
    """
    # Crear bins basados en la distribucion esperada
    breakpoints = np.percentile(expected, np.linspace(0, 100, n_bins + 1))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf

    expected_counts = np.histogram(expected, breakpoints)[0]
    actual_counts = np.histogram(actual, breakpoints)[0]

    # Evitar division por cero
    expected_pct = (expected_counts + 1) / (len(expected) + n_bins)
    actual_pct = (actual_counts + 1) / (len(actual) + n_bins)

    psi = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    return float(psi)


def interpret_psi(psi: float) -> str:
    """Interpreta el valor de PSI."""
    if psi < 0.1:
        return "ESTABLE - no hay drift significativo"
    elif psi < 0.25:
        return "MODERADO - monitorear, posible drift"
    else:
        return "SIGNIFICATIVO - drift detectado, investigar"


class FeatureDriftMonitor:
    """Monitorea drift de features comparando con baseline."""

    def __init__(self):
        self._baselines: Dict[str, np.ndarray] = {}
        self._history: List[Dict] = []

    def set_baseline(self, feature_name: str, values: np.ndarray):
        """Establece la distribucion baseline (de training)."""
        self._baselines[feature_name] = np.array(values, dtype=float)

    def check_drift(self, feature_name: str,
                    current_values: np.ndarray) -> Dict:
        """Compara valores actuales con baseline."""
        if feature_name not in self._baselines:
            return {'error': f'No baseline for {feature_name}'}

        baseline = self._baselines[feature_name]
        current = np.array(current_values, dtype=float)

        psi = calculate_psi(baseline, current)
        interpretation = interpret_psi(psi)

        # Estadisticas comparativas
        result = {
            'feature': feature_name,
            'psi': psi,
            'interpretation': interpretation,
            'baseline_mean': float(np.mean(baseline)),
            'current_mean': float(np.mean(current)),
            'mean_shift': float(np.mean(current) - np.mean(baseline)),
            'baseline_std': float(np.std(baseline)),
            'current_std': float(np.std(current)),
        }

        self._history.append({**result, 'timestamp': datetime.now()})
        return result

    def check_all(self, current_data: Dict[str, np.ndarray]) -> List[Dict]:
        """Verifica drift en todas las features monitoreadas."""
        results = []
        for name, values in current_data.items():
            if name in self._baselines:
                results.append(self.check_drift(name, values))
        return results

    def get_alerts(self, threshold: float = 0.25) -> List[Dict]:
        """Retorna features con drift por encima del threshold."""
        return [h for h in self._history if h.get('psi', 0) > threshold]


# Demo drift detection
print("\n--- Drift Detection ---")

if HAS_PANDAS:
    drift_monitor = FeatureDriftMonitor()

    # Baseline = datos de training
    baseline_income = df_customers['income'].values
    drift_monitor.set_baseline('income', baseline_income)
    drift_monitor.set_baseline('age', df_customers['age'].values.astype(float))

    # Simular datos de produccion (con drift)
    np.random.seed(123)
    # Income con inflacion (drift leve)
    prod_income_mild = np.random.lognormal(10.1, 0.8, 1000)
    # Income con cambio dramatico (drift fuerte)
    prod_income_strong = np.random.lognormal(11, 1.2, 1000)

    print(f"\n  Drift check - income (mild shift):")
    result_mild = drift_monitor.check_drift('income', prod_income_mild)
    print(f"    PSI: {result_mild['psi']:.4f} → {result_mild['interpretation']}")
    print(f"    Mean: {result_mild['baseline_mean']:.0f} → {result_mild['current_mean']:.0f}")

    print(f"\n  Drift check - income (strong shift):")
    result_strong = drift_monitor.check_drift('income', prod_income_strong)
    print(f"    PSI: {result_strong['psi']:.4f} → {result_strong['interpretation']}")
    print(f"    Mean: {result_strong['baseline_mean']:.0f} → {result_strong['current_mean']:.0f}")

    # Sin drift (mismo generador)
    prod_income_same = np.random.lognormal(10, 0.8, 1000)
    result_same = drift_monitor.check_drift('income', prod_income_same)
    print(f"\n  Drift check - income (no drift):")
    print(f"    PSI: {result_same['psi']:.4f} → {result_same['interpretation']}")


# =====================================================================
#   PARTE 7: POINT-IN-TIME CORRECTNESS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: POINT-IN-TIME CORRECTNESS ===")
print("=" * 80)

"""
EL ERROR MAS SUTIL Y DESTRUCTIVO en ML:

Imagina que entrenas un modelo para predecir si un cliente comprara
en los proximos 7 dias. Usas como feature "n_purchases_last_30d".

PERO: al entrenar, calculas esa feature HOY, incluyendo compras
que ocurrieron DESPUES del momento de prediccion.
→ LEAKAGE TEMPORAL. El modelo ve el futuro.

POINT-IN-TIME: para cada ejemplo de training, las features DEBEN
calcularse usando SOLO datos disponibles HASTA ese momento.

  Fecha prediccion: 2024-03-15
  Features: solo datos hasta 2024-03-14
  Label: compro entre 2024-03-15 y 2024-03-22?

  Si calculas n_purchases_last_30d usando datos hasta hoy (2024-12-01),
  estas incluyendo compras de marzo-diciembre → LEAKAGE.
"""


class PointInTimeFeatureComputer:
    """Computa features respetando point-in-time."""

    def __init__(self):
        self._feature_fns: Dict[str, Callable] = {}

    def register(self, name: str, compute_fn: Callable):
        """
        compute_fn debe aceptar (data, cutoff_date) y devolver
        solo features calculadas con datos <= cutoff_date.
        """
        self._feature_fns[name] = compute_fn

    def compute_at(self, feature_name: str, data: Any,
                   cutoff_date: datetime) -> Any:
        """Computa una feature con datos hasta cutoff_date."""
        return self._feature_fns[feature_name](data, cutoff_date)


# Demo
print("\n--- Point-in-Time Features ---")

if HAS_PANDAS:
    # Historial de transacciones
    np.random.seed(42)
    n_txns = 2000
    df_txns = pd.DataFrame({
        'customer_id': np.random.choice(range(100), n_txns),
        'date': pd.date_range('2024-01-01', periods=n_txns, freq='4h'),
        'amount': np.random.lognormal(3, 1, n_txns),
    })

    pit = PointInTimeFeatureComputer()

    def purchases_last_30d(data, cutoff):
        """Numero de compras en los ultimos 30 dias ANTES de cutoff."""
        cutoff_ts = pd.Timestamp(cutoff)
        start = cutoff_ts - pd.Timedelta(days=30)
        mask = (data['date'] >= start) & (data['date'] < cutoff_ts)
        return data[mask].groupby('customer_id').size()

    def avg_amount_last_30d(data, cutoff):
        """Media de monto en los ultimos 30 dias ANTES de cutoff."""
        cutoff_ts = pd.Timestamp(cutoff)
        start = cutoff_ts - pd.Timedelta(days=30)
        mask = (data['date'] >= start) & (data['date'] < cutoff_ts)
        return data[mask].groupby('customer_id')['amount'].mean()

    pit.register('purchases_30d', purchases_last_30d)
    pit.register('avg_amount_30d', avg_amount_last_30d)

    # Calcular en dos momentos distintos
    cutoff_1 = datetime(2024, 4, 1)
    cutoff_2 = datetime(2024, 6, 1)

    p30_apr = pit.compute_at('purchases_30d', df_txns, cutoff_1)
    p30_jun = pit.compute_at('purchases_30d', df_txns, cutoff_2)

    print(f"  Purchases 30d (cutoff=Apr 1): {p30_apr.mean():.1f} promedio")
    print(f"  Purchases 30d (cutoff=Jun 1): {p30_jun.mean():.1f} promedio")
    print(f"  Mismo feature, distinto momento → distinto resultado (correcto)")


# =====================================================================
#   PARTE 8: FEATURE SERVING (ONLINE VS OFFLINE)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: FEATURE SERVING ===")
print("=" * 80)

"""
DOS MODOS DE SERVIR FEATURES:

1. OFFLINE (batch):
   - Para TRAINING y batch inference.
   - Se computan sobre datasets completos.
   - Latencia no importa.
   - Se pueden usar joins complejos y aggregaciones.

2. ONLINE (real-time):
   - Para INFERENCE en produccion.
   - Latencia < 100ms.
   - Features pre-computadas y cacheadas en KV store.
   - Solo lookup, NO computacion compleja.

PATRON:
  Batch pipeline (diario/horario) → Computa features → Store en Redis/DynamoDB
  Serving API → Lee features pre-computadas → Modelo → Prediccion
"""


class OnlineFeatureServer:
    """Simula un servidor de features online con cache."""

    def __init__(self, max_latency_ms: float = 100):
        self._store: Dict[str, Dict[str, float]] = {}
        self.max_latency_ms = max_latency_ms
        self._stats = {'hits': 0, 'misses': 0, 'total_latency_ms': 0}

    def materialize(self, feature_name: str,
                    entity_values: Dict[str, float]):
        """Pre-computa y almacena features (batch process)."""
        self._store[feature_name] = entity_values

    def get_features(self, entity_id: str,
                     feature_names: List[str]) -> Dict[str, Optional[float]]:
        """Sirve features para una entidad (online, baja latencia)."""
        start = time.time()

        result = {}
        for fname in feature_names:
            if fname in self._store and entity_id in self._store[fname]:
                result[fname] = self._store[fname][entity_id]
                self._stats['hits'] += 1
            else:
                result[fname] = None
                self._stats['misses'] += 1

        latency = (time.time() - start) * 1000
        self._stats['total_latency_ms'] += latency
        return result

    def stats(self):
        total = self._stats['hits'] + self._stats['misses']
        hit_rate = self._stats['hits'] / max(total, 1)
        avg_latency = self._stats['total_latency_ms'] / max(total, 1)
        print(f"  Online server: {total} lookups, "
              f"hit_rate={hit_rate:.2%}, avg_latency={avg_latency:.3f}ms")


# Demo
print("\n--- Online Feature Serving ---")

server = OnlineFeatureServer()

# Materializar features (simulando batch pipeline)
server.materialize('avg_order_value', {
    str(i): float(np.random.lognormal(3, 1)) for i in range(100)
})
server.materialize('purchase_frequency', {
    str(i): float(np.random.uniform(0, 5)) for i in range(100)
})

# Servir (simulando API call)
for entity_id in ['0', '42', '99', '999']:
    features = server.get_features(
        entity_id, ['avg_order_value', 'purchase_frequency']
    )
    found = sum(1 for v in features.values() if v is not None)
    print(f"  Entity {entity_id}: {found}/{len(features)} features found")

server.stats()


# =====================================================================
#   PARTE 9: TESTING DE FEATURE PIPELINES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: TESTING DE FEATURES ===")
print("=" * 80)

"""
Las features son CODIGO y necesitan TESTS:

1. UNIT TESTS: cada feature produce output correcto para input conocido.
2. SCHEMA TESTS: dtype, shape, rango, nulls.
3. STATISTICAL TESTS: distribucion razonable, sin drift.
4. INTEGRATION TESTS: pipeline completo funciona end-to-end.
5. REGRESSION TESTS: nueva version no rompe modelos existentes.
"""


class FeatureTestSuite:
    """Suite de tests para features."""

    def __init__(self):
        self._tests: List[Dict] = []
        self._results: List[Dict] = []

    def add_test(self, name: str, test_fn: Callable[[], bool],
                 category: str = "unit"):
        self._tests.append({
            'name': name, 'test_fn': test_fn, 'category': category
        })

    def run(self) -> Dict:
        """Ejecuta todos los tests."""
        passed = 0
        failed = 0
        errors = []

        for test in self._tests:
            try:
                result = test['test_fn']()
                if result:
                    passed += 1
                else:
                    failed += 1
                    errors.append(f"FAIL: {test['name']}")
            except Exception as e:
                failed += 1
                errors.append(f"ERROR: {test['name']}: {str(e)}")

        summary = {
            'total': len(self._tests),
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'success_rate': passed / max(len(self._tests), 1),
        }
        self._results.append(summary)
        return summary

    def report(self, summary: Dict):
        status = "✓ ALL PASSED" if summary['failed'] == 0 else "✗ FAILURES"
        print(f"\n  Test Results: {status}")
        print(f"    Passed: {summary['passed']}/{summary['total']}")
        if summary['errors']:
            for err in summary['errors']:
                print(f"    {err}")


# Demo
print("\n--- Feature Tests ---")

suite = FeatureTestSuite()

# Unit tests
suite.add_test(
    "avg_order_value_positive",
    lambda: all(df_customers['total_spent'] / (df_customers['n_purchases'] + 1) >= 0)
    if HAS_PANDAS else True,
    "unit"
)

suite.add_test(
    "income_log_finite",
    lambda: all(np.isfinite(np.log1p(df_customers['income'])))
    if HAS_PANDAS else True,
    "unit"
)

suite.add_test(
    "psi_same_distribution_low",
    lambda: calculate_psi(
        np.random.randn(1000), np.random.randn(1000)
    ) < 0.1,
    "statistical"
)

suite.add_test(
    "psi_different_distribution_high",
    lambda: calculate_psi(
        np.random.randn(1000), np.random.randn(1000) + 5
    ) > 0.25,
    "statistical"
)

results = suite.run()
suite.report(results)


# =====================================================================
#   PARTE 10: PIPELINE END-TO-END Y BEST PRACTICES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: PIPELINE E2E Y BEST PRACTICES ===")
print("=" * 80)

"""
PIPELINE COMPLETO DE FEATURES EN PRODUCCION:

  Raw Data → Ingestion → Feature Computation → Validation → Store → Serving
                                                    ↓
                                              Monitoring & Alerts

CHECKLIST DE PRODUCCION:
  ☐ Cada feature tiene tests unitarios.
  ☐ Cada feature tiene metadata (owner, description, version).
  ☐ Features versionadas; cambios no rompen modelos activos.
  ☐ Point-in-time correctness verificado.
  ☐ Drift monitoring configurado con alertas.
  ☐ Train-serve skew < 1% (misma logica batch y online).
  ☐ Feature freshness SLA definido.
  ☐ Backfill strategy documentada.
  ☐ Cache invalidation policy definida.
  ☐ Feature deprecation policy en vigor.
"""


class ProductionFeaturePipeline:
    """Pipeline end-to-end de features para produccion."""

    def __init__(self, name: str):
        self.name = name
        self.store = FeatureStore(f"{name}_store")
        self.drift_monitor = FeatureDriftMonitor()
        self.validator = FeatureValidator()
        self.test_suite = FeatureTestSuite()
        self._status = "initialized"

        # Reglas de validacion estandar
        self.validator.add_rule("no_nulls",
            lambda v: not np.any(pd.isna(v)) if HAS_PANDAS else True,
            severity="error")
        self.validator.add_rule("no_infinites",
            lambda v: not np.any(np.isinf(np.array(v, dtype=float))),
            severity="error")
        self.validator.add_rule("has_variance",
            lambda v: float(np.std(np.array(v, dtype=float))) > 1e-10,
            severity="warning")

    def register_feature(self, name: str, compute_fn: Callable,
                         dtype: str = "float64", description: str = "",
                         owner: str = "unknown"):
        """Registra feature con validacion y monitoring automatico."""
        self.store.register_quick(name, compute_fn, dtype, description, owner)

    def run(self, data: Any, feature_names: List[str] = None) -> Dict[str, Any]:
        """Ejecuta pipeline completo: compute → validate → monitor."""
        self._status = "running"
        names = feature_names or self.store.list_features()

        # 1. Computar features
        results = self.store.compute_batch(names, data)

        # 2. Validar
        validation_passed = True
        for name, values in results.items():
            val_result = self.validator.validate(name, values)
            if not val_result['passed']:
                validation_passed = False
                print(f"  [ALERT] Feature '{name}' fallo validacion")

        # 3. Monitorear drift (si hay baseline)
        for name, values in results.items():
            if name in self.drift_monitor._baselines:
                drift = self.drift_monitor.check_drift(name, np.array(values))
                if drift['psi'] > 0.25:
                    print(f"  [ALERT] Drift detectado en '{name}': "
                          f"PSI={drift['psi']:.4f}")

        self._status = "completed" if validation_passed else "completed_with_warnings"
        return results

    def set_baselines(self, data: Any):
        """Establece baselines para drift monitoring."""
        for name in self.store.list_features():
            values = self.store.compute(name, data)
            self.drift_monitor.set_baseline(name, np.array(values))
        print(f"  Baselines set for {len(self.store.list_features())} features")

    def health_check(self) -> Dict:
        """Status del pipeline."""
        alerts = self.drift_monitor.get_alerts()
        return {
            'pipeline': self.name,
            'status': self._status,
            'n_features': len(self.store.list_features()),
            'n_drift_alerts': len(alerts),
            'cache_size': len(self.store._cache),
        }


# Demo pipeline E2E
print("\n--- Pipeline End-to-End ---")

if HAS_PANDAS:
    pipeline = ProductionFeaturePipeline("ecommerce")

    pipeline.register_feature(
        'avg_order_value',
        lambda df: df['total_spent'] / (df['n_purchases'] + 1),
        description="Average order value", owner="data_team"
    )
    pipeline.register_feature(
        'income_log',
        lambda df: np.log1p(df['income']),
        description="Log income", owner="ml_team"
    )
    pipeline.register_feature(
        'recency_score',
        lambda df: 1.0 / (df['days_since_last'] + 1),
        description="Recency score (inverse of days)", owner="ml_team"
    )

    # Baselines con datos de training
    pipeline.set_baselines(df_customers)

    # Ejecutar con datos "nuevos" (simular produccion)
    print("\n  Ejecutando pipeline con datos de produccion...")
    np.random.seed(999)
    df_prod = pd.DataFrame({
        'customer_id': range(500),
        'age': np.random.randint(18, 75, 500),
        'income': np.random.lognormal(10, 0.8, 500),
        'n_purchases': np.random.poisson(10, 500),
        'total_spent': np.random.lognormal(6, 1.5, 500),
        'days_since_last': np.random.exponential(30, 500).astype(int),
        'is_premium': np.random.binomial(1, 0.2, 500),
    })

    features = pipeline.run(df_prod)

    print(f"\n  Features computadas:")
    for name, values in features.items():
        print(f"    {name}: mean={values.mean():.4f}, shape={values.shape}")

    health = pipeline.health_check()
    print(f"\n  Health: {health}")


# =====================================================================
#   RESUMEN FINAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== RESUMEN: FEATURE STORES Y PRODUCCION ===")
print("=" * 80)

print("""
  CONCEPTOS CLAVE:

  1. FEATURE STORE: fuente unica de verdad para features.
     → Evita inconsistencias y duplicacion.

  2. REGISTRY: catalogo con metadata, busqueda, impact analysis.
     → Saber que features hay y quien las usa.

  3. VERSIONADO: blue-green features, comparacion de versiones.
     → Cambiar features sin romper modelos.

  4. VALIDACION: nulls, rango, varianza, outliers.
     → Detectar problemas ANTES de que lleguen al modelo.

  5. DRIFT DETECTION: PSI, KS test.
     → Alertar cuando los datos cambian.

  6. POINT-IN-TIME: features calculadas respetando temporalidad.
     → Evitar leakage temporal (el error mas comun y sutil).

  7. SERVING: offline (batch) vs online (real-time).
     → Misma feature, dos modos de acceso.

  8. TESTING: unit, schema, statistical, integration.
     → Features son codigo y necesitan tests.

  9. PIPELINE E2E: compute → validate → monitor → serve.
     → Automatizacion completa.

  HERRAMIENTAS REALES:
    - Feast (open source)
    - Tecton (enterprise)
    - Hopsworks (open source)
    - Vertex AI Feature Store (GCP)
    - SageMaker Feature Store (AWS)
""")

print("=" * 80)
print("=== FIN MODULO 15, ARCHIVO 03 ===")
print("=" * 80)
