# Ejercicios Prácticos: Caso de Diseño

Para asentar lo aprendido, intenta resolver estos tres escenarios reales. No necesitas escribir código, solo diseñar la solución usando los nombres de los servicios de GCP.

## Escenario A: Ingesta de Logs
Tu empresa tiene una App que genera 1 millón de eventos de log por minuto. Quieres ver un dashboard en tiempo real con los errores más comunes.
1. ¿Qué servicio recibiría los logs desde la App?
2. ¿Qué herramienta de procesamiento usarías para filtrar solo los errores?
3. ¿Dónde guardarías los datos finales para el dashboard?
4. **Solución sugerida:** Pub/Sub -> Dataflow -> BigQuery.

## Escenario B: Pipeline de Facturación
Un proveedor sube un archivo CSV con las facturas del mes a un Bucket de GCS de forma irregular (cualquier día entre el 1 y el 5). Quieres que el dato se cargue en BigQuery en cuanto llegue.
1. ¿Qué disparador (trigger) usarías?
2. ¿Qué servicio de cómputo ejecutaría la validación del CSV?
3. ¿Cómo asegurarías que el script tiene permiso para leer el Bucket?
4. **Solución sugerida:** GCS Event Trigger -> Cloud Function -> BigQuery (usando una Service Account específica).

## Escenario C: Optimización de Costes
Heredas un proyecto donde BigQuery cuesta 2.000€ al mes. Ves que hay una tabla de 10TB llamada `logs_historicos` de la que se hacen muchas queries de "Ventas por Tienda" mensuales. La tabla NO está particionada.
1. ¿Qué dos cambios técnicos harías en la tabla para bajar el coste?
2. ¿Qué harías con los archivos originales en Cloud Storage que tienen más de 2 años?
3. **Solución sugerida:** 1. Clonar la tabla con Particionado (por fecha) y Clustering (por id_tienda). 2. Crear una Lifecycle Policy en GCS para mover datos antiguos a Coldline/Archive.

## Reto Extra: Seguridad
Un desarrollador junior te pide el archivo JSON de la Service Account para probar un script en su local. ¿Qué le respondes?
- **Respuesta Senior:** "No te doy el JSON. Haz un `gcloud auth application-default login` con tu cuenta personal y asegúrate de que tu usuario tiene el rol de `BigQuery Data Viewer` en el entorno de desarrollo".

## Resumen: Pensar en Cloud
Estos ejercicios demuestran que el Data Engineering en GCP es un juego de arquitectura. La respuesta correcta siempre busca el equilibrio entre facilidad de mantenimiento, seguridad y coste.
