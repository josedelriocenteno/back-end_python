"""
TESTING: MOCKING Y SOBREESCRITURA DE DEPENDENCIAS
-----------------------------------------------------------------------------
Cómo probar tus rutas aislando la lógica de componentes externos como 
bases de datos o APIs de terceros.
"""

from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

app = FastAPI()

# Dependencia real que queremos evitar en un test unitario
def get_external_api_token():
    # Esto llamaría a un servidor de Auth real y tardaría mucho
    print("Llamando a servidor remoto...")
    return "real-token-123"

@app.get("/data")
def get_protected_data(token: str = Depends(get_external_api_token)):
    return {"token_used": token, "data": "Top Secret"}

# --- CÓDIGO DEL TEST ---

def test_get_data_with_mock():
    # 1. Definimos el Mock (el "sustituto")
    def mock_get_token():
        return "fake-mock-token"

    # 2. Sobreescribimos la dependencia en la app
    app.dependency_overrides[get_external_api_token] = mock_get_token

    # 3. Ejecutamos el test
    client = TestClient(app)
    response = client.get("/data")
    
    # 4. Verificamos que se usó el mock
    assert response.status_code == 200
    assert response.json()["token_used"] == "fake-mock-token"

    # 5. IMPORTANTE: Limpiar los overrides al terminar
    app.dependency_overrides = {}

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'dependency_overrides' es un diccionario: {Original: Sustituto}.
2. Te permite testear endpoints que requieren Login sin tener que crear 
   usuarios reales en cada test.
3. Te permite simular fallos de red o errores de DB de forma predecible.
4. Siempre limpia el diccionario al final del test para no afectar a otros 
   archivos de prueba.
"""
