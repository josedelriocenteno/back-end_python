# Logs en Pipelines: Monitorización Estructurada

En un entorno de datos, un "print" no es suficiente. Necesitas logs que permitan reconstruir qué pasó cuando un pipeline falló en mitad de la noche.

## 1. Logging Estructurado (JSON)
Evita los logs de texto plano. Usa JSON para que herramientas como ELK (Elasticsearch, Logstash, Kibana) o Grafana Loki puedan indexarlos y permitir búsquedas rápidas.
```json
{"timestamp": "2024-03-15T10:00:01Z", "pipeline": "ingest_orders", "task": "extract", "status": "ERROR", "error_code": "API_TIMEOUT", "retry_count": 2}
```

## 2. Contexto del Dato
Un log de Data Engineering debe incluir metadatos sobre el lote de datos que se está procesando:
- `batch_id`: ID único de la ejecución.
- `rows_processed`: Cuántas filas se leyeron.
- `source_system`: De qué API o DB viene.

## 3. Niveles de Log Profesionales
- **INFO:** Inicio/Fin de tareas, volumen de datos procesados.
- **WARNING:** Reintentos automáticos, datos con calidad dudosa que han pasado el filtro.
- **ERROR:** El pipeline se detiene o una tarea crítica ha fallado tras agotar reintentos.
- **DEBUG:** Solo para desarrollo. Muestra las consultas SQL generadas o trozos de la respuesta de la API.

## 4. Trazabilidad entre Tareas
Si el pipeline tiene 10 pasos, todos los logs de esa ejecución deben compartir un mismo `trace_id`. Esto permite ver el flujo completo de un dato desde que entra hasta que sale.

## 5. Tip Senior: No inundes el disco
Configura políticas de rotación y retención. No necesitas los logs detallados (DEBUG) de un pipeline que funcionó bien hace 6 meses. Quédate solo con los errores y los sumarios de ejecución (INFO).

## Resumen: Ojos en el Sistema
Los logs son los ojos del ingeniero. Un sistema bien loqueado es un sistema fácil de depurar, reduciendo el "Mean Time to Recovery" (MTTR) cuando las cosas van mal.
