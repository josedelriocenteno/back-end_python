# Dashboards con Grafana: Visualizando el Caos

Tener millones de métricas en Prometheus no sirve de nada si no puedes verlas de forma intuitiva. **Grafana** es la herramienta estándar para crear cuadros de mando (dashboards) visuales y profesionales.

## 1. Conexión a la fuente (Data Source)
Grafana es agnóstico. Se conecta a Prometheus, BigQuery, Cloud Monitoring, CloudWatch, etc., y permite mezclar datos de todos ellos en una sola pantalla.

## 2. Tipos de Paneles
*   **Graph (Time Series):** Para ver la evolución temporal (ej: CPU en las últimas 24h).
*   **Stat / Singlestat:** Un número gigante para resaltar un dato crítico (ej: "Error rate: 0.05%").
*   **Table:** Para ver listados (ej: "Top 10 procesos más lentos").
*   **Gauge:** El típico reloj de velocidad.

## 3. Principios de un Buen Dashboard
*   **Jerarquía:** Lo más importante (Golden Signals) arriba a la izquierda.
*   **Contexto:** Pon leyendas y unidades claras (¿Son milisegundos o segundos?).
*   **Dashboard Fatality:** No pongas 50 gráficos en una pantalla. Si necesitas buscar mucho, el dashboard ha fallado. Crea varios dashboards por cada capa (Infraestructura, App, Datos).

## 4. Variables y Filtros Dinámicos
Usa variables para que el mismo dashboard sirva para todo.
*   Un menú desplegable arriba donde elijas `Entorno: [Prod, Staging, Dev]` o `Servicio: [Billing, Users, Data-Ingest]`. Los gráficos se actualizarán solos al cambiar la opción.

## 5. El "Dashboard de Guardia" (On-call)
Es un dashboard especial diseñado para ser visto rápidamente cuando suena el teléfono a las 3 AM. Debe responder tres preguntas en 10 segundos:
1.  ¿Está roto?
2.  ¿Dónde está roto?
3.  ¿Qué impacto tiene en el usuario?

## Resumen: Comunicación Visual
Un dashboard bien diseñado es una herramienta de comunicación. Permite que tanto los desarrolladores como los jefes de negocio entiendan el estado del proyecto de un solo vistazo, reduciendo el estrés y facilitando la toma de decisiones basada en datos reales.
