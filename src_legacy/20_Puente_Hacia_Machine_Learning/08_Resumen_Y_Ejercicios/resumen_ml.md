# Resumen y Ejercicios: Puente hacia el Machine Learning

¡Felicidades! Has completado el tema que une la ingeniería con la ciencia de datos. Entender estos conceptos te permitirá ser el puente necesario en cualquier equipo de IA, garantizando que los modelos sean sólidos, escalables y útiles para el negocio.

## 1. Resumen de Conceptos Clave

| Concepto | Definición Rápida | Herramienta Clave |
| :--- | :--- | :--- |
| **Model** | Archivo binario con los patrones aprendidos. | Scikit-Learn, ONNX. |
| **Supervisado** | Aprender con ejemplos etiquetados. | Regresión, Clasificación. |
| **No Supervisado** | Encontrar grupos en datos sin etiquetas. | K-Means, Clustering. |
| **EDA** | Análisis previo para entender los datos. | Pandas, Seaborn. |
| **Features** | Las variables que el modelo lee. | Feature Engineering. |
| **Scaling** | Poner todas las variables en el mismo rango. | StandardScaler. |
| **MLOps** | DevOps para el ciclo de vida de la IA. | MLflow, DVC. |
| **Inferencia** | El acto de predecir con el modelo. | FastAPI, Batch Pipelines. |

## 2. Los Mandamientos del Data Engineer en ML
1.  **Limpiarás los datos antes que nada:** El modelo es tan bueno como los datos que recibe.
2.  **No usarás ML si no hace falta:** El código tradicional es tu primera opción.
3.  **Versionarás todo:** El modelo, el código y los datos deben ir de la mano.
4.  **Monitorearás el Drift:** El mundo cambia, asegúrate de que tu modelo también lo haga.

---

## 3. Ejercicios Prácticos

### Ejercicio 1: El Dilema del Algoritmo
**Escenario:** Tienes una base de datos de usuarios de un e-commerce y quieres hacer dos tareas:
1. Predecir cuánto dinero se gastará un usuario el mes que viene.
2. Agrupar a los usuarios en "Tipos de Compradores" para el equipo de marketing.
*   **Tarea:** Identifica qué tipo de aprendizaje (Supervisado/No supervisado) y qué tipo de problema (Clasificación/Regresión/Clustering) es cada uno de los dos puntos.

### Ejercicio 2: El Detective de Features
**Escenario:** Quieres predecir si un cliente cancelará su suscripción de internet. Tienes estas columnas en tu DB: `ID_Cliente`, `Nombre`, `Fecha_Alta`, `GB_Consumidos_Mes`, `Ciudad`, `Factura_Media_Mensual`.
*   **Tarea:** ¿Qué columnas usarías como **Features** y cuáles descartarías por no aportar información? ¿Cómo transformarías `Fecha_Alta` en algo útil para el modelo?

### Ejercicio 3: La API de la IA
**Escenario:** Tienes un archivo `modelo.pkl` que predice el riesgo de lluvia.
*   **Tarea:** Escribe un pequeño esquema de una API con FastAPI que reciba `temperatura` y `humedad` y devuelva la predicción. (Usa el ejemplo visto en el tema 07 como referencia).

### Ejercicio 4: MLOps en Acción
**Escenario:** Has desplegado un modelo que prefiere canciones para usuarios de una App. Tras 3 meses funcionando, notas que los usuarios cada vez pinchan menos en las sugerencias del modelo.
*   **Tarea:** ¿Cómo se llama este fenómeno? ¿Qué pasos seguirías en tu pipeline de MLOps para solucionar el problema?

---

## 4. Conclusión Final
Como ingeniero, tu valor en el mundo del Machine Learning no es saber derivar una función de pérdida, sino saber **orquestar, versionar y desplegar** la inteligencia de forma que sea fiable. Has construido el puente; ahora es el momento de cruzarlo y empezar a crear sistemas inteligentes.
