# Migraciones Seguras: Sobreviviendo a Producción

Aplicar una migración en local con 5 filas es instantáneo. Aplicar la misma migración en producción con 10 millones de filas puede tirar tu aplicación durante horas. Aquí te enseño cómo evitarlo.

## 1. El Peligro del "Access Exclusive Lock"

Casi todas las operaciones DDL (`ALTER TABLE`, `ADD COLUMN`) requieren un bloqueo exclusivo sobre la tabla. 
*   **Problema:** Mientras dure la migración, nadie puede leer ni escribir en esa tabla. Tu API empezará a devolver errores de Timeout.

## 2. Estrategias para Migraciones Seguras

### A. Añadir Columnas con Cuidado
*   Desde Postgres 11, añadir una columna con un `DEFAULT` constante es casi instantáneo. 
*   Si usas una versión anterior, **primero añade la columna sin default** (es rápido) y luego actualiza los datos en pequeños lotes (batches).

### B. Crear Índices de forma Concurrente
Nunca crees un índice normal en una tabla de producción activa.
```sql
-- En Alembic, usa op.create_index(..., postgresql_concurrently=True)
CREATE INDEX CONCURRENTLY idx_name ON table(col);
```

### C. No Validar Constraints Inmediatamente
Si añades una `CHECK constraint` o una `FOREIGN KEY`, Postgres querrá validar todos los datos existentes, bloqueando la tabla.
*   **Solución:** Añádela como `NOT VALID` y valídala después en un proceso separado que no bloquee.

## 3. Backups: Tu Seguro de Vida

Antes de ejecutar `alembic upgrade head` en producción:
1.  **Backup de Datos:** Haz un snapshot de la base de datos.
2.  **Backup de Esquema:** Guarda el SQL de cómo estaba la base de datos antes.

## 4. El "Dry Run" (Simulacro)

Alembic permite generar el SQL que se va a ejecutar sin llegar a ejecutarlo:
```bash
alembic upgrade head --sql > migration_script.sql
```
*   Revisa ese SQL manualmente. Busca palabras clave peligrosas como `DROP` o `REWRITE`.

## 5. Migraciones de Datos vs Migraciones de Esquema

*   **Esquema:** Cambia la estructura (Añadir columna).
*   **Datos:** Cambia el contenido (Poner a todos los usuarios como 'activos').
*   *Backend Tip:* Intenta no mezclarlas. Haz el cambio de esquema en una migración y el cambio de datos en otra (o mejor aún, vía un script de Python independiente o un worker de Celery).

## Resumen para el SRE / Senior Developer

1.  **Horas de Baja Actividad:** Ejecuta las migraciones pesadas cuando haya menos tráfico.
2.  **Transacciones:** Asegúrate de que tu herramienta de migraciones use transacciones para que, si falla a mitad, la DB no se quede en un estado híbrido roto.
3.  **Timeout:** Configura un `lock_timeout` en tu sesión de migración para que falle rápido si no consigue el bloqueo, en lugar de quedarse esperando y bloqueando la cola de otras queries.
