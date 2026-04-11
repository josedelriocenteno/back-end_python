# Volúmenes Básicos: Persistencia en un mundo efímero

Por defecto, los contenedores son "efímeros": si borras un contenedor, todos los datos creados dentro mueren con él. Para bases de datos y archivos permanentes, necesitamos **almacenamiento externo**.

## 1. Bind Mounts (Montajes de enlace)
Mapean un directorio de tu máquina real a un directorio del contenedor.
- **Uso:** `docker run -v /mi/carpeta/local:/app/data ...`
- **Ventaja:** Ideal para desarrollo (Hot Reload). Cambias un archivo en tu IDE y el contenedor lo ve al instante.
- **Contra:** Depende de la estructura de carpetas de tu ordenador. Difícil de mover a la nube.

## 2. Docker Volumes (Volúmenes gestionados)
Docker crea y gestiona una carpeta en un lugar especial del sistema (normalmente `/var/lib/docker/volumes/`).
- **Uso:** `docker run -v nombre_volumen:/var/lib/postgresql/data ...`
- **Ventaja:** Independiente del SO. Más rápido que los bind mounts en Mac/Windows. Docker se encarga de los permisos.
- **Uso ideal:** Bases de datos en producción.

## 3. Anonymous Volumes (Volúmenes Anónimos)
Si no le pones nombre, Docker le asigna un ID aleatorio.
- **Peligro:** Son difíciles de reutilizar y suelen acabar llenando el disco de basura olvidada.

## 4. Diferencia clave: ¿Quién manda?
- **Bind Mount:** Tú mandas. Si borras el archivo en tu PC, desaparece del contenedor.
- **Volume:** Docker manda. La App del contenedor escribe datos y Docker los protege en un lugar seguro.

## Resumen: Cuándo usar cada uno
- **Desarrollo:** Bind Mounts (para ver cambios de código en vivo).
- **Producción:** Docker Volumes (para que los datos de la DB sobrevivan a actualizaciones de la imagen).
