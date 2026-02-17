# Cloud Monitoring: El cuadro de mandos de la nube

Cloud Monitoring te da visibilidad sobre la salud y el rendimiento de tus aplicaciones e infraestructura mediante métricas, dashboards y chequeos de tiempo de actividad.

## 1. Métricas de Sistema (Out-of-the-box)
GCP recoge automáticamente cientos de métricas sin que tú hagas nada:
*   **Compute Engine:** Uso de disco, CPU, tráfico de red.
*   **Cloud Storage:** Número de peticiones, ancho de banda.
*   **BigQuery:** Tiempo de ejecución de queries, slots consumidos.

## 2. Métricas Personalizadas (Custom Metrics)
Puedes enviar tus propias métricas desde Python usando la SDK de Cloud Monitoring.
*   **Ejemplo:** `filas_procesadas`, `valor_total_ventas`.
*   Esto une la monitorización técnica con la monitorización de negocio en una sola herramienta.

## 3. Uptime Checks: El vigilante externo
Cloud Monitoring hace una petición a tu API desde diferentes lugares del mundo (EE.UU, Europa, Asia) cada minuto.
*   Si la API no responde desde 2 o más regiones, te avisa. 
*   Es la mejor forma de saber si tu servicio es accesible para tus usuarios finales.

## 4. Dashboards Gestionados
Igual que Grafana, GCP tiene su propio editor de dashboards integrado. 
*   **Ventaja:** No hay que instalar nada, ya tiene acceso a todas las métricas de GCP.
*   **Desventaja:** Menos flexible que Grafana para customizaciones visuales extremas.

## 5. MQL (Monitoring Query Language)
Es el lenguaje de consulta de Cloud Monitoring (equivalente a PromQL de Prometheus).
*   Permite hacer medias móviles, calcular tasas de cambio y unir métricas de diferentes recursos para ver el impacto global de un cambio.

## Resumen: Control del Rendimiento
Cloud Monitoring es la herramienta que te dice si tu infraestructura de datos está escalando correctamente o si estás a punto de quedarte sin recursos. Es la base para construir una operación de datos proactiva y no reactiva.
