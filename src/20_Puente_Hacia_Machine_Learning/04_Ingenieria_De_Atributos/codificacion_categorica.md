# Codificación Categórica: De Texto a Números

Como la mayoría de los algoritmos de ML solo entienden números, debemos transformar las categorías de texto (ej: "Rojo", "Azul") en representaciones numéricas coherentes.

## 1. Label Encoding (Codificación por etiquetas)
Asigna un número único a cada categoría.
*   **Ejemplo:** Rojo -> 0, Azul -> 1, Verde -> 2.
*   **Cuándo usar:** Solo para variables **ordinales** (donde el orden importa).
*   **Peligro:** El modelo puede pensar que Verde (2) es "mejor" o "superior" a Rojo (0) solo porque el número es mayor.

## 2. One-Hot Encoding (OHE)
Crea una columna nueva por cada categoría, con valores 0 o 1.
*   **Ejemplo:**
    | Color | Rojo | Azul | Verde |
    | :--- | :---: | :---: | :---: |
    | Rojo | 1 | 0 | 0 |
    | Verde | 0 | 0 | 1 |
*   **Cuándo usar:** Para variables **nominales** sin orden (Ciudad, Color). 
*   **Peligro:** Si tienes 1.000 ciudades, crearás 1.000 columnas nuevas (**La maldición de la dimensionalidad**), lo que puede ralentizar mucho el entrenamiento.

## 3. Binning (Agrupamiento en cubos)
Agrupa valores en categorías más amplias.
*   **Ejemplo:** En lugar de 20 tipos de café, agrupas en "Café Solo", "Café con Leche" e "Otros".
*   **Objetivo:** Reducir la complejidad y el ruido de categorías muy poco frecuentes.

## 4. Target Encoding
Sustituye la categoría por la media de lo que queremos predecir.
*   **Ejemplo:** En la categoría "Madrid", calculas el precio medio del alquiler en Madrid y usas ese número.
*   **Peligro:** Riesgo alto de **Leakage** (el modelo conoce la respuesta antes de predecirla), por lo que debe hacerse con mucho cuidado.

## Resumen: Traduciendo el mundo
Elegir la técnica de codificación adecuada es vital: One-Hot para evitar jerarquías inexistentes y Label Encoding cuando el orden es parte de la información. Una mala traducción del texto a números puede confundir al modelo y degradar su precisión de forma invisible.
