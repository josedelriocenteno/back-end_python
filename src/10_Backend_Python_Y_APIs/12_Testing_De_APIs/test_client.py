"""
TESTING: EL PODER DEL TESTCLIENT
-----------------------------------------------------------------------------
Cómo testear diferentes métodos HTTP, headers, y envío de datos JSON.
"""

from fastapi.testclient import TestClient
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/", status_code=201)
def create_item(item: Item):
    return item

client = TestClient(app)

# 1. TEST DE CREACIÓN (POST)
def test_create_item():
    # Enviamos un JSON usando el argumento 'json'
    item_data = {"name": "Monitor 4K", "price": 450.0}
    response = client.post("/items/", json=item_data)
    
    assert response.status_code == 201
    assert response.json()["name"] == "Monitor 4K"
    assert "price" in response.json()

# 2. TEST DE VALIDACIÓN (Error 422)
def test_create_item_invalid():
    # Enviamos datos que sabemos que fallarán (price como string)
    invalid_data = {"name": "X", "price": "gratis"}
    response = client.post("/items/", json=invalid_data)
    
    # FastAPI/Pydantic deben detectar el error automáticamente
    assert response.status_code == 422
    assert "detail" in response.json()

# 3. TEST CON HEADERS
def test_headers():
    # Podemos simular el envío de tokens o cabeceras custom
    response = client.get("/me", headers={"Authorization": "Bearer my-token"})
    # ... aserciones ...

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'client.post(..., json={})': envía el Content-Type: application/json.
2. 'client.post(..., data={})': envía un formulario (form-data).
3. Prueba siempre el 'camino feliz' (éxito) y los 'caminos de error' (validación fallida).
"""
