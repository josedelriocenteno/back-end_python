# Debugging de Errores Difíciles: El detective de datos

Hay errores que no aparecen en los tests y que solo ocurren en producción bajo condiciones extrañas. Aquí tienes técnicas avanzadas de observabilidad para resolverlos.

## 1. El error "Heisenbug"
Es el error que desaparece cuando intentas observarlo (ej: cuando pones un `breakpoint`, la sincronización de hilos cambia y el error no ocurre).
*   **Técnica:** Usa **Logging de Alta Fidelidad** (mucho detalle) enviado a un sistema de buffering (Redis/Kafka) para no ralentizar el proceso pero capturar toda la historia.

## 2. El error de "Condición de Carrera" (Race Condition)
Ocurre cuando dos procesos intentan modificar el mismo dato a la vez.
*   **Observabilidad:** Necesitas **timestamps de microsegundos** en tus logs y trazas para ver quién llegó primero realmente.

## 3. El error de "Degradación Lenta"
No es un fallo, es que el sistema se vuelve lento poco a poco.
*   **Observabilidad:** Mira las métricas de **Garbage Collection (GC)** de Python o el **Saturation** de la base de datos. A menudo es una fuga de conexiones (Connection Leak) que acaba bloqueando todo.

## 4. El error de "Datos Fantasma"
Datos que aparecen duplicados o que "desaparecen".
*   **Técnica:** Implementa **Auditoría de Ingesta**. Loguea el `hash` del archivo de entrada y compáralo con el `hash` de los datos en destino. Si no coinciden, alguien está modificando el dato en el camino.

## 5. El poder del "Exemplar"
Algunos sistemas modernos (como Prometheus + Grafana) te permiten hacer click en un pico de un gráfico (métrica) y saltar directamente a ver la traza asociada a ese punto concreto del tiempo.
*   Esto une la vista macro (la montaña del gráfico) con la vista micro (el rastro del usuario).

## Resumen: Sherlock Holmes del Cloud
Para resolver errores difíciles, necesitas herramientas que te den contexto, orden cronológico y visibilidad profunda. No confíes en tu intuición; confía en los datos que tu sistema de observabilidad ha recogido por ti.
