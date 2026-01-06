"""
errores_modelos.py
===================

Objetivo:
- Detectar y manejar errores en entrenamiento e inferencia de modelos
- Evitar que errores rompan pipelines de ML
- Facilitar trazabilidad, logging y depuración profesional
"""

import logging
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.exceptions import NotFittedError

# -------------------------------------------------------------------
# 1️⃣ EJEMPLO DE DATASET
# -------------------------------------------------------------------

# Datos de ejemplo
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# -------------------------------------------------------------------
# 2️⃣ ENTRENAMIENTO DE MODELO
# -------------------------------------------------------------------

def entrenar_modelo(X, y):
    """
    Entrena un modelo de regresión lineal
    Maneja errores comunes: datos vacíos, shape incorrecto, valores NaN
    """
    try:
        if X.size == 0 or y.size == 0:
            raise ValueError("Datos de entrenamiento vacíos")

        if np.isnan(X).any() or np.isnan(y).any():
            raise ValueError("Datos contienen NaN")

        modelo = LinearRegression()
        modelo.fit(X, y)
        logging.info("Modelo entrenado correctamente")
        return modelo

    except ValueError as e:
        logging.error(f"Error en entrenamiento: {e}")
        raise
    except Exception as e:
        logging.critical("Error inesperado durante el entrenamiento", exc_info=True)
        raise

# Entrenamiento exitoso
modelo = entrenar_modelo(X, y)

# -------------------------------------------------------------------
# 3️⃣ INFERENCIA DE MODELO
# -------------------------------------------------------------------

def predecir(modelo, X_nuevos):
    """
    Realiza predicciones con el modelo entrenado
    Maneja errores típicos: modelo no entrenado, shape inválido
    """
    try:
        if X_nuevos.size == 0:
            raise ValueError("Datos de predicción vacíos")
        return modelo.predict(X_nuevos)
    except NotFittedError:
        logging.error("El modelo no ha sido entrenado")
        raise
    except ValueError as e:
        logging.error(f"Error en predicción: {e}")
        raise
    except Exception as e:
        logging.critical("Error inesperado durante inferencia", exc_info=True)
        raise

# Predicción exitosa
X_test = np.array([[6], [7]])
predicciones = predecir(modelo, X_test)
print("Predicciones:", predicciones)

# -------------------------------------------------------------------
# 4️⃣ BUENAS PRÁCTICAS PROFESIONALES
# -------------------------------------------------------------------

# 1️⃣ Validar datos antes de entrenar o predecir (shape, NaN, tipos)
# 2️⃣ Diferenciar errores recuperables (ValueError) de críticos (Exception)
# 3️⃣ Loggear errores con contexto suficiente (fila, columna, pipeline)
# 4️⃣ Capturar NotFittedError para prevenir inferencia antes de entrenamiento
# 5️⃣ Separar entrenamiento, evaluación e inferencia en funciones distintas
# 6️⃣ Evitar detener todo el pipeline si es posible, manejar errores parciales
# 7️⃣ Mantener reproducibilidad documentando versiones de datos y modelos
