# Cloud Logging: El diario de tu infraestructura

**Cloud Logging** (antes Stackdriver Logging) es el lugar centralizado donde todos tus servicios de GCP escriben sus logs. Para un Data Engineer, es el primer sitio donde mirar cuando un pipeline "desaparece" o falla.

## 1. Logs Automáticos
Casi todo lo que pasa en GCP se registra solo:
- Cuándo se leyó un archivo de un Bucket.
- Quién lanzó una query en BigQuery.
- Los errores de sistema de una Cloud Function.

## 2. Logs Estructurados (JSON)
Si escribes tus propios logs desde Python, hazlo en formato JSON.
- **Ventaja:** Cloud Logging detectará automáticamente campos como `severity` (ERROR, INFO), `trace_id` o metadatos personalizados, permitiéndote filtrar logs de forma ultra rápida.

## 3. Explorador de Logs
Es la interfaz web para buscar.
- Usa **Logs Analytics** para lanzar queries SQL sobre tus propios logs. Sí, puedes usar SQL para saber cuántas veces ha fallado tu pipeline en la última semana.

## 4. Log Sinks (Exportación)
Los logs en el explorador suelen guardarse 30 días. Si necesitas guardarlos por cumplimiento legal o para analizarlos a largo plazo:
- Crea un **Log Sink** que envíe automáticamente una copia de todos los logs a un Bucket de Cloud Storage o a una tabla de BigQuery.

## 5. Log-based Metrics
Puedes crear una métrica basada en un log.
- **Ejemplo:** "Crea un número que cuente cuántas veces aparece la palabra 'Timeout' en los logs de mi script de Python". Luego puedes crear un gráfico o una alerta con ese número.

## Resumen: Todo queda registrado
Cloud Logging es la memoria de tu plataforma de datos. Un buen Data Engineer no solo escribe código, diseña qué información debe quedar registrada en los logs para que el "yo del futuro" pueda arreglar los problemas a las 3 de la mañana en minutos.
