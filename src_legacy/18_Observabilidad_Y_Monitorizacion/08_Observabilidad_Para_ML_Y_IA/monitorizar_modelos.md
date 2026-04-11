# Monitorizar Modelos de ML: Más allá del código

Monitorizar un modelo de Machine Learning es mucho más difícil que monitorizar una API. Un modelo puede no "romperse" nunca (siempre devuelve una respuesta), pero su respuesta puede dejar de ser útil.

## 1. Salud del Servicio (Infraestructura)
Esto es lo que ya conoces:
*   **Latencia de inferencia:** ¿Cuánto tarda el modelo en predecir? (Vital si es en tiempo real).
*   **Uso de memoria/GPU:** Las máquinas de ML son muy caras, hay que optimizarlas.
*   **Throughput:** ¿Cuántas predicciones por segundo estamos sirviendo?

## 2. Model Drift (Desviación del Modelo)
El mundo real cambia y el modelo se queda obsoleto.
*   **Data Drift:** El dato que llega hoy es diferente al dato con el que se entrenó (ej: cambian las modas o el comportamiento de los sensores).
*   **Concept Drift:** La relación entre las variables cambia (ej: antes de la pandemia, ciertos patrones de viaje eran normales; después, ya no).

## 3. Monitorizando la Calidad del Dato de Entrada
Un modelo de ML es una función matemática: $f(x) = y$.
*   Si $x$ (las features) tiene nulos, valores extremos (outliers) o formatos nuevos, $y$ (la predicción) será basura.
*   **Estrategia:** Valida las features con Great Expectations ANTES de pasarlas al modelo.

## 4. Métricas de Rendimiento del Modelo (Model Performance)
Si tienes el "Ground Truth" (el resultado real que ocurrió después), compáralo con la predicción:
*   **Precisión, Recall, F1-Score.**
*   **RMSE (Root Mean Square Error)** para modelos de regresión.
*   **Importante:** Vigila si estas métricas caen con el tiempo. Es la señal de que necesitas re-entrenar el modelo.

## 5. Explicabilidad y Sesgo (Bias)
Monitoriza si el modelo está tomando decisiones injustas basándose en etiquetas sensibles (ej: género, raza, código postal). La observabilidad en ML también es una cuestión de ética y cumplimiento legal.

## Resumen: Vigilancia Constante
Monitorizar ML es monitorizar una entidad "viva" que se degrada con el tiempo. Necesitas unir métricas de sistemas, calidad de datos y estadística avanzada para asegurar que tu sistema de IA sigue aportando valor real al negocio.
