# Despliegue y Monitoreo: La IA en el mundo real

El modelo ya funciona en el laboratorio. Ahora hay que llevarlo a la calle y asegurarnos de que no se vuelva "loco" con el paso del tiempo.

## 1. Estrategias de Despliegue (Deployment)

### A. Inferencia Online (Tiempo Real)
El modelo vive dentro de una API (FastAPI, Flask) o un servidor especializado (TFServing).
*   **Uso:** Una App móvil pide una predicción y el modelo responde en milisegundos.

### B. Inferencia Batch (Lotes)
El modelo se ejecuta una vez al día sobre millones de filas.
*   **Uso:** Calcular el riesgo de fuga de todos los clientes de un banco cada noche para que los comerciales tengan la lista por la mañana.

### C. Inferencia en el Borde (Edge)
El modelo corre directamente en el móvil del usuario o en un sensor de una fábrica.
*   **Ventaja:** Funciona sin internet y es ultra-rápido.

## 2. Monitoreo: Detectando problemas

### A. Model Drift (Desviación del Modelo)
Los patrones del mundo cambian.
*   **Ejemplo:** Un modelo de predicción de moda entrenado en 2019 fallará en 2020 debido a la pandemia. Los datos han cambiado tanto que el modelo ya no es válido.

### B. Latencia y Errores
Vigilamos cuánto tarda el modelo en responder. Los modelos pesados pueden degradar el rendimiento de la App.

## 3. Re-entrenamiento: El ciclo se cierra
Cuando detectamos que la precisión del modelo baja (Drift), lanzamos de nuevo todo el pipeline:
1. Recolectamos datos nuevos.
2. Limpiamos y preparamos.
3. Entrenamos un nuevo modelo.
4. Evaluamos que sea mejor que el actual.
5. Sustituimos el modelo viejo por el nuevo.

## 4. Pruebas A/B
No solemos cambiar un modelo por otro a ciegas.
*   Damos el modelo A al 50% de los usuarios y el modelo B al otro 50%.
*   Medimos cuál se comporta mejor en el mundo real antes de hacer el cambio definitivo.

## Resumen: Responsabilidad Post-Despliegue
Llevar un modelo a producción es solo el principio. Un sistema de ML maduro incluye monitoreo automático y pipelines de re-entrenamiento que garanticen que la inteligencia del sistema evoluciona a la par que los datos y el comportamiento de los usuarios en el mundo real.
