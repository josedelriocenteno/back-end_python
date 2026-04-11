# Alertas Buenas vs. Malas: Evitando el ruido

Diseñar alertas es un arte. Una mala configuración puede destruir la productividad de un equipo y generar un estrés innecesario. Aprende a distinguir lo que aporta valor de lo que es puro ruido.

## 1. Las 4 Características de una Buena Alerta
Para que una alerta sea de calidad, debe ser:
1.  **Accionable:** Si no puedo hacer nada para arreglarlo, no debería ser una alerta.
2.  **Urgente:** Requiere atención en los próximos minutos u horas.
3.  **Real:** El problema existe de verdad (no es un error momentáneo de red de 2 segundos).
4.  **Específica:** Me dice exactamente qué está fallando (no un genérico "Error en el sistema").

## 2. Ejemplos Reales
*   **ALERTA MALA:** "Uso de CPU > 80%". (Puede ser un pico normal, deja de sonar a los 2 minutos, genera estrés inútil).
*   **ALERTA BUENA:** "La latencia del 99% de las peticiones supera los 5s durante más de 10 min". (Esto indica una degradación real del servicio que los usuarios están notando).

## 3. Estrategias para Reducir el Ruido
*   **Intervalo de observación (For):** No alertes al primer segundo de fallo. Espera a que la condición se mantenga (ej: "durante 5 minutos"). Esto filtra los "glitches" o picos puntuales.
*   **Deduplicación:** Si un clúster de 10 máquinas falla, no envíes 10 alertas. Agrupa los mensajes en uno solo: "Fallo en el clúster X (10 instancias afectadas)".
*   **Alertas Predictivas:** En lugar de "Disco Lleno (100%)", alerta cuando "Al ritmo actual, el disco se llenará en 4 horas".

## 4. Clasificación de Notificaciones
*   **Emergencias (3 AM):** Solo por PagerDuty / SMS / Llamada.
*   **Errores durante el día:** Canal de Slack `#ops-alerts`.
*   **Información / Status:** Email resumen diario.

## 5. El "Check de Utilidad" semanal
Revisa tus alertas una vez por semana.
*   ¿Cuántas han sonado?
*   ¿Cuáles no hemos arreglado porque "no eran importantes"? -> **Bórralas o súbeles el umbral.**
*   ¿Qué fallo tuvimos que NO avisó la alerta? -> **Crea una nueva.**

## Resumen: Calidad sobre Cantidad
Tu objetivo como ingeniero es tener el **mínimo número de alertas posible** que garanticen la salud del sistema. Menos ruido significa respuestas más rápidas y un equipo más feliz y productivo.
