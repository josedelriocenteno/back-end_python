# Migraciones en Aplicaciones API: El Flujo de Trabajo con Alembic

En una aplicación profesional, nunca ejecutas comandos SQL de creación de tablas (`CREATE TABLE`) manualmente en producción. Usamos Alembic para que el esquema de la base de datos evolucione al mismo ritmo que el código.

## 1. El ciclo de desarrollo
1.  **Modificar Modelo:** Añades un campo `bio` a tu clase `User` en SQLAlchemy.
2.  **Generar Migración:** Ejecutas `alembic revision --autogenerate -m "Add bio field"`.
3.  **Revisar Script:** Verificas que el archivo Python creado en la carpeta `alembic/versions` hace lo que esperas.
4.  **Aplicar Local:** Ejecutas `alembic upgrade head` para actualizar tu base de datos de desarrollo.
5.  **Desplegar:** Al hacer merge en la rama principal, el pipeline de CI/CD ejecutará el `upgrade head` en el servidor de producción.

## 2. Integración con FastAPI
En el archivo `main.py`, es común ver que algunos sistemas ejecutan las migraciones al arrancar. Aunque es cómodo para proyectos pequeños, en sistemas grandes preferimos hacerlo antes de arrancar la app para detectar fallos temprano.

## 3. El peligro de 'Base.metadata.create_all()'
Muchos tutoriales de FastAPI enseñan a usar este comando.
*   **Por qué NO usarlo:** Solo crea tablas si no existen. Si añades una columna nueva, `create_all` no hará nada.
*   **Solución:** Borra esa línea tan pronto como instales Alembic.

## 4. Migraciones y Zero-Downtime
Cuando tu API tiene mucho tráfico, no puedes parar el servicio para migrar.
*   **Regla de Oro:** Tus scripts de migración deben ser retro-compatibles.
*   Ejemplo: Si quieres borrar una columna, primero lanza una versión que no la use, y en la siguiente versión de la API, bórrala de la DB.

## 5. Rollbacks en API
Si una migración falla en producción:
1.  Haz rollback de la base de datos: `alembic downgrade -1`.
2.  Haz rollback del código (vuelve a la versión anterior de la imagen Docker).

## Resumen: El historial de ADN de tu DB
Las migraciones son el historial de cómo ha crecido tu sistema. Tratarlas con cuidado y revisarlas antes de aplicarlas es una responsabilidad crítica del desarrollador backend.
