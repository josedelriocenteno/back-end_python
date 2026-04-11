# Sobreajuste (Overfitting) y el Dilema del Sesgo-Varianza

Un modelo de ML debe ser capaz de **generalizar**. Es decir, debe funcionar bien con datos nuevos que nunca ha visto, no solo con los datos con los que estudió.

## 1. Underfitting (Subajuste)
El modelo es "demasiado simple" para entender el patrón.
*   **Síntoma:** Falla mucho tanto en los datos de entrenamiento como en los de test.
*   **Analogía:** Un estudiante que no ha estudiado nada para el examen.
*   **Causa:** Modelo poco potente o falta de atributos (features).

## 2. Overfitting (Sobreajuste)
El modelo es "demasiado complejo" y ha memorizado el ruido de los datos de entrenamiento.
*   **Síntoma:** Acierta al 100% en el entrenamiento pero falla estrepitosamente en el test. No sabe generalizar.
*   **Analogía:** Un estudiante que se aprende el examen de memoria pero no entiende la lógica; si cambias una coma, suspende.
*   **Causa:** Modelo demasiado potente para pocos datos, o entrenamiento durante demasiado tiempo.

## 3. El Dilema Sesgo (Bias) vs. Varianza (Variance)
Es el equilibrio que todo Data Scientist busca:
*   **Bias (Sesgo):** Error debido a suposiciones erróneas (causa Underfitting). El modelo no "ve" la realidad.
*   **Varianza:** Error debido a una excesiva sensibilidad a pequeñas variaciones (causa Overfitting). El modelo ve "fantasmas" donde solo hay ruido.

## 4. ¿Cómo combatir el Overfitting?
1.  **Más Datos:** La mejor medicina. Cuantos más ejemplos vea, más difícil será que memorice uno concreto.
2.  **Regularización (L1/L2):** Penalizar al modelo si se vuelve demasiado complejo matemáticamente.
3.  **Cross-Validation (Validación Cruzada):** Mezclar y rotar los datos de entrenamiento y test varias veces para asegurar que el resultado es sólido.
4.  **Simplificación:** Reducir el número de atributos o usar un algoritmo menos complejo.

## 5. La técnica del Early Stopping
En redes neuronales, vigilamos el error en el set de test mientras entrenamos. En el momento en que el error de test empieza a subir (aunque el de entrenamiento siga bajando), **detenemos el proceso**. Ahí es donde el modelo ha dejado de aprender y ha empezado a memorizar.

## Resumen: El punto de equilibrio
El éxito en ML no es tener un 0% de error en el laboratorio, es encontrar el equilibrio donde el modelo entiende la esencia del problema sin distraerse con el ruido. Un modelo que generaliza bien es el único que aporta valor real cuando se despliega en producción.
