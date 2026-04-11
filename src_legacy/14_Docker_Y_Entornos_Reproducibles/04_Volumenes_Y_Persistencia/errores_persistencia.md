# Errores Comunes de Persistencia

La persistencia es donde más "vudú" ocurre en Docker. Estos son los problemas que te volverán loco si no los conoces.

## 1. El error del "Directorio Vacío"
Si montas un Bind Mount encima de una carpeta que YA tenía archivos en la imagen (ej: `/app`), la carpeta local sobreescribirá la del contenedor.
- **Resultado:** Tu código desaparece y la App falla al arrancar.
- **Solución:** Monta solo carpetas específicas de datos (`/app/data`), no la raíz de la App.

## 2. Conflictos de Permisos (Linux)
Docker corre como root por defecto. Si crea un archivo en un Bind Mount, ese archivo pertenecerá a root en tu PC.
- **Problema:** No podrás editar el archivo con tu IDE o borrarlo sin `sudo`.
- **Solución:** Usa la variable `USER` en el Dockerfile o el flag `--user $(id -u):$(id -g)` al ejecutar.

## 3. El Volumen "Fantasma" (Dangling Volumes)
Si borras contenedores con `docker rm` pero no usas el flag `-v`, el volumen sigue existiendo en el disco ocupando espacio, pero ya no tiene nombre ni dueño.
- **Solución:** Limpia periódicamente con `docker volume prune`.

## 4. Persistencia en Windows/Mac (Rendimiento)
Los Bind Mounts en Windows/Mac son lentos porque tienen que traducir los permisos de archivos entre dos sistemas operativos diferentes.
- **Síntoma:** Tu API tarda 2 segundos en responder en local pero 0.1s en el servidor.
- **Solución:** Usa **Named Volumes** para datos pesados (DBs) incluso en desarrollo.

## 5. Escribir en la capa de escritura (Copy-on-Write)
Escribir archivos directamente dentro del contenedor sin volumen funcional.
- **Problema:** Cada escritura es lenta (Docker tiene que copiar el archivo a una capa nueva) y el disco del contenedor crecerá infinitamente.
- **Solución:** Todo lo que sea "escribir datos" debe ir a un volumen.

## Resumen: Aislamiento Real
La persistencia rompe el aislamiento del contenedor. Hazlo con cuidado, mantén los permisos bajo control y monitoriza siempre el tamaño de tus volúmenes en el servidor.
