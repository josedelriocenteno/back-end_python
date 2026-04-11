"""
RESUMEN: ACCESO A DATOS DESDE PYTHON
-----------------------------------------------------------------------------
Este archivo condensa los conceptos clave aprendidos en el tema 09.
"""

# 1. EL ESPECTRO DE HERRAMIENTAS
# Psycopg3: Driver nativo. Máxima velocidad, SQL puro, ideal para ETLs.
# SQLAlchemy Core: Expresividad programática. Seguridad sin objetos pesados.
# SQLAlchemy ORM: Productividad máxima. Objetos Python mapeados a tablas.

# 2. LAS 3 REGLAS DE ORO DEL RENDIMIENTO
# - Evitarás el N+1: Usa joinedload() o selectinload().
# - Usarás Pooling: Nunca abras una conexión por cada request.
# - Operarás en Lotes: Usa executemany() o copy() para inserciones masivas.

# 3. SEGURIDAD ANTE TODO
# Jamás concatenarás strings: Siempre parámetros %s o :mapping.
# Las credenciales vivirán en variables de entorno (.env).

# 4. ARQUITECTURA PROFESIONAL
# Lógica de Negocio -> vive en SERVICIOS.
# Lógica de Persistencia -> vive en REPOSITORIOS.
# Atomicidad -> gestionada por el UNIT OF WORK.

# 5. EVOLUCIÓN
# Las bases de datos mutan: Alembic es obligatorio para versionar el esquema.

"""
PENSAMIENTO SENIOR:
No hay una herramienta mejor que otra. Un buen desarrollador backend elige 
el ORM para la rapidez de entrega de la lógica de negocio y el SQL puro 
para los cuellos de botella de rendimiento.
"""
