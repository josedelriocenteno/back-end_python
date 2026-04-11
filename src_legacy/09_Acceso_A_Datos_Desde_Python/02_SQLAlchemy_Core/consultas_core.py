"""
SQLALCHEMY CORE: CONSULTAS EXPRESIVAS (SELECT, INSERT, UPDATE, DELETE)
-----------------------------------------------------------------------------
Core nos permite construir SQL usando funciones de Python. Es más seguro que 
concatenar strings y permite construir queries dinámicas fácilmente.
"""

from sqlalchemy import select, insert, update, delete
from .metadata_y_tablas import users_table

def query_examples(conn):
    
    # 1. SELECT (Básico)
    # Genera: SELECT users.id, users.name FROM users WHERE users.name = 'Alice'
    stmt = select(users_table).where(users_table.c.name == "Alice")
    result = conn.execute(stmt)
    
    for row in result:
        print(f"ID: {row.id}, Name: {row.name}")

    # 2. INSERT
    stmt_ins = insert(users_table).values(name="Bob", email="bob@example.com")
    conn.execute(stmt_ins)

    # 3. UPDATE
    stmt_upd = update(users_table).where(users_table.c.name == "Bob").values(name="Robert")
    conn.execute(stmt_upd)

    # 4. DELETE
    stmt_del = delete(users_table).where(users_table.c.id > 100)
    conn.execute(stmt_del)

def advanced_selects(conn):
    # Selección de columnas específicas (users_table.c es el atajo para columns)
    stmt = select(users_table.c.name, users_table.c.email).order_by(users_table.c.name.desc())
    
    # Operadores complejos
    from sqlalchemy import and_, or_
    stmt_complex = select(users_table).where(
        and_(
            users_table.c.name.like("A%"),
            or_(users_table.c.id < 10, users_table.c.id > 20)
        )
    )
    
    print(conn.execute(stmt_complex).all())

"""
RESUMEN PARA EL DESARROLLADOR:
1. '.c' es el acceso a las columnas de la tabla.
2. SQLAlchemy Core se encarga de la parametrización (seguridad) automáticamente.
3. Las sentencias son inmutables: select() devuelve un objeto que puedes modificar 
   con .where(), .limit(), etc.
4. Es ideal para queries muy dinámicas donde los filtros cambian según el input.
"""
