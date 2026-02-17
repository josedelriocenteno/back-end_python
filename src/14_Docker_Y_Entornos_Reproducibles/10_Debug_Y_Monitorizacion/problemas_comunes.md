# Problemas Comunes en Producción (Docker)

Cuando algo va mal en el servidor, los nervios pueden traicionarte. Aquí los fallos típicos y cómo resolverlos rápidamente.

## 1. El contenedor no arranca (Exited 0 o 1)
- **Causa:** El script de Python ha terminado. 
- **Solución:** Mira `docker logs`. Probablemente falte una variable de entorno critica o una dependencia no instalada.
- **Tip:** Si el log está vacío, intenta correrlo con `-it` y sobreescribe el comando con `bash` para ver si puedes lanzarlo a mano.

## 2. Error: No space left on device
Docker es un gran consumidor de disco. Capas viejas e imágenes olvidadas se acumulan.
- **Solución:**
  ```bash
  docker system prune -a --volumes # ¡CUIDADO! Borra todo lo que no esté en uso.
  ```

## 3. Tiempo de respuesta lento (Latencia)
- **Causa:** El contenedor está siendo "estrangulado" (Throttling) por falta de CPU.
- **Solución:** Revisa `docker stats`. Si el % de CPU está cerca del límite que pusiste en el Compose, súbelo o escala horizontalmente.

## 4. El "Zombie Container"
Un contenedor que no responde a `docker stop` ni a `docker kill`.
- **Causa:** El proceso PID 1 ha ignorado las señales del kernel o está en un estado de E/S ininterrumpible.
- **Solución:** A veces solo queda reiniciar el servicio de Docker del host o forzar la eliminación con `docker rm -f`.

## 5. DNS Intermitente
Los contenedores a veces dejan de verse entre ellos.
- **Causa:** Conflictos en la red interna de Docker por restos de redes borradas a medias.
- **Solución:** `docker network prune` y reiniciar el stack con `docker compose down && docker compose up -d`.

## Resumen: Mantener la calma
Casi todos los problemas de Docker tienen su explicación en los logs o en el consumo de recursos. Usa siempre límites de CPU y RAM, monitoriza el disco y asegúrate de que tu PID 1 gestiona bien las señales de salida.
