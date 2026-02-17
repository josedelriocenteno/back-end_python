"""
DISEÑO DE ENDPOINTS: FILTROS, ORDEN Y PAGINACIÓN
-----------------------------------------------------------------------------
Patrones para crear listados escalables que no matan a la base de datos.
"""

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 1. ESQUEMA DE PAGINACIÓN CIUDADANA
# Un patrón común es encapsular los parámetros de paginación en una clase.
class PaginationParams(BaseModel):
    offset: int = 0
    limit: int = 10

def get_pagination_params(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return {"skip": offset, "limit": limit}

# 2. ENDPOINT CON FILTROS Y PAGINACIÓN
@app.get("/logs/")
async def list_logs(
    level: Optional[str] = Query(None, pattern="^(INFO|ERROR|DEBUG)$"),
    search: Optional[str] = None,
    sort_by: str = "timestamp",
    order: str = Query("desc", pattern="^(asc|desc)$"),
    pagination: dict = Depends(get_pagination_params) # Dependencia para reutilizar
):
    """
    Ejemplo de endpoint robusto:
    - Valida niveles de log permitidos (Regex).
    - Valida orden ascendente o descendente.
    - Limita el máximo de registros por página a 100 para evitar abusos.
    """
    return {
        "filters": {"level": level, "search": search},
        "sorting": {"by": sort_by, "order": order},
        "pagination": pagination
    }

# 3. PAGINACIÓN CON METADATOS (Wrappers)
# En lugar de devolver una lista plana [], devolvvemos un objeto con info extra.
class PaginatedResponse(BaseModel):
    total: int
    count: int
    offset: int
    limit: int
    items: List[dict]

@app.get("/v2/items/", response_model=PaginatedResponse)
async def list_items_v2():
    return {
        "total": 1000,
        "count": 10,
        "offset": 0,
        "limit": 10,
        "items": [{"id": 1, "name": "Item 1"}]
    }

"""
RESUMEN PARA EL DESARROLLADOR:
1. Limita siempre el 'limit'. Jamás permitas traer 10,000 registros de golpe.
2. Usa 'Query' con regex o elipsis (...) para hacer los parámetros obligatorios.
3. El uso de 'Depends' para la paginación te permite tener una lógica única 
   para todos tus listados.
"""
