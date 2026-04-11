# Testing de Código Concurrente

Testear código asíncrono o multihilo es significativamente más difícil que el código secuencial. El mayor enemigo aquí es el **No-Determinismo**: el test pasa en tu local pero falla en el CI/CD.

## 1. Herramientas Obligatorias
- **Pytest-asyncio:** Ya lo vimos en el Tema 12. Permite hacer `await` dentro de los tests.
- **Pytest-timeout:** Imprescindible. Si un test asíncrono tiene un deadlock, se quedará colgado para siempre, bloqueando toda la pipeline. Pon un timeout de 10s a cada test.

## 2. Evitar el "Sleep" en los Tests
Usar `time.sleep()` o `asyncio.sleep()` para esperar a que una tarea termine es una mala práctica.
- **Solución:** Usa **Polling con Timeout**. Mira si el resultado está listo cada 0.1s hasta un máximo de 5s.

## 3. Test de Condiciones de Carrera (Monkey Patching)
Para forzar errores de concurrencia, puedes usar técnicas de "Chaos Engineering":
- Introduce retrasos aleatorios en tus mocks para ver si el sistema sigue siendo coherente cuando el orden de respuesta de las APIs cambia.

## 4. Aislamiento del Bucle de Eventos
Asegúrate de que cada test crea y destruye su propio Event Loop. Si los tests comparten el loop, el estado sucio de un test (tareas sin cancelar) arruinará al siguiente.

## 5. Testing de Multiprocessing
Testear procesos separados es doloroso porque los mocks no se comparten entre procesos. 
- **Estrategia Senior:** Testea la lógica de la función por separado (Unit Test) y luego haz un test de integración que verifique que el sistema de procesos el lanza y recoge los datos correctamente, sin intentar mockear el interior del subproceso.

## Resumen: Rigor en la Incertidumbre
El código concurrente requiere una suite de tests más robusta y "paranoica". Si un test falla una de cada 100 veces, no es un error aleatorio, es una Race Condition real que ocurrirá en producción bajo carga. Investígala hasta encontrar la raíz del problema.
