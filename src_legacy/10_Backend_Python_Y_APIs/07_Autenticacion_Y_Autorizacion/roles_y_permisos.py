"""
SEGURIDAD: ROLES Y PERMISOS (RBAC)
-----------------------------------------------------------------------------
Cómo implementar un sistema de permisos basado en roles de forma elegante 
usando dependencias de FastAPI.
"""

from fastapi import Depends, HTTPException, status
from enum import Enum
from typing import List

# 1. DEFINICIÓN DE ROLES
class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    USER = "user"

# 2. CLASE DE DEPENDENCIA DE ROLES
class RoleChecker:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Depends(get_current_user)): # Dependencia de JWT
        """
        Este método se ejecuta cuando se usa la clase en un Depends().
        """
        user_role = user.get("role")
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado. Se requiere uno de los roles: {[r.value for r in self.allowed_roles]}"
            )
        return user

# 3. INSTANCIACIÓN DE LOS GUARDIAS
# Creamos objetos reutilizables para nuestras rutas
allow_admin = RoleChecker([Role.ADMIN])
allow_staff = RoleChecker([Role.ADMIN, Role.EDITOR])

app = FastAPI()

# 4. USO EN LOS ENDPOINTS
@app.get("/admin-dashboard")
def get_dashboard(admin: dict = Depends(allow_admin)):
    """Solo admins pueden entrar."""
    return {"message": "Bienvenido, Administrador"}

@app.post("/articles")
def create_article(editor: dict = Depends(allow_staff)):
    """Admins y Editores pueden crear artículos."""
    return {"message": "Artículo creado"}

"""
RESUMEN PARA EL DESARROLLADOR:
1. El uso de Clases como dependencias ('RoleChecker') permite configurar la 
   lógica una sola vez y reutilizarla en muchas rutas.
2. Si las reglas cambian (ej: ahora los usuarios pro también pueden entrar), 
   solo cambias la lista de roles en la definición de la ruta.
3. Para sistemas ultra-grandes, considera cargar los permisos desde la DB 
   dinámicamente en lugar de hardcodearlos en decoradores.
"""
