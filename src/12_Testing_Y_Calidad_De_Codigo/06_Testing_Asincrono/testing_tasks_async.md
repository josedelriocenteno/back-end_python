# Testing de Background Tasks (Tareas en Segundo Plano)

En APIs modernas con FastAPI o Celery, es común responder al usuario "202 Accepted" y procesar la tarea (como generar un PDF o procesar una imagen) en segundo plano. ¿Cómo testeamos algo que ocurre "después" de que la API responde?

## 1. El reto: La asincronía "invisible"
Si testeas el endpoint y compruebas el resultado inmediatamente, el test fallará porque la tarea aún no habrá terminado.

## 2. Estrategia 1: Ejecución Síncrona en Tests
Es la más sencilla. Configura tu sistema para que, **solo en el entorno de test**, las tareas no se vayan al segundo plano sino que se ejecuten en el hilo principal.
- **FastAPI:** Usa el objeto `BackgroundTasks` pero ejecútalo manualmente en el test.
- **Celery:** Usa la configuración `task_always_eager = True`. Así, cuando llames a `.delay()`, el test esperará a que termine.

## 3. Estrategia 2: Spies de Tareas
Si no quieres ejecutar la lógica real, puedes usar un **Mock** para verificar que la tarea se "encoló" correctamente.
```python
@patch("app.tasks.enviar_email_bienvenida.delay")
def test_registro_encola_email(mock_task, client):
    client.post("/register", json={"email": "nuevo@user.com"})
    # Verificamos que la tarea se mandó a la cola con el email correcto
    mock_task.assert_called_once_with("nuevo@user.com")
```

## 4. Estrategia 3: Polling (Sondeo) con Tiempo de Espera
Para tests de integración E2E reales, tendrás que esperar.
- Ejecutas la acción.
- Entras en un bucle: ¿Está listo el PDF? -> Esperar 0.5s -> ¿Está listo?
- **Tip Senior:** Usa librerías como `tenacity` o `wait-for-it` para gestionar estos bucles con un "timeout" máximo (ej: 5 segundos) para que el test no se quede colgado para siempre.

## 5. Inspección de la Cola (Message Broker)
Si usas Redis o RabbitMQ, tus tests de integración pueden conectarse a la cola para ver si el mensaje está ahí y si el formato JSON es el correcto.

## Resumen: Fiabilidad en el desacoplamiento
Testear tareas en segundo plano requiere decidir entre velocidad (Estrategia 1) o realismo (Estrategia 3). Un buen desarrollador senior usa la ejecución síncrona para unit tests y el sondeo real para un par de tests críticos de integración.
