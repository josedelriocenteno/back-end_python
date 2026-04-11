# Cloud Functions: Procesamiento por Eventos

Cloud Functions es la unidad mínima de cómputo en GCP. Es código puro (una sola función) que se ejecuta en respuesta a un evento. Es lo que se conoce como FaaS (Function as a Service).

## 1. Arquitectura Event-Driven
La función está "dormida" hasta que algo la despierta:
- Se sube un archivo a un Bucket de Cloud Storage.
- Llega un mensaje a un tópico de Pub/Sub.
- Se recibe una petición HTTP.
- Un log de error crítico aparece en el sistema.

## 2. Lenguajes Soportados
Google soporta oficialmente Python, Node.js, Go, Java, .NET y Ruby. 
- Para Data Engineering, **Python** es la opción estándar. Solo necesitas un archivo `main.py` y un `requirements.txt`.

## 3. Limitaciones Importantes
- **Tiempo de ejecución:** Máximo 60 minutos (normalmente se usan para tareas de menos de 5-10 mins).
- **Memoria:** Hasta 16GB.
- **Estado:** Son "Stateless". No guardan archivos en disco para la siguiente ejecución. Todo lo que quieras guardar debe ir a Cloud Storage o una DB.

## 4. Casos de Uso en Data
- **Landing to Bronze:** En cuanto llega un `.csv` de un proveedor, la Cloud Function lo valida y lo mueve a la carpeta de datos crudos.
- **Micro-Ingesta:** Una función que se dispara cada 5 minutos (vía Cloud Scheduler) para consultar el precio del Bitcoin y guardarlo en BigQuery.
- **Notificaciones:** Enviar un mensaje de Slack si un pipeline crítico falla.

## 5. 1ª Gen vs 2ª Gen
- **2ª Gen (Recomendada):** Basada en Cloud Run. Permite ejecuciones más largas, más memoria y manejar múltiples peticiones al mismo tiempo en la misma instancia.

## Resumen: El "pegamento" de la nube
Las Cloud Functions son las piezas que unen los diferentes servicios de datos. Son baratas, rápidas de programar y escalan de forma transparente para el ingeniero.
