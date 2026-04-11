# Docker Logs: Tu ventana al interior del contenedor

Cuando una aplicación falla en un contenedor, no puedes entrar a mirar archivos de texto fácilmente. Docker centraliza toda la "salida estándar" (stdout) y la "salida de error" (stderr) en un solo lugar.

## 1. El comando maestro
`docker logs mi_app`
- Muestra todo el historial de la App desde que arrancó.

## 2. Flags de Supervivencia
- `-f` (Follow): Ver los logs en tiempo real (como `tail -f`).
- `--tail 100`: Ver solo las últimas 100 líneas (ideal si la App lleva meses corriendo).
- `--since 5m`: Ver solo lo que ha pasado en los últimos 5 minutos.
- `-t`: Añade marcas de tiempo a cada línea.

## 3. El formato JSON (Driver de Logs)
Docker guarda los logs en archivos JSON en el host. 
- **Peligro:** Si tu App escribe muchos logs, estos archivos pueden llenar el disco duro del servidor rápidamente.
- **Solución:** Configura el "Log Rotation" en el daemon de Docker o en el Compose.

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## 4. Logs en modo Detached
Cuando corres `docker compose up -d`, no ves nada. Usa `docker compose logs -f web` para "engancharte" a la salida de un servicio específico.

## 5. Salida Estándar vs Archivos
- **MAL:** Configurar tu App de Python para que escriba en `/app/logs/error.log`. Docker no podrá capturar esos logs.
- **BIEN:** Configura el logger de Python (`logging.StreamHandler`) para escribir en la terminal (`sys.stdout`). Es la forma estándar y recomendada.

## Resumen: Visibilidad Directa
No compliques tu sistema de logging. Haz que tu App escupa todo por la terminal y deja que Docker se encargue de almacenarlo, rotarlo y enviarlo si es necesario a sistemas externos como ELK o CloudWatch.
