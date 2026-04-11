"""
DISEÑO DE ENDPOINTS: RUTAS Y PARÁMETROS
-----------------------------------------------------------------------------
Cómo recibir información del cliente de forma estructurada y tipada.
"""

from fastapi import FastAPI, Path, Query, Body
from typing import Annotated, Optional

app = FastAPI()

# 1. PATH PARAMETERS (Parámetros de Ruta)
# Se usan para identificar un recurso específico.
@app.get("/users/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(title="El ID del usuario a recuperar", ge=1)]
):
    return {"user_id": user_id}

# 2. QUERY PARAMETERS (Parámetros de Consulta)
# Se usan para filtrar, ordenar o paginar. Son opcionales por defecto.
@app.get("/products/")
async def search_products(
    q: Annotated[Optional[str], Query(max_length=50)] = None,
    price_min: float = 0.0,
    price_max: float = 1000.0,
    sort: str = "price_asc"
):
    return {"query": q, "filters": [price_min, price_max], "sort": sort}

# 3. REQUEST BODY (Cuerpo de la Petición)
# Datos complejos (JSON) enviados en el cuerpo.
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float

@app.post("/products/")
async def create_product(product: Product):
    return product

# 4. PARÁMETROS MIXTOS
# Puedes combinar todos en un solo endpoint.
@app.put("/users/{user_id}/items/{item_id}")
async def update_user_item(
    user_id: int, 
    item_id: int, 
    active: bool = True, # Query param
    note: str = Body(...) # Obligamos a que 'note' venga en el JSON del body
):
    return {"u": user_id, "i": item_id, "active": active, "note": note}

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'Path': obligatorio, identifica el "quién".
2. 'Query': opcional, define el "cómo" (filtros).
3. 'Body': datos complejos para crear o modificar.
4. 'Annotated': Forma moderna de añadir validación extra (min_length, regex, etc) 
   sin ensuciar la firma de la función.
"""
