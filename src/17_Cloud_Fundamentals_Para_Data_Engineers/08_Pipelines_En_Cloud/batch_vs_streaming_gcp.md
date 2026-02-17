# Batch vs. Streaming en GCP: Casos Reales

Elegir entre Batch y Streaming en la nube no es solo una elección técnica, es una elección de coste y necesidad de negocio. GCP ofrece herramientas para ambos.

## 1. El modelo Batch (Por lotes)
- **Frecuencia:** Cada hora, día o semana.
- **Carga:** Ingesta desde GCS, procesos programados en Airflow.
- **Herramientas:** Cloud Storage -> BigQuery / Dataflow Batch.
- **Caso Real:** "Sincronizar las facturas de ayer con el cierre contable". No importa si tardas 10 minutos más, importa que el coste sea mínimo.

## 2. El modelo Streaming (En tiempo real)
- **Frecuencia:** Constante (segundo a segundo).
- **Carga:** Mensajes en Pub/Sub, datos de sensores IoT.
- **Herramientas:** Pub/Sub -> Dataflow Streaming -> BigQuery.
- **Caso Real:** "Detectar que un servidor se está sobrecalentando y enviar una alerta inmediata". Cada segundo de retraso cuenta.

## 3. Latencia vs. Coste
- **Batch:** Latencia alta (minutos/horas), coste bajo (cargas gratis, máquinas apagadas el resto del tiempo).
- **Streaming:** Latencia mínima (milisegundos/segundos), coste alto (servicios siempre encendidos, pago por MB insertado).

## 4. Arquitectura Lambda en GCP
A veces necesitas ambos.
- **Capa Rápida:** Streaming para el dashboard en vivo de hoy.
- **Capa Batch:** Proceso nocturno que recalcula todo con calma para corregir errores del streaming y asegurar que el dato de ayer sea 100% correcto.

## 5. Unificación (Apache Beam)
Gracias a Dataflow y Beam, hoy la diferencia es menor. Puedes escribir un único código de limpieza y decirle a GCP:
- "Ejecútalo sobre este archivo histórico de logs". (Batch)
- "Ejecútalo sobre este flujo de Pub/Sub en vivo". (Streaming)

## Resumen: La Pragmática del Dato
Pregúntate siempre: "¿Qué pasa si este dato tarda 1 hora más en llegar?". Si la respuesta es "nada importante", elige **Batch**. Si la respuesta es "perdemos dinero o clientes", elige **Streaming**.
