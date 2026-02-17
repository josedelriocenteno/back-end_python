"""
VALIDACIÓN: PYDANTIC BÁSICO
-----------------------------------------------------------------------------
Pydantic es el motor que permite a FastAPI validar que los datos que entran 
a tu API tienen la forma y el tipo correctos.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# 1. EL MODELO BASE
# Se define heredando de BaseModel. Cada atributo tiene un tipo de Python 3.10+
class UserBase(BaseModel):
    username: str
    email: EmailStr # Requiere 'pip install pydantic[email]'
    age: Optional[int] = None
    is_active: bool = True

# 2. METADATOS Y RESTRICCIONES (Field)
# 'Field' permite añadir validaciones extra que no se pueden expresar solo con tipos.
class Product(BaseModel):
    # ge: Greater than or Equal (>=)
    # lt: Less Than (<)
    name: str = Field(..., min_length=3, max_length=100, description="Nombre descriptivo")
    price: float = Field(..., ge=0, description="El precio no puede ser negativo")
    tags: List[str] = Field(default_factory=list)

# 3. USO MANUAL (Fuera de FastAPI)
def example_validation():
    # Caso 1: Datos válidos
    valid_data = {"name": "Laptop Pro", "price": 1200.50}
    product = Product(**valid_data)
    print(f"Producto validado: {product.name}")

    # Caso 2: Datos inválidos
    invalid_data = {"name": "Lo", "price": -10}
    try:
        Product(**invalid_data)
    except ValueError as e:
        print(f"Error detectado correctamente: {e}")

# 4. CONVERSIÓN A DICCIONARIO / JSON
def conversion_examples():
    p = Product(name="Teclado", price=45.0)
    # Convertir a dict
    print(p.model_dump()) 
    # Convertir a JSON string
    print(p.model_dump_json())

"""
RESUMEN PARA EL DESARROLLADOR:
1. Pydantic hace coercion (conversión) de tipos: si envías "42" y esperas int, lo convierte.
2. 'EmailStr' es mejor que 'str' porque valida el formato de correo automáticamente.
3. 'Field' es tu herramienta para añadir reglas de negocio (min/max).
4. 'description' en 'Field' aparecerá automáticamente en la documentación de Swagger.
"""

if __name__ == "__main__":
    example_validation()
