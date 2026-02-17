# Arquitectura de un Pipeline End-to-End en GCP

Diseñar un pipeline profesional requiere combinar todos los servicios que hemos visto en una estructura lógica y segura. Este es el plano de una arquitectura "estándar" en GCP.

## 1. Fase 1: Ingesta (Ingestion)
- **Fuentes:** APIs, Bases de Datos On-premise, logs de Web.
- **Servicios:** 
  - **Cloud Functions:** Para disparar la extracción.
  - **Pub/Sub:** Para recibir datos en streaming de forma segura y escalable.

## 2. Fase 2: Almacenamiento Crudo (Bronze / Landing)
- **Servicio:** **Cloud Storage**.
- Los datos se guardan tal cual vienen de la fuente. Si algo falla en el futuro, siempre podemos volver aquí y re-procesar los datos originales.

## 3. Fase 3: Procesamiento y Limpieza (Silver)
- **Servicios:**
  - **Dataflow:** Si la transformación es muy compleja o requiere Python/Java pesado.
  - **BigQuery (Cargas):** Si el dato ya viene estructurado.
- Se eliminan nulos, se corrigen formatos de fecha y se validan esquemas.

## 4. Fase 4: Modelado y Analítica (Gold)
- **Servicio:** **BigQuery**.
- Aquí es donde el analista hace `SELECT`. Las tablas están particionadas, tienen clustering y contienen métricas de negocio listas para PowerBI o Looker.

## 5. Fase 5: Orquestación (The Glue)
- **Servicio:** **Cloud Composer (Airflow)**.
- Se encarga de enganchar todas las fases: "Si la ingesta terminó, empieza la limpieza. Si la limpieza falló, manda un Slack".

## 6. Monitoreo Vertical
- **Cloud Monitoring / Logging:** Atraviesa todas las fases para darnos alertas en caso de error.

## Resumen: El Ecosistema Funcionando
Una arquitectura de datos exitosa no es la que usa la herramienta más moderna, sino la que garantiza que el dato viaja de la fuente al negocio de forma segura, barata y automatizada. Este diseño de capas es la base para cualquier Data Engineer en el ecosistema de Google.
