#!/bin/bash

# COMANDOS ESENCIALES DE DOCKER
# -----------------------------------------------------------------------------
# Esta es la "navaja suiza" que usarás el 90% del tiempo.

# 1. GESTIÓN DE IMÁGENES
docker pull python:3.11-slim   # Descarga una imagen del Registry
docker images                  # Lista todas las imágenes locales
docker rmi <image_id>          # Borra una imagen local

# 2. GESTIÓN DE CONTENEDORES (Ciclo de vida)
# -d: modo 'detached' (fondo)
# -p: mapeo de puertos <host>:<contenedor>
# --name: nombre legible para no usar el ID
docker run -d -p 8080:80 --name mi_api nginx

docker ps                      # Lista contenedores corriendo
docker ps -a                   # Lista TODOS (incluyendo parados)
docker stop mi_api             # Para el contenedor
docker start mi_api            # Lo vuelve a arrancar
docker rm mi_api               # Borra el contenedor (debe estar parado)

# 3. INTERACCIÓN Y DEBUG
docker logs mi_api             # Ver la salida de consola de la App
docker logs -f mi_api          # Ver logs en tiempo real (follow)
docker inspect mi_api          # Ver TODA la configuración JSON
docker exec -it mi_api bash    # Entrar a la terminal "dentro" del contenedor

# 4. LIMPIEZA TOTAL
docker system prune            # Borra TODO lo que no se esté usando
                               # (Usa esto cuando te quedes sin disco)

# CONSEJO SENIOR:
# ---------------
# Usa siempre etiquetas (tags) en tus imágenes (ej: python:3.11) en lugar 
# de 'latest'. 'latest' cambia con el tiempo y romperá tu build si no 
# tienes cuidado.
