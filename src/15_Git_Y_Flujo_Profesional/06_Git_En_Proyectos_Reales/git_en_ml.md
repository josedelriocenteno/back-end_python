# Git en ML: Versionado de Modelos y Experimentos

El Machine Learning (ML) rompe el flujo tradicional de Git porque manejamos archivos binarios gigantes (modelos) y conjuntos de datos que Git no puede gestionar eficientemente.

## 1. El límite de Git: Los Archivos Binarios
Git no está diseñado para guardar archivos de 500MB (`modelo_final.h5`). El repositorio se volvería lentísimo.
- **Solución:** Usa **Git LFS (Large File Storage)** para archivos grandes o herramientas específicas como **DVC (Data Version Control)**.

## 2. Código vs. Pesos
- Git guarda el **Código** del modelo (la arquitectura de la red neuronal).
- DVC/MLflow guarda los **Pesos** (los parámetros entrenados) y el **Dataset**.

## 3. Trazabilidad de Experimentos
En cada commit de Git deberías poder saber qué hiperparámetros se usaron.
- **Tip Senior:** Usa etiquetas (tags) para marcar commits que produjeron modelos con buena precisión: `accuracy-0.94-v2`.

## 4. Colaboración en Notebooks
Al igual que en Data Engineering, los notebooks son difíciles de mezclar. Prioriza "refactorizar" el código del notebook a archivos `.py` en cuanto la lógica sea estable para poder usar el flujo normal de PRs.

## 5. CI/CD para Modelos (CML)
Usa **CML (Continuous Machine Learning)** para que, al hacer una PR, GitHub Actions entrene una versión pequeña del modelo y publique los resultados de precisión directamente como un comentario en la PR.

## Resumen: El Triángulo de la Reproducibilidad
Un proyecto de ML profesional versiona: **Código + Datos + Modelo**. Git gestiona el código, y herramientas auxiliares gestionan el resto, permitiendo que cualquier experimento sea recreado meses después.
