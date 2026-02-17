# Estructura de Proyecto Profesional (Production-Ready)

En proyectos reales, no ponemos todo el código en un solo archivo `main.py`. Necesitamos una estructura que permita escalar a cientos de endpoints y decenas de desarrolladores.

## 1. El Layout Estándar de la Industria

```text
mi_proyecto_backend/
├── alembic/                # Migraciones de base de datos
├── app/                    # Directorio principal de la app
│   ├── main.py             # Punto de entrada (Configuracion FastAPI)
│   ├── api/                # Capa de transporte (Routes)
│   │   ├── api_v1/         # Versionado de la API
│   │   │   ├── api.py      # Router central que une todos los módulos
│   │   │   └── endpoints/  # Archivos separados por recurso (users.py, items.py)
│   ├── core/               # Configuracion global, seguridad, variables de entorno
│   ├── db/                 # Sesion de base de datos y modelos SQLAlchemy
│   ├── crud/               # Lógica de operaciones a DB (Repositorios)
│   ├── models/             # Modelos de SQLAlchemy
│   ├── schemas/            # Schemas de Pydantic
│   └── services/           # Lógica de negocio compleja
├── tests/                  # Suite de pruebas Pytest
├── .env                    # Variables de entorno (NO se sube a Git)
├── .gitignore              # Archivos ignorados por Git
├── pyproject.toml          # Dependencias de Poetry
└── README.md               # Documentación inicial
```

## 2. Por qué esta estructura

*   **Modularidad:** Si necesitas cambiar algo en los usuarios, sabes que está en `app/api/api_v1/endpoints/users.py`.
*   **Versionado fácil:** Si lanzas la V2 de tu API, puedes crear la carpeta `api_v2` sin romper la `api_v1`.
*   **Desacoplamiento:** Los `schemas` (cómo se ven los datos al cliente) están separados de los `models` (cómo se ven en la DB).
*   **Inyección de Dependencias:** La configuración centralizada en `core/` y `db/` facilita inyectar la base de datos en cualquier endpoint.

## 3. El Router de FastAPI (`APIRouter`)

Usamos `APIRouter` para dividir las rutas en archivos lógicos.
```python
# app/api/api_v1/endpoints/users.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def get_users(): ...
```

Luego se importan todos en un router príncipe:
```python
# app/api/api_v1/api.py
api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["Users"])
```

## Resumen: Pensar en Grande

Incluso si tu proyecto hoy es pequeño, estructurarlo así desde el día 1 te ahorrará el "Refactor del Infierno" seis meses después. El orden en los archivos refleja el orden en el diseño de tu sistema.
