# ¿Cómo funciona un LLM? (Explicación para Ingenieros)

A menudo los LLMs parecen mágicos, pero bajo el capó son sistemas matemáticos que realizan una tarea muy específica: **Predecir la siguiente palabra**.

## 1. El concepto de Autoregresión
Un LLM es un modelo autoregresivo. Si le das la frase "El gato está sobre la...", el modelo calcula las probabilidades de todas las palabras que conoce para esa posición:
*   "mesa": 85%
*   "cama": 10%
*   "luna": 0.01%
El modelo elige una (basándose en un parámetro llamado **Temperatura**) y repite el proceso incluyendo esa palabra nueva, hasta que decide terminar la frase.

## 2. Tokens: La unidad mínima de medida
Los LLMs no leen palabras, leen **Tokens**.
*   Un token puede ser una palabra entera ("perro"), una parte de una palabra ("-ando") o incluso un solo carácter.
*   **Regla aproximada:** 1.000 tokens son unas 750 palabras.
*   **Context Window (Ventana de Contexto):** Es la cantidad máxima de tokens que el modelo puede "recordar" a la vez. Si tu prompt + la respuesta superan este límite, el modelo empezará a olvidar el principio de la conversación.

## 3. Embeddings: El Mapa Semántico
Para procesar las palabras matemáticamente, el modelo las convierte en **Embeddings** (vectores numéricos de miles de dimensiones).
*   En este espacio matemático, palabras con significados similares (ej: "rey" y "reina") están físicamente cerca una de otra. Esto es lo que permite al modelo entender el "significado" y no solo la ortografía.

## 4. El Entrenamiento: Pre-training vs. RLHF
Los modelos pasan por dos fases:
1.  **Pre-training:** Leen todo internet para aprender gramática y conocimientos generales. Se convierten en "completadores de texto" muy potentes.
2.  **RLHF (Reinforcement Learning from Human Feedback):** Humanos evalúan las respuestas para enseñar al modelo a ser útil, educado y a seguir instrucciones, en lugar de simplemente completar frases al azar.

## 5. Alucinaciones: El Efecto Secundario
Como el modelo es una "calculadora de probabilidades", a veces predice una palabra que suena muy convincente pero que es falsa. Esto es una **Alucinación**. Ocurre porque el modelo no tiene una base de datos de hechos real, sino un mapa de relaciones estadísticas.

## Resumen: Probabilidad con Esteroides
Entender que un LLM es un sistema de predicción probabilística de tokens es vital para un ingeniero. Esto nos ayuda a diseñar mejores prompts, a validar las salidas y a entender por qué a veces fallan de forma tan creativa.
