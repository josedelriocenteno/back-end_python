# Hardening Básico: Blindando el contenedor

El "Hardening" es el proceso de endurecer la seguridad del sistema desactivando todo lo que no sea estrictamente necesario.

## 1. Solo Lectura (`--read-only`)
Muchos ataques intentan descargar un script malicioso dentro del contenedor y ejecutarlo. 
- **Solución:** Ejecuta el contenedor con el sistema de archivos en modo solo lectura.
- `docker run --read-only ...`
- **Nota:** Tendrás que montar volúmenes específicos para las carpetas donde la App realmente necesite escribir (ej: `/tmp` o `/logs`).

## 2. Desactivar el escalado de privilegios
Evita que el usuario pueda usar comandos `su` o `sudo` aunque logre hackear la password.
- `docker run --security-opt=no-new-privileges:true ...`

## 3. Limitar recursos (DoS)
Un ataque de denegación de servicio puede intentar que tu contenedor consuma toda la RAM del host.
- `docker run --memory="512m" --cpus="1.0" ...`
- Si el contenedor intenta usar más, Docker lo matará antes de que afecte a otros servicios del servidor.

## 4. Borrar el historial de Shell
Si entras al contenedor a hacer algo y dejas el historial de comandos, estás dejando pistas a los atacantes.
- **Tip Senior:** Configura `ENV HISTSIZE=0` en tu Dockerfile.

## 5. Eliminar capacidades de red innecesarias
Docker permite dar permisos de bajo nivel (Capabilities). El 90% de las Apps no necesitan permisos para manipular el tráfico de red directo.
- `--cap-drop=ALL --cap-add=NET_BIND_SERVICE` (Quita todo y solo deja abrir puertos).

## Resumen: Superficie de ataque mínima
Cuanto menos "cosas" tenga tu contenedor, más difícil será hackearlo. Elimina ejecutables, quita permisos de escritura y limita los recursos de hardware. Un contenedor blindado es una preocupación menos en el día a día.
