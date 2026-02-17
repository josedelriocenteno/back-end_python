"""
SEGURIDAD: IMPLEMENTACIÓN AVANZADA DE JWT (ROTACIÓN)
-----------------------------------------------------------------------------
Cómo implementar un sistema de tokens en FastAPI que rote los tokens de 
refresco para máxima seguridad.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import uuid

# 1. SECRETOS Y TIEMPOS (Usa siempre .env)
SECRET_KEY = "clave-maestra-super-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 15
REFRESH_TOKEN_DAYS = 7

app = FastAPI()

# 2. GENERADOR DE TOKENS
def create_tokens(user_id: str):
    """
    Genera el par de tokens (Access y Refresh) con IDs únicos (jti).
    """
    now = datetime.now(timezone.utc)
    
    # Payload Access
    access_payload = {
        "sub": user_id,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_MINUTES),
        "type": "access",
        "jti": str(uuid.uuid4())
    }
    
    # Payload Refresh
    refresh_payload = {
        "sub": user_id,
        "exp": now + timedelta(days=REFRESH_TOKEN_DAYS),
        "type": "refresh",
        "jti": str(uuid.uuid4())
    }
    
    return {
        "access_token": jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM),
        "refresh_token": jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)
    }

# 3. ENDPOINT DE REFRESCO CON ROTACIÓN
@app.post("/auth/refresh")
async def refresh_access_token(old_refresh_token: str):
    """
    Valida el token viejo y entrega un par NUEVO (Rotación).
    Si alguien robó el viejo y lo intenta usar después de esta rotación, 
    podremos detectar la brecha de seguridad.
    """
    try:
        payload = jwt.decode(old_refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Tipo de token inválido")
        
        user_id = payload.get("sub")
        # Aquí deberías verificar en DB si el 'jti' ya fue usado o revocado
        
        # Generamos un par totalmente nuevo
        return create_tokens(user_id)
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token de refresco inválido o expirado")

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'sub' es el sujeto (quién es el usuario).
2. 'jti' permite rastrear y anular este token específico si fuera necesario.
3. La rotación de los tokens de refresco asegura que si alguien los intercepta, 
   solo le servirán una vez.
"""
