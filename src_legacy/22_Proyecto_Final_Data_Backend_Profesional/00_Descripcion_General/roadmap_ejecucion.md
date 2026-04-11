# Roadmap de Ejecución: Paso a Paso

Construir un sistema complejo requiere orden. No intentes programar la IA antes de tener dónde guardar los datos. Sigue este orden de batalla:

## Fase 1: Cimientos (Semana 1)
1.  **Entorno:** Configura el repositorio con `poetry`, `docker-compose` y los linters.
2.  **Infraestructura:** Levanta los contenedores de PostgreSQL y la base de datos Vectorial (ChromaDB o pgvector).
3.  **Modelado:** Diseña las tablas SQL para las noticias y los usuarios.

## Fase 2: Ingesta y Pipelines (Semana 2)
1.  **Extractor:** Crea un script que descargue datos (usando una API de noticias o scraping ético).
2.  **Pipeline ETL:** Implementa el procesamiento con Python (limpieza, normalización).
3.  **Embeddings:** Genera los vectores de las noticias y guárdalos en la Vector DB.

## Fase 3: Backend y API (Semana 3)
1.  **FastAPI:** Crea los endpoints para consultar las noticias y ver las estadísticas.
2.  **Seguridad:** Implementa el login con OAuth2 y JWT.
3.  **Tests:** Escribe pruebas unitarias y de integración para tu API.

## Fase 4: Inteligencia y RAG (Semana 4)
1.  **Módulo RAG:** Implementa la lógica de búsqueda semántica y respuesta con LLM (OpenAI/Gemini).
2.  **Agentes:** Crea un agente que pueda generar un reporte PDF semanal automáticamente.
3.  **Observabilidad:** Añade logs profesionales y monitorización de costes de tokens.

---

## Consejos para el Éxito
*   **Commit early, commit often:** No esperes a tener todo listo para subir a Git.
*   **Documenta mientras programas:** Es mucho más fácil escribir el README ahora que dentro de un mes.
*   **MVP Primero:** Haz que el flujo básico funcione antes de añadir "features de lujo".
