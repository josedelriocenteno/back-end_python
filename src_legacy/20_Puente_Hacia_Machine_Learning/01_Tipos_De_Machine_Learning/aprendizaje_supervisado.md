# Aprendizaje Supervisado: El método de los ejemplos

Es el tipo de Machine Learning más común y utilizado en la industria. Se llama "Supervisado" porque el algoritmo aprende bajo la supervisión de un conjunto de datos que ya tienen la **respuesta correcta** (etiquetas).

## 1. ¿Cómo funciona?
Le damos al modelo un par de datos: `(Entrada, Etiqueta)`.
*   **Ejemplo:** (Foto de un perro, "Perro"), (Foto de un coche, "Coche").
*   El modelo busca la relación matemática para que, cuando reciba una foto nueva (sin etiqueta), pueda decir con seguridad: "Esto es un Perro".

## 2. Los dos problemas principales

### A. Clasificación (Categorías)
El objetivo es predecir una etiqueta discreta (una categoría).
*   **Pregunta:** "¿Es esto A o B?"
*   **Ejemplos:**
    *   Filtro de Spam (Spam o No Spam).
    *   Diagnóstico médico (Sano o Enfermo).
    *   Reconocimiento de imágenes (Gato, Perro, Pájaro).

### B. Regresión (Valores numéricos)
El objetivo es predecir un número continuo.
*   **Pregunta:** "¿Cuánto valdrá X?"
*   **Ejemplos:**
    *   Precio de una vivienda basado en metros cuadrados.
    *   Temperatura de mañana.
    *   Ventas estimadas para el próximo trimestre.

## 3. Algoritmos Comunes
*   **Regresión Lineal:** Para problemas sencillos de números.
*   **Árboles de Decisión:** Muy intuitivos y potentes.
*   **Random Forest:** Una colección de muchos árboles de decisión.
*   **Redes Neuronales:** Para problemas complejos como visión o lenguaje.

## 4. El peligro: El Overfitting (Sobreajuste)
Ocurre cuando el modelo "memoriza" los ejemplos en lugar de "aprender" la lógica. Es como un estudiante que se sabe las preguntas del examen de memoria pero no entiende el tema; si le cambias una coma en la pregunta, falla.

## Resumen: Aprender con respuestas
El aprendizaje supervisado es como un niño con un profesor: el profesor le da problemas y las soluciones, y con el tiempo el niño aprende a resolver problemas similares por su cuenta. Es la herramienta por excelencia para la predicción y clasificación empresarial.
