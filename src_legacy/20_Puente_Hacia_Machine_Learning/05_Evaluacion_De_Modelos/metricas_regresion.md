# Métricas de Regresión: Midiendo la distancia al error

En problemas donde predecimos un número continuo (ej: el precio de una casa), no podemos decir "acertó o falló", porque es casi imposible que el modelo prediga el valor exacto al céntimo. Medimos **qué tan cerca** se quedó del valor real.

## 1. El concepto de "Residuo"
El residuo es la diferencia entre el valor real ($y$) y la predicción del modelo ($\hat{y}$).
*   $\text{Residuo} = y - \hat{y}$

## 2. Métricas Principales

### A. Error Medio Absoluto (MAE)
Es la media de la suma de los errores sin signo.
*   **Interpretación:** "En promedio, el modelo se equivoca por 1.500€".
*   **Ventaja:** Muy fácil de explicar al negocio. No penaliza demasiado los errores grandes (outliers).

### B. Error Medio Cuadrático (MSE)
Eleva los errores al cuadrado antes de hacer la media.
*   **Efecto:** Al elevar al cuadrado, los errores grandes pesan muchísimo más que los pequeños.
*   **Uso:** Cuando un error grande es inaceptable para el negocio.

### C. Raíz del Error Medio Cuadrático (RMSE)
Es la raíz cuadrada del MSE.
*   **Ventaja:** Devuelve el error a las unidades originales (ej: €, metros, litros). Es la métrica estándar en la industria para regresión.

### D. Coeficiente de Determinación ($R^2$)
Nos dice qué porcentaje de la variación de los datos es capaz de explicar el modelo.
*   **Escala:** Va de 0 a 1.
*   **$R^2 = 0.9$:** El modelo explica el 90% de la variabilidad (Muy bueno).
*   **$R^2 = 0.1$:** El modelo no es mucho mejor que predecir siempre la media de los datos (Malo).

## 3. ¿Cuándo usar cada una?
*   Si tienes datos con muchos errores de lectura o ruidos extremos -> **MAE**.
*   Si los errores grandes son catastróficos para tu empresa -> **MSE/RMSE**.
*   Si quieres saber la calidad general del ajuste comparado con la media -> **$R^2$**.

## Resumen: La búsqueda de la precisión
En regresión, el performance es un juego de distancias. El objetivo es minimizar la suma de los residuos. Un buen Data Engineer monitoriza estas métricas en producción para detectar si la precisión del modelo se degrada conforme cambian las condiciones del mercado o del sistema.
