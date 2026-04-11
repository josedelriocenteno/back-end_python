"""
SEGURIDAD: PROTECCIÓN DE RUTAS POR ROLES
-----------------------------------------------------------------------------
Cómo implementar un sistema de permisos por roles de forma limpia y 
reutilizable en FastAPI.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Annotated
from enum import Enum

# 1. DEFINICIÓN DE ROLES
class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    USER = "user"

# 2. SIMULACIÓN DE USUARIO AUTENTICADO
# En un caso real, esto vendría de decodificar un JWT.
async def get_current_user():
    return {"id": 1, "username": "ana_dev", "role": UserRole.EDITOR}

# 3. EL GUARDIÁN DE ROLES (Role Checker)
class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[dict, Depends(get_current_user)]):
        """
        Esta función se ejecuta automáticamente cuando se usa en un Depends().
        """
        if user["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso insuficiente. Requiere uno de: {[r.value for r in self.allowed_roles]}"
            )
        return user

# 4. INSTANCIACIÓN DE DEPENDENCIAS
# Creamos objetos listos para ser inyectados en las rutas.
require_admin = RoleChecker([UserRole.ADMIN])
require_editor = RoleChecker([UserRole.ADMIN, UserRole.EDITOR])

app = FastAPI()

# 5. USO EN LAS RUTAS
@app.get("/config")
def get_config(admin: Annotated[dict, Depends(require_admin)]):
    """Solo los administradores pueden ver la configuración."""
    return {"config": "Super Secret"}

@app.post("/articles")
def create_article(editor: Annotated[dict, Depends(require_editor)]):
    """Admins y Editores pueden crear artículos."""
    return {"status": "Created by " + editor["username"]}

"""
RESUMEN PARA EL DESARROLLADOR:
1. Usar una clase como dependencia (__call__) permite una sintaxis muy limpia.
2. Si un usuario sin permiso llama a '/config', recibirá un 403 Forbidden 
   automáticamente antes de que se ejecute la lógica de la función.
3. Este patrón es totalmente compatible con tests unitarios permitiendo 
   'overrides' de los roles.
"""
