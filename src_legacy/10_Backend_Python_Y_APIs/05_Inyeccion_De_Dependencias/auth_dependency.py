"""
INYECCIÓN DE DEPENDENCIAS: SEGURIDAD (AUTH)
-----------------------------------------------------------------------------
Protegiendo rutas de forma declarativa inyectando el usuario autenticado.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Header
from typing import Optional

app = FastAPI()

# 1. DEPENDENCIA DE AUTENTICACIÓN
def get_current_user(x_token: str = Header(...)):
    """
    Dependencia que valida un Token en el Header 'X-Token'.
    """
    if x_token != "super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o ausente"
        )
    # Imaginemos que buscamos en DB y devolvemos un objeto de usuario
    return {"id": 1, "username": "admin", "role": "admin"}

# 2. DEPENDENCIA DE AUTORIZACIÓN (Roles)
def get_admin_user(current_user: dict = Depends(get_current_user)):
    """
    Dependencia que depende de otra: requiere autenticación y verifica el rol.
    """
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user

# 3. USANDO LAS DEPENDENCIAS EN RUTAS
@app.get("/me")
def read_current_user(user: dict = Depends(get_current_user)):
    return user

@app.delete("/system-reset")
def reset_system(admin: dict = Depends(get_admin_user)):
    return {"message": "System reset by admin"}

"""
RESUMEN PARA EL DESARROLLADOR:
1. Las dependencias pueden encadenarse: A -> B -> C.
2. Si una dependencia lanza una excepción (como 401), el endpoint nunca 
   llega a ejecutarse.
3. Es la forma más potente de FastAPI para manejar seguridad sin ensuciar 
   la lógica del controlador.
"""
