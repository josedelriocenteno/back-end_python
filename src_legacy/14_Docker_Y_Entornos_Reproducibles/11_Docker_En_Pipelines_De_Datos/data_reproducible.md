# Data Science Reproducible: Notebooks y Entornos

En ciencia de datos, compartir un Jupyter Notebook sin el entorno de Docker es como compartir una receta de cocina sin decir en qué planeta estás cocinando: la gravedad y la presión cambian el resultado.

## 1. Docker como Entorno de Notebook
Evita instalar `jupyter` directamente en tu PC.
- Usa la imagen oficial de `jupyter/datascience-notebook`.
- Monta tu carpeta de trabajo con un Bind Mount.
- **Beneficio:** Cualquiera puede abrir tu notebook y correrlo sin configurar nada.

## 2. Garantía de Resultados (Determinismo)
Al fijar las versiones de NumPy, Pandas y el propio kernel de Python en una imagen de Docker, eliminas las pequeñas variaciones de redondeo o comportamiento que ocurren entre diferentes versiones.

## 3. Entrenamiento en GPU con Docker
Instalar los drivers de NVIDIA y CUDA en local es frustrante.
- **Solución:** Usa **NVIDIA Container Toolkit**. Permite que el contenedor de Docker acceda directamente a la tarjeta gráfica de tu ordenador de forma aislada y controlada.

## 4. El "Snapshot" del Dato
Complementa Docker con herramientas como **DVC (Data Version Control)**.
- Docker versiona el **Código**.
- DVC versiona los **Datos**.
Juntos, te permiten viajar en el tiempo y recrear exactamente cómo se entrenó un modelo hace 6 meses.

## 5. Producción: Del Notebook a la API
Docker facilita el paso de un experimento a un servicio productivo. Simplemente empaqueta tu modelo entrenado (`model.pkl`) dentro de una imagen de FastAPI y ya tienes un microservicio de predicción listo para la nube.

## Resumen: Rigor Científico
La reproducibilidad no es opcional en los datos. Docker elimina la incertidumbre del entorno, permitiendo que tus análisis y modelos sean verificables y estables, bases fundamentales de cualquier infraestructura de datos senior.
