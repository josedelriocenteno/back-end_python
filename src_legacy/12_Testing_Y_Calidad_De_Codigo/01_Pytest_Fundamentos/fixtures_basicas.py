"""
PYTEST: FIXTURES BÁSICAS
-----------------------------------------------------------------------------
Las fixtures sirven para preparar el escenario repetitivo (Setup) y 
limpiarlo después (Teardown).
"""

import pytest

# 1. DEFINICIÓN DE LA FIXTURE
@pytest.fixture
def usuario_ejemplo():
    """
    Esta función crea un objeto que podemos 'inyectar' en cualquier test.
    """
    print("\n[SETUP] Creando usuario de prueba...")
    return {
        "id": 99,
        "username": "test_user",
        "email": "test@example.com",
        "is_active": True
    }

# 2. USO DE LA FIXTURE
# Simplemente ponemos el nombre de la función de la fixture como argumento.
def test_usuario_tiene_email_valido(usuario_ejemplo):
    assert "@" in usuario_ejemplo["email"]
    assert usuario_ejemplo["id"] == 99

def test_usuario_esta_activo_por_defecto(usuario_ejemplo):
    assert usuario_ejemplo["is_active"] is True

"""
¿POR QUÉ USAR FIXTURES EN LUGAR DE VARIABLES GLOBALES?
------------------------------------------------------
1. AISLAMIENTO: Cada test recibe una COPIA fresca de la fixture. Si un test 
   modifica el objeto, no afecta al siguiente test.
2. MODULARIDAD: Puedes tener fixtures que dependen de otras fixtures.
3. LIMPIEZA: Pueden gestionar conexiones a DB que se cierran automágicamente.
"""

"""
EJECUCIÓN:
Prueba ejecutar: pytest -s src/12_Testing...
El flag '-s' permite ver los prints (verás el mensaje de [SETUP]).
"""
