# Errores de Rendimiento: Anti-patrones Comunes

En el desarrollo Backend, es fácil escribir SQL que funciona pero que "explota" cuando la base de datos crece a miles o millones de registros. Estos son los errores más comunes y cómo evitarlos.

## 1. El SELECT * (Pecado Capital)
*   **Error:** Traer todas las columnas cuando solo necesitas dos.
*   **Impacto:** Sobrecarga la red, consume memoria extra en Python y evita que Postgres use "Index Only Scans".
*   **Solución:** Especifica siempre las columnas: `SELECT id, email FROM users...`.

## 2. N+1 Queries (El Fantasma del ORM)
*   **Error:** Consultar un objeto y luego hacer una query por cada uno de sus hijos en un bucle.
*   **Código Python (Malo):**
    ```python
    users = session.query(User).all()
    for user in users:
        print(user.roles) # Esto lanza una query extra por cada usuario
    ```
*   **Impacto:** 100 usuarios = 101 queries. Latencia inaceptable.
*   **Solución:** Usa `eager loading` (JOINs) en tu ORM.

## 3. Funciones en el WHERE
*   **Error:** Aplicar funciones a la columna indexada.
*   **Malo:** `WHERE DATE(created_at) = '2023-01-01'`
*   **Impacto:** Invalida el índice B-Tree (Postgres tiene que hacer Seq Scan).
*   **Solución:** Filtra por rango: `WHERE created_at >= '2023-01-01 00:00:00' AND created_at <= '2023-01-01 23:59:59'`.

## 4. El "Like" al principio
*   **Error:** Búsquedas con comodín al inicio: `WHERE name LIKE '%apple'`.
*   **Impacto:** Los índices B-Tree no sirven para buscar por el final del string. Seq Scan obligatorio.
*   **Solución:** Evítalo si puedes o usa extensiones como `pg_trgm` con índices `GIN`.

## 5. Falta de Foreign Keys e Índices en Ellas
*   **Error:** No crear un índice en la columna de la Foreign Key.
*   **Impacto:** Cada vez que borras o actualizas un registro padre, Postgres tiene que escanear la tabla hija para comprobar la integridad. Los JOINs también se vuelven lentos.
*   **Solución:** Por regla general, **toda FK debería tener un índice**.

## 6. OFFSET Masivo para Paginación
*   **Error:** Usar `OFFSET 1000000 LIMIT 10`.
*   **Impacto:** Postgres tiene que calcular y descartar el millón de filas antes de devolverte las 10 que quieres. 
*   **Solución:** Usa "Keyset Pagination" (Filtra por el ID de la última fila vista): `WHERE id > last_seen_id ORDER BY id LIMIT 10`.

## 7. No Usar Tipos de Datos Correctos
*   **Error:** Guardar UUIDs o IPs como TEXT.
*   **Impacto:** Consultas más lentas, comparaciones más pesadas y más espacio en disco.
*   **Solución:** Usa los tipos nativos de Postgres (`UUID`, `INET`, `JSONB`).

## Resumen: La Mentalidad "Scale-First"

1.  **Mide siempre:** Usa `EXPLAIN ANALYZE` en desarrollo con datos realistas.
2.  **Limita los resultados:** Casi nunca necesitas traer más de 100-500 registros a la vez en una API.
3.  **ORM con cuidado:** El ORM es una conveniencia, no una excusa para ignorar cómo funciona SQL.
4.  **Índices con cabeza:** No indexas por si acaso, indexa lo que necesitas.
