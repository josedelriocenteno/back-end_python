# Recursos y Servicios: El catálogo de GCP

Entender qué es un "recurso" y cómo se agrupan en "servicios" es fundamental para navegar por la consola de Google Cloud y usar sus herramientas.

## 1. ¿Qué es un Recurso?
Es el objeto fundamental que creas en la nube. 
- Una tabla de BigQuery es un recurso.
- Una instancia de base de datos SQL es un recurso.
- Incluso una regla de firewall es un recurso.
Todos los recursos tienen una URL única interna llamada **Self Link**.

## 2. Los Servicios (APIs)
Google Cloud es un conjunto de APIs gigantesco. Para usar un servicio (ej: BigQuery), primero debes **Habilitar la API** correspondiente en tu proyecto.
- Si la API de BigQuery no está habilitada, no puedes crear tablas aunque tengas permisos de administrador.

## 3. Categorías Principales para Data Engineering
- **Storage:** Cloud Storage, Cloud SQL, Bigtable.
- **Compute:** Compute Engine (VMs), Kubernetes Engine (GKE), Cloud Run.
- **Big Data:** BigQuery, Dataflow, Dataproc, Pub/Sub.
- **AI/ML:** Vertex AI, Vision API.

## 4. gcloud CLI y Cloud Shell
Aunque existe la consola web, el Data Engineer profesional usa la terminal.
- **gcloud:** La herramienta de línea de comandos para gestionar casi cualquier recurso de GCP.
- **Cloud Shell:** Una máquina virtual gratuita con Linux y el SDK de Google Cloud preinstalado que puedes abrir desde tu navegador.

## 5. El concepto de "Managed Service" (Servicio Gestionado)
Muchos servicios de GCP son versiones de herramientas código abierto pero gestionadas por Google.
- **Cloud SQL** = MySQL / Postgres gestionado.
- **Dataproc** = Hadoop / Spark gestionado.
- **Cloud Composer** = Apache Airflow gestionado.
Esto significa que Google se encarga de los parches y la alta disponibilidad, tú solo de usarlos.

## Resumen: Una gran caja de piezas
GCP es como un Lego infinito. Dominar la ingeniería de datos en la nube es saber qué pieza (recurso) elegir de qué caja (servicio) para construir la arquitectura más eficiente y robusta para tu problema específico.
