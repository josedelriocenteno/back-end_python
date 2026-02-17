# Recolección y Preparación de Datos

"Garbage In, Garbage Out". Si alimentas a tu modelo con basura, predecirá basura. Por eso, esta etapa de ingeniería es la más crítica de todo el proceso.

## 1. Recolección (Data Sourcing)
Debemos identificar todas las fuentes de información:
*   **Internas:** Bases de datos SQL (ventas, usuarios), logs de servidores.
*   **Externas:** APIs de clima, datos demográficos, redes sociales.
*   **Estrategia:** Unimos todo en un **Data Warehouse** o **Data Lake** para tener una fuente única de verdad para el entrenamiento.

## 2. Preparación (Data Cleaning)
Los datos del mundo real son "sucios". Debemos realizar tareas de:
*   **Manejo de Nulos:** ¿Borramos la fila con datos faltantes o rellenamos con la media/mediana?
*   **Deduplicación:** Eliminar registros repetidos que pueden sesgar al modelo.
*   **Outliers (Valores atípicos):** Identificar datos erróneos (ej: un usuario de 200 años de edad) que pueden confundir al algoritmo.

## 3. Formateo y Tipado
El ML necesita números.
*   Asegurarse de que las fechas estén en el formato correcto.
*   Convertir booleanos (True/False) en números (1/0).
*   Garantizar que todos los datos de una columna tengan el mismo tipo.

## 4. Análisis Exploratorio (EDA)
Antes de entrenar, miramos los datos:
*   **Distribución:** ¿Hay muchos más hombres que mujeres en los datos? Esto puede causar un modelo sesgado.
*   **Correlación:** ¿Qué variables parecen estar relacionadas con lo que queremos predecir?

## 5. El impacto en el Performance
Como vimos en temas anteriores, usar formatos como **Parquet** en esta fase acelera enormemente la lectura de datos durante el entrenamiento, reduciendo el tiempo de experimentación del Data Scientist.

## Resumen: La base del edificio
La recolección y preparación es el trabajo "sucio" pero esencial. Un buen Data Engineer entrega un conjunto de datos limpio, coherente y fácil de leer, permitiendo que el resto del equipo se centre en la inteligencia del modelo en lugar de en arreglar errores de formato.
