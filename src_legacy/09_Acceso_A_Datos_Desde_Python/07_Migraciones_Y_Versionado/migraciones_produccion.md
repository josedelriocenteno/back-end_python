# Migraciones en Producción: La Guía de Supervivencia

Lanzar `alembic upgrade head` en local es fácil. En producción, con millones de usuarios conectados, es una operación de alto riesgo.

## 1. El Bloqueo del Esquema (DDL Locks)

Cuando haces un `ALTER TABLE`, Postgres bloquea la tabla para cualquier lectura o escritura.
*   **Problema:** Si tienes una query de lectura muy larga corriendo, la migración esperará a que termine, y mientras tanto, TODAS las demás peticiones se encolarán detrás de la migración.
*   **Solución:** Configura un `lock_timeout`.
    ```sql
    SET lock_timeout = '2s';
    ```

## 2. Migraciones que NO bloquean (Zero Downtime)

### A. Añadir una columna
Añadir una columna `nullable` es casi instantáneo.
*   **Pro Tip:** No añadas columnas con un valor por defecto (`DEFAULT 'xyz'`) en tablas de millones de filas si usas Postgres < 11, ya que reescribirá toda la tabla.

### B. Crear Índices
Nunca uses `CREATE INDEX` en producción. Usa `CREATE INDEX CONCURRENTLY`. En Alembic se configura así:
```python
op.create_index('idx_name', 'table_name', ['col'], postgresql_concurrently=True)
```
*   *Nota:* Las migraciones concurrentes no pueden ejecutarse dentro de una transacción. Debes poner `render_as_batch=True` en `env.py`.

## 3. El Flujo de Despliegue (Blue/Green)

Para evitar romper la app cuando cambias la DB:
1.  **Paso 1:** Despliega la migración que AÑADE la columna (la app antigua simplemente la ignora).
2.  **Paso 2:** Despliega el nuevo código Python que usa la columna.
3.  **Paso 3 (Opcional):** Si era un renombrado, borra la columna vieja en una migración futura.

## 4. Auditoría antes de aplicar

Usa el modo "off-line" para generar el SQL y dárselo a un DBA o revisarlo tú mismo antes de ejecutar nada:
`alembic upgrade head --sql > script.sql`

## 5. Checklist para el Senior Developer

1.  [ ] ¿He probado el `downgrade` en mi máquina?
2.  [ ] ¿He revisado si hay alguna operación que bloquee tablas críticas?
3.  [ ] ¿Tengo un backup reciente de la DB antes de lanzar el comando?
4.  [ ] ¿La migración es pequeña o estoy intentando cambiar todo el sistema de una vez?

## Resumen: Pragmatismo en la Evolución

En producción, la estabilidad vale más que la elegancia. Prefiere hacer tres migraciones pequeñas y seguras que una sola "perfecta" que tire el servicio durante 10 minutos.
