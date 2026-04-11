reproducibilidad_datos.md
Introducción

En proyectos de Machine Learning y Data Science, reproducibilidad significa que cualquier persona o tú mismo en el futuro puedas obtener exactamente los mismos resultados a partir del mismo código y datos. Esto es fundamental para:

Validar experimentos.

Compartir modelos con confianza.

Evitar sorpresas al desplegar a producción.

Mantener integridad de los pipelines de datos.

1️⃣ Versionar datos

Guardar copias exactas de datasets usados en experimentos.

Mantener hashes o checksums (MD5, SHA256) para verificar que no se modificaron.

Usar carpetas separadas por versión:

data/
├── v1/
│   ├── train.csv
│   └── test.csv
├── v2/
│   └── train.csv


Siempre registra qué versión del dataset se usó para cada experimento.

2️⃣ Versionar código y pipelines

Usa control de versiones (git) y tags o ramas para cada experimento importante.

Mantén archivos de configuración separados (JSON, YAML, .env) para que no haya valores hardcodeados que rompan reproducibilidad.

Documenta versiones de librerías en un requirements.txt o environment.yml.

3️⃣ Semillas aleatorias (Random Seeds)

Muchos modelos y algoritmos dependen de aleatoriedad:

Scikit-learn, PyTorch, TensorFlow, NumPy, Python random.

Para obtener los mismos resultados:

import random
import numpy as np
import torch

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)  # si se usa GPU
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


Nota: Algunos algoritmos paralelos aún pueden introducir ligeras diferencias, pero la mayoría será reproducible.

4️⃣ Guardar preprocesamientos

No solo el dataset original importa:

Escaladores (StandardScaler, MinMaxScaler)

Codificadores (OneHotEncoder)

Selección de features

Siempre guarda estos objetos junto con el modelo, usando pickle o joblib:

from sklearn.preprocessing import StandardScaler
import joblib

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, "scaler.joblib")


Esto asegura que nuevos datos se transformen exactamente igual.

5️⃣ Guardar modelos con versión

Cada modelo entrenado debe tener su propio nombre/versionado, como vimos en modelos_serializados.py.

Evita sobrescribir modelos antiguos.

6️⃣ Control de experimentos

Opciones recomendadas:

MLflow: registro de métricas, hiperparámetros y artefactos.

Weights & Biases (wandb): dashboards y seguimiento de experimentos.

DVC (Data Version Control): versiona datasets y pipelines completos.

Esto te permite reconstruir experimentos exactos sin depender de memoria o suposiciones.

7️⃣ Reproducibilidad en pipelines

Cuando crees pipelines de ML:

Cada paso debe ser determinístico si se busca reproducibilidad.

Evita side effects inesperados (modificar datos globales, usar variables externas).

Documenta orden de pasos y dependencias.

Ejemplo de pipeline reproducible:

1. Cargar dataset v1
2. Limpiar y normalizar datos
3. Aplicar feature selection
4. Entrenar modelo con seed=42
5. Guardar modelo + preprocesadores
6. Evaluar y registrar métricas

8️⃣ Hashing y validación

Para confirmar que los datos no han cambiado:

import hashlib

def hash_file(path: str) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

print(hash_file("data/train.csv"))


Guarda estos hashes junto con tus experimentos.

9️⃣ Buenas prácticas adicionales

Separar entorno de desarrollo del de producción.

Evitar paths absolutos y usar rutas relativas.

Guardar metadatos de datasets y modelos (fecha, autor, versión de librerías).

Automatizar reproducibilidad con scripts en lugar de hacer pasos manuales.

Resumen

Datos, código y modelos versionados

Seeds y preprocesamiento consistentes

Pipelines determinísticos

Logs y hashes para verificación

Uso de herramientas de tracking (MLflow, DVC, wandb)

Con esto, un proyecto de Data/ML pasa de ser frágil y propenso a errores a ser fiable, auditable y reproducible, incluso años después de creado.