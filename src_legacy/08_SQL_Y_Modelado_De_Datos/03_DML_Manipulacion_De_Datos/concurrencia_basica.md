# Concurrencia Básica: Locks y Conflictos en SQL

En un backend moderno, no eres el único usuario de la base de datos. Tienes múltiples instancias de tu API, workers de Celery, procesos de BI y quizás otras aplicaciones accediendo a los mismos datos simultáneamente. Esto es **Concurrencia**.

## 1. El Problema: Race Conditions

Imagina que dos usuarios intentan comprar el último item en stock al mismo tiempo:
1.  **API 1 (Usuario A):** Lee stock = 1.
2.  **API 2 (Usuario B):** Lee stock = 1.
3.  **API 1:** Actualiza stock = 0 y confirma compra.
4.  **API 2:** Actualiza stock = 0 y confirma compra.
**Resultado:** Has vendido dos veces algo que solo tenías una vez. Mal negocio.

## 2. Locks (Bloqueos) de Fila

Para evitar esto, Postgres usa bloqueos. Cuando haces un `UPDATE` o `DELETE`, Postgres bloquea esa fila hasta que hagas `COMMIT` o `ROLLBACK`.

### SELECT FOR UPDATE (Bloqueo Pesimista)
Esta es la herramienta fundamental para el desarrollador Backend. Le dices a la DB: "Voy a leer esta fila y pienso actualizarla, así que no dejes que nadie más la toque".

```sql
BEGIN;
    -- Bloquea la fila del producto 101
    SELECT stock FROM products 
    WHERE id = 101 
    FOR UPDATE;

    -- Aquí haces tu lógica en Python: if stock > 0...
    
    UPDATE products SET stock = stock - 1 WHERE id = 101;
COMMIT; -- Al hacer COMMIT, se libera el bloqueo
```

## 3. Tipos de Bloqueos Comunes

| Nivel | Tipo | Descripción |
| :--- | :--- | :--- |
| **Row** | `FOR UPDATE` | El más común. Nadie puede modificar la fila hasta que termines. |
| **Row** | `FOR SHARE` | Otros pueden leer (`SELECT`), pero nadie puede modificar. |
| **Table** | `ACCESS EXCLUSIVE` | Bloqueo total de tabla (ej: al hacer un `ALTER TABLE`). Nadie puede ni leer ni escribir. |

## 4. Deadlocks (Puntos Muertos)

Ocurre cuando dos transacciones se bloquean mutuamente esperando que la otra suelte un recurso.

**Ejemplo de Deadlock:**
1.  Trx A bloquea Fila 1.
2.  Trx B bloquea Fila 2.
3.  Trx A intenta bloquear Fila 2 (espera a Trx B).
4.  Trx B intenta bloquear Fila 1 (espera a Trx A).
**Resultado:** Ambas esperan para siempre. Postgres detecta esto y mata a una de las dos transacciones con un error descriptivo.

### Cómo evitar Deadlocks:
*   **Orden de Actualización:** Asegúrate de que todas tus funciones actualicen las tablas siempre en el mismo orden (ej: siempre primero `users` y luego `orders`).
*   **Transacciones Cortas:** Cuanto menos tiempo retengas un bloqueo, menos probabilidad de conflicto.

## 5. Optimistic Locking (Bloqueo Optimista)

A veces no queremos bloquear la fila (porque es muy lento o hay poca colisión). En su lugar, usamos una columna `version`.

1.  Lees la fila: `SELECT id, name, version FROM users WHERE id = 1;` (Obtienes version=5).
2.  Intentas actualizar solo si la versión no ha cambiado:
```sql
UPDATE users 
SET name = 'New Name', version = version + 1 
WHERE id = 1 AND version = 5;
```
En Python, compruebas si se actualizó alguna fila. Si `rowcount == 0`, alguien se te adelantó y debes reintentar o avisar al usuario.

## 6. Resumen para Performance Backend

1.  **Observabilidad:** Monitorea bloqueos largos. Una transacción "colgada" en Python puede congelar partes críticas de tu DB.
2.  **SKIP LOCKED:** Una función genial de Postgres para sistemas de colas (workers).
    ```sql
    -- Coge la primera tarea disponible que no esté bloqueada por otro worker
    SELECT * FROM tasks 
    WHERE status = 'pending' 
    LIMIT 1 
    FOR UPDATE SKIP LOCKED;
    ```
3.  **No bloquees por leer:** Por defecto, Postgres permite lecturas concurrentes sin esperas (`MVCC`), úsalo a tu favor.
