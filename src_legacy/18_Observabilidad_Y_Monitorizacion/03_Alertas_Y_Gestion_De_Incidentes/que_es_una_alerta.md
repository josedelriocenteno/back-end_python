# ¿Qué es una Alerta?

Una **Alerta** es la señal que emite un sistema de monitorización cuando una métrica o un log atraviesa un umbral predefinido que requiere atención humana. Las alertas son el "teléfono de emergencia" de tu plataforma de datos.

## 1. El ciclo de vida de una Alerta
1.  **Observación:** Prometheus lee la métrica (ej: `% CPU`).
2.  **Evaluación:** Se comprueba la regla (ej: "¿Es la CPU > 90% durante más de 5 minutos?").
3.  **Disparo (Firing):** La condición se cumple y la alerta se activa.
4.  **Notificación:** El sistema envía un mensaje (Slack, Email, SMS).
5.  **Resolución:** Un humano arregla el problema y la métrica vuelve a valores normales.

## 2. Tipos de Alertas según su Gravedad
*   **Crítica (Critical / Page):** El sistema está caído o los datos se están perdiendo. Despierta a alguien a las 3 AM.
*   **Advertencia (Warning):** Hay un problema que no es inminente pero debe arreglarse hoy (ej: "El disco está al 80%").
*   **Informativa:** No requiere acción inmediata, solo queda registrada para el reporte semanal.

## 3. Elementos de una buena Alerta
Una alerta profesional debe incluir:
*   **Qué está pasando:** "Latencia alta en el servicio de facturación".
*   **Gravedad:** "CRITICAL".
*   **Contexto:** Link al Dashboard de Grafana para ver el gráfico.
*   **Instrucciones:** Link al "Playbook" (manual de instrucciones) para saber cómo arreglarlo.

## 4. Alertas de Síntoma vs. Alertas de Causa
*   **Síntoma (Recomendado):** "Los usuarios no pueden subir archivos". (Nos dice que el negocio está sufriendo).
*   **Causa:** "La CPU del servidor A está al 95%". (Puede ser normal si hay un proceso pesado, no siempre significa que el usuario sufra).
**Tip Senior:** Prioriza siempre alertar sobre los síntomas que afectan al cliente final.

## 5. El coste del ruido
Si una alerta suena y no hay nada que arreglar, es una "Falsa Alarma". Muchas falsas alarmas provocan **Alert Fatigue**, haciendo que el equipo las ignore y que, el día que ocurra un desastre real, nadie preste atención.

## Resumen: Eficiencia en la Respuesta
Las alertas no son para "saber cosas", son para "hacer cosas". Cada alerta debe ser una llamada a la acción clara y necesaria. Si no requiere que un humano haga nada, no pongas una alerta; pon un gráfico en un dashboard.
