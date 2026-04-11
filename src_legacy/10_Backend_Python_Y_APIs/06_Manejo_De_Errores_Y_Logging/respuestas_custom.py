"""
ERRORES: RESPUESTAS CUSTOM Y CONSISTENCIA
-----------------------------------------------------------------------------
Cómo asegurar que todos los errores de tu API tengan la misma forma 
estandarizada para facilitar el trabajo del frontend.
"""

from pydantic import BaseModel
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

# 1. EL MODELO DE ERROR ESTÁNDAR
class APIError(BaseModel):
    status: str = "error"
    code: str
    message: str
    details: dict | None = None

app = FastAPI()

def api_error_response(code: str, message: str, status_code: int, details: dict = None):
    """
    Helper para generar respuestas de error consistentes.
    """
    error = APIError(code=code, message=message, details=details)
    return JSONResponse(
        status_code=status_code,
        content=error.model_dump()
    )

@app.get("/users/{id}")
def get_user(id: int):
    if id == 999:
        return api_error_response(
            code="USER_NOT_FOUND",
            message=f"No existe un usuario con el identificador {id}",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"requested_id": id}
        )
    return {"id": id, "name": "Test"}

"""
RECOMENDACIÓN PARA EL DESARROLLADOR:
-----------------------------------------------------------------------------
Adopta el estándar JSON:API o simplemente crea uno propio pero SÍGUELO 
en todos los módulos. Una API profesional es predecible. Si yo sé que 
tus errores siempre tienen un campo 'code' que puedo traducir, mi código 
frontend será mucho más robusto.
"""

"""
RESUMEN:
1. Crea un wrapper para tus errores.
2. Usa códigos de error internos (strings como 'AUTH_EXPIRED') además del código HTTP.
3. Los metadatos extra en 'details' son oro para el debugging en el frontend.
"""
