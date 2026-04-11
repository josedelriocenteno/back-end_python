# El Ecosistema Modern Data Stack (MDS)

Más allá de Spark y Kafka, existe una explosión de herramientas SaaS que buscan simplificar cada paso de la ingeniería de datos. Esto es lo que se conoce como el **Modern Data Stack**.

## 1. Ingesta (Fivetran / Airbyte)
Herramientas "No-Code" que conectan cientos de APIs (Facebook, Salesforce, etc) con tu Warehouse con solo unos clicks. Eliminan la necesidad de escribir scripts de extracción manuales.

## 2. Warehouse (Snowflake / BigQuery)
La pieza central donde todo se almacena y transforma vía SQL.

## 3. Transformación (dbt)
El estándar para modelar los datos dentro del Warehouse.

## 4. Observabilidad (Great Expectations / Monte Carlo)
Herramientas que monitorizan la calidad y avisan si los datos "parecen raros", incluso si los pipelines no han dado error técnico.

## 5. Reverse ETL (Census / Hightouch)
Mover el dato modelado **desde** el Warehouse de vuelta a las herramientas de negocio (ej: enviar un segmento de "clientes VIP" a Salesforce para que el equipo de ventas los llame).

## 6. La paradoja de la herramienta
- **Junior:** Quiere aprender todas las herramientas.
- **Senior:** Entiende los conceptos (Idempotencia, Calidad, Particionado) y sabe que puede aplicarlos con cualquier herramienta, sea código puro o un SaaS de pago.

## Resumen: Flexibilidad y Enfoque
El Modern Data Stack permite montar una infraestructura de datos potente en días en lugar de meses. El reto del ingeniero hoy no es solo programar, sino saber elegir la combinación de herramientas más eficiente para su empresa.
