# Reintentos y Recovery: El diseño resiliente

En un sistema distribuido y cloud, los fallos temporales (glitches) son inevitables. Tu pipeline debe estar diseñado para auto-repararse siempre que sea posible.

## 1. El concepto de "Retries" (Reintentos)
Si una API devuelve un error 500 o la red falla un segundo, no queremos que todo el pipeline de 4 horas muera.
*   **Estrategia:** Reintentar la tarea automáticamente X veces antes de darla por fallida.

## 2. Exponential Backoff (Espera Exponencial)
No reintentes inmediatamente. Si el servidor de origen está saturado, reintentar al segundo siguiente solo lo saturará más.
*   **Estrategia:** Espera 1s, luego 2s, luego 4s, luego 8s... así das tiempo al sistema externo a recuperarse.

## 3. Circuit Breaker (Disyuntor)
Si un servicio externo falla constantemente (ej: 10 veces seguidas), el "disyuntor" se abre y dejas de llamarlo durante un tiempo.
*   Evitas gastar recursos inútilmente y permites que el sistema externo se recupere sin tu presión constante.

## 4. Checkpoints (Puntos de control)
Si tu pipeline tiene 10 pasos y falla en el paso 9, no quieres empezar de cero desde el paso 1.
*   Guarda el estado intermedio en una tabla temporal o un bucket de GCS.
*   Al reiniciar, el pipeline lee el checkpoint y continúa desde donde se quedó.

## 5. El botón de "Backfill" (Recuperación histórica)
A veces el error no es temporal y tienes que volver a procesar los datos de hace 3 días.
*   Tu código debe estar preparado para recibir una fecha como parámetro y re-ejecutar el proceso de ese día sin duplicar datos (usando Idempotencia, que veremos a continuación).

## Resumen: Tolerancia a Fallos
Diseñar para el éxito es fácil; diseñar para el fallo es lo que define a un ingeniero senior. Un sistema resiliente es aquel que asume la imperfección de la nube y tiene mecanismos automáticos para recuperarse sin necesidad de intervención manual constante.
