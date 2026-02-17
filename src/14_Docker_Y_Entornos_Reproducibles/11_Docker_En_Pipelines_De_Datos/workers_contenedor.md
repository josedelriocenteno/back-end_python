# Workers en Contenedores: Escalado masivo

Si tienes una cola de tareas (como vimos en el Tema 13) con Celery o Redis, Docker te permite escalar la capacidad de procesamiento de forma casi infinita.

## 1. Separación de Imágenes
Usa la misma imagen de Docker para tu API y para tu Worker. Solo cambia el comando de arranque.
- **API:** `CMD ["uvicorn", "main:app", ...]`
- **Worker:** `CMD ["celery", "-A", "tasks", "worker", ...]`

## 2. Escalado con Docker Compose
Puedes levantar múltiples instancias de un mismo servicio.
```bash
docker compose up -d --scale worker=5
```
Esto creará 5 contenedores independientes escuchando la misma cola de tareas.

## 3. Recursos Asimétricos
El Worker suele necesitar mucha más CPU que la API.
```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'
  worker:
    deploy:
      resources:
        limits:
          cpus: '2.0'
```

## 4. El problema del "Graceful Shutdown" en Workers
Cuando detienes un contenedor (`docker stop`), Docker envía un SIGTERM. El Worker de Celery debe terminar de procesar la tarea actual antes de morir para no perder el dato.
- **Solución:** Asegúrate de que tu script de Python captura las señales y que Docker da tiempo suficiente (default 10s) antes de enviar el SIGKILL matando el proceso a la fuerza.

## 5. El estado compartido: REDIS / RabbitMQ
Los workers nunca deben guardar estado en su propio disco. Todo se coordina a través de un broker externo. Docker Compose facilita enormemente levantar este entorno completo de forma local.

## Resumen: Procesamiento Elástico
Containerizar tus workers te permite adaptar tu infraestructura a la carga de trabajo real. Si tienes 1 millón de emails por enviar, levantas 50 contenedores de worker, y cuando la cola se vacíe, los cierras para ahorrar costes.
