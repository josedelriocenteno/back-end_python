# Errores Típicos en el Acceso a Datos

Incluso con los mejores drivers y ORMs, es fácil cometer errores que degradan el rendimiento, comprometen la seguridad o corrompen los datos. Aquí están los anti-patrones más comunes en la integración Python-SQL.

## 1. No cerrar conexiones (Leaks)
*   **Problema:** Crear conexiones y no cerrarlas (vía `close()` o context managers).
*   **Consecuencia:** El servidor de base de datos alcanza su límite de conexiones (`max_connections`) y la app deja de responder.
*   **Solución:** Usa SIEMPRE `with` blocks o un gestor de pooling que controle el ciclo de vida.

## 2. El problema N+1 (El asesino silencioso)
*   **Problema:** Traer una lista de padres y luego consultar sus hijos uno por uno en un loop.
*   **Consecuencia:** Si tienes 100 usuarios y quieres sus posts, haces 101 queries. Latencia inaceptable.
*   **Solución:** Usa `JOINs` (SQL) o `Eager Loading` (ORM) para traer todo en una o dos queries.

## 3. Lógica de negocio en la base de datos (Exceso de lógica)
*   **Problema:** Abusar de Triggers o Stored Procedures para reglas de negocio complejas que cambian frecuentemente.
*   **Consecuencia:** Difícil de testear, difícil de debuguear (no sale en los logs de Python) y difícil de versionar con Git.
*   **Solución:** Mantén la integridad en la DB (Constraints), pero la lógica de negocio en servicios Python.

## 4. Lógica de integridad en el código (Falta de integridad)
*   **Problema:** Intentar validar unicidad o claves foráneas solo en Python.
*   **Consecuencia:** Las condiciones de carrera (Race Conditions) permitirán que entren datos corruptos.
*   **Solución:** Deja que la base de datos sea el "árbitro final" con `UNIQUE` y `FOREIGN KEY` constraints.

## 5. Fetchall masivo (OOM Errors)
*   **Problema:** Ejecutar `SELECT * FROM massive_table` y llamar a `.fetchall()`.
*   **Consecuencia:** Python intenta cargar 10 GB de datos en 2 GB de RAM. `MemoryError`.
*   **Solución:** Usa cursores de servidor (server-side cursors) o procesa en lotes (chunks).

## 6. Ignorar el Pooling
*   **Problema:** Abrir una conexión TCP nueva por cada request de usuario.
*   **Consecuencia:** El handshake de TCP + autenticación de Postgres añade ~50-100ms a cada petición. Tu app se siente lenta "porque sí".
*   **Solución:** Usa un Connection Pooler (como `psycopg-pool` o `SQLAlchemy QueuePool`).

## 7. Acoplamiento al ORM
*   **Problema:** Importar modelos de la DB en todas partes y usarlos como objetos de transferencia de datos (DTO).
*   **Consecuencia:** Un cambio en la tabla rompe toda la aplicación, incluyendo capas de presentación que no deberían saber nada de SQL.
*   **Solución:** Usa Pydantic o Dataclasses para mover datos entre capas.

## Resumen: La Ley de Fugas y Bloqueos

El acceso a datos es un juego de equilibrio entre **red**, **memoria** y **CPU**. Entender estos anti-patrones te permitirá escribir código que no solo funcione hoy, sino que siga funcionando cuando tu base de datos tenga millones de registros.
