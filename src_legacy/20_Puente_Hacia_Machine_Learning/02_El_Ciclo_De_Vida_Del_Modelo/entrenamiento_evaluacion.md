# Entrenamiento y Evaluación del Modelo

Una vez los datos están listos, pasamos a la fase "matemática" donde el algoritmo se convierte en un modelo útil.

## 1. División de los Datos (Train/Test Split)
Nunca entrenamos con todos los datos. Siempre los dividimos:
*   **Training Set (70-80%):** Datos para que el modelo aprenda.
*   **Testing Set (20-30%):** Datos que el modelo nunca ve durante el entrenamiento. Se usan para "examinarle" al final.
*   **Validación Set:** A veces se usa una tercera división para ajustar los parámetros (Hyperparameters).

## 2. El proceso de Entrenamiento
El algoritmo toma los datos de entrenamiento y empieza a ajustar sus parámetros internos para minimizar el error. Es un proceso iterativo que puede durar milisegundos o semanas, dependiendo de la complejidad.

## 3. Evaluación: ¿Cómo de bien lo hace?
Usamos los datos de **Test** para calcular métricas:
*   **Accuracy (Exactitud):** % de aciertos totales. (Cuidado: puede ser engañoso si los datos están descompensados).
*   **Error Medio Cuadrático (MSE):** Para problemas de números (regresión). Cuanto menor, mejor.
*   **Matriz de Confusión:** Nos dice dónde se equivoca: ¿Dice "Spam" cuando es un email "Bueno"? o viceversa.

## 4. Hyperparameter Tuning
Son las "perillas" del algoritmo (ej: cuántas ramas tiene un árbol de decisión).
*   Cambiamos estas perillas y volvemos a entrenar hasta encontrar la combinación que dé el menor error en el set de validación.

## 5. Guardado del Modelo (Serialization)
Cuando estamos contentos con el modelo, lo guardamos en un archivo binario.
*   **Formatos comunes:** `.pkl` (Pickle), `.h5` (HDF5), o el estándar moderno **ONNX**.
*   Este archivo es lo que el Data Engineer desplegará en producción.

## Resumen: La prueba de fuego
El entrenamiento es el aprendizaje y la evaluación es el examen. Dividir siempre los datos es la regla de oro del ML: si examinas a un alumno con las mismas preguntas que ha estudiado, solo estarás midiendo su memoria, no su capacidad de aprender y generalizar.
