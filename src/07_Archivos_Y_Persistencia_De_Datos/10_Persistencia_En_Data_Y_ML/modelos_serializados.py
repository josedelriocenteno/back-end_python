"""
modelos_serializados.py
=======================

OBJETIVO
--------
Proveer funciones y patrones para:
1. Guardar modelos entrenados en disco
2. Cargar modelos para predicciones posteriores
3. Mantener versionado y reproducibilidad
4. Evitar problemas típicos de compatibilidad y corrupción de modelos

TODO explicado paso a paso, sin asumir conocimientos previos.
"""

from pathlib import Path
import pickle
import joblib  # Alternativa eficiente para modelos grandes
from typing import Any, Optional

# ============================================================
# 1️⃣ Carpeta base para modelos
# ============================================================
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "modelos"
MODELS_DIR.mkdir(exist_ok=True)  # Crear si no existe

# ============================================================
# 2️⃣ Guardar modelos
# ============================================================
def guardar_modelo_pickle(modelo: Any, nombre_archivo: str, versionar: bool = True):
    """
    Guarda un modelo Python usando pickle.
    
    Args:
        modelo: objeto del modelo (scikit-learn, statsmodels, etc.)
        nombre_archivo: nombre del archivo final
        versionar: si True guarda backup de versión anterior
    """
    path = MODELS_DIR / f"{nombre_archivo}.pkl"

    if versionar and path.exists():
        backup_path = MODELS_DIR / f"{nombre_archivo}.bak"
        path.replace(backup_path)
        print(f"[Modelo] Backup creado: {backup_path}")

    with path.open("wb") as f:
        pickle.dump(modelo, f)
    print(f"[Modelo] Guardado con pickle: {path}")

def guardar_modelo_joblib(modelo: Any, nombre_archivo: str, versionar: bool = True):
    """
    Guarda un modelo usando joblib (más eficiente para objetos grandes).
    
    Args:
        modelo: objeto del modelo
        nombre_archivo: nombre del archivo final
        versionar: si True crea backup
    """
    path = MODELS_DIR / f"{nombre_archivo}.joblib"

    if versionar and path.exists():
        backup_path = MODELS_DIR / f"{nombre_archivo}.bak"
        path.replace(backup_path)
        print(f"[Modelo] Backup creado: {backup_path}")

    joblib.dump(modelo, path)
    print(f"[Modelo] Guardado con joblib: {path}")

# ============================================================
# 3️⃣ Cargar modelos
# ============================================================
def cargar_modelo_pickle(nombre_archivo: str) -> Optional[Any]:
    """
    Carga un modelo previamente guardado con pickle.
    
    Args:
        nombre_archivo: nombre del archivo sin extensión
    
    Returns:
        objeto del modelo o None si falla
    """
    path = MODELS_DIR / f"{nombre_archivo}.pkl"
    if not path.exists():
        print(f"[Modelo] Archivo no encontrado: {path}")
        return None

    try:
        with path.open("rb") as f:
            modelo = pickle.load(f)
        print(f"[Modelo] Cargado correctamente: {path}")
        return modelo
    except Exception as e:
        print(f"[Modelo] Error cargando modelo: {path} | Detalle: {e}")
        return None

def cargar_modelo_joblib(nombre_archivo: str) -> Optional[Any]:
    """
    Carga un modelo previamente guardado con joblib.
    """
    path = MODELS_DIR / f"{nombre_archivo}.joblib"
    if not path.exists():
        print(f"[Modelo] Archivo no encontrado: {path}")
        return None
    
    try:
        modelo = joblib.load(path)
        print(f"[Modelo] Cargado correctamente: {path}")
        return modelo
    except Exception as e:
        print(f"[Modelo] Error cargando modelo: {path} | Detalle: {e}")
        return None

# ============================================================
# 4️⃣ Buenas prácticas adicionales
# ============================================================

# - Siempre versionar modelos para no perder entrenamientos previos.
# - Usar joblib para modelos grandes (p. ej., RandomForest con muchos árboles).
# - Mantener estructura clara: MODELS_DIR / nombre_modelo.ext
# - Evitar guardar modelos directamente en el root del proyecto.
# - Documentar la versión de librerías al guardar modelo (recomendado en JSON paralelo).

# ============================================================
# 5️⃣ Ejemplo de uso
# ============================================================

if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris

    # 1️⃣ Entrenar modelo
    iris = load_iris()
    X, y = iris.data, iris.target
    modelo_rf = RandomForestClassifier(n_estimators=10, random_state=42)
    modelo_rf.fit(X, y)

    # 2️⃣ Guardar modelo
    guardar_modelo_pickle(modelo_rf, "iris_rf")
    guardar_modelo_joblib(modelo_rf, "iris_rf_joblib")

    # 3️⃣ Cargar modelo
    modelo_cargado_pickle = cargar_modelo_pickle("iris_rf")
    modelo_cargado_joblib = cargar_modelo_joblib("iris_rf_joblib")

    # 4️⃣ Predecir usando modelo cargado
    if modelo_cargado_pickle is not None:
        predicciones = modelo_cargado_pickle.predict(X)
        print(f"[Predicciones pickle] {predicciones[:5]}")

    if modelo_cargado_joblib is not None:
        predicciones = modelo_cargado_joblib.predict(X)
        print(f"[Predicciones joblib] {predicciones[:5]}")
