"""
MANEJO DE ERRORES DE VALIDACIÓN
-----------------------------------------------------------------------------
FastAPI lanza un error 422 (Unprocessable Entity) por defecto. Aprende a 
personalizarlo para que el frontend sepa exactamente qué corregir.
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

# 1. CUSTOMIZANDO EL HANDLER GLOBAL
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Transforma el error denso de Pydantic en una respuesta amigable para el frontend.
    """
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Datos inválidos", "details": errors}
    )

class Product(BaseModel):
    name: str = Field(..., min_length=5)
    price: float = Field(..., gt=0)

@app.post("/products/")
async def create_product(product: Product):
    return product

"""
ESTRUCTURA DE RESPUESTA CUSTOM:
-----------------------------------------------------------------------------
Si envías {"name": "X", "price": -5}, recibirás:
{
  "error": "Datos inválidos",
  "details": [
    {"field": "name", "message": "ensure this value has at least 5 characters", "type": "value_error.any_str.min_length"},
    {"field": "price", "message": "ensure this value is greater than 0", "type": "value_error.number.not_gt"}
  ]
}
"""

"""
RESUMEN PARA EL DESARROLLADOR:
1. El frontend odia los errores 500 genéricos. Ayúdales con detalles 422 claros.
2. Pydantic te da la localización exacta del error (campo anidado, tipo de error).
3. Centraliza tus handlers de excepción para que toda tu API tenga errores consistentes.
"""
