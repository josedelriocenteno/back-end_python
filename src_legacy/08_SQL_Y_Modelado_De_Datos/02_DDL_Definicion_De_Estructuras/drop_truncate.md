# DDL: DROP y TRUNCATE - El Fin del Camino para los Datos

En el ciclo de vida de una base de datos, borrar estructuras es tan común como crearlas, pero el riesgo es infinitamente mayor. Un comando de una línea puede destruir meses de datos si no se entiende la diferencia entre `DROP` y `TRUNCATE`.

## 1. DROP TABLE: Borrado Estructural

El comando `DROP` elimina la tabla por completo: sus datos, sus índices, sus privilegios y su propia existencia en el esquema.

```sql
DROP TABLE users;
```

### Comportamiento Profesional:
*   **IF EXISTS:** Para evitar que tus scripts de migración o CI/CD fallen si la tabla no existe.
    ```sql
    DROP TABLE IF EXISTS old_logs;
    ```
*   **CASCADE:** Si la tabla es referenciada por otras (Foreign Keys), Postgres impedirá el borrado a menos que uses `CASCADE`.
    ```sql
    -- ¡CUIDADO! Esto borrará también las tablas que dependan de 'users'
    DROP TABLE users CASCADE;
    ```

## 2. TRUNCATE: Limpieza de Datos Masiva

`TRUNCATE` es el "botón de reset" para los datos de una tabla, pero manteniendo la estructura intacta.

```sql
TRUNCATE TABLE logs;
```

### ¿Por qué TRUNCATE y no DELETE?
A diferencia de `DELETE FROM table;`, `TRUNCATE`:
1.  **Es mucho más rápido:** No escanea las filas una a una, simplemente desasigna las páginas de datos.
2.  **No genera tanto WAL:** Consume mucho menos espacio en log de transacciones.
3.  **Libera espacio en disco:** `DELETE` suele dejar "huecos" (bloat) que requieren un `VACUUM` posterior. `TRUNCATE` devuelve el espacio al SO inmediatamente.

### Opciones de TRUNCATE:
```sql
-- Reinicia los contadores (SERIAL/IDENTITY) a 1
TRUNCATE TABLE users RESTART IDENTITY;

-- Limpia varias tablas a la vez y sus descendientes
TRUNCATE TABLE users, orders CASCADE;
```

## 3. Comparativa Crítica: DROP vs TRUNCATE vs DELETE

| Característica | DROP | TRUNCATE | DELETE |
| :--- | :--- | :--- | :--- |
| **Nivel** | Estructura (DDL) | Datos (DDL/DML*) | Datos (DML) |
| **Velocidad** | Instantáneo | Muy Rápido | Lento (fila a fila) |
| **Mantiene Estructura** | No | Sí | Sí |
| **Reinicia IDs** | N/A | Opcional | No |
| **Rollback** | Sí (en Postgres) | Sí (en Postgres) | Sí |
| **Dispara Triggers** | No | No (normalmente) | Sí |

> [!IMPORTANT]
> En PostgreSQL, tanto `DROP` como `TRUNCATE` son **transaccionales**. Esto significa que si los ejecutas dentro de un `BEGIN; ... ROLLBACK;`, los datos/tablas se recuperan. Esto **NO** ocurre así en otras bases de datos como MySQL u Oracle.

## 4. Mejores Prácticas en Backend

1.  **Nunca manual en Prod:** El borrado de tablas debe estar siempre en un archivo de migración (`Alembic/Django`).
2.  **Tablas Temporales:** Usa `TRUNCATE` en tus suites de tests para limpiar la base de datos entre pruebas; es infinitamente más rápido que borrar y recrear.
3.  **Auditoría:** Antes de un `DROP` o `TRUNCATE` masivo en producción, considera renombrar la tabla (`ALTER TABLE name RENAME TO name_old_date`) por unos días antes de borrarla definitivamente. Es el "seguro de vida" del DB Admin.
4.  **Soft Delete:** En aplicaciones backend modernas, rara vez usamos `DROP` o `DELETE` real sobre datos de usuario. Solemos usar una columna `is_deleted` o `deleted_at`. El espacio es barato, los datos no.
