# Salidas Estructuradas: La IA que habla JSON

El mayor problema de los LLMs para un backend es su tendencia a hablar "demasiado". Si tu API espera un JSON limpio pero la IA responde: "Claro, aquí tienes tu objeto: { ... }", tu código romperá. Debemos forzar la **Salida Estructurada**.

## 1. El Prompt Determinista
Incluye siempre la instrucción de formato y prohíbe el texto adicional.
*   **Prompt:** "Analiza el sentimiento de este texto. Responde ÚNICAMENTE en formato JSON plano con la clave 'sentimiento' y el valor (positivo/negativo). No incluyas preámbulos ni explicaciones."

## 2. Definición del Esquema
Es mucho mejor darle el esquema exacto que esperas.
*   **Prompt:** 
    "Devuelve un JSON con este esquema:
     {
       "id": "integer",
       "resumen": "string",
       "prioridad": "high|medium|low"
     }"

## 3. JSON Mode (OpenAI / Anthropic)
La mayoría de las APIs modernas tienen un parámetro `response_format: { "type": "json_object" }`.
*   **Ventaja:** El modelo garantiza que la salida será un JSON válido. Si no lo es, el propio motor de IA lo reintenta internamente.
*   **Requisito:** Aun usando este modo, debes mencionar la palabra "JSON" explícitamente en el prompt.

## 4. Validación con Pydantic
Incluso si la IA devuelve JSON, siempre debes validarlo en tu backend antes de procesarlo.
```python
from pydantic import BaseModel, ValidationError

class AnalisisResponse(BaseModel):
    sentimiento: str
    puntuacion: float

# Después de recibir la respuesta de la IA (res_ai)
try:
    data = AnalisisResponse.model_validate_json(res_ai)
    print(f"Todo correcto: {data.sentimiento}")
except ValidationError as e:
    print(f"La IA se equivocó de formato: {e}")
```

## 5. El Futuro: Herramientas de extracción (Instructor / Outlines)
Existen librerías como **Instructor** (para Python) que te permiten pasar una clase Pydantic directamente a la llamada de la IA y recibir el objeto ya instanciado y validado. Magia para el desarrollador.

## Resumen: Integración Segura
Lograr que la IA hable el mismo lenguaje que tus microservicios (JSON) es lo que permite automatizar procesos de negocio complejos. No permitas el texto libre en tus integraciones de backend; estructura siempre la salida para garantizar la estabilidad de tu sistema.
