# ¿Qué es RAG (Retrieval-Augmented Generation)?

Los LLMs son inteligentes, pero tienen dos grandes limitaciones:
1.  **Conocimiento Cortado:** Solo saben lo que había en internet hasta el día en que terminó su entrenamiento.
2.  **No conocen tus datos:** No saben nada de tus facturas, tus manuales internos o tus clientes.

**RAG** es la arquitectura que soluciona esto dándole al modelo un "Libro de Consulta" en el momento de responder.

## 1. El concepto: Examen a libro abierto
Imagina que un estudiante hace un examen:
*   **Sin RAG:** Usa solo su memoria (el entrenamiento del modelo). Puede olvidar detalles o inventar (alucinar).
*   **Con RAG:** El profesor le deja tener el manual de la empresa sobre la mesa. El estudiante lee la pregunta, busca el párrafo relevante en el manual y redacta la respuesta basándose en lo que acaba de leer.

## 2. Los 3 pasos de RAG

### A. Retrieval (Recuperación)
El sistema busca en tu base de datos (usualmente una Vector DB) los trozos de información más relevantes para la pregunta del usuario.

### B. Augmentation (Aumentación)
Añadimos esos trozos de información al prompt original del usuario.
*   **Prompt aumentado:** "Usa únicamente este contexto para responder a la pregunta. Si no está en el contexto, di que no lo sabes. CONTEXTO: [Párrafos recuperados] PREGUNTA: [Pregunta del usuario]"

### C. Generation (Generación)
El LLM lee el "super-prompt" y genera una respuesta informada y veraz.

## 3. Ventajas de RAG vs. Fine-tuning
| Característica | Fine-tuning (Re-entrenar) | RAG (Contexto) |
| :--- | :--- | :--- |
| **Coste** | Muy alto (GPU, tiempo). | Bajo (API de Vector DB). |
| **Actualización** | Lenta (hay que re-entrenar). | Instantánea (añades un PDF a la DB). |
| **Alucinaciones** | Altas. | Muy bajas (se ciñe al texto). |
| **Privacidad** | Difícil de controlar. | Fácil (filtros de metadata en la DB). |

## 4. ¿Por qué es el estándar en la industria?
RAG permite construir aplicaciones de IA fiables, baratas y que siempre tienen la información actualizada al segundo. Es la base de los asistentes virtuales modernos, buscadores corporativos y sistemas de análisis de documentos.

## Resumen: Inteligencia con Memoria Externa
RAG transforma un LLM genérico en un experto en tu dominio específico. Al separar el "motor de lenguaje" (la IA) de la "fuente de verdad" (tus datos), consigues lo mejor de ambos mundos: una comunicación natural unida a una precisión documental absoluta.
