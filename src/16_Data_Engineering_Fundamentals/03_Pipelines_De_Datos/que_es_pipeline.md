# ¿Qué es un Pipeline? El sistema circulatorio del dato

Un pipeline de datos es un conjunto de procesos automatizados que transforman datos crudos en información lista para ser consumida. Sin pipelines, el dato es estático e inútil.

## 1. La anatomía del Pipeline
Todo pipeline profesional tiene estos componentes:
- **Source (Fuente):** Donde nace el dato (BBDD, API, Kafka).
- **Processing (Procesamiento):** La lógica que limpia y transforma.
- **Sink (Destino):** Donde muere el dato (BigQuery, S3).
- **Buffer:** Opcional, para manejar picos de datos (RabbitMQ, PubSub).

## 2. Los desafíos del Pipeline
- **Latencia:** Cuánto tarda el dato en llegar de la fuente al destino.
- **Fiabilidad:** ¿Qué pasa si el servidor se apaga a mitad del pipeline?
- **Escalabilidad:** ¿Puede el pipeline manejar 10x más datos el Black Friday?

## 3. Composición de Piplines
Un gran pipeline suele estar compuesto por pequeños pipelines modulares:
1. **Ingestion Pipeline:** Solo mueve datos de A a B.
2. **Cleansing Pipeline:** Limpia y normaliza.
3. **Analytics Pipeline:** Genera las métricas finales.

## 4. El concepto de "Data Lineage" (Trazabilidad)
Es saber de dónde viene un dato. Si un dashboard muestra un número erróneo, el pipeline debe permitirte rastrear ese número hasta el registro original de la API de origen.

## 5. Tip Senior: Despliegue de Pipelines
Trata tus pipelines como código. Deben tener tests unitarios, estar en Git y desplegarse mediante CI/CD. Un pipeline escrito "a mano" en un servidor es una bomba de relojería.

## Resumen: Automatización Total
Un pipeline exitoso es aquel que no requiere intervención humana. Una vez diseñado, configurado y desplegado, debe funcionar de forma silenciosa e incansable 24/7.
