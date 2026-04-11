"""
SQLALCHEMY CORE: JOINS Y FILTROS AVANZADOS
-----------------------------------------------------------------------------
Cómo unir tablas y realizar agregaciones complejas sin usar el ORM.
"""

from sqlalchemy import select, func, join
from .metadata_y_tablas import users_table, addresses_table

def join_examples(conn):
    
    # 1. JOIN IMPLÍCITO (Recomendado en 2.0)
    # Genera: SELECT ... FROM users JOIN addresses ON users.id = addresses.user_id
    stmt = select(users_table.c.name, addresses_table.c.street).join(
        addresses_table, users_table.c.id == addresses_table.c.user_id
    )
    
    # 2. LEFT OUTER JOIN
    stmt_left = select(users_table.c.name, addresses_table.c.street).join(
        addresses_table, isouter=True
    )

    # 3. AGREGACIONES (SQLAlchemy Functions)
    # Genera: SELECT users.name, count(addresses.id) ... GROUP BY users.name
    stmt_agg = select(
        users_table.c.name, 
        func.count(addresses_table.c.id).label("total_addresses")
    ).join(addresses_table).group_by(users_table.c.name).having(func.count(addresses_table.c.id) > 1)

    result = conn.execute(stmt_agg).all()
    for row in result:
        print(f"User {row.name} has {row.total_addresses} addresses")

def set_operations():
    """
    Core también soporta UNION, INTERSECT, etc.
    """
    from sqlalchemy import union
    s1 = select(users_table.c.name).where(users_table.c.id < 5)
    s2 = select(users_table.c.name).where(users_table.c.id > 10)
    stmt_union = union(s1, s2)
    # ...

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'func' da acceso a TODAS las funciones de tu base de datos (Postgres, Oracle, etc).
2. '.join()' es el método principal para unir tablas.
3. '.label()' es vital para dar nombres limpios a las columnas calculadas.
4. Core es extremadamente potente para analítica pesada donde el ORM sería 
   demasiado complejo de mapear.
"""
