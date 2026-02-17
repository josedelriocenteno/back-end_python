# Serving y Predicciones: Cerrando el círculo

Una vez que el modelo de ML está entrenado, hay que ponerlo a trabajar. El Data Engineer facilita el flujo de datos hacia el modelo y el almacenamiento de sus resultados.

## 1. Batch Scoring (Predicciones Masivas)
El modelo se ejecuta una vez al día sobre todos los usuarios.
- **Proceso:** Airflow despierta una tarea de Spark -> El modelo lee de S3 -> Escribe predicciones en BigQuery.
- **Ejemplo:** "Calcular la probabilidad de compra para los 10 millones de usuarios de mi web para enviarles un email mañana".

## 2. Online Inference (Predicciones en tiempo real)
El modelo responde a una petición inmediata.
- **Proceso:** La App envía un JSON a una API -> La API consulta el Feature Store (Redis) -> El modelo predice -> Devuelve el resultado.
- **Ejemplo:** "Detectar si esta transacción de tarjeta de crédito es fraude en los próximos 200 milisegundos".

## 3. Almacenamiento de Predicciones (Inference Store)
Siempre guarda lo que el modelo ha predicho.
- **Por qué:** Para poder comparar más tarde si el modelo acertó o falló. Es la base para el aprendizaje continuo.

## 4. Monitorización de modelos (Drift)
Los datos del mundo real cambian. Si entrenaste un modelo de recomendación de ropa de invierno y llega el verano, el modelo fallará.
- **Data Drift:** Cambian los datos que recibe el modelo.
- **Concept Drift:** Cambia la relación entre los datos y lo que queremos predecir.
- El Data Engineer debe alertar si la distribución de los datos de entrada ha cambiado drásticamente.

## 5. El Data Engineer como habilitador
Tu éxito no es que el modelo sea preciso, eso es tarea del Data Scientist. Tu éxito es que el modelo reciba datos frescos, no se caiga nunca y que sus predicciones lleguen al lugar donde el negocio pueda usarlas.

## Resumen: Impacto Real
Llevar un modelo a producción es la fase más difícil del Machine Learning. La Ingeniería de Datos proporciona la infraestructura necesaria para que la inteligencia artificial deje de ser magia y se convierta en una herramienta operativa del día a día.
