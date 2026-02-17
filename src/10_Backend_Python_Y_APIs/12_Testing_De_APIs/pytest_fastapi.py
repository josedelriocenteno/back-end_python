"""
TESTING: CONFIGURACIÓN DE PYTEST CON FASTAPI
-----------------------------------------------------------------------------
El testing es lo que permite que tu backend sea mantenible a largo plazo. 
Usamos Pytest por su sencillez y potencia.
"""

import pytest
from fastapi.testclient import TestClient
from .hello_api import app

# 1. EL TEST CLIENT
# FastAPI proporciona una utilidad para simular peticiones HTTP sin 
# necesidad de levantar el servidor real.
client = TestClient(app)

# 2. TU PRIMER TEST DE API
def test_read_main():
    """
    Verifica que el endpoint root devuelva un 200 y el mensaje esperado.
    """
    # Act: Realizar la petición
    response = client.get("/")
    
    # Assert: Validar resultados
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Backend Python!"}

# 3. TEST CON PARÁMETROS
def test_say_hello():
    response = client.get("/hello/Antigravity")
    assert response.status_code == 200
    assert response.json()["message"] == "Hola, Antigravity!"

"""
CÓMO EJECUTAR LOS TESTS:
-----------------------------------------------------------------------------
Desde la raíz del proyecto, simplemente lanza:
$ pytest

Para ver más detalle:
$ pytest -v

Para ver los prints de tu código:
$ pytest -s
"""

"""
RESUMEN PARA EL DESARROLLADOR:
1. Divide tus tests por archivos: test_auth.py, test_users.py, etc.
2. Cada función que empiece por 'test_' será ejecutada por Pytest.
3. El TestClient usa la librería 'httpx' internamente, por lo que la sintaxis 
   es idéntica a la de un cliente real.
"""
