# ¿Cuándo usar Threads en el Backend moderno?

En la era de `asyncio` y `multiprocessing`, el viejo `threading` parece haber quedado relegado. Sin embargo, sigue teniendo casos de uso fundamentales donde es la mejor (o la única) opción.

## 1. Integración con Librerías Síncronas (Legacy)
Si tu backend tiene que conectarse a una base de datos vieja (ej: un SQL Server de hace 15 años) o una API industrial que solo tiene un driver síncrono bloqueante:
- **Asyncio fallará:** El driver bloqueará todo el servidor.
- **Threading es la solución:** Envuelve la llamada síncrona en un hilo. FastAPI hace esto automáticamente cuando usas `def` en lugar de `async def`.

## 2. Esperas de I/O de Alta Latencia y Baja Frecuencia
Si tienes que esperar 10 segundos a que un script externo termine, pero solo lo haces una vez cada hora:
- No merece la pena complicar el sistema con colas de tareas pesadas (Celery). Un simple hilo es suficiente y consume muy pocos recursos.

## 3. Interfaces de Usuario (GUI o CLI Interactivo)
Si estás haciendo una herramienta de terminal para el equipo de HR o Finance que debe mostrar una barra de progreso mientras descarga datos:
- Los hilos permiten que la barra de progreso siga animándose (Hilo 1) mientras la descarga ocurre (Hilo 2).

## 4. El "ThreadPoolExecutor": Lo mejor de dos mundos
`asyncio` tiene una función maravillosa llamada `loop.run_in_executor()`. Permite llamar a funciones síncronas desde código async de forma segura, usando un pool de hilos de fondo. 
- Proporciona la sencillez del multithreading con la potencia del Event Loop.

## 5. Limitaciones Críticas (No olvidar el GIL)
Recuerda: **NUNCA uses hilos para acelerar cálculos matemáticos en Python.** Solo servirán para tareas donde la CPU esté ociosa esperando a la red o al disco.

## Resumen: Una herramienta más
Un desarrollador senior no desprecia los hilos por ser "antiguos". Los hilos son una herramienta de bajo nivel, madura y robusta. Aprende a usarlos para rellenar los huecos donde `asyncio` no llega, especialmente al trabajar con sistemas heredados o dependencias síncronas.
