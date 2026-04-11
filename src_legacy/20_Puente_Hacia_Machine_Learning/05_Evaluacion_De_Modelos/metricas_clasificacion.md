# Métricas de Clasificación: ¿Cómo sabemos si el modelo acierta?

En problemas de clasificación (ej: ¿Es Spam?), no basta con decir "el modelo es bueno". Necesitamos números que cuantifiquen su calidad según el tipo de error que cometa.

## 1. La Matriz de Confusión
Es la herramienta base para entender los aciertos y errores.
*   **Verdaderos Positivos (VP):** El email era Spam y el modelo dijo Spam (Acierto).
*   **Verdaderos Negativos (VN):** El email era Bueno y el modelo dijo Bueno (Acierto).
*   **Falsos Positivos (FP):** El email era Bueno y el modelo dijo Spam (**Error Grave: Alerta falsa**).
*   **Falsos Negativos (FN):** El email era Spam y el modelo dijo Bueno (**Error: Se le escapó el spam**).

## 2. Métricas Principales

### A. Accuracy (Exactitud)
$\text{Exactitud} = \frac{\text{Aciertos Totales}}{\text{Total de Casos}}$
*   **Cuándo usar:** Cuando tus datos están equilibrados (ej: 50% spam, 50% bueno).
*   **Peligro:** Si el 99% de tus emails son buenos, un modelo que diga "Siempre es Bueno" tendría un 99% de Accuracy pero sería un modelo inútil.

### B. Precision (Precisión)
$\text{Precisión} = \frac{VP}{VP + FP}$
*   **Pregunta:** De todos los que dije que eran Spam, ¿cuántos lo eran de verdad?
*   **Objetivo:** Minimizar los Falsos Positivos. Es clave en sistemas de Diagnóstico Médico (no quieres decir que alguien está enfermo si no lo está).

### C. Recall (Sensibilidad / Recuperación)
$\text{Recall} = \frac{VP}{VP + FN}$
*   **Pregunta:** De todos los Spam que existen, ¿cuántos fui capaz de detectar?
*   **Objetivo:** Minimizar los Falsos Negativos. Es clave en sistemas de Detección de Incendios (no quieres que se te escape un fuego).

### D. F1-Score
Es el equilibrio (media armónica) entre Precision y Recall.
*   **Uso:** Cuando quieres un modelo que sea bueno en ambas métricas a la vez.

## 3. Curva ROC y AUC
Miden la capacidad del modelo para separar las dos clases a diferentes niveles de umbral.
*   **AUC = 1.0:** Modelo perfecto.
*   **AUC = 0.5:** El modelo predice al azar (como tirar una moneda).

## Resumen: Elige tu arma
No hay una métrica "mejor" que otra; depende del coste del error. Si eres un banco detectando fraude, prefieres un Recall alto (bloquear todo el fraude aunque molestes a algún cliente). Si eres una red social filtrando contenido ofensivo, prefieres Precision (no borrar contenido inofensivo por error).
