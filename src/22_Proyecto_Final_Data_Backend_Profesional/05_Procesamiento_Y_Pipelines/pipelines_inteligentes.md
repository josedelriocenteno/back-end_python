# Procesamiento y Pipelines: La inteligencia en movimiento

En esta etapa del proyecto, el dato bruto se convierte en conocimiento. Aquí es donde aplicas las técnicas de procesamiento masivo y asincronía.

## 1. El Pipeline de Procesamiento
Tu sistema debe manejar la llegada de datos de forma asíncrona para no bloquear la API.
*   **Worker Asíncrono:** Usa `asyncio` o librerías como `TaskIQ` o `Celery` para procesar las noticias en background.
*   **Paralelismo:** Si tienes que procesar 10.000 noticias históricas, usa `multiprocessing` para aprovechar todos los núcleos de tu CPU.

## 2. Enriquecimiento con IA (Stage 1)
Antes de guardar la noticia, el pipeline debe:
1.  **Analizar el Sentimiento:** ¿Es una noticia positiva o negativa para el mercado?
2.  **Extraer Entidades:** ¿De qué empresa habla? (Google, Apple, Tesla).
3.  **Resumir:** Crea un resumen de 2 frases para mostrar en la lista principal del frontend.

## 3. Calidad de Datos (Data Quality)
Implementa validaciones en el pipeline:
*   **Schema Validation:** Usa Pydantic para asegurar que el objeto noticia tiene todos los campos necesarios.
*   **Deduplicación:** Si dos fuentes traen la misma noticia, el pipeline debe detectar que el contenido es idéntico (puedes usar un hash del texto) y no guardarla dos veces.

---

## Reto de Performance
Optimiza tu pipeline para que el proceso de "Embedding + Carga en Vector DB" no tarde más de 2 segundos por noticia. Recuerda usar **Bash Inserción** si cargas muchas noticias a la vez.
