# Tracking de Experimentos con MLflow

Cuando entrenas modelos, haces cientos de pruebas: cambias una variable, pruebas otro algoritmo, ajustas un parámetro... Si no anotas todo, olvidarás cuál fue la prueba que dio el mejor resultado. **MLflow** es la solución a este caos.

## 1. ¿Qué es MLflow Tracking?
Es un servidor centralizado (o local) donde tu código de Python envía información sobre cada entrenamiento.

## 2. Los 4 elementos que registramos

### A. Parámetros
Configuraciones fijas del experimento.
*   `learning_rate`: 0.01
*   `epochs`: 100
*   `batch_size`: 32

### B. Métricas
Resultados numéricos del experimento.
*   `accuracy`: 0.94
*   `f1_score`: 0.92
*   Registra la métrica en cada iteración para ver la curva de aprendizaje.

### C. Artefactos
Archivos generados.
*   El archivo `.pkl` del modelo.
*   Gráficos PDF de la importancia de las variables.
*   Logs del entrenamiento.

### D. Tags y Notas
Información contextual (ej: "Prueba con datos de diciembre", "Usuario: Jose").

## 3. Ejemplo de uso conceptual
```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("algoritmo", "RandomForest")
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_artifact("modelo.pkl")
```

## 4. Interfaz de Usuario (UI)
MLflow te ofrece una web donde puedes ver una tabla con todos tus experimentos, compararlos entre sí y ver gráficos de cuál es el modelo más preciso con un simple clic.

## 5. Model Serving
MLflow también facilita el despliegue del modelo como una API REST con un solo comando, lo que acorta el tiempo desde que el Data Scientist termina su trabajo hasta que el Data Engineer lo tiene en producción.

## Resumen: Orden en el Laboratorio
MLflow es el "cuaderno de bitácora" del científico de datos. Al automatizar el registro de cada prueba, eliminamos el error humano y permitimos que el equipo se centre en mejorar la IA sabiendo que el historial de éxitos y fracasos está a salvo y organizado.
