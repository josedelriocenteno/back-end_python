"""
reproducibilidad_errores.py
============================

Objetivo:
- Detectar y manejar errores en pipelines de ML
- Asegurar reproducibilidad y trazabilidad
- Facilitar debugging en entornos complejos
"""

import logging
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.exceptions import NotFittedError
import hashlib
import json

# -------------------------------------------------------------------
# 1️⃣ VERSIONADO DE DATOS
# -------------------------------------------------------------------

def hash_dataframe(df: pd.DataFrame) -> str:
    """
    Genera hash único para un DataFrame
    - Permite detectar cambios en datos
    """
    df_bytes = df.to_json().encode('utf-8')
    return hashlib.md5(df_bytes).hexdigest()

# Dataset de ejemplo
datos = {
    "id": [1, 2, 3],
    "valor": [10, 20, 30]
}
df = pd.DataFrame(datos)
hash_datos = hash_dataframe(df)
logging.info(f"Hash de dataset: {hash_datos}")

# -------------------------------------------------------------------
# 2️⃣ PIPELINE SIMPLIFICADO DE ML
# -------------------------------------------------------------------

def entrenar_pipeline(df: pd.DataFrame):
    """
    Pipeline de entrenamiento con validaciones y logging
    """
    try:
        # Validación de datos
        if df.isnull().any().any():
            raise ValueError("Datos contienen valores nulos")
        if df.empty:
            raise ValueError("Dataset vacío")

        X = df[["id"]].values
        y = df["valor"].values

        # Entrenamiento del modelo
        modelo = LinearRegression()
        modelo.fit(X, y)
        logging.info("Modelo entrenado correctamente")

        return modelo

    except ValueError as e:
        logging.error(f"Error en pipeline: {e}")
        raise
    except Exception as e:
        logging.critical("Error inesperado en pipeline", exc_info=True)
        raise

modelo = entrenar_pipeline(df)

# -------------------------------------------------------------------
# 3️⃣ DEBUG EN INFERENCIA
# -------------------------------------------------------------------

def predecir_pipeline(modelo, X_nuevos):
    """
    Predicción con logging y manejo de errores
    """
    try:
        if X_nuevos.size == 0:
            raise ValueError("Datos de predicción vacíos")
        return modelo.predict(X_nuevos)
    except NotFittedError:
        logging.error("El modelo no está entrenado")
        raise
    except Exception as e:
        logging.critical("Error inesperado durante inferencia", exc_info=True)
        raise

X_test = np.array([[4], [5]])
predicciones = predecir_pipeline(modelo, X_test)
logging.info(f"Predicciones: {predicciones}")

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Versionar datasets usando hashes para reproducibilidad
# 2️⃣ Loggear hashes, versiones de modelos y parámetros
# 3️⃣ Separar claramente validación, entrenamiento e inferencia
# 4️⃣ Capturar errores esperados (ValueError, NotFittedError)
# 5️⃣ Loggear errores críticos con exc_info para debugging profundo
# 6️⃣ Mantener pipelines reproducibles, con semillas aleatorias si hay stochasticidad
# 7️⃣ Evitar que un fallo en un paso bloquee todo el pipeline sin registro
# 8️⃣ Facilitar auditoría posterior de resultados y errores
