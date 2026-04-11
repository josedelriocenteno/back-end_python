# PostgreSQL en Docker: Configuración Profesional

Correr una base de datos en un contenedor es sencillo, pero hacerlo de forma robusta para producción requiere cuidar varios detalles.

## 1. La Imagen Base
Usa siempre la versión específica y busca la variante `alpine` para ahorrar espacio.
```yaml
image: postgres:15-alpine
```

## 2. Variables obligatorias
PostgreSQL necesita estas tres variables para arrancar correctamente por primera vez:
- `POSTGRES_DB`: El nombre de la base de datos inicial.
- `POSTGRES_USER`: El usuario administrador.
- `POSTGRES_PASSWORD`: La contraseña (usa siempre secretos o archivos `.env`).

## 3. Persistencia de Datos
Si no montas un volumen en `/var/lib/postgresql/data`, tus datos desaparecerán cada vez que borres el contenedor. Usa siempre **Named Volumes** para mayor rendimiento.

## 4. El punto de entrada `/docker-entrypoint-initdb.d/`
Cualquier archivo `.sql` o `.sh` que metas en esta carpeta del contenedor se ejecutará **automáticamente** la primera vez que la base de datos se cree.

## 5. El Healthcheck (Crucial para Compose)
Define un healthcheck para que otros servicios (como tu API) no intenten conectarse antes de que la DB esté realmente lista para recibir conexiones.
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U user -d db"]
  interval: 5s
  timeout: 5s
  retries: 5
```

## 6. Configuración de PostgreSQL (`postgresql.conf`)
Si necesitas tunear parámetros avanzados (como `max_connections` o `shared_buffers`):
- Puedes sobreescribir el comando de arranque: 
  `command: postgres -c 'max_connections=200'`
- O mapear tu propio archivo de configuración: 
  `-v ./my-postgres.conf:/etc/postgresql/postgresql.conf`

## Resumen: Una roca en el contenedor
Una base de datos dockerizada es predecible y fácil de replicar. Configura bien los volúmenes, los secretos y el healthcheck para que tu infraestructura de datos sea sólida desde el primer día.
