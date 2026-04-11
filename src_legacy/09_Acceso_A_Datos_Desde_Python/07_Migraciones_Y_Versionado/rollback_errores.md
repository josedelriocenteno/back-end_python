# Rollback de Errores: Qué hacer cuando explota

Un rollback es tu paracaídas. Si una migración falla o corrompe datos, debes saber cómo volver al estado anterior en segundos.

## 1. El comando Downgrade

Alembic permite volver atrás una o varias versiones.
```bash
# Volver a la versión inmediatamente anterior
alembic downgrade -1

# Volver a un ID de revisión específico
alembic downgrade 7de1a2b3c4d5

# Volver al inicio (borra todo el esquema)
alembic downgrade base
```

## 2. Por qué fallan los Rollbacks

1.  **Downgrade no definido:** El desarrollador dejó `pass` en la función `downgrade()`. (Pecado capital).
2.  **Migración Destructiva:** Si el upgrade hizo un `DROP TABLE`, el downgrade la creará vacía. Los datos se perdieron.
3.  **Inconsistencia de Datos:** La migración falló a la mitad y la base de datos está en un estado híbrido.

## 3. Transacciones en Migraciones

Alembic, por defecto, intenta envolver cada migración en una transacción de base de datos. 
*   **Si falla el upgrade:** La transacción se deshace (Rollback de SQL) y la tabla `alembic_version` no se actualiza. Tu DB sigue sana.
*   **Cuidado con MySQL:** Algunas bases de datos (como MySQL) no soportan transacciones en comandos DDL. ¡En Postgres esto no es un problema!

## 4. Reparando la Tabla de Versiones (`stamp`)

A veces la DB está correcta pero el puntero de Alembic se ha perdido.
*   **Comando `stamp`:** "Sella" la base de datos en una versión específica sin ejecutar ningún SQL.
*   `alembic stamp head` -> Marca la DB como si estuviera en la última versión.

## 5. El plan de desastre (DR)

Si el downgrade de Alembic falla en producción:
1.  **Restaurar el Backup:** Es la opción más lenta pero la más segura si hubo pérdida de datos.
2.  **Hotfix Manual:** Entrar vía `psql`, arreglar la tabla manualmente y luego hacer un `alembic stamp` para que Alembic crea que todo está bien.

## Resumen: La Responsabilidad del Downgrade

Escribir el `upgrade` es solo la mitad del trabajo. Un desarrollador backend profesional dedica el mismo tiempo a asegurar que su `downgrade` deja la base de datos exactamente como estaba, ahorrando crisis innecesarias al equipo de SRE.
