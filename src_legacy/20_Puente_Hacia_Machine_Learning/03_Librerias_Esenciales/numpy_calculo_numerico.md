# NumPy: El corazón matemático de Python

**NumPy** (Numerical Python) es la librería fundamental para el cómputo científico en Python. Casi todas las librerías de Machine Learning (Pandas, Scikit-Learn, TensorFlow) están construidas sobre ella.

## 1. El Array de NumPy (ndarray)
La pieza central es el objeto `array`. A diferencia de las listas de Python, los arrays de NumPy:
*   **Son homogéneos:** Todos los elementos deben ser del mismo tipo (ej: todos float64).
*   **Son eficientes:** Están escritos en C, lo que los hace órdenes de magnitud más rápidos y compactos en memoria que las listas.
*   **Vectorización:** Permiten realizar operaciones sobre todos los elementos sin usar bucles `for`.

## 2. Operaciones Vectorizadas
```python
import numpy as np

# Creación de un array
pesos = np.array([70, 80, 65, 90])

# Operación sobre todo el array al instante
pesos_kg = pesos * 0.453  # Convierte libras a kg en un solo paso
```

## 3. Funciones Útiles para ML
*   `np.mean()`, `np.median()`, `np.std()`: Para análisis estadístico rápido.
*   `np.reshape()`: Vital para cambiar la forma de los datos (ej: de una lista plana a una matriz de imagen).
*   `np.transpose()`: Invertir filas por columnas (álgebra lineal).
*   `np.dot()`: Producto escalar, la base de cómo las neuronas procesan información.

## 4. Broadcasting
Es la capacidad de NumPy de operar con arrays de diferentes formas.
*   Si sumas un número a una matriz, NumPy entiende que debe sumar ese número a **cada elemento** de la matriz automáticamente.

## 5. ¿Por qué un Data Engineer necesita saber NumPy?
Aunque no escribas algoritmos desde cero, entender los arrays de NumPy es esencial para:
*   Manejar datos de imagen o audio (que son arrays de números).
*   Optimizar cálculos masivos que con Python puro serían imposibles.
*   Interoperar con modelos de ML que esperan datos en este formato.

## Resumen: Velocidad y Precisión
NumPy transforma a Python en una herramienta de cálculo de alto rendimiento. Dominar sus arrays y operaciones vectorizadas es el primer paso para poder manejar los volúmenes de datos que requiere el Machine Learning moderno.
