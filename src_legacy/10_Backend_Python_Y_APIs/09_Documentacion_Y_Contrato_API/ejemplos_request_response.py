"""
DOCUMENTACIÓN: EJEMPLOS DE REQUEST Y RESPONSE
-----------------------------------------------------------------------------
Añadir ejemplos reales en la documentación hace que la vida de los 
desarrolladores frontend sea mucho más fácil.
"""

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

# 1. EJEMPLO EN EL MODELO (Schema)
class User(BaseModel):
    username: str = Field(..., examples=["jdoe_88"])
    full_name: str = Field(..., examples=["John Doe"])
    age: int = Field(..., examples=[35])

    # Configuración extra para el schema de OpenAPI
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "tester_pro",
                    "full_name": "Test User",
                    "age": 25
                }
            ]
        }
    }

# 2. EJEMPLOS MÚLTIPLES EN EL BODY
@app.post("/items/")
async def create_item(
    payload: dict = Body(
        ...,
        examples=[
            {
                "summary": "Un ejemplo básico",
                "description": "Lo que normalmente enviaría un usuario normal.",
                "value": {"name": "Lápiz", "qty": 10}
            },
            {
                "summary": "Un ejemplo corporativo",
                "description": "Pedido masivo de oficina.",
                "value": {"name": "Caja de folios", "qty": 500}
            }
        ]
    )
):
    return payload

# 3. DOCUMENTANDO RESPUESTAS MÚLTIPLES
@app.get("/users/{id}", responses={
    200: {"description": "Usuario encontrado", "content": {"application/json": {"example": {"id": 1, "name": "John"}}}},
    404: {"description": "El usuario no existe", "content": {"application/json": {"example": {"detail": "User not found"}}}}
})
def get_user(id: int):
    return {"id": id}

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'examples' en 'Field' sirve para campos individuales.
2. 'json_schema_extra' sirve para documentar el objeto completo.
3. Los ejemplos aparecen en Swagger y ayudan a generar clientes automáticos 
   con herramientas como 'openapi-generator'.
"""
