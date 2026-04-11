"""
TESTING: FIXTURES DE BASE DE DATOS PROFESIONALES
-----------------------------------------------------------------------------
El patrón 'Fixture' permite inyectar datos y conexiones en nuestros tests 
de forma limpia usando Pytest.
"""

import pytest
from sqlalchemy import create_engine
from .modelos_orm import Base, User

# Fixture de sesión de base de datos reutilizable
@pytest.fixture(scope="session")
def engine():
    """Crea el engine una sola vez por cada ejecución de tests."""
    engine = create_engine("sqlite://") # Memoria
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def db(engine):
    """Proporciona una sesión limpia para cada test."""
    connection = engine.connect()
    transaction = connection.begin()
    
    # Aquí podríamos configurar una sesión de SQLAlchemy
    # session = Session(bind=connection)
    
    yield connection # El test ocurre aquí
    
    # Rollback al final: el test nunca 'ensucia' la DB para el siguiente!
    transaction.rollback()
    connection.close()

# Fixture con datos pre-cargados
@pytest.fixture
def seed_users(db):
    """Inyecta datos iniciales comunes para varios tests."""
    users = [
        {"username": "admin", "email": "admin@test.com"},
        {"username": "guest", "email": "guest@test.com"}
    ]
    # ... Lógica de inserción ...
    return users

"""
RESUMEN PARA EL DESARROLLADOR:
1. El patrón 'rollback-only' es la forma más rápida de mantener tests limpios.
2. Separa las fixtures de 'Infraestructura' (engine, connection) de las de 
   'Datos' (seed_users).
3. Usa el fixture 'conftest.py' para compartir estas fixtures entre varios 
   archivos de test.
"""
