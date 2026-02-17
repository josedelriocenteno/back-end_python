"""
FASTAPI: VALIDACIÓN PROFESIONAL DE RESPUESTAS
-----------------------------------------------------------------------------
No te limites a 'assert response.status_code == 200'. Comprueba que el 
JSON devuelto sigue la estructura correcta (Schema).
"""

import pytest
from pydantic import BaseModel, ValidationError

# 1. EL ESQUEMA QUE ESPERAMOS (Nuestro contrato)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

def test_endpoint_respeta_el_schema(client):
    response = client.get("/users/1")
    data = response.json()
    
    # ACT: Intentamos instanciar el modelo con los datos recibidos
    try:
        UserResponse(**data)
        # Si llega aquí, es que el JSON tiene todos los campos y tipos correctos
    except ValidationError as e:
        pytest.fail(f"La respuesta de la API no cumple con el Schema: {e}")

# 2. TEST DE LISTAS (PAGINACIÓN)
def test_listado_usuarios_tiene_formato_correcto(client):
    response = client.get("/users?page=1")
    json_data = response.json()
    
    assert "items" in json_data
    assert "total" in json_data
    assert isinstance(json_data["items"], list)
    
    if json_data["items"]:
        # Validamos el primer elemento de la lista
        UserResponse(**json_data["items"][0])

"""
¿POR QUÉ VALIDAR CONTRA EL MODELO?
----------------------------------
Si alguien cambia el nombre de un campo en el backend de 'username' a 
'user_name', pero se olvida de actualizar el test, un assert simple 
podría seguir pasando, pero tu frontend se rompería. Validar contra el 
esquema asegura que el 'Contrato' entre backend y frontend es sagrado.
"""
