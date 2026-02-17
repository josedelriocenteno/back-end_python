"""
TESTING: TESTS DE INTEGRACIÓN (API + DB)
-----------------------------------------------------------------------------
Probando que todo el sistema funciona en conjunto. Usamos una base de datos 
de test separada para no romper nada.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from .db_dependency import get_db, Base
from .main import app

# 1. SETUP DE DB DE TEST
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. FIXTURE DE SESIÓN DE DB
@pytest.fixture()
def db():
    # Creamos las tablas antes del test
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    # Borramos todo después del test para limpieza
    Base.metadata.drop_all(bind=engine)

# 3. FIXTURE DEL CLIENTE CON OVERRIDE
@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

# 4. EL TEST REAL
def test_create_user_in_db(client):
    response = client.post("/users/", json={"email": "test@test.com", "password": "123"})
    assert response.status_code == 201
    
    # Verificamos que realmente se puede leer después
    response_get = client.get("/users/")
    assert len(response_get.json()) == 1
    assert response_get.json()[0]["email"] == "test@test.com"

"""
RESUMEN PARA EL DESARROLLADOR:
1. Los tests de integración son más lentos pero dan mucha más confianza que 
   los unitarios.
2. Usa 'pytest-cov' para saber qué porcentaje de tus endpoints están testeados.
3. Lo ideal es correr estos tests contra una imagen de Docker de Postgres 
   idéntica a la de producción para evitar el "funciona en mi local".
"""
