"""
reproducibilidad.py
===================

Buenas prácticas: asegurar reproducibilidad en ML/Data

Objetivos:
- Garantizar que experimentos puedan repetirse exactamente
- Controlar aleatoriedad en librerías y pipelines
- Registrar configuraciones y datos usados
"""

# -------------------------------------------------------------------
# 1️⃣ PROBLEMA
# -------------------------------------------------------------------

# Muchas veces en ML:
# - Cada entrenamiento produce resultados distintos
# - Métricas cambian aunque los datos y el código sean iguales
# - Dificulta debugging, comparación de modelos y despliegue

# Causas frecuentes:
# - Random seed no fijada
# - Shuffle de datasets
# - Librerías con paralelismo / operaciones no determinísticas
# - Diferentes versiones de librerías o datos

# -------------------------------------------------------------------
# 2️⃣ FIJAR RANDOM SEED
# -------------------------------------------------------------------

import random
import numpy as np
import torch  # si usas PyTorch

SEED = 42

# Python random
random.seed(SEED)

# Numpy
np.random.seed(SEED)

# PyTorch
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# -------------------------------------------------------------------
# 3️⃣ CONTROLAR ALEATORIEDAD EN DATASETS
# -------------------------------------------------------------------

from sklearn.model_selection import train_test_split
import pandas as pd

# Ejemplo de dataset
df = pd.DataFrame({
    "x": range(100),
    "y": [x*2 + np.random.randn() for x in range(100)]
})

# Split reproducible
train_df, test_df = train_test_split(df, test_size=0.2, random_state=SEED, shuffle=True)

# -------------------------------------------------------------------
# 4️⃣ PIPELINES PURAS
# -------------------------------------------------------------------

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función pura: transformación reproducible
    """
    df_new = df.copy()
    df_new["x2"] = df_new["x"] ** 2
    return df_new

# -------------------------------------------------------------------
# 5️⃣ GUARDAR CONFIGURACIÓN Y METADATA
# -------------------------------------------------------------------

import json
from dataclasses import dataclass, asdict

@dataclass
class ConfigExperimento:
    seed: int
    modelo: str
    parametros: dict

config = ConfigExperimento(
    seed=SEED,
    modelo="RegresionLineal",
    parametros={"alpha": 0.01, "iteraciones": 1000}
)

# Guardar configuración para reproducibilidad
with open("config_experimento.json", "w") as f:
    json.dump(asdict(config), f, indent=2)

# -------------------------------------------------------------------
# 6️⃣ GUARDAR RESULTADOS Y MODELO
# -------------------------------------------------------------------

from sklearn.linear_model import LinearRegression
from joblib import dump

# Features y target
X_train = feature_engineering(train_df)[["x", "x2"]].values
y_train = train_df["y"].values

# Entrenar modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Guardar modelo
dump(modelo, "modelo_entrenado.joblib")

# -------------------------------------------------------------------
# 7️⃣ BENEFICIOS DE ESTE ENFOQUE
# -------------------------------------------------------------------

# 1. Experimentos reproducibles: mismos datos + misma seed → mismo modelo
# 2. Debugging sencillo
# 3. Comparación de experimentos consistente
# 4. Documentación y trazabilidad completas
# 5. Preparado para despliegue seguro en producción

# -------------------------------------------------------------------
# 8️⃣ CONCLUSIÓN
# -------------------------------------------------------------------

# Principios clave de reproducibilidad en ML/Data:
# - Fijar random seeds en todas las librerías
# - Controlar shuffle y splits de datasets
# - Pipelines puras y modularizadas
# - Guardar configuración, metadatos y modelos
# - Versionar datasets y librerías
# - Documentar todo para reproducibilidad profesional
