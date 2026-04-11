"""
SEGURIDAD: IMPLEMENTACIÓN DE JWT EN FASTAPI
-----------------------------------------------------------------------------
JSON Web Tokens (JWT) permiten una autenticación segura y escalable sin 
necesidad de estado en el servidor.
"""

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt # pip install python-jose[cryptography]
from passlib.context import CryptContext # pip install passlib[bcrypt]
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# 1. CONFIGURACIÓN (Debería ir en .env)
SECRET_KEY = "mi-clave-super-secreta-que-nadie-conoce"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hashear contraseñas (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Definimos dónde buscar el token (en la URL /token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 2. UTILIDADES DE SEGURIDAD
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 3. DEPENDENCIA PARA OBTENER EL USUARIO ACTUAL
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificamos el token con nuestra clave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Aquí buscaríamos el usuario en la DB real
    return {"username": username, "active": True}

"""
RESUMEN PARA EL DESARROLLADOR:
1. Nunca guardes contraseñas en plano. Usa Bcrypt (passlib).
2. El 'sub' (Subject) del JWT suele ser el ID o email del usuario.
3. El JWT es público (ba64 decode), lo que es SECRETO es la firma. Jamás 
   pongas datos sensibles (como el password) DENTRO del JWT.
4. 'OAuth2PasswordBearer' hace que Swagger muestre el botón de 'Authorize' 
   automáticamente.
"""
