# Rollback: Qué hacer cuando todo falla

Un "Rollback" es el proceso de deshacer una migración que ha causado problemas. A pesar de que todos intentamos hacer migraciones perfectas, un ingeniero senior siempre tiene un plan de huida.

## 1. El Método Alembic

Si acabas de ejecutar una migración y ves que la API empieza a fallar:
```bash
alembic downgrade -1
```
*   Esto ejecutará la función `downgrade()` de tu último script.
*   **IMPORTANTE:** Solo funcionará si definiste correctamente el `downgrade`. Si usaste `op.drop_table` en el upgrade, el downgrade debería ser un `op.create_table` con toda la estructura anterior.

## 2. El Peligro de las Migraciones Destructivas

Si tu migración hizo un `DROP COLUMN` o un `DROP TABLE`, el `downgrade` de Alembic recreará la estructura pero **LOS DATOS HABRÁN DESAPARECIDO**. 
*   En este caso, Alembic no puede salvarte. Necesitas restaurar un Backup.

## 3. Estrategias de Retrocompatibilidad (Blue-Green)

Para evitar desastres, usa la estrategia de los dos pasos:
1.  **Paso 1 (Despliegue):** Añade la nueva columna pero mantén la antigua. Tu código Python debe ser capaz de leer de ambas.
2.  **Paso 2 (Limpieza):** Una vez verificado que todo funciona bien con el nuevo código, lanza una segunda migración para borrar lo antiguo.
*   *Ventaja:* Si tienes que volver atrás el código Python, la base de datos sigue siendo compatible.

## 4. Rollbacks de Datos Masivos

Si una migración de datos corrompió registros (ej: puso el precio de todos los productos a 0 por error):
1.  **Para el sistema:** Pon la app en modo mantenimiento.
2.  **Identifica el daño:** Usa los logs o una copia del backup para ver los valores anteriores.
3.  **Script de reparación:** Escribe un script de Python que corrija los datos en lotes pequeños.

## 5. El Factor Humano: "No entres en pánico"

Un error en base de datos es estresante, pero las decisiones tomadas con prisas suelen empeorar la situación (ej: borrar la tabla equivocada intentando arreglar la primera).

1.  **Comunica:** Avisa al equipo y a los usuarios.
2.  **Analiza:** Mira los logs de PostgreSQL.
3.  **Decide:** ¿Downgrade de Alembic o Restaurar Backup completo?

## Resumen: Un Downgrade Bien Probado vale por Dos

Nunca des una migración por terminada si no has probado el `downgrade` en tu entorno de desarrollo. La capacidad de volver atrás es lo que separa a un sistema robusto de uno frágil.
