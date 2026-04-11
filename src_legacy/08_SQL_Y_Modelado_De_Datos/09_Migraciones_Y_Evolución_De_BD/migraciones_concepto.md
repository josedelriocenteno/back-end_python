# Migraciones: Versionando tu Base de Datos

En el desarrollo Backend profesional, nunca alteramos la base de datos de producción lanzando comandos SQL manuales. Usamos **Migraciones**.

## 1. ¿Qué es una Migración?

Una migración es un archivo (generalmente Python o SQL) que describe un cambio incremental en el esquema de la base de datos. 

*   Es como el "Git para tu base de datos".
*   Permite que todos los desarrolladores del equipo tengan exactamente la misma estructura.
*   Automatiza el despliegue en entornos de Testing, Staging y Producción.

## 2. El Ciclo de Vida de una Migración

1.  **Diseño:** Decides añadir una columna `status` a la tabla `Users`.
2.  **Generación:** Usas una herramienta (Alembic/Django) para crear el archivo de migración.
3.  **Revisión:** Verificas que el SQL generado sea correcto y no bloquee la base de datos.
4.  **Aplicación:** Ejecutas la migración contra la DB. La herramienta marca esa migración como "completada" en una tabla especial (ej: `alembic_version`).

## 3. Estructura de un archivo de migración

Cada migración debe tener dos partes:
*   **Up (Upgrade):** Los cambios que quieres aplicar (ej: `CREATE TABLE`).
*   **Down (Downgrade):** Los cambios necesarios para deshacer lo anterior (ej: `DROP TABLE`). Esto es vital para poder volver atrás si algo falla.

## 4. Por qué NO usar comandos manuales

1.  **Falta de Trazabilidad:** ¿Quién creó esa tabla? ¿Cuándo? ¿Por qué?
2.  **Inconsistencia entre Entornos:** "En mi ordenador funciona, pero en producción falta una columna".
3.  **Riesgo Humano:** Un error tipográfico en un `ALTER TABLE` manual puede ser catastrófico. Las migraciones se prueban en local antes de llegar a producción.

## 5. Herramientas Líderes en Python

*   **Alembic:** El estándar para proyectos con SQLAlchemy. Es extremadamente flexible y potente.
*   **Django Migrations:** Integrado en el framework Django. Muy automatizado y fácil de usar.
*   **Yoyo Migrations:** Una opción más simple basada en SQL puro para proyectos que no usan ORMs pesados.

## Resumen: La Base de Datos es Código

Trata tu esquema de base de datos con el mismo respeto que tu código Python. Versiona cada cambio, revísalo en equipo y automatiza su despliegue. En los siguientes temas veremos cómo usar Alembic y cómo hacer que estas migraciones sean seguras en entornos con millones de registros.
