"""
Ejemplo Básico: Entrenamiento de un modelo de clasificación.
Este script muestra el flujo completo: Carga -> Preparación -> Entrenamiento -> Evaluación.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Crear o cargar datos (Simulamos un dataset de flores Iris simplificado)
data = {
    'largo_petalo': [1.4, 1.3, 1.5, 4.5, 4.8, 5.1, 5.8, 6.2, 5.9],
    'ancho_petalo': [0.2, 0.2, 0.2, 1.3, 1.5, 1.6, 2.1, 2.3, 2.2],
    'especie': ['setosa', 'setosa', 'setosa', 'versicolor', 'versicolor', 'versicolor', 'virginica', 'virginica', 'virginica']
}

df = pd.DataFrame(data)

# 2. Separar características (X) de la etiqueta (y)
X = df[['largo_petalo', 'ancho_petalo']]
y = df['especie']

# 3. Dividir en Entrenamiento y Test
# Usamos un tamaño de test pequeño por el poco volumen de datos del ejemplo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. Crear e Instanciar el Modelo
model = RandomForestClassifier(n_estimators=10)

# 5. Entrenamiento (Fit)
print("Entrenando el modelo...")
model.fit(X_train, y_train)

# 6. Predicción
print("Realizando predicciones...")
y_pred = model.predict(X_test)

# 7. Evaluación
accuracy = accuracy_score(y_test, y_pred)
print(f"\nExactitud del modelo: {accuracy * 100:.2f}%")
print("\nInforme detallado:")
print(classification_report(y_test, y_pred))

# 8. Uso con datos nuevos
nueva_flor = pd.DataFrame({'largo_petalo': [2.0], 'ancho_petalo': [0.5]})
prediccion = model.predict(nueva_flor)
print(f"\nPredicción para una flor de 2.0x0.5: {prediccion[0]}")
