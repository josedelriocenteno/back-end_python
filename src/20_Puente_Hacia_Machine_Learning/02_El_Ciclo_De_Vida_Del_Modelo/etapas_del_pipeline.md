# Etapas del Pipeline de Machine Learning

Un modelo de Machine Learning no nace de la nada. Es el resultado de un proceso estructurado que a menudo se dibuja como un ciclo infinito.

## 1. El Ciclo de Vida (ML Life Cycle)
Este proceso suele dividirse en las siguientes fases principales:

### A. Definición del Problema
Antes de tocar el código, hay que saber qué queremos resolver. ¿Es predecir ventas? ¿Es clasificar imágenes de radiografías? ¿Tenemos los datos necesarios para ello?

### B. Ingesta y Preparación (Data Engineering)
Es la fase donde más tiempo se pasa (80%). Recolectar datos de DBs, APIs o CSVs, limpiarlos, quitar duplicados y resolver nulos.

### C. Ingeniería de Atributos (Feature Engineering)
Transformamos los datos limpios en un formato que el modelo entienda mejor (ej: convertir "Lunes" en el número 1, o escalar precios de 0 a 1).

### D. Entrenamiento (Training)
Elegimos un algoritmo y le damos los datos para que aprenda. Aquí es donde se genera el "Modelo" como archivo binario.

### E. Evaluación y Ajuste
Probamos el modelo con datos que nunca ha visto. Si falla mucho, ajustamos los parámetros del algoritmo (Hyperparameters) y volvemos a entrenar.

### F. Despliegue (Deployment)
Llevamos el modelo a producción. Puede ser una API que responde en milisegundos o un proceso batch que se ejecuta cada noche.

### G. Monitoreo y Re-entrenamiento
El mundo cambia. Un modelo que predecía bien en 2023 puede fallar en 2024. Vigilamos su precisión y lo re-entrenamos cuando sea necesario.

## 2. El papel de los diferentes roles
*   **Data Engineer:** Fases A, B, C, F, G (La infraestructura y los datos).
*   **Data Scientist:** Fases A, C, D, E (El modelo y los algoritmos).
*   **MLOps Engineer:** Fases F, G (La automatización y estabilidad en producción).

## Resumen: Un viaje continuo
El ML no es un proyecto corto, es un producto vivo. Entender estas etapas permite organizar mejor el trabajo y asegura que el modelo no solo sea inteligente hoy, sino que siga aportando valor conforme llegan nuevos datos.
