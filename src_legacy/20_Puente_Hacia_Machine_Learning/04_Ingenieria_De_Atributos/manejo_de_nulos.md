# Manejo de Nulos: Curando las heridas del dato

Los valores faltantes (`NaN`, `None`, `null`) son el enemigo número uno de los algoritmos de Scikit-Learn. Si intentas entrenar un modelo con nulos, el código lanzará un error. Tienes tres formas de arreglarlo.

## 1. Eliminación (Drop)
Simplemente borras la fila o la columna que contiene el nulo.
*   **Pros:** Rápido y limpio. No inventas datos.
*   **Contras:** Si tienes muchos nulos, puedes acabar borrando el 50% de tu dataset, perdiendo información valiosa.
*   **Uso:** Solo si tienes muchísimos datos y muy pocos nulos.

## 2. Imputación (Impute)
Rellenas el hueco con un valor calculado.
*   **Numéricos:** Rellenar con la **Media** (promedio) o la **Mediana** (más robusta a valores extremos).
*   **Categóricos:** Rellenar con la **Moda** (el valor más frecuente).
*   **Constante:** Rellenar con un valor fijo como `0` o `"Desconocido"`.

## 3. Imputación Avanzada
Usar inteligencia para rellenar los huecos.
*   **K-Nearest Neighbors (KNN Imputer):** Busca las filas más parecidas a la que tiene el nulo y mira qué valor tienen ellas.
*   **Modelado:** Usar otro modelo de ML secundario para predecir cuál debería ser el valor faltante.

## 4. Crear una Feature de Aviso (Indicator)
A veces, el hecho de que un dato falte es una información en sí misma.
*   Creas una columna nueva llamada `edad_es_nulo` (1 si era nulo, 0 si no). Luego rellenas la edad con la media.
*   El modelo ahora puede "saber" que ese dato ha sido inventado y decidir si se fía de él o no.

## 5. ¿Cuál elegir?
1. Si falta más del 60% de los datos de una columna -> **Borra la columna**.
2. Si falta el 5% y tienes muchos registros -> **Borra las filas**.
3. En el resto de casos -> **Imputa con Mediana (Números) o Moda (Texto)**.

## Resumen: Integridad ante todo
Manejar nulos es un ejercicio de equilibrio. Inventar demasiados datos puede sesgar el modelo; borrar demasiados puede dejarlo ciego. Como Data Engineer, tu objetivo es mantener la máxima cantidad de información posible garantizando que el algoritmo pueda ser entrenado sin errores técnicos.
