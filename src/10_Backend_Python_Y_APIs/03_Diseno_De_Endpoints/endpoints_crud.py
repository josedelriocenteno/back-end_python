"""
DISEÑO DE ENDPOINTS: PATRÓN CRUD PROFESIONAL
-----------------------------------------------------------------------------
Un CRUD profesional no solo mueve datos; maneja códigos de estado correctos 
y validaciones de recursos.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Mock de base de datos para el ejemplo
DB = {}

# 1. ESQUEMAS (Pydantic)
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

# 2. ENDPOINTS
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """
    POST: Crea un recurso. Devuelve 201 Created.
    """
    new_id = len(DB) + 1
    new_item = Item(id=new_id, **item.model_dump())
    DB[new_id] = new_item
    return new_item

@app.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    """
    GET (Coleccion): Lista recursos con paginacion basica.
    """
    return list(DB.values())[skip : skip + limit]

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """
    GET (Unico): Detalle de un recurso. 404 si no existe.
    """
    if item_id not in DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item no encontrado"
        )
    return DB[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    """
    PUT: Reemplazo total del recurso.
    """
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item no existe")
    
    updated_item = Item(id=item_id, **item.model_dump())
    DB[item_id] = updated_item
    return updated_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    DELETE: Elimina el recurso. Devuelve 204 No Content.
    """
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item no existe")
    del DB[item_id]
    return None

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'status_code' en el decorador define el éxito predeterminado.
2. 'response_model' asegura que el cliente solo reciba lo que definiste.
3. 'HTTPException' es la forma de romper el flujo y devolver un error al cliente.
4. Usa '204 No Content' para deletes exitosos; es el estándar de la industria.
"""
