# Normalización y Escalado: Igualando las fuerzas

En un modelo de ML, el valor absoluto de un número puede confundir al algoritmo si las escalas son muy diferentes. Debemos "nivelar el campo de juego".

## 1. El problema de las escalas
Imagina que entrenas un modelo para predecir salud con dos atributos:
*   **Edad:** Rango de 0 a 100.
*   **Ingresos Anuales:** Rango de 0 a 200.000.
El algoritmo pensará que los ingresos son 2.000 veces más importantes que la edad solo porque el número es más grande. Esto es un error.

## 2. Técnicas Principales

### A. Min-Max Scaling (Normalización)
Escala todos los valores entre 0 y 1.
*   **Fórmula:** $x_{new} = \frac{x - min}{max - min}$
*   **Uso:** Cuando conoces los límites exactos de los datos y no tienes muchos outliers.

### B. Standard Scaling (Estandarización)
Transforma los datos para que tengan una media de 0 y una desviación estándar de 1.
*   **Fórmula:** $x_{new} = \frac{x - \mu}{\sigma}$
*   **Uso:** Es la más común. Muy robusta para la mayoría de algoritmos (especialmente SVM y Redes Neuronales).

## 3. ¿Cuándo esOBLIGATORIO escalar?
*   **K-Nearest Neighbors (KNN):** Calcula distancias. Si una escala es mayor, la distancia se arruina.
*   **Gradient Descent:** Algoritmos que optimizan (Redes Neuronales, Regresión Logística). Convergen mucho más rápido si los datos están escalados.
*   **PCA:** Necesita que todas las variables tengan la misma varianza.

## 4. Cuándo NO es necesario
*   **Árboles de Decisión y Random Forest:** Son inmunes a la escala. Les da igual si un número es 1 o 1.000.000, solo miran dónde hacer el "corte".

## 5. El error del "Data Leakage"
**Importante:** Calcula el escalado solo con los datos de **Entrenamiento** (`fit`), y luego aplica ese mismo escalado a los datos de **Test** (`transform`). Nunca calcules el máximo o la media sobre todo el dataset a la vez, o estarás "haciendo trampas".

## Resumen: Proporción Justa
El escalado garantiza que cada atributo contribuya al modelo según su importancia real, no según la magnitud de su unidad de medida. Es una de las "higiene" básicas que separan a un entusiasta de un profesional del Machine Learning.
