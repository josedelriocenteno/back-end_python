# El Pipeline de RAG: De documento a respuesta

Para un ingeniero de datos, implementar RAG significa construir una tubería (pipeline) robusta que procese la información para que sea consumible por la IA.

## 1. Fase de Ingesta (Ingestion)

### A. Carga de Documentos
Extraer texto de PDFs, Markdown, HTML o bases de datos SQL.
### B. Chunking (Troceado)
Dividir documentos largos en trozos pequeños. 
*   **Estrategia:** Solapamiento (Overlap). Dejar un poco del final del chunk anterior al principio del siguiente para no perder el contexto de las frases cortadas.
### C. Embedding y Almacenamiento
Convertir cada trozo en un vector y guardarlo en la Vector DB junto con el texto original y sus metadatos (autor, fecha, URL).

## 2. Fase de Consulta (Retrieval)

1.  **Pregunta del usuario:** "¿Cómo pido vacaciones en RRHH?"
2.  **Query Embedding:** Convertimos la pregunta en un vector usando el mismo modelo que en la ingesta.
3.  **Vector Search:** Buscamos los $K$ vectores más similares en la base de datos (Top-K).

## 3. Fase de Generación (Generation)

### Re-ranking (Opcional pero recomendado)
A veces la búsqueda vectorial trae resultados "parecidos" pero no "útiles". Un modelo más pequeño y rápido (Re-ranker) vuelve a ordenar esos 10 resultados para asegurar que los mejores estén arriba.

### Construcción del Prompt
```text
System: Eres un asistente virtual de RRHH. Responde basándote solo en el contexto.
Contexto: {contexto_recuperado}
Usuario: {pregunta}
```

## 4. Retos Técnicos del Pipeline
*   **Calidad del Chunking:** Si los trozos son demasiado pequeños, falta contexto. Si son muy grandes, entra ruido y gastas muchos tokens.
*   **Actualización de Datos:** Si el documento original cambia, debes actualizar el vector en la base de datos.
*   **Evaluación del RAG:** No es fácil saber si el RAG funciona bien. Usamos frameworks como **RAGAS** para medir la fidelidad de la respuesta al contexto.

## 5. El componente "Caché Semántica"
Para ahorrar dinero, podemos guardar preguntas frecuentes y sus respuestas en una caché. Si llega una pregunta "semánticamente similar" a una ya respondida, devolvemos la respuesta de la caché sin llamar al LLM.

## Resumen: Ingeniería de Contexto
Implementar RAG es un reto de ingeniería de datos tradicional aplicado a un nuevo motor de salida. Un pipeline bien diseñado garantiza que la IA siempre tenga la información correcta en el momento justo, eliminando las alucinaciones y maximizando el valor de los datos privados de la empresa.
