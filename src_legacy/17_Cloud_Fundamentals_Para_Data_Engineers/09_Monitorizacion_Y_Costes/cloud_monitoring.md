# Cloud Monitoring: El cuadro de mandos

Mientras que los logs son texto, **Cloud Monitoring** trata sobre números. Te permite ver la salud de tu sistema mediante métricas y dashboards visuales.

## 1. Métricas de Infraestructura
Google te da cientos de métricas "de caja":
- `% de CPU` usada en tus workers de Dataflow.
- `Número de Bytes` leídos en BigQuery.
- `Latencia` de respuesta de tus Cloud Functions.

## 2. Dashboards Personalizados
Crea paneles visuales que agrupen la información crítica.
- **Layout de un Dashboard de Datos:**
  - Gráfico de "Ingesta de filas por minuto".
  - Contador de "Pipelines Fallidos en últimas 24h".
  - Gráfico de "Gasto acumulado en BigQuery hoy".

## 3. Métricas Personalizadas (Custom Metrics)
Tu código de Python puede enviar métricas propias a Cloud Monitoring.
- **Ejemplo:** "Porcentaje de registros con emails mal formados en la última carga". 
- Esto permite monitorizar no solo si el código corre, sino si el **contenido** es correcto.

## 4. Agrupación por Etiquetas (Labels)
Usa las etiquetas que pusiste a tus proyectos para crear gráficos comparativos. "Gasto del Equipo A vs Equipo B".

## 5. Uptime Checks
Configura una prueba que intente conectar a tu base de datos o API cada minuto. Si el Uptime Check falla, Cloud Monitoring sabrá que el servicio está caído antes de que lo reporte un usuario.

## Resumen: Gestión Visual
"Lo que no se mide, no se puede mejorar". Cloud Monitoring te da los ojos necesarios para detectar cuellos de botella y asegurar que tus sistemas de datos rinden al nivel esperado por el negocio.
