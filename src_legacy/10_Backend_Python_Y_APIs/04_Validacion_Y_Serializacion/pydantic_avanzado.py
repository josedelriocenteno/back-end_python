"""
VALIDACIÓN: PYDANTIC AVANZADO
-----------------------------------------------------------------------------
Validadores personalizados, dependencias entre campos y modelos anidados.
"""

from pydantic import BaseModel, field_validator, model_validator, Field
from typing import Optional
import re

class UserRegistration(BaseModel):
    username: str
    password: str
    password_confirm: str
    phone: Optional[str] = None

    # 1. FIELD VALIDATOR (Validador de campo individual)
    @field_validator("username")
    @classmethod
    def username_must_be_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("El nombre de usuario debe ser alfanumérico")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and not re.match(r"^\+?1?\d{9,15}$", v):
            raise ValueError("Formato de teléfono inválido")
        return v

    # 2. MODEL VALIDATOR (Validador de múltiples campos / lógica compleja)
    # Se ejecuta después de validar cada campo individual.
    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegistration":
        if self.password != self.password_confirm:
            raise ValueError("Las contraseñas no coinciden")
        return self

# 3. MODELOS ANIDADOS
# Ideal para representar estructuras jerárquicas como Facturas o Perfiles.
class Address(BaseModel):
    city: str
    country: str = "España"

class UserProfile(BaseModel):
    full_name: str
    address: Address # Un modelo dentro de otro

# 4. CONFIGURACIÓN DEL MODELO (ConfigDict)
class StrictModel(BaseModel):
    name: str
    age: int

    model_config = {
        "extra": "forbid",    # Lanza error si envían campos que no existen
        "str_strip_whitespace": True # Limpia espacios al inicio/final automáticamente
    }

"""
RESUMEN PARA EL DESARROLLADOR:
1. Use '@field_validator' para reglas que afecten solo a una columna.
2. Use '@model_validator' para reglas que comparen dos o más campos.
3. 'mode="after"' asegura que ya tienes los datos parseados y tipados en el validador.
4. 'model_config' te da control total sobre el comportamiento del modelo (extra fields, strict mode).
"""

if __name__ == "__main__":
    try:
        UserRegistration(username="user!!", password="123", password_confirm="456")
    except ValueError as e:
        print(f"Error complejo: {e}")
