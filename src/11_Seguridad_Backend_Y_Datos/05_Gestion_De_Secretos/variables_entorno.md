# Variables de Entorno: El estándar de 12-Factor App

La forma más básica y aceptada de inyectar secretos en una aplicación es mediante las **Variables de Entorno (Environment Variables)**. Este enfoque sigue el manifiesto [12-Factor App](https://12factor.net/config).

## 1. ¿Por qué usar variables de entorno?
- **Separación de Código y Configuración:** El mismo código corre en local, staging y producción sin cambios; solo cambian las variables que recibe.
- **Evita el Hardcoding:** No hay contraseñas escritas en el código Python.
- **Compatibilidad Universal:** Todos los sistemas operativos y plataformas de la nube soportan variables de entorno nativamente.

## 2. El archivo `.env` (Solo para Desarrollo)
En local, usamos un archivo `.env` para no tener que configurar variables manualmente cada vez.
```env
# .env file
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=abc-123-xyz
DEBUG=True
```
**CRÍTICO:** Este archivo NUNCA debe subirse a Git. Usa `.env.example` con valores vacíos como plantilla para otros desarrolladores.

## 3. Uso en Python con `python-dotenv`
```python
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables del archivo .env a os.environ

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL no está configurada")
```

## 4. Mejor aún: Pydantic Settings
Para proyectos profesionales, usa Pydantic para validar que las variables existen y tienen el formato correcto.
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
print(settings.database_url) # Acceso tipado y validado
```

## 5. El peligro de 'print(os.environ)'
Nunca imprimas todas las variables de entorno en los logs o en una página de error, ya que estarías exponiendo todos los secretos del sistema.

## Resumen: La base de la portabilidad
Las variables de entorno son la forma más sencilla de pasar de "mi ordenador" a "el servidor" de forma segura. Dominar `BaseSettings` de Pydantic te dará un nivel de robustez extra al detectar fallos de configuración en el mismo instante en que arranca la aplicación.
