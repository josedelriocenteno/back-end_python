"""
RENDIMIENTO: CONNECTION POOLING
-----------------------------------------------------------------------------
Por qué no debes abrir una conexión por cada petición y cómo configurarlo.
"""

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# 1. EL PROBLEMA
# Abrir una conexión TCP + SSL + Auth a Postgres tarda entre 50ms y 200ms.
# Si tu API recibe 100 req/sec, el servidor colapsará solo abriendo sockets.

# 2. LA SOLUCIÓN: POOLING
# Mantenemos un "estanque" de conexiones abiertas y las prestamos.
DATABASE_URL = "postgresql+psycopg://user:password@localhost/dbname"

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool, # Es el predeterminado para la mayoría de DBs
    pool_size=10,         # Mínimo de conexiones siempre listas
    max_overflow=20,      # Permitir hasta 20 más si el tráfico sube
    pool_timeout=30,      # Si después de 30s no hay libre, lanza error
    pool_recycle=1800,    # Refrescar conexiones cada 30 min (evita timeouts de red)
    pool_pre_ping=True    # Verifica si la conexión sigue viva antes de darla
)

def pool_stats(eng):
    """
    Inspecionar el estado del pool (útil para monitorización).
    """
    print(f"Pool Size: {eng.pool.size()}")
    print(f"Checked in: {eng.pool.checkedin()}")
    print(f"Checked out: {eng.pool.checkedout()}")

"""
CONNECTION POOLING EXTERNO (PgBouncer):
-----------------------------------------------------------------------------
En infraestructuras masivas (Kubernetes con cientos de pods), incluso el 
pooling de SQLAlchemy se queda corto. Se usa 'PgBouncer' como proxy intermedio.
En ese caso, en SQLAlchemy pondremos un pool_size=1 o usaremos NullPool para 
dejar que PgBouncer haga el trabajo duro.
"""

"""
RESUMEN PARA EL DESARROLLADOR:
1. El pooling es obligatorio en cualquier aplicación que reciba más de 1 req/sec.
2. 'pool_pre_ping=True' es vital en entornos de nube (AWS/Azure) donde los 
   balancesadores cortan conexiones inactivas.
3. No pongas un pool_size gigantesco (ej: 500) a menos que tu DB tenga RAM para 
   mantener 500 procesos de Postgres.
"""
