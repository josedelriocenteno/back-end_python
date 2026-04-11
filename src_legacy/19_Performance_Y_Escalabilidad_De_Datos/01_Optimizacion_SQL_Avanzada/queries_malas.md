# Anti-patrones SQL: Lo que NO debes hacer

Incluso con los mejores índices del mundo, una query mal escrita puede destruir el rendimiento de tu base de datos. Estos son los errores más comunes cometidos por desarrolladores junior y senior.

## 1. SELECT *
*   **El problema:** Traes todas las columnas, incluso las de tipo `TEXT` gigante que no necesitas. Aumenta el tráfico de red y el uso de memoria en la base de datos y en tu app.
*   **Solución:** Escribe solo las columnas que vas a usar: `SELECT id, nombre, email...`.

## 2. Funciones en el WHERE (Sargability)
```sql
-- MAL: El motor no puede usar el índice de fecha_nacimiento
SELECT * FROM usuarios WHERE YEAR(fecha_nacimiento) = 1990;

-- BIEN: El motor USA el índice
SELECT * FROM usuarios WHERE fecha_nacimiento >= '1990-01-01' AND fecha_nacimiento <= '1990-12-31';
```
*   **Regla:** Nunca apliques una función a una columna indexada en el `WHERE`.

## 3. El comodín al principio (`LIKE '%abc'`)
*   **El problema:** Los índices B-Tree funcionan de izquierda a derecha. Un `LIKE 'abc%'` usa el índice, pero un `LIKE '%abc'` obliga a un Sequential Scan (leerlo todo).
*   **Solución:** Usa índices `TRIGRAM` o motores de búsqueda como Elasticsearch si necesitas buscar por el final del string.

## 4. El "N+1" Queries (Desde la App)
*   **El problema:** Tu código de Python hace una query para sacar 100 pedidos, y luego hace un bucle y lanza 100 queries individuales para sacar el nombre del cliente de cada pedido.
*   **Solución:** Usa un `JOIN` o un `IN (...)` para traerlo todo en una o dos queries máximo.

## 5. Ordenar por columnas no indexadas
*   **El problema:** `ORDER BY algo_que_no_es_indice` obliga a la base de datos a volcar los datos a disco para ordenarlos (External Sort). Es lentísimo.
*   **Solución:** Indexa la columna por la que sueles ordenar habitualmente.

## 6. No usar LIMIT
*   **El problema:** Lanzar una query que devuelve 1 millón de registros a una aplicación que solo va a mostrar los primeros 20.
*   **Solución:** Usa siempre `LIMIT` y `OFFSET` (paginación) para proteger los recursos.

## Resumen: Limpieza y Eficiencia
Escribir buen SQL es un ejercicio de minimalismo: pide solo lo que necesites, de la forma más directa posible, y permite que el motor use sus índices. Evitar estos anti-patrones es la forma más barata y efectiva de optimizar cualquier sistema de datos.
