# Logs de Inferencia: El rastro de la decisión

En un pipeline de IA, cada predicción debe dejar una huella auditable. Esto es lo que llamamos **Logging de Inferencia**.

## 1. ¿Qué debemos loguear en cada predicción?
Para poder depurar un error de IA en el futuro, necesitas guardar:
1.  **Request ID / Trace ID:** Para unirlo con el resto de la App.
2.  **Input Features:** Los datos exactos que recibió el modelo (sin procesar y procesados).
3.  **Model Version:** ¿Qué versión exacta del modelo respondió? (ej: `v2.1.4`).
4.  **Prediction Output:** El resultado y el score de confianza.
5.  **Execution Metadata:** Tiempo de CPU, memoria usada, ID del servidor.

## 2. Formato: Logs Estructurados (JSON)
Igual que vimos en el sub-tema 01, la inferencia debe ser JSON. Esto permite buscar rápidamente: "Dime todas las predicciones de la versión v2.1 que tardaron más de 500ms".

## 3. El peligro del PII (Datos Personales)
**MUY IMPORTANTE:** Al loguear las features de entrada, ten cuidado de no guardar nombres, DNI, o tarjetas de crédito.
*   **Estrategia:** Loguea solo IDs anónimos o aplica técnicas de enmascaramiento antes de escribir el log.

## 4. Almacenamiento: Logs Calientes vs Fríos
*   **Calientes (Cloud Logging):** Guarda las últimas 24h para debugging inmediato.
*   **Fríos (BigQuery / GCS):** Guarda el histórico de meses para analizar el Drift y hacer re-entrenamientos.

## 5. Logs de Explicabilidad (Explainability)
Si usas técnicas como SHAP o LIME para saber "por qué" el modelo decidió algo, guarda esas "importancias de las variables" en el log.
- "Se denegó el crédito porque la variable `ahorros_totales` era muy baja".
- Esto es vital para responder a reclamaciones legales de clientes.

## Resumen: La Caja Negra ahora es Transparente
Los logs de inferencia son el diario de tu modelo. Sin ellos, cuando un modelo falle o se comporte de forma extraña, no tendrás ninguna forma de explicar qué pasó, perdiendo la trazabilidad y la capacidad de mejora.
