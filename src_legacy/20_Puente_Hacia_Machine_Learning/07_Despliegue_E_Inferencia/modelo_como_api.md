# Modelo como API: Inferencia en Tiempo Real

La forma más común de consumir un modelo de ML en una aplicación web o móvil es exponiéndolo a través de una **API REST**.

## 1. El Stack Tecnológico
Para servir modelos en Python, solemos usar:
*   **FastAPI:** El framework más rápido y moderno para crear APIs.
*   **Uvicorn:** El servidor que ejecuta FastAPI.
*   **Pydantic:** Para validar que los datos que envía el usuario son correctos antes de pasárselos al modelo.

## 2. Flujo de una petición de IA
1.  **Request:** El cliente envía datos (ej: JSON con la edad y ciudad del usuario).
2.  **Validación:** Pydantic comprueba que son números y strings correctos.
3.  **Pre-procesamiento:** Se aplican las transformaciones necesarias (escalado, codificación) que el modelo espera.
4.  **Inferencia:** El modelo (`model.predict()`) genera la respuesta.
5.  **Response:** La API devuelve el resultado al cliente.

## 3. Ejemplo conceptual con FastAPI
```python
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("modelo_final.pkl")

@app.post("/predict")
def predict(data: dict):
    # En un caso real usaríamos Pydantic para validar 'data'
    prediction = model.predict([list(data.values())])
    return {"resultado": int(prediction[0])}
```

## 4. Retos de la Inferencia Online
*   **Latencia:** El modelo debe responder en menos de 100-200ms para no arruinar la experiencia del usuario.
*   **Concurrencia:** ¿Qué pasa si 1.000 personas piden una predicción a la vez? Necesitamos balanceadores de carga y varias instancias del modelo.
*   **Memoria:** Algunos modelos de Deep Learning ocupan Gigabytes de RAM; el servidor debe tener capacidad suficiente.

## 5. Servidores Especializados (Model Servers)
Para casos de alto rendimiento, no escribimos la API a mano. Usamos software que ya viene optimizado:
*   **BentoML:** Excelente para empaquetar modelos como microservicios.
*   **TFServing:** Específico para modelos de TensorFlow.
*   **TorchServe:** Específico para modelos de PyTorch.

## Resumen: La IA al servicio del usuario
Convertir un modelo en una API es el paso final para que la inteligencia artificial se convierta en una funcionalidad real de un producto. La clave aquí es la **velocidad** y la **robustez**: el usuario no debe percibir que detrás de la aplicación hay una red neuronal compleja realizando millones de cálculos matemáticos.
