# Costes de Monitorización: El observador observado

La observabilidad no es gratis. Guardar trillones de logs y métricas tiene un precio, y si no tienes cuidado, la monitorización puede acabar costando más que el propio proceso de datos.

## 1. El coste de Cloud Logging
Se cobra por Gigabyte de log almacenado.
*   **Tip:** No loguees cada fila de tu ETL en nivel `INFO`. Usa `DEBUG` y asegúrate de que el nivel en producción sea más restrictivo.
*   **Exclusión:** Usa "Log Exclusion Filters" para tirar a la basura logs ruidosos que no te interesan (ej: health checks constantes de un balanceador de carga).

## 2. El coste de las Métricas
GCP cobra por el número de puntos de datos que envías y por el número de métricas personalizadas.
*   **Tip:** No crees métricas con demasiadas dimensiones (etiquetas). Si tienes una etiqueta `user_id` en una métrica y tienes 1 millón de usuarios, acabarás con 1 millón de series temporales, lo cual es carísimo.

## 3. Retención y Almacenamiento
*   **Logging:** Por defecto son 30 días. Subir a 365 días multiplica el coste.
*   **Monitoreo:** Las métricas de GCP son gratis si usas las estándar y tienen una retención fija (normalmente 6 semanas).

## 4. Optimización con Log Sinks
Si necesitas guardar logs de auditoría por ley durante 5 años:
*   **MAL:** Dejarlos en Cloud Logging (Carísimo).
*   **BIEN:** Crear un Sink que los mueva automáticamente a **Cloud Storage** en clase **Archive**. El coste se reduce un 99%.

## 5. Monitorizando la monitorización
Crea una alerta de coste específica para tus servicios de observabilidad. Si el volumen de logs sube de repente un 500%, suele significar que hay un bot atacando tu web o que un desarrollador se ha dejado un log activado en un bucle infinito.

## Resumen: Equilibrio Financiero
Un buen Data Engineer sabe que la observabilidad perfecta es infinita en coste. Tu trabajo es encontrar el equilibrio: tener suficiente visibilidad para arreglar problemas rápido sin romper el presupuesto de la empresa.
