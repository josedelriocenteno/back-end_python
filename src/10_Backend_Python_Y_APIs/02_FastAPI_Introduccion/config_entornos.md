# Gestión de Entornos y Configuración Segura

"Jamás pongas datos sensibles en el código". Esta es la regla número 1 de la seguridad backend. En FastAPI, usamos Pydantic para gestionar la configuración de forma limpia y tipada.

## 1. Variables de Entorno (.env)
Crea un archivo `.env` para tus secretos:
```text
PROJECT_NAME="Mi API de Producción"
DATABASE_URL="postgresql://user:secret@localhost:5432/db"
JWT_SECRET="mi_clave_secreta_super_larga"
DEBUG=True
```

## 2. Settings con Pydantic (BaseSettings)
Esta es la forma más profesional de leer configuraciones. Pydantic validará que las variables existan y tengan el tipo correcto.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Pydantic carga automáticamente desde el entorno o archivo .env
    PROJECT_NAME: str = "FastAPI App"
    DATABASE_URL: str
    JWT_SECRET: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"

# Instancia global para usar en toda la app
settings = Settings()
```

## 3. Diferenciando Entornos (Dev vs Prod)
Puedes tener múltiples archivos ( `.env.development`, `.env.production`) y cargar el correcto dependiendo de una variable de sistema `ENV`.

```python
import os
env_file = f".env.{os.getenv('ENV', 'development')}"
settings = Settings(_env_file=env_file)
```

## 4. El Objeto `app.state`
A veces queremos guardar configuraciones dentro de la instancia de la app para que estén disponibles en todas partes:
```python
app = FastAPI()
app.state.settings = settings
```

## 5. Inyección en Endpoints
FastAPI permite inyectar la configuración en las rutas usando `Depends`:
```python
@app.get("/info")
def get_info(config: Settings = Depends(get_settings)):
    return {"app_name": config.PROJECT_NAME}
```

## Resumen: Configuración Inmutable y Segura
Al usar Pydantic Settings, conviertes tus variables de entorno en objetos de Python tipados. Esto evita errores de "Variable no encontrada" en tiempo de ejecución y mejora drásticamente la seguridad de tu sistema.
