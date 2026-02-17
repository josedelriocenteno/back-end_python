# Configuración de Uvicorn (El Motor ASGI)

Uvicorn es el puente entre el mundo exterior (HTTP) y tu código de Python (ASGI). Configurarlo correctamente es la diferencia entre una API estable y una que se cae bajo presión.

## 1. Comandos Esenciales de CLI

*   **Desarrollo:** `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
    *   `--reload`: Detecta cambios en el código (nunca en producción).
    *   `--host 0.0.0.0`: Permite que la API sea visible desde fuera del contenedor Docker o red local.

*   **Producción (Concepto):** En producción, no usamos solo Uvicorn. Usamos **Gunicorn** como administrador de procesos (manager) y a Uvicorn como el worker.
    `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`

## 2. Configuración Programática

Puedes configurar los logs y el comportamiento de Uvicorn desde un archivo de configuración o directamente en Python:

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        proxy_headers=True, # Vital si estás detrás de un Load Balancer como Nginx
        workers=4           # Número de procesos simultáneos
    )
```

## 3. Worker Strategy: ¿Cuántos necesito?
Una regla empírica común es:
`Numero de Workers = (2 * Número de Cores de CPU) + 1`
*   Si tu servidor tiene 2 CPUs, pon 5 workers. Esto asegura que mientras un worker está esperando a la base de datos (I/O), otro puede estar procesando un request de CPU.

## 4. Timeout y Keep-Alive
*   **Keep-Alive:** Mantiene la conexión abierta para que el cliente no tenga que renegociar el handshake TCP constantemente.
*   **Timeout:** Si un request tarda demasiado, Uvicorn debe matarlo para liberar recursos.

## 5. Logs y Formateo
Uvicorn soporta logs en formato JSON, lo cual es vital para herramientas de observabilidad como DataDog o el stack ELK (Elasticsearch, Logstash, Kibana).

## Resumen: El Servidor Invisible
Un buen desarrollador se preocupa de que su servidor esté optimizado. Asegúrate de entender qué significa estar detrás de un proxy (`proxy_headers`) y cuánta carga puede soportar realmente tu configuración de workers.
