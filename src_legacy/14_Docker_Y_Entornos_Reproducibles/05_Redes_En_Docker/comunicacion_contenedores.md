# Comunicación entre Contenedores: El poder del DNS Interno

El error número 1 al empezar con Docker es intentar conectar la App a la DB usando `localhost`. **¡Error!** Para la App, `localhost` es ella misma, no el contenedor de la DB.

## 1. El concepto de "Service Discovery"
Dentro de una red de Docker personalizada, cada contenedor es un "servidor" con su propio nombre.
- Contenedor 1: `--name app`
- Contenedor 2: `--name db`

Desde el código Python de `app`, puedes conectar a la base de datos usando simplemente el host `db`. Docker se encarga de traducir ese nombre a la IP interna correcta automáticamente.

## 2. Ejemplo práctico de conexión (SQLAlchemy)
```python
# MAL (No funciona en Docker)
DATABASE_URL = "postgresql://user:pass@localhost:5432/dbname"

# BIEN (Usando el nombre del servicio/contenedor)
DATABASE_URL = "postgresql://user:pass@db:5432/dbname"
```

## 3. El puerto Interno vs Externo
- **Puerto 5432:** Es el puerto donde escucha Postgres DENTRO de la red de Docker. Es el que usa tu App Python.
- **Puerto 5433:** Podría ser el puerto que mapeas a tu PC real para entrar con un cliente SQL (DBeaver/DataGrip).
- **Senior Tip:** Tu App nunca debe usar el puerto mapeado al host; siempre debe usar el puerto nativo del contenedor a través de la red interna.

## 4. Visibilidad entre redes
Si el Contenedor A está en `red_1` y el Contenedor B está en `red_2`, **no podrán hablar entre ellos** aunque conozcan sus nombres. El aislamiento es real.
- **Solución:** Un contenedor puede estar conectado a múltiples redes a la vez.

## 5. Comprobación de conectividad
Si algo falla, entra al contenedor de la App y usa `ping` o `curl`:
```bash
docker exec -it app apt update && apt install -y iputils-ping
docker exec -it app ping db
```

## Resumen: Nombres sobre IPs
En Docker, olvida las direcciones IP. Diseña tus aplicaciones para que consuman nombres de servicios configurables por variables de entorno. Esto hará que tu backend sea flexible y fácil de orquestar.
