"""
PYTEST: FIXTURES AVANZADAS (YIELD Y SCOPE)
-----------------------------------------------------------------------------
Cómo gestionar recursos que necesitan limpieza (Teardown) y controlar 
cuántas veces se ejecuta una fixture.
"""

import pytest

# 1. FIXTURE CON TEARDOWN (YIELD)
@pytest.fixture
def base_datos_temporal():
    """
    Usa 'yield' en lugar de 'return'. 
    Todo lo que hay ANTES del yield es el SETUP.
    Todo lo que hay DESPUÉS del yield es el TEARDOWN.
    """
    print("\n[SETUP] Conectando a DB temporal...")
    db = {"conexion": "activa", "datos": []}
    
    yield db # Aquí es donde se ejecutan los tests
    
    print("\n[TEARDOWN] Cerrando conexión y limpiando...")
    db["conexion"] = "cerrada"

# 2. SCOPE DE LAS FIXTURES
# 'function' (por defecto): Se ejecuta una vez por cada función de test.
# 'module': Se ejecuta una vez por cada archivo .py.
# 'session': Se ejecuta UNA VEZ para toda la suite de tests (ej: levantar Docker).
@pytest.fixture(scope="module")
def singleton_resource():
    print("\n[MODULE SETUP] Recurso pesado cargado (solo una vez por archivo)")
    return "Dato compartido"

def test_paso_1(base_datos_temporal, singleton_resource):
    base_datos_temporal["datos"].append("item1")
    assert len(base_datos_temporal["datos"]) == 1

def test_paso_2(base_datos_temporal, singleton_resource):
    # base_datos_temporal se ha reseteado porque su scope es 'function'
    assert len(base_datos_temporal["datos"]) == 0

"""
CONSEJO SENIOR:
---------------
Usa 'session' scope para cosas que tarden mucho en arrancar (como un motor 
de base de datos). Usa 'function' (por defecto) para datos específicos que 
quieras que estén limpios en cada prueba. El aislamiento es tu prioridad.
"""
