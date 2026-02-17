# Hardening de API: Preparándonos para Producción

El "Hardening" es el proceso de fortalecer un sistema para reducir su superficie de vulnerabilidad. Una aplicación FastAPI "recién salida del horno" necesita estos ajustes antes de enfrentarse a internet.

## 1. Desactivación de Docs en Producción
A menos que tu API sea pública, no querrás que los hackers vean tu estructura de endpoints fácilmente.
```python
from fastapi import FastAPI
import os

app = FastAPI(
    docs_url=None if os.getenv("ENV") == "prod" else "/docs",
    redoc_url=None if os.getenv("ENV") == "prod" else "/redoc"
)
```

## 2. Servidores y Proxies (Gunicorn + Uvicorn)
Nunca uses solo Uvicorn en producción. Usa un servidor de procesos como Gunicorn para gestionar los fallos de workers y la concurrencia real. Además, coloca siempre un **Nginx** o **HAProxy** delante para gestionar el SSL y el buffering de peticiones lentas.

## 3. Límites de Tamaño (Payload Limit)
Protege tu memoria RAM limitando el tamaño máximo del cuerpo de las peticiones.
*   Nginx: `client_max_body_size 1M;`

## 4. Gestión de Secretos Profesional
No uses archivos `.env` en servidores de producción reales. Usa servicios de gestión de secretos como:
*   AWS Secrets Manager
*   HashiCorp Vault
*   GitHub Actions Secrets (para el despliegue)

## 5. Contenedores Seguros (Docker Hardening)
*   **No root:** No ejecutes tu app como usuario `root` dentro del contenedor. Crea un usuario con pocos privilegios.
*   **Imágenes Ligeras:** Usa `python:3.11-slim` o `alpine` para reducir las librerías innecesarias que podrían tener vulnerabilidades.
*   **Read-only Filesystem:** Si tu app no necesita escribir archivos, lanza el contenedor con el sistema de archivos en modo lectura.

## 6. Dependencias Actualizadas
Usa herramientas como `Safety` o `Snyk` para escanear tus dependencias en busca de vulnerabilidades conocidas (CVEs).
```bash
# Escanear dependencias instaladas
safety check
```

## 7. Cifrado en Reposo (At Rest)
Asegúrate de que la base de datos PostgreSQL no solo cifra la comunicación (TLS), sino que los archivos en el disco del servidor también están cifrados por el proveedor cloud.

## Resumen: La Última Milla
Hardening es la diferencia entre una app que simplemente funciona y una app industrial. Estas medidas no afectan a la funcionalidad, pero son las que permiten que el desarrollador duerma tranquilo por las noches.
