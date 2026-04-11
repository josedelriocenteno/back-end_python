"""
PYTEST: GENERACIÓN DE DATOS REALISTAS CON FAKER
-----------------------------------------------------------------------------
NUNCA uses 'test1', 'test2' como datos. Usa la librería Faker para generar 
datos que se parezcan a la realidad y detecten fallos de formato.
"""

import pytest
from faker import Faker

fake = Faker(["es_ES"]) # Configuramos en español

@pytest.fixture
def fake_user_factory():
    """
    Una fixture que devuelve una función (Factory Pattern). 
    Útil para crear muchos usuarios en un solo test.
    """
    def _create_user():
        return {
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "bio": fake.text(max_nb_chars=100)
        }
    return _create_user

def test_registro_usuarios_masivos(fake_user_factory):
    # Generamos 10 usuarios realistas en un segundo
    usuarios = [fake_user_factory() for _ in range(10)]
    
    for u in usuarios:
        assert "@" in u["email"]
        assert len(u["name"]) > 2
        print(f"Probando con usuario: {u['name']} <{u['email']}>")

"""
¿POR QUÉ FAKER?
---------------
1. DATOS INESPERADOS: Faker puede generar nombres con acentos, direcciones 
   muy largas o formatos de teléfono raros que tus validaciones podrían 
   no estar manejando bien.
2. LEGIBILIDAD: Es más fácil entender un fallo si ves que ocurrió con 
   'Calle Mayor 15' que con 'string_aleatorio_3'.
3. ESCALABILIDAD: Pestañeando puedes generar un catálogo de 1.000 productos 
   o una base de datos de 5.000 clientes.
"""
