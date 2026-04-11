# Errores Comunes en ML: El catálogo de fallos

A diferencia del software tradicional, donde un error suele ser un "Crash", en ML los errores suelen ser "Silenciosos" y "Estadísticos". Estos son los más comunes.

## 1. Training-Serving Skew (Sesgo de Entrenamiento-Producción)
*   **El problema:** El código que limpia los datos para entrenar el modelo es diferente al código que limpia los datos en la API de producción.
*   **Consecuencia:** El modelo recibe datos con un formato sutilmente diferente (ej: unidades en metros vs pies) y predice mal sin dar error.
*   **Solución:** Usa la misma librería de transformación (ej: un archivo `.py` compartido o Feature Stores) en ambos sitios.

## 2. Model Stale (Modelo Caducado)
*   **El problema:** El modelo se entrenó con datos de hace un año y el mundo ha cambiado (ej: inflación, nuevas leyes).
*   **Consecuencia:** El accuracy cae poco a poco cada mes.
*   **Solución:** Implementa alertas de degradación de performance y pipelines de re-entrenamiento automático.

## 3. Data Leakage en Producción (Fuga de datos)
*   **El problema:** Durante la inferencia, el modelo recibe por error una variable que contiene la respuesta que intenta predecir.
*   **Consecuencia:** El modelo parece "Dios" (100% acierto) pero en realidad es un fallo de diseño que engaña al negocio.

## 4. Falta de Feedback Loop
*   **El problema:** Guardas las predicciones pero nadie guarda lo que pasó después en la realidad.
*   **Consecuencia:** Tienes un modelo en producción y no tienes ni idea de si está acertando o fallando. Estás volando a ciegas.

## 5. Ignorar los Outliers (Valores atípicos)
*   **El problema:** Llega un dato con un valor imposible (ej: precio de un café = 1.000.000€).
*   **Consecuencia:** El modelo de ML "explota" matemáticamente y devuelve un valor absurdo (`NaN` o Infinito).
*   **Solución:** Clipping y validación de rangos antes de la inferencia.

## Resumen: Cuidado con la confianza ciega
En ML, "no hay errores en el log" no significa que "todo vaya bien". Debes ser un escéptico constante y monitorizar no solo el sistema, sino la coherencia estadística y de negocio de tus predicciones.
