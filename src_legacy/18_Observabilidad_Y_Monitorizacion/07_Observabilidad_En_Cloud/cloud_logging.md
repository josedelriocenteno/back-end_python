# Cloud Logging: El cerebro de los logs en GCP

Google Cloud Logging (antiguamente Stackdriver) es un servicio totalmente gestionado que permite almacenar, buscar, analizar y alertar sobre los logs de todos tus recursos en GCP y más allá.

## 1. Agregación Automática
Cualquier cosa que escribas en el "Standard Output" (stdout) de una Cloud Function, Cloud Run o Compute Engine, Google lo captura automáticamente y lo mete en Cloud Logging. No necesitas configurar servidores de logs.

## 2. Logs Explorer: El buscador avanzado
Es la interfaz web para buscar logs. Permite usar un lenguaje de consulta potente:
*   `resource.type="cloud_run_revision" AND severity>=ERROR`
*   `textPayload:"timeout"`
*   `jsonPayload.user_id = 456` (Si usas logs estructurados en JSON).

## 3. Log-based Metrics: De logs a gráficos
Puedes convertir una frase en un número.
*   **Ejemplo:** Cada vez que aparezca la frase "Error de pago" en los logs, crea una métrica llamada `total_errores_pago`.
*   Esto permite crear alarmas sobre logs sin tener que programar nada en tu código de Python.

## 4. Log Sinks: Exportando el conocimiento
Los logs en Cloud Logging tienen una retención limitada (normalmente 30 días). Si quieres guardarlos para siempre o analizarlos con SQL:
*   **Sink a BigQuery:** Para analítica de seguridad o auditoría a largo plazo.
*   **Sink a Cloud Storage:** Para archivado barato.
*   **Sink a Pub/Sub:** Para disparar otro proceso automáticamente cuando ocurre un evento específico en el log.

## 5. Structured Logging en GCP
Si envías JSON, GCP lo "aplana" automáticamente. Verás campos como `severity`, `timestamp` y `httpRequest` perfectamente integrados en la consola, permitiéndote filtrar por latencia de petición o por código de estado HTTP de forma nativa.

## Resumen: Visibilidad Centralizada
Cloud Logging es el primer sitio donde debes mirar cuando algo falla en la nube. Su capacidad para centralizar trillones de líneas de log y permitirte encontrar una aguja en un pajar en segundos es lo que lo hace indispensable para cualquier Data Engineer.
