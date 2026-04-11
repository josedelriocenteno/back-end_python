# Ejercicio Final: Stack Completo Dockerizado

Tu misión es poner en práctica todo lo aprendido creando un entorno de desarrollo profesional para una API de seguimiento de tareas.

## Requisitos del Proyecto
Crea una estructura de archivos con:
1. **FastAPI App:** Un endpoint para guardar tareas y otro para leerlas.
2. **PostgreSQL:** Con un volumen para persistencia.
3. **Redis:** Para cachear el número total de tareas.
4. **Dockerfile:** Multi-stage, optimizado y con usuario no-root.
5. **Docker Compose:** Que orqueste los 3 servicios en una red privada.

## Pasos sugeridos
1. Escribe el `main.py` de la API conectando a `db` (Postgres) y `cache` (Redis).
2. Crea el `requirements.txt` con `fastapi, uvicorn, sqlalchemy, psycopg2-binary, redis`.
3. Crea un `Dockerfile` que instale las dependencias y copie el código.
4. Escribe el `docker-compose.yml` mapeando puertos y volúmenes.
5. Lanza el comando `docker compose up --build` y verifica que todo habla entre sí.

## Bonus Points (Senior)
- Añade un **Healthcheck** a la base de datos en el Compose.
- Usa un **perfil** para lanzar una herramienta visual como `pgadmin`.
- Crea un archivo `.dockerignore` que excluya todo rastro de desarrollo.

---
Si logras que este stack funcione de forma fluida, estarás listo para cualquier entorno backend real en el mercado. ¡Suerte!
