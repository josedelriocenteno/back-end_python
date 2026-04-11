# Cargas Incrementales: Eficiencia en el Movimiento de Datos

En Data Engineering, rara vez volvemos a procesar todos los datos históricos cada día. Para ser eficientes y escalables, usamos **Cargas Incrementales**.

## 1. ¿Qué es una Carga Incremental?

Es un proceso que solo extrae, transforma y carga los datos que han cambiado o se han creado desde la última ejecución exitosa.

*   **Pros:** Menos carga en la DB, menos costes de nube, más velocidad.
*   **Contras:** Requiere una lógica de control más compleja (gestión de "punteros").

## 2. Estrategias de Identificación

¿Cómo sabemos qué datos son "nuevos"?

### A. Basada en Timestamps (Watermarking)
Es la más común. Usamos una columna como `updated_at` o `created_at`.
1.  Buscas el valor máximo en tu tabla de destino: `SELECT MAX(updated_at) FROM target`.
2.  Extraes de la tabla origen: `SELECT * FROM source WHERE updated_at > :last_max_value`.

### B. Basada en IDs Autoincrementales
Si los IDs solo crecen y no hay actualizaciones de registros antiguos.
1.  `SELECT * FROM source WHERE id > :last_processed_id`.

### C. Change Data Capture (CDC)
La base de datos nos avisa de cada cambio (INSERT, UPDATE, DELETE). Es la más avanzada y requiere herramientas como **Debezium**.

## 3. Manejo de Actualizaciones: Delta Load

Cuando un registro antiguo cambia, la carga incremental debe reflejarlo.
*   **Merge / Upsert:** Usamos `ON CONFLICT` (Postgres) para insertar si es nuevo o actualizar si ya existe.
*   **SCD Type 2 (Slowly Changing Dimensions):** Guardamos el historial. En lugar de sobreescribir, creamos una nueva fila con el nuevo valor y una fecha de validez.

## 4. El Problema de los Borrados

Las cargas basadas en timestamps NO detectan si un registro fue borrado físicamente (`DELETE`) en el origen.
*   **Solución 1:** Auditoría de borrados (Trigger que guarda IDs borrados en una tabla aparte).
*   **Solución 2:** Soft Delete (`is_deleted = true`). El "borrado" es una actualización más y será captado por el timestamp.

## 5. Implementación desde Python (Pseudo-código)

```python
def run_incremental_load():
    last_ts = get_last_processed_timestamp()
    
    # Extraer solo lo nuevo
    new_data = db_source.execute(
        "SELECT * FROM orders WHERE updated_at > %s", (last_ts,)
    ).fetchall()
    
    if new_data:
        # Cargar en destino usando UPSERT
        load_to_warehouse(new_data)
        
        # Actualizar el puntero (Estado)
        new_max_ts = max(d['updated_at'] for d in new_data)
        update_checkpoint(new_max_ts)
```

## Resumen: No proceses lo que ya conoces

Las cargas incrementales son la base de los pipelines de datos modernos. Entender cómo gestionar el "estado" de tu carga y cómo manejar los conflictos de datos te permitirá construir sistemas que escalen a terabytes de información sin morir en el intento.
