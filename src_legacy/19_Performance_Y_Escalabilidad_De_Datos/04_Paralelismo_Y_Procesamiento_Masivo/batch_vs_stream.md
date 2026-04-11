# Batch vs. Streaming: El tiempo del dato

Elegir cómo procesar los datos influye dramáticamente en el rendimiento, el coste y la frescura de la información (Latencia).

## 1. Procesamiento Batch (Lotes)
Los datos se acumulan y se procesan todos juntos en momentos específicos (ej: cada noche a las 2 AM).
*   **Pros:** Muy eficiente en coste (uso masivo de recursos en poco tiempo). Fácil de debugear y de recuperar si falla (Idempotencia).
*   **Contras:** Latencia alta. El negocio recibe los datos con horas o días de retraso.
*   **Uso:** Reportes de ventas mensuales, backups, analítica histórica.

## 2. Procesamiento Streaming (Tiempo Real)
Los datos se procesan a medida que llegan, uno a uno o en micro-lotes.
*   **Pros:** Latencia mínima (milisegundos o segundos). El negocio puede reaccionar al instante.
*   **Contras:** Muy complejo de mantener. Coste alto (servidores encendidos 24/7). Difícil de gestionar fallos y orden de llegada.
*   **Uso:** Detección de fraude bancario, recomendaciones en tiempo real, monitorización de sistemas críticos.

## 3. El Micro-Batch
Es un punto medio (como Apache Spark Streaming). Los datos se procesan en lotes pequeños (ej: cada 5 segundos). Combina la eficiencia del batch con una latencia aceptable para casi todos los casos de uso.

## 4. El coste de la inmediatez
Pregúntate siempre: "¿Necesita el negocio este dato YA o puede esperar una hora?". 
*   Pasar de un proceso de 1 hora a uno de 1 segundo puede multiplicar la complejidad y el coste por 10. No lo hagas si no es estrictamente necesario.

## 5. Arquitectura Lambda y Kappa
*   **Lambda:** Tienes dos caminos; uno rápido (streaming) para resultados aproximados hoy y uno lento (batch) para resultados exactos mañana.
*   **Kappa:** Todo es streaming. El histórico se trata como si fuera un flujo de datos infinito que se vuelve a reproducir.

## Resumen: Calidad vs. Velocidad
El procesamiento batch es el rey de la eficiencia; el streaming es el rey de la oportunidad. Un Data Engineer senior evalúa el valor de negocio de la latencia antes de elegir la tecnología de procesamiento masivo.
