"""
FASTAPI: TESTING CON AUTENTICACIÓN
-----------------------------------------------------------------------------
Cómo probar rutas protegidas simulando que el usuario ya está logueado.
"""

import pytest
from fastapi.testclient import TestClient
from .test_fastapi import app # Reusamos la app anterior

# 1. SIMULACIÓN DE HEADERS
def test_ruta_protegida_falla_sin_token(client):
    # Imagina que /config requiere token
    response = client.get("/config")
    # Si no enviamos nada, debería ser 401
    assert response.status_code == 401

def test_ruta_protegida_pasa_con_token_fake(client):
    """
    Simulamos que el cliente ya tiene un token JWT.
    """
    headers = {"Authorization": "Bearer token-secreto-de-test"}
    
    # ACT: Pasamos los headers en la petición
    response = client.get("/config", headers=headers)
    
    # Aquí ya dependerá de cómo gestiones el token en el backend
    assert response.status_code == 200

# 2. DEPENDENCY OVERRIDES (El nivel PRO)
from .dependencias import get_current_user

def test_override_de_usuario_para_roles(client):
    """
    Sustituimos la función de obtener el usuario por una que siempre 
    devuelva un ADMIN, sin importar el token real.
    """
    def mock_admin_user():
        return {"id": 1, "role": "admin"}
    
    # Inyectamos el mock SOLO para este test
    app.dependency_overrides[get_current_user] = mock_admin_user
    
    response = client.get("/admin-panel")
    assert response.status_code == 200
    
    # IMPORTANTE: Limpiar el override después del test
    app.dependency_overrides = {}

"""
RECOMENDACIÓN SENIOR:
---------------------
Crea fixtures como 'admin_client' o 'user_client' que ya vengan con los 
headers o los overrides pre-configurados. Esto hará que tus tests sean 
leibles: 'def test_delete_user(admin_client): ...'
"""
