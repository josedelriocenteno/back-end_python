# Alertas en Cloud: Notificaciones Efectivas

Gestionar alertas en la nube es mucho más que enviar un email. GCP permite crear flujos complejos de notificación para asegurar que el mensaje llegue a la persona adecuada en el momento justo.

## 1. Canales de Notificación
Cloud Monitoring soporta múltiples destinos:
*   **Slack / PagerDuty:** Para el equipo de ingeniería.
*   **Webhooks:** Para disparar un script automático que intente arreglar el problema.
*   **Email / SMS:** Como respaldo.
*   **Pub/Sub:** Para automatizaciones avanzadas (ej: apagar un servidor si el coste sube demasiado).

## 2. Tipos de Condiciones de Alerta
*   **Threshold (Umbral):** La métrica supera un valor fijo.
*   **Absent (Ausencia):** La métrica DEJA de llegar (ej: "Airflow no ha emitido ningún log en 1 hora"). Es vital para detectar pipelines que se quedan "colgados" en silencio.
*   **Forecast (Pronóstico):** Alertar basándose en una tendencia futura.

## 3. Manejo de Incidentes
Cuando una alerta de GCP se dispara, crea un **Incidente**.
*   Puedes ver cuánto duró el incidente.
*   Añadir comentarios sobre qué se hizo para arreglarlo.
*   Revisar el historial para ver si el mismo fallo se repite cada lunes.

## 4. Filtros y Agregaciones
Usa las etiquetas (labels) de GCP para no volverte loco con las alertas.
*   No pongas una alerta por cada base de datos. Pon una alerta genérica: "Avisa si CUALQUIERA de las bases de datos con la etiqueta `env=prod` tiene poco espacio en disco".

## 5. Alertas de Presupuesto (Budgets)
Como Data Engineer, tus alertas más importantes a veces no son técnicas, son de dinero.
*   Configura alertas en **Cloud Billing** para que te avisen cuando lleves gastado el 50%, 90% y 100% de tu presupuesto mensual. Esto evita sorpresas desagradables al final del mes.

## Resumen: Comunicación Crítica
Las alertas en cloud son el seguro de vida de tu plataforma. Configurarlas correctamente, usando los canales adecuados y evitando el ruido, es lo que garantiza que tu sistema de datos sea profesional y confiable 24/7.
