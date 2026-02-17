"""
INYECCIÓN DE DEPENDENCIAS: CONCEPTOS BÁSICOS
-----------------------------------------------------------------------------
La inyección de dependencias (DI) permite que tus funciones reciban lo que 
necesitan para trabajar en lugar de tener que crearlo ellas mismas. 
En FastAPI, esto se logra con la función 'Depends'.
"""

from fastapi import FastAPI, Depends, Query
from typing import Annotated

app = FastAPI()

# 1. DEPENDENCIA BÁSICA (Lógica compartida)
# Supongamos que varios endpoints necesitan los mismos parámetros de búsqueda.
def common_parameters(
    q: str | None = None, 
    skip: int = 0, 
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(params: Annotated[dict, Depends(common_parameters)]):
    """
    FastAPI ejecuta 'common_parameters', recolecta los resultados y 
    los inyecta en 'params'.
    """
    return params

@app.get("/users/")
async def read_users(params: Annotated[dict, Depends(common_parameters)]):
    return params

# 2. DEPENDENCIAS COMO CLASES
# A veces es más limpio usar una clase para agruper lógica y estado.
class Paginator:
    def __init__(self, default_limit: int = 10):
        self.default_limit = default_limit

    def __call__(self, skip: int = 0, limit: int = 10):
        return {"skip": skip, "limit": min(limit, self.default_limit)}

# Instanciamos la clase con una configuración
my_paginator = Paginator(default_limit=50)

@app.get("/products/")
async def read_products(pagination: Annotated[dict, Depends(my_paginator)]):
    return pagination

"""
RESUMEN PARA EL DESARROLLADOR:
1. 'Depends' ayuda a cumplir el principio DRY (Don't Repeat Yourself).
2. Podrías cambiar la lógica de 'common_parameters' en un solo lugar y 
   afectaría a toda la API.
3. FastAPI detecta automáticamente sub-dependencias (Dependencias que dependen 
   de otras dependencias).
4. El uso de 'Annotated' es la recomendación oficial para mejor soporte de 
   editores y linters.
"""
