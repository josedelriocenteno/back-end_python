# Backup y Restauración de Volúmenes

Tener los datos en un volumen no significa que estén a salvo de errores humanos o fallos de disco del servidor. Necesitas una estrategia de backup fría.

## 1. El problema: Los volúmenes son "opacos"
Como los volúmenes los gestiona Docker, no puedes entrar simplemente con el explorador de archivos y copiarlos.

## 2. Estrategia: El Contenedor de Backup (Patrón Sidecar)
Lanzamos un contenedor temporal que monta el volumen y el directorio actual, y comprime los datos.

```bash
# Backup de un volumen a un archivo .tar.gz
docker run --rm \
  -v mi_volumen_datos:/source:ro \
  -v $(pwd):/backup \
  alpine tar -czf /backup/backup_datos.tar.gz -C /source .
```

## 3. Restauración de un Backup
El proceso inverso: descomprimir el archivo dentro de un nuevo volumen.

```bash
# Restaurar desde el archivo al volumen
docker run --rm \
  -v mi_nuevo_volumen:/target \
  -v $(pwd):/backup \
  alpine sh -c "tar -xzf /backup/backup_datos.tar.gz -C /target"
```

## 4. Backup de Bases de Datos (⚠️ Importante)
No hagas backup de los archivos crudos de una base de datos mientras está encendida (puede haber corrupción).
- **Mejor:** Usa las herramientas de la propia DB (`pg_dump` para Postgres) desde fuera o dentro del contenedor.

## 5. Automatización (Cron)
En un entorno senior, un script de bash ejecuta estos comandos de backup cada noche y sube el resultado a un almacenamiento en la nube (S3, Google Cloud Storage).

## Resumen: La regla de tres
- Una copia es ninguna.
- Dos copias es una.
- Tres copias es seguridad.
No confíes solo en que "Docker lo guarda". Los volúmenes deben ser tratados como activos críticos de la empresa.
