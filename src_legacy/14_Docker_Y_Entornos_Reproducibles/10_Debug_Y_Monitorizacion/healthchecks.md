# Healthchecks: ¿Está viva o solo encendida?

Un contenedor puede estar en estado `Running` porque el proceso de Python no ha muerto, pero estar "congelado" (Deadlock) y no responder peticiones. El **Healthcheck** le dice a Docker cómo verificar la salud real de la App.

## 1. ¿Por qué usarlos?
- Sin healthcheck, Docker solo sabe si el proceso existe.
- Con healthcheck, Docker sabe si la App puede atender usuarios.
- Los orquestadores (Docker Compose, Kubernetes) pueden reiniciar automáticamente contenedores "No Saludables" (Unhealthy).

## 2. Implementación en el Dockerfile
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1
```

## 3. Implementación en Docker Compose
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 1m30s
      timeout: 10s
      retries: 3
      start_period: 40s # Da tiempo a que la App arranque antes de empezar a vigilar
```

## 4. El endpoint `/health` en FastAPI
Crea siempre un endpoint ligero para este propósito:
```python
@app.get("/health")
def health_check():
    # Aquí puedes verificar la conexión a la DB o Redis
    return {"status": "ok"}
```

## 5. Estados del Healthcheck
1. **Starting:** Durante el `start_period`.
2. **Healthy:** El test dio OK.
3. **Unhealthy:** El test falló N veces (según `retries`).

## Resumen: Autogestión de fallos
Un sistema senior es resiliente. Los Healthchecks permiten que la infraestructura detecte errores de software y los corrija reiniciando el servicio, minimizando el tiempo de caída (Downtime) sin intervención humana.
