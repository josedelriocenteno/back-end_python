# Cloud Composer: Airflow gestionado

**Cloud Composer** es la versión gestionada de **Apache Airflow** dentro de Google Cloud. Es el "Cerebro" que orquesta todos tus servicios de datos (GCS, BigQuery, Dataflow, etc.).

## 1. ¿Por qué usar Composer y no instalar Airflow?
- **Despliegue en 1 Click:** Google crea todo el entorno (Kubernetes, Postgres para metadatos, Redis) por ti.
- **Escalabilidad:** Puedes aumentar el número de workers si tienes muchos DAGs corriendo a la vez.
- **Integración Nativa:** Viene con todos los operadores de Google Cloud instalados y configurados para usar las identidades de IAM de forma segura.

## 2. Arquitectura de Composer
Composer corre sobre **Google Kubernetes Engine (GKE)**.
- **Airflow Web Server:** La interfaz que ya conoces.
- **Airflow Scheduler:** El que decide qué tarea toca ejecutar.
- **GCS Bucket:** Cada entorno de Composer tiene un bucket asociado. Subes tus archivos `.py` de los DAGs a la carpeta `/dags/` de ese bucket y Airflow los detecta al instante.

## 3. El rol del Orquestador
**Regla de Oro:** Composer (Airflow) es un director de orquesta, no un músico.
- **BIEN:** Usar Composer para decir: "Extrae de la API, sube a GCS y dile a BigQuery que cargue el dato".
- **MAL:** Leer un archivo de 5GB de Pandas dentro de una tarea de Airflow. Saturarás el entorno y harás que falle.

## 4. Versiones 1 vs 2
- **Composer 2 (Recomendado):** Usa **Airflow 2** y tiene auto-escalado real de workers. Mucho más eficiente y rápido que la versión 1.

## 5. Secretos y Variables
Usa las variables de Airflow para configuraciones, pero para passwords y API Keys, integra Composer con **Google Secret Manager** para que tu código sea 100% seguro.

## Resumen: Control Centralizado
Cloud Composer es lo que permite que una colección de scripts sueltos se convierta en una plataforma de datos industrial. Es la herramienta que te da visibilidad sobre qué ha fallado, cuándo y por qué, permitiéndote gestionar cientos de pipelines con un solo equipo.
