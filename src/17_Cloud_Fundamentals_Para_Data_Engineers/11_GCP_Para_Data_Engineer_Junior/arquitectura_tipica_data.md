# Arquitectura Típica de Datos en una Empresa

Aunque cada empresa es un mundo, el 80% de las arquitecturas de datos modernas en Google Cloud siguen un patrón similar. Entender este "plano" te ayudará a orientarte en cualquier proyecto nuevo.

## 1. El flujo de Izquierda a Derecha
Los datos nacen en los sistemas operacionales y mueren en los dashboards de decisión.

## 2. Ingesta (El Puente)
- **Fuentes:** SAP, Salesforce, Logs de la web, Base de datos de la App (Postgres).
- **Herramientas:** 
  - **Fivetran / Airbyte / BQ Data Transfer:** Para traer datos de SaaS.
  - **Cloud Functions / Cloud Run:** Para scripts personalizados de Python.
  - **Cloud Pub/Sub:** Para eventos en tiempo real.

## 3. Data Lake (El Almacén)
- **Servicio:** **Cloud Storage**.
- Se organiza en capas:
  - `landing/`: El dato tal cual llega.
  - `archive/`: El dato de hace meses/años en clase Coldline.

## 4. Data Warehouse (La Factoría)
- **Servicio:** **BigQuery**.
- Aquí el dato se transforma.
- **dbt:** Es la herramienta estándar que casi todas las empresas usan hoy dentro de BigQuery para crear las tablas finales.

## 5. Orquestación (El Director)
- **Servicio:** **Cloud Composer (Airflow)**.
- Encadenar los procesos: "Si Fivetran terminó de traer los datos de Salesforce, lanza el modelo de dbt en BigQuery".

## 6. Consumo (El Valor)
- **Looker / Tableau / PowerBI:** Conectados directamente a BigQuery.
- **Vertex AI:** Para que los Data Scientists entrenen modelos consumiendo de las tablas Gold de BigQuery.

## Resumen: Simplicidad sobre Complejidad
Una arquitectura profesional evita complicarse con herramientas exóticas. Se basa en servicios estables (GCS, BQ) y bien orquestados. Como Junior, tu objetivo es entender cómo fluye el dato entre estas piezas sin romperse.
