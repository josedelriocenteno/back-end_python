# Cloud Run: Contenedores Serverless

Cloud Run es, probablemente, el mejor servicio de cómputo para un Data Engineer moderno. Te permite ejecutar contenedores Docker de forma totalmente gestionada y escalable.

## 1. El concepto: Contenedor -> URL
Tú empaquetas tu código (ej: un script de Python que limpia datos) en una imagen Docker y se la das a Cloud Run. Google te devuelve una URL. Cuando alguien llama a esa URL, Google enciende el contenedor, procesa la petición y lo apaga.

## 2. Escalado a Cero
Si nadie usa tu servicio, Cloud Run tiene **coste CERO**. No pagas por una máquina encendida; solo pagas por los segundos que tu código está corriendo.
- Si de repente llegan 1.000 peticiones a la vez, Cloud Run levanta 100 contenedores en segundos para atenderlas.

## 3. Cloud Run Jobs
Para Data Engineering, esta es la joya de la corona. A diferencia de un "Servicio" (que espera peticiones HTTP), un **Job** simplemente corre hasta que termina su tarea.
- **Uso:** Pipelines Batch que procesan un lote de archivos y luego se detienen.

## 4. Ventajas para Datos
- **Sin límites de lenguaje:** Puedes usar Python, Rust, Go o incluso C++. Si cabe en un Docker, corre en Cloud Run.
- **Conectividad:** Se integra perfectamente con Cloud Storage y BigQuery usando IAM.
- **Recursos:** Puedes asignar hasta 8 CPUs y 32GB de RAM por contenedor.

## 5. Despliegue Directo desde Git
Puedes configurar Cloud Run para que, cada vez que hagas `git push` a tu repositorio, se cree una nueva versión del pipeline automáticamente.

## Resumen: Simplicidad y Potencia
Cloud Run elimina la fricción de gestionar servidores. Es ideal para microservicios de datos, APIs de ML y pequeños procesos ETL que antes requerían una máquina virtual completa y cara.
