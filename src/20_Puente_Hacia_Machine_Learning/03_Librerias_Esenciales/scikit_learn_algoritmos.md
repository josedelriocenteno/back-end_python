# Scikit-Learn: El estándar de oro para algoritmos

**Scikit-Learn** (`sklearn`) es la librería más popular para el Machine Learning tradicional (no profundo). Contiene cientos de algoritmos de clasificación, regresión y clustering listos para usar.

## 1. La Filosofía de Scikit-Learn: `fit` y `predict`
Todos los algoritmos en sklearn comparten la misma interfaz, lo que hace que sea muy fácil cambiar de uno a otro:
1.  **Instanciar:** `model = RandomForestClassifier()`
2.  **Entrenar:** `model.fit(X_train, y_train)` (Aprende de los datos).
3.  **Predecir:** `predictions = model.predict(X_test)` (Aplica lo aprendido).

## 2. Herramientas de Pre-procesamiento
No solo tiene algoritmos, también tiene herramientas para preparar los datos:
*   **Escalado:** `StandardScaler` para que todas las columnas tengan el mismo rango.
*   **Codificación:** `OneHotEncoder` para convertir texto en números.
*   **División:** `train_test_split` para separar los datos automáticamente.

## 3. Pipelines de Scikit-Learn
Esta es la funcionalidad favorita de los ingenieros. Permite encadenar pasos:
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Creamos un flujo automático: Escalado -> Modelo
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svc', SVC())
])

pipe.fit(X_train, y_train)
```
*   **Ventaja:** Evitas el error de procesar los datos de entrenamiento de una forma y los de producción de otra. El pipeline garantiza la consistencia.

## 4. Evaluación del Modelo
Sklearn facilita medir el éxito:
*   `accuracy_score()`, `f1_score()` para clasificación.
*   `mean_squared_error()` para regresión.
*   `plot_confusion_matrix()` para visualizar errores.

## 5. ¿Cuándo usar Scikit-Learn?
*   Para datos tabulares (CSV, SQL).
*   Para modelos clásicos (Regresiones, Árboles, SVM).
*   **No se usa** para Visión Artificial pesada o Procesamiento de Lenguaje complejo (ahí usamos TensorFlow o PyTorch).

## Resumen: Potencia y Consistencia
Scikit-Learn es la librería que democratizó el Machine Learning. Su API consistente y su amplia documentación la hacen la herramienta ideal para empezar a construir modelos profesionales de alta calidad con muy pocas líneas de código.
