# Optimización de Costes: Tips del Experto

Una vez que tenemos el control, el siguiente paso es la optimización activa. Aquí tienes un checklist de acciones que reducen la factura de GCP de forma inmediata.

## 1. BigQuery: Poda y Almacenamiento
- **Particionado Permanente:** Prohíbe las tablas sin particionar en datasets grandes.
- **Clustering:** Reduce los bytes leídos al buscar filtros específicos.
- **Vistas Materializadas:** Ahorran cómputo repetitivo en agregaciones.

## 2. Cloud Storage: Lifecycle polices
- Todo lo que no se haya tocado en 90 días -> **Coldline**.
- Todo lo que no se haya tocado en 365 días -> **Archive**.
- Borra versiones antiguas de objetos que ya no necesites.

## 3. Cómputo: Preemptibles y Serverless
- Usa **Spot VMs** (Preemptibles) para todos tus clústeres de Spark de prueba y para pipelines batch que admitan reintentos.
- Pasa de Compute Engine a **Cloud Run** siempre que el proceso lo permita. Pagar solo cuando el código corre es la mayor optimización posible.

## 4. Red: Egress Cost
- Mantén el tráfico dentro de la red de Google.
- **Tip:** No descargues datos de S3 (AWS) a GCP si no es estrictamente necesario. Mover datos entre nubes diferentes es una de las partidas más caras de la factura.
- Usa **Private Google Access** para hablar con las APIs de Google sin salir a internet.

## 5. El "Zombi Hunt" (Caza de Zombis)
Busca y elimina:
- IPs públicas estáticas reservadas pero no asignadas a ninguna máquina.
- Snapshots de discos duros de máquinas que ya borraste hace meses.
- Discos persistentes (`pd-standard`) que se quedaron sueltos al borrar una VM.

## Resumen: Mejora Continua
La optimización de costes no es una tarea de una vez, es un proceso continuo. Un sistema optimizado es un sistema elegante que usa los recursos justos para dar el máximo valor al negocio.
