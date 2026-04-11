# ¿Qué son los Embeddings? (Frases como Vectores)

Un **Embedding** es una representación numérica (un vector de números flotantes) de un trozo de texto (una palabra, una frase o un párrafo) que captura su **significado semántico**.

## 1. De la palabra a la matemática
Si tenemos tres palabras: "perro", "cachorro" y "refrigerador".
*   En una búsqueda tradicional (por palabras), "perro" y "cachorro" son totalmente diferentes.
*   En el mundo de los **Embeddings**, el vector de "perro" y el de "cachorro" estarán numéricamente muy cerca, mientras que el de "refrigerador" estará muy lejos de ambos.

## 2. El espacio de alta dimensionalidad
Un modelo de embeddings (como `text-embedding-3-small` de OpenAI) convierte un texto en un vector de, por ejemplo, 1536 dimensiones.
*   Cada dimensión representa una "característica" abstracta que el modelo ha aprendido (ej: tono emocional, temática animal, tiempo verbal).
*   **Magia:** Podemos hacer matemáticas con el lenguaje. `Actor + Mujer ≈ Actriz`.

## 3. Similitud del Coseno (Cosine Similarity)
Para saber qué tan parecidos son dos textos, calculamos el ángulo entre sus dos vectores.
*   **Ángulo 0 (Coseno 1):** Significados idénticos.
*   **Ángulo 90 (Coseno 0):** No tienen nada que ver.
*   Esto permite al backend realizar **Búsquedas Semánticas**: buscar por significado en lugar de buscar por palabras clave exactas.

## 4. El Proceso de Generación
1.  **Texto:** "Cómo configurar un servidor en Python".
2.  **Llamada a API de Embeddings:** Envías el texto.
3.  **Resultado:** `[0.12, -0.045, 0.88, ... 1533 números más]`.
Este vector es lo que guardaremos en nuestra base de datos.

## 5. Casos de Uso
*   **Buscadores Inteligentes:** Buscar "recetas de postres" y que aparezca "tarta de manzana" aunque no diga la palabra "postre".
*   **Recomendadores:** Encontrar productos similares a los que el usuario ya ha comprado.
*   **Detección de Anomalías:** Ver si un log de error es "muy diferente" a los logs habituales.

## Resumen: El ADN Semántico
Los Embeddings son la forma en que los ordenadores "entienden" el concepto detrás de las palabras. Son la herramienta fundamental para conectar bases de datos tradicionales con la inteligencia de los LLMs, permitiendo búsquedas contextuales que antes eran ciencia ficción.
