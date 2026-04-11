# Migraciones de Base de Datos en Docker

Los scripts de `init.sql` solo corren la primera vez. Para los cambios posteriores (añadir una columna, cambiar un tipo de dato), necesitamos un sistema de migraciones (como **Alembic** para SQLAlchemy).

## 1. El reto: ¿Quién corre la migración?
Tienes dos opciones principales en una arquitectura dockerizada:

### Opción A: El contenedor de la API al arrancar
Modificas el comando de arranque de tu API para que primero migre y luego arranque.
```bash
# CMD en el Dockerfile
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0"]
```
- **Pro:** Siempre estás actualizado.
- **Contra:** Si tienes 10 workers de la API, 10 procesos intentarán migrar la DB a la vez (peligroso!).

### Opción B: Un contenedor independiente de "Setup"
Un servicio en el `docker-compose.yml` que corre y se muere.
```yaml
migration-task:
  build: .
  command: alembic upgrade head
  depends_on:
    - db
```
- **Pro:** Más limpio y seguro. Controlas exactamente cuándo ocurre la migración.

## 2. Espera a la DB (Wait-for-it)
Incluso con `depends_on`, la DB puede tardar unos segundos en estar "lista" internamente.
- **Solución:** Usa scripts como `wait-for-it.sh` o el healthcheck de Docker para asegurar que el comando de migración no falle por falta de conexión al milisegundo 1.

## 3. Persistencia de los archivos de migración
Asegúrate de que la carpeta `migrations/` se mapee como un Bind Mount en desarrollo para que cuando generes una nueva migración (`alembic revision --autogenerate`), el archivo se guarde en tu ordenador real y no desaparezca al cerrar Docker.

## Resumen: Evolución Controlada
La base de datos no es estática. Integrar el sistema de migraciones en tu flujo de Docker garantiza que todos los desarrolladores y todos los servidores (Staging, Prod) tengan exactamente el mismo esquema de datos sin intervención manual.
