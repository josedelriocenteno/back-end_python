"""
ERRORES: EXCEPCIONES HTTP EN FASTAPI
-----------------------------------------------------------------------------
Cómo romper el flujo de ejecución para informar al cliente de que algo ha 
ido mal de forma controlada.
"""

from fastapi import FastAPI, HTTPException, status

app = FastAPI()

# 1. USO BÁSICO DE HTTPException
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # Condición de error común: recurso no encontrado
    if item_id == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item no encontrado"
        )
    return {"item_id": item_id}

# 2. AÑADIENDO HEADERS A LA EXCEPCIÓN
# Muy útil en seguridad (ej: indicar cómo autenticarse).
@app.get("/secret")
async def read_secret(authorized: bool = False):
    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tienes permiso para ver el secreto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"secret": "The cake is a lie"}

# 3. EXCEPCIONES PERSONALIZADAS (DENTRO DEL SERVICIO)
# Es una buena práctica crear tus propias excepciones de negocio.
class InsufficientFundsException(Exception):
    def __init__(self, amount: float):
        self.amount = amount

@app.post("/transfer")
def make_transfer(amount: float):
    if amount > 100:
        # Lanzamos una excepción de Python pura, no de FastAPI aún
        raise InsufficientFundsException(amount)
    return {"message": "Transferencia exitosa"}

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'raise HTTPException' detiene inmediatamente la ejecución de la función.
2. Usa 'status.HTTP_...' en lugar de números a fuego (404) por legibilidad.
3. No pongas demasiada información técnica en el 'detail' para evitar fugas 
   de información (Information Disclosure).
4. El cliente recibirá un JSON con la clave 'detail' por defecto.
"""
