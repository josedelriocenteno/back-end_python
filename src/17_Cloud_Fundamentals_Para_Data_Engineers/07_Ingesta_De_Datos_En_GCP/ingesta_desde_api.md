# Ingesta desde APIs Externas con Python

Muchos datos (conversiones de Ads, información del tiempo, precios de competencia) vienen de APIs externas. El Data Engineer debe escribir el código que actúe como puente entre internet y GCP.

## 1. El Flujo Estándar
1. **Extracción:** Script de Python llama a la API externa.
2. **Transformación Básica:** Conversión de JSON a una lista de diccionarios.
3. **Persistencia:** Guardar como Parquet en un Bucket de GCS (Capa Bronze).
4. **Carga:** Movemos de GCS a BigQuery.

## 2. Bibliotecas Clave en Python
- `requests` o `httpx`: Para hacer las llamadas HTTP a la API.
- `google-cloud-storage`: Para subir el resultado al Bucket.
- `google-cloud-bigquery`: Para disparar la carga final si no queremos pasar por GCS (aunque pasar por GCS es una mejor práctica).

## 3. Manejo de Secretos
**NUNCA** guardes la API Key o el Password en el código de Python.
- Usa **Google Secret Manager**. Tu script de Python consulta el secreto en tiempo de ejecución de forma segura.

## 4. Paginación y Límites (Rate Limiting)
Las APIs suelen tener límites.
- Tu script debe manejar la paginación (ej: pedir 100 resultados, luego los siguientes 100).
- Debes implementar esperas (`time.sleep`) si la API te dice que vas demasiado rápido (Error 429).

## 5. Dónde ejecutar este código
- **Cloud Functions:** Para APIs pequeñas que se consultan cada hora.
- **Cloud Run:** Para APIs que devuelven volúmenes grandes de datos que requieren más de 10 minutos de proceso.
- **Cloud Composer (Airflow):** Para orquestar múltiples llamadas a APIs con dependencias complejas.

## Resumen: Integración Total
La ingesta desde APIs es lo que permite que el Data Warehouse sea una fuente de verdad para toda la empresa, no solo para los datos internos. Un buen script de ingesta es resiliente a fallos de red y protege las credenciales de la empresa.
