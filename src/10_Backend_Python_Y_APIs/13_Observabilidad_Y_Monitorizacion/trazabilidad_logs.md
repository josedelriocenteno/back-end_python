# Trazabilidad y Agregación de Logs

Cuando tienes una API con muchos usuarios, los archivos de log en texto plano se vuelven imposibles de manejar. Necesitas un sistema de **Logging Centralizado**.

## 1. El Stack ELK / EFK
*   **Elasticsearch:** La base de datos donde se guardan y buscan los logs.
*   **Logstash / Fluentd:** Los mensajeros que recogen los logs del servidor y los llevan a Elasticsearch.
*   **Kibana:** La interfaz para buscar. Permite hacer búsquedas tipo: `status_code: 500 AND user_id: 123`.

## 2. Logs Estructurados (JSON)
En lugar de escribir texto libre, tu API debería emitir JSON.
*   **Mal:** `Error en el login del usuario 4`
*   **Bien:** `{"event": "login_failed", "user_id": 4, "ip": "1.2.3.4", "severity": "error"}`
Esto permite que Elasticsearch indexe cada campo y puedas filtrar por ellos en un segundo.

## 3. Tracing Distribuido (OpenTelemetry)
Si tu API llama a otros microservicios, necesitas saber dónde se pierde el tiempo.
*   **Trace ID:** Un ID que viaja a través de todos los servidores.
*   **Span:** El tiempo que se tarda en una operación concreta (ej: una query SQL).
*   **Herramienta:** Jaeger o Honeycomb.

## 4. Contexto en los Logs
Asegúrate de que cada línea de log incluya automáticamente:
*   `Environment` (prod/stg).
*   `App Version`.
*   `Correlation ID` (para unir logs de la misma petición).

## 5. Rotación de Logs
No dejes que los archivos de log llenen el disco duro del servidor. Usa herramientas como `logrotate` o, mejor aún, envía los logs directamente a la salida estándar (`stdout`) para que Docker los gestione.

## Resumen: Convirtiendo Ruido en Señal
La trazabilidad no sirve para culpar a nadie, sino para entender el comportamiento de sistemas complejos y ruidosos. En una empresa senior, buscar el origen de un error en producción debería llevar segundos, no horas.
