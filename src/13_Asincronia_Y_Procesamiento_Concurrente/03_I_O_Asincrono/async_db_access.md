# Acceso a Bases de Datos Asíncronas

La base de datos suele ser el mayor cuello de botella de una aplicación backend. Si tu API es asíncrona pero tu driver de DB es síncrono, estás perdiendo el 90% de las ventajas de rendimiento.

## 1. Drivers Asíncronos vs Síncronos
- **Síncronos (Prohibidos en Async):** `psycopg2`, `mysql-connector`. Bloquean el hilo entero mientras la DB procesa la query.
- **Asíncronos (Recomendados):** `asyncpg` (Postgres), `aiomysql` (MySQL), `motor` (MongoDB). Estos permiten que FastAPI atienda a otros usuarios mientras espera los datos.

## 2. El Stack Moderno (SQLAlchemy + Async)
SQLAlchemy 1.4+ y 2.0 permiten un flujo 100% asíncrono.
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# La URL debe empezar por 'postgresql+asyncpg://'
engine = create_async_engine("url_de_db")
async_session = sessionmaker(engine, class_=AsyncSession)

async with async_session() as session:
    result = await session.execute(select(User))
    users = result.scalars().all()
```

## 3. Ventajas del acceso asíncrono
- **Parallel Queries:** Puedes lanzar 3 consultas distintas a la DB al mismo tiempo con `asyncio.gather` y obtener los resultados en lo que tarda la más lenta.
- **Consumo de recursos:** El servidor gasta mucha menos memoria porque no necesita un hilo real del SO para cada usuario esperando a la DB.

## 4. El peligro: El pool de conexiones
Un error común es pensar que por ser async puedes lanzar 1.000 queries a la vez.
- **Realidad:** Tu base de datos tiene un límite de conexiones (ej: 100). Si lanzas 1.000, la mayoría fallarán por "Timeout al obtener conexión".
- **Solución:** Configura correctamente el tamaño del Pool y usa Semáforos si es necesario.

## 5. Cuándo NO usar DB asíncrona
Si estás haciendo un script de migración que corre solo, añadir la complejidad de `asyncio` no te aporta nada. Úsala solo cuando tengas muchos clientes simultáneos (Servidores Web).

## Resumen: Integridad y Rapidez
Para un backend senior, el acceso asíncrono a datos es obligatorio en 2024. `asyncpg` es conocido por ser hasta 3 veces más rápido que `psycopg2` en entornos de alta concurrencia gracias a su arquitectura no bloqueante.
