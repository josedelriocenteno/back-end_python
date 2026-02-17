# Técnicas de Prompting para Desarrolladores

El **Prompt Engineering** no es solo "hablar con la IA". Para un ingeniero, es el proceso de diseñar entradas que maximicen la fiabilidad, reduzcan las alucinaciones y garanticen que la respuesta sea útil para el software que la va a recibir.

## 1. Zero-shot Prompting
Dar una instrucción directa sin ejemplos.
*   **Prompt:** "Resume este texto en 3 puntos clave: [texto]"
*   **Uso:** Tareas sencillas y directas que el modelo conoce bien.

## 2. Few-shot Prompting
Darle al modelo unos pocos ejemplos de lo que queremos antes de pedirle la tarea real.
*   **Prompt:** 
    "Entrada: El producto es caro -> Sentimiento: Negativo
     Entrada: Me encanta la rapidez -> Sentimiento: Positivo
     Entrada: El diseño es normal -> Sentimiento: "
*   **Ventaja:** Ayuda enormemente al modelo a entender el formato y el tono que esperamos, especialmente en tareas complejas.

## 3. Chain-of-Thought (Cadena de Pensamiento)
Pedirle al modelo que explique su razonamiento paso a paso antes de dar la respuesta final.
*   **Prompt:** "Resuelve este problema matemático. Piensa paso a paso y explica cada etapa antes de dar el resultado final."
*   **Por qué funciona:** Obliga al modelo a usar más tokens para "pensar", lo que reduce drásticamente los errores lógicos y matemáticos.

## 4. System Prompt (Instrucciones de Sistema)
En las APIs de IA, dividimos el mensaje en roles. El `System Prompt` define la personalidad y las reglas del modelo.
*   **Ejemplo:** "Eres un analista de seguridad experto. Tu tarea es encontrar vulnerabilidades en código Python. Responde siempre de forma técnica y no des consejos generales de programación."
*   **Impacto:** El modelo se mantiene mucho más enfocado y es más difícil de "engañar" por el usuario final (Prompt Injection).

## 5. Delimitadores: Estructurando el Caos
Usa delimitadores claros para que el modelo sepa qué es la instrucción y qué es el dato.
*   **Prompt:** 
    "Resume el texto delimitado por triples comillas:
     \"\"\"
     [aquí va el texto gigante]
     \"\"\" "
*   **Ventaja:** Evita que el modelo se confunda si el texto de entrada contiene instrucciones que parecen órdenes.

## Resumen: Diseñar para la Precisión
Como ingeniero, dejas de ser un "escritor" para ser un "diseñador de contexto". Aplicar estas técnicas sistemáticamente convierte a la IA en un componente predecible y potente dentro de tu arquitectura de software, capaz de realizar tareas complejas con una tasa de error mínima.
