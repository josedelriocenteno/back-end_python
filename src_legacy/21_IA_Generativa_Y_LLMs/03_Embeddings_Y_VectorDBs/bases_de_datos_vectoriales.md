# Bases de Datos Vectoriales: Almacenando Significados

Una base de datos tradicional (como Postgres) es excelente buscando por `ID` o por `nombre`. Una **Base de Datos Vectorial** (Vector DB) está diseñada para buscar por **Similitud**.

## 1. El reto de la escala
Si tienes 10.000 vectores de 1536 dimensiones, buscar el "más cercano" a una pregunta del usuario es fácil. Pero si tienes 100 millones de vectores, la búsqueda lineal es demasiado lenta. 

Las Vector DBs utilizan algoritmos de **Búsqueda Aproximada de Vecinos (ANN)** para encontrar resultados en milisegundos.

## 2. Funcionamiento: El Índice Vectorial
A diferencia de un índice B-Tree, las Vector DBs usan:
*   **HNSW (Hierarchical Navigable Small World):** Crea un grafo de conexiones entre vectores similares. Es muy rápido y preciso.
*   **IVF (Inverted File Index):** Divide el espacio en "clústeres" y busca solo en el clúster más cercano.

## 3. Tipos de Vector DBs

### A. Específicas (Nativas)
Diseñadas desde cero para vectores.
*   **Pinecone:** SaaS (nube) puro. Muy fácil de usar y escala increíble.
*   **Weaviate / Qdrant / Milvus:** De código abierto, muy potentes para grandes volúmenes.
*   **Chroma:** Ideal para desarrollo local y prototipos sencillos.

### B. Extensiones de Bases de Datos Clásicas
*   **pgvector (PostgreSQL):** La opción favorita para ingenieros backend. Te permite tener tus tablas de siempre y tus vectores en la misma base de datos.

## 4. El flujo de trabajo (Pipeline)
1.  **Chunking:** Divides tus documentos largos en trozos pequeños (chunks).
2.  **Embedding:** Pasas cada chunk por un modelo de IA para obtener su vector.
3.  **Indexing:** Guardas el vector + el texto original (metadata) en la Vector DB.
4.  **Query:** Cuando el usuario pregunta, conviertes su pregunta en un vector y pides a la DB los 5 resultados más cercanos.

## 5. Metadata Filtering
Una gran ventaja de estas bases de datos es que permiten filtrar por datos normales Y por vector a la vez.
*   **Consulta:** "Busca documentos similares a X **pero solo** los que sean del año 2024".

## Resumen: Memoria de Largo Plazo para la IA
Las Bases de Datos Vectoriales son el disco duro semántico de tus aplicaciones. Permiten que tu IA tenga acceso a millones de piezas de información privada de forma instantánea, convirtiéndose en el componente crítico de cualquier arquitectura de RAG (Retrieval Augmented Generation).
