# Errores Comunes: SQL desde Python

Integrar Python con SQL parece sencillo, pero hay sutiles trampas en las que incluso desarrolladores senior caen. Evitarlas te ahorrará horas de debugging y problemas de rendimiento en producción.

## 1. El Cursor Olvidado (Memory Leak)
*   **Error:** Abrir cursores y no cerrarlos.
*   **Impacto:** Consumo excesivo de memoria en tu servidor y posible límite de cursores abiertos en PostgreSQL.
*   **Solución:** Usa siempre `with conn.cursor() as cur:`.

## 2. Abuso de f-strings (SQL Injection)
*   **Error:** Inyectar variables directamente en el string de SQL.
*   **Malo:** `cur.execute(f"SELECT * FROM users WHERE name = '{name}'")`
*   **Impacto:** Tu base de datos puede ser borrada totalmente con un simple input de usuario malintencionado.
*   **Solución:** Usa marcadores de posición: `cur.execute("... WHERE name = %s", (name,))`.

## 3. Olvidar el COMMIT (The Silent Fail)
*   **Error:** Hacer un `INSERT` o `UPDATE` y ver que "no pasa nada" en la DB.
*   **Causa:** Por defecto, muchas librerías (incluyendo versiones antiguas de psycopg) inician una transacción y esperan a un `.commit()`. Si el script termina sin él, se hace un ROLLBACK silencioso.
*   **Solución:** Usa el context manager `with conn:` que gestiona el commit/rollback por ti.

## 4. Consultas en Bucle (The N+1 Problem)
*   **Error:** Ejecutar una query dentro de un loop `for`.
*   **Impacto:** Miles de viajes de ida y vuelta (round-trips) a la base de datos. Latencia altísima.
*   **Solución:** Usa `JOINs` en tu SQL para traer todos los datos en una sola query o usa `executemany()` para escrituras.

## 5. Convertir todo a Listas en Python
*   **Error:** Hacer `.fetchall()` sobre una tabla de millones de filas.
*   **Impacto:** Python intentará cargar gigabytes de datos en la RAM de tu servidor y probablemente crasheará (OOM - Out of Memory).
*   **Solución:** Itera sobre el cursor directamente (él irá pidiendo platos de datos poco a poco) o usa cursores de servidor para datos masivos.

## 6. Manejo Genérico de Excepciones
*   **Error:** Usar `except Exception:` para errores de SQL.
*   **Impacto:** No sabes por qué falló la query (¿Falta de permisos? ¿Dato inválido? ¿Timeout?).
*   **Solución:** Captura excepciones específicas de Psycopg: `psycopg.errors.UniqueViolation`, `psycopg.errors.ForeignKeyViolation`, etc.

## 7. No Usar un Pool de Conexiones
*   **Error:** Abrir y cerrar una conexión física por cada petición HTTP en tu API.
*   **Impacto:** Abrir una conexión a Postgres es una operación costosa (dar de alta el proceso, autenticar, etc.). Tu API será lenta.
*   **Solución:** Usa un **Connection Pool** (vía Psycopg Pool o SQLAlchemy) para reutilizar conexiones abiertas.

## Resumen: Checklist de Robustez Python-SQL

1.  [ ] ¿Todos mis cursores están dentro de un `with`?
2.  [ ] ¿He eliminado todas las concatenaciones de strings en mis queries?
3.  [ ] ¿Estoy capturando errores específicos de base de datos?
4.  [ ] ¿Estoy usando un Pool de conexiones en mi servidor de aplicaciones?
5.  [ ] ¿Mis queries pesadas usan iteradores en lugar de `.fetchall()`?
