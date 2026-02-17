# Patrones de Ingesta: Push vs. Pull

Elegir cómo viaja el dato desde el origen hasta tu nube es la decisión arquitectónica más importante del Data Engineer.

## 1. Modelo PULL (Tirar del dato)
Es el más común. Tu sistema (ej: Airflow) "va" a buscar el dato.
- **Pros:** Control total del horario. Podemos re-intentar si falla.
- **Contras:** Si el dato llega a la fuente a las 3:05 y tu proceso corre a las 4:00, hay una latencia de 55 minutos.
- **Ejemplo:** Script Python que consulta una API de facturación una vez al día.

## 2. Modelo PUSH (El dato viene a nosotros)
El sistema origen nos "empuja" el dato.
- **Pros:** Latencia mínima. El dato se procesa en cuanto ocurre.
- **Contras:** El origen debe ser capaz de enviarlo. Si nuestro sistema está caído, podemos perder el dato si no hay una cola (Kafka/PubSub) en medio.
- **Ejemplo:** Un Webhook de Shopify enviando un JSON a una Cloud Function cada vez que hay una venta.

## 3. Ingesta por Eventos (Event-Driven)
Es una variante del PUSH.
- El sistema origen sube un archivo a un Bucket.
- **Evento:** El Bucket dispara una notificación a una Cloud Function.
- **Acción:** La función lo procesa inmediatamente.
- **Uso:** Ideal para archivos que llegan a horas irregulares de diferentes proveedores.

## 4. Change Data Capture (CDC)
Para ingestar bases de datos operacionales (Postgres, Oracle) sin saturarlas.
- En lugar de hacer `SELECT *` de toda la tabla cada hora, el sistema lee el "log de transacciones" de la base de datos y solo se lleva los cambios (Inserts, Updates, Deletes).
- **Herramientas:** Datastream (GCP), Debezium.

## 5. El criterio de elección
- **¿Volumen gigante?** -> Pull / Batch.
- **¿Necesitas velocidad?** -> Push / Streaming.
- **¿Minimizar impacto en origen?** -> CDC.

## Resumen: Arquitectura a medida
No hay un patrón único. Un buen Data Engineer combina Pull para históricos y datos maestros, con Push/Event-driven para acciones de usuario críticas, creando un ecosistema de datos ágil y equilibrado.
