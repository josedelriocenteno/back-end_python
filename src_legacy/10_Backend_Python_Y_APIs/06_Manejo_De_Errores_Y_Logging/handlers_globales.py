"""
ERRORES: HANDLERS GLOBALES (MAPPING)
-----------------------------------------------------------------------------
Permite capturar excepciones de Python normales (de tu lógica de negocio) 
y transformarlas en respuestas HTTP automáticas en un solo lugar.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

# Importamos la excepción de negocio del archivo anterior (simulado)
class InsufficientFundsException(Exception):
    def __init__(self, amount: float):
        self.amount = amount

app = FastAPI()

# 1. EL HANDLER GLOBAL
@app.exception_handler(InsufficientFundsException)
async def insufficient_funds_handler(request: Request, exc: InsufficientFundsException):
    """
    Cada vez que en CUALQUIER lugar del código se lance 'InsufficientFundsException',
    esta función se activará y enviará un 400 al cliente.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": "BANK_001",
            "message": f"Fondos insuficientes para la operación de {exc.amount}€",
            "support_url": "https://banco.com/soporte"
        }
    )

# 2. CAPTURAR ERRORES NO CONTROLADOS (EL 'CATCH-ALL')
@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    """
    Captura errores inesperados (bugs, DB down, etc) para que no 
    se envíe un 'Internal Server Error' feo al cliente.
    """
    # Aquí deberías loguear el error real para los desarrolladores
    print(f"CRITICAL ERROR: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={"message": "Ha ocurrido un error inesperado en el servidor. Inténtelo más tarde."}
    )

@app.get("/test-error")
def test_handler():
    raise InsufficientFundsException(amount=500.0)

"""
RESUMEN PARA EL DESARROLLADOR:
1. Los handlers globales mantienen tus servicios limpios de lógica HTTP.
2. Tus servicios lanzan excepciones de Python; tu API las mapea a códigos HTTP.
3. Esto es el patrón 'Error Mapping' y es fundamental para desacoplar el nucleo 
   de la aplicación de la interfaz web.
"""
