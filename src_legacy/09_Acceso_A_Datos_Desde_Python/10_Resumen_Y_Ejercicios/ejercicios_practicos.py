"""
EJERCICIOS PRÁCTICOS: ACCESO A DATOS
-----------------------------------------------------------------------------
Pon a prueba tus conocimientos con estos retos de nivel Senior.
"""

# RETO 1: LA PESADILLA N+1
# Tienes una tabla 'Order' y una tabla 'OrderItem'. Escribe una función 
# usando SQLAlchemy ORM que recupere los últimos 10 pedidos y sus ítems 
# asegurando que SOLO se lanzan 2 queries a la base de datos (usa selectinload).

# RETO 2: EL REPOSITORIO GENÉRICO
# Implementa una clase BaseRepository que use TypeVars para que funcione 
# con cualquier modelo de SQLAlchemy, incluyendo métodos: get_by_id, list_all y save.

# RETO 3: EL ANALISTA DE DATOS
# Tienes un DataFrame de Pandas con 500,000 registros de ventas. 
# Escribe un script que los inserte en una tabla de Postgres de forma 
# eficiente (batching) y que maneje conflictos de duplicados (UPSERT) 
# basándose en la columna 'transaction_id'.

# RETO 4: MIGRACIÓN DE ALTO RIESGO
# Imagina que tienes que añadir una columna 'social_security_number' a una 
# tabla de 50 millones de filas. Escribe el script de Alembic (upgrade()) 
# asegurando que no bloqueas la tabla para lecturas.

# RETO 5: EL UNIT OF WORK
# Crea un decorador @transactional que envuelva una función de servicio 
# y asegure que se inicia una sesión de base de datos, se hace commit si 
# la función termina con éxito, y rollback si hay una excepción.

"""
¡Si puedes resolver estos 5 retos, estás listo para trabajar en cualquier 
equipo de Backend o Data Engineering de alto nivel!
"""
