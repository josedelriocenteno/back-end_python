"""
TESTING: PRUEBAS DE REPOSITORIOS
-----------------------------------------------------------------------------
Cómo probar la capa de acceso a datos sin ensuciar la base de datos de 
producción y asegurando que las queries funcionan.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .modelos_orm import Base, User
from .patron_repository import UserRepository

# 1. SETUP DE BASE DE DATOS DE TEST
# Usamos un engine independiente (normalmente una DB temporal o SQLite)
TEST_DATABASE_URL = "sqlite:///:memory:" # Muy rápido para tests unitarios

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

# 2. TEST DEL REPOSITORIO
def test_user_repository_add_and_get(db_session):
    # Arrange (Preparar)
    repo = UserRepository(db_session)
    new_user = User(username="tester", email="test@example.com")

    # Act (Actuar)
    repo.add(new_user)
    db_session.commit()
    
    # Assert (Afirmar)
    retrieved_user = repo.get_by_id(1)
    assert retrieved_user is not None
    assert retrieved_user.username == "tester"

def test_user_repository_get_non_existent(db_session):
    repo = UserRepository(db_session)
    user = repo.get_by_id(999)
    assert user is None

"""
RESUMEN PARA EL DESARROLLADOR:
1. Las pruebas de repositorios son 'Tests de Integración' ligeros.
2. Cada test debe empezar con la base de datos vacía o en un estado conocido.
3. Prueba siempre los 'edge cases' (qué pasa si no hay datos, si el ID es 
   negativo, etc.).
4. Si el repositorio usa funciones específicas de Postgres, NO uses SQLite 
   para tests; usa una instancia real de Postgres en Docker.
"""
