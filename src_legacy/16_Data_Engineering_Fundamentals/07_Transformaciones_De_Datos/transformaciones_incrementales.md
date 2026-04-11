# Transformaciones Incrementales: Escalabilidad Real

Si tu base de datos tiene 10.000 millones de registros, no puedes transformarla entera cada día. Las **Transformaciones Incrementales** solo procesan el dato nuevo, ahorrando tiempo y miles de euros en la nube.

## 1. El concepto: Solo el Delta
En lugar de `INSERT OVERWRITE` (borrar y escribir todo), usamos lógicas que detectan qué ha cambiado.

## 2. Estrategias de Detección
- **High-Watermark:** Guardas en una tabla de control cuál fue el último `updated_at` que procesaste. La siguiente vez lanzas: `SELECT * FROM source WHERE updated_at > :last_watermark`.
- **Source Partitioning:** Si la fuente está guardada por carpetas de fecha, tu proceso solo lee la carpeta de hoy.

## 3. Merge y Upsert
Cuando el dato llega al destino, puede que sea un registro nuevo o una actualización de uno viejo.
- **MERGE (SQL):** "Si el ID coincide, actualiza; si no existe, inserta". Es la forma más limpia de mantener la integridad en transformaciones incrementales.

## 4. dbt Incremental Models
dbt facilita esto enormemente con su materialización `incremental`.
```sql
{{ config(materialized='incremental') }}

select * from {{ ref('raw_data') }}
{% if is_incremental() %}
  where event_time > (select max(event_time) from {{ this }})
{% endif %}
```

## 5. El peligro: Datos que cambian en el pasado
¿Qué pasa si un pedido de hace 3 días se cancela hoy? Tu proceso incremental (que solo mira "hoy") no verá ese cambio.
- **Solución:** Re-procesar una ventana de seguridad (ej: los últimos 7 días) en cada ejecución, o usar CDC para detectar cualquier cambio sin importar la fecha.

## Resumen: Eficiencia por diseño
Las transformaciones incrementales son lo que permite que una Startup pueda manejar volúmenes de datos de una multinacional con un presupuesto ajustado. Es la marca de un ingeniero de datos que entiende la economía de la computación.
