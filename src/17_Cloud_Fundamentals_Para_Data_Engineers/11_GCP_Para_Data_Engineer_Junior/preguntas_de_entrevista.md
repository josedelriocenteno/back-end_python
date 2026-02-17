# Preguntas de Entrevista: GCP + Data

Si te estás preparando para entrar en el mundo del Data Engineering, estas son algunas de las preguntas "clásicas" que te harán sobre Google Cloud.

## 1. Sobre BigQuery
- **Pregunta:** "¿Cuál es la diferencia entre Particionado y Clustering? ¿Cuándo usarías cada uno?".
- **Respuesta clave:** Particionado para filtros de tiempo (segmenta físicamente). Clustering para filtros frecuentes con mucha variedad de valores (ordena dentro de la partición). Ambos reducen coste y tiempo.

## 2. Sobre Almacenamiento
- **Pregunta:** "Un cliente necesita guardar datos durante 5 años por ley pero casi nunca los leerá. ¿Qué clase de GCS elegirías?".
- **Respuesta clave:** `Archive Storage`. Es el más barato para guardar pero el más caro para recuperar.

## 3. Sobre Seguridad e IAM
- **Pregunta:** "¿Cómo conectarías un script de Python en local a BigQuery de forma segura?".
- **Respuesta clave:** Usando `gcloud auth application-default login` para desarrollo, o una Service Account con el rol de `BigQuery Data Viewer` si es para un servidor estable. Nunca usar mi usuario personal o subir JSONs a Git.

## 4. Sobre Pipelines
- **Pregunta:** "El pipeline ha fallado y no hay datos nuevos en el dashboard. ¿Cuáles son tus primeros 3 pasos?".
- **Respuesta clave:** 1. Mirar el estado del DAG en Airflow/Cloud Composer. 2. Revisar los **Cloud Logging** para buscar el error de Python/SQL. 3. Comprobar si el archivo crudo ha llegado al bucket de GCS.

## 5. Sobre Arquitectura
- **Pregunta:** "¿Cuándo usarías una Cloud Function frente a un Cloud Run?".
- **Respuesta clave:** Cloud Function para eventos cortos (subida de un archivo). Cloud Run para procesos más largos, microservicios que necesitan Docker o que requieren más de 10-15 minutos de ejecución.

## Resumen: Justifica tus Decisiones
En una entrevista no buscan que seas una enciclopedia de Google. Buscan que entiendas los **Trade-offs** (ventajas y desventajas) de cada servicio y que sepas elegir el más eficiente para el negocio.
