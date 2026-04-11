# Índices Compuestos y Estrategias Avanzadas

Una vez entiendes los índices básicos, el siguiente nivel es saber cómo indexar consultas que involucran múltiples columnas. Aquí es donde se separan los desarrolladores de los ingenieros de backend.

## 1. ¿Qué es un Índice Compuesto?

Es un índice que cubre múltiples columnas en una sola estructura.
```sql
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);
```

### La Regla de Oro: El Orden Importa
El orden de las columnas en el índice (`col1, col2, col3`) es crítico.
*   Postgres puede usar este índice para buscas por `col1`.
*   Postgres puede usarlo para `col1` AND `col2`.
*   **Postgres NO puede usarlo para buscar solo por `col2`** (a menos que use una estrategia lenta de skip scan).

> [!TIP]
> Pon siempre la columna más selectiva (la que filtra más filas) o la que siempre usas en el `=` primero, y las columnas de rango (`<`, `>`) o de ordenación (`ORDER BY`) después.

## 2. Índices de Recubrimiento (Covering Indexes)

Usando la cláusula `INCLUDE`, puedes guardar datos adicionales en el índice que no forman parte de la búsqueda pero sí del resultado.
```sql
CREATE INDEX idx_products_name_price 
ON products(name) 
INCLUDE (price, stock);
```
**Resultado:** Postgres puede responder la query `SELECT name, price, stock FROM products WHERE name = 'Laptop'` leyendo **solo** el índice, sin tocar el disco para leer la tabla (Index Only Scan). Esto es extremadamente rápido.

## 3. Índices GIN y GiST (Para Datos Complejos)

*   **GIN (Generalized Inverted Index):** Ideal para tipos de datos que contienen múltiples valores, como `JSONB` o `ARRAY`.
    ```sql
    -- Acelera búsquedas dentro de JSONB
    CREATE INDEX idx_products_metadata_gin ON products USING GIN (metadata);
    ```
*   **GiST (Generalized Search Tree):** Usado para datos geométricos, búsquedas de texto completo (Full Text Search) o rangos temporales.

## 4. Estrategias de Indexación en Backend

1.  **Index Only Scans:** Intenta que tus consultas críticas lean solo del índice.
2.  **Deduplicación:** En Postgres 13+, los índices B-Tree se comprimen automáticamente si hay valores repetidos, ahorrando mucho espacio.
3.  **CONCURRENTLY:** En producción, crear un índice bloquea la tabla. Usa `CREATE INDEX CONCURRENTLY` para que Postgres lo cree en segundo plano sin detener las escrituras.
    ```sql
    CREATE INDEX CONCURRENTLY idx_huge_table ON massive_data(some_col);
    ```

## 5. El Anti-Patrón: Sobredimensionar

No añadas un índice compuesto para cada combinación de columnas posible en tu WHERE.
*   Postgres puede combinar dos índices simples en tiempo de ejecución (`Bitmap Index Scan`). No siempre necesitas un compuesto.

## Resumen para Performance

*   **Compuesto:** Sigue el orden de izquierdo a derecho.
*   **Covering:** Usa `INCLUDE` para evitar leer la tabla.
*   **JSONB:** Usa `GIN` si tienes muchos metadatos dinámicos.
*   **Producción:** Siempre `CONCURRENTLY`.
*   **Limpieza:** Borra los índices que no se usan (monitoriza `pg_stat_user_indexes`).
