"""
FASTAPI: INTEGRATION TESTING CON TESTCLIENT
-----------------------------------------------------------------------------
Cómo probar tus rutas de API simulando peticiones HTTP reales de forma 
ultra rápida y sin levantar un servidor de red.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# 1. LA APP (Imagina que esto es src/main.py)
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/echo")
def echo_payload(data: dict):
    return {"received": data}

# 2. FIXTURE DEL CLIENTE
@pytest.fixture
def client():
    """
    TestClient usa la librería 'httpx' internamente para llamar a la App 
    sin usar la tarjeta de red.
    """
    return TestClient(app)

# 3. TESTS DE API
def test_health_endpoint(client):
    # ACT: Realizamos la petición
    response = client.get("/health")
    
    # ASSERT: Verificamos status y cuerpo
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_echo_endpoint_with_payload(client):
    payload = {"msg": "hola", "id": 1}
    
    # ACT: Enviamos un JSON
    response = client.post("/echo", json=payload)
    
    # ASSERT
    assert response.status_code == 200
    assert response.json()["received"] == payload

"""
¿QUÉ ESTAMOS TESTEANDO REALMENTE AQUÍ?
--------------------------------------
1. Routing: Que la ruta existe y está bien escrita.
2. Serialización: Que Pydantic puede convertir el dict en JSON y viceversa.
3. Status Codes: Que devolvemos 200/201/404 correctamente.
4. Lógica: Que la función del endpoint hace lo que debe.
"""

"""
CONSEJO SENIOR:
---------------
Usa el mismo cliente para TODA la suite de tests. Si tu App necesita una 
DB, usa 'dependency_overrides' para inyectar una DB de test al cliente 
sin tocar el código original de la App.
"""
