# Pipeline End-to-End: De Ingestión a Analytics

Vamos a ver un caso real completo: **"Analizar el comportamiento de compra de una web de E-commerce".**

## Paso 1: El Evento (Ingesta)
Cada vez que un usuario hace "click" en comprar, la web envía un JSON a un tópico de **Cloud Pub/Sub**.
- *Dato:* `{"user_id": 123, "item": "Libro", "price": 20.0, "timestamp": "2024-03-15T12:00:00Z"}`

## Paso 2: Procesamiento en Tiempo Real (Transformación)
Una **Cloud Function** (o Dataflow si hay mucho volumen) se suscribe al tópico de Pub/Sub.
- Recibe el JSON.
- Valida que el `price` sea positivo.
- Añade el campo `region='EU'`.
- Guarda el resultado en un archivo Parquet en **Cloud Storage**.

## Paso 3: Carga al Warehouse (Carga)
Cada 15 minutos, un proceso programado en **Cloud Scheduler** dispara una carga desde el bucket de GCS hacia una tabla de **BigQuery** llamada `raw_orders`.

## Paso 4: Modelado de Negocio (Analítica)
Dentro de **BigQuery**, ejecutamos una query (o un modelo de dbt) que:
- Une la tabla `raw_orders` con la tabla `customers` (que ya estaba ahí).
- Crea una tabla final llamada `daily_sales_by_region`.
- Esta tabla está **particionada por día** para que sea rápida de consultar.

## Paso 5: Visualización (Consumo)
El analista de negocio abre **Looker Studio**, conecta con la tabla `daily_sales_by_region` y ve un gráfico de barras con las ventas de hoy frente a las de ayer.

## Paso 6: Operaciones
- **Logs:** Todo el flujo escribe en **Cloud Logging**.
- **Alertas:** Si la Cloud Function del Paso 2 falla, recibes un email de **Cloud Monitoring**.

## Resumen: La Tubería Completa
Este es el trabajo real de un Data Engineer. No es solo programar en Python, es conectar servicios de forma que el dato fluya de forma autónoma, segura y verificable desde el click del usuario hasta el gráfico del jefe.
