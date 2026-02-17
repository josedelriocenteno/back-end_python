# ¿Qué son las Métricas?

Las **Métricas** son medidas numéricas agregadas que representan el estado de un sistema a lo largo del tiempo. A diferencia de los logs (que son eventos individuales), las métricas son series temporales que nos permiten ver tendencias, patrones y anomalías.

## 1. Los 4 Señales de Oro (The 4 Golden Signals)
Google define estas cuatro métricas como las más importantes para monitorizar cualquier sistema:
1.  **Latencia:** El tiempo que tarda una petición en completarse (ej: "99% de las queries tardan < 200ms").
2.  **Tráfico:** La demanda que recibe el sistema (ej: "Peticiones por segundo", "GB de datos ingestados").
3.  **Errores:** La tasa de peticiones que fallan (ej: "Error 500", "Filas rechazadas por esquema").
4.  **Saturación:** Qué tan "lleno" está el sistema (ej: "% CPU", "% Memoria", "% Disco").

## 2. Tipos de Métricas según su Naturaleza
*   **Counter (Contador):** Un valor que solo aumenta (ej: "Total de archivos procesados desde el inicio").
*   **Gauge (Indicador):** Un valor que puede subir y bajar (ej: "Número de workers activos actualmente", "Temperatura de la CPU").
*   **Histogram / Summary:** Una distribución de valores. Útil para medir latencias (ej: "El 50%, 90% y 99% de las respuestas").

## 3. Resolución y Retención
*   **Resolución:** Cada cuánto tiempo tomamos una medida (cada 1s, cada 1min). A mayor resolución, más detalle pero más coste de almacenamiento.
*   **Retención:** Cuánto tiempo guardamos las métricas (1 mes, 1 año). Los datos antiguos suelen "agregarse" para ocupar menos espacio (ej: de 1s a 1h de media).

## 4. Agregación y Dimensiones (Labels)
Las métricas profesionales incluyen etiquetas.
*   **Métrica:** `http_requests_total`
*   **Etiquetas:** `status_code=500`, `method=POST`, `service=auth`.
Esto te permite filtrar el dashboard y saber si los errores vienen solo del servicio de login o de toda la app.

## 5. El valor de la métrica
Las métricas son baratas de procesar y fáciles de visualizar en gráficos. Son la base para las **Alertas** (que veremos en la siguiente sección) y para los Dashboards de negocio.

## Resumen: El pulso del sistema
Las métricas te dicen si el sistema está sano y cómo evoluciona su rendimiento. Un Data Engineer que no mira sus métricas está operando a ciegas, esperando a que el usuario se queje para darse cuenta de que el sistema va lento.
