# Acceso de Mínimo Privilegio en la Base de Datos

Uno de los errores más comunes es que la aplicación backend se conecte a la base de datos usando el usuario `postgres` o `root`. Esto viola el principio de mínimo privilegio de forma flagrante.

## 1. El Peligro del Superusuario
Si tu App usa el usuario `root`:
- Un ataque de SQL Injection exitoso puede borrar toda la instancia de la DB.
- El atacante puede ver datos de otras aplicaciones que compartan el mismo servidor.
- El atacante puede cambiar la configuración del motor de DB para crear puertas traseras.

## 2. La configuración correcta (Separación de Roles)
En un entorno profesional, creamos usuarios de DB con permisos específicos para la App.

### Paso 1: Crear un usuario limitado
```sql
CREATE USER api_user WITH PASSWORD 'password_segura';
```

### Paso 2: Dar permisos solo a las tablas necesarias
```sql
-- Revocar permisos por defecto en el esquema público
REVOKE ALL ON SCHEMA public FROM public;

-- Dar permiso de conexión a la DB
GRANT CONNECT ON DATABASE mi_proyecto_db TO api_user;

-- Dar permisos de lectura/escritura en tablas específicas
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO api_user;

-- Prohibir explícitamente el DELETE si la App no lo necesita
REVOKE DELETE ON ALL TABLES IN SCHEMA public FROM api_user;
```

## 3. Usuarios diferentes para Tareas diferentes
- **App User:** Solo SELECT, INSERT, UPDATE. Es el que usa el API.
- **Migration User:** Permisos para `CREATE TABLE`, `ALTER TABLE`. Solo se usa durante el despliegue de Alembic.
- **Read-only User:** Solo SELECT. Usado por herramientas de analítica o BI para que no puedan romper nada accidentalmente.

## 4. Seguridad de Red (Firewall de DB)
Incluso con el mejor usuario, la base de datos no debe ser accesible desde internet.
- Prohíbe cualquier entrada que no venga de la IP de tu servidor de API.
- Configura Postgres para que solo escuche en `localhost` o en la red privada de tu nube (VPC).

## 5. Auditoría de Queries
Activa los logs de la base de datos para registrar queries que tarden mucho o que den errores de permiso denegado de forma repetida. Puede ser señal de alguien intentando saltarse los límites de privilegio.

## Resumen: La caja negra
La base de datos debe ser una caja negra a la que tu aplicación solo tiene permiso para "meter y sacar datos" específicos, nunca para cambiar las reglas del juego. Limitar los privilegios de la conexión es el seguro más barato contra desastres de inyección.
