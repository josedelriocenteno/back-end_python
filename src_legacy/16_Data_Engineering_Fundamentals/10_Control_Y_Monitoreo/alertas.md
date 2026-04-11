# Alertas: Cuando el silencio es peligroso

Una alerta es un mecanismo de notificación automática cuando una métrica sobrepasa un umbral crítico. Una buena estrategia de alertas evita el agotamiento (Alert Fatigue).

## 1. Tipos de Alertas
- **Hard Failure:** El pipeline se ha detenido por un error de código o red.
- **SLA Violation:** El pipeline sigue corriendo pero ha tardado más de lo prometido.
- **Data Anomaly:** El pipeline ha terminado pero el volumen de datos es inusualmente bajo.

## 2. Canales de Notificación
- **Slack/Discord/Teams:** Para alertas de prioridad media/baja durante el horario laboral.
- **PagerDuty/Opsgenie:** Para alertas críticas que requieren despertar a alguien a las 4 AM.
- **Email:** Solo para reportes diarios de salud (no para urgencias).

## 3. Anatomía de una buena alerta
Un mensaje de alerta debe incluir:
- **Qué pasa:** "Pipeline X ha fallado".
- **Gravedad:** "CRITICO - Dashboard de ventas afectado".
- **Contexto:** Enlace a los logs y al orquestador (Airflow).
- **Plan de acción (Runbook):** Enlace a la documentación que explica cómo arreglar este error específico.

## 4. Evitar la "Alert Fatigue"
Si envías alertas por cada pequeño aviso, el equipo acabará ignorando el canal de Slack. 
- **Regla:** Solo alerta si se requiere una acción humana inmediata. Si el sistema se auto-corrige con reintentos, no envíes una alerta crítica, simplemente loguéalo.

## 5. Alertas de "Falta de Datos"
A veces lo que falla es que **NADA** ocurre. Configura una alerta que salte si el pipeline NO ha corrido cuando debería haberlo hecho (Dead Man's Snitch).

## Resumen: Dormir Tranquilo
Las alertas son tu seguro de vida. Un sistema de alertas bien configurado te permite no tener que mirar los dashboards cada 5 minutos, confiando en que el sistema te avisará solo cuando tú seas realmente necesario.
