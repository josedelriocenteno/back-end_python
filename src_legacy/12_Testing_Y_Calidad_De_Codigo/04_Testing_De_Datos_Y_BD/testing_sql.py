"""
TESTING: PRUEBAS DE SQL Y REPOSITORIOS
-----------------------------------------------------------------------------
Cómo probar que tus queries SQL realmente devuelven lo que esperas 
usando una base de datos real (ej: SQLite en memoria).
"""

import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# 1. MODELO DE DB (Imagina que esto es src/models.py)
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

# 2. LÓGICA DE REPOSITORIO (Imagina que esto es src/repository.py)
def get_expensive_products(session, min_price: int):
    return session.query(Product).filter(Product.price >= min_price).all()

# 3. FIXTURE DE BASE DE DATOS DE TEST
@pytest.fixture
def db_session():
    """
    Crea una base de datos SQLite efímera en memoria para cada test.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session # Aquí corre el test
    
    session.close()

# 4. EL TEST REAL
def test_get_expensive_products_filters_correctly(db_session):
    # ARRANGE: Poblamos la DB con datos conocidos
    db_session.add(Product(name="Laptop", price=1000))
    db_session.add(Product(name="Mouse", price=20))
    db_session.add(Product(name="Monitor", price=300))
    db_session.commit()
    
    # ACT: Ejecutamos el repositorio
    result = get_expensive_products(db_session, 500)
    
    # ASSERT: Verificamos resultados
    assert len(result) == 1
    assert result[0].name == "Laptop"

"""
¿POR QUÉ TESTEAR CON DB Y NO CON MOCKS?
---------------------------------------
Hacer un mock de 'db.query().filter().all()' es muy complejo y no prueba 
nada real. Testear contra una DB real (aunque sea en memoria) asegura:
1. Que tu sintaxis SQL/ORM es correcta.
2. Que los tipos de datos (int vs float) coinciden.
3. Que no hay errores de 'Atributo no encontrado' en el modelo.
"""
