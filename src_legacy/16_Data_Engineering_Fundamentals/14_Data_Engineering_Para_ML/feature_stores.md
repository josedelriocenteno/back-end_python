# Feature Stores: El almacén de variables

Un **Feature Store** es un repositorio centralizado donde se guardan las variables (features) ya calculadas para que puedan ser compartidas por múltiples modelos de Machine Learning.

## 1. El problema que resuelve
- **Duplicidad:** Tres científicos de datos diferentes calculando la misma variable "Ticket Medio" con tres lógicas SQL distintas.
- **Inconsistencia:** El modelo en producción usa una lógica de cálculo diferente a la del modelo de entrenamiento.

## 2. Componentes de un Feature Store
- **Offline Store:** Grandes volúmenes de datos pasados (Parquet/S3) para entrenar modelos.
- **Online Store:** Base de datos ultra rápida (Redis/Cassandra) para que el modelo consulte la feature en milisegundos durante una predicción en vivo.
- **Registry:** Catálogo donde se documenta qué significa cada feature.

## 3. Beneficios
1. **Reutilización:** Puedes usar una feature creada para "Predicción de Abandono" en un modelo de "Recomendación de Productos".
2. **Puesta en producción inmediata:** Una vez que la feature está en el store, el modelo puede consumirla sin necesidad de que el ingeniero reescriba el código de transformación para producción.

## 4. Herramientas Populares
- **Feast:** El Feature Store de código abierto más popular.
- **Tecton:** Versión empresarial y gestionada.
- **Databricks Feature Store:** Integrado totalmente en su plataforma.

## 5. El Data Engineer y el Feature Store
Tu misión es construir los pipelines que alimentan el Feature Store. Debes asegurar que las features se calculen a tiempo, que no haya valores nulos y que la latencia del `Online Store` sea mínima.

## Resumen: Eficiencia en IA
El Feature Store es para el Machine Learning lo que el Data Warehouse es para el Business Intelligence. Es la pieza que permite pasar de "experimentos de IA" a una factoría industrial de modelos de inteligencia artificial.
