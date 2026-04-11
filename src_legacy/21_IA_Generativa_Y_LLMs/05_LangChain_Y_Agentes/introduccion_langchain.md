# LangChain: El framework para orquestar la IA

Cuando tu aplicación de IA se vuelve compleja (varios lenguajes, fuentes de datos, histórico de chats), escribir prompts a mano y gestionar llamadas a APIs se vuelve un caos. **LangChain** es el framework que pone orden en este proceso.

## 1. ¿Por qué usar un Framework?
Puedes llamar a OpenAI con la librería oficial, pero LangChain te ofrece:
*   **Abstracción:** Cambiar de GPT-4 a Claude o Llama cambiando solo una línea de código.
*   **Componibilidad:** Encadenar diferentes pasos (ej: busca en Google -> resume -> traduce -> envía email).

## 2. Los Componentes Principales

### A. Model I/O
Gestión de modelos de chat y plantillas de prompts (`PromptTemplates`). Permite reutilizar prompts con variables dinámicas.

### B. Retrieval (RAG)
Herramientas para cargar documentos, dividirlos (Splitters) e interactuar con Vector DBs de forma estandarizada.

### C. Chains (Cadenas)
El corazón de LangChain. Permiten unir acciones.
*   **LCEL (LangChain Expression Language):** Una sintaxis declarativa (usando el operador `|`) para diseñar flujos de datos.

### D. Memory (Memoria)
Los LLMs son "stateless" (no recuerdan nada). LangChain gestiona automáticamente el guardado de los últimos mensajes en una base de datos (Redis, SQL) y los inyecta en cada nuevo prompt para dar sensación de continuidad.

## 3. Ejemplo de LCEL (Pipeline sencillo)
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_template("Cuéntame un chiste sobre {tema}")

# Definimos la cadena de forma declarativa
chain = prompt | model

# Ejecutamos
print(chain.invoke({"tema": "programación"}))
```

## 4. Alternativas a LangChain
Aunque es el más popular, existen otros frameworks potentes:
*   **LlamaIndex:** El mejor si tu enfoque es puramente RAG y manejo de datos complejos.
*   **Haystack:** Muy sólido para aplicaciones industriales de búsqueda.
*   **Semantic Kernel:** La apuesta de Microsoft, ideal para entornos .NET.

## Resumen: La arquitectura de la IA
LangChain no hace que la IA sea más inteligente, hace que sea más **manejable**. Permite que los ingenieros construyan flujos de trabajo complejos, mantenibles y agnósticos al modelo, convirtiendo un script de chat sencillo en una aplicación empresarial robusta.
