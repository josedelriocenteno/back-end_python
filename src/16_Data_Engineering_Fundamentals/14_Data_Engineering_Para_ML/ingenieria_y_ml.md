# Data Engineering vs. Machine Learning: El puente

Mucha gente confunde el rol del Data Scientist con el del Data Engineer. Aunque trabajan juntos, sus misiones son diferentes pero complementarias.

## 1. La Pirámide de Necesidades
Antes de poder hacer Machine Learning (la punta de la pirámide), necesitas:
1. **Recolección:** Ingesta de datos.
2. **Almacenamiento:** Data Lake/Warehouse.
3. **Limpieza:** Transformaciones.
4. **Agregación:** Métricas y Features.
*Sin el trabajo del Data Engineer, el Data Scientist pasa el 80% de su tiempo limpiando CSVs en lugar de crear modelos.*

## 2. Definición de Features
Una **Feature** es una variable de entrada para un modelo de ML.
- **Dato Crudo:** El precio de un producto.
- **Feature:** "Media de precio del producto en los últimos 30 días comparado con la competencia".
- El Data Engineer es el responsable de crear estas Features de forma escalable y robusta.

## 3. Entrenamiento vs. Inferencia
- **Entrenamiento (Training):** El modelo aprende de datos pasados (Batch).
- **Inferencia (Serving):** El modelo predice en tiempo real sobre datos nuevos (Streaming).
- El Data Engineer debe asegurar que los datos que se usaron para entrenar sean **exactamente iguales** en formato y lógica a los que se usan para predecir (evitando el `Training-Serving Skew`).

## 4. El Ciclo de Vida del Dato en ML
1. **Ingesta:** Traer el histórico.
2. **Feature Engineering:** Crear las variables.
3. **Labeling:** Identificar qué queremos predecir (Ventas, Fraude).
4. **Output Storage:** Guardar las predicciones del modelo para que la App las use.

## 5. El rol del MLOps
Es la intersección entre Data Engineering y ML. Se encarga de automatizar el despliegue de modelos, monitorizar si el modelo está perdiendo precisión y gestionar el re-entrenamiento automático.

## Resumen: Base Sólida
El Machine Learning es el motor de un coche de carreras; la Ingeniería de Datos es el chasis, el combustible y la carretera. Sin una infraestructura de datos de calidad, los modelos de IA son frágiles e impredecibles.
