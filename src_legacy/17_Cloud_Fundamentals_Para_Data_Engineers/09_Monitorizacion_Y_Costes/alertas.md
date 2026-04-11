# Alertas: Notificaciones Inteligentes

Una alerta es la acción que ocurre cuando una métrica atraviesa un umbral peligroso. Es lo que evita que tengas que estar mirando los dashboards constantemente.

## 1. El ciclo de una Alerta
1. **Condición:** "Si el uso de CPU de BigQuery supera el 90% durante más de 5 minutos".
2. **Notification Channel:** Dónde avisar (Slack, Email, PagerDuty, o un SMS).
3. **Incident:** Se abre un incidente en la consola de Google para que el equipo lo gestione y lo cierre cuando esté arreglado.

## 2. Alertas de Fallo Técnico
- **Cloud Composer:** Notificar si un DAG falla más de 2 veces seguidas.
- **Dataflow:** Notificar si el "System Lag" (retraso en streaming) supera los 10 minutos.

## 3. Alertas de Anomalía de Datos
A veces el pipeline no falla, pero los datos son basura.
- **Log-based Alert:** "Si aparece la palabra 'Data Quality Error' en los logs, avísame".
- Ayuda a detectar problemas de origen antes de que lleguen a los reportes finales.

## 4. Alertas de "Falta de Datos"
Son las más difíciles de configurar pero las más útiles.
- "Si la tabla de ventas no ha recibido ninguna fila nueva en las últimas 2 horas, manda una alerta crítica".

## 5. Gestión del Silencio (Muting)
No dejes que las alertas te saturen (**Alert Fatigue**). 
- Configura periodos de silencio durante mantenimientos programados para que el equipo no reciba notificaciones falsas.

## Resumen: Dormir Tranquilo
Las alertas son tu red de seguridad. Un sistema bien alertado te permite ser productivo durante el día con la confianza de que la plataforma te avisará solo cuando tu intervención sea realmente necesaria.
