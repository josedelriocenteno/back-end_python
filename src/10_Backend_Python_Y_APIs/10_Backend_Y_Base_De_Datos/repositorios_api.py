"""
BACKEND + DB: PATRÓN REPOSITORIO EN LA API
-----------------------------------------------------------------------------
Cómo separar la lógica de persistencia para que tus controladores no 
dependan directamente de SQLAlchemy.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db_dependency import get_db

# 1. EL REPOSITORIO (Capa de datos)
class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def list_all(self, skip: int, limit: int):
        return self.db.query(Product).offset(skip).limit(limit).all()

    def create(self, product_data: dict):
        db_product = Product(**product_data)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

# 2. DEPENDENCIA DEL REPOSITORIO
def get_product_repo(db: Session = Depends(get_db)):
    return ProductRepository(db)

app = FastAPI()

# 3. USO EN EL ROUTER (Controlador)
@app.get("/products/{id}")
def get_product(id: int, repo: ProductRepository = Depends(get_product_repo)):
    """
    ¡MIRA QUÉ LIMPIO! El controlador no tiene ni una sola línea de SQL 
    ni de SQLAlchemy. Solo llama a métodos del repositorio.
    """
    product = repo.get_by_id(id)
    if not product:
        raise HTTPException(status_code=404)
    return product

"""
POR QUÉ USAR ESTO EN LUGAR DE DB.QUERY DIRECTO:
-----------------------------------------------------------------------------
1. DRY: Si necesitas buscar un producto en 3 endpoints diferentes, la lógica 
   está en un solo sitio.
2. Testabilidad: Puedes "mentirle" al controlador inyectando un 
   'MockProductRepository' que no use internet ni DB.
3. Velocidad de cambio: Si mañana migras tus productos a una base de datos 
   NoSQL o una API externa, solo cambias el repositorio. El controlador no 
   se entera.
"""
