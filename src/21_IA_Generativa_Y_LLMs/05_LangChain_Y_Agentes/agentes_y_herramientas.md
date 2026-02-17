# Agentes y Herramientas: Dándole manos a la IA

Un **Agente** es un sistema que utiliza un LLM como "cerebro" para decidir qué acciones tomar y en qué orden para resolver una tarea compleja. A diferencia de una cadena fija, el agente es **autónomo**.

## 1. El concepto de Agentic Loop
1.  **Entrada:** El usuario pide algo difícil ("Mira el precio de Apple y dime si debería comprar").
2.  **Razonamiento:** El LLM analiza la petición y ve que no sabe el precio actual.
3.  **Herramienta (Tool):** El agente decide usar una herramienta de búsqueda financiera.
4.  **Observación:** Recibe el resultado de la herramienta.
5.  **Decisión:** El LLM lee el resultado y decide si ya puede responder o si necesita usar otra herramienta.

## 2. Tools: Las "Manos" de la IA
Una herramienta es simplemente una función de Python que el LLM sabe que puede llamar.
*   **Ejemplos:** Buscadores web, calculadoras, consultas a bases de datos SQL, conectores de Gmail o Slack.
*   **Cómo sabe usarla:** Le pasamos al modelo el nombre de la función y una descripción en texto natural. El modelo decide llamarla basándose en esa descripción.

## 3. Framework ReAct (Reason + Act)
Es la lógica de pensamiento más común en los agentes.
*   **Thought (Pensamiento):** "Necesito obtener el tiempo en Madrid".
*   **Action (Acción):** Llamar a `get_weather_api("Madrid")`.
*   **Observation (Observación):** "Hace 22 grados y está soleado".
*   **Final Answer:** "El tiempo en Madrid es estupendo, 22 grados y sol".

## 4. LangGraph y Agentes de Estado
Para aplicaciones profesionales, LangChain ha evolucionado hacia **LangGraph**.
*   Permite definir agentes como grafos cíclicos (nodos y aristas).
*   Da un control total sobre el estado del agente, permitiendo "pausar" la IA para pedir permiso a un humano antes de ejecutar una acción crítica (ej: realizar una transferencia bancaria).

## 5. El mayor reto: El Bucle Infinito
Los agentes pueden entrar en bucles si no saben resolver una tarea. Como ingenieros, debemos poner límites:
*   `max_iterations`: Máximo número de pasos.
*   `timeout`: Máximo tiempo de ejecución.

## Resumen: Del Ayudante al Trabajador Autónomo
Los agentes representan el siguiente nivel de la GenAI. Ya no solo responden preguntas, sino que actúan en el mundo real. Entender cómo dar herramientas a un LLM y cómo controlar su razonamiento es la clave para construir la próxima generación de software inteligente.
