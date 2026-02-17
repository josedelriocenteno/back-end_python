# Vistas Materializadas: Cacheo Selectivo en la DB

En aplicaciones con grandes volúmenes de datos, a veces una query con muchas agregaciones (`SUM`, `AVG`, `COUNT`) tarda demasiado tiempo para ser ejecutada en tiempo real cada vez que un usuario accede a un dashboard. Las **Vistas Materializadas** son la solución profesional a este problema.

## 1. ¿Qué es una Vista Materializada?

A diferencia de una vista normal (que es solo un alias para una query), una vista materializada **guarda el resultado del cálculo en el disco**. 

*   Es como una tabla física que se genera a partir de una consulta.
*   **Ventaja:** Las lecturas son instantáneas.
*   **Desventaja:** Los datos no se actualizan automáticamente cuando cambia la tabla origen. Debes "refrescarlas".

## 2. Creación y Uso

```sql
CREATE MATERIALIZED VIEW sales_summary_monthly AS
SELECT 
    DATE_TRUNC('month', created_at) as month,
    product_id,
    SUM(total_amount) as total_revenue,
    COUNT(*) as total_orders
FROM orders
GROUP BY 1, 2;
```

Ahora puedes consultar `sales_summary_monthly` como si fuera una tabla normal, y será extremadamente rápida porque los datos ya están calculados y guardados.

## 3. Refresco de Datos

Como los datos están en disco, si entran nuevas órdenes, la vista se queda obsoleta. Debes ejecutar:

```sql
REFRESH MATERIALIZED VIEW sales_summary_monthly;
```

### Refresco sin Bloqueo (CONCURRENTLY)
Por defecto, `REFRESH` bloquea las lecturas a la vista. Para evitarlo en producción:
1.  La vista debe tener al menos un índice único.
    ```sql
    CREATE UNIQUE INDEX idx_sales_summary_month_prod ON sales_summary_monthly (month, product_id);
    ```
2.  Refresca concurrentemente:
    ```sql
    REFRESH MATERIALIZED VIEW CONCURRENTLY sales_summary_monthly;
    ```

## 4. Cuándo usarlas en Backend

1.  **Dashboards de Admin:** Reportes que no necesitan ser exactos al segundo (ej: ventas del mes).
2.  **Sistemas de Recomendación Simples:** Precalculas afinidades entre usuarios/productos una vez al día.
3.  **Búsquedas Complejas:** Si unir 10 tablas para un perfil de usuario es lento, materializa el perfil completo en una sola fila periódicamente.

## 5. Estrategia desde Python

Puedes usar un worker de background (como Celery) para refrescar tus vistas críticas cada X tiempo:

```python
# Tarea de Celery cada 10 minutos
def refresh_db_cache():
    with engine.connect() as conn:
        conn.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY my_view"))
```

## Resumen: Rendimiento vs Frescura

Las vistas materializadas son una de las herramientas más potentes de PostgreSQL para escalar lecturas pesadas. Son el paso intermedio perfecto antes de saltar a soluciones más complejas como Redis para cacheo.
