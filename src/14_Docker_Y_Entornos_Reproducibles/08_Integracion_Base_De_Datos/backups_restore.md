# Backups y Restore en PostgreSQL Dockerizado

Como vimos en el Tema 04, los volúmenes no son suficientes. Para bases de datos, usamos las herramientas nativas de flujo de datos.

## 1. Exportar datos (Backup)
No necesitas entrar al contenedor. Puedes lanzar el comando desde fuera usando `docker exec`.

```bash
docker exec -t nombre_db pg_dump -U mi_usuario mi_db > backup.sql
```
- `-t`: Modo terminal.
- `pg_dump`: La herramienta mágica de Postgres.
- `> backup.sql`: Redirige la salida a un archivo en tu ordenador real.

## 2. Importar datos (Restore)
Si quieres llenar tu base de datos local con un backup de producción:

```bash
cat backup.sql | docker exec -i nombre_db psql -U mi_usuario -d mi_db
```
- `-i`: Modo interactivo (para que acepte la entrada del `cat`).

## 3. Automatización de Backups (The Senior Way)
Crea un pequeño servicio en tu Compose que use una imagen con el cliente de Postgres y un script de cron.

```yaml
backup-worker:
  image: postgres:15-alpine
  volumes:
    - ./backups:/backups
  environment:
    - PGPASSWORD=supersecreto
  command: >
    sh -c "while true; do 
             pg_dump -h db -U user -d mi_db > /backups/db_$(date +%Y%m%d).sql; 
             sleep 86400; 
           done"
```

## 4. Backups en la Nube
Para máxima seguridad, el script anterior debería subir el `.sql` a un bucket de S3 o Google Cloud Storage tras terminar, y luego borrar el archivo local para no llenar el disco.

## Resumen: La tranquilidad del Dump
Tener un comando de backup probado es lo único que te permitirá dormir tranquilo cuando toques la base de datos en producción. Practica el proceso de restauración al menos una vez al mes para asegurar que los archivos de backup realmente funcionan.
