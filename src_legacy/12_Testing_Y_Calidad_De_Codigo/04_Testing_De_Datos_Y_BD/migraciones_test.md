# Testing de Migraciones de Base de Datos

Uno de los momentos más peligrosos en la vida de una App es cuando ejecutas `alembic upgrade head` en producción. ¿Cómo podemos estar seguros de que la migración no va a corromper los datos o bloquear las tablas?

## 1. El Test de "Ida y Vuelta" (Up/Down Test)
Cada vez que crees una migración, deberías correr un test automatizado que haga:
1. `alembic upgrade +1` (Aplica el cambio).
2. `alembic downgrade -1` (Revierte el cambio).
3. `alembic upgrade +1` (Vuelve a aplicar).
Si este ciclo falla, tu migración está mal escrita y fallará en producción ante un rollback.

## 2. Testear con Datos Reales (Pre-migration data)
El esquema puede ser correcto, pero ¿qué pasa si añades una columna `NOT NULL` a una tabla que ya tiene un millón de filas?
- **El Test:**
    1. Tenemos la DB en la versión N.
    2. Insertamos datos de ejemplo.
    3. Corremos la migración a la versión N+1.
    4. Verificamos que los datos siguen ahí y que la nueva columna tiene un valor por defecto coherente.

## 3. Detección de Bloqueos (Locking)
Algunas migraciones (como cambiar el tipo de una columna) bloquean la tabla entera en Postgres. Si la tabla es grande, esto significa caída del servicio.
- **Estrategia Senior:** Usa herramientas como `strong_migrations` (en Ruby) o scripts de chequeo que analicen el SQL generado por Alembic buscando operaciones peligrosas.

## 4. Migraciones "Offline" vs "Online"
- **Offline:** Requieren parar la App.
- **Online (Zero-downtime):** Permiten que la App siga corriendo mientras se migra. Esto requiere pasos intermedios (ej: añadir columna -> poblar datos -> hacerla obligatoria). Testear estos pasos es vital para sistemas de alta disponibilidad.

## 5. El archivo `env.py` de Alembic
En tus tests, puedes configurar Alembic para usar la misma `engine` de SQLite o Docker que tus otros tests, asegurando que el esquema que testeas es exactamente el que define tu código.

## Resumen: La integridad es sagrada
Testear las migraciones evita el peor de los miedos del desarrollador: la pérdida de datos. No te limites a ver si las tablas se crean; asegúrate de que el camino de evolución de los datos es seguro y reversible.
